#!/usr/bin/env python3
"""Sample fresh English YouTube uploads from the last 24 hours.

Strategy: fan out many neutral common-word searches sorted by upload date
("uploaded today" filter), dedupe by video ID, then filter out music, gaming,
kids content, spam/adverts, TV/film clips, politics, shorts, and low-res videos.
Output: a shuffled list of links + an HTML index you can open locally.

Usage:
    python3 fresh_tube.py [--words 25] [--keep 60] [--hours 24]
"""

import argparse
import html
import json
import random
import re
import sys
import time
import urllib.parse
from pathlib import Path

import yt_dlp

# Neutral high-frequency English words used as discovery queries.
SEED_WORDS = [
    "the", "how", "why", "what", "this", "that", "with", "when", "where",
    "which", "your", "about", "make", "just", "like", "into", "over",
    "after", "first", "best", "more", "very", "much", "some", "them",
    "other", "would", "could", "should", "think", "know", "people",
    "because", "through", "between", "around", "again", "still", "even",
    "back", "home", "work", "life", "time", "world", "day", "story",
]

# YouTube sp filter: type=video, upload date = today, sort by upload date.
# ("CAISAggD" sorts by date with the last-24h window; the sp token encodes
# sort=upload date + filter uploaded-today; results beyond 24h are rare.)
SP_TODAY_SORT_DATE = "CAISAggD"

# sp with a 1-hour window is not available via a single token; we rely on
# publishedAt checks post-fetch to enforce the exact window.

BANNED_TITLE = re.compile(
    r"""
    \b(
    official\s+video | music\s+video | feat\.? | \bft\.?\b |
    lyrics?\s*(video)? | full\s+album | cover\s+(song|video) |
    episode\s*\d+ | s\d+\s?e\d+ | full\s+episode | highlights? |
    trailer\b | official\s+trailer | full\s+match |
    gameplay | walkthrough | minecraft | fortnite | roblox |
    gaming | lets\s?play | speedrun |
    kids? | cartoons? | nursery | rhymes? | for\s+babies |
    news\s+today | breaking\s+news | election | trump | biden |
    politics | liberal | conservative | president\s+says |
    movie | film\s+20\d\d | full\s+movie | watch\s+free |
    episode\s+full | tv\s+show | series\s+finale |
    crypto | forex | trading\s+signals | make\s+money\s+fast |
    giveaway | subscribe\s+now | shorts?\b | \#shorts
    )\b
    """,
    re.IGNORECASE | re.VERBOSE,
)

BANNED_CHANNEL = re.compile(
    r"""
    (
    -\s*topic$ | vevo$ | music$ | tv$ | news$ | gaming$ |
    kids$ | cartoon$ | official\s+channel$ | espn | bbc | cnn | msnbc |
    fox\s?news | abc\s?news | nbc | cbs | netflix | marvel |
    wwe | ufc | nba | nfl | fifa | premier\s?league
    )
    $""",
    re.IGNORECASE | re.VERBOSE,
)


def log(msg):
    print(msg, file=sys.stderr, flush=True)


def search_word(ydl, word, max_results=100):
    """Return flat search entries for one word, sorted by upload date today."""
    q = urllib.parse.urlencode({"search_query": word, "sp": SP_TODAY_SORT_DATE})
    url = f"https://www.youtube.com/results?{q}"
    try:
        info = ydl.extract_info(url, download=False, process=False)
        entries = list(info.get("entries") or [])
        return entries[:max_results]
    except Exception as e:
        log(f"  ! search '{word}' failed: {type(e).__name__}: {e}")
        return []


def passes_flat_filters(e, cutoff_ts):
    """Cheap filters using only search-result metadata."""
    title = e.get("title") or ""
    channel = e.get("channel") or e.get("uploader") or ""
    dur = e.get("duration")
    if e.get("timestamp") and e["timestamp"] < cutoff_ts:
        return False, "old"
    if dur is not None and (dur <= 62 or dur >= 6 * 3600):
        return False, "short/too-long"
    if BANNED_TITLE.search(title):
        return False, "banned-title"
    if BANNED_CHANNEL.search(channel.strip()):
        return False, "banned-channel"
    if not re.search(r"[a-z]", title):  # no latin letters -> not English-adjacent
        return False, "no-latin"
    return True, ""


def passes_deep_filters(v, min_height=480):
    """Filters needing a full video lookup."""
    if not v:
        return False, "no-info"
    lang = (v.get("language") or "").lower()
    audio_langs = [l.lower() for l in (v.get("audio_languages") or [])]
    height = v.get("height") or 0
    if v.get("duration") is not None and v["duration"] <= 62:
        return False, "short"
    if height and height < min_height:
        return False, f"low-res({height}p)"
    if lang and not lang.startswith("en") and "en" not in audio_langs:
        return False, f"lang({lang or 'none'})"
    return True, ""


def collect(cutoff_ts, words, per_word):
    opts = {
        "quiet": True,
        "no_warnings": True,
        "skip_download": True,
        "extract_flat": True,
        "socket_timeout": 20,
        "retries": 2,
        "sleep_interval_requests": 0.4,
    }
    seen = {}
    with yt_dlp.YoutubeDL(opts) as ydl:
        for w in words:
            entries = search_word(ydl, w, per_word)
            log(f"  '{w}': {len(entries)} results")
            for e in entries:
                vid = e.get("id")
                if not vid or vid in seen:
                    continue
                ok, _ = passes_flat_filters(e, cutoff_ts)
                seen[vid] = (e, ok)
            time.sleep(0.3)
    return seen


def enrich(candidates, batch_size=8):
    """Full metadata for surviving candidates to apply deep filters."""
    opts = {
        "quiet": True,
        "no_warnings": True,
        "skip_download": True,
        "socket_timeout": 20,
        "retries": 1,
        "extract_flat": False,
        "sleep_interval_requests": 0.3,
    }
    passed = []
    with yt_dlp.YoutubeDL(opts) as ydl:
        for i in range(0, len(candidates), batch_size):
            batch = candidates[i : i + batch_size]
            for e in batch:
                vid = e["id"]
                try:
                    v = ydl.extract_info(
                        f"https://www.youtube.com/watch?v={vid}",
                        download=False,
                        process=False,
                    )
                    ok, reason = passes_deep_filters(v)
                except Exception:
                    ok, reason = False, "error"
                if ok:
                    passed.append((e, v))
                else:
                    log(f"    - {vid} {reason}")
            time.sleep(0.2)
    return passed


def duration_str(sec):
    sec = int(sec or 0)
    h, rem = divmod(sec, 3600)
    m, s = divmod(rem, 60)
    return f"{h}:{m:02d}:{s:02d}" if h else f"{m}:{s:02d}"


def write_outputs(passed, outdir):
    outdir.mkdir(parents=True, exist_ok=True)
    random.shuffle(passed)
    links = [
        f"https://www.youtube.com/watch?v={e['id']}" for e, _ in passed
    ]
    (outdir / "links.txt").write_text("\n".join(links) + "\n")

    rows = []
    for e, v in passed:
        title = html.escape(e.get("title") or "")
        chan = html.escape(e.get("channel") or e.get("uploader") or "")
        vid = e["id"]
        dur = duration_str(v.get("duration") or e.get("duration"))
        height = v.get("height") or "?"
        thumb = e.get("thumbnails")
        img = ""
        if thumb:
            best = max(thumb, key=lambda t: t.get("height") or 0)
            img = best.get("url", "")
        rows.append(
            f'<div style="width:320px;display:inline-block;vertical-align:top;'
            f'margin:8px;font-family:sans-serif">'
            f'<a href="https://www.youtube.com/watch?v={vid}">'
            f'<img src="{html.escape(img)}" style="width:320px"></a>'
            f'<b><a style="color:inherit;text-decoration:none" '
            f'href="https://www.youtube.com/watch?v={vid}">{title}</a></b><br>'
            f'<small>{chan} &middot; {dur} &middot; {height}p</small></div>'
        )
    doc = (
        "<!doctype html><meta charset=utf-8><title>Fresh uploads</title>"
        f"<h2>Fresh English uploads ({len(passed)} videos)</h2>"
        + "\n".join(rows)
    )
    (outdir / "index.html").write_text(doc)
    log(f"\nWrote {outdir/'links.txt'} and {outdir/'index.html'}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--words", type=int, default=25, help="number of seed words")
    ap.add_argument("--per-word", type=int, default=100, help="max results per word")
    ap.add_argument("--keep", type=int, default=60, help="max videos to keep")
    ap.add_argument("--hours", type=float, default=24.0, help="upload window in hours")
    ap.add_argument("--min-height", type=int, default=480)
    ap.add_argument("--seed", type=int, default=None)
    args = ap.parse_args()

    if args.seed is not None:
        random.seed(args.seed)

    pool = SEED_WORDS[:]
    random.shuffle(pool)
    words = pool[: args.words]
    cutoff_ts = time.time() - args.hours * 3600

    log(f"Searching {len(words)} words for uploads in the last {args.hours:g}h...")
    seen = collect(cutoff_ts, words, args.per_word)
    candidates = [e for e, ok in seen.values() if ok]
    log(f"Unique videos: {len(seen)}; after flat filters: {len(candidates)}")

    log("Deep-filtering candidates (resolution, language)...")
    passed = enrich(candidates[: args.keep * 6])  # cap enrichment work
    log(f"Passed deep filters: {len(passed)}")

    kept = passed[: args.keep]
    write_outputs(kept, Path("out"))
    for e, v in kept[:10]:
        log(f"  sample: {e.get('title', '')[:70]}")


if __name__ == "__main__":
    main()

# fresh-tube

[fresh-tube](https://github.com/itsfja/fresh-tube) is a small tool for seeing what was actually uploaded to YouTube
in the last 24 hours — without the algorithm deciding what you get.

> [!IMPORTANT]
> fresh-tube samples uploads; it does not (and cannot) enumerate *all* of them. See "How does it work?" below.

## How do I install it?

You need Python 3.9 or newer.

```bash
pip install yt-dlp
```

No API key, no registration, no quota.

## How do I run it?

```bash
python3 fresh_tube.py                 # defaults: 25 words, keep 60 videos
python3 fresh_tube.py --words 50 --keep 100   # wider net
```

The results land in `out/`:

- `links.txt` — a plain list of shuffled video URLs
- `index.html` — open it in a browser for a clickable grid with thumbnails

## How does it work?

YouTube has no public "everything uploaded today" firehose, so fresh-tube approximates one.

It fans out many neutral common-word searches (sorted by upload date, filtered to "uploaded today"),
deduplicates the results by video ID, and then filters out the noise:

- Music (official videos, lyric videos, albums, covers, Vevo / "- Topic" channels)
- Gaming (gameplay, walkthroughs, Minecraft/Fortnite/Roblox, etc.)
- Children's content (cartoons, nursery rhymes)
- TV, film, and sports clips (trailers, full episodes, highlights)
- Politics and news
- Spam, adverts, and get-rich-quick schemes
- Shorts and low-resolution uploads
- Non-English uploads

What's left is a shuffled, uncurated slice of today's uploads — mostly from small channels with
little or no traction yet.

The filter lists (`BANNED_TITLE`, `BANNED_CHANNEL`) live at the top of `fresh_tube.py` and are meant
to be edited when junk slips through.

> [!NOTE]
> Filtering is done with heuristics (title and channel name patterns), not YouTube's own category
> metadata, so the occasional straggler will get through.

> [!WARNING]
> Be gentle with it: the script sleeps between requests, but very large runs (hundreds of words) may
> trip YouTube's bot checks.

## What options does it take?

| Flag | Default | Meaning |
|---|---|---|
| `--words` | 25 | number of seed words to search |
| `--per-word` | 100 | max results per word |
| `--keep` | 60 | max videos in the final list |
| `--hours` | 24 | upload window |
| `--min-height` | 480 | drop videos below this resolution |
| `--seed` | random | fixed seed for reproducible runs |

## License

fresh-tube is licensed under the MIT license.

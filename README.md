# fresh-tube

See what was actually uploaded to YouTube in the last 24 hours — without the
algorithm deciding what you get.

`fresh_tube.py` samples fresh English-language uploads by fanning out many
neutral common-word searches sorted by upload date, deduplicating the results,
and filtering out the noise: music, gaming, kids content, spam, TV/film clips,
politics, shorts, and low-resolution videos. What's left is a shuffled,
uncurated slice of today's uploads — mostly from small channels with little
or no traction yet.

## Install

```bash
pip install yt-dlp
```

Python 3.9+. No API key required.

## Usage

```bash
python3 fresh_tube.py                 # defaults: 25 words, keep 60 videos
python3 fresh_tube.py --words 50 --keep 100   # wider net
```

Output lands in `out/`:

- `links.txt` — plain list of shuffled video URLs
- `index.html` — open in a browser for a clickable grid with thumbnails

## Options

| Flag | Default | Meaning |
|---|---|---|
| `--words` | 25 | number of seed words to search |
| `--per-word` | 100 | max results per word |
| `--keep` | 60 | max videos in the final list |
| `--hours` | 24 | upload window |
| `--min-height` | 480 | drop videos below this resolution |
| `--seed` | random | fixed seed for reproducible runs |

## Honest caveats

- This is a **sample**, not the complete set of today's uploads — no public
  method can give you that. More `--words` means better coverage but longer
  runtime.
- Category filtering is done with heuristics (title/channel regex), not
  YouTube's own categories, so occasional stragglers slip through. The
  `BANNED_TITLE` / `BANNED_CHANNEL` lists at the top of the script are meant
  to be edited as you notice junk.
- Be gentle: it sleeps between requests, but very large runs may trip
  YouTube's bot checks.

## License

MIT — see [LICENSE](LICENSE). Authors: itsfja & Mistral AI (Vibe Code).

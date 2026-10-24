# Agorian

Year 8 Humanities revision site. Challenge what you know.

- `src/index.html` — the page (HTML, CSS and JS in one file, no framework)
- `data/` — question sources and `bank.json`, built from the spreadsheets by `data/normalise.py`
- `img/` — public-domain artwork from Wikimedia Commons (credits in the page footer)
- `build.py` — assembles `docs/` for hosting (`--inline` embeds images for a single-file preview)
- `docs/` — what GitHub Pages serves at agorian.au

To update questions: edit the source spreadsheets, run `python3 data/normalise.py` then `python3 build.py`, commit, push.

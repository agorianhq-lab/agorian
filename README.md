# Agorian

Year 8 History revision site at [agorian.au](https://agorian.au). Challenge what you know.

One static page, no framework, no backend, no accounts. Everything a student does stays in their browser; the only thing sent anywhere is an anonymous page-visit count (GoatCounter).

## Layout

| Path | What it is |
|---|---|
| `src/index.html` | The whole app: HTML, CSS and JavaScript in one file. It reads a course description at run time, so one page serves every course. |
| `courses/history.json`, `courses/civics.json` | One file per course: units and their colour slots, modes, copy for the welcome card and the exam or test breakdown, which header tile to show, and which data files to load. |
| `data/bank.json` | **Canonical** History question bank and key terms. Edit this file directly; nothing regenerates it. |
| `data/shortq.json` | History short answer practice: questions, criteria, full-mark model responses. |
| `data/sources.json` | History source analysis practice: ten sources, four quick questions each, a timed write, and the checklist. |
| `data/civics/bank.json` | **Canonical** Civics question bank (multiple choice and word-bank gaps) and glossary terms, each term tagged with its unit. |
| `data/civics/scenarios.json` | Civics scenario practice: seven fictional scenarios with four quick questions each. Same shape as `sources.json` without the timed write. |
| `data/civics/mythfact.json` | The Myth or fact header tile: `[statement, true or false, why]`, one an hour. |
| `data/civics/play.json` | The interactives: sorts, the referendum and government simulators, the law builder, and the `spot` entry that opens Spot the error. |
| `data/civics/errors.json` | Spot the error: thirteen passages written as a student's answer, each segment either correct or a planted mistake with its `fix` and `why`. |
| `data/civics/explain.json` | Explain it in 25 words: a prompt, the three ideas (`must`) a complete answer needs, and a model of about 25 words. Opened from the Key terms page. |
| `tools/chrono.py` | Timeline events, periods and links, and the generator that renders them. |
| `tools/validate.py` | Content checks (see below). |
| `build.py` | Validates, then assembles `docs/` from the files above. |
| `docs/` | Build output. GitHub Pages serves this folder from `main`. Commit it. Civics is the front page and builds to `docs/`; History builds to `docs/history/`. `docs/civics/` is a redirect to the front page for old links. |
| `img/` | Shared artwork, public domain unless the page footer says otherwise. `img/<course>/` holds artwork only that course uses (for example the civics tile photographs, credited in that page's footer). |
| `fonts/` | Self-hosted Fraunces and Atkinson Hyperlegible (Next digits). No Google Fonts. |
| `logo/`, `palettes/`, `square/` | Design assets and exploration sheets. Not built. |
| `handout/` | Printable one-pagers. Not linked from the site. |
| `REVIEW-2026-10-25.md`, `GROWTH-RESEARCH-2026-10-25.md` | Notes. |

## Working on it

```
python3 tools/validate.py              # check every course's content files
python3 build.py                       # validate, then build docs/history/ (History) for hosting
python3 build.py --course civics       # build docs/ (Civics, the front page)
python3 build.py --inline [--course X] # one self-contained file (images and fonts embedded) in preview/, for a sandbox
```

Adding a course: write `courses/<id>.json` (copy `civics.json`), point it at its data files, and build with `--course <id>`. Units take one of three colour slots (`eu`, `jp`, `sk`); a course can recolour the slots under `colours`.

Scores and settings live in the browser's localStorage. History uses the original `agorian:` keys; every other course gets its own namespace (`agorian:<id>:`), because all courses share the agorian.au origin and question ids overlap.

Per-course switches in the course file: `badges` (the badge row on the home page and the badge toasts), `board` (the Clear your mistakes board: a question a viewer gets wrong stays on it until answered correctly twice in a row), `challenge.classCode` (the Challenge opens with a lobby where a class code typed from the board gives everyone the same 20 questions in the same order; results carry the code and the attempt number), and `links` (the Trusted sites section, each entry `name`, `url`, `by`, `icon` and `col` for the badge, `topics` from the bank, and a one-sentence `use` that completes "Best for …"; an `img` key shows a supplied logo instead of the drawn icon). History has all four off so its page is unchanged.

Branches. Work on `staging`. **Anything pushed to `main` goes live within about two minutes**, including after the site has been unpublished in the Pages settings, because a commit to the publishing source republishes it. Push to `main` only to publish.

A GitHub workflow (`.github/workflows/validate.yml`) runs the validator and the build on every push and fails if `docs/` is stale, so always build before committing.

## The validator

`tools/validate.py` fails the build if any of these are wrong:

- `bank.json` questions: integer ids, unique; unit is one of Medieval Europe, Shogunate Japan, Skills and concepts; topic, skill and question are not blank; type is one of `mc`, `ms`, `gaps`, `text`, `short`, `extended`; options are non-empty and unique; answer indices are in range (exactly one for `mc`, at least one and not all for `ms`); `gaps` have one more segment than blanks and every blank appears in its choices; `text` has at least one accepted answer; `short` has an explanation (the model answer); no topic appears under two units.
- `bank.json` terms: term and definition present, terms unique.
- `shortq.json` and `sources.json` (and `scenarios.json`): ids unique, required fields present, answer indices in range, marks in range, criteria and mark points non-empty. The timed write is optional; if a source has one it must be complete.
- `mythfact.json`: a list of `[statement, true or false, why]`, statements unique and under 120 characters.
- `play.json`: known kinds only (`sort`, `referendum`, `government`, `law`, `spot`); a `spot` entry needs `data.errors`.
- `errors.json`: ids unique, unit known, at least four segments, every planted error has a `fix` and a `why`, two or three planted errors per passage.
- `explain.json`: ids unique, unit known, exactly three `must` ideas, model at most 30 words.
- Course `links`: title, non-empty items with name, by and use, https urls, no duplicates, topics that exist in the bank, logo images that exist. `badges`, `board` and `challenge.classCode` must be booleans if present.
- Each course file names its units; every question, source and tagged term must use one of them.
- Images: every key the page, the timeline bands or the data refer to exists as `img/<key>.jpg` or `img/<course>/<key>.jpg`. Unused files are listed, not failed.

## Question formats

Every question has `id`, `unit`, `topic`, `skill`, `type`, `question`, `explanation` and `stimulus` (null or text). `source` and `srcId` record where an item came from and are stripped at build time.

| type | extra fields |
|---|---|
| `mc` | `options` (2–8), `answer` `[index]` |
| `ms` | `options`, `answer` `[index, …]` (select all that apply) |
| `gaps` | `segments` (n+1 strings), `blanks` (n answers), `choices` (n option lists). When every blank shares one option list and no answer repeats, the page treats it as a matching or ordering set and lets each option be used once. |
| `text` | `answer` list of accepted strings |
| `short` | none; `explanation` holds the model answer |
| `extended` | `answer` null; the six Section C practice prompts |

## Content rules

1. Nothing may reproduce or closely mirror a live assessment's questions, sources or prompts. Question types may match the exam; specific questions may not.
2. Mark statements are hedged ("likely", "usually"), and only full-mark exemplars are shown.
3. No school names or crests, no student data. The privacy wording on the welcome card and footer must stay true.
4. Australian English, Year 8 pitch, historically accurate.

## Counter

`gc.zgo.at/count.js` loads asynchronously and reports one anonymous path per screen (`/`, `/daily`, `/shortq/<id>`, …; other courses are prefixed, e.g. `/civics/daily`) to `agorian.goatcounter.com`. It only counts on `agorian.au`, so previews and local builds are never recorded. Opening `agorian.au/#toggle-goatcounter` once on a device stops that device being counted.

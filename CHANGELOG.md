# Changelog

## 0.4.0 — 2026-09-19

- **Lint code, not just screenshots.** `beautiful index.html`, `beautiful https://…` and the
  `beauty_render` MCP tool render HTML strings, files and URLs with headless Chromium
  (`pip install "beautiful-score[render]" && playwright install chromium`) at desktop 1280×800,
  tablet 768×1024 and mobile 375×812 — deterministic (animations off, fonts awaited, fixed
  clock, DPR 1), so the pixels and the score equal a screenshot's. A static no-browser backend
  (`[html]`, WeasyPrint) for plain HTML/CSS. `--viewports`, `--save-renders`, `--backend`.
- **Claude Code plugin.** `.claude-plugin/plugin.json` + `marketplace.json`: the skill and the
  MCP server install with `/plugin marketplace add solomonBoltin/beautiful` then
  `/plugin install beautiful@beautiful`.
- **Hall of fame.** `demo/hall_of_fame.py` renders ~80 design-led sites with the same engine and
  ranks them; the top scorers are in the README.
- **The demo page lints itself** in CI at all three viewports (`--min 60`), and was redesigned
  with the tool: desktop 67 → 92, tablet 61 → 84, mobile 49 → 78.

## 0.3.0 — 2026-09-19

- **Beauty lint.** The CLI takes files, directories and globs; `--format github` emits workflow
  annotations on the image files, `--format sarif` feeds GitHub code scanning, `--save-baseline` /
  `--baseline` gate on regressions, exit codes 0 / 1 / 2. A `.pre-commit-hooks.yaml` and a
  `beauty_lint` MCP tool. The Action annotates images and can write SARIF.
- **Calibrated against human ratings.** `research/calibrate.py` fits the score to the Reinecke &
  Gajos website ratings (Calista mirror) and tests on Calista's pairwise set; results in
  `research/CALIBRATION.md`.
- **Experimental measurements** (reported, not yet weighted): Rosenholtz feature congestion,
  Miniukovich contour congestion, Redies edge-orientation entropy and anisotropy, Ngo sequence.
- **Evidence base.** `research/SURVEY.md` — the landscape survey the formula is held to; FACTORS.md
  now says what the evidence rules out (golden ratio, Birkhoff O/C).

## 0.2.0 — 2026-09-19

- **MCP server**: `beautiful-mcp` exposes `beauty_score` and `beauty_compare` to any MCP client
  (Claude Code, Cursor, Windsurf, ...). Dependency-free.
- **GitHub Action**: score screenshots in CI and comment the table on the pull request.
- **Browser demo**: drag a screenshot in, get the score — the real package running in the page.
- **Famous sites**: twenty well-known home pages scored, with the factor breakdown.
- **`demo/loop.gif`**: a real trace of the score climbing as a button walks back to centre.
- **Factor wishlist** (`FACTORS.md`) and an issue template for proposing new factors.
- PyPI publishing via trusted publishing on version tags.
- CLI: `--json`, `--min N` (CI gate). Windows consoles no longer crash on non-ASCII hints.

## 0.1.0 — 2026-09-19

- First public release: `beauty()`, `beauty_score()`, modes `ui` / `art` / `logo`, the CLI, the
  demo set, ordering-invariant tests, CI on Linux/macOS/Windows for Python 3.9–3.13.

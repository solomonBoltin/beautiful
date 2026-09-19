# Changelog

## 0.6.0 — 2026-09-19

- **DOM rules.** Rendered pages run a rule pass with sourced thresholds: WCAG text contrast,
  font size (12 px floor, 16 px body on phones), touch targets (24 px WCAG floor, 44 px on
  phones, with the standard's exemptions), line length and line height, stretched images,
  clipped text, viewport meta, heading order, alt text, typographic noise. Errors cost points;
  every finding names its elements. Fixtures in `demo/lint/` are checked in CI.
- Demo page brought to zero rule errors by its own lint (44 px targets and 16 px body text on
  phones, shorter measure).
- `research/DESIGN-LINTS.md`: a survey of every published design lint, guideline, no-go and
  measured rule we could find, each rated for whether pixels or the DOM can enforce it.

## 0.5.0 — 2026-09-19

- **Balance stands in for symmetry.** In `ui` mode composition = *symmetric OR balanced*; balance
  is equilibrium (tighter, σ 0.20), half-mass equality, and a new *profile symmetry* (the coarse
  left-to-right mass distribution mirrored about the centre). A headline-left / illustration-right
  hero — Medium's home page — went from composition 0.16 to 0.41 and from 36 to 62; the lopsided
  sample stays at 0.10.
- **Air is good.** Whitespace is a ramp-and-plateau, not a bell: Apple (67 %) and Medium (84 %)
  are no longer punished; an empty viewport still is.
- **Defects are not taste.** Rendered pages get a DOM overflow check (scroll width, the elements
  that stick out): −10 and a hint naming them. Screenshots get a *clipping?* hint when content
  touches a side edge in many places. `report["penalties"]`.
- **See what it sees.** `beautiful --explain DIR`, MCP `explain_dir`, and a "what does it see?"
  button in the demo: one sheet per image with the mirror-disagreement map, centre of mass and
  mass split, grid lines, whitespace mask, edge map, contrast, hue wheel + template + palette,
  and the four edge bands.
- Demo page: mobile overflow fixed (the select ran off the screen — exactly what the new check
  catches); 92 / 84 / 84 at desktop / tablet / mobile.
- Every demo artefact regenerated with the new formula (`demo/rescore.py`); recalibrated:
  `ui` ρ −0.08 / −0.40, ridge 0.54 / 0.43 → `web` model refreshed.

## 0.4.1 — 2026-09-19

- MCP server speaks UTF-8 on stdio regardless of the console codepage (Windows fix).
- Hall of fame: Canva's maintenance-page capture dropped.

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

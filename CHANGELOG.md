# Changelog

## Unreleased

- **Components.** Rendered pages: every landmark, section and control is cropped from one full-page screenshot and scored on its own (`beautiful/components.py`, classic scale, controls judged on both-axis symmetry). `--components` lists them; baselines store `{score, errors, components}` and `--baseline` fails when any component gets less beautiful or a new error-level rule fires.
- **Balance counts in `logo` and `art` mode.** Composition in the generic (non-`ui`) formula was mirror
  symmetry alone, so a centred, balanced mark with no mirror axis (the Nike swoosh) scored like a
  lopsided one. A compact, balanced figure now earns most of the composition credit (`max(mirror,
  0.85·balance²·compactness)`); compactness gates it so noise and confetti, which are trivially
  balanced, gain nothing (noise 17 → 18, blobs 18 → 20, splashes 37 → 38; symmetric marks unchanged).
- **Thirteen icons, three versions each** (`demo/logos/`, `demo/results_logos.md`): Chrome, ten acclaimed
  marks and two raster icons as supplied, each scored as published, degraded, and after a search for
  the best framing. Eight of eleven famous marks come back "already at its optimum"; Nike goes 60 → 87
  when re-framed by centre of mass.
- **Five rendered scenarios** (`demo/scenes/`, `demo/gifs/`): sign-in, dashboard, pricing, product page and phone onboarding, each a real HTML page walking from a flawed state to a polished one, every frame rendered by the tool's own Chromium and scored by the lint. Replaces the drawn sign-in GIF.
- **Photographs in the demo** (`demo/photos/`): a portrait, a sunset and a quetzal, with the honest finding that `art` mode underrates all three (issue #46).

## 0.7.0 — 2026-09-20

- **Rules v2: 44 DOM rules.** The 19 rule issues from the design-lint survey implemented: text
  overlap, broken images, empty controls, generic and redundant links, justified / underlined /
  all-caps / centred body text, contrast polarity, near-duplicate colours, too many hues, pure
  black-on-white, edge margins, false floor, hidden desktop nav, multiple primaries, consent
  asymmetry, pre-ticked opt-ins, urgency and confirmshaming text, placeholder residue, focus rings
  removed, motion without reduced-motion, marquee/blink, off-scale spacing, thumb reach, and the
  AI-look signature (a note, never a penalty). Every finding carries `source`, `why` and `fix`.
  Fixtures `demo/lint/bad.html` (33 rules) and `floor.html` (5 more) are proven in CI.
- **The 100-site benchmark.** `research/top100.py` renders the 100 most acclaimed home pages
  (after dropping 44 bot walls, consent dialogs and blank captures by eye) and scores them;
  `research/degrade.py` makes a broken twin of each (a block shifted off its grid, content
  clipped by the viewport, an overlapping duplicate, a stretched region, a contrast wash,
  clutter, a lopsided crop, a colour cast); `research/benchmark.py` measures whether a score
  separates acclaimed from 100 random pages and from broken renders — see `research/BENCHMARK.md`.
- **`ui` is now a fitted formula; the literature formula is `classic`.** The benchmark showed
  the literature-weighted formula could not tell acclaimed design from a random page (AUC 0.59)
  and preferred the broken twin 37 % of the time. `research/fit_ui.py` keeps the explicit shape —
  a weighted sum of documented curves over pixel measurements — but centres each curve on what
  acclaimed pages measure and fits the weights to four targets at once: acclaimed > ordinary,
  original > degraded twin, the crowd-rating correlation must not go negative, and 21 curated
  UI orderings (rebalanced > original, composed screens > unstyled, designed pages > plain text
  dumps) must hold. Priors keep it a *UI* score: composition ≥ 0.15 of the weight, the
  photographic-texture and amount-of-content terms capped. Cross-validated: AUC 0.72 (was 0.59),
  original beats its twin 74 % (was 63 %), ρ vs crowd ratings +0.14 (was −0.08), 18 of 21
  curated orderings respected — the three it misses are all "a well-set plain page beats a
  designed one", which pixels alone cannot settle and the DOM rules are for. Two new measurements
  it needed: **hierarchy** (the share of contrast that survives a block-scale blur) and
  **margin** (quiet side edges, from `edge_contact`). Every `ui` report carries the classic score
  under `classic`; `--mode=classic` returns the old report unchanged. Report: `research/FIT.md`.
- Tests and CI gates rewritten for the fitted scale (the curated orderings are the tests);
  demo tables re-scored; `research/results_top100.md` lists all 100 sites with `ui`, `classic`
  and `web`.

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

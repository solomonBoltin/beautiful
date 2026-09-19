# Fitting the `ui` formula to acclaimed design, degraded twins and human ratings

Evidence: **100 acclaimed** pages, **100 ordinary** pages, **100 original/degraded pairs**, **398 human-rated** screenshots. The formula keeps its explicit shape (a weighted sum of documented curves over pixel measurements); bells are centred on what acclaimed pages measure, weights are fitted to three targets at once and cross-validated 5-fold over the acclaimed set.

## Cross-validated (held-out acclaimed pages and their pairs)

| | shipped `ui` (literature weights) | `web` (ridge on 2013 ratings) | **fitted `ui`** |
|---|---:|---:|---:|
| AUC acclaimed > ordinary | 0.59 | 0.61 | **0.72** |
| original beats its degraded twin | 63% | 37% | **74%** |
| ρ vs human rating (398) | -0.08 | +0.60 | **+0.14** |
| ρ vs human pairwise rank (100 ordinary) | -0.40 | +0.43 | **-0.19** |
| curated UI orderings respected (the repo's test pairs) | — | — | **18/21** |

Priors that keep this a *UI* score: composition weight ≥ 0.15; the photographic-texture terms (edge-orientation entropy, anisotropy) ≤ 0.06 each. Without them the first fit put 0.20 on anisotropy and 0.02 on symmetry, scored a lopsided screen above its rebalanced twin and Apple's hero at 57: it had learned 'marketing page with a photo', not 'composed screen'.

## The fitted formula

| term | curve | centre / range | weight | descends from |
|---|---|---|---:|---|
| composition | ramp | ramp 0.109 → 0.812 | 0.15 | Ngo 2003; Bauerly & Liu 2006 — symmetric OR balanced (symmetry.py) |
| local | ramp | ramp 0.421 → 0.737 | 0.06 | local tile symmetry |
| alignment | ramp | ramp 0.133 → 0.272 | 0.04 | Miniukovich 2015 grid quality |
| contrast | ramp | ramp 0.602 → 2.07 | 0.02 | Miniukovich 2015; Reber 2004 |
| harmony | ramp | ramp 0.814 → 1 | 0.04 | Cohen-Or 2006 templates |
| edge_density | bell | bell at 0.139 ± 0.176 | 0.04 | Reinecke & Gajos 2013 (complexity, inverted-U) |
| jpeg_bpp | bell | bell at 0.102 ± 0.0878 | 0.07 | Rigau 2008 Kolmogorov proxy |
| colours | bell | bell at 6 ± 15 | 0.07 | Miniukovich 2015 dominant colours |
| whitespace | bell | bell at 0.63 ± 0.673 | 0.07 | Miniukovich 2015 white space |
| colorfulness | bell | bell at 25.3 ± 75.3 | 0.05 | Hasler & Süsstrunk 2003; Reinecke 2013 (inverted-U) |
| congestion | bell | bell at 0.0169 ± 0.0221 | 0.03 | Rosenholtz 2007 feature congestion |
| contour | bell | bell at 0.646 ± 0.103 | 0.09 | Miniukovich 2014 contour congestion |
| orientation | bell | bell at 0.899 ± 0.135 | 0.05 | Redies edge-orientation entropy |
| anisotropy | bell | bell at 0.81 ± 0.612 | 0.05 | Redies anisotropy |
| hierarchy | ramp | ramp 0.361 → 0.72 | 0.09 | coarse-structure share (this repo; visual hierarchy cue) |
| margin | ramp | ramp 0 → 1 | 0.07 | quiet side margins (edge_contact; this repo) |

## What acclaimed pages measure (the bell centres)

| measurement | acclaimed median | ordinary median | degraded median | rated median |
|---|---:|---:|---:|---:|
| composition | 0.63 | 0.7 | 0.53 | 0.615 |
| local | 0.601 | 0.675 | 0.566 | 0.625 |
| alignment | 0.187 | 0.217 | 0.185 | 0.153 |
| contrast | 1.46 | 1.16 | 1.31 | 1.37 |
| harmony | 0.914 | 0.88 | 0.909 | 0.859 |
| edge_density | 0.139 | 0.215 | 0.125 | 0.293 |
| jpeg_bpp | 0.102 | 0.136 | 0.0944 | 0.178 |
| colours | 6 | 9 | 7 | 10 |
| whitespace | 0.63 | 0.43 | 0.629 | 0.461 |
| colorfulness | 25.3 | 42.7 | 24.1 | 46.9 |
| congestion | 0.0169 | 0.0265 | 0.0176 | 0.033 |
| contour | 0.646 | 0.68 | 0.635 | 0.721 |
| orientation | 0.899 | 0.884 | 0.895 | 0.876 |
| anisotropy | 0.81 | 0.927 | 0.86 | 0.986 |
| hierarchy | 0.57 | 0.631 | 0.571 | 0.551 |
| margin | 0.983 | 0.287 | 0.948 | 0.976 |

## Per-defect: does the fitted score prefer the original?

| defect | original preferred |
|---|---:|
| cast | 42% (12) |
| clip | 85% (13) |
| clutter | 92% (12) |
| lopsided | 83% (12) |
| overlap | 77% (13) |
| shift | 92% (13) |
| stretch | 62% (13) |
| wash | 67% (12) |

## How to read this

- AUC 0.5 = coin flip; pair accuracy 50 % = coin flip. The shipped literature-weighted formula was the baseline; anything fitted here has never seen the held-out fold.
- ρ against the 2013 crowd ratings is a *constraint* (must not go negative), not the goal: acclaim by designers and crowd appeal disagree, and this formula is aimed at the former.
- The bell centres are the honest content of this file: they say what the pages people acclaim actually measure, and any future factor can be checked against them.
- Data the fit never saw: none of the sets is held out entirely; a fresh set of acclaimed pages is the next test (research/top100.py takes a candidate list).

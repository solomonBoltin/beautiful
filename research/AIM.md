# Cross-check against AIM (Aalto Interface Metrics)

AIM's metric classes (aalto-ui/aim, MIT) run directly on 103 screenshots: 15 demo screens, 20 famous home pages, 34 acclaimed pages (every third of research/top100) and 34 ordinary pages (every third of Calista's comparison set). Inputs downscaled to 640 px for both implementations. Metrics that need AIM's segmentation models (grid quality m21, white space m22) or a saliency/NIMA network (m9, m18) are not run; colour harmony m20 takes ~100 s per image and was left out.

## Does our simplified implementation agree with the reference?

| AIM metric | ours | Spearman ρ (all images) | AUC acclaimed > ordinary: AIM | ours |
|---|---|---:|---:|---:|
| m4 contour density | `edge_density` | +0.94 | 0.26 | 0.22 |
| m5 figure-ground contrast | `edge_contrast` | -0.61 | 0.41 | 0.62 |
| m6 contour congestion | `contour_congestion` | +0.56 | 0.46 | 0.33 |
| m7 subband entropy (clutter) | — (issue #13) | — | 0.27 | — |
| m8 feature congestion (clutter) | `feature_congestion` | +0.71 | 0.31 | 0.28 |
| m13 luminance std | `rms_contrast` | +1.00 | 0.37 | 0.37 |
| m15 colourfulness (Hasler–Süsstrunk) | `colorfulness.hasler` | +1.00 | 0.38 | 0.38 |
| m3 distinct RGB values | `dominant_colors` | +0.84 | 0.47 | 0.40 |

## AIM's metrics against our scores (Spearman, all images)

| AIM metric | vs `ui` | vs `classic` | vs `web` |
|---|---:|---:|---:|
| m4 contour density | -0.33 | -0.58 | +0.12 |
| m5 figure-ground contrast | -0.07 | -0.07 | +0.16 |
| m6 contour congestion | -0.17 | -0.13 | -0.37 |
| m7 subband entropy (clutter) | -0.34 | -0.52 | +0.14 |
| m8 feature congestion (clutter) | -0.20 | -0.40 | +0.08 |
| m13 luminance std | +0.12 | -0.22 | +0.17 |
| m15 colourfulness (Hasler–Süsstrunk) | -0.02 | -0.31 | +0.07 |
| m3 distinct RGB values | -0.10 | -0.52 | +0.44 |

## Demo screens, side by side

| screen | `ui` | AIM contour density | ours | AIM contrast | ours | AIM contour congestion | ours | AIM feature congestion | ours | AIM subband entropy |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| crates_io_crates_serde | 89 | 0.034 | 0.135 | 0.644 | 1.25 | 0.730 | 0.580 | 4.279 | 0.0120 | 2.728 |
| crates_io_search_q_http | 84 | 0.025 | 0.112 | 0.643 | 0.95 | 0.646 | 0.496 | 3.504 | 0.0109 | 2.464 |
| cratesio_home | 92 | 0.035 | 0.135 | 0.663 | 1.42 | 0.695 | 0.601 | 4.581 | 0.0207 | 2.634 |
| digital_office_original | 77 | 0.023 | 0.129 | 0.586 | 0.82 | 0.593 | 0.483 | 3.460 | 0.0076 | 2.834 |
| digital_office_rebalanced | 84 | 0.015 | 0.101 | 0.747 | 0.66 | 0.229 | 0.412 | 3.005 | 0.0049 | 2.456 |
| github_login_unstyled | 55 | 0.010 | 0.038 | 0.429 | 1.76 | 0.837 | 0.715 | 2.145 | 0.0051 | 0.848 |
| medium_home | 79 | 0.032 | 0.132 | 0.776 | 1.78 | 0.560 | 0.600 | 5.433 | 0.0135 | 2.641 |
| npm_home_unstyled | 79 | 0.021 | 0.084 | 0.384 | 1.81 | 0.436 | 0.543 | 4.452 | 0.0097 | 2.514 |
| pinkas_dashboard | 81 | 0.020 | 0.107 | 0.812 | 0.93 | 0.650 | 0.439 | 3.957 | 0.0087 | 2.597 |
| pinkas_dialog | 86 | 0.018 | 0.106 | 0.666 | 0.79 | 0.503 | 0.445 | 3.192 | 0.0052 | 2.548 |
| pinkas_documents | 78 | 0.017 | 0.094 | 0.638 | 0.86 | 0.725 | 0.468 | 3.282 | 0.0063 | 2.273 |
| pypi_home | 95 | 0.035 | 0.124 | 0.441 | 1.67 | 0.712 | 0.613 | 4.539 | 0.0175 | 2.620 |
| pypi_org_project_numpy | 90 | 0.035 | 0.131 | 0.463 | 1.19 | 0.792 | 0.601 | 4.334 | 0.0147 | 2.737 |
| pypi_org_search__q_http | 82 | 0.014 | 0.092 | 0.631 | 0.43 | 0.646 | 0.561 | 2.924 | 0.0126 | 1.604 |
| sample_asymmetric_ui | 60 | 0.017 | 0.045 | 0.500 | 1.76 | 0.348 | 0.497 | 3.177 | 0.0033 | 2.691 |

## How to read this

- ρ near +1: our simplified measurement orders pages the way the reference does, so replacing it would change nothing but the scale. Near 0: the two measure different things and the name is misleading; the AIM one is the literature's.
- The two AUC columns say which implementation is the better *design* signal on this data, independent of agreement.
- AIM implements Miniukovich & De Angeli's metrics as published (with their thresholds); ours were written from the papers with stated simplifications (beautiful/experimental.py).

## Findings

- **Four of our seven counterparts are the reference in all but name.** Luminance std and
  Hasler colourfulness match AIM exactly (ρ = 1.00); contour density (ρ = 0.94) and distinct
  colours (0.84) order pages the same way at a different scale. Nothing to change there.
- **Feature congestion (0.71) and contour congestion (0.56) are approximations, as
  `experimental.py` says.** They agree on the ranking of most pages and disagree on the dense
  ones; a faithful port of Rosenholtz's pyramid (AIM's m8 uses pyrtools) is the fix, and issue
  #13 covers subband entropy, which we do not compute at all.
- **Figure-ground contrast is the one real disagreement: ρ = −0.61.** AIM implements
  Miniukovich & De Angeli's definition — Canny edges are extracted at seven rising luminance
  thresholds and the measure is how many edges *survive* as the threshold rises, i.e. the share
  of a page's edges that are high-contrast. Ours (`features.contrast.edge_contrast`) is the 75th
  percentile of Sobel magnitude over strong edges: a page with a few very hard edges and much
  soft text scores high on ours and low on AIM's. On this data ours is the better acclaimed-vs-
  ordinary signal (AUC 0.62 vs 0.41), so the *number* stays, but the name is wrong: it is "hard-
  edge strength", not figure-ground contrast. Tracked in issue #47.
- **No single AIM metric separates acclaimed from ordinary pages** (every AUC is below 0.5, i.e.
  acclaimed pages have *less* contour density, clutter and colour than random ones — the
  inverted-U again), which is the same conclusion the bench reached for our raw measurements:
  the value is in the curves and the combination, not in any one statistic.
- **AIM's metrics correlate with `classic` negatively and with `ui` weakly** — expected, since both
  formulas turn these raw statistics into "in the acclaimed range" goodness rather than
  rewarding more of them. The `web` model, fitted to crowd ratings, leans the other way
  (distinct colours +0.44): the crowd likes more.

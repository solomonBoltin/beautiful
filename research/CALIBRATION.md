# Calibration against human ratings

Rating set: **398** website screenshots with mean appeal ratings (Reinecke & Gajos 2014 via the Calista mirror). Comparison set: **100** pages with Bradley–Terry scores from pairwise votes (Calista 2023). Spearman ρ throughout; 5-fold cross-validation for anything fitted. Run: `python research/calibrate.py`.

## 1. The score as shipped

| | rating set | comparison set |
|---|---:|---:|
| `beauty(mode='ui')` vs human | **-0.076** | **-0.402** |

## 2. Each factor on its own

| factor | ρ (rating) | ρ (comparison) |
|---|---:|---:|
| composition | +0.060 | -0.257 |
| alignment | -0.203 | -0.278 |
| simplicity | -0.028 | -0.142 |
| whitespace | -0.246 | -0.255 |
| harmony | +0.023 | -0.251 |
| colorfulness | +0.059 | +0.064 |
| contrast | -0.146 | -0.416 |
| local | +0.102 | -0.130 |
| *feature_congestion* (experimental, unweighted) | -0.058 | +0.144 |
| *contour_congestion* (experimental, unweighted) | -0.164 | +0.137 |
| *edge_orientation_entropy* (experimental, unweighted) | +0.098 | +0.443 |
| *anisotropy* (experimental, unweighted) | -0.110 | -0.450 |
| *sequence* (experimental, unweighted) | -0.139 | -0.200 |
| raw edge_density | -0.109 | +0.227 |
| raw jpeg_bpp | -0.264 | +0.089 |
| raw dominant_colors | +0.253 | +0.331 |
| raw colorfulness_variety | -0.024 | +0.004 |
| raw whitespace | -0.261 | -0.321 |

## 3. Non-negative weights fitted on the goodness factors

Same linear form as the shipped score. Cross-validated ρ on the rating set: **0.066**; the weights fitted on all of it, applied to the comparison set it never saw: **-0.162**.

| factor | shipped weight | fitted weight |
|---|---:|---:|
| composition | 0.28 | 0.19 |
| alignment | 0.16 | 0.00 |
| simplicity | 0.14 | 0.00 |
| whitespace | 0.10 | 0.00 |
| harmony | 0.10 | 0.00 |
| colorfulness | 0.06 | 0.19 |
| contrast | 0.10 | 0.00 |
| local | 0.06 | 0.63 |

## 4. Ridge with inverted-U terms and the experimental measurements

Inputs: the 8 goodness factors, the 5 experimental measurements, and edge density and colourfulness with their squares (the inverted-U). Best λ = 1; cross-validated ρ on the rating set: **0.544**; transfer to the comparison set: **0.432**.

| term | standardised coefficient |
|---|---:|
| anisotropy | -0.633 |
| alignment | -0.468 |
| edge_orientation_entropy | -0.421 |
| feature_congestion | -0.335 |
| contour_congestion | -0.306 |
| whitespace | -0.284 |
| edge_density² | -0.220 |
| colorfulness | +0.175 |
| simplicity | -0.146 |
| local | +0.136 |
| colorfulness | +0.131 |
| harmony | -0.107 |
| composition | +0.103 |
| edge_density | -0.057 |
| colorfulness² | -0.050 |
| sequence | -0.041 |
| contrast | -0.003 |

This ridge model ships as `beauty(image, mode='web')`: the prediction is reported as a percentile against the 398 rated sites (a web score of 70 = the model puts it above 70 % of them). Cross-validated ρ ≈ 0.54 and out-of-sample ρ ≈ 0.43 make it **advisory**, not a truth — the survey's own rule is ρ ≥ 0.7 to trust, < 0.5 advisory.

## How to read this

- Hand-crafted metric sets top out near ρ ≈ 0.6–0.7 on website ratings in the literature (Reinecke 2013: 48 % of variance; Miniukovich 2015: 49 %); learned CNNs reach r ≈ 0.85 (Webthetics). Anything in that band is as good as pixels-without-semantics get.
- A factor whose sign flips between the two sets is not robust; a factor near zero on both is carrying its weight for a reason other than appeal (e.g. it makes the hints useful).
- The comparison set is the honest test: nothing was fitted on it.

_Generated 2026-09-19 by research/calibrate.py; features cached in research/features_*.csv._

# Does the score know beauty when it sees it?

Three sets: **100 acclaimed** home pages (research/top100.py), **100 ordinary** pages (Calista's random Alexa-top-5000 set, which also carries human pairwise ranks), and **10 broken** renders (the lint fixtures at three viewports, unstyled and lopsided captures). Plus the **398 human-rated** screenshots (Reinecke & Gajos 2014) the `web` model was fitted on.

AUC = the probability that a random page from the first set outscores a random page from the second (0.5 = coin flip, 1.0 = perfect). ρ = Spearman against the human numbers.

## 1. Every score and factor, on its own

| signal | AUC acclaimed > ordinary | AUC acclaimed > broken | AUC ordinary > broken | ρ vs pairwise rank (ordinary) | ρ vs rating (rated) |
|---|---:|---:|---:|---:|---:|
| **`ui` score (shipped)** | 0.60 | 0.35 | 0.26 | -0.40 | -0.08 |
| **`web` model** | 0.61 | 0.59 | 0.47 | 0.43 | 0.60 |
| composition | 0.50 | 0.47 | 0.48 | -0.26 | 0.06 |
| alignment | 0.43 | 0.23 | 0.30 | -0.28 | -0.20 |
| simplicity | 0.72 | 0.27 | 0.15 | -0.14 | -0.03 |
| whitespace | 0.64 | 0.74 | 0.60 | -0.26 | -0.25 |
| harmony | 0.63 | 0.29 | 0.11 | -0.25 | 0.02 |
| colorfulness | 0.56 | 0.47 | 0.42 | 0.06 | 0.06 |
| contrast | 0.54 | 0.43 | 0.39 | -0.42 | -0.15 |
| local | 0.39 | 0.39 | 0.48 | -0.13 | 0.10 |
| *feature_congestion* | 0.29 | 0.71 | 0.91 | 0.14 | -0.06 |
| *contour_congestion* | 0.41 | 0.42 | 0.52 | 0.14 | -0.16 |
| *edge_orientation_entropy* | 0.58 | 0.66 | 0.59 | 0.44 | 0.10 |
| *anisotropy* | 0.40 | 0.34 | 0.44 | -0.45 | -0.11 |
| *sequence* | 0.55 | 0.48 | 0.43 | -0.20 | -0.14 |

## 2. Weights fitted to separate acclaimed from ordinary (and both from broken)

Same linear form as the shipped score; weights non-negative, sum to 1; objective 0.6·AUC(acclaimed > ordinary) + 0.4·AUC(all pages > broken), with a penalty whenever the human-rating correlation drops below the shipped weights'. 5-fold cross-validation over the acclaimed set (20 ordinary pages held out per fold).

| | shipped weights | fitted weights |
|---|---:|---:|
| AUC acclaimed > ordinary (cross-validated) | 0.62 | 0.69 |
| AUC acclaimed > ordinary (all data) | 0.60 | 0.64 |
| AUC all > broken | 0.30 | 0.52 |
| ρ vs human rating (398) | -0.08 | -0.08 |
| ρ vs human pairwise rank (100) | -0.40 | -0.15 |

| factor | shipped | fitted |
|---|---:|---:|
| composition | 0.28 | 0.02 |
| alignment | 0.16 | 0.00 |
| simplicity | 0.14 | 0.02 |
| whitespace | 0.10 | 0.27 |
| harmony | 0.10 | 0.10 |
| colorfulness | 0.06 | 0.56 |
| contrast | 0.10 | 0.01 |
| local | 0.06 | 0.01 |

## 3. What acclaimed pages have that ordinary ones don't

| factor | acclaimed median | ordinary median | broken median |
|---|---:|---:|---:|
| composition | 0.63 | 0.70 | 0.73 |
| alignment | 0.19 | 0.22 | 0.29 |
| simplicity | 0.44 | 0.10 | 0.85 |
| whitespace | 1.00 | 0.65 | 0.49 |
| harmony | 0.91 | 0.88 | 0.97 |
| colorfulness | 0.89 | 0.86 | 0.89 |
| contrast | 1.00 | 1.00 | 1.00 |
| local | 0.60 | 0.68 | 0.70 |
| feature_congestion | 0.02 | 0.03 | 0.01 |
| contour_congestion | 0.65 | 0.68 | 0.69 |
| edge_orientation_entropy | 0.90 | 0.88 | 0.84 |
| anisotropy | 0.81 | 0.93 | 1.15 |
| sequence | 0.60 | 0.50 | 0.55 |

## How to read this

- An AUC near 0.5 means the signal cannot tell acclaimed design from a random page; near 1.0 it can.
- The `ui` formula was written from the literature, not fitted; the `web` model was fitted to 398 human ratings of 2013-era sites. Neither has seen the acclaimed set before.
- Fitted weights are only worth shipping if the cross-validated AUC beats the shipped weights *and* the human-rating correlation does not fall — both are printed above; the decision is made in the changelog, not here.
- Acclaim is a designer's judgement (Awwwards, Siteinspire, brand lists); it is not the same target as crowd appeal, and the two disagree on purpose.

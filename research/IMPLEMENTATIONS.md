# Public implementations of "mathematical beauty" — what exists, and what we took from each

Checked 2026-09-20 (GitHub search, PyPI, the repositories themselves). "Relevant" means: it computes
something from pixels that a beauty score for screens could use, or it is a rated dataset a score
can be checked against. Neural predictors are listed because they are the ranking sanity test the
repo still owes itself (issue #20), not because their weights belong in a formula.

## Formula / metric implementations

| project | what it is | measures | licence | status | relation to `beautiful` |
|---|---|---|---|---|---|
| [aalto-ui/aim](https://github.com/aalto-ui/aim) — Aalto Interface Metrics | web service + Python metric classes for GUI screenshots | Miniukovich & De Angeli's set as published: PNG/JPEG size, distinct RGB, contour density, figure-ground contrast, contour congestion, subband entropy, feature congestion, luminance std, LAB/HSV stats, Hasler colourfulness, static/dynamic colour clusters, Cohen-Or harmony, grid quality and white space (need its UIED segmentation), colour-blindness simulation, plus UMSI saliency, NIMA and MD-EAM networks | MIT | maintained (2024) | **the reference implementation for half our terms.** [AIM.md](AIM.md) runs its metric classes on our screenshots and reports where our simplified versions agree. Not a dependency: it needs OpenCV, pyrtools, TensorFlow and a MongoDB-backed server |
| [RBartho/Aesthetics-Toolbox](https://github.com/RBartho/Aesthetics-Toolbox) (Redies lab, Jena) | Streamlit GUI + batch script computing the "quantitative image properties" of empirical aesthetics; DODA, a catalogue of aesthetics datasets | edge-orientation entropy, anisotropy, self-similarity (PHOG), fractal dimension, Fourier slope, colour statistics, symmetry, balance, complexity (Behavior Research Methods 2025) | MIT | maintained | source of our `edge_orientation_entropy`, `anisotropy`, `fractal`, `fourier` terms; second-order entropy and PHOG self-similarity are issue #25 |
| [Gabrock94/pyaesthetics](https://github.com/Gabrock94/pyaesthetics) | Python package, `pip install pyaesthetics` | brightness, contrast, saturation, visual complexity, symmetry, colourfulness, face detection, colour distribution, line ratios | GPL-3.0 | 0.0.8.11, March 2026, Python ≥ 3.10 | overlaps our colour and complexity terms; GPL, OpenCV + tesseract + rembg dependencies, so nothing was taken; a useful independent check on `colorfulness` and `symmetry` |
| [AlexeyGOblov/visual-attention-audit](https://github.com/AlexeyGOblov/visual-attention-audit) | Python; Rosenholtz Feature Congestion and Subband Entropy | the two MIT clutter measures | MIT | new (September 2026) | a standalone port of what our `feature_congestion` approximates and what issue #13 (subband entropy) still needs |
| [alepmaros/birkhoff-aesthetic-shannon-kolmogorov](https://github.com/alepmaros/birkhoff-aesthetic-shannon-kolmogorov) | Birkhoff's M = O/C with Shannon entropy and Kolmogorov (compression) complexity | Rigau, Feixas & Sbert 2008 measures | GPL-3.0 | 2018, unmaintained | the paper behind our `jpeg_bpp` term; the repo is a small script |
| [mtoshevska/MathematicalBeauty](https://github.com/mtoshevska/MathematicalBeauty) | survey statistics on whether people who understand an *equation* find it beautiful | Pearson and chi-square on 49 questionnaires | none | 2019 | not about images; name overlap only |

## Learned predictors (sanity tests, not formula terms)

| project | what it is | trained on | licence | relation |
|---|---|---|---|---|
| [idealo/image-quality-assessment](https://github.com/idealo/image-quality-assessment) — NIMA | MobileNet models predicting a rating distribution | AVA (aesthetics), TID2013 (technical quality); SRCC 0.61 on AVA | Apache-2.0 | archived Dec 2024; the model issue #20 names for a ranking cross-check on photographs (demo/photos) |
| [christophschuhmann/improved-aesthetic-predictor](https://github.com/christophschuhmann/improved-aesthetic-predictor) — LAION aesthetic score | MLP on CLIP ViT-L/14 embeddings | AVA + logos + Simulacra Aesthetic Captions | Apache-2.0 | what image-generation pipelines mean by "aesthetic score"; strong on photographs and art, never validated on UI |
| [carrenD/Webthetics](https://github.com/carrenD/Webthetics) | Caffe CNN with transfer learning from image-style recognition, weights released (IJHCS 2019, Dou, Zheng, Sun & Heng) | Reinecke & Gajos's rated screenshots (the same data as Calista); reports r = 0.85 against ratings vs 0.59 for hand-crafted colourfulness/complexity | none stated | the learned counterpart of our `web` model on the same data, and the ceiling it shows: pixels can predict crowd appeal well, formulas reach about 0.6 |
| UIClip (Wu et al., UIST 2024) | CLIP fine-tuned to rate UI design quality and relevance from a screenshot + description | synthetic defect pairs + designer ratings | model on Hugging Face, no public repo found | its defect-injection recipe is what research/degrade.py reproduces |

## Rated datasets

| dataset | size | ratings | used here |
|---|---|---|---|
| Calista (Reinecke & Gajos 2013/2014 mirror) | 398 rated + 100 pairwise-ranked screenshots | 1–9 appeal, crowd | yes: `web` model fit, ρ constraint in the `ui` fit, "ordinary" set of the bench |
| [nehalotaif/Comprehensive-website-aesthetics-dataset](https://github.com/nehalotaif/Comprehensive-website-aesthetics-dataset) | 1,000 portrait screenshots (922×744) of 963 sites | six automated QUESTIM metrics (saliency balance, border balance, border density, colour density, colourfulness, compression complexity) plus expert ratings 1–5 for consistency, text clarity and overall satisfaction; release pending publication | not yet — the best candidate for a fresh held-out set once released (FIT.md, "data the fit never saw") |
| AVA | 250k photographs | 1–10, photography community | not yet — the bench a photo formula needs (issue #46) |

## What this survey changes

- Our terms are simplifications of published metrics, and for half of them a reference
  implementation exists (AIM). [AIM.md](AIM.md) measures the agreement; where it is low the
  name of our term is the thing to fix.
- Nothing found is a drop-in: the reference implementations carry OpenCV, TensorFlow or GPL, and
  this package promises numpy + pillow + scipy. Ports are welcome, and each has a bench to pass
  (research/fit_ui.py, research/benchmark.py).

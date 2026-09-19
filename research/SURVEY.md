# Computational aesthetics: a landscape survey for grounding a pixel-only beauty score

*This survey is the evidence base for `beautiful`. Every factor in the formula, every weight
decision, and every item in [FACTORS.md](../FACTORS.md) should trace back to something here. Where
the survey and the code disagree, the survey wins and the code gets an issue. Flags marked
"(confirm)" are details found only through secondary sources.*

## TL;DR

- Computational aesthetics has produced ~90 years of "beauty functions", but for **pixel-only
  scoring of UIs, artworks and logos** the strongest replicated predictors are **visual
  complexity/clutter (negative, inverted-U), colourfulness (inverted-U), figure–ground contrast,
  symmetry/balance, and grid/white-space organisation**. Hand-crafted metric sets explain only
  ~30–49 % of aesthetic-rating variance; learned CNN / vision-language models reach r ≈ 0.75–0.85
  on web and mobile UIs.
- The **Birkhoff ratio (M = O/C) and the golden ratio have weak or contradictory empirical
  support** and should be de-emphasised or dropped. By contrast **natural-scene statistics
  (Fourier slope ≈ −2, fractal D ≈ 1.3–1.5) and Rosenholtz feature-congestion clutter are well
  validated** on photos/art and partly on UIs.
- Concrete calibration resources exist: the **Reinecke & Gajos 2014 LabintheWild dataset** (430
  website screenshots, ~40 k raters, 1–9 scale, ~2.4 M ratings, CC BY-NC-SA 3.0), the **Calista**
  and **UIClip / BetterApp** human-rated UI sets, and open code from **AIM (Aalto Interface
  Metrics), the Aesthetics Toolbox, NIMA, the LAION predictor and Webthetics**.

## Key findings

1. **No single closed-form function reliably predicts beauty.** Birkhoff's 1933 M = O/C launched
   the field but its polygon/vase definitions of order and complexity were not empirically
   confirmed; Eysenck's 1941 M = O × C revision fit some data better but neither generalises.
2. **HCI layout metrics (Ngo et al.'s 14 measures) are fully specified formulas** operating on
   element bounding boxes, but replications show only a subset (balance, equilibrium, symmetry,
   sequence) correlate with ratings, with modest effect sizes.
3. **Pixel-level perceptual metrics with independent validation** are the best building blocks:
   Hasler–Süsstrunk colourfulness (r > 0.9 vs human colourfulness ratings), Rosenholtz Feature
   Congestion / Subband Entropy clutter, and the Redies-group statistical image properties (Fourier
   slope, fractal dimension, PHOG self-similarity, anisotropy, edge-orientation entropy).
4. **The two most cited UI-specific hand-crafted models** — Reinecke et al. (CHI 2013,
   colourfulness + complexity, 48 % of variance) and Miniukovich & De Angeli (CHI 2015, eight
   metrics, up to 49 % on webpages / 32 % on apps) — converge on complexity and colourfulness as
   dominant, adding figure–ground contrast, grid quality and white space.
5. **Learned predictors dominate raw accuracy**: NIMA / VILA / Q-Align on photos (AVA SRCC ≈
   0.61–0.82); Webthetics on webpages (r = 0.85 vs 0.59 for hand-crafted colourfulness +
   complexity); UIClip on app design (75.12 % pairwise accuracy). But the widely used LAION
   aesthetic predictor is documented to encode cultural / demographic bias.
6. **For a pixel-only function**, the recommended architecture is a weighted linear blend of
   validated perceptual metrics (with inverted-U terms) calibrated on public UI-rating datasets,
   benchmarked against AIM and a learned model (NIMA / UIClip) as sanity checks.

## 1. Closed-form / theoretical measures

**Birkhoff (1933), *Aesthetic Measure*.** M = O/C. For polygons C = the number of distinct
straight lines containing at least one side, O = a sum of symmetry indicators (vertical symmetry,
equilibrium, rotational symmetry, relation to a horizontal–vertical network) minus unsatisfactory
form. The square scores highest (M = 1.5). Applied to vases, music, poetry. Later experiments
produced contradictory results; the ratio is the historical origin of the field, not a validated
predictor.

**Eysenck (1941)** proposed M = O × C; mid-century tests (Davis 1936; Beebe-Center & Pratt 1937)
found neither form robustly matched human preference orderings. (confirm primary numbers)

**Information aesthetics (Bense, Moles).** Order/complexity recast in Shannon terms — order as
redundancy. Inspired computable measures; not themselves validated against ratings.

**Rigau, Feixas & Sbert (2007/2008), "Informational aesthetics measures", IEEE CG&A.** Birkhoff-type
ratios from Shannon entropy and Kolmogorov (compression) complexity, applied to Mondrian and
Pollock. Descriptive, not validated predictors of rated beauty.

**Machado & Cardoso (1998), "Computing Aesthetic Value".** Aesthetic value ∝ image complexity /
processing complexity, estimated from JPEG / fractal compression ratios. Influential in
evolutionary art; not calibrated on large human datasets. (confirm venue and formula)

**Schmidhuber's compression progress.** Beauty ≈ compressibility; interestingness is its
derivative. Elegant, not a quantitative predictor of rated beauty.

**Berlyne's arousal / inverted-U.** Preference peaks at intermediate complexity — the theoretical
backbone of the inverted-U repeatedly observed in UI studies.

**Fractal / natural-scene preference.** Aks & Sprott (1996) peak near D = 1.3. Spehar, Clifford,
Newell & Taylor (2003), *Computers & Graphics* 27:813–820: across natural images, mathematical
fractals and Pollock crops, preference peaks in D ≈ 1.3–1.5, lower at 1.1–1.2 and 1.6–1.9. Spehar
et al. (2016): inverted-U for the Fourier amplitude-spectrum slope. Caveat: some replications
peak near D ≈ 1.7 and find no D–liking relation for Pollock; the optimum is stimulus-dependent.

**Golden ratio — evidence against.** Fechner's rectangle preference has repeatedly failed to
replicate. Godkewitsch (1974): an artefact of the rectangle's position in the stimulus range.
Stieger & Swami (2015), "Time to let go? No automatic aesthetic preference for the golden ratio in
art pictures": no explicit or implicit preference across three studies. Cross-cultural work
(Korean subjects, n = 277) prefers √2 and shorter ratios. **The golden ratio should carry no
positive weight in a beauty function.**

**Ramachandran & Hirstein (1999)** — eight neurological "laws" (peak shift, grouping, contrast,
isolation, symmetry, abhorrence of coincidence…); heuristics, not formulas.

**Hogarth's line of beauty.** Serpentine vase outlines rated more beautiful than Birkhoff's
measure predicts ("On the beauty of vases").

**Javid et al.** — spatial-complexity / entropy measures from information gain across partitions.

## 2. HCI / UI aesthetics metrics

**Ngo, Teo & Byrne (2000, 2003), "Modelling interface aesthetics", *Information Sciences*
152:25–46.** Fourteen layout measures, each in [0, 1], from element bounding boxes; overall
OM = Σ aᵢ Mᵢ. Balance (optical-weight difference across the axes), equilibrium (centre of mass vs
screen centre), symmetry (quadrant-wise), sequence (weight decreasing UL → UR → LL → LR, quadrant
weights 4/3/2/1), cohesion (aspect-ratio agreement), unity, proportion (closeness to 1:1, 1:√2,
1:1.618, 1:√3, 1:2), simplicity (3 / (alignment points + object count)), density, regularity,
economy, homogeneity (Boltzmann entropy of quadrant allocation), rhythm, order & complexity.
Validations: Zain, Tey & Goh (2008); Salimun et al. (2010); Altaboli & Lin (2011) confirmed
balance, unity and sequence; a 2025 reduction keeps ~7 non-redundant metrics; Bauerly & Liu
(2006/2008) isolated symmetry and balance as the strongest layout drivers.

**Zheng, Chakraborty, Lin & Rauschenberger (2009).** Quadtree decomposition of screenshots into
low-level statistics to predict appeal.

**Reinecke, Yeh, Miratrix, Mardiko, Zhao, Liu & Gajos (CHI 2013).** Colourfulness, visual
complexity and appeal ratings for 450 websites from 548 volunteers. Perceptual models of
colourfulness (Hasler–Süsstrunk-style) and complexity (quadtree / edge / space) plus demographics
**explain 48 % of the variance in appeal after 500 ms**. Complexity is the stronger predictor;
both are inverted-U. Reinecke & Gajos (CHI 2014) is the large public dataset (§5).

**Miniukovich & De Angeli (AVI 2014; CHI 2015, "Computation of Interface Aesthetics").** Eight
automatic GUI metrics: visual clutter, colour range, number of dominant colours, figure–ground
contrast, contour congestion, symmetry, grid quality, white space — grouped into information
amount, information organisation and figure–ground. N = 62 desktop webpages and 53 iPhone apps at
150 ms and 4 s. Best-fit regressions explain **up to 49 % of variance in webpage aesthetics and up
to 32 % for iPhone apps**. Clutter = weighted edge density across Canny thresholds; contour
congestion and contrast from edge / segmentation maps; grid quality from element-edge alignment;
white space = background share.

**Tuch, Presslaber, Stöcklin, Opwis & Bargas-Avila (2012).** Complexity and prototypicality drive
50 ms appeal judgements; higher complexity lowers appeal.

**Lavie & Tractinsky (2004).** Classical vs expressive aesthetics — the standard subjective scale.

**Riegler & Holzmann (2018); Alemerien & Magel; Wu et al.** — mobile complexity metrics, GUI
complexity metrics, visual block decomposition.

**AIM — Aalto Interface Metrics (Oulasvirta et al., UIST 2018 Adjunct).** Open service and MIT
codebase at interfacemetrics.aalto.fi with 17 metrics across colour perception, perceptual fluency
(clutter, symmetry, contour congestion, figure–ground contrast, grid quality, colour variability,
white space) and saliency. The most directly reusable open implementation of §2 metrics.

## 3. Perceptual feature measures

**Colourfulness — Hasler & Süsstrunk (2003), SPIE HVEI VIII.** rg = R − G, yb = ½(R + G) − B;
C = √(σ²_rg + σ²_yb) + 0.3·√(μ²_rg + μ²_yb). Correlation > 0.9 with human colourfulness ratings.
Used verbatim in `beautiful`.

**Clutter — Rosenholtz, Li & Nakano (2007), *Journal of Vision* 7(2):17.** Feature Congestion
(local covariance of luminance, colour and orientation across a Gaussian pyramid, pooled),
Subband Entropy (bits to encode via a steerable pyramid), Edge Density. Correlations with search
set-size: Feature Congestion r = .93, Edge Density r = .83, Subband Entropy r = .68. Feature
Congestion also predicts perceived screen clutter on websites. Bravo & Farid (2008) added a
segmentation-based clutter metric.

**Colour harmony.** Matsuda's hue templates (i, V, L, I, T, Y, X); Cohen-Or et al. (SIGGRAPH 2006)
fit and rotate; Tokumaru fuzzy templates. **O'Donovan, Agarwala & Hertzmann (2011), "Color
Compatibility From Large Datasets", ACM TOG 30(4).** LASSO on 334 features trained on Kuler +
COLOURlovers + MTurk ratings of 5-colour themes; public weights (weights.csv).

**Processing fluency — Reber, Schwarz & Winkielman (2004), PSPR 8(4):364–382.** Pleasure rises
with ease of processing: figural goodness, figure–ground contrast, symmetry, prototypicality,
clarity, amount of information. Why contrast, symmetry and low clutter share a sign.

**Palmer & Schloss (2010), PNAS.** Ecological valence theory — colour preference is
object-mediated, not fixed.

**Redies group + the Aesthetics Toolbox (Redies, Bartho, Koßmann, Spehar, Hübner, Wagemans &
Hayn-Leichsenring, 2025, *Behavior Research Methods* 57(4):117).** Open Python tool: lightness /
colour statistics, complexity (HOG / Gabor edge density), anisotropy, self-similarity (PHOG and
CNN), symmetry and balance, Fourier slope (three implementations), fractal dimension,
edge-orientation entropy (1st and 2nd order), CNN-feature variance, a Birkhoff-like
self-similarity / complexity ratio. Anchors: artworks self-similarity ≈ 0.68, advertisements ≈
0.62, faces ≈ 0.43; edge density vs complexity ρ up to 0.85.

**Graham & Field (2007/2008).** Art shares the 1/f amplitude statistics of natural scenes (slope
≈ −2); Spehar (2016) shows an inverted-U preference peaking around −2 to −3.

**Datta, Joshi, Li & Wang (2006), ECCV.** 56 photo features incl. rule of thirds; ~70 % high/low
classification on Photo.net. **Ke, Tang & Jing (2006), CVPR** — edge distribution, hue count, blur,
contrast. **Luo & Tang (2008); Dhar, Ordonez & Berg (2011)** — composition attributes.

## 4. Learned predictors and datasets

**AVA (Murray, Marchesotti & Perronnin, CVPR 2012).** 255,530 dpchallenge photos, ~210 votes each,
1–10. **NIMA (Talebi & Milanfar, TIP 2018)** predicts the rating distribution with an EMD loss;
AVA SRCC ≈ 0.61. RAPID, DMA-Net, A-Lamp, MP-ada, GPF-CNN precede it. **MUSIQ** (0.726), **VILA**
(CVPR 2023, 0.774), **Q-Align / OneAlign**, **UNIAA** (≈ 0.84), **AesCLIP / AesExpert**,
**AesBench** — the highest photo-domain accuracy, not UI-tuned.

**LAION-Aesthetics predictor.** MLP on CLIP ViT-L/14 embeddings, trained on AVA + SAC + LAION-Logos;
used to filter Stable Diffusion's data. **Audit — Taylor, Agnew, Sap, Fox & Zhu (2025/2026), "The
Algorithmic Gaze".** Favours captions mentioning women, filters out men and LGBTQ+ people, rates
Western and Japanese landscapes and portraits highest; conflates datasets; a majority of SAC /
Logos ratings came from a single annotator. **Do not use as a ground-truth beauty oracle.**

**ImageReward, PickScore, HPS** — human-preference reward models for text-to-image, not UI.

**Iigaya, Yi, Wahle, Tanwisuth & O'Doherty (2021), *Nature Human Behaviour* 5:743–755.** A linear
feature-summation model of low-level (contrast, saturation, hue, brightness, blur) and high-level
features predicts individual art preferences within and across people; low-level features map to
lower CNN layers. **A weighted linear sum of interpretable features is a defensible
architecture.**

**Webthetics (Dou, Zheng, Sun & Heng, 2019), IJHCS 124:56–66.** CaffeNet transfer learning on 398
Reinecke & Gajos screenshots: **r = 0.85 vs r = 0.59 for linear colourfulness + complexity**. Code:
github.com/carrenD/Webthetics. **Khani et al. (2016)**; **"Predicting Rating Distributions of
Website Aesthetics with Deep Learning" (TOCHI 2023)** — AlexNet + SPP, cross-validated LCC 0.752 on
430 stimuli vs 0.498 for a linear model.

**Generated-UI quality.** **UIClip (Wu et al., UIST 2024)** — CLIP fine-tuned on JitterWeb (~2.3 M
synthetic pairs) + BetterApp (1,200 designer pairwise ratings with CRAP labels): 75.12 % overall
design-quality accuracy, beating GPT-4V (51.58 %). **UI-Bench (2025)** — 300 generated sites, 4,000+
blinded expert pairwise judgements, TrueSkill. **Design2Code (NAACL 2025)** — visual-similarity
metrics validated against human ratings. These evaluate pairwise, not absolute pixel-only beauty.

## 5. Synthesis

### Comparison table

| Model / metric | Type | Input | Domain | Validation | Result |
|---|---|---|---|---|---|
| Birkhoff M = O/C (1933) | closed-form | geometry | polygons / vases | none quantitative | not validated / contradicted |
| Eysenck M = O × C (1941) | closed-form | geometry | polygons | small lab tests | mixed |
| Rigau et al. (2007) | entropy / Kolmogorov | pixels | paintings | descriptive | no rated-beauty validation |
| Machado & Cardoso (1998) | compression ratio | pixels | evolutionary art | qualitative | not calibrated |
| Fractal D preference (Spehar 2003) | closed-form | pixels | nature / fractal / Pollock | 220 participants | peak D ≈ 1.3–1.5 |
| Fourier slope (Graham / Spehar) | closed-form | pixels | art / photos | lab | inverted-U, peak ≈ −2 to −3 |
| Golden ratio | closed-form | geometry | rectangles / art | Stieger & Swami 2015 | no reliable preference |
| Ngo et al. (2003) | 14 box measures | element boxes | UI | Altaboli & Lin 2011 | subset significant; modest |
| Reinecke et al. (2013) | hand-crafted linear | pixels | websites | 450 sites, 548 raters | 48 % of appeal variance |
| Miniukovich & De Angeli (2015) | 8 metrics | pixels | web + iPhone | 62 web / 53 apps | ≤ 49 % web, ≤ 32 % app |
| Hasler–Süsstrunk (2003) | perceptual | pixels | natural images | scaling experiment | r > 0.9 |
| Rosenholtz clutter (2007) | perceptual | pixels | displays / scenes | search experiments | FC r = .93 |
| O'Donovan et al. (2011) | LASSO, 334 features | colour theme | colour themes | Kuler + COLOURlovers | predicts theme rating |
| Iigaya et al. (2021) | linear feature sum | pixels + labels | art | own set | predicts individual preference |
| Aesthetics Toolbox (2025) | perceptual suite | pixels | art / photos | various | ρ up to 0.85 between properties |
| AVA + NIMA | CNN | pixels | photos | AVA 255,530 | SRCC ≈ 0.61 |
| VILA (2023) | VLM | pixels | photos | AVA | SRCC 0.774 |
| LAION predictor | MLP on CLIP | pixels | generative images | AVA / SAC / Logos | biased (audit 2025) |
| Webthetics (2019) | CNN | pixels | webpages | Reinecke & Gajos 398 | r = 0.85 (vs 0.59 hand-crafted) |
| UIClip (2024) | CLIP | pixels | app / web UI | BetterApp | 75.12 % pairwise |
| Calista (2023) | CNN | pixels | websites | Reinecke & Gajos + own | r = 0.78 / 0.70 |
| Appsthetics (2024) | ResNet-50 | pixels | mobile GUI | 820 App Inventor GUIs | ρ ≈ 0.9 |
| Rating-distribution CNN (2023) | AlexNet + SPP | pixels | websites | 430 stimuli | LCC 0.752 |

### Factors ranked by strength of replicated evidence (UIs)

**Strong:** 1. visual complexity / clutter (negative, inverted-U) · 2. colourfulness (inverted-U)
· 3. figure–ground contrast · 4. symmetry & balance · 5. grid quality / alignment / white space.
**Moderate:** 6. natural-scene statistics (Fourier slope, fractal D) — strong for art, less tested
on UI · 7. colour harmony — good on themes, indirect for full UIs.
**Weak / contradictory (drop):** golden ratio and "pleasing proportions"; Birkhoff O/C; rule of
thirds for UI layout (fine for photos).

### Preferred ranges

Fourier slope ≈ −2 (preference peak −2 to −3) · fractal D 1.3–1.5 · complexity and
colourfulness intermediate · few dominant colours · more white space is generally positive ·
symmetry / balance higher is better up to a point.

### Weights / coefficients to reuse

No portable coefficient vector exists. Reinecke 2013 (complexity > colourfulness, quadratic
terms, R² ≈ 0.48); Miniukovich 2015 (clutter, colour variability, contrast dominate, R² ≤ 0.49);
Ngo replications (concentrate on balance, equilibrium, symmetry, sequence); O'Donovan public
LASSO weights; Iigaya's linear form. **Practical recommendation: fit your own ridge / LASSO with
quadratic terms for complexity and colourfulness on a public UI-rating dataset.** →
[CALIBRATION.md](CALIBRATION.md).

### Public UI / web aesthetic-rating datasets

- **Reinecke & Gajos 2014 (CHI '14)** — 2.4 M ratings from ~40 k participants on 430 websites (398
  after preprocessing), 1–9 appeal; labinthewild.org/data; CC BY-NC-SA 3.0. The primary
  calibration set.
- **Calista (Delitzas, Chatzidimitriou & Symeonidis, 2023, IJHCS 175:103019)** — the rating set
  above plus 100 Alexa-top-5000 pages with 5,094 pairwise comparisons from 174 users
  (Bradley–Terry); github.com/calista-ai/website-aesthetics-datasets.
- **Appsthetics (Lima et al., 2024)** — 820 App Inventor screenshots, 5-point beauty scale
  (extended 3,139 incl. Rico); ResNet-50 ρ ≈ 0.9. (confirm rater count and licence)
- **UIClip BetterApp + JitterWeb (UIST 2024)** — Hugging Face biglab/uiclip. (confirm licence)
- **Xing et al. (2022)** — 12,186 UI images with views / likes as implicit ground truth; no public
  download found.
- **Rico (UIST 2017)** — 72,219 Android screens with view hierarchies; no aesthetic ratings.

### Open-source implementations to compare against

AIM (interfacemetrics.aalto.fi, MIT) · Aesthetics Toolbox (Redies 2025) · NIMA
(idealo/image-quality-assessment) · LAION predictor (with the bias caveat) · Webthetics · Calista
engine · UIClip · Hasler–Süsstrunk reference implementations · Rosenholtz clutter toolbox (MIT
CVCL; bundled in AIM).

## Recommendations

**Stage 1 — build on validated perceptual primitives.** A weighted linear blend (with inverted-U
terms) of: Hasler–Süsstrunk colourfulness; Rosenholtz Feature Congestion + Subband Entropy + edge
density; figure–ground contrast and contour congestion; symmetry, balance, equilibrium; grid
quality, regularity, white space; colour count / economy; O'Donovan colour harmony; Fourier slope
and fractal D as mild bonus terms. **Drop the golden ratio and any pure Birkhoff term.**

**Stage 2 — calibrate on public human ratings.** Ridge / LASSO from the metrics to the Reinecke &
Gajos ratings, cross-validated, plus Calista and Appsthetics for transfer. Decision rule: if a
learned model reproducibly beats the linear blend by > 0.15 in ρ, add a learned residual head but
keep the interpretable model as the default.

**Stage 3 — validate and guard against bias.** Cross-check against AIM and NIMA / UIClip; audit for
LAION-style demographic bias before shipping any learned component. Target cross-validated
Spearman ρ ≥ 0.7 on held-out UI screenshots; below ρ ≈ 0.5, treat the output as advisory only.

**Stage 4 — for AI-generated UI / logo scoring**, evaluate with blinded pairwise comparisons in the
spirit of UI-Bench rather than absolute scores.

## Caveats

- Even the best hand-crafted UI models top out near 48–49 % of rating variance; roughly half of
  perceived beauty is content, semantics, brand, prototypicality and individual / cultural taste
  that pixels cannot capture.
- Optima are stimulus- and culture-dependent (fractal D, Fourier slope, proportions, colour).
- Learned models carry bias and provenance problems; AVA is competition photography; some VLM
  numbers risk contamination. No learned score is ground truth.
- Details flagged "(confirm)" need direct confirmation against the primary source.
- Element-box metrics (Ngo) require segmentation; a pure-pixel function must use pixel proxies.

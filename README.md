<h1 align="center">beautiful</h1>

<p align="center"><strong>A beauty number, 1–100, for any screenshot, logo or artwork — from pixels alone.</strong><br>
Built so AI coding agents can <em>see</em> what they ship, and fix it.</p>

<p align="center">
  <a href="https://github.com/solomonBoltin/beautiful/actions/workflows/ci.yml"><img alt="ci" src="https://github.com/solomonBoltin/beautiful/actions/workflows/ci.yml/badge.svg"></a>
  <a href="LICENSE"><img alt="MIT" src="https://img.shields.io/badge/license-MIT-2ea44f"></a>
  <img alt="python" src="https://img.shields.io/badge/python-3.9%E2%80%933.13-blue">
  <img alt="deps" src="https://img.shields.io/badge/deps-numpy%20%C2%B7%20pillow%20%C2%B7%20scipy-lightgrey">
  <img alt="weights" src="https://img.shields.io/badge/model%20weights-none-success">
</p>

```python
from beautiful import beauty

r = beauty("screenshot.png", mode="ui")
r["score"]    # 82
r["factors"]  # {'composition': 0.74, 'alignment': 0.26, 'simplicity': 0.76, 'whitespace': 0.91, ...}
r["hints"]    # ['alignment (0.26): snap element edges to a shared column/row grid', ...]
```

## Why

Your coding agent is great at logic and blind to looks. It never sees the page it just built, so it
edits CSS by guesswork and ships the lopsided, cramped, off-grid screens every vibe coder knows.

`beautiful` gives it eyes for **form**. One number to hill-climb, and a breakdown that says *which*
property is wrong — composition, alignment, white space, colour harmony, contrast — with a hint on
what to change. Every term is an explicit formula with a target range from the experimental-aesthetics
and HCI literature. No model weights, no network, no dataset.

```
render  →  beauty()  →  read the hints  →  edit  →  repeat
```

## Install

```bash
pip install git+https://github.com/solomonBoltin/beautiful
```

Python 3.9+. Pulls in `numpy`, `pillow`, `scipy` and nothing else.

## 30 seconds

```bash
beautiful screenshot.png                     # score, every factor, and the hints
beautiful --mode=art a.jpg b.jpg c.png       # several images, scores only
beautiful --json screenshot.png              # the full report as JSON
beautiful --min 70 screenshot.png            # exit 1 below 70 — a CI gate
```

```
 82  screenshot.png
      composition   0.74
      alignment     0.26
      simplicity    0.76
      whitespace    0.91
      harmony       1.00
      contrast      1.00
  ->  alignment (0.26): snap element edges to a shared column/row grid
```

Modes: **`ui`** (screens, pages, apps), **`art`** (paintings, photos, posters), **`logo`** (marks, icons).
Input can be a path, a `PIL.Image`, or a numpy array.

## Use it with your AI coding agent

The intended user is not you — it is the agent editing your UI. Give it the loop:

**Claude Code** — drop [`skills/beautiful/SKILL.md`](skills/beautiful/SKILL.md) into your project's
`.claude/skills/beautiful/` (or `~/.claude/skills/`). It triggers on any UI change and runs the loop
until the score stops moving.

**Cursor / Codex / Copilot / anything else** — paste this into your rules file (`AGENTS.md`,
`.cursorrules`, `CLAUDE.md`):

```md
After any change that renders something, screenshot it at 1280×800 and run
`beautiful --mode=ui shot.png`. Read the hints. Make one edit for the top hint,
re-render, re-score. Stop when the score stops moving. Report before/after.
```

**In CI** — fail the build when a screenshot regresses:

```bash
beautiful --mode=ui e2e/screens/*.png --min 70
```

The score is smooth enough to optimise. A card whose button drifts off centre:

| button offset | beauty (ui) |
|---:|---:|
| 160 px | 40 |
| 80 px | 43 |
| 40 px | 68 |
| 0 px | 88 |

[`demo/capture_and_score.py`](demo/capture_and_score.py) is a minimal driver (headless Chromium →
PNG → score).

---

## Demo: beauty numbers for real UI screenshots

Live pages captured headlessly at 1280×800. Two captures came through **without CSS** because the
sandbox blocked their asset CDNs; they are kept, labelled, as raw-HTML anchors.

![UI gallery](demo/ui_gallery.png)

| beauty | screen | composition | alignment | simplicity | whitespace | harmony | colour | contrast |
|---:|---|---:|---:|---:|---:|---:|---:|---:|
| **90** | Pinkas — documents (built with beautiful) | 0.82 | 0.63 | 0.85 | 0.74 | 1.00 | 0.93 | 1.00 |
| **85** | crates.io — search results (live) | 0.72 | 0.69 | 0.67 | 0.60 | 0.92 | 0.93 | 1.00 |
| **85** | Pinkas — new-document dialog | 0.97 | 0.32 | 0.75 | 0.35 | 0.94 | 0.91 | 0.95 |
| **82** | Digital Office — rebalanced mock | 0.98 | 0.32 | 0.77 | 0.25 | 0.96 | 0.96 | 0.76 |
| **82** | npmjs.com — CSS blocked (unstyled) | 0.70 | 0.23 | 0.86 | 0.90 | 1.00 | 0.90 | 1.00 |
| **82** | Pinkas — dashboard | 0.74 | 0.26 | 0.76 | 0.91 | 1.00 | 0.97 | 1.00 |
| **77** | crates.io — crate page (live) | 0.75 | 0.52 | 0.58 | 0.29 | 0.87 | 0.95 | 1.00 |
| **77** | crates.io — home (live) | 0.67 | 0.26 | 0.61 | 1.00 | 0.92 | 1.00 | 1.00 |
| **75** | PyPI — home (live) | 0.75 | 0.22 | 0.67 | 0.98 | 0.98 | 0.23 | 1.00 |
| **73** | PyPI — search results (live) | 0.91 | 0.40 | 0.75 | 0.27 | 0.79 | 0.99 | 0.37 |
| **68** | PyPI — project page (live) | 0.62 | 0.29 | 0.64 | 0.72 | 0.97 | 0.25 | 1.00 |
| **59** | Synthetic asymmetric UI sample | 0.08 | 0.61 | 0.86 | 0.48 | 0.94 | 1.00 | 1.00 |
| **51** | Digital Office — original screenshot (sidebar + off-centre modal) | 0.22 | 0.39 | 0.56 | 0.48 | 0.90 | 0.97 | 1.00 |
| **38** | github.com/login — CSS blocked (unstyled) | 0.05 | 0.31 | 1.00 | 0.07 | 1.00 | 0.88 | 1.00 |

What the numbers say, and where they are honest about their limits:

- The same product, re-composed (Digital Office 51 → 82), moves mostly on **composition** — the
  sidebar and docked modal put all the visual weight on one side.
- Production pages land at 68–85. Their weak factor is usually **alignment**: real pages have many
  container edges at many x-positions, and the metric rewards layouts that a few grid lines explain.
- The unstyled GitHub login (38) is caught by empty **whitespace** and left-anchored **composition**.
  The unstyled npm page (82) is *not* caught: a giant wordmark centred on white is, pixel-wise, a
  minimalist splash page. The function measures form, not intent.
- **contrast** saturates at 1.0 for most screens because modern UIs already meet it; it only bites
  on low-contrast designs (PyPI search results: 0.37).

### Art / logo modes

| beauty (art) | beauty (logo) | image | composition | harmony | simplicity | fractal D | Fourier α | thirds |
|---:|---:|---|---:|---:|---:|---:|---:|---:|
| **85** | 90 | radial mandala | 0.97 | 0.87 | 0.81 | 1.64 | −2.43 | 0.06 |
| **82** | 96 | shield logo | 0.93 | 0.99 | 0.25 | 1.23 | −2.78 | 0.41 |
| **69** | 96 | checkerboard | 0.97 | 1.00 | 0.82 | 1.81 | −2.16 | 0.00 |
| **67** | 95 | bilateral leaf | 0.92 | 0.97 | 0.21 | 1.11 | −2.69 | 0.55 |
| **48** | 18 | random coloured blobs | 0.06 | 0.57 | 0.35 | 1.40 | −2.73 | 0.26 |
| **47** | 54 | diagonal composition | 0.02 | 0.92 | 0.22 | 1.15 | −2.78 | 0.26 |
| **42** | 37 | abstract splashes | 0.05 | 0.92 | 0.30 | 1.32 | −2.72 | 0.15 |
| **5** | 17 | random noise | 0.05 | 0.38 | 0.00 | 2.00 | 0.01 | 0.00 |

The modes disagree on purpose: the checkerboard is a fine *logo* (96) and a dull *artwork* (69) — its
fractal dimension (1.81) is far from the 1.3–1.5 band people prefer, and it has no focal point near a
rule-of-thirds power point.

---

## The formula

```
beauty = spread( Σ_k  w_k[mode] · goodness_k )        goodness_k ∈ [0,1],  Σ w_k = 1
spread(x) = 1 + 99 · σ(8·(x − 0.55))                  mild S-curve so mid-values separate
```

Each `goodness_k` maps a raw pixel measurement through a *target curve*: a ramp when "more is
better" up to saturation, a bell when the literature says people prefer an intermediate value.

| factor | raw measurement (pixels only) | target curve (ui) | descends from |
|---|---|---|---|
| **composition** | mirror correlation about the vertical (and, weaker, horizontal) axis at a fine scale and a blurred *structural* scale; edge-weighted centre-of-mass offset (balance/equilibrium); 3×3 local tile symmetry | `symmetry_report()` score / 100 | Birkhoff 1933 order term; Ngo et al. 2003 *balance, equilibrium, symmetry*; Bauerly & Liu; Zheng et al. 2009 |
| **alignment** | only edge runs ≥ 20 px count (borders, column edges — text is ignored); share of that energy explained by the 8 strongest vertical / 16 strongest horizontal lines | ramp; low prior if the page has no structural lines | Miniukovich & De Angeli 2015 *grid quality*; Ngo *regularity*; Gestalt alignment |
| **simplicity** | Sobel edge density; JPEG bytes-per-pixel at q75 (Kolmogorov-complexity proxy); number of dominant colours (8-level quantised, > 1 % of pixels) | ramps: fewer edges / bytes / colours → higher | Reinecke & Gajos 2013; Rosenholtz 2007; Rigau, Feixas & Sbert 2008; Miniukovich 2014 |
| **whitespace** | share of pixels within a small colour distance of the dominant (background) colour | bell centred at 0.62 ± 0.22 | Miniukovich & De Angeli 2015 *white space* |
| **harmony** | saturation-weighted hue histogram fitted to the Matsuda/Cohen-Or templates *i, V, L, I, T, Y, X* over all rotations, wider templates penalised; greyscale ⇒ *N* | best-fit coverage | Cohen-Or et al. 2006; Matsuda; Itten |
| **colourfulness** | Hasler–Süsstrunk opponent-colour metric; in `ui` mode the *std* term (colour variety) only, so one bold hero colour is not "many colours" | bell 25 ± 45 (ui), 55 ± 35 (art) | Hasler & Süsstrunk 2003; Reinecke & Gajos 2013 |
| **contrast** | 75th-percentile luminance gradient at edges (figure–ground) | ramp 0.30 → 0.80 | Miniukovich; Reber, Schwarz & Winkielman 2004 |
| **fractal** (art) | box-counting dimension of the edge map | bell 1.4 ± 0.25 | Taylor et al.; Spehar et al. |
| **fourier** (art) | slope of the radially averaged log power spectrum | bell −2.5 ± 0.8 | Graham & Field; Redies et al.; Spehar 2016 |
| **thirds** (art) | edge mass inside a Gaussian around the best rule-of-thirds power point | ramp 0.10 → 0.35 | Datta et al. 2006 |

Weights (`beautiful.WEIGHTS`):

```
ui   : composition .28  alignment .16  simplicity .14  whitespace .10  harmony .10  contrast .10  colourfulness .06  local .06
art  : composition .18  harmony .16  simplicity .14  thirds .12  colourfulness .10  contrast .10  fractal .10  fourier .10
logo : composition .40  simplicity .20  harmony .12  contrast .10  economy .10  whitespace .08
```

`composition` is itself a research-shaped blend: in `ui` mode left/right symmetry gets 0.8 of the
mirror weight (a sidebar is top/bottom-uniform, which nobody reads as "composed"), local tile
symmetry is measured on a blurred structural map so text doesn't count, and top-heaviness is
discounted because screens scroll.

---

## Research: what the world has tried

### 1. Closed-form measures (1933 →)

- **Birkhoff (1933), *Aesthetic Measure*.** Birkhoff defined aesthetic measure as the ratio of order O to complexity C; complexity is the effort perception demands, order the harmony and symmetry that reward it. He applied it to polygons, vases, music and poetry. It is the ancestor of everything below, but later psychological studies found little empirical support for M = O/C as stated, and Eysenck's experiments suggested the relation should be direct rather than inverse: M = O × C. `beautiful` keeps Birkhoff's shape — order terms add, complexity terms are bell-shaped rather than purely negative.
- **Bense / Moles → Rigau, Feixas & Sbert (2007, 2008), *Informational Aesthetics Measures*.** Bense reread Birkhoff through information theory; Rigau et al. define ratios based on Shannon entropy and Kolmogorov complexity — order as the algorithmic reduction of the palette's initial uncertainty — and apply them to Mondrian, Pollock and van Gogh. Our JPEG bytes-per-pixel term is the standard cheap Kolmogorov proxy.
- **Machado & Cardoso (1998), *Computing Aesthetics*** — image-complexity ratios from compression, the same lineage.

### 2. Interface-aesthetics metric sets

- **Ngo, Teo & Byrne (2003), *Modelling interface aesthetics*.** Fourteen layout measures — balance, equilibrium, symmetry, sequence, cohesion, unity, proportion, simplicity, density, regularity, economy, homogeneity, rhythm, and order/complexity — computed from element bounding boxes. Balance is the difference in total weight on each side of the axes; equilibrium the offset of the centre of mass from screen centre. Later regressions found balance, unity and sequence the most predictive terms; a 2025 reduction keeps seven (density, symmetry, balance, proportionality, uniformity, simplicity, sequence). Ngo needs element boxes; `beautiful` computes the same ideas from pixels so it works on any screenshot.
- **Zheng, Chakraborty, Lin & Rauschenberger (2009).** Pages are decomposed by minimum-entropy quadtree, then symmetry, balance and equilibrium of the leaves are correlated with 500 ms aesthetic judgements. Balance is the optical weight on either side of an axis; equilibrium the centring of elements on the midpoint.
- **Reinecke, Yeh, Miratrix, Mardiko, Zhao, Liu & Gajos (CHI 2013).** Ratings of colourfulness, complexity and appeal for 450 websites from 548 volunteers; perceptual models of colourfulness and visual complexity plus demographics explain about half the variance in first-impression appeal. Their finding that complexity is the strongest first-impression driver sets the sign of our `simplicity` term.
- **Miniukovich & De Angeli (2014, CHI 2015), *Computation of Interface Aesthetics*.** Eight pixel-level metrics — visual clutter, colour range, dominant colours, figure-ground contrast, contour congestion, symmetry, grid quality, white space — tested on desktop pages and iPhone apps, explaining up to 49 % of variance in webpage aesthetics. Their symmetry counted contour pixels with a mirror counterpart across the vertical axis. This is the closest prior work to `beautiful`'s UI mode; several of our factors are re-implementations of theirs.
- **Bauerly & Liu (2006/2008)** validated that people judge symmetry and balance consistently in both axes, justifying quantification.

### 3. Perception-side measures

- **Hasler & Süsstrunk (2003), colourfulness** — opponent channels rg = R−G, yb = ½(R+G)−B; C = σ_rgyb + 0.3·μ_rgyb, fitted to a psychophysical study. Used verbatim.
- **Rosenholtz, Li & Nakano (2007), visual clutter** — Feature Congestion (local covariance of colour, orientation, contrast) and Subband Entropy (bits to encode via steerable pyramids), the latter born from the observation that JPEG file size tracked feature congestion. Our clutter proxies follow that shortcut.
- **Cohen-Or et al. (SIGGRAPH 2006), *Color Harmonization*** — eight hue templates (i, V, L, I, T, Y, X, N) after Matsuda/Itten; colours in the grey sectors are harmonic, templates rotate freely. Our `harmony` is the coverage of the best-fitting rotated template.
- **Reber, Schwarz & Winkielman (2004), processing fluency** — beauty is the ease of processing: symmetry, figure–ground contrast, prototypicality and less information all raise fluency and liking. This is the theoretical reason `contrast`, `simplicity` and `composition` share a sign.
- **Redies, Graham & Field, Taylor, Spehar — natural-scene statistics of art.** Large subsets of Western and East Asian art have a near scale-invariant Fourier spectrum with slope ≈ −2, like natural scenes; observers prefer random-phase images with slopes between −2 and −3 in an inverted-U; artworks also show intermediate complexity, high self-similarity and fractal dimensions around 1.3–1.5. The Redies group's open *Aesthetics Toolbox* implements these. Our `art` mode uses fractal dimension and Fourier slope with those targets.
- **Datta, Joshi, Li & Wang (2006)** — 56 hand-crafted photo features including rule of thirds, the source of our `thirds` term.
- **Iigaya, Yi, Wahle, Tanwisuth & O'Doherty (Nature Human Behaviour 2021)** — aesthetic preference for paintings is predicted by a weighted integration of low- and high-level features, and a CNN trained only on object recognition encodes many of them; the strongest evidence that a linear feature mixture (which is what `beautiful` is) captures a real share of taste.

### 4. Learned predictors (2012 →)

- **AVA (Murray et al. 2012)** — ~255 000 dpchallenge photos with rating distributions; the benchmark for photo aesthetics.
- **NIMA (Talebi & Milanfar, Google 2017)** — CNN predicting the rating *distribution* with an EMD loss; open implementation at idealo/image-quality-assessment.
- **LAION-Aesthetics predictor (Schuhmann 2022)** — a linear head on CLIP ViT-L/14 embeddings trained on AVA + SAC + LAION-Logos; used to filter Stable Diffusion's training data (score > 0.5). A 2025 audit found it was built to one person's taste and skews what it filters in.
- **Webthetics (Dou, Zheng, Sun, Heng 2019)** — CNN on 398 LabintheWild webpage screenshots rated by ~40 000 users: r = 0.85 vs r = 0.59 for hand-crafted colourfulness + complexity regression. **Calista (Delitzas et al. 2023)** and **Appsthetics (Lima et al. 2024)** extend this to pairwise-comparison datasets and mobile GUIs.
- **VILA, Q-Align, UNIAA (2023–24)** — vision-language aesthetic assessors that also explain their scores in words.

**Why `beautiful` is closed-form anyway.** Learned predictors score higher on their own benchmarks
but return a number without a reason, inherit the taste of their raters, and can't be steered
factor-by-factor. For an *agent that must edit a design*, a transparent mixture whose terms are the
very properties the agent controls (alignment, balance, palette size, contrast) is the useful tool —
and Iigaya et al. show such a mixture is not a toy. The two are complementary: use `beautiful` for
the inner optimisation loop, a learned model for a final sanity check.

---

## Validation

- `tests.py` — five ordering invariants (rebalanced > original by ≥ 15; unstyled < 45; centred dialog ≫ asymmetric sample; mandala > splashes > noise; logo shield ≫ diagonal). CI runs them on Linux, macOS and Windows, Python 3.9–3.13.
- The composition module alone was validated on a labelled symmetry set (perfect / medium / asymmetric tiers, Spearman ρ = 0.96 against tier) and a synthetic gallery (ρ = 0.92 against an a-priori ranking).
- Not validated against human appeal ratings. Doing that properly means Reinecke & Gajos's 398-page dataset or Calista's pairwise set, then fitting the weights — the obvious next step, and the honest gap between this and Webthetics-class numbers.

## Limitations

- Pixels only: no semantics. A centred wreck scores like a centred splash page (see npm above).
- Text is treated as texture; typography quality is invisible to it.
- Weights are literature-shaped, not fitted. Treat the absolute number as a scale, the ordering and the factor breakdown as the signal.
- `ui` mode assumes a screenshot of a viewport; full-page captures of very tall pages should be scored in viewport-sized slices.

## Layout

```
beautiful/
  core.py          beauty(), beauty_score(), WEIGHTS, target curves, hints
  features.py      colourfulness, harmony, complexity, whitespace, alignment, contrast, fractal, fourier, thirds
  symmetry.py      composition: mirror / rotational / local symmetry, balance (ui + generic modes)
  __main__.py      the `beautiful` CLI
skills/beautiful/  a drop-in skill for Claude Code and similar agents
demo/
  screens/         the UI screenshots scored above       art/   the art/logo samples
  results_ui.md    results_art.md   results_ui.json      ui_gallery.png   make_gallery.py
  screenshot_url.js  screenshot_file.js  capture_and_score.py  package.json
tests.py
```

## Roadmap

- [ ] Fit the weights to a public human-rating dataset and report held-out correlation
- [ ] A JavaScript/TypeScript port for the browser and Playwright
- [ ] An MCP server so any agent can call `beauty()` as a tool
- [ ] A GitHub Action that scores every screenshot a PR adds
- [ ] Publish to PyPI

See [CONTRIBUTING.md](CONTRIBUTING.md) — screenshots that break the score are the most useful thing
you can send.

## License

[MIT](LICENSE) © 2026 Solomon Bolotin. Made at [Bina Solutions](https://www.bina-solutions.co.il/),
where it keeps the [Digital Office](https://www.bina-solutions.co.il/) screens honest.

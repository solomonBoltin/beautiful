<h1 align="center">beautiful</h1>

<p align="center"><strong>A mathematical beauty score, 1–100, for any screenshot, logo or artwork.</strong><br>
Computed from pixels with explicit, inspectable formulas. No model, no dataset, no opinion you can't read.</p>

<p align="center">
  <a href="https://solomonboltin.github.io/beautiful/"><img alt="try it in your browser" src="https://img.shields.io/badge/try%20it-in%20your%20browser-7c8cff"></a>
  <a href="https://github.com/solomonBoltin/beautiful/actions/workflows/ci.yml"><img alt="ci" src="https://github.com/solomonBoltin/beautiful/actions/workflows/ci.yml/badge.svg"></a>
  <a href="https://pypi.org/project/beautiful-score/"><img alt="pypi" src="https://img.shields.io/pypi/v/beautiful-score?color=2ea44f&label=pypi"></a>
  <a href="LICENSE"><img alt="MIT" src="https://img.shields.io/badge/license-MIT-2ea44f"></a>
  <img alt="python" src="https://img.shields.io/badge/python-3.9%E2%80%933.13-blue">
  <img alt="weights" src="https://img.shields.io/badge/model%20weights-none-success">
</p>

<p align="center"><img src="demo/loop.gif" width="720" alt="A sign-in card whose button walks back to centre while the beauty score climbs from 54 to 91"></p>

```python
from beautiful import beauty

r = beauty("screenshot.png", mode="ui")
r["score"]    # 82
r["factors"]  # {'composition': 0.74, 'alignment': 0.26, 'simplicity': 0.76, 'whitespace': 0.91, ...}
r["hints"]    # ['alignment (0.26): snap element edges to a shared column/row grid', ...]
```

**Beauty has structure.** Symmetry and balance, alignment to a grid, the right amount of white
space, a harmonic palette, crisp figure–ground contrast, intermediate complexity. Ninety years of
experimental aesthetics and HCI research measured each of these and found the ranges people
prefer. `beautiful` turns those findings into one formula: every term is a pixel measurement mapped
through a documented target curve, weighted, and summed. You can read every line of it, argue with
it, and improve it.

## Install

```bash
pip install beautiful-score
```

Python 3.9+, pulls in `numpy`, `pillow`, `scipy` and nothing else. Or **[try it in your browser](https://solomonboltin.github.io/beautiful/)** — the same package running on Pyodide, your image never leaves the tab.

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

## Famous sites, scored

Twenty well-known home pages captured at 1280×800 on 2026-09-19 and scored with `--mode=ui`.
Four captures came back blank or blocked and were dropped. Full table with every factor:
[`demo/results_famous.md`](demo/results_famous.md); reproduce with `python demo/famous.py`.

![Famous sites scored](demo/famous_sites.png)

| beauty | site | what the formula sees |
|---:|---|---|
| **85** | apple.com | one centred object, symmetric, calm palette, lots of air |
| **66** | news.ycombinator.com | the best **alignment** in the set (0.70, one column grid), but no composition to speak of |
| **64** | notion.com | centred hero, but only 31 % background and many container edges |
| **61** | google.com | perfectly simple, yet the logo/search box sit high: 9 % white space in the formula's eyes |
| **60** | craigslist.org | balanced and airy; the densest edge map in the set (**simplicity** 0.11) |
| **54** | github.com | left-weighted hero, low grid quality |
| **39** | tailwindcss.com | strong left anchoring (**composition** 0.13) |
| **30** | vercel.com | a near-empty viewport with one text block bottom-left |
| **26** | stripe.com | the diagonal gradient wipes out symmetry and sends colourfulness off the chart |
| **16** | amazon.com | maximum edge density, 10 % background, 0.07 colour restraint |

The ranking is not a ranking of good websites. It is a ranking of *form in a single viewport*:
Apple's splash wins because the formula measures composition, not conversion. Craigslist beats
Stripe because Craigslist is symmetric and Stripe's hero is a diagonal. That is exactly the point —
the number is explainable, and every disagreement you have with it is a factor waiting to be
proposed (see below).

## Use it from your editor, agent or CI

**MCP server** — two tools, `beauty_score` and `beauty_compare`, for Claude Code, Cursor, Windsurf
and any MCP client. Zero extra dependencies.

```bash
claude mcp add beautiful -- beautiful-mcp
```
```json
{ "mcpServers": { "beautiful": { "command": "beautiful-mcp" } } }
```

**Claude Code skill** — copy [`skills/beautiful/`](skills/beautiful/) into `.claude/skills/`. It
runs the render → score → read hints → edit loop after any UI change.

**GitHub Action** — score the screenshots your E2E suite already produces and get the table as a
PR comment:

```yaml
- uses: solomonBoltin/beautiful@v0.2.0
  with:
    images: "e2e/screens/*.png"
    min: 60          # optional: fail the job below this
```

**Any agent** — one line in `AGENTS.md` / `.cursorrules`:

```md
After any change that renders something, screenshot it at 1280×800, run `beautiful --mode=ui shot.png`,
fix the top hint, re-score. Stop when the score stops moving. Report before/after.
```

The score is smooth enough to optimise (the GIF above is a real trace: 54 → 91 as a button walks
back to centre). [`demo/capture_and_score.py`](demo/capture_and_score.py) is a minimal driver.

---

## Demo: real UI screenshots

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

## Make the score better — propose a factor

The formula is deliberately incomplete. Rhythm, proportion, typographic hierarchy, focal-point
count, accent-colour discipline, negative-space shape: none of these are in it yet, and each is
measurable from pixels. **[FACTORS.md](FACTORS.md)** is the wishlist with a starting point for
each. To propose one, open a [factor proposal](https://github.com/solomonBoltin/beautiful/issues/new?template=1-propose-a-beauty-factor.yml)
— an idea with a source and two images the current score gets wrong is enough; you don't have to
implement it. To disprove one, open a [counterexample](https://github.com/solomonBoltin/beautiful/issues/new?template=2-score-is-wrong.yml).

Rules: pixels only (numpy / PIL / scipy, no DOM, no learned models), a cited target range, and the
demo table must move in the right direction. Every factor that lands gets a line in the table
above with your name on the source.

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
factor-by-factor. A transparent mixture whose terms are the very properties a designer controls
(alignment, balance, palette size, contrast) can be read, argued with and improved — and Iigaya et
al. show such a mixture is not a toy. The two are complementary: use `beautiful` for the inner
optimisation loop, a learned model for a final sanity check.

---

## Validation

- `tests.py` — five ordering invariants (rebalanced > original by ≥ 15; unstyled < 45; centred dialog ≫ asymmetric sample; mandala > splashes > noise; logo shield ≫ diagonal). CI runs them on Linux, macOS and Windows, Python 3.9–3.13.
- The composition module alone was validated on a labelled symmetry set (perfect / medium / asymmetric tiers, Spearman ρ = 0.96 against tier) and a synthetic gallery (ρ = 0.92 against an a-priori ranking).
- Not validated against human appeal ratings. Doing that properly means Reinecke & Gajos's 398-page dataset or Calista's pairwise set, then fitting the weights — the obvious next step, and the honest gap between this and Webthetics-class numbers. **This is the single most valuable pull request the project can receive.**

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
  mcp_server.py    the `beautiful-mcp` MCP server (dependency-free)
action.yml         the GitHub Action (+ .github/scripts/)
docs/index.html    the browser demo (Pyodide)
skills/beautiful/  a drop-in skill for Claude Code and similar agents
FACTORS.md         the factor wishlist — start here to contribute
demo/
  screens/  art/   the samples scored above          famous.py  results_famous.md  famous_sites.png
  results_ui.md    results_art.md   results_ui.json  ui_gallery.png  make_gallery.py  make_loop_gif.py
  screenshot_url.js  screenshot_file.js  capture_and_score.py  package.json
tests.py
```

## Roadmap

- [ ] Fit the weights to a public human-rating dataset and report held-out correlation
- [ ] A JavaScript/TypeScript port for the browser and Playwright (no Pyodide)
- [ ] More factors — see [FACTORS.md](FACTORS.md)
- [x] MCP server
- [x] GitHub Action
- [x] Browser demo
- [x] PyPI

See [CONTRIBUTING.md](CONTRIBUTING.md). Counterexamples and factor ideas are the most useful things
you can send.

## License

[MIT](LICENSE) © 2026 Solomon Bolotin. Made at [Bina Solutions](https://www.bina-solutions.co.il/).

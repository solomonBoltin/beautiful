# Factor wishlist — help make the score better

`beautiful` is a weighted sum of explicit, pixel-only factors. Every factor is a formula anyone
can read, argue with, and improve. **The most valuable contribution to this project is a new
factor** — or a counterexample that shows an existing one is wrong.

Propose one with the [factor proposal template](https://github.com/solomonBoltin/beautiful/issues/new?template=1-propose-a-beauty-factor.yml).
You don't have to implement it. A clear description, a source, and two images the current score
gets wrong are enough.

## Rules for a factor

1. **Pixels only.** No DOM, no element boxes, no learned models. numpy / PIL / scipy.
2. **A source.** A paper, an experiment, or a design rule with a documented reason. "I think it
   looks nicer" is a fine start for a discussion, not for a weight.
3. **A target curve.** Say whether more is always better (a ramp) or there is a sweet spot (a bell),
   and give the numbers.
4. **It must move the demo table in the right direction** (`python -m beautiful --mode=ui demo/screens/*.png`)
   without breaking `tests.py`.

## Already in the formula

composition (mirror symmetry, balance, local symmetry) · alignment (grid quality) · simplicity
(edge density, JPEG bytes/pixel, dominant colours) · whitespace · harmony (Matsuda/Cohen-Or hue
templates) · colourfulness (Hasler–Süsstrunk) · contrast (figure–ground) · fractal dimension ·
Fourier slope · rule of thirds (art only) · economy (logo)

## Measured, reported, not yet weighted (`raw["experimental"]`)

Literature-backed measurements computed on every call so that calibration against human ratings
([research/CALIBRATION.md](research/CALIBRATION.md)) can decide their weight instead of taste:
**feature congestion** (Rosenholtz 2007, simplified) · **contour congestion** (Miniukovich 2014,
proxy) · **edge-orientation entropy** and **anisotropy** (Redies / Aesthetics Toolbox) ·
**sequence** (Ngo 2003, from pixels). Each is in `beautiful/experimental.py` with its
simplifications documented; a faithful port of any of them is a welcome PR.

## Evidence says no

The survey in [research/SURVEY.md](research/SURVEY.md) is explicit: the **golden ratio** carries
no reliable preference (Godkewitsch 1974; Stieger & Swami 2015) and a pure **Birkhoff O/C** term
was never validated. Neither will be given positive weight. The **rule of thirds** stays in `art`
mode only.

## Open ideas — take one

| idea | what it would measure | a starting point | status |
|---|---|---|---|
| **rhythm / repetition** | regular spacing of repeated elements (cards, rows, list items) — Ngo's *rhythm* (sequence is now measured, see above) | autocorrelation of the horizontal/vertical edge-projection; peaks at a constant period score high | open |
| **proportion** | are the main rectangles in ratios people actually prefer? **Not the golden ratio** (no replicated preference); 1:1 and 1:√2 have some cross-cultural support | connected components of the structural edge map → aspect ratios → distance to {1:1, 1:√2}; must show signal on the calibration set before it gets weight | open, evidence-gated |
| **typographic hierarchy** | a clear size ladder (title ≫ subtitle ≫ body) instead of many nearly-equal sizes | run-length / connected-component heights of text-like regions; entropy of the height histogram | open |
| **line length** | body-text measure of ~45–75 characters reads as calm | width of text-like runs vs estimated x-height | open |
| **density gradient** | visual weight decreasing top → bottom (F/Z reading pattern) rather than uniform | row-wise edge mass fitted to a monotone curve | open |
| **focal point count** | one clear centre of attention vs many competing ones | saliency proxy (local contrast × saturation), count of separated peaks; bell centred at 1–2 | open |
| **colour temperature consistency** | a page that is all warm or all cool vs a mixed bag | variance of hue-temperature over saturated pixels | open |
| **accent discipline** | one accent colour used for a small share of pixels (buttons, links) | share of the most saturated hue cluster; bell around 2–8 % | open |
| **edge softness / consistency** | consistent corner radii and border weights | histogram of curvature at corners of structural components | open |
| **gestalt grouping** | related things close together, unrelated things apart | gap distribution between structural components; bimodal is good | open |
| **contrast ratio for text** | WCAG-style luminance ratio at text edges specifically, not all edges | text-like regions only (small connected components) | open |
| **negative-space shape** | is the empty space itself a clean shape (margins, gutters) rather than leftover gaps? | convexity / rectangularity of the largest background regions | open |
| **motion blur / sharpness** (art, photo) | crispness where it matters | Laplacian variance, weighted by saliency | open |
| **depth / layering** (art) | foreground–background separation | local contrast at large vs small scale | open |
| **cultural RTL awareness** | mirrored expectations for right-to-left interfaces | flip the balance prior when the page is RTL (detectable from where text lines end) | open |

Better weights are also a contribution. `research/calibrate.py` fits them to the Reinecke & Gajos
ratings (via the Calista mirror) and reports cross-validated ρ; every factor proposal should come
with its row in that table. Other open research items: Subband Entropy clutter, O'Donovan colour
harmony, PHOG self-similarity, element segmentation for the Ngo box metrics, cross-checks against
AIM and a learned model — all tracked as issues.

When an idea lands, its row moves to "in the formula" and the README formula table gets a line
with your name on the source.

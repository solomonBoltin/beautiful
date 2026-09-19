# Every design lint, best practice and no-go we could find — and what a beauty lint can enforce

*Five inventories, compiled 2026-09-19 from ~350 web fetches, with sources on every row:*

| # | Inventory | What it holds |
|---|---|---|
| 01 | [Automated tools](lints/01-tools.md) | ~40 lint tools (Figma plugins, stylelint/eslint plugins, axe, Lighthouse, WAVE, Android/Xcode/Flutter audits, visual-regression suites, AIM, UIS-Hunter, OwlEye, UIClip, the 2026 RL paper) and **63 distinct rules with thresholds** |
| 02 | [Platform guidelines](lints/02-guidelines.md) | WCAG 2.2, Apple HIG, Material 3, Fluent 2, GOV.UK, USWDS, Carbon, Ant, Polaris, Atlassian, Spectrum, Tailwind, shadcn/Radix, Bootstrap; typography, grid, colour and motion canon — **every number, with the disagreements** |
| 03 | [No-gos and anti-patterns](lints/03-antipatterns.md) | **194 items** from NN/g, Baymard, Smashing, deceptive.design, FTC/EDPB/DSA, typography and colour critics, "AI-slop" tells, landing-page and data-viz mistakes — ranked by how many sources cite each |
| 04 | [Measured rules](lints/04-evidence.md) | **39 evidence-backed rules with effect sizes and N** (reading, Fitts, grouping, alignment JND, contrast derivations, first impressions, scroll, thumb reach, forms) — and five pieces of folklore the lint must not encode |
| 05 | [Agent-era guideline sets](lints/05-agent-guidelines.md) | Vercel's Web Interface Guidelines, Anthropic's frontend-design skill, Cursor/Windsurf rule files, Refactoring UI, Laws of UX, Hobday's rules, checklists — and how they phrase rules for agents |

## What the landscape looks like

1. **Nothing open-source scores aesthetics from pixels with explicit, thresholded rules.** AIM computes 17 raw metrics with no pass/fail; UIClip returns a black-box score; the closest recent work (the 2026 RL paper's *spacing consistency, visual balance, content–container fit*) trains a VLM on injected defects. `beautiful` is the only formula-based scorer that also ships its calibration.
2. **The defect thresholds are stable across every tool and guideline.** Text contrast 4.5:1 / 3:1, target 24 px floor (44 pt Apple, 48 dp Material), text under 12 px, viewport meta, image aspect ratio, clipped text, horizontal overflow. These are not taste; they are the same in axe, Lighthouse, ATF, Xcode, Flutter and WCAG, and they belong in a lint as errors.
3. **Where guidelines disagree, they disagree on the same three numbers**: touch target (24 / 40 / 44 / 48), line length (45–90, sweet spot 60–75; screen studies say 45–95), body size (14–19 px, 16 px web consensus). A lint should report the strictest floor as an error and the platform figure as a warning, which is what `rules.py` does.
4. **The most-cited no-gos are all measurable**: low-contrast text (9 sources), asymmetric consent buttons (7), links that don't look like links (7), clutter without white space (6), fake urgency (6), the purple-gradient/glassmorphism "AI look" (8 in one cluster), missing hierarchy (5), rainbow palettes (5), tiny targets (5).
5. **Several famous rules are folklore** and stay out: Miller's 7 ± 2 for on-screen items (it is a memory limit; Cowan puts capacity at 4), "white space raises comprehension 20 %" (misattributed; the real study found slower reading, better comprehension), "CTA above the fold" (contradicted), the golden ratio (no replicated preference, per [SURVEY.md](SURVEY.md)), Google's 41 shades of blue as a hue threshold.
6. **The screenshot-only defect classes with published detectors** — text overlap, component occlusion, broken image placeholders, "null" rendered, blur (OwlEye / Nighthawk / Mobile-UI-Repair, ~85 % P/R) — and GVT's mock-up-diff taxonomy are the most borrowable pixel rule sets, and their training recipe (inject defects into clean screenshots) is reusable for ours.

## The catalogue, mapped to `beautiful`

Legend: **shipped** = in `beautiful/rules.py` (DOM), `beautiful/core.py` (pixels) or `beautiful/render.py`; **next** = issue open; **research** = needs a measurement we don't have yet; **no** = not encodable from pixels or DOM, or the evidence says not to.

### Defects (errors; not taste)

| Rule | Threshold | Sources agree? | Detect | Status |
|---|---|---|---|---|
| Text contrast | 4.5:1 / 3:1 large; AAA 7:1 | yes (WCAG, Apple, Material, every tool) | DOM, px | **shipped** (`text-contrast`) |
| Non-text / icon / border contrast | 3:1 | yes (WCAG 1.4.11, Material) | px, DOM | next |
| Minimum text size | < 12 px (Lighthouse, Google, Stark, WAVE); body ≥ 16 px web | yes | DOM | **shipped** (`font-size`, `font-size-mobile`) |
| Touch target floor | 24 × 24 px or 24 px clearance (WCAG 2.5.8); inline/native exempt | yes | DOM | **shipped** (`touch-target`) |
| Platform touch target | 44 pt Apple / 48 dp Material; 8 dp gap | numbers differ, intent same | DOM | **shipped** 44 warning; gap → next |
| Horizontal overflow / content wider than viewport | any | yes (Google MFT, Vercel, RL-paper D3) | DOM, px | **shipped** (overflow penalty; `clipping?` hint from pixels) |
| Text clipped / truncated | any | yes (Xcode `.textClipped`, ATF, UIS-Hunter) | DOM, px | **shipped** (`text-clipped`) |
| Image aspect distorted | > 5 % | yes (Lighthouse) | DOM, px | **shipped** (`image-distortion`) |
| Viewport meta | missing | yes | DOM | **shipped** (`viewport-meta`) |
| Alt text / accessible names | missing | yes (WCAG, every a11y tool) | DOM | **shipped** `img-alt`; empty links/buttons → next |
| Heading order | no h1, skipped level | yes | DOM | **shipped** (`heading-order`) |
| Focus visible / `outline: none` without replacement | any | yes (stylelint-a11y, Vercel, WCAG 2.4.7) | code, DOM | next |
| `prefers-reduced-motion` honoured; autoplay > 5 s pausable; no autoplay audio | — | yes | code, DOM | next |
| Broken image placeholder; "null"/"undefined" rendered; lorem-ipsum residue | — | yes (OwlEye; AI-slop) | px (OCR), DOM | next |
| Text overlap / component occlusion | — | yes (Nighthawk) | px | research (borrow the injection recipe) |
| Layout shift (CLS ≤ 0.1) | 0.1 | industry | DOM | no (needs a performance trace; Lighthouse does it) |
| Flashing > 3/s | — | WCAG 2.3.1 | px frames | no (static screenshots) |

### Typography (warnings)

| Rule | Threshold | Evidence | Detect | Status |
|---|---|---|---|---|
| Line length | 45–95 CPL supported by screen studies; > 100 or < 35 flagged; guideline sweet spot 60–75 | Dyson 2001, Shaikh 2005 vs Bringhurst/GOV.UK/Windows | DOM, px | **shipped** (`line-length`, band 35–100) |
| Line height | ≥ 1.2 floor; 1.5 tolerated (WCAG 1.4.12); 2.0 aids search | mixed | DOM | **shipped** (`line-height`) |
| Type noise | > 3 families; > 8 sizes (Ant: 3–5 sizes) | Refactoring UI, Material scale | DOM, px | **shipped** (`type-noise`) |
| Justified text; underlined non-links; all-caps body; centred long paragraphs | any | WAVE, HansCo, Butterick | DOM | next |
| Contrast polarity: light-on-dark body text under 16 px | — | Piepenbrock ×3 (replicated) | px, DOM | next |
| Widows / orphans / rivers; faux bold; kerning | — | typographers | px (OCR) | no |
| Text-spacing robustness (1.5 / 2× / 0.12 em / 0.16 em must not clip) | — | WCAG 1.4.12 | code (re-render with overrides) | research |
| "Best font" | — | Wallace 2022: no universal best font | — | **no** (do not reward a family) |

### Layout and composition (the score, and warnings)

| Rule | Threshold | Evidence | Detect | Status |
|---|---|---|---|---|
| Balance / symmetry / equilibrium | — | Ngo, Bauerly & Liu; moderated (Leder 2019) | px | **shipped** (`composition`: symmetric OR balanced) |
| Grid alignment / alignment points | edge tolerance ≤ 1 px; gap consistency ≈ 3 % (Weber) | AIM grid quality; psychophysics | px, DOM | **shipped** as `alignment` factor; a DOM edge-alignment check → next |
| 4/8 px spacing scale; spacing consistency | multiples of 4/8 (GOV.UK 5) | 10+ systems; RL-paper D1 | DOM, px | next (DOM gap histogram) |
| White space | ramp to 55 %, plateau, fall > 90 % | Miniukovich; calibration set; Chaparro 2004 | px | **shipped** (`whitespace`) |
| Clutter / density | edge density, JPEG bpp, colours; feature & contour congestion | Rosenholtz, Miniukovich | px | **shipped** (`simplicity`; congestion measured, unweighted) |
| Proximity grouping | intra/inter gap ratio ≈ 1 is ambiguous | Kubovy (replicated) | px, DOM | research |
| Screen-edge margins | 16/20 pt, 16/24 dp | Apple, Material | DOM, px | next (elements touching edges) |
| Hero "false floor" (nothing peeks above the fold) | — | NN/g, CXL (5 sources) | px, DOM | next |
| Hidden navigation on desktop | — | Pernice & Budiu 2016 (N = 179) | DOM | next |
| Multiple primary buttons | > 1 per view | Balsamiq, Dannaway (5 sources) | DOM | next (needs a "primary" heuristic) |
| Max content width | 1140–1280 consensus | systems | DOM | next (warn > 1400 px measure) |
| Above-fold attention weighting | 57 % / 74 % | NN/g 2018 | DOM | research (weight findings by position) |
| Thumb reach of primary controls | quadratic model | Bergstrom-Lehtovirta 2014 | DOM | research |
| 60-30-10 colour area | heuristic | no authoritative source | px | no (as a score); maybe a note |

### Colour

| Rule | Threshold | Evidence | Detect | Status |
|---|---|---|---|---|
| Colourfulness / restraint | Hasler–Süsstrunk, inverted-U | replicated | px | **shipped** (`colorfulness`) |
| Harmony template | Matsuda/Cohen-Or | plausible; Schloss & Palmer: harmony ≠ preference | px | **shipped** (`harmony`); O'Donovan alternative → issue #21 |
| Near-duplicate colours | ΔE < 2.3 same | Mahy 1994 | px, DOM | next ("inconsistent greys") |
| Distinct hue count | ≤ 7 pre-attentive | Healey 1996 | px | next |
| Pure #000 on #FFF | — | 3 sources | DOM | next (warning) |
| CVD simulation + re-check contrast | 8 % of men | Birch 2012 | px | next |
| Purple-gradient / glassmorphism "AI look" | — | 8 sources | px, DOM | next (hue-signature note, not a penalty) |
| Colour as the only signal | — | WCAG 1.4.1 | manual | no |

### Deceptive patterns (visual ones only)

| Rule | Detect | Status |
|---|---|---|
| Asymmetric consent buttons (bright accept, grey reject) | DOM, px | next |
| Pre-ticked consent boxes | DOM | next |
| Countdown timers / fake urgency text | DOM | next (text pattern, warning) |
| Confirmshaming copy | DOM | next (text pattern) |
| Hidden costs, roach motel, trick wording, forced continuity | manual | no |

### Not encodable, or encodable only elsewhere

Intent-based dark patterns, information-architecture and label quality, copy quality, data-viz
truthfulness, motion feel, performance metrics (Lighthouse already does CLS/LCP), and anything
needing interaction (focus traps, keyboard order beyond tabindex).

## The agent-era landscape, and where `beautiful` sits

Three tools already lint UI *for agents* deterministically, all from **source code**: ux-skill
(152 regex rules, `pip install uxskill`, MCP), Impeccable (61-rule Rust detector plus DESIGN.md
drift) and Hallmark (58 yes/no gates). Vercel's guidelines, Anthropic's frontend-design skill and
taste-skill are prose rule sets an agent reads. What none of them can do is look at the rendered
result: Checklist Design's own skill separates "what's on the page" (source) from "how it looks"
(needs a screenshot) and stops at the second. `beautiful` is the second half — the score, the
DOM rules on the *rendered* page, the overlays — and the natural pairing is: source lint (theirs)
before the build, render lint (ours) after it. Their rule records (`id, severity, why, fix,
source`) and severity vocabulary are what our findings should match; their most-cited tells (the
purple gradient, Inter as display, three identical cards, glass as decoration, nested cards,
eyebrow labels, accent > 5 % of the viewport) are pixel-checkable and are issue #41.

## How the tools compare to `beautiful` today

| Capability | axe / Lighthouse | AIM | UIClip | Design Lint (Figma) | `beautiful` |
|---|---|---|---|---|---|
| WCAG contrast, target size, font size, viewport | yes | — | — | contrast only | yes (DOM rules) |
| Pixel aesthetics with an explicit formula | — | metrics, no score | black-box score | — | yes, with calibration numbers published |
| Balance / symmetry / grid from pixels | — | yes | implicit | — | yes |
| Explains itself (overlays, hints) | messages | — | text suggestions | — | yes (`--explain`, hints) |
| Works on a URL / HTML without a screenshot | yes | URL | — | — | yes (Chromium) |
| Works on art / logos | — | — | — | — | yes |
| Token / palette conformance | — | — | — | yes | next (pixel-side count; DESIGN.md as oracle) |
| Source-code anti-pattern lint (regex) | — | — | — | — | no — use ux-skill / Impeccable / Hallmark before the build |

## Next batch (issues)

The rules marked **next** above are tracked as issues labelled `rule`. The order is by how many
sources agree and how cheap the check is: non-text contrast, target spacing, focus visibility,
reduced motion and autoplay, empty links and buttons, justified/underlined/all-caps text, contrast
polarity, near-duplicate colours and hue count, edge margins, false floor, hidden desktop nav,
multiple primaries, asymmetric consent buttons, pre-ticked boxes, lorem ipsum and "null" text,
then the pixel research items (overlap/occlusion via the injection recipe, proximity grouping,
above-fold weighting).

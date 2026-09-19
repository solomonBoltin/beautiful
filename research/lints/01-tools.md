# Automated design / UI lint tools and the rules they check — inventory

*Part of the [design-lint survey](../DESIGN-LINTS.md). Tags: **px** = pixels/screenshot,
**DOM** = DOM/CSS/runtime tree, **design** = design file, **code** = source, **manual**.*

## 1. Design-tool lints

### Design Lint (Destefanis) — Figma
- https://github.com/destefanis/design-lint, https://lintyour.design/ — MIT. Input: Figma layers. All **design**: fill / stroke / effect / text not from a shared style; border radius not in `[0, 2, 4, 8, 16, 24, 32]` (configurable); custom rules.

### Roller (Toybox) — Figma / Sketch
- https://github.com/contrastapp/roller — colour, text style, shadow, border, radius not in the library; auto-fix to nearest **design**.

### Stark — Figma / Sketch / XD / browser
- https://www.getstark.co/figma/ — contrast ≥ 4.5:1 (AA) / 7:1 (AAA) **design, px**; touch-target pass/fail **design**; text < 12 px flagged **design**; focus order, landmarks, alt annotations **manual**; vision simulators **px**.

### Contrast / Use Contrast / Figma-Contrast / Able
- https://www.figma.com/community/plugin/748533339900865323/contrast, https://github.com/romannurik/Figma-Contrast, https://usecontrast.com/, https://figmaelements.com/plugins/able/ — colour behind the selection, AA/AAA, whole-page contrast reports, CVD simulation **design**.

### aficat/design-linter — Figma
- https://github.com/aficat/design-linter — hardcoded colour vs token; font size/weight/line-height vs system; spacing vs tokens; component override misuse; button styling; contrast **design**.

### Varifind / Variables Lint; Figma Dev Mode
- Detached or missing variables **design**; Dev Mode "suggest variable", "compare changes" **design**.

### sketch-lint — Sketch
- https://github.com/saranshsolanki/sketch-lint — typography vs guideline; colour vs palette; spelling; W3C contrast vs background/artboard; vertical padding between layers **design**.

### Penpot / Framer
- Penpot: community "Token Lint" concept only. Framer: Accessibility Checker (WCAG checkpoints) and Contrast Checker plugins **DOM**.

## 2. Code / CSS / token lints

### stylelint core (design-relevant)
- https://stylelint.io/user-guide/rules/ **code**: `declaration-no-important`, `selector-max-specificity`, `number-max-precision`, `color-named`, `color-no-hex`, `color-hex-length`, `unit-allowed-list` / `unit-disallowed-list`, `declaration-property-unit-allowed-list` (force `rem` for font-size), `declaration-property-value-allowed-list` / `-disallowed-list` (z-index set, `transition: all` ban), `font-family-no-missing-generic-family-keyword`, `font-weight-notation`.

### stylelint-a11y
- https://github.com/YozhikM/stylelint-a11y **code**: `font-size-is-readable` (≥ 15 px), `line-height-is-vertical-rhythmed`, `no-spread-text` (max-width of text blocks), `no-text-align-justify`, `no-outline-none`, `selector-pseudo-class-focus` (`:hover` needs `:focus`), `media-prefers-reduced-motion`, `media-prefers-color-scheme`, `no-display-none`, `content-property-no-static-value`, `no-obsolete-attribute`, `no-obsolete-element`.

### stylelint-declaration-strict-value / stylelint-scales / rhythmguard
- https://github.com/AndyOGo/stylelint-declaration-strict-value — listed properties must be a variable/function/keyword (no magic values). `stylelint-scales` — values on a declared scale. https://github.com/PetriLahdelma/stylelint-plugin-rhythmguard — `use-scale` (spacing/radius/type/size/motion, also Tailwind class strings), `prefer-token`, `no-offscale-transform` **code**.

### eslint-plugin-jsx-a11y
- https://github.com/jsx-eslint/eslint-plugin-jsx-a11y **code**: alt-text, anchor-ambiguous-text, anchor-has-content, anchor-is-valid, aria-* validity (activedescendant, props, proptypes, role, unsupported), autocomplete-valid, click-events-have-key-events, control-has-associated-label, heading-has-content, html-has-lang, iframe-has-title, img-redundant-alt, interactive-supports-focus, label-has-associated-control, media-has-caption, mouse-events-have-key-events, no-access-key, no-aria-hidden-on-focusable, no-autofocus, no-distracting-elements, no-interactive-element-to-noninteractive-role, no-noninteractive-element-interactions, no-noninteractive-tabindex, no-redundant-roles, no-static-element-interactions, prefer-tag-over-role, role-has-required-aria-props, role-supports-aria-props, scope, tabindex-no-positive.

### eslint-plugin-tailwindcss; Tailwind IntelliSense lint
- https://github.com/francoismassart/eslint-plugin-tailwindcss **code**: classnames-order, canonical classname, negative arbitrary values, shorthand, important modifier, `no-arbitrary-value` (`p-[13px]`), `no-contradicting-classname`, `no-custom-classname`, `no-unnecessary-arbitrary-value`. IntelliSense: `cssConflict`, `invalidApply`, `invalidScreen`, `invalidVariant`, `invalidConfigPath`, `invalidTailwindDirective`, `recommendedVariantOrder`.

### shadcn/lint (agent-first)
- https://github.com/shadcn-ui/lint **code**: `no-restyle`, `no-raw-colors` (`bg-pink-500` outside theme), `no-arbitrary-values`, `no-inline-styles`, `no-unknown-classes`, `require-static-classes`.

### eslint-plugin-design-tokens; ds-lint; @lapidist/design-lint; DTCG validators
- https://github.com/PavelLazarchuk/eslint-plugin-design-tokens — no-hardcoded colors / spacing / typography / shadows / radius / borders / transitions / z-index; unknown token var **code**. ds-lint (Rust) and https://github.com/bylapidist/design-lint — hard-coded value vs token, raw element where a DS component exists, deprecated tokens **code**. design-token-kit, Cobalt, W3C DTCG validator: schema, broken alias, duplicates, unused **code**.

## 3. Runtime / browser audits

### axe-core (Deque)
- https://github.com/dequelabs/axe-core/blob/develop/doc/rule-descriptions.md **DOM**. WCAG A/AA: area-alt, aria-* (≈ 25 rules), blink, button-name, bypass, **color-contrast** (≥ 4.5:1; ≥ 3:1 for large ≥ 18 pt / 14 pt bold) **DOM, px**, definition-list, dlitem, document-title, duplicate-id-aria, form-field-multiple-labels, frame-*, html-has-lang, html-lang-valid, image-alt, input-button-name, input-image-alt, label, **link-in-text-block** (3:1 vs surrounding text or non-colour cue), link-name, list, listitem, marquee, meta-refresh, **meta-viewport** (no `user-scalable=no`, `maximum-scale<2`), nested-interactive, no-autoplay-audio (> 3 s), object-alt, role-img-alt, scrollable-region-focusable, select-name, svg-img-alt, td-headers-attr, th-has-data-cells, valid-lang, video-caption. WCAG 2.1: autocomplete-valid, avoid-inline-spacing. WCAG 2.2: **target-size** (≥ 24×24 CSS px or a 24 px clearance circle; https://dequeuniversity.com/rules/axe/4.10/target-size). AAA: color-contrast-enhanced (7:1 / 4.5:1), identical-links-same-purpose. Best practice: heading-order, page-has-heading-one, empty-heading, empty-table-header, landmark-* rules, meta-viewport-large (≥ 5×), tabindex (no > 0), skip-link, region. Experimental: **p-as-heading**, css-orientation-lock, label-content-name-mismatch, table-fake-caption.

### Lighthouse
- https://github.com/GoogleChrome/lighthouse/blob/main/core/config/default-config.js. Accessibility = axe + manual items. **font-size**: pass if ≥ 60 % of text characters are ≥ 12 px (https://developer.chrome.com/docs/lighthouse/seo/font-size) **DOM**. **tap-targets**: fail when a target < 48×48 px and ≥ 25 % of the 48 px zone overlaps another target; recommends 8 px gaps **DOM**. **viewport** meta present. Best practices: **image-aspect-ratio** (displayed vs natural) **DOM, px**, image-size-responsive (> 4 KB / 12 KB waste), paste-preventing-inputs, doctype, charset, console errors, deprecations. Performance visual metrics: CLS, LCP, FCP, Speed Index, font-display. SEO: document-title, meta-description, link-text, crawlable-anchors, image-alt.

### pa11y / HTML_CodeSniffer
- https://github.com/pa11y/pa11y, https://squizlabs.github.io/HTML_CodeSniffer/Standards/WCAG2/ — sniff IDs (`WCAG2AA.Principle1.Guideline1_4.1_4_3.G18.Fail`); contrast 4.5:1 / 7:1 (`.BgImage` warning when the background is an image), alt, labels, headings, fieldsets, table headers, iframe titles, lang, meta refresh **DOM**; keyboard/link-purpose/focus items are notices **manual**.

### WAVE (WebAIM)
- https://wave.webaim.org/api/docs?format=json — errors: alt_* missing, label_*, aria_reference_broken, language_missing, meta_refresh, heading_empty, button_empty, link_empty, blink, marquee, **contrast**. Alerts: **text_small**, **text_justified**, **underline** (underlined non-link), link_suspicious ("click here"), link_redundant, alt_suspicious/redundant/duplicate/long, heading_missing, h1_missing, heading_skipped, heading_possible, list_possible, table_layout, region_missing, tabindex, noscript, link_pdf/word, audio_video **DOM**.

### Google Mobile-Friendly Test (retired 2023; criteria live on in Lighthouse)
- "Viewport not set", "Viewport not set to device-width", "Content wider than screen", "Text too small to read" (< 12 px), "Clickable elements too close together" (48 px / 8 px), "Uses incompatible plugins" **DOM**.

### Polypane; Chrome DevTools; WebPageTest
- Polypane https://polypane.app/docs/accessibility-panel/ — WCAG 2.2 audit, contrast of every text/background pair, target size, focus-order outline, meta/social preview length checks, CVD / reduced-motion / forced-colours emulation. DevTools CSS Overview https://developer.chrome.com/docs/devtools/css-overview — colour inventory with contrast issues, **font inventory by size/weight/line-height** (typographic sprawl), unused declarations, media queries. WebPageTest "Is it usable?" = axe + HTML validation + layout-shift causes.

## 4. Native platform lints

### Android — Accessibility Test Framework / Accessibility Scanner / Espresso
- https://github.com/google/Accessibility-Test-Framework-for-Android — **TouchTargetSizeCheck** ≥ 48×48 dp (32 dp at screen edge or inside IME) **DOM**; **TextContrastCheck** 4.5:1 / 3:1 large (≥ 18 dp or ≥ 14 dp bold), tolerance 0.01, sampled from rendered pixels **px**; **ImageContrastCheck** ≥ 3:1 **px**; **TextSizeCheck** — fixed units: ERROR < 16 dp, WARNING < 28 dp; sp text in a fixed container ≥ 70 % of width/height → clipping warning **DOM**; SpeakableTextPresent, EditableContentDesc, RedundantDescription, DuplicateSpeakableText, **DuplicateClickableBounds**, ClickableSpan, LinkPurposeUnclear, TraversalOrder, UnexposedText **DOM**.

### Android Lint (static)
- https://googlesamples.github.io/android-custom-lint-rules/checks/index.md.html **code**: ContentDescription, LabelFor, ClickableViewAccessibility, KeyboardInaccessibleWidget; Typography: **SmallSp** (< 11 sp), TypographyDashes, TypographyEllipsis, TypographyQuotes, TypographyFractions; Icons: IconColors, IconDensities, IconDipSize, IconDuplicates, IconExpectedSize, IconLauncherShape, IconMixedNinePatch, MonochromeLauncherIcon.

### Xcode — `performAccessibilityAudit` / Accessibility Inspector / Interface Builder
- https://developer.apple.com/documentation/xctest/xcuiaccessibilityaudittype — `.contrast` ≥ 4.5:1 **px**; `.hitRegion` ≥ 44×44 pt **DOM**; `.textClipped` **DOM, px**; `.dynamicType`; `.sufficientElementDescription`, `.elementDetection`, `.trait`, `.parentChild`. Interface Builder: ambiguous layout, misplaced views, missing/unsatisfiable constraints **code**.

### Flutter — `AccessibilityGuideline`
- https://api.flutter.dev/flutter/flutter_test/AccessibilityGuideline-class.html — `androidTapTargetGuideline` ≥ 48×48, `iOSTapTargetGuideline` ≥ 44×44, `labeledTapTargetGuideline`, `textContrastGuideline` 4.5:1 / 3:1 sampled from rendered pixels; AAA variant 7:1 / 4.5:1 **DOM, px**.

## 5. Visual regression / screenshot QA

| Tool | Input | Rule / threshold |
|---|---|---|
| Chromatic https://www.chromatic.com/docs/threshold/ | Storybook | pixel diff, anti-aliasing ignored, `diffThreshold` 0.063; a11y = axe |
| Percy https://docs.percy.io/docs/diff-sensitivity | DOM snapshot | Strict / Recommended / Relaxed; **Layout** mode ignores text/images |
| Applitools https://applitools.com/docs/eyes/concepts/best-practices/match-levels | screenshots | Exact / Strict / Content / **Layout** (structure only) |
| BackstopJS | URLs | resemble.js, `misMatchThreshold` 0.1 % |
| Playwright `toHaveScreenshot` | page | pixelmatch YIQ `threshold` 0.2 |
| Argos | screenshots | threshold 0–1 (0.5 default) |
| Meticulous | recorded sessions | per-step pixel diff |
| Storybook addon-a11y | stories | axe |

None encode aesthetic rules; they detect *change*. Applitools/Percy "Layout" are the closest to a structural model.

## 6. Research / academic tools

### AIM — Aalto Interface Metrics
- https://interfacemetrics.aalto.fi/, https://github.com/aalto-ui/aim (UIST 2018). 17 pixel metrics: PNG file size, colour variability, static/dynamic colour clusters, colourfulness, luminance SD, colour harmony; edge density, contour congestion, figure–ground contrast, symmetry, visual complexity (quadtree balance/symmetry/equilibrium), **grid quality** (number of alignment lines), white space; Itti–Koch saliency, visual-search performance; colour-blindness simulations **px**.

### UIS-Hunter — "Don't Do That!" (ICSE 2021)
- https://xin-xia.github.io/publication/icse213.pdf — 93 Material "don't" guidelines over 17 components; OCR-based truncation/wrap/shrink detection, icon classification, colour, edge. Examples: don't truncate app-bar titles or button labels; don't put buttons/text over busy images; a confirmation dialog needs two actions; don't attach tabs to bottom navigation; one icon per button; icons for all-or-none destinations; don't alter snackbar shape **px, DOM**.

### OwlEye (ASE 2020) / Nighthawk (TSE 2022) / Mobile-UI-Repair (2024)
- https://arxiv.org/abs/2009.01417, https://arxiv.org/abs/2205.13945 — screenshot-only defect classes: **text overlap, component occlusion, missing image, "null" rendered, blurred screen**; CNN/Faster-RCNN ~85 % P/R; training data by *injecting* defects into clean Rico screenshots — a reusable synthetic-defect recipe **px**.

### GVT — GUI design violations (ICSE 2018)
- https://arxiv.org/abs/1802.04732 — mock-up vs implementation: layout (translation, size), resource (missing/extra component, wrong image/colour), text (font style/colour/content); perceptual diff + colour histograms + OCR; 98 % P / 96 % R on synthetic violations **px**.

### Others
- Apple Screen Recognition (CHI 2021) — pixel-only UI element detector, 71 % mAP. Rico — 72 k screens. GUI2DSVec — design-smell detection from GUI image. VizLinter — ASP rules for charts. Blob Listener — code-level GUI smells.

## 7. AI-era / LLM tools

- **UIClip** (UIST 2024) https://arxiv.org/abs/2404.12500 — CLIP fine-tuned on defect-injected pairs (distorted layout, off-palette colour, poor contrast, misaligned text) + human rankings → score + suggestions **px**.
- **UICrit** (UIST 2024) https://arxiv.org/html/2407.08850v2 — 3,059 designer critiques with bounding boxes on 983 Rico UIs: layout/alignment, colour, typography, spacing, hierarchy, consistency, affordance, copy **px**. **UXBench** measures critique actionability.
- **UI-Bench** (2025) — pairwise human preference of generated apps **manual**.
- **Design2Code** (2024) — block-match, text match, position match, text-colour match, CLIP / CW-SSIM **px, DOM**.
- **"Learning to detect UI principle violations via RL" (2026)** https://arxiv.org/html/2607.20690 — 19-principle taxonomy with screenshot-vs-HTML detectability: A1 non-text contrast ≥ 3:1, A3 target ≥ 24 px, B1–B5 dark patterns, C1 similarity, C2 Von Restorff, C3 Miller chunking, C4 Hick, C6 Fitts, **D1 spacing consistency, D2 visual balance, D3 content-container fit** (largest gains); synthetic inject→render→verify data; 4B VLM at 84 % F1.
- **GPT-4 heuristic evaluation in Figma** (CHI 2024) https://arxiv.org/abs/2403.13139 — 52 % accurate; good at misalignment and text errors, poor at "aesthetic & minimalist design".
- **Vercel Web Interface Guidelines** https://github.com/vercel-labs/web-interface-guidelines — ~103 MUST/SHOULD/NEVER rules run as a skill against source (see [05-agent-guidelines.md](05-agent-guidelines.md)).

## 8. Master deduplicated rule list

| # | Rule (threshold) | Implemented by | Detect |
|---|---|---|---|
| 1 | Text contrast ≥ 4.5:1 normal / ≥ 3:1 large (≥ 18 pt or ≥ 14 pt bold); AAA 7:1 / 4.5:1 | axe, Lighthouse, pa11y, WAVE, Polypane, DevTools, Stark, Contrast/Able, sketch-lint, ATF, Scanner, Flutter, XCUI, RL-paper | px, DOM, design |
| 2 | Non-text / icon contrast ≥ 3:1 | ATF ImageContrastCheck, Scanner, RL-paper A1 | px |
| 3 | Links distinguishable from body text not by colour alone | axe link-in-text-block | DOM |
| 4 | Touch target ≥ 48×48 dp (Android); 32 dp at edge/IME | ATF, Scanner, Flutter, Lighthouse, Google MFT | DOM, px |
| 5 | Touch target ≥ 44×44 pt (iOS) | XCUI, Inspector, Flutter, Stark | DOM, design |
| 6 | Target ≥ 24×24 CSS px or 24 px clearance (WCAG 2.5.8) | axe, Lighthouse, Polypane, RL-paper | DOM |
| 7 | Targets not crowded (≥ 8 px gap; ≥ 25 % overlap of 48 px zone fails) | Lighthouse, Google MFT, ATF DuplicateClickableBounds | DOM |
| 8 | Minimum legible font size: ≥ 12 px on ≥ 60 % of text (Lighthouse); < 12 px flagged (Stark, Google); ≥ 15 px (stylelint-a11y); ≥ 16 dp fixed (ATF); ≥ 11 sp (Android SmallSp) | Lighthouse, Google, WAVE, Stark, stylelint-a11y, ATF, Android Lint | DOM, design, code |
| 9 | Text must scale (sp / Dynamic Type; no `user-scalable=no`, `maximum-scale<2`) | ATF, XCUI, axe meta-viewport, Vercel | DOM, code |
| 10 | Text not clipped / truncated / wrapped / shrunk | XCUI .textClipped, ATF, UIS-Hunter, Vercel, RL-paper D3 | DOM, px |
| 11 | Text overlap | OwlEye, Nighthawk, Mobile-UI-Repair | px |
| 12 | Component occlusion | Nighthawk, Mobile-UI-Repair | px |
| 13 | Missing / broken image | OwlEye, Nighthawk, GVT | px |
| 14 | "null"/undefined rendered | Mobile-UI-Repair | px (OCR) |
| 15 | Blurred / low-res rendering | OwlEye | px |
| 16 | Content wider than viewport | Google MFT, Vercel, RL-paper D3 | DOM, px |
| 17 | Viewport meta present / device-width | Lighthouse, Google MFT, axe | DOM |
| 18 | Image aspect ratio preserved | Lighthouse image-aspect-ratio | DOM, px |
| 19 | Images have explicit dimensions; sized to display | Lighthouse, Vercel, WebPageTest | DOM |
| 20 | No layout shift (CLS) | Lighthouse, WebPageTest | DOM |
| 21 | Colour from palette/token (no hardcoded colour); distinct-colour count | Design Lint, Roller, aficat, sketch-lint, shadcn, eslint-design-tokens, ds-lint, lapidist, stylelint, DevTools, AIM | design, code, px |
| 22 | Typography from a type scale | Design Lint, Roller, aficat, sketch-lint, eslint-design-tokens, ds-lint, stylelint-scales, DevTools | design, code, px |
| 23 | Spacing on scale (no magic numbers) | rhythmguard, stylelint-scales, eslint-design-tokens, Tailwind lint, shadcn, sketch-lint, RL-paper D1 | code, px |
| 24 | Border radius on allowed set | Design Lint, Roller, eslint-design-tokens, ds-lint, rhythmguard | design, code |
| 25 | Shadows / effects / borders from tokens | Design Lint, Roller, eslint-design-tokens, ds-lint | design, code |
| 26 | z-index from tokens | eslint-design-tokens, stylelint | code |
| 27 | No `!important`; specificity cap | stylelint | code |
| 28 | No contradicting utility classes | eslint-tailwindcss, IntelliSense | code |
| 29 | No arbitrary/unknown classes; canonical order | eslint-tailwindcss, IntelliSense, shadcn | code |
| 30 | Component not restyled; DS component over raw element | shadcn, lapidist | code |
| 31 | Detached instances / missing variables / deprecated tokens | Figma, Varifind, lapidist, DTCG | design, code |
| 32 | Token file validity | design-token-kit, Cobalt, DTCG, Style Dictionary | code |
| 33 | Line-height on rhythm; measure in range | stylelint-a11y | code, px |
| 34 | No justified text | WAVE, stylelint-a11y | DOM, code, px |
| 35 | No underlined non-link text | WAVE | DOM |
| 36 | Typographic niceties: "…", curly quotes, real dashes, nbsp in units, tabular-nums, `text-wrap: balance` | Android Lint, Vercel | code, px (OCR) |
| 37 | Icon consistency: sizes, density, style, ≤ 1 icon per button, all-or-none | Android Lint, UIS-Hunter | code, px |
| 38 | Text over busy image illegible | UIS-Hunter, pa11y | px |
| 39 | Grid alignment / misalignment | AIM Grid Quality, GPT-4 study, GVT, UICrit | px |
| 40 | Visual balance / symmetry / equilibrium | AIM, RL-paper D2 | px |
| 41 | Clutter: edge density, contour congestion, colour clusters, file size, congestion | AIM | px |
| 42 | Figure–ground contrast; white space; colourfulness; luminance SD; harmony | AIM | px |
| 43 | Saliency / primary action stands out and is large & near (Von Restorff, Fitts) | AIM, RL-paper C2/C6 | px |
| 44 | Layout fidelity vs mock-up | GVT, Applitools, Percy, Design2Code | px, DOM |
| 45 | Pixel change vs baseline | Chromatic, Percy, BackstopJS, Playwright, Argos, Meticulous | px |
| 46 | Visible focus indicator; no `outline: none`; `:hover` has `:focus` | stylelint-a11y, Vercel, Lighthouse manual | code, manual |
| 47 | Reduced motion; autoplay > 5 s pausable; no autoplay audio > 3 s | stylelint-a11y, Vercel, axe | code, DOM |
| 48 | No blink/marquee | axe, WAVE, jsx-a11y | DOM, code |
| 49 | Heading hierarchy (h1, no skips, no empty, no fake headings) | axe, WAVE, HTML_CS | DOM |
| 50 | Landmarks / skip link / single main | axe, WAVE, Lighthouse | DOM |
| 51 | Accessible names; no redundant / duplicate descriptions | axe, WAVE, jsx-a11y, ATF, XCUI, Flutter, Android Lint | DOM, code |
| 52 | Generic link text; identical names different purpose; redundant adjacent links | WAVE, jsx-a11y, axe, Lighthouse, ATF | DOM, code |
| 53 | Form labels; autocomplete; paste allowed | axe, WAVE, HTML_CS, Lighthouse, Vercel | DOM, code |
| 54 | Focus order / positive tabindex / nested interactives | axe, WAVE, jsx-a11y, ATF, Polypane | DOM, manual |
| 55 | ARIA validity | axe, jsx-a11y, WAVE | DOM, code |
| 56 | Title / lang / meta description / social preview | axe, Lighthouse, WAVE, Polypane | DOM |
| 57 | Dialog anatomy, tab/bottom-nav conflicts, snackbar shape, FAB count | UIS-Hunter | px, DOM |
| 58 | Ambiguous layout / missing constraints | Xcode IB | code |
| 59 | Dark patterns (confirmshaming, misdirection, hidden costs, trick questions, forced continuity) | RL-paper B1–B5 | DOM, px |
| 60 | Cognitive-load laws (Miller, Hick) | RL-paper C3/C4 | px |
| 61 | Empty state; long/short content; safe-area insets; theme-color | Vercel | code, manual |
| 62 | Similar functions styled consistently | RL-paper C1, UICrit, Roller/Design Lint | DOM, px, design |
| 63 | Colour-blindness safety (simulation) | AIM, Stark, Able, Polypane | px |

## What this means for `beautiful`

- Nothing open-source scores **aesthetics from pixels with explicit, thresholded rules**: AIM gives raw metrics without pass/fail, UIClip a black-box score, and the 2026 RL paper's D1–D3 (spacing consistency, balance, content fit) are the only recent *visual* rule definitions, with a synthetic-injection recipe worth copying.
- The screenshot-only defect classes with published detectors (rows 11–15: overlap, occlusion, broken image, "null", blur) and GVT's mock-up-diff taxonomy (row 44) are the most borrowable pixel rule sets.
- Every threshold in rows 1–9 is stable across tools, so implementing them from the DOM (done in `beautiful/rules.py` for 1, 5, 6, 8, 9-partial, 10, 16, 17, 18, 49, 51-partial) gives direct comparability with axe / Lighthouse / ATF.
- Token/palette conformance (rows 21–25) exists only at design/code level; a pixel-side "count distinct colours / font sizes / radii against a declared scale" would be new.

# Quantified design rules from platform guidelines and design systems — inventory

*Part of the [design-lint survey](../DESIGN-LINTS.md). Tags: **px** = screenshot, **DOM** =
DOM/computed CSS, **design** = design file / tokens, **code** = source, **manual**. Units: pt
(Apple), dp/sp (Android), epx (Windows), CSS px. Apple's and Material's live pages render
client-side; their numbers were confirmed through mirrors and derived docs and are flagged where
the exact live wording was not re-verified.*

## 1. WCAG 2.2 (W3C) — the only normative source
https://www.w3.org/WAI/WCAG22/quickref/

- **1.4.3 Contrast (Minimum), AA**: text ≥ **4.5:1**; large text ≥ **3:1** (large = ≥ 18 pt ≈ 24 px regular, or ≥ 14 pt ≈ 18.66 px bold). Exceptions: incidental, logotypes, inactive, decorative. Relative luminance: sRGB threshold 0.04045, `/12.92`, `((c+0.055)/1.055)^2.4`, weights 0.2126 / 0.7152 / 0.0722. **px, DOM**
- **1.4.6 Enhanced, AAA**: 7:1 / 4.5:1. **px, DOM**
- **1.4.11 Non-text Contrast, AA**: UI components and graphical objects ≥ **3:1**. **px, DOM**
- **1.4.12 Text Spacing, AA**: content survives line-height ≥ 1.5×, paragraph spacing ≥ 2×, letter-spacing ≥ 0.12 em, word-spacing ≥ 0.16 em. **DOM**
- **1.4.4 Resize Text, AA**: usable at 200 % zoom. **DOM**
- **1.4.10 Reflow, AA**: no two-dimensional scroll at **320 CSS px** width. **DOM**
- **1.4.8 Visual Presentation, AAA**: line width ≤ **80 characters** (40 CJK); line spacing ≥ 1.5; paragraph spacing ≥ 1.5× line spacing; not justified. **DOM, px**
- **2.5.8 Target Size (Minimum), AA**: **24 × 24 CSS px**, or a 24 px circle centred on the target that intersects no other target's circle; exceptions: inline, user-agent, essential, equivalent. **DOM, px**
- **2.5.5 Target Size (Enhanced), AAA**: 44 × 44. **DOM, px**
- **2.4.7 Focus Visible, AA**; **2.4.11 Focus Not Obscured, AA**; **2.4.13 Focus Appearance, AAA**: ≥ 2 px-thick perimeter, ≥ 3:1 change. **px, DOM**
- **2.3.1 Three Flashes, A**: ≤ 3 flashes/s; general flash = luminance change ≥ 10 % over > 25 % of a 10° field (≈ 341 × 256 px at 1024 × 768); red flash R/(R+G+B) ≥ 0.8. **px (frames)**
- **2.3.3 Animation from Interactions, AAA**: motion can be disabled (`prefers-reduced-motion`). **DOM, code**
- **1.4.1 Use of Color, A**: colour not the only cue. **manual** (partial DOM: links)
- **1.3.4 Orientation, AA**: no orientation lock. **code**
- **2.2.1 Timing Adjustable, A**: extend ≥ 10×, ≥ 20 s warning. **code**

## 2. Apple Human Interface Guidelines
https://developer.apple.com/design/human-interface-guidelines/ (values via https://gist.github.com/eonist/b9c180a67980c6e18a5184f19bff68fa, https://blog.logrocket.com/ux-design/all-accessible-touch-target-sizes/, https://ivomynttinen.com/blog/ios-design-guidelines/)

- Hit target ≥ **44 × 44 pt** (visionOS ≥ 60 pt). **px, DOM**
- Contrast: ≤ 17 pt → 4.5:1; ≥ 18 pt → 3:1; ≥ 14 pt bold → 3:1 (WCAG-aligned). **px, DOM**
- Dynamic Type (Large): Large Title 34/41, Title 1 28/34, Title 2 22/28, Title 3 20/25, Headline 17/22 semibold, Body 17/22, Callout 16/21, Subhead 15/20, Footnote 13/18, Caption 1 12/16, Caption 2 11/13. **Minimum text 11 pt; body 17 pt.** SF Pro Text ≤ 19 pt, Display ≥ 20 pt. **DOM, design**
- Line height: 120–130 % text, 110–120 % display. **DOM**
- Layout margins 16 pt (compact) / 20 pt (regular); 8-pt grid; spacing 4/8/12/16/20/24/32/40/48. **px, DOM**
- Bars: nav 44 pt (50 iPad), tab bar 49 pt, toolbar 44, table row ≥ 44, text field 44; alert width 270 pt, radius 14 pt; tab bar ≤ 5 tabs; alert ≤ 3 buttons. **px, DOM**
- Icons: nav/toolbar stroke 1–1.5 pt; tab icons ≈ 25–28 pt; app icon 1024². **design, px**
- Motion: Reduce Motion respected; typical 100/200/300/500 ms. **code**
- macOS body 13 pt (min ~10), watchOS 16, tvOS 29, visionOS 17 — *to confirm against live HIG*. **DOM**

## 3. Google Material Design 3
https://m3.material.io/ (via https://developer.android.com/develop/ui/compose/layouts/adaptive/use-window-size-classes, https://github.com/yhongm/material-design-skill/blob/master/references/typography.md, https://m2.material.io/design/usability/accessibility.html, https://m2.material.io/design/color/dark-theme.html)

- Touch target ≥ **48 × 48 dp** (~9 mm) even if the visual is smaller; ≥ **8 dp** between targets; pointer targets ≥ 44 dp. **px, DOM**
- Contrast: small text 4.5:1, large (≥ 18 pt / ≥ 14 pt bold) 3:1; icons 3:1; M3 colour pairs guarantee ≥ 3:1. **px, DOM**
- Tonal palette tones 0, 10, …, 90, 95, 98, 99, 100; light primary tone 40 / on-primary 100 / container 90 / on-container 10; dark flips (80/20/30/90). Tone difference ≥ 40 → ~3:1, ≥ 50 → 4.5–7:1. **code, design**
- Window size classes: compact < 600 dp, medium 600–839, expanded 840–1199, large 1200–1599, extra-large ≥ 1600; height compact < 480, medium 480–899, expanded ≥ 900. **DOM**
- Margins: compact 16 dp, medium/expanded 24 dp; pane spacer 24 dp; 4/8/12 columns. **px, DOM**
- Grid 4 dp baseline / 8 dp spacing; density −4 dp per step. **px, DOM**
- Type scale (size/lh/weight/tracking): Display L 57/64, M 45/52, S 36/44; Headline L 32/40, M 28/36, S 24/32; Title L 22/28, M 16/24/500, S 14/20/500; Body L 16/24, M 14/20, S 12/16; Label L 14/20/500, M 12/16/500, S 11/16/500. **Smallest role 11 sp.** **DOM, design**
- Elevation levels 0/1/3/6/8/12 dp (cards L1, menus L2, dialogs/FAB L3). **DOM, design**
- M2 dark theme: surface #121212; overlay by elevation 0 % → 16 % (1 dp 5 %, 2 dp 7 %, 3 dp 8 %, 4 dp 9 %, 6 dp 11 %, 8 dp 12 %, 12 dp 14 %, 16 dp 15 %, 24 dp 16 %); on-surface 15.8:1; desaturated tone-200 primaries; text emphasis 87/60/38 % (light) and 100/70/50 % (dark). **px, DOM**
- Motion tokens: short 50–200 ms, medium 250–400, long 450–600, extra-long 700–1000; easings emphasized-decelerate (0.05, 0.7, 0.1, 1), emphasized-accelerate (0.3, 0, 0.8, 0.15), standard (0.2, 0, 0, 1). M2: simple 100 ms, medium 200–300, complex 300–500; enter 225 / exit 195; tablet +30 %, wearable −30 %. **code, DOM**
- Icons: 24 dp canvas, 20 dp live area, 2 dp padding, 2 dp stroke, keylines square 18 / circle 20, optical sizes 20/24/40/48. **design, px**

## 4. Microsoft Fluent 2 / Windows
https://fluent2.microsoft.design/layout, https://fluent2.microsoft.design/typography, https://learn.microsoft.com/en-us/windows/apps/design/

- Base unit **4 px**; all sizes and positions in multiples of 4 epx (text exempt). Spacing ramp 2, 4, 6, 8, 10, 12, 16, 20, 24, 28, 32, 36, 40, 48, 52, 56 px. **px, DOM**
- Touch target 7.5 mm ≈ **40 × 40 epx** (Windows); Fluent web/iOS 44; Android 48. **px, DOM**
- Windows spacing: 8 epx between buttons; 12 epx control–label; 16 epx surface-to-edge text; gutters 12 (< 640) / 24 epx (≥ 640). **px, DOM**
- Breakpoints: Windows ≤ 640 / 641–1007 / ≥ 1008; Fluent web 320, 480, 640, 1024, 1366, 1920; 12-column grid. **DOM**
- Type ramp (epx): Caption 12/16, Body 14/20, Body Strong 14/20 semibold, Body Large 18/24, Subtitle 20/28, Title 28/36, Title Large 40/52, Display 68/92; Fluent web adds Caption 2 10/14, Subtitle 2 16/22, Title 3 24/32, Title 1 32/40. **DOM**
- Minimum text 12 px regular / 14 px semibold; **50–60 characters per line** ideal, never < 20 or > 60; no bold/italic in the ramp; sentence case; left-align. **DOM, px**

## 5. GOV.UK Design System
https://design-system.service.gov.uk/

- Type scale (desktop → mobile, size/lh px): 80/80 → 53/55; 48/50 → 32/35; 36/40 → 27/30; 27/30 → 21/25; 24/30 → 21/25; 19/25 → 19/25; 16/20 → 16/20; line heights are multiples of 5 px; tablet breakpoint 640 px. **DOM**
- Body **19 px**, lead 24, small 16 (sparingly). **DOM**
- Spacing scale units 1–9: 5, 10, 15, 20, 25, 30, 40, 50, 60 px desktop (mobile 5, 10, 15, 15, 15, 20, 25, 30, 40). **DOM**
- Layout: page width 960 px (max 1020 incl. margins), gutter 30 / 15; text column ≤ **75 characters** (Service Manual: 60–70). **DOM, px**
- Focus: 3 px, yellow #ffdd00 background + black bottom border (links); yellow outline + thick black border (inputs). **px, DOM**

## 6. US Web Design System
https://designsystem.digital.gov/design-tokens/

- Spacing (8 px base): 1px, 2px, 4, 8, 12, 16, 20, 24, 32, 40, 48, 56, 64, 72, 80, 120, card 160/240, mobile 320/480, tablet 640/880, desktop 1024/1200, widescreen 1400. **DOM**
- Font sizes: theme 3xs 13, 2xs 14, xs 15, sm 16, md 17, lg 22, xl 32, 2xl 40, 3xl 48 px. **DOM**
- Measure tokens 44 / 60 / 64 / 68 / 72 / 88 ex. Line-height tokens 1, 1.15, 1.35, 1.5, 1.62, 1.75 (1.62 for reading text). **DOM**
- Colour "magic number" (grade difference): ≥ 40 → AA large (3:1); ≥ 50 → AA text (4.5:1) / AAA large; ≥ 70 → AAA (7:1). **code, px**

## 7. IBM Carbon
https://carbondesignsystem.com/

- 2x Grid mini unit 8 px; breakpoints sm 320 (4 cols), md 672 (8, 16 px margin), lg 1056 (16), xlg 1312, max 1584 (24 px margin); gutter 32 px. Aspect ratios 1:1, 2:1, 2:3, 3:2, 4:3, 16:9. **DOM**
- Spacing tokens 2, 4, 8, 12, 16, 24, 32, 40, 48, 64, 80, 96, 160 px. **DOM**
- Type scale `Yn = Yn−1 + {INT[(n−2)/4]+1}×2`, Y1 = 12: 12, 14, 16, 18, 20, 24, 28, 32, 36, 42, 48, 54, 60, 66, 72, 80, 88, 96, … **DOM**
- Type tokens: label-01 12/1.333/0.32 px; body-01 14/1.428/0.16; body-02 16/1.5; heading-03 20/1.4; heading-05 32/1.25; heading-07 54/1.19 light. Productive base 14 px, expressive 16. **DOM**

## 8. Ant Design
https://ant.design/docs/spec/layout, https://ant.design/docs/spec/font

- Base grid 8 px; 24-column grid; design board 1440 px with 1168 px content; all numbers multiples of 8. **DOM, px**
- Base font 14 px / line-height 22; scale 12/20, 14/22, 16/24, 20/28, 24/32, 30/38, 38/46, 46/54, 56/64, 68/76; weights 400/500/600; **use 3–5 sizes at most**; text alpha primary 88 %, secondary 65 %, disabled 25 %; border #D9D9D9; targets AAA 7:1. **DOM**

## 9. Shopify Polaris
https://github.com/Shopify/polaris/tree/main/polaris-tokens/src

- Space tokens 0, 1, 2, 4, 6, 8, 12, 16, 20, 24, 28, 32, 40, 48, 64, 80, 96, 112, 128 px (4 px base); button-group gap 8, card padding 16, table cell 6. **DOM**
- Font sizes 11 … 40 px; line heights 12–48; weights 450/550/650/700; letter-spacing −0.54 … 0. Breakpoints 0 / 490 / 768 / 1040 / 1440. **DOM**

## 10. Atlassian Design System
https://atlassian.design/foundations/spacing, /typography

- Space 0, 2, 4, 6, 8, 12, 16, 20, 24, 32, 40, 48, 64, 80 px; small 0–8 inside components, medium 12–24 container padding, large 32–80 between page content. **DOM**
- Headings xxl 32/36, xl 28/32, l 24/28, m 20/24, s 16/20, xs 14/20, xxs 12/16 (bold); body L 16/24, M 14/20 (default), S 12/16; paragraph spacing 16/12/8. **DOM**

## 11. Salesforce Lightning; 12. Adobe Spectrum; 13. Tailwind; 14. shadcn / Radix; 15. Bootstrap

- Lightning spacing 2, 4, 8, 12, 16, 24, 32, 48 px. **DOM**
- Spectrum font sizes desktop/mobile (≈ 1.125 ratio, mobile ≈ 1.25×): 25 = 10/12, 75 = 12/15, 100 = 14/17, 200 = 16/19, 300 = 18/22, 400 = 20/24, 500 = 22/27, 700 = 28/34, 900 = 36/44, 1000 = 40/49 … 1500 = 73/88; line-height 1.3 heading / 1.5 body; spacing 1, 2, 4, 6, 8, 12, 16, 20, 24, 32, 40, 48, 64, 80, 96; component height 32 desktop / 40 mobile; radii 3–16 px. **DOM**
- Tailwind: spacing 0.25 rem (4 px) × n; breakpoints 640/768/1024/1280/1536; containers up to 1280; radius 2/4/6/8/12/16/24/32; font xs 12/16, sm 14/20, base 16/24, lg 18/28, xl 20/28, 2xl 24/32, 3xl 30/36, 4xl 36/40, 5xl+ lh 1. **DOM, code**
- shadcn `--radius` 0.625 rem (10 px), sm…4xl = 0.6/0.8/1/1.4/1.8/2.2/2.6×; Radix space-1…9 = 4, 8, 12, 16, 24, 32, 40, 48, 64 px; scaling 90–110 %. **code, DOM**
- Bootstrap 5.3: breakpoints 576/768/992/1200/1400; containers 540/720/960/1140/1320; gutter 24 px. **DOM**

## 16. Typography canon

- **Bringhurst**, *Elements of Typographic Style* §2.1.2 (http://webtypography.net/2.1.2): measure **45–75 characters, 66 ideal**; multi-column 40–50. **DOM, px**
- **Butterick**, *Practical Typography* (https://practicaltypography.com/summary-of-key-rules.html): body 15–25 px on screen; line spacing 120–145 %; line length 45–90 chars; one space after a period; caps letter-spacing +5–12 %; first-line indent 1–4× size *or* paragraph space 4–10 pt, not both; all-caps only under one line. **DOM, px**
- Modular scale ratios 1.067, 1.125, 1.2, 1.25, 1.333, 1.414, 1.5, 1.618; 1.125–1.25 for dense UI, 1.333+ for marketing. **DOM**
- Web consensus (Smashing 2014, NN/g-derived): desktop 50–75 (up to 85), mobile 30–50; line-height ≈ 150 %; 16 px body minimum (Butterick, USWDS, GOV.UK small, Tailwind base). **DOM, px**
- Disagreement range for measure: **45–90**, sweet spot **60–75**.

## 17. Grid / spacing canon

- 8-pt grid (Bryn Jackson, spec.fm 2015): all dimensions multiples of 8; 4-pt half step inside components; icons 16/24/32/48; avoid 14, 18, 22, 30. Confirmed by Apple, Material, Windows (4), Carbon, Polaris, Tailwind, Radix, Atlassian, Spectrum, USWDS, Salesforce; **GOV.UK is the outlier (5 px)**. **px, DOM**
- 12-column grids: Fluent, Material expanded, Bootstrap, Tailwind; Ant 24; Carbon 16; GOV.UK fractional.

## 18. Layout canon

- Max content widths: Bootstrap 1320, Tailwind 1280, Ant 1168–1440, Carbon 1584, USWDS 1200/1400, GOV.UK 960, Polaris 1440; consensus 1140–1280 px on 1280–1440 viewports. **DOM**
- Laws of UX (https://lawsofux.com/): Fitts, proximity (no numbers); Doherty threshold 400 ms; Miller 7 ± 2; Hick's. NN/g response times 0.1 / 1 / 10 s. **manual / code**
- NN/g touch targets: 1 × 1 cm, ≥ 2 mm gap; fingertip 1.6–2 cm, thumb 2.5 cm. **px (needs DPI)**
- F/Z patterns, above-the-fold, white-space ratios: no numeric thresholds published. **manual**

## 19. Colour canon

- 60-30-10 (dominant/secondary/accent by area) — heuristic, no authoritative source. **px**
- Palette 3–5 colours, one accent; no platform states a colour count. **px, manual**
- Material dark: desaturated tone-200 primaries on #121212; text opacity 87/60/38 %; overlay 0–16 %. **px, DOM**
- Semantic bg/foreground token pairs (shadcn, M3, Polaris) → "foreground used on wrong background" is lintable. **code**

## 20. Motion; 21. Iconography

- Material 50–1000 ms (typical 150–400); enter 225 / exit 195; Apple 100–500; Doherty 400; NN/g 100 ms "instant"; `prefers-reduced-motion` per WCAG 2.3.3. **code, DOM**
- Material 24 dp canvas / 20 live / 2 stroke, optical 20/24/40/48; Apple 1–1.5 pt stroke, tab icons 25–28 pt, macOS 16/32/128/256/512; Windows list icons 32 epx; canon sizes 16/24/32/48. **design, px**

## Master table (deduplicated, with disagreements)

| Rule | Numbers by source | Detect |
|---|---|---|
| Min touch/pointer target | WCAG AA **24 px** (AAA 44); Apple **44 pt** (visionOS 60); Material **48 dp** (pointer 44); Windows 40 epx / 7.5 mm; Fluent web 44; NN/g 1 cm | px, DOM |
| Gap between targets | Material 8 dp; NN/g 2 mm; WCAG 24 px circle non-overlap | px, DOM |
| Text contrast | 4.5:1 / 3:1 large (WCAG, Apple, Material); AAA 7:1 (Ant targets AAA) | px, DOM |
| Non-text / icon / border contrast | 3:1 (WCAG 1.4.11, Material, GOV.UK focus) | px, DOM |
| Focus indicator | GOV.UK 3 px #ffdd00; WCAG AAA 2 px perimeter, 3:1 change | px, DOM |
| Minimum text size | Apple 11 pt (body 17); Material 11 sp (body 14); Windows 12 / 14 semibold; GOV.UK 16; Butterick/web 15–16 body; Spectrum 10 desktop | DOM, px |
| Default body size | Apple 17; Material 14–16; Windows 14; GOV.UK 19; USWDS 16–17; Atlassian/Ant/Carbon 14; Tailwind 16; Spectrum 14 / 17 mobile | DOM |
| Body line-height | WCAG ≥ 1.5; Butterick 1.2–1.45; Material ~1.43–1.5; Windows 1.43; GOV.UK ~1.32; USWDS 1.5–1.62; Spectrum 1.5; Apple ~1.3 | DOM |
| Heading line-height | Spectrum 1.3; USWDS 1.15; Carbon 1.19–1.4; Tailwind 5xl+ 1.0 | DOM |
| Line length | Bringhurst 45–75 (66); Butterick 45–90; WCAG ≤ 80; Windows 50–60; GOV.UK ≤ 75; mobile 30–50; USWDS 44–88 ex | DOM, px |
| Paragraph spacing | WCAG 2× size (1.4.12) / 1.5× line spacing (1.4.8); Butterick 4–10 pt | DOM |
| Letter/word spacing | WCAG 0.12 em / 0.16 em; caps +5–12 % | DOM |
| Type scale ratio | 1.067–1.618; Spectrum 1.125; Carbon additive; ≤ 3–5 sizes (Ant) | DOM |
| Spacing base unit | 4 px (Fluent, Tailwind, Polaris, Windows) / 8 px (Material, Apple, Carbon, Atlassian, USWDS, Ant); GOV.UK 5 px | px, DOM |
| Spacing scale | 2/4/8/12/16/24/32/48/64 (+40/80/96) across 10+ systems | DOM |
| Screen-edge margin | Apple 16/20 pt; Material 16/24 dp; Windows 12/24 epx; Carbon 16/24 px | px, DOM |
| Gutter | Bootstrap/Windows 24; GOV.UK 30; Carbon 32; Material 24 dp | DOM |
| Breakpoints | Material 600/840/1200/1600; Windows 640/1008; Bootstrap 576/768/992/1200/1400; Tailwind 640/768/1024/1280/1536; Carbon 320/672/1056/1312/1584; GOV.UK 640; Polaris 490/768/1040/1440; USWDS 480/640/880/1024/1200/1400 | DOM |
| Max content width | 960–1320 px; consensus 1140–1280 | DOM |
| Reflow / zoom | 320 px width, 200 % zoom (WCAG) | DOM |
| Grid alignment | 4/8 multiples; Windows all dims × 4 epx | px, DOM |
| Component heights | Apple bars 44/49 pt, row 44; Spectrum 32/40; Windows control 32 epx | px, DOM |
| Elevation | M3 0/1/3/6/8/12 dp; dark overlay 0–16 % | DOM, px |
| Text emphasis opacity | Material 87/60/38 % light, 100/70/50 % dark; Ant 88/65/25 % | DOM, px |
| Colour proportion | 60/30/10 heuristic; ≤ 3–5 hues | px |
| Flashing | ≤ 3/s; ≥ 10 % luminance over ≥ 25 % of a 10° field | px (frames) |
| Motion duration | Material 50–1000 ms (typical 150–400); enter 225 / exit 195; feedback ≤ 400 ms; 100 ms instant | code, DOM |
| Reduced motion | `prefers-reduced-motion` honoured (WCAG 2.3.3, Apple, Material) | DOM, code |
| Icon geometry | 24 canvas / 20 live / 2 stroke (Material); Apple 1–1.5 pt stroke; 16/24/32/48 | design, px |
| Orientation lock | none (WCAG 1.3.4) | code |
| Colour-only meaning | prohibited (WCAG 1.4.1) | manual / partial DOM |

Highest-value pixel-detectable lints from this set: contrast (text, non-text, focus), target size and gap, 4/8 px alignment of edges and gaps, text-size floor, line length, line-height ratio, colour-area ratio, edge margins, elevation/overlay consistency, flash detection.

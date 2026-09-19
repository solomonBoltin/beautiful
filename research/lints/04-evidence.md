# Empirically measured rules about interface quality — inventory with numbers

*Part of the [design-lint survey](../DESIGN-LINTS.md). Excludes what [SURVEY.md](../SURVEY.md)
already covers (Birkhoff, Ngo, Reinecke & Gajos, Miniukovich, Rosenholtz, Hasler–Süsstrunk,
Redies, Palmer & Schloss). Each entry: rule · study · effect size · N · URL · detectability.
⚠ = confirmed only through secondary sources. ✗ = folklore the lint must NOT encode.*

## 1. Reading and typography

### 1.1 Line length

| Rule | Study | Finding | N | Detect |
|---|---|---|---|---|
| ~55 CPL best comprehension; 100 CPL fastest on screen | Dyson & Haselgrove 2001, *IJHCS* 54:585 | 55 CPL better comprehension than 100; 100 read fastest; 55 "supports effective reading at normal and fast speeds" | adults 18–55 | DOM, px |
| 95 CPL read fastest online; users prefer the extremes | Shaikh & Chaparro 2005, *Usability News* 7(2) | 35/55/75/95 tested; 95 fastest; satisfaction unaffected; comprehension equal | 20 | DOM, px |
| No reliable speed difference among 45/76/132 CPL for adults ⚠ | Bernard et al. 2002 (SURL) | children preferred medium | — | — |

**Encoding:** flag body text < 35 or > 100 CPL; treat 45–95 as evidence-supported. The "66 characters" ideal is print typography, not screen evidence. Sources: [Dyson & Haselgrove](https://www.sciencedirect.com/science/article/abs/pii/S1071581901904586), [Dyson review](https://stu.westga.edu/~ssynan1/literacy/Dyson.pdf), [Shaikh & Chaparro](https://journals.sagepub.com/doi/abs/10.1177/154193120504900514), [Viget on the misconception](https://www.viget.com/articles/the-line-length-misconception).

### 1.2 Font size

| Rule | Study | Finding | N | Detect |
|---|---|---|---|---|
| Fluent reading needs x-height ≥ 0.2° visual angle (≈ 9–10 px x-height at desktop distance) | Legge & Bigelow 2011, *J. Vision* 11(5):8 | Reading speed flat over a 10× range; drops sharply below the critical print size | review | DOM |
| 12 pt read faster than 10 pt on screen; 12 vs 14 no difference ⚠ | Bernard et al. 2001/2002 (SURL) | small effect; Arial/Verdana preferred | 20–60 | DOM |
| Font choice alone changes an individual's reading speed by up to 35 %, no single best font | Wallace, Bylinskii, Dobres, Kerr et al. 2022, *ACM TOCHI* 29(4) | 16 fonts normalised by x-height; no comprehension loss | 352 | DOM (argues *against* rewarding any font) |
| 18 pt and wider character spacing speed dyslexic and non-dyslexic readers; line spacing matters less | Rello, Pielot, Marcos, Carlini 2013, W4A | — | 92 (46 dyslexic) ⚠ | DOM |
| BDA: 12–14 pt sans, 1.5 line spacing, no italics/underline for emphasis | British Dyslexia Association 2023 | guidance | — | DOM |

Sources: [Legge & Bigelow](https://jov.arvojournals.org/article.aspx?articleid=2191906), [Wallace 2022](https://dl.acm.org/doi/10.1145/3502222), [HFI on Bernard](https://www.humanfactors.com/Newsletters/more_about_fonts.html), [Rello 2013](https://pielot.org/pubs/Rello2013-W4A-SizeMatters.pdf), [BDA style guide](https://cdn.bdadyslexia.org.uk/uploads/documents/Advice/style-guide/BDA-Style-Guide-2023.pdf).

### 1.3 Contrast polarity

| Rule | Study | Finding | N | Detect |
|---|---|---|---|---|
| Dark text on light → better acuity and proofreading, young and old | Piepenbrock, Mayr, Mund, Buchner 2013, *Ergonomics* 56(7) | no extra ocular strain | 169 | px |
| The advantage is largest for small text | Piepenbrock, Mayr, Buchner 2014, *Human Factors* 56(5) | polarity × size interaction | — | px, DOM |
| Mechanism: smaller pupil under positive polarity | Piepenbrock et al. 2014, *Ergonomics* 57(11) | — | — | — |

**Encoding:** light-on-dark body text under ~16 px is a warning; dark mode is fine for large and UI text. Sources: [2013](https://pubmed.ncbi.nlm.nih.gov/23654206/), [2014 HF](https://journals.sagepub.com/doi/abs/10.1177/0018720813515509), [pupil](https://pubmed.ncbi.nlm.nih.gov/25135324/).

### 1.4 Letter spacing, line spacing, x-height

| Rule | Study | Finding | Detect |
|---|---|---|---|
| Standard letter spacing is optimal for normal readers; wider slows central-vision reading | Chung 2002, *IOVS* 43:1270 | peaks at standard spacing | DOM |
| Extra-large spacing helps dyslexic children (accuracy ×2, speed +20 % ⚠) | Zorzi et al. 2012, *PNAS* 109(28) | N = 94 children | DOM |
| Layouts must survive line-height 1.5, paragraph 2×, letter 0.12 em, word 0.16 em | WCAG 2.1 SC 1.4.12 (cites Zorzi) | normative | code (apply overrides, check clipping) |
| Double line spacing improved visual search on web pages | Ling & van Schaik 2007, *Interacting with Computers* 19(2) | F(2,124) = 38.83 | DOM |
| x-height, not point size, drives perceived size ⚠ | Beier, Oderkerk et al. 2021 | — | DOM (needs font metrics) |
| Sub-pixel rendering: +5 % speed, +17 % word recognition | Gugerty 2004; Dillon et al. CHI 2006 | low value on HiDPI today | px |

Sources: [Chung](https://pubmed.ncbi.nlm.nih.gov/11923275/), [Zorzi](https://pubmed.ncbi.nlm.nih.gov/22665803/), [WCAG 1.4.12](https://www.w3.org/WAI/WCAG22/Understanding/text-spacing.html), [Ling & van Schaik](https://www.sciencedirect.com/science/article/abs/pii/S0141938207000133), [Dillon](https://dl.acm.org/doi/10.1145/1124772.1124849), [Beier review](https://thereadabilityconsortium.org/wp-content/uploads/2023/07/1100000089-Beier-Vol16-HCI-089.pdf).

### 1.5 How people read on screens

| Rule | Study | Finding | Detect |
|---|---|---|---|
| 79 % scan, 16 % read word by word | Nielsen 1997 | lab study, small N | manual |
| Users read ~20 % of the words on an average page (28 % max) | Nielsen 2008 on Weinreich et al. 2008; 59,573 page views | 17 % of views < 4 s | DOM (word count) |
| F-shaped reading persists 2006 → 2019, desktop and mobile; a *failure* pattern good formatting suppresses | Nielsen 2006 (232 users); Pernice 2017; NN/g 2019 (500+) | — | manual; proxies: heading density, left-edge alignment |

Sources: [How users read](https://www.nngroup.com/articles/how-users-read-on-the-web/), [How little](https://www.nngroup.com/articles/how-little-do-users-read/), [F-pattern](https://www.nngroup.com/articles/f-shaped-pattern-reading-web-content-discovered/), [2019](https://www.nngroup.com/articles/how-people-read-online/).

## 2. Target size, Fitts's law, touch

| Rule | Study | Finding | N | Detect |
|---|---|---|---|---|
| ≥ 9.2 mm (discrete) / 9.6 mm (serial) thumb targets; errors stop improving above 9.6 / 7.7 mm | Parhi, Karlson & Bederson 2006, MobileHCI | verbatim from abstract | ~20 ⚠ | DOM (px → mm needs DPR) |
| Error rate > 40 % below 8 mm; drops sharply above 15 mm; touches systematically offset ⚠ | Henze, Rukzio, Boll 2011 ("100,000,000 Taps") | 91,731 installs, 120 M taps; offset compensation −7.79 % errors | 91,731 | DOM |
| 10 mm buttons → 98–99.4 % accuracy ⚠ | Lee & Zhai 2009 | — | — | DOM |
| Walking: 6.74 mm → up to 23 % error; 10 mm much better; 20 mm solves it ⚠ | Schildbach & Rukzio 2010 | — | — | DOM |
| Accuracy depends on screen position more than on age: centre ~7 mm, edges ~12 mm, corners ~2× spacing | Hoober 2017, UXmatters (field data) | edge lists ≥ 9–10 mm tall | large | DOM (position-aware) |
| Kiosk / large screens: ≥ 20 mm; plateau at 20 mm | Chen 2013; Duff 2010; Jackson (W3C TF summary) | Duff: 10 mm worst, 30 best | small | DOM |
| Platform minimums: Apple 44 pt (~7 mm); Material 48 dp (~9 mm) + 8 dp; Microsoft 9 mm ideal / 7 min / 2 mm gap; Fluent 40 epx | guidelines | — | — | DOM |
| WCAG 2.5.8 AA 24 × 24 px or non-overlapping 24 px circles; 2.5.5 AAA 44 × 44 | W3C | normative; cites Parhi | — | DOM |
| Fingertip 1.6–2 cm, thumb pad ~2.5 cm ⚠ | NN/g citing MIT Touch Lab | the "10–14 mm" figure could not be traced to a primary page | — | — |

Sources: [Parhi](https://www.microsoft.com/en-us/research/publication/target-size-study-for-one-handed-thumb-use-on-small-touchscreen-devices/), [Henze](https://eprints.lancs.ac.uk/id/eprint/57576/), [Hoober pt 3](https://www.uxmatters.com/mt/archives/2017/07/design-for-fingers-touch-and-people-part-3.php), [W3C summary](https://www.w3.org/WAI/GL/mobile-a11y-tf/wiki/Summary_of_Research_on_Touch/Pointer_Target_Size), [WCAG 2.5.8](https://www.w3.org/WAI/WCAG22/Understanding/target-size-minimum.html), [NN/g](https://www.nngroup.com/articles/touch-target-size/), [Microsoft](https://learn.microsoft.com/en-us/windows/apps/develop/input/guidelines-for-targeting), [LukeW](https://www.lukew.com/ff/entry.asp?1085=).

## 3. Choice, memory, grouping, alignment

| Rule | Study | Finding | Detect |
|---|---|---|---|
| Hick–Hyman: RT = a + b·log₂(n+1), a ≈ 200 ms, b ≈ 150 ms/bit | Hick 1952; Hyman 1953; Proctor & Schneider 2018 | holds for unpractised, equiprobable, memorised choices; weaker for visible options | DOM (cost model, not a cap) |
| Breadth beats depth: 16×32 (36 s) < 32×16 (46 s) < 8×8×8 (58 s) | Larson & Czerwinski CHI 1998 (N = 19 ⚠) | 512 leaves; moderate breadth + depth best | DOM |
| ✗ Miller 7 ± 2 is a *memory* limit, not a screen-item limit | Miller 1956; Cowan 2001 (*BBS* 24:87, capacity ≈ 4 chunks) | visible options need not be memorised | do NOT lint "> 7 items" |
| Grouping by proximity decays exponentially with relative distance | Kubovy & Wagemans 1995; Kubovy, Holcombe & Wagemans 1998 | f(v) = exp(−α(v/v₀ − 1)); one constant across subjects | px, DOM: intra/inter-group gap ratio near 1 is maximally ambiguous |
| Alignment JND: Weber fraction 0.02–0.04 for separation/length; vernier 2–5 arcsec | classic psychophysics (Weber; Westheimer) | misalignment of ~2–4 % of the reference span is noticed; 1 px edge offsets are above threshold | px, DOM: edge tolerance ≤ 1 px; gap consistency ≈ 3 % |
| ✗ "White space increases comprehension 20 % (Lin 2004)" is misattributed (Myhill traced it; Lin disowned it) | Real evidence: Chaparro, Baker, Shaikh, Hull, Brady 2004 — margins → slower reading but better comprehension | — | encode margins as comprehension-positive with a speed cost; never cite 20 % |

Sources: [Proctor & Schneider](https://web.ics.purdue.edu/~dws/pubs/ProctorSchneider_2018_QJEP.pdf), [Larson & Czerwinski](https://dl.acm.org/doi/10.1145/274644.274649), [Cowan](https://www.researchgate.net/publication/11830840_The_Magical_Number_4_in_Short-Term_Memory_A_Reconsideration_of_Mental_Storage_Capacity), [Kubovy & Wagemans](https://journals.sagepub.com/doi/10.1111/j.1467-9280.1995.tb00597.x), [Kubovy 1998](https://www.sciencedirect.com/science/article/abs/pii/S0010028597906733), [Weber for separation](https://opg.optica.org/josaa/abstract.cfm?uri=josaa-10-1-5), [vernier review](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC8523788/), [Myhill on Lin 2004](https://www.linkedin.com/pulse/lin-2004-did-discover-margins-white-space-increase-20-carl-myhill), [Chaparro 2004](https://portfolio.erau.edu/en/publications/reading-online-text-a-comparison-of-four-white-space-layouts/).

## 4. Colour and contrast

| Rule | Study | Finding | Detect |
|---|---|---|---|
| WCAG 4.5:1 = ANSI 3:1 × 1.5 contrast-sensitivity loss at 20/40 (Arditi & Faye); 7:1 ≈ 20/80; large text 3:1 | WCAG Understanding 1.4.3 / 1.4.6 | derivation stated explicitly | px, DOM |
| APCA Lc levels: 90 body preferred; 75 body minimum; 60 non-body; 45 headlines; 30 spot text; 15 non-text (≥ 5 px) — with font-size/weight lookup | Somers / Myndex APCA (WCAG 3 candidate) | polarity-aware; Lc 60 ≈ 3:1, 75 ≈ 4.5:1, 90 ≈ 7:1 in light mode | px, DOM (needs size and weight) |
| ΔE JND ≈ 1.0; 2.3 ΔE76 average perceptibility; > 5 clearly different | Mahy, Van Eycken, Oosterlinck 1994 | — | px, DOM: near-duplicate palette colours ΔE < 2.3 |
| ~7 hues can be found rapidly in a display | Healey 1996, IEEE Vis | pre-attentive search limit | px (hue clusters) |
| ≤ 8 categorical colours by hue for CVD safety ⚠ | Cloudscape / data-design standards citing Ware | — | DOM |
| Red-green CVD: ~8 % men, ~0.5 % women (N. European) | Birch 2012, *JOSA A* 29:313 | meta | px (simulate deutan/protan) |
| Preference ≠ harmony: both rise with hue similarity; figure legibility rises with hue and lightness contrast | Schloss & Palmer 2011, *APP* 73:551 | — | px: score harmony by hue similarity, legibility by contrast; do not conflate |
| Colour-emotion axes (warm–cool, heavy–light, active–passive) predictable from CIELAB, culture-independent | Ou, Luo, Woodcock, Wright 2004, *Color Res. Appl.* 29 | 3 factors | px |
| High saturation → visual discomfort (fNIRS); red text most fatiguing ⚠ | 2022 fNIRS study | moderate | px (area-weighted chroma) |

Sources: [WCAG 1.4.3](https://www.w3.org/WAI/WCAG21/Understanding/contrast-minimum.html), [APCA in a nutshell](https://git.apcacontrast.com/documentation/APCA_in_a_Nutshell.html), [colour difference](https://en.wikipedia.org/wiki/Color_difference), [Mahy 1994 discussion](http://johnthemathguy.blogspot.com/2017/07/is-10-delta-e-just-noticeable-difference.html), [Healey](https://vis.cs.brown.edu/docs/pdf/Healey-1996-CEC.pdf), [Cloudscape](https://cloudscape.design/foundation/visual-foundation/data-vis-colors/), [Birch](https://www.researchgate.net/publication/223985289_Worldwide_prevalence_of_red-green_color_deficiency), [Schloss & Palmer](https://palmerlab.berkeley.edu/pdf/Schloss&Palmer(2011).pdf), [Ou & Luo](https://onlinelibrary.wiley.com/doi/abs/10.1002/col.20010).

## 5. Layout perception, first impressions, aesthetics–usability

| Rule | Study | Finding | N | Detect |
|---|---|---|---|---|
| Visual appeal judged in 50 ms; 50 ms ratings correlate with 500 ms | Lindgaard, Fernandes, Dudek, Brown 2006, *BIT* 25(2) | 3 studies | ~40 each | px (global statistics dominate) |
| Complexity and prototypicality act at 17 ms; prototypicality grows with exposure | Tuch, Presslaber, Stöcklin, Opwis, Bargas-Avila 2012, *IJHCS* 70(11) | 119 screenshots | — | px |
| Beauty ↔ perceived usability r ≈ 0.59–0.60; weak with actual usability | Kurosu & Kashimura 1995; Tractinsky 1997 | replicated cross-culturally | 252 / 104 | manual (the justification for a beauty lint) |
| Symmetry/balance predict appeal but are moderated by gender and expertise; slightly broken symmetry is penalised heavily; complexity raises liking | Bauerly & Liu 2006; Tuch 2010; Gartus & Leder 2013; Leder 2019 ("Symmetry is not a universal law of beauty") | — | — | px: weight symmetry modestly; penalise *near*-symmetry more than clear asymmetry |
| Users prefer non-minimalist bar charts (low data-ink ratio) | Inbar, Tractinsky & Meyer 2007, ECCE | 87 students | 87 | do not reward data-ink maximisation |

Sources: [Lindgaard](https://www.tandfonline.com/doi/abs/10.1080/01449290500330448), [Tuch 2012](https://storage.googleapis.com/gweb-research2023-media/pubtools/pdf/38315.pdf), [aesthetic–usability](https://en.wikipedia.org/wiki/Aesthetic%E2%80%93usability_effect), [Bauerly & Liu](https://www.sciencedirect.com/science/article/abs/pii/S1071581906000048), [Gartus & Leder](https://pmc.ncbi.nlm.nih.gov/articles/PMC3859553/), [Leder 2019](https://journals.sagepub.com/doi/full/10.1177/0276237418777941), [Inbar](https://www.semanticscholar.org/paper/81eb351c2c0ed8a4407db6e294eb0de904c5c85c).

## 6. Scroll, fold, attention, ads

| Rule | Study | Finding | Detect |
|---|---|---|---|
| 57 % of viewing time above the fold; 74 % in the first two screenfuls; 80 % in 2010 | NN/g Fessenden 2018 eyetracking | — | DOM (weight by vertical position) |
| 66 % of engaged time below the fold; median scroll depth ~1000–1500 px | Chartbeat 2013 (2 B visits) | — | DOM |
| Banner blindness: ad-like items found 58 % vs 94 % | Benway & Lane 1998 | — | px, DOM (essential content styled as ad boxes) |
| Banner blindness persists on mobile and desktop | Pernice 2018 | — | same |
| ✗ "CTA above the fold" is not a law: +304 % moving the CTA *below* on a complex offer (confounded) | CXL / Aagaard | single A/B | manual |
| Hidden (hamburger) nav: desktop use 27 % vs 48 % visible / 50 % combo; ≥ 39 % slower desktop, 15 % mobile | Pernice & Budiu 2016, N = 179 | — | DOM |
| Core Web Vitals: LCP ≤ 2.5 s, CLS ≤ 0.1, INP ≤ 200 ms (p75); thresholds chosen so ~10 % of origins are "poor" | web.dev | CrUX | code |
| Load 1 → 3 s: +32 % mobile bounce; → 5 s: +90 %; 53 % abandon over 3 s | Google/SOASTA 2017 (900k pages) | industry | code |

Sources: [NN/g scrolling](https://www.nngroup.com/articles/scrolling-and-attention/), [Chartbeat via Slate](https://slate.com/technology/2013/06/how-people-read-online-why-you-wont-finish-this-article.html), [Benway 1998](https://www.ruf.rice.edu/~lane/papers/banner_blindness.pdf), [Pernice 2018](https://www.nngroup.com/articles/banner-blindness-old-and-new-findings/), [CXL fold](https://cxl.com/blog/above-the-fold/), [NN/g hamburger](https://www.nngroup.com/articles/hamburger-menus/), [CWV thresholds](https://web.dev/articles/defining-core-web-vitals-thresholds), [Google 2017](https://blog.amp.dev/2017/02/28/new-industry-benchmarks-for-mobile-page-speed/).

## 7. Mobile ergonomics

| Rule | Study | Finding | Detect |
|---|---|---|---|
| 49 % one-handed thumb; 36 % cradle; 15 % two thumbs; ~75 % thumb-driven | Hoober 2013 (1,333 observations) | — | DOM |
| Thumb reach = quadratic model of screen size, hand size and grip; bottom-inner reachable, top-far corner not | Bergstrom-Lehtovirta & Oulasvirta CHI 2014 (N = 20) | — | DOM (reachability of primary controls) |
| ✗ "96 % tap accuracy bottom vs 61 % top (NN/g)" — found only in a marketing post; unverified | — | — | — |

Sources: [Hoober 2013](https://www.uxmatters.com/mt/archives/2013/02/how-do-users-really-hold-mobile-devices.php), [Bergstrom-Lehtovirta](http://www.netlab.tkk.fi/~oulasvir/pubs/paper2117.pdf).

## 8. Icons and labels; 9. Forms

| Rule | Study | Finding | Detect |
|---|---|---|---|
| Label-only and icon+label beat icon-only for learning; benefit fades with practice | Wiedenbeck 1999, *BIT* 18(2) | — | DOM (icon buttons without text) |
| Universal icons are rare (home, search, print); icons need labels | NN/g Harley 2014 | — | DOM |
| Top-aligned labels: 50 ms saccade; right-aligned left labels 170–240 ms; left-aligned left labels ~500 ms; bold labels +60 % ⚠ | Penzo 2006, UXmatters | informal | DOM |
| Inline validation: +22 % success, −22 % errors, +31 % satisfaction, −42 % time ⚠ | Wroblewski / Etre 2009, A List Apart (N = 22) | — | code |
| 11 → 4 fields: +120 % conversion | Imagescape (single site) | — | DOM |
| Checkout averages 11.3 fields / 5.1 steps; 8 suffice; 17 % abandon for complexity | Baymard 2024 | benchmark | DOM |
| Field width should match expected input length | Baymard | qualitative | DOM |

Sources: [Wiedenbeck](https://www.tandfonline.com/doi/abs/10.1080/014492999119129), [NN/g icons](https://www.nngroup.com/articles/icon-usability/), [Penzo](https://www.uxmatters.com/mt/archives/2006/07/label-placement-in-forms.php), [A List Apart](https://alistapart.com/article/inline-validation-in-web-forms/), [Imagescape](https://www.imagescape.com/media/filer_public/06/94/0694c7f4-8914-4598-8871-b857fbc12737/form_case_study.pdf), [Baymard fields](https://baymard.com/blog/checkout-flow-average-form-fields), [Baymard width](https://baymard.com/blog/form-field-usability-matching-user-expectations).

## 10. Accessibility population numbers

| Number | Source | Detect |
|---|---|---|
| 94.8 % of top-1M home pages fail WCAG A/AA; 51 errors/page | WebAIM Million 2025 | DOM |
| Low-contrast text on 79.1 % of pages; missing alt 55.5 %; missing labels 48.2 %; empty links 45.4 %; empty buttons 29.6 %; missing lang 15.8 % — six categories = 96 % of errors | WebAIM Million 2025 | DOM |
| ≥ 2.2 billion people with vision impairment | WHO World Report on Vision 2019 | — |
| 35.4 % of US adults ≥ 40 have vestibular dysfunction | Agrawal et al. 2009, NHANES | code (reduced motion) |
| ~8 % men / 0.5 % women red-green CVD | Birch 2012 | px |

Sources: [WebAIM Million 2025](https://webaim.org/projects/million/2025), [WHO](https://www.who.int/news-room/fact-sheets/detail/blindness-and-visual-impairment), [NHANES](https://pubmed.ncbi.nlm.nih.gov/19468085/), [C39](https://www.w3.org/WAI/WCAG22/Techniques/css/C39).

## 11. Industry folklore — status

| Claim | Status |
|---|---|
| Google "41 shades of blue" → +$200 M/yr | real experiment; revenue anecdotal; do not derive a hue threshold |
| "Lin 2004: white space +20 % comprehension" | ✗ misattributed |
| "Miller 7 ± 2 menu items" | ✗ misapplied |
| "CTA must be above the fold" | contradicted by CXL case; NN/g 2018 gives attention weighting, not a rule |
| Amazon "100 ms = 1 % sales" | unsourced; do not encode |

## Master table

| # | Rule | Number | Evidence | Detect |
|---|---|---|---|---|
| 1 | Body line length | 45–95 CPL ok; ~55 best comprehension; 95–100 fastest | replicated | DOM, px |
| 2 | Minimum text size | x-height ≥ 0.2° (≈ 9–10 px x-height; ≥ 12 pt ≈ 16 px body) | replicated | DOM |
| 3 | No universal best font | up to 35 % WPM spread per person | single large study | DOM (don't reward a font) |
| 4 | Contrast polarity | dark-on-light for small text | replicated ×3 | px |
| 5 | Letter spacing | standard; wider only for a dyslexia mode | replicated | DOM |
| 6 | Line height | tolerate 1.5; 2.0 aids search; ≥ 1.4 dyslexia | mixed | DOM |
| 7 | Text-spacing robustness | 1.5 / 2× / 0.12 em / 0.16 em must not clip | normative | code |
| 8 | Touch target size | ≥ 9.2–9.6 mm (≈ 44–48 px @ 160 dpi); < 8 mm → > 40 % error | replicated | DOM |
| 9 | Target spacing | ≥ 2 mm / 8 dp; corners ~2× | industry + field | DOM |
| 10 | WCAG target size | 24 AA / 44 AAA | normative | DOM |
| 11 | Position-aware size | centre 7 mm, edges 12 mm | industry | DOM |
| 12 | Choice cost | RT ≈ 200 + 150·log₂(n+1) ms | replicated | DOM |
| 13 | Nav breadth/depth | 2 levels × 16–32 over 3 × 8 | single + model | DOM |
| 14 | Hidden nav | −20 % discoverability, +39 % time desktop | N = 179 | DOM |
| 15 | Proximity grouping | exponential in relative distance; gap ratio ≈ 1 is ambiguous | replicated | px, DOM |
| 16 | Alignment tolerance | edges ≤ 1 px; gaps ≤ ~3 % | psychophysics | px, DOM |
| 17 | Text contrast | 4.5 / 3 / 7; APCA Lc 75 body, 60 UI, 45 headline, 30 spot, 15 non-text | normative + derivation | px, DOM |
| 18 | Colour duplicates | ΔE < 2.3 same; > 5 distinct | replicated | px, DOM |
| 19 | Distinct hues | ≤ 7 pre-attentive; ≤ 8 categorical | single + guidance | px |
| 20 | CVD safety | 8 % men; simulate | replicated | px |
| 21 | Harmony vs legibility | hue similarity vs hue/lightness contrast | replicated | px |
| 22 | Colour emotion | Ou–Luo CIELAB models | replicated | px |
| 23 | First impression | stable at 50 ms; complexity/prototypicality at 17 ms | replicated | px |
| 24 | Aesthetic–usability | r ≈ 0.59–0.60 | replicated | manual |
| 25 | Symmetry/balance | positive but moderated; near-symmetry penalised | mixed | px |
| 26 | Data-ink minimalism | users prefer non-minimal | single | px |
| 27 | Above-fold weighting | 57 % attention above fold | industry eyetracking | DOM |
| 28 | Banner-like styling | found 58 % vs 94 % | replicated | px, DOM |
| 29 | Layout stability | CLS ≤ 0.1; LCP ≤ 2.5 s; INP ≤ 200 ms | industry | code |
| 30 | Speed | 1 → 3 s = +32 % bounce | industry | code |
| 31 | Thumb reach | 49 % one-thumb; quadratic model | field + model | DOM |
| 32 | Icons need labels | label > icon-only | single + NN/g | DOM |
| 33 | Label placement | top 50 ms vs left 500 ms | informal | DOM |
| 34 | Inline validation | −42 % time, −22 % errors | single | code |
| 35 | Form fields | fewer; 8 suffice | industry | DOM |
| 36 | Field width | match expected length | qualitative | DOM |
| 37 | Word count | users read ~20 % | single large dataset | DOM |
| 38 | Reduced motion | 35 % of 40+ vestibular | population survey | code |
| 39 | Prevalence baseline | 79 % pages low-contrast; 94.8 % fail | industry crawl | DOM |

**Not encodable / debunked:** Miller 7 ± 2 for on-screen items; "Lin 2004 +20 %"; "CTA above the fold"; 41-shades hue; the "96 % / 61 %" tap figure.

**Still secondary-sourced (verify before shipping a threshold):** Bernard SURL Ns; Henze's "> 40 % below 8 mm"; Lee & Zhai and Schildbach numbers; MIT Touch Lab fingertip widths; Zorzi 2012 effect sizes; Larson & Czerwinski N; Ou–Luo equation constants; Ware's 5–10 colour-code claim (use Healey's 7).

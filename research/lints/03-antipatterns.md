# Design no-gos, anti-patterns and smells — inventory

*Part of the [design-lint survey](../DESIGN-LINTS.md). 194 items from 48 sources (NN/g ×12,
deceptive.design, Smashing ×3, FTC/EDPB/DSA, Baymard ×2, Supercharge ×2, HansCo, MockFlow,
Balsamiq, Access Guide, 925studios, dev.to ×3, vibecodekit, Canva, data-viz ×5, Web Pages That
Suck, and others). Detectability: **px** = pixels/screenshot, **dom** = DOM/CSS, **code** =
source/markup, **man** = manual judgement. Items are numbered so the ranked list can reference them.*

## 1. Navigation & information architecture

| # | No-go | Why | Source | Detect |
|---|---|---|---|---|
| 1 | Hidden/hamburger navigation on desktop | Discoverability −20%, tasks 39% slower | NN/g [Hamburger Menus](https://www.nngroup.com/articles/hamburger-menus/) | dom, px |
| 2 | Mystery-meat navigation (icons/images whose destination is unknown until hover) | Users can't predict link targets | Flanders, [Web Pages That Suck](http://www.webpagesthatsuck.com/mysterymeatnavigation.html) | dom, man |
| 3 | Icons without visible text labels | Recognition varies wildly | NN/g [Icon Usability](https://www.nngroup.com/articles/icon-usability/) | dom, px |
| 4 | Too many navigation techniques on one page | Combined menus, tabs, sidebars, breadcrumbs create a mess | NN/g [Top 10 Mistakes](https://www.nngroup.com/articles/top-10-mistakes-web-design/) | dom, man |
| 5 | Competing/near-duplicate link labels and categories | Users can't tell which path leads where | NN/g [Top 10 Enduring](https://www.nngroup.com/articles/top-10-enduring/) | dom, man |
| 6 | Poor category names (org chart, not user mental model) | People can't locate what they need | NN/g Top 10 Enduring | man |
| 7 | Centered logo on desktop | Users 6× more likely to fail to reach home | NN/g [Centered Logos](https://www.nngroup.com/articles/centered-logos/) | dom, px |
| 8 | Missing "Home" link / logo link | Users get stranded | Flanders; NN/g Enduring | dom |
| 9 | Not changing visited-link colour | Navigational disorientation | NN/g Top 10 Mistakes | dom |
| 10 | Links that look like ads / placed in ad positions | Banner blindness makes them invisible | NN/g Top 10 Mistakes | px, man |
| 11 | Repetitive links | Redundant interaction cost | NN/g Top 10 Enduring | man |
| 12 | Islands of information (no cross-links) | Users must piece things together | NN/g Top 10 Enduring | man |
| 13 | Splash pages / intro screens | Pure interaction cost | Flanders ([SitePoint](https://www.sitepoint.com/flanders-web-pages-suck/)) | dom, man |
| 14 | Opening new browser windows unasked | Kills Back, disorients | NN/g Top 10 Mistakes | code |
| 15 | PDFs for online reading | Breaks browser flow | NN/g Top 10 Mistakes | code |
| 16 | Violating platform/web conventions | Users expect familiar behaviour | NN/g [Heuristic #4](https://www.nngroup.com/articles/ten-usability-heuristics/) | man |
| 17 | Mega-dropdown hover menus that trigger accidentally | Error-prone | Smashing [Frustrating Design Patterns](https://www.smashingmagazine.com/2021/09/smashing-workshop-frustrating-design-patterns/) | dom, man |
| 18 | Overcomplicated navigation with unclear labels | Abandonment | MockFlow [18 UI Mistakes](https://mockflow.com/blog/ui-design-mistakes) | man |

## 2. Content, readability & text density

| # | No-go | Why | Source | Detect |
|---|---|---|---|---|
| 19 | Walls of text / non-scannable paragraphs | Scannable layout +47% usability | NN/g [Concise, Scannable](https://www.nngroup.com/articles/concise-scannable-and-objective-how-to-write-for-the-web/), [Chunking](https://www.nngroup.com/articles/chunking/) | dom, px |
| 20 | Overwhelming information density / clutter | Hard to scan | NN/g Enduring; MockFlow #18; Heuristic #8 | px, dom |
| 21 | Lorem-ipsum / placeholder residue | Signals unfinished, machine-generated | AI-slop sources (§12) | dom |
| 22 | Weightless generic headline copy ("Build faster. Ship smarter.") | Says nothing; AI tell | [925studios AI Slop Tells](https://www.925studios.co/blog/ai-slop-design-tells) | dom, man |
| 23 | Not answering users' questions (price missing) | Price is the key qualifier | NN/g Top 10; Enduring | man |
| 24 | Fixed/unresizable font size | Hurts readers over 40 | NN/g Top 10 Mistakes | dom |
| 25 | Poor / overly literal search | Can't handle typos, plurals | NN/g | man |
| 26 | Jargon instead of users' language | Heuristic #2 | NN/g Heuristics | man |
| 27 | Vague error messages / no recovery guidance | Heuristic #9 | NN/g; Smashing [Error Messages](https://medium.com/@smashingmag/designing-better-error-messages-ux-f89ed25cb795) | dom, man |

## 3. Typography

| # | No-go | Why | Source | Detect |
|---|---|---|---|---|
| 28 | Low-contrast text (grey on grey, light grey on white) | Legibility, confidence, mobile glare | NN/g [Low-Contrast Text](https://www.nngroup.com/articles/low-contrast/); HansCo; Supercharge | px, dom |
| 29 | Tiny type (< ~14–16px body; never below 8pt) | Unreadable on mobile | NN/g; Smashing [Tap Targets](https://www.smashingmagazine.com/2023/04/accessible-tap-target-sizes-rage-taps-clicks/) | dom, px |
| 30 | Too many typefaces (> 2–3) | No hierarchy | HansCo [Bad Typography](https://hanscostudio.com/bad-typography-examples/); Skillshare | dom, px |
| 31 | Centered body text / long centered paragraphs | Ragged start positions disrupt reading | HansCo; MockFlow | dom, px |
| 32 | Justified text producing rivers | Uneven gaps distract | HansCo; [Pagination.com](https://pagination.com/fix-typography-rivers-widows-orphans/) | dom, px |
| 33 | Widows / orphans / runts | Visual imbalance | HansCo; [Superside](https://www.superside.com/knowledge/widows-vs-orphans); Typefi | px, dom |
| 34 | Bad leading (too tight/loose) | Legibility | HansCo; [Digital Ink](https://www.digital.ink/blog/typography-mistakes/) | dom |
| 35 | Bad tracking / letterspaced lowercase | Word-shape recognition | HansCo | dom |
| 36 | Poor kerning in headings/logos | Off-balance pairs | HansCo | px |
| 37 | All-caps body / overuse of caps, bold, italics | "Loud and disorganised" | HansCo; Skillshare [5 Typography Mistakes](https://www.skillshare.com/en/blog/typography-mistakes/) | dom |
| 38 | Faux bold / faux italic | Distorted glyphs | Typefi [Common typographic issues](https://help.typefi.com/hc/en-us/articles/360003700755-Common-typographic-issues) | dom, code |
| 39 | Long line lengths (> ~75 chars) | Eye loses the return sweep | NN/g Chunking (50–75) | dom |
| 40 | Insufficient paragraph spacing | Text becomes a wall | NN/g Chunking | dom |
| 41 | Display fonts used for body | Aesthetics over clarity | HansCo | dom, man |
| 42 | Inconsistent type hierarchy | Weak structure | HansCo; MockFlow #16 | dom |
| 43 | Text over busy images without scrim | Unreadable | Erik Kennedy [7 Rules](https://www.learnui.design/blog/7-rules-for-creating-gorgeous-ui-part-1.html) | px |
| 44 | Text so cramped it is illegible | — | Flanders | px |
| 45 | Inter/Roboto as the only font with no pairing decision | AI tell; generic | 925studios; [dev.to Purple Gradient](https://dev.to/james_anderson_h/the-purple-gradient-problem-why-ai-ui-all-looks-alike-and-how-to-fix-it-3j65) | dom |

## 4. Layout & composition

| # | No-go | Why | Source | Detect |
|---|---|---|---|---|
| 46 | Horizontal overflow / sideways scroll | Content cut off | [dev.to Mobile CSS](https://dev.to/ohugonnot/mobile-css-consistency-all-best-practices-in-2026-4l5l); RapidDev | dom, px |
| 47 | Content clipped at container edges | Information lost | RapidDev | px, dom |
| 48 | Overlapping elements | Broken rendering | general | dom, px |
| 49 | Misaligned edges / mixed alignment in one row | Visual tension | UXPin [Alignment](https://www.uxpin.com/studio/blog/alignment-in-design-making-text-and-visuals-more-appealing/); Brucira | px, dom |
| 50 | Too many alignment points / off-grid elements | No visual order | UXPin; UXMagic | px, dom |
| 51 | Inconsistent spacing (not on a 4/8px scale) | Unpolished | Design Systems Collective [Spacing](https://www.designsystemscollective.com/spacing-alignment-in-ui-creating-visual-rhythm-and-breathing-room-2c382b112272) | dom |
| 52 | Elements touching viewport edges / unequal margins | Cramped, unbalanced | Anonymous Design [Layout Mistakes](https://anonymous.com.sg/common-ui-layout-mistakes-and-how-to-fix-them-quickly/) | px, dom |
| 53 | Cramped elements, no white space | "Double your white space" | Erik Kennedy; Brucira | px, dom |
| 54 | Everything centered / no left-aligned anchor | Removes reading axis | HansCo; UXPin | dom |
| 55 | Missing visual hierarchy | Eye doesn't know where to look | MockFlow #16; Brucira [12 Problems](https://blog.brucira.com/ui-ux-design-best-practices/) | px |
| 56 | Giant hero with nothing peeking above the fold ("false floor") | Illusion of completeness stops scrolling | NN/g [Illusion of Completeness](https://www.nngroup.com/articles/illusion-of-completeness/); CXL [False Bottom](https://cxl.com/blog/false-bottom/) | px, dom |
| 57 | Sticky headers/footers/banners covering content | Reduces usable viewport | Smashing | dom, px |
| 58 | Layout shift (CLS) — media without reserved dimensions | Content jumps | [21st.dev](https://21st.dev/blog/react-scroll-animation-components); Thrive | dom, code |
| 59 | Z-index pile-ups | Elements hidden behind others | general | dom |
| 60 | Pages/images too heavy | Slow load | Flanders; MockFlow #10 | code |
| 61 | Frames / iframes for layout | Breaks navigation | Flanders | dom |
| 62 | Inconsistent design across pages | Disorientation | MockFlow #5; Heuristic #4 | dom |
| 63 | Nested cards inside cards | Visual noise; AI tell | dev.to Purple Gradient | dom |
| 64 | Same corner radius on everything / not scaled to element size | "The most common smell" | [92learns Border Radius](https://blog.92learns.com/border-radius-rules/); CodeFronts | dom |
| 65 | Mixed rounded and sharp corners on siblings | Inconsistency | 92learns | dom |
| 66 | Inner radius = outer radius on nested elements | Corners look wrong | 92learns; CodeFronts | dom |
| 67 | Overuse/misuse of shadows | Clutter without depth meaning | MockFlow #6 | dom |
| 68 | Multiple light sources / light from below | "Light comes from the sky" | Erik Kennedy; CodeFronts | dom, px |
| 69 | Competing calls-to-action | Split attention; −266% conversions | Brucira; [KlientBoost](https://www.klientboost.com/landing-pages/landing-page-mistakes/); CXL | dom |
| 70 | Orphan/lonely elements outside any group | Breaks proximity | Anonymous Design | px |
| 71 | Tombstoning (headings stacked in adjacent columns at same height) | Reads as one heading | Typefi | px |

## 5. Colour

| # | No-go | Why | Source | Detect |
|---|---|---|---|---|
| 72 | Pure #000 on pure #FFF | Harsh, eye strain | Supercharge [Pure Black & White](https://supercharge.design/articles/pure-black-and-pure-white-in-ui-design) | dom |
| 73 | Rainbow / too many hues | Chaotic | Supercharge [8 UI Color Mistakes](https://supercharge.design/blog/8-common-ui-color-mistakes); CareerFoundry [7 Palette Mistakes](https://careerfoundry.com/en/blog/ui-design/common-color-palette-mistakes/) | px, dom |
| 74 | Clashing colours / neon on neon | Hard on eyes | Supercharge 8; MockFlow #4 | px |
| 75 | Over-saturated large areas (esp. dark mode) | Visual vibration | Supercharge [Dark UI](https://supercharge.design/articles/6-mistakes-to-avoid-in-dark-ui-design) | px |
| 76 | Large bright surfaces in dark UI | Overpower design | Supercharge Dark UI | px |
| 77 | Shadows for depth in dark mode instead of layering | Invisible depth | Supercharge Dark UI | dom |
| 78 | Accent colour on non-interactive things | False affordance | Supercharge | dom |
| 79 | Colour as the only signal | Fails colourblind users | a11y-collective [Colour mistakes](https://www.a11y-collective.com/blog/common-mistakes-with-using-colour-in-accessibility/) | dom, man |
| 80 | Low-contrast placeholder text | Placeholders must meet contrast | a11y-collective | dom |
| 81 | Inconsistent colour meanings | Decoration mistaken for controls | Supercharge 8 | dom |
| 82 | Brand palette applied raw to product UI | Every screen looks like marketing | — | man |
| 83 | Gradient overuse / gradient text on numbers | AI tell | dev.to; 925studios | dom |
| 84 | Purple/indigo-to-blue hero gradient; untouched Tailwind indigo-500 | The canonical AI-slop tell | [dev.to Tailwind Indigo](https://dev.to/alanwest/why-every-ai-built-website-looks-the-same-blame-tailwinds-indigo-500-3h2p) | dom, px |
| 85 | Inconsistent greys (many near-identical tokens) | Incoherence | [dev.to "Why AI UIs look off"](https://dev.to/kiwibreaksme/why-ai-generated-uis-look-off-and-the-one-principle-that-fixes-it-4j20) | dom |
| 86 | Dark-mode inversion errors (images/shadows/logos not adapted) | Broken dark theme | Supercharge Dark UI | px |
| 87 | Following colour trends blindly | Dates quickly | Supercharge 8 | man |

## 6. Imagery & iconography

| # | No-go | Why | Source | Detect |
|---|---|---|---|---|
| 88 | Stretched/distorted images | Amateurish | [LinkedIn](https://www.linkedin.com/advice/3/how-can-you-avoid-common-mistakes-web-design-images); Canva | dom, px |
| 89 | Pixelated/blurry upscales, low-res logos | Loss of trust | [PerfectVector](https://perfectvector.com/blog/pixelated-logo); NN/g Bad Icons | px, dom |
| 90 | Raster logo where SVG is needed | Blurs on HiDPI | [Mykola Designer](https://www.mykoladesigner.com/article/logo-dimensions-for-website) | code |
| 91 | Wrong crop / aspect errors on cards | Heads cut off | Canva | px |
| 92 | Mixed icon styles / inconsistent stroke weights | Incoherence | dev.to "look off"; 92learns | px, dom |
| 93 | Generic thin-line icons atop every card | AI tell | 925studios | px |
| 94 | Emoji as UI icons | Inconsistent across OS | [vibecodekit](https://vibecodekit.dev/ai-slop-design), SmoothUI | dom |
| 95 | Icons with an established different meaning repurposed | Misread | NN/g [Bad Icons](https://www.nngroup.com/articles/bad-icons/) | man |
| 96 | Esoteric icon metaphors | Too many inferences | NN/g Bad Icons | man |
| 97 | Redundant identical icons next to every list item | Adds nothing | NN/g Bad Icons | dom |
| 98 | Icons only meaningful as a set | Fail alone | NN/g Bad Icons | man |
| 99 | Purposeless images / stock clichés | Clutter | MockFlow #9 | man |
| 100 | Missing alt / decorative images not marked | Accessibility | MockFlow #11 | code |

## 7. Affordance & interaction (visually detectable)

| # | No-go | Why | Source | Detect |
|---|---|---|---|---|
| 101 | Flat UI with weak signifiers | +22% task time, +25% fixations | NN/g [Flat UI Elements](https://www.nngroup.com/articles/flat-ui-less-attention-cause-uncertainty/) | px, dom |
| 102 | Links not distinguishable | Users can't find them | Balsamiq [Buttons vs Links](https://balsamiq.com/blog/buttons-links/) | dom |
| 103 | Buttons that look like labels / vice versa | Ambiguous clickability | Balsamiq [17 Button Practices](https://balsamiq.com/blog/button-design-best-practices/); Dannaway | px, dom |
| 104 | Multiple primary buttons on one screen | If everything screams, nothing guides | Balsamiq; [Dannaway](https://www.adhamdannaway.com/blog/ui-design/button-design-tips) | dom |
| 105 | Primary and secondary CTAs styled identically | No hierarchy | 92learns | dom |
| 106 | Inconsistent button/link styling across pages | Confusion | MockFlow #12 | dom |
| 107 | Disabled buttons with no explanation / low contrast | "Blocked but don't know why" | Smashing [Disabled Buttons](https://www.smashingmagazine.com/2021/08/frustrating-design-patterns-disabled-buttons/) | dom |
| 108 | Active controls that look disabled | False unavailability | NN/g Low-Contrast | px, dom |
| 109 | Missing focus indicator (`outline:none`) | Keyboard users lost | [Access Guide](https://www.accessguide.io/guide/focus-indicator); Frontend Checklist | dom, code |
| 110 | Tap targets < 44×44 / < 27×27 inline | Error rate doubles at 30px | Smashing; [72Technologies](https://www.72technologies.com/blog/tap-targets-thumb-zones-mobile-ux) | dom |
| 111 | Targets closer than ~8–10px | Mis-taps | Smashing | dom |
| 112 | No system status feedback | Heuristic #1 | NN/g; MockFlow #17 | man, dom |
| 113 | Spinner forever / no skeleton | Uncertainty | NN/g Heuristic #1 | man |
| 114 | Inline validation that blocks valid edge cases | 100% abandonment when unfixable | Smashing Disabled Buttons | man |
| 115 | Frozen filters / no applied-filters overview | 32% of sites | Baymard; Smashing | dom |
| 116 | CAPTCHA as a routine gate | Frustrating | Smashing | dom |
| 117 | No "emergency exit" (undo/cancel/close) | Heuristic #3 | NN/g | dom |
| 118 | Fake dropdowns / custom controls breaking native behaviour | Violates conventions | NN/g; Smashing | dom |
| 119 | Bounce/elastic easing on every hover | AI tell | dev.to | dom, code |

## 8. Motion

| # | No-go | Why | Source | Detect |
|---|---|---|---|---|
| 120 | Auto-forwarding carousels | Item visible 20% of time; reads as ad | NN/g [Auto-Forwarding](https://www.nngroup.com/articles/auto-forwarding/) | dom, code |
| 121 | Carousels in general (esp. hero) | Frustrating | Smashing; NN/g | dom |
| 122 | Parallax / scroll-jacking | Motion sickness, ignored | NN/g [Parallax](https://www.nngroup.com/articles/parallax-usability/) | code, man |
| 123 | Animation without `prefers-reduced-motion` | Vestibular triggers (~35% of adults) | [Frontend Checklist](https://frontendchecklist.io/rules/accessibility/reduced-motion) | code |
| 124 | Autoplay video / animated backgrounds | Distraction, bandwidth | Thrive; NN/g | dom, code |
| 125 | Animated elements that look like ads | Banner blindness | NN/g | man |
| 126 | Jank / animations that cause layout shift | Dropped frames | 21st.dev; Thrive | code |
| 127 | Text that animates away before it can be read | Missed content | NN/g Parallax | man |
| 128 | Heavy plugins | — | Flanders | code |

## 9. Mobile-specific

| # | No-go | Why | Source | Detect |
|---|---|---|---|---|
| 129 | Missing/incorrect viewport meta | Rendered at desktop width | dev.to Mobile CSS; RapidDev | code |
| 130 | Fixed-width / non-responsive layout | 60% of traffic mobile | MockFlow #1; KlientBoost | dom, px |
| 131 | Text requiring zoom / unreadable at 320px | Unusable | Smashing | px, dom |
| 132 | Hover-only interactions | Touch has no hover | Smashing | dom, code |
| 133 | Fixed-position elements jumping on iOS Safari | Broken sticky bars | dev.to | man |
| 134 | Keyboard covering focused inputs | Can't see what you type | Baymard [Mobile Checkout](https://baymard.com/blog/mobile-checkout) | man |
| 135 | Wrong input keyboard types (no `inputmode`/`type`) | Slower entry | Baymard | code |
| 136 | Submit button hidden below fold, reason invisible | — | Smashing | px |

## 10. Modals, overlays & interruptions

| # | No-go | Why | Source | Detect |
|---|---|---|---|---|
| 137 | Modal for non-essential content (newsletter on arrival) | Strong user disdain | NN/g [Modal Dialogs](https://www.nngroup.com/articles/modal-nonmodal-dialog/) | dom |
| 138 | Modal interrupting a high-stakes flow | Pressures | NN/g | man |
| 139 | Modal requiring info outside the modal | Can't decide inside it | NN/g | man |
| 140 | Upsell modals without context | — | NN/g | man |
| 141 | Pop-ups / interstitials generally | Users resist | NN/g; Smashing | dom |
| 142 | Infinite scroll without a footer/escape | Unreachable footer | Smashing [Infinite Scroll](https://kerbco.com/designing-a-better-infinite-scroll-smashing-magazine/) | dom |
| 143 | Nagging (repeated prompts) | Deceptive | deceptive.design [Types](https://www.deceptive.design/types) | man |
| 144 | Forced account creation before use | 26% cart abandonment | NN/g; Baymard [Checkout](https://baymard.com/blog/current-state-of-checkout-ux) | dom, man |

## 11. Deceptive / dark patterns

*Brignull's 2025 type list, Mathur et al. taxonomy, FTC 2022 report, EDPB taxonomy, DSA Art. 25. Most need intent (man); the visual ones are flaggable.*

| # | No-go | Why | Source | Detect |
|---|---|---|---|---|
| 145 | Confirmshaming | Emotional manipulation | deceptive.design; Mathur; FTC | dom |
| 146 | Visual interference / asymmetric buttons (bright Accept, grey Reject) | Steers via style | deceptive.design; EDPB; [CookieYes](https://www.cookieyes.com/blog/dark-patterns-in-cookie-consent/) | dom, px |
| 147 | Hidden/buried reject or opt-out | EDPB finding | [UniConsent/noyb](https://www.uniconsent.com/blog/noby-guidelines-on-cookie-banner-dark-pattern-2024); FTC | dom |
| 148 | Pre-ticked boxes / preselection | Influences by default | deceptive.design; DSA Art. 25 | dom |
| 149 | Fake urgency (countdowns) | False beliefs | deceptive.design; FTC | dom |
| 150 | Fake scarcity | False beliefs | deceptive.design; Mathur | dom |
| 151 | Fake social proof | Misleads | deceptive.design; Mathur | dom |
| 152 | Disguised ads | Mistaken for content | deceptive.design; NN/g | man |
| 153 | Trick wording / double negatives | Confusing | deceptive.design; FTC | man |
| 154 | Hidden costs / subscription | Sneaking | deceptive.design; FTC | man |
| 155 | Sneak into basket | — | Mathur | man |
| 156 | Roach motel / hard to cancel | Obstruction | deceptive.design; FTC | man |
| 157 | Forced action / enrollment | — | deceptive.design; Mathur | man |
| 158 | Cookie walls | Access conditional on consent | EDPB | dom |
| 159 | Overloading (too many consent choices) | EDPB | [Securiti](https://securiti.ai/blog/edpb-guidelines-on-dark-patterns-in-social-media/) | dom |
| 160 | Comparison prevention | — | deceptive.design | man |
| 161 | Currency confusion | Obscures cost | deceptive.design | man |
| 162 | Addictive design (infinite feeds, autoplay next) | — | deceptive.design | man |
| 163 | Auto-renewal terms in tiny/low-contrast text | Concealment | FTC [Bringing Dark Patterns to Light](https://www.ftc.gov/reports/bringing-dark-patterns-light) | dom, px |
| 164 | Privacy-choice UIs steering to most-sharing option | FTC; EDPB | — | dom |
| 165 | Any interface that "deceives, manipulates or materially distorts" free decision | [DSA Art. 25](https://dsa-library.com/article/25/) | — | man |

## 12. "AI-generated UI" smells (2024–2026)

| # | No-go | Why | Source | Detect |
|---|---|---|---|---|
| 166 | Purple-to-blue/cyan hero gradient | The canonical tell | dev.to; [prg.sh](https://prg.sh/ramblings/Why-Your-AI-Keeps-Building-the-Same-Purple-Gradient-Website); 925studios | px, dom |
| 167 | Glassmorphism + neon glow everywhere | Most common pattern in training data | dev.to; [Medium AI Design Slop](https://mohitphogat.medium.com/ai-design-slop-why-every-ai-built-interface-looks-the-same-and-how-to-fix-it-bf874e0b470c) | dom |
| 168 | Centered hero + single CTA "floating in space" | Generic | dev.to; 925studios | dom, px |
| 169 | Row of 3 (or 6) identical rounded cards, icon + heading + 2 lines | "Hero + 3 features" cliché | 925studios; [SmoothUI](https://smoothui.dev/blog/ai-design-slop) | dom |
| 170 | Gradient "Get Started" button | Default CTA | 925studios | dom |
| 171 | Dark hero that "could belong to ten thousand products" | No identity | 925studios | man |
| 172 | Default shadcn grey / default Tailwind blue untouched | No decisions made | dev.to ×2 | dom |
| 173 | Perfectly even algorithmic spacing with no rhythm | No hierarchy decisions | 925studios | dom |
| 174 | Emoji as feature icons | Cheap, inconsistent | vibecodekit; SmoothUI | dom |
| 175 | "Bento box" grids as default | Cliché | vibecodekit | man |
| 176 | Incoherence across axes (radius, shadow, accent, spacing, icons, type, motion each vary) | "It's not ugly components, it's incoherence" | dev.to "look off" | dom |
| 177 | Gradient text on big stat numbers | Effect for effect's sake | dev.to | dom |

## 13. Landing / marketing pages

| # | No-go | Why | Source | Detect |
|---|---|---|---|---|
| 178 | Full navigation menu on a landing page | Exit ramps | CXL [High-Converting LP](https://cxl.com/blog/how-to-build-a-high-converting-landing-page/); KlientBoost | dom |
| 179 | Multiple competing CTAs | Up to −266% | KlientBoost; CXL | dom |
| 180 | Weak/unclear headline | Lost in 5 seconds | KlientBoost; Thrive | man |
| 181 | Message mismatch between ad and page | Scent breaks | CXL | man |
| 182 | No trust signals near CTA | — | Thrive [10 LP Mistakes](https://thriveagency.com/news/10-landing-page-mistakes-that-kill-conversions-and-how-to-fix-them/) | man |
| 183 | Slow load / poor mobile | Abandonment | KlientBoost | code |
| 184 | Unclear field labels / missing checkout messaging (92% of sites) | Form errors | Baymard [Holistic Checkout](https://baymard.com/blog/holistic-view-on-checkout-usability) | dom |
| 185 | No clear primary button in checkout; asking the same info twice | Baymard | — | dom, man |
| 186 | Shipping cost revealed only at review | Hidden costs | Baymard; deceptive.design | man |
| 187 | Product pages that don't let users assess fit (90% of apparel) | Baymard benchmark | [StyleImprint](https://www.styleimprint.app/blog/baymard-90-fashion-product-page-mistakes) | man |

## 14. Data visualisation

| # | No-go | Why | Source | Detect |
|---|---|---|---|---|
| 188 | 3D pies/bars | Foreground slices look bigger | [Querio](https://querio.ai/blogs/bad-data-visualization-examples); Eval Academy | px |
| 189 | Chartjunk | Every pixel should carry data | [Useful Data Tips](https://usefuldatatips.com/tips/visualization/avoiding-chartjunk) | px |
| 190 | Truncated Y-axis on bars | Exaggerates differences | Querio; ChartGen | px, man |
| 191 | Dual-axis with mismatched scales | False correlation | Querio | man |
| 192 | Pie with too many slices | Unreadable | Eleken | px |
| 193 | Rainbow colormaps for ordered data | No perceptual order | Datavizkit | px |
| 194 | Missing axis labels/units/legend | Uninterpretable | 5of10 | px, man |

## Master list — ranked by how many sources cite the no-go

| Rank | No-go | Sources (n) | Detect |
|---|---|---|---|
| 1 | Low-contrast text (incl. placeholders, disabled, fine print) | 9 | px, dom |
| 2 | Visual interference / asymmetric choice styling, preselection | 7 | dom, px |
| 3 | Weak affordance: links/buttons indistinguishable; inconsistent button styles | 7 | px, dom |
| 4 | Clutter / information overload / no white space | 6 | px, dom |
| 5 | Fake urgency / scarcity / social proof | 6 | dom |
| 6 | Purple/indigo gradient + glassmorphism + Inter "AI slop" look | 8 (one cluster) | px, dom |
| 7 | Missing / inconsistent visual hierarchy | 5 | px, dom |
| 8 | Too many colours / rainbow / clashing palette | 5 | px |
| 9 | Tiny tap targets / targets too close | 5 | dom |
| 10 | Carousels / auto-forwarding | 4 | dom, code |
| 11 | Hidden navigation, mystery meat, unlabeled icons | 5 | dom, px |
| 12 | Inconsistent spacing / misalignment / off-grid | 5 | dom, px |
| 13 | Pure #000 on #FFF | 3 | dom |
| 14 | Hard to cancel / roach motel / forced enrollment | 4 | man |
| 15 | Forced account creation | 4 | dom |
| 16 | Modals for non-essential content | 3 | dom |
| 17 | Parallax / scroll-jacking / no reduced-motion | 5 | code |
| 18 | Non-responsive / fixed-width / missing viewport | 4 | code, dom |
| 19 | Walls of text / no chunking | 4 | dom, px |
| 20 | Illusion of completeness / false floor | 5 | px |
| 21 | Identical 3-card feature grids / generic hero | 4 | dom |
| 22 | Too many typefaces / centered body / rivers / widows | 5 | dom, px |
| 23 | Multiple primary CTAs | 5 | dom |
| 24 | Disabled buttons without explanation | 2 | dom |
| 25 | Inconsistent radius / shadows / light direction | 5 | dom |
| 26 | Stretched / pixelated images, low-res logos | 5 | px |
| 27 | Colour as only signal | 2 | dom |
| 28 | Confirmshaming | 3 | dom |
| 29 | Truncated axes / 3D charts / chartjunk | 5 | px |
| 30 | Unchanged visited links; new windows; PDFs; ad-like design | 1 (canonical) | dom |
| 31 | Layout shift / overlapping / horizontal overflow | 4 | dom, code |
| 32 | Missing focus indicator | 3 | dom |
| 33 | Hover-only interactions on touch | 2 | code |
| 34 | Saturated large areas / bright surfaces in dark mode | 1 | px |
| 35 | Emoji as icons; mixed icon styles | 3 | dom, px |

## What this means for `beautiful`

- **Highest-ROI pixel checks**: contrast on text regions, tiny text height, edge-touching content, horizontal overflow, "everything centered", three identical cards, purple-gradient hue signature, clipped/overlapping boxes, image aspect mismatch, hero filling > 90 % of the first viewport with nothing peeking.
- **Highest-ROI DOM checks**: `outline: none` without replacement, viewport meta, tap-target size/gap, more than one primary button per view, count of distinct font families / radii / shadow definitions (an incoherence score), `autoplay`, no `prefers-reduced-motion`, placeholder-only labels, disabled buttons with no adjacent hint, pre-checked consent boxes, countdown-timer text, lorem-ipsum regex.
- **Manual only**: deceptive-pattern intent, IA and label quality, copy quality, data-viz truthfulness.

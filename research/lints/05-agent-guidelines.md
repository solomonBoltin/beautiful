# Guideline sets, checklists and skills written for AI coding agents (2024–2026) — inventory

*Part of the [design-lint survey](../DESIGN-LINTS.md). Tags: **px** = screenshot only, **dom** =
rendered DOM / computed CSS, **code** = static source, **man** = human/LLM judgement.*

## Part A — Rule sets built for agents

### A1. Vercel Labs — Web Interface Guidelines
https://github.com/vercel-labs/web-interface-guidelines (MIT). Three files: `README.md` (130 bold-lead bullets, 7 sections), `AGENTS.md` (107 rules with **MUST / SHOULD / NEVER**), `command.md` (103-rule review prompt that outputs `file:line` findings, terse, ending with an "Anti-patterns (Flag These)" list). Installed as a skill (`npx skills add vercel-labs/agent-skills --skill web-design-guidelines`).

Condensed rules: full keyboard support, visible unobscured `:focus-visible` rings, never `outline: none` without replacement (dom/code); hit target ≥ 24 px (mobile ≥ 44), mobile inputs ≥ 16 px, never `user-scalable=no`, `touch-action: manipulation` (dom/code); forms: never block paste, loading buttons keep their label, inline errors + focus the first, `autocomplete`/`inputmode`, placeholders end with `…`, warn on unsaved changes (dom/code/man); URL reflects state, links are `<a>`, never `<div onClick>` navigation (code); optimistic UI with undo, confirm destructive, `aria-live` (dom/man); animation: honour reduced motion, animate only `transform`/`opacity`, never `transition: all`, autoplay > 5 s needs pause (code/dom); layout: optical alignment ± 1 px, `env(safe-area-inset-*)`, no unwanted scrollbars (px/code/dom); content: `…` not `...`, curly quotes, `text-wrap: balance`, `tabular-nums`, nbsp in `10 MB` / `⌘ K`, icons have labels, accessible names, skip link, h1–h6 (code/dom); truncate/line-clamp/`min-w-0` (code); explicit image dimensions, `font-display: swap`, virtualise > 50 items (code); dark mode: `color-scheme`, `theme-color`, native `<select>` colours (code); design: layered shadows, concentric nested radii, hue-consistent borders/shadows, contrast increases on hover/active/focus, prefer APCA (dom).

### A2. Anthropic — `frontend-design` skill
https://github.com/anthropics/skills/blob/main/skills/frontend-design/SKILL.md. Persona prose + a two-pass process (token plan → genericness review → build → screenshot self-critique). Rules: ground aesthetics in the subject; one or two distinct typefaces, line length < 80 ch; avoid accenting one word in a headline, ALL-CAPS labels, unnecessary labels; structural devices (numbering, eyebrows, dividers) must carry information; one orchestrated motion moment, not fade-and-slide on every section; the **five default clusters to avoid**: cream + serif + terracotta; near-black + acid accent; broadsheet hairlines; the SaaS-card kit (identical rounded cards, one radius, `rgba(0,0,0,.1)` shadow, gradient washes); template chrome (tracked eyebrows, `A · B · C` meta, `→` on links). Quality floor: responsive, visible focus, reduced motion, harmonious palette (dom).

### A3. Anthropic — Cookbook "Prompting for frontend aesthetics"
https://platform.claude.com/cookbook/coding-prompting-for-frontend-aesthetics. Avoid Inter/Roboto/Arial/system and repetitive picks (Space Grotesk); pair a distinctive display with a refined body; dominant colour + sharp accents via CSS variables; no purple gradients on white; animation for high-impact moments; backgrounds with atmosphere; name the defaults to avoid explicitly.

### A4. Impeccable (Paul Bakaus)
https://github.com/pbakaus/impeccable · https://impeccable.style (Apache-2.0). SKILL.md + 24 verb commands + a **Rust deterministic detector** (`npx impeccable detect [dir|html|url] --json`, 61 rules, exit 0/2, inline waivers, rule packs, post-edit hook) + `PRODUCT.md` / `DESIGN.md` context. Craft floor: text ≥ 4.5:1 / large 3:1, secondary text on colour tinted from the hue never grey, shadows with offset + blur, tight-in/generous-between spacing, measure 65–75 ch, display ≤ 6 rem, tracking ≥ −0.04 em, one motion moment, states hover/disabled/loading/error/empty, themed selection/caret/scrollbar/focus. Refuse list (defaults, not bans): identical icon+heading+text cards as structure, nested cards, hero-metric template, **eyebrow above heading (hard ban)**, section numbers without sequence, gradient text, glass as decoration, `border-left` stripes, hard offset shadows, monospace costume, emoji icons. Detector ids: `overused-font`, `gradient-text`, `gray-on-color`, `side-tab`, `bounce-easing`, `dark-glow`, `radial-halo`, `layout-transition`, `transition-property`, `monotonous-spacing`, `em-dash-overuse`, `marketing-buzzword`, `ai-color-palette`, `broken-image`, `text-shadow`, `design-system-{color,font,font-size,radius}` drift vs DESIGN.md, `focus-visible`, `google-font`. Audit: 5 dimensions × 0–4 → /20, P0–P3.

### A5. Hallmark (Nutlope / Together AI)
https://github.com/Nutlope/hallmark (MIT). SKILL.md + 20 references; **58 yes/no gates** all of which must be "no", plus a 6-axis self-critique (Philosophy, Hierarchy, Execution, Specificity, Restraint, Variety, 1–5; < 3 forces revision); enforces structural variety with a macrostructure stamp. Gates include: Inter/Roboto/Open Sans/Poppins/Lato/system as display; purple→blue or cyan→magenta gradients; 3-equal-column icon-above-heading grid; nested cards; side stripes; centred `100vh` hero; pure `#000`/`#fff`; `transition: all`; uniform `hover:scale-105`; bounce easing; animating layout properties; fading focus rings; auto-rotate without pause; Jane Doe / Acme / Nexus; zero-chroma neutrals (min 0.005); **accent > ~5 % of viewport**; spacing off the 4 px scale; prose `max-width` outside 45–75 ch; interactive elements lacking `:focus-visible`/`:active`/`:disabled`; transforms without reduced-motion fallback; mixed icon libraries or emoji icons; horizontal scroll anywhere 320–1920; > 3 font families; contrast vs *computed* background (body 4.5:1 / APCA Lc ≥ 60); the AI nav fingerprint (wordmark-left, 4–5 links, button-right, hairline) and footer fingerprint; hero padding-bottom < 1.3× top; invented metrics; fake browser chrome; values outside `:root` tokens; clickable text wrapping; two `sticky; top: 0`. Typography: display + body pairing mandatory, weight extremes, ratio scales, display lh 1.05–1.2 / body 1.5–1.65, banned default families (Inter … Montserrat … Georgia-default …). Colour: OKLCH, one accent ≤ 3 %, dark paper L 12–18 %, ink L 92–96 %. Copy: specific verbs, errors what/why/how, loading copy tiers; microcopy bans.

### A6. taste-skill (Leonxlnx)
https://github.com/Leonxlnx/taste-skill. 1,206-line SKILL.md, dials `DESIGN_VARIANCE / MOTION_INTENSITY / VISUAL_DENSITY`, "Pre-Flight Fail" / "BANNED as default" / "Override:" clauses. Rules: one icon family with global stroke; emoji discouraged; `100dvh` never `h-screen`; Inter discouraged, serif very discouraged as default, Fraunces/Instrument Serif banned as defaults; max 1 accent, saturation < 80 %; the "Lila rule" (no purple/blue glow default); one palette, no warm/cool grey mixing; the premium-consumer palette ban (cream/brass/espresso hexes); anti-centre bias when variance > 4; shape consistency lock; CTA on one line ≤ 3 words; no duplicate CTA intent; label above input; hero fits the fold (headline ≤ 2 lines, subtext ≤ 20 words, ≤ 4 text elements, no trust strip in hero); nav ≤ 80 px; each layout family at most once per page; **eyebrows ≤ 1 per 3 sections**; em dash banned in copy.

### A7. UI/UX Pro Max (nextlevelbuilder)
https://github.com/nextlevelbuilder/ui-ux-pro-max-skill. SKILL.md + Python search over CSVs (79 styles, 192 palettes, 74 font pairs, **119 UX guidelines** as Do/Don't rows with severity, 192 reasoning rules) + `pro-rules.md` pre-delivery checklist: no emoji icons; `cursor-pointer` on clickables; 4.5:1; focus visible; reduced motion; responsive at **375 / 768 / 1024 / 1440**; one icon family, stroke 1.5/2 px, 24 pt; touch ≥ 44 pt iOS / 48 dp Android; tap feedback 80–150 ms; 4/8 dp rhythm; safe areas; dark-mode contrast tested independently. Critical anti-patterns: removed focus rings, icon-only buttons without labels, hover-only, 0 ms transitions, fixed-pixel containers, body < 12 px, grey on grey, animating width/height, placeholder-only labels.

### A8. ux-skill (Laith Aljunaidy) — a deterministic anti-slop linter
https://github.com/Laith0003/ux-skill · `pip install uxskill` (MIT; MCP server with 18 tools; `/ux-lint` and `/ux-evolve` loops until score ≥ 90). `data/anti-patterns.json`: **152 regex rules** `{id, category, severity, name, why, fix, detection:{type, pattern, scope}}`, scored 0–100 with a gate at 65; categories A11y 41, Content 33, Layout 15, Typography 14, Visual 13, Quality 12, Motion 10, Color 9, Performance 5. All **code**. Representative ids: inter-as-display, purple-to-blue-gradient, three-equal-card-grid, fake-name-john-doe, lorem-ipsum-leak, emoji-in-ui, centered-everything-hero, gradient-text-rainbow, card-glow-purple-shadow, timing-300ms-default, pill-rounded-full-everywhere, blur-bg-only-decoration, testimonial-fake-five-stars, nav-equal-hamburger-desktop, heading-skip-h1-h3, arbitrary-z-index-9999, viewport-no-zoom, outline-none-no-focus-visible, placeholder-as-label, div-onclick-no-role, h-screen-no-dvh-fallback, filler-marketing-verbs, generic-cta-text, round-number-stats, animating-layout-properties, img-no-dimensions, box-shadow-multilayer-default, glass-morphism-default, transition-property-all, animation-duration-too-long, cta-buttons-clustered-in-hero, target-blank-no-noopener, autoplay-without-muted, marquee-tag, tabindex-positive, text-align-justify-web, full-viewport-width-overflow. Its blog names "accent saturation > 80 %" and "Inter ≥ 40 px" as tells.

### A9. Checklist Design skill
https://github.com/Checklist-Design/skills (MIT) — **129 checklists** from checklist.design bundled offline; `audit` mode (🟢 present / 🟡 partial / 🔴 missing / ⚪ not needed / ❔ can't tell, every row with a "Why") and `critique` mode. Explicitly separates "what's on the page" (answerable from source) from "how it looks" (needs a screenshot). Families: design-system components (32), flows (13), mobile (25 screens), web app (30), website (landing, 404, pricing, …). Sample items: modular type scale 1.25/1.333/1.5; explicit line-height per style (1.5 body / 1.2 heading / 1.1 display); interactive-state colours; 4.5:1 and 3:1 verified pairs; parallel dark-mode tokens; landing page: one headline for a skeptic, one primary CTA, social proof below the fold.

### A10. refactoring-ui-skill (s0xDk)
https://github.com/s0xDk/refactoring-ui-skill — Refactoring UI as numeric rules: spacing scale `4 8 12 16 24 32 48 64 96 …` (adjacent steps ≥ 25 % apart); type scale `12 14 16 18 20 24 30 36 48 60 72`, px/rem never em; two weights; 8–10 greys, 5–10 shades named 100–900 in HSL; five elevation shadows; large text = 24 px regular / 18.66 px bold; 3:1 functional borders; dark mode never pure black, elevation by lightness.

### A11. make-interfaces-feel-better (Jakub Krehel)
https://github.com/jakubkrehel/make-interfaces-feel-better — 19 principles with review output (HIGH/MEDIUM/LOW, `path:line`, Block / Needs changes / Approve): concentric radius (outer = inner + padding); optical alignment; shadows for elevation, borders for structure (3-layer light shadow); interruptible animations; stagger enter animations (800 ms, 100 ms section stagger); `-webkit-font-smoothing`; tabular numbers; `text-wrap: balance/pretty`; 1 px inset image outlines; scale on press; skip animation on load; never `transition: all`; minimum hit area; icon stroke matched to text weight.

### A12–A13. claude-frontend-kit; addyosmani web-quality-skills
https://github.com/ChlupacTheBosmer/claude-frontend-kit — verification gates (`axe-run`, `viewport-shots`, `check-overflow`, `check-images`, `check-dashes`, `detect`) and a `design-review` agent: live browser at 1440×900 → states → responsive 1440/768/375 (targets, no horizontal scroll, no overlap) → polish → WCAG AA → robustness → tokens → console; triage Blocker/High/Medium/Nit, "problems over prescriptions", screenshot every finding. https://github.com/addyosmani/web-quality-skills — evidence-led a11y (Lighthouse → a11y tree → fix → re-run); critical: missing labels, alt, contrast, keyboard traps, no focus indicators.

### A14. DESIGN.md — Google Stitch's open standard
https://github.com/google-labs-code/design.md (spec + CLI linter); collections https://github.com/VoltAgent/awesome-design-md (73 brands), ux-skill (160), designmd.co. YAML front matter of typed tokens (`colors`, `typography`, `rounded`, `spacing`, `components`) + Markdown body in fixed order ending with **Do's and Don'ts**. Consumed by Stitch, Claude Code, Cursor, Gemini CLI, Codex; impeccable lints drift against it. A project's DESIGN.md is a machine-readable oracle for token conformance.

### A15. Cursor / Windsurf / Copilot rule files
awesome-cursorrules (257 files) and cursor.directory are overwhelmingly stack rules; a grep across all 257 returns ~15 UI-quality lines ("mobile-first responsive", "Shadcn/Radix", "ARIA where necessary", "sufficient contrast", "feedback for actions"). **Cursor/Windsurf collections contain almost no visual-quality rules**; they delegate to component libraries. Containers: `.windsurf/rules/*.md`, `.github/copilot-instructions.md`, `AGENTS.md` (builder.io: imperative lowercase one-liners under Do/Don't).

### A16. Product builders (Lovable, Figma Make, v0, Magic Patterns, Stitch)
Lovable `.lovable/design-system.json` + rules files (adherence prompts, not blocking); Figma Make `Guidelines.md` as a system prompt ("more context isn't always better"); v0 brief template with concrete constraints ("light theme, high contrast", "max 3-column"); Magic Patterns design-system import. Shared "centroid" named by several analyses: violet/indigo primary, Inter, rounded cards, marketing spacing.

### A17. Review checklists for AI-generated UI (2025–2026)
21st.dev checklist (text in HTML before JS; real links; Tab through; the states nobody generates; reduced motion; dragged-in deps; hard-coded values); UIZZE checklist (domain-specific labels, read without colour, narrow width keeps identity, compare to an existing route at the same viewport, "do not substitute a numeric aesthetic score for evidence"); a mobile QC checklist (320/375/390/414/768; modal scroll-lock; safe areas; ≥ 44 pt; longest text at 320).

### A18–A19. Surveys and the consolidated "AI slop" tells
Rankings (ruoqijin, wilwaldon toolkit, trilogyai, getclaudeskills) agree on the shared enemy. Tells by source count: purple/indigo→blue/cyan gradient (14 sources, traced to Tailwind indigo-500); Inter/Roboto/system as display (11); three identical icon-above-heading cards (10); glassmorphism with neon glow (9); gradient text (6); bounce easing / uniform `hover:scale` (6); nested cards (4); uniform radius/padding (5); centred `100vh` hero (5); emoji icons (5); generic copy, fake stats, Jane Doe, $9/$29/$99, five stars (5); dark hero, pure #000/#fff (4); eyebrows, 01/02/03, `→` on buttons, single italic word (4); aurora blobs and noise overlays (3); animate-on-scroll everywhere (3); default shadcn tokens (2); cream + brass + espresso "premium" palette (2). Bento is listed as a *choice*, not a tell. Sources: https://www.925studios.co/blog/ai-slop-design-tells, https://www.mania.design/blog/spot-the-slop-a-ui-designers-guide-to-fixing-ai-defaults/, https://dev.to/james_anderson_h/the-purple-gradient-problem-why-ai-ui-all-looks-alike-and-how-to-fix-it-3j65, https://smoothui.dev/blog/ai-design-slop, https://prg.sh/ramblings/Why-Your-AI-Keeps-Building-the-Same-Purple-Gradient-Website, https://alexlavaee.me/blog/lessons-learned-designing-with-ai/, https://uxskill.laithjunaidy.com/blog/why-ai-uses-purple-gradients.html, https://trilogyai.substack.com/p/fixing-visual-ai-slop.

## Part B — Classic practitioner rule sets these draw on

- **B1. Refactoring UI** (Wathan & Schoger): systematise everything (spacing/type/colour/shadow scales); hierarchy via weight and colour, not size; ≤ 3 text colours; labels last; start with too much white space; more space around a group than within; hand-picked type scale; line length 45–75 ch; baseline alignment; don't centre > 2–3 lines; HSL, 8–10 greys, 5–10 shades; tinted greys; never colour alone; **never grey text on coloured backgrounds**; light from above; five elevation shadows; two-part shadows; everything has an intended size; empty states; fewer borders.
- **B2. Anthony Hobday — 28 safe rules** (https://anthonyhobday.com/sideprojects/saferules/): near-black/near-white; saturated neutrals (warm or cool, not both); distinct palette brightness; optical alignment; container border contrasts with both; measurements on a scale; 12 columns; closer elements lighter; shadow blur = 2× distance; container brightness ≥ 12 % diff dark / 7 % light; outer padding ≥ inner; body ≥ 16 px; line length ≈ 70 ch; button horizontal padding = 2× vertical; ≤ 2 typefaces; nested corners inner = outer − gap; no shadows in dark UI; lower contrast on icons paired with text.
- **B3. Laws of UX** (Yablonski, 30 laws): Doherty < 400 ms; Fitts; Hick; Jakob; proximity; similarity; Miller (7 ± 2 — a memory law, see [04-evidence.md](04-evidence.md)); serial position; Von Restorff (one distinct primary CTA).
- **B4. Growth.Design** — 106 biases; the design-detectable subset overlaps B3.
- **B5. Erik Kennedy — 7 rules**: light from the sky; black and white first; double your white space; text-on-image methods (overlay ~35 %, floor fade, scrim); make text pop and un-pop; good fonts.
- **B6. Practical UI** (Dannaway): space groups; consistency; hierarchy; colour purposefully (interactive only); 3:1 components / 4.5:1 text; single sans; taller x-height; limit uppercase; regular + bold only; no pure black; left-align; body lh ≥ 1.5.
- **B7–B8.** checklist.design (bundled in A9); ux-checklist.com (process phases, man).
- **B9. A11Y Project checklist** (WCAG-mapped): `lang`, unique title, zoom not disabled, landmarks, no autofocus; visible focus in layout order; alt on all images; one h1, no skipped levels; real lists; `<a>` for links, recognisable; labels, fieldsets, associated errors; no autoplay; contrast incl. icons, input borders, text over images, `::selection`; rotation; no horizontal scroll; target size.
- **B10. Front-End Checklist** (385 rules, Critical→Low, "for humans and AI agents"): viewport meta, readable mobile sizes, no horizontal scroll, don't disable zoom, visible focus, `prefers-color-scheme`, transform/opacity animations, tokens as custom properties, CLS, lazy-load offscreen, loading indicators, virtualise long lists, page weight < 1500 KB, load < 3 s.
- **B11. Design System Checklist** (Karacizmeli): coverage map of foundations and 30 components.
- **B12. Team design-QA checklists**: OverlayQA (margins match spec, grid alignment, no overflow 320–1920, type scale, tokens incl. hover/focus, all states, WCAG AA); breakpoints 320/375/390/414/768/1024/1280/1440/1920, ± 1 px around them; dark-mode checklist (no flash of wrong theme, contrast in both themes, dividers visible, focus rings on dark); loading/empty/error (spinner only when nothing to show, show-delay 150–300 ms + min visible 300–500 ms, skeletons mirror layout); landing page (one value proposition, one primary CTA, 5-second test).

## Part C — Deduplicated master list, ranked by how many sources include the rule

| # | Rule | Sources | Tag |
|---|---|---|---|
| 1 | Text ≥ 4.5:1 (large 3:1); components/borders/focus rings ≥ 3:1; verify in both themes | 15 | dom |
| 2 | Visible focus on every interactive element; never `outline: none` without `:focus-visible`; sticky UI never covers focus | 14 | dom/code |
| 3 | No purple/indigo→blue/cyan/pink gradient (hero, CTA, mesh, text) | 14 | code/px |
| 4 | Design loading / empty / error / disabled / success states | 13 | man/dom |
| 5 | Honour `prefers-reduced-motion` with an intentional alternative | 12 | code |
| 6 | No Inter/Roboto/Arial/system as display; pair distinctive display + refined body | 11 | code |
| 7 | Never colour alone for state/meaning | 10 | dom |
| 8 | No three/six identical icon-above-heading cards as structure | 10 | code/px |
| 9 | Visible labels; placeholder is never the label; inline errors tied to the field | 9 | dom/code |
| 10 | Glass/backdrop-blur/glow only as purposeful depth | 9 | code |
| 11 | No horizontal scroll at any viewport 320–1920 | 9 | dom |
| 12 | Hit target ≥ 44 (mobile) / ≥ 24 (web) | 9 | dom |
| 13 | Semantic elements: `<button>`, `<a href>`; no `div onClick` | 8 | code/dom |
| 14 | Real copy: no lorem/Jane Doe/Acme, no buzzwords, no invented stats or $9/$29/$99 tiers | 8 | code |
| 15 | Line length 45–75 ch (< 80 max) | 8 | dom |
| 16 | Animate only `transform`/`opacity` | 8 | code |
| 17 | Consistent 4/8 spacing scale; tight within, generous between | 8 | dom/px |
| 18 | One icon library, one stroke, never emoji as icons | 8 | code/dom |
| 19 | Tinted neutrals; no pure #000/#fff; warm or cool, not both | 7 | code/dom |
| 20 | Explicit image dimensions; `fetchpriority` / lazy correctly | 7 | code |
| 21 | Heading hierarchy, landmarks, skip link, `lang`, unique title | 7 | dom |
| 22 | Icon-only buttons need `aria-label`; decorative images hidden; meaningful ones have alt | 7 | dom |
| 23 | Consistent radius; concentric nested radii | 7 | dom |
| 24 | Exactly one primary CTA per view; hierarchy via weight/colour | 7 | px/man |
| 25 | No gradient text | 6 | code |
| 26 | No bounce easing / uniform `hover:scale` | 6 | code |
| 27 | Never `transition: all` | 6 | code |
| 28 | No eyebrow above every heading; no 01/02/03 without a sequence; no single italic word | 6 | dom/px |
| 29 | Body ≥ 16 px (inputs ≥ 16 on mobile); nothing meaningful < 12 px; body lh 1.5–1.75, display 1.05–1.2 | 6 | dom |
| 30 | ≤ 2 typefaces; ≤ 2 weights per screen | 6 | dom |
| 31 | Autoplay > 5 s needs pause; carousels pause on hover/focus | 6 | dom/code |
| 32 | No nested cards; fewer borders | 5 | dom |
| 33 | Never disable zoom | 5 | code |
| 34 | Never grey text on coloured backgrounds | 5 | dom |
| 35 | Skeletons mirror layout; show-delay 150–300 ms, min visible 300–500 ms | 5 | dom |
| 36 | Centred `100vh` hero is a default, not a choice; hero fits the fold | 5 | px |
| 37 | Coloured side-stripe cards are a tell | 5 | code |
| 38 | Hover-only affordances need focus + tap equivalents | 5 | dom |
| 39 | `tabular-nums` for number columns | 5 | code |
| 40 | Optical alignment ± 1 px; everything aligned to something | 5 | px/dom |
| 41 | Layered shadows with offset + blur (blur ≈ 2× distance), tinted; none in dark UI | 5 | dom |
| 42 | One orchestrated motion moment; interruptible | 5 | dom |
| 43 | Tokens only (DESIGN.md / `:root`); lint drift | 5 | code |
| 44 | Confirm destructive or offer undo | 5 | dom/man |
| 45 | `…`, curly quotes, nbsp before units, `text-wrap: balance` | 5 | code |
| 46 | Clickable text on one line; nav ≤ 80 px | 4 | dom |
| 47 | Accent ≤ ~5 % of viewport; saturation < 80 %; one accent | 4 | px |
| 48 | Dark mode: `color-scheme`, `theme-color`, parallel tokens, lighter elevation | 4 | code/dom |
| 49 | `100dvh`; safe-area insets; `overscroll-behavior: contain` | 4 | code |
| 50 | Long-content resilience; test the longest strings at 320 px | 4 | code/dom |
| 51 | URL reflects state; Back restores scroll | 3 | code |
| 52 | Limit uppercase; +0.05 em tracking when used | 3 | code |
| 53 | Don't scale icons/screenshots beyond intended size | 3 | px |
| 54 | Virtualise > 50 items | 3 | code |
| 55 | Tooltip timing 800–1000 ms first, 0 ms on focus; never required info in tooltips | 3 | code |
| 56 | Section-layout variety; no template nav/footer fingerprint | 3 | px/man |
| 57 | ≤ 5–7 nav items; ≤ 4 options at a decision point | 3 | dom |
| 58 | Verify at 375 / 768 / 1024 / 1440 (+ 320, 1920) | 3 | px |

## Part D — How agent-facing sources phrase rules

1. **Imperative one-liners**, optional bold lead-in ("**Never `transition: all`.** Explicitly list…").
2. **Modal prefixes** `MUST / SHOULD / NEVER` (Vercel) or **Do / Don't pairs** (UI/UX Pro Max, DESIGN.md, builder.io).
3. **A recurring category taxonomy**: Accessibility · Focus · Forms · Motion · Typography · Colour · Layout/Spacing · Content/Copy · Images · Performance · Navigation/State · Touch · Dark mode · i18n · Anti-patterns.
4. **Explicit severity**: ux-skill `critical/high/medium/low`; impeccable `P0–P3` + 0–4 dimension scores; make-interfaces `HIGH/MEDIUM/LOW` → Block/Needs changes/Approve; Front-End Checklist Critical→Low.
5. **Yes/no gates** where every answer must be "no" (Hallmark's 58) and "BANNED as default" + "Override:" clauses (taste) — bans are framed as *defaults to refuse unless the brief earns them*.
6. **Machine-readable rule records**: `{id, category, severity, name, why, fix, detection}` (ux-skill); `{id, category, scopes, severity, description}` with inline waivers (impeccable).
7. **Reviewer output**: `file:line` findings grouped by file, terse (Vercel); status-marker tables with a "Why" (Checklist Design); "problems over prescriptions", screenshot each visual finding (design-review agent).
8. **Numbers where possible**: 44/24 px targets, 4.5/3:1, 45–75 ch, ≤ 5 % accent area, < 80 % saturation, ≤ 3 families, ≤ 1 eyebrow per 3 sections, 150–300 ms show-delay, 800 ms tooltip, 0.005 min chroma, ≥ 25 % spacing steps.

**Gap for `beautiful`:** none of these tools scores from screenshots; ux-skill, impeccable, Hallmark and taste are regex/source-driven, and the LLM-judged ones say screenshots are needed for "how it looks". The **px**-tagged rules above (white-space ratios, alignment, accent-area %, card-grid uniformity, hero composition, nav/footer fingerprints, shadow halo vs offset, contrast on *computed* backgrounds) are exactly where a screenshot- and DOM-aware scorer adds rather than duplicates; and a project's DESIGN.md is a per-project oracle for token drift.

---
name: beautiful
description: Score any screenshot, logo or artwork 1–100 for beauty and get concrete hints on what to fix. Use after ANY change that renders something (a page, a component, a dialog, a chart, a logo) and before declaring UI work done. Trigger words - UI, UX, layout, design, CSS, screenshot, "looks off", "make it prettier", "polish".
---

# beautiful — see what you ship

You cannot look at a page. `beautiful` can measure one. Use it as your eyes for form:
composition, alignment, white space, colour harmony and contrast, all from pixels.

## Install (once)

```bash
python -m pip install git+https://github.com/solomonBoltin/beautiful
```

## The loop

1. **Render** the thing you changed to a PNG at the size a user sees it (a 1280×800 viewport
   for pages; the natural size for a logo). Use whatever screenshot tool the project has
   (Playwright, Puppeteer, the browser tool, `demo/screenshot_url.js` in the repo).
2. **Score** it:
   ```bash
   beautiful --mode=ui shot.png        # ui | art | logo
   ```
   You get the number, every factor in 0–1, and hints ordered by how much each one costs.
3. **Read the hints, not just the number.** Each hint names the weakest factor and the edit
   that raises it. Typical: "composition: centre the main block", "alignment: snap element
   edges to a shared grid", "whitespace: adjust padding so ~60% of the canvas is background".
4. **Make one edit** that addresses the top hint. Re-render. Re-score.
5. **Stop** when the score stops moving, or at the target the task set. Report the
   before/after numbers and the factor that moved.

Score the viewport, not a full-page capture of a very tall page. Score each state that
matters (empty state, dialog open, mobile width) separately.

## Reading the scale

| score | means |
|---:|---|
| 85+ | composed, aligned, calm — production quality |
| 70–84 | fine; one factor is dragging it (read the hint) |
| 50–69 | something structural is off — usually composition or white space |
| < 50 | unstyled, lopsided, or cluttered |

## Do not

- Chase the number with tricks (centring a wreck still scores as centred; the function
  measures form, not intent). Fix the cause the hint names.
- Trade legibility for symmetry. Text is texture to this metric; keep type readable.
- Treat one point as signal. Differences under ~3 points are noise; a factor moving by 0.2 is not.

## As a gate

```bash
beautiful --mode=ui shot.png --min 70   # exit 1 below 70 — usable in CI or a pre-commit hook
```

---
name: beautiful
description: Measure the beauty of any screenshot, logo or artwork as a number 1–100 with a factor breakdown (composition, alignment, white space, colour harmony, contrast, complexity) and concrete hints. Use after ANY change that renders something and before declaring UI work done. Trigger words - UI, UX, layout, design, CSS, screenshot, "looks off", "make it prettier", "polish".
---

# beautiful — measure, don't guess

Looking at a page tells you *that* something is off. `beautiful` tells you *what*, as a number
you can move: composition, alignment, white space, colour harmony, contrast, complexity — each
an explicit formula from the aesthetics literature, computed from pixels.

## Install (once)

```bash
python -m pip install beautiful-score          # or: pip install git+https://github.com/solomonBoltin/beautiful
```

Or as an MCP tool, so you can call `beauty_score` / `beauty_compare` directly:

```bash
claude mcp add beautiful -- beautiful-mcp
```

## The loop

1. **Render** the thing you changed to a PNG at the size a user sees it (a 1280×800 viewport
   for pages; the natural size for a logo). Use the project's screenshot tool (Playwright,
   Puppeteer, the browser tool, `demo/screenshot_url.js` in the repo).
2. **Score** it:
   ```bash
   beautiful --mode=ui shot.png        # ui | art | logo
   ```
   You get the number, every factor in 0–1, and hints ordered by how much each one costs.
3. **Read the hints, not just the number.** Each names the weakest factor and the edit that
   raises it: "composition: centre the main block", "alignment: snap element edges to a shared
   grid", "whitespace: adjust padding so ~60% of the canvas is background".
4. **Make one edit** for the top hint. Re-render. Re-score (or `beauty_compare` before/after).
5. **Stop** when the score stops moving, or at the target the task set. Report before/after
   and the factor that moved.

Score the viewport, not a full-page capture of a very tall page. Score each state that
matters (empty state, dialog open, mobile width) separately.

## Reading the scale

| score | means |
|---:|---|
| 85+ | composed, aligned, calm |
| 70–84 | fine; one factor is dragging it (read the hint) |
| 50–69 | something structural is off — usually composition or white space |
| < 50 | unstyled, lopsided, or cluttered |

## Do not

- Chase the number with tricks (centring a wreck still scores as centred; the function
  measures form, not intent). Fix the cause the hint names.
- Trade legibility for symmetry. Text is texture to this metric; keep type readable.
- Treat one point as signal. Differences under ~3 points are noise; a factor moving by 0.2 is not.

## As a lint

```bash
beautiful shots/                          # every image in a folder, worst visible at a glance
beautiful --min 70 shots/                 # exit 1 below 70
beautiful --save-baseline .beautiful.json shots/   # remember today's scores
beautiful --baseline .beautiful.json shots/        # exit 1 on any regression > 3 points
beautiful --format github shots/          # annotations in a GitHub workflow
beautiful --format sarif shots/ > b.sarif # GitHub code scanning
```

Read `raw["experimental"]` too (feature congestion, contour congestion, edge-orientation
entropy, sequence): they are measured but not yet weighted, and they often name the problem
before the score moves.

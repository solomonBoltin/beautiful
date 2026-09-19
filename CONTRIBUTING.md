# Contributing to beautiful

Thanks for helping make the web less ugly. This project is small on purpose: three modules,
no model weights, every term an explicit formula. Contributions that keep it that way are
the easiest to merge.

## Set up

```bash
git clone https://github.com/solomonBoltin/beautiful
cd beautiful
python -m pip install -e .
python tests.py
```

`tests.py` checks the ordering invariants (a rebalanced page beats the original, an unstyled
page scores low, a mandala beats noise, ...). It must pass on every change. CI runs it on
Linux, macOS and Windows across Python 3.9–3.13.

## What is welcome

- **A factor that is a real property of the pixels**, with the paper it descends from and a
  target range. Add the measurement to `beautiful/features.py`, the goodness mapping and
  weight to `beautiful/core.py`, and a row to the formula table in the README.
- **Screenshots that break the score** — a page that looks great and scores low, or the
  reverse. Open an issue with the image and what you expected. These become test cases.
- **Fitting the weights to human ratings.** The weights are literature-shaped, not fitted.
  A pull request that fits them against a public dataset (Reinecke & Gajos 2013, Calista
  2023) and reports held-out correlation would be the most valuable change this repo can get.
- **Ports** (JavaScript / TypeScript, Rust) that reproduce the demo table within ±2 points.
- **Agent integrations**: an MCP server, a GitHub Action, editor extensions.

## What is not welcome

- Learned models as a dependency. Use one *next to* `beautiful`, not inside it.
- Semantic heuristics ("if it looks like a login page"). The function measures form.
- Weight changes without a stated reason and a before/after on the demo table.

## Pull requests

1. One change per PR, with the demo table regenerated if scores move
   (`python -m beautiful --mode=ui demo/screens/*.png`).
2. Keep functions pure: numpy in, numbers out. No I/O outside `to_rgb`.
3. Cite the source of any target range in a comment.

By contributing you agree that your work is released under the MIT licence.

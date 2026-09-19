# Changelog

## 0.2.0 — 2026-09-19

- **MCP server**: `beautiful-mcp` exposes `beauty_score` and `beauty_compare` to any MCP client
  (Claude Code, Cursor, Windsurf, ...). Dependency-free.
- **GitHub Action**: score screenshots in CI and comment the table on the pull request.
- **Browser demo**: drag a screenshot in, get the score — the real package running in the page.
- **Famous sites**: twenty well-known home pages scored, with the factor breakdown.
- **`demo/loop.gif`**: a real trace of the score climbing as a button walks back to centre.
- **Factor wishlist** (`FACTORS.md`) and an issue template for proposing new factors.
- PyPI publishing via trusted publishing on version tags.
- CLI: `--json`, `--min N` (CI gate). Windows consoles no longer crash on non-ASCII hints.

## 0.1.0 — 2026-09-19

- First public release: `beauty()`, `beauty_score()`, modes `ui` / `art` / `logo`, the CLI, the
  demo set, ordering-invariant tests, CI on Linux/macOS/Windows for Python 3.9–3.13.

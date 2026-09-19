"""A dependency-free MCP (Model Context Protocol) server exposing `beauty()` as a tool.

    beautiful-mcp                      # speaks MCP over stdio (JSON-RPC 2.0, newline-delimited)

Register it with any MCP client, e.g. Claude Code:

    claude mcp add beautiful -- beautiful-mcp

or in a `.mcp.json` / Cursor / Windsurf config:

    {"mcpServers": {"beautiful": {"command": "beautiful-mcp"}}}

Tools
-----
    beauty_score   image path (+ mode) -> the 1-100 number, factors, hints
    beauty_compare two image paths     -> which is more beautiful and by how much, factor by factor

The protocol subset implemented here (initialize, ping, tools/list, tools/call, notifications)
is the whole of what a tool-only server needs, so the package keeps its "numpy, pillow, scipy
and nothing else" promise.
"""
from __future__ import annotations

import json
import sys

from . import __version__
from .core import WEIGHTS, beauty

PROTOCOL_VERSION = "2024-11-05"

TOOLS = [
    {
        "name": "beauty_score",
        "description": (
            "Score an image (screenshot, logo, artwork) for beauty on a 1-100 scale, computed from "
            "pixels alone with explicit formulas (symmetry, balance, alignment, white space, colour "
            "harmony, contrast, complexity). Returns the score, every factor in 0-1, raw measurements "
            "and hints naming the weakest factors and what to change."
        ),
        "inputSchema": {
            "type": "object",
            "properties": {
                "image": {"type": "string", "description": "Path to a PNG/JPEG/WebP file"},
                "mode": {
                    "type": "string",
                    "enum": list(WEIGHTS),
                    "default": "ui",
                    "description": "ui = screens and pages, art = paintings/photos/posters, logo = marks and icons",
                },
            },
            "required": ["image"],
        },
    },
    {
        "name": "beauty_compare",
        "description": (
            "Score two images with the same formula and report which is more beautiful, the difference, "
            "and which factors moved. Use it to check that an edit improved a design."
        ),
        "inputSchema": {
            "type": "object",
            "properties": {
                "before": {"type": "string", "description": "Path to the earlier image"},
                "after": {"type": "string", "description": "Path to the later image"},
                "mode": {"type": "string", "enum": list(WEIGHTS), "default": "ui"},
            },
            "required": ["before", "after"],
        },
    },
]


def _score(args: dict) -> dict:
    r = beauty(args["image"], args.get("mode", "ui"))
    return {"score": r["score"], "mode": r["mode"], "factors": r["factors"], "hints": r["hints"], "raw": r["raw"]}


def _compare(args: dict) -> dict:
    mode = args.get("mode", "ui")
    a, b = beauty(args["before"], mode), beauty(args["after"], mode)
    moved = {k: round(b["factors"][k] - a["factors"][k], 3) for k in a["factors"]
             if abs(b["factors"][k] - a["factors"][k]) >= 0.02}
    return {
        "before": a["score"], "after": b["score"], "delta": b["score"] - a["score"],
        "verdict": "after is more beautiful" if b["score"] > a["score"]
                   else "before is more beautiful" if a["score"] > b["score"] else "no change",
        "factors_moved": dict(sorted(moved.items(), key=lambda kv: -abs(kv[1]))),
        "hints_for_after": b["hints"],
    }


HANDLERS = {"beauty_score": _score, "beauty_compare": _compare}


def _handle(msg: dict):
    """Return a response dict, or None for notifications."""
    method, mid, params = msg.get("method"), msg.get("id"), msg.get("params") or {}
    if method == "initialize":
        result = {
            "protocolVersion": params.get("protocolVersion", PROTOCOL_VERSION),
            "capabilities": {"tools": {}},
            "serverInfo": {"name": "beautiful", "version": __version__},
            "instructions": (
                "beautiful returns a mathematical beauty score, 1-100, for an image file. Read the "
                "hints: each names the weakest factor and the edit that raises it. Score the viewport "
                "a user sees, not a full-page capture. Differences under 3 points are noise."
            ),
        }
    elif method == "ping":
        result = {}
    elif method == "tools/list":
        result = {"tools": TOOLS}
    elif method == "tools/call":
        name, args = params.get("name"), params.get("arguments") or {}
        if name not in HANDLERS:
            return _error(mid, -32602, f"unknown tool {name!r}")
        try:
            payload = HANDLERS[name](args)
            result = {"content": [{"type": "text", "text": json.dumps(payload, ensure_ascii=False, indent=1)}],
                      "isError": False}
        except Exception as e:  # report tool failures inside the result, per spec
            result = {"content": [{"type": "text", "text": f"{type(e).__name__}: {e}"}], "isError": True}
    elif method is None or str(method).startswith("notifications/"):
        return None
    else:
        return _error(mid, -32601, f"method not found: {method}")
    return {"jsonrpc": "2.0", "id": mid, "result": result}


def _error(mid, code, message):
    return {"jsonrpc": "2.0", "id": mid, "error": {"code": code, "message": message}}


def main() -> int:
    out = sys.stdout
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        try:
            msg = json.loads(line)
        except json.JSONDecodeError:
            out.write(json.dumps(_error(None, -32700, "parse error")) + "\n")
            out.flush()
            continue
        resp = _handle(msg)
        if resp is not None:
            out.write(json.dumps(resp, ensure_ascii=False) + "\n")
            out.flush()
    return 0


if __name__ == "__main__":
    sys.exit(main())

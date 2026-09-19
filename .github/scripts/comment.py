"""Create or update the pull-request comment carrying beautiful-table.md (marker: <!-- beautiful-score -->)."""
import json
import os
import subprocess

repo, pr = os.environ["REPO"], os.environ["PR"]
body = open("beautiful-table.md", encoding="utf-8").read()
marker = "<!-- beautiful-score -->"

def gh(*args, **kw):
    return subprocess.run(["gh", "api", *args], check=True, capture_output=True, text=True, **kw).stdout

comments = json.loads(gh(f"repos/{repo}/issues/{pr}/comments?per_page=100"))
existing = next((c for c in comments if marker in (c.get("body") or "")), None)
payload = json.dumps({"body": body})
if existing:
    gh("-X", "PATCH", f"repos/{repo}/issues/comments/{existing['id']}", "--input", "-", input=payload)
    print("updated comment", existing["id"])
else:
    gh("-X", "POST", f"repos/{repo}/issues/{pr}/comments", "--input", "-", input=payload)
    print("created comment")

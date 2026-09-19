"""Screenshot a list of URLs/HTML files with headless Chromium and score them.
    npm install   (in demo/)   then:   python demo/capture_and_score.py
"""
import json, subprocess, sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from beautiful import beauty
HERE = os.path.dirname(os.path.abspath(__file__))
TARGETS = {  # name: url or local html path
    "pypi_home": "https://pypi.org/",
    "cratesio_home": "https://crates.io/",
}
os.makedirs(f"{HERE}/screens", exist_ok=True)
out = {}
for name, target in TARGETS.items():
    png = f"{HERE}/screens/{name}.png"
    script = "screenshot_url.js" if target.startswith("http") else "screenshot_file.js"
    subprocess.run(["node", f"{HERE}/{script}", target, png], check=True, cwd=HERE)
    r = beauty(png, "ui")
    out[name] = {"score": r["score"], "factors": r["factors"], "hints": r["hints"]}
    print(f"{r['score']:3d}  {name}")
json.dump(out, open(f"{HERE}/results_ui.json", "w"), indent=1)

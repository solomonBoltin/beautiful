"""Parametric SVG of the 'in' icon + Chromium rasteriser + beauty(logo) scorer."""
import io, sys, json, itertools
sys.path.insert(0, __import__("os").path.join(__import__("os").path.dirname(__file__), "..", ".."))
from PIL import Image
from beautiful import beauty

BG, INK, MINT = "#1b5e4a", "#ffffff", "#7fd1ae"

def svg(scale=1.0, dx=0, dy=0, stroke=1.0, char=1.0, face=True, gap=1.0, bg=BG, mint=MINT, size=1024, tile=True, radius=0.225, show_i=True, arch_dx=0):
    """Geometry in a 1000-unit box, mark drawn around the centre (500,500). scale multiplies the mark."""
    S = 1000; w = 42 * stroke                      # stroke / stem width
    # 'i': stem + dot; arch 'n': outline path; character: rounded square with a face, sitting on the baseline inside the arch
    stem_h, dot_h = 150 * 1.0, 62
    ix, arch_x, arch_w, arch_h = -165, -95, 340, 230       # relative to mark centre, baseline at +115
    base = 115
    g = []
    if show_i:
        g.append(f'<rect x="{ix - w/2}" y="{base - stem_h}" width="{w}" height="{stem_h}" rx="{w/2}" fill="{INK}"/>')
        g.append(f'<rect x="{ix - w/2}" y="{base - stem_h - 24*gap - dot_h}" width="{w}" height="{dot_h}" rx="{w/2}" fill="{INK}"/>')
    arch_x += arch_dx
    r = arch_w / 2
    top = base - arch_h
    # arch: outer path with rounded top corners; stroke-only outline with rounded caps
    g.append(f'<path d="M{arch_x + w/2},{base} V{top + r} A{r - w/2},{r - w/2} 0 0 1 {arch_x + arch_w - w/2},{top + r} V{base}" fill="none" stroke="{INK}" stroke-width="{w}" stroke-linecap="round"/>')
    cw = 135 * char; cx = arch_x + arch_w / 2; cy0 = base - cw
    g.append(f'<rect x="{cx - cw/2}" y="{cy0}" width="{cw}" height="{cw}" rx="{cw*0.22}" fill="{mint}"/>')
    if face:
        ey = cy0 + cw * 0.42; ex = cw * 0.2; er = cw * 0.055
        g.append(f'<circle cx="{cx - ex}" cy="{ey}" r="{er}" fill="{bg}"/><circle cx="{cx + ex}" cy="{ey}" r="{er}" fill="{bg}"/>')
        g.append(f'<path d="M{cx - cw*0.17},{cy0 + cw*0.62} Q{cx},{cy0 + cw*0.78} {cx + cw*0.17},{cy0 + cw*0.62}" fill="none" stroke="{bg}" stroke-width="{max(6, cw*0.06)}" stroke-linecap="round"/>')
    tile_el = f'<rect width="{S}" height="{S}" rx="{S*radius}" fill="{bg}"/>' if tile else ""
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {S} {S}" width="{size}" height="{size}">{tile_el}'
            f'<g transform="translate({S/2 + dx},{S/2 + dy}) scale({scale})">{"".join(g)}</g></svg>')

class Raster:
    def __init__(self):
        from playwright.sync_api import sync_playwright
        self.p = sync_playwright().start(); self.b = self.p.chromium.launch()
        self.page = self.b.new_page(viewport={"width": 1024, "height": 1024}, device_scale_factor=1)
    def png(self, s, size=1024):
        self.page.set_viewport_size({"width": size, "height": size})
        self.page.set_content(f'<html><body style="margin:0;background:#fff">{s}</body></html>')
        return Image.open(io.BytesIO(self.page.screenshot())).convert("RGB")
    def close(self): self.b.close(); self.p.stop()

def score(im): return beauty(im, "logo")

if __name__ == "__main__":
    R = Raster()
    im = R.png(svg(size=512), 512); r = score(im); im.save("v0.png")
    print("v0", r["score"], {k: round(v, 2) for k, v in r["factors"].items()}, r["hints"][:3])
    R.close()

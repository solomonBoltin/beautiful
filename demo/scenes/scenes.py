"""Five real-HTML scenes, each parameterised by t in [0, 1]: t = 0 is the flawed page a rushed
commit ships, t = 1 is the polished one. Every intermediate frame is rendered by the tool's own
frozen Chromium and scored by the lint (pixels + DOM rules), so the GIFs are traces of the
function, not mock-ups. `python demo/make_scene_gifs.py` builds them."""
from __future__ import annotations


def lerp(a, b, t):
    return a + (b - a) * t


FONT = "font-family: -apple-system, 'SF Pro Text', 'Segoe UI', Inter, Helvetica, Arial, sans-serif;"


def signin(t):
    """A sign-in split screen: t=0 the card is off-axis, the primary button is a shouting orange on
    a teal brand, labels float; t=1 one accent, one axis, 16px body, 44px targets."""
    off = round(lerp(140, 0, t)); accent = f"hsl({round(lerp(28, 216, t))}, {round(lerp(95, 62, t))}%, {round(lerp(50, 44, t))}%)"
    lab_off = round(lerp(48, 0, t)); gap = round(lerp(8, 20, t)); btn_h = round(lerp(34, 48, t)); body = round(lerp(13, 16, t))
    hero_w = round(lerp(62, 50, t))
    return f"""<!doctype html><html><head><meta name=viewport content="width=device-width,initial-scale=1"><style>
*{{box-sizing:border-box;margin:0}} body{{{FONT} background:#f6f7f9;color:#1b1f27;font-size:{body}px;line-height:1.5}}
.wrap{{display:grid;grid-template-columns:{hero_w}fr {100-hero_w}fr;min-height:100vh}}
.hero{{background:{"linear-gradient(160deg,#0f2b46,#123e6b 60%,#1b5a94)" if t < .5 else "linear-gradient(160deg,#eaf1fb,#dde8f8)"};color:{"#fff" if t < .5 else "#0f2b46"};padding:64px;display:flex;flex-direction:column;justify-content:center}}
.hero h1{{font-size:40px;line-height:1.15;font-weight:700;max-width:520px;letter-spacing:-.01em}}
.hero p{{margin-top:16px;font-size:18px;opacity:.85;max-width:440px}}
.hero .art{{margin-top:40px;display:grid;grid-template-columns:repeat(3,1fr);gap:12px;max-width:440px}}
.shot{{margin-top:40px;width:{round(lerp(380,460,t))}px;border-radius:14px;background:#fff;border:1px solid #cfdcf0;padding:22px;box-shadow:0 24px 48px rgba(15,43,70,.12)}} .shot b{{display:block;width:36%;height:14px;border-radius:7px;background:#0f2b46;margin-bottom:14px}} .shot i{{display:block;height:10px;border-radius:5px;background:#d6e0ee;margin-bottom:10px}} .bars{{display:flex;gap:10px;align-items:flex-end;height:110px;margin-top:18px}} .bars s{{flex:1;display:block;border-radius:6px 6px 0 0;background:#2b62d9}}
.hero .art i{{display:block;height:64px;border-radius:12px;background:{"rgba(255,255,255,.12)" if t < .5 else "rgba(15,43,70,.08)"}}}
.side{{display:flex;align-items:center;justify-content:center;padding:40px}}
.card{{width:400px;background:#fff;border:1px solid #e3e6ec;border-radius:16px;padding:36px;transform:translateX({off}px)}}
.logo{{width:40px;height:40px;border-radius:10px;background:{accent};margin-bottom:20px}}
h2{{font-size:24px;font-weight:700;margin-bottom:{gap}px}} .sub{{color:#5b6472;margin-bottom:{gap+8}px}}
label{{display:block;font-weight:600;margin:0 0 6px {lab_off}px}}
input{{width:100%;height:{btn_h}px;border:1px solid #cfd4dc;border-radius:10px;padding:0 14px;font:inherit;background:#fbfbfc}}
.f{{margin-bottom:{gap}px}} .row{{display:flex;justify-content:space-between;align-items:center;margin:4px 0 {gap+4}px}}
a{{color:{accent};text-decoration:none;font-weight:600}}
button{{width:100%;height:{btn_h}px;border:0;border-radius:10px;background:{accent};color:#fff;font:inherit;font-weight:700;font-size:{body}px;cursor:pointer}}
.alt{{margin-top:{gap}px;text-align:center;color:#5b6472}}
</style></head><body><div class=wrap><section class=hero><h1>Ship pages you can measure.</h1><p>One number for composition, contrast, hierarchy and forty-four DOM rules — on every commit.</p>{"<div class=art><i></i><i></i><i></i></div>" if t < .5 else "<div class=shot><b></b><i style=width:60%></i><i style=width:80%></i><i style=width:45%></i><div class=bars><s style=height:40%></s><s style=height:70%></s><s style=height:55%></s><s style=height:90%></s><s style=height:75%></s></div></div>"}</section>
<section class=side><form class=card><div class=logo></div><h2>Welcome back</h2><p class=sub>Sign in to your workspace</p>
<div class=f><label for=e>Email</label><input id=e type=email placeholder="you@company.com"></div>
<div class=f><label for=p>Password</label><input id=p type=password placeholder="••••••••"></div>
<div class=row><label style="margin:0;font-weight:500"><input type=checkbox style="width:auto;height:auto;margin-right:8px">Keep me signed in</label><a href="#">Forgot password?</a></div>
<button type=button>Sign in</button><p class=alt>New here? <a href="#">Create an account</a></p></form></section></div></body></html>"""


def dashboard(t):
    """An analytics dashboard: t=0 cards drift off the grid, four accent hues fight, the chart is
    washed grey-on-grey; t=1 one 8px grid, one accent, crisp contrast."""
    drift = lerp(1, 0, t); hue = lambda i: round(lerp([340, 30, 120, 270][i], 216, t))
    txt = f"rgb({round(lerp(150,27,t))},{round(lerp(150,31,t))},{round(lerp(150,39,t))})"
    cards = "".join(f"""<div class=card style="transform:translate({round(drift*[26,-18,12,-30][i])}px,{round(drift*[0,14,-10,8][i])}px)"><div class=k>{k}</div><div class=v style="color:hsl({hue(i)},70%,42%)">{v}</div><div class=d>{d}</div></div>"""
                    for i, (k, v, d) in enumerate([("Revenue", "$48.2k", "+12% vs last week"), ("Active users", "9,318", "+4%"), ("Churn", "1.9%", "−0.3 pt"), ("NPS", "62", "+5")]))
    bars = "".join(f"<i style='height:{h}%;background:hsl({hue(j%4) if t<1 else 216},{round(lerp(80,60,t))}%,{round(lerp(60,48,t))}%)'></i>" for j, h in enumerate([42, 58, 50, 71, 64, 80, 74, 90, 86, 78, 94, 88]))
    rows = "".join(f"<tr><td>{a}</td><td>{b}</td><td><span class=tag>{c}</span></td><td class=r>{d}</td></tr>" for a, b, c, d in
                   [("Acme Corp", "Enterprise", "active", "$12,400"), ("Northwind", "Team", "trial", "$0"), ("Globex", "Team", "active", "$3,200"), ("Initech", "Starter", "past due", "$640")])
    side_w = round(lerp(292, 240, t)); pad = round(lerp(18, 24, t))
    return f"""<!doctype html><html><head><meta name=viewport content="width=device-width,initial-scale=1"><style>
*{{box-sizing:border-box;margin:0}} body{{{FONT} background:#f4f5f8;color:{txt};font-size:15px;line-height:1.5}}
.app{{display:grid;grid-template-columns:{side_w}px 1fr;min-height:100vh}}
nav{{background:{"#0f172a" if t < .5 else "#fff"};border-right:1px solid #e2e6ee;color:{"#cbd5e1" if t < .5 else "#3c4452"};padding:{pad}px}} nav .b{{font-weight:700;color:{"#fff" if t < .5 else "#0f172a"};font-size:18px;margin-bottom:28px}}
nav a{{display:block;padding:10px 12px;border-radius:8px;color:inherit;text-decoration:none;margin-bottom:4px;font-size:15px}} nav a.on{{background:{"#1e293b" if t < .5 else "#eef2ff"};color:{"#fff" if t < .5 else "#1e3a8a"}}}
main{{padding:{pad + 8}px {pad + 12}px}} h1{{font-size:26px;font-weight:700;letter-spacing:-.01em}} .sub{{color:#5b6472;margin:4px 0 24px}}
.grid{{display:grid;grid-template-columns:repeat(4,1fr);gap:{round(lerp(10,20,t))}px;margin-bottom:24px}}
.card{{background:#fff;border:1px solid #e2e6ee;border-radius:14px;padding:18px 20px}} .k{{font-size:13px;color:#5b6472;font-weight:600;text-transform:uppercase;letter-spacing:.04em}}
.v{{font-size:28px;font-weight:700;margin:6px 0 2px}} .d{{font-size:13px;color:#5b6472}}
.panel{{background:#fff;border:1px solid #e2e6ee;border-radius:14px;padding:22px;margin-bottom:24px}} .panel h2{{font-size:16px;font-weight:700;margin-bottom:16px}}
.chart{{height:180px;display:flex;align-items:flex-end;gap:12px}} .chart i{{flex:1;border-radius:6px 6px 0 0;display:block}}
table{{width:100%;border-collapse:collapse}} td,th{{padding:12px 10px;border-bottom:1px solid #eef0f4;text-align:left}} th{{font-size:13px;color:#5b6472;text-transform:uppercase;letter-spacing:.04em}}
.tag{{background:#eef2ff;color:#3730a3;padding:2px 10px;border-radius:999px;font-size:13px;font-weight:600}} .r{{text-align:right;font-variant-numeric:tabular-nums}}
</style></head><body><div class=app><nav><div class=b>◈ Lumen</div><a class=on href="#">Overview</a><a href="#">Customers</a><a href="#">Billing</a><a href="#">Reports</a><a href="#">Settings</a></nav>
<main><h1>Overview</h1><p class=sub>Week 38 · updated 2 minutes ago</p><div class=grid>{cards}</div>
<div class=panel><h2>Weekly revenue</h2><div class=chart>{bars}</div></div>
<div class=panel><h2>Recent accounts</h2><table><tr><th>Account</th><th>Plan</th><th>Status</th><th class=r>MRR</th></tr>{rows}</table></div></main></div></body></html>"""


def pricing(t):
    """Three pricing tiers: t=0 the highlighted tier is taller and shifted, the CTA colours differ
    per card, the body text is centred and long; t=1 equal cards, one primary, left-set copy."""
    lift = round(lerp(-38, -12, t)); shift = round(lerp(34, 0, t)); align = "center" if t < .5 else "left"
    ctas = [f"hsl({round(lerp(h, 216, t))},70%,45%)" for h in (0, 140, 280)]
    def card(i, name, price, feats, hi=False):
        st = f"transform:translate({shift if i==1 else 0}px,{lift if hi else 0}px);" + ("border:2px solid #2b62d9;" if hi else "")
        li = "".join(f"<li>{f}</li>" for f in feats)
        return f"""<div class=card style="{st}"><div class=n>{name}</div><div class=p>{price}<span>/mo</span></div><ul>{li}</ul><button style="background:{ctas[i] if t<1 else ('#2b62d9' if hi else '#fff')};color:{'#fff' if (t<1 or hi) else '#2b62d9'};border:1px solid {'#2b62d9' if t==1 else ctas[i]}">Choose {name}</button></div>"""
    intro = "Every plan includes the pixel score, the DOM rules, the MCP server and the GitHub Action. Pick the seat count that fits your team; you can change it any time and we prorate the difference to the day."
    return f"""<!doctype html><html><head><meta name=viewport content="width=device-width,initial-scale=1"><style>
*{{box-sizing:border-box;margin:0}} body{{{FONT} background:#fff;color:#1b1f27;font-size:16px;line-height:1.55}}
header{{display:flex;justify-content:space-between;align-items:center;padding:20px 64px;border-bottom:1px solid #eceff3}} header b{{font-size:18px}} header a{{color:#3c4452;text-decoration:none;margin-left:28px;font-weight:500}}
.hd{{text-align:{align};max-width:{round(lerp(900,640,t))}px;margin:56px auto 40px;padding:0 24px}} h1{{font-size:40px;font-weight:700;letter-spacing:-.01em;margin-bottom:14px}} .hd p{{color:#5b6472;font-size:18px}}
.tiers{{display:grid;grid-template-columns:repeat(3,300px);gap:{round(lerp(12,24,t))}px;justify-content:center;padding:0 24px 80px}}
.card{{border:1px solid #e3e6ec;border-radius:16px;padding:28px;background:#fff}} .n{{font-weight:700;font-size:18px}} .p{{font-size:38px;font-weight:700;margin:10px 0 18px}} .p span{{font-size:15px;color:#5b6472;font-weight:500}}
ul{{list-style:none;padding:0;margin:0 0 24px}} li{{padding:7px 0 7px 26px;position:relative;color:#3c4452}} li:before{{content:"✓";position:absolute;left:0;color:#2b62d9;font-weight:700}}
button{{width:100%;height:46px;border-radius:10px;font:inherit;font-weight:700;cursor:pointer}}
</style></head><body><header><b>◈ beautiful</b><nav><a href="#">Docs</a><a href="#">Pricing</a><a href="#">GitHub</a></nav></header>
<div class=hd><h1>Simple pricing for every team</h1><p>{intro}</p></div>
<div class=tiers>{card(0,"Starter","$0",["1 project","Pixel score","Desktop viewport"])}{card(1,"Team","$29",["Unlimited projects","All 44 DOM rules","Three viewports","GitHub Action"],True)}{card(2,"Enterprise","$99",["SSO and audit log","Private renderer","Priority support","Custom rules"])}</div></body></html>"""


def product(t):
    """An e-commerce product page: t=0 six badges and stickers fight for the eye, the gallery is
    stretched, prices in three sizes; t=1 one image, one price, one primary action."""
    n_badges = round(lerp(6, 1, t)); stretch = lerp(1.35, 1, t); gap = round(lerp(12, 32, t))
    badges = "".join(f"<span class=badge style='background:hsl({[0,40,120,200,280,320][i]},85%,{round(lerp(50,42,t))}%)'>{b}</span>"
                     for i, b in enumerate(["-30% TODAY", "FREE SHIPPING", "NEW", "BESTSELLER", "LIMITED", "HOT"][:n_badges]))
    return f"""<!doctype html><html><head><meta name=viewport content="width=device-width,initial-scale=1"><style>
*{{box-sizing:border-box;margin:0}} body{{{FONT} background:#fff;color:#1b1f27;font-size:16px;line-height:1.55}}
header{{display:flex;justify-content:space-between;align-items:center;padding:18px 64px;border-bottom:1px solid #eceff3}} header b{{font-size:18px}} header a{{color:#3c4452;text-decoration:none;margin-left:28px;font-weight:500}}
.pd{{display:grid;grid-template-columns:1fr 1fr;gap:{gap+16}px;padding:48px 64px;max-width:1180px;margin:0 auto}}
.gal{{background:{"#e6e9ef" if t < .5 else "#fafbfc"};border:1px solid #e3e6ec;border-radius:16px;height:{round(lerp(520,460,t))}px;display:flex;align-items:center;justify-content:center;overflow:hidden}}
.shoe{{width:360px;height:200px;border-radius:120px 120px 40px 40px;background:linear-gradient(135deg,#1e3a5f,#3b82f6);transform:scaleX({stretch:.2f});box-shadow:0 30px 60px rgba(20,30,60,.25)}}
.badges{{display:flex;gap:8px;flex-wrap:wrap;margin-bottom:14px}} .badge{{color:#fff;font-size:12px;font-weight:800;padding:4px 10px;border-radius:6px;letter-spacing:.05em}}
h1{{font-size:{round(lerp(26,34,t))}px;font-weight:700;letter-spacing:-.01em;margin-bottom:8px}} .by{{color:#5b6472;margin-bottom:{gap}px}}
.price{{font-size:{round(lerp(38,30,t))}px;font-weight:700}} .old{{font-size:{round(lerp(24,16,t))}px;color:#6b7480;text-decoration:line-through;margin-left:10px}} .save{{display:{'inline' if t<.7 else 'none'};color:#c0262d;font-weight:700;margin-left:10px;font-size:20px}}
p.desc{{color:#3c4452;margin:{gap}px 0;max-width:520px}}
.sizes{{display:flex;gap:10px;margin-bottom:{gap}px}} .sizes span{{width:48px;height:44px;border:1px solid #cfd4dc;border-radius:8px;display:grid;place-items:center;font-weight:600}} .sizes span.on{{border-color:#1b1f27;background:#1b1f27;color:#fff}}
.cta{{display:flex;gap:12px}} button{{height:52px;border-radius:12px;font:inherit;font-weight:700;font-size:16px;padding:0 28px;cursor:pointer}}
.pri{{background:#1b1f27;color:#fff;border:0;flex:1}} .sec{{background:{'hsl(20,90%,50%)' if t<.6 else '#fff'};color:{'#fff' if t<.6 else '#1b1f27'};border:1px solid #cfd4dc}}
.meta{{margin-top:{gap}px;color:#5b6472;font-size:14px}} .meta b{{color:#1b1f27}}
</style></head><body><header><b>◈ Northstar</b><nav><a href="#">Men</a><a href="#">Women</a><a href="#">Sale</a><a href="#">Cart (1)</a></nav></header>
<div class=pd><div class=gal><div class=shoe></div></div><div><div class=badges>{badges}</div><h1>Meridian Runner</h1><p class=by>Northstar · Road running · 4.8 ★ (2,140 reviews)</p>
<div><span class=price>$129</span><span class=old>$184</span><span class=save>SAVE $55!!!</span></div>
<p class=desc>A neutral daily trainer with a responsive foam midsole, a breathable knit upper and a 32 mm stack. Built for easy miles and long Sundays.</p>
<div class=sizes><span>8</span><span>8.5</span><span class=on>9</span><span>9.5</span><span>10</span><span>11</span></div>
<div class=cta><button class=pri>Add to cart</button><button class=sec>Save</button></div>
<p class=meta><b>Free returns</b> within 30 days · Ships tomorrow · Carbon-neutral delivery</p></div></div></body></html>"""


def onboarding(t):
    """A phone onboarding screen (render at mobile): t=0 the illustration bleeds off the right
    edge, 12px text, cramped 32px buttons, a shouting secondary; t=1 margins, 16px body, 48px targets."""
    bleed = round(lerp(60, 0, t)); body = round(lerp(12, 16, t)); tgt = round(lerp(32, 48, t)); pad = round(lerp(8, 24, t))
    sec = f"hsl({round(lerp(0, 216, t))},{round(lerp(85, 60, t))}%,{round(lerp(50, 96, t))}%)"; sec_txt = "#fff" if t < .5 else "#2b62d9"
    return f"""<!doctype html><html><head><meta name=viewport content="width=device-width,initial-scale=1"><style>
*{{box-sizing:border-box;margin:0}} html,body{{height:100%}} body{{{FONT} background:#fff;color:#1b1f27;font-size:{body}px;line-height:1.5;overflow-x:hidden}}
.scr{{min-height:100vh;display:flex;flex-direction:column;padding:56px {pad}px {pad}px}}
.ill{{position:relative;height:300px;margin-bottom:28px}} .ill i{{position:absolute;border-radius:24px}}
.ill .a{{left:{pad}px;top:20px;width:{round(lerp(300,240,t))}px;height:220px;background:linear-gradient(135deg,#2b62d9,#7c3aed);transform:translateX({bleed}px)}}
.ill .b{{left:{round(lerp(180,150,t))}px;top:150px;width:140px;height:130px;background:#fbbf24;transform:translateX({bleed}px)}}
.ill .c{{left:{round(lerp(40,36,t))}px;top:200px;width:90px;height:90px;border-radius:50%;background:#10b981}}
h1{{font-size:{round(lerp(22,30,t))}px;font-weight:700;letter-spacing:-.01em;line-height:1.2;margin-bottom:10px}} p{{color:#5b6472;margin-bottom:auto}}
.dots{{display:flex;gap:6px;justify-content:center;margin:24px 0}} .dots i{{width:8px;height:8px;border-radius:50%;background:#d7dbe3}} .dots i.on{{background:#2b62d9;width:24px;border-radius:4px}}
button{{width:100%;height:{tgt}px;border-radius:12px;font:inherit;font-weight:700;font-size:{body}px;border:0;margin-bottom:{round(lerp(6,12,t))}px;cursor:pointer}}
.pri{{background:#2b62d9;color:#fff}} .sec{{background:{sec};color:{sec_txt}}}
</style></head><body><div class=scr><div class=ill><i class=a></i><i class=b></i><i class=c></i></div>
<h1>Measure every screen before you ship it</h1><p>Score composition, contrast and hierarchy on each commit, with the rules that catch what pixels miss.</p>
<div class=dots><i class=on></i><i></i><i></i></div><button class=pri>Get started</button><button class=sec>I already have an account</button></div></body></html>"""


SCENES = {
    "signin": (signin, "desktop", "Sign-in split screen: off-axis card, clashing accent, floating labels → one axis, one accent, 48 px targets"),
    "dashboard": (dashboard, "desktop", "Analytics dashboard: cards off the grid, four accents, washed text → 8 px grid, one accent, crisp contrast"),
    "pricing": (pricing, "desktop", "Pricing tiers: the highlighted tier lifted and shifted, three CTA colours, centred paragraph → equal cards, one primary"),
    "product": (product, "desktop", "Product page: six badges, a stretched hero, three price sizes → one image, one price, one action"),
    "onboarding": (onboarding, "mobile", "Phone onboarding: illustration bleeding off the edge, 12 px text, 32 px buttons → margins, 16 px body, 48 px targets"),
}

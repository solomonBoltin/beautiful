"""Sanity checks: known orderings must hold. Run: python tests.py"""
import os, sys
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from beautiful import beauty, beauty_score
from beautiful.experimental import accent_discipline
S = lambda p, m="ui": beauty_score(f"demo/screens/{p}.png", m)
A = lambda p, m="art": beauty_score(f"demo/art/{p}.png", m)
checks = [
    ("rebalanced Digital Office beats the original", S("digital_office_rebalanced") > S("digital_office_original") + 15),
    ("unstyled page scores low", S("github_login_unstyled") < 45),
    ("asymmetric sample scores below centred dialog", S("sample_asymmetric_ui") < S("pinkas_dialog") - 15),
    ("art: mandala beats abstract splashes beats noise", A("mandala_radial") > A("abstract_splashes") > A("random_noise")),
    ("logo: shield beats diagonal composition", A("shield_logo", "logo") > A("diagonal_composition", "logo") + 20),
]
r = beauty("demo/screens/pinkas_documents.png", "ui")
x = r["raw"]["experimental"]
checks += [
    ("experimental measurements are reported", all(k in x for k in ("feature_congestion", "contour_congestion", "edge_orientation_entropy", "anisotropy", "sequence"))),
    ("experimental values are in range", 0 <= x["contour_congestion"] <= 1 and 0 <= x["edge_orientation_entropy"] <= 1 and 0 <= x["sequence"] <= 1),
    ("unstyled page is more contour-congested than the composed one",
     beauty("demo/screens/github_login_unstyled.png")["raw"]["experimental"]["contour_congestion"] > x["contour_congestion"]),
]
med = beauty("demo/screens/medium_home.png", "ui")
checks += [
    ("asymmetric-but-balanced hero (Medium) is recognised as composed",
     med["factors"]["composition"] > 0.35 and med["factors"]["composition"] > beauty("demo/screens/sample_asymmetric_ui.png")["factors"]["composition"] + 0.2),
    ("airy pages are not punished for white space", med["factors"]["whitespace"] > 0.9),
    ("edge contact is measured on every side", all(k in med["raw"]["experimental"]["edge_contact"] for k in ("left", "right", "top", "bottom"))),
]
w = beauty("demo/screens/pinkas_documents.png", "web")
checks += [
    ("web mode returns a 1..100 percentile score with contributions", 1 <= w["score"] <= 100 and "contributions" in w["web"] and w["mode"] == "web"),
]
single_accent = np.ones((100, 100, 3), dtype=np.float32)
single_accent[:5] = (1, 0, 0)
two_accents = single_accent.copy()
two_accents[5:10] = (0, 0, 1)
checks += [
    ("one small saturated accent is measured near its canvas share",
     abs(accent_discipline(single_accent)["accent_share"] - 0.05) < 0.01),
    ("a similarly sized second accent lowers accent-discipline goodness",
     accent_discipline(two_accents)["accent_discipline"] < accent_discipline(single_accent)["accent_discipline"]),
]
ok = True
for name, cond in checks:
    print(("PASS " if cond else "FAIL ") + name); ok &= bool(cond)
sys.exit(0 if ok else 1)

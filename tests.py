"""Sanity checks: known orderings must hold. Run: python tests.py"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from beautiful import beauty, beauty_score
S = lambda p, m="ui": beauty_score(f"demo/screens/{p}.png", m)
A = lambda p, m="art": beauty_score(f"demo/art/{p}.png", m)
checks = [
    # the fitted `ui` formula (research/fit_ui.py): the curated orderings it was required to respect
    ("rebalanced Digital Office beats the original", S("digital_office_rebalanced") > S("digital_office_original") + 5),
    ("unstyled page scores low", S("github_login_unstyled") < 60),
    ("asymmetric sample scores below centred dialog", S("sample_asymmetric_ui") < S("pinkas_dialog") - 15),
    ("composed application screens beat the unstyled one", min(S("pinkas_documents"), S("pinkas_dashboard"), S("crates_io_search_q_http")) > S("github_login_unstyled") + 10),
    ("balanced-but-asymmetric hero (Medium) beats the lopsided sample", S("medium_home") > S("sample_asymmetric_ui") + 15),
    # the literature formula is still there, unchanged, as `classic`
    ("classic: rebalanced Digital Office beats the original by a wide margin", S("digital_office_rebalanced", "classic") > S("digital_office_original", "classic") + 15),
    ("classic: unstyled page scores low", S("github_login_unstyled", "classic") < 45),
    ("art: mandala beats abstract splashes beats noise", A("mandala_radial") > A("abstract_splashes") > A("random_noise")),
    ("logo: shield beats diagonal composition", A("shield_logo", "logo") > A("diagonal_composition", "logo") + 20),
    ("logo: a stroke end off the mark's radius scale costs points", beauty_score("demo/lint/caps-mismatch.png", "logo") < beauty_score("demo/lint/caps-match.png", "logo") - 2),
]
r = beauty("demo/screens/pinkas_documents.png", "ui")
x = r["raw"]["experimental"]
checks += [
    ("fitted ui report carries the classic score and the model provenance", r["mode"] == "ui" and 1 <= r["classic"]["score"] <= 100 and "fitted_on" in r["model"] and "composition" in r["factors"]),
    ("experimental measurements are reported", all(k in x for k in ("feature_congestion", "contour_congestion", "edge_orientation_entropy", "anisotropy", "sequence", "hierarchy"))),
    ("experimental values are in range", 0 <= x["contour_congestion"] <= 1 and 0 <= x["edge_orientation_entropy"] <= 1 and 0 <= x["sequence"] <= 1 and 0 <= x["hierarchy"] <= 1),
    ("unstyled page is more contour-congested than the composed one",
     beauty("demo/screens/github_login_unstyled.png")["raw"]["experimental"]["contour_congestion"] > x["contour_congestion"]),
]
med = beauty("demo/screens/medium_home.png", "classic")
checks += [
    ("asymmetric-but-balanced hero (Medium) is recognised as composed",
     med["factors"]["composition"] > 0.35 and med["factors"]["composition"] > beauty("demo/screens/sample_asymmetric_ui.png", "classic")["factors"]["composition"] + 0.2),
    ("airy pages are not punished for white space", med["factors"]["whitespace"] > 0.9 and beauty("demo/screens/medium_home.png")["factors"]["whitespace"] > 0.8),
    ("edge contact is measured on every side", all(k in med["raw"]["experimental"]["edge_contact"] for k in ("left", "right", "top", "bottom"))),
]
w = beauty("demo/screens/pinkas_documents.png", "web")
checks += [
    ("web mode returns a 1..100 percentile score with contributions", 1 <= w["score"] <= 100 and "contributions" in w["web"] and w["mode"] == "web"),
]
ok = True
for name, cond in checks:
    print(("PASS " if cond else "FAIL ") + name); ok &= bool(cond)
sys.exit(0 if ok else 1)

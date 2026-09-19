"""Sanity checks: known orderings must hold. Run: python tests.py"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from beautiful import beauty_score
S = lambda p, m="ui": beauty_score(f"demo/screens/{p}.png", m)
A = lambda p, m="art": beauty_score(f"demo/art/{p}.png", m)
checks = [
    ("rebalanced Digital Office beats the original", S("digital_office_rebalanced") > S("digital_office_original") + 15),
    ("unstyled page scores low", S("github_login_unstyled") < 45),
    ("asymmetric sample scores below centred dialog", S("sample_asymmetric_ui") < S("pinkas_dialog") - 15),
    ("art: mandala beats abstract splashes beats noise", A("mandala_radial") > A("abstract_splashes") > A("random_noise")),
    ("logo: shield beats diagonal composition", A("shield_logo", "logo") > A("diagonal_composition", "logo") + 20),
]
ok = True
for name, cond in checks:
    print(("PASS " if cond else "FAIL ") + name); ok &= bool(cond)
sys.exit(0 if ok else 1)

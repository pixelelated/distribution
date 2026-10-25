#!/usr/bin/env python3
"""#1057: RETENTION and A5 against a stub pair whose image has no
cloud_reconcile (the endpoint read stubbed to what both_changed left; sleeps
instant). Control on the fixed tool: with the script present and no record
appearing, RETENTION is its FAIL alone (its two checks gated on the kill point).
    python3 -I -B pos1057/drive.py <cloud-round-trip> unfixed|fixed"""
import contextlib, io, os, sys, types
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from common import args, load, verdict

tool, expect = args()
crt = load(tool)
crt._PREFIX = ""
crt.backend_files = lambda path: []
crt.backend_bytes = lambda path: None
crt.time = types.SimpleNamespace(sleep=lambda s: None, time=__import__("time").time, monotonic=__import__("time").monotonic)
crt.run_rc = lambda dev, cmd, *a, **k: (127, "sh: cloud_reconcile: not found")


def pair(has_script):
    held = {}
    class Dev:
        host, port = "stub", 0
        def __init__(self, side): self.side = side
        def run(self, cmd, check=True):
            if "command -v cloud_reconcile" in cmd: return "/usr/bin/cloud_reconcile\n" if has_script else ""
            if "cloud_reconcile" in cmd and "pgrep" not in cmd: return "sh: cloud_reconcile: not found\n"
            return ""
        def sha(self, path): return crt.sha(held[("dev", self.side)])
        def write(self, path, data): pass
    class Pair:
        saves_remote = "/pixelelated/Saves"; spath = "pixelelated/Saves"
        a, b = Dev("a"), Dev("b")
        def path(self, rel): return "/storage/cloud-qa/" + rel
        def both_changed(self, rel, h0, ha, hb, a_offset=3600): held[("dev", "a")] = ha; held["cloud"] = hb
        def cloud_sha(self, rel, folder=None): return crt.sha(held["cloud"])
    return Pair()


def run(fx, has_script):
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        f = fx(pair(has_script))
    lines = [l.strip() for l in buf.getvalue().splitlines() if l.strip()]
    for l in lines:
        print("   ", l[:150])
    return f, lines


f_ret, ret = run(crt.fx_retention, False)
f_a5, a5 = run(crt.fx_a5, False)
vacuous = sum(1 for l in ret if l.startswith("PASS"))
skips = sum(1 for l in ret + a5 if l.startswith("SKIP") and "cloud_reconcile" in l)
control = "n/a"
if skips == 2:
    f_c, c = run(crt.fx_retention, True)
    control = "FAIL alone" if f_c == 1 and not any(l.startswith("PASS") for l in c) else f"{c}"
print(f"RETENTION: {f_ret} failure(s), {vacuous} PASS line(s); A5: {f_a5}; SKIPs naming cloud_reconcile: {skips}; control: {control}")
observed = ("unfixed" if vacuous == 2 and skips == 0 else "fixed" if skips == 2 and f_ret == 0 and control == "FAIL alone" else "neither")
verdict("pos1057", expect, observed, f"{vacuous} vacuous PASS, {skips} SKIP, control {control}")

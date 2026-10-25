#!/usr/bin/env python3
"""#1092's host positive: how does KILL1 judge a re-run the stall ceiling
ended?

    python3 -I -B drive.py <path to cloud-round-trip> unfixed|fixed

Runs the tool's own fx_kill1 against a stub link: the kill lands, the
cloud holds whole v2 after it, and the re-run returns one of four faces:
  A  webdav, 124, the wrapper's stall line, the last per-file line at 100%
     (LINK's drained face), whole v2 after;
  B  webdav, 124, no stall line, whole v2 after;
  C  s3, 124, the stall line and 100%, whole v2 after;
  D  webdav, the drained face, but one file torn after.
Nothing leaves this process; no ssh, no endpoint.
"""
import contextlib, importlib.machinery, importlib.util, io, re, sys, types

tool, want = sys.argv[1], sys.argv[2]
loader = importlib.machinery.SourceFileLoader("crt", tool)
spec = importlib.util.spec_from_loader("crt", loader)
crt = importlib.util.module_from_spec(spec)
loader.exec_module(crt)

STALL = "rclone copy made no progress for 36s and was ended (it returned 143); reporting 124\n"
PROGRESS = " *  savestates/kill1-2.state:100% /3.004Mi, 0/s, -\n"
FACES = {
    "A": ("webdav", 124, STALL, PROGRESS, None),
    "B": ("webdav", 124, "", PROGRESS, None),
    "C": ("s3", 124, STALL, PROGRESS, None),
    "D": ("webdav", 124, STALL, PROGRESS, "savestates/kill1-2.state"),
}


class StubLink:
    def __init__(self, face):
        self.kind, self.rc, self.since, self.out, self.torn = face
        self.v2, self.calls = {}, 0
        self.dev = types.SimpleNamespace(run=lambda *a, **k: "FREE", write=lambda *a, **k: None)
        self.root, self.saves_remote = "/storage/qa-saves", "/pixelelated/Saves"
        self.args = types.SimpleNamespace(vocabulary=False)
    def reset(self): self.calls = 0
    def plant_cloud(self, files, where): pass
    def plant_device(self, root, files): self.v2 = dict(files)
    def stamps(self): return {}
    def start(self, cmd, env=""): pass
    def wait_marker(self, rx, timeout=0): return True, PROGRESS
    def inflight(self, out): return "savestates/kill1-2.state"
    def kill_group(self, sig, wait=0, then_kill_at=None): return 0.01
    def ended(self): return (0, "")
    def endpoint_quiet(self, limit=180): return 0.0
    def keep(self, key, out): pass
    def settle(self, side):
        self.calls += 1
        got = {r: (len(d), crt.sha(d)) for r, d in self.v2.items()}
        if self.calls > 1 and self.torn:            # after the re-run
            got[self.torn] = (1_048_576, "0" * 64)
        return got


def run(face):
    L = StubLink(FACES[face])
    crt.backend = lambda *a, **k: L.kind if a and a[0] == "backend" else ""
    crt.caps = lambda: {"commit": "atomic" if L.kind == "s3" else "partial"}
    crt.run_rc = lambda dev, cmd, env="": (L.rc, L.out)
    crt.log_mark = lambda dev: 0
    crt.log_since = lambda dev, mark: L.since
    crt.touch_offset = lambda *a, **k: None
    crt.assert_message = lambda *a, **k: 0
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        crt.fx_kill1(L)
    return [l.strip() for l in buf.getvalue().splitlines() if "re-run" in l and l.strip().startswith(("PASS", "FAIL", "SKIP"))
            and not l.strip().startswith(("PASS  1a re-run:", "PASS  1b re-run:"))]


seen = {}
for face in FACES:
    lines = [l for l in run(face) if l.split()[1].startswith("1a")]
    exit_line = next((l for l in lines if "re-run exits" in l or "stall ceiling" in l), "none")
    whole_line = next((l for l in lines if "after the re-run" in l), "none")
    seen[face] = (exit_line.split()[0], whole_line)
    print(f"{face} exit: {exit_line[:150]}")
    print(f"{face} after: {whole_line[:200]}")

names_state = "TORN (" in seen["D"][1]
fixed_ok = (seen["A"][0] == "SKIP" and seen["B"][0] == "FAIL" and seen["C"][0] == "FAIL"
            and seen["A"][1].startswith("PASS") and seen["D"][1].startswith("FAIL") and names_state)
unfixed_ok = all(seen[f][0] == "FAIL" for f in "ABC") and not names_state
detail = f"A {seen['A'][0]}, B {seen['B'][0]}, C {seen['C'][0]}; D's after-line names the state: {names_state}"
if want == "fixed" and fixed_ok:
    print(f"pos1092: fixed-expectation-met ({detail})")
elif want == "unfixed" and unfixed_ok:
    print(f"pos1092: unfixed-expectation-met ({detail})")
else:
    print(f"pos1092: UNEXPECTED ({want}: {detail})")
    sys.exit(1)

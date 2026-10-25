#!/usr/bin/env python3
"""#1066: does cloud-round-trip's cleanup delete an occupied
/storage/roms/vectrex it refused? A stub device rooted under $TMPDIR (no ssh,
backend() a no-op): seeded occupied, the fixed tool's content_root() asked
first where it exists, then restore_device(). Control on the fixed tool: an
absent vectrex is claimed and its fixture removed.
    python3 -I -B pos1066/drive.py <cloud-round-trip> unfixed|fixed"""
import os, re, subprocess, sys, types
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from common import args, load, scratch, verdict

tool, expect = args()
crt = load(tool)
crt.backend = lambda *a, **k: ""


def stub(root):
    class Dev:
        host, port = "stub-device", 0
        def _map(self, s):    # one pass, only where a path starts: the root itself contains /tmp/
            return re.sub(r"(?<![\w/.-])/(storage|tmp)/", root.replace("\\", "\\\\") + r"/\1/", s)
        def run(self, cmd, check=True):
            return subprocess.run(["bash", "-c", self._map(cmd)], capture_output=True, text=True).stdout
        def write(self, path, data):
            path = self._map(path); os.makedirs(os.path.dirname(path), exist_ok=True); open(path, "wb").write(data)
        def sha(self, path):
            return None
    return Dev()


a = types.SimpleNamespace(real_roms=False, keep=False)
root = scratch("pos1066")
lib = f"{root}/storage/roms/vectrex"
os.makedirs(lib); os.makedirs(f"{root}/storage/.config", exist_ok=True)
open(f"{lib}/a-real-game.vec", "wb").write(b"somebody's game\n")
dev = stub(root)
refused = None
if hasattr(crt, "content_root"):
    try:
        crt.content_root(dev, a)
    except crt.Fail as e:
        refused = str(e).replace(root, "<root>")
crt.restore_device(crt.Prepared(dev), a, None)
kept = os.path.exists(f"{lib}/a-real-game.vec")
print(f"refusal: {refused or 'none'}; after the cleanup the occupied library is {'STILL THERE' if kept else 'DELETED'}")
control = "n/a (no content_root)"
if hasattr(crt, "content_root"):
    root2 = scratch("pos1066c"); dev2 = stub(root2); crt.OWNED.clear()
    os.makedirs(f"{root2}/storage/.config", exist_ok=True)
    c = crt.content_root(dev2, a); dev2.write(f"{c}/fixture.rom", b"the run's own fixture")
    crt.restore_device(crt.Prepared(dev2), a, None)
    control = "REMOVED" if not os.path.exists(f"{root2}/storage/roms/vectrex") else "STILL THERE"
    print(f"control: an absent vectrex claimed, its fixture written, after the cleanup: {control}")
observed = "fixed" if (kept and refused and control == "REMOVED") else "unfixed" if not kept else "neither"
verdict("pos1066", expect, observed, f"library {'kept' if kept else 'deleted'}; control {control}")

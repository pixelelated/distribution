#!/bin/bash
# brief section 5's path-safe shape tally, as written (lines 385-406).
cd /workspace/repos/pixelelated/distribution.worktrees/m6-os-device-quirks-676 || exit 2
python3 -I - <<'PY'
import subprocess, re, collections
Q = "projects/ROCKNIX/packages/hardware/quirks/devices"
out = subprocess.run(["git", "ls-tree", "-r", "-z", "8ebaf8daad", "--", Q], capture_output=True, text=True, check=True).stdout
modes = collections.Counter(); blobs = []
for ent in out.split("\0"):
    if not ent: continue
    meta, path = ent.split("\t", 1); mode, typ, oid = meta.split()
    modes[mode] += 1
    if mode in ("100644", "100755"): blobs.append((path, oid))
print("modes", dict(modes), "blobs", len(blobs))
pats = {"/etc/profile": r"\. /etc/profile", "set_setting": r"set_setting", "/storage": r"/storage", "/sys writers": r"> */sys|tee /sys", "DEVICE_": r"DEVICE_[A-Z_]+=", "guard": r"\[ -[efd] \"?/(sys|dev)"}
she = collections.Counter(); hits = collections.Counter(); hits_sh = collections.Counter(); nsh = 0
for path, oid in blobs:
    body = subprocess.run(["git", "cat-file", "-p", oid], capture_output=True, text=True).stdout
    first = body.split("\n", 1)[0]; is_sh = first.startswith("#!")
    if is_sh: she[first] += 1; nsh += 1
    for k, rx in pats.items():
        if re.search(rx, body): hits[k] += 1; hits_sh[k] += is_sh
print("shebangs", she.most_common(3), "shell files", nsh)
print("over the blobs", dict(hits)); print("over the shell", dict(hits_sh))
PY

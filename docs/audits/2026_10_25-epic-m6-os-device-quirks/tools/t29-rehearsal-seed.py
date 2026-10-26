#!/usr/bin/env python3
"""T29 (#676, #1125): what tools/vm-upgrade-rehearsal seeds at the retired
GENERIC_X64 names, and what the fixed 091-retired-vm-fixes does with it.

    python3 -I -B docs/audits/2026_10_25-epic-m6-os-device-quirks/tools/t29-rehearsal-seed.py \
        [--rev <git rev of the rehearsal; default the working tree>] [--busybox <busybox>] \
        [--expect old|new]

1. The seed bodies. At a revision with `retired_body()` (S3's), that function is
   run under bash for each of the four names. At an earlier revision, the one
   line `:112` echoes into each of the four is used.
2. Each body's sha256 against the WRITTEN table of the working tree's 091
   (the fixed one, #1124).
3. That 091, under busybox sh (default: the M6 donor's, the image's shell for
   #!/bin/sh), over a scratch /storage seeded the rehearsal's way with no
   stamp: the four, plus the fifth name with the owner's bytes when the
   revision seeds one. Kept or removed is read after one run.

--expect old: none of the four is in WRITTEN and the fixed 091 keeps all
four (#1125's defect). --expect new: all four are, the fixed 091 removes the
four, and keeps the fifth. Writes only under a temporary directory. No guest.
"""
from pathlib import Path
import argparse, hashlib, os, re, subprocess, sys, tempfile

Q = "projects/ROCKNIX/packages/hardware/quirks/devices/QEMU Standard PC (Q35 + ICH9, 2009)/091-retired-vm-fixes"
NAMES = ["tmpfiles.d/20-x64-fd-improvements.conf", "sysctl.d/10-generic-x64.conf",
         "modules-load.d/x64-virtual-modules.conf", "profile.d/091-generic-x64-services"]
ap = argparse.ArgumentParser()
ap.add_argument("--rev")
ap.add_argument("--busybox", type=Path,
                default=Path("/workspace/artifacts/m6-donor/1a0266484423/image/system/usr/bin/busybox"))
ap.add_argument("--expect", choices=["old", "new"])
a = ap.parse_args()
tool = (subprocess.run(["git", "show", f"{a.rev}:tools/vm-upgrade-rehearsal"], capture_output=True, text=True,
                       check=True).stdout if a.rev else Path("tools/vm-upgrade-rehearsal").read_text())
print(f"rehearsal: {a.rev or 'working tree'}; 091: working tree")
BB = a.busybox.resolve()
print(f"shell: {BB} sh; sha256 {hashlib.sha256(BB.read_bytes()).hexdigest()}")

owned = None
if "retired_body() {" in tool:
    fn = tool[tool.index("retired_body() {"):]
    fn = fn[:fn.index("\n}\n") + 3]
    bodies = {n: subprocess.run(["bash", "-c", fn + 'retired_body "$1"', "_", n], capture_output=True,
                                text=True, check=True).stdout for n in NAMES}
    m = re.search(r'^OWNED=\.config/(\S+)', tool, re.M); o = re.search(r'^OWNED_BYTES="(.*)"$', tool, re.M)
    owned = (m.group(1), o.group(1) + "\n")
else:
    line = re.search(r"echo '(# seeded by vm-upgrade-rehearsal[^']*)' > \\\$f", tool).group(1)
    bodies = {n: line + "\n" for n in NAMES}

src = Path(Q).read_text()
written = set(tuple(l.split()) for l in src.split('WRITTEN="', 1)[1].split('"', 1)[0].splitlines())
intable = 0
for n in NAMES:
    h = hashlib.sha256(bodies[n].encode()).hexdigest()
    ok = (n, h) in written; intable += ok
    print(f"seed {n}: sha256 {h} {'in' if ok else 'NOT in'} WRITTEN")

script = src
for old in ("STAMP=/storage/.cache/retired-vm-fixes", "MASKS_STAMP=/storage/.cache/retired-rescue-masks",
            "MASKS_NOTE=/run/retired-rescue-masks.stamped", "C=/storage/.config"):
    assert script.count(old) == 1
    var, path = old.split("=", 1); script = script.replace(old, f'{var}="${{QA_ROOT}}{path}"')
with tempfile.TemporaryDirectory(prefix="t29-seed-", dir=os.environ.get("TMPDIR")) as t:
    root = Path(t); conf = root / "storage/.config"
    for d in (conf, root / "storage/.cache", root / "run"):
        d.mkdir(parents=True)
    for n, b in list(bodies.items()) + ([owned] if owned else []):
        (conf / n).parent.mkdir(parents=True, exist_ok=True); (conf / n).write_text(b)
    (root / "091").write_text(script)
    r = subprocess.run([str(BB), "sh", str(root / "091")], env={"PATH": str(BB.parent), "QA_ROOT": str(root)},
                       capture_output=True, text=True, timeout=30)
    kept = sum((conf / n).exists() for n in NAMES)
    owned_kept = (conf / owned[0]).read_text() == owned[1] if owned and (conf / owned[0]).exists() else None
    print(f"fixed 091 over the seed: rc={r.returncode} the four kept={kept} removed={4 - kept} "
          f"fifth={'none seeded' if owned is None else ('kept' if owned_kept else 'removed')}")
want = {"old": (0, 4, None), "new": (4, 0, True)}
got = (intable, kept, owned_kept)
if a.expect:
    if got != want[a.expect]:
        print(f"t29-rehearsal-seed: UNEXPECTED on {a.expect}: got {got} want {want[a.expect]}"); sys.exit(1)
    print(f"t29-rehearsal-seed: {a.expect}-expectation-met")

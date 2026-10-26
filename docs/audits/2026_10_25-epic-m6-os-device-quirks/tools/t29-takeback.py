#!/usr/bin/env python3
"""T29 (#676, #1124): what GENERIC_X64's 091-retired-vm-fixes removes before
and after its stamp exists.

    python3 -I -B docs/audits/2026_10_25-epic-m6-os-device-quirks/tools/t29-takeback.py \
        [--file <091-retired-vm-fixes>] [--busybox <busybox>] [--expect unfixed|fixed]

The script is #!/bin/sh, so it runs here under busybox sh (default: the M6
donor's, /workspace/artifacts/m6-donor/1a0266484423/image/system/usr/bin/busybox)
with PATH limited to that busybox's applet links, as on the image. /storage and
/run are redirected to a scratch root; nothing else in the script changes.

The two known contents are rebuilt from the retired 099-mount-configuration-fixes
at 73b20caf86 and 8bb74015e6 (the heredoc that wrote
tmpfiles.d/30-x64-mount-points.conf) and checked against the script's own
WRITTEN hashes before any case runs.

Cases, after one run of the script (the seat's G-12, and f):
  a edited         no stamp; edited content at a listed name
  b1 known-73b     no stamp; the 73b20caf86 content at its name
  b2 known-8bb     no stamp; the 8bb74015e6 content at its name
  c stamped        stamp present; edited content at a listed name
  d dangling       no stamp; a dangling symlink at a listed name
  e empty          no stamp; nothing at any listed name
  f live-link      no stamp; a symlink at a listed name to a file the user owns

--expect unfixed asserts what the file at 8ebaf8daad does; --expect fixed what
the fix must do. Without --expect it prints and exits 0. Writes only under a
temporary directory. No guest; nothing runs on a unit.
"""
from pathlib import Path
import argparse, hashlib, os, subprocess, sys, tempfile

Q = "projects/ROCKNIX/packages/hardware/quirks/devices/QEMU Standard PC (Q35 + ICH9, 2009)"
ap = argparse.ArgumentParser()
ap.add_argument("--file", type=Path, default=Path(f"{Q}/091-retired-vm-fixes"))
ap.add_argument("--busybox", type=Path,
                default=Path("/workspace/artifacts/m6-donor/1a0266484423/image/system/usr/bin/busybox"))
ap.add_argument("--expect", choices=["unfixed", "fixed"])
a = ap.parse_args()
BB = a.busybox.resolve()
ver = subprocess.run([str(BB)], capture_output=True, text=True).stdout.splitlines()[0]
print(f"shell: {BB} sh ({ver}); sha256 {hashlib.sha256(BB.read_bytes()).hexdigest()}")
print(f"file: {a.file}")

src = a.file.read_text()
for old in ("STAMP=/storage/.cache/retired-vm-fixes", "MASKS_STAMP=/storage/.cache/retired-rescue-masks",
            "MASKS_NOTE=/run/retired-rescue-masks.stamped", "C=/storage/.config"):
    assert src.count(old) == 1, f"t29-takeback: expected one '{old}'"
    var, path = old.split("=", 1)
    src = src.replace(old, f'{var}="${{QA_ROOT}}{path}"')

# The two known contents, from the retired quirk, checked against WRITTEN.
NAME = "tmpfiles.d/30-x64-mount-points.conf"
written = {}
for line in a.file.read_text().split('WRITTEN="', 1)[1].split('"', 1)[0].splitlines():
    f, s = line.split()
    written.setdefault(f, []).append(s)
known = []
for c in ("73b20caf86", "8bb74015e6"):
    old = subprocess.run(["git", "show", f"{c}:{Q}/099-mount-configuration-fixes"],
                         capture_output=True, text=True, check=True).stdout.splitlines()
    i = old.index(f"cat <<EOF >/etc/{NAME}")
    body = "\n".join(old[i + 1:old.index("EOF", i)]) + "\n"
    h = hashlib.sha256(body.encode()).hexdigest()
    assert h in written[NAME], f"t29-takeback: {c}'s content hashes {h}, not in WRITTEN"
    print(f"known content {c}: sha256 {h} (in WRITTEN)")
    known.append(body)

OTHER = "tmpfiles.d/10-generic-x64-journald.conf"
CASES = {"a edited": dict(stamp=False, put={OTHER: "my own edit\n"}),
         "b1 known-73b": dict(stamp=False, put={NAME: known[0]}),
         "b2 known-8bb": dict(stamp=False, put={NAME: known[1]}),
         "c stamped": dict(stamp=True, put={OTHER: "my own edit\n"}),
         "d dangling": dict(stamp=False, link={OTHER: "nowhere"}),
         "e empty": dict(stamp=False),
         "f live-link": dict(stamp=False, link={OTHER: "mine.conf"})}
res = {}
with tempfile.TemporaryDirectory(prefix="t29-takeback-", dir=os.environ.get("TMPDIR")) as t:
    for name, case in CASES.items():
        root = Path(t) / name.split()[0]
        conf = root / "storage/.config"; cache = root / "storage/.cache"
        for d in (conf, cache, root / "run"):
            d.mkdir(parents=True)
        stamp = cache / "retired-vm-fixes"
        if case["stamp"]:
            stamp.write_text("stamped before this boot\n")
        for f, body in case.get("put", {}).items():
            (conf / f).parent.mkdir(parents=True, exist_ok=True); (conf / f).write_text(body)
        for f, target in case.get("link", {}).items():
            (conf / f).parent.mkdir(parents=True, exist_ok=True); os.symlink(target, conf / f)
        if name.startswith("f"):
            (conf / "tmpfiles.d/mine.conf").write_text("the user's own rule\n")
        script = root / "091-retired-vm-fixes"; script.write_text(src)
        env = {"PATH": str(BB.parent), "QA_ROOT": str(root)}
        r = subprocess.run([str(BB), "sh", str(script)], env=env, capture_output=True, text=True, timeout=30)
        names = list(case.get("put", {})) + list(case.get("link", {}))
        kept = all(os.path.lexists(conf / f) for f in names) if names else None
        res[name] = (kept, stamp.exists())
        print(f"{name}: rc={r.returncode} {'kept' if kept else 'removed' if kept is False else 'nothing placed'} "
              f"stamp={'yes' if stamp.exists() else 'no'} stderr={r.stderr.strip()[:160]!r}")

# (kept, stamp after the run)
want = {"unfixed": {"a edited": (False, True), "b1 known-73b": (False, True), "b2 known-8bb": (False, True),
                    "c stamped": (True, True), "d dangling": (True, True), "e empty": (None, True),
                    "f live-link": (False, True)},
        "fixed": {"a edited": (True, False), "b1 known-73b": (False, True), "b2 known-8bb": (False, True),
                  "c stamped": (True, True), "d dangling": (False, True), "e empty": (None, True),
                  "f live-link": (True, False)}}
if not a.expect:
    sys.exit(0)
bad = [k for k, v in want[a.expect].items() if res[k] != v]
if bad:
    print(f"t29-takeback: UNEXPECTED on {a.expect}: " + ", ".join(bad)); sys.exit(1)
print(f"t29-takeback: {a.expect}-expectation-met")

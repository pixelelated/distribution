#!/usr/bin/env python3
"""T17 (#664): does backuptool's member check stop a settings archive that
writes outside /storage through a symlink member?

    python3 -I -B docs/audits/2026_10_26-epic-m6-cloud-setup-content/tools/t17-archive-fixture.py \
        [--file <backuptool>] [--busybox <busybox>]

Two halves, each with the product's own code or the image's tools:
  1. backuptool's foreign_member(), cut out of the script by name and run in
     bash with the M6 donor's busybox applets first on PATH, over the member
     list the donor busybox `tar -tzf` prints for the archive;
  2. the donor busybox `tar -xzf <archive> -C <root>`, the extraction the
     restore runs with -C / (backuptool :1679), into a scratch root holding storage/.config, as every device's /storage does.

Archives, built here with Python's tarfile (synthetic, no credential):
  escape    storage/.config/escape -> <scratch>/outside (an absolute symlink
            member), then storage/.config/escape/note.txt
  control   a member named storage/../outside-control.txt, which
            foreign_member exists to refuse

This is a named substitute for a full `backuptool restore` (which extracts
with -C / and is a stage-E or guest proof): it shows what the check judges
and what the extractor does with the same bytes. Writes only under a
temporary directory.
"""
from pathlib import Path
import argparse, io, os, subprocess, sys, tarfile, tempfile

ap = argparse.ArgumentParser()
ap.add_argument("--file", type=Path,
                default=Path("projects/ROCKNIX/packages/rocknix/sources/scripts/backuptool"))
ap.add_argument("--busybox", type=Path,
                default=Path("/workspace/artifacts/m6-donor/1a0266484423/image/system/usr/bin/busybox"))
a = ap.parse_args()
BB = a.busybox.resolve()
src = a.file.read_text()
start = src.index("foreign_member() {")
func = src[start:src.index("\n}\n", start) + 3]
print(f"file: {a.file}; foreign_member() lines {src[:start].count(chr(10)) + 1}-{src[:start].count(chr(10)) + func.count(chr(10))}")
print(f"tar and awk: {BB} (busybox applets first on PATH)")

t = Path(tempfile.mkdtemp(prefix="t17-archive-", dir=os.environ.get("TMPDIR")))
bbin = t / "bbin"; bbin.mkdir()
for applet in subprocess.run([str(BB), "--list"], capture_output=True, text=True, check=True).stdout.split():
    os.symlink(BB, bbin / applet)
env = {"PATH": f"{bbin}:/usr/bin:/bin"}


def build(name, members):
    path = t / f"{name}.tar.gz"
    with tarfile.open(path, "w:gz") as tf:
        for m in members:
            ti = tarfile.TarInfo(m["name"])
            if m.get("link"):
                ti.type, ti.linkname = tarfile.SYMTYPE, m["link"]
                tf.addfile(ti)
            else:
                data = m["data"].encode()
                ti.size = len(data)
                tf.addfile(ti, io.BytesIO(data))
    return path


outside = t / "outside"; outside.mkdir()
cases = {
    "escape": [{"name": "storage/.config/escape", "link": str(outside)},
               {"name": "storage/.config/escape/note.txt", "data": "written through a symlink member\n"}],
    "control": [{"name": "storage/../outside-control.txt", "data": "a dot-dot member\n"}],
}
res = {}
for name, members in cases.items():
    arc = build(name, members)
    listing = subprocess.run([str(bbin / "tar"), "-tzf", str(arc)], capture_output=True, text=True, env=env)
    mfile = t / f"{name}.members"; mfile.write_text(listing.stdout)
    check = subprocess.run(["bash", "-c", func + '\nforeign_member "$1"', "_", str(mfile)],
                           capture_output=True, text=True, env=env)
    verdict = {0: "refused (a member a restore can't put back)", 1: "accepted (no foreign member)"}.get(check.returncode, f"unreadable ({check.returncode})")
    root = t / f"root-{name}"; root.mkdir()
    (root / "storage/.config").mkdir(parents=True)   # a device always has /storage/.config
    ext = subprocess.run([str(bbin / "tar"), "-xzf", str(arc), "-C", str(root)], capture_output=True, text=True, env=env)
    escaped = (outside / "note.txt").exists() if name == "escape" else (t / "outside-control.txt").exists()
    res[name] = (check.returncode, escaped)
    print(f"{name}: members {listing.stdout.split()}; foreign_member -> rc {check.returncode}, {verdict}"
          f"{' first: ' + check.stdout.strip() if check.stdout.strip() else ''}; "
          f"busybox tar -xzf -C root -> rc {ext.returncode}{' (' + ext.stderr.strip()[:100] + ')' if ext.stderr.strip() else ''}; "
          f"a file landed outside the root: {'yes' if escaped else 'no'}")
link = t / "root-escape/storage/.config/escape"
print(f"escape: storage/.config/escape in the root is {'a symlink to ' + os.readlink(link) if link.is_symlink() else 'not a symlink'}")

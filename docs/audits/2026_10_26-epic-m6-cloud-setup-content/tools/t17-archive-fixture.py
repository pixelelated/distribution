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

--restore (stage E, S7, #1136; the guest run's shape, guest-cycle/pl18.out):
the real `backuptool restore --no-restart`, unmodified, inside a bubblewrap
sandbox (bwrap, unprivileged): /storage is a scratch directory, /var and
/tmp are tmpfs, /etc/profile an empty file bound over the host's, and the
donor's busybox applets first on PATH at /bbin. One hand-made archive per
case, each the newest under /storage/roms/backup, on a fresh /storage
holding storage/.config/game/existing.cfg:
  regular        storage/.config/game/t17.cfg                      (control)
  directory      storage/.config/t17d/ and t17d/f.cfg               (control)
  symlink        storage/.config/t17-link -> /var/tmp/t17-outside
  symlink-child  storage/.config/t17-escape -> /var/tmp/t17-outside, then t17-escape/note.txt
  hardlink       storage/.config/t17-hard, a hard link to /var/tmp/t17-target
  device         storage/.config/t17-dev, a character device 1,3
  fifo           storage/.config/t17-fifo
  revert-dir     game/existing.cfg (new bytes), t17r/child.cfg, then a file t17r:
                 regular members whose extraction fails on a directory the
                 restore itself made -- the revert's own case
Reported per case, read inside the sandbox before it ends: the restore's rc
and why line, the t17-* paths left in /storage/.config with their types,
whether anything exists at /var/tmp/t17-outside, whether
.restore-in-progress is left, and existing.cfg's bytes. --expect unfixed |
fixed asserts the file at 8ebaf8daad's shape or the fix's.
"""
from pathlib import Path
import argparse, io, os, subprocess, sys, tarfile, tempfile

ap = argparse.ArgumentParser()
ap.add_argument("--file", type=Path,
                default=Path("projects/ROCKNIX/packages/rocknix/sources/scripts/backuptool"))
ap.add_argument("--busybox", type=Path,
                default=Path("/workspace/artifacts/m6-donor/1a0266484423/image/system/usr/bin/busybox"))
ap.add_argument("--restore", action="store_true", help="the full restore in a bubblewrap sandbox (stage E, S7)")
ap.add_argument("--expect", choices=["unfixed", "fixed"])
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


def restore_cases():
    """--restore: the real `backuptool restore --no-restart` in a bubblewrap sandbox."""
    def arc(path, members):
        import time
        with tarfile.open(path, "w:gz") as tf:
            for kind, name, extra in members:
                ti = tarfile.TarInfo(name); ti.mtime = int(time.time())
                if kind == "sym": ti.type, ti.linkname = tarfile.SYMTYPE, extra; tf.addfile(ti)
                elif kind == "hard": ti.type, ti.linkname = tarfile.LNKTYPE, extra; tf.addfile(ti)
                elif kind == "chr": ti.type, ti.devmajor, ti.devminor = tarfile.CHRTYPE, 1, 3; tf.addfile(ti)
                elif kind == "fifo": ti.type = tarfile.FIFOTYPE; tf.addfile(ti)
                elif kind == "dir": ti.type, ti.mode = tarfile.DIRTYPE, 0o755; tf.addfile(ti)
                else:
                    data = extra.encode(); ti.size, ti.mode = len(data), 0o644; tf.addfile(ti, io.BytesIO(data))
    C = {
        "regular": [("file", "storage/.config/game/t17.cfg", "a restored setting\n")],
        "directory": [("dir", "storage/.config/t17d/", ""), ("file", "storage/.config/t17d/f.cfg", "in a folder\n")],
        "symlink": [("sym", "storage/.config/t17-link", "/var/tmp/t17-outside")],
        "symlink-child": [("sym", "storage/.config/t17-escape", "/var/tmp/t17-outside"),
                          ("file", "storage/.config/t17-escape/note.txt", "through the link\n")],
        "hardlink": [("hard", "storage/.config/t17-hard", "/var/tmp/t17-target")],
        "device": [("chr", "storage/.config/t17-dev", "")],
        "fifo": [("fifo", "storage/.config/t17-fifo", "")],
        "revert-dir": [("file", "storage/.config/game/existing.cfg", "new bytes from the archive\n"),
                       ("file", "storage/.config/t17r/child.cfg", "made a folder\n"),
                       ("file", "storage/.config/t17r", "a file where the restore made a folder\n")],
    }
    sbin = t / "sandbox-bin"; sbin.mkdir()
    for applet in subprocess.run([str(BB), "--list"], capture_output=True, text=True, check=True).stdout.split():
        os.symlink("/bb/busybox", sbin / applet)
    profile = t / "profile"; profile.write_text("# empty: the host's /etc/profile is not the image's\n")
    probe = r'''
mkdir -p /var/run /var/tmp /var/log; printf 'outside target\n' > /var/tmp/t17-target
/bin/bash /t17/backuptool restore --no-restart > /tmp/out 2>&1; rc=$?
echo "rc=$rc"
echo "why=$(grep -m1 '^>>> why' /tmp/out | sed 's/^>>> why //')"
echo "left=$(for p in /storage/.config/t17*; do [ -e "$p" ] || [ -L "$p" ] || continue; if [ -L "$p" ]; then k=link; elif [ -d "$p" ]; then k=dir; elif [ -p "$p" ]; then k=fifo; elif [ -c "$p" ]; then k=chardev; else k=file; fi; printf '%s:%s ' "${p##*/}" "$k"; done)"
echo "outside=$([ -e /var/tmp/t17-outside ] && echo yes || echo no)"
echo "target=$(cat /var/tmp/t17-target)"
echo "mark=$([ -e /storage/.config/.restore-in-progress ] && echo yes || echo no)"
echo "existing=$(cat /storage/.config/game/existing.cfg)"
echo "tail=$(tail -n 3 /tmp/out | tr '\n' ' ' | sed 's/\x1b\[[0-9;]*m//g' | cut -c1-220)"
'''
    res = {}
    for name, members in C.items():
        root = t / f"restore-{name}"
        (root / "storage/.config/game").mkdir(parents=True)
        (root / "storage/roms/backup").mkdir(parents=True)
        (root / "storage/.config/game/existing.cfg").write_text("the live setting\n")
        arc(root / "storage/roms/backup/2099_01_01-000000-T17-pixelelated_SETTINGS.tar.gz", members)
        cmd = ["bwrap", "--unshare-all", "--die-with-parent",
               "--ro-bind", "/usr", "/usr", "--ro-bind", "/bin", "/bin", "--ro-bind", "/lib", "/lib", "--ro-bind", "/lib64", "/lib64",
               "--ro-bind", "/etc", "/etc", "--ro-bind", str(profile), "/etc/profile",
               "--proc", "/proc", "--dev", "/dev", "--tmpfs", "/tmp", "--tmpfs", "/var",
               "--bind", str(root / "storage"), "/storage",
               "--ro-bind", str(a.file.resolve()), "/t17/backuptool",
               "--ro-bind", str(BB), "/bb/busybox", "--ro-bind", str(sbin), "/bbin",
               # The caller's environment stays outside: a TMPDIR naming a host path
               # that the sandbox does not have made mktemp fail (#549's lesson).
               "--clearenv", "--setenv", "PATH", "/bbin:/usr/bin:/bin", "--setenv", "HOME", "/tmp",
               "/bin/bash", "-c", probe]
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
        got = dict(l.split("=", 1) for l in r.stdout.splitlines() if "=" in l)
        res[name] = got
        print(f"restore {name}: rc {got.get('rc')}; why {got.get('why') or '-'}; left in .config: {got.get('left') or 'nothing'}; "
              f"/var/tmp/t17-outside: {got.get('outside')}; the hard link's target: {got.get('target')!r}; "
              f"mark left: {got.get('mark')}; existing.cfg: {got.get('existing')!r}"
              + (f"; the restore's last words: {got.get('tail', '').strip()!r}" if name == "revert-dir" else "")
              + (f"; sandbox stderr: {r.stderr.strip()[:160]}" if r.stderr.strip() else ""))
    REFUSED = "THIS BACKUP HOLDS FILES A RESTORE CAN'T PUT BACK"
    ok_fixed = {n: (res[n].get("rc") != "0" and res[n].get("why") == REFUSED and not res[n].get("left", "").strip()
                    and res[n].get("outside") == "no" and res[n].get("mark") == "no")
                for n in ("symlink", "symlink-child", "hardlink", "device", "fifo")}
    ok_fixed["regular"] = res["regular"].get("rc") == "0"
    ok_fixed["directory"] = res["directory"].get("rc") == "0" and "t17d:dir" in res["directory"].get("left", "")
    ok_fixed["revert-dir"] = (res["revert-dir"].get("rc") == "1" and res["revert-dir"].get("mark") == "no"
                              and "YOUR SETTINGS ARE UNCHANGED" in res["revert-dir"].get("tail", "")
                              and "t17r" not in res["revert-dir"].get("left", "") and res["revert-dir"].get("existing") == "the live setting")
    ok_unfixed = {"symlink": res["symlink"].get("rc") == "0" and "t17-link:link" in res["symlink"].get("left", ""),
                  "symlink-child": res["symlink-child"].get("mark") == "yes" and "t17-escape:dir" in res["symlink-child"].get("left", ""),
                  "revert-dir": res["revert-dir"].get("mark") == "yes" and "t17r:dir" in res["revert-dir"].get("left", ""),
                  "regular": res["regular"].get("rc") == "0"}
    if a.expect:
        want = ok_fixed if a.expect == "fixed" else ok_unfixed
        bad = [k for k, v in want.items() if not v]
        if bad:
            print(f"t17-archive-fixture --restore: UNEXPECTED on {a.expect}: " + ", ".join(bad)); sys.exit(1)
        print(f"t17-archive-fixture --restore: {a.expect}-expectation-met")


if a.restore:
    restore_cases()

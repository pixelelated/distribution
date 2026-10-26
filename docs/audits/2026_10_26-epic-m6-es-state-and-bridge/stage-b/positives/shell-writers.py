#!/usr/bin/env python3
"""T21 (#668) stage B: the shell writers of system.cfg, killed at their steps,
and the seed copied before the record is consulted.

    python3 -I -B shell-writers.py <001-functions> <seed system.cfg> <busybox> <os-release> <state-fixture> <scratch>

The functions are 8ebaf8daad's 001-functions, sourced at their own path
(/etc/profile.d/001-functions) with no path rewritten, in a bubblewrap sandbox
started with --clearenv: a tmpfs root whose /usr/bin is the donor image's
busybox applets plus bash (sourcing sets PATH=/usr/bin:..., so the image's
applets answer, as on a device), /storage and /tmp scratch, /usr/config
holding the image's seed. A kill point is an applet name shadowed by a
script that SIGKILLs the top shell at that step -- the step, not a path, is
what changes. Every case's files are then read on the host, and
state-fixture (the pin's AtomicFile and SystemConf) says what the
interface's next load would do with them.

  K1  killed while the temporary is being written (awk prints a line, then the kill)
  K2  killed after the temporary is whole, before the rename
  K3  killed just after the rename
  S1  system.cfg missing, a whole system.cfg.backup holding the player's keys:
      set_setting copies the image's seed first (001-functions:540-543), then
      the interface's next load records the seeded file over the record

Writes only under <scratch>. Exit 0 when K1-K3 keep the old or the new file
whole; S1 is reported as observed (it is the lead's positive, expected to
show the record lost).
"""
import os, shutil, subprocess, sys
from pathlib import Path

fn, seed, busybox, osrel, fixture, scratch = (Path(a) for a in sys.argv[1:7])
OLD = b"system.hostname=qa\nqa.setting=older\nqa.keep=kept\n"
REC = b"system.hostname=qa\nqa.setting=record\nqa.keep=kept\nqa.marker=player\n"
applets = subprocess.run([str(busybox), "--list"], capture_output=True, text=True, check=True).stdout.split()

def sandbox(case_dir, shadow):
    """bwrap argv for one case: shadow maps an applet name to a script body."""
    storage = case_dir / "storage"
    bb = case_dir / "bb"
    bb.mkdir(exist_ok=True)
    shutil.copy2(busybox, bb / "busybox")
    a = ["bwrap", "--die-with-parent", "--clearenv", "--unshare-pid", "--unshare-net",
         "--setenv", "PATH", "/usr/bin", "--setenv", "HOME", "/storage",
         "--tmpfs", "/", "--dir", "/usr",
         "--ro-bind", "/usr/lib", "/usr/lib", "--ro-bind", "/usr/lib64", "/usr/lib64",
         "--symlink", "usr/lib", "/lib", "--symlink", "usr/lib64", "/lib64",
         "--dir", "/etc", "--ro-bind", "/etc/ld.so.cache", "/etc/ld.so.cache",
         "--ro-bind", str(osrel), "/etc/os-release",
         "--dir", "/etc/profile.d", "--ro-bind", str(fn), "/etc/profile.d/001-functions",
         "--dir", "/usr/config/system/configs", "--ro-bind", str(seed), "/usr/config/system/configs/system.cfg",
         "--dir", "/bb", "--ro-bind", str(bb / "busybox"), "/bb/busybox",
         "--dir", "/usr/bin", "--ro-bind", "/usr/bin/bash", "/usr/bin/bash", "--symlink", "usr/bin", "/bin",
         "--dir", "/storage", "--bind", str(storage), "/storage",
         "--tmpfs", "/tmp", "--proc", "/proc", "--dev", "/dev"]
    for name in applets:
        if name in ("bash",):
            continue
        if name in shadow:
            script = case_dir / f"shadow-{name}"
            script.write_text("#!/bb/busybox sh\n" + shadow[name] + "\n")
            script.chmod(0o755)
            a += ["--ro-bind", str(script), f"/usr/bin/{name}"]
        else:
            a += ["--symlink", "/bb/busybox", f"/usr/bin/{name}"]
    return a

def run_case(name, shadow, live_bytes, rec_bytes):
    d = scratch / name
    if d.exists():
        shutil.rmtree(d)
    cfg = d / "storage/.config/system/configs"
    cfg.mkdir(parents=True)
    live, rec = cfg / "system.cfg", cfg / "system.cfg.backup"
    if live_bytes is not None:
        live.write_bytes(live_bytes); live.chmod(0o600)
    rec.write_bytes(rec_bytes); rec.chmod(0o600)
    argv = sandbox(d, shadow) + ["/usr/bin/bash", "-c",
        'export TOP=$$; . /etc/profile.d/001-functions; set_setting qa.setting newer; echo "set_setting rc=$?"']
    r = subprocess.run(argv, capture_output=True, text=True, timeout=30)
    after = live.read_bytes() if live.exists() else None
    ch = subprocess.run([str(fixture), "choose", str(live)], capture_output=True, text=True).stdout.strip()
    return d, live, rec, r, after, ch

def lines(b):
    return "absent" if b is None else "%d lines, marker %s, qa.setting=%s" % (
        b.count(b"\n"), "present" if b"qa.marker=player" in b else "absent",
        next((l.split(b"=", 1)[1].decode() for l in b.splitlines() if l.startswith(b"qa.setting=")), "-"))

fail = 0
NEW = b"system.hostname=qa\nqa.keep=kept\nqa.setting=newer\n"
kills = {
    "K1": {"awk": 'echo "system.hostname=qa"; kill -9 "$TOP"; exit 1'},
    "K2": {"mv": 'kill -9 "$TOP"; exit 1'},
    "K3": {"mv": '/bb/busybox mv "$@"; kill -9 "$TOP"'},
}
for name, shadow in kills.items():
    d, live, rec, r, after, ch = run_case(name, shadow, OLD, REC)
    state = "old" if after == OLD else "new" if after == NEW else "OTHER"
    temps = sorted(p.name for p in live.parent.iterdir() if ".tmp" in p.name)
    ok = state in ("old", "new") and (ch.startswith("source=Live") or ch.startswith("source=Backup"))
    fail |= not ok
    print(f"{name} {list(shadow)[0]} shadowed: bash rc {r.returncode}; system.cfg {state}; record {'unchanged' if rec.read_bytes() == REC else 'CHANGED'}; next interface load {ch}; left behind {temps or 'nothing'}; {'ok' if ok else 'FAIL'}")

# The unkilled run, as a control: the writer itself works in this sandbox.
d, live, rec, r, after, ch = run_case("K0", {}, OLD, REC)
print(f"K0 control (no kill): {r.stdout.strip()}; system.cfg {'new' if after == NEW else 'OTHER: ' + lines(after)}; next interface load {ch}")
fail |= after != NEW

# S1: the seed before the record.
d, live, rec, r, after, ch = run_case("S1", {}, None, REC)
print(f"S1 system.cfg absent, record holds the player's keys: {r.stdout.strip()}")
print(f"   system.cfg after set_setting: {lines(after)}; mode {oct(live.stat().st_mode & 0o777) if live.exists() else '-'}")
print(f"   system.cfg.backup after set_setting: {lines(rec.read_bytes())}")
print(f"   the interface's next load chooses: {ch}")
g = subprocess.run([str(fixture), "get", str(live), str(d / ".lock"), "qa.marker"], capture_output=True, text=True)
print(f"   a SystemConf load of that file (the pin's code): {g.stdout.strip()} rc {g.returncode}")
print(f"   system.cfg.backup after the interface's load: {lines(rec.read_bytes())}")
print("== result:", "PASS (K0-K3)" if not fail else "FAIL", "; S1 as observed above")
sys.exit(1 if fail else 0)

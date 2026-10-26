#!/usr/bin/env python3
"""T17 (#664): the mode each writer leaves its file with, observed.

    python3 -I -B docs/audits/2026_10_26-epic-m6-cloud-setup-content/tools/t17-mode-fixture.py [--umask 022]

Real functions, scratch paths, under the given umask (default 022, the
device's): cloud_connections.atomic() over rclone.conf and active-connection
(and over an existing 0644 rclone.conf, to see whether the old mode survives);
cloud_connections.save()'s staging directory and staged copy (stopped at the
first rclone call, which raises); cloud_oauth's _write_whole() (session.json),
_state_locked() (session.lock) and the marker writes; cloud_device_id's
write_id and remember_previous, and a cloud_scan-style `> file` write, run
through bash with the M6 donor's busybox. No rclone runs (the one call reached
is answered by a stub that fails). Writes only under a temporary directory.
"""
from pathlib import Path
import argparse, importlib.machinery, importlib.util, os, stat, subprocess, sys, tempfile

ap = argparse.ArgumentParser()
ap.add_argument("--umask", default="022")
ap.add_argument("--busybox", type=Path,
                default=Path("/workspace/artifacts/m6-donor/1a0266484423/image/system/usr/bin/busybox"))
a = ap.parse_args()
os.umask(int(a.umask, 8))
SRC = Path("projects/ROCKNIX/packages/network/rclone/sources").resolve()
sys.path.insert(0, str(SRC))
t = Path(tempfile.mkdtemp(prefix="t17-mode-", dir=os.environ.get("TMPDIR")))
print(f"umask {a.umask}; scratch under TMPDIR")


def mode(p):
    return oct(stat.S_IMODE(os.lstat(p).st_mode))


import cloud_connections as c
c.CONFIG = t / "rclone/rclone.conf"; c.ACTIVE = t / "rclone/active-connection"
c.LOCK = t / "run/cloud_sync.lock"; c.SYSTEM = t / "system.cfg"
c.atomic(c.CONFIG, b"[qa]\ntype = local\n")
print(f"atomic() new rclone.conf: {mode(c.CONFIG)}")
c.CONFIG.chmod(0o644)
c.atomic(c.CONFIG, b"[qa]\ntype = local\n")
print(f"atomic() over an existing 0644 rclone.conf: {mode(c.CONFIG)}")
c.atomic(c.ACTIVE, b"qa\n")
print(f"atomic() active-connection: {mode(c.ACTIVE)}")
with c.locked():
    print(f"locked(): {c.LOCK.name} {mode(c.LOCK)} (opened 'a')")
seen = {}
real_run = c.run
def stop_at_first_rclone(args):
    staged = Path(args[args.index("--config") + 1])
    seen["dir"] = mode(staged.parent); seen["file"] = mode(staged)
    raise c.Refused("stub: no rclone in the fixture")
c.run = stop_at_first_rclone
try:
    c.save("second", "local", [("nounc", "true")])
except c.Refused:
    pass
c.run = real_run
print(f"save(): staging directory {seen.get('dir')}, staged rclone.conf {seen.get('file')}; "
      f"left behind after a refusal: {sorted(p.name for p in c.CONFIG.parent.glob('.connection-*'))}")

loader = importlib.machinery.SourceFileLoader("cloud_oauth_mode", str(SRC / "cloud_oauth"))
spec = importlib.util.spec_from_loader(loader.name, loader); o = importlib.util.module_from_spec(spec); loader.exec_module(o)
o.STATE_DIR = str(t / "cloud_oauth"); o.LOG_FILE = str(t / "cloud_sync.log")
o.write_state(status="waiting", pin="0000")
print(f"cloud_oauth STATE_DIR: {mode(o.STATE_DIR)}; session.json: {mode(o.state_path('session.json'))}; "
      f"session.lock: {mode(o.state_path('session.lock'))}; cloud_sync.log (log()): ", end="")
o.log("fixture line"); print(mode(o.LOG_FILE))
open(o.state_path("signed-in"), "w").close()
print(f"cloud_oauth marker signed-in: {mode(o.state_path('signed-in'))}")

BB = a.busybox.resolve()
bins = t / "bbin"; bins.mkdir()
for applet in subprocess.run([str(BB), "--list"], capture_output=True, text=True, check=True).stdout.split():
    os.symlink(BB, bins / applet)
did = (SRC / "cloud_device_id").read_text()
start = did.index("write_id() {"); end = did.index("\n}\n", did.index("remember_previous() {")) + 3
script = (f'ID_FILE="{t}/cloud_sync-device-id"\nPREVIOUS_FILE="${{ID_FILE}}.previous"\n' + did[start:end]
          + '\numask ' + a.umask + '\nwrite_id "Anbernic-RG-SP-0123456789" && remember_previous "ROCKNIX-ee5013fc56"\n'
          + f'echo "scan result" > "{t}/scan-state"\n')
r = subprocess.run(["bash", "-c", script], capture_output=True, text=True, env={"PATH": f"{bins}:/usr/bin:/bin"})
print(f"cloud_device_id write_id: {mode(t / 'cloud_sync-device-id')}; .previous: {mode(t / 'cloud_sync-device-id.previous')}; "
      f"a cloud_scan-style '> file': {mode(t / 'scan-state')} (bash rc {r.returncode})")

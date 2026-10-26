#!/usr/bin/env python3
"""T21 (#668) stage C, Astra's SO-23: an empty HOSTNAME saved by the interface,
then the next boot's chksysconfig.

    python3 -I -B hostname-empty.py <state-fixture> <chksysconfig> <001-functions> <seed> <busybox> <os-release> <scratch>

1. The pin's SystemConf (state-fixture `set`) saves system.hostname as "" on a
   whole system.cfg beside its whole record: the save the HOSTNAME row makes
   when the player clears it (GuiSettings.cpp addInputTextConfigRow's
   updateVal, GuiMenu.cpp:9929; no empty check).
2. 8ebaf8daad's chksysconfig `verify`, unrewritten, in bubblewrap with
   --clearenv, the donor's busybox as /usr/bin (shell-writers.py's sandbox),
   plus two things the image has and the donor does not: an /etc/profile that
   sources 001-functions (chksysconfig:25 sources /etc/profile), and `grep`,
   which the donor's busybox does not carry. The host's GNU grep stands in
   for it, named as a substitute; rsync stays absent and its line is reported.

Prints which keys each file holds (names and counts only). Writes only under
<scratch>. Exit 0 always: this is a lead's positive, reported as observed.
"""
import shutil, subprocess, sys
from pathlib import Path

fixture, ck, fn, seed, busybox, osrel, scratch = (Path(a) for a in sys.argv[1:8])
d = scratch / "so23"
if d.exists():
    shutil.rmtree(d)
cfg = d / "storage/.config/system/configs"
cfg.mkdir(parents=True)
live, rec = cfg / "system.cfg", cfg / "system.cfg.backup"
text = b"system.hostname=qa\nqa.marker=player\nwifi.ssid=QA-NET\nqa.keep=kept\n"
live.write_bytes(text); live.chmod(0o600)
rec.write_bytes(text); rec.chmod(0o600)
(d / "empty").write_bytes(b"")

def state(label):
    for f in (live, rec):
        b = f.read_bytes() if f.exists() else None
        if b is None:
            print(f"   {label}: {f.name} absent")
            continue
        keys = [l.split(b"=", 1)[0].decode() for l in b.splitlines() if b"=" in l]
        print(f"   {label}: {f.name} {len(keys)} keys; system.hostname line {'present' if b'system.hostname=' in b else 'ABSENT'}; "
              f"qa.marker {'present' if b'qa.marker=player' in b else 'ABSENT'}")

print("== 0 before")
state("before")
r = subprocess.run([str(fixture), "set", str(live), str(d / ".lock"), "system.hostname", str(d / "empty")], capture_output=True, text=True)
print(f"== 1 the interface saves system.hostname as empty (the pin's SystemConf): rc {r.returncode}")
state("after the save")
r = subprocess.run([str(fixture), "get", str(live), str(d / ".lock"), "qa.marker"], capture_output=True, text=True)
print(f"   the interface's next start (a fresh SystemConf load): {r.stdout.strip()}")
state("after that start")

bb = d / "bb"; bb.mkdir(); shutil.copy2(busybox, bb / "busybox")
applets = subprocess.run([str(busybox), "--list"], capture_output=True, text=True, check=True).stdout.split()
a = ["bwrap", "--die-with-parent", "--clearenv", "--unshare-pid", "--unshare-net",
     "--setenv", "PATH", "/usr/bin", "--setenv", "HOME", "/storage",
     "--tmpfs", "/", "--dir", "/usr",
     "--ro-bind", "/usr/lib", "/usr/lib", "--ro-bind", "/usr/lib64", "/usr/lib64",
     "--symlink", "usr/lib", "/lib", "--symlink", "usr/lib64", "/lib64",
     "--dir", "/etc", "--ro-bind", "/etc/ld.so.cache", "/etc/ld.so.cache", "--ro-bind", str(osrel), "/etc/os-release",
     "--dir", "/etc/profile.d", "--ro-bind", str(fn), "/etc/profile.d/001-functions",
     "--dir", "/usr/config/system/configs", "--ro-bind", str(seed), "/usr/config/system/configs/system.cfg",
     "--dir", "/bb", "--ro-bind", str(bb / "busybox"), "/bb/busybox",
     "--dir", "/usr/bin", "--ro-bind", "/usr/bin/bash", "/usr/bin/bash", "--symlink", "usr/bin", "/bin",
     "--dir", "/storage", "--bind", str(d / "storage"), "/storage",
     "--tmpfs", "/tmp", "--proc", "/proc", "--dev", "/dev"]
(d / "profile").write_text(". /etc/profile.d/001-functions\n")
a += ["--ro-bind", str(d / "profile"), "/etc/profile"]
for name in applets:
    if name != "bash":
        a += ["--symlink", "/bb/busybox", f"/usr/bin/{name}"]
if "grep" not in applets:
    print("   (substitute: the host's /usr/bin/grep stands in for grep, which the donor's busybox lacks)")
    a += ["--ro-bind", "/usr/bin/grep", "/usr/bin/grep"]
a += ["--ro-bind", str(ck), "/usr/bin/chksysconfig.real"]
r = subprocess.run(a + ["/usr/bin/bash", "/usr/bin/chksysconfig.real", "verify"], capture_output=True, text=True, timeout=60)
print(f"== 2 the next boot's chksysconfig verify (8ebaf8daad, unrewritten): rc {r.returncode}")
for line in (r.stdout + r.stderr).splitlines():
    if line.strip():
        print("   said:", line.strip()[:160])
state("after chksysconfig")

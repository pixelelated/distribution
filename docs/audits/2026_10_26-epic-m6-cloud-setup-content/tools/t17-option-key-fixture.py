#!/usr/bin/env python3
"""T17 (#664): does an option-shaped key reach rclone as a flag? (Astra's A-45,
Argon's R-18/R-40; #1131) And does a killed save's staging stay? (F-06, PL-08)

    python3 -I -B docs/audits/2026_10_26-epic-m6-cloud-setup-content/tools/t17-option-key-fixture.py \
        [--sources <dir holding cloud_connections.py and cloud_remote>] [--rclone <path>] [--expect unfixed|fixed]

The product's own cloud_remote argv parsing (its `key=value` split, read from
the file) and cloud_connections.save(), with CONFIG, ACTIVE, LOCK and SYSTEM
pointed into a scratch directory and RCLONE at the M6 donor's rclone 1.75.2.
The backend is `local`: no network. Each case on a fresh scratch root:

  control   settings [("nounc", "true")]: saved into rclone.conf
  config    settings [("--config", <scratch>/elsewhere.conf)]: where does the section land?
  dash-key  settings [("--log-file", <scratch>/flag.log)]: is a second flag honoured?
  sigkill   (stage E, S4) a save in a child process whose rclone is a stub
            that sleeps on `config`, SIGKILLed once its staging exists: what
            is left beside rclone.conf?
  sweep     (stage E, S4) a `.connection-*` directory and `.rclone.conf-*` and
            `.active-connection-*` files planted beside rclone.conf, then the
            control's save: are they still there?

Prints, per case: save()'s outcome, whether rclone.conf holds the section,
whether the outside file exists and holds it, and what is left. --expect
unfixed asserts what the files at 8ebaf8daad do; --expect fixed what the fix
must do (the two option-shaped keys refused before staging, nothing written
outside; the planted leftovers swept). Writes only under a temporary
directory. No value here is a credential.
"""
from pathlib import Path
import argparse, configparser, importlib, os, signal, subprocess, sys, tempfile, time

ap = argparse.ArgumentParser()
ap.add_argument("--rclone", default="/workspace/artifacts/m6-donor/1a0266484423/image/system/usr/bin/rclone")
ap.add_argument("--sources", type=Path, default=Path("projects/ROCKNIX/packages/network/rclone/sources"))
ap.add_argument("--expect", choices=["unfixed", "fixed"])
a = ap.parse_args()
SRC = a.sources.resolve()
sys.path.insert(0, str(SRC))
c = importlib.import_module("cloud_connections")
print(f"sources: {a.sources}")

# cloud_remote's own split (cloud_remote:329-334), read from the file so a change there shows here.
remote = (SRC / "cloud_remote").read_text()
assert 'key, value = pair.split("=", 1)' in remote and 'if "=" not in pair:' in remote, "cloud_remote's split moved"


def split(argv):
    out = []
    for pair in argv:
        if "=" not in pair:
            raise SystemExit("cloud_remote would refuse: " + pair)
        out.append(tuple(pair.split("=", 1)))
    return out


def has(path, name):
    if not path.exists():
        return "absent"
    p = configparser.ConfigParser(interpolation=None)
    p.read(path)
    return "holds the section" if p.has_section(name) else "exists, no section"


def point(root):
    c.RCLONE = a.rclone
    c.CONFIG = root / "rclone/rclone.conf"; c.ACTIVE = root / "rclone/active-connection"
    c.LOCK = root / "run/cloud_sync.lock"; c.SYSTEM = root / "system.cfg"


def left(root):
    d = root / "rclone"
    return sorted(p.name for p in d.iterdir() if p.name.startswith(".")) if d.exists() else []


res = {}
for case in ("control", "config", "dash-key"):
    root = Path(tempfile.mkdtemp(prefix=f"t17-optkey-{case}-", dir=os.environ.get("TMPDIR")))
    point(root)
    outside = root / "elsewhere.conf"; flaglog = root / "flag.log"
    argv = {"control": ["nounc=true"],
            "config": ["nounc=true", f"--config={outside}"],
            "dash-key": ["nounc=true", f"--log-file={flaglog}"]}[case]
    try:
        c.save("qa", "local", split(argv))
        outcome = "saved"
    except c.Refused as exc:
        outcome = "refused: " + str(exc)
    res[case] = (outcome == "saved", has(c.CONFIG, "qa") == "holds the section",
                 outside.exists(), flaglog.exists())
    print(f"{case}: save() {outcome}; rclone.conf {has(c.CONFIG, 'qa')}; "
          f"outside conf {has(outside, 'qa')}; flag.log {'exists' if flaglog.exists() else 'absent'}; "
          f"staging left {left(root)}")

# sigkill: a child saves through a stub rclone that sleeps on `config`; killed once staging exists.
root = Path(tempfile.mkdtemp(prefix="t17-optkey-sigkill-", dir=os.environ.get("TMPDIR")))
stub = root / "rclone-stub"
stub.write_text('#!/bin/sh\necho $$ > "$0.pid"\ncase " $* " in *" config "*) sleep 30 ;; esac\nexit 0\n')
stub.chmod(0o755)
child_code = (
    "import sys; from pathlib import Path; sys.path.insert(0, sys.argv[1]); import cloud_connections as c; "
    "r = Path(sys.argv[2]); c.RCLONE = sys.argv[3]; c.CONFIG = r / 'rclone/rclone.conf'; "
    "c.ACTIVE = r / 'rclone/active-connection'; c.LOCK = r / 'run/cloud_sync.lock'; c.SYSTEM = r / 'system.cfg'; "
    "c.save('qa', 'local', [('nounc', 'true')])")
child = subprocess.Popen([sys.executable, "-I", "-B", "-c", child_code, str(SRC), str(root), str(stub)],
                         stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
staged = False
for _ in range(100):
    if any(n.startswith(".connection-") for n in left(root)):
        staged = True
        break
    time.sleep(0.1)
os.kill(child.pid, signal.SIGKILL); child.wait()
pidf = Path(str(stub) + ".pid")
if pidf.exists():
    try:
        os.kill(int(pidf.read_text().strip()), signal.SIGKILL)
    except (ProcessLookupError, ValueError):
        pass
after_kill = left(root)
res["sigkill"] = any(n.startswith(".connection-") for n in after_kill)
print(f"sigkill: staging seen before the kill: {'yes' if staged else 'no'}; left after SIGKILL: {after_kill}")

# sweep: plant an earlier save's leftovers, then save.
root = Path(tempfile.mkdtemp(prefix="t17-optkey-sweep-", dir=os.environ.get("TMPDIR")))
point(root)
(root / "rclone").mkdir(parents=True)
(root / "rclone/.connection-old").mkdir(mode=0o700)
(root / "rclone/.connection-old/rclone.conf").write_text("[old]\ntype = local\n")
(root / "rclone/.rclone.conf-old").write_text("[old]\ntype = local\n")
(root / "rclone/.active-connection-old").write_text("old\n")
(root / "rclone/.keep-me").write_text("not a leftover of a save\n")
try:
    c.save("qa", "local", [("nounc", "true")])
    outcome = "saved"
except c.Refused as exc:
    outcome = "refused: " + str(exc)
after = left(root)
res["sweep"] = (outcome == "saved", [n for n in after if n != ".keep-me"], ".keep-me" in after)
print(f"sweep: save() {outcome}; left beside rclone.conf: {after}")

want = {"unfixed": {"control": (True, True, False, False), "config": (False, False, True, False),
                    "dash-key": (True, True, False, True), "sigkill": True,
                    "sweep": (True, [".active-connection-old", ".connection-old", ".rclone.conf-old"], True)},
        "fixed": {"control": (True, True, False, False), "config": (False, False, False, False),
                  "dash-key": (False, False, False, False), "sigkill": True,
                  "sweep": (True, [], True)}}
if a.expect:
    bad = [f"{k}={res[k]}" for k, v in want[a.expect].items() if res[k] != v]
    if bad:
        print(f"t17-option-key-fixture: UNEXPECTED on {a.expect}: " + ", ".join(bad))
        sys.exit(1)
    print(f"t17-option-key-fixture: {a.expect}-expectation-met")

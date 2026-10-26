#!/usr/bin/env python3
"""T17 (#664), stage C: does an option-shaped key reach rclone as a flag? (Astra's A-45)

    python3 -I -B docs/audits/2026_10_26-epic-m6-cloud-setup-content/tools/t17-option-key-fixture.py [--rclone <path>]

The product's own cloud_remote argv parsing (its `key=value` split, read from
the file) and cloud_connections.save(), with CONFIG, ACTIVE, LOCK and SYSTEM
pointed into a scratch directory and RCLONE at the M6 donor's rclone 1.75.2.
The backend is `local`: no network. Three cases, each on a fresh scratch root:

  control   settings [("nounc", "true")]: saved into rclone.conf
  config    settings [("--config", <scratch>/elsewhere.conf)]: where does the section land?
  dash-key  settings [("--log-file", <scratch>/flag.log)]: is a second flag honoured?

Prints, per case: save()'s outcome, whether rclone.conf holds the section,
and whether the outside file exists and holds the section. Writes only under
a temporary directory. No value here is a credential.
"""
from pathlib import Path
import argparse, configparser, os, sys, tempfile

ap = argparse.ArgumentParser()
ap.add_argument("--rclone", default="/workspace/artifacts/m6-donor/1a0266484423/image/system/usr/bin/rclone")
a = ap.parse_args()
SRC = Path("projects/ROCKNIX/packages/network/rclone/sources").resolve()
sys.path.insert(0, str(SRC))
import cloud_connections as c

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


for case in ("control", "config", "dash-key"):
    root = Path(tempfile.mkdtemp(prefix=f"t17-optkey-{case}-", dir=os.environ.get("TMPDIR")))
    c.RCLONE = a.rclone
    c.CONFIG = root / "rclone/rclone.conf"; c.ACTIVE = root / "rclone/active-connection"
    c.LOCK = root / "run/cloud_sync.lock"; c.SYSTEM = root / "system.cfg"
    outside = root / "elsewhere.conf"; flaglog = root / "flag.log"
    argv = {"control": ["nounc=true"],
            "config": ["nounc=true", f"--config={outside}"],
            "dash-key": ["nounc=true", f"--log-file={flaglog}"]}[case]
    try:
        c.save("qa", "local", split(argv))
        outcome = "saved"
    except c.Refused as exc:
        outcome = "refused: " + str(exc)
    print(f"{case}: save() {outcome}; rclone.conf {has(c.CONFIG, 'qa')}; "
          f"outside conf {has(outside, 'qa')}; flag.log {'exists' if flaglog.exists() else 'absent'}; "
          f"staging left {sorted(p.name for p in c.CONFIG.parent.glob('.connection-*')) if c.CONFIG.parent.exists() else []}")

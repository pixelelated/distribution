#!/usr/bin/env python3
"""T17 (#664), stage E, S5 (#1132): does `cloud_content_restore --set-systems`
install a selection whose write failed part-way?

    python3 -I -B docs/audits/2026_10_26-epic-m6-cloud-setup-content/tools/t17-selection-fixture.py \
        [--sources <dir holding cloud_content_restore and cloud_content_transfer>] [--busybox <busybox>] [--expect unfixed|fixed]

The real cloud_content_restore runs under bash with the M6 donor's busybox
applets first on PATH, its absolute paths rewritten into a scratch root as
tools/t17-content-fixture.py does; cloud_remote and cloud_scan are stubs, and
no rclone runs (--set-systems calls none). The device's selection holds
`snes` before each case.

  full-card  300 well-formed names (about 3 KB), written under `ulimit -f 1`
             with SIGXFSZ ignored: the write fails with EFBIG once its first
             kilobyte is down. The substitute, named: a file-size limit in
             place of a full card's ENOSPC; both end the same printf part-way.
  control    the same 300 names with no limit: all installed

--expect unfixed asserts what the file at 8ebaf8daad does (a partial selection
installed); --expect fixed what the fix must do (the old selection byte for
byte, no temp file left, a log line). Writes only under a temporary directory.
"""
from pathlib import Path
import argparse, os, re, subprocess, sys, tempfile

ap = argparse.ArgumentParser()
ap.add_argument("--sources", type=Path, default=Path("projects/ROCKNIX/packages/network/rclone/sources"))
ap.add_argument("--busybox", type=Path,
                default=Path("/workspace/artifacts/m6-donor/1a0266484423/image/system/usr/bin/busybox"))
ap.add_argument("--expect", choices=["unfixed", "fixed"])
a = ap.parse_args()
BB = a.busybox.resolve()
NAMES = ["system%03d" % i for i in range(300)]
print(f"sources: {a.sources}; applets: {BB}")


def make():
    t = Path(tempfile.mkdtemp(prefix="t17-selection-", dir=os.environ.get("TMPDIR")))
    root = t / "root"; tmp = t / "tmp"; tmp.mkdir()
    for d in ("storage/.config/rclone", "storage/roms/snes", "storage/.cache/cloud_sync", "var/log", "run"):
        (root / d).mkdir(parents=True)
    (root / "storage/.config/rclone/rclone.conf").write_text("[qa]\ntype = local\n")
    (root / "storage/.config/cloud_sync.conf").write_text('CONTENT_REMOTE="/pixelelated/Content"\n')
    (root / "storage/.cache/cloud_sync/content-systems").write_text("snes\n")
    bins = t / "bin"; bins.mkdir()
    for applet in subprocess.run([str(BB), "--list"], capture_output=True, text=True, check=True).stdout.split():
        os.symlink(BB, bins / applet)
    scripts = t / "scripts"; scripts.mkdir()
    (scripts / "cloud_scan").write_text('#!/bin/bash\n[ "$1" = --context ] && echo ' + "0" * 64 + '\n')
    (scripts / "cloud_remote").write_text('#!/bin/bash\ncase "$1" in active) echo "qa:" ;; esac\n')
    for name in ("cloud_content_restore", "cloud_content_transfer"):
        s = (a.sources / name).read_text()
        s = s.replace(". /etc/profile\n", ": profile not sourced in the fixture\n")
        s = s.replace("/var/log/cloud_sync.log", str(root / "var/log/cloud_sync.log"))
        s = s.replace("/var/run/cloud_sync.lock", str(root / "run/cloud_sync.lock"))
        s = s.replace("/storage/", str(root / "storage") + "/").replace('"/storage"', '"' + str(root / "storage") + '"')
        s = re.sub(r'(?<![\w/])/tmp/', str(tmp) + "/", s)
        (scripts / name).write_text(s)
    for f in scripts.iterdir():
        f.chmod(0o755)
    env = {"PATH": f"{bins}:/usr/bin:/bin", "TMPDIR": str(tmp), "HOME": str(t)}
    return root, scripts, env


res = {}
for case, limit in (("full-card", True), ("control", False)):
    root, scripts, env = make()
    sel = root / "storage/.cache/cloud_sync/content-systems"
    before = sel.read_bytes()
    cmd = f'exec bash "{scripts / "cloud_content_restore"}" --set-systems "$@"'
    if limit:
        cmd = 'trap "" XFSZ; ulimit -f 1; ' + cmd
    r = subprocess.run(["bash", "-c", cmd, "_"] + NAMES, capture_output=True, text=True, env=env, timeout=120)
    after = sel.read_bytes() if sel.exists() else b""
    lines = after.decode().splitlines()
    temps = sorted(p.name for p in sel.parent.iterdir() if ".tmp." in p.name)
    logf = root / "var/log/cloud_sync.log"
    logged = [l for l in (logf.read_text().splitlines() if logf.exists() else []) if "set-systems" in l]
    ok_line = next((l for l in r.stdout.splitlines() if l.startswith("OK ")), "")
    state = "old" if after == before else ("all" if lines == NAMES else f"partial ({len(lines)} of {len(NAMES)} names)")
    res[case] = (state, bool(temps), bool(logged))
    print(f"{case}: rc {r.returncode}; {ok_line or 'no OK line'}; the selection now: {state}; "
          f"temp left: {temps or 'none'}; set-systems log lines: {len(logged)}"
          + (f" ({logged[-1].split(']', 2)[-1].strip()[:120]})" if logged else ""))

want = {"unfixed": {"full-card": ("partial", False, False), "control": ("all", False, False)},
        "fixed": {"full-card": ("old", False, True), "control": ("all", False, False)}}
if a.expect:
    bad = []
    for k, v in want[a.expect].items():
        got = res[k]
        if (got[0].split(" ")[0], got[1], got[2]) != v:
            bad.append(f"{k}={got}")
    if bad:
        print(f"t17-selection-fixture: UNEXPECTED on {a.expect}: " + ", ".join(bad))
        sys.exit(1)
    print(f"t17-selection-fixture: {a.expect}-expectation-met")

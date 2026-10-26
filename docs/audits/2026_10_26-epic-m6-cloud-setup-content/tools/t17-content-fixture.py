#!/usr/bin/env python3
"""T17 (#664): what the content scripts hand rclone from their arguments and
from cloud_sync.conf.

    python3 -I -B docs/audits/2026_10_26-epic-m6-cloud-setup-content/tools/t17-content-fixture.py \
        [--sources <dir holding the scripts>] [--busybox <busybox>] [--expect unfixed|fixed]
        [--real-rclone <rclone>] [--only backup|match]

The real cloud_content_backup, cloud_content_restore and cloud_content_transfer
run under bash with the M6 donor's busybox applets first on PATH. Their
absolute paths are rewritten into a scratch root (/storage, /var/log, /var/run,
/tmp, and `. /etc/profile` dropped); nothing else in them changes. Their
siblings cloud_scan and cloud_remote are stubs (a fixed context digest; an
active remote `qa:`), and `rclone` is a stub that records every argv and
answers the listings a match needs. No network, no real cloud; the stub's
answers are named in each case.

Cases:
  backup-traversal  cloud_content_backup '../.config': does a copy reach
                    rclone with a source outside /storage/roms?
  backup-control    cloud_content_backup snes: the harness copies a system
  match-netopts     cloud_sync.conf RCLONE_NET_OPTS="... --delete-excluded";
                    cloud_content_restore --match, then --match --apply: does
                    the flag reach the deleting sync?
  match-control     the same with the shipped bound: it does not
  match-netopts-real, match-control-real (with --real-rclone): the same two
                    with a real rclone and a local-backend "cloud" under the
                    scratch root -- the cloud holds snes/a.zip; the device
                    holds a.zip, b.zip (not in the cloud) and a.srm (a save
                    beside the ROM). Which files does the apply delete?
  match-include-real (stage E, S2; Argon's R-9): RCLONE_NET_OPTS carrying
                    --include=* ahead of the save excludes, no
                    --delete-excluded. rclone warns that the order of
                    --include and --exclude is indeterminate, and goes on.
  For the -real cases (stage E, S2) the deleting sync's argv is read: does the
  allowed --timeout 5s reach it (the control), does the offending flag, and
  does cloud_sync.log name a dropped flag by its name alone?

--expect unfixed asserts what the files at 8ebaf8daad do; --expect fixed what
a fix must do (the traversal refused before any rclone call; the deleting
sync never carries --delete-excluded, the save is kept in both -real cases,
--timeout 5s still arrives, and the log names what it dropped). --only runs one
group (backup for S3, match for S2). Writes only under a temporary directory.
"""
from pathlib import Path
import argparse, os, re, subprocess, sys, tempfile

ap = argparse.ArgumentParser()
ap.add_argument("--sources", type=Path, default=Path("projects/ROCKNIX/packages/network/rclone/sources"))
ap.add_argument("--busybox", type=Path,
                default=Path("/workspace/artifacts/m6-donor/1a0266484423/image/system/usr/bin/busybox"))
ap.add_argument("--expect", choices=["unfixed", "fixed"])
ap.add_argument("--real-rclone", type=Path, help="a real rclone for the -real cases (M6's donor copy)")
ap.add_argument("--only", choices=["backup", "match"])
a = ap.parse_args()
BB = a.busybox.resolve()
print(f"sources: {a.sources}; applets: {BB}")

STUB_RCLONE = r'''#!/bin/bash
# Records argv (unit-separated), answers what the content scripts ask.
{ printf '%s\037' "$@"; echo; } >> "$QA_ROOT/calls"
verb=""; for x in "$@"; do case "$x" in -*) ;; *) verb="$x"; break ;; esac; done
last=""; for x in "$@"; do case "$x" in qa:*|/*) last="$x" ;; esac; done
case "$verb" in
  lsf)
    case " $* " in
      *" --dirs-only "*) case "$last" in */ROMs/) echo "snes/" ;; esac ;;
      *" -R "*) ;;
      *) case "$last" in qa:*/ROMs/snes) echo "a.zip" ;; esac ;;
    esac ;;
  sync) case " $* " in *" --dry-run "*) echo "NOTICE: b.zip: Skipped delete as --dry-run is set (size 5)" ;; esac ;;
  size) printf 'Total objects: 0\nTotal size: 0 B (0 Byte)\n' ;;
esac
exit 0
'''


def make(conf_netopts, real=None):
    t = Path(tempfile.mkdtemp(prefix="t17-content-", dir=os.environ.get("TMPDIR")))
    root = t / "root"; tmp = t / "tmp"; tmp.mkdir()
    cloud = t / "cloud"
    for d in ("storage/.config/rclone", "storage/roms/snes", "storage/.cache/cloud_sync", "var/log", "run"):
        (root / d).mkdir(parents=True)
    (root / "storage/.config/rclone/rclone.conf").write_text("[qa]\ntype = local\n")
    conf = 'CONTENT_REMOTE="/pixelelated/Content"\n' if real is None else f'CONTENT_REMOTE="{cloud}"\n'
    if real is not None:
        (cloud / "ROMs/snes").mkdir(parents=True)
        (cloud / "ROMs/snes/a.zip").write_text("rom\n")
    if conf_netopts is not None:
        conf += f'RCLONE_NET_OPTS="{conf_netopts}"\n'
    (root / "storage/.config/cloud_sync.conf").write_text(conf)
    (root / "storage/roms/snes/a.zip").write_text("rom\n")
    (root / "storage/roms/snes/b.zip").write_text("rom the cloud does not have\n")
    (root / "storage/roms/snes/a.srm").write_text("save beside the rom\n")
    (root / "storage/.config/x.cfg").write_text("a config file\n")
    (root / "storage/.cache/cloud_sync/content-systems").write_text("snes\n")
    bins = t / "bin"; bins.mkdir()
    for applet in subprocess.run([str(BB), "--list"], capture_output=True, text=True, check=True).stdout.split():
        if applet not in ("rclone",):
            os.symlink(BB, bins / applet)
    stubs = t / "stubs"; stubs.mkdir()
    if real is None:
        (stubs / "rclone").write_text(STUB_RCLONE)
    else:
        (stubs / "rclone").write_text('#!/bin/bash\n{ printf "%s\\037" "$@"; echo; } >> "$QA_ROOT/calls"\nexec ' + str(real) + ' "$@"\n')
    (stubs / "rclone").chmod(0o755)
    scripts = t / "scripts"; scripts.mkdir()
    (scripts / "cloud_scan").write_text('#!/bin/bash\n[ "$1" = --context ] && echo ' + "0" * 64 + '\n')
    (scripts / "cloud_remote").write_text('#!/bin/bash\ncase "$1" in active) echo "qa:" ;; selection-reason) echo "YOUR CLOUD STORAGE ISN\'T SET UP YET" ;; esac\n')
    for name in ("cloud_content_backup", "cloud_content_restore", "cloud_content_transfer"):
        s = (a.sources / name).read_text()
        s = s.replace(". /etc/profile\n", ": profile not sourced in the fixture\n")
        s = s.replace("/var/log/cloud_sync.log", str(root / "var/log/cloud_sync.log"))
        s = s.replace("/var/run/cloud_sync.lock", str(root / "run/cloud_sync.lock"))
        s = s.replace("/storage/", str(root / "storage") + "/").replace('"/storage"', '"' + str(root / "storage") + '"')
        s = re.sub(r'(?<![\w/])/tmp/', str(tmp) + "/", s)
        (scripts / name).write_text(s)
    for f in scripts.iterdir():
        f.chmod(0o755)
    env = {"PATH": f"{stubs}:{bins}:/usr/bin:/bin", "QA_ROOT": str(root), "TMPDIR": str(tmp),
           "CEILING_DIR_ROOT": str(root / "run"), "HOME": str(t),
           "RCLONE_CONFIG": str(root / "storage/.config/rclone/rclone.conf")}
    return t, root, scripts, env


def calls(root):
    p = root / "calls"
    return [l.rstrip("\037").split("\037") for l in p.read_text().splitlines()] if p.exists() else []


def run(scripts, env, *args):
    return subprocess.run(["bash", str(scripts / args[0])] + list(args[1:]), capture_output=True, text=True,
                          env=env, timeout=120)


res = {}
NETOPTS = "--contimeout 15s --timeout 5s --low-level-retries 10 --retries 1"
for name, dirs in (() if a.only == "match" else (("backup-traversal", ["../.config"]), ("backup-control", ["snes"]))):
    t, root, scripts, env = make(None)
    r = run(scripts, env, "cloud_content_backup", *dirs)
    copies = [c for c in calls(root) if "copy" in c]
    sources = [next((x for x in c if x.startswith("/")), "") for c in copies]
    outside = any("/roms/../" in s or not s.startswith(str(root / "storage/roms")) for s in sources)
    res[name] = (r.returncode, bool(copies), outside)
    shown = [s.replace(str(root), "<root>") for s in sources]
    print(f"{name}: rc {r.returncode}; rclone copy calls {len(copies)}; sources {shown}; "
          f"a source outside /storage/roms: {'yes' if outside else 'no'}")

for name, netopts in (() if a.only == "backup" else (("match-netopts", NETOPTS + " --delete-excluded"), ("match-control", None))):
    t, root, scripts, env = make(netopts)
    p = run(scripts, env, "cloud_content_restore", "--match")
    plan = (root / "storage/.cache/cloud_sync/content-match-plan")
    planned = plan.read_text().splitlines()[1:] if plan.exists() else []
    ap_ = run(scripts, env, "cloud_content_restore", "--match", "--apply")
    deleting = [c for c in calls(root) if "sync" in c and "--dry-run" not in c]
    flag = any("--delete-excluded" in c for c in deleting)
    maxdel = [c[c.index("--max-delete") + 1] for c in deleting if "--max-delete" in c]
    res[name] = (p.returncode, ap_.returncode, len(deleting), flag)
    print(f"{name}: preview rc {p.returncode}, plan {planned}; apply rc {ap_.returncode}; deleting syncs {len(deleting)}, "
          f"--max-delete {maxdel}; --delete-excluded on the deleting sync: {'yes' if flag else 'no'}")

if a.real_rclone and a.only != "backup":
    print(f"real rclone: {a.real_rclone} {subprocess.run([str(a.real_rclone), 'version'], capture_output=True, text=True).stdout.splitlines()[0]}")
    for name, netopts, bad in (("match-netopts-real", NETOPTS + " --delete-excluded", "--delete-excluded"),
                               ("match-include-real", NETOPTS + " --include=*", "--include"),
                               ("match-control-real", None, None)):
        t, root, scripts, env = make(netopts, real=a.real_rclone.resolve())
        p = run(scripts, env, "cloud_content_restore", "--match")
        plan = (root / "storage/.cache/cloud_sync/content-match-plan")
        planned = plan.read_text().splitlines()[1:] if plan.exists() else []
        ap_ = run(scripts, env, "cloud_content_restore", "--match", "--apply")
        left = sorted(x.name for x in (root / "storage/roms/snes").iterdir()) if (root / "storage/roms/snes").exists() else []
        res[name] = ("a.srm" in left, "b.zip" in left)
        deleting = [c for c in calls(root) if "sync" in c and "--dry-run" not in c]
        timeout = any("--timeout" in c and c[c.index("--timeout") + 1] == "5s" for c in deleting)
        carried = bool(bad) and any(x == bad or x.startswith(bad + "=") for c in deleting for x in c)
        logf = root / "var/log/cloud_sync.log"
        log = logf.read_text() if logf.exists() else ""
        dropped = [l for l in log.splitlines() if "RCLONE_NET_OPTS" in l and "allowlist" in l]
        named = "none" if not dropped else ("named" if bad and bad in dropped[0] and (bad + "=") not in dropped[0] else "other")
        if netopts is not None:
            res[name + ":argv"] = (timeout, carried)
            res[name + ":log"] = named
        print(f"{name}: preview rc {p.returncode}, plan {planned}; apply rc {ap_.returncode}; "
              f"left on the device in roms/snes: {left}; the save a.srm kept: {'yes' if 'a.srm' in left else 'NO'}; "
              f"deleting sync: --timeout 5s {'yes' if timeout else 'no'}, {bad or 'no flag'} {'carried' if carried else 'not carried'}; "
              f"drop logged: {named}" + (f" ({dropped[0].split(']', 1)[-1].strip()[:140]})" if dropped else ""))

want = {"unfixed": {"backup-traversal": (0, True, True), "backup-control": (0, True, False),
                    "match-netopts": (0, 0, 1, True), "match-control": (0, 0, 1, False),
                    "match-netopts-real": (False, False), "match-control-real": (True, False),
                    "match-include-real": (False, False),
                    "match-netopts-real:argv": (True, True), "match-include-real:argv": (True, True),
                    "match-netopts-real:log": "none", "match-include-real:log": "none"},
        "fixed": {"backup-traversal": "refused", "backup-control": (0, True, False),
                  "match-netopts": "no-flag", "match-control": (0, 0, 1, False),
                  "match-netopts-real": (True, False), "match-control-real": (True, False),
                  "match-include-real": (True, False),
                  "match-netopts-real:argv": (True, False), "match-include-real:argv": (True, False),
                  "match-netopts-real:log": "named", "match-include-real:log": "named"}}
if a.expect:
    w = want[a.expect]; bad = []
    for k, v in w.items():
        if k not in res:
            continue
        got = res[k]
        if v == "refused":
            ok = got[0] != 0 and not got[1]
        elif v == "no-flag":
            ok = not got[3]
        else:
            ok = got == v
        if not ok:
            bad.append(f"{k}={got}")
    if bad:
        print(f"t17-content-fixture: UNEXPECTED on {a.expect}: " + ", ".join(bad)); sys.exit(1)
    print(f"t17-content-fixture: {a.expect}-expectation-met")

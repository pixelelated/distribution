#!/usr/bin/env python3
"""T21 (#668) stage B: the interface's writers killed at every step (D-CLOUD-078).

    python3 -I -B kill-writer.py <state-fixture> <killer.so> <scratch dir>

Three writers, each run once to count its file-system calls, then once per
call with SIGKILL before that call:

  A  AtomicFile::writeText over an existing private file (both stores' primitive)
  B  Settings::saveFile's two writes in its order (live, then its record)
  C  SystemConf::set + saveSystemConf (the settings lock, the merge, the record)

After each kill: the live file must be the old text or the new text, whole;
the record must be the old record, the old live text (a SystemConf load records
the file it has just read, by design: SystemConf.cpp:232-238), or the new text;
and AtomicFile::chooseConfig
must name a whole source. Leftover temporaries are counted (what a kill
leaves behind). Exit 0 when every kill point keeps the invariant, 1 otherwise.
Writes only under <scratch dir>.
"""
import os, re, shutil, subprocess, sys
from pathlib import Path

fixture, killer, scratch = sys.argv[1], sys.argv[2], Path(sys.argv[3])
OLD = b"system.hostname=qa\nqa.k=old\nqa.keep=kept\n"
REC = b"system.hostname=qa\nqa.k=record\nqa.keep=kept\n"
NEW_TEXT = b"system.hostname=qa\nqa.k=new\nqa.keep=kept\n"
fail = 0

def run(args, kill_at=None):
    env = {"PATH": "/usr/bin:/bin", "LD_PRELOAD": killer}
    if kill_at:
        env["KILL_AT"] = str(kill_at)
    return subprocess.run([fixture] + args, env=env, capture_output=True, text=True, timeout=20)

def ops_of(r):
    m = re.search(r"ops=(\d+)", r.stderr)
    return int(m.group(1)) if m else None

def fresh(case, n):
    d = scratch / f"{case}-{n:03d}"
    if d.exists():
        shutil.rmtree(d)
    d.mkdir(parents=True)
    live = d / "system.cfg"
    live.write_bytes(OLD); live.chmod(0o600)
    rec = d / "system.cfg.backup"
    rec.write_bytes(REC); rec.chmod(0o600)
    (d / "new.txt").write_bytes(NEW_TEXT)
    (d / "value.txt").write_bytes(b"new")
    return d, live, rec

def args_for(case, d, live):
    if case == "A":
        return ["write", str(live), str(d / "new.txt")]
    if case == "B":
        return ["settings-shape", str(live), str(d / "new.txt")]
    return ["set", str(live), str(d / ".system.cfg.lock"), "qa.k", str(d / "value.txt")]

for case, label in (("A", "AtomicFile::writeText"), ("B", "Settings::saveFile's two writes"), ("C", "SystemConf::set + saveSystemConf")):
    d, live, rec = fresh(case, 0)
    clean = run(args_for(case, d, live))
    total = ops_of(clean)
    new_live = live.read_bytes()
    print(f"== {case} {label}: unkilled rc {clean.returncode}, {total} calls; live after = {'new' if new_live != OLD else 'old'}")
    bad = 0
    for n in range(1, (total or 0) + 1):
        d, live, rec = fresh(case, n)
        r = run(args_for(case, d, live), kill_at=n)
        killed = r.returncode == -9
        lb, rb = live.read_bytes() if live.exists() else None, rec.read_bytes() if rec.exists() else None
        live_ok = lb in (OLD, new_live)
        rec_ok = rb in (REC, OLD, new_live)
        ch = run(["choose", str(live)]).stdout.strip()
        whole = ch.startswith("source=Live") or ch.startswith("source=Temporary") or ch.startswith("source=Backup")
        temps = sorted(p.name for p in d.iterdir() if ".tmp" in p.name or ".new." in p.name)
        state = ("old" if lb == OLD else "new" if lb == new_live else "OTHER") + "/" + ("record" if rb == REC else "old" if rb == OLD else "new" if rb == new_live else "OTHER")
        ok = live_ok and rec_ok and whole
        bad += 0 if ok else 1
        print(f"  kill before call {n:2d}: {'killed' if killed else 'ran to end'}; live/record {state}; next load {ch}; left behind {len(temps)}{' ' + ','.join(temps) if temps else ''}; {'ok' if ok else 'FAIL'}")
    print(f"  {case}: {total} kill points, {bad} broke the invariant")
    fail |= bad > 0

print("== result:", "PASS (every kill left the old or the new state whole)" if not fail else "FAIL")
sys.exit(1 if fail else 0)

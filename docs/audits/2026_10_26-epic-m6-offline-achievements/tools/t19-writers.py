"""T19 (#666): 02 § The writers, generated from the four scripts and the unit
at 8ebaf8daad (the brief's § 6 and § 7: one row per writing statement, the
generator asserting its row count and exiting 1 on drift).

    python3 -I -B docs/audits/2026_10_26-epic-m6-offline-achievements/tools/t19-writers.py [<rev>]

A writing statement is a line (comments excluded) that redirects into a file,
moves, touches, removes or makes a directory, opens a lock read-write, sets a
system.cfg key, makes a fifo or a temporary, or (python) writes, replaces,
unlinks or makes a directory. Each hit is mapped to its target by the first
TARGETS pattern its text matches, and to the lock it runs under by the shell
function that encloses it. A hit no pattern maps, a TARGETS row no hit uses,
or a count other than EXPECTED exits 1. The mode column is the same for
every row: no script sets one (no umask, chmod or chown in the four, no
UMask= in the unit), so each file ends with its writer's umask -- the
service's under systemd, the ctl's caller's (EmulationStation's when a page
runs it) -- which the guest window reads back.
"""
import re, subprocess, sys

REV = sys.argv[1] if len(sys.argv) > 1 else "8ebaf8daad"
P = "projects/ROCKNIX/packages/network/raofflineproxy"
FILES = ["sources/raofflineproxy-ctl", "sources/raofflineproxy-refresh", "sources/raofflineproxy-cache-images",
         "sources/raofflineproxy-cache-indexed", "system.d/raofflineproxy.service"]
EXPECTED = 77
WRITE = re.compile(r"""(^|[^0-9&<>-])>>?[ \t]*"?\$\{?[A-Za-z_]|(^|[^0-9&<>-])>>?[ \t]*"[^"&]*"|\bmv -f\b|\btouch\b|\brm -f\b|\brm -rf\b|\bmkdir -p\b|^\s*:\s*>|\bset_setting\b|write_text\(|write_bytes\(|os\.replace\(|\.unlink\(|\.mkdir\(|mkfifo|mktemp|<>"|>&9""")

# (pattern over the statement, target, how it writes, reader)
TARGETS = [
    (r"trap 'rm -f", "the run's temporaries (the job list, the fifo, the ready sets, `scan-cursor.next`, `running`)", "the EXIT trap's `rm -f`", "(cleanup: nothing reads them after)"),
    (r"set_setting", "`system.cfg` (`global.retroachievements.offlineproxy`, `.hardcore`, `.offlineproxy.hardcore_was`)", "`set_setting` from `/etc/profile`, each value read back before the next", "`setsettings.sh`, `cheevos_ppsspp.sh`, `daemons/006` at boot, EmulationStation's SystemConf"),
    (r"MARKER_DIR", "`/storage/.cache/services/`", "`mkdir -p`", "the unit's `ConditionPathExists`"),
    (r"\$\{MARKER\}", "`/storage/.cache/services/raofflineproxy.conf` (the marker)", "direct (`touch`, `rm -f`)", "the unit's `ConditionPathExists`; `099-networkservices` rewrites it at boot"),
    (r"FLUSH_STAMP|\$\{MINE\}", "`last-flush` (the service's, patch 003)", "taken by rename to `.$$`, read, removed", "the ctl's `flushed`, for `OfflineAchievements.cpp:119`"),
    (r"\$\{RUNNING\}", "`running`", "temp + rename (`mark_running`); removed at the end and by `take_lock`", "EmulationStation (a run it did not start, bound 900 s)"),
    (r"SCAN_LOG", "`scan.log` (and `scan.log.1`)", "append; rotated once past 1,048,576 B in `slog` only -- the helpers' stderr appends bypass the check", "a person, over a shell"),
    (r'^\s*:\s*>\s*"\$1"|> "\$1" 2>/dev/null', "the ready-set file `$1` (`/tmp/raofflineproxy-ready.*`)", "direct (truncate, then the python's stdout)", "`games_made_ready`"),
    (r"PROXY_DIR", "`/storage/.config/raofflineproxy/`", "`mkdir -p`", "the service, the helpers, the ctl"),
    (r"SCAN_STAMP", "`last-scan`", "temp + rename (`write_stamp`); its status ignored by every caller", "`CloudText::parseScanStamp`"),
    (r"SCAN_CURSOR|tmp\.write_text\(value|os\.replace\(tmp, proposal\)|tmp\.unlink\(\)", "`scan-cursor` (and `.next`, `.next.tmp`)", "temp + `os.replace` (python), then `mv -f` with a read-back (`commit_cursor`)", "the next listing"),
    (r"SCRATCH", "`/tmp/raofflineproxy-probe.*` (the probe's own `online_state.json`)", "`mktemp -d`, removed by `rm -rf`", "`is_online`"),
    (r"out\.write_text", "the job list (`$1` of `list_jobs`, `/tmp/raofflineproxy-{scan,topup}.*`)", "direct, strict UTF-8", "`raofflineproxy-cache-indexed`"),
    (r"JOBS_FIFO", "`/tmp/raofflineproxy-scan-out.*` (a fifo)", "`mktemp -u` then `mkfifo` (a name, then the object)", "`run_jobs`, fd 8"),
    (r"READY_BEFORE|READY_AFTER", "`/tmp/raofflineproxy-ready.*`", "`mktemp`; removed at the end and by the EXIT trap", "`games_made_ready`"),
    (r"\$\{LIST\}|LIST=", "`/tmp/raofflineproxy-{scan,topup}.*` (the job list)", "`mktemp`; removed by the EXIT trap", "`raofflineproxy-cache-indexed`"),
    (r"SC_OUT", "`/tmp/raofflineproxy-topup-sc.*`", "`mktemp`, stdout of `run-smart-cache`; removed", "`do_topup` (its last `\"type\":\"result\"` line)"),
    (r"INDEX_PENDING|\$\{mine\}", "`index-pending` (and `.tmp`, `.ack.$$`)", "temp + rename; acknowledged by rename aside", "`do_topup`"),
    (r"TOPUP_MARK", "`last-topup-attempt`", "direct (`touch`, unguarded)", "`do_topup`'s half-hour gate and its `-nt` played check"),
    (r"SCAN_LOCK|>&9", "`/var/run/raofflineproxy-scan.lock`", "opened read-write without truncating (created if absent); the holder's pid written at offset 0", "`stop_running_run`, `RunLock::holder` in EmulationStation"),
    (r"PENDING_LOCK", "`/var/run/raofflineproxy-index-pending.lock`", "opened read-write (created if absent)", "`pending_lock`"),
    (r"CURSOR\.(parent|write_text|unlink)", "`image_cache/verify-cursor`", "direct `write_text` -- the one stamp here without temp and rename", "the next `--verify` pass"),
    (r"ABSENT_FILE|tmp\.write_text\(\"\"\.join", "`image_cache/absent` (and `.tmp`)", "temp + `os.replace`", "the next image pass"),
    (r"target\.unlink", "a damaged cached image under `image_cache/static/`", "unlink", "the fetch that follows in the same pass"),
]

LOCKS = {
    "the scan lock (fd 9, `take_lock`)": {"mark_running", "unmark_running", "slog", "ready_games_into", "write_stamp", "commit_cursor",
                                         "list_jobs", "run_jobs", "cancelled", "run_image_pass", "do_scan", "do_topup", "take_lock", "do_images", "do_refresh"},
    "the index-pending lock (fd 6), best effort": {"write_index_pending", "ack_index_pending", "pending_lock"},
    "none": {"put_back", "enable_undo", "do_enable", "stop_running_run", "do_disable", "do_flushed", "is_online", "do_index_offline"},
}


def src(path):
    r = subprocess.run(["git", "show", f"{REV}:{P}/{path}"], capture_output=True, text=True)
    if r.returncode:
        sys.stderr.write(r.stderr); sys.exit(2)
    return r.stdout.splitlines()


rows, unmapped, used = [], [], set()
for f in FILES:
    lines = src(f)
    func = ""
    for n, text in enumerate(lines, 1):
        m = re.match(r"^([a-z_]+)\(\)\s*\{", text) or (re.match(r"^def ([a-z_]+)\(", text) if not f.endswith("ctl") else None)
        if m:
            func = m.group(1)
        if re.match(r"^\s*#", text) or not WRITE.search(text):
            continue
        hit = None
        for i, (pat, target, how, reader) in enumerate(TARGETS):
            if re.search(pat, text):
                hit = i; break
        if hit is None:
            unmapped.append(f"{f}:{n}: {text.strip()[:100]}"); continue
        used.add(hit)
        _, target, how, reader = TARGETS[hit]
        if f.endswith("ctl"):
            lock = next((k for k, v in LOCKS.items() if func in v), None)
            if lock is None:
                unmapped.append(f"{f}:{n}: function {func!r} has no lock row"); continue
        else:
            lock = "the caller's: the scan lock when the ctl runs it; none by hand"
        rows.append((f"`{f.split('/')[-1]}:{n}`", func or "(top level)", target, how, lock, reader))

print("| Line | Function | File | Writes by | Mode | Lock held | Reader | proved |")
print("| --- | --- | --- | --- | --- | --- | --- | --- |")
for line, func, target, how, lock, reader in rows:
    print(f"| {line} | `{func}` | {target} | {how} | the writer's umask (none set) | {lock} | {reader} | tree |")
problems = []
if unmapped:
    problems.append("unmapped: " + "; ".join(unmapped))
unused = [TARGETS[i][1] for i in range(len(TARGETS)) if i not in used]
if unused:
    problems.append("targets no hit uses: " + "; ".join(unused))
if len(rows) != EXPECTED:
    problems.append(f"rows {len(rows)}, expected {EXPECTED}")
print()
print(f"rows={len(rows)} expected={EXPECTED} targets={len(TARGETS)} rev={REV}" + ("" if not problems else " DRIFT"))
for p in problems:
    print("t19-writers:", p, file=sys.stderr)
sys.exit(1 if problems else 0)

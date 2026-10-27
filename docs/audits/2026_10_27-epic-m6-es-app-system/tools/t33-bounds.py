"""02 § The bounds: every network or script wait reachable from T33's 77 paths (#680, Q2).

    python3 -I t33-bounds.py <es worktree> <commit> <paths.txt> [http=4,process=6,waits=4,bounded=2]

Three kinds of row:
- **http**: an HttpReq constructed (`new HttpReq(` or on the stack), read by
  t33lib with comments and strings skipped. es-core's HttpReq (T21's file,
  cited from T32's bounds: HttpReq.h:45-90, HttpReq.cpp:204-213) sets a
  10 s connect and no total and no stall bound unless the options say so;
  `req.wait()` (HttpReq.cpp:638-644) has no bound of its own.
- **process**: § 5's process-start grep, line for line, comments included
  (`(system|popen)(`, `runSystemCommand(`, `executeScript`).
- **waits**: a wait the grep cannot see, named by L-01, L-02 and L-09 and
  matched by a pattern that must hit exactly one line in its file.
A row is "bounded" when something ends it however the far side behaves: a
total or stall timeout, or a `timeout N` prefix on the command. Win32 rows
are dead (`#if WIN32`, :1-:1267, L-21) and counted apart.
Exits 1 when a construction or start has no row, a row matches nothing, a
wait pattern hits other than once, or a count differs. Rows are keyed by
file and order, so a fix that moves lines keeps them (D-WORKFLOW-210).
"""
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from t33lib import in_comment_or_string, show  # noqa: E402

# (file, kind, order) -> (what waits, on which thread, the bound as written, bounded, lead)
ROWS = {
    ("ZaparooSupport.cpp", "http", 1): ("`isZaparooEnabled`: GET `127.0.0.1:7497/health`, under `mZaparooLock`", "a detached thread (`:22-27`, `checkZaparooEnabledAsync`); and the caller's thread for a direct call (`guis/GuiGameOptions.cpp:59`, `:281`)",
                                        "connect `defaultDelay` (3 s from the async probe, `:38`); no total, no stall", False, "L-09: a service that accepts and never answers holds the probe and `mZaparooLock` forever"),
    ("ZaparooSupport.cpp", "http", 2): ("`writeZaparooCard`: POST `127.0.0.1:7497/api/v0.1`", "the caller's (the game-options page, the interface thread)",
                                        "connect 10 s (the default); no total, no stall", False, "L-09: unbounded after connect; outside the lanes, recorded"),
    ("Win32ApiSystem.cpp", "http", 1): ("bezels.txt (dead)", "--", "dead inside `#if WIN32`", None, "L-21"),
    ("Win32ApiSystem.cpp", "http", 2): ("the update version URL (dead)", "--", "dead inside `#if WIN32`", None, "L-21"),
    ("CloudOffer.cpp", "process", 1): ("`cloud_setup --seed-folders saves`", "`GuiLoading`'s worker; the page waits",
                                       "`timeout 90`", True, "L-18: the bound is sound; rc 0 alone reads DONE"),
    ("Win32ApiSystem.cpp", "process", 1): ("`executeScript(command)` defined (dead)", "--", "dead inside `#if WIN32`", None, "L-21"),
    ("Win32ApiSystem.cpp", "process", 2): ("`executeScript(command, fn)` defined (dead)", "--", "dead inside `#if WIN32`", None, "L-21"),
    ("Win32ApiSystem.cpp", "process", 3): ("`batocera-bluetooth forgetBT` (dead)", "--", "dead inside `#if WIN32`", None, "L-21"),
    ("Win32ApiSystem.h", "process", 1): ("`executeScript` declared (dead with its file)", "--", "a declaration", None, "L-21"),
    ("Win32ApiSystem.h", "process", 2): ("`executeScript` declared (dead with its file)", "--", "a declaration", None, "L-21"),
}
WAITS = [
    ("NetworkThread.cpp", r"WatchersManager::getInstance\(\)->ResetComponent\(sCheevosToken\)", "`checkCheevosTokenSoon` -> es-core's `ResetComponent`, which takes `mWatchersLock` (`WatchersManager.cpp:92-100`)",
     "the interface thread (`guis/GuiRetroAchievementsSettings.cpp:806`, `:257`, `:191`)", "as long as the watcher thread holds `mWatchersLock` across every `check()` (`WatchersManager.cpp:181-196`), each of which may be a network call", False, "L-01: rule 6, es-core's lock (T21's file) put to the pause"),
    ("CaptureRotation.cpp", r"readAllText\(LAUNCH_LOG\)", "the whole `/var/log/exec.log`, read and scanned", "the interface thread, after every RetroArch exit (`FileData.cpp:1166-1167`)",
     "the launcher's truncation (#280): the log is this session's only", True, "L-02: priced by the retro's time-to-play line (G-03's `stat`)"),
    ("CaptureRotation.cpp", r"readAllText\(RETROARCH_CONFIG\)", "`retroarch.cfg`, read and scanned", "the interface thread, after every RetroArch exit",
     "none: the file's size, which nothing bounds (L-02: the launcher's truncation covers only the log)", False, "L-02"),
    ("ZaparooSupport.cpp", r"std::unique_lock<std::mutex> lock\(mZaparooLock\)", "`mZaparooLock` taken by `isZaparooEnabled`", "whichever thread asks second, the game-options page among them",
     "as long as the first holder's request (no total bound above)", False, "L-09"),
]
PROC = re.compile(r"(^|[^A-Za-z_])(system|popen)\(|runSystemCommand\(|executeScript")

tree, commit, paths_file = sys.argv[1:4]
want = dict((k, int(v)) for k, v in (kv.split("=") for kv in sys.argv[4].split(","))) if len(sys.argv) > 4 else {}
found, line_of, fail = [], {}, []
srcs = {}
for path in [l.strip() for l in open(paths_file) if l.strip()]:
    src = show(tree, commit, path)
    f = path.rsplit("/", 1)[1]
    srcs[f] = src
    hits = []
    for pat in (r"\bnew\s+HttpReq\s*\(", r"\bHttpReq\s+[A-Za-z_]\w*\s*\("):
        hits += [m.start() for m in re.finditer(pat, src) if not in_comment_or_string(src, m.start())]
    for n, at in enumerate(sorted(hits), 1):
        found.append((f, "http", n)); line_of[(f, "http", n)] = src.count("\n", 0, at) + 1
    n = 0
    for i, line in enumerate(src.split("\n"), 1):
        if PROC.search(line):
            n += 1
            found.append((f, "process", n)); line_of[(f, "process", n)] = i
fail += ["%s %s %d (line %d) has no row" % (k[0], k[1], k[2], line_of[k]) for k in found if k not in ROWS]
fail += ["a row names %s %s %d, which is not there" % k for k in ROWS if k not in found]
print("| Line | Kind | What waits | Thread | Bound as written | Bounded | Lead |")
print("| --- | --- | --- | --- | --- | --- | --- |")
yes = lambda b: "dead" if b is None else ("yes" if b else "**no**")
for k in sorted(found, key=lambda k: (k[1], k[0], k[2])):
    r = ROWS.get(k, ("?", "?", "?", False, "?"))
    print("| `%s:%d` | %s | %s | %s | %s | %s | %s |" % (k[0], line_of[k], k[1], r[0], r[1], r[2], yes(r[3]), r[4]))
waits = 0
for f, pat, what, thread, bound, b, lead in WAITS:
    hits = [i for i, line in enumerate(srcs.get(f, "").split("\n"), 1) if re.search(pat, line)]
    if len(hits) != 1:
        fail.append("the wait /%s/ hits %d lines in %s" % (pat, len(hits), f))
        continue
    waits += 1
    print("| `%s:%d` | wait | %s | %s | %s | %s | %s |" % (f, hits[0], what, thread, bound, yes(b), lead))
rows = [ROWS[k] for k in found if k in ROWS] + [(0, 0, 0, w[5]) for w in WAITS]
counts = {"http": sum(1 for k in found if k[1] == "http"), "process": sum(1 for k in found if k[1] == "process"), "waits": waits,
          "bounded": sum(1 for r in rows if r[3] is True), "dead": sum(1 for r in rows if r[3] is None)}
live = len(rows) - counts["dead"]
print()
print("generated, asserted: %d http, %d process lines, %d waits; %d live, %d bounded, %d dead (Win32)" % (counts["http"], counts["process"], counts["waits"], live, counts["bounded"], counts["dead"]))
fail += ["%s %d, expected %d" % (k, counts[k], v) for k, v in want.items() if counts.get(k) != v]
if fail:
    print("FAIL t33-bounds: " + "; ".join(fail))
    sys.exit(1)

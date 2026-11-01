#!/usr/bin/env python3
"""T36 (#683) stage B: the generated tables of 02-forward-audit.md, each asserting its counts.

  t36-tables.py --write <02>     rewrite every <!-- gen:NAME --> ... <!-- /gen:NAME --> block in 02
  t36-tables.py --check <02>     exit 1 when a block in 02 differs from what the pin gives now
  t36-tables.py --print NAME     print one table
  --expect NAME=N                override one expected count (the constructed drift: exit 1)

Reads the EmulationStation pin with `git show` only; writes nothing in the ES worktree.
Every table's last line is "generated, asserted: N rows"; an assertion that fails prints
"ASSERT <name>: ..." and the script exits 1 before anything is written.
"""
import argparse, json, os, re, subprocess, sys, collections

W = os.environ.get("T36_ES", "/home/max/Development/emulationstation-next.worktrees/m6-es-core-utils-resources-683")
PIN = "16dbac5211eea7e70db7394372033be2be7df829"
MB, RM, BAT, BATBASE = "cada856d86", "f6c542872e", "b2ceb55a7e", "1750dded8c"
AUD = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ROOT = subprocess.run(["git", "-C", AUD, "rev-parse", "--show-toplevel"], capture_output=True, text=True, check=True).stdout.strip()
FSU = "es-core/src/utils/FileSystemUtil.cpp"

EXPECT = {
    "coverage": 58, "fork-added": 6, "fork-modified": 9, "upstream-carried": 43,
    "inventory-fork-own": 15, "inventory-upstream-carried": 43, "identical-to-rocknix-master": 43,
    "batocera-commits": 13, "batocera-files": 9,
    "leads": 19, "floor": 26,
    "cache-entry-points": 9, "cache-writers": 8, "cache-erasing-lines": 8, "linesets": 17,
    "spawn-lines": 16, "spawn-real": 13, "spawn-linux": 11,
    "write-sites": 18, "write-sites-linux": 10,
    "path-transforms": 22,
}
FAILS = []

def git(*a):
    return subprocess.run(["git", "-C", W, *a], capture_output=True, text=True, check=True).stdout

def show(path, rev=PIN):
    return git("show", f"{rev}:{path}")

def blob(path, rev):
    r = subprocess.run(["git", "-C", W, "rev-parse", "--short", f"{rev}:{path}"], capture_output=True, text=True)
    return r.stdout.strip() if r.returncode == 0 else ""

def check(name, got):
    want = EXPECT[name]
    if got != want:
        FAILS.append(f"ASSERT {name}: expected {want}, the pin gives {got}")

def table(head, rows, name):
    out = ["| " + " | ".join(head) + " |", "| " + " | ".join("---" for _ in head) + " |"]
    out += ["| " + " | ".join(str(c) for c in r) + " |" for r in rows]
    out.append("")
    out.append(f"generated, asserted: {len(rows)} rows (`tools/t36-tables.py --print {name}`)")
    return "\n".join(out)

DEF = re.compile(r'^\s*(?:static\s+|template<[^>]*>\s*)?(?:const\s+)?[A-Za-z_:<>,\*& ]+?[\s\*&]([A-Za-z_~][A-Za-z_0-9:~]*)\s*\([^;]*\)\s*(?:const)?\s*$')

def functions(text):
    """(line, name) of every definition-shaped line, used to name the function around a line."""
    out = []
    for i, l in enumerate(text.split("\n"), 1):
        m = DEF.match(l)
        if m and m.group(1) not in ("if", "while", "for", "switch", "return"):
            out.append((i, m.group(1)))
    return out

def enclosing(defs, line):
    name = "--"
    for i, n in defs:
        if i <= line:
            name = n
        else:
            break
    return name

def win32_lines(text):
    """The set of lines inside a WIN32-only preprocessor branch (the image never builds them)."""
    stack, inwin, out = [], False, set()
    for i, l in enumerate(text.split("\n"), 1):
        s = l.strip()
        if re.match(r'#\s*if', s):
            winish = bool(re.search(r'\b_?WIN32\b', s))
            neg = bool(re.match(r'#\s*ifndef', s)) or "!" in s
            stack.append(("win", not neg) if winish else ("other", False))
        elif re.match(r'#\s*else', s) and stack:
            kind, w = stack[-1]
            stack[-1] = (kind, (not w) if kind == "win" else w)
        elif re.match(r'#\s*endif', s) and stack:
            stack.pop()
        inwin = any(k == "win" and w for k, w in stack)
        if inwin:
            out.add(i)
    return out

def paths58():
    return [l.strip() for l in open(os.path.join(AUD, "stage-a", "paths.txt")) if l.strip()]

# ---------------------------------------------------------------- coverage
SECTIONS = [
    (r'utils/FileSystemUtil\.', "the file cache; the paths; the writes and reads"),
    (r'utils/Platform\.', "the processes; the device reads"),
    (r'utils/StringUtil\.', "the device reads, the renderers and the words (case helpers); the processes (`shellQuote`, `maskSecrets`)"),
    (r'utils/(TimeUtil|TimeText)\.', "the device reads, the renderers and the words"),
    (r'utils/MathExpr\.', "the device reads, the renderers and the words (the `_(` line)"),
    (r'utils/(ZipFile\.|zip_file\.hpp)', "the writes and reads; the structure (reading scope)"),
    (r'utils/han\.h', "the structure (reading scope)"),
    (r'utils/(ThreadPool|StringListLock|ConcurrentVector)\.', "the texture and font caches (threads, L-17); the structure"),
    (r'utils/(OfflineProxyUrl|CommandLineUtil)\.', "the structure (fork files whole)"),
    (r'utils/', "the structure"),
    (r'resources/(Font|TabStops)\.', "the texture and font caches (the font)"),
    (r'resources/', "the texture and font caches"),
    (r'renderers/Renderer_(GL21|GLES10|GLES20)\.', "the structure (no image compiles the body)"),
    (r'renderers/', "the device reads, the renderers and the words; the structure"),
]

def coverage():
    ps = paths58()
    status = {}
    for l in git("diff", "--name-status", MB, PIN, "--", *ps).splitlines():
        st, p = l.split("\t", 1)
        status[p] = {"A": "fork-added", "M": "fork-modified"}.get(st, st)
    inv = json.load(open(os.path.join(ROOT, "docs", "reviews", "inventory.json")))
    cols = inv["columns"]
    invt = {r["path"]: r["tier"] for r in (dict(zip(cols, x)) for x in inv["rows"]) if r["tree"] == "es"}
    bat = collections.Counter()
    for l in git("log", "--format=%h", "--name-only", f"{BATBASE}..{BAT}", "--", *ps).splitlines():
        if l.strip() in ps:
            bat[l.strip()] += 1
    batc = len([c for c in git("log", "--format=%h", f"{BATBASE}..{BAT}", "--", *ps).splitlines() if c.strip()])
    rows, cnt, icnt, ident = [], collections.Counter(), collections.Counter(), 0
    for p in ps:
        lines = show(p).count("\n") + (0 if show(p).endswith("\n") else 1)
        prov = status.get(p, "upstream-carried")
        same = blob(p, PIN) == blob(p, RM) and blob(p, RM) != ""
        ident += same
        cnt[prov] += 1
        icnt[invt.get(p, "absent")] += 1
        sec = next(s for rx, s in SECTIONS if re.search(rx, p))
        rows.append([f"`{p}`", lines, prov, invt.get(p, "absent"), "yes" if same else "no", bat.get(p, 0), sec])
    check("coverage", len(rows))
    check("fork-added", cnt["fork-added"]); check("fork-modified", cnt["fork-modified"]); check("upstream-carried", cnt["upstream-carried"])
    check("inventory-fork-own", icnt["fork-own"]); check("inventory-upstream-carried", icnt["upstream-carried"])
    check("identical-to-rocknix-master", ident)
    check("batocera-commits", batc); check("batocera-files", len(bat))
    t = table(["Path", "Lines (`grep -c ''`)", "Against the merge base `cada856d86`", "Inventory tier", "Blob = ROCKNIX `f6c542872e`",
               "Batocera commits since `1750dded8c`", "Read under (`02` §)"], rows, "coverage")
    return t + (f"\n\nTotals: fork-added {cnt['fork-added']}, fork-modified {cnt['fork-modified']}, upstream-carried {cnt['upstream-carried']};"
                f" inventory fork-own {icnt['fork-own']}, upstream-carried {icnt['upstream-carried']}; {ident} of {len(rows)} blobs identical to ROCKNIX's master;"
                f" batocera {batc} commits on {len(bat)} files since `{BATBASE}`.")

# ---------------------------------------------------------------- the leads
BRIEF = os.path.join(ROOT, "docs", "reviews", "briefs", "es-core-utils-resources.md")
LEADS = {  # id: (family, owner, disposition at stage B)
    "L-01": ("a player sentence", "T36", "case 3.1 at stage C (FAIL at the pin expected); a fix only under a stream brief"),
    "L-02": ("a write's claim", "T20 (#1177, `d9afa5c7c`) -- collision", "control 3.4 at stage C, never re-fixed here; § The merge debt"),
    "L-03": ("a write's claim", "`renameFile`: T21 (#1191, `f7c16144d`) -- collision; `copyFile`: T36", "case 3.2 at stage C; `copyFile`'s half this slice's (rule 6)"),
    "L-04": ("a write's claim", "the pause (#1186, T21 PL-20); call sites their owners'", "text case 3.3; the return or the supersession put to the stage-D pause"),
    "L-05": ("a process's contract", "T36 (ruling (j): T35's PL-03 fix is `Scripting`'s)", "3.5's two host rcs at stage A; G-07 reads `SigIgn` first (errata), then the image's shell and wrapper"),
    "L-06": ("a process's contract", "T26 (#1225, `a5d2d3756`) -- collision", "control 3.9 at stage C, never re-fixed here; § The merge debt"),
    "L-07": ("a layout computed from a moving number", "T36", "case 3.16 at stage C; G-02 and G-06 frames"),
    "L-08": ("a layout computed from a moving number", "the coordinator's rule sweep (erratum against `es-code-traps.md:118`); T34 PL-17 beside it", "positive 3.8 at stage C; recorded as a rule erratum"),
    "L-09": ("a layout computed from a moving number", "T36", "case 3.17 at stage C"),
    "L-10": ("a lifetime or a thread", "T36", "TSan case 3.11 at stage C"),
    "L-11": ("a lifetime or a thread", "T36", "teardown case 3.12 at stage C"),
    "L-12": ("a read of a file another process writes", "T36 (ruling (h): the cache's fix is T36's, T35's 3.11 the case)", "positive 3.13 at stage C; T35's 3.11 re-run at T35's tips (ruling (h) as (a))"),
    "L-13": ("a process's contract", "the coordinator's rule sweep (erratum against `es-native-ui.md:103`); #1220 the callers'", "text case 3.7 at stage C; recorded as a rule erratum"),
    "L-14": ("a player's secret in a log", "T36", "case 3.10 at stage C, its value built at run time"),
    "L-15": ("a lifetime or a thread", "T36", "ASan case 3.6 at stage C"),
    "L-16": ("a write's claim", "T36", "case 3.15 at stage C"),
    "L-17": ("a lifetime or a thread", "T36", "TSan programs 3.25 at stage C; the threads named in § The texture and font caches"),
    "L-18": ("a lifetime or a thread", "T36", "text case 3.24 at stage C (recorded)"),
    "L-19": ("a read of a file another process writes", "T36 (new at stage B)", "case 3.26 at stage C (FAIL at the pin expected); reaches #1263's `TextureData.cpp:336-339`"),
}
FLOOR_STATUS = {
    "3.19": "run at stage C; its output is held (D-WORKFLOW-215), only a neutral line in public",
    "3.20": "run at stage C; its output is held (D-WORKFLOW-215), only a neutral line in public",
    "3.14": "re-run at stage C from T35's tips of that minute, named with the time and T35's stage (ruling (h) as (a)); again at the hand-back",
    "3.5": "run at stage A: `seq 400 rc=0`, `seq 200000 rc=141` on `/usr/bin/dash` (`stage-a/runs.out`); G-07 the image's",
    "3.26": "new at stage B (L-19): `writeAllText(p)`; `exists(p)`; `removeFile(p)`; `CHECK_FALSE(exists(p))` -- FAIL at the pin expected",
}

def leads():
    text = open(BRIEF).read().split("\n")
    lrows, frows = {}, {}
    for l in text:
        m = re.match(r'^\| (L-\d\d) \| ([^|]*) \|', l)
        if m:
            lrows[m.group(1)] = m.group(2).strip()
        m = re.match(r'^\| (?:\*\*)?(3\.\d+)(?:\*\*)? \| ([^|]*) \| ([^|]*) \|', l)
        if m and m.group(1) not in frows:
            frows[m.group(1)] = (m.group(2).strip(), m.group(3).strip())
    lrows["L-19"] = "`utils/FileSystemUtil.cpp:1067`, `:1080`, `:1084` (stage B's read)"
    frows["3.26"] = ("`utils/FileSystemUtil.cpp:1059-1087`", "`removeFile`, linked whole")
    if sorted(lrows) != sorted(LEADS):
        FAILS.append(f"ASSERT leads: the brief's ids {sorted(lrows)} against the dispositions {sorted(LEADS)}")
    check("leads", len(lrows))
    want = [f"3.{i}" for i in range(1, 27)]
    if sorted(frows, key=lambda k: int(k.split('.')[1])) != want:
        FAILS.append(f"ASSERT floor: ids {sorted(frows)}")
    check("floor", len(frows))
    a = [[k, lrows[k], *LEADS[k], "tree"] for k in sorted(lrows)]
    b = [[k, *frows[k], FLOOR_STATUS.get(k, "stage C"), "tool-run"]
         for k in sorted(frows, key=lambda k: int(k.split('.')[1]))]
    return (table(["Lead", "Lines at the pin", "Family", "Owner", "Disposition at stage B", "proved:"], a, "leads") + "\n\n" +
            table(["Case", "At the pin", "Function", "Status", "proved:"], b, "leads"))

# ---------------------------------------------------------------- the file cache
ENTRY = [  # name, pattern of its definition, lock, what it does, its answer to a file another process wrote
    ("FileCache::queryCacheEntry", r'static std::optional<bool> queryCacheEntry\(', "shared, then unique for the insert",
     "a hit answered under the shared lock; a miss stat'ed with no lock (`statKey`) and stored by `insertEntry`",
     "the entry stands until an erase or the reset: a file created, removed or rewritten outside is not seen"),
    ("FileCache::insertEntry", r'static const FileCache& insertEntry\(', "unique (the caller's)",
     "re-checks the key, then the parent's wildcard, then stores the stat", "a listed parent stores `absent` without the stat it made (L-12)"),
    ("FileCache::getCacheEntry", r'static const FileCache\* getCacheEntry\(', "shared (the caller's)",
     "the key, else the parent's `/*` wildcard as a static `absent`", "a listed directory answers `absent` for every name not listed"),
    ("FileCache::fromStat64", r'static int fromStat64\(', "unique, after an unlocked `stat64`",
     "overwrites the entry with the stat it made (`mFileCache[...] = cache`), with no `UseFileCache` gate", "a refresh path (`exists(p, false)`, the uncached `is*`); `add` (`:168-180`) also overwrites, so not the only writer (04)"),
    ("FileCache::add", r'static void add\(const std::string& key, bool exists', "unique",
     "a listing's entries and its `/*` wildcard (`getDirContent`, `getDirectoryFiles`)", "a listing's snapshot; `_symlink` set only here, from `d_type`"),
    ("FileCache::remove", r'static void remove\(const std::string& key\)', "unique",
     "erases the key and every ancestor's `/*` wildcard", "the writers below call it; nothing outside ES does"),
    ("FileCache::resetCache / FileSystemCache::reset()", r'static void resetCache\(', "unique",
     "clears the whole map", "the only way a remembered answer about an outside write goes"),
    ("FileSystemCache::reset(file)", r'void FileSystemCache::reset\(const std::string& file\)', "unique (through `remove`)",
     "erases one key and its ancestors' wildcards", "a caller that knows the path can drop it"),
    ("FileCache::isCached", r'static bool isCached\(', "shared", "the key or the parent's wildcard present; never stats", "says only that an answer is remembered"),
]
ERASING = {1051: "removeDirectory", 1067: "removeFile", 1097: "createDirectory", 1445: "writeAllText",
           1457: "renameFile", 1458: "renameFile", 1506: "copyFile", 1507: "copyFile"}
ERASE_NOTE = {
    "removeDirectory": "erase, then `rmdir`; nothing re-reads between",
    "removeFile": "**erase, then `isDirectory(_path)` re-stats and stores `exists` (`:1080`), then `unlink` (`:1084`): the deleted path is left cached as present (L-19)**",
    "createDirectory": "`exists(path, false)` rewrites, erase, then `mkdir`; the recursion's parents the same",
    "writeAllText": "erase after `fclose`; skipped when `fopen` fails (nothing written)",
    "renameFile": "erase both after `exists(dst, false)` and `removeFile(dst)`; the rename after the erase",
    "copyFile": "erase both after the copy; skipped on an open failure",
}
LINESETS = [  # who cited, the line they cited, the pin's line it maps to (from the brief's take-up rows)
    ("T34's brief", 144), ("T34's brief", 185), ("T34's brief", 195), ("T34's brief", 203), ("T34's brief", 220),
    ("T35", 296), ("T35", 323), ("T35", 1127), ("T35", 1131), ("T35", 161), ("T35", 162),
    ("T33", 345), ("T33", 348), ("T33", 350), ("T33", 238), ("T26", 138), ("T26", 1164),
]

def filecache():
    src = show(FSU); L = src.split("\n"); defs = functions(src)
    rows = []
    for name, rx, lock, does, outside in ENTRY:
        hits = [i for i, l in enumerate(L, 1) if re.search(rx, l)]
        if len(hits) != 1:
            FAILS.append(f"ASSERT cache-entry-points: {name} found at {hits}")
            continue
        rows.append([f"`{name}`", f"`:{hits[0]}`", lock, does, outside])
    check("cache-entry-points", len(rows))
    erasing = [i for i, l in enumerate(L, 1) if "FileCache::remove(" in l and i > 353]
    if dict((i, enclosing(defs, i)) for i in erasing) != ERASING:
        FAILS.append(f"ASSERT cache-erasing-lines: {[(i, enclosing(defs, i)) for i in erasing]}")
    check("cache-erasing-lines", len(erasing))
    # the removeFile property, asserted from the text: a cache read follows the erase before the unlink
    rf = [i for i in erasing if ERASING.get(i) == "removeFile"]
    after = "\n".join(L[rf[0]:rf[0] + 18]) if rf else ""
    if not (re.search(r'isDirectory\(_path\)', after) and after.find("isDirectory(_path)") < after.find("unlink(")):
        FAILS.append("ASSERT L-19: removeFile no longer re-reads the cache between its erase and its unlink")
    wr = collections.OrderedDict()
    for i in erasing:
        wr.setdefault(ERASING[i], []).append(i)
    w = [[f"`{f}`", ", ".join(f"`:{i}`" for i in ls), "unique (inside `remove`)", ERASE_NOTE[f]] for f, ls in wr.items()]
    adds = [[f"`{enclosing(defs, i)}`", f"`:{i}`", "unique", "a listing's write" if "add(" in L[i - 1] else "a stat's write", "--"]
            for i, l in enumerate(L, 1) if i > 353 and re.search(r'FileCache::(add|fromStat64)\(', l)
            and i not in win32_lines(src)]
    check("cache-writers", len(w) + 2)  # the six erasing writers, plus the listing writes and the stat writes as two kinds
    ls = []
    win = win32_lines(src)
    for who, n in LINESETS:
        ls.append([who, f"`:{n}`", f"`{enclosing(defs, n)}`", "WIN32 only" if n in win else "built",
                   "`" + L[n - 1].strip().replace("|", "\\|")[:70] + "`"])
    check("linesets", len(ls))
    return (table(["Entry point", "At the pin", "Lock", "What it does", "Its answer to a file another process wrote"], rows, "filecache") + "\n\n" +
            table(["Writer", "Erase lines", "Lock", "Order, read from the source"], w, "filecache") + "\n\n" +
            table(["Function", "Line", "Lock", "Kind", "Erases"], adds, "filecache") + "\n\n" +
            table(["Cited by", "Line", "The pin's function at that line", "Image", "The pin's text at that line"], ls, "filecache"))

# ---------------------------------------------------------------- the processes
SPAWN = re.compile(r'system\(|popen\(|execl|execv|fork\(')
FN = {  # function: (shell, waits, returns, callers' thread as read)
    "run": ("`system()` (`/bin/sh -c`) when waiting; `execl(\"/bin/sh\")` in a grandchild when not",
            "when `waitForExit` (the launch, `main.cpp:540`, `InputManager.cpp:1272`, `Scripting.cpp:133`, `:142`); not at `Scripting.cpp:45`",
            "`WEXITSTATUS` of the wrap's `exit $xs` (L-05); `0` when not waiting, or when the first `fork` fails",
            "the launch on the interface thread (`FileData.cpp:1100-1103`)"),
    "runShutdownCommand": ("`system()`", "yes", "`system()`'s raw status, not `WEXITSTATUS`", "the quit path"),
    "runRestartCommand": ("`system()`", "yes", "`system()`'s raw status, not `WEXITSTATUS`", "the quit path"),
    "runSystemCommand": ("`execl(\"/usr/bin/sh\")` in a grandchild", "**yes**: the child waits for the grandchild and the caller waits for the child (L-13)",
                          "`0` always (`:879`)", "the interface thread for most of its 80 call lines (#1220)"),
    "GetShOutput": ("`popen()` (`/bin/sh -c`)", "yes (to EOF, `pclose`)", "each `fgets` chunk loses its last byte: the newline of a short line, a real character past 255 bytes or at an unterminated end (L-06); `popen` failure unchecked",
                    "its 27 call lines' (T26's collision)"),
    "GetShOutputLines": ("`popen()`", "yes", "the lines; `popen` failure returns none", "its 9 call lines'"),
}

def processes():
    rows, real, linux = [], 0, 0
    for p in paths58():
        src = show(p); L = src.split("\n"); defs = functions(src); win = win32_lines(src)
        for i, l in enumerate(L, 1):
            m = SPAWN.search(l)
            if not m:
                continue
            code = l.split("//", 1)[0]
            kind = "spawn" if SPAWN.search(code) else "comment"
            fn = enclosing(defs, i)
            fn = fn.split("::")[-1]
            plat = "WIN32 only" if i in win else "built"
            real += kind == "spawn"; linux += kind == "spawn" and plat == "built"
            sh, waits, ret, thr = FN.get(fn, ("--", "--", "--", "--")) if kind == "spawn" else ("--", "--", "--", "--")
            rows.append([f"`{p.split('/')[-1]}:{i}`", f"`{fn}`", kind, plat, sh, waits, ret, thr])
    check("spawn-lines", len(rows)); check("spawn-real", real); check("spawn-linux", linux)
    return table(["Line", "Function", "Match", "Image", "Shell", "Waits", "Returns", "Callers' thread"], rows, "processes")

# ---------------------------------------------------------------- the writes and reads
WRITE = re.compile(r'fopen\(.*"wb?"|_wfopen\(.*L"wb?"|ofstream|std::rename\(|[^_a-zA-Z]unlink\(|[^_a-zA-Z]rmdir\(|[^_a-zA-Z]mkdir\(.*0755|MoveFileW|DeleteFileW|RemoveDirectoryW|CreateDirectoryW')
WNOTE = {
    "removeDirectory": ("`rmdir`", "atomic", "nothing (the directory stays)", "true when `rmdir` returned 0; true when absent"),
    "removeFile": ("`unlink` / `rmdir`", "atomic", "nothing", "true when it returned 0; true when absent; the path left cached as present (L-19)"),
    "createDirectory": ("`mkdir 0755`, parents by recursion", "per directory", "the parents made so far", "false on a race with another creator (L-16)"),
    "writeAllText": ("`fopen \"wb\"` in place, `fwrite`, `fclose`", "**no**: truncate then write", "a truncated or short file", "nothing: `void` (L-04, #1186)"),
    "renameFile": ("`std::rename`", "atomic on one filesystem", "src or dst", "true over an absent source (L-03; T21's fix)"),
    "copyFile": ("`fopen \"wb\"` in place, 512-byte `fread`/`fwrite`", "**no**", "a short destination", "true over an absent source and over a short write (L-03)"),
}

def writes():
    src = show(FSU); L = src.split("\n"); defs = functions(src); win = win32_lines(src)
    rows, linux = [], 0
    for i, l in enumerate(L, 1):
        if not WRITE.search(l.split("//", 1)[0]) or l.lstrip().startswith("#define"):
            continue
        fn = enclosing(defs, i); plat = "WIN32 only" if i in win else "built"
        linux += plat == "built"
        mech, atom, left, claim = WNOTE.get(fn, ("--", "--", "--", "--"))
        rows.append([f"`FileSystemUtil.cpp:{i}`", f"`{fn}`", plat, mech, atom, left, claim])
    pf = show("es-core/src/utils/Platform.cpp"); pl = pf.split("\n"); pwin = win32_lines(pf)
    for i, l in enumerate(pl, 1):
        if "O_CREAT" in l:
            plat = "WIN32 only" if i in pwin else "built"; linux += plat == "built"
            rows.append([f"`Platform.cpp:{i}`", f"`{enclosing(functions(pf), i)}`", plat, "`open` with `O_CREAT` and `O_WRONLY`, mode `0644`, no truncation",
                         "yes (creates or leaves)", "an empty file or the old one", "nothing: `void`"])
    zf = show("es-core/src/utils/ZipFile.cpp").split("\n")
    zl = [i for i, l in enumerate(zf, 1) if "mz_zip_reader_extract_file_to_file" in l]
    for i in zl:
        rows.append([f"`ZipFile.cpp:{i}`", "`ZipFile::extract`", "built", "miniz `MZ_FOPEN(..., \"wb\")` (`zip_file.hpp:6634`)", "**no**",
                     "a partial member", "miniz's status"])
        linux += 1
    check("write-sites", len(rows)); check("write-sites-linux", linux)
    return table(["Site", "Function", "Image", "Mechanism", "Atomic", "What an interrupted write leaves", "What its return claims"], rows, "writes")

# ---------------------------------------------------------------- the paths
PATHS = {  # function: (input class, output, case)
    "getCWDPath": ("none", "the generic cwd, `\"\"` when `getcwd` fails past 2,048 bytes", "--"),
    "getPreferredPath": ("any path", "unchanged off WIN32", "--"),
    "getGenericPath": ("any path", "`\\` to `/`, `//` folded, trailing `/` dropped", "3.21's inputs"),
    "getEscapedPath": ("a ROM path (the launch's `%ROM%`)", "a backslash before each character of the list at `:679`", "3.19 (held at stage B)"),
    "getCanonicalPath": ("any path", "the `.`/`..` fold", "3.20 (held at stage B)"),
    "getAbsolutePath": ("a relative path and a base", "`getCanonicalPath(base + \"/\" + path)` unless absolute", "--"),
    "getParent": ("any path", "the text before the last `/`", "--"),
    "getFileName": ("any path", "the text after the last `/`", "--"),
    "getStem": ("any path", "the file name less its last extension", "--"),
    "getExtension": ("any path", "from the last `.` of the file name", "--"),
    "changeExtension": ("a path and an extension", "the extension replaced", "--"),
    "resolveRelativePath": ("a path and a root", "`./` and `~/` resolved against the root", "--"),
    "createRelativePath": ("a path and a root", "`./`-relative by string prefix", "3.21 (`.//a.png`)"),
    "removeCommonPath": ("a path and a prefix", "the rest by string prefix, not by component", "3.21"),
    "resolveSymlink": ("a path", "`readlink`'s target, made absolute", "--"),
    "combine": ("a base and a name", "joined; a leading `/..` climbs the base", "--"),
    "megaBytesToString": ("a size", "a display string", "--"),
    "kiloBytesToString": ("a size", "a display string", "--"),
    "getTempPath": ("none", "the temp folder, created", "--"),
    "getPdfTempPath": ("none", "the PDF temp folder, emptied", "--"),
    "getFileMd5": ("a file", "hex MD5", "--"),
    "getFileCrc32": ("a file", "hex CRC32", "--"),
}

NOT_PATHS = {"readAllText"}  # a std::string read, listed in the writes and reads

def pathfns():
    src = show(FSU)
    names = [n for i, n in functions(src) if re.match(r'^\s*std::string\s', src.split("\n")[i - 1])]
    names = [n for n in dict.fromkeys(names) if n not in NOT_PATHS]
    if sorted(names) != sorted(PATHS):
        FAILS.append(f"ASSERT path-transforms: the pin's std::string functions {sorted(names)} against the table's {sorted(PATHS)}")
    check("path-transforms", len(names))
    defs = dict((n, i) for i, n in functions(src))
    rows = [[f"`{n}`", f"`:{defs.get(n, '?')}`", *PATHS.get(n, ("?", "?", "?"))] for n in names]
    return table(["Transform", "At the pin", "Input class", "Output", "Case"], rows, "paths")

GEN = {"coverage": coverage, "leads": leads, "filecache": filecache, "processes": processes, "writes": writes, "paths": pathfns}

def main():
    ap = argparse.ArgumentParser()
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--write"); g.add_argument("--check"); g.add_argument("--print", dest="pr")
    ap.add_argument("--expect", action="append", default=[])
    a = ap.parse_args()
    for e in a.expect:
        k, v = e.split("="); EXPECT[k] = int(v)
    names = [a.pr] if a.pr else list(GEN)
    out = {n: GEN[n]() for n in names}
    if FAILS:
        print("\n".join(FAILS)); sys.exit(1)
    if a.pr:
        print(out[a.pr]); return
    path = a.write or a.check
    doc = open(path).read(); new = doc
    for n, t in out.items():
        rx = re.compile(r'(<!-- gen:%s -->\n)(?:.*?\n)?(<!-- /gen:%s -->)' % (n, n), re.S)
        if not rx.search(new):
            print(f"ASSERT block: no gen:{n} block in {path}"); sys.exit(1)
        new = rx.sub(lambda m: m.group(1) + t + "\n" + m.group(2), new)
    if a.check:
        if new != doc:
            print(f"DRIFT: {path}'s generated blocks differ from the pin's tables"); sys.exit(1)
        print(f"check: {len(out)} blocks match the pin"); return
    open(path, "w").write(new)
    for n, t in out.items():
        print(f"{n}: {t.strip().splitlines()[-1] if n not in ('coverage',) else [l for l in t.splitlines() if l.startswith('generated')][0]}")

if __name__ == "__main__":
    main()

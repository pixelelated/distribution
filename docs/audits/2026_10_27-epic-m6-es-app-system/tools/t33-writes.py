"""02 § The writes: every save_file( / writeAllText( / std::ofstream line in T33's slice (#680, Q4).

    python3 -I t33-writes.py <es worktree> <commit> <paths.txt> [lines=11]

The lines are § 5's grep, read the same way: a plain line match, comments
included, so `CustomFeatures.cpp:151` (inside a /* */ block) and
`Win32ApiSystem.cpp:979` (inside `#if WIN32`, :1-:1267) are rows marked
dead, as the brief's § 4 Q4 asks. D-CLOUD-078 asks every writer for
temp-and-rename; the comparison is JourneyTiers' writer
(`guis/GuiMenu.cpp:5066`, `AtomicFile::writeText`) and es-core's
`AtomicFileUtil` (`es-file-tests`). Each row carries its `Already written:`
line (upgrade-and-install.md, D-WORKFLOW-050): what a cut file left by this
writer reads as to the code at the pin.

Exits 1 when a line has no row, a row names a line with no match, or the
count differs from the one given. At another commit a line takes the row of
the pin's line of the same order in its file (D-WORKFLOW-210); a file
whose every write line a stream replaced (S1a's `Gamelist.cpp`) prints its
pin rows as replaced and counts none of them.
"""
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from t33lib import show  # noqa: E402

PAT = re.compile(r"save_file\(|writeAllText\(|std::ofstream")
# (file, line, what it writes and its tier, how, last good copy, Already written, disposition)
ROWS = [
    ("CaptureRotation.cpp", 175, "a game's `.rotation` record beside its save states (saves tier, synced)", "in place (`writeAllText`)", "none",
     "a cut record lacks `from=checked-launch` and reads as untrusted (`:124`), the core's table standing in; but the running process caches the new turns with the destination's mtime after an unchecked write (`:175-180`, EP-40), so a failed write reads as the new rotation until restart", "L-03: Backlog #1186's site (§ 1 e); temp-and-rename through `AtomicFile::writeText`"),
    ("CollectionSystemManager.cpp", 345, "a custom collection's `custom-<name>.cfg` (settings tier, in backuptool's archive)", "in place (`std::ofstream`, truncate then write, no error check)", "none",
     "a cut list reads as a shorter collection: the games past the cut are silently out of it, and the next save writes the shorter list back", "L-23: a stream (temp-and-rename through `AtomicFileUtil`, which also drops the cache entry `:1610`/`:1613` remember)"),
    ("CustomFeatures.cpp", 151, "nothing: `c:\\temp\\test.xml` inside a /* */ block", "dead text", "--", "nothing inherited: the line never compiled", "left: upstream's comment"),
    ("FileFilterIndex.cpp", 1313, "a dynamic collection's filter `.xcc` (settings tier, in backuptool's archive)", "in place (`pugi::save_file`)", "none",
     "a cut `.xcc` is a parse error: `CollectionFilter::load` returns false and the collection is left empty (`CollectionSystemManager.cpp:1114-1124` clears, then adds only on a successful load; EP-19); the page that saved it ignores `save()`'s result (EP-43)", "L-23: a stream, as `:345`"),
    ("Gamelist.cpp", 308, "`saveToXml`: the launch's `%GAMEINFOXML%` file (`FileData.cpp:639`) or a gamelist recovery file (`:336`)", "remove (`:307`) then `pugi::save_file`: no file between", "none",
     "a cut recovery file is a parse error at the next load and the entry is not recovered; the launch's file is rewritten every launch", "Backlog #1186's site (§ 1 e)"),
    ("Gamelist.cpp", 474, "`updateGamelist`: the system's `gamelist.xml` (game content tier, D-CLOUD-049, synced)", "in place (`pugi::save_file`)", "none",
     "a cut `gamelist.xml` is a parse error: the system shows no metadata until the next save, which then starts from an empty `<gameList>` (`:427`) and keeps only the dirty entries", "L-05's writer: a stream (temp-and-rename) with the uncached read `:413`"),
    ("Gamelist.cpp", 622, "`packGamelist`: `gamelist.xml`", "copy aside to `.old` (`:619-620`), then in place", "`gamelist.xml.old`",
     "as `:474`; the `.old` beside it is the previous file, which nothing reads back", "Backlog #1186's site (§ 1 e)"),
    ("Gamelist.cpp", 841, "`cleanupGamelist`: `gamelist.xml`", "copy aside to `.old` (`:838-839`), then in place", "`gamelist.xml.old`",
     "as `:622`", "with `:622`"),
    ("KeyboardMapping.cpp", 426, "a `.keys` mapping at its own path (settings tier)", "in place (`writeAllText`)", "none",
     "a cut `.keys` is a JSON parse error: the mapping loads empty", "recorded: outside the lanes (D-UI-079)"),
    ("KeyboardMapping.cpp", 429, "a `.keys` mapping at a named path", "in place (`writeAllText`)", "none", "as `:426`", "recorded with `:426`"),
    ("Win32ApiSystem.cpp", 979, "a Windows marker file (`ok`)", "dead inside `#if WIN32`", "--", "nothing inherited: no image carries it", "L-21: recorded"),
]

tree, commit, paths_file = sys.argv[1:4]
want = dict((k, int(v)) for k, v in (kv.split("=") for kv in sys.argv[4].split(","))) if len(sys.argv) > 4 else {}
PIN = "16dbac5211"


def read_lines(rev):
    out = []
    for path in [l.strip() for l in open(paths_file) if l.strip()]:
        for i, line in enumerate(show(tree, rev, path).split("\n"), 1):
            if PAT.search(line):
                out.append((path.rsplit("/", 1)[1], i))
    return out


lines = read_lines(commit)
shown = {}
gone = set()   # D-WORKFLOW-210 (S1a, #1271): a file whose every write line a stream replaced
if not commit.startswith(PIN):
    pin = read_lines(PIN)
    remap = {}
    for f in sorted(set(f for f, _ in pin) | set(f for f, _ in lines)):
        a_ = [l for g, l in pin if g == f]
        b_ = [l for g, l in lines if g == f]
        if a_ and not b_:
            gone.add(f)
            continue
        if len(a_) != len(b_):
            print("FAIL t33-writes: %s has %d write lines at the pin and %d at %s" % (f, len(a_), len(b_), commit))
            sys.exit(1)
        remap.update({(f, y): x for x, y in zip(a_, b_)})
    shown = {(f, x): y for (f, y), x in remap.items()}
    lines = [(f, remap[(f, l)]) for f, l in lines]
fail = []
rows = {(r[0], r[1]): r for r in ROWS}
for k in rows:
    if k[0] in gone:
        continue
    if k not in lines:
        fail.append("a row names %s:%d, where no write matches" % k)
for k in lines:
    if k not in rows:
        fail.append("%s:%d has no row" % k)
print("| Line | Writes | How | Last good copy | Already written | Disposition proposed |")
print("| --- | --- | --- | --- | --- | --- |")
for f, l in lines:
    r = rows.get((f, l), (f, l, "?", "?", "?", "?", "?"))
    print("| `%s:%d` | %s | %s | %s | %s | %s |" % (f, shown.get((f, l), l), r[2], r[3], r[4], r[5], r[6]))
for k in sorted(r for r in rows if r[0] in gone):
    print("| `%s:%d` (the pin's line) | %s | **replaced at this commit**: written through `AtomicFile::writeText` | -- | -- | resolved by the stream |" % (k[0], k[1], rows[k][2]))
live = sum(1 for f, l in lines if rows.get((f, l), (0,) * 4)[3] not in ("dead text", "dead inside `#if WIN32`"))
print()
print("generated, asserted: %d lines (%d live, %d dead) in %d files" % (len(lines), live, len(lines) - live, len(set(f for f, _ in lines))))
if "lines" in want and len(lines) != want["lines"]:
    fail.append("lines %d, expected %d" % (len(lines), want["lines"]))
if fail:
    print("FAIL t33-writes: " + "; ".join(fail))
    sys.exit(1)

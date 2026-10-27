"""02 § The library: one row per unit of the game lists, collections, metadata and filters (#680, Q6).

    python3 -I t33-library.py <es worktree> <commit> <paths.txt> [units=11]

Each row's facts are read at the cited lines (the pin's); the tool adds,
from the tree, the unit's lines (.cpp / .h) and its includers outside the
77 (quoted or angle-bracket form, tests excluded). Exits 1 when a unit's
files are not both in the 77, a cited caller line does not hold the
pattern it names, or the count differs.
"""
import os
import re
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from t33lib import show  # noqa: E402

POOL = "loadConfig's ThreadPool (`SystemData.cpp:1202-1258`), one work item per system"
# unit -> (what reads it, what writes it, thread, what the first frame waits for, [(file, line, pattern)] checked)
UNITS = [
    ("Gamelist", "each system's `gamelist.xml`: `parseGamelist` (`SystemData.cpp:128`), `packGamelist` first when PackGamelists (`:126`)",
     "`updateGamelist` at exit when SaveGamelistsOnExit (`SystemData.cpp:1570`) and from the API (`services/HttpServerThread.cpp:688`); `cleanupGamelist` from the menu (`guis/GuiMenu.cpp:437`, `:1157`); `saveToXml` for the launch (`FileData.cpp:639`) -- § The writes", POOL + "; the writes on the interface thread, at exit, or the API's pool",
     "every system's parse: the pool's `wait` (`SystemData.cpp:1246-1258`) under the splash",
     [("es-app/src/SystemData.cpp", 128, "parseGamelist"), ("es-app/src/SystemData.cpp", 1570, "updateGamelist"), ("es-app/src/guis/GuiMenu.cpp", 437, "cleanupGamelist")]),
    ("MetaData", "each game node, `loadFromXML` inside the parse; with PreloadMedias a cached `exists` per image (`:223`)",
     "through Gamelist's `addFileDataNode`; the editor (`guis/GuiMetaDataEd.cpp`, T31's)", POOL, "inside the parse; PreloadMedias adds one `exists` per image, thumbnail and marquee", []),
    ("Genres", "`:/genres.xml` (`Genres::init`, `main.cpp:811`)", "none", "main()'s ThreadPool (`main.cpp:806`)",
     "`waitAllExcept(vlcInit)` (`main.cpp:846`) before the systems load", [("es-app/src/main.cpp", 811, "Genres::init")]),
    ("PlatformId", "no file: the name table, read as each system loads (`SystemData.cpp:1410`)", "none", "the loader", "a table lookup", [("es-app/src/SystemData.cpp", 1410, "getPlatformId")]),
    ("LangParser", "no file: the region and language table, read when a name is formatted", "none", "the interface thread", "nothing", []),
    ("FileTag", "no file: nine tag names and icons (L-25: three reach no msgid)", "none", "the interface thread", "nothing", []),
    ("CollectionSystemManager", "the collections folder, `custom-<name>.cfg`, the `.xcc` filters, es_systems.cfg and the theme's collections (§ The reads)",
     "`custom-<name>.cfg` in place (`:345`, `saveCustomCollection`, from `:149` and `guis/GuiCollectionSystemsOptions.cpp:435`)",
     "`loadCollectionSystems` as one pool item (`SystemData.cpp:1214`) or on the main thread without a pool (`:1278`); `updateSystemsList` on the main thread (`:1288`); reloads on the interface thread (L-06)",
     "the collections' load and the systems list before the first view", [("es-app/src/SystemData.cpp", 1214, "loadCollectionSystems"), ("es-app/src/SystemData.cpp", 1288, "updateSystemsList")]),
    ("FileFilterIndex", "the `.xcc` (`CollectionFilter::load`, `:1144`); each game's metadata as the index is built",
     "the `.xcc` in place (`:1313`, `CollectionFilter::save`, from the filter editor, T31's `guis/GuiGamelistFilter`)",
     "built per system (`SystemData.cpp:657`) on the loader; the filter's change on the interface thread", "each system's index while it loads", [("es-app/src/SystemData.cpp", 657, "new FileFilterIndex")]),
    ("FileSorts", "no file: the 28 sort types (T2 FD-15: the index against them, `FileData.cpp:1659`)", "none", "the interface thread", "nothing",
     [("es-app/src/FileData.cpp", 1659, "FileSorts::getSortTypes")]),
    ("CustomFeatures", "es_features.cfg, the user's then the image's (`loadEsFeaturesFile`, `SystemData.cpp:1196`)", "none (`:151` is dead text)",
     "the main thread, before the pool", "the features file's parse", [("es-app/src/SystemData.cpp", 1196, "loadEsFeaturesFile")]),
    ("LibretroRatio", "no file: the ratio table (`guis/GuiMenu.cpp:11341`)", "none", "the interface thread", "nothing", [("es-app/src/guis/GuiMenu.cpp", 11341, "LibretroRatio::getInstance")]),
]

tree, commit, paths_file = sys.argv[1:4]
want = dict((k, int(v)) for k, v in (kv.split("=") for kv in sys.argv[4].split(","))) if len(sys.argv) > 4 else {}
paths = [l.strip() for l in open(paths_file) if l.strip()]
fail = []
print("| Unit | Lines (.cpp / .h) | Includers outside the 77 | Reads | Writes | Thread | The first frame waits for |")
print("| --- | --- | --- | --- | --- | --- | --- |")
for name, reads, writes, thread, first, checks in UNITS:
    files = ["es-app/src/%s.cpp" % name, "es-app/src/%s.h" % name]
    for f in files:
        if f not in paths:
            fail.append("%s is not in the 77" % f)
    counts = [str(len(show(tree, commit, f).splitlines())) if f in paths else "?" for f in files]
    out = subprocess.run(["git", "-C", tree, "grep", "-l", "-E", r'#include ["<]%s\.h[">]' % name, commit, "--", "es-app", "es-core"],
                         capture_output=True, text=True).stdout.split()
    inc = sorted(set(o.split(":", 1)[1] for o in out) - set(paths))
    inc = [i for i in inc if not i.startswith(("es-app/tests", "tests/"))]
    if commit.startswith("16dbac5211"):
        for f, l, pat in checks:
            line = show(tree, commit, f).split("\n")[l - 1]
            if pat not in line:
                fail.append("%s:%d does not hold %s" % (f, l, pat))
    print("| `%s` | %s | %d | %s | %s | %s | %s |" % (name, " / ".join(counts), len(inc), reads, writes, thread, first))
print()
print("generated, asserted: %d units" % len(UNITS))
if "units" in want and len(UNITS) != want["units"]:
    fail.append("units %d, expected %d" % (len(UNITS), want["units"]))
if fail:
    print("FAIL t33-library: " + "; ".join(fail))
    sys.exit(1)

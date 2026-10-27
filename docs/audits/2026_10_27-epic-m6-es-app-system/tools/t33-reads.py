"""02 § The reads: every Utils::FileSystem::exists( in T33's slice (#680, Q4).

    python3 -I t33-reads.py <es worktree> <commit> <paths.txt> [lines=83,calls=86,uncached=4]

The sites are found by t33lib's call reader (comments and strings skipped,
an argument read whole). Each is cached unless its second argument is
false (FileSystemUtil's enableCache default). The cache's rule is T21's
file, answered at its lines and cited, not re-read (T32's Q4): a miss or a
hit is remembered until resetCache() (`FileSystemUtil.cpp:345`, a launch)
or a restart; ES's own writers through Utils::FileSystem drop their path
from it (removeFile :1051, :1067; createDirectory :1097; writeAllText
:1445; renameFile :1457-1458; copyFile :1506-1507). A file written OUTSIDE
the process while ES runs -- cloud_content_restore's game content tier
(D-CLOUD-049: gamelist.xml, artwork, videos, manuals), the player over SSH
or Samba -- is not seen until a launch.

GROUPS maps each site to what it reads, its writer while ES runs, what a
remembered miss (or hit) reads as, and the disposition proposed for the
pause. `Win32ApiSystem.cpp`'s 31 lines are one group: the file is `#if
WIN32` from :1 to :1267 and compiles to nothing on every image (L-21).
Exits 1 when a site has no group, a group names a line with no site, or a
count differs from the one given. At a commit other than the pin, each
line is matched to the pin's line of the same order in its file (stage E,
D-WORKFLOW-210), and the table prints the commit's own line.
"""
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from t33lib import call_args, in_comment_or_string, show  # noqa: E402

OUT = "outside ES only (cloud_content_restore's game content, D-CLOUD-049; the player over SSH); the scraper and the API write through Utils::FileSystem and drop the entry"
THEME = "a theme installer (ES's own, through Utils::FileSystem) or the player"
WIN32 = [76, 82, 85, 159, 166, 324, 329, 349, 354, 378, 383, 484, 653, 657, 661, 672, 729, 739, 783, 802, 831, 840, 866, 871, 915, 947, 968, 984, 1210, 1214, 1217]
GROUPS = [
    ("CaptureRotation.cpp", [51], "fromTable: a core's rotation table under /usr/config/emulationstation/rotation", "nobody: the image's read-only tree",
     "nothing can change it while ES runs; sTables memoises the answer anyway (:44-53)", "left cached: deliberate, beside the four uncached reads (Q4)"),
    ("CaptureRotation.cpp", [113], "read(): a game's .rotation record beside its save states", "ES (write :175) and the cloud's saves tier",
     "uncached", "uncached at the pin: a record restored from the cloud is seen"),
    ("CaptureRotation.cpp", [146], "the launcher's /var/log/exec.log after a RetroArch exit", "the launcher (outside ES)",
     "uncached", "uncached at the pin (L-02 is its size, not its cache)"),
    ("CaptureRotation.cpp", [161], "retroarch.cfg after a RetroArch exit", "RetroArch (outside ES)",
     "uncached", "uncached at the pin"),
    ("CaptureRotation.cpp", [170], "write(): the record before it is rewritten", "ES and the cloud's saves tier",
     "uncached", "uncached at the pin"),
    ("CollectionSystemManager.cpp", [133, 1439], "the collections folder under the user's ES path", "ES itself (createDirectory :134); the player",
     "a remembered miss calls createDirectory on a folder that exists: harmless", "left cached"),
    ("CollectionSystemManager.cpp", [963], "a dynamic collection's filter (.xcc) at startup", "ES (FileFilterIndex.cpp:1313, through std::ofstream); a settings restore",
     "a remembered miss loads the collection without its filter until a restart; ES's own writer is not Utils::FileSystem, so its first save is not seen by this read either", "recorded with L-23 (the same files)"),
    ("CollectionSystemManager.cpp", [1147], "a custom collection's config before it is populated", "ES (std::ofstream :345); a settings restore",
     "a remembered miss shows the custom collection empty until a restart", "recorded with L-23"),
    ("CollectionSystemManager.cpp", [1317], "es_systems.cfg", "the image; the player",
     "nothing changes it in a session that matters: a new file needs a restart regardless", "left cached"),
    ("CollectionSystemManager.cpp", [1369, 1372, 1391], "the theme set's folder, its collections.info and each system's theme", THEME,
     "a remembered miss offers fewer collection themes until a restart", "left cached: theme files"),
    ("CollectionSystemManager.cpp", [1610, 1613], "deleteCustomCollection: the .xcc, then the custom-<name>.cfg", "ES (FileFilterIndex.cpp:1313, CollectionSystemManager.cpp:345, both std::ofstream)",
     "a file whose miss was remembered earlier in the session (the .xcc at :963 is the same path, getFilteredCollectionPath) and written since by std::ofstream: the delete reads it absent and returns false", "recorded with L-23: the stream that makes the writers atomic routes them through Utils::FileSystem, which drops the entry"),
    ("CustomFeatures.cpp", [164, 167], "es_features.cfg, the user's then the image's", "the image; the player",
     "read once at startup", "left cached"),
    ("FileFilterIndex.cpp", [867, 889], "showFile: a media path a game's metadata names, for a has-<media> filter", OUT,
     "a remembered answer keeps a game in (or out of) a has-media filter until a launch", "recorded: the family of L-05 and L-11, outside the lanes (D-UI-079)"),
    ("FileFilterIndex.cpp", [1144], "CollectionFilter::load: the .xcc", "ES (std::ofstream :1313)",
     "as :963", "recorded with L-23"),
    ("Gamelist.cpp", [190], "loadGamelistFile: a game file the gamelist.xml names but the scan did not find", "the player, a cloud ROM restore",
     "a remembered miss drops the entry from the list until a restart", "recorded: the scan reads the folder, which the cache does not serve"),
    ("Gamelist.cpp", [304], "saveToXml: the system's folder before the write", "the player",
     "a remembered hit for a folder removed since lets the write fail; the folder is the system's own", "left cached"),
    ("Gamelist.cpp", [352], "removeFromGamelistRecovery: the recovery file", "ES itself (removeFile :353, writeAllText)",
     "ES's own writes drop the entry", "left cached"),
    ("Gamelist.cpp", [413], "updateGamelist: gamelist.xml before ES merges and writes it", "cloud_content_restore (D-CLOUD-049), the player; ES itself (save_file :474, not through Utils::FileSystem)",
     "a gamelist.xml that arrived after startup reads as absent: the next save (a played game, an edit) starts from an empty <gameList> (:427) and writes only the dirty entries over the restored file (:474), losing every other entry's metadata", "L-05: a stream (uncached, with :116's gate); G-04's variant the positive, image side"),
    ("Gamelist.cpp", [531, 644], "cleanupGamelist / packGamelist: gamelist.xml", "as :413",
     "a remembered miss skips the cleanup: the safe direction", "recorded with L-05"),
    ("Gamelist.cpp", [601, 705], "packGamelist / cleanupGamelist: each media path the xml names", OUT,
     "a remembered miss removes the entry for a file restored since; a remembered hit keeps a dangling one", "recorded with L-05: the cleanup runs from a menu action, after which a launch has not reset the cache"),
    ("Gamelist.cpp", [732, 735, 738, 740, 743, 745, 748], "cleanupGamelist: the media file a game's name implies, by suffix and extension", OUT,
     "a remembered miss leaves media restored since unlinked", "recorded with L-05"),
    ("Genres.cpp", [22], "genres.xml in the resources", "nobody: the image's read-only tree",
     "read once", "left cached"),
    ("KeyboardMapping.cpp", [222], "a game's or system's .keys file", "ES (writes :426, :429); the player; a settings restore",
     "a remembered miss loads no mapping until the next launch resets the cache", "left cached: outside the lanes (D-UI-079)"),
    ("KeyboardMapping.cpp", [324], "deleteFile: the .keys file", "ES (writes :426, :429, not through Utils::FileSystem)",
     "a mapping saved this session and deleted before a launch: the remembered miss skips removeFile, the file stays", "recorded: outside the lanes (D-UI-079)"),
    ("MetaData.cpp", [223], "loadFromXML with PreloadMedias: each image, thumbnail or marquee path", OUT,
     "the load is at startup or a reload; a file absent then drops its metadata until the next load", "recorded: the family of L-05"),
    ("SystemRandomPlaylist.cpp", [87, 97, 104], "a random game's media path", OUT,
     "a remembered hit hands a removed file to the player; a remembered miss skips one restored since", "recorded with L-11: outside the lanes (D-UI-079)"),
    ("SystemScreenSaver.cpp", [51, 375, 388], "the screensaver's title folder", "ES itself (createDirectory)",
     "harmless", "left cached"),
    ("SystemScreenSaver.cpp", [157], "startScreenSaver: ten retries for a random game video", OUT,
     "ten retries over the same cached answers never see a file appear; a removed video's remembered hit is handed on", "L-11: recorded, outside the lanes (D-UI-079)"),
    ("SystemScreenSaver.cpp", [164, 208], "startScreenSaver: the chosen video or image before it plays", OUT,
     "a remembered hit plays a removed file (the player sees the fallback)", "L-11: recorded, outside the lanes (D-UI-079)"),
    ("SystemScreenSaver.cpp", [694, 730, 733], "the bezel set's systems folder, its image and .info", THEME,
     "a remembered miss shows the screensaver without the bezel", "left cached: theme files"),
    ("SystemScreenSaver.cpp", [787], "the game's marquee for the screensaver", OUT,
     "a remembered miss hides the marquee", "L-11's family: recorded"),
    ("Win32ApiSystem.cpp", WIN32, "Windows-only paths", "none: the file is `#if WIN32` (:1-:1267) and compiles to nothing",
     "nothing: no image carries it", "L-21: dead on every image; recorded"),
]

tree, commit, paths_file = sys.argv[1:4]
want = dict((k, int(v)) for k, v in (kv.split("=") for kv in sys.argv[4].split(","))) if len(sys.argv) > 4 else {}
PIN = "16dbac5211"


def read_sites(rev):
    out = []
    for path in [l.strip() for l in open(paths_file) if l.strip()]:
        src = show(tree, rev, path)
        for m in re.finditer(r"\bFileSystem::exists\s*\(", src):
            if in_comment_or_string(src, m.start()):
                continue
            a, _ = call_args(src, src.index("(", m.start()))
            line = src.count("\n", 0, m.start()) + 1
            cached = not (len(a) > 1 and a[1].strip() == "false")
            out.append((path.rsplit("/", 1)[1], line, cached))
    return out


# GROUPS are written in the pin's lines. At another commit (stage E, D-WORKFLOW-210)
# a line takes the group of the pin's line of the same order in its file, so a
# fix that moves lines keeps its rows; a file whose line count changed fails.
sites = read_sites(commit)
if not commit.startswith(PIN):
    pin_lines = sorted(set((f, l) for f, l, _ in read_sites(PIN)))
    now_lines = sorted(set((f, l) for f, l, _ in sites))
    remap = {}
    for f in sorted(set(f for f, _ in pin_lines) | set(f for f, _ in now_lines)):
        a_ = [l for g, l in pin_lines if g == f]
        b_ = [l for g, l in now_lines if g == f]
        if len(a_) != len(b_):
            print("FAIL t33-reads: %s has %d exists( lines at the pin and %d at %s" % (f, len(a_), len(b_), commit))
            sys.exit(1)
        remap.update({(f, y): x for x, y in zip(a_, b_)})
    shown = {(f, x): y for (f, y), x in remap.items()}
    sites = [(f, remap[(f, l)], c) for f, l, c in sites]
else:
    shown = {}
lines = sorted(set((f, l) for f, l, _ in sites))
fail = []
group_of = {}
for i, (f, ls, *_rest) in enumerate(GROUPS):
    for l in ls:
        if (f, l) not in lines:
            fail.append("a group names %s:%d, where there is no exists(" % (f, l))
        group_of[(f, l)] = i
for f, l in lines:
    if (f, l) not in group_of:
        fail.append("%s:%d has no group" % (f, l))
print("| Line | Reads | Writer while ES runs | Cache | A remembered answer reads as | Disposition proposed |")
print("| --- | --- | --- | --- | --- | --- |")
for f, l in lines:
    calls = [s for s in sites if s[0] == f and s[1] == l]
    g = GROUPS[group_of[(f, l)]] if (f, l) in group_of else (f, [l], "?", "?", "?", "?")
    cache = "cached" if all(c for _, _, c in calls) else "uncached"
    print("| `%s:%d` | %s%s | %s | %s | %s | %s |" % (f, shown.get((f, l), l), g[2], " (%d calls)" % len(calls) if len(calls) > 1 else "", g[3], cache, g[4], g[5]))
counts = {"lines": len(lines), "calls": len(sites), "uncached": sum(1 for s in sites if not s[2])}
print()
print("generated, asserted: %d lines, %d calls, %d uncached, in %d files" % (counts["lines"], counts["calls"], counts["uncached"], len(set(f for f, _ in lines))))
fail += ["%s %d, expected %d" % (k, counts[k], v) for k, v in want.items() if counts.get(k) != v]
if fail:
    print("FAIL t33-reads: " + "; ".join(fail))
    sys.exit(1)

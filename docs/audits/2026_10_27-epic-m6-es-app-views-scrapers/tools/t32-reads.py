"""02 § The reads: every Utils::FileSystem::exists( in T32's slice (#679, Q4).

    python3 -I t32-reads.py <es worktree> <commit> <paths.txt> [lines=49,calls=50,uncached=0]

The sites are found by t32lib's call reader (comments and strings skipped,
an argument read whole). Each is cached unless its second argument is
false (FileSystemUtil's enableCache default). The cache's rule, read at
the pin in es-core/src/utils/FileSystemUtil.cpp (T21's file): a miss or a
hit is remembered until resetCache() (a launch) or a restart; ES's own
writers through Utils::FileSystem drop their path from it (removeFile
:1051, :1067; createDirectory :1097; writeAllText :1445; renameFile
:1457-1458; copyFile :1506-1507), so the scraper's downloads (HttpReq's
rename) and the HTTP API's media (writeAllText) are seen at once; a file
written OUTSIDE the process while ES runs -- cloud_content_restore's game
content tier (D-CLOUD-049: artwork, videos, manuals), the player over SSH
or Samba -- is not, until a launch.

GROUPS maps each site to what it reads, its writer while ES runs, what a
remembered miss (or hit) reads as, and the disposition proposed for the
pause. Exits 1 when a site has no group, a group names a line with no
site, or a count differs from the one given.
"""
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from t32lib import call_args, in_comment_or_string, show  # noqa: E402

OUT = "outside ES only (cloud_content_restore's game content, the player over SSH); the scraper and the API write through Utils::FileSystem and drop the entry"
GROUPS = [
    ("GamesDBJSONScraperResources.cpp", [37], "the scrapers' resource directory", "ES itself (createDirectory, :38)",
     "a remembered miss calls createDirectory on a directory that exists: harmless", "left cached: nothing changes on screen"),
    ("Scraper.cpp", [88, 92, 96, 100, 104, 108, 112, 116, 120, 124, 128], "hasAnyMedia: each media path a game's metadata names", OUT,
     "a remembered hit for a file removed since counts the game as having media: GAMES MISSING ALL MEDIA skips it", "L-09: a stream question (uncached, or the scrape's run resetting the cache first)"),
    ("Scraper.cpp", [137, 141, 145, 149, 153, 157, 161, 165, 169, 173, 177], "hasMissingMedia: the same paths", OUT,
     "a remembered miss for a file restored since counts it missing: the game is fetched again", "L-09: as above"),
    ("Scraper.cpp", [407], "MDResolveHandle: the media path already in the game's metadata", OUT,
     "with ScrapeOverWrite off, a remembered miss downloads over a file the player kept", "L-09: a stream question"),
    ("Scraper.cpp", [440], "MDResolveHandle: the save-as path the download would write", OUT,
     "as :407: a remembered miss overwrites; a remembered hit keeps a file removed since and records its path", "L-09: a stream question"),
    ("Scraper.cpp", [808], "getSaveAsPath: the media folder under the system's root", "ES itself (createDirectory, :809); the player",
     "a remembered hit for a folder removed since leaves the download nowhere to land (the write fails)", "recorded"),
    ("HttpServerThread.cpp", [754], "the delete route: the game's own file before removeFile", "the player, a cloud restore of ROMs",
     "a remembered miss skips the delete: the safe direction", "left cached (the brief's reading confirmed)"),
    ("DetailedContainer.cpp", [667, 669, 677, 679, 681], "a folder's snapshot: its first game's titleshot / boxart / fanart / cartridge / mix", OUT,
     "a remembered miss falls to the next source or the default picture until a launch", "recorded with L-08 (the same rule)"),
    ("DetailedContainer.cpp", [756, 762, 765, 768, 771], "the per-game theme extras' xml (by stem, by CRC32, then theme.xml)", "the player or a theme installer",
     "a remembered miss shows no per-game extras until a launch", "left cached: theme files, not game content"),
    ("DetailedContainer.cpp", [817, 819, 827, 829, 831], "the selected game's picture source (titleshot / boxart / fanart / cartridge / mix)", OUT,
     "a remembered miss shows the fallback picture until a launch", "L-08: the stream with :903 and :916"),
    ("DetailedContainer.cpp", [863], "the marquee (getMarqueePath)", OUT, "a remembered miss leaves the marquee blank until a launch", "L-08"),
    ("DetailedContainer.cpp", [873], "each md_* image's metadata path", OUT, "a remembered miss leaves the image blank until a launch", "L-08"),
    ("DetailedContainer.cpp", [903], "the manual or the magazine (two calls), PreloadMedias off", OUT,
     "a remembered miss hides MANUAL (or shows NO MANUAL) until a launch", "L-08: the guest's G-09 positive; a stream question"),
    ("DetailedContainer.cpp", [916], "the map, PreloadMedias off", OUT, "a remembered miss hides MAP until a launch", "L-08: as :903"),
    ("GridGameListView.cpp", [208], "a folder tile's image (getImagePath)", OUT,
     "a remembered miss names the folder without its picture flag at populate", "recorded"),
    ("ISimpleGameListView.cpp", [619], "the theme's logo element path", "a theme installer",
     "a remembered miss leaves the header without its logo", "left cached: theme files"),
    ("ISimpleGameListView.cpp", [910], "the system's logo property, for the parent folder's row", "a theme installer",
     "a remembered miss gives the .. row no picture", "left cached: theme files"),
]

tree, commit, paths_file = sys.argv[1:4]
want = dict((k, int(v)) for k, v in (kv.split("=") for kv in sys.argv[4].split(","))) if len(sys.argv) > 4 else {}
sites = []
for path in [l.strip() for l in open(paths_file) if l.strip()]:
    src = show(tree, commit, path)
    for m in re.finditer(r"\bFileSystem::exists\s*\(", src):
        if in_comment_or_string(src, m.start()):
            continue
        a, _ = call_args(src, src.index("(", m.start()))
        line = src.count("\n", 0, m.start()) + 1
        cached = not (len(a) > 1 and a[1].strip() == "false")
        sites.append((path.rsplit("/", 1)[1], line, cached))
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
    print("| `%s:%d` | %s%s | %s | %s | %s | %s |" % (f, l, g[2], " (%d calls)" % len(calls) if len(calls) > 1 else "", g[3], cache, g[4], g[5]))
counts = {"lines": len(lines), "calls": len(sites), "uncached": sum(1 for s in sites if not s[2])}
print()
print("generated, asserted: %d lines, %d calls, %d uncached, in %d files" % (counts["lines"], counts["calls"], counts["uncached"], len(set(f for f, _ in lines))))
fail += ["%s %d, expected %d" % (k, counts[k], v) for k, v in want.items() if counts.get(k) != v]
if fail:
    print("FAIL t32-reads: " + "; ".join(fail))
    sys.exit(1)

"""02 § The views: the five game list styles and the system carousel (#679, Q5, Q6).

    python3 -I t32-views.py <es worktree> <commit> [views=6,helpbars=2]

From the headers and sources under es-app/src/views at the commit: each
view class's base (`class X : public Y`), its getName() default (`return
"<style>"`), whether it defines getHelpPrompts (else whose it inherits),
and its populate function's line. NOTES records what draws each view and
what it reads per item on the interface thread before the first frame,
read at the lines. Exits 1 when a drawable view has no note, a note names
no class, a style's getName() default is missing, or a count differs.
"""
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from t32lib import show  # noqa: E402

NOTES = {
    "SystemView": ("the system carousel (`mCarousel`, `SystemView.cpp:196` `populate`, `TextureLoader::paused` while it runs)",
                   "per visible system: its theme's view elements (`getViewElements`, when `mViewNeedsReload`) and its extras (`loadExtras`) -- after UPDATE GAMELISTS, every system's again (G-09)"),
    "BasicGameListView": ("`TextListComponent` (`mList`, theme element `gamelist`, `:44`)", "per file: `GameNameFormatter::getDisplayName` (`:76`), metadata only; no file read"),
    "DetailedGameListView": ("Basic's list and the `DetailedContainer` panel (the `md_*` and the theme's extras)", "Basic's populate; on each cursor move the container's cached `exists(` reads (§ The reads, `:817-916`)"),
    "VideoGameListView": ("Basic's list and the container's video", "as Detailed; the video on each cursor move"),
    "GridGameListView": ("`ImageGridComponent` (`mGrid`, theme element `gamegrid`, `:229`)",
                         "per file: `getImagePath` (`:131-153`, 3.31) and, for a folder, a cached `exists` (`:208`); **on SCREENSHOTS (IMAGEVIEWER), `DisplayAspect::forScreenshot(file)` per tile through `setTileDecorator` (`:42-47`) -- a capture record read per tile (`DisplayAspect.cpp:99-131`), L-14**"),
    "CarouselGameListView": ("`CarouselComponent` (`mList`, theme element `gamecarousel`, `:37`)", "per file: `getDisplayName` (`:83`), metadata only"),
}

tree, commit = sys.argv[1:3]
want = dict((k, int(v)) for k, v in (kv.split("=") for kv in sys.argv[3].split(","))) if len(sys.argv) > 3 else {}
import subprocess  # noqa: E402
names = [p for p in subprocess.run(["git", "-C", tree, "ls-tree", "-r", "--name-only", commit, "--", "es-app/src/views"], capture_output=True, text=True, check=True).stdout.split()
         if not os.path.basename(p).startswith("ViewController.")]   # T2's (#649), outside the 42
classes, defaults, helpbars, populate = {}, {}, set(), {}
for p in names:
    s = show(tree, commit, p)
    base = os.path.basename(p)
    for m in re.finditer(r"^class (\w+)\s*:\s*public (\w+)", s, re.M):
        classes[m.group(1)] = (m.group(2), p)
    for m in re.finditer(r'return "(basic|detailed|video|grid|gamecarousel)"', s):
        defaults[base.rsplit(".", 1)[0]] = (m.group(1), "%s:%d" % (base, s.count("\n", 0, m.start()) + 1))
    for m in re.finditer(r"^\S.*\b(\w+)::getHelpPrompts\(", s, re.M):
        helpbars.add(m.group(1))
    for m in re.finditer(r"^void (\w+)::(populateList|populate)\(", s, re.M):
        populate[m.group(1)] = "%s:%d" % (base, s.count("\n", 0, m.start()) + 1)


def inherited(c, table):
    while c is not None and c not in table:
        c = classes.get(c, (None,))[0]
    return c


fail = ["%s has no note" % c for c in classes if (c == "SystemView" or (c.endswith("GameListView") and not c.startswith("I"))) and c not in NOTES]
fail += ["a note names %s, which is no class here" % n for n in NOTES if n not in classes]
for c in NOTES:
    if c != "SystemView" and c not in defaults:
        fail.append("%s has no getName() default" % c)
print("| View | Base | Style (`getName()` default) | Draws | Populate | Help bar | Reads per item before the first frame |")
print("| --- | --- | --- | --- | --- | --- | --- |")
for c in NOTES:
    base = classes.get(c, ("?",))[0]
    style = "`%s` (`%s`)" % defaults[c] if c in defaults else "-"
    pop = inherited(c, populate)
    hb = inherited(c, helpbars)
    print("| `%s` | `%s` | %s | %s | %s | %s | %s |" % (c, base, style, NOTES[c][0], ("`%s`" % populate[pop]) + ("" if pop == c else " (`%s`'s)" % pop) if pop else "-",
                                                    "`%s::getHelpPrompts`%s" % (hb, "" if hb == c else " (inherited)") if hb else "-", NOTES[c][1]))
counts = {"views": len(NOTES), "helpbars": len(helpbars)}
print()
print("generated, asserted: %d views (the five styles and the carousel); getHelpPrompts defined by %d classes: %s; %d view classes under views/ in all"
      % (counts["views"], counts["helpbars"], ", ".join(sorted(helpbars)), len(classes)))
fail += ["%s %d, expected %d" % (k, counts[k], v) for k, v in want.items() if counts.get(k) != v]
if fail:
    print("FAIL t32-views: " + "; ".join(fail))
    sys.exit(1)

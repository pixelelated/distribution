"""The title shapes of T31's pages against es-menu-map-check and the map (#678, Q7).

    python3 -I t31-titles.py <es worktree> <commit> <docs/es-menu-map.md> [paths.txt]

For each .cpp of the slice at <commit>: the titles the checker sees (its own
three SCREEN_PATTERNS, loaded from tools/es-menu-map-check, never retyped),
and the titles a wider sweep sees:
  - GuiSettings(<any window expression>, _("T")) -- new or direct;
  - a MenuComponent built with a literal title, as a member initialiser
    (mMenu(window, _("T")...)) or a construction (MenuComponent(w, _("T")...));
  - setTitle(_("T")) and setSubtitle-free title components:
    a TextComponent whose text is the page's header (mTitle / title / mHeader
    built from _("T"), Utils::String::toUpper(_("T")) included);
  - a title that is not a _() literal (GuiSettings(w, <expression>)), recorded
    in its own column: a computed title, or a raw "..." the catalog never sees
    (GuiMoonlight.cpp's at the pin), or GuiSettings' own constructor parameter.
Each literal title is judged by the checker's own names_screen() against the
map's body and by its own Not-mapped parse, so "mapped" here is what the
checker would say if it could see the title.

Asserts the brief's hand counts (§ 5, version 2): 12 .cpp with a title by the
checker's shapes, 27 by the wider sweep, 10 with no _() literal title (the
brief's "no title by any shape": 37 - 27). A count that differs
is printed with the files, and the tool exits 1: the brief's number is a
hand count, this tool's is the line. The paths default to
.qa-scratch/t31/paths.txt.
"""
import importlib.machinery
import importlib.util
import re
import subprocess
import sys
from pathlib import Path

tree, commit, map_path = sys.argv[1:4]
paths_file = sys.argv[4] if len(sys.argv) > 4 else ".qa-scratch/t31/paths.txt"

loader = importlib.machinery.SourceFileLoader("es_menu_map_check", "tools/es-menu-map-check")
spec = importlib.util.spec_from_loader("es_menu_map_check", loader)
checker = importlib.util.module_from_spec(spec)
loader.exec_module(checker)
checker.MAP = Path(map_path)
map_text, declared = checker.map_text_and_exclusions()
body = re.sub(r"^## Not mapped\b.*?(?=^## |\Z)", "", map_text, flags=re.M | re.S)

WIDER = [
    re.compile(r'\bGuiSettings\s*\(\s*[\w>.\-]+\s*,\s*_\("([^"]+)"\)'),
    re.compile(r'\b(?:mMenu|mMenu\.\w+|MenuComponent)\s*\(\s*[\w>.\-]+\s*,\s*(?:Utils::String::toUpper\()?_\("([^"]+)"\)'),
    re.compile(r'\bsetTitle\s*\(\s*(?:Utils::String::toUpper\()?_\("([^"]+)"\)'),
    re.compile(r'\b(?:mTitle|title|mHeader)\s*=\s*std::make_shared<TextComponent>\s*\(\s*[\w>.\-]+\s*,\s*(?:Utils::String::toUpper\()?_\("([^"]+)"\)'),
]
COMPUTED = re.compile(r'\bGuiSettings\s*\(\s*[\w>.\-]+\s*,\s*(?!_\(")([^,;)]+(?:\([^()]*\))?)')

def show(path):
    return subprocess.run(["git", "-C", tree, "show", "%s:%s" % (commit, path)],
                          capture_output=True, text=True, check=True).stdout

def where(title):
    if title in declared:
        return "declared"
    if checker.names_screen(body, title):
        return "mapped"
    return "neither"

cpps = [l.strip() for l in open(paths_file) if l.strip().endswith(".cpp")]
seen_checker, seen_wider, none, neither_pages = [], [], [], []
print("| File | Checker's shapes | Wider sweep (_() literal) | Not a _() literal | The map |")
print("| --- | --- | --- | --- | --- |")
for path in cpps:
    src = show(path)
    name = path.rsplit("/", 1)[1]
    ck = sorted({m.group(1) for p in checker.SCREEN_PATTERNS for m in p.finditer(src)})
    wd = sorted({m.group(1) for p in WIDER for m in p.finditer(src)} | set(ck))
    comp = sorted({re.sub(r"\s+", " ", m.group(1)).strip() for m in COMPUTED.finditer(src)})
    if ck:
        seen_checker.append(name)
    if wd:
        seen_wider.append(name)
    if not wd:
        none.append(name)
    verdicts = ["%s: %s" % (t, where(t)) for t in wd]
    if wd and all(where(t) == "neither" for t in wd):
        neither_pages.append(name)
    print("| `%s` | %s | %s | %s | %s |" % (name, ", ".join(ck) or "-", ", ".join(t for t in wd if t not in ck) or "-",
                                            ", ".join("`%s`" % c.replace("|", "\\|") for c in comp) or "-", "; ".join(verdicts) or "-"))
print()
print(".cpp %d; with a title by the checker's shapes %d; by the wider sweep %d; with no _() literal title %d; "
      "pages whose every literal title is in neither the map's body nor ## Not mapped %d"
      % (len(cpps), len(seen_checker), len(seen_wider), len(none), len(neither_pages)))
print("no title: " + ", ".join(none))
print("neither: " + ", ".join(neither_pages))
fail = []
for what, got, want in (("checker", len(seen_checker), 12), ("wider", len(seen_wider), 27), ("none", len(none), 10)):
    if got != want:
        fail.append("%s %d, the brief's hand count %d" % (what, got, want))
if fail:
    print("FAIL t31-titles: " + "; ".join(fail))
    sys.exit(1)

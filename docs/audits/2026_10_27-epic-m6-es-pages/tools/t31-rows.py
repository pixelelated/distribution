"""Every value-binding row builder call in T31's slice, with its store and overload (#678, Q2).

    python3 -I t31-rows.py <es worktree> <commit> <paths.txt>

Reads each call by balanced brackets (t31lib.call_args) in the slice's .cpp
files at <commit>; the declarations and definitions in GuiSettings.h/.cpp are
skipped (a call is a site whose receiver is not a declaration). The builders
and their stores, as GuiSettings.h declares them at the pin:

  addSwitch(title, settingsID, storeInSettings[, onChanged])           -- 3 or 4 args
  addSwitch(title, description, settingsID, storeInSettings, onChanged) -- 5 args
  addOptionList(title, values, settingsID, storeInSettings[, cb]) / with a description
  addInputTextConfigRow(title, settingsID, password, storeInSettings = false, editor)
  addFileBrowser(title, settingsID, type, storeInSettings = false)
  storeInSettings true -> Settings (es_settings.cfg); false -> SystemConf (system.cfg)

  addWithDescription: GuiSettings' 3-argument form (comp, setCursorHere) passes
  multiLine = true; its func form, and MenuComponent's (mMenu.), default
  multiLine = false unless the seventh argument says otherwise.

addInputTextRow binds no key (the caller's onsave writes) and is listed with
store "caller's onsave". Output: a table and the totals per builder; exits 1
when the per-builder totals differ from the counts asserted at the end, which
were taken from this tool's first run and checked against the brief's
switches and two-line-rows runs (26 addSwitch lines of which 3 in GuiSettings'
own header/source; 14 addWithDescription lines in 7 files).
"""
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from t31lib import call_args, in_comment_or_string, literal, show  # noqa: E402

tree, commit, paths_file = sys.argv[1:4]
BUILDERS = ("addSwitch", "addOptionList", "addInputTextConfigRow", "addFileBrowser", "addWithDescription", "addInputTextRow")
# The receiver may not cross a line: "places." at a comment's end once took the
# next line's call into the comment (the DEVELOPER ID row, found by its absence).
CALL = re.compile(r"(?:(\b[\w\]\)]+(?:->|\.))[ \t]*)?\b(%s)\s*\(" % "|".join(BUILDERS))

def store(flag):
    v = flag.strip()
    if v == "true":
        return "Settings"
    if v == "false":
        return "SystemConf"
    return "<%s>" % v

rows, totals = [], {}
for path in [l.strip() for l in open(paths_file) if l.strip().endswith(".cpp")]:
    src = show(tree, commit, path)
    name = path.rsplit("/", 1)[1]
    for m in CALL.finditer(src):
        if in_comment_or_string(src, m.start(2)):
            continue
        if src[:m.start(2)].endswith("GuiSettings::"):
            continue  # a definition in GuiSettings.cpp, not a call
        builder, receiver = m.group(2), (m.group(1) or "")
        a, _ = call_args(src, src.index("(", m.start(2)))
        line = src.count("\n", 0, m.start()) + 1
        lab = literal(a[0]) if a else None
        lab = lab if lab is not None else "<%s>" % (a[0][:40] if a else "")
        key, st, form = "-", "-", ""
        if builder == "addSwitch":
            if len(a) >= 5:
                key, st, form = a[2], store(a[3]), "with description"
            else:
                key, st, form = a[1], store(a[2]), "no description"
        elif builder == "addOptionList":
            if len(a) >= 6 or (len(a) == 5 and not a[4].startswith(("[", "std::bind", "nullptr"))):
                key, st, form = a[3], store(a[4]), "with description"
            else:
                key, st, form = a[2], store(a[3]), "no description"
        elif builder == "addInputTextConfigRow":
            key, st = a[1], store(a[3]) if len(a) > 3 else "SystemConf (default)"
            form = "password" if len(a) > 2 and a[2].strip() == "true" else "plain"
        elif builder == "addFileBrowser":
            key, st = a[1], store(a[3]) if len(a) > 3 else "SystemConf (default)"
        elif builder == "addInputTextRow":
            st, form = "caller's onsave", "password" if len(a) > 2 and a[2].strip() == "true" else "plain"
        elif builder == "addWithDescription":
            menu = receiver.startswith("mMenu") or receiver.startswith("menu")
            if not menu and len(a) <= 4 and (len(a) < 4 or a[3].strip() in ("true", "false")):
                form = "GuiSettings comp form: multiLine = true"
            elif len(a) >= 7:
                form = "func form: multiLine = %s" % a[6].strip()
            else:
                form = "%s func form: multiLine = false" % ("MenuComponent" if menu else "GuiSettings")
        keylit = literal(key) if key != "-" else None
        rows.append((name, line, builder, lab, keylit if keylit is not None else key, st, form))
        totals[builder] = totals.get(builder, 0) + 1

print("| Site | Builder | Label | Key | Store | Form |")
print("| --- | --- | --- | --- | --- | --- |")
for r in rows:
    print("| `%s:%d` | %s | %s | `%s` | %s | %s |" % tuple(x.replace("|", "\\|") if isinstance(x, str) else x for x in r))
print()
print("calls %d: %s" % (len(rows), ", ".join("%s %d" % kv for kv in sorted(totals.items()))))
EXPECT = {}
if len(sys.argv) > 4:
    EXPECT = dict((k, int(v)) for k, v in (kv.split("=") for kv in sys.argv[4].split(",")))
bad = ["%s %d, expected %d" % (k, totals.get(k, 0), v) for k, v in EXPECT.items() if totals.get(k, 0) != v]
if bad:
    print("FAIL t31-rows: " + "; ".join(bad))
    sys.exit(1)

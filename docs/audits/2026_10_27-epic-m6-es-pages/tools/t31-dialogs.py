"""Every GuiMsgBox( site in T31's slice, read whole, with where back lands (#678, Q1).

    python3 -I t31-dialogs.py <es worktree> <commit> <paths.txt> [--expect N]

Each site's argument list is read by balanced parentheses (strings, chars and
comments skipped), never by a window of lines. The buttons are the string
arguments in GuiMsgBox's name slots (es-core/src/guis/GuiMsgBox.h at the
commit: text, name1, func1[, name2, func2[, name3, func3]][, icon]); a site
with only the text gets the header's default name1 "OK" and a null func1.

Where back lands is GuiMsgBox's own rule (GuiMsgBox.cpp:116-134 at the pin):
one button -> that button; else the first button whose upper-cased text is
_("OK") or _("NO"); else the last button. The rule is asserted against the
source at the commit, so a change to it fails this tool rather than leaving a
stale table.

Output: one row per site -- file:line, the message's first words, the buttons
in order, the landing, and the landing's callback as written (cut at 60
characters) -- then the totals. Exits 1 when the site count differs from
--expect (default 50) or the accelerator rule no longer reads as above.
"""
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from t31lib import call_args, in_comment_or_string, show as _show  # noqa: E402

args = sys.argv[1:]
expect = 50
if "--expect" in args:
    i = args.index("--expect")
    expect = int(args[i + 1])
    del args[i:i + 2]
tree, commit, paths_file = args[:3]

def show(path):
    return _show(tree, commit, path)

rule = show("es-core/src/guis/GuiMsgBox.cpp")
if not re.search(r'if\(mButtons\.size\(\) == 1\)\s*\{\s*mAcceleratorFunc = mButtons\.front\(\)->getPressedFunc\(\);', rule) \
        or 'toUpper((*it)->getText()) == _("OK") || Utils::String::toUpper((*it)->getText()) == _("NO")' not in rule \
        or "mAcceleratorFunc = mButtons.back()->getPressedFunc();" not in rule:
    print("FAIL t31-dialogs: GuiMsgBox's accelerator rule is not the one this tool models")
    sys.exit(1)

def label(expr):
    m = re.fullmatch(r'_\("((?:[^"\\]|\\.)*)"\)', expr)
    if m:
        return m.group(1)
    m = re.fullmatch(r'"((?:[^"\\]|\\.)*)"', expr)
    if m:
        return m.group(1)
    return "<" + expr + ">"

def message(expr):
    lits = re.findall(r'"((?:[^"\\]|\\.)*)"', expr)
    words = " ".join(lits).replace("\\n", " ").split()
    return (" ".join(words[:7]) + (" ..." if len(words) > 7 else "")) if words else "<" + expr[:50] + ">"

ICON = re.compile(r"^(GuiMsgBoxIcon::)?ICON_\w+$")
rows, by_landing = [], {}
for path in [l.strip() for l in open(paths_file) if l.strip()]:
    src = show(path)
    for m in re.finditer(r"\bGuiMsgBox\s*\(", src):
        # skip a match inside a comment or a string: rescan the line's prefix
        if in_comment_or_string(src, m.start()):
            continue
        a, _end = call_args(src, src.index("(", m.start()))
        line = src.count("\n", 0, m.start()) + 1
        rest = a[2:]
        if rest and ICON.match(rest[-1]):
            rest = rest[:-1]
        names, funcs = [], []
        if not rest:
            names, funcs = ["OK"], ["nullptr"]
        else:
            for k in range(0, len(rest), 2):
                names.append(label(rest[k]))
                funcs.append(rest[k + 1] if k + 1 < len(rest) else "nullptr")
        # GuiMsgBox drops an empty name2/name3
        kept = [(n, f) for n, f in zip(names, funcs) if n != ""]
        if len(kept) == 1:
            land = kept[0]
        else:
            land = next(((n, f) for n, f in kept if n.upper() in ("OK", "NO")), kept[-1])
        fn = re.sub(r"\s+", " ", land[1])
        rows.append((path.rsplit("/", 1)[1], line, message(a[1] if len(a) > 1 else ""), " / ".join(n for n, _ in kept), land[0], fn[:60] + ("..." if len(fn) > 60 else "")))
        by_landing[land[0]] = by_landing.get(land[0], 0) + 1

print("| Site | Message (first words) | Buttons in order | Back lands on | Its callback |")
print("| --- | --- | --- | --- | --- |")
for f, l, msg, buttons, land, fn in rows:
    print("| `%s:%d` | %s | %s | %s | `%s` |" % (f, l, msg.replace("|", "\\|"), buttons, land, fn.replace("|", "\\|")))
files = len({r[0] for r in rows})
print()
print("sites %d in %d files; back lands on: %s" % (len(rows), files, ", ".join("%s %d" % kv for kv in sorted(by_landing.items(), key=lambda kv: -kv[1]))))
if len(rows) != expect:
    print("FAIL t31-dialogs: %d sites, expected %d" % (len(rows), expect))
    sys.exit(1)

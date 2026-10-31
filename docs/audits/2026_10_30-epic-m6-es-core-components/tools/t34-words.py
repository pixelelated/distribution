"""02 § The words (#681): every `_("` in the 80 at the pin with its French from
the catalog at the pin (asserted: 22 lines in 12 files, 27 occurrences, 17
distinct msgids, each with a non-empty msgstr), the player text outside `_()`
the read found, and the up-casing formatters (L-18; seven, the read's `:358` among them), each cited line asserted.
    t34-words.py <ES worktree> [paths file]"""
import os, re, subprocess, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from t34lib import PIN, COMP, die, show, paths

W = sys.argv[1]
AT = None  # stage E: `t34-words.py <tree> --at <ref>` prints only the counts at that ref, asserting each msgid has French there
if len(sys.argv) > 3 and sys.argv[2] == "--at":
    AT = sys.argv[3]; files = paths(None)
else:
    files = paths(sys.argv[2] if len(sys.argv) > 2 else None)
po = subprocess.run(["git", "-C", W, "show", (AT or PIN) + ":locale/lang/fr/LC_MESSAGES/emulationstation2.po"], capture_output=True, check=True).stdout.decode("utf-8")

def unq(s):
    return bytes(s, "utf-8").decode("unicode_escape").encode("latin-1").decode("utf-8")
cat, cur, key = {}, None, None
for line in po.split("\n"):
    m = re.match(r'^(msgid|msgstr) "(.*)"$', line)
    if m:
        key = m.group(1)
        if key == "msgid":
            cur = {"msgid": m.group(2), "msgstr": ""}
        else:
            cur["msgstr"] = m.group(2)
    elif line.startswith('"') and cur is not None and key:
        cur[key] += line[1:-1]
    elif not line.strip() and cur is not None and "msgstr" in cur and key == "msgstr":
        cat[cur["msgid"]] = cur["msgstr"]; cur, key = None, None
if cur is not None and key == "msgstr":
    cat[cur["msgid"]] = cur["msgstr"]
rx = re.compile(r'_\("((?:[^"\\]|\\.)*)"\)')
lines, occ, per = [], 0, {}
for f in files:
    for n, l in enumerate(show(W, f, AT or PIN).split("\n"), 1):
        if '_("' in l:
            ids = rx.findall(l)
            lines.append(("%s:%d" % (f[len(COMP):], n), ids))
            occ += l.count('_("'); per[f] = per.get(f, 0) + 1
distinct = sorted({i for _, ids in lines for i in ids})
if AT:
    missing = [i for i in distinct if not cat.get(i)]
    if missing:
        die("msgids with no French at %s: %s" % (AT, missing))
    print("t34-words --at %s: _(\" lines %d in %d files, %d occurrences, %d distinct msgids, each with French there; per file: %s" % (
        AT[:10], len(lines), len(per), occ, len(distinct), ", ".join("%s %d" % (f[len(COMP):], per[f]) for f in sorted(per))))
    sys.exit(0)
for what, have, want in [("_(\" lines", len(lines), 22), ("files", len(per), 12), ("occurrences", occ, 27), ("distinct msgids", len(distinct), 17)]:
    if have != want:
        die("%s: %d, expected %d" % (what, have, want))
for i in distinct:
    if not cat.get(i):
        die("msgid %r has no French at the pin" % i)
if cat.get("up/down") != "haut/bas" or cat.get("SWITCH TAB") != "CHANGER D’ONGLET":
    die("the catalog's up/down or SWITCH TAB no longer reads as the brief says")
OUT = [  # (file, line, must hold, the text, disposition)
 ("SliderComponent.cpp", 282, 'ss << "Auto"', '`"Auto"`, the AUTO sentinel\'s value text', "**3.7:** neither `_()` nor the placeholder `AUTO` (`es-ui-style-guide.md:164`); upstream's line; the contained fix `_(\"AUTO\")` with its French in the same commit; G-09 if an auto slider is reachable; S4 `a9017ff50` (#1316): `_(\"AUTO\")`, 3.7 PASS after, FAIL before"),
 ("RatingComponent.cpp", 265, '"add star"', "`\"add star\"`, the rating's OK prompt", "**L-23 (new):** a help label outside `_()`, English under every language; upstream's line; contained under rule 6; S4 `a9017ff50` (#1317): `_(\"ADD STAR\")` with `AJOUTER UNE ÉTOILE`, PL-10's case PASS after, FAIL before"),
]
FMT = [  # (file, line, must hold, the formatter)
 ("MenuComponent.cpp", 205, "toUpper", "`addWithLabel`'s label (the brief's `addGroup`; corrected by the seat, read at `:197`)"),
 ("MenuComponent.cpp", 233, "toUpper", "`addWithDescription`'s label, with a description"),
 ("MenuComponent.cpp", 236, "toUpper", "`addWithDescription`'s label, without one"),
 ("MenuComponent.cpp", 283, "toUpper", "`setTitle`"),
 ("MenuComponent.cpp", 358, "toUpper(Utils::FileSystem::getFileName(text))", "`setSubTitle`, through `getFileName`: a subtitle with a `/` keeps only what follows the last one (L-26)"),
 ("MenuComponent.cpp", 487, "toUpper", "`addButton`'s name"),
 ("ButtonComponent.cpp", 73, "toUpper", "the button's text"),
]
for f, n, must, *_ in OUT + FMT:
    if must not in show(W, COMP + f).split("\n")[n - 1]:
        die("%s:%d no longer holds %r" % (f, n, must))
print("**The 22 `_(\"` lines** (each msgid's French read from `locale/lang/fr/LC_MESSAGES/emulationstation2.po` at the pin):")
print()
print("| Line | msgid -> French |")
print("| --- | --- |")
for k, ids in lines:
    print("| `%s` | %s |" % (k, "; ".join("`%s` -> `%s`" % (i, cat[i]) for i in ids)))
print()
print("**Player text outside `_()`:**")
print()
print("| Site | Text | Disposition | proved |")
print("| --- | --- | --- | --- |")
for f, n, must, text, disp in OUT:
    print("| `%s:%d` | %s | %s | tree |" % (f, n, text, disp))
print()
print("**L-01:** `ComponentList.cpp:568`'s `_(\"up/down\")` is an icon key, not a label: the catalog translates it (`haut/bas`), `InputConfig::buttonLabel` returns it unchanged (`es-core/src/InputConfig.cpp:353-366`, T35's), and `HelpComponent::getIconTexture`'s `ICON_PATH_MAP` has no such key (`:190-194`): a null icon and `Unknown help icon \"haut/bas\"` under French on every settings list. The fork's own key sites write it untranslated (`ComponentTab.cpp:341`, `ComponentGrid.cpp:546-550`). The contained fix drops the `_()`; whether the catalog's orphan `msgid \"up/down\"` stays is one of the four rows put to the pause.")
print()
print("**L-18, the up-casing formatters** (D-WORKFLOW-144: the brand is never upper-cased through a formatter; a reading, not a check -- a `tools/vocabulary-check` rule is proposed in § The leads):")
print()
print("| Site | What it upper-cases |")
print("| --- | --- |")
for f, n, must, what in FMT:
    print("| `%s:%d` | %s |" % (f, n, what))
print()
print("Generated, asserted by `tools/t34-words.py`: %d `_(\"` lines in %d files, %d occurrences, %d distinct msgids, each with a non-empty French `msgstr` at the pin; %d player texts outside `_()`; %d formatters; every cited line asserted to hold its code." % (len(lines), len(per), occ, len(distinct), len(OUT), len(FMT)))

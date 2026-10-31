"""02 § The words: every `_("` line in the 96 with its msgids and the French catalog's entry (#682, D-UI-051, D-UI-022).

    python3 -I t35-words.py <es worktree> <commit> <paths.txt> [lines=N files=N occurrences=N msgids=N fr_missing=N glyph_lines=N plural_calls=N]

Lines are `git grep -F '_("'`'s rule; occurrences count every `_("` on a line; a msgid is
the C string literal inside, unescaped as xgettext reads it. The French entry is read from
`locale/lang/fr/LC_MESSAGES/emulationstation2.po` at the same commit (outside the 96,
read as data). The fork's own read for the tiers and the verbs is a word list over the
msgids (`es-player-text.md` § Conventions).
"""
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from t35lib import Ctx, table  # noqa: E402

c = Ctx(sys.argv, "t35-words.py <es worktree> <commit> <paths.txt> [key=value ...]")
S = "es-core/src/"
LIT = re.compile(r'_\("((?:[^"\\]|\\.)*)"\)')


def unescape(s):
    return s.encode("latin-1", "backslashreplace").decode("unicode_escape") if "\\" in s else s


def po(path):
    """Every entry as {(ctx, msgid): {"str": s, "plural": id_plural, "strs": [s0, s1, ...]}}."""
    import subprocess
    r = subprocess.run(["git", "-C", c.W, "show", f"{c.ref}:{path}"], capture_output=True, text=True)
    if r.returncode:
        c.fail.append(f"{path} not at {c.ref}")
        return {}
    out, e, key = {}, {}, None

    def flush():
        if "id" in e:
            out[(e.get("ctx"), e["id"])] = {"str": e.get("str", ""), "plural": e.get("plural"), "strs": [e[k] for k in sorted(k for k in e if k.startswith("str["))]}

    for line in r.stdout.split("\n") + [""]:
        m = re.match(r'^(msgctxt|msgid_plural|msgid|msgstr(?:\[\d+\])?) "(.*)"$', line)
        if m:
            k = {"msgctxt": "ctx", "msgid": "id", "msgid_plural": "plural", "msgstr": "str"}.get(m.group(1)) or m.group(1).replace("msgstr", "str")
            e[k] = unescape(m.group(2))
            key = k
        elif line.startswith('"') and key:
            e[key] += unescape(line[1:-1])
        elif not line.strip():
            flush()
            e, key = {}, None
    return out


PO = po("locale/lang/fr/LC_MESSAGES/emulationstation2.po")
FR = {k[1]: v["str"] for k, v in PO.items() if k[0] is None}
lines = c.grep(r'_\("')
cnt = {"lines": len(lines), "files": len({p for p, _, _ in lines}), "occurrences": 0, "msgids": 0, "fr_missing": 0, "glyph_lines": 0, "plural_calls": 0}
seen, rows, missing = {}, [], []
TIER = re.compile(r"\b(BACK ?UP|BACKUP|RESTORE|SYNC|SAVES?|SETTINGS|CLOUD|ROMS?|BIOS|UPLOAD|ARCHIVE|CONFIGURATIONS?|WI-?FI)\b", re.I)
for p, n, t in lines:
    occ = t.count('_("')
    cnt["occurrences"] += occ
    ids = [unescape(m) for m in LIT.findall(t)]
    if len(ids) != occ:
        c.fail.append(f"{p}:{n}: {occ} occurrences, {len(ids)} literals parsed")
    for i in ids:
        seen.setdefault(i, []).append(f"{p.replace(S, '')}:{n}")
    fr = [FR.get(i) for i in ids]
    for i, f in zip(ids, fr):
        if not f:
            missing.append(i)
    tiers = sorted({m.group(1).upper() for i in ids for m in TIER.finditer(i)})
    rows.append([f"`{p.replace(S, '')}:{n}`", " / ".join(f"`{i}`" for i in ids).replace("\n", "\\n"),
                 " / ".join(f"`{f}`" if f else "**--**" for f in fr).replace("\n", "\\n"),
                 ", ".join(tiers) or "--", "tree"])
cnt["msgids"] = len(seen)
cnt["fr_missing"] = len(set(missing))
glyph = c.grep(r"\\uF[0-9A-Fa-f]{3}")
cnt["glyph_lines"] = len(glyph)
PL = []
for p, n, t in c.grep(r"\b(ngettext|pgettext)\("):
    if "LocaleES" in p or p.endswith("gettext.h"):
        continue
    m1 = re.search(r'pgettext\("([^"]*)", "((?:[^"\\]|\\.)*)"\)', t)
    m2 = re.search(r'ngettext\("((?:[^"\\]|\\.)*)", "((?:[^"\\]|\\.)*)"', t)
    if m1:
        e = PO.get((m1.group(1), unescape(m1.group(2))))
        PL.append([f"`{p.replace(S, '')}:{n}`", f"`pgettext` `{m1.group(1)}` / `{m1.group(2)}`", f"`{e['str']}`" if e and e["str"] else "**--**", "tree"])
    elif m2:
        e = PO.get((None, unescape(m2.group(1))))
        fr = " / ".join(f"`{x}`" for x in e["strs"]) if e and e["strs"] else "**--**"
        PL.append([f"`{p.replace(S, '')}:{n}`", f"`ngettext` `{m2.group(1)}` / `{m2.group(2)}`", fr, "tree"])
    else:
        PL.append([f"`{p.replace(S, '')}:{n}`", "`pgettext` with a runtime key (xgettext cannot see it; the `fake_gettext_*` macros above exist so it can)", "--", "tree"])
cnt["plural_calls"] = len(PL)
cnt["plural_fr_missing"] = sum(1 for r in PL if r[2] == "**--**")
print(f"**The French catalog:** `locale/lang/fr/LC_MESSAGES/emulationstation2.po` at the pin, {len(FR)} entries parsed (context-less).\n")
print(table(["Site", "msgid(s)", "French", "Tier or verb words", "proved:"], rows))
print(f"\n**msgids without a French entry:** {', '.join(sorted(f'`{m}`' for m in set(missing))) or 'none'}.")
gp = c.need(S + "guis/GuiInputConfig.cpp", 134, r'_\("GAMEPAD %i"\)\.c_str\(\), target->getDeviceId\(\) \+ 1')
print(f"\n**`GAMEPAD %i`** (`guis/GuiInputConfig.cpp:134`): French `{FR.get('GAMEPAD %i', '--')}`; the argument is `getDeviceId() + 1`, the SDL instance id, not the seat (L-17, 3.21).")
print("\n**The glyph literals** (`\\uF...`, outside `_()`; `es-ui-style-guide.md` § Glyphs): " + ", ".join(f"`{p.replace(S, '')}:{n}`" for p, n, _ in glyph) + f" -- {len(glyph)} lines: the twelve notifications carry the light-gun `\\uF05B`, the wheel `\\uF1B9` or the pad `\\uF11B` with one space (a notification's single space) and the song `\\uF028` with two; the rest are the keyboard's key faces (DEL `\\uF177`, OK `\\uF058` or the multi-line `\\uF149`, and the shift and alt keys).")
tiered = sum(1 for r in rows if r[3] != "--")
cnt["tiered"] = tiered
print(f"\n**The fork's read for the tiers and the verbs:** {tiered} of the {len(rows)} lines carry a tier or a verb word of D-UI-022's (the column above), so the slice's strings sit outside the cloud vocabulary and owe it nothing. **The sentence-case dialogs are upstream's** (the description dialect, `es-ui-style-guide.md` § Text): recorded, not changed.")
print("\nThe `ngettext` and `pgettext` lines in the 96 outside `LocaleES` and `gettext.h`, with the catalog's context and plural entries:\n")
print(table(["Site", "Call", "French", "proved:"], PL))
c.finish("t35-words", cnt, f"{cnt['lines']} lines in {cnt['files']} files, {cnt['occurrences']} occurrences, {cnt['msgids']} msgids, {cnt['fr_missing']} without French; {cnt['glyph_lines']} glyph lines; {cnt['plural_calls']} `pgettext`/`ngettext` lines, {cnt['plural_fr_missing']} without French")

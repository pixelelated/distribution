#!/usr/bin/env python3
"""T26 (#673): which one-line `_("...")` literals of GuiMenu.cpp have French.

    python3 -I t26-french.py <pin.cpp> <fr .po>

The literals are the brief's own pattern, `_\\("[^"]*"\\)`, so a literal
carrying an escaped quote is not among them (the count says so beside it).
A msgid matches when its text, escapes as written, equals the literal's;
the .po's continuation lines are joined. French means a non-empty msgstr
on an entry not marked fuzzy. Prints the counts and every literal without
French.
"""
import re, sys
src = open(sys.argv[1], encoding="utf-8").read()
lits = sorted(set(re.findall(r'_\("([^"]*)"\)', src)))
escaped = len(set(re.findall(r'_\("((?:[^"\\]|\\.)*)"\)', src))) - len(lits)

po = {}; fuzzy = set()
entry = {}; field = None; flags = ""
def flush():
    global entry, flags
    if "msgid" in entry and entry["msgid"]:
        po[entry["msgid"]] = entry.get("msgstr", "")
        if "fuzzy" in flags:
            fuzzy.add(entry["msgid"])
    entry = {}; flags = ""
for line in open(sys.argv[2], encoding="utf-8"):
    line = line.rstrip("\n")
    if not line.strip():
        flush(); field = None; continue
    if line.startswith("#,"):
        flags += line
        continue
    if line.startswith("#"):
        continue
    m = re.match(r'(msgid|msgstr|msgctxt|msgid_plural|msgstr\[\d+\])\s+"(.*)"$', line)
    if m:
        if m.group(1) == "msgid" and "msgid" in entry:
            flush()
        field = m.group(1); entry[field] = m.group(2); continue
    m = re.match(r'"(.*)"$', line)
    if m and field:
        entry[field] += m.group(1)
flush()
have = [l for l in lits if po.get(l) and l not in fuzzy]
missing = [l for l in lits if l not in have]
print("%d unique one-line literals (the brief's pattern; %d more with an escaped quote)" % (len(lits), escaped))
print("%d with French, %d fuzzy among them, %d without" % (len(have), len([l for l in lits if l in fuzzy]), len(missing)))
for l in missing:
    print("  without French:", l[:100])

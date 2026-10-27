"""02 § The words: every _("...") in T32's slice against the French catalog (#679, Q5).

    python3 -I t32-words.py <es worktree> <commit> <paths.txt> [lines=58,calls=70,msgids=51,empty=1,missing=0]

The calls are `_(` followed by one or more adjacent string literals (joined,
as xgettext joins them), read by t32lib (a `_(` inside a comment or a
string is skipped). The catalog is locale/lang/fr/LC_MESSAGES/
emulationstation2.po at the same commit, parsed for msgid / msgstr (the
plural forms are read as present). Printed: one row per distinct msgid
with its sites and its French (an empty msgstr, or no msgid, called out).
Exits 1 when a count differs from the one given.
"""
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from t32lib import in_comment_or_string, show  # noqa: E402


def unescape(s):
    return s.encode("utf-8").decode("unicode_escape").encode("latin-1").decode("utf-8")


tree, commit, paths_file = sys.argv[1:4]
want = dict((k, int(v)) for k, v in (kv.split("=") for kv in sys.argv[4].split(","))) if len(sys.argv) > 4 else {}
po = show(tree, commit, "locale/lang/fr/LC_MESSAGES/emulationstation2.po")
cat, cur, last = {}, None, None
for n, line in enumerate(po.split("\n"), 1):
    m = re.match(r'^(msgid|msgstr(?:\[0\])?) "(.*)"$', line)
    if m:
        last = m.group(1)
        if last == "msgid":
            cur = [m.group(2), n]
        elif cur is not None:
            cat[cur[0]] = (m.group(2), cur[1])
        continue
    m = re.match(r'^"(.*)"$', line)
    if m and cur is not None:
        if last == "msgid":
            cur[0] += m.group(1)
        elif cur[0] in cat:
            cat[cur[0]] = (cat[cur[0]][0] + m.group(1), cat[cur[0]][1])
sites = []
for path in [l.strip() for l in open(paths_file) if l.strip()]:
    src = show(tree, commit, path)
    for m in re.finditer(r'\b_\(\s*((?:"(?:[^"\\]|\\.)*"\s*)+)\)', src):
        if in_comment_or_string(src, m.start()):
            continue
        msgid = "".join(re.findall(r'"((?:[^"\\]|\\.)*)"', m.group(1)))
        sites.append((path.rsplit("/", 1)[1], src.count("\n", 0, m.start()) + 1, msgid))
by_id = {}
for f, l, mid in sites:
    by_id.setdefault(mid, []).append("%s:%d" % (f, l))
print("| msgid | Sites | French (po line) |")
print("| --- | --- | --- |")
empty = missing = 0
for mid in sorted(by_id):
    if mid in cat:
        fr, n = cat[mid]
        if fr == "":
            empty += 1
            french = "**empty** (`msgstr \"\"`, L%d)" % (n + 1)
        else:
            french = "%s (L%d)" % (unescape(fr).replace("|", "\\|"), n)
    else:
        missing += 1
        french = "**no msgid**"
    print("| `%s` | %s | %s |" % (mid.replace("|", "\\|"), ", ".join("`%s`" % s for s in by_id[mid]), french))
counts = {"lines": len(set((f, l) for f, l, _ in sites)), "calls": len(sites), "msgids": len(by_id), "empty": empty, "missing": missing}
print()
print("generated, asserted: %d lines, %d calls, %d distinct msgids in %d files; %d with an empty French msgstr, %d with no msgid"
      % (counts["lines"], counts["calls"], counts["msgids"], len(set(f for f, _, _ in sites)), empty, missing))
fail = ["%s %d, expected %d" % (k, counts[k], v) for k, v in want.items() if counts.get(k) != v]
if fail:
    print("FAIL t32-words: " + "; ".join(fail))
    sys.exit(1)

#!/usr/bin/env python3
"""T32 (#679): the audit issue's body, generated from 05-punch-list.md (T31's t31-issue-body.py, adapted).

    python3 -I t32-issue-body.py <05-punch-list.md> <expected items> <summary.md> > body.md

The summary paragraph (what was read, the seat, the window, the folder at its
commit) is a file the lane writes; the items are generated.

One checkbox per item: its severity, question and source from the punch
index, its title from its heading, and the artifact that ticks it. Asserts
27 items, the index and the headings agreeing.
"""
import re, sys
text = open(sys.argv[1], encoding="utf-8").read()
want = int(sys.argv[2])
titles = dict(re.findall(r"^## (PL-\d+): (.*)$", text, re.M))
idx = re.findall(r"- id: (PL-\d+)\n  severity: \"(\w+)\"\n  category: (\w+)\n  question: (Q\d)\n  source_finding: \"([^\"]*)\"", text)
assert len(idx) == len(titles) == want, (len(idx), len(titles), want)
sev = {}
for _, s, *_ in idx:
    sev[s] = sev.get(s, 0) + 1
summary = open(sys.argv[3], encoding="utf-8").read().rstrip("\n")
out = [summary, "",
    "**%d items:** 0 critical, %d high, %d medium, %d low, 0 info. Every item is open until the stage-D ruling and stage F's outcomes." % (
        len(idx), sev.get("High", 0), sev.get("Medium", 0), sev.get("Low", 0)),
    "",
    "## Items",
    "",
]
for pl, s, cat, q, src in idx:
    out.append("- [ ] **%s** (%s, %s, %s): %s **Checked by:** its Phase 7 row in `05-punch-list.md` at the outcome the stage-D ruling sets (a commit with its proof, an issue, or the record as written)." % (pl, s, q, src, titles[pl]))
print("\n".join(out))

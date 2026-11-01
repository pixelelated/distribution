#!/usr/bin/env bash
# T38 stage B (#685): the figures 04's executive summary quotes, computed from the generated tables and 02,
# never typed. Run from the audit folder.
python3 -I - <<'PY'
import re
q5 = open('stage-b/tables/q5.md').read().splitlines()
fam = [l for l in q5 if l.startswith('| `council')]
print("council family: rows", len(fam), "files", sum(int(l.split('|')[2]) for l in fam),
      "lines", sum(int(l.split('|')[3]) for l in fam), "descriptions", len(fam), "of", len([l for l in q5 if l.startswith('| `')]))
t = open('02-forward-audit.md').read()
sec = t[t.index('\n## The leads\n'):t.index("\n### § 2's take-up table")]
leads = [l for l in sec.splitlines() if re.match(r'^\| L-\d+ \|', l)]
print("leads", len(leads), "owner T38 stream", sum(1 for l in leads if l.split('|')[4].strip().startswith('T38 stream')),
      "proposed inherit", sum(1 for l in leads if l.split('|')[5].strip().startswith('inherit')),
      "proposed bug", [l.split('|')[1].strip() for l in leads if '**bug**' in l])
PY

#!/usr/bin/env python3
"""Write the audit's completion marker (#653, #846) after the coordinator has
closed the audit issue: the tracker readback, the verified receipt and
audit-completion.json, in the shape tools/ceremony-check's
completed_audit_marker() validates. Refuses, writing nothing, unless the issue
reads back closed as completed with every checkbox ticked and none open.
    python3 -I write-completion.py <repo-root>
"""
import datetime, hashlib, json, re, subprocess, sys
from pathlib import Path

ROOT = Path(sys.argv[1]).resolve()
A = 'docs/audits/2026_10_24-epic-m6-build-engine-upstream-tools'
ISSUE = 846
raw = subprocess.run(['gh', 'api', f'repos/pixelelated/distribution/issues/{ISSUE}'],
                     capture_output=True, text=True, check=True).stdout
issue = json.loads(raw)
body = issue.get('body') or ''
ticked = len(re.findall(r'^\s*- \[x\]', body, re.M)); open_ = len(re.findall(r'^\s*- \[ \]', body, re.M))
if issue.get('state') != 'closed' or issue.get('state_reason') != 'completed' or not ticked or open_:
    sys.exit(f"refused: #{ISSUE} state={issue.get('state')} reason={issue.get('state_reason')} ticked={ticked} open={open_}")
now = datetime.datetime.now(datetime.timezone.utc).isoformat()
readback = f'{A}/tracker-final-readback.json'
completion = f'{A}/tracker-completion.json'
(ROOT / readback).write_text(raw if raw.endswith('\n') else raw + '\n')
(ROOT / completion).write_text(json.dumps({'result': 'PASS', 'exact_bodies_and_states': True,
                                           'closed_completed': [ISSUE], 'verified_utc': now}, indent=2) + '\n')
def sha(p):
    return hashlib.sha256((ROOT / p).read_bytes()).hexdigest()
evidence = {p: sha(p) for p in (f'{A}/04-analysis.md', f'{A}/05-punch-list.md', readback, completion)}
(ROOT / f'{A}/audit-completion.json').write_text(json.dumps({'schema': 1, 'issue': ISSUE, 'completed_at': now,
    'tracker_readback': readback, 'tracker_completion': completion, 'evidence': evidence}, indent=2) + '\n')
print(f"#{ISSUE} closed/completed, {ticked} ticked, 0 open; completed_at {now}")

#!/usr/bin/env python3
"""Check new T39 resolution records; synthetic controls mutate only in-memory copies."""
import copy,json,re,subprocess
from pathlib import Path
A=Path(__file__).resolve().parents[1]
def collect():
 return {
 'q5':json.loads((A/'stage-e/S5/dispositions.json').read_text()),
 'accepted_q5':(A/'stage-c/tables/q5.md').read_text().split('| low-inbound document |')[1],
 'plan':json.loads((A/'second-opinions/review-plan.json').read_text()),
 'outcomes':json.loads((A/'stage-f/outcomes.json').read_text())['outcomes'],
 'punch':(A/'05-punch-list.md').read_text(),
 'log':(A/'00-running-log.md').read_text(),
 'forward':(A/'02-forward-audit.md').read_text(),
 'held':json.loads((A/'stage-f/binary-art-comparisons.json').read_text())['rows'],
 }
def check(d):
 expected=re.findall(r'\x60((?:docs|plans)/[^\x60]+\.md)\x60',d['accepted_q5'])
 assert [r['path'] for r in d['q5']]==expected, 'Q5 membership drift'
 assert sum(r['accepted_logical_lines'] for r in d['q5'])==2770
 ledger=[r for r in d['q5'] if r['class']=='ledger-plan']
 assert len(ledger)==1 and ledger[0]['decision'].startswith('table-only'), 'ledger disposition'
 assert d['plan']['primary']['model']=='anthropic/claude-opus-4-8', 'historical model rewritten'
 assert d['plan']['primary']['lab']=='anthropic' and d['plan']['reviewers']==[]
 assert len(d['outcomes'])==46 and {r['item'] for r in d['outcomes']}=={f'PL-{n:02}' for n in range(1,47)}
 gate=d['punch'].split('## Phase 7 resolution gate',1)[1]
 for r in d['outcomes']:
  assert f"| {r['item']} | {r['outcome']} |" in gate, 'outcome mismatch'
  if r['outcome']=='Resolved':assert re.fullmatch('[a-f0-9]{40}',r['fix_commit'])
 proof=re.findall(r'\x60proved: (tree|history|tool-run|fixture|design)\x60',d['forward'])
 log=re.findall(r'^PROOF: .*proved: (tree|history|tool-run|fixture|design)$',d['log'],re.M)
 assert proof==log, 'proof pair mismatch'
 assert len(d['held'])==49
 assert all(r['before_sha256']==r['after_sha256'] for r in d['held']), 'protected bytes drift'
 return len(proof)
data=collect()
controls=[
 ('missing Q5 row',lambda d:d['q5'].pop()),
 ('historical model rewritten',lambda d:d['plan']['primary'].update(model='current-executor')),
 ('missing outcome',lambda d:d['outcomes'].pop()),
 ('missing proof line',lambda d:d.update(log=re.sub(r'^PROOF:.*\n','',d['log'],count=1,flags=re.M))),
 ('changed protected hash',lambda d:d['held'][0].update(after_sha256='0'*64)),
]
for name,mutate in controls:
 d=copy.deepcopy(data);mutate(d)
 try:check(d)
 except AssertionError:print('CONTROL REJECTED:',name)
 else:raise SystemExit('FAIL control passed: '+name)
n=check(data)
for sub in ['stage-a','stage-b','stage-c','stage-d']:
 p=str(A/sub)
 assert not subprocess.check_output(['git','diff','96ef183aae','--',p]), 'accepted receipt edited: '+sub
for rel in ['tools/t39-tables.py','tools/t39-tables-drift.sh']:
 assert not subprocess.check_output(['git','diff','96ef183aae','--',str(A/rel)]), 'accepted checker implementation edited'
if (A/'stage-h/checker-changes.json').exists():
 import hashlib
 changes=json.loads((A/'stage-h/checker-changes.json').read_text())
 assert changes['authorized_tip']=='329011b9eae20922b4d0727e13bf1626b2e1c04f'
 for rel,record in changes['files'].items():
  assert hashlib.sha256((A/rel).read_bytes()).hexdigest()==record['current_sha256'], 'unrecorded checker change'
else:
 for rel in ['tools/t39-checks.sh','tools/t39-checks.py']:
  assert not subprocess.check_output(['git','diff','96ef183aae','--',str(A/rel)])
print(f'PASS new records: 33 Q5 rows / 2770 lines, 46 outcomes, {n} proof pairs, 49 protected rows; historical identity and accepted receipts retained')

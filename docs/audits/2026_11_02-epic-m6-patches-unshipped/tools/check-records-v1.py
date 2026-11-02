#!/usr/bin/env python3
"""Check new D records against retained source receipts; reruns no A-C producer."""
import collections,gzip,hashlib,json,pathlib,re
R=pathlib.Path(__file__).resolve().parents[1]
def read(p):return json.loads((R/p).read_text())
def sha(b):return hashlib.sha256(b).hexdigest()
rows=read('stage-b/table-input.json');keys={x['path'] for x in rows};assert len(rows)==len(keys)==432
text=(R/'02-forward-audit.md').read_text()
for title,next_title in [('Provenance','Coverage'),('Coverage','Configuration inputs (12)')]:
 part=text.split('## '+title+'\n',1)[1].split('## '+next_title+'\n',1)[0]
 paths=[s.split(' | ')[0][2:] for s in part.splitlines() if s.startswith('| projects/')]
 assert len(paths)==432 and set(paths)==keys,(title,len(paths))
assert len(read('stage-b/recipes.json'))==31 and len(read('stage-b/plans.json'))==114
assert len(read('stage-b/configurations.json'))==12
opened=read('stage-b/open-inputs.json');assert len(opened)==len({x['path'] for x in opened})==93
assert all(x['owner'] and x['application'] and x['receipts'] for x in opened)
calls=[];native=[];paths=set()
for folder in ['application','application-overlay']:
 d=R/'stage-b'/folder
 for p in d.glob('G[0-9][0-9][0-9].json'):
  for row in json.loads(p.read_text()).get('rows',[]):
   if not row.get('normal_called'):continue
   n=row['normal'];assert n['exit']==0 and row['promoted']
   stem=p.stem+'-'+str(row['index']).zfill(3)
   assert sha((d/(stem+'.stdout')).read_bytes())==n['stdout_sha256']
   assert sha((d/(stem+'.stderr')).read_bytes())==n['stderr_sha256']
   calls.append(row['status'])
   if row['native']:native.append(row['status']);paths.add(row['path'])
summary=read('stage-b/table-summary.json')
assert len(calls)==779 and len(native)==600 and len(paths)==333
assert dict(collections.Counter(calls))==summary['normal_calls_including_context']
assert dict(collections.Counter(native))==summary['normal_native_calls']
assert (summary['open_native_paths'],summary['mixed_native_paths'],summary['wholly_open_native_paths'])==(93,6,87)
controls=read('stage-c/table-controls.json');assert [x['exit'] for x in controls]==[1,1,1,1,0]
for x in controls:
 f=pathlib.Path(x['argv'][2]);b=f.read_bytes()
 assert sha(b)==x['fixture_sha256'] and sha(gzip.decompress(b))==x['decoded_input_sha256']
 assert sha(pathlib.Path(x['argv'][1]).read_bytes())==x['producer_sha256']
# Bind the unmodified generated table prefix before the later analysis append.
prefix=text.split('\n## Proof classification',1)[0]
expected=controls[-1]['rendered_output_before_analysis_append_sha256']
assert any(sha(prefix.rstrip('\n').encode()+b'\n'*n)==expected for n in range(5)), 'generated table prefix changed'
forward=re.findall(r'proved:\s*(P\d+)\s+(\S+)',text)
log=re.findall(r'PROOF:\s*(P\d+)\s+(\S+)',(R/'00-running-log.md').read_text())
record=read('stage-c/proof-agreement.json')
assert forward==log and len(forward)==14 and [list(x) for x in forward]==record['forward']
plan=read('second-opinions/review-plan.json')
assert plan['depth']=='local' and plan['reviewers']==[] and plan['primary']['lab']=='openai'
assert list((R/'second-opinions').iterdir())==[R/'second-opinions/review-plan.json']
issues=read('stage-d/live-issues.json')
assert issues['audit_body_equal'] and issues['slice_body_unchanged_from_A']
assert issues['audit']['body']==(R/'stage-d/audit-issue-body.md').read_text()
print('PASS new D record integrity: 432/432 tables; 31 recipes/114 plans/12 configs; 779 actual normal exits and output hashes; 600 native calls/333 paths; 93 open keys; retained exact fixture/program identities; 14 proof pairs; Local identity; live tracker custody')

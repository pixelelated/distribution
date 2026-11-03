from prooflib import *
print('FULL STREAM/ERRATA\n'+(P/'full-streams.txt').read_text())
register=blob('docs/decision-register.md',ROOT).decode()
for line in register.splitlines():
 if line.startswith('| D-WORKFLOW-233 ') or line.startswith('| D-WORKFLOW-234 '):print('DECISION',line)
print('BRIEF HASH',sha((P/'full-brief.txt').read_bytes()))
m=json.loads(ext('MANIFEST.json'));bad=[];read={}
for name,v in m['members'].items():
 b=ext(name);read[name]=b
 if len(b)!=v['bytes'] or sha(b)!=v['sha256']:bad.append(name)
assert len(m['members'])==126
(P/'external-verification.json').write_text(json.dumps(dict(manifest_sha256=sha((P/'external-MANIFEST.json').read_bytes()),members=len(read),bytes=sum(map(len,read.values())),mismatches=bad,names=list(read)),indent=2)+'\n')
print('EXTERNAL',len(read),sum(map(len,read.values())),'MISMATCHES',bad)
print('EXTERNAL JSON NAMES',[n for n in read if n.endswith('.json')])
for name in ['stage-e/owner-outcomes.json','stage-e/owner-outcome-controls.json','stage-e/input-manifest.json','stage-f/retirement-controls-v2.json','stage-h/plan-summary.json','stage-h/retirement-result.json','stage-h/closing-census.json']:
 x=j(A+name);print('\nSHAPE',name,json.dumps(shape(x,2),ensure_ascii=True)[:6500])
print('MANIFEST OTHER FIELDS',json.dumps({k:v for k,v in m.items() if k!='members'},indent=2))

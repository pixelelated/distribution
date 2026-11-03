import json,subprocess,hashlib,re,os
from pathlib import Path
p=Path('/tmp/m6-t46-records-proof-t5-20261103'); repo=Path('/workspace/tmp/m6-t46-proof-t5-20261103/repo'); ref='e9d512a230cf8dbd2cd985ae7984a6ef7eb9f9fc'; prep='docs/qa-logs/2026-11-03-m6-records-preparation/'
assert set(os.sched_getaffinity(0))==set(range(8,24))
receipts=[]
def get(path,save=False):
 q=subprocess.run(['git','show',ref+':'+path],cwd=repo,capture_output=True); receipts.append({'argv':q.args,'rc':q.returncode,'stdout_sha256':hashlib.sha256(q.stdout).hexdigest(),'stdout_bytes':len(q.stdout)}); assert q.returncode==0,q.stderr
 if save:
  dst=p/'inputs'/path.removeprefix(prep); dst.parent.mkdir(parents=True,exist_ok=True); dst.write_bytes(q.stdout)
 return q.stdout
def shape(d):
 if isinstance(d,dict):return {k:('list:'+str(len(v)) if isinstance(v,list) else 'dict:'+str(len(v)) if isinstance(v,dict) else v) for k,v in d.items()}
 if isinstance(d,list):return {'length':len(d),'first_shape':shape(d[0]) if d else None}
 return d
for n in ['p1-routes/retention.json','root-route-verification.json','reader-routes.json','t1-report.json','root-t39-bridge-verification.json']:
 d=json.loads((p/'inputs'/n).read_bytes());print('SHAPE',n,json.dumps(shape(d)))
 for k,v in (d.items() if isinstance(d,dict) else []):
  if isinstance(v,list) and v and isinstance(v[0],dict):print('ITEM SHAPE',k,json.dumps(shape(v[0])))
for n in ['p1-routes/routes.json','p1-routes/target-metadata.json','p1-routes/entrypoints.json','p1-routes/index-headers.json','p1-routes/structural-findings.json','p1-routes/documentary-groups.json','p1-routes/commands.json','p1-routes/owning-issue.json','p1-routes/reproduce.txt','p1-routes/SHA256SUMS','p1-routes/documentary-candidates.tsv.utf8.json','classify-routes.py']:
 b=get(prep+n,True)
 if n.endswith('.json'):
  d=json.loads(b);print('P1 SHAPE',n,json.dumps(shape(d))[:2200])
  if n.endswith('structural-findings.json'):print(json.dumps(d,indent=2)[:7000])
 elif n.endswith('classify-routes.py'):print('CLASSIFIER SOURCE\n',b.decode())
print('ACTUAL BRIEF INSTRUCTIONS')
for line in (p/'brief.stdout').read_text().splitlines():
 if any(s in line.lower() for s in ['lint','model','primary','timestamp','range','criteria','ownership','scope.json','full tracked','whitespace']):print(line)
print('TOOL INTERFACES')
for rec in json.loads((p/'inputs/tool-help.json').read_bytes()):print(json.dumps({'argv':rec['argv'],'exit':rec['exit'],'stdout_prefix':rec.get('stdout','')[:600],'stderr_prefix':rec.get('stderr','')[:160]}))
for file in ['tools/lint-audit-artifacts','tools/box-check','tools/work-log-index','tools/ceremony-check','tools/forbidden-terms-check']:
 src=get(file).decode(); lines=src.splitlines(); hits=set()
 for i,line in enumerate(lines):
  if re.search(r'primary|reviewers|models|MODELS|Local|LOCAL|--phase|pre-issue|--issue|add_argument|--gate|--write|--check|--stdin|Usage:|usage:',line):hits.update(range(max(0,i-1),min(len(lines),i+3)))
 print('SOURCE',file,'LINES',len(lines))
 for i in sorted(hits):print(str(i+1)+': '+lines[i])
print('RULE CHANGES SINCE PRIOR T43 ROOT')
q=subprocess.run(['git','diff','--name-only','f1000e157c2f0248820e1b77055e81521b079a3f',ref,'--','.claude/rules','AGENTS.md','CLAUDE.md'],cwd=repo,capture_output=True);print(q.stdout.decode());receipts.append({'argv':q.args,'rc':q.returncode,'stdout_sha256':hashlib.sha256(q.stdout).hexdigest()})
for rule in ['instruction-files.md','adversarial-council.md','worktrees.md']:
 print('APPLICABLE RULE',rule,'\n',get('.claude/rules/'+rule).decode())
(p/'command-06.json').write_text(json.dumps(receipts,indent=2)+'\n')

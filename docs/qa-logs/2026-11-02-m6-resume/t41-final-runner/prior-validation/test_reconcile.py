#!/usr/bin/env python3
"""Synthetic record controls for D226 reconciliation. No historical code executes."""
import copy, hashlib, json, pathlib as P, subprocess as S, sys
OWN=P.Path('/workspace/tmp/m6-coordinator/kit/selftest/accept-t41-candidate-01a19d12');ns={'__name__':'fixture_library'}
for file in ['t41_checks.py','t41_reconcile.py','t41_execution.py','t41_supplement.py']:
 text=(OWN/file).read_text().split("\nif __name__=='__main__':")[0];exec(compile(text,file,'exec'),ns)
sha=lambda b:hashlib.sha256(b).hexdigest()
F=OWN/'fixtures';state=json.loads((F/'state.json').read_text());inv=json.loads((F/'audit/stage-b/corrected/inventory-rows.json').read_text());RESULTS=[]
class Records:
 def __init__(self):self.fixture=True;self.af='audit';self.tip='f'*40;self.data={};self.refs={};self.inv=copy.deepcopy(inv)
 def put(self,path,b,refs=()):
  b=b.encode() if isinstance(b,str) else b;self.data[path]=b
  for ref in [self.tip,*refs]:self.refs.setdefault(ref,{})[path]=b
 def blob(self,path,ref=None):
  try:return self.refs[ref or self.tip][path]
  except KeyError:raise ns['Absent']('missing fixture immutable path '+path)
 def audit(self,p):
  try:return self.data[self.af+'/'+p]
  except KeyError:raise ns['Absent']('missing fixture record '+p)
 def tree(self,ref,path):
  return {p:'100644 blob '+sha(b) for p,b in self.refs.get(ref,{}).items() if not path or p==path or p.startswith(path.rstrip('/')+'/')}
 def inventory(self):return self.inv
 def corrected(self,p):return self.audit('stage-b/corrected/'+p)
 def co(self,p):return json.loads(self.corrected(p))

def setup():
 r=Records();a=ns['STAGE_A'];c=ns['STAGE_C'];b=ns['STAGE_B'];source=ns['SOURCE'];p1=ns['P1']
 for row in inv:
  p=row['path'].replace('\\u002d','-');raw=S.check_output(['git','-C',str(F/'repo'),'show',state['base']+':'+p]);r.put(p,raw,[p1,source,c])
 for name in ['slices','areas','inventory']:r.put('docs/reviews/'+name+'.json','{"synthetic":true}\n',[p1])
 block=('synthetic retained membership block\n'+'# synthetic\n'*147).encode();expected=('synthetic retained output\n'*99).encode()
 brief='<!-- t41 block.sh begin -->\n```bash\n'+block.decode()+'```\n<!-- t41 block.sh end -->\n<!-- t41 block expected begin -->\n```\n'+expected.decode()+'```\n<!-- t41 block expected end -->\n'
 brief+='F=$(git ls-tree -d --name-only 6ec78bbf8c\nd.pop("tier_exception",None)\ntools/lint-audit-artifacts "$L/pass/$F"\ntools/lint-audit-artifacts "$L/fail/$F"\n'
 r.put(ns['BRIEF'],brief,[ns['AUTH']])
 r.put('audit/stage-a/p1-qa-scratch/block.sh',block,[a])
 for p in ['block.out','block-tip.out','p1-qa-scratch/block-expected.txt']:r.put('audit/stage-a/'+p,expected,[a])
 paths='\n'.join(sorted(x['path'] for x in inv))+'\n'
 for side in ['p1','tip']:
  for name in ['paths','text']:r.put(f'audit/stage-a/{side}-qa-scratch/{name}.txt',paths,[a])
 combined="block rc=0\nblock at the tip rc=0\nblock = the brief's expected lines\nthe same lines at the tip\nt4 plan: local D-WORKFLOW-184 0\nlint, a Local plan, rc=0\nlint, tier_exception removed, rc=1\n"
 r.put('audit/stage-a/run/stage-a.out',combined,[a])
 r.put('tools/lint-audit-artifacts','synthetic unchanged historical lint bytes\n',[ns['STAGE_A_PROGRAM']])
 r.put(ns['T4_FOLDER']+'/second-opinions/review-plan.json',json.dumps(dict(depth='local',reviewers=[],tier_exception='D-WORKFLOW-184')),[ns['T4']])
 r.put('audit/stage-a/lint-local-pass.out','synthetic positive\nPASS\n',[a]);r.put('audit/stage-a/lint-local-fail.out','  FAIL  second-opinions/review-plan.json or its call evidence is invalid: local-only cannot satisfy Epic/Milestone\n1 CONTRACT FAILURE(S)\n',[a])
 program=b'# synthetic formal program bytes, never run\n';draft=b'# synthetic draft bytes, never run\n'
 r.put('audit/tools/t41-tables.py',program,[c]);r.put('audit/stage-b/corrected/t41-tables.py',draft,[b,c])
 checks=[]
 for kind,msg in zip(['drop','reach','header'],['membership: expected 107 rows','reach: expected shipped 103/test 4','From header census: expected 87']):
  output='negatives/'+kind+'.out';raw=('AssertionError: '+msg+'\n').encode();r.put('audit/stage-c/'+output,raw,[c]);args=['python3','-I','audit/tools/t41-tables.py','stats','--bytes-from' if kind=='header' else '--rows-from','/synthetic/bytes' if kind=='header' else '/synthetic/'+kind+'.json']
  checks.append(dict(name='formal-generator-negative-'+kind,argv=args,rc=1,output=output,sha256=sha(raw),start='synthetic UTC',elapsed_seconds=.01))
 for mode in ['stats','provenance','coverage','currency','json']:
  raw=('synthetic '+mode+'\n').encode();output='tables/'+mode+'.txt';r.put('audit/stage-c/'+output,raw,[c]);r.put('audit/stage-b/corrected/table-'+mode+'.txt',raw,[c]);checks.append(dict(name='formal-generator-'+mode,argv=['python3','-I','audit/tools/t41-tables.py',mode],rc=0,output=output,sha256=sha(raw),start='synthetic UTC',elapsed_seconds=.01))
 r.put('audit/stage-c/validation.json',json.dumps(dict(checked_program_sha256=sha(program),checks=checks,outputs_equal_accepted_tables=True)),[c])
 r.put('audit/stage-c/promotion.json',json.dumps(dict(formal_sha256=sha(program),draft_sha256=sha(draft))),[c])
 return r

def run(label,fn,expected,modify=None):
 r=setup()
 if modify:modify(r)
 try:msg=ns[fn](r);state='PASS'
 except Exception as e:state=type(e).__name__;msg=str(e)
 ok=state==expected;RESULTS.append(dict(label=label,ok=ok,state=state,reason=msg));print(('PASS' if ok else 'FAIL')+' TEST '+label+': '+state)

def changed_final(r,p):r.refs[r.tip][p]+=b'changed\n'
def changed_receipt(r,p):r.data[p]+=b'changed\n'
def mutate_validation(r,fn):
 p='audit/stage-c/validation.json';v=json.loads(r.data[p]);fn(v);r.put(p,json.dumps(v),[ns['STAGE_C']])

if __name__=='__main__':
 run('retained 99-line output changed','reconcile_membership','Invalid',lambda r:changed_receipt(r,'audit/stage-a/block-tip.out'))
 run('membership inputs changed at final tip','reconcile_membership','Invalid',lambda r:changed_final(r,'docs/reviews/slices.json'))
 run('selected source blob changed','reconcile_membership','Invalid',lambda r:changed_final(r,inv[0]['path']))
 run('membership reconciliation control','reconcile_membership','PASS')
 run('historical lint program changed','reconcile_lint','Invalid',lambda r:changed_final(r,'tools/lint-audit-artifacts'))
 run('later T4 edits do not rewrite the historical immutable input','reconcile_lint','PASS',lambda r:changed_final(r,ns['T4_FOLDER']+'/second-opinions/review-plan.json'))
 run('historical lint refusal changed','reconcile_lint','Invalid',lambda r:changed_receipt(r,'audit/stage-a/lint-local-fail.out'))
 run('historical Local proof reconciliation control','reconcile_lint','PASS')
 run('formal program changed','reconcile_generator','Invalid',lambda r:changed_final(r,'audit/tools/t41-tables.py'))
 run('formal output hash tamper','reconcile_generator','Invalid',lambda r:mutate_validation(r,lambda v:v['checks'][0].update(sha256='0'*64)))
 run('negative command falsely passed','reconcile_generator','Invalid',lambda r:mutate_validation(r,lambda v:v['checks'][1].update(rc=0)))
 run('negative ordering lost','reconcile_generator','Invalid',lambda r:mutate_validation(r,lambda v:v['checks'].reverse()))
 run('unknown negative fixture identity never passes','reconcile_generator','Absent')
 run('invented identity cannot auto-approve','reconcile_generator','Absent',lambda r:mutate_validation(r,lambda v:[x.update(input_identity='invented') for x in v['checks'][:3]]))
 (OWN/'checks-reconcile.json').write_text(json.dumps(RESULTS,indent=2)+'\n')
 bad=sum(not x['ok'] for x in RESULTS);print('RECONCILIATION TEST SUMMARY:',len(RESULTS)-bad,'passed,',bad,'failed');sys.exit(bool(bad))

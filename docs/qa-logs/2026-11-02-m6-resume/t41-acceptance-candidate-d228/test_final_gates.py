#!/usr/bin/env python3
"""Tiny synthetic Git/record fixtures for D226 executable seams. No real tools run.
Stubs enforce the READ tool interfaces, then final gates actually spawn them.
"""
import collections, hashlib, json, os, pathlib as P, re, shutil, subprocess as S, sys
OWN=P.Path('/workspace/tmp/m6-coordinator/kit/selftest/accept-t41-candidate-01a19d12')
F=OWN/'executable-fixtures';R=F/'repo';RESULTS=[]
TR='c9fe606e8d7e7e0f6c70cc686764d1503029d278'
ENV=dict(os.environ,GIT_CONFIG_NOSYSTEM='1',GIT_CONFIG_GLOBAL='/dev/null',GIT_AUTHOR_NAME='Codex synthetic',GIT_AUTHOR_EMAIL='codex-fixture@invalid',GIT_COMMITTER_NAME='Codex synthetic',GIT_COMMITTER_EMAIL='codex-fixture@invalid',GIT_AUTHOR_DATE='2026-11-02T00:00:00Z',GIT_COMMITTER_DATE='2026-11-02T00:00:00Z')
def write(p,b):
    assert p.absolute().is_relative_to(OWN) and p.resolve()==p.absolute()
    p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(b.encode() if isinstance(b,str) else b)
def js(p,v):write(p,json.dumps(v,indent=2)+'\n')
def git(*args):
    p=S.run(['git','-c','core.hooksPath=/dev/null','-c','commit.gpgsign=false','-C',str(R),*args],env=ENV,capture_output=True)
    if p.returncode:raise RuntimeError(repr(args)+p.stderr.decode())
    return p.stdout.decode().strip()
def commit(m):git('add','-A');git('commit','-qm','synthetic '+m+' #688');return git('rev-parse','HEAD')
STUB=r'''#!/usr/bin/python3
import sys,os,json,pathlib,re
root=pathlib.Path(__file__).resolve().parents[1];name=pathlib.Path(__file__).name;args=sys.argv[1:]
cfg=json.loads((root/'docs/fixture-control.json').read_text())
with open(pathlib.Path(os.environ['TMPDIR'])/'invocations.jsonl','a') as f:f.write(json.dumps([name,args,os.getcwd()])+'\n')
if cfg.get('fail')==name:print('synthetic command failure');sys.exit(cfg.get('rc',1))
if cfg.get('empty')==name:sys.exit(0)
if name=='lint-audit-artifacts':
 assert args in [['audit'],['audit','--issue','1408']],args
 if (root/'audit/resolution.txt').read_text().strip()!='resolved':print('PASS pre-issue artifacts (does not certify resolution)');sys.exit(0)
 print('PASS')
elif name=='rules-check':assert args==['--quiet']
elif name=='register-check':assert args==[];print('register-check: synthetic IDs each once')
elif name=='work-log-index':assert args==['--check'];print('work-log index: current')
elif name=='ceremony-check':
 assert args==['--gate']
 import subprocess
 for ref in ['next','upstream/next']:assert subprocess.run(['git','rev-parse','--verify',ref+'^{commit}'],capture_output=True).returncode==0
elif name=='hooks-test':
 assert args==[]
 tmp=pathlib.Path(os.environ['TMPDIR']);assert str(tmp).startswith('/workspace/tmp/m6-coordinator/kit/selftest/accept-t41-candidate-01a19d12/')
 (tmp/'synthetic-hook-proof').write_text('fixture only');print('PASS')
elif name=='box-check':assert len(args)==2 and args[0]=='--issue' and args[1].isdigit();print('box-check: 1 issue(s), 0 open checkbox(es), 0 fail, 0 issue(s) with rows to re-derive against')
elif name=='forbidden-terms-check':
 assert args in [[],['--stdin']]
 text=sys.stdin.read() if args else '\n'.join(p.read_text(errors='replace') for p in (root/'audit').rglob('*') if p.is_file())
 pattern=os.environ.get('FORBIDDEN_PATTERNS','fixture[ ]forbidden[ ]term');n=sum(bool(re.search(pattern,x,re.I)) for x in text.splitlines())
 if args:print('forbidden-terms-check: %d line(s) on stdin carry a listed word'%n if n else 'forbidden-terms-check: 0 hits on stdin')
 else:print('forbidden-terms-check: %d hits in tracked files'%n)
 sys.exit(1 if n else 0)
else:sys.exit(90)
'''
GH=r'''#!/usr/bin/python3
import pathlib,json,sys
p=pathlib.Path(__file__).with_name('gh-state.json');v=json.loads(p.read_text())
if v.get('sleep'):
 import time;time.sleep(v['sleep'])
if v.get('rc'):print('synthetic gh unavailable',file=sys.stderr);sys.exit(v['rc'])
if v.get('malformed'):print('not-json');sys.exit(0)
a=sys.argv[1:];assert a[0]=='api' and a[1].startswith('repos/pixelelated/distribution/issues/'),a
n=a[1].split('/')[4];assert n.isdigit()
if '/comments?' in a[1]:assert a[2:]==['--paginate','--slurp'];print(json.dumps([[{'id':1,'body':'synthetic comment'}]]))
else:assert len(a)==2;print(json.dumps({'number':int(n),'body':v.get('body','- [x] PL-01 Deferred #1409\n'),'state':'open'}))
'''
def setup():
 if F.exists():return json.loads((F/'state.json').read_text())
 R.mkdir(parents=True);git('init','-q')
 tools=['lint-audit-artifacts','rules-check','register-check','work-log-index','ceremony-check','box-check','forbidden-terms-check']
 for n in tools:
  write(R/'tools'/n,STUB);(R/'tools'/n).chmod(0o755)
 write(R/'.githooks/hooks-test',STUB);(R/'.githooks/hooks-test').chmod(0o755)
 write(R/'.githooks/secret-patterns',"SECRET_PATTERNS='devpassword=[A-Za-z0-9]{4,}'\n")
 write(R/'audit/05-punch-list.md','synthetic Phase 7 outcome');write(R/'audit/resolution.txt','resolved\n')
 js(R/'audit/second-opinions/review-plan.json',dict(depth='local',reviewers=[],tier_exception='D-WORKFLOW-184'))
 write(R/'audit/tools/t41-tables.py',"raise RuntimeError('accepted generator MUST NOT execute')\n")
 js(R/'docs/fixture-control.json',{})
 base=commit('fixture baseline');write(R/'docs/lane-record.md','synthetic lane record\n');tip=commit('lane')
 git('checkout','-q',base);write(R/'docs/coordinator-record.md','synthetic exact coordinator\n');coord=commit('coordinator');git('checkout','-q',tip)
 js(F/'fixture-refs.json',{TR:base});js(F/'state.json',dict(base=base,tip=tip,coord=coord))
 # Reader receipt paths; final tools must instead see exact Git checkout bytes.
 for p in (R/'audit').rglob('*'):
  if p.is_file():write(F/'audit'/p.relative_to(R/'audit'),p.read_bytes())
 js(F/'issues/1408.json',dict(number=1408,body='- [x] PL-01 Deferred #1409\n'))
 js(F/'issues/1409.json',dict(number=1409,body='- [ ] integration artifact\n'))
 js(F/'issues/688.json',dict(number=688,body='- [ ] final coordinator acceptance\n'))
 write(F/'bin/gh',GH);(F/'bin/gh').chmod(0o755);js(F/'bin/gh-state.json',{})
 return dict(base=base,tip=tip,coord=coord)

def run(label,sections,expected,state,tip=None,coord=None,extra=None):
 env=dict(ENV,DIST_REPO=str(R),DISPATCH_TIP=state['base'],AUDIT_ISSUE='1408',BUGS='1409',ACCEPT_FIXTURE_ROOT=str(F),ACCEPT_ONLY=sections,ACCEPT_DIR=str(OWN/'executable-runs'),OUT=str(OWN/'executable-runs.out'),PATH=str(F/'bin')+':/usr/bin:/bin')
 if extra:env.update(extra)
 p=S.run(['bash',str(OWN/'t41-accept.sh'),tip or state['tip'],coord or state['coord']],env=env,capture_output=True)
 text=p.stdout.decode();vs=re.findall(r'^VERDICT (PASS|FAIL|CANNOT|ABSENT|RAN) ([a-z-]+) -- (.*)$',text,re.M)
 counts=collections.Counter(x[0] for x in vs);summary='SUMMARY: pass %d, fail %d, cannot %d, absent %d, ran %d'%tuple(counts[x] for x in ['PASS','FAIL','CANNOT','ABSENT','RAN']);rc=1 if counts['FAIL'] else 2 if counts['CANNOT'] or counts['ABSENT'] else 0
 ok=len(vs)==len(sections.split()) and all(x[0]==expected for x in vs) and summary in text and p.returncode==rc and f'ACCEPT-RC {rc}' in text
 RESULTS.append(dict(label=label,ok=ok,verdicts=vs,rc=p.returncode));print(('PASS' if ok else 'FAIL')+' TEST '+label)
 if not ok:print(text[-2200:],p.stderr.decode()[:300])
 return vs

def change(label,section,expected,state,path,value):
 git('checkout','-q',state['tip']);write(R/path,value);tip=commit(label)
 try:run(label,section,expected,state,tip=tip)
 finally:git('checkout','-q',state['tip'])

def check_artifacts(state):
 records=list((OWN/'executable-runs').glob('final-gates-*/*.json'));parsed=[json.loads(p.read_text()) for p in records]
 good=bool(records)
 for p,v in zip(records,parsed):
  for kind in ['stdout','stderr']:
   b=(p.parent/v[kind]).read_bytes();good &= hashlib.sha256(b).hexdigest()==v[kind+'_masked_sha256']
  good &= P.Path(v['cwd']).is_relative_to(OWN) and 'elapsed_seconds' in v and 'rc' in v
 good &= any(v['argv'][:4]==['python3','-I','-m','py_compile'] for v in parsed)
 good &= any(v['label']=='integration-history-ref' and v['argv'][2]=='refs/remotes/upstream/next' for v in parsed)
 good &= any(v['label']=='integration-merge' and v['argv'][-1]==state['tip'] for v in parsed)
 good &= not any(v['argv'][0] in ['patch','tar'] or (v['argv'][0]=='python3' and v['argv'][1:4]!=['-I','-m','py_compile']) for v in parsed)
 RESULTS.append(dict(label='actual masked command/exit/hash and no-replay census',ok=bool(good)))
 print(('PASS' if good else 'FAIL')+' TEST actual receipt census')

if __name__=='__main__':
 st=setup()
 for ref in ['refs/heads/next','refs/remotes/upstream/next']:git('update-ref',ref,st['base'])
 # Fail-first on all new final seams; controls then execute the genuine interface.
 change('lint pre-issue is not resolution','lint','FAIL',st,'audit/resolution.txt','open\n')
 run('both resolution lint commands','lint','PASS',st)
 change('syntax error refused','generators','FAIL',st,'audit/tools/t41-tables.py','def broken(:\n')
 run('syntax only never executes raising producer','generators','PASS',st)
 for tool in ['register-check','rules-check','work-log-index','ceremony-check','hooks-test']:
  change(tool+' fails','checkers','FAIL',st,'docs/fixture-control.json',json.dumps({'fail':tool}))
 run('all new current checkers and six AC27 interfaces','checkers','PASS',st)
 change('forbidden new record','forbidden','FAIL',st,'docs/lane-record.md','fixture forbidden term\n')
 run('forbidden public positive then current records','forbidden','PASS',st)
 change('secret new record','secret','FAIL',st,'docs/lane-record.md','dev'+'password='+'QwErTyUiOpAsDfGh'+'\n')
 run('secret compilation positive and current records','secret','PASS',st)
 change('checkbox checker failure','lane-boxes','FAIL',st,'docs/fixture-control.json',json.dumps({'fail':'box-check'}))
 run('open inherited bug and lane are not premature closure requirements','audit-boxes bug-boxes lane-boxes','PASS',st)
 p=F/'issues/1408.json';b=p.read_bytes();js(p,dict(number=1408,body='- [ ] PL-01 unresolved\n'));run('unresolved audit outcome','audit-boxes','FAIL',st);write(p,b)
 change('reviewed tool changed','lint','CANNOT',st,'tools/lint-audit-artifacts',STUB+'\n# changed tool\n')
 # Exact immutable tips with a real tiny local merge; conflicts remain a failed gate.
 git('checkout','-q',st['base']);write(R/'docs/conflict.md','base\n');cb=commit('conflict base');write(R/'docs/conflict.md','lane\n');ct=commit('conflict lane')
 git('checkout','-q',cb);write(R/'docs/conflict.md','coordinator\n');cc=commit('conflict coordinator')
 run('simulated merge conflict','merge','FAIL',st,tip=ct,coord=cc);git('checkout','-q',st['tip'])
 run('exact coordinator simulation and post-merge checkers','merge','PASS',st)
 # Exercise gh through the same subprocess seam, with a synthetic executable.
 # Reader fixtures normally short-circuit live reads. Directly instantiate its
 # final gate for this narrowly targeted test, without real issue or repo access.
 namespace={'__name__':'fixture_library'}
 for file in ['t41_checks.py','t41_reconcile.py','t41_execution.py','t41_supplement.py']:
  src=(OWN/file).read_text();src=src.split("\nif __name__=='__main__':")[0];exec(compile(src,file,'exec'),namespace)
 os.environ.update(DIST_REPO=str(R),DISPATCH_TIP=st['base'],ACCEPT_FIXTURE_ROOT=str(F),ACCEPT_DIR=str(OWN/'executable-runs'),PATH=str(F/'bin')+':/usr/bin:/bin');sys.argv=['fixture',st['tip'],st['coord']]
 rr=namespace['Reader']();fg=namespace['FinalGates'](rr)
 for config,error,label in [({'rc':1},'Cannot','live issue command rc refuses'),({'malformed':True},'JSONDecodeError','live issue malformed JSON refuses')]:
  js(F/'bin/gh-state.json',config)
  try:fg.issues(688);ok=False
  except Exception as e:ok=type(e).__name__==error
  RESULTS.append(dict(label=label,ok=ok));print(('PASS' if ok else 'FAIL')+' TEST '+label)
 js(F/'bin/gh-state.json',{'sleep':2})
 try:fg.command('synthetic-timeout',['gh','api','repos/pixelelated/distribution/issues/688'],timeout=.02);ok=False
 except Exception as e:ok=type(e).__name__=='Cannot'
 RESULTS.append(dict(label='timed out command is CANNOT with receipt',ok=ok));print(('PASS' if ok else 'FAIL')+' TEST timeout receipt')
 saved=fg.env['PATH'];fg.env['PATH']=str(F/'missing-bin')
 try:fg.issues(688);ok=False
 except Exception as e:ok=type(e).__name__=='Cannot'
 fg.env['PATH']=saved;RESULTS.append(dict(label='missing executable is CANNOT with receipt',ok=ok));print(('PASS' if ok else 'FAIL')+' TEST missing executable')
 js(F/'bin/gh-state.json',{'body':'password='+'SyntheticValueForMask\n'})
 v=fg.issues(688);cs=fg.issues(688,True)
 ok=v['number']==688 and len(cs)==1
 evidence=b''.join(p.read_bytes() for p in fg.root.glob('*.stdout'))
 ok &= b'SyntheticValueForMask' not in evidence and b'password=***' in evidence
 RESULTS.append(dict(label='live issue/comments actual command and on-disk masking',ok=ok));print(('PASS' if ok else 'FAIL')+' TEST live issue positive and mask')
 js(F/'bin/gh-state.json',{})
 check_artifacts(st)
 js(OWN/'checks-final-gates.json',RESULTS)
 bad=sum(not x['ok'] for x in RESULTS);print('FINAL-GATE TEST SUMMARY:',len(RESULTS)-bad,'passed,',bad,'failed');sys.exit(bool(bad))

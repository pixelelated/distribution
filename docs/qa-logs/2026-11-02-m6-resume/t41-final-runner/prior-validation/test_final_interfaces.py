#!/usr/bin/env python3
"""ONLY synthetic Git/tool interfaces for executor/timeouts/append/whitespace.
No actual final gate, accepted producer, application or distribution merge runs.
Codex (GPT-6), /root, wN:p5, session01a19d12-1c5f-7022-8053-102f6a94b7fe.
"""
import copy,hashlib,json,os,pathlib as P,re,subprocess as S,tempfile
OWN=P.Path(__file__).parent;ns={'__name__':'fixture_library'}
for name in ['t41_checks.py','t41_reconcile.py','t41_execution.py','t41_supplement.py']:exec(compile((OWN/name).read_text().split("\nif __name__=='__main__':")[0],name,'exec'),ns)
ROOT=P.Path(tempfile.mkdtemp(prefix='interface-fixtures-',dir=OWN));RESULTS=[];DAY=ns['DAY_LOG'];INDEX=ns['LOG_INDEX'];sha=ns['sha']
SELF=dict(harness='Codex',model='GPT-6',effort='not exposed by this harness',session='01a19d12-1c5f-7022-8053-102f6a94b7fe',pane='wN:p5',identity_source='actual harness and recovered Herdr identity')
os.environ['ACCEPT_DIR']=str(ROOT/'receipts');os.environ['ACCEPT_EXECUTOR_JSON']=json.dumps(SELF)
ENV=dict(os.environ,GIT_CONFIG_GLOBAL='/dev/null',GIT_CONFIG_NOSYSTEM='1',GIT_CONFIG_COUNT='0',GIT_AUTHOR_NAME='Codex synthetic',GIT_AUTHOR_EMAIL='fixture@invalid',GIT_COMMITTER_NAME='Codex synthetic',GIT_COMMITTER_EMAIL='fixture@invalid')

def write(p,b):
 assert p.resolve()==p.absolute() and p.is_relative_to(OWN);p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(b.encode() if isinstance(b,str) else b)
def git(repo,*args,expect=(0,)):
 p=S.run(['git','-c','core.hooksPath=/dev/null','-c','commit.gpgsign=false','-C',str(repo),*args],env=ENV,capture_output=True);assert p.returncode in expect,(args,p.stderr);return p.stdout

def commit(repo):git(repo,'add','-A');git(repo,'commit','-qm','synthetic T41 interface #688');return git(repo,'rev-parse','HEAD').decode().strip()
class Read:
 def __init__(self,repo,base,coord,tip,accepted=None):self.repo=str(repo);self.dispatch=base;self.coord=coord;self.tip=tip;self.fixture=True;self.af='audit';self.accepted=accepted or base
 def git(self,*args,missing=False):
  assert args[0] in ['ls-tree','show','cat-file','merge-base','log','diff-tree','rev-parse'];return git(P.Path(self.repo),*args)
 def tree(self,ref,path):
  if ref==ns['STAGE_D']:ref=self.accepted
  raw=self.git('ls-tree','-rz',ref,*(['--',path] if path else []));return {x.split(b'\t',1)[1].decode():x.split(b'\t',1)[0].decode() for x in raw.split(b'\0') if x}
 def blob(self,path,ref=None):return self.git('show',(ref or self.tip)+':'+path)

STUB=r'''#!/usr/bin/python3
import pathlib,sys,json,time
root=pathlib.Path(__file__).resolve().parents[1];cfg=json.loads((root/'docs/control.json').read_text());args=sys.argv[1:]
if cfg.get('sleep'):time.sleep(.3)
if pathlib.Path(__file__).name=='forbidden-terms-check':
 assert args in [[],['--stdin']]
 if args:
  assert 'synthetic t41 sentinel' in sys.stdin.read();print('forbidden-terms-check: 1 line(s) on stdin carry a listed word');sys.exit(1)
 print('forbidden-terms-check: 0 hits in tracked files');sys.exit(0)
day=root/'docs/work-logs/2026_11-work_logs/2026_11_02-work_log.md';index=root/'docs/work-logs/INDEX.md'
rendered=b'# synthetic generated index\n'+b'\n'.join(x for x in day.read_bytes().splitlines() if x.startswith(b'## '))+b'\n'
assert args in [[],['--write'],['--check']]
if not args:sys.stdout.buffer.write(rendered)
elif args==['--write']:
 index.write_bytes(rendered)
 if cfg.get('wrong_index'):index.write_bytes(b'wrong index\n')
 if cfg.get('other_write'):(root/'docs/other.md').write_text('unrelated mutation\n')
 if cfg.get('day_write'):day.write_bytes(day.read_bytes()+b'changed\n')
 print('wrote docs/work-logs/INDEX.md')
else:sys.exit(0 if index.read_bytes()==rendered else 1)
'''
BASE=b'# Work log\n\n## 00:01 UTC -- base\n\nbase body\n'
def entry(title,body=None,blanks=1):return ('\n'*blanks+'## '+title+'\n\n'+(body or title)+'\n').encode()
A=entry('01:00 UTC -- coordinator');B=entry('02:00 UTC -- lane',blanks=2)
def tiny(label,change=None,config=None,whitespace=False):
 repo=ROOT/label/'repo';repo.mkdir(parents=True);git(repo,'init','-q')
 write(repo/DAY,BASE);write(repo/INDEX,b'base index\n');write(repo/'docs/other.md',b'common\n');write(repo/'docs/control.json',json.dumps(config or {}))
 for name in ['work-log-index','forbidden-terms-check']:write(repo/'tools'/name,STUB);(repo/'tools'/name).chmod(0o755)
 base=commit(repo);co=BASE+A;lane=BASE+B
 if change:co,lane=change(co,lane)
 write(repo/DAY,co);write(repo/INDEX,b'coordinator index\n')
 if label=='other-conflict':write(repo/'docs/other.md',b'coordinator\n')
 coord=commit(repo);git(repo,'checkout','-q','--detach',base)
 write(repo/DAY,lane);write(repo/INDEX,b'lane index\n')
 if label=='other-conflict':write(repo/'docs/other.md',b'lane\n')
 accepted=base;headers=[]
 if whitespace:
  for tail in ['01-research-notes.md','stage-a/order.out','stage-a/run/stage-a-extra.out','stage-a/run/stage-a.out']:write(repo/'audit'/tail,b'accepted original with space \n')
  accepted=commit(repo)
  for root in ['stage-f/generator-input-proof','stage-f/generator-input-proof-attempt-1']:
   path='audit/'+root+'/fixtures/bytes/projects/example/header.patch';headers.append(path);write(repo/path,b'X-Proof-From: synthetic\ncontext \n')
 tip=commit(repo) if whitespace else commit(repo)
 r=Read(repo,base,coord,tip,accepted)
 if whitespace:r.d228_headers={p:r.tree(tip,p)[p] for p in headers}
 return r

def gate(r):return ns['FinalGates'](r)
def dest(f):
 d=f.root/'synthetic-clone';f.command('synthetic-clone',['git','clone','--quiet','--no-hardlinks','--template=',f.r.repo,str(d)])
 f.command('synthetic-checkout',['git','checkout','--quiet','--detach',f.r.coord],d);return d

def test(label,fn,expected='PASS'):
 try:
  details=fn();state='PASS';reason=''
 except Exception as e:state=type(e).__name__;reason=str(e);details=None
 ok=state==expected;RESULTS.append(dict(label=label,ok=ok,state=state,reason=reason,details=details));print(('PASS' if ok else 'FAIL')+' TEST '+label+': '+state,flush=True)

def append_case(label,change=None,config=None):
 r=tiny(label,change,config);f=gate(r);d=dest(f);_,rc=f.command('synthetic-merge',['git','merge','--no-commit','--no-ff',r.tip],d,expect=(0,1));assert rc==1,'fixture must produce real Git conflicts'
 f.merge_worklogs(d);raw=(d/DAY).read_bytes();assert raw.startswith(BASE) and b'<<<<<<<' not in raw
 record=json.loads((f.root/'append-merge.json').read_bytes());assert record['merged_sha256']==sha(raw) and record['executor']==SELF
 assert git(d,'diff','--name-only','--diff-filter=U')==b''
 return dict(receipt=str(f.root/'append-merge.json'),merged_sha256=sha(raw))

test('append two independent complete entries',lambda:append_case('append-good'))
test('append shared identical entry preserves both orders',lambda:append_case('append-shared',lambda a,b:(a+entry('03:00 UTC -- shared'),b+entry('03:00 UTC -- shared'))))
test('unrelated conflict refused',lambda:append_case('other-conflict'), 'Invalid')
test('changed base body refused',lambda:append_case('nonappend',lambda a,b:(a.replace(b'base body',b'edited body'),b)), 'Invalid')
test('partial append refused',lambda:append_case('partial',lambda a,b:(a,BASE+b'\npartial text\n')), 'Invalid')
test('same heading different body refused',lambda:append_case('duplicate-heading',lambda a,b:(a,BASE+entry('01:00 UTC -- coordinator','different'))), 'Invalid')
test('append order cycle refused',lambda:append_case('cycle',lambda a,b:(a+entry('04:00 UTC -- x')+entry('05:00 UTC -- y'),b+entry('05:00 UTC -- y')+entry('04:00 UTC -- x'))), 'Invalid')
test('index tool unrelated write refused',lambda:append_case('other-write',config={'other_write':True}), 'Invalid')
test('index tool day mutation refused',lambda:append_case('day-write',config={'day_write':True}), 'Invalid')
test('index render/write mismatch refused',lambda:append_case('wrong-index',config={'wrong_index':True}), 'Invalid')

r=tiny('metadata');f=gate(r);d=dest(f)
def metadata():
 f.command('metadata-positive',['git','rev-parse','HEAD'],d)
 p=next(f.root.glob('*-metadata-positive.json'));v=json.loads(p.read_bytes());assert v['executor']==SELF and v['tool_author']==ns['TOOL_AUTHOR'] and v['timeout_seconds']==120 and v['elapsed_seconds']>=0 and v['rc']==0 and v['fixture']
 assert 'identity' not in v
 return dict(receipt=str(p),sha256=sha(p.read_bytes()))
test('actual executor separate from tool author',metadata)
def missing():
 saved=os.environ.pop('ACCEPT_EXECUTOR_JSON')
 try:gate(r)
 finally:os.environ['ACCEPT_EXECUTOR_JSON']=saved
test('missing executor is CANNOT',missing,'Cannot')
def identity(raw,fixture=True):
 saved=os.environ['ACCEPT_EXECUTOR_JSON'];old=r.fixture;os.environ['ACCEPT_EXECUTOR_JSON']=raw;r.fixture=fixture
 try:
  f=gate(r);assert f.executor==ns['ROOT_EXECUTOR'];return 'root metadata accepted without executing a command'
 finally:os.environ['ACCEPT_EXECUTOR_JSON']=saved;r.fixture=old
test('root observed identity configuration only',lambda:identity(json.dumps(ns['ROOT_EXECUTOR']),False))
test('author cannot masquerade as final executor',lambda:identity(json.dumps(SELF),False),'Invalid')
test('executor metadata missing pane refused',lambda:identity(json.dumps({k:v for k,v in SELF.items() if k!='pane'})),'Invalid')
test('invalid executor JSON refused',lambda:identity('{bad'), 'JSONDecodeError')
def forbidden_timeout():
 f.record_paths=lambda:[];f.forbidden(d,whole=True)
 records=[json.loads(x.read_bytes()) for x in f.root.glob('*-forbidden-*.json')]
 assert {x['label']:x['timeout_seconds'] for x in records}=={'lane-forbidden-positive':120,'lane-forbidden-tree':1200}
 assert all(x['rc'] in [0,1] and x['elapsed_seconds']>=0 for x in records)
 return dict(receipts=[x['label'] for x in records])
test('only full tree scan gets bounded 1200s',forbidden_timeout)
test('unbounded timeout refused',lambda:f.command('bad-timeout',['git','status'],d,timeout=0),'Invalid')
test('excess timeout refused',lambda:f.command('bad-timeout',['git','status'],d,timeout=1201),'Invalid')
def timed():
 write(d/'docs/control.json','{"sleep":true}')
 try:f.command('synthetic-timeout',['tools/forbidden-terms-check'],d,timeout=.02)
 finally:
  v=json.loads(next(f.root.glob('*-synthetic-timeout.json')).read_bytes());assert v['timed_out'] and v['timeout_seconds']==.02 and v['elapsed_seconds']>=.02;write(d/'docs/control.json','{}')
test('timeout CANNOT retains bounded command receipt',timed,'Cannot')

def whitespace_case(label,alter=None,cached=False):
 r=tiny(label,whitespace=True)
 if alter:
  git(P.Path(r.repo),'checkout','-q','--detach',r.tip);alter(r,P.Path(r.repo));r.tip=commit(P.Path(r.repo))
 f=gate(r);d=dest(f);f.integration_whitespace(d)
 if cached:
  _,rc=f.command('synthetic-merge',['git','merge','--no-commit','--no-ff',r.tip],d,expect=(0,1))
  if rc:f.merge_worklogs(d)
  f.integration_whitespace(d,cached=True)
 paths=list(f.root.glob('*-full.json'));assert paths
 for path in paths:
  v=json.loads(path.read_bytes());assert v['rc']==2 and sha((f.root/v['raw_stdout']).read_bytes())==v['stdout_sha256'];assert sha((f.root/v['raw_stderr']).read_bytes())==v['stderr_sha256']
 receipt=json.loads((f.root/'whitespace-tips.json').read_bytes());assert len(receipt['excluded'])==6 and receipt['remaining_rc']==0
 return dict(receipts=[str(p) for p in paths],sha256=sha((f.root/'whitespace-tips.json').read_bytes()))
test('six bound whitespace records retain original rc2 and other paths rc0',lambda:whitespace_case('white-good',cached=True))
test('altered accepted whitespace record refused',lambda:whitespace_case('white-altered',lambda r,p:write(p/'audit/stage-a/order.out',b'changed original \n')),'Invalid')
test('altered D228 header whitespace refused',lambda:whitespace_case('white-header',lambda r,p:write(p/next(iter(r.d228_headers)),b'changed header \n')),'Invalid')
test('extra fixture whitespace refused',lambda:whitespace_case('white-extra-fixture',lambda r,p:write(p/'audit/stage-f/generator-input-proof/fixtures/extra.patch',b'new whitespace \n')),'Invalid')
test('nonfixture whitespace refused',lambda:whitespace_case('white-nonfixture',lambda r,p:write(p/'docs/unrelated.md',b'new whitespace \n')),'Invalid')
test('accepted record mode change refused',lambda:whitespace_case('white-mode',lambda r,p:(p/'audit/stage-a/order.out').chmod(0o755)),'Invalid')

out=ROOT/'checks-final-interfaces.json';out.write_text(json.dumps(RESULTS,indent=2)+'\n');bad=sum(not x['ok'] for x in RESULTS);print('FINAL INTERFACES',len(RESULTS)-bad,'passed,',bad,'failed',out,sha(out.read_bytes()));raise SystemExit(bool(bad))

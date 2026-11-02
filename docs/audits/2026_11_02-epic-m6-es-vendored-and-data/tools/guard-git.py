"""Tiny new Git fixture proves confinement receives actual per-commit raw diffs, including a reverted source edit."""
import pathlib,tempfile,subprocess,os,json,sys,importlib.util,datetime,hashlib
sys.dont_write_bytecode=True
A=pathlib.Path(__file__).resolve().parents[1]
s=importlib.util.spec_from_file_location('confinement',A/'tools/confinement.py');g=importlib.util.module_from_spec(s);s.loader.exec_module(g)
root=pathlib.Path(tempfile.mkdtemp(prefix='m6-t44-confinement-'));repo=root/'repo';repo.mkdir();g.D=repo
env=dict(os.environ,GIT_CONFIG_NOSYSTEM='1',GIT_CONFIG_GLOBAL='/dev/null',GIT_AUTHOR_NAME='T44 synthetic fixture',GIT_AUTHOR_EMAIL='fixture@example.invalid',GIT_COMMITTER_NAME='T44 synthetic fixture',GIT_COMMITTER_EMAIL='fixture@example.invalid',GIT_OPTIONAL_LOCKS='0')
events=[]
def run(*args):
    start=datetime.datetime.now(datetime.timezone.utc).isoformat();r=subprocess.run(['git','-C',str(repo),*args],capture_output=True,env=env)
    events.append(dict(argv=['git','-C',str(repo),*args],start=start,end=datetime.datetime.now(datetime.timezone.utc).isoformat(),rc=r.returncode,stdout=r.stdout.decode(),stderr=r.stderr.decode()));assert r.returncode==0;return r.stdout.decode().strip()
run('init','-q','--template=')
source='projects/ROCKNIX/packages/ui/emulationstation/package.mk';record=g.AUDIT+'synthetic-record.md'
for p in [source,record]:
    f=repo/p;f.parent.mkdir(parents=True,exist_ok=True);f.write_text('base\n')
run('add','--',source,record);run('commit','-qm','synthetic base');base=run('rev-parse','HEAD')
(repo/record).write_text('new audit record\n');run('add','--',record);run('commit','-qm','synthetic allowed record');positive=run('rev-parse','HEAD')
assert g.diff(base,positive)==[(record,'100644')];print('PASS tiny Git allowed audit commit')
(repo/source).write_text('planted source edit\n');run('add','--',source);run('commit','-qm','synthetic forbidden source');bad=run('rev-parse','HEAD')
try:g.diff(positive,bad)
except ValueError as e:assert str(e)=='FORBIDDEN_PATH:'+source;print('PASS tiny Git source commit refused:',e)
else:raise AssertionError('source commit accepted')
(repo/source).write_text('base\n');run('add','--',source);run('commit','-qm','synthetic restore source');tip=run('rev-parse','HEAD')
assert g.diff(base,tip)==[(record,'100644')]
refused=[]
for c in run('rev-list','--reverse',base+'..'+tip).splitlines():
    parent=run('show','-s','--format=%P',c)
    try:g.diff(parent,c)
    except ValueError as e:assert str(e).startswith('FORBIDDEN_PATH:');refused.append(c)
assert refused==[bad,tip]
print('PASS tiny Git per-commit guard rejects source edit and revert despite clean cumulative source')
out=A/'stage-c/tiny-git';out.mkdir(exist_ok=False)
receipt=dict(schema=1,private_scratch=str(root),fixture_contents={source:['base\n','planted source edit\n','base\n'],record:['base\n','new audit record\n']},base=base,positive=positive,bad=bad,tip=tip,rejected_commits=refused,events=events,program_sha256=hashlib.sha256(pathlib.Path(__file__).read_bytes()).hexdigest(),guard_sha256=hashlib.sha256((A/'tools/confinement.py').read_bytes()).hexdigest(),cpus=sorted(os.sched_getaffinity(0)),limits='Synthetic Git metadata only; no source copied, no live ref changed, no ES invocation; private tiny objects retained until authorized retirement')
(out/'receipt.json').write_text(json.dumps(receipt,indent=2)+'\n')
print('OWNED_PRIVATE_SCRATCH',root)

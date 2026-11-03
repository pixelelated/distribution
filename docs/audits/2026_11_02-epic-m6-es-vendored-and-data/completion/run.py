import datetime,hashlib,json,os,pathlib,subprocess,sys,time
R=pathlib.Path('/workspace/repos/pixelelated/distribution.worktrees/m6-es-vendored-and-data-691')
A=R/'docs/audits/2026_11_02-epic-m6-es-vendored-and-data'
def sha(b):return hashlib.sha256(b).hexdigest()
def now():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def run(out,cmd,inputs=(),timeout=120):
 out=pathlib.Path(out);out.mkdir(parents=True,exist_ok=False)
 env={**os.environ,'LC_ALL':'C','GIT_OPTIONAL_LOCKS':'0','PYTHONDONTWRITEBYTECODE':'1'}
 def g(*args):return subprocess.check_output(['git',*args],cwd=R,env=env)
 scope={}
 for f in sorted((A/'completion').rglob('*')):
  if f.is_file() and not f.is_symlink() and not f.is_relative_to(out):scope[str(f.relative_to(R))]=sha(f.read_bytes())
 for name in ['audit-completion.json','tracker-completion.json','tracker-final-readback.json']:
  f=A/name
  if f.exists():scope[str(f.relative_to(R))]=sha(f.read_bytes())
 (out/'scope.json').write_text(json.dumps(scope,indent=2)+'\n')
 bindings={}
 for name in inputs:
  f=pathlib.Path(name);f=f if f.is_absolute() else R/f;bindings[str(f)]={'sha256':sha(f.read_bytes()),'bytes':f.stat().st_size}
 rec={'argv':cmd,'cwd':str(R),'start':now(),'head':g('rev-parse','HEAD').decode().strip(),'index_entries_sha256':sha(g('ls-files','--stage','-z')),'inputs':bindings,'scope_sha256':sha((out/'scope.json').read_bytes()),'scope_limit':'current completion records before command; this output directory excluded; accepted baseline bound by immutable HEAD','runner_sha256':sha(pathlib.Path(__file__).read_bytes()),'cpus':sorted(os.sched_getaffinity(0)),'timeout_seconds':timeout,'executor':{'harness':'Codex','model':'openai/gpt-6-astra','effort':'xhigh','identity_source':'own observed Herdr footer; UI observation, not provider attestation','session':'01a19d12-1c5f-7022-8053-102f6a94b7fe','pane':'wN:p5'}}
 started=time.monotonic()
 try:
  p=subprocess.run(cmd,cwd=R,env=env,capture_output=True,timeout=timeout);rc,stdout,stderr=p.returncode,p.stdout,p.stderr
 except subprocess.TimeoutExpired as e:rc,stdout,stderr=124,e.stdout or b'',(e.stderr or b'')+b'\nTIMEOUT\n'
 for name,b in [('stdout',stdout),('stderr',stderr)]:(out/name).write_bytes(b);rec[name+'_sha256']=sha(b)
 rec.update(end=now(),elapsed_seconds=time.monotonic()-started,rc=rc)
 (out/'receipt.json').write_text(json.dumps(rec,indent=2)+'\n');print(json.dumps({'name':str(out),'rc':rc,'stdout_sha256':sha(stdout),'stderr_sha256':sha(stderr)}),flush=True);return rc
if __name__=='__main__':
 out=sys.argv[1];timeout=int(sys.argv[2]);split=sys.argv.index('--');sys.exit(run(out,sys.argv[split+1:],sys.argv[3:split],timeout))

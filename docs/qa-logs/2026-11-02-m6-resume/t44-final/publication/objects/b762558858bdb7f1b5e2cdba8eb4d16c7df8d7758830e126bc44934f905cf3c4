#!/usr/bin/env python3
"""Complete receipts for explicitly selected new T44 record commands."""
import argparse, datetime, hashlib, json, os, pathlib, subprocess, sys, time
def digest(b):return hashlib.sha256(b).hexdigest()
def now():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def main():
 p=argparse.ArgumentParser();p.add_argument('--repo',required=True);p.add_argument('--out',required=True);p.add_argument('--timeout',type=int,default=120);p.add_argument('--input',action='append',default=[]);p.add_argument('command',nargs=argparse.REMAINDER);a=p.parse_args()
 out=pathlib.Path(a.out);out.mkdir(parents=True,exist_ok=False)
 cmd=a.command[1:] if a.command[:1]==['--'] else a.command
 env={**os.environ,'LC_ALL':'C','GIT_OPTIONAL_LOCKS':'0','PYTHONDONTWRITEBYTECODE':'1'}
 def g(*args):return subprocess.check_output(['git',*args],cwd=a.repo,env=env)
 inputs={}
 for name in a.input:
  f=pathlib.Path(name);f=f if f.is_absolute() else pathlib.Path(a.repo)/f
  inputs[str(f)]={'sha256':digest(f.read_bytes()),'bytes':f.stat().st_size}
 # Bind current tracked and audit-untracked ordinary records without opening held paths.
 scope=[]
 for name in g('ls-files','-z').split(b'\0'):
  if not name:continue
  s=name.decode(); f=pathlib.Path(a.repo)/s
  if s.startswith(('docs/audits/2026_11_02-epic-m6-es-vendored-and-data/','.github/sessions/saved-session-state-feature-m6-es-vendored-and-data-691','docs/work-logs/2026_11-work_logs/2026_11_03','docs/retros/2026-11-03-m6-es-vendored-and-data')) and f.is_file() and not f.is_symlink():scope.append({'path':s,'sha256':digest(f.read_bytes())})
 (out/'input-scope.json').write_text(json.dumps(scope,indent=2)+'\n')
 rec={'argv':cmd,'cwd':a.repo,'inputs':inputs,'scope_sha256':digest((out/'input-scope.json').read_bytes()),'scope_note':'tracked ordinary T44 records before invocation; output directory excluded; explicit extra inputs above','head':g('rev-parse','HEAD').decode().strip(),'index_tree_before':g('write-tree').decode().strip(),'runner_sha256':digest(pathlib.Path(__file__).read_bytes()),'started_at':now(),'cpus':sorted(os.sched_getaffinity(0)),'executor':{'harness':'Codex','model':'openai/gpt-6-astra','effort':'xhigh','lane':'wN:p5','session':'01a19d12-1c5f-7022-8053-102f6a94b7fe','identity_source':'own observed Herdr footer; UI observation, not provider attestation'},'python':sys.version,'locale':'C','timeout_seconds':a.timeout}
 start=time.monotonic()
 try:
  result=subprocess.run(cmd,cwd=a.repo,env=env,capture_output=True,timeout=a.timeout);rc=result.returncode;stdout=result.stdout;stderr=result.stderr
 except subprocess.TimeoutExpired as e:rc=124;stdout=e.stdout or b'';stderr=(e.stderr or b'')+b'\nRECORD COMMAND TIMEOUT\n'
 (out/'stdout').write_bytes(stdout);(out/'stderr').write_bytes(stderr)
 rec.update(ended_at=now(),elapsed_seconds=time.monotonic()-start,rc=rc,stdout_sha256=digest(stdout),stderr_sha256=digest(stderr))
 (out/'receipt.json').write_text(json.dumps(rec,indent=2)+'\n')
 print(json.dumps({'out':str(out),'rc':rc,'stdout_sha256':digest(stdout),'stderr_sha256':digest(stderr)}));return rc
if __name__=='__main__':sys.exit(main())

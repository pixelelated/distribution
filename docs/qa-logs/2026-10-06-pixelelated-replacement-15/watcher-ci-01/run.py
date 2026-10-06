from pathlib import Path
import datetime,hashlib,json,os,subprocess,sys
owner=Path(__file__).resolve().parent;tree=owner/'tree'
assert not (owner/'qa.start').exists();(owner/'qa.start').write_text(datetime.datetime.now(datetime.timezone.utc).isoformat()+'\n')
(owner/'run.path').write_text(str(Path.cwd()/os.environ['RASTERATOPS_BUILD_RUN'])+'\n')
seal=json.loads((owner/'seal.json').read_text());result=1
try:
 for name,digest in seal.items():assert hashlib.sha256(Path(name).read_bytes()).hexdigest()==digest,name
 workflow=(tree/'.github/workflows/fork-checks.yml').read_text();assert 'python3 docs/qa-logs/2026-10-04-watch-progress/test-watch-build.py' in workflow;assert 'python3 docs/qa-logs/2026-10-03-watch-job/test-watch-build.py' not in workflow
 with (owner/'artifacts/routing.log').open('x') as f:
  process=subprocess.Popen(['python3',str(tree/'docs/qa-logs/2026-10-04-watch-progress/test-watch-build.py'),'--root',str(tree)],stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True)
  (owner/'artifacts/test.pid').write_text(str(process.pid)+'\n')
  for line in process.stdout:f.write(line);f.flush();print(line,end='',flush=True)
  result=process.wait()
 for name,digest in seal.items():assert hashlib.sha256(Path(name).read_bytes()).hexdigest()==digest,name
finally:
 (owner/'inner.rc').write_text(str(result)+'\n');(owner/'outer.rc').write_text(str(result)+'\n')
sys.exit(result)

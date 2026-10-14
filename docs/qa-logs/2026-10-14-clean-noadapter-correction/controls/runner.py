from pathlib import Path
import subprocess,json,time,os,resource
out=Path('/workspace/tmp/pix565-correction-controls-20261014-01');out.mkdir();start=time.time()
cmd=['python3','-I','-B','/tmp/pix565-noadapter-scrub-correction-20261014/candidate/tools/pixelelated-state-check-test','--self-test']
def limits():
 os.sched_setaffinity(0,{min(os.sched_getaffinity(0))});resource.setrlimit(resource.RLIMIT_AS,(1024**3,1024**3));resource.setrlimit(resource.RLIMIT_FSIZE,(16*1024**2,16*1024**2))
with (out/'stdout.json').open('xb') as so,(out/'stderr').open('xb') as se:
 p=subprocess.Popen(cmd,stdout=so,stderr=se,preexec_fn=limits);timed=False;signals=[]
 try:rc=p.wait(timeout=120)
 except subprocess.TimeoutExpired:
  timed=True;p.terminate();signals.append('TERM')
  try:rc=p.wait(timeout=5)
  except subprocess.TimeoutExpired:p.kill();signals.append('KILL');rc=p.wait(timeout=2)
j={'argv':cmd,'original_exit':rc,'timed_out':timed,'signals':signals,'elapsed_seconds':time.time()-start};(out/'result.json').write_text(json.dumps(j,indent=2)+'\n');print(json.dumps(j));raise SystemExit(0 if rc==0 and not timed else 1)

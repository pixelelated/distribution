import datetime,hashlib,json,os,subprocess,time
from pathlib import Path
o=Path(__file__).resolve().parent
m=json.loads((o/'inputs.json').read_text())
assert hashlib.sha256((o/'inputs/diagnostic.c').read_bytes()).hexdigest()==m['candidate_sha256']
args=['docker','run','--rm','--pull=never','--network=none','--read-only','--cpus=1','--memory=1g','--memory-swap=1g','--pids-limit=128','--cap-drop=ALL','--security-opt=no-new-privileges','--user',str(os.getuid())+':'+str(os.getgid()),'--tmpfs','/tmp:rw,nosuid,size=128m','--cidfile',str(o/'container.cid'),'-v',str(o/'inputs')+':/inputs:ro','-v',str(o/'out')+':/work:rw']
for r in m['trees']:args+=['-v',r['host']+'/toolchain:'+r['canonical']+'/toolchain:ro']
args+=[m['image'],'/bin/bash','/inputs/compile.sh']
start=time.monotonic(); result={'started':datetime.datetime.now(datetime.timezone.utc).isoformat(),'timeout':False}
try:
 with (o/'compiler.log').open('xb') as f:
  proc=subprocess.Popen(args,stdout=f,stderr=subprocess.STDOUT)
  result['docker_cli_pid']=proc.pid
  try:rc=proc.wait(timeout=180)
  except subprocess.TimeoutExpired:
   result['timeout']=True
   if (o/'container.cid').exists():
    cid=(o/'container.cid').read_text().strip()
    subprocess.run(['docker','kill',cid],timeout=15,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
   rc=proc.wait(timeout=30)
  result['original_docker_rc']=rc
except Exception as e:
 result['exception']=str(e);rc=125
result['seconds']=time.monotonic()-start
result['outputs']={p.name:{'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in (o/'out').iterdir() if p.is_file()}
result['status']='PASS' if rc==0 and not result['timeout'] and all('cloud-signin-window-'+r['device'] in result['outputs'] for r in m['trees']) else 'FAIL'
(o/'result.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result))
raise SystemExit(0 if result['status']=='PASS' else (rc or 1))

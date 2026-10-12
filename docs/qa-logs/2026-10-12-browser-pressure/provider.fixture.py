import subprocess,time,json
from pathlib import Path
import sys
r=Path(sys.argv[1]).resolve()
with (r/'provider-page.json').open('wb') as out,(r/'provider-stderr.txt').open('wb') as err:
 p=subprocess.Popen(['tools/signin-memory','10570','--url','https://www.dropbox.com/login','--seconds','90','--key',str(r/'qa-key'),'--json'],stdout=out,stderr=err)
 deadline=time.monotonic()+190
 try:
  for delay,name in [(20,'provider-20s'),(30,'provider-50s'),(25,'provider-75s')]:
   time.sleep(delay)
   if p.poll() is not None:break
   subprocess.run(['tools/vm-visual-qa','--monitor',str(r/'monitor.sock'),'shot',str(r/(name+'.png'))],check=True,timeout=25)
   print('Captured '+name,flush=True)
  rc=p.wait(timeout=max(1,deadline-time.monotonic()))
 except BaseException:
  p.terminate()
  try:p.wait(timeout=10)
  except subprocess.TimeoutExpired:p.kill();p.wait()
  raise
(r/'provider-result.json').write_text(json.dumps({'original_rc':rc})+'\n')
print('Provider diagnostic ended with rc '+str(rc),flush=True)
raise SystemExit(rc)

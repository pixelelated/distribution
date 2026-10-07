"""EXPLICIT execution entrypoint. Do not run until root approves launch."""
from pathlib import Path
from datetime import datetime,timezone
import json,os,subprocess,sys
owner=Path(__file__).resolve().parent
assert sys.argv[1:]==['--run'],'Review scripts and use --run only after coordinated launch approval'
assert not (owner/'controller-submission.json').exists() and not (owner/'controller-result.json').exists()
assert not os.environ.get('RASTERATOPS_BUILD_RUN')
def write(p,j):
 with p.open('x') as f:json.dump(j,f,indent=2);f.write('\n')
stamp=datetime.now(timezone.utc).isoformat()
write(owner/'controller-submission.json',{'utc':stamp,'submission_is_not_completion':True,'entrypoint':str(owner/'sequence.py')})
with (owner/'controller.log').open('xb',buffering=0) as log:
 child=subprocess.Popen([sys.executable,'-I',str(owner/'sequence.py')],cwd='/workspace/repos/rocknix',stdin=subprocess.DEVNULL,stdout=log,stderr=subprocess.STDOUT,start_new_session=True,close_fds=True)
write(owner/'controller-pid.json',{'pid':child.pid,'utc':stamp})
print(json.dumps({'state':'submitted','pid':child.pid,'owner':str(owner),'completion':str(owner/'controller-result.json'),'submission_is_not_completion':True}))

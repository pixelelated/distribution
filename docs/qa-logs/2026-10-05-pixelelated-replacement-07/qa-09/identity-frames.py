from pathlib import Path
import subprocess,sys,json,time
owner=Path('/workspace/tmp/pixelelated-m7-qa-09');phase=sys.argv[1]
for attempt in range(90):
 r=subprocess.run(['./tools/vm-pair','ssh','a','curl -sS -m 3 http://127.0.0.1:1234/isIdle'],capture_output=True,text=True)
 if r.returncode==0 and r.stdout.strip() and json.loads(r.stdout)==[True]:break
 time.sleep(1)
else:raise RuntimeError('ES did not reach idle')
v=['./tools/vm-visual-qa','--monitor','/tmp/rocknix-qemu-monitor.sock']
subprocess.run(v+['dismiss'],check=True)
subprocess.run(v+['run',str(owner/'identity.steps'),'--outdir',str(owner/'artifacts'/('identity-'+phase))],check=True)
print('CAPTURED '+phase+' actual identity/manual-update frames; semantic review required',flush=True)

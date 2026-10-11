from pathlib import Path
import importlib.util,sys,time,json,subprocess,hashlib
s=importlib.util.spec_from_file_location('v','/tmp/pix537-vm.py');v=importlib.util.module_from_spec(s);s.loader.exec_module(v)
lang,size=sys.argv[1:3];finish=len(sys.argv)>3 and sys.argv[3]=='finish';O=Path('/tmp/pix537-oauth21')/(lang[:2]+size);D=Path('/workspace/repos/rocknix.worktrees/m7-cloud-connections')
def state(want):
 for _ in range(150):
  a=json.loads(v.remote('cat /var/run/cloud_oauth/session.json'))
  if a.get('status')==want:return a
  time.sleep(.2)
 raise RuntimeError('authorization did not reach '+want)
def walk(label,steps):
 p=O/(label+'.steps');p.write_text(steps)
 subprocess.run([str(D/'tools/vm-visual-qa'),'--monitor',str(v.O/'monitor.sock'),'run',str(p),'--outdir',str(O/label)],check=True)
def fail():
 v.remote('touch /storage/qa537/oauth-fail');state('failed')
if not finish:
 subprocess.run(['python3','/tmp/pix537-oauth-prepare21.py',lang,size],check=True)
 walk('start',Path('/tmp/pix537-renew-start.steps').read_text());a=state('waiting')
 walk('phone',Path('/tmp/pix537-phone-choice.steps').read_text());fail()
 walk('failed',Path('/tmp/pix537-failed.steps').read_text())
 v.remote('rm -f /storage/qa537/oauth-fail')
 walk('retry',Path('/tmp/pix537-retry.steps').read_text())
else:a=json.loads((O/'first-state-private.json').read_text())
b=state('waiting');assert a['attempt']!=b['attempt'] and a['session']!=b['session']
walk('retry-phone',Path('/tmp/pix537-phone-choice.steps').read_text());fail()
walk('failed-again',Path('/tmp/pix537-failed.steps').read_text())
walk('cancelled','key right\nkey x\nwait-for-change\nsettle\nshot cancelled-return\n')
final=state('idle')
after=v.remote('sha256sum /storage/.config/rclone/rclone.conf /storage/.config/rclone/active-connection /storage/.config/cloud_sync.conf /storage/qa537/provider/save.srm')
assert after==(O/'before.sha256').read_text()
alive=v.remote("pgrep -f '^/usr/bin/python3 /usr/bin/rclone authorize' >/dev/null && echo alive || echo ended").strip();assert alive=='ended'
(O/'result.json').write_text(json.dumps({'fresh_attempt':a['attempt']!=b['attempt'],'fresh_session':a['session']!=b['session'],'fresh_pin':a.get('pin')!=b.get('pin'),'cancelled_status':final['status'],'authorize_child_ended':alive=='ended','unchanged_hashes':after.splitlines(),'es_sha256':v.remote('sha256sum /usr/bin/emulationstation').split()[0]},indent=2)+'\n')
print('PASS actual UI retry, new ownership, cancellation and unchanged credentials/paths/payload',lang,size,flush=True)

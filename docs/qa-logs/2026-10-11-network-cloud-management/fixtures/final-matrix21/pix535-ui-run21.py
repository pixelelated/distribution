import importlib.util,json,subprocess,sys,time
from pathlib import Path
s=importlib.util.spec_from_file_location('v','/tmp/pix537-vm.py');v=importlib.util.module_from_spec(s);s.loader.exec_module(v)
D=Path('/workspace/repos/rocknix.worktrees/m7-cloud-connections');lang,size=sys.argv[1:3];subset=sys.argv[3] if len(sys.argv)>3 else 'all';assert lang in ['en_US','fr_FR'];O=Path('/tmp/pix535-ui21')/(lang[:2]+size);O.mkdir(parents=True,exist_ok=True)
def reset(extra='',state=None):
 v.remote('systemctl stop essway; rm -f /storage/qa537/wifi/state.json /storage/qa537/wifi/fail /tmp/emulationstation.ready')
 if state:
  p=O/'state-fixture.json';p.write_text(json.dumps(state));v.scp(p,'/storage/qa537/wifi/state.json')
 v.remote('. /etc/profile >/dev/null 2>&1; set_setting system.language '+lang+'; '+extra+'systemctl start essway')
 for _ in range(100):
  if 'ready' in v.remote('test -f /tmp/emulationstation.ready && echo ready || true'):break
  time.sleep(.2)
 else:raise RuntimeError('ES not ready')
def walk(label,steps):
 pending=[]
 for line in steps.splitlines():
  if not line.startswith('shot '): pending.append(line); continue
  name=line.split(' ',1)[1];p=O/(label+'-'+name+'.steps');p.write_text('\n'.join(pending)+'\n')
  out=O/label/name
  subprocess.run([str(D/'tools/vm-visual-qa'),'--monitor',str(v.O/'monitor.sock'),'run',str(p),'--outdir',str(out)],check=True)
  # A visually still loading surface is not completion. Read the command
  # owner before capturing the result or sending the next action.
  for _ in range(170):
   busy=v.remote("pgrep -f 'wifictl (enable|connect|join)' >/dev/null && echo busy || echo idle").strip()
   if busy=='idle':break
   time.sleep(1)
  else:raise RuntimeError('Wi-Fi operation stalled')
  shot=O/'capture.steps';shot.write_text('settle\nshot '+name+'\n')
  subprocess.run([str(D/'tools/vm-visual-qa'),'--monitor',str(v.O/'monitor.sock'),'run',str(shot),'--outdir',str(out)],check=True)
  pending=[]
 assert not any(x.strip() for x in pending), 'unexecuted final steps'
 print('PASS walk',label,flush=True)
prefix=Path('/tmp/pix535-open.steps').read_text().split('shot picker-saved')[0]+'shot picker-saved\n'
if subset in ('all', 'happy'):
 reset()
 walk('full-happy', Path('/tmp/pix535-open.steps').read_text()+Path('/tmp/pix535-branches.steps').read_text().replace('key z\nwait-for-change\nkey down','key esc\nwait-for-change\nkey down')+'key x\nwait-for-change\nkey x\nwait-for-change\nsettle\nshot saved-connected\n')
 state=json.loads(v.remote('cat /storage/qa537/wifi/state.json'));assert state['current']=='DSaved' and state['saved']['Remembered']=='DSaved';(O/'saved-state.json').write_text(json.dumps(state,indent=2)+'\n')
if subset in ('all', 'failure'):
 reset('touch /storage/qa537/wifi/fail; ')
 walk('failed',prefix+'key x\nwait-for-change\nsettle\nshot open-failed\nkey x\nwait-for-change\nkey down\nkey x\nwait-for-change\nsettle\nshot protected-prompt\nkey b\nkey a\nkey d\nkey ret\nwait-for-change\nsettle\nshot protected-failed\n')
 v.remote('rm -f /storage/qa537/wifi/fail')
 walk('protected-success','key x\nwait-for-change\nkey x\nwait-for-change\n'+''.join('key '+x+'\n' for x in 'testpass123')+'key ret\nwait-for-change\nsettle\nshot protected-connected\n')
 state=json.loads(v.remote('cat /storage/qa537/wifi/state.json'));assert state['current']=='BPrivate';(O/'protected-state.json').write_text(json.dumps(state,indent=2)+'\n')
if subset in ('all', 'multiple'):
 reset(state={'current':'','saved':{'Remembered':'DSaved','Second profile':'DSaved'}})
 walk('multiple-profiles',prefix+'key down x3\nkey x\nwait-for-change\nsettle\nshot profiles\nkey x\nwait-for-change\nsettle\nshot chosen-profile\nkey x\nwait-for-change\nsettle\nshot chosen-connected\n')
 state=json.loads(v.remote('cat /storage/qa537/wifi/state.json'));assert state['current']=='DSaved';(O/'multiple-state.json').write_text(json.dumps(state,indent=2)+'\n')
print('PASS complete Wi-Fi UI fixtures',lang,size,flush=True)

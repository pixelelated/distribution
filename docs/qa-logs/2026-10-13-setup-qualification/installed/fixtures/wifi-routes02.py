from pathlib import Path
import sys,json,time,subprocess,traceback,importlib.util,importlib.machinery
from ui import out,remote,shot
r=Path(__file__).parent;repo=Path('/workspace/repos/rocknix.worktrees/m7-player-setup');profile,lang=sys.argv[1:];case=r/('wifi-routes-'+profile);case.mkdir();result={'rc':1,'cases':[],'started':time.time()};fixture=repo/'docs/qa-logs/2026-10-13-wifi-picker-source/fixtures/wifictl-fixture.py'
loader=importlib.machinery.SourceFileLoader('vq',str(repo/'tools/vm-visual-qa'));spec=importlib.util.spec_from_loader(loader.name,loader);vq=importlib.util.module_from_spec(spec);loader.exec_module(vq);mon=vq.Monitor(str(r/'vm/monitor.sock'))
def walk(keys,d):
 lines=[]
 for k in keys:lines+=['key '+k,'wait-for-change','settle']
 vq.run_steps(mon,lines,str(d/'walk'))
def frame(d,label):
 ok,_=vq.settle(mon.frame,timeout=12,quiet=1);assert ok;shot(d/(label+'.png'))
def wait_idle():
 end=time.monotonic()+45
 while time.monotonic()<end:
  if out('curl -fsS http://127.0.0.1:1234/isIdle 2>/dev/null || true').replace(' ','').strip()=='[true]':return
  time.sleep(.4)
 raise RuntimeError('frontend readiness')
try:
 for route in ['protected','unknown','manual','saved','profiles']:
  d=case/route;d.mkdir();dest='/storage/qa-wifi-577-'+profile+'-'+route
  assert out('cloud_oauth status').strip()=='idle'
  remote('systemctl stop essway.service; mkdir -p '+dest,capture_output=True)
  remote("python3 - <<'P'\nfrom pathlib import Path\nimport subprocess\np='/usr/bin/wifictl'\nfor i in range(8):\n if not any(l.split()[4]==p for l in Path('/proc/self/mountinfo').read_text().splitlines()):break\n subprocess.run(['umount',p],check=True)\nelse:raise RuntimeError('bind bound')\nP",capture_output=True)
  with fixture.open('rb') as f:remote('cat > '+dest+'/fixture.py',stdin=f)
  plan={'scans':[{'networks':['Fixture network']} for _ in range(4)],'security':{'Fixture network':route if route in ['open','protected'] else 'unknown'}}
  state={'profiles':[],'current':'','next_scan':0}
  if route in ['saved','profiles']:state['profiles']=[{'name':'Fixture profile A','ssid':'Fixture network'}]
  if route=='profiles':state['profiles'].append({'name':'Fixture profile B','ssid':'Fixture network'})
  for name,value in [('plan.json',json.dumps(plan)),('state.json',json.dumps(state)),('ALLOW-SYNTHETIC-WIFI','577\n'),('wifictl','#!/bin/sh\nexport PIXELELATED_WIFI_577_DIR='+dest+'\nexec python3 '+dest+'/fixture.py "$@"\n')]:remote('cat > '+dest+'/'+name,input=value,text=True,capture_output=True)
  remote('chmod 755 '+dest+'/wifictl; mount --bind '+dest+'/wifictl /usr/bin/wifictl; mount --make-private /usr/bin/wifictl; . /etc/profile >/dev/null 2>&1; set_setting system.language '+lang+'; systemctl start essway.service',capture_output=True);wait_idle()
  identity=out('cat /proc/sys/kernel/random/boot_id; pidof emulationstation; sha256sum /proc/$(pidof emulationstation)/exe').strip();assert 'f6fd61b7bea859467f1a3b0e1f890c975bfef9aaafd1866e727752727de013b3' in identity
  vq.run_steps(mon,['wake','settle'],str(d/'initial'));walk(['ret','up x6','x','down x5','x'],d);time.sleep(1);frame(d,'picker')
  walk(['down','right','x'] if route=='manual' else ['x'],d);time.sleep(1);frame(d,'outcome')
  if route=='saved':walk(['x'],d);time.sleep(1);frame(d,'connected')
  elif route=='profiles':walk(['x'],d);frame(d,'selected-profile');walk(['z'],d);frame(d,'cancelled-profile')
  elif route!='open':walk(['esc'],d);frame(d,'back')
  rows=[json.loads(x) for x in out('cat '+dest+'/calls.jsonl').splitlines()];(d/'calls.jsonl').write_text(json.dumps(rows,indent=2)+'\n');state=json.loads(out('cat '+dest+'/state.json'));(d/'state.json').write_text(json.dumps(state,indent=2)+'\n')
  starts=[x['command'] for x in rows if x['phase']=='start'];mutations=[x for x in starts if x in ['connect','connect-open','join','forget']]
  assert mutations==(['connect-open'] if route=='open' else ['join'] if route=='saved' else []),(route,mutations)
  if route in ['open','saved']:assert state['current']=='Fixture network'
  if route=='saved':assert state['active_profile']=='Fixture profile A'
  assert identity==out('cat /proc/sys/kernel/random/boot_id; pidof emulationstation; sha256sum /proc/$(pidof emulationstation)/exe').strip()
  result['cases'].append({'route':route,'rc':0,'identity':identity,'synthetic_mutations':mutations})
 result['rc']=0
except BaseException as e:result['error']=str(e);traceback.print_exc()
finally:
 result['ended']=time.time();(case/'result.json').write_text(json.dumps(result,indent=2)+'\n')
raise SystemExit(result['rc'])

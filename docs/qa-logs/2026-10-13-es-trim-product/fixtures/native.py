from ui import *
import hashlib
case=r/'native';case.mkdir();(r/'page-server/case.json').write_text(json.dumps({'name':'native'}))
def identity():return out('cat /proc/sys/kernel/random/boot_id; pidof emulationstation').strip()
def events():
 p=r/'page-server/events.jsonl'
 return [json.loads(l) for l in p.read_text().splitlines() if json.loads(l).get('run')=='native'] if p.exists() else []
def waitfor(fn,seconds,label):
 end=time.monotonic()+seconds
 while time.monotonic()<end:
  if fn():return
  time.sleep(.3)
 raise RuntimeError(label)
result={'rc':1,'before':identity()}
try:
 key('x');waitfor(lambda:any(e.get('kind')=='loaded' for e in events()),35,'page did not load');shot(case/'loaded.png')
 key('a');waitfor(lambda:any(e.get('kind')=='input' and e.get('length')==1 for e in events()),10,'virtual keyboard input not applied');shot(case/'typed.png')
 key('esc');waitfor(lambda:out('pidof cloud-signin-window || true').strip()=='',20,'browser did not exit')
 time.sleep(2);shot(case/'returned.png');result['after']=identity();assert result['before']==result['after'];result.update(rc=0,events=events(),input_scope='QEMU keyboard a; not physical gamepad/OSK selection proof')
finally:
 result['ended']=time.time();(case/'result.json').write_text(json.dumps(result,indent=2)+'\n')
raise SystemExit(result['rc'])

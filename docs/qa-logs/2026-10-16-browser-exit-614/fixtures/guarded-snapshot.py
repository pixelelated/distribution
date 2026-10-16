import json,os,subprocess,hashlib,time
from pathlib import Path
rows=[]
for p in Path('/proc').iterdir():
 if not p.name.isdigit():continue
 try:
  exe=(p/'exe').resolve().name;argv=(p/'cmdline').read_bytes().replace(b'\0',b' ').decode(errors='replace');fields=(p/'stat').read_text().rsplit(')',1)[1].split()
  if exe=='emulationstation' or any(x in argv for x in ['cloud-signin-window','WebKit','/usr/bin/cloud_oauth','/usr/bin/rclone authorize']):rows.append({'pid':int(p.name),'start':int(fields[19]),'exe':exe,'argv':argv,'state':fields[0]})
 except (FileNotFoundError,ProcessLookupError):pass
e=dict(os.environ,SWAYSOCK='/run/0-runtime-dir/sway-ipc.0.sock');s=subprocess.run(['swaymsg','-r','-t','get_tree'],env=e,capture_output=True,text=True,check=True,timeout=5);tree=json.loads(s.stdout);windows=[]
def walk(n):
 if n.get('app_id'):windows.append({k:n.get(k) for k in ['id','pid','app_id','focused','name']})
 for c in n.get('nodes',[])+n.get('floating_nodes',[]):walk(c)
walk(tree)
paths=['/usr/bin/cloud-signin-window','/usr/bin/cloud_oauth','/usr/bin/emulationstation'];hashes={p:hashlib.sha256(Path(p).read_bytes()).hexdigest() for p in paths}
print(json.dumps({'boot':Path('/proc/sys/kernel/random/boot_id').read_text().strip(),'processes':rows,'windows':windows,'hashes':hashes,'keyboard_names':[p.read_text().strip() for p in Path('/sys/class/input').glob('event*/device/name')],'guard':Path('/storage/qa614/guard.jsonl').exists(),'page_events':Path('/storage/qa614/page-events.jsonl').read_text()[-12000:] if Path('/storage/qa614/page-events.jsonl').exists() else ''}))

hb=json.loads(Path('/storage/qa614/heartbeat.json').read_text());assert time.monotonic()-hb['at']<3 and hb['guards']==0
state=subprocess.run(['systemctl','is-active','qa614-observer02'],capture_output=True,text=True,timeout=3);assert state.returncode==0 and state.stdout.strip()=='active'
assert not Path('/storage/qa614/observer-result.json').exists()
print('OBSERVER_ARMED='+json.dumps(hb))

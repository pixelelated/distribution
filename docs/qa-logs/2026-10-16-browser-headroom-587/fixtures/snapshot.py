import json,os,subprocess,time
from pathlib import Path
R=Path('/storage/qa587');hb=json.loads((R/'heartbeat.json').read_text());assert time.monotonic()-hb['at']<3 and hb['guards']==0
assert subprocess.run(['systemctl','is-active','--quiet','qa587-observer']).returncode==0
rows=[]
for p in Path('/proc').iterdir():
 if not p.name.isdigit():continue
 try:
  exe=p.joinpath('exe').resolve().name;stat=(p/'stat').read_text().rsplit(')',1)[1].split();comm=(p/'comm').read_text().strip()
  if exe in ['emulationstation','cloud-signin-window'] or 'WebKit' in comm:rows.append({'pid':int(p.name),'start':int(stat[19]),'exe':exe,'comm':comm})
 except (OSError,ValueError):pass
e=dict(os.environ,SWAYSOCK='/run/0-runtime-dir/sway-ipc.0.sock');p=subprocess.run(['swaymsg','-r','-t','get_tree'],env=e,capture_output=True,text=True,check=True,timeout=5);windows=[]
def walk(n):
 if n.get('app_id'):windows.append({k:n.get(k) for k in ['pid','app_id','focused']})
 for c in n.get('nodes',[])+n.get('floating_nodes',[]):walk(c)
walk(json.loads(p.stdout))
events=[json.loads(x) for x in (R/'page-events.jsonl').read_text().splitlines()] if (R/'page-events.jsonl').exists() else []
print(json.dumps({'at':time.monotonic(),'boot':Path('/proc/sys/kernel/random/boot_id').read_text().strip(),'processes':rows,'windows':windows,'observer':hb,'loaded':sum(x['kind']=='loaded' for x in events),'paint_ready':sum(x['kind']=='paint-ready' for x in events),'input':sum(x['kind']=='input' for x in events),'meminfo':{x.split(':')[0]:int(x.split()[1]) for x in Path('/proc/meminfo').read_text().splitlines()}}))

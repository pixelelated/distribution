from pathlib import Path
import json,gzip,base64,hashlib,subprocess
names=['observer.py','fake-rclone','input.jsonl','samples.jsonl','page-events.jsonl','observer-result.json','cleanup-result.json','kernel.log','heartbeat.json']+[f'case{i}-window.log' for i in range(1,5)]
files={}
for dirname in ['qa614','qa614-run01']:
 for name in names:
  p=Path('/storage')/dirname/name
  if not p.exists():continue
  raw=p.read_bytes();assert len(raw)<8*1024**2
  files[dirname+'/'+name]={'sha256':hashlib.sha256(raw).hexdigest(),'bytes':len(raw),'base64':base64.b64encode(raw).decode()}
p=subprocess.run(['systemctl','show','--no-pager','qa614-observer02','-p','Result','-p','ExecMainCode','-p','ExecMainStatus','-p','ActiveState'],capture_output=True,text=True,timeout=5);assert p.returncode==0
value={'files':files,'observer_service':{'rc':p.returncode,'stdout':p.stdout,'stderr':p.stderr}}
packed=gzip.compress(json.dumps(value).encode(),mtime=0);print('GUEST_EXPORT='+base64.b64encode(packed).decode())

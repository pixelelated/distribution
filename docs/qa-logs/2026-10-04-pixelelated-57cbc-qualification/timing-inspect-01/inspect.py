from pathlib import Path
import subprocess,json,hashlib,datetime
owner=Path(__file__).parent
ssh=['ssh','-i',str(owner/'pair/qa-key'),'-p','10026','-o','BatchMode=yes','-o','ConnectTimeout=8','-o','StrictHostKeyChecking=no','-o','UserKnownHostsFile=/dev/null','-o','LogLevel=ERROR','root@127.0.0.1']
code="""from pathlib import Path
import json,hashlib,time
p=Path('/storage/roms/nes/Bench.srm');s=p.stat()
print(json.dumps({'mtime_ns':s.st_mtime_ns,'size':s.st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'current_epoch':time.time(),'last_backup':Path('/storage/.cache/cloud_sync/last-backup').read_text(),'persistent_log_dirs':[str(p) for p in Path('/storage').glob('.*log*')]}))
"""
g=json.loads(subprocess.check_output(ssh+['python3 -'],input=code.encode()))
remote=Path('/workspace/tmp/pixelelated-m7-timing-diagnostic-01/cloud/data/pixelelated/Saves/nes/Bench.srm');s=remote.stat()
r={'mtime_ns':s.st_mtime_ns,'size':s.st_size,'sha256':hashlib.sha256(remote.read_bytes()).hexdigest()}
result={'observed_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'guest':g,'remote':r,'guest_minus_remote_mtime_ms':(g['mtime_ns']-r['mtime_ns'])/1e6}
(owner/'artifacts/failed-save-facts.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))

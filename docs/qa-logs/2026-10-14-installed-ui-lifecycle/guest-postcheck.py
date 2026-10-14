#!/usr/bin/env python3
"""Compact post-smoke receipt; no configuration values or private archives exported."""
import hashlib,json,os,stat,subprocess
from pathlib import Path
q=Path('/storage/qa570flows');b=json.loads((q/'binding.json').read_text());rows={}
for n,v in b['members'].items():
    p=Path('/')/n
    rows[n]={'sha256':hashlib.file_digest(p.open('rb'),'sha256').hexdigest(),'mode':stat.filemode(p.stat().st_mode)}
    assert rows[n]['sha256']==v['sha256'] and rows[n]['mode']==v['mode'],n
mounts=[line.split()[4] for line in Path('/proc/self/mountinfo').read_text().splitlines() if line.split()[4] in ['/usr/bin/rclone','/usr/bin/wifictl']]
assert not mounts
broker=subprocess.run(['cloud_oauth','status'],capture_output=True,text=True,timeout=10);assert broker.returncode==0 and broker.stdout.strip()=='idle'
browser=subprocess.run(['pidof','cloud-signin-window'],capture_output=True,text=True,timeout=5);assert browser.returncode==1 and not browser.stdout.strip()
listeners=[]
for path in ['/proc/net/tcp','/proc/net/tcp6']:
    for line in Path(path).read_text().splitlines()[1:]:
        f=line.split()
        # The actual proxy may legitimately own loopback8080; it is outside this UI owner.
        if f[3]=='0A' and int(f[1].rsplit(':',1)[1],16)==53682:listeners.append(f[1])
assert not listeners
restored=json.loads((q/'configuration-restored.json').read_text());assert restored['status']=='PASS'
assert not list(Path('/storage/roms/gb').rglob('*.gb'))
print(json.dumps({'status':'PASS','boot_id':Path('/proc/sys/kernel/random/boot_id').read_text().strip(),'products':rows,'owned_seam_mounts':mounts,'browser_original_rc':browser.returncode,'broker_original_rc':broker.returncode,'broker_status':broker.stdout.strip(),'synthetic_listeners':listeners,'configuration_restored':restored},indent=2))

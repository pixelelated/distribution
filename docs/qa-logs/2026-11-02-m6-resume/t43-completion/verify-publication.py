"""Retain and reconcile sealed ordinary T43 completion receipts, without replay."""
from pathlib import Path
import collections
import datetime
import hashlib
import json
import os
import stat
import subprocess

OUT=Path(__file__).resolve().parent
SRC=Path('/workspace/tmp/m6-t43/completion-publication')
TIP='fd1238800b61431a8febeebe8cf44f41d2384bbb'
OLD='8282cbcade3be32b437f7391be7e216d9a6b1074'
sha=lambda b:hashlib.sha256(b).hexdigest()
def read(name):
    parts=name.split('/');assert all(x not in ('','.','..') for x in parts)
    fd=os.open('/',os.O_RDONLY|os.O_DIRECTORY)
    try:
        for part in [*SRC.parts[1:],*parts[:-1]]:
            nxt=os.open(part,os.O_RDONLY|os.O_DIRECTORY|os.O_NOFOLLOW,dir_fd=fd);os.close(fd);fd=nxt
        f=os.open(parts[-1],os.O_RDONLY|os.O_NOFOLLOW|os.O_NONBLOCK,dir_fd=fd)
        try:
            before=os.fstat(f);assert stat.S_ISREG(before.st_mode);chunks=[]
            while b:=os.read(f,65536):chunks.append(b)
            after=os.fstat(f);assert (before.st_ino,before.st_size,before.st_mtime_ns)==(after.st_ino,after.st_size,after.st_mtime_ns)
            return b''.join(chunks)
        finally:os.close(f)
    finally:os.close(fd)
manifest=read('MANIFEST.json');assert sha(manifest)=='8362d8ad8a4ba80ab967eb567af5888440123cde2b6312c27824febcafe71ee6'
m=json.loads(manifest);assert m['completion_tip']==TIP and m['accepted_final']==OLD and len(m['members'])==94
data={name:read(name) for name in m['members']}
for name,v in m['members'].items():assert sha(data[name])==v['sha256'] and len(data[name])==v['bytes'],name
assert sum(map(len,data.values()))==m['total_bytes']==291940
for name in ('checkpoint-request.md','checkpoint-posted.json','checkpoint-readback.json'):
    assert name in m['future_delivery_appendices'];data[name]=read(name)
live=json.loads((OUT/'live-checkpoint.json').read_text())
assert json.loads(data['checkpoint-readback.json'])['body']==data['checkpoint-request.md'].decode()==live['body']
assert str(json.loads(data['checkpoint-readback.json'])['id'])==str(live['id'])=='6591825691'
records=[]
for name,b in data.items():
    if not name.endswith('.json'):continue
    r=json.loads(b)
    if not isinstance(r,dict) or not all(k in r for k in ('argv','exit','stdout_sha256','stderr_sha256')):continue
    if name=='completion-exact-scan-result.json':stem='completion-exact-scan'
    else:stem=name[:-5]
    for stream in ('stdout','stderr'):assert sha(data[stem+'.'+stream])==r[stream+'_sha256'],(name,stream)
    assert r['exit']==(1 if name=='postcommit-scan.json' else 0),name
    records.append({'receipt':name,'exit':r['exit'],'stdout_sha256':r['stdout_sha256'],'stderr_sha256':r['stderr_sha256']})
pub=json.loads(data['publication.json'])
for name,v in pub['checks'].items():
    r=json.loads(data[v['receipt']]);assert r['exit']==v['exit']==0 and r['finished']==v['finished'],name
assert data['status.stdout']==data['postcommit-status.stdout']==b''
assert data['remote.stdout'].decode().split()[0]==TIP
assert '0 hits in 137088 tracked files' in data['forbidden.stdout'].decode()
assert b'external ordinary-file scan packet required' in data['postcommit-scan.stderr']
scan=json.loads(data['completion-exact-scan-manifest.json']);res=json.loads(data['completion-exact-scan-result.json'])
changed=set(subprocess.check_output(['git','diff','--name-only','-z',OLD,TIP]).decode().strip('\0').split('\0'))
assert scan['base']==OLD and scan['tip']==TIP and scan['count']==len(changed)==61 and not scan['excluded_paths']
assert {r['path'] for r in scan['files']}==changed and len(scan['files'])==61
payload=hashlib.sha256();total=0
for i,r in enumerate(scan['files']):
    b=subprocess.check_output(['git','show',TIP+':'+r['path']]);assert len(b)==r['bytes'] and sha(b)==r['sha256'];total+=len(b)
    if i:payload.update(b'\n')
    payload.update(b)
assert total==scan['total_bytes']==399862 and payload.hexdigest()==scan['stdin_sha256']==res['stdin_sha256']
assert total+60==scan['stdin_bytes']==res['stdin_bytes'] and sha(data['completion-exact-scan-manifest.json'])==res['manifest_sha256']
assert sha(subprocess.check_output(['git','show',TIP+':tools/forbidden-terms-check']))==res['tool_sha256']
dest=OUT/'publication';dest.mkdir(exist_ok=False);objects=dest/'objects';objects.mkdir();index={}
for name,b in data.items():
    h=sha(b);(objects/h).write_bytes(b);index[name]={'sha256':h,'bytes':len(b),'object':'objects/'+h,'core_manifest_member':name in m['members']}
(dest/'MANIFEST.json').write_bytes(manifest)
(dest/'retention-index.json').write_text(json.dumps({'files':index,'not_read_delivery_appendices':[n for n in m['future_delivery_appendices'] if n not in data]},indent=2)+'\n')
result={'result':'PASS new completion publication/scan/command bindings; no producer replay','observed_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'tip':TIP,'core_files':94,'core_bytes':291940,'checkpoint_appendices':3,'new_command_receipts':records,'exits':dict(collections.Counter(r['exit'] for r in records)),'scan_paths':61,'scan_repository_bytes':399862,'scan_input_sha256':payload.hexdigest(),'original_scan_refusal_preserved':True,'supported_normal_stdin_scan_pass':True,'remote_tip_exact':True,'status_empty':True,'checkpoint_exact_live':True}
(OUT/'publication-verification.json').write_text(json.dumps(result,indent=2)+'\n')
print('PASS94core +3checkpoint files;',len(records),'command receipts;',result['exits'],'61exact paths;',total,'bytes')

"""Confined completion receipt retention and immutable comparison; no replay."""
from pathlib import Path,PurePosixPath
import hashlib,json,os,stat,subprocess,datetime
OUT=Path(__file__).parent
SRC=Path('/tmp/m6-t44-completion-0s8xu7tm')
TIP='ad0df587128577212337aa76d171b0b9cfaae4a4'
A='docs/audits/2026_11_02-epic-m6-es-vendored-and-data/'
sha=lambda b:hashlib.sha256(b).hexdigest()
def read(name):
 parts=PurePosixPath(name).parts;assert parts and not name.startswith('/') and all(p not in ('.','..') for p in parts)
 fd=os.open(SRC,os.O_RDONLY|os.O_DIRECTORY|os.O_NOFOLLOW)
 try:
  for p in parts[:-1]:
   nxt=os.open(p,os.O_RDONLY|os.O_DIRECTORY|os.O_NOFOLLOW,dir_fd=fd);os.close(fd);fd=nxt
  f=os.open(parts[-1],os.O_RDONLY|os.O_NOFOLLOW,dir_fd=fd)
  with os.fdopen(f,'rb') as stream:
   assert stat.S_ISREG(os.fstat(stream.fileno()).st_mode);return stream.read()
 finally:os.close(fd)
def gitshow(path):return subprocess.check_output(['git','show',TIP+':'+path])
manifest=read('SHA256SUMS');assert sha(manifest)=='84a424d716d9903b5d7d0b73e674dce52d95ea2fdd3ef089271e63f3fdba2880'
expected={}
for row in manifest.decode().splitlines():
 h,n=row.split('  ',1);assert n not in expected;expected[n]=h
assert len(expected)==52
expected['SHA256SUMS']=sha(manifest)
files=set()
for folder,dirs,names in os.walk(SRC,followlinks=False):
 assert not any((Path(folder)/d).is_symlink() for d in dirs)
 files.update(str((Path(folder)/n).relative_to(SRC)) for n in names)
assert files==set(expected),files^set(expected)
data={n:read(n) for n in expected}
assert all(sha(data[n])==h for n,h in expected.items())
assert sha(data['RETURN.md'])=='f74c6a7b03bcfef269537a132fa72b91c6bb0a547bc4adc5f1778e34075b44cd'
assert sha(data['publication-readback.json'])=='f8aa54317ca0ceeeda81b2222aaeec8ec0dc39885e6ef44476f9fa0546866546'
pub=json.loads(data['publication-readback.json']);assert pub['tip']==TIP
runner=gitshow(A+'completion/run.py');assert runner==data['run.py']
assert gitshow(A+'completion/completion-read.py')==data['completion-read.py']
for item in pub['command_receipts']:
 b=data[item['path']];assert sha(b)==item['sha256'];r=json.loads(b);folder=item['path'].rsplit('/',1)[0]
 assert r['rc']==item['rc']==0 and r['head']==item['head'] and r['runner_sha256']==sha(runner)
 assert r['cpus']==list(range(8,24)) and r['start']<=r['end'] and r['argv']
 for s in ['stdout','stderr']:assert sha(data[folder+'/'+s])==r[s+'_sha256']
 assert sha(data[folder+'/scope.json'])==r['scope_sha256']
assert len(pub['command_receipts'])==11
assert data['published-head/stdout'].decode().splitlines()==[TIP,pub['tree']]
assert data['remote-tip/stdout'].decode()==TIP+'\trefs/heads/feature/m6-es-vendored-and-data-691\n'
assert not data['published-status/stdout']
scan=json.loads(data['exact-final-read-scan/stdout']);assert scan['tip']==TIP and scan['final_clean'] and scan['es_clean']
proof=json.loads((OUT/'coordinator-verification.json').read_bytes())
assert len(scan['records'])==106 and {v['path'] for v in scan['records']}==set(proof['changed_paths'])
pieces=[]
for v in scan['records']:
 b=gitshow(v['path']);assert len(b)==v['bytes'] and sha(b)==v['sha256'];pieces.append(b+b'\n')
payload=b''.join(pieces);s=scan['scan'];assert sha(payload)==s['stdin_sha256'] and len(payload)==s['input_bytes'] and s['rc']==0
assert s['program_sha256']==sha(gitshow('tools/forbidden-terms-check'))
assert s['stdout']=='forbidden-terms-check: 0 hits on stdin\n' and not s['stderr']
for name in ['stdout','stderr']:assert sha(s[name].encode())==s[name+'_sha256']
checkpoint=json.loads(data['checkpoint-readback.json'])['checkpoint'];live=json.loads((OUT/'live-checkpoint.json').read_bytes())
assert checkpoint['body']==live['body'] and int(checkpoint['id'])==int(live['id'])==6592329438
liveissues={x['issue_number']:x for x in json.loads((OUT/'live-issues.json').read_bytes())}
for n,old in json.loads(data['verified-issues.json'])['issues'].items():
 new=liveissues[int(n)]
 for k in ['body','state','closed_at']:assert old[k]==new[k]
dest=OUT/'publication';dest.mkdir(exist_ok=False);(dest/'objects').mkdir()
index=[]
for name,b in data.items():
 h=sha(b);target=dest/'objects'/(h+'.json')
 obj={'encoding':'utf8-json','raw':b.decode(),'sha256':h,'bytes':len(b)}
 if not target.exists():target.write_text(json.dumps(obj,indent=2)+'\n')
 assert json.loads(target.read_bytes())['raw'].encode()==b
 index.append({'path':name,'bytes':len(b),'sha256':h,'stored':'objects/'+target.name,'encoding':'utf8-json'})
(dest/'index.json').write_text(json.dumps({'source':str(SRC),'entries':index,'manifest_sha256':sha(manifest)},indent=2)+'\n')
result={'result':'PASS completion publication and exact final record scan','at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'tip':TIP,'files':len(index),'bytes':sum(x['bytes'] for x in index),'command_receipts':11,'all_rc0':True,'new_record_paths':106,'raw_record_bytes':sum(len(x)-1 for x in pieces),'scanner_input_bytes':len(payload),'scan_rc':0,'remote_and_clean_exact':True,'checkpoint':6592329438,'checkpoint_exact':True,'no_producer_execution':True}
(OUT/'publication-verification.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result))

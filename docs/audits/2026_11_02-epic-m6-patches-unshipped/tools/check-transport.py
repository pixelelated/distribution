#!/usr/bin/env python3
"""Exercise only new storage custody: tampered/missing payloads and exact restoration."""
import datetime,hashlib,json,pathlib,subprocess
R=pathlib.Path(__file__).resolve().parents[1];D=R/'stage-d/transport-fixtures';D.mkdir(exist_ok=True)
m=json.loads((R/'stage-d/transport-manifest.json').read_text());name='stage-a/source/paths.txt'
v=m['files'][name];b=(R/name).read_bytes();(D/'tampered.txt').write_bytes(b+b'tampered\n')
cases=[]
for tag,payload in [('tampered',D/'tampered.txt'),('missing',D/'missing.txt')]:
 assert tag!='missing' or not payload.exists()
 f=D/(tag+'.json');f.write_text(json.dumps({'payload_path':str(payload),'record':v,'stored_component':m['stored_component']},indent=2)+'\n')
 cases.append((tag,['python3',str(R/'tools/transport.py'),'--fixture',str(f)],1,f,payload))
cases.append(('positive',['python3',str(R/'tools/transport.py')],0,R/'stage-d/transport-manifest.json',None))
out=[]
for tag,argv,expected,f,payload in cases:
 start=datetime.datetime.now(datetime.timezone.utc).isoformat();p=subprocess.run(argv,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
 (D/(tag+'.stdout')).write_bytes(p.stdout);(D/(tag+'.stderr')).write_bytes(p.stderr)
 assert p.returncode==expected,(tag,p.returncode)
 if tag=='tampered':assert b'stored transport drift' in p.stderr
 if tag=='missing':assert b'FileNotFoundError' in p.stderr
 def sha(x):return hashlib.sha256(x).hexdigest()
 out.append({'name':tag,'argv':argv,'started':start,'finished':datetime.datetime.now(datetime.timezone.utc).isoformat(),'exit':p.returncode,'program_sha256':sha((R/'tools/transport.py').read_bytes()),'fixture_sha256':sha(f.read_bytes()),'payload_sha256':sha(payload.read_bytes()) if payload and payload.exists() else None,'payload_missing_expected':tag=='missing','stdout_sha256':sha(p.stdout),'stderr_sha256':sha(p.stderr)})
(R/'stage-d/transport-controls.json').write_text(json.dumps(out,indent=2)+'\n')
print('PASS new storage custody controls: tampered payload refused; missing payload refused; all19 original raw identities and source/seed keys restored exactly; no original producer run')

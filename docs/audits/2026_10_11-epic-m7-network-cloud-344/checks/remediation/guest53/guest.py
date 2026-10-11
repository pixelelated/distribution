from pathlib import Path
import subprocess,json,hashlib
C=Path('/storage/.config/rclone/rclone.conf');A=C.with_name('active-connection');P=Path('/storage/qa537/provider/save.srm')
original={p:p.read_bytes() if p.exists() else None for p in (C,A)}
h=lambda p:hashlib.sha256(p.read_bytes()).hexdigest() if p.exists() else None
payload=h(P);results=[]
commands=[['cloud_scan'],['cloud_backup','--yes','--saves-only'],['cloud_restore','--yes','--saves-only'],['cloud_content_backup','--selected'],['cloud_content_restore','--selected']]
try:
 for state in ('unselected','missing','unconfigured'):
  C.write_text('[spare]\ntype = alias\nremote = /storage/qa537/provider\n');A.write_text('missing\n' if state=='missing' else '\n');C.chmod(0o600);A.chmod(0o600)
  if state=='unconfigured':C.unlink()
  cfg=h(C);active=h(A)
  expected="YOUR CLOUD STORAGE ISN'T SET UP YET" if state=='unconfigured' else 'CHOOSE A CONNECTION BEFORE USING CLOUD TOOLS.'
  for cmd in commands:
   r=subprocess.run(cmd,capture_output=True,text=True,timeout=20)
   reason=[x for x in r.stdout.splitlines() if x.startswith('>>> why ')]
   assert r.returncode==1 and '>>> why '+expected in reason,(state,cmd,r.returncode,reason)
   assert cfg==h(C) and active==h(A) and payload==h(P)
   results.append({'state':state,'command':cmd,'rc':r.returncode,'reason':expected,'configuration_selection_payload_unchanged':True})
finally:
 for p,data in original.items():
  if data is None:p.unlink(missing_ok=True)
  else:p.write_bytes(data);p.chmod(0o600)
print(json.dumps({'result':'PASS','controls':results,'restored':all((p.read_bytes() if p.exists() else None)==v for p,v in original.items())},indent=2))

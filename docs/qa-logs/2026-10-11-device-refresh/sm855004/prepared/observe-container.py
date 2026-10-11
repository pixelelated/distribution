from pathlib import Path
import datetime,json,subprocess,time
O=Path(__file__).resolve().parent;j=json.loads((O/'inputs.json').read_text())
for _ in range(180):
 r=subprocess.run(['docker','inspect','pixelelated-m7-sm8550-refresh04'],capture_output=True,text=True)
 if r.returncode==0:
  d=json.loads(r.stdout)[0]
  if d['State']['Running']:
   assert d['Config']['Labels']['pixelelated.m7.owner']=='sm8550-refresh04'
   assert d['Image']==j['container_image_id'] and d['Config']['Image']==j['container']
   assert d['Config']['User']=='1000:1000' and d['Config']['WorkingDir']==j['container_worktree']
   mounts=[{k:m[k] for k in ['Type','Source','Destination','RW']} for m in d['Mounts']]
   assert any(m['Source']==j['host_worktree'] and m['Destination']==j['container_worktree'] and m['RW'] for m in mounts)
   assert any(m['Source']==j['source_cache'] and m['Destination']==j['container_worktree']+'/sources' for m in mounts)
   assert any(m['Source']==j['nix_private_store'] and m['Destination']=='/nix' and m['RW'] for m in mounts)
   assert any(m['Source']==j['nix_snapshot'] and m['Destination']==j['nix_snapshot'] and not m['RW'] for m in mounts)
   (O/'container-observed.json').write_text(json.dumps({'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'id':d['Id'],'image':d['Image'],'reference':d['Config']['Image'],'user':d['Config']['User'],'workdir':d['Config']['WorkingDir'],'command':d['Config']['Cmd'],'state':d['State'],'mounts':mounts},indent=2)+'\n')
   for _ in range(120):
    runtime=O/'artifacts/container-runtime.json'
    if runtime.exists():
     value=json.loads(runtime.read_text());assert value['result']=='PASS' and value['TMPDIR']=='/tmp' and value['actual_temporary_write_read'];break
    time.sleep(1)
   else:raise AssertionError('actual container runtime proof absent')
   ready=O/'artifacts/.container-gate.json'
   ready.write_text(json.dumps({'result':'PASS','container':d['Id'],'runtime_proof':value},indent=2)+'\n')
   ready.replace(O/'artifacts/container-gate.json')
   print('PASS observed actual pinned SM8550 container, stable-path mounts and effective TMPDIR',flush=True);break
 time.sleep(1)
else:raise SystemExit('SM8550 running container was not observed')

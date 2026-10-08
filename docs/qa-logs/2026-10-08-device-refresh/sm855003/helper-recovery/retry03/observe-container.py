from pathlib import Path
import datetime,json,subprocess,time
O=Path(__file__).resolve().parent;j=json.loads((O/'inputs.json').read_text())
for _ in range(180):
 r=subprocess.run(['docker','inspect','pixelelated-m7-sm8550-refresh03'],capture_output=True,text=True)
 if r.returncode==0:
  d=json.loads(r.stdout)[0]
  if d['State']['Running']:
   assert d['Config']['Labels']['pixelelated.m7.owner']=='sm8550-refresh03'
   assert d['Image']==j['container_image_id'] and d['Config']['Image']==j['container']
   assert d['Config']['User']=='1000:1000' and d['Config']['WorkingDir']==j['container_worktree']
   mounts=[{k:m[k] for k in ['Type','Source','Destination','RW']} for m in d['Mounts']]
   assert any(m['Source']==j['host_worktree'] and m['Destination']==j['container_worktree'] and m['RW'] for m in mounts)
   assert any(m['Source']==j['source_cache'] and m['Destination']==j['container_worktree']+'/sources' for m in mounts)
   for source,dest,rw in [(str(O),str(O),True),(j['nix_private_store'],'/nix',True),(j['nix_snapshot'],j['nix_snapshot'],False)]:
    assert any(m['Source']==source and m['Destination']==dest and m['RW']==rw for m in mounts),(source,dest,rw)
   (O/'container-observed.json').write_text(json.dumps({'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'id':d['Id'],'image':d['Image'],'reference':d['Config']['Image'],'user':d['Config']['User'],'workdir':d['Config']['WorkingDir'],'command':d['Config']['Cmd'],'state':d['State'],'mounts':mounts},indent=2)+'\n')
   print('PASS observed actual pinned SM8550 container and isolated stable-path mounts',flush=True);break
 time.sleep(1)
else:raise SystemExit('SM8550 running container was not observed')

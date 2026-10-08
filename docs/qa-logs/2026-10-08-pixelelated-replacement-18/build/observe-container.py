from pathlib import Path
import datetime,json,subprocess,time
owner=Path('/workspace/tmp/pixelelated-m7-replacement-18')
j=json.loads((owner/'inputs.json').read_text())
for attempt in range(180):
 r=subprocess.run(['docker','inspect','pixelelated-m7-build18'],capture_output=True,text=True)
 if r.returncode==0:
  d=json.loads(r.stdout)[0]
  if d['State']['Running']:
   assert d['Config']['Labels']['pixelelated.m7.owner']=='replacement18'
   assert d['Image']==j['container_image_id']
   assert d['Config']['Image']==j['container']
   assert d['Config']['User']=='1000:1000'
   assert d['Config']['WorkingDir']=='/workspace/repos/rocknix.worktrees/m7-pixelelated'
   mounts=[{k:m[k] for k in ['Type','Source','Destination','RW']} for m in d['Mounts']]
   assert any(m['Source']==j['host_worktree'] and m['Destination']==d['Config']['WorkingDir'] for m in mounts)
   result={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'id':d['Id'],'image':d['Image'],'image_reference':d['Config']['Image'],'user':d['Config']['User'],'workdir':d['Config']['WorkingDir'],'command':d['Config']['Cmd'],'state':d['State'],'mounts':mounts}
   (owner/'container-observed.json').write_text(json.dumps(result,indent=2)+'\n')
   print('PASS observed running pinned container and isolated mounts',flush=True)
   break
 time.sleep(1)
else:raise SystemExit('running build container not observed')

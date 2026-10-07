"""Fresh affected UI profiles, prepared only after candidate16 build verification."""
from pathlib import Path
from datetime import datetime,timezone
import ast,hashlib,json,re,shutil,subprocess

base=Path('/workspace/tmp');build=base/'pixelelated-m7-replacement-16'
assert json.loads((build/'completion.json').read_text())['result']=='PASS'
manifest=build/'inputs.json';inputs=json.loads(manifest.read_text())
mh=hashlib.sha256(manifest.read_bytes()).hexdigest()
assert inputs['emulationstation_commit']=='72494bc72e3d64d4dcfeb4e6478052bbdf166c5b'
parents={'root-reasons':'pixelelated-m7-p4-cloud-ui-fixes-04',
         'recovery':'pixelelated-m7-p4-recovery-ui-fixes-06',
         'partial-retry':'pixelelated-m7-p4-coverage-ui-05'}
created=[]
for resolution,gl in [('640x480','none'),('1280x800','auto')]:
 for kind,parent_name in parents.items():
  old=base/parent_name;owner=base/('pixelelated-m7-p4-build16-'+kind+'-'+resolution+'-01')
  assert not owner.exists();owner.mkdir(mode=0o700);(owner/'artifacts').mkdir(mode=0o700)
  mapping={parent_name:owner.name,'m7-pixelelated-replacement15':'m7-pixelelated-replacement16',
    'pixelelated-m7-replacement-15':'pixelelated-m7-replacement-16','pixelelated-m7-qa-19':'pixelelated-m7-image-16',
    'ed5a6a51f5974deec8748fbf0dbd2f4984b690f5':inputs['distribution_commit'],
    'ed5a6a51f5':inputs['distribution_commit'][:10],
    '0bc7c44d06fc0180eaa170d8ec68bad2247c34af90319a9491beafeb538580d6':mh}
  names=['run.sh','outer.sh','verify-inputs.py','check-payload.py','proxy-identity.py','seed.py','stop-guest.py','cloud-ui-proof.py']
  if kind=='partial-retry':names.append('seed-oracle.py')
  for name in names:
   s=(old/name).read_text()
   for a,b in mapping.items():s=s.replace(a,b)
   if name=='run.sh':
    assert '--gl none --res 640x480' in s
    s=s.replace('--gl none --res 640x480','--gl '+gl+' --res '+resolution)
    s=re.sub(r'CLOUD_QA_NAME=\S+', 'CLOUD_QA_NAME='+owner.name,s)
    needle='printf \'%s\\n\' "$TASK_PID" > "$TASK_OWNER/guest.pid"'
    assert needle in s
    s=s.replace(needle,needle+'\ntr "\\0" "\\n" < "/proc/$TASK_PID/cmdline" > "$ROCKNIX_ARTIFACTS/qemu-argv.txt"')
   if name=='cloud-ui-proof.py' and kind=='root-reasons':
    start=s.index("  cases=[('chooser-" );end=s.index('  for name,action in cases:',start)
    s=s[:start]+"  cases=[('legacy-root',root_content)]+[('reason-'+kind,lambda k=kind:reason(k)) for kind in ['future','malformed','config','record']]\n"+s[end:]
    needle="check(re.search(r'^gb\\|10\\|',guest('cat /storage/.cache/cloud_sync/scan/scan').stdout,re.M),'legacy root game visible')"
    assert needle in s
    s=s.replace(needle,needle+"\n check(re.search(r'^gb\\|10\\|1\\|',guest('cat /storage/.cache/cloud_sync/scan/scan').stdout,re.M),'legacy-root row reports supported installed Game Boy capability')")
   if name=='cloud-ui-proof.py' and kind=='partial-retry':
    start=s.index(" cases=[('en_US','mid-copy-kill-ui-retry-next-shelf'")
    end=s.index('\nfinally:',start)
    s=s[:start]+''' for language in ['en_US','fr_FR']:
  case=language+'-mid-copy-kill-ui-retry-next-shelf';print('START '+case,flush=True)
  reset(language);guest('rm -f /storage/.config/.restore-finish-pending');kill_during_move()
  # Final backup deliberately stops ES. Restore its actual lifecycle before
  # the next language and final running-identity proof; assert cloud stability.
  cloud=hashes();start();check(hashes()==cloud,'ES restart after backup preserves every cloud byte')
  rows.append({'case':case,'status':'PASS','visual_review':'pending actual frames'})
  (out/'results.json').write_text(json.dumps(rows,indent=2)+'\\n')
'''+s[end:]
   if name=='cloud-ui-proof.py':
    width,height=map(int,resolution.split('x'))
    s+=f'''
import struct
frames=sorted(out.glob('*.png'))
assert frames,'No direct frames retained'
for frame in frames:
 raw=frame.read_bytes();assert raw[:8]==b'\\x89PNG\\r\\n\\x1a\\n',frame
 assert struct.unpack('>II',raw[16:24])==({width},{height}),frame
save('frame-dimensions',{{'count':len(frames),'width':{width},'height':{height},'visual_review':'pending primary inspection'}})
'''
   (owner/name).write_text(s);shutil.copymode(old/name,owner/name)
   if name.endswith('.py'):ast.parse(s)
   if name.endswith('.sh'):subprocess.run(['bash','-n',str(owner/name)],check=True)
  (owner/'provenance.json').write_text(json.dumps({'prepared_utc':datetime.now(timezone.utc).isoformat(),'state':'prepared, not submitted','parent':str(old),'kind':kind,'resolution':resolution,'requested_gl':gl,'distribution_commit':inputs['distribution_commit'],'ES_commit':inputs['emulationstation_commit'],'manifest_sha256':mh,'scope':'Focused candidate16 installed UI after verified build/bundle/raw-update payload. Exact product unchanged within each run. Direct frame review and full QA20 remain required before acceptance; focused checks run first to expose remaining product defects.'},indent=2)+'\n')
  paths=sorted(p for p in owner.iterdir() if p.is_file())
  (owner/'harness.sha256').write_text(''.join(hashlib.sha256(p.read_bytes()).hexdigest()+'  '+str(p)+'\n' for p in paths))
  created.append(str(owner))
print(json.dumps({'prepared_not_executed':created},indent=2))

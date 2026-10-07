from pathlib import Path
from datetime import datetime,timezone
import ast,hashlib,json,shutil,subprocess
base=Path('/workspace/tmp')
for resolution in ['640x480','1280x800']:
 old=base/('pixelelated-m7-p4-build16-partial-retry-'+resolution+'-01')
 owner=old.with_name(old.name[:-2]+'02')
 subprocess.run(['sha256sum','-c',str(old/'harness.sha256')],check=True,stdout=subprocess.DEVNULL)
 assert not owner.exists();owner.mkdir(mode=0o700);(owner/'artifacts').mkdir(mode=0o700)
 names=[Path(line.split(None,1)[1]).name for line in (old/'harness.sha256').read_text().splitlines()]
 for name in names:
  text=(old/name).read_text().replace(old.name,owner.name)
  if name=='cloud-ui-proof.py':
   start=" guest('systemctl stop essway; mkdir -p /storage/roms/gb; printf \"newer local save with different size\\\\n\" > /storage/roms/gb/Conflict.srm; /usr/bin/cloud_backup --yes --saves-only')"
   assert text.count(start)==1
   prefix=''' def legacy_parent_snapshot():
  parent=data/'ROCKNIX'
  if not parent.exists():return {'exists':False,'entries':[]}
  st=parent.stat()
  return {'exists':True,'device':st.st_dev,'inode':st.st_ino,'entries':[str(p.relative_to(parent)) for p in sorted(parent.rglob('*'))]}
 legacy_before=legacy_parent_snapshot()
 check(not legacy_before['entries'],'no old-root descendants remain before next backup')
 save('legacy-parent-before-backup',legacy_before)
'''
   text=text.replace(start,prefix+start)
   assertion=" check(not (data/'ROCKNIX').exists(),'next backup does not recreate old root')"
   assert text.count(assertion)==1
   text=text.replace(assertion," legacy_after=legacy_parent_snapshot()\n save('legacy-parent-after-backup',legacy_after)\n check(legacy_after==legacy_before,'next backup preserves the prior empty-or-absent old parent exactly')")
   text=text.replace("new_shelf=str(kept[0].relative_to(data)),scope=", "new_shelf=str(kept[0].relative_to(data)),legacy_parent_before=legacy_before,legacy_parent_after=legacy_after,scope=")
  (owner/name).write_text(text);shutil.copymode(old/name,owner/name)
  if name.endswith('.py'):ast.parse(text)
  if name.endswith('.sh'):subprocess.run(['bash','-n',str(owner/name)],check=True)
 (owner/'provenance.json').write_text(json.dumps({'prepared_utc':datetime.now(timezone.utc).isoformat(),'parent':str(old),'issue':486,
  'correction':'Observe old parent existence/device/inode/descendants immediately before and after backup. Require no old descendants and no change. Prior01 allowed an empty parent after MOVE, then incorrectly required absence after backup.',
  'unchanged':'Actual strict-partial copy, PID/start-tick kill, original-byte/pointer/record protection, actual UI retry, every original destination hash, final marker and next-backup displaced-save checks. Candidate16 and installed product bytes unchanged.',
  'resolution':resolution,'state':'prepared, not submitted'},indent=2)+'\n')
 files=sorted(p for p in owner.iterdir() if p.is_file())
 (owner/'harness.sha256').write_text(''.join(hashlib.sha256(p.read_bytes()).hexdigest()+'  '+str(p)+'\n' for p in files))
 print(owner)

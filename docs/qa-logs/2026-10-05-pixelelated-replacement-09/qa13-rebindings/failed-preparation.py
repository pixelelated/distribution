from pathlib import Path
import ast,datetime,hashlib,json,shutil,subprocess
root=Path('/workspace/repos/rocknix.worktrees/conflict-resolution')
dest=root/'docs/qa-logs/2026-10-05-pixelelated-replacement-09/qa13-rebindings';dest.mkdir()
base=Path('/workspace/tmp');old='/workspace/tmp/pixelelated-m7-qa-11';new='/workspace/tmp/pixelelated-m7-qa-13'
assert json.loads((Path(new)/'completion.json').read_text())['actual_tool_rc']==0
names=['boot-qualification-03','image-10','settings-09','link-09','guest-09','runtime-10','predecessor-06','cloud-ui-04','signin-ui-04','signin-1g-04']
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
prepared=[]
for name in names:
 owner=base/('pixelelated-m7-'+name)
 for f in ['qa.start','start','inner.rc','outer.rc','tool-wrapper.rc']:assert not (owner/f).exists(),(name,f)
 members=[];changes={}
 for line in (owner/'harness.sha256').read_text().splitlines():
  wanted,filename=line.split(None,1);p=Path(filename);assert sha(p)==wanted;members.append(p)
  if p.suffix in {'.py','.sh'} and old in p.read_text():
   text=p.read_text().replace(old,new)
   if p.suffix=='.py':ast.parse(text)
   changes[p]=text
 assert changes,name
 prepared.append((owner,members,changes))
rows=[]
for owner,members,changes in prepared:
 out=dest/owner.name;out.mkdir();backup=owner/'before-qa13';backup.mkdir()
 shutil.copyfile(owner/'harness.sha256',backup/'harness.sha256');shutil.copyfile(owner/'harness.sha256',out/'harness-before.sha256')
 for p,text in changes.items():
  shutil.copyfile(p,backup/p.name);p.write_text(text)
  if p.suffix=='.sh':subprocess.run(['bash','-n',str(p)],check=True)
  shutil.copyfile(p,out/p.name)
 receipt={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'owner':str(owner),'unstarted':True,'previous_dependency':old,'new_dependency':new,'changed_files':[str(p) for p in changes],'assertions_unchanged':True,'reason':'Same09 fourteen-suite original proof plus corrected comparison/actual upgrade accepted in QA13; QA11 remains failed/clean disk.'}
 rp=owner/'qa13-rebinding.json';rp.write_text(json.dumps(receipt,indent=2)+'\n');members.append(rp)
 (owner/'harness.sha256').write_text(''.join(f'{sha(p)}  {p}\n' for p in sorted(members)))
 shutil.copyfile(rp,out/rp.name);shutil.copyfile(owner/'harness.sha256',out/'harness.sha256');rows.append(receipt)
(dest/'rebindings.json').write_text(json.dumps(rows,indent=2)+'\n')
print('Rebound and resealed',len(rows),'strictly unstarted owners; original source/seals retained.')

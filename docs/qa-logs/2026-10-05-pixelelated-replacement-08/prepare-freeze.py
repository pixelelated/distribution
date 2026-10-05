from pathlib import Path
import datetime,hashlib,json,os,re,subprocess,shutil
repo=Path('/workspace/repos/rocknix');tree=Path('/workspace/repos/rocknix.worktrees/m7-pixelelated-replacement08');owner=Path('/workspace/tmp/pixelelated-m7-replacement-08');prev=Path('/workspace/tmp/pixelelated-m7-replacement-07')
publication=json.loads(Path('/tmp/pixelelated-replacement08-published.json').read_text());commit=publication['next']
es='f6f0c134212bc696f2f6a747c8d390a588f2f0ce'
assert subprocess.check_output(['git','-C',str(repo),'rev-parse','next'],text=True).strip()==commit
assert not subprocess.check_output(['git','-C',str(repo),'status','--porcelain'],text=True).strip()
assert subprocess.check_output(['git','-C','/home/max/Development/emulationstation-next.worktrees/qa-integration','rev-parse','HEAD'],text=True).strip()==es
for n in ['new','syntax','lifetime']:assert Path('/tmp/pixelelated-gpu436-controls/'+n+'.rc').read_text().strip()=='0'
assert Path('/tmp/pixelelated-gpu436-controls/old.rc').read_text().strip()=='1'
assert json.loads((prev/'build-attempt-02/completion.json').read_text())['actual_tool_rc']==0
assert not tree.exists() and not owner.exists()
subprocess.run(['git','-C',str(repo),'worktree','add','-b','build/m7-pixelelated-replacement08',str(tree),commit],check=True)
owner.mkdir();(owner/'copy-artifacts').mkdir()
j=json.loads((prev/'inputs.json').read_text());files={};links={}
for raw in subprocess.check_output(['git','-C',str(tree),'ls-files','-z','--','packages','projects','scripts','config','distributions','Makefile','LICENSE.md','TRADEMARK.md','tools/watch-build','tools/watch-job']).split(b'\0'):
 if not raw:continue
 name=os.fsdecode(raw);p=tree/name
 if p.is_symlink():links[name]=os.readlink(p)
 elif p.is_file():files[name]=hashlib.sha256(p.read_bytes()).hexdigest()
 else:raise RuntimeError(name)
assert set(files)==set(j['source_files']) and links==j['source_symlinks']
changed=sorted(p for p,h in files.items()if h!=j['source_files'][p]);expected=['projects/ROCKNIX/packages/ui/emulationstation/package.mk'];assert changed==expected,changed
qa={os.fsdecode(p):hashlib.sha256((tree/os.fsdecode(p)).read_bytes()).hexdigest()for p in subprocess.check_output(['git','-C',str(tree),'ls-files','-z','--','tools']).split(b'\0')if p and (tree/os.fsdecode(p)).is_file()}
assert sorted(p for p in qa if qa[p]!=j['qa_source_files'].get(p))==['tools/vm-qa']
assert hashlib.sha256(Path(j['host_options_path']).read_bytes()).hexdigest()==j['host_options_sha256']
assert subprocess.check_output(['docker','image','inspect',j['container'],'--format','{{.Id}}'],text=True).strip()==j['container_image_id']
previous_commit=j['distribution_commit']
j.update(distribution_commit=commit,distribution_branch='build/m7-pixelelated-replacement08',emulationstation_commit=es,frozen_at=datetime.datetime.now(datetime.timezone.utc).isoformat(),build_mode='independent checksum/inode-verified copy of completed a258 root; canonical container path; rebuild ES/image',source_files=files,source_symlinks=links,qa_source_files=qa,host_worktree=str(tree),cache_parent_distribution=previous_commit,cache_parent_manifest_sha256=hashlib.sha256((prev/'inputs.json').read_bytes()).hexdigest(),cache_parent_bundle=(prev/'bundle.path').read_text().strip().split('/')[-1],purpose='M7.P3 System Settings empty GPU capability crash #436; retain splash/proxy repairs')
p=owner/'inputs.json';p.write_text(json.dumps(j,sort_keys=True,indent=2)+'\n');p.chmod(0o400)
receipt={'manifest_sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'source_files':len(files),'source_symlinks':len(links),'qa_source_files':len(qa),'changed_inputs':changed,'commit':commit,'emulationstation_commit':es};(owner/'freeze-receipt.json').write_text(json.dumps(receipt,indent=2)+'\n')
def adapt(s):return s.replace('m7-pixelelated-replacement07','m7-pixelelated-replacement08').replace('pixelelated-m7-replacement-07','pixelelated-m7-replacement-08')
for name in ['verify-source.py','build.sh','outer.sh']:
 source=prev/('build-attempt-02/'+name if name in ['build.sh','outer.sh'] else name)
 s=adapt(source.read_text()).replace('pixelelated-m7-replacement-08/build-attempt-02','pixelelated-m7-replacement-08')
 if name=='build.sh':
  s=s.replace('for TASK_PACKAGE in busybox raofflineproxy;','for TASK_PACKAGE in emulationstation;')
  s=s.replace(' build.pixelelated-GENERIC_X64.x86_64/.stamps/linux/build_target','')
  assert 'Refusing build: start watch-build from the frozen worktree' in s
 p=owner/name;p.write_text(s);p.chmod(0o755)
copy=(prev/'copy-cache.sh').read_text()
copy=re.sub(r'm7-pixelelated-replacement0[67]',lambda m:'m7-pixelelated-replacement0'+{'6':'7','7':'8'}[m.group()[-1]],copy)
copy=re.sub(r'pixelelated-m7-replacement-0[67]',lambda m:'pixelelated-m7-replacement-0'+{'6':'7','7':'8'}[m.group()[-1]],copy)
copy=copy.replace(previous_commit,commit)
a,b=copy.split('assert product==',1);_,c=b.split(',product',1);copy=a+'assert product=='+repr(expected)+',product'+c
(owner/'copy-cache.sh').write_text(copy);(owner/'copy-cache.sh').chmod(0o755)
shutil.copy2(prev/'progress.py',owner/'progress.py')
(owner/'copy-outer.sh').write_text('#!/bin/bash\nset -uo pipefail\n'+str(owner)+'/copy-cache.sh\nresult=$?\nprintf "%s\\n" "$result" > '+str(owner)+'/copy.outer.rc\nexit "$result"\n');(owner/'copy-outer.sh').chmod(0o755)
shutil.copy2(prev/'package-freshness.log',owner/'package-freshness-inherited07.log')
for p in owner.glob('*.sh'):subprocess.run(['bash','-n',str(p)],check=True)
for p in owner.glob('*.py'):compile(p.read_text(),str(p),'exec')
subprocess.run(['python3',str(owner/'verify-source.py')],cwd=tree,check=True)
(owner/'harness.sha256').write_text(''.join(hashlib.sha256((owner/name).read_bytes()).hexdigest()+'  '+str(owner/name)+'\n'for name in ['build.sh','outer.sh','verify-source.py','copy-cache.sh','copy-outer.sh','progress.py']))
print(json.dumps(receipt,indent=2))

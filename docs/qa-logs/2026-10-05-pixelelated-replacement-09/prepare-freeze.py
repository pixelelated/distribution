from pathlib import Path
import datetime,hashlib,json,os,re,subprocess,shutil
repo=Path('/workspace/repos/rocknix');tree=Path('/workspace/repos/rocknix.worktrees/m7-pixelelated-replacement09');owner=Path('/workspace/tmp/pixelelated-m7-replacement-09');prev=Path('/workspace/tmp/pixelelated-m7-replacement-08')
publication=json.loads(Path('/tmp/pixelelated-replacement09-source-published.json').read_text());commit=publication['next'];j=json.loads((prev/'inputs.json').read_text());es=j['emulationstation_commit'];sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
assert subprocess.check_output(['git','-C',str(repo),'rev-parse','next'],text=True).strip()==commit
assert not subprocess.check_output(['git','-C',str(repo),'status','--porcelain'],text=True).strip()
assert subprocess.check_output(['git','-C','/home/max/Development/emulationstation-next.worktrees/qa-integration','rev-parse','HEAD'],text=True).strip()==es
assert json.loads((prev/'completion.json').read_text())['actual_tool_rc']==0
assert json.loads(Path('/workspace/tmp/pixelelated-m7-boot-qualification-02/completion.json').read_text())['actual_tool_rc']==0
assert not tree.exists() and not owner.exists()
subprocess.run(['git','-C',str(repo),'worktree','add','-b','build/m7-pixelelated-replacement09',str(tree),commit],check=True)
owner.mkdir();(owner/'copy-artifacts').mkdir();files={};links={}
for raw in subprocess.check_output(['git','-C',str(tree),'ls-files','-z','--','packages','projects','scripts','config','distributions','Makefile','LICENSE.md','TRADEMARK.md','tools/watch-build','tools/watch-job']).split(b'\0'):
 if not raw:continue
 name=os.fsdecode(raw);p=tree/name
 if p.is_symlink():links[name]=os.readlink(p)
 elif p.is_file():files[name]=sha(p)
 else:raise RuntimeError(name)
oldpatch='projects/ROCKNIX/packages/network/raofflineproxy/patches/018-rasteratops-platform-identity.patch';newpatch=oldpatch.replace('018-rasteratops','018-pixelelated')
assert set(files)-set(j['source_files'])=={newpatch} and set(j['source_files'])-set(files)=={oldpatch}
assert links==j['source_symlinks']
assert all(h==j['source_files'][p] for p,h in files.items() if p!=newpatch)
oldbytes=(Path(j['host_worktree'])/oldpatch).read_bytes();assert oldbytes.replace(b', \'OS_NAME="RASTERATOPS"\'',b'')==(tree/newpatch).read_bytes()
expected=sorted([oldpatch,newpatch]);qa={os.fsdecode(p):sha(tree/os.fsdecode(p)) for p in subprocess.check_output(['git','-C',str(tree),'ls-files','-z','--','tools']).split(b'\0') if p and (tree/os.fsdecode(p)).is_file()}
assert qa==j['qa_source_files'];assert sha(Path(j['host_options_path']))==j['host_options_sha256']
assert subprocess.check_output(['docker','image','inspect',j['container'],'--format','{{.Id}}'],text=True).strip()==j['container_image_id']
previous_commit=j['distribution_commit'];j.update(distribution_commit=commit,distribution_branch='build/m7-pixelelated-replacement09',frozen_at=datetime.datetime.now(datetime.timezone.utc).isoformat(),build_mode='independent checksum/inode-verified copy of completed72121 root; canonical container path; rebuild proxy/image',source_files=files,source_symlinks=links,qa_source_files=qa,host_worktree=str(tree),cache_parent_distribution=previous_commit,cache_parent_manifest_sha256=sha(prev/'inputs.json'),cache_parent_bundle=(prev/'bundle.path').read_text().strip().split('/')[-1],purpose='M7.P3 remove unshipped proxy OS identity #409; retain installed GPU and splash repairs')
p=owner/'inputs.json';p.write_text(json.dumps(j,sort_keys=True,indent=2)+'\n');p.chmod(0o400)
receipt={'manifest_sha256':sha(p),'source_files':len(files),'source_symlinks':len(links),'qa_source_files':len(qa),'changed_inputs':expected,'commit':commit,'emulationstation_commit':es};(owner/'freeze-receipt.json').write_text(json.dumps(receipt,indent=2)+'\n')
def adapt(s):return s.replace('m7-pixelelated-replacement08','m7-pixelelated-replacement09').replace('pixelelated-m7-replacement-08','pixelelated-m7-replacement-09')
expected_config=Path('/tmp/pixelelated-proxy-identity-side-a6zv2vqr/linux/raofflineproxy/config.py');assert 'RASTERATOPS' not in expected_config.read_text();shutil.copy2(expected_config,owner/'expected-proxy-config.py')
for name in ['verify-source.py','build.sh','outer.sh']:
 s=adapt((prev/name).read_text())
 if name=='build.sh':
  s=s.replace('for TASK_PACKAGE in emulationstation;','for TASK_PACKAGE in raofflineproxy;')
  anchor="print('PASS assembled initramfs quiet fallback, OS_NAME export, XML/text, proxy, identity and licence payload',flush=True)"
  assert anchor in s
  s=s.replace(anchor,"import hashlib\nproxy_source=Path(j['build_root'])/'build'/('raofflineproxy-'+j['proxy_commit'])/'linux/raofflineproxy/config.py'\nassert hashlib.sha256(proxy_source.read_bytes()).hexdigest()=="+repr(sha(expected_config))+"\n"+anchor)
 p=owner/name;p.write_text(s);p.chmod(0o755)
copy=(prev/'copy-cache.sh').read_text();mapping={'m7-pixelelated-replacement07':'m7-pixelelated-replacement08','m7-pixelelated-replacement08':'m7-pixelelated-replacement09','pixelelated-m7-replacement-07':'pixelelated-m7-replacement-08','pixelelated-m7-replacement-08':'pixelelated-m7-replacement-09'};pattern=re.compile('|'.join(map(re.escape,mapping)));copy=pattern.sub(lambda m:mapping[m.group()],copy).replace(previous_commit,commit)
# Renames must enumerate both old and new input paths, independent of Git rename heuristics.
copy=copy.replace("'diff','--name-only'","'diff','--no-renames','--name-only'")
a,b=copy.split('assert product==',1);_,c=b.split(',product',1);copy=a+'assert product=='+repr(expected)+',product'+c
(owner/'copy-cache.sh').write_text(copy);(owner/'copy-cache.sh').chmod(0o755)
shutil.copy2(prev/'progress.py',owner/'progress.py');(owner/'copy-outer.sh').write_text(adapt((prev/'copy-outer.sh').read_text()));(owner/'copy-outer.sh').chmod(0o755)
shutil.copy2(prev/'package-freshness-inherited07.log',owner/'package-freshness-inherited07.log')
for p in owner.glob('*.sh'):subprocess.run(['bash','-n',str(p)],check=True)
for p in owner.glob('*.py'):compile(p.read_text(),str(p),'exec')
subprocess.run(['python3',str(owner/'verify-source.py')],cwd=tree,check=True)
(owner/'harness.sha256').write_text(''.join(sha(owner/name)+'  '+str(owner/name)+'\n' for name in ['build.sh','outer.sh','verify-source.py','copy-cache.sh','copy-outer.sh','progress.py','expected-proxy-config.py']))
print(json.dumps(receipt,indent=2))

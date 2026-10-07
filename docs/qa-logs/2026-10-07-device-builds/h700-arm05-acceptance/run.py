from pathlib import Path
import datetime,hashlib,json,os,subprocess,sys,time
owner=Path(__file__).resolve().parent
build_owner=Path('/workspace/tmp/pixelelated-m7-h700-arm-05')
tree=Path('/workspace/repos/rocknix.worktrees/m7-pixelelated-h700-01')
(owner/'run.path').write_text(str(Path.cwd()/os.environ['RASTERATOPS_BUILD_RUN'])+'\n')
rc=1
try:
 for path,sha in json.loads((owner/'seal.json').read_text()).items():assert hashlib.sha256(Path(path).read_bytes()).hexdigest()==sha
 run=Path((build_owner/'run.path').read_text().strip())
 pids=[json.loads((build_owner/'launcher-pid.json').read_text())['pid']]+[int((run/n).read_text()) for n in ['build.pid','watcher.pid','command.pid']]
 while not (build_owner/'launcher-result.json').exists() or any(Path('/proc',str(pid)).exists() for pid in pids):
  print('Waiting for H700 arm05 owner completion and process exit',flush=True);time.sleep(15)
 assert not (build_owner/'owner-verification.json').exists(),'Owner already verified elsewhere; inspect rather than overwrite'
 subprocess.run(['python3','-I',str(owner/'verify-owner.py'),str(build_owner)],check=True)
 verified=json.loads((build_owner/'owner-verification.json').read_text())
 actual=json.loads((build_owner/'runtime-start.json').read_text())
 current=subprocess.check_output(['docker','ps','-aq','--no-trunc'],text=True).split()
 for row in actual['containers']:
  assert row['id'] not in current and not Path('/proc',str(row['host_pid'])).exists(),row['id']
 if verified['result']!='PASS':
  (owner/'artifacts/acceptance.json').write_text(json.dumps({'result':'BUILD_FAILED','owner_verified':verified,'container_exited':True,'utc':datetime.datetime.now(datetime.timezone.utc).isoformat()},indent=2)+'\n')
  raise RuntimeError('H700 arm build failed; retain original owner and investigate')
 subprocess.run(['python3','-I',str(build_owner/'verify-source.py')],cwd=tree,check=True)
 output=build_owner/'artifacts/output-manifest.json';m=json.loads(output.read_text());assert m['result']=='PASS'
 root=tree/'build.pixelelated-H700.arm';installed=root/'image/system';actual_files=set();actual_links={};elf=[]
 for p in installed.rglob('*'):
  name=str(p.relative_to(installed))
  if p.is_symlink():actual_links[name]=os.readlink(p)
  elif p.is_file():
   actual_files.add(name);assert hashlib.file_digest(p.open('rb'),'sha256').hexdigest()==m['files'][name],name
   with p.open('rb') as f:header=f.read(20)
   if header[:6]==b'\x7fELF\x01\x01' and header[18:20]==b'\x28\x00':elf.append(name)
 assert actual_files==set(m['files']) and actual_links==m['symlinks']
 assert set(elf)==set(m['arm_elf'])
 assert 'usr/bin/retroarch' in elf and any('libretro' in name and name.endswith('.so') for name in elf)
 assert (root/'.stamps/arm/build_target').is_file()
 for name,sha in m['stamps'].items():assert hashlib.sha256((root/name).read_bytes()).hexdigest()==sha,name
 with (owner/'artifacts/retroarch-readelf.txt').open('x') as out:
  subprocess.run(['readelf','-h','-l',str(installed/'usr/bin/retroarch')],check=True,stdout=out)
 receipt={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'result':'PASS','scope':'H700 arm compatibility artifact; no aarch64 firmware or physical-device claim','distribution_commit':subprocess.check_output(['git','-C',str(tree),'rev-parse','HEAD'],text=True).strip(),'actual_containers_exited':[x['id'] for x in actual['containers']],'actual_container_host_pids_exited':[x['host_pid'] for x in actual['containers']],'files_independently_hashed':len(actual_files),'symlinks_verified':len(actual_links),'arm_elf_objects':len(elf),'retroarch_and_libretro_arm_elf':True,'build_stamps_verified':len(m['stamps']),'output_manifest_sha256':hashlib.sha256(output.read_bytes()).hexdigest(),'owner_results':verified['channels'],'sealed_build_inputs':verified['sealed_inputs'],'tracked_status':subprocess.check_output(['git','-C',str(tree),'status','--porcelain'],text=True)}
 (owner/'artifacts/acceptance.json').write_text(json.dumps(receipt,indent=2)+'\n');print(json.dumps(receipt),flush=True)
 rc=0
finally:
 (owner/'inner.rc').write_text(str(rc)+'\n');(owner/'outer.rc').write_text(str(rc)+'\n')
sys.exit(rc)

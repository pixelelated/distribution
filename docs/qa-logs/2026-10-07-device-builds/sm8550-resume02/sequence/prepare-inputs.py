"""Create the new immutable build input record after accepted recovery."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,os,subprocess
sequence=Path(__file__).resolve().parent
c=json.loads((sequence/'configuration.json').read_text())
tree=Path(c['tree']);owner=Path(c['build_owner']);previous=Path(c['failed_owner'])
def read(p):return json.loads(Path(p).read_text())
def sha(p):
 with Path(p).open('rb') as f:return hashlib.file_digest(f,'sha256').hexdigest()
def write(p,j):
 with p.open('x') as f:json.dump(j,f,indent=2,sort_keys=True);f.write('\n')
assert read(Path(c['recovery_owner'])/'owner-verification.json')['result']=='PASS'
assert read(Path(c['recovery_owner'])/'artifacts/recovery.json')['new_commit']==c['new_commit']
assert subprocess.check_output(['git','-C',str(tree),'rev-parse','HEAD'],text=True).strip()==c['new_commit']
assert not subprocess.check_output(['git','-C',str(tree),'status','--porcelain'],text=True).strip()
j=read(previous/'inputs.json');j.update(distribution_commit=c['new_commit'],frozen_at=datetime.now(timezone.utc).isoformat(),build_mode='warm aarch64 after exact eight-scope recovery; accepted ARM unchanged',purpose='M7.P5 #503 FEX repair and #492 SM8550 completion',retry_of=str(previous),recovery_receipt=str(Path(c['recovery_owner'])/'artifacts/recovery.json'),arm_manifest_sha256=c['arm_manifest_sha256'])
j['arm_original_manifest']=j['arm_manifest']
j['arm_original_distribution_commit']=c['old_commit']
j['arm_manifest']=str(owner/'artifacts/arm-output-manifest.json')
assert sha(j['arm_manifest'])==c['arm_manifest_sha256']
old_product=set(j['source_files'])|set(j['source_symlinks'])
names=subprocess.check_output(['git','-C',str(tree),'ls-files','-z','--',*c['product_roots'],'tools/watch-build','tools/watch-job']).decode().split('\0');names=[n for n in names if n]
assert old_product<=set(names)
assert set(names)-old_product==set(c['product_delta']),set(names)-old_product
j['source_files']={n:sha(tree/n) for n in names if not (tree/n).is_symlink()}
j['source_symlinks']={n:os.readlink(tree/n) for n in names if (tree/n).is_symlink()}
j['qa_source_files']={n:sha(tree/n) for n in j['qa_source_files']}
j['qualified_product_delta']=subprocess.check_output(['git','-C',str(tree),'diff','--name-only',j['qualified_product_commit'],c['new_commit'],'--',*c['product_roots']],text=True).splitlines()
j['retry_product_delta']=c['product_delta']
nix=read('/workspace/tmp/pixelelated-m7-fex-guest-controls-02/inputs.json')
for key in ['nix_version','nixpkgs_url','expected_rootfs','toolchain32','toolchain64']:j[key]=nix[key]
j.update(fex_commit='e869aa644a16e4332cdc15c1ea0b4d13d482385d',nix_snapshot=str(Path(c['nix_control'])/'runtime/nixpkgs'),nix_private_store=str(owner/'nix'),nix_dependency_owner=c['nix_control'],nix_retention='Active #503/#492 build input; release private copy after accepted firmware/source custody')
controls=read('/workspace/tmp/pixelelated-m7-fex-guest-controls-02/runtime/control-result.json')
for bits in [32,64]:
 row=next(r for r in controls['records'] if r['case']=='fixed'+str(bits))
 j['guest_libraries'+str(bits)]=sorted(n for n in row['libraries'] if n!='libPlaceholderX11.so')
source=Path(c['nix_control'])/'nix';dest=owner/'nix';assert not dest.exists();dest.mkdir()
subprocess.run(['cp','-a','--reflink=auto',str(source)+'/.',str(dest)],check=True)
files={};links={}
for base,dirs,names in os.walk(source,followlinks=False):
 for name in dirs+names:
  src=Path(base)/name;rel=src.relative_to(source);dst=dest/rel
  if src.is_symlink():assert dst.is_symlink() and os.readlink(src)==os.readlink(dst);links[str(rel)]=os.readlink(src)
  elif src.is_file():
   digest=sha(src);assert digest==sha(dst) and (src.stat().st_dev,src.stat().st_ino)!=(dst.stat().st_dev,dst.stat().st_ino)
   files[str(rel)]=digest
write(owner/'artifacts/nix-private-copy.json',{'result':'PASS','source':str(source),'destination':str(dest),'files':files,'symlinks':links,'independent_inodes':True,'method':'cp -a --reflink=auto; independent readback','retention':j['nix_retention']})
j['nix_private_copy_sha256']=sha(owner/'artifacts/nix-private-copy.json')
j['nix_toolchain_hashes']={nix[key]:sha(source/Path(nix[key]).relative_to('/nix')) for key in ['toolchain32','toolchain64']}
j['nix_archive_hashes']={str(Path(c['nix_control'])/'runtime'/name):sha(Path(c['nix_control'])/'runtime'/name) for name in ['nix.tar.xz','nixpkgs.tar.xz']}
write(owner/'inputs.json',j)
write(owner/'freeze-receipt.json',{'utc':datetime.now(timezone.utc).isoformat(),'distribution_commit':c['new_commit'],'branch':j['distribution_branch'],'inputs_sha256':sha(owner/'inputs.json'),'product_delta':c['product_delta'],'source_files':len(j['source_files']),'arm_carried_from':str(previous),'arm_manifest_sha256':c['arm_manifest_sha256'],'container':j['container'],'global_jobs':24,'webkit_jobs':4,'scope':'Prepared, not submitted; exact FEX repair with original Nix snapshot'})
sealed=['inputs.json','freeze-receipt.json','run.py','verify-source.py','verify-arm.py','verify-fex.py','inside-build.sh','artifacts/arm-output-manifest.json']
write(owner/'seal.json',{str(owner/n):sha(owner/n) for n in sealed})
accept=Path(c['accept_owner'])
write(accept/'seal.json',{str(accept/n):sha(accept/n) for n in ['run.py','verify-firmware.py','verify-owner.py']})
subprocess.run(['python3','-I',str(owner/'verify-source.py')],cwd=tree,check=True)
print('PASS fresh SM8550 inputs include new patch, original ARM and private exact Nix copy',flush=True)

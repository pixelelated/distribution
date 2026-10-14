#!/usr/bin/env python3
"""Bind the qa19/20 standard runner sequence to completed final image inputs; UNRUN."""
import argparse,hashlib,json,os,re,shutil,stat,subprocess
from pathlib import Path,PurePosixPath
HERE=Path(__file__).resolve().parent
MINIO='sha256:14cea493d9a34af32f524e538b8346cf79f3321eff8e708c1e2960462bd8936e'
def sha(p):
 with p.open('rb') as f:return hashlib.file_digest(f,'sha256').hexdigest()
def write(p,v):
 with p.open('x') as f:json.dump(v,f,indent=2);f.write('\n')
def git(tree,*args):return subprocess.check_output(['git','-C',str(tree),*args],text=True,timeout=30).strip()
def local(root,name):
 pending=list(PurePosixPath('/'+name).parts[1:]);done=[];links=[]
 while pending:
  part=pending.pop(0)
  if part in ('','.'):continue
  if part=='..':assert done;done.pop();continue
  p=root.joinpath(*done,part)
  if p.is_symlink():
   target=os.readlink(p);links.append({'path':'/'+ '/'.join(done+[part]),'target':target});assert len(links)<=40
   target=PurePosixPath(target)
   if target.is_absolute():done=[];pending=list(target.parts[1:])+pending
   else:pending=list(target.parts)+pending
  else:done.append(part)
 return root.joinpath(*done),{'resolved':'/'+ '/'.join(done),'links':links}
p=argparse.ArgumentParser(description=__doc__)
for n in ['checkout','verification','system-root','es-source','retroarch-source','baseline','owner']:p.add_argument('--'+n,type=Path,required=True)
a=p.parse_args();tree=a.checkout.resolve(strict=True);verify=a.verification.resolve(strict=True);out=a.owner.absolute()
assert out.parent==Path('/workspace/tmp') and re.fullmatch('pix[A-Za-z0-9_-]+',out.name) and not out.exists()
assert len(str(out/'runtime/rocknix-qemu-monitor-b.sock').encode())<=107
report=json.loads(verify.read_text());inputs=verify.with_name('inputs.json');meta=json.loads(inputs.read_text())
assert report['status']=='PASS' and not report['runtime_qualified'] and report['source']==meta['source'] and report['es_commit']==meta['es_commit']
commit=report['source'];es_commit=report['es_commit'];assert re.fullmatch('[0-9a-f]{40}',commit) and re.fullmatch('[0-9a-f]{40}',es_commit)
assert git(tree,'rev-parse','HEAD')==commit and not git(tree,'status','--porcelain=v1','--untracked-files=no')
pin=re.search(r'^PKG_VERSION="([0-9a-f]{40})"', (tree/'projects/ROCKNIX/packages/ui/emulationstation/package.mk').read_text(),re.M);assert pin and pin[1]==es_commit
es=a.es_source.resolve(strict=True);assert git(es,'rev-parse','HEAD')==es_commit and not git(es,'status','--porcelain=v1','--untracked-files=no')
root=a.system_root.resolve(strict=True);assert root.is_relative_to(tree) and root.parts[-2:]==('image','system')
installed={}
for name in ['usr/bin/busybox','usr/bin/rclone']:
 p,chain=local(root,name);facts=report['products'][name]
 assert p.is_file() and sha(p)==facts['sha256'] and p.stat().st_size==facts['bytes'] and stat.filemode(p.stat().st_mode)==facts['mode'] and chain==facts['link_chain']
 # last-good-scripts-test executes these ordinary paths on the host; refuse a
 # root-absolute symlink that would escape into the host filesystem.
 assert (root/name).resolve(strict=True)==p
 installed[name]=facts
ra=a.retroarch_source.resolve(strict=True);assert ra.is_relative_to(tree) and (ra/'gfx/video_thread_wrapper.c').is_file()
baseline=a.baseline.resolve(strict=True);assert (baseline/'BASELINE.txt').is_file();baseline_files=[f for f in baseline.rglob('*') if f.is_file()];assert 0<len(baseline_files)<=256 and sum(f.stat().st_size for f in baseline_files)<=128*1024**2
images=[(Path(n),v) for n,v in meta['artifacts'].items() if n.endswith('.img.gz')];assert len(images)==1
image,facts=images[0];assert image.is_file() and image.stat().st_size==facts['bytes'];raw=verify.with_name('candidate.img');assert raw.is_file() and 0<raw.stat().st_size<=16*1024**3
for line in (HERE/'SHA256SUMS').read_text().splitlines():
 h,n=line.split('  ',1);assert sha(HERE/n)==h
names=['vm-pair','vm-qa','vm-serial','vm-stop','cloud-test-backend','cloud-round-trip','emulator-exit-test','time-to-play','vm-visual-qa','frame-diff','last-good-scripts-test','retroarch-wrapper-test','vocabulary-check','es-untranslated','es-menu-map-check','register-check','watch-build-submit','watch-build','watch-job','host-maintenance/build-admission','host-maintenance/retention-report']
files=[tree/'tools'/n for n in names]+list((tree/'tools/vm-walks').rglob('*'))+[tree/'projects/ROCKNIX/devices/GENERIC_X64/vm'/n for n in ['generic-x64-vm','profile.json']]
files=[f for f in files if f.is_file()];assert all(not f.is_symlink() for f in files)
files += [ra/'gfx/video_thread_wrapper.c']+baseline_files
# Exact published ES checkout is also checked before/after the owned run.
files += [es/n for n in ['tests/cloud-oauth-lifetime.py','tests/gpu-governor-save.py','tests/credential-quoting.py']]
assert sum(f.stat().st_size for f in files)<=160*1024**2
out.mkdir(mode=0o700)
for n in ['records','pair','runtime','tmp','cloud','artifacts','scan','lifecycle-owner']:(out/n).mkdir(mode=0o700)
for n in ['run.py','close.py','census.py']:shutil.copyfile(HERE/n,out/n)
shutil.copyfile(verify,out/'records/image-verification.original.json');shutil.copyfile(inputs,out/'records/image-inputs.original.json')
name=out.name.lower()+'-s3';assert len(name)<=63
cfg={'status':'PREPARED_UNRUN','checkout':str(tree),'commit':commit,'es_commit':es_commit,'es_source':str(es),'retroarch_source':str(ra),'system_root':str(root),'installed_host_inputs':installed,'baseline':str(baseline),'image':dict(facts,path=str(image),raw_bytes=raw.stat().st_size),'verification_sha256':sha(verify),'image_inputs_sha256':sha(inputs),'dependencies':{str(f):sha(f) for f in files},'code':{n:sha(out/n) for n in ['run.py','close.py','census.py']},'host_pid_namespace':Path('/proc/self/ns/pid').stat().st_ino,'minio_image':MINIO,'minio_name':name,'work_seconds':5700,'cleanup_seconds':180,'bounds_seconds':{'pair-up':900,'backend-up':120,'standard':3600,'sftp':300,'s3':300,'backend-down':25,'pair-down':70},'record_limit_bytes':512*1024**2,'scratch_budget_bytes':8*1024**3}
write(out/'config.json',cfg)
write(out/'retention-plan.json',{'volume':'/workspace','scan_roots':[str(out/'scan')],'reference_stores':[],'protected':[str(image),str(verify),str(inputs),str(root),str(baseline)],'candidates':[],'builds':[{'name':'m7-final-standard-cloud-baseline','terms_bytes':{'temporary_raw_image':raw.stat().st_size,'two_guest_disks':32*1024**3,'host_fixture_and_backend_margin':8*1024**3,'original_logs_and_frames':512*1024**2},'basis':'Accepted qa19/20 pair+standard WebDAV then SFTP and local MinIO rounds, once per final image. Two unchanged 4CPU/8GiB guests, default boot/profile; existing host controls.5700s work+180s cleanup. No real accounts or providers. No new per-service/cgroup cap claim.','evidence':[{'path':str(out/n),'sha256':sha(out/n)} for n in ['config.json','run.py','records/image-verification.original.json']]}]})
write(out/'admission-plan.json',{'checkout':str(tree),'retention_plan':str(out/'retention-plan.json'),'retention_report':str(out/'retention-report.json'),'stage':'m7-final-standard-cloud-baseline','profiles':[{'PROJECT':'ROCKNIX','DEVICE':'GENERIC_X64','ARCH':'x86_64'}],'outputs':[{'path':str(out),'issue':349,'kind':'qa-scratch','release_when':'Original 15 standard rows and one SFTP/S3 row, failures/restoration/cleanup exported and reviewed; actual owner/guests/backends gone, admission consumed, then explicitly retire private disks/key/backend data/tmp.'}]})
print(json.dumps({'status':'PREPARED_UNRUN','owner':str(out),'command':['python3','-I','-B',str(out/'run.py')]}))

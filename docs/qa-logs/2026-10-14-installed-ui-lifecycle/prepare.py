#!/usr/bin/env python3
"""Prepare one networked installed-UI owner; no VM, service or browser is launched."""
import argparse,hashlib,json,re,shutil,subprocess,tarfile
from pathlib import Path
HERE=Path(__file__).resolve().parent
INNER='c46457c66881e965ba4d5c078a9082aa341fba4dac7679c60665de391e9b1b35'
ARCHIVE='f720474af56d0532d1d898d74c87b8bd5aaac75c83c4aac93f197661de225b6e'
COMMIT='d6a87f05c1935516115b2cca1af22151a0209224'; ES='3178b832b8d134198b2b4eede4f725d4ed283f8c'
def sha(p):
    with p.open('rb') as f:return hashlib.file_digest(f,'sha256').hexdigest()
def write(p,obj):
    with p.open('x') as f:json.dump(obj,f,indent=2);f.write('\n')
def sealed(root,expected):
    assert sha(root/'SHA256SUMS')==expected
    names=set()
    for line in (root/'SHA256SUMS').read_text().splitlines():
        h,n=line.split('  ',1);p=Path(n)
        assert not p.is_absolute() and '..' not in p.parts and n not in names
        assert not (root/p).is_symlink() and sha(root/p)==h;names.add(n)
    assert {str(p.relative_to(root)) for p in root.rglob('*') if p.is_file()}==names|{'SHA256SUMS'}
p=argparse.ArgumentParser(description=__doc__)
for n in ['checkout','verification','archive','owner']:p.add_argument('--'+n,type=Path,required=True)
p.add_argument('--ssh-port',type=int,required=True);p.add_argument('--vnc',type=int,required=True)
p.add_argument('--playwright-python',type=Path,default=Path('/tmp/pixelelated-import-qa-venv/bin/python'))
p.add_argument('--chromium',type=Path,default=Path('/home/max/.cache/ms-playwright/chromium-1223/chrome-linux64/chrome'))
a=p.parse_args();tree=a.checkout.resolve(strict=True);out=a.owner.absolute();verify=a.verification.resolve(strict=True)
assert out.parent==Path('/workspace/tmp') and not out.exists() and re.fullmatch(r'pix[A-Za-z0-9_-]+',out.name)
assert len(str(out/'vm/monitor.sock').encode())<=107
assert 1024<=a.ssh_port<65536 and 100<=a.vnc<=199 and len({a.ssh_port,5900+a.vnc,18080})==3
assert subprocess.check_output(['git','-C',str(tree),'rev-parse','HEAD'],text=True,timeout=15).strip()==COMMIT
report=json.loads(verify.read_text());inputs=verify.with_name('inputs.json');meta=json.loads(inputs.read_text())
assert report['status']=='PASS' and report['source']==meta['source']==COMMIT and report['es_commit']==meta['es_commit']==ES
assert not report['runtime_qualified']
images=[(Path(n),v) for n,v in meta['artifacts'].items() if n.endswith('.img.gz')];assert len(images)==1
image,facts=images[0];assert image.is_file() and image.stat().st_size==facts['bytes'] and re.fullmatch('[0-9a-f]{64}',facts['sha256'])
raw=verify.with_name('candidate.img');assert raw.is_file() and 0<raw.stat().st_size<=16*1024**3
assert a.playwright_python.is_file() and a.chromium.is_file() and sha(a.archive)==ARCHIVE
for line in (HERE/'SHA256SUMS').read_text().splitlines():
    h,n=line.split('  ',1);assert sha(HERE/n)==h,n
helper=tree/'projects/ROCKNIX/devices/GENERIC_X64/vm/generic-x64-vm'
tools=[helper,helper.with_name('profile.json')]+[tree/x for x in ['tools/vm-serial','tools/vm-stop','tools/watch-build','tools/watch-job','tools/watch-build-submit','tools/host-maintenance/build-admission','tools/host-maintenance/retention-report','tools/pixelelated-state-check-test','tools/pixelelated-state-check','docs/qa-logs/2026-10-13-clean-state-565/run-first-boot.sh']]
assert sha(tools[-1])=='a49a0bb3f8b5ed937dafc7524c70e2ce9ce74e925478d421dc0f7e3a20e957da'
out.mkdir(mode=0o700)
for n in ['vm','records','clean','source','scan','lifecycle-owner']:(out/n).mkdir(mode=0o700)
source=out/'source/smoke';source.mkdir()
with tarfile.open(a.archive,'r:gz') as t:
    members=t.getmembers();assert len(members)<100 and sum(m.size for m in members)<1024**2
    for m in members:
        n=Path(m.name);assert not n.is_absolute() and '..' not in n.parts and (m.isfile() or m.isdir())
        dest=source/n
        if m.isdir():dest.mkdir(parents=True,exist_ok=True)
        else:
            dest.parent.mkdir(parents=True,exist_ok=True)
            with dest.open('xb') as f:f.write(t.extractfile(m).read())
sealed(source,INNER)
dependencies=json.loads((source/'dependencies.json').read_text())
for n,h in dependencies.items():assert sha(Path(n))==h,n
# Recent's accepted helper copies this small fixture directory. Bind its complete input set too.
extra=Path('/workspace/repos/rocknix.worktrees/m7-player-setup/docs/qa-logs/2026-10-13-library-setup-source/fixtures')
for f in extra.iterdir():
    if f.is_file():assert not f.is_symlink() and f.stat().st_size<=2*1024**2;dependencies[str(f)]=sha(f)
for n in ['vm-lifecycle.py','guest-postcheck.py','close.py','census.py']:shutil.copyfile(HERE/n,out/n)
shutil.copyfile(verify,out/'records/image-verification.original.json');shutil.copyfile(inputs,out/'records/image-inputs.original.json')
cfg={'status':'PREPARED_UNRUN','checkout':str(tree),'commit':COMMIT,'es_commit':ES,'helper':str(helper),'ssh_port':a.ssh_port,'vnc':a.vnc,'image':dict(facts,path=str(image),raw_bytes=raw.stat().st_size),'verification_sha256':sha(verify),'image_inputs_sha256':sha(inputs),'packet_manifest':INNER,'packet_archive':ARCHIVE,'tools':{str(f):sha(f) for f in tools},'dependencies':dependencies,'code':{n:sha(out/n) for n in ['vm-lifecycle.py','guest-postcheck.py','close.py','census.py']},'playwright_python':str(a.playwright_python.absolute()),'chromium':str(a.chromium.resolve()),'host_pid_namespace':Path('/proc/self/ns/pid').stat().st_ino,'work_seconds':1800,'smoke_seconds':900,'cleanup_seconds':90,'host_record_limit_bytes':256*1024**2}
write(out/'config.json',cfg)
write(out/'retention-plan.json',{'volume':'/workspace','scan_roots':[str(out/'scan')],'reference_stores':[],'protected':[str(image),str(verify),str(inputs),str(source)],'candidates':[],'builds':[{'name':'m7-installed-ui-smoke','terms_bytes':{'raw_disk':raw.stat().st_size,'guest_disk':16*1024**3,'records_browser_temporary_margin':1024**3},'basis':'One fresh canonical networked 4 CPU/8 GiB guest at 640x480. Original clean proof before SSH provisioning. Existing smoke gets hard900s; lifecycle boot/provision/export included in1800s work plus90s cleanup. No host/service cgroup cap claimed. No backend or provider allocation.','evidence':[{'path':str(out/n),'sha256':sha(out/n)} for n in ['config.json','vm-lifecycle.py','records/image-verification.original.json']]}]})
write(out/'admission-plan.json',{'checkout':str(tree),'retention_plan':str(out/'retention-plan.json'),'retention_report':str(out/'retention-report.json'),'stage':'m7-installed-ui-smoke','profiles':[{'PROJECT':'ROCKNIX','DEVICE':'GENERIC_X64','ARCH':'x86_64'}],'outputs':[{'path':str(out),'issue':571,'kind':'qa-scratch','release_when':'Original clean/smoke/restoration/owner results exported and reviewed; actual VM and descendants gone, admission consumed, then explicitly retire disk and temporary key.'}]})
print(json.dumps({'status':'PREPARED_UNRUN','owner':str(out),'command':['python3','-I','-B',str(out/'vm-lifecycle.py')]}))

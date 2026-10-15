#!/usr/bin/env python3
"""UNRUN: prepare only one fresh clean-state/default-loader owner for final d4af image."""
import argparse,hashlib,json,re,shutil,subprocess
from pathlib import Path
HERE=Path(__file__).resolve().parent
COMMIT='d4af5a255f4778a6ecf63ca5b37e05a0f1c83e3a';ES='3178b832b8d134198b2b4eede4f725d4ed283f8c'
VERIFY='57575bcb84179c00e5e71ff341494b30f3103627d7bca2047588dc4dd4b5654d'
INPUTS='be406d291c670610471bb31c01379552f0b4e1bb6c5ff2d73c33f56d103a2bcc'
MEMBERS=['etc/os-release','usr/bin/emulationstation','usr/bin/cloud-signin-window','usr/bin/gst-inspect-1.0','usr/lib/gstreamer-1.0/gst-plugin-scanner','usr/lib/gstreamer-1.0/libgstopengl.so','usr/lib/libgstcontroller-1.0.so.0','usr/lib/libgstreamer-1.0.so.0','usr/lib/libgstnet-1.0.so.0','usr/lib/gstreamer-1.0/libgstadaptivedemux2.so','usr/lib/gstreamer-1.0/libgstrtpmanager.so','usr/lib/gstreamer-1.0/libgstrtsp.so','usr/lib/gstreamer-1.0/libgstudp.so']
def sha(p):
 with Path(p).open('rb') as f:return hashlib.file_digest(f,'sha256').hexdigest()
def write(p,obj):
 with p.open('x') as f:json.dump(obj,f,indent=2);f.write('\n')
p=argparse.ArgumentParser(description=__doc__)
for n in ['checkout','clean-checkout','verification','owner']:p.add_argument('--'+n,type=Path,required=True)
p.add_argument('--vnc',type=int,required=True);a=p.parse_args()
tree=a.checkout.resolve(strict=True);clean_tree=a.clean_checkout.resolve(strict=True);verify=a.verification.resolve(strict=True);out=a.owner.absolute()
assert Path('/proc/self/ns/pid').stat().st_ino==4026531836,'actual host namespace required'
assert out.parent==Path('/workspace/tmp') and re.fullmatch('pix[A-Za-z0-9_-]+',out.name) and not out.exists() and 100<=a.vnc<=199
assert len(str(out/'vm/monitor.sock').encode())<=107
for line in (HERE.parent/'SHA256SUMS').read_text().splitlines():
 h,n=line.split('  ',1);assert sha(HERE.parent/n)==h,n
assert subprocess.check_output(['git','-C',str(tree),'rev-parse','HEAD'],text=True,timeout=15).strip()==COMMIT
assert sha(verify)==VERIFY and sha(verify.with_name('inputs.json'))==INPUTS
report=json.loads(verify.read_text());meta=json.loads(verify.with_name('inputs.json').read_text())
assert report['status']=='PASS' and report['source']==meta['source']==COMMIT and report['es_commit']==meta['es_commit']==ES
images=[(Path(n),v) for n,v in meta['artifacts'].items() if n.endswith('.img.gz')];assert len(images)==1
image,facts=images[0];assert image.is_file() and not image.is_symlink() and image.stat().st_size==facts['bytes'] and image.is_relative_to(tree/'target')
clean=clean_tree/'docs/qa-logs/2026-10-13-clean-state-565/run-first-boot.sh'
assert sha(clean)=='a49a0bb3f8b5ed937dafc7524c70e2ce9ce74e925478d421dc0f7e3a20e957da'
assert sha(clean_tree/'tools/pixelelated-state-check')=='6d061af89caba886bd3417ee96dc01e37675655aa1ed92f423b9db02164dff03'
helper=Path('/workspace/repos/rocknix.worktrees/m7-offline-vm-567/projects/ROCKNIX/devices/GENERIC_X64/vm/generic-x64-vm')
assert sha(helper)=='5b058ed8a8b11135cd5997e3d925939baff30726033125acf1244863a756318d'
assert sha(helper.with_name('profile.json'))=='26c420ecb0cc7aae29050554c55f522e62337cf6726619a59337c073f1c65406'
tools=[helper,helper.with_name('profile.json'),clean]+[tree/n for n in ['tools/vm-serial','tools/vm-stop','tools/watch-build','tools/watch-job','tools/watch-build-submit','tools/host-maintenance/build-admission','tools/host-maintenance/retention-report']]+[clean_tree/n for n in ['tools/pixelelated-state-check','tools/pixelelated-state-check-test','tools/vm-serial']]
clean_tools=json.loads((HERE.parent/'clean-tool-bindings.json').read_text())
for n,h in clean_tools.items():assert sha(clean_tree/n)==h,n
out.mkdir(mode=0o700)
for n in ['vm','records','clean','host-tmp','scan','lifecycle-owner']:(out/n).mkdir(mode=0o700)
for n in ['vm-lifecycle.py','guest.py','close.py','census.py']:shutil.copy2(HERE/n,out/n)
shutil.copy2(verify,out/'records/final-result.json');shutil.copy2(verify.with_name('inputs.json'),out/'records/final-inputs.json')
config={'status':'PREPARED_UNRUN','checkout':str(tree),'commit':COMMIT,'es_commit':ES,'clean_helper':str(clean),'helper':str(helper),'vnc':a.vnc,'image':dict(facts,path=str(image)),'verification_sha256':VERIFY,'inputs_sha256':INPUTS,'members':{n:report['products'][n] for n in MEMBERS},'tools':{str(f):sha(f) for f in tools},'code':{n:sha(out/n) for n in ['vm-lifecycle.py','guest.py','close.py','census.py']},'work_seconds':1800,'cleanup_seconds':90,'host_record_limit_bytes':64*1024**2,'host_pid_namespace':4026531836}
write(out/'config.json',config)
write(out/'retention-plan.json',{'volume':'/workspace','scan_roots':[str(out/'scan')],'reference_stores':[],'protected':[str(HERE.parent),str(image),str(verify),str(verify.with_name('inputs.json')),str(clean_tree),str(tree),str(helper)],'candidates':[],'builds':[{'name':'m7-final-clean-composition','terms_bytes':{'raw_image_ceiling':16*1024**3,'guest_disk':16*1024**3,'records_margin':128*1024**2},'basis':'Fresh 8GiB4CPU/no-NIC guest. Qualified untouched serial clean gate followed by existing three installed default-loader subprocesses.1800s lifecycle work plus90s cleanup. No phone/Wi-Fi/Recent/cloud/backup/gameplay matrix.','evidence':[{'path':str(out/'config.json'),'sha256':sha(out/'config.json')}]}]})
write(out/'admission-plan.json',{'checkout':str(tree),'retention_plan':str(out/'retention-plan.json'),'retention_report':str(out/'retention-report.json'),'stage':'m7-final-clean-composition','profiles':[{'PROJECT':'ROCKNIX','DEVICE':'GENERIC_X64','ARCH':'x86_64'}],'outputs':[{'path':str(out),'issue':344,'kind':'qa-scratch','release_when':'Review untouched clean/installed-loader originals and owner cleanup; consume admission then guarded retirement of only this owner.'}]})
print(json.dumps({'status':'PREPARED_UNRUN','owner':str(out)}))

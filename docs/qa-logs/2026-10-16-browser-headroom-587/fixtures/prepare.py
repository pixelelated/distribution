#!/usr/bin/env python3
"""Prepare one exact077197 fresh 1GiB/no-NIC browser-headroom owner."""
import argparse,hashlib,json,re,shutil,subprocess
from pathlib import Path
HERE=Path(__file__).resolve().parent
COMMIT='077197e6cd3ea31f33b28aaf3882a694b3423b53';ES='16dbac5211eea7e70db7394372033be2be7df829'
VERIFY='9b5651ed408f37175984288309619637d8f5505dd1da2775bdeea88d7029c182'
INPUTS='1683901d927565c902a7d9a743b194bbb35321ac0bbe4a9bc5514e2b3f9a1862'
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
assert subprocess.check_output(['git','-C',str(tree),'rev-parse','HEAD'],text=True,timeout=15).strip()==COMMIT
assert sha(verify)==VERIFY and sha(verify.with_name('inputs.json'))==INPUTS

assert str(verify)=='/workspace/tmp/pix-m7-zerotier-generic-readback-20261015-02/artifacts/result.json'
assert sha(verify)=='9b5651ed408f37175984288309619637d8f5505dd1da2775bdeea88d7029c182'
assert sha(verify.with_name('inputs.json'))=='1683901d927565c902a7d9a743b194bbb35321ac0bbe4a9bc5514e2b3f9a1862'
acceptance=json.loads(Path('/tmp/pix-m7-zerotier-vm-proof-20261015-03/artifact-bindings.json').read_text())
for row in acceptance:assert sha(Path(row['path']))==sha(Path('/tmp/pix-m7-zerotier-vm-proof-20261015-03')/row['copy'])==row['sha256']
consumed=json.loads((Path('/tmp/pix-m7-zerotier-vm-proof-20261015-03/evidence/reader-admission-consumed.json')).read_text())
assert consumed['state']=='consumed' and consumed['id']=='ee024372b00f4314afa9fc96495b83de'
assert consumed['source']['head']=='077197e6cd3ea31f33b28aaf3882a694b3423b53' and all(consumed['original_result'][k]==0 for k in ['command_rc','monitor_rc','runner_rc'])
assert consumed['evidence_sha256']==sha(Path('/tmp/pix-m7-zerotier-vm-proof-20261015-03/evidence/reader-consumption-evidence.json'))

report=json.loads(verify.read_text());meta=json.loads(verify.with_name('inputs.json').read_text())
assert report['status']=='PASS' and report['source']==meta['source']==COMMIT and report['es_commit']==meta['es_commit']==ES
images=[(Path(n),v) for n,v in meta['artifacts'].items() if n.endswith('.img.gz')];assert len(images)==1
image,facts=images[0];assert image.is_file() and not image.is_symlink() and image.stat().st_size==facts['bytes'] and image.is_relative_to(tree/'target')
clean=clean_tree/'docs/qa-logs/2026-10-13-clean-state-565/run-first-boot.sh'
assert sha(clean)=='a49a0bb3f8b5ed937dafc7524c70e2ce9ce74e925478d421dc0f7e3a20e957da'
assert sha(clean_tree/'tools/pixelelated-state-check')=='65ab515ec2c0ccdf474f08128cabf1dea774846a8add3725cd05d334b2e1eba6'
helper=Path('/workspace/repos/rocknix.worktrees/m7-offline-vm-567/projects/ROCKNIX/devices/GENERIC_X64/vm/generic-x64-vm')
assert sha(helper)=='5b058ed8a8b11135cd5997e3d925939baff30726033125acf1244863a756318d'
assert sha(helper.with_name('profile.json'))=='26c420ecb0cc7aae29050554c55f522e62337cf6726619a59337c073f1c65406'
tools=[helper,helper.with_name('profile.json'),clean]+[tree/n for n in ['tools/vm-serial','tools/vm-visual-qa','tools/vm-stop','tools/watch-build','tools/watch-job','tools/watch-build-submit','tools/host-maintenance/build-admission','tools/host-maintenance/retention-report']]+[clean_tree/n for n in ['tools/pixelelated-state-check','tools/pixelelated-state-check-test','tools/vm-serial']]
clean_tools=json.loads((Path('/tmp/pix-m7-zerotier-vm-proof-20261015-03/clean-tool-bindings.json')).read_text())
for n,h in clean_tools.items():assert sha(clean_tree/n)==h,n
tools += [Path(row['path']) for row in acceptance]
out.mkdir(mode=0o700)
(out/'launcher').mkdir(mode=0o700)
shutil.copy2(helper,out/'launcher/generic-x64-vm')
profile=json.loads(helper.with_name('profile.json').read_text());profile['memory_mib']=1024
write(out/'launcher/profile.json',profile)
helper=out/'launcher/generic-x64-vm'
tools += [helper,helper.with_name('profile.json')]
for n in ['vm','records','clean','host-tmp','scan','lifecycle-owner','requests','responses','frames']:(out/n).mkdir(mode=0o700)
for n in ['vm-lifecycle.py','census.py']:shutil.copy2(HERE/n,out/n)
shutil.copy2(verify,out/'records/final-result.json');shutil.copy2(verify.with_name('inputs.json'),out/'records/final-inputs.json')
config={'status':'PREPARED_UNRUN','checkout':str(tree),'commit':COMMIT,'es_commit':ES,'clean_helper':str(clean),'helper':str(helper),'vnc':a.vnc,'image':dict(facts,path=str(image)),'verification_sha256':VERIFY,'inputs_sha256':INPUTS,'members':{n:report['products'][n] for n in MEMBERS},'tools':{str(f):sha(f) for f in tools},'code':{n:sha(out/n) for n in ['vm-lifecycle.py','census.py']},'work_seconds':2400,'cleanup_seconds':90,'host_record_limit_bytes':64*1024**2,'host_pid_namespace':4026531836}
config['zerotier_members']={n:report['products'][n] for n in ['usr/sbin/zerotier-one', 'usr/sbin/zerotier-cli', 'usr/sbin/zerotier-idtool', 'usr/sbin/zerotier-join.sh', 'usr/lib/systemd/system/zerotier-one.service']}
config['zerotier_snapshot']='pix-zt-'+out.name
write(out/'config.json',config)
write(out/'retention-plan.json',{'volume':'/workspace','scan_roots':[str(out/'scan')],'reference_stores':[],'protected':[str(HERE/'prepare.py'),str(image),str(verify),str(verify.with_name('inputs.json')),str(clean_tree),str(tree),str(helper)],'candidates':[],'builds':[{'name':'m7-browser-headroom','terms_bytes':{'raw_image_ceiling':16*1024**3,'guest_disk':16*1024**3,'records_margin':128*1024**2},'basis':'Fresh diagnostic 1GiB4CPU/no-NIC software-rendered guest. Untouched clean gate then service headroom and synthetic queue preservation.2400s lifecycle plus90s cleanup.','evidence':[{'path':str(out/'config.json'),'sha256':sha(out/'config.json')}]}]})
write(out/'admission-plan.json',{'checkout':str(tree),'retention_plan':str(out/'retention-plan.json'),'retention_report':str(out/'retention-report.json'),'stage':'m7-browser-headroom','profiles':[{'PROJECT':'ROCKNIX','DEVICE':'GENERIC_X64','ARCH':'x86_64'}],'outputs':[{'path':str(out),'issue':587,'kind':'qa-scratch','release_when':'Review headroom/lifecycle originals and owner cleanup; consume admission then retire only this disposable guest disk.'}]})
print(json.dumps({'status':'PREPARED_UNRUN','owner':str(out)}))

#!/usr/bin/env python3
"""Prepare only: continue a qualified, stopped retained-update disk; do not launch."""
import argparse,hashlib,json,re,shutil,subprocess
from pathlib import Path
HERE=Path(__file__).resolve().parent
MEMBERS=['etc/os-release','usr/bin/emulationstation','usr/bin/cloud-signin-window','usr/bin/gst-inspect-1.0','usr/lib/gstreamer-1.0/gst-plugin-scanner','usr/lib/gstreamer-1.0/libgstopengl.so','usr/lib/libgstcontroller-1.0.so.0','usr/lib/libgstreamer-1.0.so.0','usr/lib/libgstnet-1.0.so.0','usr/lib/gstreamer-1.0/libgstadaptivedemux2.so','usr/lib/gstreamer-1.0/libgstrtpmanager.so','usr/lib/gstreamer-1.0/libgstrtsp.so','usr/lib/gstreamer-1.0/libgstudp.so']
def sha(p):
    with p.open('rb') as f:return hashlib.file_digest(f,'sha256').hexdigest()
def write(p,obj):
    with p.open('x') as f:json.dump(obj,f,indent=2);f.write('\n')
def load(p):return json.loads(p.read_text())
def shape(p):
    s=p.stat();return {'device':s.st_dev,'inode':s.st_ino,'bytes':s.st_size,'mtime_ns':s.st_mtime_ns,'mode':s.st_mode}
p=argparse.ArgumentParser(description=__doc__)
for n in ['checkout','verification','retained-owner','retained-evidence','owner']:p.add_argument('--'+n,type=Path,required=True)
p.add_argument('--vnc',type=int,required=True)
p.add_argument('--state-checker',type=Path,required=True);p.add_argument('--state-checker-sha256',required=True)
a=p.parse_args();tree=a.checkout.resolve(strict=True);verify=a.verification.resolve(strict=True);prior=a.retained_owner.resolve(strict=True);evidence=a.retained_evidence.resolve(strict=True);out=a.owner.absolute()
assert Path('/proc/self/ns/pid').stat().st_ino==4026531836,'prepare in actual host namespace'
assert prior.parent==out.parent==Path('/workspace/tmp') and not out.exists() and re.fullmatch(r'pix[A-Za-z0-9_-]+',out.name)
assert len(str(out/'vm/monitor.sock').encode())<=107 and 100<=a.vnc<=199
for line in (HERE/'SHA256SUMS').read_text().splitlines():
    h,n=line.split('  ',1);assert sha(HERE/n)==h,n
pc=load(prior/'config.json');pv=load(prior/'vm-result.json');vr=load(verify);inputs=load(verify.with_name('inputs.json'))
assert vr['status']=='PASS' and vr['source']==inputs['source'] and vr['es_commit']==inputs['es_commit']
assert re.fullmatch('[0-9a-f]{40}',vr['source']) and vr['source']!=pc['commit']
assert subprocess.check_output(['git','-C',str(tree),'rev-parse','HEAD'],text=True,timeout=10).strip()==vr['source']
pin=re.search(r'^PKG_VERSION="([0-9a-f]{40})"$',(tree/'projects/ROCKNIX/packages/ui/emulationstation/package.mk').read_text(),re.M);assert pin and pin.group(1)==vr['es_commit']
assert a.state_checker.is_file() and re.fullmatch('[0-9a-f]{64}',a.state_checker_sha256) and sha(a.state_checker)==a.state_checker_sha256
updates=[(Path(n),v) for n,v in inputs['artifacts'].items() if n.endswith('.tar')];assert len(updates)==1
update,facts=updates[0];assert update.is_file() and update.stat().st_size==facts['bytes'] and 0<facts['bytes']<=4*1024**3 and re.fullmatch('[0-9a-f]{64}',facts['sha256'])
assert pv['rc']==0 and not pv['cleanup_errors'] and not pv.get('forced_host_child_cleanup') and not pv['remaining_host_children']
assert len(pv['boots'])==2 and pv['boots'][0]['boot_id']!=pv['boots'][1]['boot_id'] and all(b['interfaces']==['lo'] for b in pv['boots'])
assert all(r['original_returncode']==0 and not r['timed_out'] for r in pv['commands'])
assert [r['phase'] for r in pv['phases']]==['seed','before','after','backup']
assert load(evidence/'analysis.json')['result']=='PASS' and load(evidence/'export-result.json')['original_exit']==0
assert load(evidence/'admission-consumed.json')['state']=='consumed' and load(evidence/'admission-consumed.json')['original_result']=={'command_rc':0,'monitor_rc':0,'runner_rc':0,'utc':load(evidence/'admission-consumed.json')['original_result']['utc']}
assert load(evidence/'host-exits.json')['original_exit']==0
assert all(not Path('/proc',str(pid)).exists() for pid in load(evidence/'host-exits.json')['pids_absent'])
assert not (prior/'vm/vm.pid').exists() and 'down: owned QEMU exited' in (prior/'vm-stop.log').read_text()
assert sha(evidence/'vm-result.json')==sha(prior/'vm-result.json') and sha(evidence/'config.json')==sha(prior/'config.json')
for n,h in pc['verification'].items():assert sha(Path(n))==h
oldreports=[Path(n) for n in pc['verification'] if n.endswith('/result.json')];assert len(oldreports)==1
oldreport=load(oldreports[0]);assert oldreport['status']=='PASS' and oldreport['source']==pc['commit'] and oldreport['es_commit']==pc['es_commit']
for r in pv['phases']:
    assert r['result']=='PASS' and sha(prior/'phases'/r['phase']/(r['phase']+'.result.json'))==r['result_sha256']
for r in load(prior/'guest-manifest.json'):assert sha(prior/'guest'/r['path'])==r['sha256']
assert load(prior/'guest/backup-child.json')=={'returncode':0,'timed_out':False}
assert load(prior/'guest/after.json')['boot']==load(prior/'guest/backup.json')['boot']==pv['boots'][1]['boot_id']
base=prior/'vm/disk.qcow2';ovmf=prior/'vm/OVMF.fd'
assert base.is_file() and not base.is_symlink() and 0<base.stat().st_size<=20*1024**3 and ovmf.is_file() and not ovmf.is_symlink()
helper=Path(pc['helper']);assert sha(helper)==pc['tools'][str(helper)]=='5b058ed8a8b11135cd5997e3d925939baff30726033125acf1244863a756318d'
tools=[helper,helper.with_name('profile.json')]+[tree/n for n in ['tools/vm-serial','tools/vm-stop','tools/watch-build','tools/watch-job','tools/watch-build-submit','tools/host-maintenance/build-admission','tools/host-maintenance/retention-report']]
originals=[verify,verify.with_name('inputs.json'),prior/'config.json',prior/'vm-result.json',prior/'guest-manifest.json',prior/'vm-stop.log']
originals += [prior/'guest'/n for n in ['seed.json','before.json','after.json','backup.json','backup-child.json']]
originals += [Path(n) for n in pc['verification']]
originals += [evidence/n for n in ['analysis.json','acceptance.json','host-exits.json','export-result.json','admission-consumed.json']]
out.mkdir(mode=0o700)
for n in ['vm','records','provenance','scan','host-tmp','lifecycle-owner']:(out/n).mkdir(mode=0o700)
provenance={}
for i,f in enumerate(originals):
    n='provenance/%02d-%s'%(i,f.name);shutil.copyfile(f,out/n);provenance[str(f)]={'copy':n,'sha256':sha(f)}
for n in ['vm-lifecycle.py','guest.py','state.py','close.py','census.py']:shutil.copyfile(HERE/n,out/n)
shutil.copyfile(a.state_checker,out/'state-checker.py')
cfg={'status':'PREPARED_UNRUN','checkout':str(tree),'commit':vr['source'],'es_commit':vr['es_commit'],'previous_commit':pc['commit'],'previous_es_commit':pc['es_commit'],'previous_members':{n:oldreport['products'][n] for n in ['etc/os-release','usr/bin/emulationstation']},'state_checker_sha256':a.state_checker_sha256,'update':dict(facts,path=str(update)),'input_media_bytes':((facts['bytes']+128*1024**2+1024**2-1)//(1024**2))*1024**2,'guest_update_free_bytes':2*facts['bytes']+1024**3,'snapshot_name':'pix572-update-'+out.name,'retained_id':pc['id'],'previous_boots':pv['boots'],'retained_owner':str(prior),'retained_evidence':str(evidence),'base':{'path':str(base),'shape':shape(base)},'ovmf':{'path':str(ovmf),'sha256':sha(ovmf)},'helper':str(helper),'vnc':a.vnc,'tools':{str(f):sha(f) for f in tools},'code':{n:sha(out/n) for n in ['vm-lifecycle.py','guest.py','state.py','close.py','census.py']},'provenance':provenance,'members':{n:vr['products'][n] for n in MEMBERS},'retained_receipts':{n:sha(prior/'guest'/n) for n in ['seed.json','before.json','after.json','backup.json','backup-child.json']},'work_seconds':4200,'cleanup_seconds':180,'host_record_limit_bytes':64*1024**2,'host_pid_namespace':4026531836}
write(out/'config.json',cfg)
write(out/'retention-plan.json',{'volume':'/workspace','scan_roots':[str(out/'scan')],'reference_stores':[],'protected':[str(base),str(ovmf),str(prior),str(evidence),str(verify),str(verify.with_name('inputs.json')),str(update),str(a.state_checker.resolve())],'candidates':[],'builds':[{'name':'m7-retained-installed-loader','terms_bytes':{'overlay_maximum':16*1024**3,'private_update_media':cfg['input_media_bytes'],'records_and_uefi_margin':128*1024**2},'basis':'One normal 8 GiB/4 CPU/no-NIC retained guest; only the owned QCOW2 overlay is writable. Ordinary verified-tar update/reboot then existing installed-loader cases; accepted retained lifecycle4200s work plus180s cleanup. Protected original disk is hashed before/after; no host/service cgroup cap claimed.','evidence':[{'path':str(out/n),'sha256':sha(out/n)} for n in ['config.json','vm-lifecycle.py','guest.py']]}]})
write(out/'admission-plan.json',{'checkout':str(tree),'retention_plan':str(out/'retention-plan.json'),'retention_report':str(out/'retention-report.json'),'stage':'m7-retained-installed-loader','profiles':[{'PROJECT':'ROCKNIX','DEVICE':'GENERIC_X64','ARCH':'x86_64'}],'outputs':[{'path':str(out),'issue':572,'kind':'qa-scratch','release_when':'Review original loader/state/base-hash/owner receipts, actual owners absent and admission consumed, then retire this overlay/OVMF. The previous retained base has its separate owner; coordinator retires it only after this named consumer is done.'}]})
print(json.dumps({'status':'PREPARED_UNRUN','owner':str(out),'base':str(base),'command':['python3','-I','-B',str(out/'vm-lifecycle.py')]}))

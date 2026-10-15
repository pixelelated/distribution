#!/usr/bin/env python3
"""UNRUN. Bind completed relink to one existing qualified no-NIC guest owner."""
import argparse,hashlib,json,re,shutil,subprocess
from pathlib import Path
HERE=Path(__file__).resolve().parent
COMMIT='fac608ff89940ce358ea9b8a95e9a08a6fe26568'
def sha(p):
 with Path(p).open('rb') as f:return hashlib.file_digest(f,'sha256').hexdigest()
def read(p):return json.loads(p.read_text())
def write(p,x):p.write_text(json.dumps(x,indent=2)+'\n')
def seal(p):
 for line in (p/'SHA256SUMS').read_text().splitlines():
  digest,name=line.split('  ',1);assert not Path(name).is_absolute() and '..' not in Path(name).parts and sha(p/name)==digest

def main():
 p=argparse.ArgumentParser(description=__doc__)
 for name in ['checkout','verification','build-owner','owner']:p.add_argument('--'+name,type=Path,required=True)
 p.add_argument('--vnc',type=int,required=True);a=p.parse_args()
 tree=a.checkout.resolve(strict=True);verify=a.verification.resolve(strict=True);build=a.build_owner.resolve(strict=True);out=a.owner.absolute()
 assert out.parent==Path('/workspace/tmp') and re.fullmatch('pix[A-Za-z0-9_-]+',out.name) and not out.exists() and 100<=a.vnc<=199
 seal(HERE);plan=read(HERE/'build-plan.json');stage=build/'stages/dolphin-relink';b=read(stage/'result.json');artifact=read(stage/'target-artifact.json');container=read(stage/'container-result.json')
 assert b['status']==container['status']=='PASS' and b['original_attach_exit']==b['original_container_exit']==b['watchdog_original_exit']==0
 assert b['cleanup']['status']=='PASS' and not b['cleanup']['forced_stop'] and b['cleanup']['exact_id_absent'] and b['cleanup']['survivors']==[]
 assert b['container_result_sha256']==sha(stage/'container-result.json')
 assert artifact['plan_sha256']==sha(HERE/'build-plan.json') and artifact['candidate_source_sha256']==plan['candidate_source_sha256']
 run=Path(read(stage/'watch-run.json')['run']);assert run.parent==tree/'.build-runs'
 launcher=read(stage/'submit/launcher-result.json');watch=read(run/'runner-result.json')
 assert launcher['runner_returncode']==watch['runner_rc']==watch['command_rc']==watch['monitor_rc']==0
 assert (stage/'submit/tool-wrapper.rc').read_text().strip()==(run/'build.rc').read_text().strip()=='0'
 pids=[launcher['pid']]+[int((run/n).read_text()) for n in ['build.pid','command.pid','watcher.pid']]
 assert all(not Path('/proc',str(pid)).exists() for pid in pids)
 candidate=build/'work/dolphin-emu-nogui';assert sha(candidate)==artifact['sha256'] and candidate.stat().st_size==artifact['bytes']
 coordinator_commit=subprocess.check_output(['git','-C',str(tree),'rev-parse','HEAD'],text=True).strip()
 v=read(verify/'result.json');i=read(verify/'inputs.json');assert v['status']=='PASS' and v['source']==i['source']==COMMIT and v['es_commit']==i['es_commit']
 images=[(Path(k),r) for k,r in i['artifacts'].items() if k.endswith('.img.gz')];assert len(images)==1
 image,ir=images[0];assert image.is_file() and not image.is_symlink() and image.stat().st_size==ir['bytes']
 helper=Path('/workspace/repos/rocknix.worktrees/m7-offline-vm-567/projects/ROCKNIX/devices/GENERIC_X64/vm/generic-x64-vm')
 assert sha(helper)=='5b058ed8a8b11135cd5997e3d925939baff30726033125acf1244863a756318d'
 out.mkdir(mode=0o700)
 for n in ['records','scan','logs','vm','source','source/case','source/owner','lifecycle-owner']:(out/n).mkdir()
 for n in ['vm-lifecycle.py','close.py','census.py']:shutil.copy2(HERE/n,out/n)
 case=out/'source/case'
 for n in ['guest-proof.py','run-guest.sh']:shutil.copy2(HERE/n,case/n)
 staged={}
 for name,f in [('dolphin-emu-nogui',candidate),('target-artifact.json',stage/'target-artifact.json'),('build-result.json',stage/'result.json')]:
  assert not f.is_symlink();staged[name]={'source':str(f),'bytes':f.stat().st_size,'sha256':sha(f),'mode':0o444}
 write(case/'inputs.json',{'staged':staged,'build_plan_sha256':sha(HERE/'build-plan.json'),'candidate_source_sha256':plan['candidate_source_sha256'],'source_packet_seal_sha256':sha(HERE/'SHA256SUMS')})
 (case/'SHA256SUMS').write_text(''.join(sha(f)+'  '+f.name+'\n' for f in sorted(case.iterdir())))
 case_seal=sha(case/'SHA256SUMS')
 for n in ['guest-owner.py','guest-manifest.py','census.py']:shutil.copy2(HERE/n,out/'source/owner'/n)
 for name in ['result','inputs']:shutil.copy2(verify/(name+'.json'),out/'records'/('final-image-'+name+'.json'))
 write(out/'source/owner/binding.json',{'case_seal':case_seal,'verification_sha256':sha(verify/'result.json'),'owner_files':{n:sha(out/'source/owner'/n) for n in ['guest-owner.py','guest-manifest.py','census.py']}})
 tools=[helper,helper.parent/'profile.json']+[tree/n for n in ['tools/vm-serial','tools/vm-stop','tools/watch-build','tools/watch-job','tools/watch-build-submit']]
 config={'checkout':str(tree),'coordinator_commit':coordinator_commit,'commit':COMMIT,'es_commit':v['es_commit'],'vnc':a.vnc,'helper':str(helper),'image':{'path':str(image),**ir},'system':v['payload']['SYSTEM'],'verification_sha256':sha(verify/'result.json'),'verification_inputs_sha256':sha(verify/'inputs.json'),'case_seal':case_seal,'tools':{str(f):sha(f) for f in tools},'code':{n:sha(out/n) for n in ['vm-lifecycle.py','close.py','census.py']},'source':{str(f.relative_to(out/'source')):sha(f) for f in sorted((out/'source').rglob('*')) if f.is_file()},'work_seconds':1200,'cleanup_seconds':120,'guest_case_seconds':180,'guest_owner_seconds':210}
 write(out/'config.json',config);write(out/'records/build-basis.json',{'owner':str(build),'stage_result_sha256':sha(stage/'result.json'),'container_result_sha256':sha(stage/'container-result.json'),'runner_result_sha256':sha(run/'runner-result.json'),'launcher_result_sha256':sha(stage/'submit/launcher-result.json'),'source_packet_seal_sha256':sha(HERE/'SHA256SUMS'),'absent_pids':pids})
 write(out/'retention-plan.json',{'volume':'/workspace','scan_roots':[str(out/'scan')],'reference_stores':[],'protected':[str(HERE),str(build),str(out/'source'),str(out/'records'),str(verify),str(image)],'candidates':[],'builds':[{'name':'m7-dolphin-ra-startup','terms_bytes':{'raw_image_ceiling':16*1024**3,'guest_disk':16*1024**3,'input_output_media':512*1024**2,'input_staging':64*1024**2},'basis':'Reused qualified no-NIC8GiB4CPU guest lifecycle; four startup cases only.180s guest work210s owner,1200s host lifecycle120s cleanup. No gameplay, account, award, or cache copy.','evidence':[{'path':str(out/'config.json'),'sha256':sha(out/'config.json')}]}]})
 write(out/'admission-plan.json',{'checkout':str(tree),'retention_plan':str(out/'retention-plan.json'),'retention_report':str(out/'retention-report.json'),'stage':'m7-dolphin-ra-startup','profiles':[{'PROJECT':'ROCKNIX','DEVICE':'GENERIC_X64','ARCH':'x86_64'}],'outputs':[{'path':str(out/'vm'),'issue':584,'kind':'qa-scratch','release_when':'Retain exact case, original guest/host/cleanup exits and candidate/source bindings; consume admission before retiring owned media.'}]})
 print(json.dumps({'status':'PREPARED_UNRUN','owner':str(out)}))
if __name__=='__main__':main()

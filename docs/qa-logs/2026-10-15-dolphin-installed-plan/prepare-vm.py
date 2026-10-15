#!/usr/bin/env python3
"""UNRUN: bind a completed NEW image to three installed Dolphin startup cases."""
import argparse,hashlib,json,re,shutil,subprocess
from pathlib import Path
HERE=Path(__file__).resolve().parent
OLD_COMMIT='fac608ff89940ce358ea9b8a95e9a08a6fe26568'
OLD_EXE='e6c6207d663f7ab53ca6f9fe3c836c98751545b45b869cf32477f7f130e0170b'
HELPER=Path('/workspace/repos/rocknix.worktrees/m7-offline-vm-567/projects/ROCKNIX/devices/GENERIC_X64/vm/generic-x64-vm')
HELPER_SHA='5b058ed8a8b11135cd5997e3d925939baff30726033125acf1244863a756318d'
PROFILE_SHA='26c420ecb0cc7aae29050554c55f522e62337cf6726619a59337c073f1c65406'
BUILD_ROOT='build.pixelelated-GENERIC_X64.x86_64'
def sha(p):
 with Path(p).open('rb') as f:return hashlib.file_digest(f,'sha256').hexdigest()
def read(p):return json.loads(p.read_text())
def write(p,x):p.write_text(json.dumps(x,indent=2)+'\n')
def git(tree,*args):return subprocess.check_output(['git','-C',str(tree),*args],timeout=15).decode().strip()
def seal(p):
 for line in (p/'SHA256SUMS').read_text().splitlines():
  digest,name=line.split('  ',1);assert not Path(name).is_absolute() and '..' not in Path(name).parts and sha(p/name)==digest

def main():
 p=argparse.ArgumentParser(description=__doc__)
 for name in ['checkout','frozen-checkout','verification','owner']:p.add_argument('--'+name,type=Path,required=True)
 for name in ['source-commit','coordinator-commit','es-commit','image-sha256','verification-sha256','verification-inputs-sha256','installed-executable-sha256']:p.add_argument('--'+name,required=True)
 p.add_argument('--vnc',type=int,required=True);a=p.parse_args()
 for name in ['source_commit','coordinator_commit','es_commit']:assert re.fullmatch('[0-9a-f]{40}',getattr(a,name)),name
 for name in ['image_sha256','verification_sha256','verification_inputs_sha256','installed_executable_sha256']:assert re.fullmatch('[0-9a-f]{64}',getattr(a,name)),name
 assert a.source_commit!=OLD_COMMIT and a.installed_executable_sha256!=OLD_EXE,'new completed image required; no known-bad replay'
 tree=a.checkout.resolve(strict=True);frozen=a.frozen_checkout.resolve(strict=True);verify=a.verification.resolve(strict=True);out=a.owner.absolute()
 assert out.parent==Path('/workspace/tmp') and re.fullmatch('pix[A-Za-z0-9_-]+',out.name) and not out.exists() and 100<=a.vnc<=199
 seal(HERE);resources=read(HERE/'resources.json');products=read(HERE/'product-bindings.json')
 assert git(tree,'rev-parse','HEAD')==a.coordinator_commit and git(frozen,'rev-parse','HEAD')==a.source_commit
 assert git(frozen,'status','--porcelain','--untracked-files=all','--',products['package'])==''
 actual={str(f.relative_to(frozen)):sha(f) for f in sorted((frozen/products['package']).rglob('*')) if f.is_file()}
 assert actual==products['files'],'final Dolphin recipe/patches/defaults differ from reviewed source'
 assert sha(verify/'result.json')==a.verification_sha256 and sha(verify/'inputs.json')==a.verification_inputs_sha256
 v=read(verify/'result.json');i=read(verify/'inputs.json')
 assert v['status']=='PASS' and v['source']==i['source']==a.source_commit and v['es_commit']==i['es_commit']==a.es_commit
 assert i['identity']['build_commit']==a.source_commit and i['identity']['dirty']=='no'
 images=[(Path(k),r) for k,r in i['artifacts'].items() if k.endswith('.img.gz')];assert len(images)==1
 image,ir=images[0];assert image.is_relative_to(frozen/'target') and image.is_file() and not image.is_symlink() and image.stat().st_size==ir['bytes'] and ir['sha256']==a.image_sha256
 # Full compressed image hash is checked by the admitted lifecycle before inflation.
 expected=v['products']['usr/bin/dolphin-emu-nogui'];assert expected['sha256']==a.installed_executable_sha256 and expected['link_chain']=={'resolved':'/usr/bin/dolphin-emu-nogui','links':[]}
 staged=frozen/BUILD_ROOT/'image/system';dolphin=frozen/BUILD_ROOT/'build'/('dolphin-sa-'+resources['pin'])
 assert git(dolphin,'rev-parse','HEAD')==resources['pin']
 assert sha(dolphin/'Source/Core/DolphinNoGUI/MainNoGUI.cpp')==products['main_nogui_sha256'],'final build source does not contain qualified lifecycle'
 exe=staged/'usr/bin/dolphin-emu-nogui';assert exe.is_file() and not exe.is_symlink() and sha(exe)==expected['sha256'] and exe.stat().st_size==expected['bytes']
 link=staged/'usr/share/dolphin-emu/sys';assert link.is_symlink() and str(link.readlink())=='../../config/dolphin-emu' and link.resolve(strict=True)==staged/'usr/config/dolphin-emu'
 source_rows=[]
 for r in resources['resources']:
  for f in [dolphin/r['source'],staged/r['installed'],staged/r['resolved'].lstrip('/')]:
   assert f.resolve(strict=True).is_relative_to(frozen) and sha(f)==r['sha256'] and f.stat().st_size==r['bytes']
  row=v['products'][r['installed']];assert row['sha256']==r['sha256'] and row['bytes']==r['bytes'] and row['link_chain']==r['link_chain'] and row['mode']=='-rw-r--r--','final staged/SYSTEM resource readback mismatch'
  source_rows.append({'source':str(dolphin/r['source']),'staged':str(staged/r['installed']),**r})
 assert sha(HELPER)==HELPER_SHA and sha(HELPER.parent/'profile.json')==PROFILE_SHA
 out.mkdir(mode=0o700)
 for n in ['records','scan','logs','vm','source','source/case','source/owner','lifecycle-owner']:(out/n).mkdir()
 for n in ['vm-lifecycle.py','close.py','census.py']:shutil.copy2(HERE/n,out/n)
 case=out/'source/case'
 for n in ['guest-proof.py','run-guest.sh','resources.json']:shutil.copy2(HERE/n,case/n)
 # No executable, candidate overlay, resources or production inputs enter input media.
 write(case/'inputs.json',{'staged':{},'source_commit':a.source_commit,'es_commit':a.es_commit,'installed_executable':expected,'source_packet_seal_sha256':sha(HERE/'SHA256SUMS')})
 (case/'SHA256SUMS').write_text(''.join(sha(f)+'  '+f.name+'\n' for f in sorted(case.iterdir())))
 case_seal=sha(case/'SHA256SUMS')
 for n in ['guest-owner.py','guest-manifest.py','census.py']:shutil.copy2(HERE/n,out/'source/owner'/n)
 for name in ['result','inputs']:shutil.copy2(verify/(name+'.json'),out/'records'/('final-image-'+name+'.json'))
 write(out/'source/owner/binding.json',{'case_seal':case_seal,'verification_sha256':a.verification_sha256,'owner_files':{n:sha(out/'source/owner'/n) for n in ['guest-owner.py','guest-manifest.py','census.py']}})
 tools=[HELPER,HELPER.parent/'profile.json']+[tree/n for n in ['tools/vm-serial','tools/vm-stop','tools/watch-build','tools/watch-job','tools/watch-build-submit']]
 config={'checkout':str(tree),'coordinator_commit':a.coordinator_commit,'frozen_checkout':str(frozen),'commit':a.source_commit,'es_commit':a.es_commit,'vnc':a.vnc,'helper':str(HELPER),'image':{'path':str(image),**ir},'system':v['payload']['SYSTEM'],'verification_sha256':a.verification_sha256,'verification_inputs_sha256':a.verification_inputs_sha256,'case_seal':case_seal,'tools':{str(f):sha(f) for f in tools},'code':{n:sha(out/n) for n in ['vm-lifecycle.py','close.py','census.py']},'source':{str(f.relative_to(out/'source')):sha(f) for f in sorted((out/'source').rglob('*')) if f.is_file()},'work_seconds':1200,'cleanup_seconds':120,'guest_case_seconds':180,'guest_owner_seconds':210}
 write(out/'config.json',config)
 write(out/'records/installed-source-basis.json',{'source_commit':a.source_commit,'frozen_checkout':str(frozen),'package_files':actual,'main_nogui_sha256':sha(dolphin/'Source/Core/DolphinNoGUI/MainNoGUI.cpp'),'installed_executable':expected,'resources':source_rows,'source_packet_seal_sha256':sha(HERE/'SHA256SUMS'),'old_cache_dependency':False})
 write(out/'retention-plan.json',{'volume':'/workspace','scan_roots':[str(out/'scan')],'reference_stores':[],'protected':[str(HERE),str(frozen),str(out/'source'),str(out/'records'),str(verify),str(image),str(HELPER),str(HELPER.parent/'profile.json')],'candidates':[],'builds':[{'name':'m7-dolphin-installed-startup','terms_bytes':{'raw_image_ceiling':16*1024**3,'guest_disk':16*1024**3,'input_output_media':512*1024**2,'input_staging':64*1024**2},'basis':'Qualified no-NIC8GiB4CPU lifecycle; three installed startup cases.180s guest work210s owner,1200s host lifecycle120s cleanup. No old baseline, private binary, resource overlay, gameplay, account or cache copy.','evidence':[{'path':str(out/'config.json'),'sha256':sha(out/'config.json')}]}]})
 write(out/'admission-plan.json',{'checkout':str(tree),'retention_plan':str(out/'retention-plan.json'),'retention_report':str(out/'retention-report.json'),'stage':'m7-dolphin-installed-startup','profiles':[{'PROJECT':'ROCKNIX','DEVICE':'GENERIC_X64','ARCH':'x86_64'}],'outputs':[{'path':str(out/'vm'),'issue':592,'kind':'qa-scratch','release_when':'Retain exact installed resources, case, original guest/host/cleanup exits and final source bindings; consume admission before retiring owned media.'}]})
 print(json.dumps({'status':'PREPARED_UNRUN','owner':str(out)}))
if __name__=='__main__':main()

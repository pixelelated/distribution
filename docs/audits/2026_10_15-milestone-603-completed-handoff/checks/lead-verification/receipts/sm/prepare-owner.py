#!/usr/bin/env python3
"""Bind reviewed device helper templates and fresh measurements; never launch/copy/build."""
from pathlib import Path
import argparse,datetime,hashlib,json,os,re,shutil,subprocess
P=Path(__file__).resolve().parent
COMMIT='9aa7affee9d4ad5e69725cab20b6d7ad84d93dea'
OLD='f8636de1d105275dbf9420bbabbbc26f79abb10f'
GIB=1024**3
PRODUCT=['packages','projects','config','scripts','distributions','Makefile','LICENSE.md','TRADEMARK.md']
def sha(p):
 with p.open('rb') as f:return hashlib.file_digest(f,'sha256').hexdigest()
def git(t,*args):return subprocess.check_output(['git','-C',str(t),*args],text=True).strip()
def put(p,j):
 with p.open('x') as f:json.dump(j,f,indent=2);f.write('\n')
def main():
 q=argparse.ArgumentParser(description=__doc__);q.add_argument('--device',choices=['SM8550'],required=True);q.add_argument('--owner',type=Path,required=True);q.add_argument('--timestamp',required=True)
 for n in ['audit','vm','publication']:
  q.add_argument('--'+n+'-evidence',type=Path,required=True);q.add_argument('--'+n+'-sha256',required=True)
 q.add_argument('--h700-acceptance',type=Path);q.add_argument('--h700-acceptance-sha256');a=q.parse_args();device=a.device;tag=device.lower()
 tree=Path('/workspace/repos/rocknix.worktrees/m7-pixelelated-'+tag+'-05');parent=tree.with_name('m7-pixelelated-'+tag+'-04');owner=a.owner
 assert owner.is_absolute() and owner.parent==Path('/workspace/tmp') and re.fullmatch(r'pix-m7-'+tag+r'-refresh-20261015-[0-9]{2}',owner.name)
 assert owner==Path('/workspace/tmp/pix-m7-sm8550-refresh-20261015-02')
 assert not owner.exists();assert tree.resolve(strict=True)==tree and parent.resolve(strict=True)==parent
 assert git(tree,'rev-parse','HEAD')==COMMIT and git(tree,'branch','--show-current')=='build/'+tree.name
 assert not git(tree,'status','--porcelain')
 assert git(parent,'rev-parse','HEAD')==OLD
 subprocess.run(['python3','-I','-S','-B',str(P/'verify-cache-parent.py'),'--baseline',str(P/'cache-parent-baseline.json')],check=True)
 subprocess.run(['python3','-I','-S','-B',str(P/'verify-source-delta.py'),'--tree',str(tree)],check=True)
 assert git(tree,'merge-base','--is-ancestor',COMMIT,'origin/next')==''
 assert re.fullmatch(r'[0-9]{8}T[0-9]{6}Z',a.timestamp);stamp=datetime.datetime.strptime(a.timestamp,'%Y%m%dT%H%M%SZ').replace(tzinfo=datetime.timezone.utc)
 assert 0<=(datetime.datetime.now(datetime.timezone.utc)-stamp).total_seconds()<86400
 assert os.getuid()==1000 and os.getgid()==1000
 assert os.readlink('/proc/self/ns/pid')=='pid:[4026531836]','actual-host namespace required'
 for line in (P/'SHA256SUMS').read_text().splitlines():h,n=line.split('  ',1);assert sha(P/n)==h,n
 evidence=[]
 for n in ['audit','vm','publication']:
  f=getattr(a,n+'_evidence').resolve(strict=True);h=getattr(a,n+'_sha256');assert re.fullmatch('[0-9a-f]{64}',h) and sha(f)==h
  evidence.append({'role':n,'path':str(f),'sha256':h,'semantic_review':'Root must independently verify completed applicable audit, accepted VM state/affected results, and current published source. Hash binding alone does not establish those facts.'})
 if device=='SM8550':
  assert a.h700_acceptance and a.h700_acceptance_sha256 and sha(a.h700_acceptance)==a.h700_acceptance_sha256
  subprocess.run(['python3','-I','-S','-B',str(P/'verify-h700-acceptance.py'),'--acceptance',str(a.h700_acceptance),'--sha256',a.h700_acceptance_sha256],check=True)
  evidence.append({'role':'completed-H700-independent-acceptance','path':str(a.h700_acceptance.resolve()),'sha256':a.h700_acceptance_sha256})
  hc=json.loads((P/'host-checker-binding.json').read_text())
  assert sha(P/'host-checker/pixelelated-state-check')==hc['host_checker_sha256']=='65ab515ec2c0ccdf474f08128cabf1dea774846a8add3725cd05d334b2e1eba6'
  evidence.append({'role':'corrected-host-checker-binding','path':str(P/'host-checker-binding.json'),'sha256':sha(P/'host-checker-binding.json')})
 roots=['build.pixelelated-'+device+'.arm','build.pixelelated-'+device+'.aarch64']
 for n in roots:assert (parent/n).is_dir() and not (tree/n).exists()
 assert not (tree/'target').exists() and not (tree/'release').exists()
 original=json.loads((P/'originals'/device/'parent-inputs.json').read_text())
 parent_binding=json.loads((P/'cache-parent-baseline.json').read_text())
 assert sha(P/'originals'/device/'parent-inputs.json')==parent_binding['originals']['parent_inputs']['sha256']
 owner.mkdir(mode=0o700);(owner/'artifacts').mkdir();(owner/'cache-launch').mkdir();(owner/'acceptance').mkdir();(owner/'acceptance/artifacts').mkdir()
 rows=[]
 measured=[parent/n for n in roots]+[Path('/workspace/cache/rocknix-sources')]
 if device=='SM8550':measured.append(Path('/workspace/tmp/pix-m7-sm8550-refresh-20261015-01/nix'))
 for i,path in enumerate(measured):
  assert path.is_dir() and path.resolve()==path
  argv=['du','-s','-x','--block-size=1','--',str(path)];r=subprocess.run(argv,capture_output=True,text=True,timeout=300,env=dict(os.environ,LC_ALL='C'))
  (owner/('measurement-'+str(i)+'.stdout')).write_text(r.stdout);(owner/('measurement-'+str(i)+'.stderr')).write_text(r.stderr)
  assert r.returncode==0
  rows.append({'path':str(path),'allocated_bytes':int(r.stdout.split()[0]),'original_returncode':r.returncode,'argv':argv})
 copied=sum(r['allocated_bytes'] for r in rows if r['path']!='/workspace/cache/rocknix-sources')
 measurement={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'rows':rows,'copy_required_bytes':max((500 if device=='H700' else 600)*GIB,copied+300*GIB),'build_required_bytes':300*GIB,'basis':'Fresh allocated bytes plus retained canonical300GiB operating reserve; reserve is an operating bound, not a new build-time/peak prediction.'}
 put(owner/'capacity-measurement.json',measurement)
 j={k:v for k,v in original.items() if k not in ['cache_parent_provenance','nix_archive_hashes','nix_toolchain_hashes','expected_rootfs','toolchain32','toolchain64','nix_snapshot','nix_version','nixpkgs_url','nix_dependency_owner','source_files','source_symlinks','qa_source_files','arm_manifest_sha256']}
 j.update(host_worktree=str(tree),distribution_commit=COMMIT,distribution_branch='build/'+tree.name,build_timestamp=a.timestamp,frozen_at=datetime.datetime.now(datetime.timezone.utc).isoformat(),cache_parent_tree=str(parent),cache_parent_distribution=OLD,cache_roots=roots,cache_preparation_owner=str(owner),emulationstation_commit='16dbac5211eea7e70db7394372033be2be7df829',es_repository='/home/max/Development/emulationstation-next.worktrees/m7-wifi-normal-exit-20261015',purpose='M7 #600 SM8550 ABL checksum retry: independent copies of consumed failed partial build; no accepted parent image or RC/physical action',gate_evidence=evidence,prior_arm_manifest=original['prior_arm_manifest'],arm_manifest=str(owner/'artifacts/arm-output-manifest.json'),container_name='pix-m7-'+tag+'-'+a.timestamp.lower(),container_label='m7-'+tag+'-'+a.timestamp.lower())
 if device=='SM8550':j.update(cache_parent_nix='/workspace/tmp/pix-m7-sm8550-refresh-20261015-01/nix',nix_private_store=str(owner/'nix'),nix_snapshot_policy='Frozen recipe b6018f87 URL; no previous snapshot override',nix_installer_original_bytes_retained=False)
 for stale in ['qualified_bundle','qualified_product_commit','qualified_product_delta','upstream_base','recipe_files','nix_retention','compiler_freeze_at','copy_manifest_sha256','cache_parent_documentation_guard']:j.pop(stale,None)
 j['cache_parent_manifest_sha256']=parent_binding['originals']['parent_inputs']['sha256']
 j['cache_parent_provenance']={'cache_run':parent_binding['cache_run'],'cache_original_result':[0,0,0],'partial_build_run':parent_binding['old_run'],'partial_build_original_result':[2,0,2],'failed_consumed':parent_binding['originals']['failed_consumed'],'accepted_build':False,'parent_binding_sha256':sha(P/'cache-parent-baseline.json')}
 j['build_identity_set']='New SM8550 checksum-repair source and fresh root-supplied timestamp; accepted H700/VM remain f863 with their own original identities.'
 j['build_mode']='Independent verified copies from stopped SM04 after consumed copy0 and normal partial build2; canonical ARM then aarch64 with all 12 normal affected-package cleans.'
 j['shared_source_delta']={'path':'source-delta.json','sha256':sha(P/'source-delta.json'),'guard_sha256':sha(P/'verify-source-delta.py')}
 j['abl_expected_sha256']=sha(P/'abl-expected.json')
 j['prior_arm_manifest_sha256']=sha(Path(j['prior_arm_manifest']))
 assert j['prior_arm_manifest_sha256']==original['prior_arm_manifest_sha256']
 j['cache_parent_guard']={'baseline_sha256':sha(P/'cache-parent-baseline.json'),'guard_sha256':sha(P/'verify-cache-parent.py')}
 j['source_files']={};j['source_symlinks']={};j['qa_source_files']={}
 for group,names in [('source_files',PRODUCT),('qa_source_files',['tools'])]:
  raw=subprocess.check_output(['git','-C',str(tree),'ls-files','-z','--',*names])
  for name in raw.split(b'\0'):
   if not name:continue
   f=tree/os.fsdecode(name)
   if f.is_symlink():j['source_symlinks'][str(f)]=os.readlink(f)
   else:j[group][str(f)]=sha(f)
 j['host_options_sha256']=sha(Path(j['host_options_path']))
 j['selected_account_policy']='Only exact compiled shared ScreenScraper developer pair allowed by separately bound corrected host checker; frozen firmware tools unchanged, no private values serialized. Actual output reader required.'
 j['host_state_checker']=dict(hc,path=str(owner/'acceptance/pixelelated-state-check'))
 put(owner/'inputs.json',j)
 for src in (P/'templates'/device).rglob('*'):
  if src.is_file():
   dst=owner/src.relative_to(P/'templates'/device);dst.write_text(src.read_text().replace('@OWNER@',str(owner)).replace('@TREE@',str(tree)))
 for name in ['verify-additions.py','dolphin-sys-source-manifest.json','proxy-source-proof.json','consume-stage.py','verify-cache-parent.py','cache-parent-baseline.json','verify-source-delta.py','source-delta.json','product-delta.diff','frozen-tools.json','accepted-vm-binding.json','abl-expected.json']:
  shutil.copy2(P/name,owner/name)
 if device=='SM8550':shutil.copy2(P/'verify-fex.py',owner/'verify-fex.py')
 # Frozen identity/pin/product checks and selected host options are repeated by
 # verify-source before copy, build, and independent firmware acceptance.
 put(owner/'copy-seal.json',{n:sha(owner/n) for n in ['copy-cache.sh','copy-cache.py','verify-source.py','verify-cache-parent.py','cache-parent-baseline.json','verify-source-delta.py','source-delta.json','product-delta.diff','frozen-tools.json','accepted-vm-binding.json','abl-expected.json','progress.py','inputs.json','capacity-measurement.json']})
 files=[x for x in owner.iterdir() if x.is_file() and x.suffix in ['.py','.sh','.json'] and x.name not in ['build-seal.json']]
 put(owner/'build-seal.json',{str(x):sha(x) for x in files})
 acc=owner/'acceptance';shutil.copy2(P/'host-checker/pixelelated-state-check',acc/'pixelelated-state-check')
 put(acc/'seal.json',{str(x):sha(x) for x in [acc/'run.py',acc/'verify-firmware.py',acc/'pixelelated-state-check',owner/'inputs.json',owner/'verify-additions.py']})
 for stage,base,need in [('cache',owner/'cache-launch',measurement['copy_required_bytes']),('build',owner,measurement['build_required_bytes']),('acceptance',acc,64*GIB)]:
  scan=base/'empty-retention-scan';scan.mkdir()
  protected=[str(parent),*[str(parent/n) for n in roots],'/workspace/cache/rocknix-sources',str(owner/'capacity-measurement.json')]
  if device=='SM8550':protected.append(j['cache_parent_nix'])
  if stage!='cache':protected += [str(tree/n) for n in roots]
  terms={'independent_cache_copy_and_build_allowance' if stage=='cache' else ('normal_package_build_allowance' if stage=='build' else 'independent_firmware_bundle_and_scratch'):need}
  retention={'volume':'/workspace','scan_roots':[str(scan)],'reference_stores':[],'protected':protected,'candidates':[],'builds':[{'name':'m7-'+tag+'-'+stage,'terms_bytes':terms,'basis':measurement['basis']+' No deletion credit. Empty explicit scan is not whole-volume classification.','evidence':[{'path':str(owner/'capacity-measurement.json'),'sha256':sha(owner/'capacity-measurement.json')}]}]}
  outputs=[{'path':str(tree/n),'kind':'build-cache','issue':555,'release_when':'Queued device build and artifact/source custody accepted, then scoped retention review'} for n in roots]
  outputs += [{'path':str(tree/n),'kind':'firmware','issue':555,'release_when':'Independent artifact acceptance and next immediate named consumer recorded'} for n in ['target','release']]
  outputs += [{'path':str(tree/n),'kind':'qa-scratch','issue':555,'release_when':'Original build channels consumed and compact evidence retained; generated staging no longer needed'} for n in ['.doc_cache','.es_cache','.build-runs']]
  outputs += [{'path':str(owner),'kind':'qa-scratch','issue':555,'release_when':'Original channels consumed and compact immutable evidence retained; preserve required corresponding source'}]
  if device=='SM8550':outputs.append({'path':j['nix_private_store'],'kind':'build-cache','issue':555,'release_when':'FEX build/input provenance and required corresponding source retained; scoped retirement review'})
  if stage=='acceptance':outputs.append({'path':'/workspace/artifacts/pixelelated-candidates','kind':'firmware','issue':555,'release_when':'Required accepted candidate consumer and corresponding-source retention complete'})
  admission={'checkout':str(tree),'container_checkout':j['container_worktree'],'retention_plan':str(base/'retention-plan.json'),'retention_report':str(base/'retention-report.json'),'stage':'m7-'+tag+'-'+stage,'profiles':[{'PROJECT':'ROCKNIX','DEVICE':device,'ARCH':arch} for arch in ['arm','aarch64']],'outputs':outputs}
  put(base/'retention-plan.json',retention);put(base/'admission-plan.json',admission)
 put(owner/'preparation.json',{'status':'PREPARED_UNRUN','source':COMMIT,'owner':str(owner),'packet_sha256':sha(P/'SHA256SUMS'),'input_sha256':sha(owner/'inputs.json'),'measurement_sha256':sha(owner/'capacity-measurement.json'),'cache_copy_executed':False,'build_executed':False,'admission_prepared':False})
 print(json.dumps({'owner':str(owner),'device':device,'source':COMMIT,'status':'PREPARED_UNRUN'}))
if __name__=='__main__':main()

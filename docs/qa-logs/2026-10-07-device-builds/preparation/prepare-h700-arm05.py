from pathlib import Path
import ast,datetime,hashlib,json,os,shutil,subprocess
tree=Path('/workspace/repos/rocknix.worktrees/m7-pixelelated-h700-01');prior=Path('/workspace/tmp/pixelelated-m7-h700-arm-04');owner=Path('/workspace/tmp/pixelelated-m7-h700-arm-05')
recovery=Path('/workspace/tmp/pixelelated-m7-h700-arm04-recovery-01')
assert json.loads((recovery/'owner-verification.json').read_text())['result']=='PASS'
assert json.loads((recovery/'artifacts/recovery.json').read_text())['deleted_payloads']==0
j=json.loads((prior/'inputs.json').read_text())
head=subprocess.check_output(['git','-C',str(tree),'rev-parse','HEAD'],text=True).strip();assert head=='43d0bc3bf47fd858ba8d5c55fbdf52535a0db2aa'
assert not subprocess.check_output(['git','-C',str(tree),'status','--porcelain'],text=True).strip()
paths=['config','distributions','packages','projects','scripts','Makefile']
changed=subprocess.check_output(['git','-C',str(tree),'diff','--name-only',j['qualified_product_commit'],head,'--',*paths],text=True).splitlines()
expected=['projects/ROCKNIX/packages/compat/box86/package.mk','projects/ROCKNIX/packages/compat/lib32/package.mk','projects/ROCKNIX/packages/emulators/libretro/desmume-lr/package.mk','projects/ROCKNIX/packages/emulators/libretro/gpsp-lr/package.mk','projects/ROCKNIX/packages/emulators/libretro/retroarch/package.mk','projects/ROCKNIX/packages/emulators/standalone/daedalusx64-sa/package.mk','projects/ROCKNIX/packages/graphics/spirv-tools/package.mk','scripts/build_distro']
assert changed==expected,changed
allocated=int(subprocess.check_output(['du','-sx','--block-size=1',str(tree/j['build_root'])],text=True).split()[0]);required=(100+18+40)*2**30+max(0,30044336128-allocated)
s=os.statvfs('/workspace');available=s.f_bavail*s.f_frsize;assert available>=required,(available,required)
owner.mkdir(mode=0o700);(owner/'artifacts').mkdir()
j.update(distribution_commit=head,frozen_at=datetime.datetime.now(datetime.timezone.utc).isoformat(),qualified_product_delta=changed,build_mode='preserved warm H700 root; every interrupted or changed package scope moved aside; generated roots use DISTRONAME')
for key in ['source_files','qa_source_files']:j[key]={p:hashlib.sha256((tree/p).read_bytes()).hexdigest() for p in j[key]}
j['source_symlinks']={p:os.readlink(tree/p) for p in j['source_symlinks']}
(owner/'inputs.json').write_text(json.dumps(j,sort_keys=True,indent=2)+'\n')
for name in ['run.py','verify-source.py','inside-build.sh','spirv-host-smoke.py']:
 code=(prior/name).read_text().replace(str(prior),str(owner));(owner/name).write_text(code)
 if name.endswith('.py'):ast.parse(code)
capacity={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'available_bytes':available,'required_remaining_arm_bytes':required,'current_root_allocated_bytes':allocated,'baseline_arm_root_bytes':30044336128,'scope':'arm-stage only; later firmware/SM8550 capacity not established'}
(owner/'capacity.json').write_text(json.dumps(capacity,indent=2)+'\n')
receipt={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'commit':head,'branch':j['distribution_branch'],'qualified_product':j['qualified_product_commit'],'product_delta':changed,'delta_scope':'host GCC12 warning handling plus generated-name build roots and ARM handoffs; source pins/configuration namespace unchanged','inputs_sha256':hashlib.sha256((owner/'inputs.json').read_bytes()).hexdigest(),'source_files':len(j['source_files']),'qa_source_files':len(j['qa_source_files']),'source_symlinks':len(j['source_symlinks']),'container':j['container'],'container_image_id':j['container_image_id'],'global_jobs':j['global_jobs'],'webkit_jobs':j['webkit_jobs'],'scope':'prepared; not submitted'}
(owner/'freeze-receipt.json').write_text(json.dumps(receipt,indent=2)+'\n')
subprocess.run(['python3','-I',str(owner/'verify-source.py')],cwd=tree,check=True)
names=['inputs.json','capacity.json','run.py','verify-source.py','inside-build.sh','spirv-host-smoke.py','freeze-receipt.json']
(owner/'seal.json').write_text(json.dumps({str(owner/n):hashlib.sha256((owner/n).read_bytes()).hexdigest() for n in names},indent=2)+'\n')
print(json.dumps({'freeze':receipt,'capacity':capacity}),flush=True)

from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,os,subprocess,shutil,ast
coord=Path('/workspace/repos/rocknix.worktrees/conflict-resolution')
tree=Path('/workspace/repos/rocknix.worktrees/m7-pixelelated-h700-01')
prior=Path('/workspace/tmp/pixelelated-m7-h700-arm-01')
owner=Path('/workspace/tmp/pixelelated-m7-h700-arm-02')
j=json.loads((prior/'inputs.json').read_text())
assert json.loads((prior/'recovery.json').read_text())['result']=='PASS'
head=subprocess.check_output(['git','-C',str(tree),'rev-parse','HEAD'],text=True).strip()
assert head.startswith('f5f815faff')
assert not subprocess.check_output(['git','-C',str(tree),'status','--porcelain'],text=True).strip()
paths=['config','distributions','packages','projects','scripts','Makefile']
changed=subprocess.check_output(['git','-C',str(tree),'diff','--name-only',j['qualified_product_commit'],head,'--',*paths],text=True).splitlines()
assert changed==['projects/ROCKNIX/packages/graphics/spirv-tools/package.mk'],changed
allocated=int(subprocess.check_output(['du','-sx','--block-size=1',str(tree/j['build_root'])],text=True).split()[0])
required=(100+18+40)*1024**3+max(0,30044336128-allocated)
fs=os.statvfs('/workspace');available=fs.f_bavail*fs.f_frsize
assert available>=required,(available,required)
owner.mkdir(mode=0o700);(owner/'artifacts').mkdir()
j.update(distribution_commit=head,frozen_at=datetime.now(timezone.utc).isoformat(),build_mode='resume preserved warm root; all interrupted package scopes moved aside; host GCC12 repair only',qualified_product_delta=changed)
for key in ['source_files','qa_source_files']:
    j[key]={p:hashlib.sha256((tree/p).read_bytes()).hexdigest() for p in j[key]}
j['source_symlinks']={p:os.readlink(tree/p) for p in j['source_symlinks']}
(owner/'inputs.json').write_text(json.dumps(j,sort_keys=True,indent=2)+'\n')
(owner/'verify-source.py').write_text((prior/'verify-source.py').read_text().replace(str(prior),str(owner)))
(owner/'capacity.json').write_text(json.dumps({'utc':datetime.now(timezone.utc).isoformat(),'available_bytes':available,'required_remaining_arm_bytes':required,'current_root_allocated_bytes':allocated,'baseline_arm_root_bytes':30044336128,'operating_allowance_gib':100,'growth_allowance_gib':40,'artifact_allowance_gib':18,'scope':'arm only; excludes future aarch64/SM8550 fit'},indent=2)+'\n')
shutil.copy2(coord/'.build-runs/spirv-host-smoke.py',owner/'spirv-host-smoke.py')
script='''#!/bin/bash
set -euo pipefail
./scripts/build spirv-tools:host
python3 -I OWNER/spirv-host-smoke.py
./scripts/build_distro
'''.replace('OWNER',str(owner))
(owner/'inside-build.sh').write_text(script)
run=(prior/'run.py').read_text().replace("assert not (tree/j['build_root']).exists()","assert (tree/j['build_root']).is_dir()")
run=run.replace("+str(tree)+'/sources'","+str(tree)+'/sources -v '+str(owner)+':'+str(owner)")
run=run.replace("ARCH=arm ./scripts/build_distro'","ARCH=arm bash "+str(owner)+"/inside-build.sh'")
ast.parse(run);(owner/'run.py').write_text(run)
receipt={'utc':datetime.now(timezone.utc).isoformat(),'commit':head,'branch':j['distribution_branch'],'qualified_product':j['qualified_product_commit'],'product_delta':changed,'delta_scope':'pre_configure_host GCC12 warning severity only; source pins and target flags unchanged','inputs_sha256':hashlib.sha256((owner/'inputs.json').read_bytes()).hexdigest(),'source_files':len(j['source_files']),'qa_source_files':len(j['qa_source_files']),'source_symlinks':len(j['source_symlinks']),'container':j['container'],'container_image_id':j['container_image_id'],'global_jobs':24,'webkit_jobs':4,'scope':'prepared, not submitted'}
(owner/'freeze-receipt.json').write_text(json.dumps(receipt,indent=2)+'\n')
subprocess.run(['python3','-I',str(owner/'verify-source.py')],cwd=tree,check=True)
names=['inputs.json','verify-source.py','run.py','inside-build.sh','spirv-host-smoke.py','capacity.json','freeze-receipt.json']
(owner/'seal.json').write_text(json.dumps({str(owner/n):hashlib.sha256((owner/n).read_bytes()).hexdigest() for n in names},indent=2)+'\n')
print(json.dumps(receipt),flush=True)

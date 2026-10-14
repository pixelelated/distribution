#!/usr/bin/env python3
"""Prepare a fresh serialized host readback owner after engineering completion."""
import argparse
import hashlib
import json
from pathlib import Path
import shlex
import shutil

p=argparse.ArgumentParser(description=__doc__)
p.add_argument('--build-owner',type=Path,required=True)
p.add_argument('--owner',type=Path,required=True)
a=p.parse_args(); source=Path(__file__).resolve().parent; build=a.build_owner.resolve(strict=True); owner=a.owner.absolute()
assert owner.parent==Path('/workspace/tmp') and not owner.exists()
inputs=json.loads((build/'build-inputs.json').read_text()); tree=Path(inputs['checkout'])
run=Path((build/'run.path').read_text().strip())
assert json.loads((run/'admission-consumed.json').read_text())['state']=='consumed'
assert json.loads((build/'owner-result.json').read_text())['status']=='PASS'
assert json.loads((build/'resource-result.json').read_text())['status']=='PASS'
assert json.loads((build/'launcher-result.json').read_text())['runner_returncode']==0
verifier=source/'verify-image.py'; assert verifier.is_file()
owner.mkdir(mode=0o700)
for part in ['artifacts','empty-scan']:(owner/part).mkdir(mode=0o700)
shutil.copy2(verifier,owner/'verify-image.py')
def sha(f):
    with f.open('rb') as stream:return hashlib.file_digest(stream,'sha256').hexdigest()
def write(name,data):(owner/name).write_text(json.dumps(data,indent=2)+'\n')
write('inputs.json',{'scope':'completed image identity and selected installed mappings; no runtime qualification',
 'build_owner':str(build),'build_run':str(run),'source':inputs['commit'],'verifier_sha256':sha(verifier),
 'work_seconds':1500,'cleanup_seconds':15,'host_cpu_affinity':[0],
 'per_process_virtual_memory_bytes':8*1024**3,'scratch_ceiling_bytes':24*1024**3,
 'evidence_basis':'Existing verifier max raw16GiB+SYSTEM4GiB+kernel128MiB+bounded small receipts. No compilation, VM, service, mount or provider.'})
argv=['taskset','-c','0','prlimit','--as='+str(8*1024**3),'--fsize='+str(16*1024**3),'--',
 'timeout','--signal=TERM','--kill-after=15s','1500s','python3','-I',str(owner/'verify-image.py'),
 '--build-owner',str(build),'--output',str(owner/'artifacts')]
(owner/'run.sh').write_text('#!/bin/bash\nset -eu\nexec '+shlex.join(argv)+'\n')
plan={'volume':'/workspace','scan_roots':[str(owner/'empty-scan')],'reference_stores':[],
 'protected':[str(tree/'target'),str(build/'owner-result.json'),str(run/'admission-consumed.json')],
 'candidates':[],'builds':[{'name':'m7-completed-image-readback',
 'terms_bytes':{'bounded_raw_payload_and_records':24*1024**3,'operating_margin':8*1024**3},
 'basis':'Serialized host artifact readback after original compilation owners exited and admission consumed. No claimed reclamation; outputs remain held for immediately queued guest qualification.',
 'evidence':[{'path':str(owner/n),'sha256':sha(owner/n)} for n in ['inputs.json','verify-image.py','run.sh']]}]}
write('retention-plan.json',plan)
write('admission-plan.json',{'checkout':str(tree),'retention_plan':str(owner/'retention-plan.json'),
 'retention_report':str(owner/'retention-report.json'),'stage':'m7-completed-image-readback',
 'profiles':[{'PROJECT':'ROCKNIX','DEVICE':'GENERIC_X64','ARCH':'x86_64'}],
 'outputs':[{'path':str(owner/'artifacts'),'issue':588,'kind':'qa-scratch',
 'release_when':'Immediate clean/default-boot/retained qualification no longer needs raw SYSTEM/KERNEL/image; compact original identity records retained.'}]})
print(json.dumps({'status':'PREPARED_UNRUN','owner':str(owner),'command':['bash',str(owner/'run.sh')]}))

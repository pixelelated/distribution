#!/usr/bin/env python3
"""UNRUN plan preparation. No compiler, container, guest, import of test code or admission granted."""
import argparse
import hashlib
import json
from pathlib import Path
import re

HERE=Path(__file__).resolve().parent


def write(path,value):
    path.write_text(json.dumps(value,indent=2)+'\n')


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--owner',type=Path,required=True)
    p.add_argument('--checkout',type=Path,required=True)
    args=p.parse_args()
    if not re.fullmatch(r'/workspace/tmp/[A-Za-z0-9_-]+',str(args.owner)) or args.owner.resolve()!=args.owner:
        p.error('fresh real /workspace/tmp owner required')
    args.owner.mkdir(mode=0o700)  # not an old owner or old compile invocation
    for name in ('scan','logs','records','submit'): (args.owner/name).mkdir()
    binding=json.loads((HERE/'input-bindings.json').read_text())
    evidence=[{'path':str(HERE/'input-bindings.json'),'sha256':hashlib.sha256((HERE/'input-bindings.json').read_bytes()).hexdigest()}]
    evidence += [{'path':name,'sha256':digest} for name,digest in binding['historical_evidence'].items() if name.endswith('/attempt03/compile-result.json')]
    retention={'volume':'/workspace','scan_roots':[str(args.owner/'scan')],'reference_stores':[],
        'protected':[str(HERE),str(args.checkout/'tools/host-maintenance'),str(Path(binding['toolchain']['physical_root']).parents[1]),
                     '/home/max/Development/emulationstation-next.worktrees/m7-md5-alignment'],
        'candidates':[], 'builds':[{'name':'m7-md5-target-314da58d',
        'terms_bytes':{'two_sanitized_libraries':1073741824,'compiler_scratch':536870912,'artifacts_logs':268435456,'public_source_snapshots':33554432},
        'basis':'Attempt03 full target-library compile PASS at435642368-byte cgroup peak and zeroOOM; reuse4GiB/2CPU cap and one compiler job. Conservative old disk allowance plus32MiB public source snapshots; no cache copy. Fresh runtime admission is separate.',
        'evidence':evidence}]}
    write(args.owner/'retention-plan.json',retention)
    outputs=[]
    for name,kind in (('builds','build-cache'),('tmp','qa-scratch'),('sources','qa-scratch'),('artifacts','qa-scratch')):
        outputs.append({'path':str(args.owner/name),'issue':574,'kind':kind,
            'release_when':'Consume original command/container/watcher/launcher results; preserve compact source/compile/failure receipts. Retire builds/tmp/snapshots after compile acceptance; artifacts only after the newly allocated target checks are consumed. No automatic deletion.'})
    admission={'checkout':str(args.checkout),'retention_plan':str(args.owner/'retention-plan.json'),
        'retention_report':str(args.owner/'retention-report.json'),'stage':'m7-md5-target-314da58d',
        'profiles':[{'PROJECT':'ROCKNIX','DEVICE':'GENERIC_X64','ARCH':'x86_64'}], 'outputs':outputs}
    write(args.owner/'admission-plan.json',admission)
    print('Prepared plans only; coordinator must produce and review a fresh capacity report/admission.')


if __name__=='__main__': main()

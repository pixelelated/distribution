#!/usr/bin/env python3
"""UNRUN. Fresh single-stage plan; no export, admission grant, container or compiler."""
import argparse
from pathlib import Path
import re
import sys
sys.path.insert(0,str(Path(__file__).resolve().parent))
from common import DISK_LIMIT, HERE, SEQUENCES, read, require, sha, verify_packet, write

from mame import predecessors


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--owner',type=Path,required=True)
    parser.add_argument('--stage',choices=sum(SEQUENCES.values(),[]),required=True)
    parser.add_argument('--checkout',type=Path,required=True)
    args=parser.parse_args();owner=args.owner;family=args.stage.split('-')[0];sequence=SEQUENCES[family]
    require(re.fullmatch('/workspace/tmp/[A-Za-z0-9_-]+',str(owner)) and owner.resolve()==owner,'real simple family owner required')
    require(args.checkout.is_absolute() and args.checkout.resolve()==args.checkout,'real absolute checkout required')
    verify_packet(HERE);binding=read(HERE/'bindings.json')
    sealed=args.checkout/binding['sealed_plan_path'];verify_packet(sealed)
    require(sha(sealed/'SHA256SUMS')==binding['sealed_plan_manifest_sha256'],'wrong prospective OSD-corrected plan')
    if args.stage==sequence[0]:
        owner.mkdir(mode=0o700);(owner/'work').mkdir();(owner/'work/format-tools').mkdir();(owner/'work/format-tools/tmp').mkdir();(owner/'stages').mkdir()
        write(owner/'family.json',{'family':family,'checkout':str(args.checkout),'runner_manifest_sha256':sha(HERE/'SHA256SUMS')})
    predecessors(owner,args.stage)
    expected_manifest=sha(HERE/'SHA256SUMS')
    info=read(owner/'family.json')
    require(info=={'family':family,'checkout':str(args.checkout),'runner_manifest_sha256':expected_manifest},'family/source differs')
    for previous in sequence[:sequence.index(args.stage)]:
        result=read(owner/'stages'/previous/'result.json')
        require(result['status']=='PASS' and result['stage']==previous and result['watchdog_original_exit']==0,'predecessor stage not completed')
    stage=owner/'stages'/args.stage;stage.mkdir()
    for name in ('scan','logs','submit'): (stage/name).mkdir()
    outputs=[{'path':str(owner/'work'),'issue':574,'kind':'build-cache','release_when':'Retire after selected converter VM qualification; preserve compact source/artifact/failure receipts.'},
             {'path':str(owner/'stages'),'issue':574,'kind':'qa-scratch','release_when':'Preserve original child/container/watcher/launcher channels and host identity/cleanup receipts before scratch retirement.'}]
    old=read(sealed/'input-bindings.json')
    retention={'volume':'/workspace','scan_roots':[str(stage/'scan')],'reference_stores':[],
      'protected':[str(HERE),str(sealed),str(Path(old['toolchain']['physical_root']).parents[1]),old['chdman']['archive']['path']],
      'candidates':[],'builds':[{'name':'m7-format-'+args.stage,'terms_bytes':{'selected_family_scratch_ceiling':DISK_LIMIT},
        'basis':'Sealed1c0e93: one job,4GiB/2CPU,6GiB scratch; no accepted cache copy. MAME897821359 source bytes; one1800s family clock including export/bootstrap/configure/build. Runtime sampled ceiling; existing bytes already reduce available space and remaining stages conservatively reserve6GiB again.',
        'evidence':[{'path':str(sealed/'input-bindings.json'),'sha256':sha(sealed/'input-bindings.json')},{'path':str(HERE/'bindings.json'),'sha256':sha(HERE/'bindings.json')}]}]}
    write(stage/'retention-plan.json',retention)
    write(stage/'admission-plan.json',{'checkout':str(args.checkout),'retention_plan':str(stage/'retention-plan.json'),
      'retention_report':str(stage/'retention-report.json'),'stage':'m7-format-'+args.stage,
      'profiles':[{'PROJECT':'ROCKNIX','DEVICE':'GENERIC_X64','ARCH':'x86_64'}],'outputs':outputs})
    write(stage/'selection.json',{'stage':args.stage,'owner':str(owner),'runner_manifest_sha256':sha(HERE/'SHA256SUMS'),
          'sealed_manifest_sha256':sha(sealed/'SHA256SUMS')})
    print(str(stage/'admission-plan.json'))


if __name__=='__main__':main()

#!/usr/bin/env python3
"""UNRUN: prepare one fresh 180s closure owner; no allocation/container/target."""
import argparse
from pathlib import Path
import re
import sys
sys.path.insert(0,str(Path(__file__).resolve().parent))
from common import DISK_LIMIT, HERE, read, require, sha, verify_packet, write
from prerequisites import snapshot


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--owner',type=Path,required=True)
    parser.add_argument('--checkout',type=Path,required=True)
    args=parser.parse_args();owner=args.owner;name='chdman-closure'
    require(re.fullmatch('/workspace/tmp/[A-Za-z0-9_-]+',str(owner)) and owner.resolve()==owner
            and not owner.exists(),'fresh real simple owner required; no resume/replay')
    require(args.checkout.is_absolute() and args.checkout.resolve()==args.checkout,'real checkout required')
    verify_packet(HERE);extra=read(HERE/'bindings.json');inputs=snapshot()
    sealed=Path(extra['sealed_plan_root']);binding=read(sealed/'input-bindings.json')
    owner.mkdir(mode=0o700);(owner/'stages').mkdir();stage=owner/'stages'/name;stage.mkdir()
    for directory in ('scan','logs','submit'):(stage/directory).mkdir()
    write(owner/'family.json',{'family':'chdman','checkout':str(args.checkout),'runner_manifest_sha256':sha(HERE/'SHA256SUMS')})
    write(stage/'build-input.json',inputs)
    outputs=[{'path':str(owner/'stages'),'issue':574,'kind':'qa-scratch',
              'release_when':'Preserve original closure/loader bundle, readelf/version receipts, child/container/watcher/launcher and exact cleanup evidence; stage needed ELF bundle for immediately queued VM proof, then retire temporary owner output.'}]
    retention={'volume':'/workspace','scan_roots':[str(stage/'scan')],'reference_stores':[],
      'protected':[str(HERE),str(sealed),extra['closure_packet_root'],extra['build_owner'],
                   str(Path(binding['toolchain']['physical_root']).parents[1]),binding['chdman']['archive']['path']],
      'candidates':[],'builds':[{'name':'m7-format-chdman-closure','terms_bytes':{'closure_scratch_ceiling':DISK_LIMIT},
        'basis':'Fresh180s4GiB/2CPU closure only. Read-only archive/SDK/completed work/build receipts/packets. 1GiB sampled new scratch ceiling; 512MiB closure bound. No export, rebuild, host target execution or original family clock reuse.',
        'evidence':[{'path':str(HERE/'bindings.json'),'sha256':sha(HERE/'bindings.json')},
                    {'path':str(stage/'build-input.json'),'sha256':sha(stage/'build-input.json')}]}]}
    write(stage/'retention-plan.json',retention)
    write(stage/'admission-plan.json',{'checkout':str(args.checkout),'retention_plan':str(stage/'retention-plan.json'),
      'retention_report':str(stage/'retention-report.json'),'stage':'m7-format-chdman-closure',
      'profiles':[{'PROJECT':'ROCKNIX','DEVICE':'GENERIC_X64','ARCH':'x86_64'}],'outputs':outputs})
    write(stage/'selection.json',{'stage':name,'owner':str(owner),'runner_manifest_sha256':sha(HERE/'SHA256SUMS'),
          'sealed_manifest_sha256':sha(sealed/'SHA256SUMS')})
    print(str(stage/'admission-plan.json'))


if __name__=='__main__':main()

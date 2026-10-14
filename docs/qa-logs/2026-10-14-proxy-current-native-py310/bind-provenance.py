#!/usr/bin/env python3
"""UNRUN: export only a consumed successful native build for fresh VM staging."""
import argparse
import json
from pathlib import Path
import re
import sys
sys.path.insert(0,str(Path(__file__).resolve().parent))
from common import HERE, read, require, sha, verify_packet, write
from native import output_path, predecessors, inspect_source

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--owner',type=Path,required=True)
    args=parser.parse_args();owner=args.owner
    require(re.fullmatch('/workspace/tmp/[A-Za-z0-9_-]+',str(owner)) and owner.resolve()==owner,'real exact owner required')
    verify_packet(HERE);binding=read(HERE/'plan/input-bindings.json')
    require(read(owner/'family.json')['runner_manifest_sha256']==sha(HERE/'SHA256SUMS'),'different runner family')
    predecessors(owner,'proxy-build')
    stage=owner/'stages/proxy-build';result=read(stage/'result.json')
    require(result['status']=='PASS' and all(result[k]==0 for k in ('original_attach_exit','original_container_exit','watchdog_original_exit'))
            and result['cleanup']['status']=='PASS' and not result['cleanup']['forced_stop'],'original final stage not successful')
    watch=read(stage/'watch-run.json');run=Path(watch['run']);consumed=read(run/'admission-consumed.json')
    require(consumed['state']=='consumed' and consumed['run']==str(run) and
            all(consumed['original_result'][k]==0 for k in ('runner_rc','command_rc','monitor_rc')),'final original channels not consumed')
    require(sha(run/'admission.json')==watch['admission_sha256'],'final admission changed')
    inside=read(stage/'container-result.json');require(inside['status']=='PASS' and not inside['monitor_errors'] and inside['sampler_exited'],'container monitor failed')
    require(all(x['original_exit']==0 and x['reaped'] and not x.get('forced_group_stop') for x in inside['children']),'original child result failed')
    native=read(stage/'native-build.json')
    require(native['input_bindings_sha256']==sha(HERE/'plan/input-bindings.json'),'native inputs differ')
    source=inspect_source(owner/'work/proxy-native','proxy',binding)
    binary=output_path(owner/'work/proxy-native',binding);artifact=read(stage/'target-artifact.json')
    require(sha(binary)==artifact['sha256'] and binary.stat().st_size==artifact['bytes'],'built ELF changed')
    output=owner/'qualification-inputs';output.mkdir()
    with (output/'libraproxy_rchash.so').open('xb') as stream:stream.write(binary.read_bytes())
    (output/'libraproxy_rchash.so').chmod(0o644)
    records={}
    for name in ['result.json','container-result.json','native-build.json','target-artifact.json','compiler-inputs.json','selected-stage.json','logs/selected-stage.stderr','logs/elf-header.stdout','logs/elf-dynamic.stdout','logs/elf-symbols.stdout','logs/elf-versions.stdout','host-cgroup.json','watchdog-result.json']:
        p=stage/name;records[name]={'original_path':str(p),'bytes':p.stat().st_size,'sha256':sha(p)}
    receipt={'schema':1,'status':'CURRENT_SOURCE_BUILD_BOUND_VM_UNRUN','pins':native['pins'],
             'source':source,'native_patches':[],'recipe_sha256':native['recipe_sha256'],
             'input_bindings_sha256':native['input_bindings_sha256'],
             'runner_manifest_sha256':sha(HERE/'SHA256SUMS'),'elf':artifact,
             'original_records':records,'admission_consumed':{'path':str(run/'admission-consumed.json'),'sha256':sha(run/'admission-consumed.json')},
             'scope':'Current native source linkage only. No VM loader, target hashing, service, default-boot, Dolphin gameplay or final-image acceptance inferred.'}
    write(output/'native-build-receipt.json',receipt)
    proof=output/'native-build-receipt.json'
    require(proof.stat().st_size<1024**2,'oversized build receipt')
    write(output/'native-provenance.json',{
        'image_sha256':'1a23cf5740dbb69cdca76d753a0f6121c35e6e12f27649e792aeebc71e8cc490',
        'source_pins_verified':True,
        'qualification':'Fresh source-bound candidate ELF; disposable VM20 file-bind overlay must match elf.sha256. The accepted image itself is unchanged. Runtime qualification remains independent and UNRUN.',
        'elf':{'sha256':artifact['sha256'],'bytes':artifact['bytes']},
        'build_receipt':{'path':'native-build-receipt.json','bytes':proof.stat().st_size,'sha256':sha(proof)}})
    print(json.dumps({'status':'PREPARED_ONLY','output':str(output),'elf_sha256':artifact['sha256']}))
if __name__=='__main__':main()

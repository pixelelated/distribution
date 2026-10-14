#!/usr/bin/env python3
"""UNRUN proxy source identity and existing original-result consumption contract."""
import os
from pathlib import Path
import stat
from common import HERE, SEQUENCES, read, require, safe_member, sha, write

def predecessors(owner,stage):
    for name in SEQUENCES['proxy'][:SEQUENCES['proxy'].index(stage)]:
        previous=owner/'stages'/name;result=read(previous/'result.json')
        require(result['stage']==name and result['status']=='PASS' and result['original_attach_exit']==0
                and result['original_container_exit']==0 and result['watchdog_original_exit']==0
                and result['cleanup']['status']=='PASS' and not result['cleanup']['forced_stop'],
                'predecessor original/cleanup did not pass: '+name)
        require(read(previous/'selection.json')['runner_manifest_sha256']==sha(HERE/'SHA256SUMS'),
                'predecessor used different runner source')
        watched=read(previous/'watch-run.json');run=Path(watched['run'])
        require(sha(run/'admission.json')==watched['admission_sha256'],'predecessor admission changed')
        consumed=read(run/'admission-consumed.json')
        require(consumed['state']=='consumed' and consumed['run']==str(run)
                and all(consumed['original_result'][k]==0 for k in ('runner_rc','command_rc','monitor_rc')),
                'predecessor original result must be consumed before next stage')


def files_in(root):
    result={}
    def error(exc):raise exc
    for directory,dirs,files in os.walk(root,followlinks=False,onerror=error):
        for name in dirs:
            require(not (Path(directory)/name).is_symlink(),'source directory alias')
        for name in files:
            path=Path(directory)/name;info=path.lstat()
            require(stat.S_ISREG(info.st_mode) and path.resolve()==path,'nonregular/aliased file')
            relative=str(path.relative_to(root));safe_member(relative)
            result[relative]={'sha256':sha(path),'bytes':info.st_size,'mode':stat.S_IMODE(info.st_mode)}
    return result



def output_path(work,binding):
    return work/'sources'/binding['archives']['raofflineproxy']['archive_root']/'.x86_64-rocknix-linux-gnu/libraproxy_rchash.so'


def inspect_source(work,family,binding):
    require(family=='proxy','wrong source family')
    require(sha(work/'source-inventory.json')==binding['source_inventory_sha256'],'source inventory changed')
    expected=read(work/'source-inventory.json');actual=files_in(work/'sources')
    output=str(output_path(work,binding).relative_to(work/'sources'))
    extras=set(actual)-set(expected)
    require(extras <= {output},'unexpected generated source paths')
    require(all(actual.get(n)==v for n,v in expected.items()),'original source bytes or modes changed')
    return {'files':len(expected),'inventory_sha256':sha(work/'source-inventory.json'),
            'native_patches':[],'all_original_sources_unchanged':True}

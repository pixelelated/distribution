#!/usr/bin/env python3
"""Read-only binding to the successful, consumed CHD build; no recovery bypass."""
from pathlib import Path
import os
import re
from common import HERE, read, require, same_process, sha, verify_packet


def snapshot():
    extra=read(HERE/'bindings.json');build=Path(extra['build_owner'])
    checkout=Path(extra['build_checkout']);runner=checkout/extra['build_runner_path']
    sealed=Path(extra['sealed_plan_root']);closure=Path(extra['closure_packet_root'])
    for root,key in [(runner,'build_runner_manifest_sha256'),(sealed,'sealed_plan_manifest_sha256'),
                     (closure,'closure_manifest_sha256')]:
        require(root.is_absolute() and root.resolve()==root,'real immutable packet root required')
        verify_packet(root);require(sha(root/'SHA256SUMS')==extra[key],'bound source packet changed: '+str(root))
    require(build.resolve()==build and read(build/'family.json')=={'family':'chdman','checkout':str(checkout),
            'runner_manifest_sha256':extra['build_runner_manifest_sha256']},'wrong completed build family')
    stage=build/'stages/chdman-build';result=read(stage/'result.json')
    require(result['stage']=='chdman-build' and result['status']=='PASS'
            and all(result[k]==0 for k in ('original_attach_exit','original_container_exit','watchdog_original_exit'))
            and not result.get('forced_client_stop') and not result.get('watchdog_timeout'),'original build did not pass')
    cleanup=result['cleanup'];terminal=cleanup['container_terminal_state']
    require(cleanup['status']=='PASS' and not cleanup['forced_stop'] and cleanup['exact_id_absent']
            and not cleanup['survivors'] and not cleanup.get('remaining_cgroup_pids')
            and terminal['ExitCode']==0 and not any(terminal[k] for k in ('Running','OOMKilled','Dead')),
            'original build container/cleanup did not pass')
    require(re.fullmatch('[0-9a-f]{64}',cleanup['exact_cid']),'original exact CID absent')
    require(read(stage/'selection.json')['runner_manifest_sha256']==extra['build_runner_manifest_sha256']
            and read(stage/'cleanup-complete.json')['status']=='PASS'
            and read(stage/'watchdog-result.json')['status']=='PASS','build source/cleanup/watchdog differs')
    require(sha(stage/'container-result.json')==result['container_result_sha256'],'original container result changed')
    inside=read(stage/'container-result.json');child=read(stage/'selected-stage.json')
    require(inside['status']=='PASS' and inside['stage']=='chdman-build' and inside['children']==[child]
            and inside['source_before']==inside['source_after'] and inside['sampler_exited']
            and not inside['monitor_errors'] and child['original_exit']==0 and child['reaped']
            and not child.get('forced_group_stop'),'original build child/source/resource contract differs')
    watched=read(stage/'watch-run.json');run=Path(watched['run'])
    require(run.parent==checkout/'.build-runs' and run.resolve()==run,'unexpected original watched-run path')
    require(sha(run/'admission.json')==watched['admission_sha256'],'original admission changed')
    admission=read(run/'admission.json');consumed=read(run/'admission-consumed.json')
    require(consumed['state']=='consumed' and consumed['run']==str(run) and consumed['id']==admission['id']
            and consumed['checkout']==str(checkout)
            and all(consumed['original_result'][k]==0 for k in ('runner_rc','command_rc','monitor_rc')),
            'successful original admission must be consumed before closure')
    require(os.stat('/proc/self/ns/pid').st_ino==admission['pid_namespace'],'actual admitted host PID view required')
    require(all(not same_process(item) for item in cleanup['observed_host_processes']),
            'recorded original container process survives')
    group=Path(read(stage/'host-cgroup.json')['path'])
    require(group.is_relative_to('/sys/fs/cgroup') and group.name in
            (cleanup['exact_cid'],'docker-'+cleanup['exact_cid']+'.scope'),'unexpected original cgroup path')
    require(not (group/'cgroup.procs').exists() or not (group/'cgroup.procs').read_text().split(),
            'original cgroup still populated')
    binding=read(sealed/'input-bindings.json');work=build/'work/format-tools'
    artifact=read(stage/'target-artifact.json')
    relative=Path(binding['chdman']['archive_root'])/'chdman';target=work/relative
    require(artifact['path']==str(Path('/work/format-tools')/relative)
            and target.resolve()==target and target.is_file()
            and 0<target.stat().st_size==artifact['bytes']<=256*1024**2 and sha(target)==artifact['sha256'],
            'actual completed target differs from original receipt')
    require(sha(work/'source-inventory.json')==inside['source_after']['inventory_sha256'],'source inventory changed')
    generated=read(stage/'generated-after.json')
    require(generated==inside['generated_after'] and generated['chdman']['sha256']==artifact['sha256']
            and generated['chdman']['bytes']==artifact['bytes'],'post-build target inventory differs')
    files=[build/'family.json',stage/'result.json',stage/'container-result.json',stage/'selected-stage.json',
           stage/'target-artifact.json',stage/'generated-after.json',stage/'selection.json',
           stage/'cleanup-complete.json',stage/'watchdog-result.json',stage/'watch-run.json',
           stage/'host-cgroup.json',run/'admission.json',run/'admission-consumed.json',
           work/'source-inventory.json',work/'pristine-source-inventory.json',work/'configured-generated.json']
    return {'build_owner':str(build),'build_stage':str(stage),'work':str(build/'work'),
            'artifact':artifact,'host_target':str(target),'original_admission':str(run),
            'file_sha256':{str(path):sha(path) for path in files},
            'build_runner_manifest_sha256':sha(runner/'SHA256SUMS'),
            'sealed_manifest_sha256':sha(sealed/'SHA256SUMS'),'closure_manifest_sha256':sha(closure/'SHA256SUMS')}

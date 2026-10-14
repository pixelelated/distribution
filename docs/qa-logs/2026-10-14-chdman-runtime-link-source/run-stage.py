#!/usr/bin/env python3
"""UNRUN coordinator entry. Exactly one selected stage per fresh admission/submission."""
import argparse
import fcntl
import json
import os
from pathlib import Path
import re
import signal
import subprocess
import sys
import time
sys.path.insert(0,str(Path(__file__).resolve().parent))
from common import DISK_LIMIT, HERE, LIMITS, SEQUENCES, command, host_cgroup, identity, read, require, same_process, sha, verify_packet, write
from docker_owner import DOCKER, DockerOwner

from mame import predecessors


def replace_state(path,value):
    temp=path.with_suffix('.new')
    with temp.open('x') as stream:json.dump(value,stream)
    os.replace(temp,path)


def disk_usage(root):
    allocated=0;apparent=0
    for directory,dirs,files in os.walk(root,followlinks=False):
        for name in files:
            try:stat=(Path(directory)/name).lstat()
            except FileNotFoundError:continue
            allocated+=stat.st_blocks*512;apparent+=stat.st_size
    return {'allocated_bytes':allocated,'apparent_bytes':apparent}


def verify_inputs(binding):
    def visit(value):
        if isinstance(value,dict):
            if 'path' in value and 'sha256' in value:
                require(sha(value['path'])==value['sha256'],'retained input changed: '+value['path'])
            if 'path' in value and 'target' in value:
                require(os.readlink(value['path'])==value['target'],'retained symlink changed')
            for child in value.values():visit(child)
        elif isinstance(value,list):
            for child in value:visit(child)
    visit(binding['toolchain'])


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--owner',type=Path,required=True)
    parser.add_argument('--stage',choices=sum(SEQUENCES.values(),[]),required=True)
    parser.add_argument('--checkout',type=Path,required=True)
    args=parser.parse_args();owner=args.owner;stage=owner/'stages'/args.stage
    family=args.stage.split('-')[0];sequence=SEQUENCES[family]
    require(re.fullmatch('/workspace/tmp/[A-Za-z0-9_-]+',str(owner)) and owner.resolve()==owner,'real owner required')
    require(os.getuid()!=0 and args.checkout.resolve()==args.checkout,'normal build user and real checkout required')
    verify_packet(HERE);extra=read(HERE/'bindings.json');sealed=args.checkout/extra['sealed_plan_path'];verify_packet(sealed)
    require(sha(sealed/'SHA256SUMS')==extra['sealed_plan_manifest_sha256'],'sealed plan changed')
    predecessors(owner,args.stage)
    expected_manifest=sha(HERE/'SHA256SUMS')
    require(read(owner/'family.json')=={'family':family,'checkout':str(args.checkout),'runner_manifest_sha256':expected_manifest},'family identity changed')
    require(read(stage/'selection.json')=={'stage':args.stage,'owner':str(owner),'runner_manifest_sha256':sha(HERE/'SHA256SUMS'),'sealed_manifest_sha256':sha(sealed/'SHA256SUMS')},'wrong selection')
    run=Path(os.environ.get('RASTERATOPS_BUILD_RUN',''))
    require(str(run) not in ('','.') and not run.is_absolute() and '..' not in run.parts,'must use admitted watch-build')
    admission=read(args.checkout/run/'admission.json')
    expected_admission=read(stage/'admission-plan.json')
    require(admission['state']=='running' and all(admission[k]==expected_admission[k] for k in
            ('checkout','outputs','profiles')),'wrong active admission')
    require(read(args.checkout/run/'admission-plan.json')==expected_admission,'wrong admitted stage plan')
    require(admission['pid_namespace']==os.stat('/proc/self/ns/pid').st_ino,'not the admitted host PID namespace')
    lock=(owner/'family.lock').open('a');fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
    for previous in sequence[:sequence.index(args.stage)]:
        require(read(owner/'stages'/previous/'result.json')['status']=='PASS','predecessor did not complete')
    with (stage/'started').open('x') as stream:stream.write(str(time.time()))
    write(stage/'watch-run.json',{'run':str(args.checkout/run),'admission_sha256':sha(args.checkout/run/'admission.json')})
    binding=read(sealed/'input-bindings.json');clock=owner/'clock.json'
    if not clock.exists():
        require(args.stage==sequence[0],'family clock missing')
        write(clock,{'boot_id':identity(os.getpid())['boot_id'],'deadline_monotonic':time.monotonic()+LIMITS[family],
                     'started_utc_epoch':time.time(),'wall_seconds':LIMITS[family]})
    timing=read(clock);require(timing['boot_id']==identity(os.getpid())['boot_id'],'host reboot; old allocation cannot resume')
    deadline=timing['deadline_monotonic'];require(time.monotonic()<deadline,'family deadline expired; no extension')
    nonce=os.urandom(16).hex()
    write(stage/'container-owner.json',{'stage':args.stage,'nonce':nonce,'name':'pix574-format-'+nonce,
          'host_runner':identity(os.getpid()),'host_pid_namespace':os.stat('/proc/self/ns/pid').st_ino,
          'deadline_monotonic':deadline,'runner_manifest_sha256':sha(HERE/'SHA256SUMS')})
    result={'status':'FAIL','stage':args.stage,'started':time.time(),'original_attach_exit':None}
    guard=None;client=None;docker=None;observed={};cg=None;monitor_error=None
    def interrupted(sig,frame):raise KeyboardInterrupt('host signal '+str(sig))
    signal.signal(signal.SIGTERM,interrupted);signal.signal(signal.SIGINT,interrupted)
    try:
        verify_inputs(binding)
        if args.stage=='chdman-export':
            archive=binding['chdman']['archive']
            require(Path(archive['path']).stat().st_size==archive['bytes'] and sha(archive['path'])==archive['sha256'],'source archive changed')
        require(time.monotonic()<deadline,'family deadline exhausted during input checks')
        if args.stage!='chdman-export':
            exported=read(owner/'stages/chdman-export/container-result.json')['source_after']
            require(sha(owner/'work/format-tools/source-inventory.json')==exported['inventory_sha256'],'export inventory changed')
            write(stage/'expected-source.json',exported)
            previous=sequence[sequence.index(args.stage)-1]
            write(stage/'expected-generated.json',read(owner/'stages'/previous/'generated-after.json'))
            if args.stage=='chdman-build':
                require(sha(owner/'work/format-tools/configured-generated.json')==read(owner/'stages/chdman-configure/configured-generated-binding.json')['sha256'],'configured generated inventory changed')
        for path in (stage/'watchdog.stdout',stage/'watchdog.stderr'):require(not path.exists(),'watchdog output exists')
        with (stage/'watchdog.stdout').open('xb') as out,(stage/'watchdog.stderr').open('xb') as err:
            guard=subprocess.Popen([sys.executable,'-I','-S','-B',str(HERE/'watchdog.py'),str(stage)],stdout=out,stderr=err,start_new_session=True)
        write(stage/'watchdog-client.json',{'pid':guard.pid,'identity':identity(guard.pid)})
        until=time.monotonic()+5
        while not (stage/'watchdog-ready.json').exists():
            require(guard.poll() is None and time.monotonic()<until,'watchdog did not arm');time.sleep(.1)
        require(same_process(read(stage/'watchdog-ready.json')['identity']),'watchdog identity unavailable')
        docker=DockerOwner(stage,stage/'host-docker')
        physical=Path(binding['toolchain']['physical_root']).parents[1]
        inside=Path(binding['toolchain']['required_container_root']).parents[1]
        meta=read(stage/'container-owner.json')
        argv=['create','--pull=never','--name',meta['name'],'--cidfile',str(stage/'container.cid'),
              '--label','pix574.owner='+nonce,'--label','pix574.stage='+args.stage,
              '--network','none','--read-only','--memory','4g','--memory-swap','4g','--cpus','2','--pids-limit','256',
              '--cap-drop','ALL','--security-opt','no-new-privileges','--user',str(os.getuid())+':'+str(os.getgid()),
              '--tmpfs','/tmp:rw,nosuid,nodev,size=64m',
              '-v',str(physical)+':'+str(inside)+':ro','-v',str(sealed)+':/plan:ro',
              '-v',str(HERE)+':/runner:ro','-v',str(owner/'work')+':/work:rw','-v',str(stage)+':/receipts:rw']
        if args.stage=='chdman-export':argv+=['-v',binding['chdman']['archive']['path']+':/mame-source.tar.gz:ro']
        remaining=deadline-time.monotonic();require(remaining>0,'family deadline exhausted before container creation')
        argv += [binding['toolchain']['builder_image'],'python3','-I','-S','-B','/runner/inner.py',args.stage,str(remaining)]
        write(stage/'docker-create-command.json',DOCKER+argv)
        code,out,err=docker.call('create',*argv,seconds=30)
        require(code==0,'container create failed')
        cid=(stage/'container.cid').read_text().strip();require(re.fullmatch('[0-9a-f]{64}',cid),'invalid CID')
        require(out.decode().strip()==cid,'create/cidfile mismatch')
        with (stage/'logs/container.stdout').open('xb') as out,(stage/'logs/container.stderr').open('xb') as err:
            client=subprocess.Popen(DOCKER+['start','--attach',cid],stdout=out,stderr=err,start_new_session=True)
        write(stage/'docker-client.json',{'pid':client.pid,'identity':identity(client.pid)})
        until=min(deadline,time.monotonic()+30)
        while not (stage/'inner-ready.json').exists():
            require(client.poll() is None and guard.poll() is None and time.monotonic()<until,'container readiness failed');time.sleep(.1)
        state=docker.inspect(cid);require(state and state['state']['Running'],'ready container is not running')
        pid=state['state']['Pid'];ident=identity(pid);require(ident is not None,'host init PID unreadable')
        ready=read(stage/'inner-ready.json')
        require(os.stat('/proc/'+str(pid)+'/ns/pid').st_ino==ready['pid_namespace'],'host/container PID namespace identity mismatch')
        status=Path('/proc/'+str(pid)+'/status').read_text();nspid=re.search(r'^NSpid:\s+(.+)$',status,re.M)
        require(nspid and list(map(int,nspid.group(1).split()))==[pid,ready['pid']],'not the actual host PID view')
        cg=host_cgroup(pid,cid);write(stage/'host-cgroup.json',{'path':str(cg),'init':ident})
        observed[(ident['pid'],ident['start_ticks'])]=ident
        replace_state(stage/'observed-host-processes.json',list(observed.values()))
        write(stage/'host-admitted.json',{'stage':args.stage,'host_init':ident,'pid_namespace':ready['pid_namespace']})
        last_disk=0
        with (stage/'host-resources.jsonl').open('x') as stream:
            while True:
                now=time.monotonic();require(now<deadline,'family deadline exceeded')
                require(guard.poll() is None,'independent watchdog failed/intervened')
                members=cg/'cgroup.procs'
                if members.exists():
                    for value in members.read_text().split():
                        item=identity(int(value))
                        if item is not None:observed[(item['pid'],item['start_ticks'])]=item
                replace_state(stage/'observed-host-processes.json',list(observed.values()))
                stat=os.statvfs(owner)
                row={'monotonic':now,'remaining_seconds':deadline-now,'available_bytes':stat.f_bavail*stat.f_frsize,
                     'meminfo':Path('/proc/meminfo').read_text(),'cpu_stat':Path('/proc/stat').read_text(),
                     'memory_pressure':Path('/proc/pressure/memory').read_text(),'cpu_pressure':Path('/proc/pressure/cpu').read_text(),
                     'observed_container_processes':len(observed)}
                require(row['available_bytes']>=512*1024**2,'host free-space floor crossed')
                if now-last_disk>=5:
                    row['scratch']=disk_usage(owner);last_disk=now
                    require(max(row['scratch'].values())<=DISK_LIMIT,'6GiB scratch forecast exceeded')
                stream.write(json.dumps(row)+'\n');stream.flush()
                if client.poll() is not None:break
                time.sleep(1)
        result['original_attach_exit']=client.wait(timeout=5)
        result['container_result_sha256']=sha(stage/'container-result.json')
        inside_result=read(stage/'container-result.json')
        require(result['original_attach_exit']==0 and inside_result['status']=='PASS','original child/container failure')
        verify_inputs(binding)
        result['status']='PASS'
    except BaseException as exc:result['error']=repr(exc)
    finally:
        # Block a second user interrupt while the exact owned container is retired.
        signal.signal(signal.SIGTERM,signal.SIG_IGN);signal.signal(signal.SIGINT,signal.SIG_IGN)
        try:
            if docker is None:docker=DockerOwner(stage,stage/'host-docker')
            cleanup=docker.cleanup();result['cleanup']=cleanup
            if cleanup['status']!='PASS' or cleanup['forced_stop']:result['status']='FAIL'
            terminal=cleanup.get('container_terminal_state')
            if terminal:
                result['original_container_exit']=terminal['ExitCode']
                if terminal['ExitCode']!=0 or terminal['OOMKilled'] or terminal['Dead']:result['status']='FAIL'
            elif result['status']=='PASS':result['status']='FAIL';result['missing_terminal_container_state']=True
            if cleanup['status']=='PASS':write(stage/'cleanup-complete.json',{'status':'PASS'})
        except BaseException as exc:result['cleanup_error']=repr(exc);result['status']='FAIL'
        if client is not None:
            if client.poll() is None:
                client.terminate()
                try:client.wait(timeout=5)
                except subprocess.TimeoutExpired:client.kill();client.wait(timeout=5)
                result['forced_client_stop']=True;result['status']='FAIL'
            result['original_attach_exit']=client.returncode
        if guard is not None:
            if not (stage/'cleanup-complete.json').exists():
                write(stage/'cleanup-request.json',{'reason':'parent cleanup incomplete'})
            try:result['watchdog_original_exit']=guard.wait(timeout=300)
            except subprocess.TimeoutExpired:
                guard.terminate()
                try:guard.wait(timeout=30)
                except subprocess.TimeoutExpired:guard.kill();guard.wait(timeout=5)
                result['watchdog_original_exit']=guard.returncode;result['watchdog_timeout']=True
            if result['watchdog_original_exit']!=0:result['status']='FAIL'
        else:result['watchdog_original_exit']=None
        result['ended']=time.time();result['final_disk']=disk_usage(owner)
        if max(result['final_disk'].values())>DISK_LIMIT:result['status']='FAIL'
        write(stage/'result.json',result);lock.close()
    print(json.dumps({'status':result['status'],'stage':args.stage,'result':str(stage/'result.json')}))
    return 0 if result['status']=='PASS' else 1


if __name__=='__main__':raise SystemExit(main())

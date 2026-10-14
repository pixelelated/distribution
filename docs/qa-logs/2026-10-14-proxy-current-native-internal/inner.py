#!/usr/bin/env python3
"""UNRUN. One selected export/configure stage in its private offline container."""
import json
import os
from pathlib import Path
import resource
import signal
import subprocess
import sys
import threading
import time
sys.path.insert(0,str(Path(__file__).resolve().parent))
from native import output_path
from common import DISK_LIMIT, SEQUENCES, identity, read, require, sha, verify_packet, verify_source, write

WORK=Path('/work/proxy-native'); RECORDS=Path('/receipts'); PLAN=Path('/plan')


def disk_usage(roots):
    allocated=0; apparent=0
    for root in roots:
        for directory,dirs,files in os.walk(root,followlinks=False):
            for name in ['.']+files:
                path=Path(directory)/name
                try:stat=path.lstat()
                except FileNotFoundError:continue # compiler rename, next sample/final rescan catches remaining bytes
                allocated+=stat.st_blocks*512;apparent+=stat.st_size
    return {'allocated_bytes':allocated,'apparent_bytes':apparent}


def telemetry():
    root=Path('/sys/fs/cgroup')
    data={name:(root/name).read_text().strip() for name in
          ('memory.current','memory.peak','memory.max','memory.events','memory.swap.max','cpu.stat','cpu.max','pids.current','pids.max')}
    require(int(data['memory.max'])==4*1024**3 and data['memory.swap.max']=='0','wrong container memory/swap cap')
    quota,period=map(int,data['cpu.max'].split());require(quota==2*period,'wrong CPU quota')
    require(data['pids.max']=='256','wrong pids limit')
    events=dict(line.split() for line in data['memory.events'].splitlines())
    require({'oom','oom_kill'}<=events.keys() and all(int(v)==0 for k,v in events.items() if k.startswith('oom')),'OOM observed')
    return data


def main():
    require(len(sys.argv)==3,'stage and remaining deadline required')
    stage=sys.argv[1];family=stage.split('-')[0];remaining=float(sys.argv[2])
    require(family in SEQUENCES and stage in SEQUENCES[family] and 0<remaining<=600,'invalid stage/budget')
    deadline=time.monotonic()+remaining
    resource.setrlimit(resource.RLIMIT_CORE,(0,0))
    result={'status':'FAIL','stage':stage,'started':time.time(),'children':[]}
    stop=threading.Event();fault=[];thread=None
    def interrupt(_sig,_frame):raise KeyboardInterrupt('stage interrupted')
    signal.signal(signal.SIGTERM,interrupt)
    def sample():
        try:
            last_disk=0
            with (RECORDS/'container-resources.jsonl').open('x') as stream:
                while not stop.is_set():
                    now=time.monotonic();row={'monotonic':now,'remaining_seconds':deadline-now,'cgroup':telemetry()}
                    if now-last_disk>=5:
                        row['disk']=disk_usage([Path('/work'),RECORDS,Path('/tmp')]);last_disk=now
                        require(max(row['disk'].values())<=DISK_LIMIT,'1GiB scratch ceiling exceeded')
                    stream.write(json.dumps(row)+'\n');stream.flush()
                    require(now<deadline,'family deadline exhausted')
                    stop.wait(1)
        except BaseException as exc:fault.append(repr(exc))
    def child(label,argv,env):
        p=None;receipt={'argv':list(map(str,argv)),'started':time.time(),'label':label}
        try:
            with (RECORDS/'logs'/(label+'.stdout')).open('xb') as out,(RECORDS/'logs'/(label+'.stderr')).open('xb') as err:
                p=subprocess.Popen(receipt['argv'],env=env,stdout=out,stderr=err,start_new_session=True)
                receipt['identity']=identity(p.pid);receipt['pid']=p.pid
                while p.poll() is None:
                    require(not fault,'resource monitor failed: '+repr(fault))
                    require(time.monotonic()<deadline,'family deadline exhausted')
                    time.sleep(.2)
                receipt['original_exit']=p.returncode
                require(p.returncode==0,'original child failed: '+label)
        finally:
            if p is not None:
                if p.poll() is None:
                    receipt['forced_group_stop']=True;os.killpg(p.pid,signal.SIGTERM)
                    try:p.wait(timeout=5)
                    except subprocess.TimeoutExpired:os.killpg(p.pid,signal.SIGKILL);p.wait(timeout=5)
                receipt['original_exit']=p.returncode;receipt['reaped']=True
            receipt['ended']=time.time();write(RECORDS/(label+'.json'),receipt);result['children'].append(receipt)
    try:
        verify_packet(PLAN);verify_packet(Path('/runner'))
        binding=read(PLAN/'input-bindings.json');tc=Path(binding['toolchain']['required_container_root'])
        require(WORK.is_dir() and (WORK/'tmp').is_dir(),'private work directory absent')
        write(RECORDS/'inner-ready.json',{'pid':os.getpid(),'identity':identity(os.getpid()),
              'pid_namespace':os.stat('/proc/self/ns/pid').st_ino,'stage':stage})
        until=min(deadline,time.monotonic()+30)
        while not (RECORDS/'host-admitted.json').exists():
            require(time.monotonic()<until,'host PID handshake timed out');time.sleep(.1)
        require(read(RECORDS/'host-admitted.json')['stage']==stage,'wrong host handshake')
        thread=threading.Thread(target=sample);thread.start()
        env={'PATH':'/usr/bin:/bin','LANG':'C','LC_ALL':'C','TMPDIR':str(WORK/'tmp'),
             'PIX583_WORK':str(WORK),'PIX583_TC':str(tc),'CCACHE_DISABLE':'1',
             'CCACHE_TEMPDIR':str(WORK/'tmp'),'MAKEFLAGS':'-j1'}
        compiler_inputs={}
        for name in ('gcc','gcc-15.2.0','as','ld.bfd','readelf'):
            path=tc/'bin'/('x86_64-rocknix-linux-gnu-'+name)
            compiler_inputs[name]={'path':str(path),'resolved':str(path.resolve()),'sha256':sha(path)}
        write(RECORDS/'compiler-inputs.json',compiler_inputs)
        if stage=='proxy-export':
            child('export',['python3','-I','-S','-B','/runner/export.py'],env)
        else:
            result['source_before']=verify_source(WORK,family,binding)
            require(result['source_before']==read(RECORDS/'expected-source.json'),'source export receipt changed')
            binary=output_path(WORK,binding)
            require(not binary.exists(),'target already exists; no replay')
            child('selected-stage',['bash','/plan/build-stage.sh'],env)
            require(binary.resolve()==binary and binary.is_file() and binary.stat().st_size<8*1024**2,'target absent/aliased/oversized')
            for label,args in [('elf-header',['-h']),('elf-dynamic',['-d']),('elf-symbols',['-Ws']),('elf-versions',['--version-info'])]:
                child(label,[str(tc/'bin/x86_64-rocknix-linux-gnu-readelf'),*args,str(binary)],env)
            import re
            header=(RECORDS/'logs/elf-header.stdout').read_text()
            dynamic=(RECORDS/'logs/elf-dynamic.stdout').read_text()
            symbols=(RECORDS/'logs/elf-symbols.stdout').read_text()
            require('ELF64' in header and 'DYN (Shared object file)' in header and 'Advanced Micro Devices X86-64' in header,'unexpected ELF target')
            needed=re.findall(r'\(NEEDED\).*?\[([^]]+)\]',dynamic)
            require(needed==['libc.so.6'] and '(RPATH)' not in dynamic and '(RUNPATH)' not in dynamic,'unexpected dynamic closure; stop and review')
            for symbol in ('raproxy_hash_file','raproxy_hash_disc_datasource','raproxy_7z_list_entries','raproxy_hash_7z_entry'):
                require(any(line.rstrip().endswith(' '+symbol) and ' UND ' not in line for line in symbols.splitlines()),'missing native export: '+symbol)
            artifact={'path':str(binary),'bytes':binary.stat().st_size,'sha256':sha(binary),
                      'needed':needed,'execution':'NOT EXECUTED; VM loader/native qualification required'}
            write(RECORDS/'target-artifact.json',artifact)
            write(RECORDS/'native-build.json',{'schema':1,'status':'BUILT_UNQUALIFIED',
                  'input_bindings_sha256':sha(PLAN/'input-bindings.json'),
                  'source_inventory_sha256':sha(WORK/'source-inventory.json'),
                  'recipe_sha256':binding['recipes']['raofflineproxy']['sha256'],
                  'native_patches':[], 'pins':{k:v['pin'] for k,v in binding['archives'].items()},
                  'compiler_inputs_sha256':sha(RECORDS/'compiler-inputs.json'),
                  'original_build_receipt_sha256':sha(RECORDS/'selected-stage.json'),
                  'artifact':artifact,'source_pins_verified':False,
                  'qualification':'Coordinator must consume original outer/container/child/monitor exits, then bind this exact ELF in a fresh VM before provenance acceptance.'})
        result['source_after']=verify_source(WORK,family,binding)
        if stage!='proxy-export':require(result['source_after']==result['source_before'],'source changed during build')
        require(not fault,'resource monitor failed')
        result['final_cgroup']=telemetry();result['final_disk']=disk_usage([Path('/work'),RECORDS,Path('/tmp')])
        require(max(result['final_disk'].values())<=DISK_LIMIT and time.monotonic()<deadline,'final resource bound exceeded')
        result['status']='PASS'
    except BaseException as exc:result['error']=repr(exc)
    finally:
        if 'source_after' not in result and (WORK/'source-inventory.json').exists():
            try:
                result['source_after']=verify_source(WORK,family,binding)
            except BaseException as exc:result['source_after_error']=repr(exc)
        stop.set()
        if thread:thread.join(timeout=10)
        result['sampler_exited']=not thread or not thread.is_alive()
        result['monitor_errors']=fault
        if fault or not result['sampler_exited']:result['status']='FAIL'
        result['ended']=time.time();result['max_child_rss_kib']=resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss
        write(RECORDS/'container-result.json',result)
    return 0 if result['status']=='PASS' else 1


if __name__=='__main__':raise SystemExit(main())

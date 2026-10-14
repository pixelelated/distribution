#!/usr/bin/env python3
"""UNRUN. Offline disposable guest only; synthetic bytes and finite sanitizer probes."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import resource
import signal
import socket
import subprocess
import time

HERE = Path(__file__).resolve().parent


def require(ok, message):
    if not ok: raise RuntimeError(message)


def sha(path):
    with path.open('rb') as stream: return hashlib.file_digest(stream, 'sha256').hexdigest()


def write(path, value):
    path.write_text(json.dumps(value, indent=2) + '\n')


def call(owner, label, argv, env, seconds):
    prefix = owner / label
    code = None
    timed_out = False
    started = time.monotonic()
    argv = [str(a) for a in argv]
    with prefix.with_suffix('.stdout').open('xb') as out, prefix.with_suffix('.stderr').open('xb') as err:
        process = subprocess.Popen(argv,env=env,stdout=out,stderr=err,start_new_session=True)
        try:
            code = process.wait(timeout=seconds)
        except subprocess.TimeoutExpired:
            timed_out = True
        finally:
            if process.poll() is None:
                try: os.killpg(process.pid,signal.SIGKILL)
                except ProcessLookupError: pass
                process.wait(timeout=5)
            code = process.returncode
            write(prefix.with_suffix('.json'), {'argv':argv,'pid':process.pid,'process_group':process.pid,
                'original_exit':code,'timed_out':timed_out,'elapsed':time.monotonic()-started,
                'executable_sha256':sha(Path(argv[0]))})
    require(not timed_out,label + ': timeout, originals retained')
    # No successful expectation has large output. Keep original files on failure
    # without pulling a sanitizer flood into the Python process or serial log.
    require(prefix.with_suffix('.stdout').stat().st_size <= 65536 and prefix.with_suffix('.stderr').stat().st_size <= 65536,label + ': oversized output')
    return code,prefix.with_suffix('.stdout').read_text(),prefix.with_suffix('.stderr').read_text()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--disposable-vm',action='store_true')
    parser.add_argument('--input',type=Path,required=True,help='new read-only md5 export')
    parser.add_argument('--scratch',type=Path,required=True,help='empty coordinator-mounted tmpfs, at most512MiB')
    args = parser.parse_args()
    require(args.disposable_vm and os.geteuid()==0,'explicit disposable root guest required')
    require(os.uname().machine=='x86_64' and [n for _,n in socket.if_nameindex()]==['lo'],'requires no-NIC GENERIC_X64 guest')
    require(args.input.is_absolute() and args.input.resolve()==args.input,'real absolute input path required')
    require(os.statvfs(args.input).f_flag & os.ST_RDONLY,'input must be read-only')
    scratch = args.scratch
    require(scratch.is_absolute() and scratch.resolve()==scratch and scratch.parent==Path('/tmp'),'private /tmp scratch mount required')
    mounts=[line for line in Path('/proc/self/mountinfo').read_text().splitlines() if line.split()[4]==str(scratch)]
    require(len(mounts)==1 and mounts[0].split(' - ')[1].split()[0]=='tmpfs','scratch must be a distinct tmpfs mount')
    st = os.statvfs(scratch)
    require(st.f_blocks*st.f_frsize<=512*1024**2 and st.f_bavail*st.f_frsize>=256*1024**2,'scratch must provide256–512MiB')
    require(not list(scratch.iterdir()),'scratch already used; no replay')
    for line in (HERE/'SHA256SUMS').read_text().splitlines():
        digest,name=line.split('  ',1)
        require(Path(name).name==name and sha(HERE/name)==digest,'runtime packet changed')
    binding = json.loads((HERE/'input-bindings.json').read_text())
    compiled = json.loads((args.input/'compile-result.json').read_text())
    outer = json.loads((args.input/'result.json').read_text())
    require(compiled['status']==outer['status']=='PASS' and outer['original_docker_exit']==0,'new compile and original container result must pass')
    require(compiled['input_binding_sha256']==sha(HERE/'input-bindings.json') and compiled['candidate_commit']==binding['candidate']['commit'],'source binding differs')
    require(compiled['baseline_repair']==binding['baseline_repair'],'repaired baseline mislabeled')
    expected = {'artifacts/'+mode+'/'+name for mode in ('baseline-repaired','candidate') for name in ('pix574-md5-alignment','pix574-regression-hash','pix574-wii-partition-probe')}
    expected |= {'artifacts/candidate/pix574-fixture-writer','artifacts/lib/libasan.so.8','artifacts/lib/libubsan.so.1'}
    require(set(compiled['artifacts'])==expected,'unexpected artifact set')
    for name,digest in compiled['artifacts'].items():
        require((args.input/name).resolve()==args.input/name and sha(args.input/name)==digest,'artifact changed: '+name)
    for mode in ('baseline-repaired','candidate'):
        name='records/contract-'+mode+'.json'
        require(sha(args.input/name)==compiled['contract_reports'][name],'compiler contract record changed')
        require(json.loads((args.input/name).read_text())['status']=='PASS','instrumentation/include contract did not pass')
    for soname,item in binding['sanitizer_runtimes'].items():
        require(sha(args.input/'artifacts/lib'/soname)==item['sha256'],'wrong target sanitizer runtime')
    resource.setrlimit(resource.RLIMIT_CORE,(0,0))
    resource.setrlimit(resource.RLIMIT_FSIZE,(64*1024**2,64*1024**2))
    # ASan reserves a large virtual shadow; do not impose an incompatible AS cap.
    def interrupted(_sig,_frame): raise KeyboardInterrupt('runtime interrupted')
    signal.signal(signal.SIGTERM,interrupted)
    signal.signal(signal.SIGALRM,interrupted)
    signal.alarm(300)
    out=scratch/'receipts';out.mkdir()
    env={'PATH':'/usr/bin:/bin','LANG':'C.UTF-8','TMPDIR':str(scratch),
         'LD_LIBRARY_PATH':str(args.input/'artifacts/lib'),
         'ASAN_OPTIONS':'detect_leaks=1:halt_on_error=1:abort_on_error=1',
         'UBSAN_OPTIONS':'halt_on_error=1:print_stacktrace=1'}
    result={'status':'FAIL','checks':[],'source_binding_sha256':sha(HERE/'input-bindings.json'),
            'scope':'MD5 and repaired wrapper subset only; not CHD/DolphinTool/full RVZ/Wii-image qualification'}
    def check(label,argv,expected=None,rc=0,seconds=30):
        original,text,err=call(out,label,argv,env,seconds)
        require(original==rc and not err,label+': original exit or sanitizer stderr failed')
        if expected is not None: require(text==expected,label+': exact output differs')
        result['checks'].append(label)
        return text
    try:
        lengths=(0,1,55,56,63,64,65,127,128,129,1024)
        pattern=bytes((i*13+7)&255 for i in range(1024))
        expected=''.join(f'{offset} {length} {split} '+hashlib.md5(pattern[:length],usedforsecurity=False).hexdigest()+'\n'
                         for offset in range(8) for length in lengths for split in range(3))
        require(len(expected.splitlines())==264,'independent oracle row count')
        for mode in ('baseline-repaired','candidate'):
            check(mode+'-md5-264',[args.input/'artifacts'/mode/'pix574-md5-alignment'],expected)
        result['digest_comparisons_per_build']=264
        fixtures=scratch/'fixtures'
        check('make',[args.input/'artifacts/candidate/pix574-fixture-writer',fixtures])
        pairs=['gamecube',fixtures/'official-gamecube.iso','saturn',fixtures/'saturn.iso','saturn',fixtures/'saturn.cue']
        answer='c7803b704fa43d22d8f6e55f4789cb45\n4cd9c8e41cd8d137be15bbe6a93ae1d8\n4cd9c8e41cd8d137be15bbe6a93ae1d8\n'
        for mode in ('baseline-repaired','candidate'):
            exe=args.input/'artifacts'/mode/'pix574-regression-hash'
            check(mode+'-formats',[exe,'1',*pairs],answer)
            check(mode+'-repeat',[exe,'16',*pairs],answer*16,seconds=60)
        part=(fixtures/'wii-helper-partition.bin').read_bytes()
        expected=hashlib.md5(part[0x1000:0x35e0]+part[0x4100:0x4200]+part[0x5100:0x5280],usedforsecurity=False).hexdigest()+'\n'
        for mode in ('baseline-repaired','candidate'):
            check(mode+'-wii-helper',[args.input/'artifacts'/mode/'pix574-wii-partition-probe',fixtures/'wii-helper-partition.bin'],expected)
        check('candidate-wii-short',[args.input/'artifacts/candidate/pix574-wii-partition-probe',fixtures/'wii-helper-short-section.bin'],'FAIL\n',rc=2)
        result['status']='PASS'
        return 0
    except BaseException as exc:
        result['error']=repr(exc)
        raise
    finally:
        signal.alarm(0)
        write(out/'result.json',result)
        print(json.dumps(result),flush=True)


if __name__ == '__main__': raise SystemExit(main())

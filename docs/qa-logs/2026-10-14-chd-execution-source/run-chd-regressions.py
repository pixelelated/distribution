#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""UNRUN: selected CHD cases from sealed run-regressions.py, no completed suites.

This is a case runner, not an admission/lifecycle owner. Coordinator must wrap it
with the existing 240s guest owner, descendant cleanup and original-exit capture.
"""
import argparse
import importlib.util
import json
import os
from pathlib import Path
import re
import sys
import time
sys.dont_write_bytecode=True
HERE=Path(__file__).resolve().parent
INPUT=Path('/tmp/pix-input/pix574-chd')
PRIVATE=Path('/run/pix574-chd')
spec=importlib.util.spec_from_file_location('bounded',HERE/'bounded.py')
bounded=importlib.util.module_from_spec(spec);spec.loader.exec_module(bounded)
require=bounded.require
sha=bounded.sha


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',type=Path,required=True)
    parser.add_argument('--chdman-sha256',required=True,help='actual admitted target ELF SHA256; no placeholder/default')
    args=parser.parse_args();started=time.monotonic();deadline=started+235
    require(sys.version_info>=(3,11),'immutable bounded.py requires Python3.11+')
    require(os.geteuid()==0 and os.uname().machine=='x86_64','disposable GENERIC_X64 root guest required')
    require(sorted(p.name for p in Path('/sys/class/net').iterdir())==['lo'],'no-NIC guest required')
    require(HERE==INPUT/'packet' and INPUT.resolve()==INPUT and os.statvfs(INPUT).f_flag&os.ST_RDONLY,'exact read-only public packet required')
    for line in (HERE/'SHA256SUMS').read_text().splitlines():
        digest,name=line.split('  ',1)
        require(Path(name).name==name and sha(HERE/name)==digest,'packet member changed')
    binding=json.loads((HERE/'input-bindings.json').read_text())
    require(PRIVATE.resolve()==PRIVATE and PRIVATE.stat().st_mode&0o777==0o700,'private scratch must be real and mode0700')
    mounts=[s for s in Path('/proc/self/mountinfo').read_text().splitlines() if s.split()[4]==str(PRIVATE)]
    require(len(mounts)==1 and mounts[0].split(' - ')[1].split()[0]=='tmpfs'
            and 'noexec' not in mounts[0].split()[5].split(','),'private executable tmpfs required')
    fs=os.statvfs(PRIVATE)
    require(fs.f_blocks*fs.f_frsize<=2*1024**3 and fs.f_bavail*fs.f_frsize>=128*1024**2,'private scratch exceeds2GiB or lacks128MiB free')
    artifacts=PRIVATE/'artifacts'
    for name,row in binding['artifacts'].items():
        path=artifacts/name
        require(path.resolve()==path and path.stat().st_size==row['bytes'] and sha(path)==row['sha256'],'retained artifact changed: '+name)
    generator=INPUT/'original/make-fixtures.py';zstd=PRIVATE/'lib/libzstd.so.1';chdman=PRIVATE/'chdman'
    for path,row in [(generator,binding['corrected_generator']),(zstd,binding['zstd_library'])]:
        require(path.resolve()==path and path.stat().st_size==row['bytes'] and sha(path)==row['sha256'],'generator/Zstd identity changed')
    require(re.fullmatch('[0-9a-f]{64}',args.chdman_sha256) and chdman.resolve()==chdman
            and sha(chdman)==args.chdman_sha256,'actual chdman ELF hash required')
    with chdman.open('rb') as stream:header=stream.read(20)
    require(header[:7]==b'\x7fELF\x02\x01\x01' and header[18:20]==b'\x3e\x00','target x86_64 ELF required, not a wrapper')
    require(args.output.parent==Path('/tmp/pix-output') and args.output.parent.resolve()==args.output.parent
            and re.fullmatch('pix574-chd-[A-Za-z0-9_-]+',args.output.name),'fresh output under /tmp/pix-output required')
    args.output.mkdir(mode=0o700)
    work=PRIVATE/'work';work.mkdir(mode=0o700)
    for name in ('home','tmp','config','cache'):(work/name).mkdir(mode=0o700)
    libpath=':'.join(str(p) for p in (PRIVATE/'lib',artifacts/'lib',PRIVATE/'chdman-lib'))
    require((PRIVATE/'chdman-lib').is_dir(),'coordinator must stage the inspected chdman loader closure')
    env={'PATH':'/usr/bin:/bin','LANG':'C','LC_ALL':'C','HOME':str(work/'home'),'TMPDIR':str(work/'tmp'),
         'USER':'pix574-synthetic','LOGNAME':'pix574-synthetic','XDG_CONFIG_HOME':str(work/'config'),
         'XDG_CACHE_HOME':str(work/'cache'),'LD_LIBRARY_PATH':libpath,
         'ASAN_OPTIONS':'detect_leaks=1:halt_on_error=1:abort_on_error=1',
         'UBSAN_OPTIONS':'halt_on_error=1:print_stacktrace=1'}
    result={'status':'FAIL','checks':[],'chdman_sha256':args.chdman_sha256,'environment':env,
            'candidate_commit':binding['candidate_commit'],'baseline_repair':binding['baseline_repair'],
            'total_outer_limit_seconds':240,'work_deadline_monotonic':deadline,'outer_cleanup_required':True,
            'scope':'uncompressed single-track CHD and new CHD-bearing transitions only; not native proxy/Wii image/gameplay'}
    def call(label,argv,expected=None,seconds=30,empty_stderr=True):
        remaining=min(seconds,deadline-time.monotonic())
        require(remaining>0,'shared work deadline exhausted')
        receipt,out,err=bounded.run(args.output,label,argv,remaining,env,work)
        require(receipt['returncode']==0 and not receipt['timed_out'],label+': original child failed')
        if empty_stderr:require(not err,label+': stderr/sanitizer diagnostic retained')
        if expected is not None:require(out==expected,label+': exact ordered hashes differ')
        result['checks'].append(label)
    try:
        fixtures=work/'fixtures'
        call('make',[artifacts/'candidate/pix574-fixture-writer',fixtures])
        cases=work/'rvz-cases'
        call('make-rvz',[sys.executable,'-I','-S','-B',generator,'--output',cases,'--zstd-library',zstd])
        cases,rows=bounded.synthetic_manifest(cases)
        by_name={r['name']:r for r in rows}
        for name,expected in binding['corrected_cases'].items():
            require(by_name[name]==expected,'generated case differs from accepted attempt02: '+name)
        expected=binding['expected'];gc=expected['official_gc'];saturn=expected['saturn'];cd=fixtures/'saturn.chd'
        # chdman progress is preserved on stderr, exactly as in the old runner.
        call('chd-create',[chdman,'createcd','-i',fixtures/'saturn.cue','-o',cd,'-c','none','-np','1'],empty_stderr=False)
        require(cd.stat().st_size>124,'real CHD creation missing/short')
        for mode in ('baseline-repaired','candidate'):
            exe=artifacts/mode/'pix574-regression-hash'
            pairs=['gamecube',fixtures/'official-gamecube.iso','saturn',fixtures/'saturn.iso',
                   'saturn',fixtures/'saturn.cue','saturn',cd,'gamecube',fixtures/'official-gamecube.iso']
            answer='\n'.join([gc,saturn,saturn,saturn,gc])+'\n'
            call(mode+'-formats',[exe,'1',*pairs],answer)
            call(mode+'-repeat',[exe,'16',*pairs],answer*16,seconds=60)
        transition=['saturn',cd,'gamecube',cases/'mixed-zstd.rvz','nes',cases/'ordinary.nes','saturn',fixtures/'saturn.cue']
        answer='\n'.join([saturn,expected['rvz'],expected['nes'],saturn])+'\n'
        call('rvz-cd-transition',[artifacts/'candidate/pix574-regression-hash','16',*transition],answer*16,seconds=60)
        require(time.monotonic()<deadline,'shared work deadline exhausted')
        result.update(status='PASS',ordered_hash_rows=234,wrapper_invocations=5,
                      fixtures={str(p.relative_to(work)):sha(p) for folder in (fixtures,cases) for p in folder.iterdir() if p.is_file()})
    except BaseException as exc:
        result['error']=repr(exc)
        raise
    finally:
        result['elapsed']=time.monotonic()-started
        with (args.output/'result.json').open('x') as stream:json.dump(result,stream,indent=2);stream.write('\n')
        print(json.dumps(result),flush=True)
    return 0


if __name__=='__main__':raise SystemExit(main())

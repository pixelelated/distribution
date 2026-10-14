#!/usr/bin/env python3
"""Guest-only worker; invoked only by guest-run.py under its single deadline."""
import argparse
import os
from pathlib import Path
import shutil
import subprocess
import sys
import time
sys.dont_write_bytecode=True
sys.path.insert(0,str(Path(__file__).resolve().parent))
from guest_support import HERE,INPUT,SCRATCH,identity,interpreter,read,require,sha,verify_input,write


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--run-id',required=True)
    parser.add_argument('--output',type=Path,required=True)
    parser.add_argument('--deadline',type=float,required=True)
    args=parser.parse_args();out=args.output
    binding,bundle=verify_input()
    base={'PATH':'/usr/bin:/bin','LANG':'C','LC_ALL':'C','HOME':str(SCRATCH/'home'),
          'USER':'pix574-synthetic','LOGNAME':'pix574-synthetic','TMPDIR':str(SCRATCH/'tmp'),
          'XDG_CONFIG_HOME':str(SCRATCH/'config'),'XDG_CACHE_HOME':str(SCRATCH/'cache'),
          'XDG_DATA_HOME':str(SCRATCH/'data'),'XDG_STATE_HOME':str(SCRATCH/'state'),
          'PYTHONDONTWRITEBYTECODE':'1',
          'ASAN_OPTIONS':'detect_leaks=1:halt_on_error=1:abort_on_error=1',
          'UBSAN_OPTIONS':'halt_on_error=1:print_stacktrace=1'}
    for name in ('home','tmp','config','cache','data','state'):(SCRATCH/name).mkdir(mode=0o700)
    write(out/'environment.json',base)

    def run(label,argv,seconds,env=base):
        remaining=min(seconds,args.deadline-time.monotonic())
        require(remaining>0,'single work deadline exhausted')
        argv=[str(v) for v in argv];started=time.monotonic()
        receipt={'argv':argv,'executable_sha256':sha(argv[0]),'timeout':False}
        with (out/(label+'.stdout')).open('xb') as stdout,(out/(label+'.stderr')).open('xb') as stderr:
            child=subprocess.Popen(argv,stdout=stdout,stderr=stderr,env=env,cwd=SCRATCH,start_new_session=True)
            receipt.update(identity=identity(child.pid),pid=child.pid,process_group=child.pid)
            write(out/(label+'.started.json'),receipt)
            try:child.wait(timeout=remaining)
            except subprocess.TimeoutExpired:
                # The supervisor owns all descendant sessions, including oracle children.
                receipt['timeout']=True
                write(out/(label+'.timeout.json'),dict(receipt,elapsed=time.monotonic()-started))
                raise RuntimeError(label+': deadline; supervisor must retire descendants')
        receipt.update(returncode=child.returncode,elapsed=time.monotonic()-started)
        write(out/(label+'.json'),receipt)
        require(child.returncode==0,label+': original child failed')
        return receipt

    run('stage',[sys.executable,'-I','-S','-B',INPUT/'stager/guest-stage.py','--input',INPUT/'bundle',
                 '--manifest-sha256',binding['bundle_manifest_sha256'],'--run-id',args.run_id],60)
    staged=Path('/tmp')/('pix574-dolphin-'+args.run_id)
    stage_receipt=staged.with_suffix('.stage.json')
    shutil.copyfile(stage_receipt,out/'stage-copy.json')
    require(read(stage_receipt)['status']=='STAGED_NOT_EXECUTED','stager did not complete')
    # The original stager deliberately makes a non-executing /tmp copy. Preserve it;
    # only this independently rechecked copy is executed on the admitted exec tmpfs.
    private=SCRATCH/'bundle';shutil.copytree(staged,private)
    for name,row in bundle['files'].items():
        path=private/name
        require(path.stat().st_size==row['bytes'] and path.stat().st_mode&0o7777==row['mode']
                and sha(path)==row['sha256'],'private bundle copy differs: '+name)
    require(sha(private/'manifest.json')==binding['bundle_manifest_sha256'],'private manifest changed')
    hash_root=SCRATCH/'hash';hash_root.mkdir(mode=0o700);(hash_root/'lib').mkdir(mode=0o700)
    for name,item in binding['files'].items():
        if not name.startswith('hash/'):continue
        dst=SCRATCH/name;shutil.copyfile(INPUT/name,dst);dst.chmod(0o755)
        require(dst.stat().st_size==item['bytes'] and sha(dst)==item['sha256'],'private hash artifact differs')
    program=private/'dolphin-tool';hash_binary=hash_root/'pix574-regression-hash'
    installed=Path(interpreter(program));loader=private/bundle['loader']
    require(installed.is_file() and os.access(installed,os.X_OK),'installed PT_INTERP unavailable')
    def file_identity(path):
        return dict(invocation_path=str(path),resolved_path=str(path.resolve(strict=True)),
                    bytes=path.stat().st_size,mode=path.stat().st_mode&0o7777,sha256=sha(path))
    hash_interp=Path(interpreter(hash_binary))
    require(hash_interp.is_file() and os.access(hash_interp,os.X_OK),'hash PT_INTERP unavailable')
    comparison={'installed':file_identity(installed),'private':file_identity(loader),
                'hash_binary_installed_loader':file_identity(hash_interp),'sys_lookup_measured':False,
                'sys_source_contract':'LINUX_LOCAL_DEV uses /proc/self/exe parent + /Sys; both private ELF files are siblings of Sys',
                'help_limit':'OptionParser exits before SetUserDirectory/UICommon::Init'}
    comparison['identical_bytes']=comparison['installed']['sha256']==comparison['private']['sha256']
    write(out/'loader-identities.json',comparison)
    libpath=str(private/'lib')+':'+str(hash_root/'lib')
    target=dict(base,LD_LIBRARY_PATH=libpath)
    write(out/'target-environment.json',target)
    for label,ld in [('installed-loader',installed),('private-loader',loader)]:
        run(label+'-list',[ld,'--library-path',libpath,'--list',program],10)
        require(not (out/(label+'-list.stderr')).read_bytes(),'loader list stderr present')
    run('direct-help',[program,'convert','--help'],10,target)
    run('private-help',[loader,'--library-path',libpath,program,'convert','--help'],10,target)
    for label in ('direct-help','private-help'):
        help_text=(out/(label+'.stdout')).read_text().lower()
        require('usage: convert' in help_text and '--input' in help_text
                and not (out/(label+'.stderr')).read_bytes(),'help output did not match')
    run('generator',[sys.executable,'-I','-S','-B',INPUT/'original/make-fixtures.py',
                     '--output',SCRATCH/'cases','--zstd-library',private/'lib/libzstd.so.1'],30)
    manifest=read(SCRATCH/'cases/manifest.json')
    raw=next(r for r in manifest if r['name']=='synthetic.iso')
    shutil.copyfile(SCRATCH/'cases/manifest.json',out/'synthetic-manifest.json')
    # Actual ELF paths, never a loader wrapper: immutable oracle hashes argv[0]
    # itself and passes this inherited environment to each native command.
    run('oracle',[sys.executable,'-I','-S','-B',INPUT/'oracle/run-independent-format.py',
                  '--dolphin-tool',program,'--hash-binary',hash_binary,
                  '--cases',SCRATCH/'cases','--original-packet',INPUT/'original',
                  '--output',out/'oracle','--dolphin-sha256',binding['dolphin_sha256'],
                  '--hash-sha256',binding['hash_sha256']],235,target)
    result=read(out/'oracle/result.json')
    require(result['result']=='PASS' and result['dolphin_sha256']==binding['dolphin_sha256']
            and result['hash_binary_sha256']==binding['hash_sha256'] and len(result['cases'])==9,'oracle result differs')
    labels=['decode-'+str(i) for i in range(5)]+['encode-none','roundtrip-none','hash-none','encode-zstd','roundtrip-zstd','hash-zstd']
    originals=[]
    for label in labels:
        row=read(out/'oracle'/(label+'.json'));hash_case=label.startswith('hash-')
        expected=hash_binary if hash_case else program
        require(row['returncode']==0 and not row['timed_out'] and row['argv'][0]==str(expected)
                and row['executable_sha256']==sha(expected),'original oracle child differs: '+label)
        require(not (out/'oracle'/(label+'.stderr')).read_bytes(),'native stderr present: '+label)
        originals.append(dict(label=label,returncode=row['returncode'],executable_sha256=row['executable_sha256']))
    encoded={}
    for mode in ('none','zstd'):
        path=out/'oracle'/('dolphin-'+mode+'.rvz')
        encoded[str(path.relative_to(out))]={'sha256':sha(path),'bytes':path.stat().st_size,
            'expected_gamecube_md5':raw['expected'],'generator_raw_sha256':raw['sha256']}
    for name,row in bundle['files'].items():
        path=private/name
        require(path.stat().st_size==row['bytes'] and path.stat().st_mode&0o7777==row['mode']
                and sha(path)==row['sha256'],'private payload changed during run: '+name)
    require(sha(hash_binary)==binding['hash_sha256'],'candidate changed during run')
    write(out/'native-proxy-input.json',dict(status='INDEPENDENT_FORMAT_PASS_NATIVE_PROXY_UNRUN',
        files=encoded,dolphin_sha256=binding['dolphin_sha256'],hash_binary_sha256=binding['hash_sha256'],
        generator_sha256=binding['files']['original/make-fixtures.py']['sha256'],
        legal_data='Self-created nonbootable PX5740 synthetic GameCube data; no game/ROM/account'))
    write(out/'worker-result.json',dict(status='PASS',originals=originals,sys_lookup_measured=False,
        counts={'synthetic_decodes':5,'independent_encodes':2,'roundtrips':2,'candidate_hashes':2},
        retained_rvz=list(encoded),limits='GameCube NONE/Zstandard only; no native proxy, gameplay, Wii, CHD or observed Sys lookup claim'))


if __name__=='__main__':main()

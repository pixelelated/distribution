#!/usr/bin/env python3
"""Stage exact qualified converter and execute only the remaining CHD cases."""
import argparse
import importlib.util
import json
import os
from pathlib import Path
import shutil
import sys
import time
sys.dont_write_bytecode=True
sys.path.insert(0,str(Path(__file__).resolve().parent))
from guest_support import HERE,INPUT,SCRATCH,OUTPUT,read,write,sha,require,interpreter,verify_packet


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--run-id',required=True)
    parser.add_argument('--output',type=Path,required=True)
    parser.add_argument('--deadline',type=float,required=True)
    args=parser.parse_args();out=args.output
    verify_packet();binding=read(HERE/'stage-bindings.json')
    require(time.monotonic()<args.deadline,'shared outer deadline exhausted')
    allowed=set(binding['files'])|{'owner/'+p.name for p in HERE.iterdir()}
    require({str(p.relative_to(INPUT)) for p in INPUT.rglob('*') if p.is_file()}==allowed,'unexpected public inputs')
    for name,row in binding['files'].items():
        p=INPUT/name
        require(not p.is_symlink() and p.resolve()==p and p.stat().st_size==row['bytes'] and sha(p)==row['sha256'],'input changed: '+name)
    case=INPUT/'packet';spec=importlib.util.spec_from_file_location('chd_bounded',case/'bounded.py');bounded=importlib.util.module_from_spec(spec);spec.loader.exec_module(bounded)
    for name,row in binding['files'].items():
        dest=row.get('stage_to')
        if dest:
            p=SCRATCH/dest;require(not p.exists(),'stage target exists');p.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(INPUT/name,p);p.chmod(row.get('mode',0o644));require(sha(p)==row['sha256'],'staging changed')
    chd=SCRATCH/'chdman';loader=SCRATCH/'chdman-loader';interp=Path(interpreter(chd));libs=SCRATCH/'chdman-lib'
    write(out/'loader-bindings.json',{'actual_chdman_sha256':sha(chd),'private_loader_sha256':sha(loader),'installed_interpreter':str(interp),'installed_resolved':str(interp.resolve()),'installed_sha256':sha(interp),'closure_manifest_sha256':binding['closure_manifest_sha256']})
    home=SCRATCH/'probe-home';home.mkdir(mode=0o700)
    env={'PATH':'/usr/bin:/bin','LANG':'C','LC_ALL':'C','HOME':str(home),'LD_LIBRARY_PATH':str(libs)}
    calls=[]
    def call(label,argv,seconds=20):
        remaining=min(seconds,args.deadline-time.monotonic());require(remaining>0,'outer work deadline exhausted')
        receipt,stdout,stderr=bounded.run(out,label,argv,remaining,env,SCRATCH)
        calls.append({'label':label,'original_returncode':receipt['returncode'],'timed_out':receipt['timed_out']})
        write(out/(label+'-receipt-binding.json'),calls[-1])
        require(receipt['returncode']==0 and not receipt['timed_out'],'original child failed: '+label)
        return stdout,stderr
    for label,argv in [('installed-loader',[interp,'--library-path',libs,'--list',chd]),('private-loader',[loader,'--library-path',libs,'--list',chd])]:
        stdout,stderr=call(label,argv);require('not found' not in stdout+stderr,'unresolved loader dependency')
    for label,argv in [('direct-help',[chd,'help']),('private-help',[loader,'--library-path',libs,chd,'help'])]:
        stdout,stderr=call(label,argv);require('chdman' in (stdout+stderr).lower(),'converter help absent')
    caseout=OUTPUT/('pix574-chd-'+args.run_id)
    try:
        call('selected-chd-cases',[sys.executable,'-I','-S','-B',case/'run-chd-regressions.py','--output',caseout,'--chdman-sha256',binding['chdman_sha256']],seconds=235)
        result=read(caseout/'result.json')
        require(result['status']=='PASS' and result['ordered_hash_rows']==234 and len(result['checks'])==8,'selected CHD result incomplete')
        write(out/'worker-result.json',{'status':'PASS','calls':calls,'case_output':str(caseout),'ordered_hash_rows':234,'original_case_exit':0,'chdman_sha256':sha(chd),'full_image_qualified':False})
    except BaseException as exc:
        write(out/'worker-result.json',{'status':'FAIL','calls':calls,'error':repr(exc)});raise

if __name__=='__main__':raise SystemExit(main())

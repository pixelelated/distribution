#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""UNRUN; optional separately supplied pinned DolphinTool, synthetic bytes only.

No product build, download or emulator launch. Conversion is explicit future
runtime and requires coordinator allocation plus an already qualified oracle tool.
"""
import argparse
import importlib.util
import json
from pathlib import Path
import sys
sys.dont_write_bytecode = True
spec=importlib.util.spec_from_file_location('bounded',Path(__file__).with_name('bounded.py'))
bounded=importlib.util.module_from_spec(spec);spec.loader.exec_module(bounded)


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    for name in ['dolphin-tool','hash-binary','cases','original-packet','output']:
        parser.add_argument('--'+name,type=Path,required=True)
    parser.add_argument('--dolphin-sha256',required=True)
    parser.add_argument('--hash-sha256',required=True)
    args=parser.parse_args()
    bounded.require(bounded.sha(args.dolphin_tool)==args.dolphin_sha256,'independent oracle binary changed')
    bounded.require(bounded.sha(args.hash_binary)==args.hash_sha256,'hash binary changed')
    binding=json.loads(Path(__file__).with_name('source-bindings.json').read_text())
    bounded.require(bounded.sha(args.original_packet/'make-fixtures.py')==binding['original_generator_sha256'],'original generator changed')
    args.cases,rows=bounded.synthetic_manifest(args.cases)
    raw=next(r for r in rows if r['name']=='synthetic.iso')
    data=(args.cases/raw['name']).read_bytes()
    bounded.require(args.output.is_absolute(),'new owner must be absolute')
    args.output.mkdir(mode=0o700)
    user=args.output/'dolphin-user';user.mkdir(mode=0o700)
    results=[]
    def convert(label,source,dest,fmt,extra=()):
        receipt,out,err=bounded.run(args.output,label,[args.dolphin_tool,'convert','-u',user,'-i',source,'-o',dest,'-f',fmt,*extra],60)
        bounded.require(receipt['returncode']==0 and dest.is_file(),label+': original conversion failed')
        results.append(dict(label=label,output_sha256=bounded.sha(dest)))
    for index,row in enumerate(r for r in rows if r['expected'] is not None and r['name'].lower().endswith('.rvz')):
        dest=args.output/('decoded-'+str(index)+'.iso')
        convert('decode-'+str(index),args.cases/row['name'],dest,'iso')
        bounded.require(dest.read_bytes()==data,'Dolphin disagrees with our full RVZ reconstruction')
    for mode in ['none','zstd']:
        dest=args.output/('dolphin-'+mode+'.rvz')
        convert('encode-'+mode,args.cases/raw['name'],dest,'rvz',['-b','131072','-c',mode,'-l','3'])
        decoded=args.output/('roundtrip-'+mode+'.iso')
        convert('roundtrip-'+mode,dest,decoded,'iso')
        bounded.require(decoded.read_bytes()==data,'independent encoder/decoder roundtrip differs')
        result,out,err=bounded.run(args.output,'hash-'+mode,[args.hash_binary,'1','gamecube',dest],15)
        bounded.require(result['returncode']==0 and out==raw['expected']+'\n' and not err,'independently encoded RVZ hash differs')
    (args.output/'result.json').write_text(json.dumps(dict(result='PASS',cases=results,
        dolphin_sha256=args.dolphin_sha256,hash_binary_sha256=args.hash_sha256,
        limits='synthetic GameCube NONE/Zstandard only; no full-disc/gameplay integrity claim'),indent=2)+'\n')
    print('PASS independent Dolphin conversion and independently encoded RVZ hash controls')


if __name__=='__main__':
    main()

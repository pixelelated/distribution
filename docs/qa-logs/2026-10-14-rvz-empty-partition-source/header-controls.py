#!/usr/bin/env python3
"""UNRUN: bounded pure-Python header controls; no native converter or zstd load.

Coordinator admission required. These selected checks do not certify RVZ format;
only the actual independent Dolphin decoder can qualify the new fixtures.
"""
import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
import struct
import sys
sys.dont_write_bytecode=True


def require(value,message):
    if not value:raise RuntimeError(message)


def load(path,expected,name):
    require(hashlib.sha256(path.read_bytes()).hexdigest()==expected,'source changed: '+name)
    spec=importlib.util.spec_from_file_location(name,path)
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
    return module


def header_hashes(data):
    size=struct.unpack_from('>I',data,0xc)[0]
    return (data[0x10:0x24]==hashlib.sha1(data[0x48:0x48+size]).digest()
            and data[0x34:0x48]==hashlib.sha1(data[:0x34]).digest())


def empty_table_hash(data):
    require(struct.unpack_from('>II',data,0x48+0x90)==(0,0),'unexpected partition table shape')
    return data[0xe8:0xfc]==hashlib.sha1(b'').digest()


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--historical-generator',type=Path,required=True)
    args=parser.parse_args();here=Path(__file__).resolve().parent
    binding=json.loads((here/'source-findings.json').read_text())
    old=load(args.historical_generator,binding['historical_generator_sha256'],'historical_generator')
    new=load(here/'make-fixtures.py',binding['candidate_generator_sha256'],'candidate_generator')
    raw=old.raw_disc();candidate_raw=new.raw_disc();retained=binding['retained_raw']
    require(raw==candidate_raw and len(raw)==retained['bytes']
            and hashlib.sha256(raw).hexdigest()==retained['sha256'],'legal raw data changed')
    require(old.oracle(raw)==new.oracle(raw)==retained['expected_gamecube_md5'],'native expected MD5 changed')
    original_sha={False:'619520814570cc970ef3becdd23686389a332d4f99e4d8488860372f6f935608',
                  True:'18062e512925aac1cd75fadb95f6edb7dcdb3f5d399c0302a24ab34c7dfd0658'}
    results=[]
    for packed in (False,True):
        before,old_locations=old.rvz(raw,packed=packed)
        after,new_locations=new.rvz(raw,packed=packed)
        require(hashlib.sha256(before).hexdigest()==original_sha[packed],'historical bytes differ from attempt01 manifest')
        require(header_hashes(before) and header_hashes(after),'outer checksums must both be valid')
        require(before[0xe8:0xfc]==bytes(20) and not empty_table_hash(before),'historical defect absent')
        require(empty_table_hash(after),'candidate lacks empty-table digest')
        require(len(before)==len(after) and old_locations==new_locations,'payload layout changed')
        permitted=set(range(0x10,0x24))|set(range(0x34,0x48))|set(range(0xe8,0xfc))
        changed={i for i,(a,b) in enumerate(zip(before,after)) if a!=b}
        require(changed and changed<=permitted,'change escaped three checksum fields')
        bad=bytearray(after);bad[0xe8:0xfc]=bytes(20);new.seal(bad)
        require(header_hashes(bad) and not empty_table_hash(bad) and bad==before,'resealed original negative must remain invalid')
        flipped=bytearray(after);flipped[0xe8]^=1;new.seal(flipped)
        require(header_hashes(flipped) and not empty_table_hash(flipped),'corrupt partition digest must remain invalid')
        results.append(dict(packed=packed,historical_sha256=original_sha[packed],
                            candidate_sha256=hashlib.sha256(after).hexdigest(),changed_bytes=len(changed)))
    print(json.dumps(dict(status='PASS',scope='selected header controls only; independent decoder still required',
                          raw_sha256=retained['sha256'],expected_native_md5=retained['expected_gamecube_md5'],cases=results)))


if __name__=='__main__':main()

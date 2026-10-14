#!/usr/bin/env python3
"""HELD: bind already staged synthetic inputs and installed ELF bytes; no load/run."""
import argparse
import hashlib
import json
from pathlib import Path
import re
import signal

ROOT=Path('/run/pix583-native-inputs')
PACKET=Path(__file__).resolve().parents[1]
BINDINGS_SHA256='d66230e0c13c527b20b00d305b2fd9da4b0f65585aa4591a2a8bd29a1add2682'


def need(value,message):
    if not value:raise RuntimeError(message)


def sha(path):
    with Path(path).open('rb') as stream:return hashlib.file_digest(stream,'sha256').hexdigest()


def row(relative):
    path=(ROOT/relative).resolve(strict=True)
    need(path.is_relative_to(ROOT) and path.is_file(),'input outside staging: '+relative)
    return {'path':relative,'bytes':path.stat().st_size,'sha256':sha(path)}


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    for role in ('rchash','zstd','crypto'):parser.add_argument('--'+role,type=Path,required=True)
    parser.add_argument('--dolphin-sha256',required=True)
    parser.add_argument('--image-sha256',required=True)
    args=parser.parse_args()
    def expired(*_):raise TimeoutError('10-second admission preparation limit')
    signal.signal(signal.SIGALRM,expired);signal.alarm(10)
    need(ROOT.resolve(strict=True)==ROOT,'staged input root redirects')
    need(sha(PACKET/'bindings.json')==BINDINGS_SHA256,'packet binding changed')
    binding=json.loads((PACKET/'bindings.json').read_text())
    need(args.image_sha256==binding['accepted_image_sha256'],'unreviewed VM image')
    need(re.fullmatch('[0-9a-f]{64}',args.dolphin_sha256),'expected converter identity required')
    files=list(ROOT.rglob('*'))
    need(not any(p.is_symlink() for p in files),'no symlinks in staged public inputs')
    need(sum(p.stat().st_size for p in files if p.is_file())<=32*1024*1024,'32MiB staging budget exceeded')
    need((ROOT/'synthetic-manifest.json').stat().st_size<=65536,'oversized generator manifest')
    manifest=json.loads((ROOT/'synthetic-manifest.json').read_text())
    raw=next(r for r in manifest if r['name']=='synthetic.iso')
    raw_file=row('synthetic.iso')
    need(raw_file['bytes']==raw['bytes'] and raw_file['sha256']==raw['sha256'],'generator/raw identity mismatch')
    libraries={}
    for role,soname in (('rchash','libraproxy_rchash.so'),('zstd','libzstd.so.1'),('crypto','libcrypto.so.3')):
        path=getattr(args,role);resolved=path.resolve(strict=True)
        need(path.is_absolute() and resolved.is_relative_to(Path('/usr/lib')),'installed /usr/lib library required')
        need(resolved.stat().st_size<=64*1024*1024,'unexpected native library size')
        libraries[role]={'path':str(path),'resolved_path':str(resolved),'sha256':sha(resolved),'soname':soname}
    provenance=ROOT/'native-provenance.json'
    need(provenance.stat().st_size<=65536,'oversized provenance')
    admission={'schema':1,'synthetic_only':True,'image_sha256':args.image_sha256,
        'boot_id':Path('/proc/sys/kernel/random/boot_id').read_text().strip(),
        'ports':[8080,18081],'prepared':'prepared','prepared_source_sha256':sha(ROOT/'prepared/source.json'),
        'inputs':{'iso':raw_file,'rvz_none':row('dolphin-none.rvz'),'rvz_zstd':row('dolphin-zstd.rvz')},
        'synthetic_manifest':row('synthetic-manifest.json'),'expected_hash':raw['expected'],
        'oracle':{'dolphin_pin':binding['dolphin_pin'],'dolphin_sha256':args.dolphin_sha256,
                  'result':row('oracle/result.json'),
                  'receipts':{label:row('oracle/'+label+'.json') for mode in ('none','zstd')
                              for label in ('encode-'+mode,'roundtrip-'+mode,'hash-'+mode)},
                  'hash_stdout':{mode:row('oracle/hash-'+mode+'.stdout') for mode in ('none','zstd')}},
        'libraries':libraries,'native_provenance':json.loads(provenance.read_text())}
    target=ROOT/'admission.json'
    with target.open('x') as stream:stream.write(json.dumps(admission,indent=2)+'\n')
    signal.alarm(0)
    print(json.dumps({'status':'PREPARED_ONLY','admission':str(target),'sha256':sha(target)}))


if __name__=='__main__':main()

#!/usr/bin/env python3
"""Apply the exact diagnostic overlay to an owned extracted standard CEF SDK.

No download, build, process launch, user creation or permission change. UNRUN.
"""
import argparse
import gzip
import hashlib
import json
import pathlib
import subprocess


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--sdk',type=pathlib.Path,required=True)
    args=parser.parse_args()
    sdk=args.sdk.resolve(strict=True)
    packet=pathlib.Path(__file__).resolve().parent
    spec=json.loads((packet/'probe-inputs.json').read_text())
    if not sdk.name.startswith('cef_binary_154.0.34+'):
        parser.error('expected separately admitted exact standard CEF SDK')
    for relative, expected in spec['modified_files'].items():
        path=sdk/relative
        if path.is_symlink() or sdk not in path.resolve().parents or digest(path)!=expected['before_sha256']:
            raise SystemExit('source mismatch: '+relative)
    patch=gzip.decompress((packet/'cefsimple-probe.patch.gz').read_bytes())
    if hashlib.sha256(patch).hexdigest()!=spec['patch_sha256']:
        raise SystemExit('patch hash mismatch')
    command=['patch','--batch','--fuzz=0','-p1']
    subprocess.run(command+['--dry-run'],input=patch,cwd=sdk,check=True)
    subprocess.run(command,input=patch,cwd=sdk,check=True)
    for relative, expected in spec['modified_files'].items():
        if digest(sdk/relative)!=expected['after_sha256']:
            raise SystemExit('result hash mismatch: '+relative)
    print(json.dumps({'prepared':True,'cef_commit':spec['cef_commit'],'compiled':False,'runtime':'UNRUN'}))


if __name__ == '__main__':
    main()

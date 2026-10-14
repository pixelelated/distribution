#!/usr/bin/env python3
"""Restore byte-identical execution packet from compact evidence storage; run nothing."""
import argparse
import gzip
import hashlib
import json
from pathlib import Path

p=argparse.ArgumentParser(description=__doc__)
p.add_argument('--source',type=Path,required=True)
p.add_argument('--destination',type=Path,required=True)
a=p.parse_args();source=a.source.resolve(strict=True);dest=a.destination.absolute()
assert dest.is_relative_to('/tmp') or dest.is_relative_to('/workspace/tmp')
assert not dest.exists() and not dest.is_symlink()
mapping=json.loads((source/'stored-artifacts.json').read_text())
manifest=(source/'execution-SHA256SUMS.txt').read_bytes();files={}
for line in manifest.decode().splitlines():
 digest,name=line.split('  ',1);relative=Path(name)
 assert not relative.is_absolute() and '..' not in relative.parts
 row=mapping.get(name)
 raw=gzip.decompress((source/row['stored']).read_bytes()) if row else (source/name).read_bytes()
 assert hashlib.sha256(raw).hexdigest()==digest
 files[relative]=raw
# Validate every byte before creating a fresh caller-owned output.
dest.mkdir(parents=True,mode=0o700)
for name,raw in files.items():
 path=dest/name;path.parent.mkdir(parents=True,exist_ok=True);path.write_bytes(raw)
(dest/'SHA256SUMS').write_bytes(manifest)
print(json.dumps({'destination':str(dest),'original_manifest_sha256':hashlib.sha256(manifest).hexdigest(),'files':len(files),'executed':False}))

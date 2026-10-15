#!/usr/bin/env python3
"""Run after original guest-owner exit; bind closed output streams and compact files."""
import hashlib,json
from pathlib import Path
root=Path('/tmp/pix-output');rows=[]
for f in sorted(root.rglob('*')):
    if f.is_symlink():raise RuntimeError('unexpected output symlink')
    if not f.is_file():continue
    assert f.name!='guest-export-manifest.json','export already attempted'
    assert f.stat().st_size<=64*1024**2
    with f.open('rb') as stream:digest=hashlib.file_digest(stream,'sha256').hexdigest()
    rows.append({'path':str(f.relative_to(root)),'bytes':f.stat().st_size,'sha256':digest})
assert len(rows)<=256 and sum(r['bytes'] for r in rows)<=208*1024**2
with (root/'guest-export-manifest.json').open('x') as stream:json.dump(rows,stream,indent=2);stream.write('\n')

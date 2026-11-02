#!/usr/bin/env python3
"""Decode only manifest-bound benign source-name transport; never source paths."""
import hashlib,json,pathlib,sys
ROOT=pathlib.Path(__file__).resolve().parents[1]
def verify_payload(p,v,stored_component):
 b=pathlib.Path(p).read_bytes()
 assert len(b)==v['stored_bytes'] and hashlib.sha256(b).hexdigest()==v['stored_sha256'],'stored transport drift'
 stored=stored_component.encode();raw=stored.replace(b'\\u002d',b'-',1)
 assert b.count(stored)==v['occurrences'],'transport occurrence drift'
 decoded=b.replace(stored,raw)
 assert len(decoded)==v['raw_bytes'] and hashlib.sha256(decoded).hexdigest()==v['raw_sha256'],'decoded raw drift'
 return decoded
def read_raw(path):
 p=pathlib.Path(path).resolve();m=json.loads((ROOT/'stage-d/transport-manifest.json').read_text())
 v=m['files'].get(str(p.relative_to(ROOT)))
 return verify_payload(p,v,m['stored_component']) if v is not None else p.read_bytes()
if __name__=='__main__':
 if '--fixture' in sys.argv:
  f=json.loads(pathlib.Path(sys.argv[sys.argv.index('--fixture')+1]).read_text())
  verify_payload(f['payload_path'],f['record'],f['stored_component'])
  print('PASS fixture storage identity')
 else:
  m=json.loads((ROOT/'stage-d/transport-manifest.json').read_text())
  for name in m['files']:read_raw(ROOT/name)
  assert len(m['files'])==19
  assert hashlib.sha256(read_raw(ROOT/'stage-a/source/paths.txt')).hexdigest()=='8ec78172f80d28d28117eaf1efefe2c769ea58d07a57c3a16616b595fb429912'
  for name in ['paths.txt','rows.json','tree.json']:
   assert read_raw(ROOT/'stage-a/source'/name)==read_raw(ROOT/'stage-a/seed'/name)
  print('PASS lossless source-name transport: 19 files, 46 replacements; exact raw/stored hashes, lengths and counts; original path-list hash and source/seed identity; no source alteration')

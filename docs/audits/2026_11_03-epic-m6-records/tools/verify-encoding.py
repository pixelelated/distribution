"""Verify new lossless representation and all actual retained receipt streams."""
import hashlib,json,pathlib
A=pathlib.Path(__file__).resolve().parents[1];R=A.parents[2];m=json.loads((A/'stage-d/publication-encoding/manifest.json').read_text());by={x['path']:x for x in m['rows']}
def sha(b):return hashlib.sha256(b).hexdigest()
for x in m['rows']:
 b=(R/x['path']).read_bytes();assert sha(b)==x['stored_sha256']
 orig=json.loads(b).encode() if x['format']=='json-utf8-string' else json.loads((R/x['original_archive']).read_text()).encode()
 assert sha(orig)==x['original_sha256'] and len(orig)==x['original_bytes']
 if x['format']!='json-utf8-string':assert json.loads(orig)==json.loads(b)
count=0
for p in A.rglob('receipt.json'):
 r=json.loads(p.read_text())
 for s in ['stdout','stderr']:
  f=p.parent/s;b=f.read_bytes();x=by.get(str(f.relative_to(R)))
  if x and x['format']=='json-utf8-string':b=json.loads(b).encode()
  assert sha(b)==r[s+'_sha256'],str(f)
 count+=1
print('PASS lossless29-file transport and '+str(count)+' original receipt stream hashes; no controls replayed')

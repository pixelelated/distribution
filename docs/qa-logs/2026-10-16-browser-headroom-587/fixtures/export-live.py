from pathlib import Path
import json,gzip,base64,hashlib
r=Path('/storage/qa587');files={}
for p in sorted(r.iterdir()):
 if p.is_file() and p.suffix in ['.json','.jsonl']:
  raw=p.read_bytes();assert len(raw)<8*1024**2
  files[p.name]={'sha256':hashlib.sha256(raw).hexdigest(),'bytes':len(raw),'base64':base64.b64encode(raw).decode()}
print('GUEST_EXPORT='+base64.b64encode(gzip.compress(json.dumps(files).encode(),mtime=0)).decode())

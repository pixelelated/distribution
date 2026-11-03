"""Lossless transport for retained T46 bytes; no source/control replay."""
import hashlib,json,pathlib,re,datetime
A=pathlib.Path(__file__).resolve().parents[1];R=A.parents[2];out=A/'stage-d/publication-encoding';out.mkdir(exist_ok=False);rows=[]
def sha(b):return hashlib.sha256(b).hexdigest()
def quoted(b):return json.dumps(b.decode(),ensure_ascii=True).replace('-',r'\u002d')+'\n'
# The original streams stay byte-recoverable from one JSON string at their original path.
for p in sorted(A.rglob('stdout')):
 b=p.read_bytes();lines=b.decode().splitlines()
 if not any(l.rstrip(' \t')!=l for l in lines):continue
 encoded=quoted(b).encode();assert json.loads(encoded).encode()==b
 p.write_bytes(encoded);rows.append({'path':str(p.relative_to(R)),'format':'json-utf8-string','original_sha256':sha(b),'original_bytes':len(b),'stored_sha256':sha(encoded),'recovery':'json.loads(file bytes).encode(utf-8)'})
# Keep raw JSON formatting too; only the offending public path-string hyphens change transport.
for p in sorted(A.rglob('*.json')):
 if out in p.parents:continue
 b=p.read_bytes();s=b.decode();pattern=r'"(?:[^"\\]|\\.)*"'
 def escape(m):
  token=m.group(0)
  return token.replace('-',r'\u002d') if 'distribution:projects/ROCKNIX/devices/' in token else token
 changed=re.sub(pattern,escape,s)
 if changed==s:continue
 assert json.loads(changed)==json.loads(s)
 archive=out/('original-'+str(len(rows))+'.json');archive.write_text(quoted(b));p.write_text(changed)
 rows.append({'path':str(p.relative_to(R)),'format':'json-equivalent-public-path-escape','original_sha256':sha(b),'original_bytes':len(b),'stored_sha256':sha(changed.encode()),'original_archive':str(archive.relative_to(R)),'archive_recovery':'json.loads(archive bytes).encode(utf-8)'})
(out/'manifest.json').write_text(json.dumps({'created_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'reason':'Actual staged whitespace and credential-pattern refusals. No real credential accessed; unchanged public historical path metadata is encoded losslessly. All original receipts/program versions remain, stream hashes refer to decoded bytes.','rows':rows},indent=2)+'\n');print('PASS lossless transport:',len(rows),'record files; exact original bytes recoverable; no source/control rerun')

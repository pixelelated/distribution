from pathlib import Path
import hashlib,importlib.machinery,json,re,shlex,tempfile
owner=Path(__file__).parent
module=importlib.machinery.SourceFileLoader('scan',str(owner/'scan-artifact.py')).load_module()
line,=[x for x in (owner/'secret-patterns').read_text().splitlines() if x.startswith('SECRET_PATTERNS=')]
patterns=re.compile(shlex.split(line)[0].split('=',1)[1].encode())
rows=json.loads((owner/'context-review.json').read_text())['contexts'];allow=json.loads((owner/'allowlist.json').read_text());results=[]
with tempfile.TemporaryDirectory(prefix='pixelelated-context-controls-') as name:
 root=Path(name)
 for row in rows:
  p=root/row['path'];p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(row['text'].encode())
  assert module.scan(root,allow,patterns)['pass']
  removed=dict(allow);removed['branding']=[r for r in allow['branding'] if (r['path'],r['context_sha256'])!=(row['path'],row['context_sha256'])]
  assert not module.scan(root,removed,patterns)['pass']
  p.write_bytes(b'UNREVIEWED-'+row['text'].encode());assert not module.scan(root,allow,patterns)['pass']
  p.write_bytes(row['text'].encode());other=root/'different-path';p.rename(other);assert not module.scan(root,allow,patterns)['pass'];other.unlink()
  results.append({'path':row['path'],'context_sha256':row['context_sha256'],'exact_pass':True,'removed_reject':True,'altered_reject':True,'different_path_reject':True})
(owner/'artifacts/context-controls.json').write_text(json.dumps({'passed':True,'contexts':results},indent=2)+'\n')
print('PASS',len(rows),'exact contexts and',3*len(rows),'negative controls')

"""Seal current owned record bytes and verify retained command streams, without replay."""
import hashlib,json,pathlib,subprocess
A=pathlib.Path(__file__).resolve().parents[1];R=A.parents[2];rows=[];verified=[]
def sha(b):return hashlib.sha256(b).hexdigest()
for receipt in sorted(A.rglob('receipt.json')):
 x=json.loads(receipt.read_text())
 for s in ['stdout','stderr']:
  assert sha((receipt.parent/s).read_bytes())==x[s+'_sha256'],str(receipt)
 verified.append({'receipt':str(receipt.relative_to(A)),'rc':x['rc'],'sha256':sha(receipt.read_bytes())})
paths=set()
for argv in [('git','diff','--name-only','-z','8710a6210a40de0110244d03a886161ee06faf29'),('git','ls-files','--others','--exclude-standard','-z')]:paths.update(x.decode() for x in subprocess.check_output(argv,cwd=R).split(b'\0') if x)
for path in sorted(paths):
 p=R/path;assert p.is_file() and not p.is_symlink();b=p.read_bytes();rows.append({'path':path,'sha256':sha(b),'bytes':len(b)})
x={'files':rows,'receipts_verified':verified,'qualification':'Pre-seal snapshot excludes this newly produced manifest and its outer receipt. Final published-tree observation covers committed bytes externally. Historical inputs/failed program versions preserved; no command replay.'};p=A/'stage-d/sealed-manifest.json';assert not p.exists();p.write_text(json.dumps(x,indent=2,sort_keys=True)+'\n');print('PASS retained stream integrity:',len(verified),'receipts;',len(rows),'new record paths sealed')

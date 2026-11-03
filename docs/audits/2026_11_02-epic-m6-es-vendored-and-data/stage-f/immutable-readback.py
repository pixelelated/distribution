from pathlib import Path
import json,hashlib,subprocess,datetime,sys
R=Path('/workspace/repos/pixelelated/distribution.worktrees/m6-es-vendored-and-data-691')
A='docs/audits/2026_11_02-epic-m6-es-vendored-and-data'
D='923dd5371ded83fa965449a83f7a16d15a174772'
def sha(b):return hashlib.sha256(b).hexdigest()
def git(*args):return subprocess.check_output(['git',*args],cwd=R)
tip=git('rev-parse','HEAD').decode().strip()
def readtree(ref):
 rows=[]
 p=subprocess.Popen(['git','cat-file','--batch'],cwd=R,stdin=subprocess.PIPE,stdout=subprocess.PIPE)
 for row in git('ls-tree','-r','-z',ref,'--',A).split(b'\0'):
  if not row:continue
  meta,name=row.split(b'\t');mode,kind,oid=meta.decode().split();assert kind=='blob'
  p.stdin.write(oid.encode()+b'\n');p.stdin.flush();header=p.stdout.readline().decode().split();b=p.stdout.read(int(header[2]));assert p.stdout.read(1)==b'\n'
  rows.append({'path':name.decode(),'mode':mode,'oid':oid,'bytes':len(b),'sha256':sha(b)})
 p.stdin.close();assert p.wait()==0
 return rows
d=readtree(D);current=readtree(tip);lookup={x['path']:x for x in current};editable=json.loads((R/A/'stage-e/allowlist.json').read_text())['editable']
assert len(d)==274
for x in d:
 if x['path'] not in editable:assert lookup[x['path']]==x,x['path']
manifestpath=A+'/stage-d/payload-manifest.json';manifest=git('show',D+':'+manifestpath)
assert sha(manifest)=='67b7001b027e7ffbaa9afa840b0554bb391de2c07459d33808119bc1c5d08509'
m=json.loads(manifest)['files'];assert len(m)==273
dm={x['path'][len(A)+1:]:x for x in d}
assert set(m)==set(dm)-{'stage-d/payload-manifest.json'}
for name,value in m.items():assert all(dm[name][k]==value[k] for k in ('bytes','sha256')),name
out={'result':'PASS','observed_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'tip':tip,'accepted_d':D,'D_artifact_count':len(d),'preserved_D_noneditable':268,'editable_narratives':editable,'D_payload_manifest_sha256':sha(manifest),'D_artifacts':d,'current_audit_records':current,'limits':'Immutable artifact reconciliation only. Does not execute an accepted producer, regenerate tables, rerun tests or infer a combined ES source. Current list covers this observed commit; later publication carries a separate exact-final list.'}
Path(sys.argv[1]).write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({'result':'PASS','tip':tip,'D_artifacts':len(d),'noneditable_preserved':268,'current_records':len(current),'output_sha256':sha(Path(sys.argv[1]).read_bytes())}))

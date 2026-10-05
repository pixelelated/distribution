from pathlib import Path
import datetime,hashlib,json,sys
root=Path('/workspace/tmp/pixelelated-m7-ui-14/artifacts');receipt=Path('/tmp/pixelelated-ui14-reviewed.json');batch=Path('/tmp/pixelelated-ui14-review-batch.json')
prior=json.loads(receipt.read_text()) if receipt.exists() else []
if sys.argv[1]=='next':
 seen={r['path'] for r in prior};rows=[]
 for p in sorted(root.rglob('*.png')):
  if p.relative_to(root).parts[0].startswith('boot-') or str(p) in seen:continue
  rows.append(dict(path=str(p),sha256=hashlib.sha256(p.read_bytes()).hexdigest()))
  if len(rows)==int(sys.argv[2]):break
 batch.write_text(json.dumps(rows,indent=2)+'\n');print(json.dumps(rows))
elif sys.argv[1]=='accept':
 rows=json.loads(batch.read_text());assert rows
 for r in rows:
  assert r['path'] not in {x['path'] for x in prior};assert hashlib.sha256(Path(r['path']).read_bytes()).hexdigest()==r['sha256'];r.update(reviewed_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),method='Direct view_image',observation=sys.argv[2],passed=True);prior.append(r)
 receipt.write_text(json.dumps(prior,indent=2)+'\n');batch.unlink();print(json.dumps({'reviewed':len(prior),'accepted_batch':len(rows)}))
else:raise SystemExit('next COUNT or accept OBSERVATION')

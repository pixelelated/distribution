from pathlib import Path
import json,hashlib,zipfile,datetime
owner=Path('/tmp/pixelelated-cleanup-runtime-02')
assert json.loads((owner/'completion.json').read_text())['job_rc']==0
store=Path('/workspace/artifacts/pixelelated-build-custody/issue-456-runtime-02')
prior=json.loads(Path('/workspace/tmp/pixelelated-m7-inventory-02/source-inventory-qualified.json').read_text())
rclone=next(r for r in prior['records'] if r['package']=='rclone');arc=Path(rclone['recovered_archive_path']);arcsha=hashlib.sha256(arc.read_bytes()).hexdigest();assert arcsha==rclone['recovered_archive_sha256']
with zipfile.ZipFile(arc) as z:
 names=[n for n in z.namelist() if n.endswith('/rclone')];assert len(names)==1
 binarysha=hashlib.sha256(z.read(names[0])).hexdigest()
rows=[]
for n in ['03','05','06','07','08']:
 inputs=Path('/workspace/tmp/pixelelated-m7-replacement-'+n+'/inputs.json');m=json.loads(inputs.read_text());j=json.loads((owner/('source-inventory-'+n+'.json')).read_text())
 assert not j['errors'] and j['distribution_commit']==m['distribution_commit'] and j['input_manifest_sha256']==hashlib.sha256(inputs.read_bytes()).hexdigest()
 r=next(r for r in j['records'] if r['package']=='rclone');assert r['unpacked_binary_sha256']==binarysha
 r.update(recovered_archive_path=str(arc),recovered_archive_sha256=arcsha,archive_retention='Protected external archive, exact consumed binary match reverified for cleanup custody; do not remove archive with build tree.')
 p=store/('source-inventory-'+n+'-qualified.json');p.write_text(json.dumps(j,indent=2,sort_keys=True)+'\n')
 rows.append({'tree':n,'commit':j['distribution_commit'],'manifest':str(p),'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'source_roots':len(j['records']),'cache_inputs':sum(len(r['cache']) for r in j['records']),'errors':len(j['errors'])})
out={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'source_cache':'/workspace/cache/rocknix-sources','source_cache_must_be_retained':True,'rclone_archive':str(arc),'rclone_archive_sha256':arcsha,'trees':rows,'scope':'Exact matching archives/git inputs and local frozen source manifests; this is cleanup custody, not the complete backed-up release source/licence bundle','deletion_performed':False}
p=owner/'source-custody.json';p.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))

from pathlib import Path
import json,hashlib,zipfile
owner=Path('/workspace/tmp/pixelelated-m7-inventory-12');tree=Path('/workspace/repos/rocknix.worktrees/m7-pixelelated-replacement16');inputs=Path('/workspace/tmp/pixelelated-m7-replacement-16/inputs.json');j=json.loads((owner/'artifacts/source-inventory.json').read_text())
assert not j['errors'] and j['distribution_commit']=='ee014909137e03706e0b3020b8396be589aaa705'
assert j['input_manifest_sha256']==hashlib.sha256(inputs.read_bytes()).hexdigest()
rec=next(r for r in j['records'] if r['package']=='rclone');old=json.loads(Path('/workspace/tmp/pixelelated-m7-inventory-02/source-inventory-qualified.json').read_text());prev=next(r for r in old['records'] if r['package']=='rclone');archive=Path(prev['recovered_archive_path']);digest=hashlib.sha256(archive.read_bytes()).hexdigest();assert digest==prev['recovered_archive_sha256']=='982b5aa772841168f8e380f139e9e787b2a105403e32b94da8676a0e1c0a13ab'
with zipfile.ZipFile(archive) as z:
 names=[n for n in z.namelist() if n.endswith('/rclone')];assert len(names)==1
 assert hashlib.sha256(z.read(names[0])).hexdigest()==rec['unpacked_binary_sha256']
rec.update(recovered_archive_path=str(archive),recovered_archive_sha256=digest,archive_retention='Retained upstream archive verifies against exact replacement16 consumed binary; original cache ZIP is deleted by the recipe.')
proxy=next(r for r in j['records'] if r['package']=='raofflineproxy');assert proxy['unpacked']=='raofflineproxy-879b158995d412af434301ebdae581f66b8b6d57'
assert any(c.get('sha256')=='984957322337d1325f1b0fc11502336a80241ec511fd041c969bb0103c231664' for c in proxy['cache'])
(owner/'artifacts/source-inventory-qualified.json').write_text(json.dumps(j,indent=2,sort_keys=True)+'\n');print('PASS exact replacement16 proxy archive, source inventory and recovered rclone bytes',flush=True)

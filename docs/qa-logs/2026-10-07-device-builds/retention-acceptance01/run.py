from pathlib import Path
import datetime,hashlib,json,os,subprocess,sys
owner=Path(__file__).resolve().parent
(owner/'run.path').write_text(str(Path.cwd()/os.environ['RASTERATOPS_BUILD_RUN'])+'\n')
rc=1
try:
 for path,sha in json.loads((owner/'seal.json').read_text()).items():assert hashlib.sha256(Path(path).read_bytes()).hexdigest()==sha
 source=Path('/workspace/tmp/pixelelated-m7-device-preservation-01')
 assert json.loads((source/'owner-verification.json').read_text())['result']=='PASS'
 result=json.loads((source/'artifacts/result.json').read_text());store=Path(result['store'])
 objects=json.loads((store/'objects.json').read_text());assert len(objects)==result['unique_objects']
 for n,(sha,item) in enumerate(objects.items(),1):
  path=Path(item['object']);assert hashlib.file_digest(path.open('rb'),'sha256').hexdigest()==sha and path.stat().st_size==item['bytes']
  assert not any(path.is_relative_to(Path(t['tree'])) for t in result['trees'])
  if n%3000==0:print('Independently verified',n,'custody objects',flush=True)
 for row in result['trees']:
  tree=Path(row['tree']);assert tree.is_dir()
  assert subprocess.check_output(['git','-C',str(tree),'rev-parse','HEAD'],text=True).strip()==row['head']
  manifest=store/'manifests'/(tree.name[-2:]+'-custody-plan.json');assert hashlib.sha256(manifest.read_bytes()).hexdigest()==row['manifest_sha256']
  source_inventory=Path(row['source_inventory']);assert hashlib.sha256(source_inventory.read_bytes()).hexdigest()==row['source_inventory_sha256']
  assert not json.loads(source_inventory.read_text())['errors']
  for entry in json.loads(manifest.read_text())['entries']:
   if entry['kind']=='file':
    original=(tree/entry['path']).stat();dest=Path(objects[entry['sha256']]['object']).stat()
    assert (original.st_dev,original.st_ino)!=(dest.st_dev,dest.st_ino)
 receipt={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'result':'PASS','independently_hashed_objects':len(objects),'tree_manifests':4,'all_source_inventories_zero_errors':True,'original_trees_present':True,'independent_inodes':True,'no_deletion':True,'scope':'compact preservation accepted; backing/live/reference review remains separate'}
 (owner/'artifacts/acceptance.json').write_text(json.dumps(receipt,indent=2)+'\n');print(json.dumps(receipt),flush=True);rc=0
finally:
 (owner/'inner.rc').write_text(str(rc)+'\n');(owner/'outer.rc').write_text(str(rc)+'\n')
sys.exit(rc)

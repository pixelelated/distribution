#!/usr/bin/env python3
import datetime,hashlib,json,pathlib
R=pathlib.Path(__file__).resolve().parents[1];roots={};archives={};files=[]
def hashfile(p):
 h=hashlib.sha256()
 with open(p,'rb') as f:
  for b in iter(lambda:f.read(4*1024*1024),b''):h.update(b)
 return h.hexdigest()
for folder in ['application','application-overlay']:
 d=R/'stage-b'/folder
 for p in sorted(d.glob('G[0-9][0-9][0-9].json')):
  x=json.loads(p.read_text());files.append({'path':str(p.relative_to(R)),'sha256':hashfile(p)})
  for a in x.get('cache_observations',[]):archives[a['path']]=a['sha256']
  proj=x.get('projection')
  if proj:roots[proj['projection_root']]={'evidence':str(p.relative_to(R)),'role':'needed source members'}
  if x.get('final_prefix_root'):roots[x['final_prefix_root']]={'evidence':str(p.relative_to(R)),'role':'successful prefix'}
  for row in x.get('rows',[]):
   if row.get('candidate_root'):roots[row['candidate_root']]={'evidence':str(p.relative_to(R)),'role':'normal candidate'}
 for p in d.glob('partial-failure-control*.json'):
  x=json.loads(p.read_text());roots[x['projection_root']]={'evidence':str(p.relative_to(R)),'role':'constructed guard fixture'}
actual={p:hashfile(p) for p in archives};assert actual==archives,'cache archive changed'
for root,v in roots.items():
 p=pathlib.Path(root);assert p.is_relative_to('/workspace/tmp/m6-t43') and p.is_dir();v['exists']=True
(R/'stage-d/custody.json').write_text(json.dumps({'at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'source_receipts':files,'owned_receipt_bound_roots':roots,'archive_hashes_before':archives,'archive_hashes_after':actual,'archives_unchanged':True,'retirement':'Not performed at D; only these owned roots may be retired after receipt custody and explicit E–H dispatch. Shared caches and unknown scratch paths are excluded.','execution':'No build/compiler/config/recipe/guest/provider/device/cloud/host-ledger action or permission answer by this lane. Source/record jobs CPUs8–23. No runtime slot requested or allocated.'},indent=2)+'\n')
print('PASS cache bytes unchanged:',len(archives),'archives; receipt-bound retained projection roots:',len(roots))

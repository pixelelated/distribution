from pathlib import Path
import os,time,json,subprocess,hashlib,datetime
out=Path(__file__).parent;roots=[Path(p) for p in ['/workspace/tmp','/workspace/artifacts','/workspace/repos/rocknix.worktrees','/workspace/cache/rocknix-sources']];targets=[Path('/workspace/repos/rocknix.worktrees/m7-pixelelated-replacement'+n) for n in ['03','05','06','07','08']]
errors=[];disks=[];count=0;last=time.monotonic()
for root in roots:
 for base,dirs,files in os.walk(root,followlinks=False,onerror=lambda e:errors.append(str(e))):
  count+=1
  disks.extend(str(Path(base)/n) for n in files if n.endswith('.qcow2'))
  if time.monotonic()-last>10:print('Inspected',count,'directories; found',len(disks),'qcow2 paths',flush=True);last=time.monotonic()
rows=[]
for i,raw in enumerate(disks):
 p=Path(raw);r=subprocess.run(['qemu-img','info','--force-share','--backing-chain','--output=json',str(p)],capture_output=True,text=True,timeout=30)
 row={'path':raw,'rc':r.returncode}
 if r.returncode:row['error']=r.stderr.strip()
 else:
  j=json.loads(r.stdout);row['chain']=j
  row['backing_references_proposed_tree']=[v for x in j for k,v in x.items() if k in ['backing-filename','full-backing-filename'] and any((Path(v) if Path(v).is_absolute() else p.parent/str(v)).resolve().is_relative_to(t) for t in targets)]
  row['disk_inside_proposed_tree']=any(p==t or t in p.parents for t in targets)
 rows.append(row)
 if i%25==0:print('Inspected',i+1,'of',len(disks),'backing chains',flush=True)
container_hits=[];container_count=0
for cid in subprocess.check_output(['docker','ps','-q'],text=True).split():
 j=json.loads(subprocess.check_output(['docker','inspect',cid],text=True))[0];container_count+=1
 for m in j['Mounts']:
  p=Path(m['Source'])
  if any(p==t or p in t.parents or t in p.parents for t in targets):container_hits.append({'id':cid,'source':str(p),'destination':m['Destination']})
report={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'roots':list(map(str,roots)),'excluded_subdirectories':[],'followed_directory_symlinks':False,'directories':count,'discovery_errors':errors,'records':rows,'containers':container_count,'container_matches':container_hits,'scope':'All qcow2-suffixed files under the four project-owned storage roots, including package builds and source caches; symlinked directories are not followed','deletion_performed':False}
p=out/'dependencies.json';p.write_text(json.dumps(report,indent=2)+'\n')
summary={'utc':report['utc'],'report_sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'directories':count,'disks':len(rows),'discovery_errors':len(errors),'qemu_errors':sum(r['rc']!=0 for r in rows),'backing_matches':sum(bool(r.get('backing_references_proposed_tree')) for r in rows),'disks_inside_proposed_trees':sum(r.get('disk_inside_proposed_tree',False) for r in rows),'container_matches':len(container_hits),'root_process_check':'requires separate interactive sudo readback','deletion_performed':False}
(out/'summary.json').write_text(json.dumps(summary,indent=2)+'\n');print(json.dumps(summary),flush=True)
assert not errors and not any(r['rc'] for r in rows) and not any(r.get('backing_references_proposed_tree') for r in rows) and not container_hits

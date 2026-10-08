#!/usr/bin/env python3
"""Map the already sealed five profiles to retained inputs; no licence clearance."""
from pathlib import Path
import collections,datetime,hashlib,json,tarfile
HERE=Path(__file__).resolve().parent
REPO=HERE.parents[3]
BASE=REPO/'docs/qa-logs/2026-10-08-final-inventory/profiles'
A=Path('/workspace/artifacts/pixelelated-release-sources/m7-archives-a7022b76da76a9f6771bb7693d6f6e25854c6731db0750bb46dde29f14d49fce')
G=Path('/workspace/artifacts/pixelelated-release-sources/m7-git-266c8393884189dec9419628b3e7e527b965598d7b9b31e4ea31fd9af2204dc9')
S=Path('/workspace/artifacts/pixelelated-build-inputs/m7-final-supplement/d61541b1d2aa7cac7b3f5dfc0197e846c0da359d2f60d48770ff0f8156758051')
sha=lambda b:hashlib.sha256(b).hexdigest()
AM=json.loads((A/'manifest.json').read_text());GM=json.loads((G/'manifest.json').read_text());SM=json.loads((S/'manifest.json').read_text())
for p in (A,G,S):assert sha((p/'manifest.json').read_bytes())==p.name.split('-')[-1]
profiles={p.parent.name:json.loads(p.read_text()) for p in BASE.glob('*/publication-worklist.json')};assert len(profiles)==5
roots={};dist={}
for d in AM['distribution_trees']:
 p=A/d['member'];assert sha(p.read_bytes())==d['sha256']
 with tarfile.open(p) as tar:roots[d['distribution_commit']]={m.name:sha(tar.extractfile(m).read()) for m in tar if m.isfile()}
 dist[d['distribution_commit']]=d
edges=collections.defaultdict(list)
for e in GM['submodule_edges']:edges[e['parent_commit']].append(e['commit'])
def closure(commit):
 todo=[commit];seen=set()
 while todo:
  c=todo.pop()
  if c in seen:continue
  assert c in GM['snapshots'];seen.add(c);todo.extend(edges[c])
 return sorted(seen)
records=[];rowmap={};shared={};hist=collections.Counter()
for profile,doc in sorted(profiles.items()):
 commit=doc['distribution_commit'];files=roots[commit]
 for row in doc['components']:
  name=row['component'];recipe=row['recipe'];assert files[recipe]==row['recipe_sha256']
  prefix=str(Path(recipe).parent)+'/'
  local={p:h for p,h in files.items() if p.startswith(prefix)}
  for inherited in row['recipe_inheritance']:assert files[inherited['path']]==inherited['sha256']
  rec={'profile':profile,'component':name,'distribution_commit':commit,'profile_worklist_sha256':sha((BASE/profile/'publication-worklist.json').read_bytes()),'recipe':recipe,'recipe_sha256':row['recipe_sha256'],'recipe_declared_license':row['recipe_metadata'].get('PKG_LICENSE'),'image_install_stamp':row['image_install_stamp'],'distribution_member':dist[commit]['member'],'distribution_member_sha256':dist[commit]['sha256'],'local_recipe_directory_files':local,'inherited_recipes':row['recipe_inheritance'],'input_members':[],'component_references':[],'source_disposition':row['source_disposition'],'licence_disposition':'HOLD: recipe declaration is metadata; assess notices, vendored/static use and special inputs before publication.'}
  u=row.get('unpacked_source') or {};cache=u.get('cache',[])
  for c in cache:
   if 'git_head' in c:
    key=name+'/'+c['name'];assert GM['root_inputs'][key]==c['git_head'];commits=closure(c['git_head'])
    rec['input_members'].append({'custody':'git','root_input':key,'root_commit':c['git_head'],'recursive_snapshots':[{'commit':co,**GM['snapshots'][co]} for co in commits],'extra_cache_members':[{'member':e['archive_member'],'sha256':e['sha256']} for e in GM['extra_source_cache_content'] if Path(e['source_cache']).is_relative_to(Path('/workspace/cache/rocknix-sources')/key)]})
   else:
    h=c['sha256'];assert h in AM['archives'] and (A/'archives'/h).stat().st_size==AM['archives'][h]['bytes'];rec['input_members'].append({'custody':'archives','member':'archives/'+h,'sha256':h,'original_name':c['name']})
  if u.get('source_packages'):
   shared[(profile,name)]=list(u['source_packages']);rec['component_references']=[profile+':'+x for x in u['source_packages']]
  if name=='lib32':
   target=profile.rsplit('-',1)[0]+'-arm';assert target in profiles;rec['component_references']=[target+':*'];rec['source_disposition']+='; every companion ARM component is mapped in this index'
  if name=='rclone':
   fn='rclone-v1.75.1-linux-'+('amd64' if profile=='vm18-x86_64' else 'arm64')+'.zip';assert fn in SM['files'];rec['input_members'].append({'custody':'supplement','member':fn,**SM['files'][fn],'kind':'prebuilt binary archive; not corresponding source'})
  if name=='idtech-lr':
   fn=u['downloaded_asset']['sha256']+'-doom.tar.gz';assert fn in SM['files'];rec['input_members'].append({'custody':'supplement','member':fn,**SM['files'][fn],'kind':'shareware data archive; provenance/redistribution disposition open'})
  if not cache and name not in ('rclone','idtech-lr','lib32') and not rec['component_references']:
   assert row['source_disposition'].startswith(('local metapackage/','local/generated package;','local helper source/')), (profile,name,row['source_disposition'])
  assert local
  rowmap[(profile,name)]=rec;records.append(rec);hist[profile]+=1
for (profile,name),targets in shared.items():
 for target in targets:assert (profile,target) in rowmap,(profile,name,target)
assert len(records)==2327
result={'schema':1,'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'result':'PASS_INVENTORIED_INPUT_MEMBER_MAPPING','scope':'Maps the existing five qualified component profiles to retained inputs and frozen local recipes. Does not prove all dynamic downloads, complete licences, publication source, independent off-host retrieval or backup. No missing install stamp is treated as a build-only exclusion.','custodies':{n:{'path':str(p),'manifest_sha256':sha((p/'manifest.json').read_bytes())} for n,p in [('archives',A),('git',G),('supplement',S)]},'counts':dict(hist),'component_profile_rows':len(records),'unique_component_names':len({r['component'] for r in records}),'publication_bundle_complete':False,'components':records}
(HERE/'component-member-index.json').write_text(json.dumps(result,sort_keys=True,indent=2)+'\n')
print(json.dumps({k:result[k] for k in ('result','counts','component_profile_rows','unique_component_names','publication_bundle_complete')},indent=2))

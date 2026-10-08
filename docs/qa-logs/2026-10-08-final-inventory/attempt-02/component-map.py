#!/usr/bin/env python3
"""Map the consumed-source record and actual installation stamps to recipes.

This is build evidence and a publication work list, not a legal assessment or
proof that corresponding-source release archives have been published.
"""
import argparse,json,hashlib,re
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('--tree',type=Path,required=True);p.add_argument('--inputs',type=Path,required=True);p.add_argument('--inventory',type=Path,required=True);p.add_argument('--output',type=Path,required=True);a=p.parse_args()
inputs=json.loads(a.inputs.read_text());inventory=json.loads(a.inventory.read_text());b=a.tree/inputs['build_root'];canonical=Path(inputs['container_worktree'])
assert not inventory['errors']
assert all(r.get('provenance') for r in inventory['records'])
def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def cache(path):
 d={}
 for line in path.read_text().splitlines():
  folder=Path(line.removesuffix('@?+?@'));name=folder.name
  assert name not in d,name
  d[name]=str(folder.relative_to(canonical)/'package.mk')
 return d
recipes=cache(b/'.cache_package_global');recipes.update(cache(b/'.cache_package_local'))
records={x['package']:x for x in inventory['records']};installed={x.name for x in (b/'image/.stamps').iterdir() if (x/'install_target').exists()}
def metadata(path,seen=None):
 seen=set() if seen is None else seen
 assert path not in seen,path
 seen.add(path);values={};chain=[]
 text=(a.tree/path).read_text();assert sha(a.tree/path)==inputs['source_files'][path]
 for line in text.splitlines():
  include=re.match(r'^\. \$\{ROOT\}/(.*package\.mk)$',line)
  if include:
   inherited,parents=metadata(include[1],seen.copy());values.update(inherited);chain+=parents
  match=re.match(r'^(PKG_LICENSE|PKG_TOOLCHAIN|PKG_SECTION|PKG_SITE|PKG_URL)=[\"\']([^\"\'\n]*)[\"\']',line)
  if match:values[match[1]]=match[2]
 chain.append({'path':path,'sha256':sha(a.tree/path)})
 return values,chain
rows=[];missing=[]
for name in sorted(set(records)|installed):
 path=recipes[name];text=(a.tree/path).read_text();assert sha(a.tree/path)==inputs['source_files'][path]
 values,chain=metadata(path)
 rec=records.get(name)
 if rec:provenance=rec['provenance']
 else:
  assert values.get('PKG_SECTION')=='virtual' or name=='debug',name
  provenance='local metapackage/build recipe; no separately unpacked component root'
 if not values.get('PKG_LICENSE'):missing.append(name)
 rows.append({'component':name,'recipe':path,'recipe_sha256':sha(a.tree/path),'recipe_metadata':values,'recipe_inheritance':chain,'image_install_stamp':name in installed,'unpacked_source':rec,'source_disposition':provenance,'publication_disposition':'HOLD: preserve consumed archives/git trees, fork patches/build scripts and applicable notices in the P5 corresponding-source/component bundle; verify retrieval before publication' if name in installed else 'build-only dependency: retain with reproducibility inputs; not counted as an installed runtime package'})
report={'distribution_commit':inputs['distribution_commit'],'input_manifest_sha256':sha(a.inputs),'consumed_inventory_sha256':sha(a.inventory),'components':rows,'counts':{'mapped_components':len(rows),'unpacked_roots':len(records),'image_install_stamps':len(installed),'local_meta_packages':len(installed-set(records))},'missing_recipe_license':missing,'publication_bundle_complete':False}
a.output.write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({'counts':report['counts'],'missing_recipe_license':missing,'publication_bundle_complete':False}))

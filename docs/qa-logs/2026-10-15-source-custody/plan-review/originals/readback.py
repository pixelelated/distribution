from pathlib import Path
import ast,difflib,hashlib,json,re,subprocess,tarfile
P=Path('/tmp/pix-m7-source-custody-refresh-20261015');R=Path('/workspace/repos/rocknix.worktrees/m7-player-setup');D=R/'docs/qa-logs/2026-10-15-source-custody/plan'
def h(b):return hashlib.sha256(b).hexdigest()
def j(p):return json.loads(p.read_text())
def git(*args):return subprocess.check_output(['git','-C',str(R),*args])
assert h((P/'SHA256SUMS').read_bytes())=='f345980a2e20c305b770e686b5c6ff4aa915cfae78c8778981bc6a48713a951d'
sealed={}
for line in (P/'SHA256SUMS').read_text().splitlines():
 sha,name=line.split('  ',1);assert h((P/name).read_bytes())==sha;sealed[name]=sha
assert len(sealed)==124
archive=D/'source-proposal.tar.gz';assert h(archive.read_bytes())=='719cc2809abeff8509b2fd1142c073457fed4d59e170f344b5cfb22156aa83f1'
with tarfile.open(archive) as tf:
 files=[m for m in tf.getmembers() if m.isfile()]
 assert len(files)==125 and len({m.name for m in files})==125
 for m in files:
  name=str(Path(m.name).relative_to('source-packet'));assert tf.extractfile(m).read()==(P/name).read_bytes()
refs=j(P/'reference-index.json')
for r in refs:
 assert h((P/r['member']).read_bytes())==r['sha256']==h(Path(r['original']).read_bytes())
assert len(refs)==21
d=j(P/'product-delta.json')
for old in d['historical_sources']:
 names=git('diff','--name-only',old,d['source'],'--',*d['scope']).decode().splitlines()
 assert sorted(names)==sorted(x['path'] for x in d['paths'])
assert len(d['paths'])==73
changes=[]
for row in d['paths']:
 current=git('show',d['source']+':'+row['path']) if row['current'] else None
 if current is not None:assert h(current)==row['current']['sha256']==h((P/'source-f863'/row['path']).read_bytes())
 olds={}
 for old,meta in row['historical'].items():
  before=git('show',old+':'+row['path']) if meta else None
  if before is not None:assert h(before)==meta['sha256']
  olds[old]=before
 if row['path'].endswith('package.mk'):
  pat=rb'^PKG_VERSION=.*$';after=re.findall(pat,current or b'',re.M)
  previous={old:re.findall(pat,raw or b'',re.M) for old,raw in olds.items()}
  if any(v!=after for v in previous.values()):changes.append(row['path'])
assert sorted(changes)==sorted(x['path'] for x in d['changed_version_declarations']) and len(changes)==4
recipes=j(P/'current-component-recipes.json')
for r in recipes.values():assert h(git('show',d['source']+':'+r['recipe']))==r['sha256']==h((P/'source-f863'/r['recipe']).read_bytes())
for r in j(P/'component-source-delta.json')['complete_selected_package_directory_manifest']:
 assert h(git('cat-file','blob',r['git_blob']))==r['sha256']
helper_hashes={}
for n in ['source-inventory.py','component-map.py']:
 old=(P/'references/collectors'/n).read_text();new=(P/'collectors'/n).read_text()
 a=ast.parse(old);b=ast.parse(new)
 def funcs(tree):return {x.name:ast.dump(x,include_attributes=False) for x in tree.body if isinstance(x,(ast.FunctionDef,ast.AsyncFunctionDef))}
 assert funcs(a)==funcs(b)
 helper_hashes[n]={'historical':h(old.encode()),'candidate':h(new.encode())}
 assert (Path('/tmp/pix-m7-final-inventory-review-20261015/templates')/n).read_bytes()==new.encode()
assert (R/'docs/qa-logs/2026-10-08-final-inventory/attempt-03/source-inventory.py').read_bytes()==(P/'references/collectors/source-inventory.py').read_bytes()
projection=j(P/'historical-member-projection.json');assert h(Path(projection['original']).read_bytes())==projection['sha256']
original=j(Path(projection['original']));notice=j(P/'notice-provenance-worklist.json')
assert len(notice['components'])==18 and all(r['publication_clearance'] is False for r in notice['components'])
vm=j(P/'references/vm-build-inputs.json');vi=j(P/'references/vm-artifact-inputs.json');vr=j(P/'references/vm-artifact-result.json')
assert vi['build_inputs_sha256']==h((P/'references/vm-build-inputs.json').read_bytes())
assert 'source_cache' not in vm and len(vm['product_sha256'])==6
assert vi['build_closeout']==vr['build_closeout'] and vi['build_closeout']['qualification'] is False and vi['build_closeout']['original_launcher_returncode'] is None
result={'status':'PASS_FINITE_SOURCE_AND_ARCHIVED_RECORD_READBACK_ONLY','proposal_seal_sha256':h((P/'SHA256SUMS').read_bytes()),'archived_original_regular_files':len(files),'original_references_exact':len(refs),'historical_bases':len(d['historical_sources']),'product_paths':len(d['paths']),'changed_version_declarations':changes,'current_recipe_records':len(recipes),'selected_package_directory_blobs':len(j(P/'component-source-delta.json')['complete_selected_package_directory_manifest']),'collector_hashes':helper_hashes,'unchanged_helper_function_AST':True,'candidate_collectors_equal_new_binding_draft':True,'notice_rows':18,'historical_member_map_hash_exact':True,'vm_original_schema_and_nonqualified_closeout_exact':True,'collector_or_preparer_executed':False,'cache_traversal':False,'network':False,'runtime':False,'scope':'Source diff and supplied immutable evidence only. No current cache/manifest membership or publication clearance inferred.'}
(Path(__file__).parent/'readback.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))

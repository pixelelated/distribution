from pathlib import Path
import datetime,hashlib,json,shutil,subprocess
R=Path('/workspace/repos/rocknix.worktrees/conflict-resolution'); D=R/'docs/qa-logs/2026-10-08-source-custody/git-complete';D.mkdir()
O=Path('/workspace/tmp/pixelelated-m7-source-git-03');run=Path((O/'run.path').read_text().strip())
for name in ('inner.rc','outer.rc','tool-wrapper.rc','launcher-result.json','launcher-pid.json','launcher-start.json','launcher-submission.json','run.path','run.py','script-sha256.json','console.log','owner-consumption.json'):
 shutil.copy2(O/name,D/name)
(D/'run').mkdir()
for name in ('build.rc','build.status','build.pid','watcher.pid','command.pid','build.log'):
 shutil.copy2(run/name,D/'run'/name)
shutil.copy2(O/'artifacts/result.json',D/'result.json')
result=json.loads((D/'result.json').read_text());cust=Path(result['path']);shutil.copy2(cust/'manifest.json',D/'custody-manifest.json');m=json.loads((D/'custody-manifest.json').read_text())
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
assert sha(D/'custody-manifest.json')==result['manifest_sha256']
B=Path('/workspace/repos/rocknix.worktrees/m7-pixelelated-sm8550-02/build.pixelelated-SM8550.aarch64');A=next((B/'build').glob('azahar-sa-*'));C=A/'.aarch64-rocknix-linux-gnu';P=Path('externals/teakra/src/test_verifier/data/teaklite2_tests_result.bin');cache=C/'CMakeCache.txt';ninja=C/'build.ninja'
flags={l.split(':',1)[0]:l.split('=',1)[1] for l in cache.read_text().splitlines() if l.startswith(('BUILD_TESTING:','ENABLE_TESTS:','TEAKRA_BUILD_TOOLS:','TEAKRA_RUN_TESTS:'))};assert len(flags)==4 and set(flags.values())=={'OFF'}
assert 'teaklite2_tests_result' not in ninja.read_text() and '/test_verifier/' not in ninja.read_text()
pointer=(A/P).read_bytes();assert len(pointer)==134 and b'baffcd4f805a7480d969401792443a34aa39f813b4f0ae49c6365f1d1f3ce120' in pointer
stage=B/'install_pkg'/A.name;assert stage.is_dir();listing=[str(p.relative_to(stage)) for p in stage.rglob('*') if p.is_file() or p.is_symlink()];assert listing and not any('test_verifier' in n or 'teaklite2_tests_result' in n for n in listing)
proof=D/'lfs-proof';proof.mkdir()
source_paths=['CMakeLists.txt','externals/CMakeLists.txt','externals/teakra/CMakeLists.txt','externals/teakra/src/CMakeLists.txt','externals/teakra/src/test_verifier/CMakeLists.txt',str(P)]
records=[]
for rel in source_paths:
 target=proof/rel;target.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(A/rel,target);records.append({'path':rel,'sha256':sha(A/rel)})
recipe=R/'projects/ROCKNIX/packages/emulators/standalone/azahar-sa/package.mk';frozen=Path('/workspace/repos/rocknix.worktrees/m7-pixelelated-sm8550-02')/recipe.relative_to(R);shutil.copy2(frozen,proof/'package.mk')
lfs={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'result':'PASS_UNUSED_TEST_FIXTURE_DISPOSITION','profile':'sm855003-aarch64','azahar_commit':'fbd3fb02f71e5f9ed5134037fd59bad96c7d2b8a','teakra_commit':'3d697a18df504f4677b65129d9ab14c7c597e3eb','pointer_path':str(P),'pointer_sha256':hashlib.sha256(pointer).hexdigest(),'lfs_payload_sha256':'baffcd4f805a7480d969401792443a34aa39f813b4f0ae49c6365f1d1f3ce120','lfs_payload_bytes':357257824,'cache_pointer_bytes':134,'actual_build_flags':flags,'cmake_cache_path':str(cache),'cmake_cache_sha256':sha(cache),'build_ninja_path':str(ninja),'build_ninja_sha256':sha(ninja),'no_test_verifier_or_fixture_build_edge':True,'package_stage':str(stage),'package_stage_files':sorted(listing),'source_files':records,'recipe_sha256':sha(frozen),'disposition':'Pointer retained with exact source. Payload was not present in the accepted build tree, referenced by its generated build graph or installed by this package. Accuracy tests and tools were disabled. No payload download needed to preserve this build; enabling that upstream test later requires its fixture. No general licence/publication conclusion.'}
(D/'lfs-disposition.json').write_text(json.dumps(lfs,indent=2)+'\n')
extras=[]
for x in m['extra_source_cache_content']:
 names=list(x['files']);tops=[]
 for n in names:
  p=Path(x['source_cache'])/n
  for parent in [p.parent,*p.parents]:
   if parent==Path(x['source_cache']):break
   if (parent/'.git').exists():
    if str(parent) not in tops:tops.append(str(parent))
    break
 repos=[]
 for p in tops:
  head=subprocess.check_output(['git','-C',p,'rev-parse','HEAD'],text=True).strip();status=subprocess.check_output(['git','-C',p,'status','--porcelain','--untracked-files=no'],text=True)
  repos.append({'path':p,'head':head,'tracked_status':status})
 extras.append({'source_cache':x['source_cache'],'tracked_parent_commit':x['tracked_commit'],'archive_member':x['archive_member'],'sha256':x['sha256'],'files':len(x['files']),'bytes':sum(v.get('bytes',0) for v in x['files'].values()),'nested_repositories':repos,'disposition':'Separate verified archive retained. Build use and licence remain under #528; directory presence is not proof of consumption.'})
(D/'extra-cache-review.json').write_text(json.dumps(extras,indent=2)+'\n')
print(json.dumps({'retained':str(D),'lfs_result':lfs['result'],'stage_files':len(listing),'extra_cache_groups':len(extras),'nested_repositories':sum(len(e['nested_repositories']) for e in extras)},indent=2))

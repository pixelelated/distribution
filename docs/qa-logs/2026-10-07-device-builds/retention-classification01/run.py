from pathlib import Path
import datetime,hashlib,json,os,subprocess,sys
owner=Path(__file__).resolve().parent
coord=Path('/workspace/repos/rocknix.worktrees/conflict-resolution')
(owner/'run.path').write_text(str(Path.cwd()/os.environ['RASTERATOPS_BUILD_RUN'])+'\n')
rc=1
try:
 for path,sha in json.loads((owner/'seal.json').read_text()).items():assert hashlib.sha256(Path(path).read_bytes()).hexdigest()==sha
 source=Path('/workspace/tmp/pixelelated-m7-device-dependencies-01')
 assert json.loads((source/'owner-verification.json').read_text())['result']=='PASS'
 report=json.loads((source/'artifacts/dependencies.json').read_text())
 assert not report['inventory']['errors'] and not report['artifact_reference_scan_errors']
 assert not report['container_matches'] and not report['inventory']['active']
 candidates=Path('/workspace/artifacts/pixelelated-candidates/sha256')
 bundles=sorted({Path(r['manifest']).parent for r in report['artifact_path_references'] if Path(r['manifest']).is_relative_to(candidates)})
 for b in bundles:
  with (owner/'artifacts'/('bundle-'+b.name+'.log')).open('x') as output:
   subprocess.run(['nice','-n','10','ionice','-c','3','python3','-I',str(owner/'candidate-store.py'),'verify',str(b)],check=True,stdout=output,stderr=subprocess.STDOUT)
  cache=json.loads((b/'cache-ready.json').read_text())
  assert cache['checksum_equal'] is True and cache['independent_regular_files']>0
  print('Verified independent immutable candidate',b.name,flush=True)
 custody=Path('/workspace/artifacts/pixelelated-build-custody/issue-494-device-capacity-01')
 assert json.loads(Path('/workspace/tmp/pixelelated-m7-device-preservation-acceptance-01/artifacts/acceptance.json').read_text())['result']=='PASS'
 plans={n:json.loads((custody/'manifests'/(n+'-custody-plan.json')).read_text()) for n in ['09','10','12','14']}
 entries={n:{e['path']:e for e in p['entries']} for n,p in plans.items()}
 classified=[]
 for row in report['artifact_path_references']:
  p=Path(row['manifest']);key=row['key'];value=Path(row['value'])
  if p.is_relative_to(custody):
   assert key==['tree'] or key==['host_worktree'] or (len(key)==3 and key[0]=='trees' and key[2]=='tree'),row
   reason='original tree identity in verified independent custody metadata'
  else:
   assert p.parent in bundles,row
   if p.name=='manifest.json':assert key==['inputs','host_worktree'];reason='historical build origin; all immutable bundle bytes verified independently'
   elif p.name=='container-actual.json':assert key[:2]==['container','mounts'] and key[-1]=='source';reason='historical mount record; current container inventory has no matches'
   elif p.name.startswith('cache-') or key[0] in ['cache_ready','cache']:
    assert key[-1] in ['old','new'],row
    reason='completed cache-copy origin/destination; checksum-equal independent-file receipt verified'
   elif 'completion' in p.name:
    assert key==['run'] or key[0] in ['result_channels','owned_processes'],row
    tree=next(Path(v['tree']) for v in plans.values() if value.is_relative_to(Path(v['tree'])))
    rel=str(value.relative_to(tree));n=tree.name[-2:]
    assert rel in entries[n] or any(name.startswith(rel+'/') for name in entries[n]),row
    reason='historical completed owner path; referenced file/directory represented in accepted independent custody'
   else:raise AssertionError(row)
  classified.append(dict(row,classification=reason,manifest_sha256=hashlib.sha256(p.read_bytes()).hexdigest()))
 held=[]
 for row in report['external_edges']:
  if row['kind']=='symlink':
   p=Path(row['source']);target=Path(row['target'])
   assert p.is_symlink() and p.resolve()==target
   assert target.is_relative_to(Path(plans['12']['tree']))
   held.append(dict(row,classification='retained QA overlay source dependency; keep replacement12 entirely in this batch'))
  else:assert row['kind']=='cross-store-json' and any(r['manifest']==row['source'] and r['value']==row['target'] for r in classified),row
 assert len(held)==14 and len(classified)==52
 review=json.loads(Path('/workspace/tmp/pixelelated-m7-device-retention-review-01/artifacts/report.json').read_text())
 proposed=[r for r in review['trees'] if not r['tree'].endswith('12')]
 gross=sum(r['allocated_bytes_at_storage_report'] for r in proposed)
 payload={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'result':'ROOT_READBACK_REQUIRED','report_sha256':hashlib.sha256((source/'artifacts/dependencies.json').read_bytes()).hexdigest(),'immutable_bundles_verified':[str(b) for b in bundles],'artifact_references_classified':classified,'held_source_dependencies':held,'proposed_trees':[r['tree'] for r in proposed],'held_tree':plans['12']['tree'],'gross_candidate_bytes':gross,'preservation_store_cost_bytes':59297792,'potential_net_bytes':gross-59297792,'process_unreadable':len(report['process_readback']['unreadable']),'deletion_performed':False,'remaining':'Fresh privileged process readback, measured next-stage capacity, concrete exact removal proposal and explicit approval.'}
 (owner/'artifacts/classification.json').write_text(json.dumps(payload,indent=2)+'\n')
 print(json.dumps({k:v for k,v in payload.items() if k not in ['artifact_references_classified','held_source_dependencies','immutable_bundles_verified']}) ,flush=True)
 rc=0
finally:
 (owner/'inner.rc').write_text(str(rc)+'\n');(owner/'outer.rc').write_text(str(rc)+'\n')
sys.exit(rc)

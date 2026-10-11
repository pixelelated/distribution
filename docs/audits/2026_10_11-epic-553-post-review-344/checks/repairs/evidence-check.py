from pathlib import Path
import hashlib,json,re,datetime
R=Path('/workspace/repos/rocknix.worktrees/m7-component-inputs')
A=R/'docs/audits/2026_10_11-epic-553-post-review-344';P=Path(__file__).resolve().parent
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
load=lambda p:json.loads(p.read_text())
supp=load(A/'checks/adjudication/supplemental-evidence.json')['files']
for f,record in supp.items():
    p=R/f;assert sha(p)==record['sha256'] and p.stat().st_size==record['bytes'],f
assert len(supp)==25
binding=load(R/'docs/qa-logs/2026-10-11-component-inputs/rclone-1.75.2-binding.json')
assert binding['publication_clearance'] is False and len(binding['remaining'])==3
assert sha(R/binding['recipe'])==binding['recipe_sha256']
recipe=(R/binding['recipe']).read_text();assert 'PKG_VERSION="1.75.2"' in recipe
old=binding['prior_disposition'];assert sha(R/old['path'])==old['sha256']
sums=Path(binding['fetched_inputs']['SHA256SUMS']['path']).read_text()
for name,record in binding['fetched_inputs'].items():
    assert sha(Path(record['path']))==record['sha256'],name
    if name!='SHA256SUMS':assert record['sha256'] in sums and record['sha256'] in recipe,name
upgrade=Path('/workspace/tmp/pixelelated-m7-upgrade20')
manifest=load(A/'checks/adjudication/upgrade-prepared-manifest.json')
for f,h in manifest.items():assert sha(upgrade/f)==h,f
assert len(manifest)==8
assert sha(upgrade/'rehearsal.sh')==sha(A/'checks/adjudication/upgrade-rehearsal.sh')
function=lambda t:t.split('wait_for_storage() {',1)[1].split('\n}\n',1)[0]
assert function((upgrade/'rehearsal.sh').read_text())==function((R/'tools/vm-upgrade-rehearsal').read_text())
base=R/'docs/qa-logs/2026-10-11-container-temporary-path'
assert load(base/'pixelelated-m7-build20/launcher-result.json')['runner_returncode']==2
for f in ['inner.rc','outer.rc']:assert (base/'pixelelated-m7-build20'/f).read_text().strip()=='2'
controls=load(base/'pix549-container-tmp01/controls.json')
assert controls['user']=='1000:1000' and '@sha256:' in controls['container']
assert [c['returncode'] for c in controls['cases']]==[1,0]
assert 'No such file or directory' in controls['cases'][0]['stderr']
checks=load(A/'checks/result.json');names=checks['commands'][0]['command'][1:]
recipes=re.findall(r'[^\s]+/package.mk', (A/'checks/pkgcheck.log').read_text())
assert len(names)==13 and len(recipes)==14 and len(set(recipes))==14
modules=[x for x in load(A/'second-opinions/payload-source-manifest.json')['included'] if x['path'].startswith('applied-proxy/')]
frozen=Path('/workspace/repos/rocknix.worktrees/m7-pixelelated-replacement20/build.pixelelated-GENERIC_X64.x86_64/build/raofflineproxy-c7ebd1b6e777f3751ff0ecdf8aba54045844e00d')
roots=[Path('/workspace/tmp/pix541-refresh72/final-patched'),frozen]
for x in modules:
    rel=x['path'].removeprefix('applied-proxy/')
    for root in roots:assert sha(root/rel)==x['sha256'],str(root/rel)
assert len(modules)==10
reports=[R/'docs/qa-logs/2026-10-11-pixelelated-replacement-20/clean-standard-report.md',*R.glob('docs/qa-logs/2026-10-11-pixelelated-replacement-19/standard/*webdav*/report.md'),*R.glob('docs/qa-logs/2026-10-08-pixelelated-replacement-18/qa21/artifacts/rocknix-images/*webdav*/time-to-play/time-to-play.md')]
assert len(reports)==3
for p in reports:
    s=p.read_text();assert "| the exit sync's stamp | - | 1 |" in s and '`?` x1' in s,p
assert 'Outcomes: completed x1.' in reports[0].read_text()
result={'result':'PASS','utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'supplemental_artifacts_rehashed':25,'current_rclone_binding':True,'publication_clearance':False,'upgrade_inputs_rehashed':8,'readiness_function_unchanged':True,'original_build20_results':[2,2,2],'original_container_controls':[1,0],'package_names':13,'recipe_files':14,'applied_proxy_modules_rehashed_against_both_roots':10,'game_to_game_outcome_unobserved_on_all_three_prior_reports':True,'report_hashes':{str(p.relative_to(R)):sha(p) for p in reports}}
(P/'evidence-result.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))

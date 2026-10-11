from pathlib import Path
import json,hashlib,re,subprocess,datetime
p=Path(__file__).resolve().parent;qa=Path('/workspace/tmp/pixelelated-m7-qa20');fix=Path('/workspace/tmp/pix550-551-proof02')
source='1a026648442321609b2288c2c9c06803817f9df2'
def read(path):return json.loads(path.read_text())
def digest(path):return hashlib.sha256(path.read_bytes()).hexdigest()
original=read(qa/'launcher-result.json');assert original['runner_returncode']==1
assert not Path('/proc',str(original['pid'])).exists()
terminal=read(fix/'launcher-result.json');assert terminal['runner_returncode']==0
assert not Path('/proc',str(terminal['pid'])).exists()
steps=read(qa/'result.json');expected=['pair-up','clean-payload','standard','after-defaults','information','sftp','s3','pair-down','webdav-down','sftp-down','s3-down','bundle-after']
assert [x['step'] for x in steps]==expected,steps
assert all(x['returncode']==(1 if x['step']=='standard' else 0) for x in steps),steps
standard=next((qa/'artifacts/rocknix-images').glob('qa-1a02664844-webdav-a-*/report.md'))
rows=re.findall(r'^\| ([a-z-]+) \| ([^|]+) \|',standard.read_text(),re.M)
rows={k:v.strip() for k,v in rows if k!='suite'}
assert len(rows)==15,rows
assert rows.pop('scripts')=='FAIL (1)'
assert all(v=='PASS' for v in rows.values()),rows
scripts=standard.with_name('scripts.log');failures=[x for x in scripts.read_text(errors='replace').splitlines() if x.lstrip().startswith('FAIL ')]
assert len(failures)==7
record=read(Path('/workspace/repos/rocknix.worktrees/m7-component-inputs/docs/qa-logs/2026-10-11-regression-fixtures/original-log.json'))
assert digest(scripts)==record['sha256']
result=read(fix/'result.json');assert result['result']=='PASS' and result['returncode']==0 and result['failures']==0 and result['skips']==0 and result['source']==source
assert result['passes']==1378,result
for f,h in result['tool_sha256'].items():assert digest(Path('/workspace/repos/rocknix.worktrees/m7-component-inputs')/f)==h,f
protocols={}
for backend in ['webdav','sftp','s3']:
 report=next((qa/'artifacts/rocknix-images').glob('qa-1a02664844-'+backend+'-a-*/round-trip.log'))
 text=report.read_text();passes=sum(x.lstrip().startswith('PASS ') for x in text.splitlines())
 assert passes==108,(backend,passes)
 assert not any(x.lstrip().startswith(('FAIL ','SKIP ')) for x in text.splitlines()),backend
 assert text.strip().endswith('PASSED'),backend
 protocols[backend]={'passes':passes,'log_sha256':digest(report)}
frames=read(p/'clean-frame-review.json')['entries'];assert len(frames)==4
for row in frames:
 assert row['status']=='reviewed' and row['source']['distribution']==source and row['source']['overlay'] is False
 f=qa/'artifacts/information/frames'/Path(row['frame']).name
 assert digest(f)==row['sha256']
subprocess.run(['python3','/workspace/tmp/pixelelated-m7-upgrade20/preflight.py'],check=True)
subprocess.run(['python3','/workspace/tmp/pixelelated-m7-build20b/verify-source.py'],check=True)
answer={'result':'PASS','kind':'composed qualification; original QA20 remains FAIL','source':source,'original_launcher_returncode':1,'resolved_original_scripts_failures':7,'corrected_regression':result,'unchanged_original_suites':rows,'protocols':protocols,'reviewed_clean_information_frames':4,'retained_upgrade':'not yet run','utc':datetime.datetime.now(datetime.timezone.utc).isoformat()}
(p/'result.json').write_text(json.dumps(answer,indent=2)+'\n');print('PASS explicit clean qualification composition; original QA20 remains failed',flush=True)

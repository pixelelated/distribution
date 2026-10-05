from pathlib import Path
import datetime,hashlib,json,re,sys
owner=Path(__file__).parent
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
prior=json.loads((owner/'prior-inputs.json').read_text())
for item in ['completion','report']:
 p=Path(prior[item]['path']);assert sha(p)==prior[item]['sha256']
completion=json.loads(Path(prior['completion']['path']).read_text())
assert completion['actual_tool_session']==64718 and completion['actual_tool_rc']==1
assert all(v==1 for v in completion['result_channels'].values()) and completion['qemu_absent']
report=Path(prior['report']['path']).read_text()
rows=re.findall(r'^\| ([a-z-]+) \| (PASS|FAIL \(1\)) \|',report,re.M)
expected={'scripts','lifetime','wrapper','vocabulary','french','quoting','menumap','register','pair-identity','fresh','round-trip','exit','time-to-play','walks'}
assert {name for name,result in rows if result=='PASS'}==expected,rows
assert [(n,r) for n,r in rows if r!='PASS']==[('frame-diff','FAIL (1)')]
assert 'cf511ce79b' in report and '79d560046ee52e28b72f16588168dd7c8fb2637c1cc585713216a8ec828e9d81' in report
for file,key in [('prior-artifacts.json','artifact_manifest_sha256'),('claims.txt','claims_sha256'),('comparison-controls.json','controls_sha256')]:assert sha(owner/file)==prior[key]
for row in json.loads((owner/'prior-artifacts.json').read_text()):assert sha(Path(row['path']))==row['sha256'],row['path']
controls=json.loads((owner/'comparison-controls.json').read_text());assert controls['passed'] and controls['baseline_unchanged'] and controls['candidate_frames_unchanged']
for name,wanted in controls['baseline_manifest'].items():assert sha(Path('/workspace/artifacts/rocknix-images/walk-baseline')/name)==wanted
for name,key in [('tools/frame-diff','engine_sha256'),('tools/vm-walks/masks.txt','masks_sha256')]:assert sha(Path(name))==controls[key]
assert sha(owner/'claims.txt')==controls['claims_sha256']
out={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'passed':True,'original_qa_tool':64718,'original_qa_actual_rc':1,'same_candidate_default_suites':sorted(expected),'comparison_correction_issue':439,'scope':'Fourteen original09 suite passes remain at QA11; corrected comparison and actual upgrade execute in QA13. No QA11 result is rewritten.'}
(owner/'artifacts/prior-suites.json').write_text(json.dumps(out,indent=2)+'\n')
print('PASS verified same-image fourteen-suite evidence and original QA11 failure; corrected comparison remains required',flush=True)

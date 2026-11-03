from prooflib import *
errors=[];facts={}
for c in j(A+'stage-f/scan-controls.json'):
 name=c['name'];prefix=A+'stage-f/fixtures/'+name
 assert sha(blob(prefix+'.json'))==c['fixture_sha256'],name
 assert sha(blob(A+'tools/final-record-scan.py'))==c['reader_sha256'],name
 for stream in ('stdout','stderr'):assert sha(blob(prefix+'.'+stream))==c[stream+'_sha256'],(name,stream)
 assert c['exit']==(0 if name=='scan-positive' else 1)
 if c['expected_refusal']:assert c['expected_refusal'] in blob(prefix+'.stderr').decode()
facts['scan_control_exits']=[1,1,0]
pres=j(A+'stage-d/program-preservation.json')
print('PROGRAM PRESERVATION',json.dumps(pres,indent=2)[:5000])
# Resolve every literal initial binding discrepancy with exact bytes, retaining the preliminary result.
initial=json.loads((P/'reconcile-bindings-results.json').read_text());resolved=[]
for row in initial['errors']:
 detail=row['detail'];path=detail['path'];data=blob(path)
 if path=='.githooks/hooks-test':
  assert sha(data)==detail['expected'];resolved.append({'receipt':detail['receipt'],'resolution':'The preliminary reader excluded .githooks paths; direct immutable read matches the expected hash.','hash':sha(data)})
 elif path==A+'tools/final-confinement.py':
  needle=b"'retirement-owner-scope.py',";assert data.count(needle)==1
  prior=data.replace(needle,b'',1);assert sha(prior)==detail['expected']
  resolved.append({'receipt':detail['receipt'],'qualification':'Exact older source reconstructed in memory by removing the single new-tool allowlist entry. No original-version source file is retained separately; original controls are not claimed against final bytes.','expected_old_sha256':sha(prior),'current_sha256':sha(data)})
 else:errors.append(row)
facts['resolved_initial_binding_reports']=resolved
facts['source_version_qualification']='Four early F confinement/control receipts name45612b79; final guard isb7ee4e57. Exact single-entry inverse reconstructs45612b79. No original control replay or claim that old controls ran current bytes.'
# Preserve14 original program record count without equating it with all18 D-stage helper files.
if isinstance(pres,dict):
 for key,value in pres.items():
  if isinstance(value,(dict,list)):facts['program_preservation_'+key+'_count']=len(value)
facts['accepted_support_report_sha256']=sha((P/'accepted-d-support.txt').read_bytes())
assert facts['accepted_support_report_sha256']=='340e89f5817bd5e9be8316c40c745f9520acf883317abd0976653029df63c349'
facts['brief_sha256']=sha((P/'full-brief.txt').read_bytes())
facts['stream_with_errata_sha256']=sha((P/'full-streams.txt').read_bytes())
(P/'reconcile-supplement-results.json').write_text(json.dumps({'errors':errors,'facts':facts},indent=2)+'\n')
print('SUPPLEMENT',json.dumps({'errors':errors,'facts':facts},indent=2))

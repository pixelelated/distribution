"""Verify retained actual responses; no network or repeated tracker mutation."""
import hashlib,json,pathlib
A=pathlib.Path(__file__).resolve().parents[1];T=A/'stage-d/tracker';expected=json.loads((A/'stage-d/created-issues.json').read_text())
def read(n):return json.loads((T/(n+'.stdout')).read_text())
commands=json.loads((T/'commands.json').read_text())
for c in commands:
 for stream in ['stdout','stderr']:assert hashlib.sha256((T/(c['name']+'.'+stream)).read_bytes()).hexdigest()==c[stream+'_sha256']
audit=read('audit-after');bug=read('bug');bp=read('bug-parent');parent=read('audit-parent');ownerparent=read('slice-parent')
assert parent['number']==693 and ownerparent['number']==1415
assert audit['milestone']['number']==6 and audit['state']=='open'
assert bug['milestone'] is None and bug['state']=='open'
assert commands[-1]['rc']==1 and bp['status']=='404' and bp['message']=='No parent issue found'
assert audit['body']==expected['audit']['body'] and bug['body']==expected['bug']['body']
result={'audit':{'number':1417,'id':audit['id'],'parent':693,'milestone':6,'body_sha256':hashlib.sha256(audit['body'].encode()).hexdigest(),'state':'open'},'bug':{'number':1416,'id':bug['id'],'parent':None,'parent_endpoint_status':404,'parent_endpoint_message':bp['message'],'milestone':None,'body_sha256':hashlib.sha256(bug['body'].encode()).hexdigest(),'state':'open'},'slice_parent':1415,'exact_body_readback':True,'erratum':'Original tracker helper expected generic Not Found. Actual endpoint returns No parent issue found; old failed assertion and all responses preserved. No mutation/read replay required.'}
p=A/'stage-d/tracker-verified.json'
if p.exists():raise SystemExit('refuse overwrite')
p.write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result));print('PASS exact retained tracker bodies, linkage and explicit no-parent response')

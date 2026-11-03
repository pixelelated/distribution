import datetime,hashlib,json,pathlib,subprocess
A=pathlib.Path(__file__).resolve().parents[1];out=A/'stage-d/tracker';out.mkdir(exist_ok=False);commands=[]
def api(name,path,extra=[]):
 argv=['gh','api',path,*extra];start=datetime.datetime.now(datetime.timezone.utc).isoformat();p=subprocess.run(argv,capture_output=True);end=datetime.datetime.now(datetime.timezone.utc).isoformat();(out/(name+'.stdout')).write_bytes(p.stdout);(out/(name+'.stderr')).write_bytes(p.stderr);r={'name':name,'argv':argv,'cwd':str(pathlib.Path.cwd()),'start':start,'end':end,'rc':p.returncode,'stdout_sha256':hashlib.sha256(p.stdout).hexdigest(),'stderr_sha256':hashlib.sha256(p.stderr).hexdigest()};commands.append(r);(out/'commands.json').write_text(json.dumps(commands,indent=2)+'\n');return p.returncode,json.loads(p.stdout) if p.stdout else {}
base='repos/pixelelated/distribution/issues/'
rc,audit=api('audit-before',base+'1417');assert rc==0
rc,linked=api('attach-audit-to-693',base+'693/sub_issues',['--method','POST','-F','sub_issue_id='+str(audit['id'])]);assert rc==0
rc,parent=api('audit-parent',base+'1417/parent');assert rc==0 and parent['number']==693
rc,ownerparent=api('slice-parent',base+'693/parent');assert rc==0 and ownerparent['number']==1415
rc,audit=api('audit-after',base+'1417');assert rc==0 and audit['milestone']['number']==6 and audit['state']=='open'
rc,bug=api('bug',base+'1416');assert rc==0 and bug['milestone'] is None and bug['state']=='open'
rc,bp=api('bug-parent',base+'1416/parent');assert rc!=0 and bp.get('status')=='404' and bp.get('message')=='Not Found'
expected=json.loads((A/'stage-d/created-issues.json').read_text())
assert audit['body']==expected['audit']['body'] and bug['body']==expected['bug']['body']
result={'audit':{'number':1417,'id':audit['id'],'parent':parent['number'],'milestone':audit['milestone']['number'],'body_sha256':hashlib.sha256(audit['body'].encode()).hexdigest(),'state':audit['state']},'bug':{'number':1416,'id':bug['id'],'parent':None,'parent_endpoint_status':404,'milestone':None,'body_sha256':hashlib.sha256(bug['body'].encode()).hexdigest(),'state':bug['state']},'slice_parent':ownerparent['number'],'exact_body_readback':True}
(out/'summary.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result));print('PASS actual audit parent693/M6; reactive bug no parent/milestone; exact bodies')

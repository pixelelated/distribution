import base64,datetime,hashlib,json,pathlib,re,subprocess
A=pathlib.Path(__file__).resolve().parents[1];out=A/'stage-f/live-readback';out.mkdir(exist_ok=False);expected=json.loads((A/'stage-f/expected-issues.json').read_text());commands=[]
def sha(b):return hashlib.sha256(b).hexdigest()
def api(name,path):
 argv=['gh','api',path];start=datetime.datetime.now(datetime.timezone.utc).isoformat();p=subprocess.run(argv,capture_output=True);end=datetime.datetime.now(datetime.timezone.utc).isoformat();commands.append({'argv':argv,'cwd':str(pathlib.Path.cwd()),'start':start,'end':end,'rc':p.returncode,'stdout_sha256':sha(p.stdout),'stderr_sha256':sha(p.stderr),'stdout_base64':base64.b64encode(p.stdout).decode(),'stderr_base64':base64.b64encode(p.stderr).decode()});(out/'commands.json').write_text(json.dumps(commands,indent=2)+'\n');return p.returncode,json.loads(p.stdout)
base='repos/pixelelated/distribution/issues/';rows=[]
for number,key,count in [(1417,'auditExpected',1),(1416,'bugExpected',2)]:
 rc,x=api(str(number),base+str(number));assert rc==0 and x['body']==expected[key] and x['state']=='open';ticks=re.findall(r'^- \[([ xX])\]',x['body'],re.M);assert len(ticks)==count and all(t.lower()=='x' for t in ticks);rc,parent=api(str(number)+'-parent',base+str(number)+'/parent')
 if number==1417:assert rc==0 and parent['number']==693 and x['milestone']['number']==6;owner=693
 else:assert rc==1 and parent['status']=='404' and parent['message']=='No parent issue found' and x['milestone'] is None;owner=None
 rows.append({'number':number,'state':x['state'],'parent':owner,'milestone':6 if number==1417 else None,'checked':count,'unchecked':0,'body_sha256':sha(x['body'].encode()),'body':x['body']})
rc,owner=api('693',base+'693');assert rc==0;ticks=re.findall(r'^- \[([ xX])\]',owner['body'],re.M);assert len(ticks)==18 and all(t==' ' for t in ticks)
(out/'issues.json').write_text(json.dumps(rows,indent=2)+'\n');(out/'summary.json').write_text(json.dumps({'issues':[{k:v for k,v in x.items() if k!='body'} for x in rows],'slice_693_unchecked':18,'slice_body_sha256':sha(owner['body'].encode()),'slice_not_edited':True},indent=2)+'\n');print('PASS exact1417 one checked/open/M6/parent693;1416 two checked/open/no parent or milestone;693 eighteen unchanged unchecked criteria')

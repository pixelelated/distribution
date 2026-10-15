from pathlib import Path
import concurrent.futures,datetime,hashlib,json,re,subprocess,time
OUT=Path(__file__).parent

def pick(d,keys):return {k:d.get(k) for k in keys if k in d}
def read(label,endpoint,kind):
 start=time.monotonic();utc=datetime.datetime.now(datetime.timezone.utc).isoformat()
 r=subprocess.run(['gh','api','--method','GET','--include',endpoint],capture_output=True,timeout=25)
 # Never retain raw response headers, error streams, authentication material or unselected bodies.
 raw=r.stdout.decode('utf-8','replace');assert len(r.stdout)<2*1024**2
 split=re.split(r'\r?\n\r?\n',raw,maxsplit=1);head=split[0];body=split[1] if len(split)>1 else ''
 status=re.search(r'^HTTP/\S+\s+(\d+)',head,re.M)
 status=int(status[1]) if status else None
 try:d=json.loads(body)
 except ValueError:d={}
 receipt={'endpoint':endpoint,'method':'GET','observed_utc':utc,'exit_code':r.returncode,'http_status':status,'elapsed_seconds':round(time.monotonic()-start,6),'raw_response_retained':False,'response_body_bytes':len(body.encode()),'stderr_bytes':len(r.stderr)}
 allowed_headers={}
 for l in head.splitlines()[1:]:
  if ':' in l:
   k,v=l.split(':',1)
   if k.lower() in ('date','github-authentication-token-expiration'):allowed_headers[k.lower()]=v.strip()
 receipt['allowed_response_headers']=allowed_headers
 if status and status>=400:
  receipt['error']=pick(d,['message','status','documentation_url']);data=None
 elif r.returncode:
  receipt['error']={'category':'transport-or-cli-failure','raw_error_omitted':True};data=None
 elif kind=='issue':
  lines=d.get('body','').splitlines();chosen=set()
  for i,l in enumerate(lines):
   if any(t in l.lower() for t in ['permission','expir','runner','security','blitterbot','bot account','disabled-runner']):chosen.update(range(max(0,i-1),min(len(lines),i+3)))
  data=pick(d,['number','title','state','updated_at','html_url']);data['selected_body_lines']=[{'line':i+1,'text':lines[i]} for i in sorted(chosen)];data['body_sha256']=hashlib.sha256(d.get('body','').encode()).hexdigest()
 elif kind=='user':data=pick(d,['login','id','type'])
 elif kind=='repo':data=pick(d,['id','full_name','html_url','private','fork','default_branch','archived','permissions']);data['owner']=d.get('owner',{}).get('login')
 elif kind=='actions':data=pick(d,['enabled','allowed_actions','sha_pinning_required'])
 elif kind=='workflow-permissions':data=pick(d,['default_workflow_permissions','can_approve_pull_request_reviews'])
 elif kind=='runners':data={'total_count':d.get('total_count'),'runners':[pick(x,['id','name','os','status','busy','ephemeral']) for x in d.get('runners',[])]}
 elif kind=='branch':data=pick(d,['name','protected']);data['commit']=d.get('commit',{}).get('sha')
 elif kind=='workflows':data={'total_count':d.get('total_count'),'workflows':[pick(x,['id','name','path','state','updated_at','html_url']) for x in d.get('workflows',[])]}
 elif kind=='runs':data={'total_count':d.get('total_count'),'runs':[pick(x,['id','name','event','path','status','conclusion','head_sha','head_branch','html_url','created_at']) for x in d.get('workflow_runs',[])]}
 elif kind=='jobs':data={'total_count':d.get('total_count'),'jobs':[pick(x,['id','name','status','conclusion','labels','runner_name','runner_group_name','html_url']) for x in d.get('jobs',[])]}
 else:raise ValueError(kind)
 result={'receipt':receipt,'data':data};(OUT/(label+'.json')).write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({'label':label,'exit_code':r.returncode,'http_status':status,'available':data is not None}),flush=True);return result
if __name__=='__main__':
 inputs=[('issue-344','repos/pixelelated/distribution/issues/344','issue'),('identity','user','user'),*[(n+'-permissions','repos/pixelelated/'+n,'repo') for n in ['distribution','emulationstation','splash','website']],('actions-permissions','repos/pixelelated/distribution/actions/permissions','actions'),('workflow-permissions','repos/pixelelated/distribution/actions/permissions/workflow','workflow-permissions'),('repository-runners','repos/pixelelated/distribution/actions/runners?per_page=100','runners'),('organization-runners','orgs/pixelelated/actions/runners?per_page=100','runners'),('next-branch','repos/pixelelated/distribution/branches/next','branch'),('workflows','repos/pixelelated/distribution/actions/workflows?per_page=100','workflows'),('recent-runs','repos/pixelelated/distribution/actions/runs?per_page=5','runs')]
 with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:list(pool.map(lambda a:read(*a),inputs))

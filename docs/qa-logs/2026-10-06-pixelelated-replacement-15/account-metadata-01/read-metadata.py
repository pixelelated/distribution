"""Retain only non-secret API identity/repository/permission/expiry metadata."""
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import datetime,json,subprocess
owner=Path('/workspace/tmp/pixelelated-m7-account-metadata-01');assert not owner.exists();owner.mkdir(mode=0o700)
def fetch(endpoint):
 r=subprocess.run(['gh','api','--method','GET','--include',endpoint],text=True,capture_output=True,timeout=25)
 if r.returncode:return {'available':False,'returncode':r.returncode,'error':'API metadata unavailable; response body/headers deliberately omitted'}
 header,body=r.stdout.split('\n\n',1);headers={}
 for row in header.splitlines()[1:]:
  if ':' in row:
   k,v=row.split(':',1)
   if k.lower() in ['x-oauth-scopes','x-accepted-oauth-scopes','github-authentication-token-expiration']:headers[k.lower()]=v.strip()
 return {'available':True,'headers':headers,'data':json.loads(body)}
endpoints=['user','orgs/pixelelated']+['repos/pixelelated/'+r for r in ['distribution','emulationstation','splash']]+['repos/pixelelated/distribution/actions/runs?per_page=10']
with ThreadPoolExecutor(max_workers=6) as pool:raw=dict(zip(endpoints,pool.map(fetch,endpoints)))
identity=raw['user'];assert identity['available'];user={k:identity['data'].get(k) for k in ['login','id','name','type']}
result={'observed_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'identity':user,'token_response_metadata':identity['headers'],'scope':'read-only current authenticated account/API metadata; no token value read or retained','token_inventory_complete':False,'expiry_reminder':'not configured or sent by this proof; requires existing receipt or named authorization'}
assert user['login']=='blitterbot' and user['id']==335883270,user
org=raw['orgs/pixelelated'];result['organization']={'available':org['available']}
if org['available']:result['organization'].update({k:org['data'].get(k) for k in ['login','id','default_repository_permission','members_can_create_repositories']})
repos=[]
for name in ['distribution','emulationstation','splash']:
 item=raw['repos/pixelelated/'+name];assert item['available'],name;data=item['data']
 repos.append({k:data.get(k) for k in ['id','full_name','html_url','private','fork','default_branch','archived','permissions']}|{'owner':data['owner']['login'],'parent':data.get('parent',{}).get('full_name')})
 assert data['full_name']=='pixelelated/'+name
result['repositories']=repos
runs=raw[endpoints[-1]];recent=[];hosted_jobs=[]
if runs['available']:
 for x in runs['data']['workflow_runs']:
  recent.append({k:x.get(k) for k in ['id','name','event','path','status','conclusion','head_sha','html_url','created_at']})
 if recent:
  jobs=fetch('repos/pixelelated/distribution/actions/runs/'+str(recent[0]['id'])+'/jobs?per_page=100')
  if jobs['available']:
   for x in jobs['data']['jobs']:hosted_jobs.append({k:x.get(k) for k in ['id','name','status','conclusion','labels','runner_name','runner_group_name','html_url']})
result['recent_runs']=recent;result['latest_run_jobs']=hosted_jobs
result['workflow_scope']='actual current run/job metadata only; not the historical throwaway-fork scheduling experiment'
(owner/'metadata.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({'owner':str(owner),'login':user['login'],'repositories':[r['full_name'] for r in repos],'response_metadata_fields':list(identity['headers']),'recent_runs':len(recent),'latest_run_jobs':len(hosted_jobs),'scope_inventory_complete':False}))

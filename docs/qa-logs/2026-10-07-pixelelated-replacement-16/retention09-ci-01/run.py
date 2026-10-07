from pathlib import Path
import hashlib,json,os,subprocess,sys
owner=Path(__file__).resolve().parent
(owner/'run.path').write_text(str(Path.cwd()/os.environ['RASTERATOPS_BUILD_RUN'])+'\n')
rc=1
try:
 for name,sha in json.loads((owner/'seal.json').read_text()).items():assert hashlib.sha256(Path(name).read_bytes()).hexdigest()==sha
 results=[]
 for number in [37566862089,37566862118]:
  with (owner/'artifacts'/f'{number}.log').open('x') as out:
   r=subprocess.run(['gh','run','watch',str(number),'--repo','pixelelated/distribution','--interval','15','--exit-status'],stdout=out,stderr=subprocess.STDOUT)
  data=json.loads(subprocess.check_output(['gh','run','view',str(number),'--repo','pixelelated/distribution','--json','headSha,status,conclusion,url,workflowName'],text=True))
  (owner/'artifacts'/f'{number}.json').write_text(json.dumps(data,indent=2)+'\n')
  assert data['headSha']=='510196b072f3bec9c108ef2ad4709e30aaa40bde'
  assert r.returncode==0 and data['status']=='completed' and data['conclusion']=='success',data
  results.append(data);print('PASS '+data['workflowName'],flush=True)
 (owner/'artifacts/result.json').write_text(json.dumps({'result':'PASS','checks':results},indent=2)+'\n')
 rc=0
finally:
 (owner/'inner.rc').write_text(str(rc)+'\n');(owner/'outer.rc').write_text(str(rc)+'\n')
sys.exit(rc)

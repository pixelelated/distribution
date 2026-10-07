from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,os,subprocess,sys
owner=Path(__file__).resolve().parent
(owner/'run.path').write_text(str(Path.cwd()/os.environ['RASTERATOPS_BUILD_RUN'])+'\n')
rc=1
def capacity():
 s=os.statvfs('/workspace')
 return {'utc':datetime.now(timezone.utc).isoformat(),'total_bytes':s.f_blocks*s.f_frsize,'used_bytes':(s.f_blocks-s.f_bfree)*s.f_frsize,'available_bytes':s.f_bavail*s.f_frsize,'reserved_free_bytes':(s.f_bfree-s.f_bavail)*s.f_frsize}
try:
 for path,sha in json.loads((owner/'seal.json').read_text()).items():assert hashlib.sha256(Path(path).read_bytes()).hexdigest()==sha
 (owner/'artifacts/before.json').write_text(json.dumps(capacity(),indent=2)+'\n')
 with (owner/'artifacts/allocated.tsv').open('x') as out,(owner/'artifacts/du-errors.log').open('x') as err:
  result=subprocess.run(['nice','-n','10','ionice','-c','3','du','-x','-B1','--max-depth=3','/workspace'],stdout=out,stderr=err)
 rows=[]
 for line in (owner/'artifacts/allocated.tsv').read_text().splitlines():
  count,path=line.split('\t',1);rows.append({'path':path,'allocated_bytes':int(count)})
 data={'utc':datetime.now(timezone.utc).isoformat(),'du_returncode':result.returncode,'complete_inventory':result.returncode==0,'capacity_after':capacity(),'rows':rows,'scope':'Read-only allocated filesystem usage. Concurrent approved cleanup can change availability during traversal; inspect both timestamps and retained errors.'}
 (owner/'artifacts/report.json').write_text(json.dumps(data,indent=2)+'\n')
 assert result.returncode in [0,1] and rows
 print(json.dumps({'observation_recorded':True,'du_returncode':result.returncode,'rows':len(rows),'complete_inventory':result.returncode==0}),flush=True)
 rc=0
finally:
 (owner/'inner.rc').write_text(str(rc)+'\n');(owner/'outer.rc').write_text(str(rc)+'\n')
sys.exit(rc)

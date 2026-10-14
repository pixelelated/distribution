from pathlib import Path
import subprocess,json,time,resource,hashlib,os
r=Path('/storage/qa574');out=r/'results';out.mkdir();result={'rc':1,'started':time.time(),'stages':[]}
def run(name,args,limit=100):
 start=time.time();p=subprocess.run(args,cwd=r,capture_output=True,timeout=limit);(out/(name+'.stdout')).write_bytes(p.stdout);(out/(name+'.stderr')).write_bytes(p.stderr);row={'name':name,'argv':args,'rc':p.returncode,'seconds':time.time()-start,'max_child_rss_kib':resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss};result['stages'].append(row);print(name,p.returncode,flush=True);assert p.returncode==0 and not p.stderr,row
try:
 run('generate',['python3',str(r/'make-fixtures.py'),'--output',str(r/'cases')])
 run('baseline',['python3',str(r/'run-hash-controls.py'),'--binary',str(r/'baseline-hash'),'--es-source',str(r/'baseline-source'),'--fixtures',str(r/'cases'),'--baseline'])
 run('candidate',['python3',str(r/'run-hash-controls.py'),'--binary',str(r/'candidate-hash'),'--es-source',str(r/'candidate-source'),'--fixtures',str(r/'cases')])
 run('retry',[str(r/'retry-control')]);assert (out/'retry.stdout').read_text().count('PASS')==27
 result['manifest']=json.loads((r/'cases/manifest.json').read_text());result['binary_hashes']={n:hashlib.sha256((r/n).read_bytes()).hexdigest() for n in ['baseline-hash','candidate-hash','retry-control']};result['rc']=0
finally:
 result['ended']=time.time();(out/'result.json').write_text(json.dumps(result,indent=2)+'\n')
raise SystemExit(result['rc'])

from pathlib import Path
import subprocess,json
p=Path(__file__).parent;tasks=[]
for name in ['reverify','inspect']:
 log=(p/'artifacts'/(name+'.log')).open('x')
 child=subprocess.Popen(['/usr/bin/python3','-I',str(p/(name+'.py'))],stdout=log,stderr=subprocess.STDOUT)
 tasks.append((name,child,log))
(p/'child-pids.json').write_text(json.dumps({name:child.pid for name,child,log in tasks})+'\n')
results={}
for name,child,log in tasks:
 rc=child.wait();log.close();results[name]=rc;(p/(name+'.rc')).write_text(str(rc)+'\n')
print(json.dumps(results),flush=True)
raise SystemExit(0 if all(rc==0 for rc in results.values()) else 1)

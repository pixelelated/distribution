from pathlib import Path
import subprocess,json,time,hashlib,tarfile,shlex,datetime,os
r=Path(__file__).parent; repo=Path('/workspace/repos/rocknix.worktrees/m7-player-setup'); packet=repo/'docs/qa-logs/2026-10-13-proxy-memory-feasibility'; guest='/tmp/pix570-proxy'
ssh=json.loads((r/'ssh-command.json').read_text()); records=[]
def command(name,cmd,timeout=90,input=None):
 start=time.monotonic(); p=subprocess.run(ssh+[cmd],input=input,capture_output=True,timeout=timeout)
 (r/(name+'.stdout')).write_bytes(p.stdout);(r/(name+'.stderr')).write_bytes(p.stderr)
 records.append({'name':name,'rc':p.returncode,'elapsed_seconds':time.monotonic()-start});(r/'commands.json').write_text(json.dumps(records,indent=2)+'\n')
 if p.returncode: raise RuntimeError(name+' failed rc='+str(p.returncode))
 return p.stdout
result={'started':datetime.datetime.now(datetime.timezone.utc).isoformat(),'scope':'installed-interpreter bytecode imports and synthetic loopback listener; not full service','packet_commit':'914b0ad56331165cb41b7384b55cbcbbed19d9f2'}
try:
 prep=json.loads((r/'trees/source.json').read_text()); old=json.loads((packet/'source.json').read_text())
 assert prep['baseline']==old['baseline'] and prep['candidate']==old['candidate']
 archive=r/'stage.tar.gz'
 with tarfile.open(archive,'w:gz') as t:
  t.add(r/'trees',arcname='trees');t.add(packet/'fixtures',arcname='fixtures')
 result['archive_sha256']=hashlib.sha256(archive.read_bytes()).hexdigest();result['source_manifest_sha256']=hashlib.sha256((r/'trees/source.json').read_bytes()).hexdigest()
 for p in sorted((packet/'fixtures').glob('*.py')):result.setdefault('fixture_sha256',{})[p.name]=hashlib.sha256(p.read_bytes()).hexdigest()
 print('Staging verified small source trees',flush=True)
 command('stage','test ! -e '+guest+' && mkdir '+guest+' && tar -xz -C '+guest,input=archive.read_bytes())
 preflight='''import sys,hashlib,json,pathlib,socket,subprocess
from pathlib import Path
r=Path('/tmp/pix570-proxy');m=json.loads((r/'trees/source.json').read_text())
for v in ('baseline','candidate'):
 for p,h in m[v].items(): assert hashlib.sha256((r/'trees'/v/p).read_bytes()).hexdigest()==h,p
with socket.socket() as s:s.bind(('127.0.0.1',19080))
active=subprocess.run(['systemctl','is-active','raofflineproxy.service'],capture_output=True,text=True)
assert active.returncode!=0
print(json.dumps({'python':sys.version,'executable':sys.executable,'sha256':hashlib.sha256(Path(sys.executable).read_bytes()).hexdigest(),'boot_id':Path('/proc/sys/kernel/random/boot_id').read_text().strip(),'meminfo':{x.split(':')[0]:x.split(':')[1].strip() for x in Path('/proc/meminfo').read_text().splitlines() if x.startswith(('MemTotal:','MemAvailable:','SwapTotal:'))},'proxy_active':active.stdout.strip(),'source_verified':True,'loopback_port':19080}))
'''
 command('preflight','python3 -B -c '+shlex.quote(preflight))
 print('Running six bytecode-only imports',flush=True)
 base=['env','PYTHONOPTIMIZE=0','MALLOC_ARENA_MAX=2','timeout','60s','python3','-B',guest+'/fixtures/bytecode.py','--prepared',guest+'/trees','--output',guest+'/bytecode']
 command('bytecode',shlex.join(base));data=command('bytecode-result','cat '+guest+'/bytecode/result.json');(r/'bytecode-result.json').write_bytes(data)
 for variant in ('baseline','candidate'):
  print('Running synthetic listener '+variant,flush=True)
  cmd=['env','PYTHONOPTIMIZE=0','MALLOC_ARENA_MAX=2','timeout','50s','python3','-B',guest+'/fixtures/readiness.py','--prepared',guest+'/trees','--variant',variant,'--state',guest+'/'+variant+'-state','--port','19080']
  command('readiness-'+variant,shlex.join(cmd));data=command('readiness-'+variant+'-result','cat '+guest+'/'+variant+'-state/result.json');(r/('readiness-'+variant+'.json')).write_bytes(data)
 command('final-guest',"cat /proc/sys/kernel/random/boot_id; ps -eo pid,args | grep '[f]ixtures/'; true")
 result.update(rc=0,result='PASS');print('Bytecode and both listener probes completed',flush=True)
except BaseException as e:
 result.update(rc=1,error=str(e));raise
finally:
 result['ended']=datetime.datetime.now(datetime.timezone.utc).isoformat();result['commands']=records;(r/'result.json').write_text(json.dumps(result,indent=2)+'\n')

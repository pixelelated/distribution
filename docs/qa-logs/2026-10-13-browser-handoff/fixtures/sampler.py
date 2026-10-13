from pathlib import Path
import time,json,sys,os,signal
out=Path(sys.argv[1]);out.mkdir(exist_ok=True)
start=time.monotonic();(out/'sampler.pid').write_text(str(os.getpid()));boot=Path('/proc/sys/kernel/random/boot_id').read_text().strip()
def nums(p):
 d={}
 for l in p.read_text().splitlines():
  k,_,v=l.partition(':');a=v.split()
  if a and a[0].isdigit():d[k]=int(a[0])
 return d
while time.monotonic()-start<150 and not (out/'stop').exists():
 t0=time.monotonic();rows=[]
 for p in Path('/proc').glob('[0-9]*'):
  try:
   exe=(p/'exe').resolve().name;s=nums(p/'smaps_rollup');stat=(p/'stat').read_text().rsplit(')',1)[1].split();tag=exe
   if exe.startswith('python'):
    a=(p/'cmdline').read_bytes().split(b'\0')
    for v in ['cloud_oauth','sampler.py','fake-rclone']:
     if any(x.endswith(v.encode()) for x in a):tag=v
    if tag=='cloud_oauth' and b'wait' in a:tag+=' wait'
   rows.append({'pid':int(p.name),'exe':exe,'tag':tag,'start':stat[19],'cpu':int(stat[11])+int(stat[12]),'pss':s.get('Pss',0),'anon':s.get('Pss_Anon',0),'rss':s.get('Rss',0)})
  except (OSError,ValueError):pass
 mem=nums(Path('/proc/meminfo'));vm={k:int(v) for k,v in (l.split() for l in Path('/proc/vmstat').read_text().splitlines()) if any(x in k for x in ['pgscan','allocstall','pgmajfault','workingset_refault','pgsteal'])}
 row={'wall_ms':time.time()*1000,'mono':time.monotonic(),'elapsed':time.monotonic()-start,'boot':boot,'mem':mem,'vmstat':vm,'processes':rows,'sampling_seconds':time.monotonic()-t0}
 with (out/'samples.jsonl').open('a') as f:f.write(json.dumps(row)+'\n');f.flush()
 if mem['MemAvailable']<100*1024:
  (out/'guard.json').write_text(json.dumps({'reason':'available_below100MiB','sample':row})+'\n')
  for p in rows:
   if p['exe']=='cloud-signin-window':os.kill(p['pid'],signal.SIGTERM)
  break
 time.sleep(max(0,1-(time.monotonic()-t0)))
(out/'sampler-result.json').write_text(json.dumps({'rc':0,'ended':time.time(),'samples_end':time.monotonic()-start})+'\n')

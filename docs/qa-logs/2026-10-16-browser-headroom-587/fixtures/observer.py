import os,time,json,signal
from pathlib import Path
R=Path('/storage/qa587');started=time.monotonic();seen={};guards=[];error=None;nxt=0

def mem():
 return {x.split(':')[0]:int(x.split()[1]) for x in Path('/proc/meminfo').read_text().splitlines()}
def process(p,smaps=False):
 try:
  stat=(p/'stat').read_text().rsplit(')',1)[1].split();exe=os.path.basename(os.readlink(p/'exe'));name=(p/'comm').read_text().strip()
  row={'pid':int(p.name),'start':int(stat[19]),'exe':exe,'comm':name,'state':stat[0]}
  if smaps:
   values={x.split(':')[0]:int(x.split()[1]) for x in (p/'smaps_rollup').read_text().splitlines()[1:] if len(x.split())==3 and x.split()[1].isdigit()}
   row.update({k:values.get(k) for k in ['Pss','Pss_Anon','Pss_File','Pss_Shmem','Rss','Swap']})
  return row
 except (OSError,ValueError):return None
try:
 while time.monotonic()-started<1500 and not (R/'observer-stop').exists():
  now=time.monotonic();m=mem();pressure=Path('/proc/pressure/memory');psi=pressure.read_text() if pressure.exists() else None
  psome=float(psi.splitlines()[0].split('avg10=')[1].split()[0]) if psi else None
  rows=[r for p in Path('/proc').iterdir() if p.name.isdigit() and (r:=process(p))]
  for row in rows:
   if row['exe']!='cloud-signin-window':continue
   identity=(row['pid'],row['start']);seen.setdefault(identity,now)
   reason='deadline' if now-seen[identity]>=90 else 'memory' if m['MemAvailable']<160*1024 or (m['MemAvailable']<256*1024 and psome is not None and psome>5) else None
   if reason and not any(x['identity']==list(identity) for x in guards):
    fd=os.pidfd_open(row['pid']);fresh=process(Path('/proc',str(row['pid'])))
    if fresh and fresh['start']==row['start']:
     signal.pidfd_send_signal(fd,signal.SIGTERM);g={'at':now,'identity':list(identity),'reason':reason,'available_kib':m['MemAvailable'],'psi':psi};guards.append(g)
     with (R/'guards.jsonl').open('a') as f:f.write(json.dumps(g)+'\n')
    os.close(fd)
  if now>=nxt:
   begin=time.monotonic();sample=[r for p in Path('/proc').iterdir() if p.name.isdigit() and (r:=process(p,True))]
   row={'at':now,'phase':(R/'phase').read_text().strip() if (R/'phase').exists() else 'setup','observer_pid':os.getpid(),'sampling_seconds':time.monotonic()-begin,'mem':m,'psi':psi,'processes':sample,'vmstat':Path('/proc/vmstat').read_text()}
   with (R/'samples.jsonl').open('a') as f:f.write(json.dumps(row)+'\n')
   assert (R/'samples.jsonl').stat().st_size<8*1024**2,'sample bound';nxt=now+2
  (R/'heartbeat.json').write_text(json.dumps({'at':now,'pid':os.getpid(),'guards':len(guards)}))
  time.sleep(.25)
except BaseException as e:error=repr(e);raise
finally:(R/'observer-result.json').write_text(json.dumps({'rc':int(bool(guards) or error is not None),'error':error,'guards':guards,'elapsed':time.monotonic()-started})+'\n')
raise SystemExit(int(bool(guards)))

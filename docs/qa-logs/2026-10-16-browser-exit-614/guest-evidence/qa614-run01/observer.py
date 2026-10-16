import os,json,time,signal,struct,selectors
from pathlib import Path
R=Path('/storage/qa614');sel=selectors.DefaultSelector();opened={};deadlines={};handled=set();guards=[];start=time.monotonic();nxt=0

def record(name,value):
 with (R/name).open('a') as f:f.write(json.dumps(value)+'\n')
def processes():
 rows=[]
 for p in Path('/proc').iterdir():
  if not p.name.isdigit():continue
  try:
   argv=(p/'cmdline').read_bytes().replace(b'\0',b' ').decode(errors='replace');stat=(p/'stat').read_text().rsplit(')',1)[1].split()
   if any(x in argv for x in ['cloud-signin-window','WebKit','cloud_oauth','emulationstation']):rows.append({'pid':int(p.name),'start':int(stat[19]),'argv':argv,'state':stat[0]})
  except (FileNotFoundError,ProcessLookupError):pass
 return rows
try:
 while time.monotonic()-start<1800 and not (R/'stop').exists():
  now=time.monotonic()
  for p in Path('/dev/input').glob('event*'):
   if str(p) in opened:continue
   fd=os.open(p,os.O_RDONLY|os.O_NONBLOCK);opened[str(p)]=fd;sel.register(fd,selectors.EVENT_READ,str(p));record('input.jsonl',{'at':now,'opened':str(p)})
  for key,_ in sel.select(.1):
   try:data=os.read(key.fd,struct.calcsize('llHHi')*128)
   except OSError:sel.unregister(key.fd);os.close(key.fd);continue
   for sec,usec,typ,code,val in struct.iter_unpack('llHHi',data):
    if typ==1:record('input.jsonl',{'at':now,'device':key.data,'type':typ,'code':code,'value':val})
  if now>=nxt:
   rows=processes();record('samples.jsonl',{'at':now,'processes':rows,'meminfo':Path('/proc/meminfo').read_text(),'pressure':Path('/proc/pressure/memory').read_text()});nxt=now+1
   for row in rows:
    if not row['argv'].startswith('/usr/bin/cloud-signin-window '):continue
    identity=(row['pid'],row['start']);deadlines.setdefault(identity,now+90)
    if now>=deadlines[identity] and identity not in handled:
     fd=os.pidfd_open(row['pid']);current=next((r for r in processes() if (r['pid'],r['start'])==identity),None)
     if current:signal.pidfd_send_signal(fd,signal.SIGTERM);guards.append({'at':now,'identity':row,'reason':'90s emergency deadline'});record('guard.jsonl',guards[-1])
     os.close(fd);handled.add(identity)
finally:
 for key in list(sel.get_map().values()):sel.unregister(key.fd);os.close(key.fd)
 (R/'observer-result.json').write_text(json.dumps({'rc':int(bool(guards)),'guards':guards,'elapsed':time.monotonic()-start,'stopped':(R/'stop').exists()})+'\n')
raise SystemExit(int(bool(guards)))

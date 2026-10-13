from pathlib import Path
import time,json
names={'cloud-signin-window','WebKitWebProcess','WebKitNetworkProcess','WebKitGPUProcess','emulationstation','sway','kswapd0'}
def snap():
 out={'wall':time.time(),'vm':{},'cpu':Path('/proc/stat').read_text().splitlines()[0],'processes':[]}
 for line in Path('/proc/vmstat').read_text().splitlines():
  k,v=line.split()
  if any(x in k for x in ['pgscan','pgsteal','allocstall','compact','pswp','pgmajfault','workingset']):out['vm'][k]=int(v)
 for p in Path('/proc').glob('[0-9]*'):
  try:
   comm=(p/'comm').read_text().strip();exe=(p/'exe').resolve().name
   if exe not in names and comm not in names:continue
   stat=(p/'stat').read_text().rsplit(')',1)[1].split();out['processes'].append({'pid':int(p.name),'exe':exe,'comm':comm,'utime':int(stat[11]),'stime':int(stat[12]),'state':stat[0],'wchan':(p/'wchan').read_text(),'schedstat':(p/'schedstat').read_text().strip()})
  except (OSError,ValueError):pass
 return out
print(json.dumps(snap()),flush=True);time.sleep(3);print(json.dumps(snap()),flush=True)

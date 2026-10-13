from pathlib import Path
import json,os,subprocess,time,datetime,re
P=Path
allowed_env={'WEBKIT_DISABLE_DMABUF_RENDERER','WEBKIT_DISABLE_COMPOSITING_MODE','WEBKIT_SKIA_ENABLE_CPU_RENDERING','LIBGL_ALWAYS_SOFTWARE','GDK_BACKEND','WLR_RENDERER'}
def read(p):
 try:return P(p).read_text().strip()
 except OSError:return ''
def numbers(p):
 d={}
 for l in read(p).splitlines():
  k,sep,v=l.partition(':');v=v.split()
  if v and v[0].isdigit():d[k]=int(v[0])
 return d

def census():
 out={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'read_only':True,'meminfo':numbers('/proc/meminfo'),'processes':[],'drm_devices':[]}
 for p in P('/proc').glob('[0-9]*'):
  try:
   name=read(p/'comm');sm=numbers(p/'smaps_rollup');st=read(p/'stat').rpartition(') ')[2].split()
   if not sm or len(st)<22:continue
   item={'pid':int(p.name),'name':name,'rss_kib':sm.get('Rss',0),'pss_kib':sm.get('Pss',0),'anon_kib':sm.get('Pss_Anon',0),'file_kib':sm.get('Pss_File',0),'shmem_kib':sm.get('Pss_Shmem',0),'cpu_ticks':int(st[11])+int(st[12]),'threads':int(st[17]),'drm_fds':[]}
   for fd in (p/'fd').iterdir():
    try:target=os.readlink(fd)
    except OSError:continue
    if re.fullmatch(r'/dev/dri/(card|renderD)[0-9]+',target):item['drm_fds'].append(target)
   if name.startswith(('WebKit','cloud-signin','sway','emulationstat')):
    item['graphics_env']={}
    for x in (p/'environ').read_bytes().split(b'\0'):
     k,_,v=x.partition(b'=')
     if k.decode(errors='replace') in allowed_env:item['graphics_env'][k.decode()]=v.decode(errors='replace')
    item['graphics_libraries']=sorted({Path(x.split()[-1]).name for x in read(p/'maps').splitlines() if '/' in x and any(t in x for t in ['libEGL','libGL','panfrost','lima','_dri.so','libvulkan'])})
   item['start_ticks']=st[19]
   item['service']=[x.rsplit('/',1)[-1] for x in read(p/'cgroup').splitlines() if '/system.slice/' in x][-1:]
   item['exe']=(p/'exe').resolve().name
   item['drm_clients']={}
   for f in (p/'fdinfo').glob('*'):
    fd=read(f)
    if 'drm-driver:' not in fd:continue
    fields={k.strip():v.strip() for l in fd.splitlines() if (k:=l.partition(':')[0]).startswith('drm-') for v in [l.partition(':')[2]]}
    if 'drm-client-id' in fields:item['drm_clients'][fields['drm-driver']+':'+fields['drm-client-id']]=fields
   out['processes'].append(item)
  except (OSError,ValueError):continue
 out['processes'].sort(key=lambda p:p['pss_kib'],reverse=True)
 for p in P('/sys/class/drm').glob('*'):
  if not re.fullmatch(r'(card|renderD)[0-9]+',p.name):continue
  driver=p/'device/driver';out['drm_devices'].append({'node':p.name,'driver':driver.resolve().name if driver.exists() else None})
 q=subprocess.run(['systemctl','list-units','--type=service','--state=running','--no-legend','--no-pager'],capture_output=True,text=True,timeout=10)
 out['running_services']=[l.split()[0] for l in q.stdout.splitlines() if l.strip()];out['services_rc']=q.returncode
 out['pressure']={n:read('/proc/pressure/'+n) for n in ['cpu','memory','io']}
 out['cpu_frequency_khz']=[read(p) for p in P('/sys/devices/system/cpu').glob('cpu*/cpufreq/scaling_cur_freq')]
 out['gpu_devfreq']=[{'driver':p.resolve().name,'frequency':read(p/'cur_freq'),'governor':read(p/'governor')} for p in P('/sys/class/devfreq').glob('*')]
 out['identity']={'hostname':read('/proc/sys/kernel/hostname'),'model':read('/proc/device-tree/model').replace('\x00',''),'boot_id':read('/proc/sys/kernel/random/boot_id'),'kernel':read('/proc/sys/kernel/osrelease')}
 out['os_release']={l.split('=',1)[0]:l.split('=',1)[1].strip('"') for l in read('/etc/os-release').splitlines() if '=' in l and l.split('=',1)[0] in {'NAME','VERSION','VERSION_ID','BUILD_ID','PRETTY_NAME','ROCKNIX_ARCH','ROCKNIX_DEVICE','LIBREELEC_ARCH'}}
 out['power']=[{'supply':p.name,'status':read(p/'status'),'capacity':read(p/'capacity'),'online':read(p/'online')} for p in P('/sys/class/power_supply').glob('*')]
 return out

import signal,hashlib
root=P('/tmp/pixelelated-browser-stack-570-20261013')
assert not root.exists(),'Refusing to reuse probe root'
initial=census()
assert initial['identity']['model']=='Anbernic RG35XX SP'
assert initial['os_release']['BUILD_ID']=='bc9dfe8141d9561dc1d8502313d00a84c4566ee8'
assert initial['meminfo']['MemAvailable']>400*1024
browsers={'cloud-signin-window','WebKitWebProcess','WebKitNetworkProcess'}
assert not [p for p in initial['processes'] if p['exe'] in browsers],'Existing browser'
assert not [p for p in initial['processes'] if p['exe'].startswith(('retroarch','retro-run','ppsspp','dolphin-emu'))],'Existing game'
root.mkdir(mode=0o700)
runtime=next(p.parent for p in P('/run').glob('**/wayland-*') if not p.name.endswith('.lock') and p.is_socket())
display=next(p.name for p in runtime.glob('wayland-*') if not p.name.endswith('.lock') and p.is_socket())
result={'initial':initial,'binary_sha256':hashlib.sha256(P('/usr/bin/cloud-signin-window').read_bytes()).hexdigest(),'cases':[],'completed':False}
def save():
 (root/'result.tmp').write_text(json.dumps(result))
 (root/'result.tmp').replace(root/'result.json')
def stop(row,sig):
 p=P('/proc')/str(row['pid'])
 try:
  if read(p/'stat').rpartition(') ')[2].split()[19]==row['start_ticks'] and (p/'exe').resolve().name==row['exe']:os.kill(row['pid'],sig)
 except (OSError,IndexError):pass
for case,url,disabled,duration in [('simple-off','https://example.org/','1',25),('simple-on','https://example.org/','0',25),('public-off','https://www.dropbox.com/login','1',65),('public-on','https://www.dropbox.com/login','0',65)]:
 before=census()
 assert not [p for p in before['processes'] if p['exe'] in browsers],'Previous browser remains'
 assert before['meminfo']['MemAvailable']>400*1024,'Insufficient recovery'
 assert before['identity']['boot_id']==initial['identity']['boot_id'],'Boot changed'
 d=root/case;d.mkdir()
 env=dict(os.environ,XDG_RUNTIME_DIR=str(runtime),WAYLAND_DISPLAY=display,GDK_BACKEND='wayland',XDG_CACHE_HOME=str(d/'cache'),XDG_DATA_HOME=str(d/'data'),XDG_CONFIG_HOME=str(d/'config'),CLOUD_SIGNIN_PAGE_FILE=str(d/'page'),CLOUD_SIGNIN_FIELD_FILE=str(d/'field'),WEBKIT_DISABLE_DMABUF_RENDERER=disabled)
 rec={'case':case,'url':url,'disable_dmabuf':disabled,'before':before,'samples':[],'frames':[],'reason':'duration','duration_limit':duration}
 owned={};proc=None;start=time.monotonic()
 try:
  with (d/'window.log').open('wb') as log:proc=subprocess.Popen(['/usr/bin/cloud-signin-window',url,url.split('/')[2],'--no-auto-keyboard'],env=env,stdout=log,stderr=log,start_new_session=True)
  rec['launcher_pid']=proc.pid
  while time.monotonic()-start<duration:
   snap=census();snap['elapsed']=round(time.monotonic()-start,3);rec['samples'].append(snap)
   for row in snap['processes']:
    if row['exe'] in browsers:owned[row['pid']]=row
   psi=snap['pressure']['memory'];match=re.search(r'some avg10=([0-9.]+)',psi);avg=float(match.group(1)) if match else 0
   if snap['meminfo']['MemAvailable']<160*1024 or avg>5:
    rec['reason']='memory guard';break
   if proc.poll() is not None:rec['reason']='browser exited';break
   if snap['elapsed']>12 and not rec['frames']:
    cap=subprocess.run(['grim',str(d/'page.png')],env=env,capture_output=True,timeout=5)
    rec['frames'].append({'file':str(d/'page.png'),'rc':cap.returncode,'elapsed':round(time.monotonic()-start,3)})
   time.sleep(2)
 finally:
  rec['loaded_marker']=(d/'page').exists()
  if proc and proc.poll() is None:proc.terminate()
  for row in owned.values():stop(row,signal.SIGTERM)
  if proc:
   try:proc.wait(timeout=8)
   except subprocess.TimeoutExpired:proc.kill();proc.wait(timeout=5)
  time.sleep(3)
  for row in owned.values():stop(row,signal.SIGKILL)
  time.sleep(3)
  rec['after']=census();rec['browser_exit']=proc.returncode if proc else None
  rec['log_summary']=[l for l in read(d/'window.log').splitlines() if any(k in l.lower() for k in ['load finished','gstreamer','libgstcontroller','memory pressure','gl context','hardware acceleration','panfrost','critical','error']) and not re.search('key|pass|token|user|psk',l,re.I)]
  result['cases'].append(rec);save()
  print(json.dumps({'case':case,'reason':rec['reason'],'loaded':rec['loaded_marker'],'samples':len(rec['samples']),'available_after_kib':rec['after']['meminfo']['MemAvailable']}),flush=True)
 assert not [p for p in rec['after']['processes'] if p['exe'] in browsers],'Browser cleanup failed'
 time.sleep(5)
result['completed']=True;result['final']=census();save()
print('BENCH COMPARISON COMPLETE',flush=True)

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
print(json.dumps(out,indent=2))

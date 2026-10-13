from pathlib import Path
import os,sys,json,time,subprocess,signal,re
spec=json.loads(sys.argv[1]);name=spec['name'];seconds=spec.get('seconds',120)
base=Path('/storage/qa-570');base.mkdir(exist_ok=True);out=base/name;out.mkdir()
browser_names={'cloud-signin-window','WebKitWebProcess','WebKitNetworkProcess','WebKitGPUProcess'}
def numbers(p):
 d={}
 for l in p.read_text().splitlines():
  k,_,v=l.partition(':');v=v.split()
  if v and v[0].isdigit():d[k]=int(v[0])
 return d
def processes():
 rows=[]
 for p in Path('/proc').glob('[0-9]*'):
  try:
   exe=(p/'exe').resolve().name
   if exe not in browser_names|{'emulationstation'}:continue
   s=numbers(p/'smaps_rollup');raw=(p/'stat').read_text().rsplit(')',1)[1].split()
   maps=[]
   for l in (p/'maps').read_text().splitlines():
    if ('libwebkit' in l or 'libjavascriptcore' in l) and len(l.split())>5:maps.append(l.split()[-1])
   rows.append(dict(pid=int(p.name),exe=exe,start_ticks=raw[19],cpu_ticks=int(raw[11])+int(raw[12]),rss_kib=s.get('Rss'),pss_kib=s.get('Pss'),anon_kib=s.get('Pss_Anon'),file_kib=s.get('Pss_File'),shmem_kib=s.get('Pss_Shmem'),libraries=sorted(set(maps))))
  except (OSError,ValueError):continue
 return rows
def sample():
 return {'t':round(time.monotonic()-start,3),'mem':numbers(Path('/proc/meminfo')),'processes':processes()}
def browsers():return [p for p in processes() if p['exe'] in browser_names]
assert not browsers(),'Existing browser must be stopped before test'
socket=next(p for p in Path('/run').glob('**/wayland-*') if p.is_socket())
env=dict(os.environ,XDG_RUNTIME_DIR=str(socket.parent),WAYLAND_DISPLAY=socket.name,GDK_BACKEND='wayland',TMPDIR=str(out),XDG_CACHE_HOME=str(out/'cache'),XDG_DATA_HOME=str(out/'data'),CLOUD_SIGNIN_PAGE_FILE=str(out/'page'),CLOUD_SIGNIN_FIELD_FILE=str(out/'field'),**spec.get('env',{}))
version_code='import ctypes; w=ctypes.CDLL("libwebkit2gtk-4.1.so.0"); print("%d.%d.%d" % (w.webkit_get_major_version(),w.webkit_get_minor_version(),w.webkit_get_micro_version()))'
v=subprocess.run(['python3','-c',version_code],env=env,capture_output=True,text=True,timeout=15);assert v.returncode==0,v.stderr
assert v.stdout.strip()==spec['engine'],v.stdout
start=time.monotonic();before=sample();rows=[];frames=[];reason='duration';p=None;error=None
try:
 with (out/'window.log').open('wb') as log:
  p=subprocess.Popen(['/usr/bin/cloud-signin-window',spec['url'],spec['url'].split('/')[2].split(':')[0],'--no-auto-keyboard'],env=env,stdout=log,stderr=log,start_new_session=True)
  while time.monotonic()-start<seconds:
   s=sample();rows.append(s);t=s['t']
   if s['mem']['MemAvailable']<32*1024:reason='low_memory_guard';break
   if p.poll() is not None:reason='browser_exit';break
   if (not frames and t>=25) or (len(frames)==1 and t>=seconds-8):
    f=out/('frame'+str(len(frames))+'.png');cap=subprocess.run(['grim',str(f)],env=env,capture_output=True,timeout=8);frames.append({'file':str(f),'rc':cap.returncode})
   time.sleep(2)
except BaseException as e:error=repr(e);reason='probe_error'
finally:
 if p and p.poll() is None:p.terminate()
 if p:
  try:p.wait(timeout=8)
  except subprocess.TimeoutExpired:p.kill();p.wait(timeout=5)
 deadline=time.monotonic()+20;forced=[]
 while browsers() and time.monotonic()<deadline:time.sleep(1)
 for b in browsers():
  forced.append(b)
  try:os.kill(b['pid'],signal.SIGKILL)
  except ProcessLookupError:pass
 time.sleep(3);after=sample()
 result={'spec':spec,'engine_report':v.stdout.strip(),'before':before,'samples':rows,'after':after,'stop_reason':reason,'forced_cleanup':forced,'browser_exit':p.returncode if p else None,'error':error,'frames':frames,'log':(out/'window.log').read_text(errors='replace') if (out/'window.log').exists() else '', 'page':(out/'page').read_text() if (out/'page').exists() else None,'sampler_logs':{p.name:p.read_text(errors='replace') for p in out.iterdir() if p.is_file() and p.name.startswith(('WebKit','cloud-signin'))}}
 print(json.dumps(result),flush=True)
 if browsers() or error:sys.exit(1)

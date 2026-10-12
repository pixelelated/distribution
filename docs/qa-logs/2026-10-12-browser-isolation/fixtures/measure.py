import os,sys,time,json,subprocess,signal,re
from pathlib import Path
case,binary,url,seconds,extra=json.loads(sys.argv[1]); seconds=int(seconds)
out=Path('/tmp/pressure-'+case);out.mkdir()
def nums(file):
 d={}
 for l in Path(file).read_text().splitlines():
  k,_,v=l.partition(':');v=v.strip().split()
  if v and v[0].isdigit():d[k]=int(v[0])
 return d
def processes():
 result=[]
 for p in Path('/proc').glob('[0-9]*'):
  try:
   exe=(p/'exe').resolve().name
   if exe not in ('cloud-signin-window','qa-current','qa-historical','WebKitWebProcess','WebKitNetworkProcess','emulationstation'):continue
   roll=nums(p/'smaps_rollup');status=nums(p/'status')
   result.append(dict(pid=int(p.name),exe=exe,rss_kib=status.get('VmRSS'),pss_kib=roll.get('Pss'),anon_kib=roll.get('Pss_Anon'),file_kib=roll.get('Pss_File'),shmem_kib=roll.get('Pss_Shmem')))
  except (OSError,ValueError):pass
 return result
def sample():
 return dict(t=round(time.monotonic()-start,3),mem=nums('/proc/meminfo'),processes=processes())
runtime=next(p.parent for p in Path('/run').glob('**/wayland-*') if not p.name.endswith('.lock') and p.is_socket())
display=next(p.name for p in runtime.glob('wayland-*') if not p.name.endswith('.lock'))
env=dict(os.environ,XDG_RUNTIME_DIR=str(runtime),WAYLAND_DISPLAY=display,GDK_BACKEND='wayland',CLOUD_SIGNIN_PAGE_FILE=str(out/'page'),CLOUD_SIGNIN_FIELD_FILE=str(out/'field'),**extra)
start=time.monotonic();before=sample();rows=[];frames=[];p=None;error=None
try:
 with (out/'window.log').open('wb') as log:
  p=subprocess.Popen([binary,url,url.split('/')[2].split(':')[0],'--no-auto-keyboard'],env=env,stdout=log,stderr=log,start_new_session=True)
  while time.monotonic()-start<seconds:
   rows.append(sample())
   t=time.monotonic()-start
   if (not frames and t>25) or (len(frames)==1 and t>seconds-12):
    f=out/('frame'+str(len(frames))+'.png');cap=subprocess.run(['grim',str(f)],env=env,capture_output=True,timeout=10)
    frames.append(dict(file=str(f),rc=cap.returncode))
   if p.poll() is not None:break
   time.sleep(3)
  libraries={}
  for row in processes():
   if row['exe']=='emulationstation':continue
   path=Path('/proc')/str(row['pid'])
   try:
    group=''; totals={}
    for line in (path/'smaps').read_text().splitlines():
     if re.match(r'^[0-9a-f]+-',line):
      name=line.split()[-1] if len(line.split())>=6 else '[anonymous]'
      group='gstreamer' if any(s in name for s in ('libgst','gstreamer-')) else 'webkit_jsc' if any(s in name for s in ('libwebkit','libjavascriptcore')) else 'anonymous' if name.startswith('[') else 'other'
     elif line.startswith('Pss:'):totals[group]=totals.get(group,0)+int(line.split()[1])
    libraries[str(row['pid'])]=dict(exe=row['exe'],pss_kib=totals)
   except OSError:pass
except BaseException as e:error=repr(e)
finally:
 if p and p.poll() is None:
  p.terminate()
  try:p.wait(timeout=8)
  except subprocess.TimeoutExpired:p.kill();p.wait(timeout=8)
 time.sleep(5)
 after=sample()
 orphans=[x for x in after['processes'] if x['exe']!='emulationstation']
 for x in orphans:
  try:os.kill(x['pid'],signal.SIGTERM)
  except ProcessLookupError:pass
 result=dict(case=case,binary=binary,url=url,seconds=seconds,extra=extra,before=before,samples=rows,after=after,orphans=orphans,frames=frames,library_pss=locals().get('libraries',{}),window_rc=p.returncode if p else None,error=error,log=(out/'window.log').read_text(errors='replace') if (out/'window.log').exists() else '',page=(out/'page').read_text() if (out/'page').exists() else None)
 print(json.dumps(result));sys.stdout.flush()
if error:sys.exit(1)

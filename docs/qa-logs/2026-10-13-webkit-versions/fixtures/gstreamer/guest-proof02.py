from pathlib import Path
import subprocess,os,time,json,hashlib
base=Path('/storage/qa-572');root=base/'package';out={'cases':{}};mounted=False
for p in Path('/proc').glob('[0-9]*'):
 try:exe=(p/'exe').resolve().name
 except OSError:continue
 assert exe not in {'cloud-signin-window','WebKitWebProcess','WebKitNetworkProcess','WebKitGPUProcess'},'browser exists'
def run(name):
 env=dict(os.environ,GST_REGISTRY=str(base/(name+'-registry.bin')))
 assert not any(x in env for x in ['GST_PLUGIN_SCANNER','GST_PLUGIN_SCANNER_1_0','GST_REGISTRY_FORK','LD_LIBRARY_PATH'])
 seen=set();start=time.monotonic()
 with (base/(name+'.out')).open('wb') as o,(base/(name+'.err')).open('wb') as e:
  p=subprocess.Popen([str(root/'usr/bin/gst-inspect-1.0'),'opengl'],env=env,stdout=o,stderr=e)
  while p.poll() is None:
   if time.monotonic()-start>45:p.kill();p.wait();raise RuntimeError('plugin probe timeout')
   for q in Path('/proc').glob('[0-9]*'):
    try:
     if (q/'exe').resolve().name=='gst-plugin-scanner':seen.add(str((q/'exe').resolve()))
    except OSError:pass
   time.sleep(.01)
 return {'rc':p.returncode,'stdout':(base/(name+'.out')).read_text(),'stderr':(base/(name+'.err')).read_text(),'scanner_executables':sorted(seen)}
try:
 out['cases']['original']=run('original');assert out['cases']['original']['rc']!=0
 assert 'libgstcontroller' in out['cases']['original']['stderr']
 subprocess.run(['mount','-t','overlay','overlay','-o','lowerdir='+str(root/'usr/lib')+':/usr/lib','/usr/lib'],check=True);mounted=True
 out['cases']['corrected']=run('corrected');assert out['cases']['corrected']['rc']==0
 assert 'Failed to load plugin' not in out['cases']['corrected']['stderr'] and 'External plugin loader failed' not in out['cases']['corrected']['stderr']
 out['installed_hashes']={}
 for rel in ['usr/lib/libgstcontroller-1.0.so.0','usr/lib/gstreamer-1.0/gst-plugin-scanner']:
  with (Path('/')/rel).open('rb') as f:out['installed_hashes'][rel]=hashlib.file_digest(f,'sha256').hexdigest()
 out['rc']=0
except BaseException as e:out.update(rc=1,error=repr(e));raise
finally:
 if mounted:subprocess.run(['umount','-l','/usr/lib'],check=True)
 print(json.dumps(out),flush=True)

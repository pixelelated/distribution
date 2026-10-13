from pathlib import Path
import subprocess, json, shlex, time, hashlib, datetime, tarfile, os
r=Path(__file__).parent; root=r.parent; ssh=json.loads((r/'ssh-command.json').read_text())
result={'started':datetime.datetime.now(datetime.timezone.utc).isoformat(),'cases':[]}
def remote(cmd,**kwargs):return subprocess.run(ssh+[cmd],check=True,**kwargs)
def now():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def switch(old):
 code='''from pathlib import Path
import os,subprocess,json,hashlib
names={'cloud-signin-window','WebKitWebProcess','WebKitNetworkProcess','WebKitGPUProcess'}
for p in Path('/proc').glob('[0-9]*'):
 try:e=(p/'exe').resolve().name
 except OSError:continue
 assert e not in names, 'Existing browser: '+str(p)
old=OLD
base=Path('/storage/qa-570/runtime-2.54.0')
for rel in ['usr/libexec/webkit2gtk-4.1','usr/lib/webkit2gtk-4.1']:
 dest=Path('/')/rel
 mounted=subprocess.run(['mountpoint','-q',str(dest)]).returncode==0
 if mounted:subprocess.run(['umount',str(dest)],check=True)
 if old:subprocess.run(['mount','--bind',str(base/rel),str(dest)],check=True)
print(json.dumps({'old_runtime_selected':old}))
'''.replace('OLD',str(old))
 return remote('python3 -c '+shlex.quote(code),capture_output=True,text=True).stdout
try:
 deadline=time.monotonic()+7200
 owner=root/'build-2540-owner'; run=Path('/workspace/repos/rocknix.worktrees/m7-webkit-versions-570/.build-runs/20261013T002229Z-4b95c641')
 while not (owner/'launcher-result.json').exists():
  if time.monotonic()>deadline:raise RuntimeError('Old-engine build did not finish within dependency wait')
  print('WAIT',now(),'2.54.0 build dependency',flush=True);time.sleep(30)
 launch=json.loads((owner/'launcher-result.json').read_text())
 assert launch['runner_returncode']==0 and (owner/'tool-wrapper.rc').read_text().strip()=='0'
 assert (run/'build.rc').read_text().strip()=='0' and json.loads((root/'build-2540-result.json').read_text())['rc']==0
 while Path('/proc',str(launch['pid'])).exists() and time.monotonic()<deadline:time.sleep(1)
 assert not Path('/proc',str(launch['pid'])).exists()
 stage=root/'runtime-2.54.0'; paths=[]
 for pattern in ['usr/lib/libwebkit2gtk-4.1.so*','usr/lib/libjavascriptcoregtk-4.1.so*']:
  matched=list(stage.glob(pattern));assert matched,pattern;paths+=matched
 for rel in ['usr/libexec/webkit2gtk-4.1','usr/lib/webkit2gtk-4.1']:
  p=stage/rel;assert p.is_dir(),rel;paths.append(p)
 archive=root/'runtime-2.54.0.tar'
 with tarfile.open(archive,'w') as t:
  for p in paths:t.add(p,arcname=str(p.relative_to(stage)))
 manifest={}
 for p in paths:
  for f in ([p] if p.is_file() else p.rglob('*')):
   if f.is_file() and not f.is_symlink():
    with f.open('rb') as s:manifest[str(f.relative_to(stage))]=hashlib.file_digest(s,'sha256').hexdigest()
 (root/'runtime-2.54.0-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
 remote('mkdir /storage/qa-570/runtime-2.54.0')
 with archive.open('rb') as s:remote('tar -xf - -C /storage/qa-570/runtime-2.54.0',stdin=s)
 verify='''from pathlib import Path
import json,hashlib
m=json.loads(INPUT)
b=Path('/storage/qa-570/runtime-2.54.0')
for n,h in m.items():
 with (b/n).open('rb') as f:assert hashlib.file_digest(f,'sha256').hexdigest()==h,n
print('Verified',len(m),'runtime files')
'''.replace('INPUT',repr(json.dumps(manifest)))
 result['payload_verification']=remote('python3 -c '+shlex.quote(verify),capture_output=True,text=True).stdout
 with (r/'measure.py').open('rb') as f:remote('cat > /tmp/qa-570-measure.py',stdin=f)
 # Alternation limits ordering effects; all trials retain the same installed app/dependencies.
 for index,engine in enumerate(['2.54.0','2.54.1','2.54.1','2.54.0','2.54.0','2.54.1']):
  old=engine=='2.54.0';name='repeat-'+str(index+1)+'-'+engine.replace('.','')
  selected=switch(old); print('START',now(),name,selected.strip(),flush=True)
  spec={'name':name,'engine':engine,'url':'https://www.dropbox.com/login','seconds':120}
  if old:spec['env']={'LD_LIBRARY_PATH':'/storage/qa-570/runtime-2.54.0/usr/lib'}
  with (r/(name+'.json')).open('wb') as o,(r/(name+'.stderr')).open('wb') as e:
   p=subprocess.run(ssh+['python3 /tmp/qa-570-measure.py '+shlex.quote(json.dumps(spec))],stdout=o,stderr=e,timeout=210)
  assert p.returncode==0,name
  j=json.loads((r/(name+'.json')).read_text());assert not j['error'] and j['stop_reason']=='duration',name
  assert not [x for x in j['after']['processes'] if x['exe']!='emulationstation'] and not j['forced_cleanup'],name
  seen={x['exe'] for s in j['samples'] for x in s['processes']}
  assert {'cloud-signin-window','WebKitWebProcess','WebKitNetworkProcess'}<=seen,(name,seen)
  mappings={v for s in j['samples'] for x in s['processes'] for v in x['libraries']}
  assert mappings and all(v.startswith('/storage/qa-570/runtime-2.54.0/usr/lib/' if old else '/usr/lib/') for v in mappings),(name,mappings)
  for frame in j['frames']:
   assert frame['rc']==0
   with (r/(name+'-'+Path(frame['file']).name)).open('wb') as o:remote('cat '+shlex.quote(frame['file']),stdout=o)
  metrics={'name':name,'engine':engine,'peak_browser_pss_kib':max(sum(x['pss_kib'] for x in s['processes'] if x['exe']!='emulationstation') for s in j['samples']),'min_available_kib':min(s['mem']['MemAvailable'] for s in j['samples'])}
  result['cases'].append(metrics);print('END',now(),json.dumps(metrics),flush=True)
  (r/'version-matrix-progress.json').write_text(json.dumps(result,indent=2)+'\n')
 switch(False);result['rc']=0
except BaseException as e:
 result.update(rc=1,error=repr(e))
 try:result['restoration']=switch(False)
 except BaseException as restore:result['restoration_error']=repr(restore)
 raise
finally:
 result['ended']=now();(r/'version-matrix-result.json').write_text(json.dumps(result,indent=2)+'\n')

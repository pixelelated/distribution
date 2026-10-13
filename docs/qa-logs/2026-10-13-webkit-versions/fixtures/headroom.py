from pathlib import Path
import subprocess,json,shlex,time,datetime
r=Path(__file__).parent; root=r.parent; ssh=json.loads((r/'ssh-command.json').read_text()); result={'started':datetime.datetime.now(datetime.timezone.utc).isoformat(),'cases':[],'assigned_mib':2048}
def remote(cmd,**kw):return subprocess.run(ssh+[cmd],check=True,**kw)
# Reuse the frozen, hash-verifying runtime selector; do not execute its original matrix.
ns={};s=(r/'version-matrix02.py').read_text();start=s.index('def switch(old):');end=s.index('\ntry:\n deadline=',start)
exec(s[start:end],dict(Path=Path,remote=remote,subprocess=subprocess,json=json,shlex=shlex,manifest=json.loads((root/'runtime-2.54.0-manifest.json').read_text())),ns);switch=ns['switch']
try:
 owner=root/'gst02/plugin-owner04'; launch=json.loads((owner/'launcher-result.json').read_text());assert launch['runner_returncode']==0 and not Path('/proc',str(launch['pid'])).exists()
 assert json.loads((root/'gst02/plugin-result04.json').read_text())['library_mount_restored']
 result['previous_boot']=remote('cat /proc/sys/kernel/random/boot_id',capture_output=True,text=True,timeout=20).stdout.strip()
 remote('sync; poweroff',timeout=20)
 time.sleep(8)
 subprocess.run(['tools/vm-stop',str(r/'vm.pid'),str(r/'disk.qcow2')],check=True)
 subprocess.run(['python3',str(r/'headroom-vm.py'),'run',str(r/'disk.qcow2'),'--headless','--daemonize','--gl','none','--res','640x480','--ssh-port','10573','--vnc','58','--pidfile',str(r/'vm.pid'),'--serial',str(r/'serial.sock'),'--monitor',str(r/'monitor.sock'),'--ovmf-vars',str(r/'OVMF.fd')],check=True)
 subprocess.run(['tools/vm-serial','--socket',str(r/'serial.sock'),'wait','--up-to','240'],check=True)
 deadline=time.monotonic()+90
 while True:
  p=subprocess.run(ssh+['test -S /run/0-runtime-dir/wayland-0 || find /run -type s -name wayland-0'],capture_output=True,timeout=15)
  if p.returncode==0:break
  assert time.monotonic()<deadline,'SSH readiness timeout';time.sleep(3)
 result['boot']=remote('cat /proc/sys/kernel/random/boot_id',capture_output=True,text=True,timeout=20).stdout.strip();assert result['boot']!=result['previous_boot']
 with (r/'measure02.py').open('rb') as f:remote('cat > /tmp/qa-570-measure02.py',stdin=f,timeout=20)
 for engine,corrected in [('2.54.0',False),('2.54.1',False),('2.54.1',True)]:
  name='headroom-'+engine.replace('.','')+('-gst' if corrected else '');old=engine=='2.54.0';selected=json.loads(switch(old));print('START',name,flush=True)
  spec={'name':name,'engine':engine,'url':'https://www.dropbox.com/login','seconds':90}
  if old:spec['env']={'LD_LIBRARY_PATH':'/storage/qa-570/runtime-2.54.0/usr/lib'}
  if corrected:remote('mount -t overlay overlay -o lowerdir=/storage/qa-572/package/usr/lib:/usr/lib /usr/lib',timeout=20)
  try:
   with (r/(name+'.json')).open('wb') as out,(r/(name+'.stderr')).open('wb') as err:
    p=subprocess.run(ssh+['python3 /tmp/qa-570-measure02.py '+shlex.quote(json.dumps(spec))],stdout=out,stderr=err,timeout=165)
   j=json.loads((r/(name+'.json')).read_text())
   for frame in j['frames']:
    with (r/(name+'-'+Path(frame['file']).name)).open('wb') as o:remote('cat '+shlex.quote(frame['file']),stdout=o,timeout=20)
   assert p.returncode==0,(name,'loading or cleanup check failed')
   assert j['before']['boot_id']==j['after']['boot_id']==result['boot']
   if corrected:assert 'GStreamer-WARNING' not in j['log'] and 'Failed to load plugin' not in j['log']
   metrics={'name':name,'peak_browser_pss_kib':max(sum(x['pss_kib'] for x in a['processes'] if x['exe']!='emulationstation') for a in j['samples']),'min_available_kib':min(a['mem']['MemAvailable'] for a in j['samples']),'page':j['page'],'selection':selected}
   result['cases'].append(metrics);print('PASS',json.dumps(metrics),flush=True)
  finally:
   if corrected:remote('umount -l /usr/lib',timeout=20)
  (r/'headroom-progress.json').write_text(json.dumps(result,indent=2)+'\n')
 result['rc']=0
except BaseException as e:result.update(rc=1,error=repr(e));raise
finally:
 try:
  result['restoration']=json.loads(switch(False));result['library_mount_restored']=remote('if mountpoint -q /usr/lib; then exit 1; else echo restored; fi',capture_output=True,text=True,timeout=20).stdout.strip()=='restored'
 except BaseException as e:result['restoration_error']=repr(e)
 result['ended']=datetime.datetime.now(datetime.timezone.utc).isoformat();(r/'headroom-result.json').write_text(json.dumps(result,indent=2)+'\n')

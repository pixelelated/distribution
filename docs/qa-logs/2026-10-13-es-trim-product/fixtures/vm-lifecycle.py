from pathlib import Path
import subprocess,json,gzip,hashlib,time,datetime,socket
r=Path(__file__).parent;repo=Path('/workspace/repos/rocknix.worktrees/m7-player-setup');facts=json.loads((r/'records/image-size.json').read_text());src=Path(facts['image']);v=r/'vm';raw=v/'disk.img';disk=v/'disk.qcow2';result={'rc':1,'started':time.time()}
def call(args,**kw):return subprocess.run([str(x) for x in args],check=True,**kw)
try:
 for port in [10602,5992]:
  with socket.socket() as s:s.bind(('127.0.0.1',port))
 assert hashlib.file_digest(src.open('rb'),'sha256').hexdigest()==facts['sha256']
 count=0
 with gzip.open(src,'rb') as a,raw.open('xb') as b:
  while True:
   chunk=a.read(4*1024*1024)
   if not chunk:break
   count+=len(chunk)
   if chunk.count(0)==len(chunk):b.seek(len(chunk),1)
   else:b.write(chunk)
  b.truncate()
 assert count==facts['raw_bytes_from_backup_lba']
 call(['qemu-img','convert','-f','raw','-O','qcow2',raw,disk],timeout=90);call(['qemu-img','resize',disk,'16G'],timeout=30);raw.unlink()
 call([repo/'projects/ROCKNIX/devices/GENERIC_X64/vm/generic-x64-vm','run',disk,'--headless','--daemonize','--gl','auto','--res','640x480','--ssh-port','10602','--vnc','92','--pidfile',v/'vm.pid','--serial',v/'serial.sock','--monitor',v/'monitor.sock','--ovmf-vars',v/'OVMF.fd'],timeout=60)
 call([repo/'tools/vm-serial','--socket',v/'serial.sock','wait','--up-to','240'],timeout=260)
 ready={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'pid':int((v/'vm.pid').read_text()),'disk':str(disk),'source_sha256':facts['sha256'],'profile':'standard hardware GL 640x480'};(r/'vm-ready.json').write_text(json.dumps(ready,indent=2)+'\n');print('VM READY; lifecycle watcher remains active through requested shutdown',flush=True)
 deadline=time.monotonic()+2400
 while not (r/'vm-stop.request').exists():
  if time.monotonic()>deadline:raise TimeoutError('QA allocation expired')
  assert (Path('/proc')/str(ready['pid'])/'cmdline').read_bytes(),'guest exited unexpectedly'
  time.sleep(1)
 result['rc']=0
finally:
 if (v/'vm.pid').exists():
  stop=subprocess.run([str(repo/'tools/vm-stop'),str(v/'vm.pid'),str(disk)],capture_output=True,text=True,timeout=30);(r/'vm-stop.log').write_text(stop.stdout+stop.stderr);result['stop_rc']=stop.returncode
  if stop.returncode:result['rc']=1
 result['ended']=time.time();(r/'vm-result.json').write_text(json.dumps(result,indent=2)+'\n')
raise SystemExit(result['rc'])

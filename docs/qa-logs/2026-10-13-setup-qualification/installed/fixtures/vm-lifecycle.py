from pathlib import Path
import subprocess,json,gzip,hashlib,time,datetime,socket,os
r=Path(__file__).parent;repo=Path('/workspace/repos/rocknix.worktrees/m7-player-setup');facts=json.loads((r/'records/image-size.json').read_text());src=Path(facts['image']);v=r/'vm';raw=v/'disk.img';disk=v/'disk.qcow2';result={'rc':1,'started':time.time(),'boots':[]}
def call(args,**kw):return subprocess.run([str(x) for x in args],check=True,**kw)
def stop():
 p=subprocess.run([str(repo/'tools/vm-stop'),str(v/'vm.pid'),str(disk)],capture_output=True,text=True,timeout=35)
 with (r/'vm-stop.log').open('a') as f:f.write(p.stdout+p.stderr)
 assert p.returncode==0
try:
 for port in [10608,5995]:
  with socket.socket() as s:s.bind(('127.0.0.1',port))
 assert hashlib.file_digest(src.open('rb'),'sha256').hexdigest()==facts['sha256']
 count=0
 with gzip.open(src,'rb') as a,raw.open('xb') as b:
  while chunk:=a.read(4*1024*1024):
   count+=len(chunk)
   if chunk.count(0)==len(chunk):b.seek(len(chunk),1)
   else:b.write(chunk)
  b.truncate()
 assert count==facts['raw_bytes_from_backup_lba']
 call(['qemu-img','convert','-f','raw','-O','qcow2',raw,disk],timeout=90);call(['qemu-img','resize',disk,'16G'],timeout=30);raw.unlink()
 deadline=time.monotonic()+5400
 for size in ['640x480','1280x800']:
  call([repo/'projects/ROCKNIX/devices/GENERIC_X64/vm/generic-x64-vm','run',disk,'--headless','--daemonize','--gl','auto','--res',size,'--ssh-port','10608','--vnc','95','--pidfile',v/'vm.pid','--serial',v/'serial.sock','--monitor',v/'monitor.sock','--ovmf-vars',v/'OVMF.fd'],timeout=60)
  pid=int((v/'vm.pid').read_text());argv=(Path('/proc')/str(pid)/'cmdline').read_bytes().split(b'\0');(r/('qemu-'+size+'.json')).write_text(json.dumps([x.decode() for x in argv if x],indent=2)+'\n')
  call([repo/'tools/vm-serial','--socket',v/'serial.sock','wait','--up-to','240'],timeout=260)
  ready={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'pid':pid,'disk':str(disk),'profile':size,'source_sha256':facts['sha256']};result['boots'].append(ready);(r/('ready-'+size+'.json')).write_text(json.dumps(ready,indent=2)+'\n');print('VM READY '+size,flush=True)
  while not (r/('finish-'+size)).exists():
   if (r/'abort').exists():raise RuntimeError('Coordinator aborted allocation')
   if time.monotonic()>deadline:raise TimeoutError('QA allocation expired')
   assert (Path('/proc')/str(pid)/'cmdline').read_bytes(),'guest exited unexpectedly'
   time.sleep(1)
  stop();print('VM STOPPED '+size,flush=True)
 result['rc']=0
finally:
 if (v/'vm.pid').exists():stop()
 result['ended']=time.time();(r/'vm-result.json').write_text(json.dumps(result,indent=2)+'\n')
raise SystemExit(result['rc'])

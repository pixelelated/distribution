from pathlib import Path
import subprocess,json,gzip,hashlib,time,datetime,socket,tarfile,shutil,shlex,os
r=Path(__file__).parent;repo=Path('/workspace/repos/rocknix.worktrees/m7-player-setup');facts=json.loads((r/'records/image-size.json').read_text());inputs=json.loads((r/'records/inputs.json').read_text());v=r/'vm';src=Path(facts['image']);raw=v/'disk.img';disk=v/'disk.qcow2';result={'rc':1,'started':time.time(),'boots':[]};deadline=time.monotonic()+900

def sha(p):return hashlib.file_digest(p.open('rb'),'sha256').hexdigest()
def call(args,**kw):return subprocess.run([str(x) for x in args],check=True,**kw)
def serial(command):
 p=call([repo/'tools/vm-serial','--socket',v/'serial.sock','--timeout','450','sh',command],capture_output=True,text=True,timeout=455)
 return p.stdout

def monitor(command):
 with socket.socket(socket.AF_UNIX) as s:
  s.settimeout(5);s.connect(str(v/'monitor.sock'));s.recv(65536);s.sendall((command+'\n').encode());data=b''
  while b'(qemu)' not in data:data+=s.recv(65536)
 text=data.decode(errors='replace')
 with (r/'monitor.log').open('a') as f:f.write(command+'\n'+text+'\n')
 assert 'Error' not in text and 'failed' not in text.lower(),text
 return text

def stop():
 p=subprocess.run([str(repo/'tools/vm-stop'),str(v/'vm.pid'),str(disk)],capture_output=True,text=True,timeout=35)
 with (r/'vm-stop.log').open('a') as f:f.write(p.stdout+p.stderr)
 assert p.returncode==0

try:
 with socket.socket() as s:s.bind(('127.0.0.1',5998))
 assert sha(src)==facts['sha256'];assert sha(Path(inputs['helper']['path']))==inputs['helper']['sha256']
 payload=v/'input-tree';payload.mkdir()
 for a in inputs['files']:
  p=Path(a['path']);assert sha(p)==a['sha256'];q=payload/a['destination'];q.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(p,q);assert sha(q)==a['sha256']
 manifest={str(p.relative_to(payload)):sha(p) for p in payload.rglob('*') if p.is_file()};(r/'records/input-files.json').write_text(json.dumps(manifest,indent=2)+'\n');(payload/'input-files.json').write_text(json.dumps(manifest,indent=2)+'\n')
 for name,size,label in [('input',256*1024**2,'PIXINPUT'),('output',256*1024**2,'PIXOUTPUT')]:
  path=v/(name+'.ext4')
  with path.open('xb') as f:f.truncate(size)
  args=['mkfs.ext4','-q','-F','-L',label]
  if name=='input':args+=['-d',payload]
  call([*args,path],timeout=60)
 (r/'records/input-image.json').write_text(json.dumps({'sha256':sha(v/'input.ext4'),'bytes':(v/'input.ext4').stat().st_size},indent=2)+'\n');shutil.rmtree(payload)
 count=0
 with gzip.open(src,'rb') as a,raw.open('xb') as b:
  while chunk:=a.read(4*1024*1024):
   count+=len(chunk)
   if chunk.count(0)==len(chunk):b.seek(len(chunk),1)
   else:b.write(chunk)
  b.truncate()
 assert count==facts['raw_bytes_from_backup_lba']
 call(['qemu-img','convert','-f','raw','-O','qcow2',raw,disk],timeout=90);call(['qemu-img','resize',disk,'16G'],timeout=30);raw.unlink()
 for size in ['640x480']:
  args=[disk,'--no-network','--headless','--daemonize','--gl','auto','--res',size,'--vnc','98','--pidfile',v/'vm.pid','--serial',v/'serial.sock','--monitor',v/'monitor.sock','--ovmf-vars',v/'OVMF.fd']
  gen=call([inputs['helper']['path'],'qemu-args',*args],capture_output=True,text=True,timeout=20)
  command=shlex.split(gen.stdout);assert command.count('-nic')==1 and command[command.index('-nic')+1]=='none';assert '-netdev' not in command and not any('hostfwd=' in s or 'netdev=net0' in s or 'cloud_ssh_port' in s for s in command)
  (r/('generated-'+size+'.json')).write_text(json.dumps(command,indent=2)+'\n')
  call([inputs['helper']['path'],'run',*args],timeout=60)
  pid=int((v/'vm.pid').read_text());actual=[x.decode() for x in (Path('/proc')/str(pid)/'cmdline').read_bytes().split(b'\0') if x];assert actual==command,(actual,command)
  (r/('qemu-'+size+'.json')).write_text(json.dumps(actual,indent=2)+'\n')
  call([repo/'tools/vm-serial','--socket',v/'serial.sock','wait','--up-to','240'],timeout=260)
  topology="import socket,json; from pathlib import Path; a=sorted(n for _,n in socket.if_nameindex()); b=sorted(p.name for p in Path('/sys/class/net').iterdir()); print(json.dumps({'interfaces':a,'sysfs':b,'boot':Path('/proc/sys/kernel/random/boot_id').read_text().strip()})); assert a==b==['lo']"
  out=serial('python3 -I -S -B -c '+shlex.quote(topology)+'; pxrc=$?; printf "PIX_TOPOLOGY_RC:%s\\n" "$pxrc"');(r/('topology-'+size+'.txt')).write_text(out);assert 'PIX_TOPOLOGY_RC:0' in out,out
  for name in ['input','output']:
   monitor('drive_add 0 if=none,id=pix'+name+',format=raw,'+('readonly=on,' if name=='input' else '')+'file='+str(v/(name+'.ext4')))
   monitor('device_add usb-storage,drive=pix'+name+',id=pix'+name+'dev,serial=pix'+name)
  command='for i in 1 2 3 4 5; do test -e /dev/disk/by-label/PIXOUTPUT && break; sleep 1; done; mkdir -p /tmp/pix-input /tmp/pix-output; mount -t ext4 -o ro,noload /dev/disk/by-label/PIXINPUT /tmp/pix-input && mount -t ext4 /dev/disk/by-label/PIXOUTPUT /tmp/pix-output; pxrc=$?; printf "PIX_MEDIA_RC:%s\\n" "$pxrc"'
  out=serial(command);(r/('media-'+size+'.txt')).write_text(out);assert 'PIX_MEDIA_RC:0' in out,out
  ready={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'pid':pid,'disk':str(disk),'profile':size,'source_sha256':facts['sha256'],'no_network':True,'deadline_epoch':time.time()+max(0,deadline-time.monotonic())};result['boots'].append(ready);(r/('ready-'+size+'.json')).write_text(json.dumps(ready,indent=2)+'\n');print('OFFLINE VM READY '+size,flush=True)
  command=(r/'run-guest.sh').read_text()
  out=serial('( '+command+'\n ); pxrc=$?; printf "PIX566_QA_RC:%s\\n" "$pxrc"')
  (r/'qa-serial.txt').write_text(out)
  assert 'PIX566_QA_RC:0' in out,out
  print(out,flush=True)
  out=serial('sync; umount /tmp/pix-output; pxrc=$?; sync; printf "PIX_UNMOUNT_RC:%s\\n" "$pxrc"');(r/('unmount-'+size+'.txt')).write_text(out);assert 'PIX_UNMOUNT_RC:0' in out,out
  stop();print('OFFLINE VM STOPPED '+size,flush=True)
 result['rc']=0
finally:
 if (v/'vm.pid').exists():stop()
 result['ended']=time.time();(r/'vm-result.json').write_text(json.dumps(result,indent=2)+'\n')
raise SystemExit(result['rc'])

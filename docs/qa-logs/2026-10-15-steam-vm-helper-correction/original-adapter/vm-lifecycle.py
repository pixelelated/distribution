from pathlib import Path
import subprocess,json,gzip,hashlib,time,datetime,socket,tarfile,shutil,shlex,os,signal,fcntl
r=Path(__file__).parent;runtime=json.loads((r/'records/runtime.json').read_text());repo=Path(runtime['checkout']);facts=json.loads((r/'records/image-size.json').read_text());inputs=json.loads((r/'records/inputs.json').read_text());v=r/'vm';src=Path(facts['image']);raw=v/'disk.img';disk=v/'disk.qcow2';result={'rc':1,'started':time.time(),'boots':[]};deadline=time.monotonic()+3600

def sha(p):
 h=hashlib.sha256()
 with p.open('rb') as f:
  for block in iter(lambda:f.read(4*1024**2),b''):h.update(block)
 return h.hexdigest()
def call(args,**kw):return subprocess.run([str(x) for x in args],check=True,**kw)
def serial(command, seconds=30, evidence=None):
 with (r/'serial.lock').open('a') as lock:
  fcntl.flock(lock,fcntl.LOCK_EX)
  argv=[str(repo/'tools/vm-serial'),'--socket',str(v/'serial.sock'),'--timeout',str(seconds),'sh',command]
  try:p=subprocess.run(argv,capture_output=True,text=True,timeout=seconds+5)
  except subprocess.TimeoutExpired as exc:
   if evidence is not None:
    (evidence/'serial.stdout').write_text((exc.stdout or b'').decode(errors='replace') if isinstance(exc.stdout,bytes) else (exc.stdout or ''))
    (evidence/'serial.stderr').write_text((exc.stderr or b'').decode(errors='replace') if isinstance(exc.stderr,bytes) else (exc.stderr or ''))
    (evidence/'serial-result.json').write_text(json.dumps({'original_exit':None,'timeout':True,'command':command},indent=2)+'\n')
   raise
  if evidence is not None:
   (evidence/'serial.stdout').write_text(p.stdout);(evidence/'serial.stderr').write_text(p.stderr)
   (evidence/'serial-result.json').write_text(json.dumps({'original_exit':p.returncode,'timeout':False,'command':command},indent=2)+'\n')
  assert p.returncode==0, 'Original serial tool failed: '+str(p.returncode)
 return p.stdout

def monitor(command):
 with (r/'serial.lock').open('a') as lock:
  fcntl.flock(lock,fcntl.LOCK_EX)
  return monitor_locked(command)

def monitor_locked(command):
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

def expired(signum,frame):raise TimeoutError('VM lifecycle deadline or termination')
signal.signal(signal.SIGALRM,expired)
signal.signal(signal.SIGTERM,expired)
signal.alarm(3600)

try:
 assert all(sha(repo/name)==h for name,h in runtime['tool_hashes'].items())
 with socket.socket() as s:s.bind(('127.0.0.1',5900+runtime['vnc']))
 assert sha(src)==facts['sha256'];assert sha(Path(inputs['helper']['path']))==inputs['helper']['sha256']
 payload=v/'input-tree';payload.mkdir()
 for a in inputs['files']:
  p=Path(a['path']);assert sha(p)==a['sha256'];q=payload/a['destination'];q.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(p,q);assert sha(q)==a['sha256']
 manifest={str(p.relative_to(payload)):sha(p) for p in payload.rglob('*') if p.is_file()};(r/'records/input-files.json').write_text(json.dumps(manifest,indent=2)+'\n');(payload/'input-files.json').write_text(json.dumps(manifest,indent=2)+'\n')
 for name,size,label in [('input',256*1024**2,'PIXINPUT'),('output',1280*1024**2,'PIXOUTPUT')]:
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
   assert count<=facts['raw_bytes_from_backup_lba']<=16*1024**3
   if chunk.count(0)==len(chunk):b.seek(len(chunk),1)
   else:b.write(chunk)
  b.truncate()
 assert count==facts['raw_bytes_from_backup_lba']
 call(['qemu-img','convert','-f','raw','-O','qcow2',raw,disk],timeout=90);call(['qemu-img','resize',disk,'16G'],timeout=30);raw.unlink()
 for size in ['640x480']:
  args=[disk,'--no-network','--headless','--daemonize','--gl','auto','--res',size,'--vnc',str(runtime['vnc']),'--pidfile',v/'vm.pid','--serial',v/'serial.sock','--monitor',v/'monitor.sock','--ovmf-vars',v/'OVMF.fd']
  gen=call([inputs['helper']['path'],'qemu-args',*args],capture_output=True,text=True,timeout=20)
  command=shlex.split(gen.stdout);assert command.count('-nic')==1 and command[command.index('-nic')+1]=='none';assert '-netdev' not in command and not any('hostfwd=' in s or 'netdev=net0' in s or 'cloud_ssh_port' in s for s in command)
  (r/('generated-'+size+'.json')).write_text(json.dumps(command,indent=2)+'\n')
  call([inputs['helper']['path'],'run',*args],timeout=60)
  pid=int((v/'vm.pid').read_text());actual=[x.decode() for x in (Path('/proc')/str(pid)/'cmdline').read_bytes().split(b'\0') if x];assert actual==command,(actual,command)
  assert actual[actual.index('-m')+1]=='8192' and actual[actual.index('-smp')+1]=='4'
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
  result['stages']=[]
  for index,case in enumerate(runtime['cases'],1):
   assert time.monotonic()+180+90<deadline, 'Not enough remaining family budget; stop before case'
   folder=r/'stages'/f'{index:02d}-{case}';folder.mkdir()
   command='python3 -I -S -B /tmp/pix-input/guest-stage.py --case '+shlex.quote(case)
   started=time.monotonic()
   print('PIX582 START ORIGINAL STAGE '+case,flush=True)
   out=serial(command+'; pxrc=$?; printf "PIX582_STAGE_RC:%s\\n" "$pxrc"',seconds=180,evidence=folder)
   (folder/'serial.txt').write_text(out)
   observations=[json.loads(line.split('PIX582_STAGE_RESULT:',1)[1]) for line in out.splitlines() if line.startswith('PIX582_STAGE_RESULT:')]
   row={'case':case,'elapsed_seconds':time.monotonic()-started,'guest_result':observations,'original_serial_rc':0}
   (folder/'host-result.json').write_text(json.dumps(row,indent=2)+'\n');result['stages'].append(row)
   assert 'PIX582_STAGE_RC:0' in out and len(observations)==1
   observed=observations[0]
   assert observed['case']==case and observed['status']=='PASS' and observed['restored'] is True and observed['original_wrapper_exit']==0
   print('PIX582 CONSUMED ORIGINAL STAGE '+case+' PASS; restoration verified',flush=True)
  out=serial('sync; umount /tmp/pix-output; pxrc=$?; sync; printf "PIX_UNMOUNT_RC:%s\\n" "$pxrc"');(r/('unmount-'+size+'.txt')).write_text(out);assert 'PIX_UNMOUNT_RC:0' in out,out
  stop();print('OFFLINE VM STOPPED '+size,flush=True)
 result['rc']=0
except BaseException as exc:
 result['error']=repr(exc)
finally:
 signal.alarm(0)
 if (v/'vm.pid').exists():
  try:
   sealed=serial('python3 -I -S -B /tmp/pix-input/guest-stage.py --seal-output; pxrc=$?; printf "PIX_SEAL_RC:%s\\n" "$pxrc"',seconds=20)
   (r/'finally-seal.txt').write_text(sealed)
   if 'PIX_SEAL_RC:0' not in sealed:result['rc']=1
   flushed=serial('sync; if grep -q " /tmp/pix-output " /proc/mounts; then umount /tmp/pix-output; fi; pxrc=$?; printf "PIX_FINALLY_FLUSH_RC:%s\\n" "$pxrc"',seconds=15)
   (r/'finally-flush.txt').write_text(flushed)
   if 'PIX_FINALLY_FLUSH_RC:0' not in flushed:result['rc']=1
  except Exception as exc:
   result['rc']=1;result['flush_error']=str(exc)
  finally:
   try:stop()
   except Exception as exc:result['rc']=1;result['stop_error']=repr(exc)
 result['ended']=time.time();(r/'vm-result.json').write_text(json.dumps(result,indent=2)+'\n')
raise SystemExit(result['rc'])

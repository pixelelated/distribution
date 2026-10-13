from pathlib import Path
import subprocess,json,time,hashlib,shlex
r=Path(__file__).parent;repo=Path('/workspace/repos/rocknix.worktrees/m7-player-setup');key=r/'vm/qa-key';res={'rc':1,'started':time.time()}
try:
 assert (r/'vm-ready.json').exists()
 subprocess.run(['ssh-keygen','-q','-t','ed25519','-N','','-f',str(key),'-C','pix570-comparison'],check=True)
 pub=key.with_name(key.name+'.pub').read_text().strip()
 cmd="mkdir -p /storage/.ssh; chmod 700 /storage/.ssh; echo "+shlex.quote(pub)+" >> /storage/.ssh/authorized_keys; chmod 600 /storage/.ssh/authorized_keys"
 subprocess.run([str(repo/'tools/vm-serial'),'--socket',str(r/'vm/serial.sock'),'sh',cmd],check=True,timeout=30)
 keys=subprocess.check_output(['ssh-keyscan','-p','10604','127.0.0.1'],stderr=subprocess.DEVNULL,timeout=15);(r/'vm/known_hosts').write_bytes(keys)
 ssh=['ssh','-i',str(key),'-p','10604','-o','BatchMode=yes','-o','ConnectTimeout=8','-o','StrictHostKeyChecking=yes','-o','UserKnownHostsFile='+str(r/'vm/known_hosts'),'root@127.0.0.1'];(r/'ssh-command.json').write_text(json.dumps(ssh)+'\n')
 def remote(c,**kw):return subprocess.run(ssh+[c],check=True,timeout=30,**kw)
 def out(c):return remote(c,capture_output=True,text=True).stdout
 boot=out('cat /proc/sys/kernel/random/boot_id').strip()
 deadline=time.monotonic()+90
 while True:
  props=dict(x.split('=',1) for x in out('systemctl show rocknix-autostart.service -p ActiveState -p Result -p ExecMainStatus -p ExecMainStartTimestampMonotonic').splitlines())
  idle=subprocess.run(ssh+['curl -fsS http://127.0.0.1:1234/isIdle'],capture_output=True,text=True,timeout=8)
  if props.get('Result')=='success' and props.get('ActiveState')=='active' and props.get('ExecMainStatus')=='0' and int(props.get('ExecMainStartTimestampMonotonic','0'))>0 and idle.returncode==0 and json.loads(idle.stdout)==[True]:break
  if time.monotonic()>deadline:raise RuntimeError('current boot not ready')
  time.sleep(1)
 assert boot==out('cat /proc/sys/kernel/random/boot_id').strip()
 remote('mkdir -p /storage/qa570compare; cp /usr/bin/emulationstation /storage/qa570compare/baseline',capture_output=True)
 facts=json.loads((r/'records/candidate.json').read_text());candidate=Path(facts['path']);assert hashlib.file_digest(candidate.open('rb'),'sha256').hexdigest()==facts['sha256']
 for src,dst in [(candidate,'candidate'),(r/'sampler.py','sampler.py')]:
  with src.open('rb') as f:remote('cat > /storage/qa570compare/'+dst,stdin=f,capture_output=True)
 remote('chmod 755 /storage/qa570compare/candidate',capture_output=True)
 hashes={line.split()[1]:line.split()[0] for line in out('sha256sum /storage/qa570compare/baseline /storage/qa570compare/candidate /usr/bin/cloud_oauth /usr/bin/cloud-signin-window /usr/bin/rclone').splitlines()}
 assert hashes['/storage/qa570compare/baseline']=='db136580f0a46442bb3fe7ac9e31606b38b816c78efc8f9b4e267284daca6502'
 assert hashes['/storage/qa570compare/candidate']==facts['sha256']
 assert hashes['/usr/bin/cloud-signin-window']=='6cbc445686d3d484ff20450342776e9eb92b47f6112a0352be1a50b334eef81b'
 actual=out("cat /proc/meminfo; dmesg | grep -E 'Memory:|reserved|cma:'; grep -iE 'renderer|opengl' /var/log/es_log.txt; getconf CLK_TCK")
 (r/'guest-platform.txt').write_text(actual)
 res.update(rc=0,boot=boot,autostart=props,idle=[True],hashes=hashes)
 print('Current boot ready; actual binaries and constrained guest platform recorded',flush=True)
finally:
 res['ended']=time.time();(r/'setup-result.json').write_text(json.dumps(res,indent=2)+'\n')

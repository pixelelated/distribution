from pathlib import Path
import subprocess,json,time,hashlib
r=Path(__file__).parent;repo=Path('/workspace/repos/rocknix.worktrees/m7-player-setup');assert (r/'vm-ready.json').exists();key=r/'vm/qa-key'
subprocess.run(['ssh-keygen','-q','-t','ed25519','-N','','-f',str(key),'-C','pix570-product-fixture'],check=True)
pub=key.with_name(key.name+'.pub').read_text().strip();subprocess.run([str(repo/'tools/vm-serial'),'--socket',str(r/'vm/serial.sock'),'sh',"mkdir -p /storage/.ssh; chmod 700 /storage/.ssh; echo '"+pub+"' >> /storage/.ssh/authorized_keys; chmod 600 /storage/.ssh/authorized_keys"],check=True)
keys=subprocess.check_output(['ssh-keyscan','-p','10602','127.0.0.1'],stderr=subprocess.DEVNULL);(r/'vm/known_hosts').write_bytes(keys)
ssh=['ssh','-i',str(key),'-p','10602','-o','BatchMode=yes','-o','ConnectTimeout=8','-o','StrictHostKeyChecking=yes','-o','UserKnownHostsFile='+str(r/'vm/known_hosts'),'root@127.0.0.1'];(r/'ssh-command.json').write_text(json.dumps(ssh)+'\n')
def remote(c,**kw):return subprocess.run(ssh+[c],check=True,timeout=30,**kw)
def out(c):return remote(c,capture_output=True,text=True).stdout
ready=out('systemctl is-active autostart.service; systemctl show autostart.service -p Result; cat /proc/sys/kernel/random/boot_id');assert 'active' in ready and 'Result=success' in ready
remote('mkdir -p /storage/qa570product; sha256sum /usr/bin/emulationstation /usr/bin/cloud_oauth /usr/bin/cloud-signin-window; cp /usr/bin/rclone /storage/qa570product/rclone-original',stdout=(r/'vm-original-identities.txt').open('w'))
for src,dst in [(r/'scratch/emulationstation','/storage/qa570product/emulationstation'),(r/'fake-rclone','/storage/qa570product/rclone-fixture')]:
 with src.open('rb') as f:remote('cat > '+dst,stdin=f)
expected=hashlib.sha256((r/'scratch/emulationstation').read_bytes()).hexdigest();assert out('sha256sum /storage/qa570product/emulationstation').split()[0]==expected
remote('chmod 755 /storage/qa570product/emulationstation /storage/qa570product/rclone-fixture; mount --bind /storage/qa570product/emulationstation /usr/bin/emulationstation; mount --bind /storage/qa570product/rclone-fixture /usr/bin/rclone; systemctl restart essway.service',capture_output=True)
deadline=time.monotonic()+50
while time.monotonic()<deadline:
 p=subprocess.run(ssh+['curl -fsS http://127.0.0.1:1234/isIdle'],capture_output=True,text=True,timeout=5)
 if p.returncode==0 and json.loads(p.stdout)==[True]:break
 time.sleep(1)
else:raise RuntimeError('frontend not idle')
actual=out('sha256sum /proc/$(pidof emulationstation)/exe; systemctl is-active essway.service; cat /proc/sys/kernel/random/boot_id; pidof emulationstation');assert actual.split()[0]==expected
(r/'vm-installed-identities.txt').write_text(actual);(r/'provision-result.json').write_text(json.dumps({'rc':0,'candidate_sha256':expected,'ready':ready,'runtime':actual},indent=2)+'\n');print('Actual candidate running; frontend idle and ready')

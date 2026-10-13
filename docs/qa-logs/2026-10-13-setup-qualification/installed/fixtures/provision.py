from pathlib import Path
import subprocess,json,time,hashlib
r=Path(__file__).parent;repo=Path('/workspace/repos/rocknix.worktrees/m7-player-setup');key=r/'vm/qa-key'
def run(args,**kw):return subprocess.run(args,check=True,timeout=30,**kw)
if not key.exists():
 run(['ssh-keygen','-q','-t','ed25519','-N','','-f',str(key),'-C','pix570-flows-fixture'])
 pub=key.with_name(key.name+'.pub').read_text().strip();run([str(repo/'tools/vm-serial'),'--socket',str(r/'vm/serial.sock'),'sh',"mkdir -p /storage/.ssh; chmod 700 /storage/.ssh; echo '"+pub+"' >> /storage/.ssh/authorized_keys; chmod 600 /storage/.ssh/authorized_keys"],capture_output=True)
keys=subprocess.check_output(['ssh-keyscan','-p','10608','127.0.0.1'],stderr=subprocess.DEVNULL);(r/'vm/known_hosts').write_bytes(keys)
ssh=['ssh','-i',str(key),'-p','10608','-o','BatchMode=yes','-o','ConnectTimeout=8','-o','StrictHostKeyChecking=yes','-o','UserKnownHostsFile='+str(r/'vm/known_hosts'),'root@127.0.0.1'];(r/'ssh-command.json').write_text(json.dumps(ssh)+'\n')
def remote(c,**kw):return run(ssh+[c],**kw)
def out(c):return remote(c,capture_output=True,text=True).stdout
ready=out('cat /proc/sys/kernel/random/boot_id; systemctl show rocknix-autostart.service -p ActiveState -p Result -p ExecMainStatus -p ExecMainStartTimestampMonotonic');assert 'ActiveState=active\n' in ready and 'Result=success\n' in ready and 'ExecMainStatus=0\n' in ready
assert int(next(x.split('=')[1] for x in ready.splitlines() if x.startswith('ExecMainStartTimestampMonotonic=')))>0
remote('mkdir -p /storage/qa570flows; cp /usr/bin/rclone /storage/qa570flows/rclone-original; sha256sum /usr/bin/emulationstation /usr/bin/cloud_oauth /usr/bin/cloud-signin-window /usr/bin/rclone',stdout=(r/'original-identities.txt').open('w'))
facts=json.loads((r/'records/candidate.json').read_text())
for src,name in [(Path(facts['path']),'emulationstation'),(r/'fake-rclone','rclone-fixture'),(r/'browser-fail','browser-fail')]:
 with src.open('rb') as f:remote('cat > /storage/qa570flows/'+name,stdin=f)
for lang in ['fr','en_GB']:
 target='/storage/.config/locale/'+lang+'/LC_MESSAGES/emulationstation2.mo'
 remote('mkdir -p '+target.rsplit('/',1)[0],capture_output=True)
 with Path('/workspace/tmp/pix-m7-setup-build-20261013/scratch/'+lang+'.mo').open('rb') as f:remote('cat > '+target,stdin=f)
 assert out('sha256sum '+target).split()[0]==facts['catalogs'][lang]
remote('chmod 755 /storage/qa570flows/emulationstation /storage/qa570flows/rclone-fixture /storage/qa570flows/browser-fail; systemctl stop essway.service; mount --bind /storage/qa570flows/emulationstation /usr/bin/emulationstation; mount --make-private /usr/bin/emulationstation; mount --bind /storage/qa570flows/rclone-fixture /usr/bin/rclone; mount --make-private /usr/bin/rclone; systemctl start essway.service',capture_output=True)
end=time.monotonic()+60
while time.monotonic()<end:
 p=subprocess.run(ssh+['curl -fsS http://127.0.0.1:1234/isIdle'],capture_output=True,text=True,timeout=5)
 if p.returncode==0 and json.loads(p.stdout)==[True]:break
 time.sleep(1)
else:raise RuntimeError('frontend not idle')
actual=out('sha256sum /proc/$(pidof emulationstation)/exe; cat /proc/sys/kernel/random/boot_id; pidof emulationstation');assert actual.split()[0]==facts['sha256']
(r/'provision-result.json').write_text(json.dumps({'rc':0,'readiness':ready,'actual':actual},indent=2)+'\n');print('Candidate ready; identities and actual autostart verified')

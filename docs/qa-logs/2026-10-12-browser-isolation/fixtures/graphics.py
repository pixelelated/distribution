from pathlib import Path
import subprocess,json,shlex,time
r=Path(__file__).parent
ssh=['ssh','-i',str(r/'qa-key'),'-p','10570','-o','BatchMode=yes','-o','ConnectTimeout=8','-o','StrictHostKeyChecking=yes','-o','UserKnownHostsFile='+str(r/'known_hosts'),'root@127.0.0.1']
assert json.loads((r/'gst-owner/launcher-result.json').read_text())['runner_returncode']==0
# The sampler is on /tmp; upload after the graphics-only reboot.
subprocess.run(ssh+['sync'],check=True,timeout=20)
subprocess.run(['tools/vm-stop',str(r/'vm.pid'),str(r/'disk.qcow2')],check=True)
args=['python3',str(r/'lowmem-vm.py'),'run',str(r/'disk.qcow2'),'--headless','--daemonize','--gl','auto','--res','640x480','--ssh-port','10570','--vnc','57','--pidfile',str(r/'vm.pid'),'--serial',str(r/'serial.sock'),'--monitor',str(r/'monitor.sock'),'--ovmf-vars',str(r/'OVMF.fd')]
subprocess.run(args,check=True)
subprocess.run(['tools/vm-serial','--socket',str(r/'serial.sock'),'wait','--up-to','240'],check=True)
pid=int((r/'vm.pid').read_text());(r/'graphics-qemu.json').write_text(json.dumps({'pid':pid,'args':(Path('/proc')/str(pid)/'cmdline').read_bytes().decode().split('\0')},indent=2))
with (r/'measure.py').open('rb') as f:subprocess.run(ssh+['cat > /tmp/pressure-measure.py'],stdin=f,check=True)
case='public-virgl';spec=json.dumps([case,'/usr/bin/cloud-signin-window','https://www.dropbox.com/login',150,{}]);print('START '+case,flush=True)
with (r/(case+'.json')).open('wb') as out,(r/(case+'.stderr')).open('wb') as err:p=subprocess.run(ssh+['python3 /tmp/pressure-measure.py '+shlex.quote(spec)],stdout=out,stderr=err,timeout=220)
(r/'graphics-result.json').write_text(json.dumps({'rc':p.returncode}));assert p.returncode==0
x=json.loads((r/(case+'.json')).read_text())
for f in x['frames']:
 with (r/(case+'-'+Path(f['file']).name)).open('wb') as out:subprocess.run(ssh+['cat '+shlex.quote(f['file'])],stdout=out,check=True)
print('GRAPHICS COMPARISON COMPLETE',flush=True)

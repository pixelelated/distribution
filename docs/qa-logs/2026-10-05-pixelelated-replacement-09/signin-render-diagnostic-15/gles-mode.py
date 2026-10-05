from pathlib import Path
import subprocess,json,datetime,time,hashlib
owner=Path(__file__).parent;out=owner/'artifacts'
ssh=['ssh','-i',str(owner/'pair/qa-key'),'-p','10026','-o','BatchMode=yes','-o','ConnectTimeout=8','-o','StrictHostKeyChecking=no','-o','UserKnownHostsFile=/dev/null','-o','LogLevel=ERROR','root@127.0.0.1']
def guest(cmd,**kw):return subprocess.run(ssh+[cmd],check=True,capture_output=True,timeout=kw.pop('timeout',60),**kw).stdout
pid=int((owner/'guest.pid').read_text());args=[x.decode() for x in (Path('/proc')/str(pid)/'cmdline').read_bytes().split(b'\0') if x]
assert any(x.startswith('virtio-gpu-pci,') for x in args) and not any('virtio-gpu-gl' in x for x in args)
(out/'actual-gl.json').write_text(json.dumps({'pid':pid,'args':args,'mode':'software'},indent=2)+'\n')
(out/'sway-before.log').write_bytes(guest('cat /var/log/sway.log'))
wrapper=guest('cat /usr/bin/sway.sh');assert hashlib.sha256(wrapper).hexdigest()==hashlib.sha256(Path('/workspace/tmp/pixelelated-m7-image-11/root/usr/bin/sway.sh').read_bytes()).hexdigest()
assert wrapper.count(b'/usr/bin/sway -V ')==1
changed=wrapper.replace(b'/usr/bin/sway -V ',b'/usr/bin/sway -d ')
guest('test ! -e /tmp/m7-sway-debug.sh && cat > /tmp/m7-sway-debug.sh',input=changed)
guest('systemctl stop essway sway; mkdir -p /run/systemd/system/sway.service.d')
drop=b'[Service]\nEnvironment=WLR_RENDERER=gles2\nExecStart=\nExecStart=/bin/sh /tmp/m7-sway-debug.sh\n'
guest('cat > /run/systemd/system/sway.service.d/99-m7-gles.conf',input=drop)
guest('systemctl daemon-reload && systemctl start sway')
for _ in range(40):
 log=guest('cat /var/log/sway.log');(out/'sway-selected-mode.log').write_bytes(log)
 if b'GL renderer: llvmpipe' in log:break
 time.sleep(.5)
else:raise RuntimeError('selected GLES2/llvmpipe renderer absent')
code="""from pathlib import Path
import json
rows=[]
for p in Path('/proc').glob('[0-9]*/cmdline'):
 try:
  args=p.read_bytes().split(b'\\0')
  if not args[0].endswith(b'/sway'):continue
  env=dict(x.split(b'=',1) for x in (p.parent/'environ').read_bytes().split(b'\\0') if b'=' in x)
  rows.append({'pid':int(p.parent.name),'argv':[x.decode() for x in args if x],'graphics_env':{k.decode():v.decode() for k,v in env.items() if k.startswith((b'WLR_',b'LIBGL_',b'MESA_',b'GALLIUM_'))}})
 except OSError:pass
assert len(rows)==1 and rows[0]['graphics_env'].get('WLR_RENDERER')=='gles2',rows
print(json.dumps(rows,indent=2))
"""
actual=guest('python3 -',input=code.encode());(out/'actual-compositor.json').write_bytes(actual)
(out/'kernel-graphics.log').write_bytes(guest('dmesg | grep -i -E "drm|virtio|gpu|frame|fence"'))
guest('systemctl start essway')
for _ in range(90):
 r=subprocess.run(ssh+['curl -sS -m 3 http://127.0.0.1:1234/isIdle'],capture_output=True,text=True)
 if r.returncode==0 and r.stdout.strip() and json.loads(r.stdout)==[True]:break
 time.sleep(1)
else:raise RuntimeError('interface did not become idle after diagnostic restart')
print('PASS runtime-only GLES2/llvmpipe renderer selected in actual compositor; debug log and software QEMU argv retained',flush=True)

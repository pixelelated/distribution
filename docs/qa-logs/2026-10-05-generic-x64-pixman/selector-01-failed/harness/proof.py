from pathlib import Path
import subprocess,sys,json,hashlib
owner=Path(__file__).parent;mode=sys.argv[1]
ssh=['ssh','-i',str(owner/'pair/qa-key'),'-p','10026','-o','BatchMode=yes','-o','ConnectTimeout=8','-o','StrictHostKeyChecking=no','-o','UserKnownHostsFile=/dev/null','-o','LogLevel=ERROR','root@127.0.0.1']
pid=int((owner/('guest.pid' if mode=='software' else 'guest-virgl.pid')).read_text())
args=(Path('/proc')/str(pid)/'cmdline').read_bytes().split(b'\0')
assert any(x.startswith(b'virtio-gpu-pci,' if mode=='software' else b'virtio-gpu-gl-pci,') for x in args)
(owner/'artifacts'/('qemu-'+mode+'.json')).write_text(json.dumps([x.decode() for x in args if x],indent=2)+'\n')
for name in ['sway-generic-x64','selector-controls.py']:
 subprocess.run(ssh+['cat > /tmp/'+name],input=(owner/name).read_bytes(),check=True)
r=subprocess.run(ssh+['python3 /tmp/selector-controls.py /tmp/sway-generic-x64 '+mode],capture_output=True,text=True,timeout=120)
(owner/'artifacts'/('controls-'+mode+'.log')).write_text(r.stdout+r.stderr);print(r.stdout,flush=True);assert r.returncode==0,(r.returncode,r.stderr)
r=subprocess.run(ssh+['cat /tmp/pixman-selector-results.json'],capture_output=True,check=True)
(owner/'artifacts'/('controls-'+mode+'.json')).write_bytes(r.stdout)

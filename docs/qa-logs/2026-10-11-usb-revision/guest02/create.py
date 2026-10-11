#!/usr/bin/env python3
"""Create only the isolated #531 USB fixture guest; never contacts a handheld."""
import gzip, hashlib, json, os, pathlib, shutil, socket, subprocess, time
O = pathlib.Path('/workspace/tmp/pixelelated-m7-usb-531-02')
R = pathlib.Path('/workspace/repos/rocknix.worktrees/m7-p5-usb-revision')
B = pathlib.Path('/workspace/artifacts/pixelelated-candidates/sha256/f557176651026f59bb5931993b12491a6019c0383321fb89fa1a05a596514fe6')
def run(a, **kw):
    return subprocess.run(a, check=True, timeout=240, **kw)
def dump(name, obj):
    (O/name).write_text(json.dumps(obj, indent=2)+'\n')
m = json.loads((B/'manifest.json').read_text())
assert m['inputs']['distribution_commit'] == '7f58b7b1c592908dcd0ba5987955e59aaa79fe66'
assert m['inputs']['emulationstation_commit'] == '1d76b3da7da75794066df1c089931b890304da7a'
name = 'pixelelated-GENERIC_X64.x86_64-0.0.1-from-ROCKNIX.img.gz'
img = B/name
for port in (10331, 5993):
    with socket.socket() as s: s.bind(('127.0.0.1', port))
for f in ('/tmp/pix531-01-ser.sock', '/tmp/pix531-01-mon.sock'):
    assert not pathlib.Path(f).exists(), f
start = time.monotonic()
with img.open('rb') as f: digest = hashlib.file_digest(f, 'sha256').hexdigest()
assert digest == m['files'][name]['sha256']
print('Image hash verified; converting fresh disposable disk', flush=True)
with gzip.open(img, 'rb') as src, (O/'image.img').open('xb') as dst:
    shutil.copyfileobj(src, dst, 2**20)
run(['qemu-img','convert','-f','raw','-O','qcow2',str(O/'image.img'),str(O/'vm.qcow2')])
run(['qemu-img','resize',str(O/'vm.qcow2'),'16G'])
(O/'image.img').unlink()
run(['ssh-keygen','-q','-t','ed25519','-N','','-f',str(O/'qa-key'),'-C','pixelelated-531-synthetic'])
cmd = [str(R/'projects/ROCKNIX/devices/GENERIC_X64/vm/generic-x64-vm'),'run','--headless','--daemonize','--gl','auto','--res','640x480','--ssh-port','10331','--vnc','93','--monitor','/tmp/pix531-01-mon.sock','--serial','/tmp/pix531-01-ser.sock','--pidfile',str(O/'vm.pid'),'--mac','52:54:00:53:01:01',str(O/'vm.qcow2')]
run(cmd)
serial = [str(R/'tools/vm-serial'),'--socket','/tmp/pix531-01-ser.sock']
run(serial+['wait','--up-to','180'])
pub = (O/'qa-key.pub').read_text().strip()
run(serial+['sh',"mkdir -p /storage/.ssh && chmod 700 /storage/.ssh && printf '%s\\n' '"+pub+"' > /storage/.ssh/authorized_keys && chmod 600 /storage/.ssh/authorized_keys"], stdout=subprocess.DEVNULL)
ssh = ['ssh','-i',str(O/'qa-key'),'-p','10331','-o','LogLevel=ERROR','-o','StrictHostKeyChecking=no','-o','UserKnownHostsFile=/dev/null','-o','BatchMode=yes','-o','ConnectTimeout=5','root@127.0.0.1']
for _ in range(30):
    ready = subprocess.run(ssh+['grep ^BUILD_ID= /etc/os-release'],capture_output=True,text=True)
    if ready.returncode == 0: break
    time.sleep(2)
else: raise RuntimeError('guest SSH unavailable')
assert m['inputs']['distribution_commit'] in ready.stdout
with (O/'network-boundary.txt').open('w') as f:
    run(ssh+['ip route replace blackhole 0.0.0.0/1 && ip route replace blackhole 128.0.0.0/1 && ip -6 route replace blackhole ::/1 && ip -6 route replace blackhole 8000::/1 && ip route && ip -6 route'], stdout=f)
source = R/'projects/ROCKNIX/packages/rocknix/sources/scripts/usbgadget'
old = subprocess.check_output(['git','-C',str(R),'show','HEAD:projects/ROCKNIX/packages/rocknix/sources/scripts/usbgadget'])
actual = subprocess.check_output(ssh+['sha256sum /usr/bin/usbgadget'],text=True).split()[0]
assert actual == hashlib.sha256(old).hexdigest(), (actual, hashlib.sha256(old).hexdigest())
dump('installed-source.json', {'/usr/bin/usbgadget': {'sha256':actual,'source_base':'1fd36fcd26','role':'old control'}})
dump('guest.json', {'command':cmd,'image_sha256':digest,'distribution':m['inputs']['distribution_commit'],'es_source':m['inputs']['emulationstation_commit'],'qemu_pid':int((O/'vm.pid').read_text()),'elapsed_seconds':round(time.monotonic()-start,3),'protected_by_blackhole_routes':True,'credentials':'synthetic SSH key only; exclude from packet'})
print('PASS isolated current-source guest ready; no personal credentials or data imported', flush=True)

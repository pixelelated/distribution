#!/usr/bin/env python3
"""Create only the synthetic #519 old-source guest; never contacts a handheld."""
import gzip, hashlib, json, os, pathlib, shutil, socket, subprocess, time
O = pathlib.Path('/workspace/tmp/pixelelated-m7-alignment-runtime-01')
R = pathlib.Path('/workspace/repos/rocknix.worktrees/conflict-resolution')
B = pathlib.Path('/workspace/artifacts/pixelelated-candidates/sha256/7f98f2d22985d11fe9c150015457894caf460104c9ce44abd16074167f23815a')
def run(a, **kw):
    return subprocess.run(a, check=True, **kw)
def dump(name, obj):
    (O/name).write_text(json.dumps(obj, indent=2)+'\n')
m = json.loads((B/'manifest.json').read_text())
assert m['inputs']['distribution_commit'] == 'ee014909137e03706e0b3020b8396be589aaa705'
assert m['inputs']['emulationstation_commit'] == '72494bc72e3d64d4dcfeb4e6478052bbdf166c5b'
name = 'pixelelated-GENERIC_X64.x86_64-0.0.1-from-ROCKNIX.img.gz'
img = B/name
for port in (10251, 5971):
    with socket.socket() as s: s.bind(('127.0.0.1', port))
for f in ('/tmp/pix519-01-ser.sock', '/tmp/pix519-01-mon.sock'):
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
run(['ssh-keygen','-q','-t','ed25519','-N','','-f',str(O/'qa-key'),'-C','pixelelated-519-synthetic'])
cmd = [str(R/'projects/ROCKNIX/devices/GENERIC_X64/vm/generic-x64-vm'),'run','--headless','--daemonize','--gl','auto','--res','640x480','--ssh-port','10251','--vnc','71','--monitor','/tmp/pix519-01-mon.sock','--serial','/tmp/pix519-01-ser.sock','--pidfile',str(O/'vm.pid'),'--mac','52:54:00:52:05:19',str(O/'vm.qcow2')]
run(cmd)
serial = [str(R/'tools/vm-serial'),'--socket','/tmp/pix519-01-ser.sock']
run(serial+['wait','--up-to','180'])
pub = (O/'qa-key.pub').read_text().strip()
run(serial+['sh',"mkdir -p /storage/.ssh && chmod 700 /storage/.ssh && printf '%s\\n' '"+pub+"' > /storage/.ssh/authorized_keys && chmod 600 /storage/.ssh/authorized_keys"], stdout=subprocess.DEVNULL)
ssh = ['ssh','-i',str(O/'qa-key'),'-p','10251','-o','LogLevel=ERROR','-o','StrictHostKeyChecking=no','-o','UserKnownHostsFile=/dev/null','-o','BatchMode=yes','-o','ConnectTimeout=5','root@127.0.0.1']
for _ in range(30):
    ready = subprocess.run(ssh+['grep ^BUILD_ID= /etc/os-release'],capture_output=True,text=True)
    if ready.returncode == 0: break
    time.sleep(2)
else: raise RuntimeError('guest SSH unavailable')
assert m['inputs']['distribution_commit'] in ready.stdout
with (O/'network-boundary.txt').open('w') as f:
    run(ssh+['ip route replace blackhole 0.0.0.0/1 && ip route replace blackhole 128.0.0.0/1 && ip -6 route replace blackhole ::/1 && ip -6 route replace blackhole 8000::/1 && ip route && ip -6 route'], stdout=f)
checks = {}
mapping = {
 '/usr/bin/cloud_migrate_layout':'projects/ROCKNIX/packages/network/rclone/sources/cloud_migrate_layout',
 '/usr/bin/cloud_scan':'projects/ROCKNIX/packages/network/rclone/sources/cloud_scan',
 '/usr/bin/cloud_backup':'projects/ROCKNIX/packages/network/rclone/sources/cloud_backup',
 '/usr/bin/cloud_restore':'projects/ROCKNIX/packages/network/rclone/sources/cloud_restore',
 '/usr/bin/start_es.sh':'projects/ROCKNIX/packages/ui/emulationstation/sources/start_es.sh',
 '/usr/lib/systemd/system/emustation.service':'projects/ROCKNIX/packages/ui/emulationstation/system.d/emustation.service',
 '/usr/lib/systemd/system/essway.service':'projects/ROCKNIX/packages/ui/emulationstation/system.d/essway.service',
 '/etc/profile.d/001-functions':'projects/ROCKNIX/packages/rocknix/profile.d/001-functions',
}
for dest, source in mapping.items():
    data = subprocess.check_output(['git','-C',str(R),'show','43d0bc3bf47fd858ba8d5c55fbdf52535a0db2aa:'+source])
    expected = hashlib.sha256(data).hexdigest()
    actual = subprocess.check_output(ssh+['sha256sum '+dest],text=True).split()[0]
    assert actual == expected, (dest,actual,expected)
    checks[dest] = {'source': source, 'sha256': actual}
dump('installed-source.json',checks)
dump('guest.json', {'command':cmd,'image_sha256':digest,'distribution':m['inputs']['distribution_commit'],'es_source':m['inputs']['emulationstation_commit'],'qemu_pid':int((O/'vm.pid').read_text()),'elapsed_seconds':round(time.monotonic()-start,3),'protected_by_blackhole_routes':True,'credentials':'synthetic SSH key only; exclude from packet'})
print('PASS fresh old-source guest ready; no personal credentials or data imported', flush=True)

"""Run in an owned QA guest: exact wrapper, real sysfs, then synthetic boundaries."""
from pathlib import Path
import json, os, shutil, subprocess, sys

wrapper = Path(sys.argv[1])
mode = sys.argv[2]
assert mode in ('software', 'virgl')
root = Path('/tmp/pixman-selector-fixture')
root.mkdir()
for name in ('bin', 'lib', 'lib64', 'usr/bin', 'usr/lib/sway', 'sys', 'dev'):
    (root / name).mkdir(parents=True, exist_ok=True)
for name in ('busybox',):
    shutil.copyfile('/usr/bin/' + name, root / 'bin' / name)
(root / 'bin/busybox').chmod(0o755)
for name in ('libc.so.6', 'libm.so.6'):
    shutil.copyfile('/usr/lib/' + name, root / 'usr/lib' / name)
shutil.copyfile('/usr/lib/ld-linux-x86-64.so.2', root / 'lib64/ld-linux-x86-64.so.2')
(root / 'lib64/ld-linux-x86-64.so.2').chmod(0o755)
for name in ('sh', 'cat', 'readlink'):
    (root / 'bin' / name).symlink_to('busybox')
(root / 'dev/null').write_bytes(b'')
(root / 'usr/bin/logger').write_text('#!/bin/sh\nexit 0\n')
(root / 'usr/bin/logger').chmod(0o755)
(root / 'usr/bin/sway.sh').write_text('#!/bin/sh\nprintf "renderer=%s\\n" "${WLR_RENDERER-unset}"\nprintf "arg=%s\\n" "$@"\n')
(root / 'usr/bin/sway.sh').chmod(0o755)
shutil.copyfile(wrapper, root / 'usr/lib/sway/sway-generic-x64')
(root / 'usr/lib/sway/sway-generic-x64').chmod(0o755)
probe = subprocess.run(['/usr/bin/busybox', 'chroot', str(root), '/bin/sh', '-c', 'printf fixture-ready'], text=True, capture_output=True, timeout=10)
assert probe.returncode == 0 and probe.stdout == 'fixture-ready', (probe.returncode, probe.stdout, probe.stderr)
print('PASS image BusyBox and /usr/lib loader fixture', flush=True)
rows = []
def run(name, want, overrides=None):
    env = {'PATH': '/bin:/usr/bin', 'WLR_DRM_DEVICES': '/dev/dri/card0'}
    env.update(overrides or {})
    r = subprocess.run(['/usr/bin/busybox', 'chroot', str(root), '/usr/lib/sway/sway-generic-x64', 'sentinel argument'], env=env, text=True, capture_output=True, timeout=10)
    assert r.returncode == 0 and r.stdout.splitlines() == ['renderer=' + want, 'arg=sentinel argument'], (name, r.returncode, r.stdout, r.stderr)
    rows.append({'name': name, 'renderer': want, 'returncode': r.returncode})
    print('PASS', name, flush=True)

# Real kernel capability; wrapper runs against real sysfs, with only its final
# compositor exec replaced by a recorder. This tests selection, not rendering.
transport = Path('/sys/class/drm/card0/device')
children = list(transport.glob('virtio[0-9]*'))
assert len(children) == 1, children
actual = children[0]
features = (actual / 'features').read_text().strip()
assert (actual / 'driver').resolve().name == 'virtio_gpu'
assert set(features) <= {'0', '1'} and len(features) >= 64
assert features[0] == ('0' if mode == 'software' else '1'), features
subprocess.run(['mount', '--bind', '/sys', str(root / 'sys')], check=True)
try:
    run('actual ' + mode + ' negotiated GPU', 'pixman' if mode == 'software' else 'unset')
finally:
    subprocess.run(['umount', str(root / 'sys')], check=True)

def fixture(driver='virtio_gpu', bits='0' * 64):
    shutil.rmtree(root / 'sys')
    gpu = root / 'sys/class/drm/card0/device/virtio1'
    gpu.mkdir(parents=True)
    if driver is not None:
        target = root / 'sys/bus/virtio/drivers' / driver
        target.mkdir(parents=True)
        (gpu / 'driver').symlink_to('/sys/bus/virtio/drivers/' + driver)
    if bits is not None:
        (gpu / 'features').write_text(bits + '\n')
    return gpu

fixture(); run('synthetic software', 'pixman')
(root / 'sys/class/drm/card0/device/virtio2').mkdir(); run('ambiguous transport children', 'unset')
fixture(bits='1' + '0' * 63); run('synthetic virgl', 'unset')
fixture(driver='i915'); run('non-virtio card', 'unset')
fixture(driver=None); run('missing driver', 'unset')
for label, bits in [('absent', None), ('empty', ''), ('short', '0'), ('nonbinary', '0' * 63 + 'x'), ('embedded newline', '0' * 32 + '\n' + '0' * 32)]:
    fixture(bits=bits); run(label + ' features', 'unset')
fixture(bits='0' * 128); run('extended software bitstring', 'pixman')
fixture()
for renderer in ('gles2', 'pixman', 'vulkan'):
    run('explicit ' + renderer, renderer, {'WLR_RENDERER': renderer})
run('explicit render device', 'unset', {'WLR_RENDER_DRM_DEVICE': '/dev/dri/renderD129'})
for label, value in [('multiple cards', '/dev/dri/card0:/dev/dri/card1'), ('unknown path', '/dev/dri/by-path/pci-card'), ('empty selection', ''), ('nonnumeric card', '/dev/dri/cardbogus'), ('missing card', '/dev/dri/card1')]:
    run(label, 'unset', {'WLR_DRM_DEVICES': value})
(root / 'sys/class/drm/card0').rename(root / 'sys/class/drm/card10')
run('multidigit card', 'pixman', {'WLR_DRM_DEVICES': '/dev/dri/card10'})
Path('/tmp/pixman-selector-results.json').write_text(json.dumps({'mode': mode, 'actual_features': features, 'actual_transport': str(transport.resolve()), 'actual_virtio': str(actual.resolve()), 'checks': rows, 'scope': 'selection only; compositor exec recorder'}, indent=2) + '\n')
print('PASS selector controls:', len(rows), flush=True)

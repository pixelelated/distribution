from pathlib import Path
import datetime, hashlib, json, sys

name, observation = sys.argv[1:]
assert name in ['signin-1g-13', 'signin-provider1g-05']
owner = Path('/workspace/tmp/pixelelated-m7-' + name)
root = owner / 'artifacts'
assert json.loads((owner / 'completion.json').read_text())['job_rc'] == 0
budget = json.loads((root / 'resource-budget.json').read_text())
assert budget['configured_memory_mib'] == 1024
assert budget['actual_measurement_rc'] == 0
assert budget['loaded_frame_captured'] and budget['loaded'] and budget['measurement_pass']
assert not budget['oom_lines'] and not budget['numerical_rss_ceiling_enforced']
firmware = json.loads((root / 'guest-physical-memory.json').read_text())
assert firmware['physical_kib'] == 1048576
qemu = json.loads((root / 'actual-gl.json').read_text())['args']
assert qemu[qemu.index('-m') + 1] == '1024'
assert 'virtio-gpu-pci,xres=640,yres=480' in qemu
renderer = json.loads((root / 'renderer-budget-1g.json').read_text())
assert renderer['passed'] and renderer['mode'] == 'software'
assert renderer['process']['graphics_env']['WLR_RENDERER'] == 'pixman'
frame = root / 'loaded-640x480.png'
result = dict(utc=datetime.datetime.now(datetime.timezone.utc).isoformat(), passed=True,
              method='Direct view_image of actual loaded frame; checked resource-budget.json and terminal/cleanup agreement.',
              frames=[dict(path=str(frame), sha256=hashlib.sha256(frame.read_bytes()).hexdigest(),
                           observation=observation, passed=True)],
              budget=budget,
              limitations=['30-second public page workload; not authenticated provider trust.',
                           'Baseline and provider pages are different workloads; RSS values are not a like-for-like growth comparison.',
                           'No arbitrary numerical RSS ceiling was added.'])
with (owner / 'visual-review.json').open('x') as f:
    f.write(json.dumps(result, indent=2) + '\n')
print(json.dumps(dict(owner=name, passed=True, peak_rss_kib=budget['peak_total_rss_kib'])))

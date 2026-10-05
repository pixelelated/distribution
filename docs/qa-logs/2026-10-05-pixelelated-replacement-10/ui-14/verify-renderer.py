"""Read only: prove actual installed selector, unit, GPU capability and compositor."""
from pathlib import Path
import argparse, hashlib, json, subprocess

ap = argparse.ArgumentParser()
ap.add_argument('mode', choices=['software', 'virgl'])
ap.add_argument('phase')
ap.add_argument('--port', default='10026')
ap.add_argument('--key', required=True)
ap.add_argument('--out', required=True, type=Path)
args = ap.parse_args()
expected = {}
base = Path('projects/ROCKNIX/devices/GENERIC_X64/filesystem')
for installed in ['usr/lib/sway/sway-generic-x64', 'usr/lib/systemd/system/sway.service.d/10-generic-x64-renderer.conf']:
    expected['/' + installed] = hashlib.sha256((base / installed).read_bytes()).hexdigest()
expected['/usr/bin/sway.sh'] = hashlib.sha256(Path('projects/ROCKNIX/packages/wayland/compositor/sway/scripts/sway.sh').read_bytes()).hexdigest()
code = r'''from pathlib import Path
import json, hashlib, subprocess
expected = EXPECTED
files = {}
for name, wanted in expected.items():
 p=Path(name); actual=hashlib.sha256(p.read_bytes()).hexdigest(); assert actual==wanted, (name,actual,wanted)
 files[name]={'sha256':actual,'mode':oct(p.stat().st_mode & 0o777)}
assert files['/usr/lib/sway/sway-generic-x64']['mode']=='0o755'
rows=[]
for p in Path('/proc').glob('[0-9]*/cmdline'):
 try:
  argv=p.read_bytes().split(b'\0')
  if not argv[0].endswith(b'/sway'):continue
  env=dict(x.split(b'=',1) for x in (p.parent/'environ').read_bytes().split(b'\0') if b'=' in x)
  rows.append({'pid':int(p.parent.name),'argv':[x.decode() for x in argv if x], 'graphics_env':{k.decode():v.decode() for k,v in env.items() if k.startswith((b'WLR_',b'LIBGL_',b'MESA_',b'GALLIUM_'))}})
 except OSError:pass
assert len(rows)==1, rows
row=rows[0]; env=row['graphics_env']; card=env['WLR_DRM_DEVICES'];assert card.startswith('/dev/dri/card') and card.removeprefix('/dev/dri/card').isdigit(),card
children=list((Path('/sys/class/drm')/Path(card).name/'device').glob('virtio[0-9]*'));assert len(children)==1,children
child=children[0];assert (child/'driver').resolve().name=='virtio_gpu'
features=(child/'features').read_text().strip();assert len(features)>=64 and set(features)<={'0','1'}
assert '-V' in row['argv'] and '-d' not in row['argv'],row
assert 'WLR_DRM_NO_ATOMIC' not in env
log=Path('/var/log/sway.log').read_text(errors='replace')
if MODE=='software':
 assert features[0]=='0' and env.get('WLR_RENDERER')=='pixman',(features,env)
 assert 'Creating pixman renderer' in log,log
else:
 assert features[0]=='1' and 'WLR_RENDERER' not in env,(features,env)
 assert 'Creating GLES2 renderer' in log and 'virgl' in log,log
unit=subprocess.check_output(['systemctl','show','sway','-p','ExecStart','-p','FragmentPath','-p','DropInPaths'],text=True)
assert 'path=/usr/lib/sway/sway-generic-x64' in unit,unit
assert '/usr/lib/systemd/system/sway.service.d/10-generic-x64-renderer.conf' in unit,unit
assert '/run/systemd/system/sway.service.d/' not in unit,unit
print(json.dumps({'files':files,'process':row,'mode':MODE,'virtio':str(child.resolve()),'negotiated_features':features,'unit':unit,'sway_log':log,'passed':True},indent=2))
'''.replace('EXPECTED', repr(expected)).replace('MODE', repr(args.mode))
ssh = ['ssh', '-i', args.key, '-p', args.port, '-o', 'BatchMode=yes', '-o', 'ConnectTimeout=8', '-o', 'StrictHostKeyChecking=no', '-o', 'UserKnownHostsFile=/dev/null', '-o', 'LogLevel=ERROR', 'root@127.0.0.1']
r = subprocess.run(ssh + ['python3 -'], input=code, text=True, capture_output=True, timeout=40)
args.out.mkdir(parents=True, exist_ok=True)
(args.out / ('renderer-' + args.phase + '.stdout')).write_text(r.stdout)
(args.out / ('renderer-' + args.phase + '.stderr')).write_text(r.stderr)
assert r.returncode == 0, (r.returncode, r.stdout, r.stderr)
j = json.loads(r.stdout)
(args.out / ('renderer-' + args.phase + '.json')).write_text(json.dumps(j, indent=2) + '\n')
print('PASS installed selector/unit and actual', args.mode, 'compositor:', args.phase, flush=True)

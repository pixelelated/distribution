from pathlib import Path
import json,sys,datetime
owner=Path(__file__).parent
pid=int(sys.argv[1]);args=[x.decode() for x in (Path('/proc')/str(pid)/'cmdline').read_bytes().split(b'\0') if x]
assert Path(args[0]).name.startswith('qemu-system-')
assert any(x.startswith('virtio-gpu-gl-pci,') for x in args),args
assert any('egl-headless' in x for x in args),args
assert any(str(owner/'guest-d.qcow2') in x for x in args),args
(owner/'artifacts/actual-gl.json').write_text(json.dumps({'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'pid':pid,'args':args},indent=2)+'\n')
print('PASS actual guest uses accelerated virtio GPU renderer')

import json,subprocess,hashlib,os
from pathlib import Path
R=Path('/storage/qa616-provider');rows=[]
for args in [['/usr/bin/cloud_oauth','cancel'],['systemctl','stop','qa616-calibration.service']]:
 p=subprocess.run(args,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL,timeout=20);rows.append({'action':args[:3],'rc':p.returncode})
for target,expected in [('/usr/bin/cloud-signin-window',json.loads((R/'binding.json').read_text())['files']['browser-launch.py']),('/storage/.config/rclone',None)]:
 mounted=any(line.split()[4]==target for line in Path('/proc/self/mountinfo').read_text().splitlines())
 if mounted:
  if expected:assert hashlib.sha256(Path(target).read_bytes()).hexdigest()==expected
  p=subprocess.run(['umount',target],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL,timeout=10);rows.append({'action':'unmount','target':target,'rc':p.returncode});assert p.returncode==0
assert hashlib.sha256(Path('/usr/bin/cloud-signin-window').read_bytes()).hexdigest()=='6cbc445686d3d484ff20450342776e9eb92b47f6112a0352be1a50b334eef81b'
assert not list(Path('/storage/.config/rclone').iterdir())
Path('/storage/.config/rclone').rmdir()
(R/'cleanup-result.json').write_text(json.dumps({'rows':rows,'original_browser_restored':True,'original_missing_rclone_directory_restored':True})+'\n')

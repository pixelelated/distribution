from pathlib import Path
import importlib.util,subprocess,json
s=importlib.util.spec_from_file_location('v','/tmp/pix537-vm.py');v=importlib.util.module_from_spec(s);s.loader.exec_module(v)
O=Path('/tmp/pix540-final-guest39');D=Path('/workspace/repos/rocknix.worktrees/m7-cloud-connections')
subprocess.run(['python3','/tmp/pix540-vm-transactions39.py'],check=True)
receipt=[v.install(D/'projects/ROCKNIX/packages/network/rclone/sources'/n,n) for n in ['cloud_connections.py','cloud_remote','cloud_oauth','cloud_scan','cloud_backup','cloud_restore','cloud_content_backup','cloud_content_restore','cloud_setup']]
(O/'installed.json').write_text(json.dumps(receipt,indent=2)+'\n')
v.scp(O/'guest.py','/storage/qa537/shutdown39.py');print(v.remote('python3 /storage/qa537/shutdown39.py'),flush=True)
(O/'result.json').write_text(v.remote('cat /storage/qa537/shutdown39/result.json')+'\n')

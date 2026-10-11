from pathlib import Path
import importlib.util,json
s=importlib.util.spec_from_file_location('v','/tmp/pix537-vm.py');v=importlib.util.module_from_spec(s);s.loader.exec_module(v)
O=Path('/tmp/pix540-content35');D=Path('/workspace/repos/rocknix.worktrees/m7-cloud-connections')
v.remote('systemctl stop essway; cp /storage/qa537/rclone-real /usr/bin/rclone; chmod 755 /usr/bin/rclone')
receipt=[v.install(D/'projects/ROCKNIX/packages/network/rclone/sources'/n,n) for n in ['cloud_scan','cloud_content_backup','cloud_content_restore']];(O/'installed.json').write_text(json.dumps(receipt,indent=2)+'\n')
v.scp(O/'guest.py','/storage/qa537/content35.py');print(v.remote('python3 /storage/qa537/content35.py'),flush=True)
for n in ['result.json','cloud_content_backup.log','cloud_content_restore.log','preview.log']:(O/n).write_text(v.remote('cat /storage/qa537/content35/'+n)+'\n')

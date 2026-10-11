import importlib.util,json,time
from pathlib import Path
s=importlib.util.spec_from_file_location('v','/tmp/pix537-vm.py');v=importlib.util.module_from_spec(s);s.loader.exec_module(v)
D=Path('/workspace/repos/rocknix.worktrees/m7-cloud-connections')
v.remote('systemctl stop essway')
proof=[v.install('/workspace/tmp/pix540-es54/emulationstation','emulationstation'),v.install('/tmp/pix535-nmcli','nmcli')]
for name in ['cloud_connections.py','cloud_remote','cloud_oauth']:
 proof.append(v.install(D/'projects/ROCKNIX/packages/network/rclone/sources'/name,name))
v.scp('/workspace/tmp/pix540-es54/emulationstation2.mo','/storage/qa537/fr-new.mo');v.remote('cp /storage/qa537/fr-new.mo /storage/qa537/fr.mo; umount /storage/.config/locale/fr/LC_MESSAGES/emulationstation2.mo; mount --bind /storage/qa537/fr.mo /usr/share/locale/fr/LC_MESSAGES/emulationstation2.mo')
import hashlib
expected=hashlib.sha256(Path('/workspace/tmp/pix540-es54/emulationstation2.mo').read_bytes()).hexdigest()
assert v.remote('sha256sum /usr/share/locale/fr/LC_MESSAGES/emulationstation2.mo').split()[0]==expected
proof.append({'name':'runtime-fr.mo','sha256':expected})
(Path('/workspace/tmp/pix540-ui55')/'installed.json').write_text(json.dumps(proof,indent=2)+'\n')
v.remote(". /etc/profile >/dev/null 2>&1; set_setting system.language en_US; rm -f /storage/qa537/wifi/state.json /storage/qa537/wifi/fail /tmp/emulationstation.ready; systemctl start essway")
for _ in range(100):
 if 'ready' in v.remote('test -f /tmp/emulationstation.ready && echo ready || true'):break
 time.sleep(.2)
else:raise RuntimeError('ES not ready')
print('PASS UI38 full source readback; ES ready')

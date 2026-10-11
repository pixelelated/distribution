from pathlib import Path
import importlib.util,sys,subprocess,time,json
s=importlib.util.spec_from_file_location('v','/tmp/pix537-vm.py');v=importlib.util.module_from_spec(s);s.loader.exec_module(v)
D=Path('/workspace/repos/rocknix.worktrees/m7-cloud-connections');lang,size=sys.argv[1:3]
O=Path('/tmp/pix537-ui21')/(lang[:2]+size);O.mkdir(parents=True,exist_ok=True)
subprocess.run(['python3','/tmp/pix537-reset-ui.py',lang],check=True)
for _ in range(100):
 if 'ready' in v.remote('test -f /tmp/emulationstation.ready && echo ready || true'):break
 time.sleep(.2)
else:raise RuntimeError('ES not ready')
before=v.remote('sha256sum /storage/qa537/provider/save.srm /storage/.config/cloud_sync.conf')
subprocess.run([str(D/'tools/vm-visual-qa'),'--monitor',str(v.O/'monitor.sock'),'run','/tmp/pix537-full-lifecycle.steps','--outdir',str(O/'lifecycle')],check=True)
after=v.remote('sha256sum /storage/qa537/provider/save.srm /storage/.config/cloud_sync.conf')
assert before==after
selection=v.remote('cloud_remote list');assert 'STATE=unselected' in selection and 'spare' not in selection and 'dropbox' in selection
(O/'lifecycle.json').write_text(json.dumps({'unchanged_payload_and_folder_settings':before.splitlines(),'final_selection':selection,'es_sha256':v.remote('sha256sum /usr/bin/emulationstation').split()[0]},indent=2)+'\n')
print('PASS source-bound cloud lifecycle and unchanged bytes',lang,size,flush=True)

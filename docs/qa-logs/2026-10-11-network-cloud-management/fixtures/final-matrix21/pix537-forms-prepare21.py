from pathlib import Path
import importlib.util,sys,time,json,hashlib
s=importlib.util.spec_from_file_location('v','/tmp/pix537-vm.py');v=importlib.util.module_from_spec(s);s.loader.exec_module(v)
lang,size=sys.argv[1:3];assert lang in ['en_US','fr_FR'];O=Path('/tmp/pix537-forms21')/(lang[:2]+size);O.mkdir(parents=True,exist_ok=True)
v.remote('cloud_oauth cancel >/dev/null 2>&1 || true; systemctl stop essway; rm -f /storage/qa537/oauth-fail /tmp/emulationstation.ready')
config=O/'synthetic-rclone.conf';config.write_text('[dropbox]\ntype = dropbox\ntoken = {"access_token":"synthetic-only"}\n\n[spare]\ntype = alias\nremote = /storage/qa537/provider\n');config.chmod(0o600);v.scp(config,'/storage/.config/rclone/rclone.conf')
v.remote("chmod 600 /storage/.config/rclone/rclone.conf; printf 'dropbox\\n' > /storage/.config/rclone/active-connection; chmod 600 /storage/.config/rclone/active-connection")
shim=O/'rclone-fixture';shim.write_text(Path('/tmp/pix537-provider-rclone').read_text().replace('+120','+300'));v.install(shim,'rclone')
v.remote('. /etc/profile >/dev/null 2>&1; set_setting system.language '+lang+'; set_setting cloudsaves.startup 0; set_setting cloudsaves.gameexit 0; systemctl start essway')
for _ in range(100):
 if 'ready' in v.remote('test -f /tmp/emulationstation.ready && echo ready || true'):break
 time.sleep(.2)
else:raise RuntimeError('ES not ready')
(O/'before.sha256').write_text(v.remote('sha256sum /storage/.config/rclone/rclone.conf /storage/.config/rclone/active-connection /storage/.config/cloud_sync.conf /storage/qa537/provider/save.srm'))
print('PASS local-only OAuth fixture ready',lang,size,flush=True)

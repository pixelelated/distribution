import importlib.util,json,sys
s=importlib.util.spec_from_file_location('v','/tmp/pix537-vm.py');v=importlib.util.module_from_spec(s);s.loader.exec_module(v)
lang=sys.argv[1];assert lang in ['en_US','fr_FR']
v.remote('systemctl stop essway')
v.remote("python3 - <<'END'\nfrom pathlib import Path\np=Path('/storage/.config/rclone/rclone.conf');p.write_text('[dropbox]\\ntype = alias\\nremote = /storage/qa537/provider\\n\\n[spare]\\ntype = alias\\nremote = /storage/qa537/provider\\n');p.chmod(0o600)\np=Path('/storage/qa537/provider/save.srm');p.parent.mkdir(exist_ok=True);p.write_bytes(b'QA SAVE CONTENT DO NOT MOVE\\n')\nEND")
print(v.remote(". /etc/profile >/dev/null 2>&1; set_setting system.language "+lang+"; cloud_remote select dropbox; sha256sum /storage/qa537/provider/save.srm; rm -f /tmp/emulationstation.ready; systemctl start essway"))

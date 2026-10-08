#!/usr/bin/env python3
import subprocess,pathlib,json,hashlib,time
base=pathlib.Path('/workspace/tmp/pixelelated-520-ui-20261008');owner=base/'backend01';ssh=['ssh', '-i', '/workspace/tmp/pixelelated-520-ui-20261008/guest01/qa-key', '-p', '10220', '-o', 'LogLevel=ERROR', '-o', 'StrictHostKeyChecking=no', '-o', 'UserKnownHostsFile=/dev/null', 'root@127.0.0.1']
scp=['scp','-q','-i',str(base/'guest01/qa-key'),'-P','10220','-o','LogLevel=ERROR','-o','StrictHostKeyChecking=no','-o','UserKnownHostsFile=/dev/null']
subprocess.run(scp+[str(owner/'payload.tar'),'root@127.0.0.1:/storage/qa520/payload.tar'],check=True)
r=subprocess.run(ssh+['sh -s'],input=(owner/'guest-setup.sh').read_bytes(),stdout=subprocess.PIPE,stderr=subprocess.STDOUT);(owner/'setup.log').write_bytes(r.stdout);print(r.stdout.decode());r.check_returncode()
manifest=json.loads((owner/'install-manifest.json').read_text());cmd='sha256sum '+' '.join(row['destination'] for row in manifest['installed_files']);out=subprocess.check_output(ssh+[cmd]).decode();(owner/'installed-sha256.txt').write_text(out);actual={line.split()[1]:line.split()[0] for line in out.splitlines()};assert all(actual[row['destination']]==row['sha256'] for row in manifest['installed_files']);print('PASS all22 installed hashes match frozen commit '+manifest['distribution_commit'])
subprocess.run(ssh+['cloud_setup --validate-folders saves,roms qa520-preflight'],check=True,stdout=open(owner/'initial-validation.json','w'))

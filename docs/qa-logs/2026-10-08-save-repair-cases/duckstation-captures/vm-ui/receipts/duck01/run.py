import pathlib,subprocess,json,hashlib,tarfile,shutil,time
b=pathlib.Path('/workspace/tmp/pixelelated-520-ui-20261008');o=b/'duck01';r=pathlib.Path('/workspace/repos/rocknix.worktrees/conflict-resolution');repo=pathlib.Path('/workspace/repos/rocknix.worktrees/m7-manual-cloud-folders');prefix='projects/ROCKNIX/packages/emulators/standalone/duckstation-sa/'
m=json.loads((r/'docs/qa-logs/2026-10-08-save-repair-cases/duckstation-captures/frozen-inputs.json').read_text());(o/'frozen-inputs.json').write_text(json.dumps(m,indent=2)+'\n');payload=o/'payload';payload.mkdir()
for rel,dest in [('scripts/start_duckstation.sh','start_duckstation.sh'),('scripts/duckstation_screenshot_path','duckstation_screenshot_path'),('config/InputPlumber/settings.ini','settings.ini'),('sources/Start Duckstation.sh','Start Duckstation.sh')]:
 src=repo/(prefix+rel);data=src.read_bytes();assert hashlib.sha256(data).hexdigest()==m['files'][prefix+rel]['sha256'];(payload/dest).write_bytes(data)
subprocess.run(['python3',str(r/'docs/qa-logs/2026-10-08-save-repair-cases/duckstation-captures/synthetic-display-rom.py'),str(payload/'synthetic-display.bin')],check=True)
with tarfile.open(o/'payload.tar','w') as tar:tar.add(payload,arcname='frozen')
ssh=['ssh','-i',str(b/'guest01/qa-key'),'-p','10220','-o','LogLevel=ERROR','-o','StrictHostKeyChecking=no','-o','UserKnownHostsFile=/dev/null','root@127.0.0.1'];scp=['scp','-q','-i',str(b/'guest01/qa-key'),'-P','10220','-o','LogLevel=ERROR','-o','StrictHostKeyChecking=no','-o','UserKnownHostsFile=/dev/null']
def call(cmd,name):
 q=subprocess.run(ssh+[cmd],stdout=subprocess.PIPE,stderr=subprocess.STDOUT);(o/name).write_bytes(q.stdout);print(q.stdout.decode(),flush=True);q.check_returncode()
call('mkdir -p /storage/qa521; cp /usr/config/duckstation/settings.ini /storage/qa521/original-settings.ini; sha256sum /usr/bin/duckstation-sa; stat -c "%a %s %n" /usr/bin/duckstation-sa','before.txt')
subprocess.run(scp+[str(o/'payload.tar'),'root@127.0.0.1:/storage/qa521/payload.tar'],check=True)
call('''set -eu
cd /storage/qa521
tar xf payload.tar
install -m 0755 /usr/bin/duckstation-sa /storage/qa521/duckstation-sa
mount --bind /storage/qa521/duckstation-sa /usr/bin/duckstation-sa
install -m 0755 frozen/duckstation_screenshot_path /usr/bin/duckstation_screenshot_path
install -m 0755 frozen/start_duckstation.sh /usr/bin/start_duckstation.sh
mount --bind "$PWD/frozen/settings.ini" /usr/config/duckstation/settings.ini
mount --bind "$PWD/frozen/Start Duckstation.sh" '/usr/config/modules/Start Duckstation.sh'
stat -c '%a %s %n' /usr/bin/duckstation-sa
sha256sum /usr/bin/duckstation-sa /usr/bin/duckstation_screenshot_path /usr/bin/start_duckstation.sh /usr/config/duckstation/settings.ini '/usr/config/modules/Start Duckstation.sh' /storage/qa521/frozen/synthetic-display.bin
. /etc/profile
set +e
timeout 20 /usr/bin/duckstation-sa -help > /storage/qa521/entrypoint-help.log 2>&1
rc=$?
cat /storage/qa521/entrypoint-help.log
echo actual_entrypoint_exit:$rc
exit "$rc"
''','stage-and-entrypoint.log')
print('PASS frozen521 scripts/config and qualified522 installed executable bytes',flush=True)

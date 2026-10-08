import pathlib,subprocess,json,time
b=pathlib.Path('/workspace/tmp/pixelelated-520-ui-20261008');r=pathlib.Path('/workspace/repos/rocknix.worktrees/conflict-resolution');o=b/'content02'
ssh=['ssh','-i',str(b/'guest01/qa-key'),'-p','10220','-o','LogLevel=ERROR','-o','StrictHostKeyChecking=no','-o','UserKnownHostsFile=/dev/null','root@127.0.0.1']
def call(cmd,name):
 q=subprocess.run(ssh+[cmd],stdout=subprocess.PIPE,stderr=subprocess.STDOUT);(o/name).write_bytes(q.stdout);q.check_returncode()
witness="cloud_setup --validation-context; sha256sum /storage/.config/cloud_sync.conf /storage/.config/rclone/rclone.conf; find /storage/qa520/provider /storage/roms -type f -exec sha256sum '{}' ';' | sort"
call('''set -e
systemctl stop essway.service
mkdir -p /storage/qa520/provider/QA-All/Saves /storage/qa520/provider/QA-All/Content /storage/qa520/provider/QA-All/Backups
for name in PSP Duck N64; do cp -a /storage/qa520/provider/QA-$name/Saves/. /storage/qa520/provider/QA-All/Saves/; cp -a /storage/qa520/provider/QA-$name/Content/. /storage/qa520/provider/QA-All/Content/; done
cloud_setup --set-saves-remote /QA-All/Saves
cloud_setup --set-settings-remote /QA-All/Backups
cloud_setup --set-content-remote /QA-All/Content
. /etc/profile
set_setting cloudsync.pick.restore.saves 1
set_setting cloudsync.pick.restore.content 0
set_setting cloudsync.pick.restore.media 0
set_setting cloudsync.pick.restore.settings 0
systemctl start essway.service
''','setup.log');call("p=$(cat /storage/qa520/provider.pid); tr '\\000' ' ' < /proc/$p/cmdline | grep -F 'rclone serve webdav /storage/qa520/provider' >/dev/null || exit 8; kill -TERM \"$p\"; sleep 1; nohup rclone serve webdav /storage/qa520/provider --addr 127.0.0.1:9038 --dir-cache-time 0 --log-file /storage/qa520/provider.log >/storage/qa520/provider.stdout 2>&1 </dev/null & echo $! > /storage/qa520/provider.pid; sleep 1; kill -0 \"$(cat /storage/qa520/provider.pid)\"",'provider-fresh.log');call(witness,'before.txt');call('cloud_setup --validate-folders saves,roms qa520-all','validation.json');j=json.loads((o/'validation.json').read_text());assert {c['category']:c['state'] for c in j['categories']}=={'saves':'present','roms':'empty'},j;time.sleep(3)
steps='''key ret
settle
key x
settle
key up x3
key x
settle
key down
key x
wait-for-change
wait 5
settle
shot restore-options
key x
key down
key x
shot selected-roms-only
key up x2
key right
key x
wait-for-change
wait 5
settle
shot selected-content-empty
''';(o/'steps.txt').write_text(steps)
q=subprocess.run(['python3',str(r/'tools/vm-visual-qa'),'--monitor','/tmp/pix520-mon.sock','run',str(o/'steps.txt'),'--outdir',str(o/'frames')],stdout=subprocess.PIPE,stderr=subprocess.STDOUT);(o/'walk.log').write_bytes(q.stdout);q.check_returncode()
call(witness,'after.txt');assert (o/'before.txt').read_bytes()==(o/'after.txt').read_bytes()
call('for f in /storage/.cache/cloud_sync/scan/done /storage/.cache/cloud_sync/scan/content-done /storage/.cache/cloud_sync/scan/systems /storage/.cache/cloud_sync/scan/scan /storage/.cache/cloud_sync/scan/state; do echo "FILE:$f"; cat "$f" 2>/dev/null || true; done; ps | grep -E "cloud_content_restore|cloud_scan" | grep -v grep || true','scan-readback.txt');print('PASS selected-only content scan captured and all provider/local file hashes unchanged',flush=True)

import pathlib,subprocess,json,time
b=pathlib.Path('/workspace/tmp/pixelelated-520-ui-20261008');r=pathlib.Path('/workspace/repos/rocknix.worktrees/conflict-resolution');o=b/'read01'
ssh=['ssh','-i',str(b/'guest01/qa-key'),'-p','10220','-o','LogLevel=ERROR','-o','StrictHostKeyChecking=no','-o','UserKnownHostsFile=/dev/null','root@127.0.0.1']
def call(cmd,name,allow=False):
 q=subprocess.run(ssh+[cmd],stdout=subprocess.PIPE,stderr=subprocess.STDOUT);(o/name).write_bytes(q.stdout)
 if not allow:q.check_returncode()
 return q.returncode
witness="cloud_setup --validation-context; sha256sum /storage/.config/cloud_sync.conf /storage/.config/rclone/rclone.conf; find /storage/qa520/provider -type f -exec sha256sum '{}' ';' | sort"
call('''systemctl stop essway.service
cloud_setup --set-saves-remote /QA-PSP/Saves
cloud_setup --set-settings-remote /QA-PSP/Backups
cloud_setup --set-content-remote /QA-PSP/Content
. /etc/profile
set_setting system.language en_US
sed -i 's/name="Language" value="[^"]*"/name="Language" value="en_US"/' /storage/.config/emulationstation/es_settings.cfg
swaymsg -s /run/0-runtime-dir/sway-ipc.0.sock "output Virtual-1 mode 640x480@60Hz"
p=$(cat /storage/qa520/provider.pid)
tr '\000' ' ' < /proc/$p/cmdline
tr '\000' ' ' < /proc/$p/cmdline | grep -F 'rclone serve webdav /storage/qa520/provider' >/dev/null || exit 8
kill -TERM "$p"
sleep 1
systemctl start essway.service
''','setup.log');call(witness,'before.txt')
rc=call('cloud_setup --validate-folders saves,roms qa520-readfailure','validation-refused.json',True);assert rc==5,rc
q=json.loads((o/'validation-refused.json').read_text());assert not q['complete'] and all(c['state']=='unreadable' for c in q['categories']),q
steps=(b/'cases02/steps.txt').read_text().replace('wait 2','wait 28').replace('shot result','shot unreadable-result');(o/'failure-steps.txt').write_text(steps)
proc=subprocess.run(['python3',str(r/'tools/vm-visual-qa'),'--monitor','/tmp/pix520-mon.sock','run',str(o/'failure-steps.txt'),'--outdir',str(o/'failure-frames')],stdout=subprocess.PIPE,stderr=subprocess.STDOUT);(o/'failure-walk.log').write_bytes(proc.stdout);proc.check_returncode();print('PASS refusal branch captured',flush=True)
call('nohup rclone serve webdav /storage/qa520/provider --addr 127.0.0.1:9038 --log-file /storage/qa520/provider.log >/storage/qa520/provider.stdout 2>&1 </dev/null & echo $! > /storage/qa520/provider.pid; sleep 1; kill -0 "$(cat /storage/qa520/provider.pid)"','provider-restart.log')
steps='key z\nsettle\nkey x\nwait-for-change\nwait 3\nsettle\nshot successful-retry\n';(o/'retry-steps.txt').write_text(steps)
proc=subprocess.run(['python3',str(r/'tools/vm-visual-qa'),'--monitor','/tmp/pix520-mon.sock','run',str(o/'retry-steps.txt'),'--outdir',str(o/'retry-frames')],stdout=subprocess.PIPE,stderr=subprocess.STDOUT);(o/'retry-walk.log').write_bytes(proc.stdout);proc.check_returncode()
call('cloud_setup --validate-folders saves,roms qa520-retry','validation-retry.json');call(witness,'after.txt');assert (o/'before.txt').read_bytes()==(o/'after.txt').read_bytes();print('PASS provider/config unchanged and actual retry captured',flush=True)

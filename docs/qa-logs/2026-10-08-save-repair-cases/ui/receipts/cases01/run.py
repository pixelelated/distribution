import pathlib,subprocess,json,time
b=pathlib.Path('/workspace/tmp/pixelelated-520-ui-20261008');r=pathlib.Path('/workspace/repos/rocknix.worktrees/conflict-resolution');o=b/'cases01'
ssh=['ssh','-i',str(b/'guest01/qa-key'),'-p','10220','-o','LogLevel=ERROR','-o','StrictHostKeyChecking=no','-o','UserKnownHostsFile=/dev/null','root@127.0.0.1']
def call(cmd,p,allow=False):
 q=subprocess.run(ssh+[cmd],stdout=subprocess.PIPE,stderr=subprocess.STDOUT);p.write_bytes(q.stdout)
 if not allow:q.check_returncode()
 return q.returncode
for name,locale,res in [('Duck','en_US','640x480'),('N64','en_US','640x480'),('Deep','en_US','640x480'),('Duck','fr_FR','1280x800')]:
 d=o/(name+'-'+locale+'-'+res);d.mkdir();print('START '+d.name,flush=True)
 call('systemctl stop essway.service; cloud_setup --set-saves-remote /QA-'+name+'/Saves; cloud_setup --set-settings-remote /QA-'+name+'/Backups; cloud_setup --set-content-remote /QA-'+name+'/Content; . /etc/profile; set_setting system.language '+locale+'; sed -i 's/name="Language" value="[^"]*"/name="Language" value="'+locale+'"/' /storage/.config/emulationstation/es_settings.cfg; swaymsg -s /run/0-runtime-dir/sway-ipc.0.sock "output Virtual-1 mode '+('--custom ' if res=='1280x800' else '')+res+'@60Hz"; systemctl start essway.service',d/'setup.log')
 call('cloud_setup --validation-context; sha256sum /storage/.config/cloud_sync.conf /storage/.config/rclone/rclone.conf; find /storage/qa520/provider -type f -exec sha256sum '{}' ';' | sort',d/'before.txt')
 rc=call('cloud_setup --validate-folders saves,roms qa520-'+name.lower(),d/'validation.json',True);j=json.loads((d/'validation.json').read_text());states={x['category']:x['state'] for x in j['categories']};assert states['saves']==('unreadable' if name=='Deep' else 'present'),states
 (d/'validation-exit.json').write_text(json.dumps({'exit_code':rc,'states':states})+'\n')
 time.sleep(3)
 q=subprocess.run(['python3',str(r/'tools/vm-visual-qa'),'--monitor','/tmp/pix520-mon.sock','run',str(o/'steps.txt'),'--outdir',str(d/'frames')],stdout=subprocess.PIPE,stderr=subprocess.STDOUT);(d/'walk.log').write_bytes(q.stdout);q.check_returncode()
 call('cloud_setup --validation-context; sha256sum /storage/.config/cloud_sync.conf /storage/.config/rclone/rclone.conf; find /storage/qa520/provider -type f -exec sha256sum '{}' ';' | sort',d/'after.txt');assert (d/'before.txt').read_bytes()==(d/'after.txt').read_bytes();print('PASS controls '+d.name,flush=True)

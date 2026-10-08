from pathlib import Path
import subprocess,json,hashlib,shlex,time
O=Path(__file__).parent;B=O.parent;R=Path('/workspace/repos/rocknix.worktrees/m7-pixelelated-replacement17');G=B/'guest03'
ssh=['ssh','-i',str(G/'qa-key'),'-p','10230','-o','LogLevel=ERROR','-o','StrictHostKeyChecking=no','-o','UserKnownHostsFile=/dev/null','-o','BatchMode=yes','-o','ConnectTimeout=5','root@127.0.0.1']
def guest(code,label):
 q=subprocess.run(ssh+['bash -s'],input=code,capture_output=True,text=True,timeout=40);(O/(label+'.stdout')).write_text(q.stdout);(O/(label+'.stderr')).write_text(q.stderr);q.check_returncode();return q.stdout
witness='set -e\ncat /proc/sys/kernel/random/boot_id\nsha256sum /storage/.config/cloud_sync.conf /storage/.config/rclone/rclone.conf /usr/bin/emulationstation /usr/bin/cloud_setup /usr/share/locale/fr/LC_MESSAGES/emulationstation2.mo\n'
before=guest(witness,'before')
script='set -e\nsystemctl stop essway.service\n. /etc/profile >/dev/null 2>&1\nset_setting system.language en_US\ncat > /storage/.config/emulationstation/es_settings.cfg <<\'XML\'\n<?xml version="1.0"?>\n<config>\n<bool name="UseOSK" value="false" />\n<int name="ScreenSaverTime" value="0" />\n<string name="Language" value="en_US" />\n</config>\nXML\nsystemctl start essway.service\n'
(O/'setup.sh').write_text(script);guest(script,'setup');time.sleep(4)
steps='settle\nshot carousel\nkey ret\nwait-for-change 12 0\nsettle\nshot main-menu\nkey x\nwait-for-change 12 0\nkey up x3\nkey x\nwait-for-change 12 0\nsettle\nshot cloud-hub\nkey up x3\nkey x\nwait-for-change 12 0\nsettle\nshot clean-folder-selection\n'
(O/'entry.steps').write_text(steps)
q=subprocess.run(['python3',str(R/'tools/vm-visual-qa'),'--monitor','/tmp/pix508-cf10-17-mon.sock','run',str(O/'entry.steps'),'--outdir',str(O/'frames')],capture_output=True,text=True,timeout=100);(O/'walk.log').write_text(q.stdout+q.stderr);q.check_returncode()
after=guest(witness,'after');assert before==after,'navigation changed cloud config or installed bytes'
(O/'result.json').write_text(json.dumps({'passed_navigation_preservation':True,'frame_review':'pending direct visual review','locale':'en_US','resolution':'640x480','frames':{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in (O/'frames').glob('*.png')}},indent=2)+'\n')
print('PASS native navigation preserves cloud paths/credentials and installed bytes; frames await direct review',flush=True)

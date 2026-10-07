from pathlib import Path
import json,subprocess,hashlib,sys,time,shlex
O=Path('/tmp/pixelelated-508-ui01');A=O/'artifacts';R=Path('/workspace/repos/rocknix.worktrees/conflict-resolution');G=json.loads(Path('/workspace/tmp/pixelelated-508-vm01/guest.json').read_text());KEY=G['ssh_identity'];PORT=str(G['ssh_port']);MON=G['monitor']
OPT=['-o','StrictHostKeyChecking=no','-o','UserKnownHostsFile=/dev/null','-o','BatchMode=yes','-o','LogLevel=ERROR','-o','ConnectTimeout=8']
def run(a,**kw):return subprocess.run([str(x) for x in a],check=True,**kw)
def remote(cmd):return run(['ssh','-i',KEY,'-p',PORT,*OPT,'root@127.0.0.1',cmd],capture_output=True,text=True,timeout=120).stdout
def scp(src,dst):run(['scp','-q','-i',KEY,'-P',PORT,*OPT,src,'root@127.0.0.1:'+dst])
def sha(p):return hashlib.file_digest(open(p,'rb'),'sha256').hexdigest()
def walk(tag,steps):
 assert remote("pgrep -f '^/usr/bin/retroarch' || true").strip()==''
 p=O/(tag+'.steps');p.write_text(steps+'\n');run([R/'tools/vm-visual-qa','--monitor',MON,'run',p,'--outdir',A/tag]);assert remote("pgrep -f '^/usr/bin/retroarch' || true").strip()==''
def start(lang):
 remote("systemctl stop essway; . /etc/profile >/dev/null 2>&1; set_setting system.language "+lang+"; rm -f /tmp/emulationstation.ready; : > /var/log/es_log.txt; sync; systemctl start essway")
 for i in range(60):
  if 'true' in remote('test -f /tmp/emulationstation.ready && curl -fsS --max-time 2 http://127.0.0.1:1234/isIdle || true'):break
  time.sleep(2)
 else:raise RuntimeError('ES did not become ready')
 (A/(lang+'-startup.log')).write_text(remote("grep -E 'cloud folder|cloud_setup|cloud_remote|Version|^BUILD_ID' /var/log/es_log.txt /etc/os-release 2>/dev/null || true"))
if __name__=='__main__':
 mode=sys.argv[1]
 if mode=='walk':walk(sys.argv[2],Path(sys.argv[3]).read_text())
 elif mode=='start':start(sys.argv[2])
 elif mode=='stage':
  remote('systemctl stop essway; mkdir -p /storage/qa-manual-ui')
  scp('/tmp/pixelelated-508-es-host04/emulationstation','/storage/qa-manual-ui/emulationstation');scp('/tmp/pixelelated-508-es-catalog05/artifacts/fr.mo','/storage/qa-manual-ui/fr.mo')
  proof=remote('chmod 755 /storage/qa-manual-ui/emulationstation; sync; mount --bind /storage/qa-manual-ui/emulationstation /usr/bin/emulationstation; mount --bind /storage/qa-manual-ui/fr.mo /usr/share/locale/fr/LC_MESSAGES/emulationstation2.mo; sha256sum /usr/bin/emulationstation /usr/share/locale/fr/LC_MESSAGES/emulationstation2.mo; pgrep -f "^/usr/bin/retroarch" || true')
  assert sha(Path('/tmp/pixelelated-508-es-host04/emulationstation')) in proof and sha(Path('/tmp/pixelelated-508-es-catalog05/artifacts/fr.mo')) in proof
  (A/'installed.log').write_text(proof)
  remote('cp -a /storage/.config/rclone/rclone.conf /storage/qa-manual-ui/before-rclone.conf; cp -a /storage/.config/cloud_sync.conf /storage/qa-manual-ui/before-cloud_sync.conf; rm -f /storage/.config/.restore-finish-pending; . /etc/profile >/dev/null 2>&1; set_setting global.retroachievements 0; set_setting cloudsaves.startup 0; set_setting cloudsaves.gameexit 0')
  remote("sed -i 's#<bool name=\"UseOSK\" value=\"true\" />#<bool name=\"UseOSK\" value=\"false\" />#' /storage/.config/emulationstation/es_settings.cfg; sed -i 's#<bool name=\"Debug\" value=\"false\" />#<bool name=\"Debug\" value=\"true\" />#' /storage/.config/emulationstation/es_settings.cfg; sync")
  start('en_US');walk('stage-carousel','wake\nwait 15\nshot carousel')
 else:raise ValueError(mode)

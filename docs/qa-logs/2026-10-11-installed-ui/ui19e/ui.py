from pathlib import Path
import subprocess,os,json,time,hashlib
P=Path(__file__).resolve().parent
ROOT=Path('/workspace/repos/rocknix')
ENV={**os.environ,'TMPDIR':str(P/'tmp'),'VM_PAIR_DIR':'/workspace/tmp/pixelelated-m7-upgrade19c/pair','VM_QEMU_RUNTIME_DIR':str(P/'runtime'),'CLOUD_QA_STATE':str(P/'cloud'),'CLOUD_QA_BACKEND':'webdav'}
MON=P/'runtime/rocknix-qemu-monitor-b.sock'
def guest(command,timeout=60):
 return subprocess.check_output([str(ROOT/'tools/vm-pair'),'ssh','b',command],env=ENV,text=True,timeout=timeout).strip()
def python(code):
 return subprocess.check_output([str(ROOT/'tools/vm-pair'),'ssh','b','python3 -'],input=code,env=ENV,text=True,timeout=90).strip()
def walk(name,steps):
 path=P/(name+'.steps');assert not path.exists(),name;path.write_text(steps)
 dest=P/'artifacts'/name;dest.mkdir()
 with (dest/'walk.log').open('w') as f:
  rc=subprocess.run([str(ROOT/'tools/vm-visual-qa'),'--monitor',str(MON),'run',str(path),'--outdir',str(dest)],env=ENV,stdout=f,stderr=subprocess.STDOUT).returncode
 (dest/'rc').write_text(str(rc)+'\n');assert rc==0,(name,rc)
 return dest
def restart(lang='en_US'):
 guest("systemctl stop essway; . /etc/profile >/dev/null 2>&1; set_setting system.language "+lang+"; set_setting global.retroachievements 0; set_setting global.retroachievements.username ''; set_setting cloudsaves.startup 0; set_setting cloudsaves.gameexit 0; for d in backup restore; do for k in content media settings; do set_setting cloudsync.pick.$d.$k 0; done; set_setting cloudsync.pick.$d.saves 1; done; rm -f /tmp/emulationstation.ready; systemctl start essway")
 for _ in range(90):
  if guest('test -f /tmp/emulationstation.ready && echo yes || true')=='yes':break
  time.sleep(.2)
 else:raise RuntimeError('ES not ready')
 guest("swaymsg -s /run/0-runtime-dir/sway-ipc.0.sock 'output Virtual-1 mode --custom 640x480@60Hz'")
 time.sleep(1)
 actual=json.loads(guest('swaymsg -s /run/0-runtime-dir/sway-ipc.0.sock -t get_outputs'))[0]['current_mode'];assert actual['width']==640 and actual['height']==480
 assert guest('sha256sum /usr/bin/emulationstation').split()[0]==hashlib.sha256(Path('/workspace/tmp/pixelelated-m7-image19/root/usr/bin/emulationstation').read_bytes()).hexdigest()
 return actual
HUB=(ROOT/'tools/vm-walks/to-manage-cloud-storage.steps').read_text()

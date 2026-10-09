from pathlib import Path
import subprocess,json,time,hashlib,shlex
P=Path('/workspace/tmp/pixelelated-m7-readiness-boot-01')
R=Path('/workspace/repos/rocknix.worktrees/m7-p5-frontend-readiness')
VM=Path('/workspace/tmp/pixelelated-m7-readiness-01')
opts=['-i',str(VM/'qa-key'),'-o','LogLevel=ERROR','-o','StrictHostKeyChecking=no','-o','UserKnownHostsFile=/dev/null','-o','BatchMode=yes','-o','ConnectTimeout=3']
def ssh(s,check=True,timeout=30):return subprocess.run(['ssh',*opts,'-p','10291','root@127.0.0.1',s],check=check,capture_output=True,text=True,timeout=timeout)
def copy(src,dest):subprocess.run(['scp','-q',*opts,'-P','10291',str(src),'root@127.0.0.1:'+dest],check=True,timeout=20)
def wait_idle():
 for n in range(180):
  r=ssh('curl -fsS http://127.0.0.1:1234/isIdle',check=False,timeout=5)
  if r.returncode==0 and json.loads(r.stdout)==[True]:return
  time.sleep(.5)
 raise RuntimeError('idle timeout')
def frame(name):
 subprocess.run([str(R/'tools/vm-visual-qa'),'--monitor','/tmp/pix529-01-mon.sock','settle','--help'],stdout=subprocess.DEVNULL,check=True)
 subprocess.run([str(R/'tools/vm-visual-qa'),'--monitor','/tmp/pix529-01-mon.sock','shot',str(P/name)],check=True)
# Baseline uses the original installed frontend unit, same healthy Sway.
ssh('systemctl stop essway; rm /run/systemd/system/essway.service; systemctl daemon-reload; systemctl start essway')
wait_idle();frame('original-carousel.png')
# Put the exact helper and unit in this disposable guest's persistent override.
ssh('mkdir -p /storage/.qa529 /storage/.config/system.d; printf "synthetic retained save\\n" > /storage/.qa529/save.srm')
helper=R/'projects/ROCKNIX/packages/wayland/compositor/sway/scripts/sway-ready'
copy(helper,'/storage/.qa529/sway-ready')
s=(R/'projects/ROCKNIX/packages/ui/emulationstation/system.d/essway.service').read_text().replace('/usr/bin/sway-ready','/storage/.qa529/sway-ready')
(P/'boot-essway.service').write_text(s);copy(P/'boot-essway.service','/storage/.config/system.d/essway.service')
ssh('chmod 755 /storage/.qa529/sway-ready; systemctl daemon-reload')
before=ssh('cat /proc/sys/kernel/random/boot_id; sha256sum /storage/.qa529/save.srm /storage/.qa529/sway-ready /storage/.config/system.d/essway.service').stdout
(P/'before.txt').write_text(before)
t=time.monotonic();r=ssh('systemctl reboot',check=False);(P/'reboot-request.json').write_text(json.dumps({'returncode':r.returncode,'stdout':r.stdout,'stderr':r.stderr})+'\n')
old=before.splitlines()[0]
for _ in range(90):
 time.sleep(1)
 r=ssh('cat /proc/sys/kernel/random/boot_id',check=False,timeout=5)
 if r.returncode==0 and r.stdout.strip()!=old:break
else:raise RuntimeError('new boot not observed')
wait_idle();elapsed=time.monotonic()-t
state=ssh('systemctl show essway -p NRestarts -p ActiveState -p FragmentPath; cat /proc/sys/kernel/random/boot_id; sha256sum /storage/.qa529/save.srm /storage/.qa529/sway-ready /storage/.config/system.d/essway.service').stdout
(P/'after.txt').write_text(state)
assert 'NRestarts=0' in state and 'ActiveState=active' in state and 'FragmentPath=/storage/.config/system.d/essway.service' in state
for line in before.splitlines()[1:]:assert line in state
j=ssh('journalctl -b -u essway -u sway -o short-monotonic --no-pager').stdout
(P/'boot-journal.txt').write_text(j)
assert 'Error initializing SDL!' not in j
frame('fixed-retained-boot-carousel.png')
(P/'result.json').write_text(json.dumps({'new_boot':True,'restarts':0,'sdl_errors':0,'retained_save_and_overlay_hashes_equal':True,'reboot_to_idle_seconds':round(elapsed,3),'source_overlay_not_new_firmware':True,'passed':True},indent=2)+'\n')
print((P/'result.json').read_text())

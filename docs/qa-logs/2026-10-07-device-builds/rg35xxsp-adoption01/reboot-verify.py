#!/usr/bin/env python3
"""Issue #500: one authorized reboot, followed only by read-only verification."""
from pathlib import Path
import datetime,json,os,re,subprocess,time
OWNER=Path('/workspace/tmp/pixelelated-m7-rg35xxsp-reboot-01')
STAGE=Path('/workspace/tmp/pixelelated-m7-rg35xxsp-adoption-01')
TREE=Path('/workspace/repos/rocknix.worktrees/conflict-resolution')
SSH=['ssh','-o','BatchMode=yes','-o','ConnectTimeout=8','rg35xxsp']
EXPECTED='43d0bc3bf47fd858ba8d5c55fbdf52535a0db2aa'
OLD_BOOT='33c0063d-cfd3-46f8-8e54-5ff4f9727283'
def now():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def record(name,obj):
 with (OWNER/name).open('x') as f:json.dump(obj,f,indent=2);f.write('\n')
def filter_text(s):return '\n'.join(x for x in s.splitlines() if not re.search('key|pass|token|user|psk',x,re.I))+'\n'
def read(cmd,timeout=25):
 r=subprocess.run(SSH+[cmd],capture_output=True,text=True,timeout=timeout)
 return r.returncode,filter_text(r.stdout+r.stderr)
rc=1
try:
 (OWNER/'run.path').write_text(str(TREE/os.environ['RASTERATOPS_BUILD_RUN'])+'\n')
 record('start.json',{'utc':now(),'pid':os.getpid(),'issue':500})
 assert json.loads((STAGE/'stage-result.json').read_text())['result']=='PASS'
 assert json.loads((STAGE/'owner-verification.json').read_text())['result']=='PASS'
 stage=json.loads((STAGE/'input.json').read_text());queue=stage['remote_queue'];sha=stage['sha256']
 for attempt in range(60):
  code,power=read('printf "capacity="; cat /sys/class/power_supply/battery/capacity; printf "external="; cat /sys/class/power_supply/axp20x-usb/online; printf "status="; cat /sys/class/power_supply/battery/status')
  assert code==0 and 'external=1' in power,'external power unavailable; no reboot'
  capacity=int(re.search(r'^capacity=(\d+)$',power,re.M)[1])
  print(now(),'power check',capacity,'percent; external power connected',flush=True)
  if capacity>=10:
   (OWNER/'power-before-reboot.txt').write_text(power);break
  time.sleep(30)
 else:raise RuntimeError('charging wait expired; verified update remains staged, no reboot')
 command=f'''set -e
[ "$(cat /proc/sys/kernel/random/boot_id)" = '{OLD_BOOT}' ]
[ "$(cat /sys/class/power_supply/axp20x-usb/online)" = 1 ]
[ "$(cat /sys/class/power_supply/battery/capacity)" -ge 10 ]
[ "$(tr -d '\\000' </proc/device-tree/rocknix-dt-id)" = sun50i-h700-anbernic-rg35xx-sp ]
[ "$(find /storage/.update -mindepth 1 -maxdepth 1 | wc -l)" -eq 1 ]
[ -f '{queue}' ]
if ps -eo comm | grep -E '^(retroarch.*|rclone|cloud_.*|scraper)$'; then echo 'REFUSED active game or cloud process'; exit 20; fi
if [ -e /var/run/cloud_sync.lock ]; then flock -n /var/run/cloud_sync.lock true; fi
[ "$(sha256sum '{queue}' | cut -d ' ' -f1)" = '{sha}' ]
[ "$(cat /sys/class/power_supply/axp20x-usb/online)" = 1 ]
sync
printf 'REQUESTING_AUTHORIZED_REBOOT\\n'
reboot
'''
 env=dict(os.environ,DEVICE_ACT_TIMEOUT='600')
 r=subprocess.run([str(TREE/'tools/device-act'),'rg35xxsp','M7 #500 authorized reboot to apply H700 43d0bc3bf4','--',command],env=env,capture_output=True,text=True)
 output=filter_text(r.stdout+r.stderr);(OWNER/'reboot.log').write_text(output);print(output,flush=True)
 record('reboot-command-result.json',{'utc':now(),'returncode':r.returncode,'single_attempt':True})
 assert r.returncode in (0,255) and 'REQUESTING_AUTHORIZED_REBOOT' in output,'reboot result needs investigation; never retry automatically'
 found=None
 for attempt in range(80):
  try:code,out=read('printf "boot_id="; cat /proc/sys/kernel/random/boot_id; cat /etc/os-release; systemctl show essway.service -p ActiveState -p SubState -p MainPID -p NRestarts',25)
  except subprocess.TimeoutExpired:code,out=124,'SSH timeout\n'
  (OWNER/'latest-boot-poll.txt').write_text(out)
  print(now(),'boot poll',attempt+1,'ssh_rc',code,'expected_build',EXPECTED in out,flush=True)
  if code==0 and EXPECTED in out and OLD_BOOT not in out and 'ActiveState=active' in out:
   found=out;break
  time.sleep(15)
 assert found is not None,'device did not return on expected build during bounded polling'
 code,out=read('''set -e
printf 'boot_id='; cat /proc/sys/kernel/random/boot_id
cat /etc/os-release
printf 'model='; tr '\\000' '\\n' </proc/device-tree/model
printf 'dt_id='; tr '\\000' '\\n' </proc/device-tree/rocknix-dt-id
for p in /sys/class/regulator/*; do if [ "$(cat "$p/name" 2>/dev/null)" = vdd-dram ]; then printf 'dram_microvolts='; cat "$p/microvolts"; fi; done
mount | grep -E ' on /storage | on /flash | on /storage/roms '
printf 'queue_entries='; find /storage/.update -mindepth 1 -maxdepth 1 | wc -l
sha256sum /flash/SYSTEM /flash/KERNEL /flash/dtb.img /usr/bin/emulationstation /usr/bin/retroarch /usr/bin/retroarch32
printf 'bootloader_sha256='
dd if=/dev/mmcblk0 bs=1024 skip=8 count=651 2>/dev/null | head -c 666105 | sha256sum
systemctl show essway.service -p ActiveState -p SubState -p MainPID -p NRestarts
printf 'battery_capacity='; cat /sys/class/power_supply/battery/capacity
printf 'external_power='; cat /sys/class/power_supply/axp20x-usb/online
''',600)
 (OWNER/'installed-readback.txt').write_text(out);assert code==0
 acceptance=json.loads(Path('/workspace/tmp/pixelelated-m7-h700-firmware-acceptance-01/artifacts/acceptance.json').read_text())
 arm=json.loads(Path('/workspace/tmp/pixelelated-m7-h700-firmware-acceptance-01/artifacts/arm-handoff.json').read_text())
 variant=next(v for v in acceptance['variants'] if v['variant']=='DDR4')
 expected={'/flash/SYSTEM':variant['system_sha256'],'/flash/KERNEL':variant['kernel_sha256'],'/flash/dtb.img':'bfc3503868e5e3cf99c9fe2b86f4b19cc23a1f0319847005858b6daaa67ee13d'}
 expected.update({'/'+v['path']:v['sha256'] for v in acceptance['architecture']})
 expected['/usr/bin/retroarch32']=next(v['sha256'] for v in arm if v['installed']=='usr/bin/retroarch32')
 for path,sha in expected.items():assert re.search(r'^'+sha+r'\s+'+re.escape(path)+r'$',out,re.M),path+' hash mismatch'
 for value in ['OS_NAME="pixelelated"','OS_VERSION="0.0.1"','BUILD_ID="'+EXPECTED+'"','model=Anbernic RG35XX SP','dt_id=sun50i-h700-anbernic-rg35xx-sp','dram_microvolts=1100000','queue_entries=0','ActiveState=active','/dev/mmcblk0p2 on /storage type ext4','/dev/mmcblk0p2 on /storage/roms type ext4','bootloader_sha256='+variant['bootloader_sha256']]:assert value in out,value
 boot=re.search(r'^boot_id=(.+)$',out,re.M)[1];assert boot!=OLD_BOOT
 record('acceptance.json',{'utc':now(),'result':'PASS','issue':500,'old_boot_id':OLD_BOOT,'new_boot_id':boot,'installed_build':EXPECTED,'hashes':expected,'bootloader_sha256':variant['bootloader_sha256'],'scope':'authorized update and physical boot/read-only installed verification; no gameplay, screenshot or deliberate cloud test'})
 code,journal=read('journalctl -b -p err --no-pager -n 35',40);(OWNER/'journal-errors-filtered.txt').write_text(journal)
 print(now(),'PASS RG35XX SP update applied and installed bytes verified',flush=True);rc=0
except Exception as error:
 record('error.json',{'utc':now(),'type':type(error).__name__,'message':str(error)});print(type(error).__name__,str(error),flush=True)
finally:
 for name in ['inner.rc','outer.rc']:(OWNER/name).write_text(str(rc)+'\n')
raise SystemExit(rc)

"""Installed EN/FR chooser, absence/refusal and explicit old-pointer recovery.

Only an isolated guest and local WebDAV fixture are accepted. Installed product
bytes stay unchanged; all UI actions use the real QEMU input and framebuffer.
"""
from pathlib import Path
import argparse,datetime,hashlib,json,os,re,shlex,subprocess,time
ap=argparse.ArgumentParser();ap.add_argument('--owner',type=Path,required=True);ap.add_argument('--tree',type=Path,required=True);ap.add_argument('--build-id',required=True);a=ap.parse_args()
owner=a.owner;tree=a.tree;out=owner/'artifacts/cloud-ui';out.mkdir();data=owner/'cloud/data';conf='/storage/.config/cloud_sync.conf';qa='/tmp/m7-audit-ui';case='setup';rows=[]
ssh=['ssh','-i',str(owner/'pair/qa-key'),'-p','10026','-o','BatchMode=yes','-o','ConnectTimeout=8','-o','StrictHostKeyChecking=no','-o','UserKnownHostsFile=/dev/null','-o','LogLevel=ERROR','root@127.0.0.1']
def guest(cmd,data=None,allowed=(0,)):
 r=subprocess.run(ssh+['. /etc/profile >/dev/null 2>&1; '+cmd],input=data,text=True,capture_output=True,timeout=120)
 if allowed is not None:assert r.returncode in allowed,(case,r.returncode,r.stdout,r.stderr)
 return r
def check(ok,text):
 print(('PASS ' if ok else 'FAIL ')+case+': '+text,flush=True)
 if not ok:raise AssertionError(text)
def save(name,value):(out/(case+'-'+name+'.json')).write_text(json.dumps(value,indent=2)+'\n')
def hashes():return {str(p.relative_to(data)):hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(data.rglob('*')) if p.is_file()}
def pointers():return guest("grep -E '^(SAVES|SETTINGS|CONTENT)_REMOTE=' "+conf).stdout
def put(path,value=b'QA content\n'):
 p=data/path;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(value)
def no_game(label):
 r=guest("pgrep -f '^/usr/bin/retroarch'",allowed=None)
 check(r.returncode==1,'no game running '+label)
def walk(tag,steps):
 no_game('before '+tag)
 p=out/(case+'-'+tag+'.steps');p.write_text('\n'.join(steps)+'\n')
 try:
  with (out/(case+'-'+tag+'.log')).open('w') as f:
   r=subprocess.run([str(tree/'tools/vm-visual-qa'),'--monitor','/tmp/rocknix-qemu-monitor-d.sock','run',str(p),'--outdir',str(out)],stdout=f,stderr=subprocess.STDOUT,timeout=300)
  check(r.returncode==0,'actual UI walk '+tag)
 finally:no_game('after '+tag)
def press(*keys):
 result=[]
 for k in keys:result+=['key '+k,'wait-for-change 30 0']
 return result
def screenshot(label):return ['settle 60 3','shot '+case+'-'+label]
def idle():
 for _ in range(120):
  r=guest('curl -sS -m 2 http://127.0.0.1:1234/isIdle',allowed=None)
  try:
   if r.returncode==0 and json.loads(r.stdout)==[True]:return
  except json.JSONDecodeError:pass
  time.sleep(.5)
 raise AssertionError('ES did not become idle')
def set_pointers(saves='/pixelelated/Saves',settings='/pixelelated/Backups',content='/Mine'):
 guest('python3 -',data=f'''from pathlib import Path
p=Path({conf!r});s=p.read_text().splitlines();values={dict(SAVES_REMOTE=saves,SETTINGS_REMOTE=settings,CONTENT_REMOTE=content,LAYOUT_KEEP='')!r};s=[x for x in s if not any(x.startswith(k+'=') for k in values)];p.write_text('\\n'.join(s+[k+'="'+v+'"' for k,v in values.items()])+'\\n')
''')
def start():guest('systemctl start essway');idle();walk('carousel',['wake','dismiss-dialogs'])
def reset(language):
 guest('systemctl stop essway; rm -f /storage/.config/cloud-layout-migration.json; rm -rf /storage/.cache/cloud_sync/scan; rm -f '+qa+'/sed; cp '+qa+'/rclone-original /storage/.config/rclone/rclone.conf; cp '+qa+'/sync-original '+conf)
 subprocess.run([str(tree/'tools/cloud-test-backend'),'reset'],check=True,stdout=subprocess.DEVNULL)
 guest('set_setting system.language '+language+'; set_setting global.retroachievements 0; set_setting kodi.enabled 0; set_setting cloudsaves.startup 0; set_setting cloudsaves.gameexit 0; set_setting cloudsync.pick.restore.saves 1; set_setting cloudsync.pick.restore.content 0; set_setting cloudsync.pick.restore.media 0; set_setting cloudsync.pick.restore.settings 0')
 set_pointers();put('pixelelated/.layout',b'layout=2\n');put('pixelelated/Saves/gb/A.srm',b'save witness\n');(data/'pixelelated/Backups').mkdir(parents=True)
def hub(tag='hub'):
 walk(tag+'-menu',['wake','dismiss-dialogs']+screenshot('menu-before')+press('ret')+screenshot('main-menu'))
 before=list(out.glob('*'+case+'-menu-before.png'));after=list(out.glob('*'+case+'-main-menu.png'))
 check(len(before)==1 and len(after)==1 and before[0].read_bytes()!=after[0].read_bytes(),'START changes the captured screen; direct main-menu review required')
 walk(tag,press('x','up','up','up','x')+screenshot('hub'))
def restore():
 hub();walk('opening-scan',press('down','x')+['settle 90 3','shot '+case+'-opening-result'])
def content_continue():
 # Source row order: saves, ROMs/BIOS, media, dimmed settings, then BACK/CONTINUE.
 walk('continue',press('down','x')+screenshot('content-ticked')+press('up','up','right','x')+screenshot('content-outcome'))

def immediate_shot(label):
 p=out/(case+'-'+label+'.png')
 subprocess.run([str(tree/'tools/vm-visual-qa'),'--monitor','/tmp/rocknix-qemu-monitor-d.sock','shot',str(p)],check=True,stdout=subprocess.DEVNULL,timeout=20)
 return p

def install_shim(name,body):
 guest('cat > '+qa+'/'+name+'; chmod 755 '+qa+'/'+name,data=body)
 check(guest('command -v '+name).stdout.strip()==qa+'/'+name,'private QA '+name+' fault selected')

def startup_timeout():
 # Same real second-marker-read stall as audit R03, now reached by installed
 # ES's actual startup worker. The timeout observer delegates to stock timeout.
 subprocess.run([str(tree/'tools/cloud-test-backend'),'reset'],check=True,stdout=subprocess.DEVNULL)
 set_pointers('/ROCKNIX/Saves','/ROCKNIX/Backups','/ROCKNIX/Content')
 put('ROCKNIX/Saves/gb/A.srm',b'old save\n');put('pixelelated/.layout',b'layout=2\n')
 remote=guest('/usr/bin/rclone listremotes').stdout.strip()
 check(re.fullmatch(r'[A-Za-z0-9_-]+:',remote) is not None,'one local QA remote')
 install_shim('timeout',f'''#!/bin/sh
if [ "$1" = 30 ] && [ "$2" = /usr/bin/cloud_scan ] && [ "$3" = --folder ]; then
 cut -d' ' -f1 /proc/uptime > {qa}/timeout-start
 /usr/bin/timeout "$@"
 rc=$?
 cut -d' ' -f1 /proc/uptime > {qa}/timeout-end
 echo "$rc" > {qa}/timeout-result
 exit "$rc"
fi
exec /usr/bin/timeout "$@"
''')
 install_shim('rclone',f'''#!/bin/sh
if [ -f {qa}/timeout-start ] && [ ! -f {qa}/timeout-result ] && [ "$1" = cat ] && [ "$2" = "{remote}/pixelelated/.layout" ]; then
 count=0
 [ ! -r {qa}/marker-read-count ] || read -r count < {qa}/marker-read-count
 count=$((count + 1)); echo "$count" > {qa}/marker-read-count
 if [ "$count" = 2 ]; then
  echo $$ > {qa}/timeout-rclone-pid
  sleep 45 & echo $! > {qa}/timeout-sleep-pid
  wait
 fi
fi
exec /usr/bin/rclone "$@"
''')
 before=hashes(),pointers()
 guest('rm -f /storage/.cache/cloud_sync/last-sync-startup; set_setting cloudsaves.startup 1; systemctl start essway')
 deadline=time.monotonic()+110;stamp=''
 while time.monotonic()<deadline:
  stamp=guest('cat /storage/.cache/cloud_sync/last-sync-startup 2>/dev/null',allowed=None).stdout
  if stamp:break
  time.sleep(.2)
 check(bool(stamp),'actual installed ES startup outcome stamp appeared')
 frames=[]
 for i in range(3):
  frames.append(str(immediate_shot('timeout-card-'+str(i))))
  time.sleep(.5)
 expected="THE CLOUD TOOK TOO LONG - IT'LL TRY AGAIN NEXT TIME"
 check(' 124 cloud-stopped '+expected in stamp,'actual startup stamp retains exact outer timeout reason')
 timing=guest('cat '+qa+'/timeout-start '+qa+'/timeout-end '+qa+'/timeout-result').stdout.splitlines()
 elapsed=float(timing[1])-float(timing[0]);check(timing[2]=='124' and 29<=elapsed<38,'stock outer timeout enforced its real thirty-second bound')
 check((hashes(),pointers())==before,'outer-timeout refusal preserves cloud and pointers')
 child=guest('for n in rclone sleep; do p=$(cat '+qa+'/timeout-${n}-pid); test ! -e /proc/$p || exit 1; done',allowed=None)
 check(child.returncode==0,'timed-out provider and sleep child actually exited')
 save('timeout',dict(stamp=stamp,seconds=elapsed,before=before,after=(hashes(),pointers()),frames=frames,visual_review='pending',scope='Installed ES startup path; stock timeout, only second local provider marker read deliberately delayed'))
 guest('set_setting cloudsaves.startup 0; rm -f '+qa+'/rclone '+qa+'/timeout')

def binding_recovery():
 subprocess.run([str(tree/'tools/cloud-test-backend'),'reset'],check=True,stdout=subprocess.DEVNULL)
 set_pointers('/ROCKNIX/Saves','/ROCKNIX/Backups','/ROCKNIX/Content')
 put('ROCKNIX/Saves/gb/A.srm',b'save witness\n');put('ROCKNIX/Content/ROMs/gb/A.gb',b'content witness\n')
 remote=guest('/usr/bin/rclone listremotes').stdout.strip()
 install_shim('rclone',f'''#!/bin/sh
if [ "$1" = copy ] && [ "$2" = "{remote}/ROCKNIX/Content" ]; then
 echo fired > {qa}/copy-fired
 exit 5
fi
exec /usr/bin/rclone "$@"
''')
 first=guest('/usr/bin/cloud_migrate_layout --apply',allowed=None)
 check(first.returncode!=0 and guest('test -s '+qa+'/copy-fired',allowed=None).returncode==0,'installed real partial migration created before endpoint change')
 guest('rm '+qa+'/rclone')
 record='/storage/.config/cloud-layout-migration.json'
 record_before=guest('sha256sum '+record).stdout.split()[0]
 original_url=guest("/usr/bin/rclone config dump | python3 -c 'import json,sys; print(next(iter(json.load(sys.stdin).values()))[\"url\"])'").stdout.strip()
 check(original_url.startswith('http://10.0.2.2:9040'),'owned local endpoint only')
 put('other-cloud/foreign-witness.txt',b'foreign endpoint witness\n')
 guest('/usr/bin/rclone config update '+shlex.quote(remote.rstrip(':'))+' url '+shlex.quote(original_url.rstrip('/')+'/other-cloud/')+' --non-interactive >/dev/null')
 before=hashes(),pointers();start();restore()
 refused=guest('/usr/bin/cloud_scan --folder',allowed=None)
 check(refused.returncode!=0 and 'THE PREVIOUS CLOUD MOVE NEEDS ITS ORIGINAL CONNECTION' in refused.stdout,'changed endpoint preserves truthful original-connection reason')
 check((hashes(),pointers())==before and guest('sha256sum '+record).stdout.split()[0]==record_before,'refusal leaves all source/partial files, pointers and binding untouched')
 walk('leave-refusal',['dismiss-dialogs']);hub()
 walk('repair-entry',press(*(['down']*8))+screenshot('connect-repair-row')+press('x')+screenshot('providers'))
 # Last provider-list action is USE A COMPUTER INSTEAD; preceding wrap is BACK.
 walk('computer-path',press('up','up','x')+screenshot('computer-setup'))
 # Existing remote check, CLOUD FOLDER, ADD ANOTHER, REPAIR A CONNECTION.
 walk('repair-choice',press('down','down','down','x')+screenshot('ssh-setup'))
 # Current fixtures already have a real test password and live SSH service.
 walk('ssh-continue',press('down','right','x')+screenshot('ssh-connect'))
 session=subprocess.Popen(ssh+['sleep 300'],stdin=subprocess.DEVNULL,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
 try:
  time.sleep(.4)
  walk('connection-continue',press('down','down','right','x')+screenshot('repair-instructions'))
  # This is the real noninteractive equivalent of editing URL in rclone config,
  # reached through the product's documented terminal recovery surface.
  guest('/usr/bin/rclone config update '+shlex.quote(remote.rstrip(':'))+' url '+shlex.quote(original_url)+' --non-interactive >/dev/null')
  check(guest('sha256sum '+record).stdout.split()[0]==record_before,'terminal repair does not rebind or replace the pending record')
  walk('verify-repaired-connection',press('right','x')+screenshot('retry-owned-move'))
  walk('retry-owned-move',press('x')+screenshot('move-finished'))
  check(guest('test ! -e '+record,allowed=None).returncode==0,'real UI retry completed and removed owned migration record')
  check((data/'pixelelated/Saves/gb/A.srm').read_bytes()==b'save witness\n' and (data/'pixelelated/Content/ROMs/gb/A.gb').read_bytes()==b'content witness\n','both source tiers survive supported recovery')
  check((data/'other-cloud/foreign-witness.txt').read_bytes()==b'foreign endpoint witness\n','other endpoint unchanged')
  save('binding-recovery',dict(refusal_stdout=refused.stdout,record_before=record_before,before=before,after=(hashes(),pointers()),recovery='Actual UI terminal-repair route plus installed rclone config update URL, then actual UI pending-move retry',visual_review='pending'))
 finally:
  session.terminate();session.wait(timeout=10)

def absence_control():
 subprocess.run([str(tree/'tools/cloud-test-backend'),'reset'],check=True,stdout=subprocess.DEVNULL)
 put('pixelelated/.layout',b'layout=2\n');before=hashes(),pointers();start();restore()
 state=guest('cat /storage/.cache/cloud_sync/scan/state').stdout
 check('CURRENT_EXISTS=0' in state,'genuine missing saves folder is classified absent')
 check((hashes(),pointers())==before,'missing folder offers creation without silently writing')
 save('absence',dict(state=state,cloud=hashes(),pointers=pointers(),visual_review='pending actual create-folder offer'))

def network_control():
 import socket
 reserved=socket.socket();reserved.bind(('127.0.0.1',0));port=reserved.getsockname()[1]
 try:
  remote=guest('/usr/bin/rclone listremotes').stdout.strip()
  guest('/usr/bin/rclone config update '+shlex.quote(remote.rstrip(':'))+' url '+shlex.quote('http://10.0.2.2:'+str(port)+'/')+' --non-interactive >/dev/null')
  before=hashes(),pointers();start();restore()
  result=guest('/usr/bin/cloud_scan --folder',allowed=None)
  check(result.returncode!=0 and 'YOUR CLOUD STOPPED ANSWERING' in result.stdout,'real closed local endpoint gives transport reason')
  check((hashes(),pointers())==before,'transport refusal preserves all state')
  save('transport',dict(stdout=result.stdout,returncode=result.returncode,cloud=hashes(),pointers=pointers(),visual_review='pending'))
 finally:reserved.close()

# The runner has provisioned a unique local endpoint. Never print its config.
check(guest("sed -n 's/^BUILD_ID=//p' /etc/os-release").stdout.strip().strip('"')==a.build_id,'candidate identity')
config=subprocess.check_output([str(tree/'tools/cloud-test-backend'),'rclone-conf'],text=True)
guest('systemctl stop essway; mkdir -p /storage/.config/rclone; cat > /storage/.config/rclone/rclone.conf; chmod 600 /storage/.config/rclone/rclone.conf; /usr/bin/cloud_sync_helper',data=config)
guest('test ! -e '+qa+'; mkdir '+qa+'; cp /storage/.config/rclone/rclone.conf '+qa+'/rclone-original; cp '+conf+' '+qa+'/sync-original; mkdir -p /storage/.config/profile.d; printf "%s\\n" '+shlex.quote('export PATH='+qa+':$PATH')+' > /storage/.config/profile.d/999-audit-ui.sh')
guest('python3 -',data='''from pathlib import Path
import xml.etree.ElementTree as E
p=Path('/storage/.config/emulationstation/es_settings.cfg');r=E.parse(p);root=r.getroot()
for name,value in [('Debug','true'),('UseOSK','false')]:
 item=next((n for n in root if n.get('name')==name),None)
 if item is None:item=E.SubElement(root,'bool',name=name)
 item.set('value',value)
r.write(p,encoding='unicode')
''')
before=guest('sha256sum /usr/bin/emulationstation /usr/bin/cloud_scan /usr/bin/cloud_migrate_layout /usr/bin/cloud_setup /usr/bin/cloud_content_restore').stdout
(out/'installed-before.sha256').write_text(before)

original_reset=reset
def reset(language):
 guest('systemctl stop essway; rm -f '+qa+'/rclone '+qa+'/timeout '+qa+'/timeout-start '+qa+'/timeout-end '+qa+'/timeout-result '+qa+'/marker-read-count '+qa+'/timeout-rclone-pid '+qa+'/timeout-sleep-pid '+qa+'/copy-fired')
 original_reset(language)
 # Throwaway password only on this loopback QA guest; required by the real
 # SSH recovery wizard. No personal credential or external account is used.
 guest('set_setting root.password qa-m7-local-only; setrootpass qa-m7-local-only')
try:
 for language in ['en_US','fr_FR']:
  for name,action in [('outer-timeout',startup_timeout),('original-connection-recovery',binding_recovery),('missing-folder',absence_control),('network-refusal',network_control)]:
   case=language+'-'+name;print('START '+case,flush=True);reset(language);action()
   rows.append({'case':case,'status':'PASS','visual_review':'pending'});(out/'results.json').write_text(json.dumps(rows,indent=2)+'\n')
finally:
 after=guest('sha256sum /usr/bin/emulationstation /usr/bin/cloud_scan /usr/bin/cloud_migrate_layout /usr/bin/cloud_setup /usr/bin/cloud_content_restore').stdout
 (out/'installed-after.sha256').write_text(after);check(after==before,'installed product hashes unchanged')
print('PASS actual timeout/recovery/refusal cases; primary visual review required',flush=True)

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
 label=re.sub(r'[^a-zA-Z0-9_-]+', '-', case).strip('-')
 before=list(out.glob('*'+label+'-menu-before.png'));after=list(out.glob('*'+label+'-main-menu.png'))
 check(len(before)==1 and len(after)==1 and before[0].read_bytes()!=after[0].read_bytes(),'START changes the captured screen; direct main-menu review required')
 walk(tag,press('x','up','up','up','x')+screenshot('hub'))
def restore():
 hub();walk('opening-scan',press('down','x')+['settle 90 3','shot '+case+'-opening-result'])
def content_continue():
 # Source row order: saves, ROMs/BIOS, media, dimmed settings, then BACK/CONTINUE.
 walk('continue',press('down','x')+screenshot('content-ticked')+press('up','up','right','x')+screenshot('content-outcome'))
def chooser(folder):
 for name in ['MyGames','My Games','Games..old']:put(name+'/ROMs/gb/Chosen.gb',b'chosen game\n')
 put('Mine/Photos/witness.jpg',b'unrelated picture\n');before=hashes();start();restore();content_continue()
 check('STATE=empty' in guest('cat /storage/.cache/cloud_sync/scan/content-location').stdout,'unrelated configured folder offers manual selection')
 walk('chooser',press('x')+screenshot('chooser'))
 offered=['/']+['/'+n for n in guest('cat /storage/.cache/cloud_sync/scan/root-dirs').stdout.splitlines() if n]
 check('/'+folder in offered,'actual opening scan lists '+folder)
 walk('select',press(*(['down']*offered.index('/'+folder)))+screenshot('chosen-row')+press('x')+screenshot('systems-after-selection'))
 check('CONTENT_REMOTE="/'+folder+'"' in pointers(),'actual UI persists '+folder)
 check(guest('test -s /storage/.cache/cloud_sync/scan/content-done',allowed=None).returncode==0,'chosen content scan completed')
 check(re.search(r'^gb\|12\|',guest('cat /storage/.cache/cloud_sync/scan/scan').stdout,re.M),'selected game appears in actual scan')
 check(hashes()==before,'selection preserves every cloud byte')
 save('selection',dict(offered=offered,selected=folder,pointers=pointers(),cloud=hashes()))
 walk('close',['dismiss-dialogs'])
def root_content():
 put('gb/Root.gb',b'root game\n');put('Mine/Photos/witness.jpg');before=hashes();start();restore();content_continue()
 check('CONTENT_REMOTE=""' in pointers(),'stranded root selected by real UI')
 check(guest('test -s /storage/.cache/cloud_sync/scan/content-done',allowed=None).returncode==0,'legacy root scan completed')
 check(re.search(r'^gb\|10\|',guest('cat /storage/.cache/cloud_sync/scan/scan').stdout,re.M),'legacy root game visible')
 check(hashes()==before,'legacy root files unchanged');save('root',dict(pointers=pointers(),cloud=hashes()));walk('close',['dismiss-dialogs'])
def reason(kind):
 if kind in ['future','malformed']:put('pixelelated/.layout',b'layout=999\n' if kind=='future' else b'layout=2\nextra\n')
 elif kind=='record':guest("printf '{invalid' > /storage/.config/cloud-layout-migration.json")
 else:guest("printf 'export SETTINGS_REMOTE=bad\\n' >> "+conf)
 expected="YOUR CLOUD SYNC SETTINGS COULDN'T BE READ" if kind=='config' else "YOUR CLOUD FOLDER COULDN'T BE READ"
 before=(hashes(),pointers());start();restore()
 result=guest('/usr/bin/cloud_scan --folder',allowed=None)
 check(result.returncode!=0 and '>>> why '+expected in result.stdout,'installed application emits '+expected)
 check("COULDN'T FIND YOUR CLOUD FOLDER" not in result.stdout,'no false missing-folder reason')
 check((hashes(),pointers())==before,'refusal preserves cloud/pointers')
 save('reason',dict(expected=expected,returncode=result.returncode,stdout=result.stdout,cloud=hashes(),pointers=pointers(),frame_review='pending actual localized opening-result frame'))
 walk('close',['dismiss-dialogs'])
def partial_recovery():
 set_pointers('/ROCKNIX/Saves','/ROCKNIX/Backups','/ROCKNIX/Content')
 old=subprocess.check_output(['git','-C',str(tree),'show','7afa9efcfc0c1ce4b89774b38878fc1b9a9063d2:projects/ROCKNIX/packages/network/rclone/sources/cloud_migrate_layout'],text=True)
 guest('cat > '+qa+'/old-writer; chmod 755 '+qa+'/old-writer',data=old)
 guest('cat > '+qa+'/sed; chmod 755 '+qa+'/sed',data='#!/bin/bash\nif [[ "$*" == *"^SETTINGS_REMOTE="* ]]; then echo fired > '+qa+'/fired; exit 1; fi\nexec /usr/bin/sed "$@"\n')
 result=guest(qa+'/old-writer --follow',allowed=None);guest('test -s '+qa+'/fired; rm '+qa+'/sed')
 check(result.returncode!=0,'actual old writer leaves partial pointers');partial=pointers();check('SAVES_REMOTE="/pixelelated/Saves"' in partial and 'SETTINGS_REMOTE="/ROCKNIX/Backups"' in partial,'old partial state reproduced')
 before=hashes();start();hub()
 steps=(tree/'tools/vm-walks/to-change-cloud-folder.steps').read_text().splitlines()
 # Prefix captured filenames so each language/case retains its own frames.
 steps=[line.replace('shot ','shot '+case+'-') if line.startswith('shot ') else line for line in steps]
 walk('folder-editor',steps)
 walk('save-selection',press('down','x')+screenshot('recovered-folder-row'))
 final=pointers();check(all(k+'="/pixelelated/'+v+'"' in final for k,v in [('SAVES_REMOTE','Saves'),('SETTINGS_REMOTE','Backups'),('CONTENT_REMOTE','Content')]),'real editor repairs complete sibling pointers')
 check(hashes()==before,'editor recovery keeps cloud bytes');save('recovery',dict(predecessor_sha256=hashlib.sha256(old.encode()).hexdigest(),partial=partial,after=final,cloud=hashes()));walk('close',['dismiss-dialogs'])
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
try:
 for language in ['en_US','fr_FR']:
  cases=[('chooser-'+folder,lambda f=folder:chooser(f)) for folder in ['MyGames','My Games','Games..old']]
  cases += [('legacy-root',root_content),('old-pointer-recovery',partial_recovery)]
  cases += [('reason-'+kind,lambda k=kind:reason(k)) for kind in ['future','malformed','config','record']]
  for name,action in cases:
   case=language+'-'+name;print('START '+case,flush=True)
   reset(language);action();rows.append({'case':case,'status':'PASS','visual_review':'pending'});(out/'results.json').write_text(json.dumps(rows,indent=2)+'\n')
finally:
 after=guest('sha256sum /usr/bin/emulationstation /usr/bin/cloud_scan /usr/bin/cloud_migrate_layout /usr/bin/cloud_setup /usr/bin/cloud_content_restore').stdout
 (out/'installed-after.sha256').write_text(after);check(after==before,'installed product hashes unchanged')
print('PASS actual chooser/recovery/refusal actions; all frames require primary review',flush=True)

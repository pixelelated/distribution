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
def archive_bytes(label, member, contents):
 import io,tarfile
 stream=io.BytesIO()
 with tarfile.open(fileobj=stream,mode='w:gz') as tar:
  info=tarfile.TarInfo(member);info.size=len(contents);info.mode=0o644
  tar.addfile(info,io.BytesIO(contents))
 return stream.getvalue()

def clear_fixture_cloud():
 subprocess.run([str(tree/'tools/cloud-test-backend'),'reset'],check=True,stdout=subprocess.DEVNULL)

import importlib.util
seed_spec=importlib.util.spec_from_file_location('seed_oracle',owner/'seed-oracle.py')
seed_oracle=importlib.util.module_from_spec(seed_spec);seed_spec.loader.exec_module(seed_oracle)

def archive_setup(root):
 clear_fixture_cloud()
 label=guest('/usr/bin/cloud_device_id --label').stdout.strip()
 device=guest('/usr/bin/cloud_device_id').stdout.strip()
 check(bool(re.fullmatch(r'[A-Za-z0-9_-]+',label)),'actual archive label safe')
 name='2026_10_06-000000-'+label+'-ROCKNIX_SETTINGS.tar.gz'
 backups=root+('/backup' if root=='/GAMES' else '/Backups')
 saves=root if root=='/GAMES' else root+'/Saves'
 set_pointers(saves,backups,'' if root=='/GAMES' else root+'/Content')
 witness=('setup-preserves-'+root+'\n').encode()
 content=archive_bytes(label,'storage/.config/m7-setup-archive-sentinel',witness)
 put(backups.lstrip('/')+'/'+device+'/'+name,content)
 before=hashes();old=pointers()
 save('before-seed',dict(cloud=before,pointers=old))
 guest('/usr/bin/cloud_setup --seed-folders')
 setup=pointers();seeded=hashes();notes=seed_oracle.expected_notes(setup)
 save('after-seed',dict(cloud=seeded,pointers=setup,expected_notes=notes))
 check(seed_oracle.valid_seed(before,seeded,notes),'setup preserves archive and writes only exact source-defined notes/current marker')
 guest('/usr/bin/cloud_scan')
 facts=dict(line.split('=',1) for line in guest('cat /storage/.cache/cloud_sync/scan/settings').stdout.splitlines() if '=' in line)
 check(facts.get('MINE')==name,'setup and full scan retain selected same-device archive')
 cloud=data/facts['SOURCE'].split(':',1)[1].lstrip('/')/name
 check(cloud.read_bytes()==content,'selected archive hash preserved')
 guest("printf 'changed locally\n' > /storage/.config/m7-setup-archive-sentinel; /usr/bin/cloud_restore --yes --system-only; /usr/bin/backuptool restore --no-restart")
 restored=guest('sha256sum /storage/.config/m7-setup-archive-sentinel').stdout.split()[0]
 check(restored==hashlib.sha256(witness).hexdigest(),'installed recovery restores exact sentinel')
 after=hashes()
 save('after-restore',dict(cloud=after,pointers=pointers(),facts=facts,sentinel_sha256=restored))
 check(all(after.get(p)==h for p,h in before.items()),'setup/scan/restore preserve every original cloud archive byte')
 check(seed_oracle.valid_seed(before,after,notes),'only exact source-defined notes/current marker accompany original archive')
 check(after==seeded,'scan and restore make no additional cloud changes')
 save('archive',dict(root=root,before_pointers=old,after_setup=setup,after_restore=pointers(),facts=facts,archive_sha256=hashlib.sha256(content).hexdigest(),sentinel_sha256=restored,cloud=hashes()))
 guest('rm -f /storage/.config/.restore-finish-pending')

def foreign_hostname():
 device=guest('/usr/bin/cloud_device_id').stdout.strip()
 name='2026_10_06-235959-FOREIGN-QA-ROCKNIX_SETTINGS.tar.gz'
 payload=archive_bytes('FOREIGN-QA','storage/.config/system.cfg',b'system.hostname=FOREIGN-QA-MUST-NOT-RESTORE\n')
 put('pixelelated/Backups/'+device+'/'+name,payload)
 guest('set_setting system.hostname M7-OWNED-HOSTNAME-WITNESS')
 before=guest('get_setting system.hostname').stdout.strip();cloud=hashes()
 local_before=guest("find /storage/roms/backup -maxdepth 1 -type f -name '*_SETTINGS.tar.gz' -exec sha256sum '{}' ';' | sort").stdout
 start();restore()
 facts=dict(line.split('=',1) for line in guest('cat /storage/.cache/cloud_sync/scan/settings').stdout.splitlines() if '=' in line)
 check(facts.get('MINE')=='' and facts.get('NEWEST')==name,'completed scan sees foreign archive but selects none for UI')
 check(guest('test -s /storage/.cache/cloud_sync/scan/done',allowed=None).returncode==0,'foreign scan completed')
 walk('foreign-row',screenshot('foreign-settings-disabled')+['dismiss-dialogs'])
 after=guest('get_setting system.hostname').stdout.strip()
 check(after==before=='M7-OWNED-HOSTNAME-WITNESS','foreign-only UI leaves hostname unchanged')
 local_after=guest("find /storage/roms/backup -maxdepth 1 -type f -name '*_SETTINGS.tar.gz' -exec sha256sum '{}' ';' | sort").stdout
 check(local_before==local_after and hashes()==cloud,'foreign-only UI changes neither local archives nor cloud')
 save('foreign-hostname',dict(before=before,after=after,facts=facts,local_archives_before=local_before,local_archives_after=local_after,cloud=hashes(),scope='Real UI restore options and disabled settings row. Does not invoke the intentional broader console restore fallback.'))

def kill_during_move():
 clear_fixture_cloud();set_pointers('/ROCKNIX/Saves','/ROCKNIX/Backups','/ROCKNIX/Content')
 label=guest('/usr/bin/cloud_device_id --label').stdout.strip()
 device=guest('/usr/bin/cloud_device_id').stdout.strip()
 name='2026_10_06-120000-'+label+'-ROCKNIX_SETTINGS.tar.gz'
 # Valid incompressible archive ensures the first real copy remains measurable.
 payload=b''.join(hashlib.sha256(str(i).encode()).digest() for i in range(262144))
 archive=archive_bytes(label,'storage/.config/m7-large-copy-witness',payload)
 relative='Backups/'+device+'/'+name
 put('ROCKNIX/'+relative,archive)
 put('ROCKNIX/Saves/gb/Conflict.srm',b'earlier cloud save\n')
 put('ROCKNIX/Saves-replaced/gb/Older.srm',b'earlier discarded save\n')
 put('ROCKNIX/Content/ROMs/gb/Witness.gb',b'content witness\n')
 before=hashes();old=pointers()
 guest('python3 -',data=f'''from pathlib import Path
p=Path({conf!r});s=p.read_text().splitlines();s=[x for x in s if not x.startswith('RCLONE_NET_OPTS=')];p.write_text('\\n'.join(s)+'\\nRCLONE_NET_OPTS="--contimeout 5s --timeout 15s --low-level-retries 1 --retries 1 --bwlimit 256k --disable copy"\\n')
''')
 start();restore();walk('move-first',press('x')+['wait 2','shot '+case+'-first-copy-running'])
 target=data/'pixelelated'/relative
 observed=None
 for _ in range(100):
  if target.is_file() and 0<target.stat().st_size<len(archive):
   observed={'destination_bytes':target.stat().st_size,'source_bytes':len(archive),'observed_utc':datetime.datetime.now(datetime.timezone.utc).isoformat()};break
  time.sleep(.1)
 save('first-copy-observation',dict(partial=observed,cloud=hashes(),before=before,pointers=pointers()))
 check(observed is not None,'actual first copy wrote a strict partial destination')
 killed=guest('python3 -',data='''from pathlib import Path
import json,os,signal
matches=[]
for p in Path('/proc').glob('[0-9]*/cmdline'):
 try:a=[x.decode() for x in p.read_bytes().split(b'\\0') if x]
 except (OSError,UnicodeError):continue
 if len(a)>3 and Path(a[0]).name=='rclone' and a[1]=='copy' and '/ROCKNIX/Backups' in a[2] and '/pixelelated/Backups' in a[3]:
  matches.append((int(p.parent.name),a, (p.parent/'stat').read_text().rsplit(')',1)[1].split()[19]))
assert len(matches)==1,matches
pid,argv,start=matches[0];assert Path('/proc',str(pid),'stat').read_text().rsplit(')',1)[1].split()[19]==start
os.kill(pid,signal.SIGKILL)
print(json.dumps({'pid':pid,'argv':argv,'start_ticks':start,'signal':'SIGKILL'}))
''')
 kill=json.loads(killed.stdout)
 save('killed-copy',dict(partial=observed,killed=kill))
 walk('interrupted',screenshot('copy-interrupted')+['dismiss-dialogs'])
 check(all((data/p).is_file() and hashlib.sha256((data/p).read_bytes()).hexdigest()==h for p,h in before.items()),'kill during copy preserved every old source byte')
 check(pointers()==old,'incomplete first copy did not publish new pointers')
 check(guest('test -s /storage/.config/cloud-layout-migration.json',allowed=None).returncode==0,'interrupted migration retains recovery record')
 guest('python3 -',data=f'''from pathlib import Path
p=Path({conf!r});s=p.read_text().replace(' --bwlimit 256k --disable copy','');p.write_text(s)
''')
 restore();walk('move-second',press('x')+['wait 1','shot '+case+'-second-copy-running','settle 180 3','shot '+case+'-second-move-done'])
 check(all((data/('pixelelated/'+p.split('/',1)[1])).is_file() and hashlib.sha256((data/('pixelelated/'+p.split('/',1)[1])).read_bytes()).hexdigest()==h for p,h in before.items()),'second real UI MOVE completed all original bytes')
 check(not any((data/'ROCKNIX').rglob('*')) if (data/'ROCKNIX').exists() else True,'old source folder removed after verified second MOVE')
 check((data/'pixelelated/.layout').read_bytes()==b'layout=2\n','second MOVE writes final marker')
 walk('close',['dismiss-dialogs'])
 def legacy_parent_snapshot():
  parent=data/'ROCKNIX'
  if not parent.exists():return {'exists':False,'entries':[]}
  st=parent.stat()
  return {'exists':True,'device':st.st_dev,'inode':st.st_ino,'entries':[str(p.relative_to(parent)) for p in sorted(parent.rglob('*'))]}
 legacy_before=legacy_parent_snapshot()
 check(not legacy_before['entries'],'no old-root descendants remain before next backup')
 save('legacy-parent-before-backup',legacy_before)
 guest('systemctl stop essway; mkdir -p /storage/roms/gb; printf "newer local save with different size\\n" > /storage/roms/gb/Conflict.srm; /usr/bin/cloud_backup --yes --saves-only')
 check((data/'pixelelated/Saves/gb/Conflict.srm').read_bytes()==b'newer local save with different size\n','next actual backup publishes new save')
 kept=[p for p in (data/'pixelelated/Saves-replaced').rglob('Conflict.srm') if p.read_bytes()==b'earlier cloud save\n']
 check(len(kept)==1,'next conflicting backup keeps displaced bytes under current discarded-save shelf')
 legacy_after=legacy_parent_snapshot()
 save('legacy-parent-after-backup',legacy_after)
 check(legacy_after==legacy_before,'next backup preserves the prior empty-or-absent old parent exactly')
 save('mid-copy-retry-and-shelf',dict(before=before,partial=observed,killed=kill,after=hashes(),pointers=pointers(),new_shelf=str(kept[0].relative_to(data)),legacy_parent_before=legacy_before,legacy_parent_after=legacy_after,scope='First and second MOVE are actual UI actions; killed actual installed rclone after partial bytes existed. Next shelf is from actual installed cloud_backup.'))

def fresh_roots():
 clear_fixture_cloud();set_pointers('/pixelelated/Saves','/pixelelated/Backups','/pixelelated/Content')
 guest('/usr/bin/cloud_setup --seed-folders')
 paths=sorted(str(p.relative_to(data)) for p in data.rglob('*') if p.is_dir())
 check(all((data/p).is_dir() for p in ['pixelelated/Saves','pixelelated/Backups','pixelelated/Content/ROMs','pixelelated/Content/BIOS']),'fresh setup creates current three tiers and content subfolders')
 check(not (data/'ROCKNIX').exists() and not (data/'Rasteratops').exists(),'fresh cloud contains no earlier branded root')
 # I337-L40 requires use after backup and sync, not only seeded directories.
 guest('systemctl stop essway; mkdir -p /storage/roms/gb; printf "fresh save witness\\n" > /storage/roms/gb/M7Fresh.srm; printf "fresh content witness\\n" > /storage/roms/gb/M7Fresh.gb')
 def operation(label, command):
     r = guest(command, allowed=None)
     (out/(case+'-'+label+'.log')).write_text(r.stdout+r.stderr)
     check(r.returncode in (0, 9), label+' installed command completes')
     return r
 before_archives=guest("find /storage/roms/backup -maxdepth 1 -type f -name '*_SETTINGS.tar.gz' -exec sha256sum '{}' ';' | sort").stdout
 operation('make-settings-backup','/usr/bin/backuptool backup')
 after_archives=guest("find /storage/roms/backup -maxdepth 1 -type f -name '*_SETTINGS.tar.gz' -exec sha256sum '{}' ';' | sort").stdout
 def archive_hashes(text):
     return {line.split(None,1)[1]:line.split(None,1)[0] for line in text.splitlines() if line.strip()}
 prior=archive_hashes(before_archives);local=archive_hashes(after_archives)
 generated={name:sha for name,sha in local.items() if prior.get(name)!=sha}
 check(bool(generated),'real backuptool created or updated a settings archive')
 operation('settings-upload','/usr/bin/cloud_backup --yes --system-only')
 operation('content-upload','/usr/bin/cloud_content_backup gb')
 put('pixelelated/Saves/gb/M7FreshRemote.srm',b'remote sync witness\n')
 operation('automatic-receive','/usr/bin/cloud_restore --yes --method=copy --update --saves-only --automatic')
 check(guest('sha256sum /storage/roms/gb/M7FreshRemote.srm').stdout.split()[0]==hashlib.sha256(b'remote sync witness\n').hexdigest(),'installed automatic receive restores the remote save witness')
 operation('automatic-send','/usr/bin/cloud_backup --yes --method=copy --update --saves-only --automatic')
 check((data/'pixelelated/Saves/gb/M7Fresh.srm').read_bytes()==b'fresh save witness\n','installed automatic send publishes the local save witness')
 check((data/'pixelelated/Content/ROMs/gb/M7Fresh.gb').read_bytes()==b'fresh content witness\n','actual content backup uses the current Content tier')
 cloud=hashes()
 for name,sha in generated.items():
     found=[path for path,h in cloud.items() if path.startswith('pixelelated/Backups/') and Path(path).name==Path(name).name and h==sha]
     check(len(found)==1,'generated settings archive reaches current Backups tier byte-identical')
 check(all(path.startswith('pixelelated/') for path in cloud),'all actual cloud writes stay under the current root')
 listing=subprocess.check_output([str(tree/'tools/cloud-test-backend'),'ls'],text=True)
 (out/(case+'-backend-ls.txt')).write_text(listing)
 check(all(prefix in listing for prefix in ['pixelelated/Saves/','pixelelated/Backups/','pixelelated/Content/']),'independent backend listing shows all three populated tiers')
 save('fresh-roots',dict(directories=paths,pointers=pointers(),generated_archives=generated,cloud=cloud,scope='Actual installed backuptool/settings/content backup and automatic save receive/send, with independent backend ls and byte witnesses. No claim about the boot scheduler.'))

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
  case=language+'-mid-copy-kill-ui-retry-next-shelf';print('START '+case,flush=True)
  reset(language);guest('rm -f /storage/.config/.restore-finish-pending');kill_during_move()
  # Final backup deliberately stops ES. Restore its actual lifecycle before
  # the next language and final running-identity proof; assert cloud stability.
  cloud=hashes();start();check(hashes()==cloud,'ES restart after backup preserves every cloud byte')
  rows.append({'case':case,'status':'PASS','visual_review':'pending actual frames'})
  (out/'results.json').write_text(json.dumps(rows,indent=2)+'\n')

finally:
 after=guest('sha256sum /usr/bin/emulationstation /usr/bin/cloud_scan /usr/bin/cloud_migrate_layout /usr/bin/cloud_setup /usr/bin/cloud_content_restore').stdout
 (out/'installed-after.sha256').write_text(after);check(after==before,'installed product hashes unchanged')
print('PASS actual chooser/recovery/refusal actions; all frames require primary review',flush=True)

import struct
frames=sorted(out.glob('*.png'))
assert frames,'No direct frames retained'
for frame in frames:
 raw=frame.read_bytes();assert raw[:8]==b'\x89PNG\r\n\x1a\n',frame
 assert struct.unpack('>II',raw[16:24])==(1280,800),frame
save('frame-dimensions',{'count':len(frames),'width':1280,'height':800,'visual_review':'pending primary inspection'})

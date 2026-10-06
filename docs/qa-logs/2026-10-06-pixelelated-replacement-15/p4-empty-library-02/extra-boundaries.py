"""Additional installed acceptance for #471; same isolated pair ownership as the frozen runner."""
from pathlib import Path
import argparse,hashlib,importlib.machinery,importlib.util,json,shlex,socket,subprocess,sys
ap=argparse.ArgumentParser();ap.add_argument('--tree',type=Path,required=True);ap.add_argument('--image',type=Path,required=True);ap.add_argument('--build-id',required=True);ap.add_argument('--output',type=Path,required=True);a=ap.parse_args()
source=a.tree/'tools/pixelelated-vm-cloud-boundaries'
loader=importlib.machinery.SourceFileLoader('frozen_boundaries',str(source));spec=importlib.util.spec_from_loader(loader.name,loader);m=importlib.util.module_from_spec(spec);loader.exec_module(m)
Q=m.QA;C=m.CONF;require=m.require;save=m.save
class Extra(m.Proof):
 def sibling_denied(self):
  self.audit_current('')
  self.put('ROCKNIX/Saves/gb/kept.srm',b'kept saves\n');self.put('ROCKNIX/Saves-replaced/gb/older.srm',b'kept history\n')
  self.migrate('--keep',guest='b');before=self.audit_snapshot(),self.pointers('b')
  self.fault('lsf-path',self.remote+'/ROCKNIX/Saves')
  for command in ['/usr/bin/cloud_migrate_layout --state','/usr/bin/cloud_scan --folder','/usr/bin/cloud_migrate_layout --apply']:
   result=self.on('a',command,allowed=None)
   require(result.returncode!=0 and '>>> why YOUR CLOUD STOPPED ANSWERING' in result.stdout,'unreadable sibling was treated as absent')
   self.on('a',f'test -s {Q}/fired')
   require((self.audit_snapshot(),self.pointers('b'))==before,'refusal moved the active earlier shelf')
  self.clear_fault()
  for _ in range(2):
   self.on('a','/usr/bin/cloud_scan --folder');self.on('a','grep -qx STATE=current /storage/.cache/cloud_sync/scan/state')
   require((self.audit_snapshot(),self.pointers('b'))==before,'repeat changed the sibling shelf')
 def record_write(self):
  self.put('ROCKNIX/Saves/gb/A.srm',b'save witness\n');self.put('ROCKNIX/Content/ROMs/gb/A.gb',b'game witness\n')
  before=self.audit_snapshot()
  shim=f'''#!/bin/bash
if [ "${{!#}}" = /storage/.config/cloud-layout-migration.json ]; then echo fired > {Q}/record-write-fired; exit 1; fi
exec /usr/bin/mv "$@"
'''
  self.on('a',f'cat > {Q}/mv; chmod 755 {Q}/mv',data=shim)
  result=self.migrate(allowed=None)
  require(result.returncode==5 and ">>> why YOUR CLOUD SYNC SETTINGS COULDN'T BE SAVED" in result.stdout,'record write refusal lost the real reason')
  self.on('a',f'test -s {Q}/record-write-fired; test ! -e /storage/.config/cloud-layout-migration.json; rm {Q}/mv')
  require(self.audit_snapshot()==before,'initial record failure changed cloud/pointers')
  self.migrate();require((self.data/'pixelelated/Saves/gb/A.srm').read_bytes()==b'save witness\n','record retry lost saves')
  require((self.data/'pixelelated/Content/ROMs/gb/A.gb').read_bytes()==b'game witness\n','record retry lost content')
 def marker_write(self):
  self.put('ROCKNIX/Saves/gb/A.srm',b'kept after failure\n');self.fault('rcat',self.remote+'/pixelelated/.layout')
  result=self.migrate(allowed=None)
  require(result.returncode!=0 and ">>> why SOME FILES DIDN'T FINISH" in result.stdout,'marker write refusal lost the real reason')
  self.on('a',f'test -s {Q}/fired; test -s /storage/.config/cloud-layout-migration.json')
  require((self.data/'pixelelated/Saves/gb/A.srm').read_bytes()==b'kept after failure\n','verified copy lost after marker fault')
  require(not (self.data/'pixelelated/.layout').exists(),'failed marker was published')
  self.clear_fault();self.migrate();require((self.data/'pixelelated/.layout').read_bytes()==b'layout=2\n','retry did not finish marker')
 def old_pointers(self,mode):
  root='/pixelelated' if mode=='--join' else '/ROCKNIX';self.conf(root+'/Saves',root+'/Backups',root+'/Content')
  if mode=='--join':self.put('ROCKNIX/Saves/gb/A.srm')
  elif mode=='--follow':self.put('pixelelated/Saves/gb/A.srm')
  old=subprocess.check_output(['git','-C',str(self.tree),'show','7afa9efcfc0c1ce4b89774b38878fc1b9a9063d2:'+m.SOURCES+'/cloud_migrate_layout'])
  self.on('a',f'cat > {Q}/old-writer; chmod 755 {Q}/old-writer',data=old.decode())
  shim=f'''#!/bin/bash
if [[ "$*" == *"^SETTINGS_REMOTE="* ]]; then echo fired > {Q}/old-writer-fired; exit 1; fi
exec /usr/bin/sed "$@"
'''
  self.on('a',f'cat > {Q}/sed; chmod 755 {Q}/sed',data=shim)
  before=self.audit_snapshot();result=self.on('a',f'{Q}/old-writer '+shlex.quote(mode),allowed=None)
  self.on('a',f'test -s {Q}/old-writer-fired; rm {Q}/sed');require(result.returncode!=0,'old writer boundary did not fail')
  partial=self.pointers();target='/ROCKNIX' if mode=='--join' else '/pixelelated'
  require(partial['SAVES_REMOTE']==target+'/Saves' and partial['SETTINGS_REMOTE']==root+'/Backups','actual predecessor did not leave the expected partial selection')
  require(self.hashes()==before['cloud'],'old pointer-only writer changed cloud')
  # This is the supported explicit folder-selection action, not an inferred intent repair.
  self.on('a','/usr/bin/cloud_setup --set-saves-remote '+shlex.quote(target+'/Saves'))
  require(all(self.pointers()[k]==target+'/'+v for k,v in [('SAVES_REMOTE','Saves'),('SETTINGS_REMOTE','Backups'),('CONTENT_REMOTE','Content')]),'explicit selection did not repair inherited mixed pointers')
  require(self.hashes()==before['cloud'],'explicit recovery changed cloud bytes')
  save(self.logs/(self.case+'-old-writer.json'),{'ref':'7afa9efcfc0c1ce4b89774b38878fc1b9a9063d2','sha256':hashlib.sha256(old).hexdigest(),'partial':partial,'after':self.pointers(),'recovery':'installed cloud_setup --set-saves-remote; corresponding UI proof separate'})
 def local_membership(self,kind):
  self.audit_current('/Mine')
  original='/storage/roms';empty=Q+'/empty-roms'
  original_entries=self.on('a',"find /storage/roms -mindepth 1 -maxdepth 1 | sort").stdout
  self.on('a',f'mkdir {empty}; mount --bind {empty} {original}')
  try:
   require(not self.on('a',"find /storage/roms -mindepth 1 -maxdepth 1").stdout.strip(),'local ROM directory is not empty')
   names=self.on('a','/usr/bin/cloud_content_restore --known-directories').stdout.splitlines();require(names,'supported membership is empty')
   system=next(n for n in reversed(names) if n!='bios')
   if kind=='last-supported':self.put('Mine/ROMs/'+system+'/A.bin',b'known membership\n')
   elif kind=='bios':self.put('Mine/BIOS/qa.bin',b'BIOS membership\n')
   else:(self.data/'Mine/ROMs'/system).mkdir(parents=True)
   before=self.audit_snapshot();out=self.on('a','/usr/bin/cloud_setup --content-location').stdout
   require('STATE=ok' in out,'supported membership missed on empty device: '+kind)
   require(self.audit_snapshot()==before,'membership lookup changed bytes or pointers')
   save(self.logs/(self.case+'-membership.json'),dict(kind=kind,supported_last=system,stdout=out))
  finally:
   self.on('a',f'umount {original}; rmdir {empty}')
   require(self.on('a',"find /storage/roms -mindepth 1 -maxdepth 1 | sort").stdout==original_entries,'original local mount was not restored')
 def closed_endpoint(self):
  self.audit_current();before=self.audit_snapshot()
  # Reserve a local host port without listening, so the guest sees a real refusal.
  with socket.socket() as sock:
   sock.bind(('127.0.0.1',0));port=sock.getsockname()[1]
   self.on('a','python3 -',data=f'''from pathlib import Path
import re
p=Path('/storage/.config/rclone/rclone.conf');s,n=re.subn(r'^url\\s*=.*$', 'url = http://10.0.2.2:{port}/',p.read_text(),flags=re.M);assert n==1;p.write_text(s)
''')
   result=self.on('a','/usr/bin/cloud_scan --folder',allowed=None)
   require(result.returncode!=0 and '>>> why YOUR CLOUD STOPPED ANSWERING' in result.stdout,'closed endpoint not distinguished from missing folder')
   require("COULDN'T FIND YOUR CLOUD FOLDER" not in result.stdout,'closed endpoint mislabeled missing')
   require(self.audit_snapshot()==before,'network refusal changed cloud or pointers')
 def run_cases(self):
  cases = [('PL001-empty-local-'+kind,lambda k=kind:self.local_membership(k)) for kind in ['last-supported','bios','empty-directory']]
  for name,action in cases:
   self.case=name;print('START '+name,flush=True)
   try:
    self.reset();action();self.results.append({'case':name,'status':'PASS'});print('PASS '+name,flush=True)
   except (AssertionError,subprocess.SubprocessError,OSError,StopIteration) as e:
    self.results.append({'case':name,'status':'FAIL','reason':str(e)});print('FAIL '+name+': '+str(e),flush=True)
   save(self.logs/'results.json',self.results)
  self.case='final-custody'
  for key,value in self.original_scripts.items():
   guest,script=key.split('/');require(self.on(guest,'sha256sum /usr/bin/'+script).stdout.split()[0]==value,'installed script changed')
  return 0 if all(row['status']=='PASS' for row in self.results) else 1
proof=Extra(a)
try:proof.start();result=proof.run_cases()
finally:proof.cleanup()
sys.exit(result)

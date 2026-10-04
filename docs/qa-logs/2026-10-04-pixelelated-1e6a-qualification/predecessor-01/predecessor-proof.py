"""RC2-script-created partial states, recovered by exact installed candidate; #391."""
from pathlib import Path
common=Path(__file__).with_name('archive-proof.py').read_text()
exec(compile(common.split('bid=guest(')[0],'<retained QA helpers>','exec'))

owner=Path(__file__).parent
source=Path('/workspace/repos/rocknix.worktrees/m7-pixelelated-replacement05/projects/ROCKNIX/packages/network/rclone/sources/cloud_migrate_layout')
old=owner/'rc2-cloud-migrate-layout'
expected=hashlib.sha256(source.read_bytes()).hexdigest()
check(guest("sed -n 's/^BUILD_ID=//p' /etc/os-release").strip('"')=='1e6a156b5477650e298b6a4dfff996673bf33fb1','exact upgraded candidate BUILD_ID')
check(sha('/usr/bin/cloud_migrate_layout')==expected,'installed migration equals frozen source')
guest('systemctl stop essway; set_setting cloudsaves.startup 0; set_setting cloudsaves.gameexit 0; set_setting global.retroachievements 0')
config=subprocess.check_output(['./tools/cloud-test-backend','rclone-conf'],text=True).rstrip()+'\n'
guest("umask 077\nmkdir -p /storage/.config/rclone\ncat > /storage/.config/rclone/rclone.conf <<'M7_QA_CONFIG'\n"+config+'M7_QA_CONFIG\n',record=False)
guest('test ! -e /tmp/m7-predecessor; test ! -e /storage/.config/profile.d/999-m7-predecessor-qa.sh; mkdir -p /tmp/m7-predecessor /storage/.config/profile.d')
scp=['scp','-q','-i',a.key,'-P',str(a.port),'-o','StrictHostKeyChecking=no','-o','UserKnownHostsFile=/dev/null','-o','LogLevel=ERROR']
subprocess.run(scp+[str(old),'root@127.0.0.1:/tmp/m7-predecessor/rc2-migrate'],check=True)
check(sha('/tmp/m7-predecessor/rc2-migrate')==hashlib.sha256(old.read_bytes()).hexdigest(),'exact RC2 migration script transferred without substitutions')
shim='''#!/bin/sh
if [ -f /tmp/m7-predecessor/fault ] && [ "$1 ${2%/}" = "$(cat /tmp/m7-predecessor/fault)" ]; then
 printf '%s\\n' "$1 $2" >> /tmp/m7-predecessor/fired
 echo 'injected QA provider operation failure' >&2
 exit 5
fi
exec /usr/bin/rclone "$@"
'''
guest("cat > /tmp/m7-predecessor/rclone <<'M7_SHIM'\n"+shim+"M7_SHIM\nchmod 755 /tmp/m7-predecessor/rclone /tmp/m7-predecessor/rc2-migrate\nprintf '%s\\n' 'export PATH=/tmp/m7-predecessor:$PATH' > /storage/.config/profile.d/999-m7-predecessor-qa.sh")
check(guest('command -v rclone')=='/tmp/m7-predecessor/rclone','real profile selects provider-operation shim')
remote=guest('/usr/bin/rclone listremotes | head -1')
assert re.fullmatch(r'[A-Za-z0-9_-]+:',remote),remote
payloads={'Backups/QA/settings.tar.gz':b'settings bytes\n','Saves/gb/A.srm':b'save bytes\n','Content/ROMs/gb/A.gb':b'game bytes\n'}
initial={'GAMES/backup/QA/settings.tar.gz':payloads['Backups/QA/settings.tar.gz'],'GAMES/gb/A.srm':payloads['Saves/gb/A.srm'],'GAMES/Content/ROMs/gb/A.gb':payloads['Content/ROMs/gb/A.gb']}
def cloud():
 return {str(p.relative_to(data)):hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(data.rglob('*')) if p.is_file()}
def execute(command,tag):
 text=guest('set +e\n'+command+' > /tmp/m7-predecessor/last.log 2>&1\nr=$?\ncat /tmp/m7-predecessor/last.log\nprintf "\\nM7_COMMAND_RC=%s\\n" "$r"\nexit 0')
 match=re.search(r'\nM7_COMMAND_RC=(\d+)\s*$',text);assert match,text
 (out/(tag+'.log')).write_text(text+'\n');(out/(tag+'.rc')).write_text(match[1]+'\n')
 return int(match[1])
def fault(op,path):
 guest("rm -f /tmp/m7-predecessor/fired; printf '%s\\n' "+q(op+' '+remote+path)+' > /tmp/m7-predecessor/fault')
def retain(tag,rc):
 record={'rc':rc,'pointers':pointers(),'cloud_sha256':cloud(),'old_script_sha256':hashlib.sha256(old.read_bytes()).hexdigest(),'installed_script_sha256':sha('/usr/bin/cloud_migrate_layout')}
 (out/(tag+'.json')).write_text(json.dumps(record,indent=2)+'\n');return record
try:
 for stage in ['backups','saves','content','complete','content-reinterrupted']:
  tag='RC2-'+stage
  subprocess.run(['./tools/cloud-test-backend','reset'],check=True,stdout=subprocess.DEVNULL)
  guest('rm -f /tmp/m7-predecessor/fault /tmp/m7-predecessor/fired /storage/.config/cloud-layout-migration.json; rm -rf /storage/.cache/cloud_sync/scan')
  conf('/GAMES','/GAMES/backup','/GAMES/Content')
  for name,content in initial.items():
   p=data/name;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(content)
  start=retain(tag+'-initial',None)
  if stage!='complete':fault('copy',{'backups':'/GAMES/backup','saves':'/GAMES','content':'/GAMES/Content','content-reinterrupted':'/GAMES/Content'}[stage])
  rc=execute('/tmp/m7-predecessor/rc2-migrate --apply',tag+'-old')
  if stage!='complete':
   check(rc!=0,tag+' predecessor returns actual operation failure')
   check(bool(guest('cat /tmp/m7-predecessor/fired')),tag+' fault is reached')
  else:check(rc==0,tag+' predecessor completes old layout')
  check(guest('test ! -e /storage/.config/cloud-layout-migration.json && echo absent')=='absent',tag+' predecessor has no new-format recovery record')
  inherited=retain(tag+'-inherited',rc)
  if stage in ['content','content-reinterrupted']:
   check(inherited['pointers']['SAVES_REMOTE']=='/ROCKNIX/Saves' and inherited['pointers']['SETTINGS_REMOTE']=='/ROCKNIX/Backups' and inherited['pointers']['CONTENT_REMOTE']=='/GAMES/Content',tag+' actual predecessor writes the reported split pointers')
  check(all(hashlib.sha256(b).hexdigest() in inherited['cloud_sha256'].values() for b in payloads.values()),tag+' every inherited payload survives')
  guest('rm -f /tmp/m7-predecessor/fault /tmp/m7-predecessor/fired')
  if stage=='content-reinterrupted':
   fault('rcat','/pixelelated/.layout')
   rc=execute('/usr/bin/cloud_migrate_layout --apply',tag+'-new-fault')
   check(rc!=0 and bool(guest('cat /tmp/m7-predecessor/fired')),tag+' installed recovery reaches and returns marker failure')
   check(guest('test -s /storage/.config/cloud-layout-migration.json && echo pending')=='pending' and not (data/'pixelelated/.layout').exists(),tag+' failed publication retains retry record without completion marker')
   retain(tag+'-new-fault',rc)
   check(execute('/usr/bin/cloud_migrate_layout --needs-step',tag+'-needs-step')==0,tag+' boot offers retry')
   scan=execute('/usr/bin/cloud_scan --folder',tag+'-scan')
   check(scan==0 and 'STATE=migration-pending' in guest('cat /storage/.cache/cloud_sync/scan/state'),tag+' transfer scan offers retry')
   guest('rm -f /tmp/m7-predecessor/fault /tmp/m7-predecessor/fired')
  rc=execute('/usr/bin/cloud_migrate_layout --apply',tag+'-retry')
  check(rc in (0,3),tag+' installed candidate recovery succeeds')
  final=retain(tag+'-recovered',rc)
  check(all((data/'pixelelated'/n).is_file() and (data/'pixelelated'/n).read_bytes()==b for n,b in payloads.items()),tag+' all candidate payload bytes match')
  check(not any(p.is_file() for root in ['GAMES','ROCKNIX'] for p in (data/root).rglob('*')),tag+' no owned payload remains under earlier folders')
  check((data/'pixelelated/.layout').read_bytes()==b'layout=2\n',tag+' exact completion marker published')
  check(final['pointers']=={'SAVES_REMOTE':'/pixelelated/Saves','SETTINGS_REMOTE':'/pixelelated/Backups','CONTENT_REMOTE':'/pixelelated/Content','LAYOUT_KEEP':''},tag+' every pointer follows recovered bytes')
  check(guest('test ! -e /storage/.config/cloud-layout-migration.json && echo absent')=='absent',tag+' completed local record cleared')
  rc=execute('/usr/bin/cloud_migrate_layout --apply',tag+'-repeat')
  check(rc in (0,3) and cloud()==final['cloud_sha256'] and pointers()==final['pointers'],tag+' repeated migration preserves exact cloud bytes and pointers')
finally:
 guest('rm -f /storage/.config/profile.d/999-m7-predecessor-qa.sh; rm -rf /tmp/m7-predecessor')
 check(sha('/usr/bin/cloud_migrate_layout')==expected,'installed candidate migration remains unchanged')
print('PASS five RC2-script-created states on actual-upgrade candidate COW',flush=True)

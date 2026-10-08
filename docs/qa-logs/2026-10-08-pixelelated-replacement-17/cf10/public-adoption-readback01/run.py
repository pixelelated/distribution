from pathlib import Path
import subprocess,json,hashlib,time,shlex
O=Path(__file__).parent;B=O.parent;R=Path('/workspace/repos/rocknix.worktrees/m7-pixelelated-replacement17');G=B/'guest03';data=B/'backend/data'
ssh=['ssh','-i',str(G/'qa-key'),'-p','10230','-o','LogLevel=ERROR','-o','StrictHostKeyChecking=no','-o','UserKnownHostsFile=/dev/null','-o','BatchMode=yes','-o','ConnectTimeout=5','root@127.0.0.1']
scp=['scp','-q','-i',str(G/'qa-key'),'-P','10230','-o','LogLevel=ERROR','-o','StrictHostKeyChecking=no','-o','UserKnownHostsFile=/dev/null']
def guest(code,d,n,timeout=50):
 q=subprocess.run(ssh+['bash -s'],input=code,capture_output=True,text=True,timeout=timeout);(d/(n+'.stdout')).write_text(q.stdout);(d/(n+'.stderr')).write_text(q.stderr);(d/(n+'.rc')).write_text(str(q.returncode)+'\n');q.check_returncode();return q.stdout
def put(p,dst):subprocess.run(scp+[str(p),'root@127.0.0.1:'+dst],check=True)
def snapshot():return {str(p.relative_to(data)):hashlib.sha256(p.read_bytes()).hexdigest() if p.is_file() else 'directory' for p in sorted(data.rglob('*'))}
def save(d,n,v):(d/(n+'.json')).write_text(json.dumps(v,indent=2)+'\n')
previous=B/'public-adoption01'
cloud=json.loads((previous/'cloud-before.json').read_text())
assert snapshot()==cloud
witness='set -e\ncat /proc/sys/kernel/random/boot_id\nsha256sum /storage/.config/rclone/rclone.conf /storage/roms/nes/CF10.srm /storage/roms/savestates/nes/CF10.state /usr/bin/emulationstation /usr/bin/cloud_setup /usr/bin/cloud_sync_helper /usr/share/post-update /usr/share/locale/fr/LC_MESSAGES/emulationstation2.mo\n. /etc/profile >/dev/null 2>&1\nprintf "startup="; get_setting cloudsync.startup\nprintf "gameexit="; get_setting cloudsync.gameexit\n'
before=(previous/'before.stdout').read_text();rows=[]
for name,content in [('public-default',None)]:
 d=O/name;d.mkdir();seed=(previous/name/'seed.conf').read_bytes();action='readonly consumption after original full post-update rc1 (#526)'
 assert guest(witness,d,'before-consumption')==before
 context=json.loads(guest('/usr/bin/cloud_setup --validation-context',d,'context'))
 expected='/pixelelated/Content' if content is None else content
 assert context['paths']['saves']=='/GAMES' and context['paths']['settings']=='/GAMES/backup' and context['paths']['content']==expected,context
 assert guest(witness,d,'after-conversion')==before,'payload, credentials, choices or installed bytes changed'
 assert snapshot()==cloud,'conversion changed provider data'
 config=guest('cat /storage/.config/cloud_sync.conf',d,'converted-config');assert 'BACKUPMETHOD="copy"' in config
 result=json.loads(guest('/usr/bin/cloud_setup --validate-folders saves,settings,roms,bios,media cf10-'+name,d,'validation'))
 assert result['complete'] and len(result['categories'])==5,result
 assert result['categories'][0]['state']=='present',result
 assert snapshot()==cloud and guest(witness,d,'after-check')==before
 confhash=hashlib.sha256(config.encode()).hexdigest()
 guest('/usr/bin/cloud_sync_helper /var/log/cloud_sync.log',d,'repeat-helper')
 assert guest('sha256sum /storage/.config/cloud_sync.conf',d,'repeat-confhash').split()[0]==confhash,'repeated helper changed converted config'
 assert snapshot()==cloud and guest(witness,d,'after-repeat')==before
 row={'case':name,'seed_sha256':hashlib.sha256(seed).hexdigest(),'action':action,'context':context,'validation':result,'cloud_local_payload_credentials_and_auto_choices_preserved':True,'repeat_idempotent':True};save(d,'result',row);rows.append(row)
 print('PASS',name,'installed conversion, read-only checks and preservation',flush=True)
save(O,'result',{'passed':True,'cases':rows,'accepted_prior_cases':[json.loads((previous/n/'result.json').read_text()) for n in ['explicit-root','custom-library']],'source_overlays':False,'scope':'public configuration/rules adoption on actual installed image; default cloud conversion completed before unrelated full-hook melonDS rc1 (#526); this check is cloud-specific acceptance only; not upstream GENERIC_X64 kernel/boot proof','retained_guest_state':'public-default /GAMES + /GAMES/backup; startup0/gameexit1; ES stopped for subsequent UI proof'})
print('PASS public-default cloud-specific preservation after original hook failure; complete post-update remains blocked by #526',flush=True)

from pathlib import Path
import subprocess,json,hashlib,time,shlex
O=Path(__file__).parent;B=O.parent;R=Path('/workspace/repos/rocknix.worktrees/m7-pixelelated-replacement18');G=B/'guest01';data=B/'backend/data'
ssh=['ssh','-i',str(G/'qa-key'),'-p','10230','-o','LogLevel=ERROR','-o','StrictHostKeyChecking=no','-o','UserKnownHostsFile=/dev/null','-o','BatchMode=yes','-o','ConnectTimeout=5','root@127.0.0.1']
scp=['scp','-q','-i',str(G/'qa-key'),'-P','10230','-o','LogLevel=ERROR','-o','StrictHostKeyChecking=no','-o','UserKnownHostsFile=/dev/null']
def guest(code,d,n,timeout=50):
 q=subprocess.run(ssh+['bash -s'],input=code,capture_output=True,text=True,timeout=timeout);(d/(n+'.stdout')).write_text(q.stdout);(d/(n+'.stderr')).write_text(q.stderr);(d/(n+'.rc')).write_text(str(q.returncode)+'\n');q.check_returncode();return q.stdout
def put(p,dst):subprocess.run(scp+[str(p),'root@127.0.0.1:'+dst],check=True)
def snapshot():return {str(p.relative_to(data)):hashlib.sha256(p.read_bytes()).hexdigest() if p.is_file() else 'directory' for p in sorted(data.rglob('*'))}
def save(d,n,v):(d/(n+'.json')).write_text(json.dumps(v,indent=2)+'\n')
ref='c445081a59518f37d9776e5412dd7b14910696f7';subtree='projects/ROCKNIX/packages/network/rclone/sources/'
public={n:subprocess.check_output(['git','-C',str(R),'show',ref+':'+subtree+n]) for n in ['cloud_sync.conf','cloud_sync-rules.txt']}
for n,v in public.items():(O/('public-'+n)).write_bytes(v)
save(O,'public-seed',{'ref':ref,'release':'20261001','files':{n:hashlib.sha256(v).hexdigest() for n,v in public.items()},'scope':'exact public cloud config/rules on fork-only GENERIC_X64; not a public GENERIC_X64 image'})
guest('set -e\nsystemctl stop essway.service\nmkdir -p /storage/cf10-public/clean /storage/roms/nes /storage/roms/savestates/nes\ncp /storage/.config/cloud_sync.conf /storage/.config/cloud_sync-rules.txt /storage/cf10-public/clean/\nprintf "synthetic CF10 local save\\n" > /storage/roms/nes/CF10.srm\nprintf "synthetic CF10 local state\\n" > /storage/roms/savestates/nes/CF10.state\n. /etc/profile >/dev/null 2>&1\nset_setting cloudsync.startup 0\nset_setting cloudsync.gameexit 1\n',O,'setup')
for name,text in {'GAMES/nes/CF10.srm':'synthetic public cloud save\n','GAMES/backup/CF10-settings.zip':'synthetic metadata-only backup fixture\n','Separate/Library/ROMs/nes/CF10.nes':'synthetic ROM metadata fixture\n','Separate/Library/BIOS/CF10.bin':'synthetic BIOS metadata fixture\n','ROMs/nes/CF10.nes':'explicit-root metadata fixture\n','BIOS/CF10.bin':'explicit-root BIOS fixture\n'}.items():
 p=data/name;assert not p.exists();p.parent.mkdir(parents=True,exist_ok=True);p.write_text(text)
cloud=snapshot();save(O,'cloud-before',cloud)
witness='set -e\ncat /proc/sys/kernel/random/boot_id\nsha256sum /storage/.config/rclone/rclone.conf /storage/roms/nes/CF10.srm /storage/roms/savestates/nes/CF10.state /usr/bin/emulationstation /usr/bin/cloud_setup /usr/bin/cloud_sync_helper /usr/share/post-update /usr/share/locale/fr/LC_MESSAGES/emulationstation2.mo\n. /etc/profile >/dev/null 2>&1\nprintf "startup="; get_setting cloudsync.startup\nprintf "gameexit="; get_setting cloudsync.gameexit\n'
before=guest(witness,O,'before');rows=[]
markers=['.cloud_sync-rules-user-first-applied','.cloud_sync-copy-default-applied','.cloud_sync-net-opts-retries-applied','.cloud_sync-sync-net-opts-five-applied']
for name,content in [('explicit-root',''),('custom-library','Separate/Library'),('public-default',None)]:
 d=O/name;d.mkdir();print('START',name,flush=True)
 seed=public['cloud_sync.conf']+((f'\nCONTENT_REMOTE="{content}"\n').encode() if content is not None else b'');p=d/'seed.conf';p.write_bytes(seed)
 guest('set -e\nmkdir -p /storage/cf10-public/'+name+'\n'+''.join('if [ -f /storage/.config/'+m+' ]; then cp /storage/.config/'+m+' /storage/cf10-public/'+name+'/; rm /storage/.config/'+m+'; fi\n' for m in markers),d,'clear-fork-markers')
 put(p,'/storage/.config/cloud_sync.conf');put(O/'public-cloud_sync-rules.txt','/storage/.config/cloud_sync-rules.txt')
 sums=guest('sha256sum /storage/.config/cloud_sync.conf /storage/.config/cloud_sync-rules.txt',d,'seed-readback').splitlines()
 assert sums[0].split()[0]==hashlib.sha256(seed).hexdigest() and sums[1].split()[0]==hashlib.sha256(public['cloud_sync-rules.txt']).hexdigest()
 assert guest(witness,d,'before-conversion')==before
 action='/usr/share/post-update' if content is None else '/usr/bin/cloud_sync_helper /var/log/cloud_sync.log'
 guest('set -e\ntimeout 120 '+action+'\n',d,'installed-conversion',150)
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
save(O,'result',{'passed':True,'cases':rows,'source_overlays':False,'scope':'public configuration/rules adoption on actual installed image; final default case uses complete shipped post-update entrypoint; not upstream GENERIC_X64 kernel/boot proof','retained_guest_state':'public-default /GAMES + /GAMES/backup; startup0/gameexit1; ES stopped for subsequent UI proof'})
print('PASS three actual installed public-configuration adoption cases',flush=True)

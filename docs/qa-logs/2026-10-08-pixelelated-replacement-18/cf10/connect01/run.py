from pathlib import Path
import json,hashlib,subprocess,os,shlex,datetime
O=Path(__file__).parent;B=O.parent;R=Path('/workspace/repos/rocknix.worktrees/m7-pixelelated-replacement18');G=B/'guest01'
env=os.environ.copy();env.update(CLOUD_QA_BACKEND='webdav',CLOUD_QA_STATE=str(B/'backend'),CLOUD_QA_PORT='19085',CLOUD_QA_DEAD_PORT='19086',CLOUD_QA_DEFAULTS=str(R/'projects/ROCKNIX/packages/network/rclone/sources/cloud_sync.conf.defaults'))
(O/'bin').mkdir();(O/'bin/rclone').symlink_to(R/'build.pixelelated-GENERIC_X64.x86_64/image/system/usr/bin/rclone');env['PATH']=str(O/'bin')+':'+env['PATH']
ssh=['ssh','-i',str(G/'qa-key'),'-p','10230','-o','LogLevel=ERROR','-o','StrictHostKeyChecking=no','-o','UserKnownHostsFile=/dev/null','-o','BatchMode=yes','-o','ConnectTimeout=5','root@127.0.0.1']
scp=['scp','-q','-i',str(G/'qa-key'),'-P','10230','-o','LogLevel=ERROR','-o','StrictHostKeyChecking=no','-o','UserKnownHostsFile=/dev/null']
def guest(command,label):
 q=subprocess.run(ssh+[command],capture_output=True,text=True,timeout=45);(O/(label+'.stdout')).write_text(q.stdout);(O/(label+'.stderr')).write_text(q.stderr);(O/(label+'.rc')).write_text(str(q.returncode)+'\n');q.check_returncode();return q.stdout

def backend(command):
 q=subprocess.run([str(R/'tools/cloud-test-backend'),command],env=env,capture_output=True,text=True,timeout=30)
 (O/('backend-'+command+'.stdout')).write_text(q.stdout);(O/('backend-'+command+'.stderr')).write_text(q.stderr);q.check_returncode();return q.stdout.strip()

def snapshot():
 return {str(p.relative_to(data)):({'kind':'file','sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'bytes':p.stat().st_size} if p.is_file() else {'kind':'directory'}) for p in sorted(data.rglob('*'))}

def save(name,value):(O/(name+'.json')).write_text(json.dumps(value,indent=2)+'\n')
boot=guest('cat /proc/sys/kernel/random/boot_id','boot-before').strip();assert len(boot)==36
versions=subprocess.check_output([str(O/'bin/rclone'),'version'],text=True);(O/'host-rclone-version.txt').write_text(versions);assert 'rclone v1.75.1' in versions
# No previous config or cloud/provider is reused. The only account is local QA.
assert not (B/'backend').exists()
backend('up');data=Path(backend('path'));assert data.is_dir() and B in data.parents
(data/'Unrelated').mkdir();(data/'Unrelated/keep.txt').write_text('CF10 synthetic unrelated cloud data\n');before=snapshot();save('cloud-before-link',before)
conf=backend('rclone-conf');(O/'synthetic-rclone.conf').write_text(conf+'\n');(O/'synthetic-rclone.conf').chmod(0o600)
guest('test ! -s /storage/.config/rclone/rclone.conf; sha256sum /storage/.config/cloud_sync.conf; mkdir -p /storage/.config/rclone','fresh-precondition')
subprocess.run(scp+[str(O/'synthetic-rclone.conf'),'root@127.0.0.1:/storage/.config/rclone/rclone.conf'],check=True)
guest('chmod 600 /storage/.config/rclone/rclone.conf; timeout 35 /usr/bin/cloud_setup --check','connection-check')
context=json.loads(guest('/usr/bin/cloud_setup --validation-context','context'))
assert {k:context['paths'][k] for k in ['saves','settings','content']}=={'saves':'/pixelelated/Saves','settings':'/pixelelated/Backups','content':'/pixelelated/Content'},context
credentials=guest('sha256sum /storage/.config/rclone/rclone.conf','credential-hash').split()[0]
paths_before=guest('sha256sum /storage/.config/cloud_sync.conf','paths-before').split()[0]
assert snapshot()==before,'link changed cloud files'
result=json.loads(guest('/usr/bin/cloud_setup --validate-folders saves,settings,roms,bios,media cf10-clean','check-all'))
assert result['complete'] and len(result['categories'])==5,result
assert all(x['state']=='missing' for x in result['categories']),result
assert snapshot()==before,'read-only validation changed cloud files'
assert guest('sha256sum /storage/.config/cloud_sync.conf','paths-after').split()[0]==paths_before
assert guest('sha256sum /storage/.config/rclone/rclone.conf','credentials-after').split()[0]==credentials
assert guest('cat /proc/sys/kernel/random/boot_id','boot-after').strip()==boot
save('cloud-after-check',snapshot());save('result',{'passed':True,'proof':'actual installed clean defaults, synthetic rclone link/check and five-category missing result write nothing to cloud','context':context,'validation':result,'credential_sha256':credentials,'sync_config_sha256':paths_before,'cloud_unchanged':True,'boot_id':boot,'backend_retained_for_immediate_ui_proof':str(B/'backend'),'port':19085,'source_overlays':False})
print('PASS fresh linking and five-category checking preserve default paths, credentials and all cloud bytes; local backend retained for immediate UI creation proof',flush=True)

from pathlib import Path
import subprocess,json,hashlib,time,struct
O=Path(__file__).parent;B=O.parent;R=Path('/workspace/repos/rocknix.worktrees/m7-pixelelated-replacement17');G=B/'guest03';data=B/'backend/data'
ssh=['ssh','-i',str(G/'qa-key'),'-p','10230','-o','LogLevel=ERROR','-o','StrictHostKeyChecking=no','-o','UserKnownHostsFile=/dev/null','-o','BatchMode=yes','-o','ConnectTimeout=5','root@127.0.0.1']
def guest(code,d,n):
 q=subprocess.run(ssh+['bash -s'],input=code,capture_output=True,text=True,timeout=45);(d/(n+'.stdout')).write_text(q.stdout);(d/(n+'.stderr')).write_text(q.stderr);q.check_returncode();return q.stdout
def snapshot():return {str(p.relative_to(data)):hashlib.sha256(p.read_bytes()).hexdigest() if p.is_file() else 'directory' for p in sorted(data.rglob('*'))}
def save(d,n,v):(d/(n+'.json')).write_text(json.dumps(v,indent=2)+'\n')
witness='set -e\ncat /proc/sys/kernel/random/boot_id\nsha256sum /storage/.config/cloud_sync.conf /storage/.config/rclone/rclone.conf /usr/bin/emulationstation /usr/bin/cloud_setup /usr/share/locale/fr/LC_MESSAGES/emulationstation2.mo\n'
before=guest(witness,O,'before');cloud=snapshot();save(O,'cloud-before',cloud)
context=json.loads(guest('/usr/bin/cloud_setup --validation-context',O,'context'))
assert context['paths']['saves']=='/pixelelated/Saves',context
entry='settle\nkey ret\nwait-for-change 12 0\nkey x\nwait-for-change 12 0\nkey up x3\nkey x\nwait-for-change 12 0\nkey up x3\nkey x\nwait-for-change 12 0\nsettle\nshot category-selection\nkey down x5\nkey x\nwait 4\nsettle\nshot check-result\n'
rows=[]
for lang,res in [('en_US','640x480'),('fr_FR','640x480'),('en_US','1280x800'),('fr_FR','1280x800')]:
 d=O/(lang+'-'+res);d.mkdir();print('START',d.name,flush=True)
 mode=('--custom ' if res=='1280x800' else '')+res+'@60Hz'
 setup=f'''set -e
systemctl stop essway.service
. /etc/profile >/dev/null 2>&1
set_setting system.language {lang}
cat > /storage/.config/emulationstation/es_settings.cfg <<'XML'
<?xml version="1.0"?>
<config>
<bool name="UseOSK" value="false" />
<int name="ScreenSaverTime" value="0" />
<string name="Language" value="{lang}" />
</config>
XML
swaymsg -s /run/0-runtime-dir/sway-ipc.0.sock "output Virtual-1 mode {mode}"
systemctl start essway.service
'''
 (d/'setup.sh').write_text(setup);guest(setup,d,'setup');time.sleep(3)
 (d/'entry.steps').write_text(entry)
 q=subprocess.run(['python3',str(R/'tools/vm-visual-qa'),'--monitor','/tmp/pix508-cf10-17-mon.sock','run',str(d/'entry.steps'),'--outdir',str(d/'frames')],capture_output=True,text=True,timeout=150);(d/'walk.log').write_text(q.stdout+q.stderr);q.check_returncode()
 outputs=json.loads(guest('swaymsg -s /run/0-runtime-dir/sway-ipc.0.sock -t get_outputs',d,'outputs'));cur=next(x['current_mode'] for x in outputs if x['name']=='Virtual-1');assert f"{cur['width']}x{cur['height']}"==res
 assert guest(witness,d,'after')==before,'cloud config, credential or installed bytes changed'
 assert snapshot()==cloud,'cloud data changed during checks/instructions'
 for p in sorted((d/'frames').glob('*.png')):
  dim=struct.unpack('>II',p.read_bytes()[16:24]);assert f'{dim[0]}x{dim[1]}'==res
  rows.append({'frame':str(p.relative_to(O)),'locale':lang,'resolution':res,'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'review':'pending','flow':'CF10','source_overlays':False})
 print('PASS data preservation and dimensions',d.name,flush=True)
save(O,'result',{'passed':True,'kind':'actual clean-default installed-image UI','frames':rows,'cloud_and_configuration_unchanged':True,'frame_review':'pending'})
print('PASS 4 locale/panel combinations; 8 actual-image frames await direct review',flush=True)

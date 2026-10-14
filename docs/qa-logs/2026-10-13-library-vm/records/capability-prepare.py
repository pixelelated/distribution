from pathlib import Path
import json,hashlib,xml.etree.ElementTree as ET,shlex,subprocess,time,re
from ui import out,remote
r=Path(__file__).parent;repo=Path('/workspace/repos/rocknix.worktrees/m7-player-setup');dest='/storage/qa575'
assert json.loads((r/'steam-owner/launcher-result.json').read_text())['runner_returncode']==1
remote('systemctl stop essway.service; mkdir -p '+dest,capture_output=True)
original=out('cat /usr/config/emulationstation/es_systems.cfg');root=ET.fromstring(original)
assert not any(s.findtext('name')=='gamecube' for s in root.findall('system'))
values={}
for line in (repo/'config/emulators/gamecube.conf').read_text().splitlines():
 if '=' in line:
  k,v=line.split('=',1);values[k]=shlex.split(v)[0]
gc=ET.SubElement(root,'system')
for field,key in [('name','NAME'),('fullname','FULLNAME'),('manufacturer','MANUFACTURER'),('release','RELEASE'),('hardware','HARDWARE'),('path','PATH'),('extension','EXTENSION'),('platform','PLATFORM'),('theme','THEME')]:ET.SubElement(gc,field).text=values['SYSTEM_'+key]
ET.SubElement(gc,'command').text='/usr/bin/runemu.sh %ROM% -P%SYSTEM% --core=%CORE% --emulator=%EMULATOR% --controllers="%CONTROLLERSCONFIG%"'
em=ET.SubElement(gc,'emulators');d=ET.SubElement(em,'emulator',name='dolphin');c=ET.SubElement(d,'cores');ET.SubElement(c,'core',default='true').text='dolphin-sa-gc';ET.SubElement(c,'core').text='dolphin-qt-gc';a=ET.SubElement(em,'emulator',name='retroarch');ET.SubElement(ET.SubElement(a,'cores'),'core').text='dolphin'
new=ET.tostring(root,encoding='utf-8');remote('cat > '+dest+'/es_systems.cfg',input=new,capture_output=True)
remote('cp /storage/.config/emulationstation/es_settings.cfg '+dest+'/original-settings.cfg; mount --bind '+dest+'/es_systems.cfg /usr/config/emulationstation/es_systems.cfg; mount --make-private /usr/config/emulationstation/es_systems.cfg',capture_output=True)
script='#!/bin/sh\nprintf "%s\\n" unexpected-launch >> /storage/qa575/launch-events\nexit 250\n'
remote('cat > '+dest+'/no-launch',input=script,text=True,capture_output=True);remote('chmod 755 '+dest+'/no-launch; : > '+dest+'/launch-events; mount --bind '+dest+'/no-launch /usr/bin/runemu.sh; mount --make-private /usr/bin/runemu.sh',capture_output=True)
for system,extension in [('gamecube','.dol'),('dreamcast','.cdi')]:
 existing=out('find /storage/roms/'+system+' -type f 2>/dev/null || true').splitlines();assert not existing,existing
 remote('mkdir -p /storage/roms/'+system,capture_output=True)
 remote('cat > /storage/roms/'+system+'/pixelelated-capability'+extension,input=b'Synthetic UI fixture only. Never launch.\n',capture_output=True)
receipt={'rc':0,'scope':'VM image does not ship GameCube; add only canonical SM8550/AMD64 declaration for UI proof; no native-emulator support claim','inputs':{p:hashlib.sha256((repo/p).read_bytes()).hexdigest() for p in ['config/emulators/gamecube.conf','projects/ROCKNIX/packages/virtual/emulators/package.mk']},'original_systems_sha256':hashlib.sha256(original.encode()).hexdigest(),'staged_systems_sha256':hashlib.sha256(new).hexdigest(),'installed':out('sha256sum /usr/config/emulationstation/es_systems.cfg /usr/config/emulationstation/es_features.cfg /usr/config/emulationstation/es_savestates.cfg /usr/bin/runemu.sh'),'launch_events':out('cat '+dest+'/launch-events')}
(r/'records/capability-preparation.json').write_text(json.dumps(receipt,indent=2)+'\n');print('Synthetic capability inputs prepared; engine launches blocked and counted')

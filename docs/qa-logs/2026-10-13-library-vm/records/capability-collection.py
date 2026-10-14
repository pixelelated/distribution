from pathlib import Path
import json,subprocess,time,sys,re,xml.etree.ElementTree as ET,shlex,traceback
from ui import out,remote,shot
r=Path(__file__).parent;name,lang,mode=sys.argv[1:];case=r/name;case.mkdir();result={'rc':1,'started':time.time(),'lang':lang,'mode':mode};dest='/storage/qa575';repo=Path('/workspace/repos/rocknix.worktrees/m7-player-setup')
def walk(keys,label):
 steps=case/(label+'.steps');steps.write_text('\n'.join(['wake','settle']+sum((['key '+k,'wait-for-change','settle'] for k in keys),[])+['shot '+label])+'\n')
 p=subprocess.run([str(repo/'tools/vm-visual-qa'),'--monitor',str(r/'vm/monitor.sock'),'run',str(steps),'--outdir',str(case/label)],timeout=90);assert p.returncode==0
try:
 remote('systemctl stop essway.service',capture_output=True)
 old=out('cat /storage/roms/gamecube/gamelist.xml 2>/dev/null || true');(case/'prior-synthetic-gamelist.xml').write_text(old)
 gamelist=b'<gameList><game><path>./pixelelated-capability.dol</path><name>pixelelated capability</name><favorite>true</favorite></game></gameList>'
 remote('cat > /storage/roms/gamecube/gamelist.xml',input=gamelist,capture_output=True)

 raw=out('cat '+dest+'/original-settings.cfg');raw=re.sub(r'^\s*<\?xml[^?]*\?>','',raw,count=1);wrap=ET.fromstring('<fixture>'+raw+'</fixture>');root=list(wrap)[0] if len(wrap)==1 and list(wrap)[0].tag=='config' else wrap;root.tag='config'
 system='gamecube' if mode.startswith('gc') else 'dreamcast'
 for node in list(root):
  if node.get('name') in ['CheevosCheckIndexesAtStart','NetPlayCheckIndexesAtStart','StartupSystem','StartupOnGameList','CollectionSystemsAuto','CheckBiosesAtLaunch']:root.remove(node)
 for key,value in [('CheevosCheckIndexesAtStart','false'),('NetPlayCheckIndexesAtStart','false'),('CheckBiosesAtLaunch','false'),('StartupOnGameList','true')]:ET.SubElement(root,'bool',name=key,value=value)
 ET.SubElement(root,'string',name='StartupSystem',value='favorites');ET.SubElement(root,'string',name='CollectionSystemsAuto',value='favorites,recent')
 remote('cat > /storage/.config/emulationstation/es_settings.cfg',input=ET.tostring(root),capture_output=True)
 settings={'system.language':lang,'global.autosave':'1','gamecube.autosave':'0','dreamcast.autosave':'0','gamecube.emulator':'','gamecube.core':'','dreamcast.emulator':'flycast','dreamcast.core':'flycast-sa','gamecube["pixelelated-capability.dol"].emulator':'','gamecube["pixelelated-capability.dol"].core':'','dreamcast["pixelelated-capability.cdi"].emulator':'','dreamcast["pixelelated-capability.cdi"].core':''}
 if mode=='gc-retro-override':settings.update({'gamecube["pixelelated-capability.dol"].emulator':'retroarch','gamecube["pixelelated-capability.dol"].core':'dolphin'})
 if mode=='dc-standalone-override':settings.update({'dreamcast.emulator':'retroarch','dreamcast.core':'flycast','dreamcast["pixelelated-capability.cdi"].emulator':'flycast','dreamcast["pixelelated-capability.cdi"].core':'flycast-sa'})
 if mode=='dc-retro-override':settings.update({'dreamcast["pixelelated-capability.cdi"].emulator':'retroarch','dreamcast["pixelelated-capability.cdi"].core':'flycast'})
 cmd='. /etc/profile >/dev/null 2>&1; '+'; '.join('set_setting '+shlex.quote(k)+' '+shlex.quote(v) for k,v in settings.items())+'; systemctl start essway.service';remote(cmd,capture_output=True)
 end=time.monotonic()+45
 while time.monotonic()<end:
  if out('curl -fsS http://127.0.0.1:1234/isIdle 2>/dev/null || true').replace(' ','').strip()=='[true]':break
  time.sleep(.4)
 else:raise RuntimeError('frontend readiness')
 result['before']=out('cat /proc/sys/kernel/random/boot_id; pidof emulationstation; sha256sum /proc/$(pidof emulationstation)/exe').strip();assert json.loads((r/'records/candidate.json').read_text())['sha256'] in result['before']
 result['collection']=out('curl -fsS http://127.0.0.1:1234/systems/favorites/games');assert 'pixelelated-capability.dol' in result['collection']
 walk([],'collection');walk(['s'],'game-options');walk(['s'],'advanced-options')
 if 'retro' not in mode:walk(['down','x'],'support-dialog');walk(['x'],'support-returned')
 walk(['z'],'returned')
 assert out('cat '+dest+'/launch-events')==''
 result['after']=out('cat /proc/sys/kernel/random/boot_id; pidof emulationstation; sha256sum /proc/$(pidof emulationstation)/exe').strip();assert result['before']==result['after']
 observed={}
 # Read literal keys. get_setting's one-argument interface is not its game-key API.
 config=out('cat /storage/.config/system/configs/system.cfg').splitlines()
 for k,v in settings.items():
  values=[line.split('=',1)[1] for line in config if line.startswith(k+'=')]
  assert values==[v], (k,v,values)
  observed[k]=values[0]
 result['selected_settings']=observed
 result['seeded_settings']=settings;result['rc']=0
except BaseException as e:result['error']=str(e);traceback.print_exc()
finally:
 result['ended']=time.time();(case/'result.json').write_text(json.dumps(result,indent=2)+'\n')
raise SystemExit(result['rc'])

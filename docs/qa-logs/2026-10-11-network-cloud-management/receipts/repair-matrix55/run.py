from pathlib import Path
import importlib.util,subprocess,json,hashlib,time
s=importlib.util.spec_from_file_location('v','/tmp/pix537-vm.py');v=importlib.util.module_from_spec(s);s.loader.exec_module(v)
O=Path('/workspace/tmp/pix540-ui55')
subprocess.run(['python3',str(O/'stage.py')],check=True)
expected='c3e6ae523baaf64497c394b71edd784a5aa66201b60bf5c7c97283fe2176f2ca'
for size,mode in [('1280','1280x800'),('640','640x480')]:
 for lang in ('en_US','fr_FR'):
  cohort=O/(lang[:2]+size);cohort.mkdir()
  for old,label in [('44','quote'),('45','missing'),('46','ssh')]:
   owner=cohort/label;owner.mkdir()
   code=Path('/workspace/tmp/pix540-ui'+old+'/run.py').read_text().replace('/workspace/tmp/pix540-ui'+old,str(owner)).replace("'en_US'",repr(lang)).replace('640x480@60Hz',mode+'@60Hz')
   driver=owner/'run.py';driver.write_text(code)
   print(time.strftime('%FT%TZ',time.gmtime()),'START',lang,size,label,flush=True)
   subprocess.run(['python3',str(driver)],check=True)
   actual=json.loads(v.remote('swaymsg -s /run/0-runtime-dir/sway-ipc.0.sock -t get_outputs'))[0]['current_mode']
   assert actual['width']==int(size) and actual['refresh']>0
   h=v.remote('sha256sum /usr/bin/emulationstation').split()[0];assert h==expected
   (owner/'source-receipt.json').write_text(json.dumps({'language':lang,'mode':actual,'binary_sha256':h,'fr_catalog_sha256':v.remote('sha256sum /storage/.config/locale/fr/LC_MESSAGES/emulationstation2.mo').split()[0]},indent=2)+'\n')
   print('PASS completed walk',lang,size,label,flush=True)
(O/'result.json').write_text(json.dumps({'result':'WALKS_COMPLETE_PENDING_VISUAL_REVIEW','cohorts':4,'walks':12,'binary_sha256':expected},indent=2)+'\n')

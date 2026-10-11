from pathlib import Path
import importlib.util,subprocess,time,json
s=importlib.util.spec_from_file_location('v','/tmp/pix537-vm.py');v=importlib.util.module_from_spec(s);s.loader.exec_module(v)
O=Path('/tmp/pix537-final-matrix21')
v.remote("systemctl stop essway; python3 - <<'END'\nfrom pathlib import Path\nimport re\np=Path('/storage/.config/emulationstation/es_settings.cfg');s=p.read_text();s=re.sub(r'<bool name=\"UseOSK\"[^>]*/>', '', s);p.write_text(s.replace('</config>', '<bool name=\"UseOSK\" value=\"true\" /></config>'))\nEND\nsystemctl start essway")
for _ in range(100):
 try:
  v.remote('swaymsg -s /run/0-runtime-dir/sway-ipc.0.sock -t get_outputs');break
 except subprocess.CalledProcessError:time.sleep(.2)
else:raise RuntimeError('no Sway')
expected='eb49472bf412118e49fd24ef8ca268c9c314b1193da896bd112036368b0a13b3'
assert v.remote('sha256sum /usr/bin/emulationstation').split()[0]==expected
for size in ['640','1280']:
 mode='1280x800' if size=='1280' else '640x480'
 v.remote("swaymsg -s /run/0-runtime-dir/sway-ipc.0.sock 'output Virtual-1 mode --custom "+mode+"@60Hz'")
 for lang in ['en_US','fr_FR']:
  for job in ['pix537-ui-lifecycle21.py','pix537-forms-run21.py','pix535-ui-run21.py','pix537-oauth-run21.py']:
   args=['python3','/tmp/'+job,lang,size]
   if job.startswith('pix535'):args+=['all']
   print(time.strftime('%FT%TZ',time.gmtime()),'START',args,flush=True)
   subprocess.run(args,check=True)
   actual=json.loads(v.remote('swaymsg -s /run/0-runtime-dir/sway-ipc.0.sock -t get_outputs'))[0]['current_mode']
   assert actual['width']==int(size) and actual['refresh']>0
   receipt={'job':job,'language':lang,'mode':actual,'es_sha256':v.remote('sha256sum /usr/bin/emulationstation').split()[0],'catalog_sha256':v.remote('sha256sum /storage/.config/locale/fr/LC_MESSAGES/emulationstation2.mo').split()[0]}
   assert receipt['es_sha256']==expected
   (O/(lang+size+'-'+job+'.json')).write_text(json.dumps(receipt,indent=2)+'\n')
   print('PASS',args,flush=True)
(O/'result.json').write_text(json.dumps({'result':'PASS','es_sha256':expected},indent=2)+'\n')
print('PASS final exact-source whole-flow matrix',flush=True)

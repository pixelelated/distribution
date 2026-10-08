import pathlib,subprocess,json,hashlib,time,shlex,datetime
B=pathlib.Path('/workspace/tmp/pixelelated-524-path-refusal');O=pathlib.Path(__file__).resolve().parent;R=pathlib.Path('/workspace/repos/rocknix')
ssh=['ssh','-i',str(B/'guest01/qa-key'),'-p','10220','-o','LogLevel=ERROR','-o','StrictHostKeyChecking=no','-o','UserKnownHostsFile=/dev/null','-o','BatchMode=yes','-o','ConnectTimeout=5','root@127.0.0.1']
scp=['scp','-q','-i',str(B/'guest01/qa-key'),'-P','10220','-o','LogLevel=ERROR','-o','StrictHostKeyChecking=no','-o','UserKnownHostsFile=/dev/null']
def call(cmd,p):
 q=subprocess.run(ssh+[cmd],stdout=subprocess.PIPE,stderr=subprocess.STDOUT);p.write_bytes(q.stdout);q.check_returncode();return q.stdout

def put(path,dest):subprocess.run(scp+[str(path),'root@127.0.0.1:'+dest],check=True)
def walk(d,steps):
 p=d/'steps.txt';p.write_text(steps)
 q=subprocess.run(['python3',str(R/'tools/vm-visual-qa'),'--monitor','/tmp/pix524-mon.sock','run',str(p),'--outdir',str(d/'frames')],stdout=subprocess.PIPE,stderr=subprocess.STDOUT);(d/'walk.log').write_bytes(q.stdout);q.check_returncode()

webdav='[qa]\ntype = webdav\nurl = http://127.0.0.1:9038\nvendor = other\n'
s3='[qa]\ntype = s3\nprovider = Minio\nendpoint = http://10.0.2.2:9039\naccess_key_id = qauser\nsecret_access_key = qa-password\nforce_path_style = true\n'
# These are local synthetic credentials, not an account or external provider.
configs={'webdav':webdav,'bucket':s3,'unreachable':webdav.replace('9038','9040')}
base_helper='/storage/qa524/frozen/usr/bin/cloud_setup'
fixture='''#!/bin/bash
case "$1" in
 --set-syncpath|--set-saves-remote|--set-settings-remote|--set-content-remote)
  case "$(cat /storage/qa524/refusal-fixture-mode)" in
   busy) exit 75 ;;
   timeout) exit 124 ;;
   settings-write) echo "Your cloud sync settings couldn't be saved."; exit 1 ;;
   unknown) echo 'untrusted synthetic provider account value must not appear in UI'; exit 1 ;;
  esac ;;
esac
exec /storage/qa524/frozen/usr/bin/cloud_setup "$@"
'''
(O/'refusal-fixture.sh').write_text(fixture);put(O/'refusal-fixture.sh','/storage/qa524/refusal-fixture.sh')
call('chmod 755 /storage/qa524/refusal-fixture.sh',O/'fixture-install.log')
# Target UI rendering through actual adapter for error statuses that require an
# environmental failure; never labeled a real provider/write/timeout test.
cases=[
 ('invalid-components','/qa//b','webdav',0,None),
 ('blank','','webdav',0,None),
 ('root','/','webdav',0,None),
 ('invalid-name','..','webdav',0,None),
 ('invalid-characters','q$d','webdav',1,None),
 ('bucket','/bad_bucket/b','bucket',0,None),
 ('unreachable','/qa/b','unreachable',0,None),
 ('busy','/qa/b','webdav',0,'busy'),
 ('timeout','/qa/b','webdav',0,'timeout'),
 ('settings-write','/qa/b','webdav',0,'settings-write'),
 ('unknown','/qa/b','webdav',0,'unknown'),
]
(O/'cases.json').write_text(json.dumps(cases,indent=2)+'\n')
witness="set -e; ! pgrep -f '^/usr/bin/retroarch'; /storage/qa524/frozen/usr/bin/cloud_setup --validation-context; sha256sum /storage/.config/cloud_sync.conf /storage/.config/rclone/rclone.conf; find /storage/qa524/provider /storage/qa524/local-witness -type f -exec sha256sum '{}' ';' | sort"
entry='key ret\nwait-for-change 12 0\nsettle\nshot main-menu\nkey x\nwait-for-change 12 0\nkey up x3\nkey x\nwait-for-change 12 0\nsettle\nshot cloud-hub\nkey up x4\nkey x\nwait-for-change 12 0\nsettle\nshot cloud-folders\n'
results=[]
for lang,res in [('en_US','640x480'),('fr_FR','640x480'),('en_US','1280x800'),('fr_FR','1280x800')]:
 d=O/(lang+'-'+res);d.mkdir();print('START',d.name,flush=True)
 config=d/'rclone.conf';config.write_text(webdav);put(config,'/storage/qa524/matrix-rclone.conf')
 mode=('--custom ' if res=='1280x800' else '')+res+'@60Hz'
 setup=f'''set -e
systemctl stop essway.service
mount --bind {base_helper} /usr/bin/cloud_setup
cp /storage/qa524/matrix-rclone.conf /storage/.config/rclone/rclone.conf
chmod 600 /storage/.config/rclone/rclone.conf
/usr/bin/cloud_setup --set-saves-remote /QA/Saves
/usr/bin/cloud_setup --set-settings-remote /QA/Backups
/usr/bin/cloud_setup --set-content-remote /QA/Content
. /etc/profile
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
 (d/'setup.sh').write_text(setup);put(d/'setup.sh','/storage/qa524/matrix-setup.sh');call('bash /storage/qa524/matrix-setup.sh',d/'setup.log');time.sleep(3)
 enter=d/'entry';enter.mkdir();walk(enter,entry)
 for name,path,backend,row,inject in (cases[5:] if (lang,res)==('en_US','640x480') else cases):
  c=d/name;c.mkdir();print('START',d.name,name,flush=True)
  (c/'rclone.conf').write_text(configs[backend]);put(c/'rclone.conf','/storage/qa524/matrix-rclone.conf')
  helper='/storage/qa524/refusal-fixture.sh' if inject else base_helper
  setup='set -e; cp /storage/qa524/matrix-rclone.conf /storage/.config/rclone/rclone.conf; chmod 600 /storage/.config/rclone/rclone.conf; mount --bind '+helper+' /usr/bin/cloud_setup'
  if inject:setup+='; printf %s '+shlex.quote(inject)+' > /storage/qa524/refusal-fixture-mode'
  call(setup,c/'setup.log');before=call(witness,c/'before.txt')
  steps=('key down x'+str(row)+'\n' if row else '')+'key x\nwait-for-change 12 0\nkey backspace x20\n'
  for char in path:
   steps+='key '+{'/':'slash','.':'dot','$':'shift-4','_':'shift-minus'}.get(char,char)+'\n'
  steps+='settle\nshot typed-path\nkey down\nkey x\nwait-for-change 12 0\nsettle\nshot '+name+'\nkey x\nwait-for-change 12 0\n'
  if row:steps+='key up x'+str(row)+'\n'
  walk(c,steps);after=call(witness,c/'after.txt');assert before==after,(d.name,name,'changed paths or payload')
  frame=[c/'frames'/('02-'+name+'.png')];assert frame[0].is_file(),frame
  import struct
  width,height=struct.unpack('>II',frame[0].read_bytes()[16:24]);assert f'{width}x{height}'==res,(width,height,res)
  result={'case':name,'locale':lang,'resolution':res,'backend':backend,'proof_kind':'injected status rendering only' if inject else ('frontend empty field refusal' if name=='blank' else 'actual installed ES/backend path attempt'),'injection':inject,'paths_config_and_payload_unchanged':True,'frame':str(frame[0].relative_to(O)),'frame_sha256':hashlib.sha256(frame[0].read_bytes()).hexdigest(),'completed_at':datetime.datetime.now(datetime.timezone.utc).isoformat()}
  results.append(result);(O/'results.json').write_text(json.dumps(results,indent=2)+'\n');print('PASS',d.name,name,flush=True)
# Restore exact production helper and working synthetic WebDAV config.
config=O/'restored-rclone.conf';config.write_text(webdav);put(config,'/storage/qa524/matrix-rclone.conf');call('set -e; mount --bind '+base_helper+' /usr/bin/cloud_setup; cp /storage/qa524/matrix-rclone.conf /storage/.config/rclone/rclone.conf; chmod 600 /storage/.config/rclone/rclone.conf; sha256sum /usr/bin/cloud_setup',O/'restored-helper.txt')
assert len(results)==39
print('PASS 39 remaining source-bound rendering cases; combine with five independently accepted matrix02 EN640 cases; all paths/config/payload unchanged within each attempt',flush=True)

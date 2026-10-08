import pathlib,subprocess,json,time,shutil
b=pathlib.Path('/workspace/tmp/pixelelated-520-ui-20261008');r=pathlib.Path('/workspace/repos/rocknix.worktrees/conflict-resolution');o=b/'native01'
ssh=['ssh','-i',str(b/'guest01/qa-key'),'-p','10220','-o','LogLevel=ERROR','-o','StrictHostKeyChecking=no','-o','UserKnownHostsFile=/dev/null','root@127.0.0.1'];scp=['scp','-q','-i',str(b/'guest01/qa-key'),'-P','10220','-o','LogLevel=ERROR','-o','StrictHostKeyChecking=no','-o','UserKnownHostsFile=/dev/null']
def call(cmd,name):
 q=subprocess.run(ssh+[cmd],stdout=subprocess.PIPE,stderr=subprocess.STDOUT);(o/name).write_bytes(q.stdout);print(q.stdout.decode(),flush=True);q.check_returncode()
for name,src in [('virtualpad.py','/tmp/pix521-virtualpad.py'),('runtime-config.py','/tmp/pix521-runtime-config.py')]:
 shutil.copy2(src,o/name);subprocess.run(scp+[src,'root@127.0.0.1:/storage/qa521/'+name],check=True)
call('python3 /storage/qa521/runtime-config.py','fixture-config.json')
cmd='''set -eu
systemctl stop essway.service
nohup python3 /storage/qa521/virtualpad.py > /storage/qa521/pad.log 2>&1 </dev/null &
sleep 1
kill -0 "$(cat /storage/qa521/pad.pid)"
cat /proc/bus/input/devices
. /etc/profile
cd /storage
nohup setsid /usr/bin/duckstation-sa -nogui -fullscreen -bios > /storage/qa521/native-default.log 2>&1 </dev/null &
echo $! > /storage/qa521/native.pid
sleep 8
kill -0 "$(cat /storage/qa521/native.pid)"
ps | grep -E 'duckstation|virtualpad' | grep -v grep
cat /storage/qa521/native.pid
tail -n 80 /storage/qa521/native-default.log
''';(o/'launch.sh').write_text(cmd);call(cmd,'launch.log')
subprocess.run(['python3',str(r/'tools/vm-visual-qa'),'--monitor','/tmp/pix520-mon.sock','shot',str(o/'native-before-hotkey.png')],check=True);print('Native fixture process launched; screenshot/hotkey output not yet asserted',flush=True)

import pathlib,subprocess,json,shutil
b=pathlib.Path('/workspace/tmp/pixelelated-520-ui-20261008');r=pathlib.Path('/workspace/repos/rocknix.worktrees/conflict-resolution');o=b/'native-custom01';ssh=['ssh','-i',str(b/'guest01/qa-key'),'-p','10220','-o','LogLevel=ERROR','-o','StrictHostKeyChecking=no','-o','UserKnownHostsFile=/dev/null','root@127.0.0.1'];scp=['scp','-q','-i',str(b/'guest01/qa-key'),'-P','10220','-o','LogLevel=ERROR','-o','StrictHostKeyChecking=no','-o','UserKnownHostsFile=/dev/null']
guest=r'''import pathlib,os,signal,time,json,configparser,hashlib,subprocess
b=pathlib.Path('/storage/qa521');pid=int((b/'native.pid').read_text());args=(pathlib.Path('/proc')/str(pid)/'cmdline').read_bytes();assert b'/usr/bin/duckstation-sa\0' in args and b'-bios' in args;os.kill(pid,signal.SIGTERM)
for _ in range(100):
 p=pathlib.Path('/proc')/str(pid)
 if not p.exists() or not (p/'cmdline').read_bytes():break
 time.sleep(.1)
else:raise RuntimeError('native process did not exit')
p=pathlib.Path('/storage/.config/duckstation/settings.ini');raw=p.read_bytes();(b/'settings-before-custom.ini').write_bytes(raw);c=configparser.ConfigParser(interpolation=None,strict=False);c.optionxform=str;c.read_string(raw.decode());c.set('Folders','Screenshots','/storage/qa521/custom-captures');custom=pathlib.Path('/storage/qa521/custom-captures');custom.mkdir();(custom/'owner-history.marker').write_bytes(b'Existing owner custom capture bytes\n')
with p.open('w') as f:c.write(f)
before=p.read_bytes();q=subprocess.run(['/usr/bin/duckstation_screenshot_path',str(p)],capture_output=True);assert q.returncode==0 and p.read_bytes()==before;old={str(x):hashlib.sha256(x.read_bytes()).hexdigest() for root in (pathlib.Path('/storage/roms/screenshots'),pathlib.Path('/storage/.config/duckstation/screenshots'),custom) for x in root.rglob('*') if x.is_file()};(b/'custom-before-files.json').write_text(json.dumps(old,indent=2)+'\n');(b/'settings-custom.ini').write_bytes(before);print(json.dumps({'old_native_pid':pid,'old_process_exited':True,'custom_helper_exit':q.returncode,'custom_setting_preserved':True,'custom_config_sha256':hashlib.sha256(before).hexdigest(),'old_files':old},indent=2))
''';(o/'prepare-guest.py').write_text(guest);q=subprocess.run(ssh+['python3 -'],input=guest.encode(),stdout=subprocess.PIPE,stderr=subprocess.STDOUT);(o/'prepare.json').write_bytes(q.stdout);q.check_returncode()
cmd='''. /etc/profile
cd /storage
nohup setsid /usr/bin/duckstation-sa -nogui -fullscreen -bios > /storage/qa521/native-custom.log 2>&1 </dev/null &
echo $! > /storage/qa521/native.pid
sleep 8
kill -0 "$(cat /storage/qa521/native.pid)"
tail -n 35 /storage/qa521/native-custom.log
''';(o/'launch.sh').write_text(cmd);q=subprocess.run(ssh+[cmd],stdout=subprocess.PIPE,stderr=subprocess.STDOUT);(o/'launch.log').write_bytes(q.stdout);q.check_returncode();subprocess.run(['python3',str(r/'tools/vm-visual-qa'),'--monitor','/tmp/pix520-mon.sock','shot',str(o/'custom-before-hotkey.png')],check=True)
print('Custom-path native launch complete; hotkey/output not yet asserted',flush=True)

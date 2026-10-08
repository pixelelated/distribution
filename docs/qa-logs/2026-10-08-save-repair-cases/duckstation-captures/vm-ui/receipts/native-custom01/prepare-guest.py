import pathlib,os,signal,time,json,configparser,hashlib,subprocess
b=pathlib.Path('/storage/qa521');pid=int((b/'native.pid').read_text());args=(pathlib.Path('/proc')/str(pid)/'cmdline').read_bytes();assert b'/usr/bin/duckstation-sa\0' in args and b'-bios' in args;os.kill(pid,signal.SIGTERM)
for _ in range(100):
 p=pathlib.Path('/proc')/str(pid)
 if not p.exists() or not (p/'cmdline').read_bytes():break
 time.sleep(.1)
else:raise RuntimeError('native process did not exit')
p=pathlib.Path('/storage/.config/duckstation/settings.ini');raw=p.read_bytes();(b/'settings-before-custom.ini').write_bytes(raw);c=configparser.ConfigParser(interpolation=None,strict=False);c.optionxform=str;c.read_string(raw.decode());c.set('Folders','Screenshots','/storage/qa521/custom-captures');custom=pathlib.Path('/storage/qa521/custom-captures');custom.mkdir();(custom/'owner-history.marker').write_bytes(b'Existing owner custom capture bytes\n')
with p.open('w') as f:c.write(f)
before=p.read_bytes();q=subprocess.run(['/usr/bin/duckstation_screenshot_path',str(p)],capture_output=True);assert q.returncode==0 and p.read_bytes()==before;old={str(x):hashlib.sha256(x.read_bytes()).hexdigest() for root in (pathlib.Path('/storage/roms/screenshots'),pathlib.Path('/storage/.config/duckstation/screenshots'),custom) for x in root.rglob('*') if x.is_file()};(b/'custom-before-files.json').write_text(json.dumps(old,indent=2)+'\n');(b/'settings-custom.ini').write_bytes(before);print(json.dumps({'old_native_pid':pid,'old_process_exited':True,'custom_helper_exit':q.returncode,'custom_setting_preserved':True,'custom_config_sha256':hashlib.sha256(before).hexdigest(),'old_files':old},indent=2))

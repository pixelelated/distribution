#!/usr/bin/python3
"""Synthetic runtime-only settings; the product bindings and screenshot path stay exact."""
import configparser,pathlib,json,hashlib
root=pathlib.Path('/storage/qa521');path=pathlib.Path('/storage/.config/duckstation/settings.ini');raw=path.read_bytes();(root/'settings-before-runtime.ini').write_bytes(raw)
c=configparser.ConfigParser(interpolation=None,strict=False);c.optionxform=str;c.read_string(raw.decode())
for section,values in {'BIOS':{'SearchDirectory':'/storage/qa521/frozen','PathNTSCU':'synthetic-display.bin','PatchFastBoot':'false'},'Console':{'Region':'NTSC-U'},'GPU':{'Renderer':'Software'},'Logging':{'LogLevel':'Debug','LogToConsole':'true','LogToFile':'true'},'Cheevos':{'Enabled':'false'}}.items():
 if not c.has_section(section):c.add_section(section)
 for key,val in values.items():c.set(section,key,val)
assert c.get('Hotkeys','Screenshot')=='SDL-0/Guide & SDL-0/B'
assert c.get('Folders','Screenshots')=='/storage/roms/screenshots'
with path.open('w') as f:c.write(f)
(root/'settings-runtime.ini').write_bytes(path.read_bytes());user=pathlib.Path('/storage/.local/share');user.mkdir(exist_ok=True);link=user/'duckstation'
if link.exists() or link.is_symlink():
 assert link.is_symlink() and link.resolve()==path.parent
else:link.symlink_to(path.parent,target_is_directory=True)
print(json.dumps({'before_sha256':hashlib.sha256(raw).hexdigest(),'runtime_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'screenshot_hotkey':c.get('Hotkeys','Screenshot'),'screenshot_folder':c.get('Folders','Screenshots'),'synthetic_bios':c.get('BIOS','PathNTSCU'),'data_root_link':str(link.resolve()),'no_gameplay_claim':True},indent=2))

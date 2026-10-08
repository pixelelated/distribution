import pathlib,json,hashlib,time,struct,os
b=pathlib.Path('/storage/qa521');root=pathlib.Path('/storage/qa521/custom-captures');old=pathlib.Path('/storage/.config/duckstation/screenshots');history=json.loads((b/'custom-before-files.json').read_text());before=set(root.glob('*.png'));assert not before
with (b/'pad.commands').open('w') as f:f.write('capture\n')
start=time.monotonic();new=[]
while time.monotonic()-start<10:
 new=list(set(root.glob('*.png'))-before)
 if len(new)==1 and new[0].stat().st_size>32:break
 time.sleep(.1)
assert len(new)==1,new;time.sleep(.2);p=new[0];raw=p.read_bytes();assert raw[:8]==b'\x89PNG\r\n\x1a\n';dims=struct.unpack('>II',raw[16:24]);assert all(pathlib.Path(x).is_file() and hashlib.sha256(pathlib.Path(x).read_bytes()).hexdigest()==digest for x,digest in history.items());assert 'Screenshots = /storage/qa521/custom-captures' in pathlib.Path('/storage/.config/duckstation/settings.ini').read_text()
print(json.dumps({'case':'DS02','native_png':str(p),'sha256':hashlib.sha256(raw).hexdigest(),'bytes':len(raw),'png_dimensions':dims,'old_capture_inventory_unchanged':history,'actual_binding':'SDL-0/Guide & SDL-0/B','native_process_pid':int((b/'native.pid').read_text()),'elapsed_to_file_seconds':time.monotonic()-start},indent=2))

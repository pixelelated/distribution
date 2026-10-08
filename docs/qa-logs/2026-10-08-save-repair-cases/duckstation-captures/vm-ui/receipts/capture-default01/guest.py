import pathlib,json,hashlib,time,struct,os
b=pathlib.Path('/storage/qa521');root=pathlib.Path('/storage/roms/screenshots');old=pathlib.Path('/storage/.config/duckstation/screenshots');history={str(p):hashlib.sha256(p.read_bytes()).hexdigest() for p in old.rglob('*') if p.is_file()};before=set(root.glob('*.png'));assert not before
with (b/'pad.commands').open('w') as f:f.write('capture\n')
start=time.monotonic();new=[]
while time.monotonic()-start<10:
 new=list(set(root.glob('*.png'))-before)
 if len(new)==1 and new[0].stat().st_size>32:break
 time.sleep(.1)
assert len(new)==1,new;time.sleep(.2);p=new[0];raw=p.read_bytes();assert raw[:8]==b'\x89PNG\r\n\x1a\n';dims=struct.unpack('>II',raw[16:24]);assert {str(x):hashlib.sha256(x.read_bytes()).hexdigest() for x in old.rglob('*') if x.is_file()}==history
print(json.dumps({'case':'DS01','native_png':str(p),'sha256':hashlib.sha256(raw).hexdigest(),'bytes':len(raw),'png_dimensions':dims,'old_capture_inventory_unchanged':history,'actual_binding':'SDL-0/Guide & SDL-0/B','native_process_pid':int((b/'native.pid').read_text()),'elapsed_to_file_seconds':time.monotonic()-start},indent=2))

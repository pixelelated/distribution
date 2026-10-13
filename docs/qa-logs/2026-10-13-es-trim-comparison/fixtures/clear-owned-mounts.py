from pathlib import Path
import subprocess,json,hashlib
allowed={'/usr/bin/emulationstation','/storage/qa570compare/baseline','/storage/qa570compare/candidate'}
removed=[]
for _ in range(32):
 rows=[l.split() for l in Path('/proc/self/mountinfo').read_text().splitlines()];owned=[x for x in rows if x[4] in allowed]
 if not owned:break
 target=max(owned,key=lambda x:int(x[0]))[4]
 subprocess.run(['umount',target],check=True,timeout=5);removed.append(target)
else:raise RuntimeError('owned mount cleanup did not converge')
assert not any(l.split()[4] in allowed for l in Path('/proc/self/mountinfo').read_text().splitlines())
files={p:hashlib.file_digest(Path(p).open('rb'),'sha256').hexdigest() for p in allowed}
assert files['/usr/bin/emulationstation']==files['/storage/qa570compare/baseline']=='db136580f0a46442bb3fe7ac9e31606b38b816c78efc8f9b4e267284daca6502'
assert files['/storage/qa570compare/candidate']=='5c08a1713e9af08054e6ec01480894987f48e9335b44fbf8e02462109438ca6f'
print(json.dumps({'removed_mounts':removed,'hashes':files}))

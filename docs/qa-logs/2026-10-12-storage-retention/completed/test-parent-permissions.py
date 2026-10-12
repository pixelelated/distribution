from pathlib import Path
from unittest.mock import patch
import importlib.util, tempfile, os, stat, json
O=Path(__file__).resolve().parent
s=importlib.util.spec_from_file_location('guards',O/'guards.py');g=importlib.util.module_from_spec(s);s.loader.exec_module(g)
passed=[]
with tempfile.TemporaryDirectory(dir=O/'tmp') as d:
 base=Path(d)
 def fixture(name):
  p=base/name;p.mkdir();f=p/'firmware';f.write_bytes(b'fixture');p.chmod(0o555);x=p.stat()
  return {'path':str(f),'identity':g.identity(f),'parent_identity':dict(device=x.st_dev,inode=x.st_ino,uid=x.st_uid,mode=x.st_mode)}
 r=fixture('success');g.check_parent(r);g.unlink_owned_payload(r)
 assert not Path(r['path']).exists() and stat.S_IMODE(Path(r['path']).parent.stat().st_mode)==0o555
 passed.append('Owned read-only parent: remove exact file and restore mode555')
 r=fixture('error')
 with patch.object(g.os,'unlink',side_effect=PermissionError('injected unlink failure')):
  try:g.unlink_owned_payload(r);raise AssertionError('failure not propagated')
  except PermissionError:pass
 assert Path(r['path']).exists() and stat.S_IMODE(Path(r['path']).parent.stat().st_mode)==0o555
 passed.append('Unlink failure: preserve file and restore mode555')
 r=fixture('changed-parent');r['parent_identity']['inode']+=1
 try:g.check_parent(r);raise AssertionError('changed parent accepted')
 except RuntimeError:pass
 assert Path(r['path']).exists() and stat.S_IMODE(Path(r['path']).parent.stat().st_mode)==0o555
 passed.append('Changed parent identity refused before mutation')
 r=fixture('changed-file');r['identity']['inode']+=1
 try:g.unlink_owned_payload(r);raise AssertionError('changed file accepted')
 except RuntimeError:pass
 assert Path(r['path']).exists() and stat.S_IMODE(Path(r['path']).parent.stat().st_mode)==0o555
 passed.append('Changed file identity refused before mutation')
 r=fixture('link-target');link=base/'link';link.symlink_to(Path(r['path']).parent,target_is_directory=True);r['path']=str(link/'firmware')
 try:g.check_parent(r);raise AssertionError('symlink parent accepted')
 except RuntimeError:pass
 assert Path(r['path']).exists()
 passed.append('Redirected parent refused before mutation')
 for p in base.iterdir():
  if p.is_dir() and not p.is_symlink():p.chmod(0o755)
print(json.dumps({'result':'PASS','checks':passed},indent=2))

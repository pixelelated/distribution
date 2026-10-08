from pathlib import Path
import hashlib,json
O=Path(__file__).resolve().parent;j=json.loads((O/'inputs.json').read_text());assert Path.cwd()==Path(j['container_worktree'])
files=j['cache_parent_provenance']['fex_carry_forward_files']
for name,h in files.items():
 p=Path(name);assert p.is_relative_to(j['container_worktree'])
 digest=hashlib.sha256()
 with p.open('rb') as stream:
  for chunk in iter(lambda:stream.read(4*1024**2),b''):digest.update(chunk)
 assert digest.hexdigest()==h,name
print('PASS unchanged accepted FEX build stamps, generated guest toolchains and package payload before rebuild',flush=True)

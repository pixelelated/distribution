import hashlib,json
from pathlib import Path
p=Path('sources/webkitgtk/webkitgtk-2.54.1.tar.xz')
h=hashlib.sha256()
with p.open('rb') as f:
 for block in iter(lambda:f.read(1024*1024),b''):h.update(block)
assert h.hexdigest()=='ea0bbb02dbdbc596874a4e7ad35b66645b3e0a232bd0e4081de5ed92eb0a397d'
assert Path(str(p)+'.sha256').read_text().strip()==h.hexdigest()
assert Path(str(p)+'.url').read_text().strip()=='https://webkitgtk.org/releases/webkitgtk-2.54.1.tar.xz'
Path('/build-owner/source-readback.json').write_text(json.dumps(dict(status='PASS',bytes=p.stat().st_size,sha256=h.hexdigest()))+'\n')

from pathlib import Path
import tarfile,hashlib,json,shutil,subprocess
out=Path('/tmp/pixelelated-proxy-aec99c');old=Path('/tmp/pixelelated-proxy-ea9aba/new/RAOfflineProxy-ea9aba6c2b8b2f27e254d696ac8738c9e5c8793e');new=out/'new'
new.mkdir(exist_ok=False)
with tarfile.open(out/'upstream.tar.gz') as t:t.extractall(new,filter='data')
new=next(new.iterdir())
def hashes(root):return {str(p.relative_to(root)):hashlib.sha256(p.read_bytes()).hexdigest() for p in root.rglob('*') if p.is_file()}
a=hashes(old);b=hashes(new);changes=[x for x in sorted(a.keys()|b.keys()) if a.get(x)!=b.get(x)]
assert len(changes)==6 and all(x.startswith(('app/','docs/')) for x in changes),changes
linux={p:h for p,h in b.items() if p.startswith(('linux/','third_party/'))}
assert all(a.get(p)==h for p,h in linux.items())
patched=out/'patched';shutil.copytree(new,patched)
patches=sorted(Path('projects/ROCKNIX/packages/network/raofflineproxy/patches').glob('*.patch'))
with (out/'patches.log').open('w') as log:
 for patch in patches:subprocess.run(['patch','-p1','--fuzz=0','-i',str(patch.resolve())],cwd=patched,stdout=log,stderr=log,check=True)
a=hashes(Path('/tmp/pixelelated-proxy-ea9aba/new-patched'));b=hashes(patched)
consumed={p:h for p,h in b.items() if p.startswith(('linux/','third_party/')) and '__pycache__' not in p}
assert all(a.get(p)==h for p,h in consumed.items())
assert set(consumed)=={p for p in a if p.startswith(('linux/','third_party/')) and '__pycache__' not in p}
r={'old':'ea9aba6c2b8b2f27e254d696ac8738c9e5c8793e','new':'aec99ce05bc0b9761366543fe9f08ea34cd8bd7a','changed_files':changes,'unchanged_raw_linux_native_files':len(linux),'patches_zero_fuzz':len(patches),'patched_linux_native_files':consumed,'archive_sha256':hashlib.sha256((out/'upstream.tar.gz').read_bytes()).hexdigest()};(out/'comparison.json').write_text(json.dumps(r,indent=2)+'\n');print({k:v for k,v in r.items() if k!='patched_linux_native_files'});print('PASS exact equality of',len(consumed),'patched Linux/native files')

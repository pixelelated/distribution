from pathlib import Path
import tarfile,hashlib,json,shutil,subprocess,difflib
out=Path('/tmp/pixelelated-proxy-865e21');old=Path('/tmp/pixelelated-proxy-aec99c/new/RAOfflineProxy-aec99ce05bc0b9761366543fe9f08ea34cd8bd7a');dest=out/'new';dest.mkdir()
with tarfile.open(out/'upstream.tar.gz') as t:t.extractall(dest,filter='data')
new=next(dest.iterdir())
def hashes(root):return {str(p.relative_to(root)):hashlib.sha256(p.read_bytes()).hexdigest() for p in root.rglob('*') if p.is_file() and '__pycache__' not in p.parts}
a=hashes(old);b=hashes(new);changes=[p for p in sorted(a.keys()|b.keys()) if a.get(p)!=b.get(p)];bundles={'linux/allium/build_bundle.sh','linux/onion/build_bundle.sh'}
assert len(changes)==17 and set(p for p in changes if not p.startswith('app/'))==bundles,changes
linux={p:h for p,h in b.items() if p.startswith(('linux/','third_party/'))};assert set(linux)=={p for p in a if p.startswith(('linux/','third_party/'))}
assert all(a[p]==h for p,h in linux.items() if p not in bundles)
(out/'unshipped-bundle.diff').write_text(''.join(''.join(difflib.unified_diff((old/p).read_text().splitlines(True),(new/p).read_text().splitlines(True),fromfile='old/'+p,tofile='new/'+p)) for p in sorted(bundles)))
for p in bundles:subprocess.run(['bash','-n',str(new/p)],check=True)
patched=out/'patched';shutil.copytree(new,patched);patches=sorted(Path('projects/ROCKNIX/packages/network/raofflineproxy/patches').glob('*.patch'))
with (out/'patches.log').open('w') as log:
 for patch in patches:subprocess.run(['patch','-p1','--fuzz=0','-i',str(patch.resolve())],cwd=patched,stdout=log,stderr=log,check=True)
a=hashes(Path('/tmp/pixelelated-proxy-aec99c/patched'));b=hashes(patched);shared={p:h for p,h in b.items() if p.startswith(('linux/','third_party/')) and p not in bundles};assert set(shared)=={p for p in a if p.startswith(('linux/','third_party/')) and p not in bundles};assert all(a[p]==h for p,h in shared.items())
consumed={p:h for p,h in shared.items() if p.startswith(('linux/raofflineproxy/','third_party/'))}
report={'old':'aec99ce05bc0b9761366543fe9f08ea34cd8bd7a','new':'865e218660e9914e3ba0b4326b5d430af995c843','archive_sha256':hashlib.sha256((out/'upstream.tar.gz').read_bytes()).hexdigest(),'changed_files':changes,'unshipped_changed_linux_bundle_scripts':sorted(bundles),'unchanged_raw_linux_native_excluding_bundle_scripts':len(linux)-2,'zero_fuzz_patches':len(patches),'identical_patched_linux_native_and_tests_excluding_bundles':shared,'consumed_python_native_files':consumed,'storage_schema_sha256':consumed['linux/raofflineproxy/storage.py']}
(out/'comparison.json').write_text(json.dumps(report,indent=2)+'\n');print({k:v for k,v in report.items() if not isinstance(v,dict)})

"""Verify complete FEX package and retained guest toolchain before image assembly."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,os,subprocess
owner=Path(__file__).resolve().parent
j=json.loads((owner/'inputs.json').read_text());root=Path.cwd()/j['build_root'];assert Path.cwd()==Path(j['container_worktree'])
fex=root/'build'/('fex-emu-'+j['fex_commit']);build=fex/'.aarch64-rocknix-linux-gnu'
installed=root/'install_pkg'/('fex-emu-'+j['fex_commit'])
def sha(p):
 h=hashlib.sha256()
 with p.open('rb') as f:
  for block in iter(lambda:f.read(4*1024**2),b''):h.update(block)
 return h.hexdigest()
version=subprocess.check_output([str(fex/'nix/.nix-profile/bin/nix'),'--version'],text=True).strip()
assert version=='nix (Nix) '+j['nix_version'],version
cache=(build/'CMakeCache.txt').read_text()
for name in ['expected_rootfs','toolchain32','toolchain64']:assert j[name] in cache,(name,j[name])
for name,h in j['nix_toolchain_hashes'].items():assert sha(Path(name))==h,name
for name in ['Guest','Guest_32']:
 ninja=(build/name/'build.ninja').read_text()
 lines=[line for line in ninja.splitlines() if line.strip().startswith('INCLUDES =')]
 assert lines,name
 bad='-I'+str(root/'toolchain/aarch64-rocknix-linux-gnu/sysroot/usr/include')
 assert not any(bad in line.split() for line in lines),name
records=[]
def elf(path,bits,machine):
 data=path.read_bytes();assert data[:6]==b'\x7fELF'+bytes([1 if bits==32 else 2,1]) and int.from_bytes(data[18:20],'little')==machine,path
 records.append({'path':str(path.relative_to(installed)),'sha256':sha(path),'bytes':len(data),'bits':bits,'machine':machine})
elf(installed/'usr/bin/FEX',64,183)
for bits,names in [(32,j['guest_libraries32']),(64,j['guest_libraries64'])]:
 folder='GuestThunks_32' if bits==32 else 'GuestThunks'
 for name in names:elf(installed/'usr/share/fex-emu'/folder/name,bits,3 if bits==32 else 62)
assert (root/'.stamps/fex-emu/build_target').is_file()
receipt={'utc':datetime.now(timezone.utc).isoformat(),'result':'PASS','nix_version':version,'nixpkgs_url':j['nixpkgs_url'],'rootfs':j['expected_rootfs'],'toolchain32':j['toolchain32'],'toolchain64':j['toolchain64'],'files':records,'scope':'Complete FEX package: native AArch64 runtime and all installed x86 guest thunks; no native execution claim'}
(owner/'artifacts/fex-package.json').write_text(json.dumps(receipt,indent=2)+'\n');print(json.dumps(receipt),flush=True)

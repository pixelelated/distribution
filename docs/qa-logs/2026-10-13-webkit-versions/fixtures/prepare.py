from pathlib import Path
import os,subprocess,json,hashlib,shutil,datetime,time,tarfile
r=Path(__file__).parent
src=Path('/workspace/repos/rocknix.worktrees/m7-pixelelated-replacement20/build.pixelelated-GENERIC_X64.x86_64/build/webkitgtk-2.54.1')
dst=r/'package-2.54.0'; fresh=r/'source-2.54.0'; cache=Path('/workspace/cache/rocknix-sources/webkitgtk')
sha=lambda p:hashlib.file_digest(p.open('rb'),'sha256').hexdigest()
result={'started':datetime.datetime.now(datetime.timezone.utc).isoformat(),'source':str(src)}
try:
 assert shutil.disk_usage(r).free>30*1024**3
 assert not dst.exists() and not fresh.exists()
 digests={'2.54.0':'846fd19ccedbae1dbfe904f26dbf2d68a800a33a50caf2ad5222c8dcb3f25682','2.54.1':'ea0bbb02dbdbc596874a4e7ad35b66645b3e0a232bd0e4081de5ed92eb0a397d','2.52.6':'179a2ea3f8f6edd4be7f31fdc55afc57bd0729f1fba648c61d4181539ac116fc'}
 for v,h in digests.items():assert sha(cache/f'webkitgtk-{v}.tar.xz')==h
 result['archives']=digests
 sentinels=[src/'.x86_64-rocknix-linux-gnu/CMakeCache.txt',src/'Source/WebKit/PlatformGTK.cmake']+list((src/'.x86_64-rocknix-linux-gnu/lib').glob('libwebkit*.so.*'))
 sentinels=[p for p in sentinels if p.is_file() and not p.is_symlink()]
 result['frozen_sentinels']={str(p):sha(p) for p in sentinels}
 print('Copying one independent WebKit package, approximately6.2GiB',flush=True)
 subprocess.run(['cp','-a','--reflink=auto',str(src),str(dst)],check=True)
 for p in sentinels:
  q=dst/p.relative_to(src);assert p.stat().st_ino!=q.stat().st_ino;assert sha(p)==sha(q)
 fresh.mkdir();subprocess.run(['tar','-xJf',str(cache/'webkitgtk-2.54.0.tar.xz'),'--strip-components=1','-C',str(fresh)],check=True)
 patches=Path.cwd()/'packages/web/webkitgtk/patches'
 result['patches']={}
 for p in sorted(patches.glob('*.patch')):
  result['patches'][p.name]=sha(p)
  subprocess.run(['patch','--batch','--forward','-p1','-i',str(p)],cwd=fresh,check=True)
 # Replace only source bytes differing from the complete, freshly patched2.54.0 archive.
 changed=[];verified=0
 for p in fresh.rglob('*'):
  rel=p.relative_to(fresh);q=dst/rel
  if p.is_dir():q.mkdir(exist_ok=True);continue
  if p.is_symlink():
   if q.is_symlink() and os.readlink(q)==os.readlink(p):continue
   if q.exists() or q.is_symlink():q.unlink()
   q.symlink_to(os.readlink(p));changed.append(str(rel));continue
  if q.is_file() and sha(q)==sha(p):verified+=1;continue
  shutil.copy2(p,q);os.utime(q,None);changed.append(str(rel));verified+=1
 with tarfile.open(cache/'webkitgtk-2.54.1.tar.xz','r:xz') as t:
  prior={Path(*Path(m.name).parts[1:]) for m in t if m.isfile() or m.issym()}
 removed=[]
 for rel in prior:
  p=fresh/rel;q=dst/rel
  if not p.exists() and not p.is_symlink() and (q.exists() or q.is_symlink()):q.unlink();removed.append(str(rel))
 for p,h in result['frozen_sentinels'].items():assert sha(Path(p))==h
 result.update(rc=0,source_files_verified=verified,changed=changed,removed=removed,package_bytes=int(subprocess.check_output(['du','-sb',str(dst)],text=True).split()[0]))
 print('Prepared2.54.0 patched source:',verified,'files;',len(changed),'changed;',len(removed),'removed',flush=True)
except BaseException as e:
 result.update(rc=1,error=str(e));raise
finally:
 result['ended']=datetime.datetime.now(datetime.timezone.utc).isoformat();(r/'prepare-result.json').write_text(json.dumps(result,indent=2)+'\n')

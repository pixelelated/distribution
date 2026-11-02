#!/usr/bin/env python3
"""T41 Stage B: only cached archives and isolated touched-file scratch."""
from pathlib import Path
import subprocess,hashlib,datetime,time,json,re,shutil,os
R=Path('/workspace/repos/pixelelated/distribution.worktrees/m6-patches-shipped-kernel-688')
T=Path('/workspace/tmp/m6-t41'); C=Path('/workspace/cache/rocknix-sources')
A=R/'docs/audits/2026_11_02-epic-m6-patches-shipped-kernel'; O=A/'stage-b'; O.mkdir(exist_ok=True)
REF='02aab33bd9842610b0d466c9c186454dc14373ee'
assert subprocess.check_output(['git','rev-parse','HEAD'],cwd=R,text=True).strip()==REF
os.environ['LC_ALL']='C'
def stamp():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def escape(s):return s.replace('mask'+'-data0','mask'+chr(92)+'u002ddata0')
def save(path,data):path.parent.mkdir(parents=True,exist_ok=True);path.write_text(escape(data))
def blob(p):return subprocess.check_output(['git','show',REF+':'+p],cwd=R)
def run(args,**kw):
 start=stamp(); tic=time.monotonic(); p=subprocess.run(args,cwd=R,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=300,**kw)
 return p,{'command':args,'start':start,'elapsed_seconds':round(time.monotonic()-tic,3),'rc':p.returncode}
paths=(A/'stage-a/p1-qa-scratch/paths.txt').read_text().replace(chr(92)+'u002d','-').splitlines()
orders={d:(A/f'stage-a/order-{d}.txt').read_text().replace(chr(92)+'u002d','-').splitlines() for d in ['GENERIC_X64','H700','SM8550']}
for d in ['DDR3','DDR4']:orders['UBOOT-'+d]=[p for p in paths if f'/u-boot-{d}/' in p]
orders['FIRMWARE']=[p for p in paths if '/kernel-firmware/patches/' in p]
assert [len(orders[d]) for d in orders]==[8,42,65,2,2,1]
spec={
 'GENERIC_X64':('linux/linux-7.1.2.tar.xz','linux-7.1.2','37198c93727be247c9fb5309bb86cd5e496c61e5322cd8c4eca9476bb0b5883f','projects/ROCKNIX/packages/linux/package.mk'),
 'H700':('linux/linux-7.2.tar.xz','linux-7.2','f9fef3d14c0df53819026f4be74459835c2a0b0dcbf5b5bbd9ea19f0829402b3','projects/ROCKNIX/packages/linux/package.mk'),
 'SM8550':('linux/linux-7.2.tar.xz','linux-7.2','f9fef3d14c0df53819026f4be74459835c2a0b0dcbf5b5bbd9ea19f0829402b3','projects/ROCKNIX/packages/linux/package.mk'),
 'UBOOT-DDR3':('u-boot-DDR3/u-boot-DDR3-v2026.01.tar.gz','u-boot-2026.01','03bb43c58d2343ee48dd191e0f181f0108425b179d84519add3a977071c3f654','projects/ROCKNIX/devices/H700/packages/u-boot-DDR3/package.mk'),
 'UBOOT-DDR4':('u-boot-DDR4/u-boot-DDR4-v2026.01.tar.gz','u-boot-2026.01','03bb43c58d2343ee48dd191e0f181f0108425b179d84519add3a977071c3f654','projects/ROCKNIX/devices/H700/packages/u-boot-DDR4/package.mk'),
 'FIRMWARE':('kernel-firmware/kernel-firmware-20260309.tar.gz','linux-firmware-20260309','28fb1b57fa9531edbd001a2462068267f10622e613abd40f952344b3f1fc5a16','projects/ROCKNIX/packages/linux-firmware/kernel-firmware/package.mk')}
records=[]; allrows=[]; checksum={}
for dev,order in orders.items():
 arc,root,expected,recipe=spec[dev]; archive=C/arc
 if arc not in checksum:
  tic=time.monotonic(); h=hashlib.sha256()
  with archive.open('rb') as f:
   for chunk in iter(lambda:f.read(1048576),b''):h.update(chunk)
  side=Path(str(archive)+'.sha256').read_text().split()[0]; actual=h.hexdigest()
  assert actual==side==expected,(dev,'archive/sidecar/recipe hash mismatch')
  assert expected in blob(recipe).decode(),(dev,'recipe hash absent')
  checksum[arc]={'sha256':actual,'sidecar':side,'recipe':recipe,'elapsed_seconds':round(time.monotonic()-tic,3)}
 print(stamp(),dev,'hash verified',flush=True)
 targetset=set(); raw={p:blob(p) for p in order}
 for p,data in raw.items():
  for l in data.decode(errors='replace').splitlines():
   if l.startswith(('--- ','+++ ')):
    q=l[4:].split()[0] if l[4:].split() else ''
    if q=='/dev/null':continue
    if '/' not in q:continue
    q=q.split('/',1)[1]
    assert q and not q.startswith('/') and '..' not in Path(q).parts,(p,q)
    targetset.add(root+'/'+q)
 targets=T/f'targets-{dev}.txt';targets.write_text('\n'.join(sorted(targetset))+'\n');save(O/targets.name,targets.read_text())
 dest=T/'src'/('stage-b-'+dev); assert not dest.exists(),str(dest)+' already exists; do not rerun over patched scratch';dest.mkdir()
 args=['tar','--extract','--file',str(archive),'--directory',str(dest),'--no-same-owner','--no-same-permissions','--verbatim-files-from','--files-from',str(targets)]
 proc,rec=run(args);out=proc.stdout.decode(errors='replace');rec.update(plan=dev,targets=len(targetset),not_in_archive=out.count('Not found in archive'))
 records.append(rec);save(O/f'tar-{dev}.out',out);save(O/f'tar-{dev}.json',json.dumps(rec,indent=2)+'\n')
 assert proc.returncode in [0,2],(dev,rec)
 if proc.returncode==2:assert 'Not found in archive' in out and all(('Not found in archive' in l or 'Exiting with failure status' in l) for l in out.splitlines()),(dev,out)
 source=dest/root; assert source.is_dir(),(dev,'archive root absent')
 pristine=T/'src'/('pristine-'+dev);shutil.copytree(source,pristine)
 save(O/f'order-{dev}.txt','\n'.join(order)+'\n')
 print(stamp(),dev,'tar',rec,flush=True)
 summaries=[]
 for i,p in enumerate(order,1):
  args=['patch','-p1','--dry-run','-N','--batch','--directory',str(source)]
  proc,rec=run(args,input=raw[p]);out=proc.stdout.decode(errors='replace');rec.update(plan=dev,index=i,path=p,offset=out.count('offset'),fuzz=out.count('fuzz'),FAILED=out.count('FAILED'))
  rec['verdict']='fails' if proc.returncode else 'fuzz' if rec['fuzz'] else 'applies with offset' if rec['offset'] else 'applies'
  save(O/f'logs/{dev}-{i:03d}.dry.out',out)
  if not proc.returncode:
   apply,arec=run([x for x in args if x!='--dry-run'],input=raw[p]);save(O/f'logs/{dev}-{i:03d}.apply.out',apply.stdout.decode(errors='replace'));rec['apply']=arec
   assert apply.returncode==0,(dev,p,'apply failed after successful dry-run')
  allrows.append(rec)
  summaries.append(f'{dev} {i:03d} {p} rc={rec["rc"]} offset={rec["offset"]} fuzz={rec["fuzz"]} FAILED={rec["FAILED"]} verdict={rec["verdict"]}')
 save(O/f'applies-{dev}.txt','\n'.join(summaries)+'\n');(T/f'applies-{dev}.txt').write_text('\n'.join(summaries)+'\n')
 print(stamp(),dev,'complete',dict(__import__('collections').Counter(x['verdict'] for x in allrows if x['plan']==dev)),flush=True)
save(O/'archive-sha256.json',json.dumps(checksum,indent=2)+'\n');save(O/'application-results.json',json.dumps({'reviewed_source':REF,'tar':records,'rows':allrows},indent=2)+'\n')
save(O/'cached-apply.py',Path(__file__).read_text())
print('DONE',len(allrows),'application rows; no source product paths written',flush=True)

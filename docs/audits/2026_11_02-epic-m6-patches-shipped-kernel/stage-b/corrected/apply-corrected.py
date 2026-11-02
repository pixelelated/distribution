#!/usr/bin/env python3
"""T41 corrected Stage-B runner. No source tree, cache or old receipt writes."""
from pathlib import Path
import subprocess,hashlib,datetime,time,json,re,shutil,os,collections
R=Path('/workspace/repos/pixelelated/distribution.worktrees/m6-patches-shipped-kernel-688')
T=Path('/workspace/tmp/m6-t41');C=Path('/workspace/cache/rocknix-sources')
A=R/'docs/audits/2026_11_02-epic-m6-patches-shipped-kernel'; O=A/'stage-b/corrected'
REF='02aab33bd9842610b0d466c9c186454dc14373ee'
CO='4c8a118cfb4efa8d13c1b41b72ef7a205da5f766'
os.environ['LC_ALL']='C'
def stamp():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def esc(s):return s.replace('mask'+'-data0','mask'+chr(92)+'u002ddata0')
def save(p,s):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(esc(s))
def js(p,o):save(p,json.dumps(o,indent=2)+'\n')
def git(*args):return subprocess.check_output(['git',*args],cwd=R)
def blob(p):return git('show',REF+':'+p)
def digest(root):
 h=hashlib.sha256()
 for p in sorted(root.rglob('*')):
  if p.is_file():h.update(str(p.relative_to(root)).encode()+b'\0'+p.read_bytes()+b'\0')
 return h.hexdigest()
def run(args,log,data=None):
 start=stamp();tic=time.monotonic();timed_out=False
 try:
  p=subprocess.run(args,cwd=R,input=data,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=180);out=p.stdout;rc=p.returncode
 except subprocess.TimeoutExpired as e:out=e.stdout or b'';rc=None;timed_out=True
 save(O/log,out.decode(errors='replace'))
 return out.decode(errors='replace'),dict(argv=args,start=start,elapsed_seconds=round(time.monotonic()-tic,3),rc=rc,timed_out=timed_out,output=log,output_sha256=hashlib.sha256((O/log).read_bytes()).hexdigest())
def attempt(plan,i,path,data,prefix,candidates,failed=None):
 rec=dict(plan=plan,index=i,path=path,patch_sha256=hashlib.sha256(data).hexdigest(),produced_at=stamp(),input_tree_sha256=digest(prefix))
 if failed is not None:
  rec.update(status='open item',blocked_by=failed,reason=f'blocked by failed predecessor {failed}',dry_rc=None,apply_rc=None,attempted=False,output_tree_sha256=None,promoted=False)
  js(O/f'rows/{plan}-{i:03d}.json',rec);return rec,prefix,failed
 candidate=candidates/f'{i:03d}';assert not candidate.exists();shutil.copytree(prefix,candidate)
 assert digest(candidate)==rec['input_tree_sha256']
 args=['patch','-p1','-N','--batch','--directory',str(candidate)]
 dryout,dry=run(args+['--dry-run'],f'logs/{plan}-{i:03d}.dry.out',data)
 rec.update(candidate=str(candidate),dry=dry,dry_rc=dry['rc'],after_dry_tree_sha256=digest(candidate),attempted=True)
 js(O/f'rows/{plan}-{i:03d}.json',rec)
 assert rec['input_tree_sha256']==rec['after_dry_tree_sha256'],'diagnostic changed candidate'
 out,apply=run(args,f'logs/{plan}-{i:03d}.apply.out',data)
 rec.update(apply=apply,apply_rc=apply['rc'],offset=out.count('offset'),fuzz=out.count('fuzz'),FAILED=out.count('FAILED'),output_tree_sha256=digest(candidate))
 good=apply['rc']==0 and not apply['timed_out'];rec['promoted']=good
 rec['status']='fails' if not good else 'fuzz' if rec['fuzz'] else 'applies with offset' if rec['offset'] else 'applies'
 assert digest(prefix)==rec['input_tree_sha256'],'candidate mutated prefix'
 js(O/f'rows/{plan}-{i:03d}.json',rec)
 return rec,candidate if good else prefix,None if good else i
started=stamp();runroot=T/'src'/('corrected-'+datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%dT%H%M%SZ'));assert not runroot.exists();runroot.mkdir()
meta=dict(start=started,source_ref=REF,coordinator=CO,runner_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),patch_version=subprocess.check_output(['patch','--version'],text=True),tar_version=subprocess.check_output(['tar','--version'],text=True),locale='C',scratch=str(runroot),identity='Codex / GPT-6-Astra / xhigh; observed live Herdr footer, not provider-attested; session 01a19d12-29e3-7fe0-9f41-038dac0a5deb')
js(O/'run-metadata.json',meta)
# Prove the real engine's failed-candidate path before producing trusted rows.
fixture=runroot/'failure-fixture';prefix=fixture/'prefix';prefix.mkdir(parents=True);(prefix/'a').write_text('alpha\n');(prefix/'b').write_text('beta\n');before=digest(prefix)
patch=b'--- a/a\n+++ b/a\n@@ -1 +1 @@\n-alpha\n+changed\n--- a/b\n+++ b/b\n@@ -1 +1 @@\n-not-the-input\n+changed\n'
r,after,failed=attempt('FIXTURE',1,'deliberately-failing-input',patch,prefix,fixture/'candidates');s,after2,failed2=attempt('FIXTURE',2,'blocked-successor',patch,after,fixture/'candidates',failed)
assert r['apply_rc']!=0 and not r['promoted'] and r['output_tree_sha256']!=before
assert after==prefix==after2 and digest(prefix)==before and s['status']=='open item' and not s['attempted'] and 'apply' not in s
js(O/'failed-candidate-guard.json',dict(result='PASS',prefix_before=before,prefix_after=digest(prefix),failure=r,successor=s));print('FAIL-first guard PASS: failed partial candidate retained; prefix unchanged; successor blocked',flush=True)
paths=(A/'stage-a/p1-qa-scratch/paths.txt').read_text().replace(chr(92)+'u002d','-').splitlines()
orders={d:(A/f'stage-a/order-{d}.txt').read_text().replace(chr(92)+'u002d','-').splitlines() for d in ['GENERIC_X64','H700','SM8550']}
for d in ['DDR3','DDR4']:orders['UBOOT-'+d]=[p for p in paths if f'/u-boot-{d}/' in p]
orders['FIRMWARE']=[p for p in paths if '/kernel-firmware/patches/' in p]
assert [len(x) for x in orders.values()]==[8,42,65,2,2,1] and len(set(p for ps in orders.values() for p in ps))==106
spec={
 'GENERIC_X64':('linux/linux-7.1.2.tar.xz','linux-7.1.2','37198c93727be247c9fb5309bb86cd5e496c61e5322cd8c4eca9476bb0b5883f','projects/ROCKNIX/packages/linux/package.mk'),
 'H700':('linux/linux-7.2.tar.xz','linux-7.2','f9fef3d14c0df53819026f4be74459835c2a0b0dcbf5b5bbd9ea19f0829402b3','projects/ROCKNIX/packages/linux/package.mk'),
 'SM8550':('linux/linux-7.2.tar.xz','linux-7.2','f9fef3d14c0df53819026f4be74459835c2a0b0dcbf5b5bbd9ea19f0829402b3','projects/ROCKNIX/packages/linux/package.mk'),
 'UBOOT-DDR3':('u-boot-DDR3/u-boot-DDR3-v2026.01.tar.gz','u-boot-2026.01','03bb43c58d2343ee48dd191e0f181f0108425b179d84519add3a977071c3f654','projects/ROCKNIX/devices/H700/packages/u-boot-DDR3/package.mk'),
 'UBOOT-DDR4':('u-boot-DDR4/u-boot-DDR4-v2026.01.tar.gz','u-boot-2026.01','03bb43c58d2343ee48dd191e0f181f0108425b179d84519add3a977071c3f654','projects/ROCKNIX/devices/H700/packages/u-boot-DDR4/package.mk'),
 'FIRMWARE':('kernel-firmware/kernel-firmware-20260309.tar.gz','linux-firmware-20260309','28fb1b57fa9531edbd001a2462068267f10622e613abd40f952344b3f1fc5a16','projects/ROCKNIX/packages/linux-firmware/kernel-firmware/package.mk')}
rows=[];tars=[];checks={}
def stripped(v):
 if v=='/dev/null':return None
 q=v.split('/',1)[1];assert q and '..' not in Path(q).parts and not q.startswith('/');return q
def targetinfo(raw):
 targets=set();created=set();old=None;new=None
 for line in raw.decode(errors='replace').splitlines():
  if line.startswith('--- '):
   bits=line[4:].split();old=bits[0] if bits else None
   if old and '/' in old and old!='/dev/null':targets.add(stripped(old))
  elif line.startswith('+++ '):
   bits=line[4:].split();new=bits[0] if bits else None
   if new and '/' in new and new!='/dev/null':
    targets.add(stripped(new))
    if old=='/dev/null':created.add(stripped(new))
  elif line.startswith('@@ -0,0 ') and new and new!='/dev/null':created.add(stripped(new))
 return targets,created
for plan,order in orders.items():
 arc,root,expected,recipe=spec[plan];archive=C/arc
 if arc not in checks:
  start=stamp();tic=time.monotonic();h=hashlib.sha256()
  with archive.open('rb') as f:
   for chunk in iter(lambda:f.read(1048576),b''):h.update(chunk)
  side=Path(str(archive)+'.sha256').read_text().split()[0]
  assert h.hexdigest()==side==expected and expected in blob(recipe).decode()
  checks[arc]=dict(sha256=h.hexdigest(),sidecar_equal=True,recipe=recipe,recipe_equal=True,start=start,elapsed_seconds=round(time.monotonic()-tic,3))
  js(O/'archive-sha256.json',checks)
 raw={p:blob(p) for p in order};targets=set();created=set()
 for data in raw.values():ts,cs=targetinfo(data);targets.update(ts);created.update(cs)
 pd=runroot/plan;initial=pd/'initial';initial.mkdir(parents=True)
 targetfile=pd/'targets.txt';targetfile.write_text('\n'.join(root+'/'+p for p in sorted(targets))+'\n')
 save(O/f'targets-{plan}.txt',targetfile.read_text());save(O/f'order-{plan}.txt','\n'.join(order)+'\n')
 args=['tar','--extract','--file',str(archive),'--directory',str(initial),'--no-same-owner','--no-same-permissions','--verbatim-files-from','--files-from',str(targetfile)]
 out,rec=run(args,f'tar-{plan}.out');missing=[l.split(': ',1)[1].rsplit(': Not found in archive',1)[0] for l in out.splitlines() if 'Not found in archive' in l]
 assert rec['rc'] in [0,2] and (rec['rc']==0 or missing)
 assert all(m.startswith(root+'/') and m[len(root)+1:] in created for m in missing),(plan,'missing member not patch-created',missing,created)
 assert all('Not found in archive' in l or 'Exiting with failure status' in l for l in out.splitlines())
 source=initial/root;source.mkdir(exist_ok=True)
 rec.update(plan=plan,targets=len(targets),not_in_archive=len(missing),missing_members=missing,created_paths=sorted(created),all_missing_accounted=True,initial_tree_sha256=digest(source),initial_tree=str(source));js(O/f'tar-{plan}.json',rec);tars.append(rec)
 prefix=source;failed=None;planrows=[]
 for i,p in enumerate(order,1):
  row,prefix,failed=attempt(plan,i,p,raw[p],prefix,pd/'candidates',failed);rows.append(row);planrows.append(row)
 save(O/f'applies-{plan}.txt','\n'.join(f'{r["plan"]} {r["index"]:03d} {r["path"]} dry_rc={r["dry_rc"]} apply_rc={r["apply_rc"]} offset={r.get("offset","NA")} fuzz={r.get("fuzz","NA")} FAILED={r.get("FAILED","NA")} status={r["status"]}'+(f' blocked_by={r["blocked_by"]}' if 'blocked_by' in r else '') for r in planrows)+'\n')
 print(plan,len(planrows),dict(collections.Counter(r['status'] for r in planrows)),flush=True)
 js(O/'application-results.json',dict(source_ref=REF,coordinator=CO,complete=False,rows=rows,tar=tars))
assert len(rows)==120 and len({r['path'] for r in rows})==106
special=next(r for r in rows if r['plan']=='H700' and r['index']==11);assert special['dry_rc']==1 and special['apply_rc']==0 and special['promoted']
meta['end']=stamp();js(O/'run-metadata.json',meta)
js(O/'application-results.json',dict(source_ref=REF,coordinator=CO,complete=True,rows=rows,tar=tars,counts=dict(collections.Counter(r['status'] for r in rows)),dry_apply_disagreements=[f'{r["plan"]}-{r["index"]:03d}' for r in rows if r['attempted'] and r['dry_rc']!=r['apply_rc']]))
print('COMPLETE 120 applications, 106 patch paths; H700 011 diagnostic failure/normal success retained',flush=True)

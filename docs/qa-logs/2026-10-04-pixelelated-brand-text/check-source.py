from pathlib import Path
import shutil,subprocess,tempfile,json
root=Path('/workspace/repos/rocknix.worktrees/conflict-resolution')
out=root/'docs/qa-logs/2026-10-04-pixelelated-brand-text'
meta='projects/ROCKNIX/packages/misc/modules/sources/gamelist.xml'
paths=['distributions/ROCKNIX/options','distributions/ROCKNIX/version','packages/linux/package.mk','projects/ROCKNIX/packages/linux/package.mk','projects/ROCKNIX/packages/rocknix/sources/scripts','projects/ROCKNIX/packages/rocknix/system.d/rocknix-report-stats.timer','projects/ROCKNIX/packages/ui/emulationstation/package.mk','docs/pixelelated/art/pixelelated-wordmark.svg','projects/ROCKNIX/packages/ui/themes/es-theme-art-book-next','LICENSE.md','TRADEMARK.md','NAMING.md',meta]
old=subprocess.check_output(['git','show','53d907dc5fb1260b032407c8bfa4e157d94288f3:'+meta],cwd=root)
results=[]
with tempfile.TemporaryDirectory(prefix='pixelelated-brand-controls-') as temp:
 t=Path(temp)
 for rel in paths:
  src=root/rel;dst=t/rel;dst.parent.mkdir(parents=True,exist_ok=True)
  if src.is_dir():shutil.copytree(src,dst,symlinks=True)
  elif src.is_symlink():dst.symlink_to(src.readlink())
  else:shutil.copy2(src,dst)
 for name,data,expected,why in [('original-XML',old,1,'FAIL Tools metadata is well-formed XML'),('old-player-text',old.replace(b'iOS 2 & 3',b'iOS 2 &amp; 3'),1,'FAIL Tools names and descriptions use the current identity'),('corrected',(root/meta).read_bytes(),0,'PASS Tools names and descriptions use the current identity')]:
  (t/meta).write_bytes(data)
  r=subprocess.run([str(root/'tools/rasteratops-identity-check'),'--tree',str(t),'--es','/home/max/Development/emulationstation-next.worktrees/qa-integration'],capture_output=True,text=True)
  (out/(name+'.log')).write_text(r.stdout+r.stderr)
  assert r.returncode==expected and why in r.stdout,(name,r.returncode,r.stdout[-300:])
  results.append({'case':name,'returncode':r.returncode,'expected_returncode':expected,'expected_diagnostic_observed':True})
  print('PASS',name,'returned',r.returncode,flush=True)
(out/'controls.json').write_text(json.dumps(results,indent=2)+'\n')

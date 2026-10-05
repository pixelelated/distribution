from pathlib import Path
import datetime,hashlib,json,shutil,subprocess
root=Path('/workspace/repos/rocknix.worktrees/conflict-resolution')
dest=root/'docs/qa-logs/2026-10-05-transfer-first-sample';dest.mkdir()
base=Path('/workspace/artifacts/rocknix-images/walk-baseline')
candidate=Path('/workspace/tmp/pixelelated-m7-qa-11/artifacts/rocknix-images/qa-cf511ce79b-webdav-a-20261005-0552/walks')
frozen=Path('/workspace/repos/rocknix.worktrees/m7-pixelelated-replacement09')
engine=frozen/'tools/frame-diff';masks=frozen/'tools/vm-walks/masks.txt'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def manifest(p):return {str(f.relative_to(p)):sha(f) for f in sorted(p.rglob('*')) if f.is_file()}
before=manifest(base);original=manifest(candidate)
claims=(root/'tools/vm-walks/claims.txt').read_text();line=next(x for x in claims.splitlines() if '#439' in x)
(dest/'current-claims.txt').write_text(claims)
(dest/'missing-claims.txt').write_text(claims.replace(line+'\n',''))
(dest/'narrow-claims.txt').write_text(claims.replace(line,line.replace('557 288 723 339','557 288 722 339')))
temp=Path('/tmp/pixelelated-transfer439-controls');temp.mkdir()
wrong=temp/'wrong-heading';missing=temp/'missing-frame'
shutil.copytree(candidate,wrong);shutil.copytree(candidate,missing)
# Negative control swaps an unrelated actual screen, not generated artwork.
shutil.copyfile(candidate/'restore-page/02-restore-page.png',wrong/'run-transfer-frames/07-t02.png')
(missing/'run-transfer-frames/07-t02.png').unlink()
results=[]
for name,tree,claim,expected in [('missing',candidate,'missing-claims.txt',1),
 ('narrow',candidate,'narrow-claims.txt',1),('current',candidate,'current-claims.txt',0),
 ('wrong-heading',wrong,'current-claims.txt',1),('missing-frame',missing,'current-claims.txt',1)]:
 with (dest/(name+'.log')).open('w') as stream:
  r=subprocess.run([str(engine),'compare',str(base),str(tree),'--masks',str(masks),'--claims',str(dest/claim),'--report',str(dest/(name+'.md'))],stdout=stream,stderr=subprocess.STDOUT)
 assert r.returncode==expected,(name,r.returncode)
 results.append({'name':name,'actual_rc':r.returncode,'expected_rc':expected})
assert manifest(base)==before and manifest(candidate)==original
for name,p in [('baseline-first.png',base/'run-transfer-frames/07-t02.png'),
 ('candidate-first.png',candidate/'run-transfer-frames/07-t02.png'),
 ('candidate-completed.png',candidate/'run-transfer-frames/22-t60.png')]:shutil.copyfile(p,dest/name)
data={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'passed':True,'results':results,
 'engine_sha256':sha(engine),'masks_sha256':sha(masks),'claims_sha256':sha(dest/'current-claims.txt'),
 'baseline_unchanged':True,'candidate_frames_unchanged':True,'baseline_manifest':before,
 'candidate_manifest':original,'scope':'Same78 original frames; no new VM, product changes or baseline replacement'}
(dest/'controls.json').write_text(json.dumps(data,indent=2)+'\n')
print(json.dumps({'passed':True,'results':results}))

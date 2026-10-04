#!/usr/bin/env python3
"""Replay actual VM frames and prove the limited #415 claims can fail."""
from pathlib import Path
import hashlib
import json
import shutil
import subprocess
import tempfile
from PIL import Image

ROOT=Path(__file__).resolve().parents[3]
OUT=Path(__file__).resolve().parent
BASE=Path('/workspace/artifacts/rocknix-images/walk-baseline')
RUN=Path('/workspace/tmp/pixelelated-m7-qa-01/artifacts/rocknix-images/qa-b137d8c373-webdav-a-20261004-0654/walks')
NAMES=('confirm-cloud-folder/03-folder-editor.png','confirm-cloud-folder/05-after-dismiss.png','to-change-cloud-folder/03-folder-editor.png')
def hashes(root):
    return {str(p.relative_to(root)):hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(root.rglob('*')) if p.is_file()}
before_base=hashes(BASE);before_run=hashes(RUN)
assert len(list(RUN.rglob('*.png')))==78
claims=(ROOT/'tools/vm-walks/claims.txt').read_text()
old=subprocess.check_output(['git','-C',str(ROOT),'show','b137d8c373:tools/vm-walks/claims.txt'],text=True)
checks=[]
with tempfile.TemporaryDirectory(prefix='pixelelated-folder-claims-') as tmp:
    temp=Path(tmp)
    def run(name,text,expected,frames=RUN):
        path=temp/(name+'.claims');path.write_text(text)
        p=subprocess.run([str(ROOT/'tools/frame-diff'),'compare',str(BASE),str(frames),'--masks',str(ROOT/'tools/vm-walks/masks.txt'),'--claims',str(path)],capture_output=True,text=True,timeout=60)
        (OUT/(name+'.log')).write_text(p.stdout+p.stderr)
        assert p.returncode==expected,(name,p.returncode)
        if expected==1: assert '**UNCLAIMED**' in p.stdout
        else: assert '**PASS**' in p.stdout
        checks.append({'case':name,'rc':p.returncode})
        print('PASS',name,'expected rc',expected)
    run('original-claims-fail',old,1)
    run('corrected-claims-pass',claims,0)
    missing='\n'.join(x for x in claims.splitlines() if not any(x.startswith('d72084ccad '+n+' ') for n in NAMES))+'\n'
    run('missing-claims-fail',missing,1)
    run('undersized-claims-fail',claims.replace('183 226 416 268','184 226 416 268'),1)
    # Construct a detector control on disposable copies, never real frames.
    mutated=temp/'unexpected';shutil.copytree(RUN,mutated)
    path=mutated/NAMES[0]
    with Image.open(path) as source:
        im=source.convert('RGB')
    for y in range(198,206):
        for x in range(600,608):
            r,g,b=im.getpixel((x,y));im.putpixel((x,y),(255-r,255-g,255-b))
    im.save(path)
    run('outside-text-fails',claims,1,mutated)
assert hashes(BASE)==before_base and hashes(RUN)==before_run
for kind,root in (('baseline',BASE),('candidate',RUN)):
    for name in NAMES:
        dst=OUT/kind/name;dst.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(root/name,dst)
(OUT/'proof.json').write_text(json.dumps({'checks':checks,'baseline_unchanged':True,'candidate_frames_unchanged':True,'screens':78,'baseline_files':before_base,'candidate_files':before_run},indent=2)+'\n')
print('PASS baseline and original78 frames remain byte-identical')

from pathlib import Path
import ast,hashlib,json,shutil,subprocess
repo=Path('/workspace/repos/rocknix.worktrees/m7-player-setup')
src=Path('/workspace/repos/rocknix.worktrees/m7-dolphin-preservation-581/docs/qa-logs/2026-10-14-dolphin-english640-source')
packet=repo/'docs/qa-logs/2026-10-14-dolphin-english640-source'
assert packet.is_dir()
subprocess.run(['sha256sum','-c','SHA256SUMS'],cwd=packet,check=True,stdout=subprocess.DEVNULL)
r=Path('/workspace/tmp/pix581-en640-prep-20261014-03');r.mkdir()
a=json.loads((packet/'allocation.example.json').read_text());a['run_id']='20261014en640layout03'
(r/'allocation.json').write_text(json.dumps(a,indent=2)+'\n')
cmd=['python3','-I','-S','-B',str(packet/'stage-input.py'),'--repo','/workspace/repos/rocknix.worktrees/m7-dolphin-preservation-581','--es-repo','/home/max/Development/emulationstation-next.worktrees/m7-rc-library-setup','--input',str(r/'input'),'--archive','/workspace/tmp/pix-m7-library-vm-20261013/records/dolphin-packaged-defaults.tar.gz','--receipt','/workspace/tmp/pix-m7-library-vm-20261013/records/dolphin-packaged-defaults.json','--allocation',str(r/'allocation.json')]
p=subprocess.run(cmd,capture_output=True,text=True,timeout=30);(r/'stage.stdout').write_text(p.stdout);(r/'stage.stderr').write_text(p.stderr);(r/'stage.rc').write_text(str(p.returncode)+'\n');assert p.returncode==0,p.stderr
shutil.copyfile('/workspace/tmp/pix-m7-library-build-20261013/scratch/emulationstation',r/'input/emulationstation');(r/'input/emulationstation').chmod(0o755)
provision='''from pathlib import Path
import hashlib,json,subprocess,time,shutil,os
s=Path('/tmp/pix-input');o=Path('/tmp/pix-output');record={'rc':1}
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def run(args):return subprocess.run(args,check=True,capture_output=True,text=True,timeout=20).stdout
try:
 assert sorted(p.name for p in Path('/sys/class/net').iterdir())==['lo']
 assert not any(line.split()[4]=='/usr/bin/emulationstation' for line in Path('/proc/self/mountinfo').read_text().splitlines())
 record['original_es_sha256']=sha(Path('/usr/bin/emulationstation'))
 run(['systemctl','stop','essway.service'])
 target=o/'emulationstation';shutil.copyfile(s/'emulationstation',target);target.chmod(0o755)
 expected='8752b5391ea8728c1a088d0a80e3776469692dda665e8f07f062fed3206263d2'
 assert sha(target)==expected and os.access(target,os.X_OK)
 run(['mount','--bind',str(target),'/usr/bin/emulationstation']);run(['mount','--make-private','/usr/bin/emulationstation'])
 run(['systemctl','start','essway.service'])
 for _ in range(35):
  p=subprocess.run(['curl','-fsS','--max-time','2','http://127.0.0.1:1234/isIdle'],capture_output=True,text=True,timeout=3)
  if p.returncode==0 and json.loads(p.stdout)==[True]:break
  time.sleep(1)
 else:raise RuntimeError('frontend not idle')
 pid=int(run(['pidof','emulationstation']).strip());assert sha(Path('/proc')/str(pid)/'exe')==expected
 record.update(rc=0,pid=pid,es_sha256=expected,mode=oct(target.stat().st_mode&0o777),catalog_sha256=sha(Path('/usr/config/locale/fr/LC_MESSAGES/emulationstation2.mo')),mountinfo=Path('/proc/self/mountinfo').read_text(),wayland=[str(p) for p in Path('/run/0-runtime-dir').glob('wayland-*') if p.is_socket()])
finally:
 (o/'provision-result.json').write_text(json.dumps(record,indent=2)+'\\n');print(json.dumps({k:v for k,v in record.items() if k!='mountinfo'}))
'''
ast.parse(provision);(r/'input/provision.py').write_text(provision)
files=[{'path':str(p),'destination':str(p.relative_to(r/'input')),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in sorted((r/'input').rglob('*')) if p.is_file()]
directories=[{'destination':str(x.relative_to(r/'input')),'mode':x.stat().st_mode&0o777} for x in sorted((r/'input').rglob('*')) if x.is_dir()]
(r/'inputs.json').write_text(json.dumps({'files':files,'directories':directories},indent=2)+'\n')
(r/'guest.sh').write_text('set -eu\npython3 -I -S -B /tmp/pix-input/provision.py\n')
owner=Path('/workspace/tmp/pix581-en640-vm-20261014-03')
subprocess.run(['python3','-I',str(repo/'docs/qa-logs/2026-10-14-independent-format-runtime/coordinator/pix-m7-new-vm.py'),'--owner',str(owner),'--inputs',str(r/'inputs.json'),'--guest-script',str(r/'guest.sh'),'--issue','581','--stage','dolphin-en640-layout','--guest-seconds','120','--vnc','127'],check=True)
f=owner/'vm-lifecycle.py';t=f.read_text();needle='  print(out,flush=True)\n';assert t.count(needle)==1
t=t.replace(needle,needle+'''  (r/'visual-ready.json').write_text(json.dumps({'pid':pid,'deadline':deadline,'phase':'provisioned; coordinator owns serial'},indent=2)+'\\n')
  print('EN640 VISUAL OWNER READY',flush=True)
  while not (r/'visual-result.json').exists():
   if (r/'abort').exists():raise RuntimeError('Coordinator aborted visual allocation')
   assert time.monotonic()<deadline, 'original lifecycle deadline'
   assert (Path('/proc')/str(pid)/'cmdline').read_bytes(),'guest exited'
   time.sleep(1)
  visual=json.loads((r/'visual-result.json').read_text());assert visual['original_batch_exit']==0 and visual['batch_session_alive'] is False and visual['reviewed_frames']==3
  # Coordinator has verified/restored the original frontend and removed its executable copy.
''')
needle2=" manifest={str(p.relative_to(payload)):sha(p) for p in payload.rglob('*') if p.is_file()};"
assert t.count(needle2)==1
fix=" for entry in sorted(inputs['directories'],key=lambda x:len(Path(x['destination']).parts),reverse=True):\n  relative=Path(entry['destination']);assert not relative.is_absolute() and '..' not in relative.parts\n  folder=payload/relative;assert folder.is_dir() and not folder.is_symlink();folder.chmod(entry['mode']);assert folder.stat().st_mode&0o777==entry['mode']\n"
t=t.replace(needle2,fix+needle2)
ast.parse(t);f.write_text(t)
plan=json.loads((owner/'retention-plan.json').read_text());plan['builds'][0]['basis']+=' Additive coordinator-owned visual handoff after provision; exact accepted singleton case, three reviewed frames and original batch exit required before completion, same900s lifecycle deadline. Directory modes are bound in inputs and preserved before mkfs, correcting failed owner01 staging.'
for row in plan['builds'][0]['evidence']:row['sha256']=hashlib.sha256(Path(row['path']).read_bytes()).hexdigest()
(owner/'retention-plan.json').write_text(json.dumps(plan,indent=2)+'\n')
print(json.dumps({'owner':str(owner),'staged_files':len(files),'stage_rc':p.returncode if hasattr(p,'returncode') else 0}))

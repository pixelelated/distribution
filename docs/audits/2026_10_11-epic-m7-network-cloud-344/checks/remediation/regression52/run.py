from pathlib import Path
import subprocess,os,json,hashlib,signal
D=Path('/workspace/repos/rocknix.worktrees/m7-cloud-connections');O=Path('/workspace/tmp/pix540-regression52');E=Path('/home/max/Development/emulationstation-next.worktrees/m7-cloud-connections')
R=Path('/workspace/repos/rocknix.worktrees/m7-pixelelated-replacement18/build.pixelelated-GENERIC_X64.x86_64/image/system')
files=list((D/'projects/ROCKNIX/packages/network/rclone/sources').glob('*'))+[D/'tools/last-good-scripts-test',E/'es-app/src/guis/GuiMenu.cpp',E/'es-app/src/CloudText.cpp']
manifest=[{'path':str(p),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in files if p.is_file()]
(O/'source-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
signal.signal(signal.SIGINT,signal.SIG_DFL)
env=dict(os.environ,QA_SYSTEM_ROOT=str(R),ES_SRC=str(E),TMPDIR=str(O/"fixtures"))
result=subprocess.run([str(D/'tools/last-good-scripts-test')],cwd=D,env=env).returncode
for row in manifest:assert hashlib.sha256(Path(row['path']).read_bytes()).hexdigest()==row['sha256']
(O/'result.json').write_text(json.dumps({'returncode':result,'inputs_unchanged':True,'candidate_system_root':str(R)},indent=2)+'\n')
raise SystemExit(result)

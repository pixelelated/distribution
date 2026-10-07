from pathlib import Path
import hashlib,json,subprocess
O=Path('/tmp/pixelelated-m7-migration-copy03'); OLD=Path('/tmp/pixelelated-m7-migration-copy02')
c=json.loads((OLD/'artifacts/commands.json').read_text());a=c['commands']['link_argv']
sysroot='/workspace/repos/rocknix.worktrees/m7-pixelelated-replacement16/build.pixelelated-GENERIC_X64.x86_64/toolchain/x86_64-rocknix-linux-gnu/sysroot'
a=[('-Wl,--dependency-file='+str(O/'link.d')) if t.startswith('-Wl,--dependency-file=') else t for t in a]
a[a.index('-o')+1]=str(O/'emulationstation');a.append('--sysroot='+sysroot)
(O/'artifacts/link-command.json').write_text(json.dumps(dict(cwd=c['cwd'],argv=a),indent=2)+'\n')
with open(O/'artifacts/link.log','w') as f:p=subprocess.run(a,cwd=c['cwd'],stdout=f,stderr=subprocess.STDOUT)
if p.returncode:raise SystemExit(p.returncode)
inputs=json.loads((OLD/'artifacts/inputs-before.json').read_text())
for d in inputs:
 assert hashlib.file_digest(open(d['path'],'rb'),'sha256').hexdigest()==d['sha256'],d['path']
(O/'artifacts/inputs-unchanged.json').write_text(json.dumps(inputs,indent=2)+'\n')
p=O/'emulationstation';out=dict(path=str(p),size=p.stat().st_size,sha256=hashlib.file_digest(open(p,'rb'),'sha256').hexdigest())
(O/'artifacts/output.json').write_text(json.dumps(out,indent=2)+'\n');print('PASS owner-local relink with explicit retained sysroot; all source/object/library inputs unchanged')

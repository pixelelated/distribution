#!/usr/bin/env python3
import json,pathlib,shutil,subprocess,sys
base=pathlib.Path('/workspace/tmp/pixelelated-510-coverage02')
root=pathlib.Path('/workspace/repos/rocknix.worktrees/conflict-resolution')
label=sys.argv[1];assert label.replace('-','').replace('_','').isalnum()
owner=base/('walk-'+label);owner.mkdir();(owner/'tools').mkdir()
for n in ['watch-build','watch-job']:shutil.copy2(root/'tools'/n,owner/'tools'/n)
(owner/'steps.txt').write_text(sys.stdin.read())
command=['python3',str(root/'tools/vm-visual-qa'),'--monitor','/tmp/pix512-mon.sock','run',str(owner/'steps.txt'),'--outdir',str(owner/'frames')]
import shlex
(owner/'run.sh').write_text('#!/bin/bash\nset -uo pipefail\nexport TMPDIR=/workspace/tmp\n'+shlex.join(command)+'\nrc=$?\nprintf "%s\\n" "$rc" > '+shlex.quote(str(owner/'inner.rc'))+'\nexit "$rc"\n')
(owner/'run.sh').chmod(0o755)
subprocess.run(['python3',str(root/'tools/watch-build-submit'),'--owner',str(owner),'--','--',str(owner/'run.sh')],cwd=owner,check=True)

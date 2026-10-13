from pathlib import Path
import subprocess,hashlib,json,difflib
r=Path(__file__).parent
repo='/workspace/repos/rocknix.worktrees/m7-player-setup'
p='projects/ROCKNIX/packages/network/cloud-signin-window/sources/cloud-signin-window.c'
s=subprocess.check_output(['git','-C',repo,'show','bc9dfe8141d9561dc1d8502313d00a84c4566ee8:'+p]).decode()
(r/'original.c').write_text(s)
new=s.replace('static const char *allowed_host = NULL;',(r/'instrument.c').read_text()+'\nstatic const char *allowed_host = NULL;')
new=new.replace('webkit_web_view_load_uri(view, argv[1]);','qa_setup(view);\n    webkit_web_view_load_uri(view, argv[1]);')
assert new!=s and new.count('qa_setup(view);')==1
(r/'diagnostic.c').write_text(new)
(r/'diagnostic.patch').write_text(''.join(difflib.unified_diff(s.splitlines(True),new.splitlines(True),fromfile='original.c',tofile='diagnostic.c')))
(r/'source.json').write_text(json.dumps({'source':'bc9dfe8141d9561dc1d8502313d00a84c4566ee8','path':p,'sha256':hashlib.sha256(s.encode()).hexdigest(),'diagnostic':hashlib.sha256(new.encode()).hexdigest()},indent=2)+'\n')

from pathlib import Path
import json,subprocess
r=Path(__file__).parent;ssh=json.loads((r/'ssh-command.json').read_text());result={}
for name,command in [('unshare','/usr/bin/unshare --help'),('mount','/usr/bin/mount --help'),('chroot','/usr/bin/chroot --help')]:
 p=subprocess.run(ssh+[command],capture_output=True,text=True,timeout=15);result[name]={'rc':p.returncode,'stdout':p.stdout,'stderr':p.stderr}
(r/'records/steam-installed-tool-help.json').write_text(json.dumps(result,indent=2)+'\n')

import sys
from pathlib import Path
sys.path.insert(0,'/tmp/pixelelated-508-ui01');from control import *
remote('systemctl stop essway')
cmd="""python3 - <<'PY2'
from pathlib import Path
import re
p=Path('/storage/.config/emulationstation/es_settings.cfg');s=p.read_text()
for k,v in [('Debug','true'),('UseOSK','false')]:
 s=re.sub(r'\\s*<bool name="'+k+r'"[^>]*/>', '', s)
 s=s.replace('</config>', '<bool name="'+k+'" value="'+v+'" />\\n</config>')
p.write_text(s)
PY2
mkdir -p /storage/qa-manual-ui/provider
: > /storage/.config/rclone/rclone.conf
nohup /usr/bin/rclone serve webdav /storage/qa-manual-ui/provider --addr 127.0.0.1:9867 > /storage/qa-manual-ui/provider.log 2>&1 < /dev/null &
echo $! > /storage/qa-manual-ui/provider.pid
sync
"""
remote(cmd);(A/'provider-owner.log').write_text(remote('cat /storage/qa-manual-ui/provider.pid; cat /proc/$(cat /storage/qa-manual-ui/provider.pid)/stat; curl -s -o /dev/null -w "%{http_code}" http://127.0.0.1:9867/'))
start('en_US');walk('640-en-cloud-hub', (R/'tools/vm-walks/to-manage-cloud-storage.steps').read_text())

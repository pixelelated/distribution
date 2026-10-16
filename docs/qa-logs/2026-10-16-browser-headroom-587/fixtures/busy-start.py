import subprocess,json,time,base64
from pathlib import Path
R=Path('/storage/qa587')
def run(a):
 p=subprocess.run(a,capture_output=True,text=True,timeout=25);row={'argv':a,'rc':p.returncode,'stdout':p.stdout,'stderr':p.stderr}
 with (R/'busy-actions.jsonl').open('a') as f:f.write(json.dumps(row)+'\n')
 assert p.returncode==0,row
 return p.stdout
run(['systemctl','stop','raofflineproxy.service'])
run(['ip','link','add','qa587dummy','type','dummy']);run(['ip','link','set','qa587dummy','up'])
(R/'peer-mode').write_text('slow\n')
run(['systemd-run','--unit=qa587-peer','--property=RuntimeMaxSec=180','--property=KillMode=control-group','/usr/bin/python3','-I','/storage/qa587/peer.py'])
time.sleep(.4);run(['systemctl','start','raofflineproxy.service'])
deadline=time.monotonic()+20
while time.monotonic()<deadline and not (R/'peer-award-entered.json').exists():time.sleep(.1)
assert (R/'peer-award-entered.json').exists(),'actual service did not enter synthetic award response'
print(json.dumps({'status':'in-flight','at':time.monotonic(),'interfaces':sorted(x.name for x in Path('/sys/class/net').iterdir()),'routes':run(['ip','route','show'])}))

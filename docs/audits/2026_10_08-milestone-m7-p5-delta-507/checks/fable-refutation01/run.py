import datetime,json,hashlib,subprocess,sys
from pathlib import Path
owner=Path(__file__).resolve().parent
root=Path.cwd()
command=json.loads((owner/'command.json').read_text())
seal=json.loads((owner/'input-seal.json').read_text())
def verify():
 return {p:hashlib.sha256((root/p).read_bytes()).hexdigest()==digest for p,digest in seal.items()}
assert subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip()==command['frozen_head']
before=verify();(owner/'input-before.json').write_text(json.dumps(before,indent=2)+'\n');assert all(before.values())
(owner/'call-start.json').write_text(json.dumps({'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'command':command['command']},indent=2)+'\n')
rc=subprocess.run(command['command']).returncode
(owner/'inner.rc').write_text(str(rc)+'\n')
after=verify();(owner/'input-after.json').write_text(json.dumps(after,indent=2)+'\n')
outer=rc if all(after.values()) else 97
(owner/'outer.rc').write_text(str(outer)+'\n')
(owner/'call-result.json').write_text(json.dumps({'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'rc':rc,'outer_rc':outer,'inputs_unchanged':all(after.values())},indent=2)+'\n')
sys.exit(outer)

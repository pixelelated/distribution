import datetime,json,subprocess,sys
from pathlib import Path
o=Path(__file__).resolve().parent;rows=[]
for i,cmd in enumerate(json.loads((o/'commands.json').read_text()),1):
 with (o/f'command-{i:02d}.log').open('w') as log:r=subprocess.run(cmd,stdout=log,stderr=subprocess.STDOUT)
 rows.append(dict(command=cmd,rc=r.returncode,log=f'command-{i:02d}.log'));print(i,r.returncode,cmd[0],flush=True)
(o/'results.json').write_text(json.dumps(dict(utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),results=rows),indent=2)+'\n');sys.exit(int(any(r['rc'] for r in rows)))

from pathlib import Path
import subprocess
r=Path(__file__).parent
for cmd in [['capability-prepare.py'],['capability-case.py','capability-gc-en640','en_US','gc-auto']]:
 p=subprocess.run(['python3',str(r/cmd[0]),*cmd[1:]],timeout=180)
 if p.returncode:raise SystemExit(p.returncode)

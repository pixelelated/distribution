"""Bounded read-only continuation status; does not infer process exits."""
from pathlib import Path
import json
base=Path('/workspace/tmp')
seq=base/'pixelelated-m7-sm8550-sequence-04'
def show(path,limit=6500):
    print('\n'+str(path))
    if path.is_file():
        data=path.read_text()
        print(data if len(data)<=limit else data[:limit]+'\n[truncated; inspect source for full record]')
    else:
        print('NOT PRESENT; absence alone does not establish completion or failure')
for name in ['state.json','controller-start.json','controller-result.json']:
    show(seq/name)
for kind in ['build','acceptance']:
    owner=base/('pixelelated-m7-sm8550-'+kind+'-04')
    runfile=owner/'run.path'
    if runfile.is_file():
        run=Path(runfile.read_text().strip())
        show(run/'build.status')
        show(run/'build.rc')
    for name in ['launcher-result.json','owner-verification.json','artifacts/acceptance.json']:
        if kind=='build' and name=='artifacts/acceptance.json':continue
        show(owner/name)
print('\nNo /proc inference performed. Use host-namespace execution for PID/container checks;')
print('sandbox-invisible PIDs are UNKNOWN, not exited. Do not launch a duplicate.')

#!/usr/bin/env python3
# Reproduce only T5 immutable record comparisons, never a lane producer/gate.
import os,pathlib,subprocess,json,datetime
p=pathlib.Path(__file__).resolve().parent
assert set(os.sched_getaffinity(0))==set(range(8,24))
runs=[]
for name in ['inspect-records.py','reconcile-core.py','reconcile-cleanup.py','reconcile-bindings.py','reconcile-supplement.py']:
 argv=['python3',str(p/name)]
 start=datetime.datetime.now(datetime.timezone.utc).isoformat()
 r=subprocess.run(argv,cwd=p,capture_output=True)
 runs.append({'argv':argv,'start':start,'rc':r.returncode})
 print(name,'rc',r.returncode)
 if r.returncode:
  print(r.stderr.decode());break
(p/'reproducer-runs.json').write_text(json.dumps(runs,indent=2)+'\n')
raise SystemExit(runs[-1]['rc'])

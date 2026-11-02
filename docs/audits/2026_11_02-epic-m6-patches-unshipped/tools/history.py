#!/usr/bin/env python3
import datetime,json,pathlib,subprocess,hashlib
R=pathlib.Path(__file__).resolve().parents[1];S='afdec2bf8b88135befcb7ec56efb3a7ea327bd73';rows=json.loads((R/'stage-b/observations.json').read_text());paths=[r['path'] for r in rows];cmd=['git','log','--format=COMMIT %H %aI %an <%ae> %s','--name-only',S,'--',*paths];p=subprocess.run(cmd,stdout=subprocess.PIPE,stderr=subprocess.PIPE);(R/'stage-b/path-history.stdout').write_bytes(p.stdout);(R/'stage-b/path-history.stderr').write_bytes(p.stderr);assert p.returncode==0
latest={};current=None
for l in p.stdout.decode().splitlines():
 if l.startswith('COMMIT '):current=l[7:]
 elif l in paths and l not in latest:latest[l]=current
assert len(latest)==432,len(latest)
(R/'stage-b/path-history.json').write_text(json.dumps({'at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'argv':cmd,'exit':p.returncode,'stdout_sha256':hashlib.sha256(p.stdout).hexdigest(),'latest_recorded_change':latest,'limit':'Distribution Git attribution only; original patch author, upstream adoption and rationale are not inferred from a committer.'},indent=2)+'\n')
print('Bound latest distribution history for all432 native paths; committer is not automatically original patch author.')

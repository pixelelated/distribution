#!/usr/bin/env python3
"""Coordinator: execute only synthetic-root controls in allocated disposable VM."""
import argparse,base64,hashlib,json,subprocess,sys
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('--source',type=Path,required=True);p.add_argument('--owner',type=Path,required=True);p.add_argument('--serial',required=True);a=p.parse_args()
files={n:(a.source/n).read_bytes() for n in ('pixelelated-state-check','pixelelated-state-check-test')}
data={n:base64.b64encode(b).decode() for n,b in files.items()}
guest='''import base64,json,subprocess,tempfile,time
from pathlib import Path
files=FILES
start=time.monotonic()
with tempfile.TemporaryDirectory(prefix="pix565-runtime-") as d:
 for n,b in files.items():
  p=Path(d)/n;p.write_bytes(base64.b64decode(b));p.chmod(0o700)
 r=subprocess.run(["python3","-B",str(Path(d)/"pixelelated-state-check-test"),"--self-test"],capture_output=True,timeout=120)
 try: report=json.loads(r.stdout)
 except Exception: report={"status":"invalid-json"}
 print(json.dumps({"schema":1,"guest_rc":r.returncode,"stderr_empty":not bool(r.stderr),"seconds":time.monotonic()-start,"report":report}))
print("PIX_CONTROLS_565_DONE")
'''.replace('FILES',repr(data))
script=a.owner/'controls.sh';script.write_text("#!/bin/sh\npython3 -B - <<'PY'\n"+guest+"\nPY\n")
r=subprocess.run([str(a.source/'vm-serial'),'--socket',a.serial,'--timeout','150','script',str(script)],capture_output=True,timeout=160)
(a.owner/'controls.serial').write_bytes(r.stdout)
assert r.returncode==0 and not r.stderr and r.stdout.count(b'PIX_CONTROLS_565_DONE')==1
report=json.loads(next(line for line in r.stdout.decode().splitlines() if line.startswith('{')))
report['source']={n:hashlib.sha256(b).hexdigest() for n,b in files.items()}
(a.owner/'controls-result.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({k:v for k,v in report.items() if k not in ('report','source')}))
print(json.dumps({'status':report['report'].get('status'),'control_count':report['report'].get('control_count')}))
sys.exit(0 if report['guest_rc']==0 and report['stderr_empty'] and report['report'].get('status')=='pass' else 2)

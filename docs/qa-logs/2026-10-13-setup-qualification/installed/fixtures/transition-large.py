from pathlib import Path
import subprocess,json,time
r=Path(__file__).parent
assert json.loads((r/'wifi-routes-en64002-owner/launcher-result.json').read_text())['runner_returncode']==0
assert not (r/'ready-1280x800.json').exists()
(r/'finish-640x480').touch(exist_ok=False)
end=time.monotonic()+300
while not (r/'ready-1280x800.json').exists():
 if (r/'vm-result.json').exists():raise RuntimeError('VM lifecycle ended before larger profile')
 if time.monotonic()>end:raise TimeoutError('larger profile did not start')
 time.sleep(1)
p=subprocess.run(['timeout','1550','python3',str(r/'large-batch.py')])
(r/'transition-large-result.json').write_text(json.dumps({'rc':p.returncode,'ended':time.time()},indent=2)+'\n')
if p.returncode==0:(r/'finish-1280x800').touch(exist_ok=False)
raise SystemExit(p.returncode)

from pathlib import Path
import os,json,tempfile,time,datetime
O=Path('/workspace/tmp/pixelelated-m7-sm8550-refresh-04')
assert os.getuid()==1000 and os.getgid()==1000
assert os.environ.get('TMPDIR')=='/tmp'
with tempfile.NamedTemporaryFile(dir=os.environ['TMPDIR']) as f:
    f.write(b'container-temporary-proof');f.flush();f.seek(0);assert f.read()==b'container-temporary-proof'
(O/'artifacts/container-runtime.json').write_text(json.dumps({'result':'PASS','utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'uid':os.getuid(),'gid':os.getgid(),'TMPDIR':os.environ['TMPDIR'],'actual_temporary_write_read':True},indent=2)+'\n')
for _ in range(180):
    p=O/'artifacts/container-gate.json'
    if p.exists():
        assert json.loads(p.read_text())['result']=='PASS';break
    time.sleep(1)
else:raise SystemExit('container identity observer did not grant the build gate')
print('PASS actual container temporary write/read and verified launch identity',flush=True)

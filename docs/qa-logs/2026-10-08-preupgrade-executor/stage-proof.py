import pathlib,subprocess,tarfile,json,hashlib,base64,zlib,shlex,datetime
P=pathlib.Path;O=P('/workspace/tmp/pixelelated-m7-alignment-executor-06')
assert json.loads((O/'launcher-result.json').read_text())['runner_returncode']==0
with tarfile.open(O/'artifacts/results.tar.gz') as t:
 plan=t.extractfile('qa519-operation/plan.json').read()
files={n:{'bytes':base64.b64encode(data).decode(),'sha256':hashlib.sha256(data).hexdigest()} for n,data in [('plan.json',plan),('operation.py',(O/'operation.py').read_bytes()),('inspect.py',(O/'inspect.py').read_bytes())]}
payload=base64.b64encode(zlib.compress(json.dumps(files).encode(),9)).decode()
source=P('/tmp/m7-519-stage-template.py').read_text()
code=source.replace('PAYLOAD',repr(payload)).replace('STAGE_NAME',repr('pixelelated-owner-519-input-synthetic-proof'))
ssh=['ssh','-i',str(O/'qa-key'),'-p','10252','-o','LogLevel=ERROR','-o','StrictHostKeyChecking=no','-o','UserKnownHostsFile=/dev/null','root@127.0.0.1']
cmd='python3 -I -B -c '+shlex.quote(code)
p=subprocess.run(ssh+[cmd],capture_output=True);assert p.returncode==0,p.stderr
q=subprocess.run(ssh+[cmd],capture_output=True);assert q.returncode==1
read='python3 -I -B -c '+shlex.quote("import pathlib,json,hashlib; p=pathlib.Path('/storage/.cache/pixelelated-owner-519-input-synthetic-proof'); print(json.dumps({x.name:{'mode':x.stat().st_mode&0o777,'sha256':hashlib.sha256(x.read_bytes()).hexdigest()} for x in p.iterdir()}))")
a=json.loads(subprocess.check_output(ssh+[read]));assert set(a)==set(files)
assert all(a[n]['sha256']==files[n]['sha256'] and a[n]['mode']==0o600 for n in files)
(O/'artifacts/staging-proof.json').write_text(json.dumps({'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'stage_rc':p.returncode,'repeat_refusal_rc':q.returncode,'all_staged_hashes_match':True,'all_staged_modes':384,'template_sha256':hashlib.sha256(source.encode()).hexdigest(),'scope':'synthetic binding and packet only; no owner paths/data imported'},indent=2)+'\n')
print('PASS same staging template preserves hashes/private modes and refuses occupied destination')

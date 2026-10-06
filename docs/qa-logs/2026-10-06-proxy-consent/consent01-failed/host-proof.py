from pathlib import Path
import subprocess,time,json,hashlib,tarfile,io
owner=Path('/workspace/tmp/pixelelated-m7-consent-01');out=owner/'artifacts'
ssh=['ssh','-i',str(owner/'pair/qa-key'),'-p','10026','-o','BatchMode=yes','-o','ConnectTimeout=8','-o','StrictHostKeyChecking=no','-o','UserKnownHostsFile=/dev/null','-o','LogLevel=ERROR','root@127.0.0.1']
def guest(cmd,**kw):return subprocess.run(ssh+[cmd],check=True,**kw)
for i in range(40):
 if subprocess.run(ssh+['true'],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL).returncode==0:break
 time.sleep(2)
else:raise RuntimeError('guest did not authenticate')
bid=guest('sed -n "s/^BUILD_ID=//p" /etc/os-release',capture_output=True,text=True).stdout.strip().strip('"')
assert bid=='55d8ee8f75965a560f75d187e34c9beaa93133f1'
guest('systemctl stop essway raofflineproxy; ip -4 route del default; ip -6 route del default 2>/dev/null || true')
guest('cat > /storage/.cache/consent-test.py',input=(owner/'consent-test.py').read_bytes())
result=subprocess.run(ssh+['python3 -I /storage/.cache/consent-test.py --output /storage/.cache/consent-proof-01 --expected-build '+bid],text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=240)
(out/'guest.log').write_text(result.stdout);print(result.stdout,flush=True)
archive=guest('cd /storage/.cache/consent-proof-01 && tar -cf - ./*.json ./*.log',capture_output=True).stdout
(out/'results.tar').write_bytes(archive)
with tarfile.open(fileobj=io.BytesIO(archive)) as tf:
 for member in tf.getmembers():
  name=member.name.removeprefix('./')
  assert member.isfile() and '/' not in name and name.endswith(('.json','.log'))
  (out/name).write_bytes(tf.extractfile(member).read())
assert result.returncode==0,result.returncode
summary=json.loads((out/'summary.json').read_text());assert summary['checks']==30
image=Path('/workspace/repos/rocknix.worktrees/m7-pixelelated-replacement12/build.pixelelated-GENERIC_X64.x86_64/image/system')
modules={}
for p in out.glob('*-result.json'):
 for name,expected in json.loads(p.read_text())['installed_modules'].items():
  assert name.startswith('/usr/lib/') and '..' not in Path(name).parts
  assert hashlib.sha256((image/name.lstrip('/')).read_bytes()).hexdigest()==expected,name
  modules[name]=expected
(out/'provenance.json').write_text(json.dumps({'build_id':bid,'checked_result_files':len(list(out.glob('*-result.json'))),'assembled_module_hashes':modules,'external_provider_contact':False,'scope':'Actual installed reporting functions with synthetic state and loopback HTTP; scheduler/UI timing not claimed'},indent=2)+'\n')
print('PASS 30 installed consent/restart cases and assembled module hashes',flush=True)

from pathlib import Path
import subprocess,time,json,hashlib
owner=Path('/workspace/tmp/pixelelated-m7-proxy-12');out=owner/'artifacts';seed=Path('/tmp/m7-proxy-predecessor')
ssh=['ssh','-i',str(owner/'pair/qa-key'),'-p','10026','-o','BatchMode=yes','-o','ConnectTimeout=8','-o','StrictHostKeyChecking=no','-o','UserKnownHostsFile=/dev/null','-o','LogLevel=ERROR','root@127.0.0.1']
assert hashlib.sha256((seed/'store.sqlite3').read_bytes()).hexdigest()=='a796c1e6ce6373a6620dfa983e16de3012b6d8feb83f9a2c178f437d8c0adca5'
def guest(cmd,**kw):return subprocess.run(ssh+[cmd],check=True,**kw)
for i in range(40):
 if subprocess.run(ssh+['true'],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL).returncode==0:break
 time.sleep(2)
else:raise RuntimeError('guest d did not authenticate')
bid=guest('sed -n "s/^BUILD_ID=//p" /etc/os-release',capture_output=True,text=True).stdout.strip().strip('"')
assert bid=='55d8ee8f75965a560f75d187e34c9beaa93133f1',bid
print('PASS exact pixelelated replacement12 BUILD_ID',flush=True)
# Execute upstream hashing tests against installed modules/library, never a source override.
native='/storage/.cache/pixelelated-native-12'
guest('mkdir -p '+native+'/fixtures')
for src,dst in [(owner/'native-test.py','test.py'),(owner/'native-runner.py','run.py'),(owner/'legacy-chd.py','legacy-chd.py')]+[(p,'fixtures/'+p.name) for p in sorted((owner/'native-fixtures').iterdir())]:
 guest('cat > '+native+'/'+dst,input=src.read_bytes())
nr=subprocess.run(ssh+['python3 '+native+'/run.py'],text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=180)
(out/'native-tests.log').write_text(nr.stdout);print(nr.stdout,flush=True)
rr=guest('cat '+native+'/result.json',capture_output=True);(out/'native-result.json').write_bytes(rr.stdout);result=json.loads(rr.stdout)
expected=Path('/workspace/repos/rocknix.worktrees/m7-pixelelated-replacement12/build.pixelelated-GENERIC_X64.x86_64/image/system/usr/lib/libraproxy_rchash.so')
assert result['library_sha256']==hashlib.sha256(expected.read_bytes()).hexdigest()
assert nr.returncode==0 and result['skipped']==0,result

guest('systemctl stop essway raofflineproxy; . /etc/profile >/dev/null 2>&1; set_setting cloudsaves.startup 0; set_setting cloudsaves.gameexit 0; set_setting global.retroachievements 0; set_setting global.retroachievements.username QA; set_setting global.retroachievements.token "<synthetic>"; ip route del default; mkdir -p /storage/.cache/pixelelated-m7-proxy-08/image_cache/static/Badge')
for src,dst in [(seed/'store.sqlite3','proxy.sqlite3'),(seed/'before.json','before.json'),(seed/'static/Badge/old.png','image_cache/static/Badge/old.png'),(owner/'guest-proof.py','guest-proof.py')]:
 guest('cat > /storage/.cache/pixelelated-m7-proxy-08/'+dst,input=src.read_bytes())
r=subprocess.run(ssh+['python3 /storage/.cache/pixelelated-m7-proxy-08/guest-proof.py'],text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=150)
(out/'guest-proof.log').write_text(r.stdout);print(r.stdout,flush=True)
for name in ['assertions.json']:
 r2=guest('cat /storage/.cache/pixelelated-m7-proxy-08/'+name,capture_output=True);(out/name).write_bytes(r2.stdout)
assert r.returncode==0,r.returncode
(out/'provenance.json').write_text(json.dumps({'build_id':bid,'predecessor_db_sha256':hashlib.sha256((seed/'store.sqlite3').read_bytes()).hexdigest(),'packaged_modules':True,'provider_contact':False},indent=2)+'\n')

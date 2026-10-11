from pathlib import Path
import subprocess,json,hashlib,shlex
p=Path(__file__).resolve().parent
def guest(code,timeout=120):return subprocess.check_output(['/workspace/repos/rocknix/tools/vm-pair','ssh','a',code],text=True,timeout=timeout)
def put(src,dst):subprocess.run(['/workspace/repos/rocknix/tools/vm-pair','scp','a',str(src),dst],check=True)
before=json.loads((p/'artifacts/seed-old.json').read_text())
for name,v in before['files'].items():
 if name.endswith('proxy.sqlite3'):continue # SQLite is proved by logical reopen below.
 actual=guest('sha256sum '+shlex.quote(name)).split()[0];assert actual==v['sha256'],name
 assert guest('stat -c %a '+shlex.quote(name)).strip()==v['mode'][2:],name
print('PASS retained settings, private modes and predecessor proxy payload through real update',flush=True)
root='/storage/.cache/pixelelated-installed-19';native='/storage/.cache/pixelelated-native-19'
guest('mkdir -p '+root+' '+native+'/fixtures')
for src,dst in [(p/'native-test.py','test.py'),(p/'native-runner.py','run.py'),(p/'legacy-chd.py','legacy-chd.py')]+[(f,'fixtures/'+f.name) for f in sorted((p/'native-fixtures').iterdir())]:put(src,native+'/'+dst)
q=subprocess.run(['/workspace/repos/rocknix/tools/vm-pair','ssh','a','python3 '+native+'/run.py --tests '+native+'/test.py --legacy-chd '+native+'/legacy-chd.py --library-sha256 6c484a2947a5f2a7c187e60dd93de73593d5fa98d57309bfb4b5f07bf390220d --output '+native+'/result.json'],text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=180)
(p/'artifacts/native.log').write_text(q.stdout);q.check_returncode()
nr=json.loads(guest('cat '+native+'/result.json'));assert nr['library_sha256']==hashlib.sha256(Path('/workspace/tmp/pixelelated-m7-image19/root/usr/lib/libraproxy_rchash.so').read_bytes()).hexdigest()
(p/'artifacts/native-result.json').write_text(json.dumps(nr,indent=2)+'\n');print('PASS installed native hashing formats and legacy CHD',flush=True)
# All network-dependent tests precede this boundary. Connected local provider
# subnet remains reachable, but the synthetic RA account can reach loopback only.
guest('systemctl stop essway.service raofflineproxy.service; . /etc/profile >/dev/null 2>&1; set_setting global.retroachievements 0; set_setting global.retroachievements.username QA; set_setting global.retroachievements.token "<synthetic>"; ip -4 route del default; ip -6 route del default 2>/dev/null || true')
assert not guest('ip -4 route show default; ip -6 route show default').strip()
put(p/'guest-proof.py',root+'/guest-proof.py')
q=subprocess.run(['/workspace/repos/rocknix/tools/vm-pair','ssh','a','python3 '+root+'/guest-proof.py'],text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=180)
(p/'artifacts/proxy-service.log').write_text(q.stdout);q.check_returncode()
(p/'artifacts/proxy-service-assertions.json').write_text(guest('cat /storage/.config/raofflineproxy/assertions.json'))
put(p/'consent-test.py',root+'/consent-test.py')
q=subprocess.run(['/workspace/repos/rocknix/tools/vm-pair','ssh','a','python3 '+root+'/consent-test.py --expected-build a0f60255abfefaddce772d0bba29977bafb7adab --output /storage/.cache/pixelelated-consent19'],text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=300)
(p/'artifacts/consent.log').write_text(q.stdout);q.check_returncode()
print('PASS actual installed service retains offline queue and reports only with consent',flush=True)
(p/'artifacts/installed-result.json').write_text(json.dumps({'passed':True,'source_overlays':False,'proxy_routes':'both default routes absent; synthetic upstream and reporting collector on loopback','retained_payloads':True,'connection_module':'/usr/bin/cloud_connections.py','rclone_version':guest('rclone version | head -1').strip()},indent=2)+'\n')

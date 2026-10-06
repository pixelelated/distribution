"""Run the installed whole-library proof in one already-created disposable guest."""
from pathlib import Path
import datetime,hashlib,json,shlex,subprocess,sys

owner=Path(__file__).resolve().parent
ssh=['ssh','-i',str(owner/'pair/qa-key'),'-p','10026','-o','BatchMode=yes','-o','ConnectTimeout=8','-o','StrictHostKeyChecking=no','-o','UserKnownHostsFile=/dev/null','-o','LogLevel=ERROR','root@127.0.0.1']
def guest(cmd,check=True,data=None):
 return subprocess.run(ssh+[cmd],input=data,text=True,capture_output=True,check=check)
expected=json.loads((owner/'installed-proxy-sha256.json').read_text())
def identity(label):
 code='from pathlib import Path\nimport hashlib,json\npaths='+repr(list(expected))+'\nprint(json.dumps({p:hashlib.sha256(Path(p).read_bytes()).hexdigest() for p in paths}))\n'
 actual=json.loads(guest("python3 - <<'IDENTITY'\n"+code+"\nIDENTITY").stdout)
 assert actual==expected,'installed helper, module or native hasher bytes changed'
 (owner/'artifacts'/('installed-'+label+'.json')).write_text(json.dumps(actual,indent=2)+'\n')

assert guest("sed -n 's/^BUILD_ID=//p' /etc/os-release").stdout.strip().strip('"')=='ed5a6a51f5974deec8748fbf0dbd2f4984b690f5'
guest('. /etc/profile >/dev/null 2>&1; test -z "$(get_setting global.retroachievements.username)"')
guest('systemctl stop essway; systemctl stop raofflineproxy')
guest('ip route del default')
assert not guest('ip -4 route show default').stdout.strip()
identity('before')
guest('mkdir -p /storage/.cache/m7-whole-library-run; cat > /storage/.cache/m7-whole-library-run/proof.py',data=(owner/'whole-library-installed.py').read_text())
result=1
try:
 with (owner/'artifacts/installed-library.log').open('x') as log:
  child=subprocess.Popen(ssh+['python3 -u /storage/.cache/m7-whole-library-run/proof.py'],text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
  (owner/'artifacts/ssh-proof.pid').write_text(str(child.pid)+'\n')
  for line in child.stdout:
   log.write(line);log.flush();print(line,end='',flush=True)
  result=child.wait()
finally:
 # Retain synthetic reports/logs only, never generated keys or database credentials.
 listing=guest("find /storage/.cache/m7-whole-library-15 -type f \\( -name '*.log' -o -name '*requests.json' -o -name 'assertions.json' -o -name 'pacing.json' -o -name '*.pid' \\)",check=False)
 base=Path('/storage/.cache/m7-whole-library-15')
 for raw in listing.stdout.splitlines():
  remote=Path(raw);relative=remote.relative_to(base)
  output=owner/'artifacts/guest'/relative;output.parent.mkdir(parents=True,exist_ok=True)
  output.write_text(guest('cat '+shlex.quote(str(remote))).stdout)
 identity('after')
 assert not guest('ip -4 route show default').stdout.strip(),'guest gained a default route'
 live=guest("pgrep -f '^/usr/bin/python3 /usr/bin/raofflineproxy-cache-indexed'",check=False)
 assert live.returncode==1,'installed caching helper survived completion'
 (owner/'artifacts/result.json').write_text(json.dumps({'verified_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'guest_returncode':result,'installed_files':len(expected),'installed_bytes_unchanged':True,'no_default_route':True,'helper_exited':True,'scope':'installed actual helper, native hashing, local HTTP and production timers; no hosted account, award or OAuth claim'},indent=2)+'\n')
assert result==0,'installed proof failed; retained guest reports are authoritative'

"""Exercise the actual installed update watcher and CLI during a guest capture."""
from pathlib import Path
from http.server import BaseHTTPRequestHandler,HTTPServer
import datetime,hashlib,json,shlex,subprocess,sys,threading,time
owner=Path(__file__).resolve().parent;label=sys.argv[1]
ssh=['ssh','-i','/workspace/tmp/pixelelated-m7-qa-19/pair/qa-key','-p','10026','-o','BatchMode=yes','-o','ConnectTimeout=8','-o','StrictHostKeyChecking=no','-o','UserKnownHostsFile=/dev/null','-o','LogLevel=ERROR','root@127.0.0.1']
def guest(command,check=True,data=None):
 return subprocess.run(ssh+['. /etc/profile >/dev/null 2>&1; '+command],input=data,text=True,capture_output=True,check=check,timeout=90)
assert guest("sed -n 's/^BUILD_ID=//p' /etc/os-release").stdout.strip().strip('"')=='ed5a6a51f5974deec8748fbf0dbd2f4984b690f5'
expected=json.loads((owner/'network-inputs.json').read_text())
def identity():
 result={}
 for path,digest in expected.items():
  value=guest('sha256sum '+shlex.quote(path)).stdout.split()[0];assert value==digest,(path,value);result[path]=value
 return result
before=identity();started=datetime.datetime.now(datetime.timezone.utc).isoformat()
guest('systemctl stop essway; set_setting updates.enabled 1; set_setting updates.force 1; set_setting global.retroachievements 0; set_setting cloudsaves.startup 0; set_setting cloudsaves.gameexit 0')
guest("python3 - <<'DEBUG'\nfrom pathlib import Path\nimport re\np=Path('/storage/.emulationstation/es_settings.cfg');s=p.read_text();s=re.sub(r'<bool name=\"Debug\" value=\"[^\"]*\"\\s*/>', '',s);entry='\\n<bool name=\"Debug\" value=\"true\" />\\n';s=s.replace('</config>',entry+'</config>') if '</config>' in s else s+entry;p.write_text(s)\nDEBUG")
guest('systemctl start essway')
log=''
for _ in range(60):
 log=guest("grep -E 'NetworkThread : Starting|CheckUpdatesComponent : Checking|ApiSystem::canUpdate|NetworkThread : No update found' /var/log/es_log.txt",check=False).stdout
 if all(x in log for x in ['NetworkThread : Starting','CheckUpdatesComponent : Checking for updates','ApiSystem::canUpdate','NetworkThread : No update found']):break
 time.sleep(1)
else:raise AssertionError('actual installed forced update watcher was not observed')
checks=[]
for args,expected_rc in [('check',1),('--help',0),('',1)]:
 result=guest('/usr/bin/rocknix-update '+args,check=False)
 assert result.returncode==expected_rc
 if args!='check':assert 'This version uses manual updates.' in result.stdout and 'https://github.com/pixelelated/distribution/releases' in result.stdout
 else:assert not result.stdout
 checks.append({'arguments':args,'returncode':result.returncode,'stdout':result.stdout})
observed=[]
class Positive(BaseHTTPRequestHandler):
 def log_message(self,*args):pass
 def do_GET(self):
  assert self.path=='/pixelelated-network-positive-control'
  observed.append(self.path);body=b'capture-positive-control\n';self.send_response(200);self.send_header('Content-Length',str(len(body)));self.end_headers();self.wfile.write(body)
server=HTTPServer(('127.0.0.1',9045),Positive);thread=threading.Thread(target=server.serve_forever,daemon=True);thread.start()
try:
 assert guest("curl --noproxy '*' -fsS --max-time 10 http://10.0.2.2:9045/pixelelated-network-positive-control").stdout=='capture-positive-control\n'
 assert len(observed)==1
finally:server.shutdown();server.server_close();thread.join(timeout=5)
assert not thread.is_alive()
assert identity()==before
settings=guest('printf "%s %s" "$(get_setting updates.enabled)" "$(get_setting updates.force)"').stdout.strip();assert settings=='1 1',settings
result={'started_utc':started,'finished_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'scope':'installed ES startup watcher with both inherited update switches enabled, direct compatibility CLI calls, and local positive capture control','watcher_log':log,'cli':checks,'settings':'updates.enabled=1 updates.force=1','positive_control':observed,'installed_bytes':before,'packet_verdict':'requires closed QEMU capture classification'}
(owner/'artifacts'/(label+'-network-exercise.json')).write_text(json.dumps(result,indent=2)+'\n')
print('PASS observed installed update watcher, CLI and local capture-positive control '+label,flush=True)

from pathlib import Path
import json,hashlib,subprocess,time,socket
r=Path('/tmp/pix-output');source=Path('/tmp/pix-input');result={'rc':1,'started':time.time()}
def sha(p):return hashlib.file_digest(p.open('rb'),'sha256').hexdigest()
def run(argv):return subprocess.run(argv,capture_output=True,text=True,check=True,timeout=20).stdout
try:
 assert sorted(n for _,n in socket.if_nameindex())==['lo']
 manifest=json.loads((source/'input-files.json').read_text());assert all(sha(source/p)==h for p,h in manifest.items())
 result['inputs_verified']=len(manifest);result['os_release']=Path('/etc/os-release').read_text();result['boot']=Path('/proc/sys/kernel/random/boot_id').read_text().strip()
 state=run(['systemctl','show','rocknix-autostart.service','-p','ActiveState','-p','Result','-p','ExecMainStatus','-p','ExecMainStartTimestampMonotonic']);assert 'ActiveState=active' in state and 'Result=success' in state and 'ExecMainStatus=0' in state
 result['autostart']=state;result['prior_es']=sha(Path('/usr/bin/emulationstation'))
 run(['systemctl','stop','essway.service'])
 run(['mount','--bind',str(source/'emulationstation'),'/usr/bin/emulationstation']);run(['mount','--make-private','/usr/bin/emulationstation'])
 target=Path('/storage/.config/locale/fr/LC_MESSAGES/emulationstation2.mo');target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes((source/'artifacts/fr.mo').read_bytes());assert sha(target)=='82f0abcf0fc95310b088ee7313eaa5738d0121d81667c8d0bbda06d9dadea472'
 run(['systemctl','start','essway.service'])
 for i in range(45):
  p=subprocess.run(['curl','-fsS','http://127.0.0.1:1234/isIdle'],capture_output=True,text=True,timeout=3)
  if p.returncode==0 and json.loads(p.stdout)==[True]:break
  time.sleep(1)
 else:raise RuntimeError('ES not idle')
 pid=int(run(['pidof','emulationstation']).strip());result['es_pid']=pid;result['es_sha256']=sha(Path('/proc')/str(pid)/'exe');assert result['es_sha256']=='8752b5391ea8728c1a088d0a80e3776469692dda665e8f07f062fed3206263d2'
 result['sockets']=[str(p) for p in Path('/run/0-runtime-dir').glob('wayland-*') if p.is_socket()];result['mountinfo']=Path('/proc/self/mountinfo').read_text();result['rc']=0
finally:
 result['ended']=time.time();(r/'provision-result.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({k:v for k,v in result.items() if k not in ['os_release','mountinfo']}))
raise SystemExit(result['rc'])

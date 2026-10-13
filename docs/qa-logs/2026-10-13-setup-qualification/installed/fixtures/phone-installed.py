from pathlib import Path
import sys,json,time,subprocess,importlib.machinery,importlib.util,hashlib,traceback
from ui import remote,out,shot,key
r=Path(__file__).parent;repo=Path('/workspace/repos/rocknix.worktrees/m7-player-setup');name,mode,lang=sys.argv[1:];rclone_bound=False;case=r/name;case.mkdir();result={'rc':1,'name':name,'mode':mode,'language':lang,'started':time.time()}
loader=importlib.machinery.SourceFileLoader('visualqa',str(repo/'tools/vm-visual-qa'));spec=importlib.util.spec_from_loader(loader.name,loader);vq=importlib.util.module_from_spec(spec);loader.exec_module(vq)
mon=vq.Monitor(str(r/'vm/monitor.sock'))
def key(k):mon.sendkey(k)
def waitfor(fn,seconds,label):
 end=time.monotonic()+seconds
 while time.monotonic()<end:
  if fn():return
  time.sleep(.3)
 raise RuntimeError(label)
def walk(keys,label=None):
 lines=[]
 for k in keys:lines+=['key '+k,'wait-for-change','settle']
 if label:lines+=['shot '+label]
 vq.run_steps(mon,lines,str(case/'walk'))
def frame(label):
 ok,t=vq.settle(mon.frame,timeout=12,quiet=1.0);result.setdefault('settles',[]).append({'frame':label,'stable':ok,'seconds':t});assert ok,'frame did not settle: '+label
 shot(case/(label+'.png'))
def identity():
 return out("python3 - <<'P'\nfrom pathlib import Path\nimport subprocess,json,hashlib\npid=subprocess.check_output(['pidof','emulationstation'],text=True).strip();p=Path('/proc')/pid;print(json.dumps({'pid':pid,'start':(p/'stat').read_text().split()[21],'boot':Path('/proc/sys/kernel/random/boot_id').read_text().strip(),'hash':hashlib.file_digest((p/'exe').open('rb'),'sha256').hexdigest()}))\nP").strip()
try:
 # Install this source only while the broker is idle, before a fresh session.
 assert out('cloud_oauth status').strip()=='idle'
 source=repo/'projects/ROCKNIX/packages/network/rclone/sources/cloud_oauth'
 assert hashlib.sha256(source.read_bytes()).hexdigest()=='95c626f8df07faef522683a857e48e31f85a58c6f738bcde24707574dc24d293'
 if out('sha256sum /usr/bin/cloud_oauth').split()[0]!='95c626f8df07faef522683a857e48e31f85a58c6f738bcde24707574dc24d293':
  with source.open('rb') as f:remote('cat > /storage/qa570flows/cloud_oauth',stdin=f)
  remote('chmod 755 /storage/qa570flows/cloud_oauth; mount --bind /storage/qa570flows/cloud_oauth /usr/bin/cloud_oauth; mount --make-private /usr/bin/cloud_oauth',capture_output=True)
 assert out('sha256sum /usr/bin/cloud_oauth').split()[0]=='95c626f8df07faef522683a857e48e31f85a58c6f738bcde24707574dc24d293'
 # This owner created the guest and every remote. Refuse any unexpected name.
 names=out('/storage/qa570flows/rclone-original listremotes').split();assert all(n=='dropbox:' for n in names),names
 remote('cloud_oauth cancel >/dev/null 2>&1; systemctl stop essway.service; rm -f /storage/qa570flows/page-loaded /storage/qa570flows/complete /storage/qa570flows/fail /storage/qa570flows/browser-fail-observed; rm -f /storage/.config/rclone/rclone.conf /storage/.config/rclone/active-connection',capture_output=True)
 # A file bind must be discovered through mountinfo, not mountpoint -q.
 remote("python3 - <<'P'\nfrom pathlib import Path\nimport subprocess\np='/usr/bin/cloud-signin-window'\nfor i in range(8):\n if not any(l.split()[4]==p for l in Path('/proc/self/mountinfo').read_text().splitlines()):break\n subprocess.run(['umount',p],check=True)\nelse:raise RuntimeError('browser bind cleanup bound')\nP",capture_output=True)
 with (r/'fake-rclone-phone').open('rb') as f:remote('cat > /storage/qa570flows/rclone-phone',stdin=f)
 remote('chmod 755 /storage/qa570flows/rclone-phone; rm -f /storage/qa570flows/typed.jsonl /storage/qa570flows/page-phase; mount --bind /storage/qa570flows/rclone-phone /usr/bin/rclone; mount --make-private /usr/bin/rclone',capture_output=True);rclone_bound=True
 result['fixture_sha256']=out('sha256sum /usr/bin/rclone').split()[0];assert result['fixture_sha256']==hashlib.sha256((r/'fake-rclone-phone').read_bytes()).hexdigest()
 remote('. /etc/profile >/dev/null 2>&1; set_setting system.language '+lang+'; test "$(get_setting system.language)" = '+lang+'; systemctl start essway.service',capture_output=True)
 waitfor(lambda:out('curl -fsS http://127.0.0.1:1234/isIdle 2>/dev/null || true').replace(' ','').strip()=='[true]',60,'frontend idle unavailable')
 result['before']=json.loads(identity());assert result['before']['hash']=='f6fd61b7bea859467f1a3b0e1f890c975bfef9aaafd1866e727752727de013b3'
 vq.run_steps(mon,['wake','settle','shot initial'],str(case/'initial'))
 walk(['ret','x','up','up','up','x']);walk(['down x5','x','x','x','down','x'])
 waitfor(lambda:out('cloud_oauth status').strip()=='waiting',30,'authorize not waiting');frame('keyboard-choice')
 walk(['down','x']);frame('phone-pairing');walk(['down','right']);key('x')
 waitfor(lambda:out('test -f /storage/qa570flows/page-loaded && echo yes || true').strip()=='yes',25,'phone browser did not load');frame('browser-loaded')
 client=subprocess.run(['/tmp/pixelelated-import-qa-venv/bin/python',str(r/'phone-installed-client.py'),str(case/'companion')],timeout=70)
 assert client.returncode==0,'installed companion failed';frame('browser-received-second-page-text')
 remote('touch /storage/qa570flows/complete',capture_output=True);waitfor(lambda:out('cloud_oauth status').strip()=='signed-in',30,'fixture sign-in did not finish')
 waitfor(lambda:out('pidof cloud-signin-window || true').strip()=='',25,'browser did not close');frame('connected')
 result['after']=json.loads(identity());assert result['before']==result['after'],'frontend identity changed'
 result['status']=out('cloud_oauth status').strip();result['remote_names']=out('/storage/qa570flows/rclone-original listremotes').split();assert result['status']=='signed-in' and result['remote_names']==['dropbox:']
 result['rc']=0
except BaseException as e:
 result['error']=str(e);traceback.print_exc()
finally:
 remote('cloud_oauth cancel >/dev/null 2>&1',capture_output=True)
 if rclone_bound:remote('umount /usr/bin/rclone',capture_output=True)
 result['final_status']=out('cloud_oauth status').strip();result['browser_absent']=out('pidof cloud-signin-window || true').strip()=='';result['ended']=time.time();(case/'result.json').write_text(json.dumps(result,indent=2)+'\n')
raise SystemExit(result['rc'])

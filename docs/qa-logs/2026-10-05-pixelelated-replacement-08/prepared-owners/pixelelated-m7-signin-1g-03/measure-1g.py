from pathlib import Path
import datetime,hashlib,json,re,subprocess,time
owner=Path(__file__).parent;out=owner/'artifacts'
ssh=['ssh','-i',str(owner/'pair/qa-key'),'-p','10026','-o','BatchMode=yes','-o','ConnectTimeout=8','-o','StrictHostKeyChecking=no','-o','UserKnownHostsFile=/dev/null','-o','LogLevel=ERROR','root@127.0.0.1']
def guest(command):return subprocess.check_output(ssh+[command],text=True,timeout=30)
mem=guest('cat /proc/meminfo');total=int(re.search(r'^MemTotal:\s+(\d+)',mem,re.M)[1]);assert 850000<total<1048576,total
(out/'guest-meminfo-before.txt').write_text(mem)
expected=hashlib.sha256(Path('/workspace/tmp/pixelelated-m7-image-09/root/usr/bin/cloud-signin-window').read_bytes()).hexdigest();actual=guest('sha256sum /usr/bin/cloud-signin-window').split()[0];assert actual==expected
with (out/'signin-memory.json').open('w') as f, (out/'signin-memory.stderr').open('w') as e:
 proc=subprocess.Popen(['./tools/signin-memory','10026','--key',str(owner/'pair/qa-key'),'--seconds','30','--json'],stdout=f,stderr=e)
 captured=False
 try:
  deadline=time.monotonic()+27
  while proc.poll() is None and time.monotonic()<deadline:
   if guest("grep -c 'load finished' /tmp/signin-memory.log 2>/dev/null || true").strip() not in ('','0'):
    subprocess.run(['./tools/vm-visual-qa','--monitor','/tmp/rocknix-qemu-monitor-d.sock','shot',str(out/'loaded-640x480.png')],check=True);captured=True;break
   time.sleep(.5)
  rc=proc.wait(timeout=120)
 finally:
  if proc.poll() is None:
   proc.terminate()
   try:proc.wait(timeout=10)
   except subprocess.TimeoutExpired:proc.kill();proc.wait()
journal=guest('journalctl -k -b --no-pager');(out/'kernel.log').write_text(journal)
oom=re.findall(r'^.*(?:oom-kill|Out of memory:|Killed process|invoked oom-killer).*$',journal,re.M)
(out/'guest-meminfo-after.txt').write_text(guest('cat /proc/meminfo'))
result={'observed_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'guest_memtotal_kib':total,'configured_memory_mib':1024,'actual_measurement_rc':rc,'loaded_frame_captured':captured,'oom_lines':oom,'payload_sha256':actual,'numerical_rss_ceiling_enforced':False}
if (out/'signin-memory.json').stat().st_size:
 d=json.loads((out/'signin-memory.json').read_text());result.update({'loaded':d['loaded'],'measurement_pass':d['pass'],'peak_total_rss_kib':d['peak_total_rss_kb']})
(out/'resource-budget.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result),flush=True)
assert rc==0 and captured and not oom and result['loaded'] and result['measurement_pass']
print('PASS loaded within the1GiB guest budget without kernel OOM; peak recorded, no numerical RSS ceiling invented',flush=True)

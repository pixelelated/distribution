from pathlib import Path
import json,subprocess,time,traceback
from ui import out,remote
r=Path(__file__).parent;d=r/'steam-installed-results';d.mkdir();result={'rc':1,'started':time.time()};src='/tmp/pix-steam-installed-source';scratch='/run/qa-steam-installed-scratch';output=scratch+'/steam-installed-return-first'
try:
 contract=json.loads((r/'records/steam-installed-source.json').read_text())
 result['prerequisites']=out('cat /proc/meminfo; grep -P "^QEMU$" /sys/class/dmi/id/sys_vendor; unshare --help')
 remote('mkdir '+src+' '+scratch+' && mount -n -t tmpfs -o size=3G,mode=700 tmpfs '+scratch,capture_output=True)
 with (r/'records/steam-installed.tar').open('rb') as f:remote('cat > '+src+'/packet.tar',stdin=f)
 assert out('sha256sum '+src+'/packet.tar').split()[0]==contract['archive_sha256']
 remote('tar xf '+src+'/packet.tar -C '+src,capture_output=True)
 command='cd '+src+' && timeout 80 env TMPDIR='+scratch+' python3 -I -S -B '+contract['packet']+'/fixture.py --disposable-vm --output '+output
 p=subprocess.run(json.loads((r/'ssh-command.json').read_text())+[command],capture_output=True,text=True,timeout=95)
 (d/'stdout').write_text(p.stdout);(d/'stderr').write_text(p.stderr);result['guest_rc']=p.returncode
 if out('test -f '+output+'/result.json && echo yes || true').strip()=='yes':
  raw=out('cat '+output+'/result.json');(d/'result.json').write_text(raw)
  for name in ['namespace-result.json','caller-observation.json']:
   if out('test -f '+output+'/'+name+' && echo yes || true').strip()=='yes':(d/name).write_text(out('cat '+output+'/'+name))
  script="from pathlib import Path\nimport tarfile,sys\nr=Path('"+output+"')\nwith tarfile.open(fileobj=sys.stdout.buffer,mode='w|') as t:\n for p in r.rglob('*'):\n  if p.is_file() and not p.is_symlink() and (p.suffix in ['.json','.jsonl','.ndjson','.log','.stdout','.stderr']) and p.stat().st_size<4*1024*1024:t.add(p,arcname=str(p.relative_to(r)),recursive=False)\n"
  raw=remote("python3 - <<'P'\n"+script+"P",capture_output=True).stdout;(d/'receipts.tar').write_bytes(raw)
 result['remaining_processes']=out("ps -eo pid,ppid,args | grep '/run/qa-steam-installed' | grep -v 'grep' || true")
 assert p.returncode==0,p.stderr
 assert json.loads((d/'result.json').read_text())['status']=='PASS'
 result['rc']=0
except BaseException as e:result['error']=repr(e);traceback.print_exc()
finally:
 result['ended']=time.time();(r/'steam-installed-result.json').write_text(json.dumps(result,indent=2)+'\n')
raise SystemExit(result['rc'])

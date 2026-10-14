from pathlib import Path
import json,subprocess,hashlib,time,tarfile,io
from ui import out,remote
r=Path(__file__).parent;d=r/'steam-corrected-results';d.mkdir();result={'rc':1,'started':time.time()}
try:
 result['prerequisites']=out("python3 - <<'P'\nimport ctypes,fcntl,lzma,tarfile,unittest.mock,os,sys\nfrom pathlib import Path\nprint(sys.version)\nfor p in ['/bin/bash','/bin/cp','/bin/rm','/bin/mkdir','/usr/bin/unshare']:\n print(p,Path(p).exists());assert Path(p).exists()\nprint('prctl',hasattr(ctypes.CDLL(None),'prctl'),'renameat2',hasattr(ctypes.CDLL(None),'renameat2'))\nP")
 remote('mkdir /run/qa-steam-corrected-source /run/qa-steam-scratch/corrected-tmp',capture_output=True)
 with (r/'records/steam-corrected.tar').open('rb') as f:remote('cat > /run/qa-steam-corrected-source/packet.tar',stdin=f)
 assert out('sha256sum /run/qa-steam-corrected-source/packet.tar').split()[0]==json.loads((r/'records/steam-corrected-source.json').read_text())['archive_sha256']
 remote('tar xf /run/qa-steam-corrected-source/packet.tar -C /run/qa-steam-corrected-source',capture_output=True)
 command='cd /run/qa-steam-corrected-source && timeout 90 unshare -n -- env TMPDIR=/run/qa-steam-scratch/corrected-tmp python3 -I -S -B docs/qa-logs/2026-10-13-steam-combined-source/null-sink-correction/driver.py --output /run/qa-steam-scratch/corrected-tmp/first'
 p=subprocess.run(json.loads((r/'ssh-command.json').read_text())+[command],capture_output=True,text=True,timeout=105);(d/'outer.stdout').write_text(p.stdout);(d/'outer.stderr').write_text(p.stderr);result['guest_rc']=p.returncode
 if out('test -f /run/qa-steam-scratch/corrected-tmp/first/result.json && echo yes || true').strip()=='yes':
  data=out('cat /run/qa-steam-scratch/corrected-tmp/first/result.json');(d/'result.json').write_text(data)
  # Keep compact evidence only; synthetic archive/file payloads remain disposable in the guest.
  raw=remote("python3 - <<'P'\nfrom pathlib import Path\nimport tarfile,sys\nr=Path('/run/qa-steam-scratch/corrected-tmp/first')\nwith tarfile.open(fileobj=sys.stdout.buffer,mode='w|') as t:\n for p in r.rglob('*'):\n  if p.is_file() and not p.is_symlink() and p.suffix in ['.json','.jsonl','.ndjson','.log'] and p.stat().st_size<4*1024*1024:t.add(p,arcname=str(p.relative_to(r)),recursive=False)\nP",capture_output=True).stdout
  (d/'compact-receipts.tar').write_bytes(raw)
 result['leftovers']=out("ps -eo pid,ppid,args | grep '/run/qa-steam' | grep -v 'grep' || true")
 assert p.returncode==0,p.stderr
 assert json.loads((d/'result.json').read_text())['status']=='PASS'
 result['rc']=0
finally:
 result['ended']=time.time();(r/'steam-corrected-result.json').write_text(json.dumps(result,indent=2)+'\n')
raise SystemExit(result['rc'])

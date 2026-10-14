from pathlib import Path
import json,subprocess,time,traceback,sys
from ui import out,remote
r=Path(__file__).parent;label=sys.argv[1];system=sys.argv[2];case=sys.argv[3];lang=sys.argv[4];d=r/('dolphin-v2-'+label);d.mkdir();owner='/tmp/pix581-installed-v2-'+label;src='/tmp/pix581-v2-source';s=json.loads((r/'records/dolphin-installed-v2-source.json').read_text());c=json.loads((r/'records/candidate.json').read_text());result={'rc':1,'started':time.time(),'guest_owner':owner,'case':case,'system':system,'language':lang}
try:
 args=['/usr/bin/bash',src+'/'+s['packet']+'/guest-session.sh',src,owner,system,case,lang,c['sha256'],c['source'],'/run/0-runtime-dir/wayland-1','Vulkan','/tmp/pix581-v2-products','/tmp/pix581-v2-defaults/dolphin-emu','/tmp/pix581-v2-defaults/receipt.json']
 result['guest_command']=args
 p=subprocess.run(json.loads((r/'ssh-command.json').read_text())+[' '.join(args)],capture_output=True,text=True,timeout=370)
 (d/'stdout').write_text(p.stdout);(d/'stderr').write_text(p.stderr);result['guest_rc']=p.returncode
 if out('test -d '+owner+' && echo yes || true').strip()=='yes':
  script="from pathlib import Path\nimport tarfile,sys\nr=Path('"+owner+"')\nwith tarfile.open(fileobj=sys.stdout.buffer,mode='w|') as t:\n for p in r.rglob('*'):\n  if p.is_file() and not p.is_symlink() and (p.suffix in ['.json','.jsonl','.ndjson','.log','.stdout','.stderr','.exit'] or p.name in ['stdout','stderr']) and p.stat().st_size<8*1024*1024 and '/storage/' not in str(p):t.add(p,arcname=str(p.relative_to(r)),recursive=False)\n"
  raw=remote("python3 - <<'P'\n"+script+"P",capture_output=True).stdout;(d/'receipts.tar').write_bytes(raw)
 result['frontend']=out('systemctl show essway.service -p ActiveState -p SubState -p Result; systemctl show sway.service -p ActiveState -p SubState -p Result')
 assert p.returncode==0,p.stderr
 result['rc']=0
except BaseException as e:result['error']=repr(e);traceback.print_exc()
finally:
 result['ended']=time.time();(d/'host-result.json').write_text(json.dumps(result,indent=2)+'\n')
raise SystemExit(result['rc'])

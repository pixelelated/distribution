from pathlib import Path
import sys,json,time,subprocess
from ui import remote,out
r=Path(__file__).parent;profile,lang=sys.argv[1:];result={'rc':1,'profile':profile,'language':lang,'started':time.time()}
try:
 assert out('cloud_oauth status').strip()=='idle'
 remote('systemctl stop essway.service',capture_output=True)
 remote("python3 - <<'P'\nfrom pathlib import Path\nimport subprocess\np='/usr/bin/wifictl'\nfor i in range(8):\n if not any(l.split()[4]==p for l in Path('/proc/self/mountinfo').read_text().splitlines()):break\n subprocess.run(['umount',p],check=True)\nelse:raise RuntimeError('bind cleanup limit')\nP",capture_output=True)
 remote('. /etc/profile >/dev/null 2>&1; set_setting system.language '+lang+'; systemctl start essway.service',capture_output=True)
 end=time.monotonic()+45
 while time.monotonic()<end:
  if out('curl -fsS http://127.0.0.1:1234/isIdle 2>/dev/null || true').replace(' ','').strip()=='[true]':break
  time.sleep(.5)
 else:raise RuntimeError('frontend readiness')
 for phase in ['initial','branches']:
  code=(r/('wifi-'+phase+'.py')).read_text().replace("wifi-en640-"+phase,"wifi-"+profile+"-"+phase).replace('/storage/qa-wifi-577-setup','/storage/qa-wifi-577-'+profile)
  dest=r/('wifi-'+profile+'-'+phase+'.py');dest.write_text(code)
  p=subprocess.run(['timeout','150','python3',str(dest)]);result[phase]=p.returncode
  if p.returncode:raise RuntimeError(phase+' failed')
 result['rc']=0
finally:
 result['ended']=time.time();(r/('wifi-'+profile+'-result.json')).write_text(json.dumps(result,indent=2)+'\n')
raise SystemExit(result['rc'])

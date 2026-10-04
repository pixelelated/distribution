"""Capture installed Tools rows on the owned QA guest; never launch a tool."""
import argparse,hashlib,json,subprocess,time,xml.etree.ElementTree as ET
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('--owner',type=Path,required=True);p.add_argument('--output',type=Path,required=True);a=p.parse_args();a.output.mkdir(parents=True,exist_ok=True)
ssh=['ssh','-i',str(a.owner/'pair/qa-key'),'-p','10026','-o','BatchMode=yes','-o','ConnectTimeout=8','-o','StrictHostKeyChecking=no','-o','UserKnownHostsFile=/dev/null','-o','LogLevel=ERROR','root@127.0.0.1']
def guest(cmd,**kw):return subprocess.run(ssh+[cmd],check=True,**kw)
def idle():
 for i in range(90):
  r=subprocess.run(ssh+['curl -sS -m 3 http://127.0.0.1:1234/isIdle'],capture_output=True,text=True)
  if r.returncode==0 and r.stdout.strip() and json.loads(r.stdout)==[True]:return
  time.sleep(1)
 raise RuntimeError('Tools view did not become idle')
settings='/storage/.config/emulationstation/es_settings.cfg';guest('systemctl stop essway')
original=guest('cat '+settings,capture_output=True).stdout
try:
 root=ET.fromstring(original)
 for typ,name,value in [('string','StartupSystem','tools'),('bool','StartupOnGameList','true')]:
  el=root.find(f"{typ}[@name='{name}']")
  if el is None:el=ET.SubElement(root,typ,{'name':name})
  el.set('value',value)
 guest('cat > '+settings,input=ET.tostring(root,encoding='utf-8',xml_declaration=True));guest('systemctl start essway');idle()
 v=['./tools/vm-visual-qa','--monitor','/tmp/rocknix-qemu-monitor-d.sock']
 # No dismiss here: it would leave the deliberately selected game list.
 for i in range(10):
  subprocess.run(v+['settle','--timeout','10','--quiet','1.2'],check=True)
  subprocess.run(v+['shot',str(a.output/f'tools-row-{i:02d}.png')],check=True)
  if i<9:subprocess.run(v+['key','down'],check=True)
 print('CAPTURED ten installed Tools rows; visual review required',flush=True)
finally:
 guest('systemctl stop essway');guest('cat > '+settings,input=original)
 assert hashlib.sha256(guest('cat '+settings,capture_output=True).stdout).digest()==hashlib.sha256(original).digest()
 guest('systemctl start essway');idle()
print('PASS original owned guest UI settings restored',flush=True)

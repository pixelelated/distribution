import json,subprocess,time
from pathlib import Path
P=Path(__file__).resolve().parent;R=Path('/workspace/tmp/pix-m7-headroom-vm-20261016-02')
def req(name,kind,value='',timeout=30):
 c=subprocess.run(['python3',str(P/'request.py'),name,kind,value,'--timeout',str(timeout)],capture_output=True,text=True,timeout=60)
 assert c.returncode==0,(name,c.stderr)
 v=json.loads((R/'responses'/(name+'.json')).read_text());assert v['status']=='PASS',(name,v)
 return v['output']
def key(name,k):req(name,'monitor','sendkey '+k+' 100');time.sleep(.3)

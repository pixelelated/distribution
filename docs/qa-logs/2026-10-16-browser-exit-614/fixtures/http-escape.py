import json,time,urllib.request,urllib.parse
from pathlib import Path
v=json.loads(Path('/var/run/cloud_oauth/session.json').read_text());assert v.get('pin');results=[]
for fields in [{'type':'v'},{'key':'escape'}]:
 fields['pin']=v['pin'];start=time.monotonic()
 req=urllib.request.Request('http://127.0.0.1:8080/',data=urllib.parse.urlencode(fields).encode())
 with urllib.request.urlopen(req,timeout=5) as response:status=response.status
 results.append({'action':'type' if 'type' in fields else 'escape','status':status,'at':start,'elapsed':time.monotonic()-start});assert status==204
 time.sleep(1)
print(json.dumps({'transport':'guest loopback to installed phone POST handler','results':results}))

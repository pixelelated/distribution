from pathlib import Path
import subprocess,json,time
r=Path(__file__).parent;results=[]
commands=[
(180,['provision1280.py']),
(330,['wifi-profile.py','en1280','en_US']),
(330,['wifi-profile.py','fr1280','fr_FR']),
(180,['browser-recovery02.py','browser-native-en1280','native','en_US']),
(180,['browser-recovery02.py','browser-phone-en1280','phone','en_US']),
(180,['browser-recovery02.py','browser-native-fr1280','native','fr_FR']),
(180,['browser-recovery02.py','browser-phone-fr1280','phone','fr_FR']),
(210,['phone-installed04.py','phone-installed-fr1280','phone','fr_FR']),
(110,['notice-frames02.py','notice-en1280-on','en_US','on']),
(110,['notice-frames02.py','notice-fr1280-on','fr_FR','on']),
(110,['notice-frames02.py','notice-en1280-off','en_US','off']),
(110,['notice-frames02.py','notice-fr1280-off','fr_FR','off']),
(330,['recent-frames02.py','en1280','en_US']),
(330,['recent-frames02.py','fr1280','fr_FR']),
]
for bound,command in commands:
 start=time.time();print('BEGIN '+str(command),flush=True)
 p=subprocess.run(['timeout',str(bound),'python3',str(r/command[0]),*command[1:]])
 results.append({'command':command,'rc':p.returncode,'started':start,'ended':time.time()});(r/'large-batch-result.json').write_text(json.dumps(results,indent=2)+'\n')
 if p.returncode:break
raise SystemExit(0 if len(results)==len(commands) and all(x['rc']==0 for x in results) else 1)

import os,json,hashlib,subprocess,time
from pathlib import Path
R=Path('/storage/qa587');R.mkdir(mode=0o700,exist_ok=True)
C=Path('/storage/.config/raofflineproxy');C.mkdir(mode=0o700,exist_ok=True)
assert not (C/'proxy.sqlite3').exists(),'fresh synthetic database only'
assert not (C/'config.json').exists(),'fresh synthetic configuration only'
cfg={'proxy_host':'127.0.0.1','proxy_port':8080,'upstream_host':'http://127.0.0.1:19081','cache_images':False,'upload_logs':False}
(C/'config.json').write_text(json.dumps(cfg)+'\n');(C/'config.json').chmod(0o600)
os.environ['RAOFFLINEPROXY_CONFIG_DIR']=str(C)
from raofflineproxy import cache_keys,storage
s=storage.Storage()
for who in ['fixture','alternate']:
 s.upsert_cache(cache_keys.login(who),json.dumps({'Success':True,'User':who,'Token':'fixture-only'}))
 for game,aid in [(10,101),(20,201)]:s.upsert_cache(cache_keys.patch(game,who),json.dumps({'Success':True,'PatchData':{'ID':game,'Title':'Synthetic','Achievements':[{'ID':aid}]}}))
assert s._connection.execute('PRAGMA integrity_check').fetchone()[0]=='ok';s.close()
subprocess.run(['bash','-lc','. /etc/profile >/dev/null 2>&1; set_setting global.retroachievements.offlineproxy 1'],check=True)
marker=Path('/storage/.cache/services/raofflineproxy.conf');marker.parent.mkdir(parents=True,exist_ok=True);marker.touch();marker.chmod(0o600)
paths=[Path('/storage/.config/system/configs/system.cfg'),C/'config.json',marker]
(R/'protected.json').write_text(json.dumps({str(p):{'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'mode':p.stat().st_mode&0o777} for p in paths},indent=2)+'\n')
modules=Path('/usr/lib/python3.14/site-packages/raofflineproxy')
(R/'installed.json').write_text(json.dumps({str(p):hashlib.sha256(p.read_bytes()).hexdigest() for p in list(modules.glob('*.pyc'))+[Path('/usr/lib/systemd/system/raofflineproxy.service'),Path('/usr/bin/raofflineproxy-ctl'),Path('/usr/bin/cloud-signin-window'),Path('/usr/bin/emulationstation')]},indent=2)+'\n')
print('Synthetic database/configuration seeded; service not started by seed step.')

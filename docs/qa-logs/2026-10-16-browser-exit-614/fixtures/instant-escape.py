import sys,json,time
from pathlib import Path
sys.path.insert(0,'/usr/bin')
n={'__name__':'qa614_keyboard','__file__':'/usr/bin/cloud_oauth'}
exec(compile(Path('/usr/bin/cloud_oauth').read_text(),'/usr/bin/cloud_oauth','exec'),n)
k=n['RemoteKeyboard']();start=time.monotonic()
try:
 bad=k.press('esc');assert bad is False
 good=k.press('escape');assert good is True
finally:k.close()
print(json.dumps({'bad_name_rejected':not bad,'escape_enqueued':good,'immediate_destroy':True,'at':start,'ended':time.monotonic()}))

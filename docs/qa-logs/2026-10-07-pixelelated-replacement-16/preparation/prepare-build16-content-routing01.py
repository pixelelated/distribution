from pathlib import Path
from datetime import datetime, timezone
import ast
import hashlib
import json
import shutil
import subprocess

old = Path('/workspace/tmp/pixelelated-m7-p4-build16-root-reasons-640x480-01')
owner = Path('/workspace/tmp/pixelelated-m7-p4-build16-content-routing-640x480-01')
assert not owner.exists()
owner.mkdir(mode=0o700)
(owner/'artifacts').mkdir(mode=0o700)
for name in ['run.sh','outer.sh','verify-inputs.py','check-payload.py','proxy-identity.py','seed.py','stop-guest.py','cloud-ui-proof.py']:
    s=(old/name).read_text().replace(old.name,owner.name)
    if name=='cloud-ui-proof.py':
        function='''def fallback_content():
 put('pixelelated/Content/ROMs/gb/Fallback.gb',b'fallback game\\n');put('Mine/Photos/witness.jpg');before=hashes();start();restore();content_continue()
 check('CONTENT_REMOTE="/pixelelated/Content"' in pointers(),'actual UI automatically selects discovered default content')
 facts=guest('cat /storage/.cache/cloud_sync/scan/content-location').stdout
 check('STATE=found-elsewhere' in facts and 'FOUND=/pixelelated/Content' in facts,'opening scan retains default fallback facts')
 scan=guest('cat /storage/.cache/cloud_sync/scan/scan').stdout
 check(re.search(r'^gb\\|14\\|1\\|',scan,re.M),'fallback supported game appears in actual scan')
 check(hashes()==before,'automatic fallback preserves every cloud byte')
 save('fallback',dict(pointers=pointers(),cloud=hashes(),facts=facts,scan=scan));walk('close',['dismiss-dialogs'])
'''
        s=s.replace('def reason(kind):',function+'def reason(kind):')
        start=s.index("  cases=[('legacy-root'");end=s.index('  for name,action in cases:',start)
        s=s[:start]+"  cases=[('automatic-fallback',fallback_content),('manual-chooser',lambda:chooser('My Games'))]\n"+s[end:]
        old_action="   reset(language);action();rows.append({'case':case,'status':'PASS','visual_review':'pending'});(out/'results.json').write_text(json.dumps(rows,indent=2)+'\\n')"
        new_action='''   reset(language)
   cursor=guest('journalctl -n 0 --show-cursor --no-pager').stdout.split('-- cursor: ',1)[1].strip()
   log_start=int(guest('wc -l < /var/log/cloud_sync.log').stdout)
   action()
   selected='/pixelelated/Content' if name=='automatic-fallback' else '/My Games'
   log=guest('tail -n +'+str(log_start+1)+' /var/log/cloud_sync.log').stdout
   line=[x for x in log.splitlines() if '[cloud_setup]' in x and 'Content path set to '+selected+' by request' in x]
   check(len(line)==1,'actual content-setting log records exactly this selection')
   journal=guest('journalctl --after-cursor '+shlex.quote(cursor)+" --no-pager | grep -v -i -E 'key|pass|token|user|psk'",allowed=None).stdout
   (out/(case+'-journal.txt')).write_text(journal)
   save('selection-log',dict(selected=selected,lines=line,cursor=cursor,pointers=pointers()))
   rows.append({'case':case,'status':'PASS','visual_review':'pending'});(out/'results.json').write_text(json.dumps(rows,indent=2)+'\\n')'''
        assert old_action in s;s=s.replace(old_action,new_action)
    (owner/name).write_text(s);shutil.copymode(old/name,owner/name)
    if name.endswith('.py'):ast.parse(s)
    if name.endswith('.sh'):subprocess.run(['bash','-n',str(owner/name)],check=True)
(owner/'provenance.json').write_text(json.dumps(dict(prepared_utc=datetime.now(timezone.utc).isoformat(),issue=467,parent=str(old),scope='Actual installed automatic default-content fallback and successful manual chooser in EN/FR640, with exact pointer, new setting log, journal, source hashes and direct frame review.',order='After selected-content01 and verified actual cleanup; no product changes.'),indent=2)+'\n')
(owner/'harness.sha256').write_text(''.join(hashlib.sha256(p.read_bytes()).hexdigest()+'  '+str(p)+'\n' for p in sorted(owner.iterdir()) if p.is_file()))
print(owner,'prepared; 9 sealed files, 4 EN/FR routing cases')

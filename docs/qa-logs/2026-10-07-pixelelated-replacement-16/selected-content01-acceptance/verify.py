from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json

q=Path('docs/qa-logs/2026-10-07-pixelelated-replacement-16')
retained=q/'p4-build16-selected-content-01'
dest=q/'selected-content01-acceptance'
assert not dest.exists()
read=lambda p:json.loads(p.read_text())
completion=read(retained/'owner-verification.json')
assert completion['result']=='PASS' and completion['sealed_inputs']==212
assert len(completion['channels'])==4 and set(completion['channels'].values())=={'0'}
cleanup=read(retained/'guest-cleanup-verification.json')
assert cleanup['passed'] and cleanup['no_live_qemu'] and cleanup['no_live_owner_processes']
for name,wanted in read(retained/'sha256.json').items():
    assert hashlib.sha256((retained/name).read_bytes()).hexdigest()==wanted,name
art=retained/'proof/artifacts'
rows=read(art/'results.json')
kinds=['legacy','tiered','bios','unsupported']
assert rows==[dict(case='PL001-installed-selected-'+k,status='PASS') for k in kinds]
details={}
for k in kinds:
    row=read(art/('PL001-installed-selected-'+k+'-selected.json'))
    expected=(('candidate16 selected '+k+' witness\n')*257).encode()
    wanted=hashlib.sha256(expected).hexdigest()
    assert row['sha256']==wanted and row['before']==row['after']
    assert row['before']['cloud'][row['cloud_path']]==wanted
    assert row['row'][1]==str(len(expected)) and row['row'][2]==('0' if k=='unsupported' else '1')
    assert row['before']['pointers']['CONTENT_REMOTE']==''
    if k=='unsupported':assert row['not_restored']
    else:
        assert row['restored_sha256']==wanted
        matches=[p for p in art.glob('*-PL001-installed-selected-'+k+'-a.log') if (wanted+'  '+row['target']) in p.read_text()]
        assert len(matches)==1 and matches[0].with_suffix('.rc').read_text().strip()=='0'
    details[k]=row
dest.mkdir()
(dest/'acceptance.json').write_text(json.dumps(dict(verified_utc=datetime.now(timezone.utc).isoformat(),result='PASS',build_id='ee014909137e03706e0b3020b8396be589aaa705',cases=4,details=details,lifecycle=dict(channels=completion['channels'],sealed_inputs=212,actual_cleanup=True),scope='Actual installed selected legacy/tiered/BIOS restore and unsupported-system control. Existing direct UI proof and separate automatic/manual routing proof retain their own scope.'),indent=2)+'\n')
(dest/'verify.py').write_bytes(Path(__file__).read_bytes())
print('PASS: actual installed legacy/tiered/BIOS bytes restored; source/pointers unchanged; unsupported flag preserved; lifecycle verified')

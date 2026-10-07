from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json

q=Path('docs/qa-logs/2026-10-07-pixelelated-replacement-16')
r=q/'p4-build16-content-routing-640x480-01'
dest=q/'content-routing01-acceptance'
assert not dest.exists()
read=lambda p:json.loads(p.read_text())
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
owner=read(r/'owner-verification.json');cleanup=read(r/'guest-cleanup-verification.json')
assert owner['result']=='PASS' and owner['sealed_inputs']==9
assert len(owner['channels'])==4 and set(owner['channels'].values())=={'0'}
assert cleanup['passed'] and cleanup['no_live_qemu'] and cleanup['no_live_owner_processes']
for name,wanted in read(r/'sha256.json').items():assert sha(r/name)==wanted,name
art=r/'artifacts/cloud-ui';results=read(art/'results.json')
expected=[l+'-'+c for l in ['en_US','fr_FR'] for c in ['automatic-fallback','manual-chooser']]
assert [row['case'] for row in results]==expected and all(row['status']=='PASS' for row in results)
assert (art/'installed-before.sha256').read_bytes()==(art/'installed-after.sha256').read_bytes()
assert all(read(r/'artifacts'/('payload-cloud-ui-'+phase+'.json'))['passed'] for phase in ['before','after'])
details={}
for case in expected:
    manual=case.endswith('manual-chooser');wanted='/My Games' if manual else '/pixelelated/Content'
    result=read(art/(case+('-selection.json' if manual else '-fallback.json')))
    assert 'CONTENT_REMOTE="'+wanted+'"\n' in result['pointers']
    if manual:
        assert result['selected']=='My Games' and wanted in result['offered']
        assert result['cloud']['My Games/ROMs/gb/Chosen.gb']==hashlib.sha256(b'chosen game\n').hexdigest()
    else:
        assert 'STATE=found-elsewhere' in result['facts'] and 'FOUND='+wanted in result['facts']
        assert 'gb|14|1|' in result['scan']
        assert result['cloud']['pixelelated/Content/ROMs/gb/Fallback.gb']==hashlib.sha256(b'fallback game\n').hexdigest()
    log=read(art/(case+'-selection-log.json'))
    assert log['selected']==wanted and len(log['lines'])==1
    assert 'Content path set to '+wanted+' by request' in log['lines'][0]
    assert (art/(case+'-journal.txt')).is_file()
    details[case]=dict(selected=wanted,selection_log=log['lines'],journal_sha256=sha(art/(case+'-journal.txt')))
frames=read(Path('.build-runs/content-routing01-frame-review.json'))
assert len(frames)==30 and {x['file'] for x in frames}=={p.name for p in art.glob('*.png')}
for row in frames:
    assert row['result']=='PASS' and row['primary_direct_review'] and row['dimensions']==[640,480]
    assert sha(art/row['file'])==row['sha256']
console=(r/'console.log').read_text()
for case in expected:
    label='selection preserves every cloud byte' if case.endswith('manual-chooser') else 'automatic fallback preserves every cloud byte'
    assert 'PASS '+case+': '+label in console
dest.mkdir()
(dest/'frames.json').write_text(json.dumps(frames,indent=2)+'\n')
(dest/'acceptance.json').write_text(json.dumps(dict(verified_utc=datetime.now(timezone.utc).isoformat(),result='PASS',build_id='ee014909137e03706e0b3020b8396be589aaa705',cases=4,direct_frames=30,details=details,lifecycle=dict(channels=owner['channels'],sealed_inputs=9,actual_cleanup=True),scope='Installed EN/FR640 automatic default-content fallback and actual manual chooser; exact stored paths, new setting logs/journals, unchanged cloud bytes and direct frames.'),indent=2)+'\n')
(dest/'verify.py').write_bytes(Path(__file__).read_bytes())
print('PASS four actual routing cases, 30 directly reviewed frames, selection logs and lifecycle')

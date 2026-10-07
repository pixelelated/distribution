from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,sys
owner=Path(sys.argv[1]);size=list(map(int,sys.argv[2].split('x')))
qa=Path('docs/qa-logs/2026-10-07-pixelelated-replacement-16');retained=qa/owner.name.removeprefix('pixelelated-m7-');art=retained/'artifacts/cloud-ui'
v=json.loads((retained/'owner-verification.json').read_text());assert v['result']=='PASS' and set(v['channels'].values())=={'0'}
assert json.loads((retained/'guest-cleanup-verification.json').read_text())['passed']
expected={lang+'-'+case for lang in ['en_US','fr_FR'] for case in ['outer-timeout','original-connection-recovery','missing-folder','network-refusal']}
rows=json.loads((art/'results.json').read_text());assert len(rows)==8 and {r['case'] for r in rows}==expected and all(r['status']=='PASS' for r in rows)
assert (art/'installed-before.sha256').read_bytes()==(art/'installed-after.sha256').read_bytes()
frames=json.loads((Path('.build-runs')/(owner.name+'-frame-review.json')).read_text());actual={p.name for p in art.glob('*.png')}
assert len(frames)==len(actual) and {r['file'] for r in frames}==actual
log=(retained/'console.log').read_text();details={}
for lang in ['en_US','fr_FR']:
 def data(case,suffix):return json.loads((art/(lang+'-'+case+'-'+suffix+'.json')).read_text())
 timeout=data('outer-timeout','timeout');assert 29<=timeout['seconds']<38 and timeout['before']==timeout['after']
 assert " 124 cloud-stopped THE CLOUD TOOK TOO LONG - IT'LL TRY AGAIN NEXT TIME" in timeout['stamp']
 assert 'PASS '+lang+'-outer-timeout: timed-out provider and sleep child actually exited' in log
 binding=data('original-connection-recovery','binding-recovery');assert '>>> why THE PREVIOUS CLOUD MOVE NEEDS ITS ORIGINAL CONNECTION' in binding['refusal_stdout']
 before,after=binding['before'][0],binding['after'][0]
 for name,value in before.items():
  target='pixelelated/'+name.removeprefix('ROCKNIX/') if name.startswith('ROCKNIX/') else name
  assert after[target]==value
 assert after['pixelelated/.layout']==hashlib.sha256(b'layout=2\n').hexdigest()
 assert all(k+'="/pixelelated/'+suffix+'"' in binding['after'][1] for k,suffix in [('SAVES_REMOTE','Saves'),('SETTINGS_REMOTE','Backups'),('CONTENT_REMOTE','Content')])
 for assertion in ['refusal leaves all source/partial files, pointers and binding untouched','terminal repair does not rebind or replace the pending record','real UI retry completed and removed owned migration record','both source tiers survive supported recovery','other endpoint unchanged']:
  assert 'PASS '+lang+'-original-connection-recovery: '+assertion in log
 missing=data('missing-folder','absence');assert 'CURRENT_EXISTS=0' in missing['state']
 assert 'PASS '+lang+'-missing-folder: missing folder offers creation without silently writing' in log
 network=data('network-refusal','transport');assert network['returncode']!=0 and '>>> why YOUR CLOUD STOPPED ANSWERING' in network['stdout'] and "COULDN'T FIND YOUR CLOUD FOLDER" not in network['stdout']
 assert 'PASS '+lang+'-network-refusal: transport refusal preserves all state' in log
 counts={name:sum(name in p for p in actual) for name in [lang+'-outer-timeout',lang+'-original-connection-recovery',lang+'-missing-folder',lang+'-network-refusal']}
 assert list(counts.values())==[3,12,4,4],counts
 details[lang]=dict(timeout_seconds=timeout['seconds'],original_connection_recovery=True,missing_folder_creation_offer=True,network_refusal_distinct=True,frames=counts)
for row in frames:
 assert row['dimensions']==size and row['result']=='PASS' and row['primary_direct_review']
 assert hashlib.sha256((art/row['file']).read_bytes()).hexdigest()==row['sha256']
dest=qa/('recovery-'+sys.argv[2]+'-acceptance');dest.mkdir()
(dest/'frames.json').write_text(json.dumps(frames,indent=2)+'\n')
(dest/'acceptance.json').write_text(json.dumps(dict(verified_utc=datetime.now(timezone.utc).isoformat(),result='PASS',owner=str(owner),dimensions=size,cases=rows,details=details,direct_frames=len(frames),installed_product_unchanged=True,scope='Installed EN/FR timeout and supported terminal-recovery UI; real missing-folder/network controls. Full clean/upgrade and protocol qualification remain separate.'),indent=2)+'\n')
print('PASS eight recovery cases and',len(frames),'directly reviewed frames')

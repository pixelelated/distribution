from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,re
qa=Path('docs/qa-logs/2026-10-07-pixelelated-replacement-16')
retained=qa/'p4-build16-supplemental-02';art=retained/'proof/artifacts'
verification=json.loads((retained/'owner-verification.json').read_text())
assert verification['result']=='PASS' and set(verification['channels'].values())=={'0'} and verification['sealed_inputs']==212
assert json.loads((retained/'guest-cleanup-verification.json').read_text())['passed']
expected=['PL003-unreadable-active-sibling','PL005-record-write-retry','PL005-marker-write-retry','PL005-real-closed-endpoint']+['PL002-already-written-'+s for s in ['join','follow','settle']]+['PL001-empty-local-'+s for s in ['last-supported','bios','empty-directory']]
rows=json.loads((art/'results.json').read_text());assert [r['case'] for r in rows]==expected and all(r['status']=='PASS' for r in rows)
ids=json.loads((art/'identities.json').read_text());assert len(ids)==2 and {i['build'] for i in ids}=={'ee014909137e03706e0b3020b8396be589aaa705'}
assert len({i['boot_id'] for i in ids})==2 and len({i['device_id'] for i in ids})==2
raw={};snapshots={}
for case in expected:
 logs=sorted(art.glob('*-'+case+'-*.log'));assert logs,case
 errors=[]
 for p in logs:
  rc=int(p.with_suffix('.rc').read_text());output=p.read_text()
  if rc:errors.append(dict(file=p.name,returncode=rc,reason_lines=[l for l in output.splitlines() if l.startswith('>>> why ')]))
 raw[case]={'commands':len(logs),'nonzero_commands':errors}
 if case.startswith('PL001'):
  v=json.loads((art/(case+'-membership.json')).read_text());assert 'STATE=ok' in v['stdout'];snapshots[case]=v
 if case.startswith('PL002'):
  v=json.loads((art/(case+'-old-writer.json')).read_text());target='/ROCKNIX' if case.endswith('-join') else '/pixelelated'
  assert v['partial']['SAVES_REMOTE']==target+'/Saves' and v['partial']['SETTINGS_REMOTE']!=target+'/Backups'
  assert all(v['after'][k]==target+'/'+suffix for k,suffix in [('SAVES_REMOTE','Saves'),('SETTINGS_REMOTE','Backups'),('CONTENT_REMOTE','Content')]);snapshots[case]=v
expected_reasons={'PL003-unreadable-active-sibling':('YOUR CLOUD STOPPED ANSWERING',3),'PL005-record-write-retry':("YOUR CLOUD SYNC SETTINGS COULDN'T BE SAVED",1),'PL005-marker-write-retry':("SOME FILES DIDN'T FINISH",1),'PL005-real-closed-endpoint':('YOUR CLOUD STOPPED ANSWERING',1)}
for case,(reason,n) in expected_reasons.items():
 errors=raw[case]['nonzero_commands'];assert len(errors)==n,(case,errors)
 assert all('>>> why '+reason in e['reason_lines'] for e in errors),(case,errors)
hashes={}
for guest in ['a','b']:
 by_phase={}
 for phase in ['setup','final-custody']:
  values={}
  for p in art.glob('*-'+phase+'-'+guest+'.log'):
   for digest,name in re.findall(r'^([0-9a-f]{64})\s+/usr/bin/(cloud_migrate_layout|cloud_scan|cloud_setup|cloud_content_restore)$',p.read_text(),re.M):values[name]=digest
  assert len(values)==4,(phase,guest,values);by_phase[phase]=values
 assert by_phase['setup']==by_phase['final-custody'];hashes[guest]=by_phase['setup']
assert hashes['a']==hashes['b']
dest=qa/'supplemental02-acceptance';dest.mkdir()
receipt=dict(verified_utc=datetime.now(timezone.utc).isoformat(),result='PASS',cases=rows,command_evidence=raw,membership_and_recovery=snapshots,installed_hashes=hashes,scope='Ten renewed installed CLI acceptance cases on candidate16, source-defined refusal/preservation/retry and mount restoration assertions. UI and full clean/upgrade qualification remain separate. Original prelaunch01 failure remains failed.')
(dest/'acceptance.json').write_text(json.dumps(receipt,indent=2)+'\n')
print('PASS ten supplemental cases, exact reasons, predecessor pointer recovery, independent guests and installed hash custody')

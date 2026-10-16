#!/usr/bin/env python3
"""Read original #614 evidence only; start no guest or service."""
import hashlib,json,tarfile
from pathlib import Path
R=Path(__file__).resolve().parent
rows=json.loads((R/'original-records.json').read_text())
with tarfile.open(R/'original-records.tar.gz','r:gz') as archive:
 assert len(archive.getmembers())==len(rows)==761
 for row in rows:
  raw=archive.extractfile(row['path']).read();assert len(raw)==row['bytes'] and hashlib.sha256(raw).hexdigest()==row['sha256'],row['path']
 def read(name):return archive.extractfile('owner/'+name).read().decode()
 def obj(name):return json.loads(read(name))
 clean=obj('clean/report.json');assert clean['status']=='pass' and clean['blocked_count']==clean['error_count']==0
 assert obj('extra/repeat-result.json')==json.loads((R/'repeat-result.json').read_text())
 initial=obj('responses/070-cleanup-diagnosis.json')['output'];assert 'ExecMainStatus=1' in initial and 'FileNotFoundError' in initial and '/proc/pressure/memory' in initial
 assert obj('responses/068-guest-cleanup.json')['status']=='FAIL'
 for member in archive.getnames():
  if member.startswith('owner/responses/1'):assert json.loads(archive.extractfile(member).read())['status']=='PASS',member
 for name in ['100-baseline','107-qemu-escape-before','112-qemu-escape-after','123-instant-uinput-before','126-instant-uinput-after','137-normal-close-before','140-normal-close-after','151-phone-handler-before','154-phone-handler-after']:
  text=obj('responses/'+name+'.json')['output'];assert 'OBSERVER_ARMED=' in text
  snap=json.loads(next(x for x in text.splitlines() if x.startswith('{')))
  assert [(p['pid'],p['start']) for p in snap['processes'] if p['exe']=='emulationstation']==[(2387,9057)]
  assert snap['hashes']['/usr/bin/cloud-signin-window']=='6cbc445686d3d484ff20450342776e9eb92b47f6112a0352be1a50b334eef81b'
  assert snap['hashes']['/usr/bin/emulationstation']=='76f18d97a46e9228ca4b7cb63a5406a4f0bb026f96763f3558d1ac942b1857c8'
  assert snap['hashes']['/usr/bin/cloud_oauth']=='95c626f8df07faef522683a857e48e31f85a58c6f738bcde24707574dc24d293'
 for case in [1,2,4]:assert '(65307)' in read(f'extra/guest-evidence/qa614/case{case}-window.log')
 inputs=[json.loads(x) for x in read('extra/guest-evidence/qa614/input.jsonl').splitlines()]
 for device in ['/dev/input/event2','/dev/input/event7','/dev/input/event5']:assert any(x.get('device')==device and x.get('code')==1 and x.get('value')==1 for x in inputs)
 page=[json.loads(x) for x in read('extra/guest-evidence/qa614/page-events.jsonl').splitlines()]
 for key in ['q','v']:assert any(x['kind']=='keydown-capture' and x['key']==key and x['trusted'] and x['active']=='field' for x in page)
 assert sum(x['kind']=='input' and x['length']==1 and x['trusted'] for x in page)==2
 cleanup=obj('extra/guest-evidence/qa614/cleanup-result.json');assert cleanup['rc']==0 and cleanup['observer']['error'] is None and cleanup['observer']['stopped'] and not cleanup['observer']['guards']
 assert cleanup['rclone_restored'] and not cleanup['kernel_failures']
 last=obj('responses/201-cleanup-census.json')['output'];snap=json.loads(next(x for x in last.splitlines() if x.startswith('{')));assert len(snap['processes'])==1 and all('cloud' not in n.lower() for n in snap['keyboard_names'])
result=json.loads((R/'repeat-result.json').read_text());assert result['status']=='PASS' and len(result['cases'])==4
close=json.loads(result['cases'][2]['action'].splitlines()[0]);assert close['original_rc']==0 and close['browser_pid_gone'] and close['elapsed']<1 and not close['guard']
exits=json.loads((R/'host-exits.json').read_text());assert all(v==0 for v in exits['original_channels'].values())
consumed=json.loads((R/'admission-consumed.json').read_text());assert consumed['state']=='consumed'
retired=json.loads((R/'retirement.json').read_text());assert retired['allocated_bytes_recovered']==2481815552
for row in json.loads((R/'frame-index.json').read_text())['frames']:assert hashlib.sha256((R/row['path']).read_bytes()).hexdigest()==row['sha256']
print('PASS: 761 immutable originals; four guarded cases; preserved observer failure; same frontend; cleanup/consumption/retirement; nine reviewed frames')

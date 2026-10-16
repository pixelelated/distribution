from pathlib import Path
import hashlib,json,tarfile,io
D=Path(__file__).resolve().parent
expected=json.loads((D/'original-sha256.json').read_text())
with tarfile.open(D/'originals.tar.gz','r:gz') as t:
 fs={m.name:t.extractfile(m).read() for m in t.getmembers() if m.isfile()}
assert set(fs)==set(expected) and len(fs)==34
assert all(hashlib.sha256(fs[n]).hexdigest()==h for n,h in expected.items())
def j(n):return json.loads(fs[n])
units=j('units.json')
for name,rc in [('pix-qa615-observer',0),('pix-qa615-attempt1',1),('pix-qa61502-observer',1),('pix-qa61502-loaded-escape',1),('pix-qa61503-observer',0),('pix-qa61503-normal-close',0)]:
 assert 'MainPID=0\n' in units[name] and f'ExecMainStatus={rc}\n' in units[name]
a=j('pix-qa615/attempt1-result.json');assert a['actions'][0]['pressed'] and not a['actions'][0]['live_after'] and 'TypeError' in a['error']
i=[json.loads(x) for x in fs['pix-qa615/input.jsonl'].splitlines()];assert {x['value'] for x in i if x.get('code')==1}=={0,1}
b=j('pix-qa61502/loaded-escape-result.json');assert not b['actions'] and 'browser_closed_before_input' in b['error']
g=j('pix-qa61502/guard.jsonl');assert g['reason']=='low_memory' and 30<g['at']-b['observed']<42
c=j('pix-qa61503/normal-close-result.json');assert len(c['actions'])==1 and c['actions'][0]['rc']==0 and not c['live_final'] and not c['guards'] and c['actions'][0]['elapsed']<3
p=json.loads((D/'preservation.json').read_text());assert p['safe_file_count']==163 and p['safe_bytes']==25549175
for key in ['boot_id','files','safe_payload','settings','local_recovery','hooks','unit_overrides','markers','temporaries','scan']:assert p[key] is True
r=json.loads((D/'cleanup-readback.json').read_text());assert r['temporary_roots_absent'] and r['failed_units_empty'] and r['processes']==[{'pid':2696,'exe':'emulationstation','start':'5810'}]
for f in json.loads((D/'frame-index.json').read_text())['frames']:
 data=(D/f['file']).read_bytes();assert data[:8]==b'\x89PNG\r\n\x1a\n' and hashlib.sha256(data).hexdigest()==f['sha256'] and f['reviewed']
print('PASS: 34 immutable originals; failures retained; early input/exit and normal close separated from pressure guard; preservation and final cleanup; six reviewed frames. Loaded-page Escape remains inconclusive.')

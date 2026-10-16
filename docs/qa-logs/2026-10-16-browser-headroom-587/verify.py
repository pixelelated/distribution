from pathlib import Path
import hashlib,json,gzip,subprocess,sys,tarfile
R=Path(__file__).resolve().parent
for line in (R/'SHA256SUMS').read_text().splitlines():
 h,n=line.split('  ',1);assert hashlib.sha256((R/n).read_bytes()).hexdigest()==h,n
manifest=json.loads((R/'originals/original-records.json').read_text())
with tarfile.open(R/'originals/original-records.tar.gz') as t:
 assert {m.name for m in t.getmembers()}=={x['path'] for x in manifest}
 for row in manifest:
  raw=t.extractfile(row['path']).read();assert len(raw)==row['bytes'] and hashlib.sha256(raw).hexdigest()==row['sha256'],row['path']
def read(n):return json.loads((R/'originals'/n).read_text())
assert read('matrix-result.json')['status']=='PASS' and len(read('matrix-result.json')['cases'])==4
assert all(c['status']=='PASS' for c in read('matrix-result.json')['cases'])
assert all(v==0 for v in read('host-exits.json')['original_channels'].values())
cleanup=read('cleanup-result.json');assert cleanup['rc']==0 and cleanup['observer']['rc']==0 and not cleanup['observer']['guards'] and not cleanup['installed_changed'] and not cleanup['kernel_failures']
assert all(v['expected']==v['actual'] for v in cleanup['protected'].values())
busy=read('busy-stop.json');assert busy['stop_rc']==0 and 'Result=timeout' in busy['unit'] and 'ExecMainStatus=9' in busy['unit'] and busy['elapsed']>=15
assert busy['pending']==read('expected-pending.json') and busy['chain'][0] and busy['integrity']=='ok'
recovery=read('recovery.json');assert recovery['status']=='PASS' and recovery['pending']==[] and recovery['integrity']=='ok'
assert read('admission-consumed.json')['state']=='consumed'
assert read('retirement.json')['allocated_bytes_recovered']==2412744704
actual=json.loads(subprocess.check_output([sys.executable,'-I',str(R/'analyze.py')],text=True));assert actual==json.loads((R/'analysis.json').read_text())
assert all(c['samples']==6 and not c['psi_available'] for c in actual['cases'])
print('PASS: four normal browser cases; busy-stop timeout preserved; synthetic recovery; exact analysis; original exits/cleanup/retirement verified. No production-stop or H700 qualification.')

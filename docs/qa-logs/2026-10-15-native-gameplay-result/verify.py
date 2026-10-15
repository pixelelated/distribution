#!/usr/bin/env python3
"""Static compact-evidence verification only; no extraction, runtime or mutation."""
from pathlib import Path
import gzip,hashlib,json,tarfile
P=Path(__file__).resolve().parent
sha=lambda b:hashlib.sha256(b).hexdigest()
def archive(name,index):
    rows=json.loads((P/index).read_text());result={}
    with tarfile.open(P/name) as t:
        members=t.getmembers()
        assert len(members)==len(rows)==len({r['path'] for r in rows})
        assert all(m.isfile() for m in members)
        assert {m.name for m in members}=={r['path'] for r in rows}
        for r in rows:
            b=t.extractfile(r['path']).read()
            assert len(b)==r['bytes'] and sha(b)==r['sha256'],r['path']
            result[r['path']]=b
    return result
host=archive('original-records.tar.gz','original-records.json')
failed=archive('failed-export-originals.tar.gz','failed-export-originals.tar.gz.members.json')
guest=archive('selected-guest-originals.tar.gz','selected-guest-originals.tar.gz.members.json')
supp=archive('supplemental-readback.tar.gz','supplemental-readback.tar.gz.members.json')
assert len(host)==846 and len(guest)==304 and len(supp)==45
manifest=gzip.decompress((P/'guest-export-manifest.json.gz').read_bytes())
assert sha(manifest)=='6e3e308f6dccb4d9aa58a69182d4f6893e2cfc50a551611aa4b340e0c8d1db94'
rows=json.loads(manifest);assert len(rows)==len({r['path'] for r in rows})==10954
by={r['path']:r for r in rows}
for n,b in guest.items():assert by[n]['bytes']==len(b) and by[n]['sha256']==sha(b)
assert sha(supp['SHA256SUMS'])=='b5058c830def636dad41690807e81a9fdf1e9240f8f89f227798473800854fd6'
for line in supp['SHA256SUMS'].decode().splitlines():
    h,n=line.split('  ',1);assert sha(supp[n])==h
accept=json.loads((P/'acceptance.json').read_text());consumed=json.loads((P/'admission-consumed.json').read_text())
assert consumed['state']=='consumed' and consumed['evidence_sha256']==sha((P/'acceptance.json').read_bytes())
assert consumed['id']=='ebed7b8ebcc040f2ae09acdf7531f8ab' and accept['disposition']=='qualified'
lookup={
 '/workspace/tmp/pix-m7-native-gameplay-20261015-03/coordinator-native03-review.json':(P/'coordinator-native03-review.json').read_bytes(),
 '/workspace/tmp/pix-m7-native-gameplay-20261015-03/vm-result.json':host['owner/vm-result.json'],
 '/workspace/tmp/pix-m7-native-gameplay-evidence-20261015-03/export-result.json':failed['export/export-result.json'],
 '/workspace/tmp/pix-m7-native-gameplay-evidence-20261015-03/host-exits.json':failed['export/host-exits.json'],
 '/workspace/tmp/pix-m7-native-gameplay-evidence-20261015-03/guest/guest-export-manifest.json':manifest}
lookup.update({'/tmp/pix-m7-native-gameplay-postreadback-20261015/'+n:b for n,b in supp.items()})
for r in accept['evidence']:assert sha(lookup[r['path']])==r['sha256'],r['path']
assert json.loads(host['run/runner-result.json'])['command_rc']==0
assert failed['failed-export-run/build.rc']==b'1\n'
er=json.loads(failed['failed-export-run/runner-result.json'])
assert (er['command_rc'],er['runner_rc'],er['monitor_rc'])==(1,1,0)
assert not json.loads(failed['export/export-result.json'])['guest_manifest_verified']
assert failed['export/guest-manifest.json']==b'[]\n'
frames=json.loads((P/'reviewed-frame-index.json').read_text())
original_reviews=json.loads(host['owner/visual-result.json'])['reviews'];assert len(frames)==len(original_reviews)==66
for r,o in zip(frames,original_reviews):
    assert all(r[k]==v for k,v in o.items())
    assert sha(host[r['retained_member']])==r['sha256']
config=json.loads(host['owner/config.json'])
for n,h in config['source'].items():assert sha(host['owner/source/'+n])==h
for n,h in config['code'].items():assert sha(host['owner/'+n])==h
seal=(P/'SHA256SUMS').read_text().splitlines();listed={}
for line in seal:
    h,n=line.split('  ',1);assert sha((P/n).read_bytes())==h,n;listed[n]=h
assert set(listed)=={str(p.relative_to(P)) for p in P.rglob('*') if p.is_file() and p.name!='SHA256SUMS'}
print(json.dumps({'status':'READY','static_only':True,'host_members':len(host),'selected_guest_members':len(guest),'supplement_members':len(supp),'reviewed_frames':len(frames),'full_original_manifest_rows':len(rows),'original_export_rc':1,'scope':accept['scope'],'seal_sha256':sha((P/'SHA256SUMS').read_bytes())},indent=2))

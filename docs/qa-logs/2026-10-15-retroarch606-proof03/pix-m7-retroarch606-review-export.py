from pathlib import Path
import argparse,base64,datetime,hashlib,json,tarfile
p=argparse.ArgumentParser();p.add_argument('--owner',type=Path,required=True);p.add_argument('--export',dest='out',type=Path,required=True);a=p.parse_args();o,e=a.owner,a.out
load=lambda p:json.loads(p.read_text());sha=lambda b:hashlib.sha256(b).hexdigest()
run=Path((o/'run.path').read_text().strip());rows=load(e/'original-records.json')
with tarfile.open(e/'original-records.tar.gz','r:gz') as t:
 assert len(t.getmembers())==len(rows)
 assert {m.name for m in t.getmembers()}=={r['path'] for r in rows}
 for r in rows:
  b=t.extractfile(r['path']).read();assert len(b)==r['bytes'] and sha(b)==r['sha256']
  prefix,rel=r['path'].split('/',1);src=(o if prefix=='owner' else run)/rel
  assert src.read_bytes()==b
ends=load(e/'host-exits.json');vm=load(o/'vm-result.json')
assert ends['channels_coherent'] and ends['original_channels']['monitor']==0
assert not vm['cleanup_errors'] and not vm['surviving_host_processes'] and not vm['remaining_host_children'] and not vm['qemu_still_live']
for pid in set(ends['pids_exited']+[r['pid'] for r in ends['qemu_identities']]):assert not Path('/proc',str(pid)).exists()
proof=load(o/'records/retroarch-proof.json');observations=[]
for f in sorted((o/'records').glob('*-retroarch-*-report.json')):
 r=load(f);obs=r.get('observation',r.get('last_observation',{}));ps=obs.get('processes',[])
 engines=[(x['pid'],x['start_ticks']) for x in ps if Path(x['exe']).name in ['retroarch','retroarch32']]
 if engines:assert len(engines)==1;observations.append({'report':f.name,'engine':engines[0],'core_sha256':obs['core_file']['sha256']})
assert observations and len({tuple(x['engine']) for x in observations})==1 and len({x['core_sha256'] for x in observations})==1
for f in (o/'records').glob('snapshot-*.json'):
 r=load(f)
 for row in r['observation']['states']:
  if row.get('exists'):
   b=base64.b64decode(row['bytes_b64'],validate=True);assert len(b)==row['bytes'] and sha(b)==row['sha256']
   if row['path'].endswith('.srm'):assert b[0]==0x55
result={'result':'VERIFIED_EXACT_ORIGINALS','verified_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'owner':str(o),'run':str(run),'members':len(rows),'bytes':sum(r['bytes'] for r in rows),'original_channels':ends['original_channels'],'proof_status':proof['status'],'one_engine_identity':observations[0]['engine'],'engine_observations':observations,'archive_sha256':sha((e/'original-records.tar.gz').read_bytes()),'state_bytes_independently_verified':True,'actual_exit_save_acceptance':False}
with (e/'root-original-review.json').open('x') as f:json.dump(result,f,indent=2);f.write('\n')
print(json.dumps({k:v for k,v in result.items() if k!='engine_observations'}))

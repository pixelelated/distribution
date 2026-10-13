"""Read-only arithmetic over prior #570 samples; no new runtime measurement."""
import gzip,hashlib,json,sys
from pathlib import Path
p=Path(sys.argv[1]); data=p.read_bytes(); trials=json.loads(gzip.decompress(data));results={}
for name,rows in trials.items():
 cpu={};seconds=0;es=[];overlap=[]
 for row in rows:
  if any(x['exe']=='cloud-signin-window' for x in row['processes']):
   overlap.append(row)
   es.extend(x['pss'] for x in row['processes'] if x['exe']=='emulationstation')
 for before,after in zip(rows,rows[1:]):
  if not all(any(x['exe']=='cloud-signin-window' for x in r['processes']) for r in (before,after)):continue
  seconds+=after['mono']-before['mono']
  old={(x['pid'],x['start']):x for x in before['processes']}
  for x in after['processes']:
   prior=old.get((x['pid'],x['start']))
   if prior and x['tag']==prior['tag']:
    delta=x['cpu']-prior['cpu']
    if delta<0:raise ValueError('CPU counter reversed')
    cpu[x['tag']]=cpu.get(x['tag'],0)+delta
 web=[x for row in overlap for x in row['processes'] if x['exe']=='WebKitWebProcess']
 results[name]={'overlap_adjacent_seconds':seconds,'es_pss_min_kib':min(es),'es_pss_max_kib':max(es),'cpu_ticks_by_tag':dict(sorted(cpu.items(),key=lambda x:-x[1])), 'webprocess_peak_pss_kib':max(x['pss'] for x in web),'webprocess_peak_anon_kib':max(x['anon'] for x in web),'minimum_available_kib':min(r['mem']['MemAvailable'] for r in overlap)}
print(json.dumps({'evidence':'reanalysis of historical samples, not a new VM run','input':str(p),'sha256':hashlib.sha256(data).hexdigest(),'limitations':['CPU ticks are not seconds: actual CLK_TCK was not recorded','Only adjacent observed PID+start counters; unobserved short-lived process CPU excluded','Only periods with browser in both samples; initial launch overlap not fully captured','Peak per-process values need not coincide; do not sum them as peak total','ES memory includes live allocations; retained PSS is not potential savings','Observer overhead not independently measured'],'cases':results},indent=2))

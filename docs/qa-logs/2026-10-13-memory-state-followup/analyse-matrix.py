import json,gzip,statistics,hashlib
from pathlib import Path
r=Path(__file__).resolve().parent;summary={};allsamples={};allmetrics={}
for name in ['run02-sham1','run02-trim1','run02-trim2','run02-sham2']:
 d=r/name
 if not (d/'result.json').exists():continue
 result=json.loads((d/'result.json').read_text());assert result['rc']==0 and result['sampler_rc']==0 and not result['guarded']
 rows=[json.loads(x) for x in gzip.decompress((d/'samples.jsonl.gz').read_bytes()).decode().splitlines()]
 assert json.loads((d/'sampler-result.json').read_text())['rc']==0
 p=result['probe'];start=p['mono_ns']/1e9;es_pid=p['pid'];overlap=[x for x in rows if any(z['exe']=='cloud-signin-window' for z in x['processes'])];settled=[x for x in overlap if start+10<=x['mono']<=start+60]
 es=[z for x in settled for z in x['processes'] if z['pid']==es_pid];web=[z for x in overlap for z in x['processes'] if z['exe']=='WebKitWebProcess'];cpu={}
 for a,b in zip(rows,rows[1:]):
  if not all(any(z['exe']=='cloud-signin-window' for z in x['processes']) for x in (a,b)):continue
  old={(z['pid'],z['start']):z for z in a['processes']}
  for z in b['processes']:
   q=old.get((z['pid'],z['start']))
   if q and q['tag']==z['tag']:cpu[z['tag']]=cpu.get(z['tag'],0)+z['cpu']-q['cpu']
 page=json.loads((d/'page-metrics.json').read_text());allmetrics[name]=page;allsamples[name]=rows
 summary[name]={'mode':result['mode'],'pss_released_kib':p['pss_before_kib']-p['pss_after_kib'],'anon_released_kib':p['anon_before_kib']-p['anon_after_kib'],'trim_ms':p['duration_ns']/1e6,'settled_es_pss_median_kib':statistics.median(z['pss'] for z in es),'settled_es_anon_median_kib':statistics.median(z['anon'] for z in es),'minimum_available_kib':min(x['mem']['MemAvailable'] for x in overlap),'web_peak_pss_kib':max(z['pss'] for z in web),'web_peak_anon_kib':max(z['anon'] for z in web),'reclaim_deltas':{k:overlap[-1]['vmstat'][k]-overlap[0]['vmstat'][k] for k in overlap[0]['vmstat']},'cpu_ticks':cpu,'CLK_TCK':100,'heartbeat_max_ms':max(z['page']['heartbeatMax'] for z in page),'evaluation_max_ms':max(z['eval_ms'] for z in page),'page_load_seen':any(z['page']['ready']=='complete' for z in page),'psi_available':any(x.get('memory_psi_available') for x in rows),'samples':len(rows),'unchanged_boot_es':result['before']==result['after'],'probe_only_in_es':result['probe_mapping_pids']==result['before']['es']}
print(json.dumps(summary,indent=2))

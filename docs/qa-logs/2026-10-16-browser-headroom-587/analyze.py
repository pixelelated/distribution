from pathlib import Path
import collections,gzip,hashlib,json,statistics
R=Path(__file__).resolve().parent
# Analysis consumes exported originals only; it launches no runtime.
rows=[json.loads(x) for x in gzip.decompress((R/'originals/guest-samples.jsonl.gz').read_bytes()).decode().splitlines()]
m=json.loads((R/'originals/matrix-result.json').read_text())
def stats(a):return {'min':min(a),'median':statistics.median(a),'max':max(a)} if a else None
out={'units':'KiB for memory; seconds for timing','cases':[]}
for c in m['cases']:
 phase=f"{c['number']}-{c['state']}-steady";all_rows=[r for r in rows if r['phase']==phase]
 rr=[r for r in all_rows if any(x['pid']==c['browser']['pid'] and x['start']==c['browser']['start'] and x.get('Pss') is not None for x in r['processes'])]
 proxy_pid={1:2733,4:7322}.get(c['number']);groups=collections.defaultdict(list)
 for r in rr:
  for group,predicate in [('proxy',lambda x:x['pid']==proxy_pid),('observer',lambda x:x['pid']==r['observer_pid']),('ES',lambda x:x['exe']=='emulationstation'),('browser_family',lambda x:x['exe']=='cloud-signin-window' or 'WebKit' in x['exe'])]:
   groups[group].append(sum(x.get('Pss') or 0 for x in r['processes'] if predicate(x)))
 first={x.split()[0]:int(x.split()[1]) for x in rr[0]['vmstat'].splitlines()};last={x.split()[0]:int(x.split()[1]) for x in rr[-1]['vmstat'].splitlines()}
 out['cases'].append({'case':c['number'],'proxy':c['state'],'samples':len(rr),'excluded_post_close_samples':len(all_rows)-len(rr),'available_kib':stats([r['mem']['MemAvailable'] for r in rr]),'pss_kib':{k:stats(v) for k,v in groups.items()},'sampling_wall_seconds':stats([r['sampling_seconds'] for r in rr]),'psi_available':any(r['psi'] is not None for r in rr),'counter_deltas':{k:last[k]-v for k,v in first.items() if k.startswith(('pgscan','pgsteal','allocstall','pgmajfault','pswp'))},'readiness_observed_seconds':c['readiness_observed_seconds']})
a=statistics.mean(c['available_kib']['median'] for c in out['cases'] if c['proxy']=='active');s=statistics.mean(c['available_kib']['median'] for c in out['cases'] if c['proxy']=='stopped');out['difference_of_condition_mean_medians_kib']=s-a
out['mem_total_kib']=rows[0]['mem']['MemTotal'];out['cma_total_kib']=rows[0]['mem']['CmaTotal'];out['swap_total_kib']=rows[0]['mem']['SwapTotal'];out['limits']=['Two runs per condition, reordered active/stopped/stopped/active; not randomized or a population estimate.','Samples tagged steady after page paint evidence; exclude samples after exact browser PID/start disappears.','Guest PSI unavailable; guard used MemAvailable and deadline only.','Observer PSS and smaps sampling wall time measured; complete polling CPU cost and short-lived serial controller overhead not isolated.','Fixed128MiB typed-array local page; no real provider, login, H700 hardware or large-cache claim.','Proxy PSS is exact systemd MainPID, not all Python processes.','Initial online slow-response stop is separate from memory matrix.']
print(json.dumps(out,indent=2))

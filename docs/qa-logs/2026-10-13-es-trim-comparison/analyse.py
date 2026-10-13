from pathlib import Path
import json,tarfile,statistics,hashlib
r=Path('/workspace/tmp/pix570-es-compare-20261013');data=[]
for name in ['baseline1','candidate1','candidate2','baseline2']:
 d=r/name
 if not (d/'result.json').exists():continue
 result=json.loads((d/'result.json').read_text());pid=result['before']['pid'];start=result['before']['start'];launch=result['launch_wall_ms']
 with tarfile.open(d/'guest.tgz') as t:rows=[json.loads(x) for x in t.extractfile('./samples.jsonl').read().splitlines()]
 samples=[]
 for row in rows:
  ps=[p for p in row['processes'] if p['pid']==pid and p['start']==start];assert len(ps)==1
  samples.append({'t':(row['wall_ms']-launch)/1000,'es':ps[0],'mem':row['mem'],'vmstat':row['vmstat']})
 early=[s for s in samples if 2<=s['t']<=6];assert len(early)>=2
 settled=[s for s in samples if 10<=s['t']<=55]
 data.append({'name':name,'mode':result['mode'],'original_rc':result['rc'],'sampler_rc':result['sampler_rc'],'boot':result['before']['boot'],'pid':pid,'binary_sha256':result['before']['sha256'],'last_sample_s_after_launch':samples[-1]['t'],'observed_samples':len(samples),'min_available_kib':min(s['mem']['MemAvailable'] for s in samples),'window2to6_sample_count':len(early),'window2to6_es_anon_median_kib':statistics.median(s['es']['anon'] for s in early),'window2to6_es_pss_median_kib':statistics.median(s['es']['pss'] for s in early),'settled10to55_sample_count':len(settled),'settled10to55_es_anon_median_kib':statistics.median(s['es']['anon'] for s in settled) if settled else None,'raw_sha256':hashlib.sha256((d/'guest.tgz').read_bytes()).hexdigest()})
summary={'schema':1,'comparison':'actual binaries; no interposer or modified browser','window_note':'2–6seconds after recorded launch chosen after first baseline guard to compare shared early lifetimes. Whole-case minima and stopped lifetimes remain separate; not a speed or peak-browser efficiency comparison.','cases':data}
if len(data)==4:
 old=[x['window2to6_es_anon_median_kib'] for x in data if x['mode']=='baseline'];new=[x['window2to6_es_anon_median_kib'] for x in data if x['mode']=='candidate'];summary.update(es_anon_median_difference_kib=statistics.median(old)-statistics.median(new),pairwise_range_kib=[min(old)-max(new),max(old)-min(new)])
(r/'analysis.json').write_text(json.dumps(summary,indent=2)+'\n');print(json.dumps(summary,indent=2))

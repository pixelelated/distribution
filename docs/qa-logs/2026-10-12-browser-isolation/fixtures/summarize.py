from pathlib import Path
import json,hashlib,statistics,shutil,datetime
r=Path(__file__).parent;d=Path.cwd()/'docs/qa-logs/2026-10-12-browser-isolation'
names=[x[0] for x in json.loads((r/'cases.json').read_text())]+['public-gst-supplied','public-virgl'];rows=[];samples={}
for name in names:
 x=json.loads((r/(name+'.json')).read_text())
 browser=lambda s:[p for p in s['processes'] if p['exe']!='emulationstation']
 rows.append(dict(case=name,seconds=x['seconds'],loaded='load finished' in x['log'],peak_browser_pss_kib=max(sum(p['pss_kib'] for p in browser(s)) for s in x['samples']),peak_browser_rss_kib=max(sum(p['rss_kib'] for p in browser(s)) for s in x['samples']),minimum_available_kib=min(s['mem']['MemAvailable'] for s in x['samples']),initial_available_kib=x['before']['mem']['MemAvailable'],after_5_seconds_available_kib=x['after']['mem']['MemAvailable'],web_processes_remaining_at_5_seconds=len(x['orphans']),error=x['error'],library_pss=x['library_pss'],settings=x['extra']))
 samples[name]=[dict(t=s['t'],available_kib=s['mem']['MemAvailable'],memtotal_kib=s['mem']['MemTotal'],processes=[{k:v for k,v in p.items() if k!='pid'} for p in s['processes']]) for s in x['samples']]
(d/'vm-summary.json').write_text(json.dumps(rows,indent=2)+'\n');(d/'vm-samples.json').write_text(json.dumps(samples,indent=2)+'\n')
es=json.loads((r/'events.json').read_text());heartbeats=[]
for name in [x for x in names if x.startswith('synthetic')]:
 e=[x for x in es if x['query']['run']==[name]];gaps=[b['t']-a['t'] for a,b in zip(e,e[1:]) if a['query']['n']==b['query']['n']]
 heartbeats.append(dict(case=name,pages=sorted({int(x['query']['n'][0]) for x in e}),events=len(e),median_same_page_gap_seconds=statistics.median(gaps),maximum_same_page_gap_seconds=max(gaps),same_page_gaps_over_two_seconds=sum(v>2 for v in gaps)))
(d/'heartbeat-summary.json').write_text(json.dumps(heartbeats,indent=2)+'\n')
consumption=[]
for name in ['boot-owner','boot-owner02','matrix-owner','gst-owner','device-owner','graphics-owner','graphics-owner02']:
 x=json.loads((r/name/'launcher-result.json').read_text());assert not Path('/proc',str(x['pid'])).exists()
 consumption.append(dict(owner=name,rc=x['runner_returncode'],exited=True,utc=x['utc'],failure_reason=('unsupported --qa before launch' if name=='boot-owner' else 'worktree monitor lock before launch' if name=='graphics-owner' else None)))
(d/'consumption.json').write_text(json.dumps(consumption,indent=2)+'\n')
frames=[dict(file=str(p.relative_to(d)),sha256=hashlib.sha256(p.read_bytes()).hexdigest(),review='reviewed native compositor: intended public page or synthetic page3',scope='diagnostic; not an ES flow baseline or host scanout qualification') for p in sorted((d/'frames').glob('*.png'))]
(d/'frames.json').write_text(json.dumps(frames,indent=2)+'\n')
print('\n'.join(f"{x['case']}: PSS {x['peak_browser_pss_kib']/1024:.1f} MiB; available {x['minimum_available_kib']/1024:.1f} MiB" for x in rows))

from pathlib import Path
import csv,datetime,hashlib,json
p=Path('/workspace/tmp/pixelelated-m7-memory-12');out=p/'artifacts'
assert json.loads((p/'completion.json').read_text())['job_rc']==0
checks={}
for name,count in [('virgl-10',10),('software-10',10),('software-sync-50',50)]:
 d=out/name;r=json.loads((d/'result.json').read_text());rows=list(csv.DictReader((d/'cycles.csv').open()));assert len(rows)==count+6
 assert len({row['pid'] for row in rows})==1 and int(rows[-1]['cycle'])==count+5
 base,last=rows[5],rows[-1]
 v=int(last['vmsize_kib'])-int(base['vmsize_kib']);rss=int(last['vmrss_kib'])-int(base['vmrss_kib'])
 assert v==r['vmsize_growth_kib'] and rss==r['rss_growth_kib'] and r['passed'] and v<1024 and rss<2048
 checks[name]=r
stamps=sorted((out/'software-sync-50').glob('*.exit-sync'));assert len(stamps)==55
texts=[f.read_text().strip() for f in stamps];assert len(set(texts))==55
assert all(t.split()[1:3]==['0','completed'] for t in texts)
frames=[];timing=[]
for t in sorted(out.glob('rocknix-images/qa-*/time-to-play/time-to-play.json')):
 d=json.loads(t.read_text());assert not d['headline_missing'] and not d['over_budget'] and not d['surface']['scaled'];assert d['surface']['surface']=='533x480' and d['surface']['panel']=='640x480'
 x=dict(path=str(t),launch_s=d['cells']['launch'][0]['t_first_game_frame'],exit_sync_s=d['cells']['exit'][0]['t_sync_stamp'],g2g_s=d['cells']['g2g'][0]['t_second_game_frame'],g2g_stamp=d['cells']['g2g'][0]['stamp'],surface=d['surface']);timing.append(x)
 for name in ['r1-launch-02-first-game-frame','g1-exit-002','g1-exit-game2','r1-exit-007','r1-exit-000']:
  f=t.parent/'frames'/(name+'.png');frames.append(dict(path=str(f),sha256=hashlib.sha256(f.read_bytes()).hexdigest(),observation='Directly viewed: emulator startup/auto-state transition or returned ES carousel, as named. Early transition samples are not settled widget-layout proof.',passed=True))
assert len(timing)==2 and len(frames)==10
r=dict(utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),passed=True,method='Recomputed growth from original cycle CSVs and checked every distinct completed exit-sync stamp; direct view_image of ten timing frames.',memory=checks,exit_sync_stamps=55,measured_cycles=70,warmup_cycles=15,frames=frames,timing=timing,limitations=['One timing repeat per profile is a smoke sample, not a performance distribution.','Both fast g2g samples lack a new sync stamp and do not prove launch during active sync.','First-frame pictures show emulator startup/auto-state transitions; not a settled widget-layout assessment.','533x480 GPU viewport fills640x480panel height with aspect sidebars, per existing surface check.'])
with (p/'visual-review.json').open('x') as f:f.write(json.dumps(r,indent=2)+'\n')
with (out/'timing-review.json').open('x') as f:f.write(json.dumps(dict(timing=timing,limitations=r['limitations']),indent=2)+'\n')
print(json.dumps(dict(passed=True,measured_cycles=70,successful_stamps=55,reviewed_frames=10)))

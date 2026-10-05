"""Five alternating exit-sync samples per layout; separate HTTP-call trace."""
from pathlib import Path
common=Path(__file__).with_name('archive-proof.py').read_text()
exec(compile(common.split('bid=guest(')[0],'<retained QA helpers>','exec'))
import statistics
check(guest("sed -n 's/^BUILD_ID=//p' /etc/os-release").strip('"')=='72121fd03a558725328ea58c092faf1b3324317f','exact pixelelated BUILD_ID')
guest('systemctl stop essway; set_setting cloudsaves.startup 0; set_setting cloudsaves.gameexit 0; mkdir -p /storage/roms/nes')
config=subprocess.check_output(['./tools/cloud-test-backend','rclone-conf'],text=True).rstrip()+'\n'
guest('mkdir -p /storage/.config/rclone\numask 077\ncat > /storage/.config/rclone/rclone.conf <<\'M7_QA_CONFIG\'\n'+config+'M7_QA_CONFIG\n',record=False)
subprocess.run(['./tools/cloud-test-backend','reset'],check=True,stdout=subprocess.DEVNULL)
for root in ['ROCKNIX','pixelelated']:
    for sub in ['Saves/nes','Backups']:(data/root/sub).mkdir(parents=True,exist_ok=True)
    (data/root/'Saves/nes/Fleet.srm').write_bytes(b'owned existing fleet save\n')
command='/usr/bin/cloud_backup --yes --saves-only --recent --automatic'
def configure(label):
    root='/ROCKNIX' if label=='legacy' else '/pixelelated'
    conf(root+'/Saves',root+'/Backups',root+'/Content')
def timestamp_valid(local_ns, previous_remote_ns):
    return previous_remote_ns is None or local_ns > previous_remote_ns + 1_000_000_000
# Meaningful negative controls: these same-size writes are not beyond the comparison window.
assert not timestamp_valid(1_000_000_000,1_000_000_000)
assert not timestamp_valid(1_999_999_999,1_000_000_000)
assert not timestamp_valid(2_000_000_000,1_000_000_000)
assert timestamp_valid(3_000_000_000,1_000_000_000)
(out/'timestamp-controls.json').write_text(json.dumps({'same_time_refused':True,'within_window_refused':True,'at_boundary_refused':True,'later_accepted':True})+'\n')
def sample(label,measured):
    time.sleep(1.15)
    configure(label)
    remote=data/('ROCKNIX' if label=='legacy' else 'pixelelated')/'Saves/nes/Bench.srm'
    previous_ns=remote.stat().st_mtime_ns if remote.exists() else None
    # Wait on the guest's actual clock. Never set either clock or force a future mtime.
    code='''import pathlib,time,os,json
previous=PREVIOUS
if previous is not None:
 deadline=time.monotonic()+30
 while time.time_ns()<=previous+2_000_000_000:
  assert time.monotonic()<deadline,'guest clock failed to cross upload boundary'
  time.sleep(.1)
p=pathlib.Path('/storage/roms/nes/Bench.srm');p.write_bytes(os.urandom(2000))
print(json.dumps({'mtime_ns':p.stat().st_mtime_ns,'guest_epoch_ns':time.time_ns()}))
'''.replace('PREVIOUS',repr(previous_ns))
    before=json.loads(guest('python3 - <<\'PY\'\n'+code+'\nPY',record=False))
    row={'layout':label,'measured':measured,'previous_remote_mtime_ns':previous_ns,'local_mtime_ns':before['mtime_ns'],'timestamp_boundary_valid':timestamp_valid(before['mtime_ns'],previous_ns)}
    with (out/'all-samples.jsonl').open('a') as f:f.write(json.dumps(dict(row,phase='before-command'))+'\n')
    assert row['timestamp_boundary_valid'],row
    result=guest('s=$(date +%s%N)\nset +e\n'+command+' > /tmp/m7-bench-last.log 2>&1\nr=$?\ne=$(date +%s%N)\nprintf "M7_SAMPLE=%s,%s\\n" "$(( (e-s)/1000000 ))" "$r"\nexit 0')
    m=re.search(r'M7_SAMPLE=(\d+),(\d+)',result);assert m,result
    row.update(milliseconds=int(m[1]),rc=int(m[2]),sentinel_sha256=sha('/storage/roms/nes/Bench.srm'))
    row['remote_sha256']=hashlib.sha256(remote.read_bytes()).hexdigest() if remote.is_file() else None
    row['remote_mtime_ns']=remote.stat().st_mtime_ns if remote.is_file() else None
    row['cloud_bytes_match']=row['sentinel_sha256']==row['remote_sha256']
    with (out/'all-samples.jsonl').open('a') as f:f.write(json.dumps(dict(row,phase='after-command'))+'\n')
    print('SAMPLE '+json.dumps(row),flush=True)
    if row['rc']!=0 or not row['cloud_bytes_match']:
        safe=guest("grep -v -i -E 'key|pass|token|user|psk' /tmp/m7-bench-last.log || true",record=False)
        (out/'failed-sample-outcome.log').write_text(safe+'\n')
        guest('sync')
    assert row['rc']==0,row
    assert row['cloud_bytes_match'],'sync did not transfer changed bytes'
    return row

source=Path('/workspace/repos/rocknix.worktrees/m7-pixelelated-replacement08/projects/ROCKNIX/packages/network/rclone/sources/cloud_backup')
check(sha('/usr/bin/cloud_backup')==hashlib.sha256(source.read_bytes()).hexdigest(),'installed cloud_backup matches frozen reviewed source without override')
guest('rm -f /storage/.cache/cloud_sync/last-backup /storage/roms/nes/Bench.srm')
warm=[sample(x,False) for x in ['legacy','current']]
j0=int(guest('journalctl -b -t cloud_migrate_layout --no-pager | wc -l'))
rows=[]
for i in range(5):
 for label in (['legacy','current'] if i%2==0 else ['current','legacy']):
  rows.append(sample(label,True))
  (out/'installed-samples.json').write_text(json.dumps({'warmup':warm,'measured':rows},indent=2)+'\n')
j1=int(guest('journalctl -b -t cloud_migrate_layout --no-pager | wc -l'))
medians={x:statistics.median([r['milliseconds'] for r in rows if r['layout']==x]) for x in ['legacy','current']}
delta=abs(medians['legacy']-medians['current'])
summary={'medians_ms':medians,'absolute_delta_ms':delta,'limit_ms':30,'migration_journal_delta':j1-j0,'source_sha256':sha('/usr/bin/cloud_backup')}
(out/'comparison.json').write_text(json.dumps(summary,indent=2)+'\n')
print('RESULT '+json.dumps(summary),flush=True)
check(j1==j0,'no migration preparation during measured syncs')
check(delta<=30,'installed legacy/current five-sample median difference within unchanged30ms limit')
print('PASS installed exact-byte alternating exit-sync timing',flush=True)

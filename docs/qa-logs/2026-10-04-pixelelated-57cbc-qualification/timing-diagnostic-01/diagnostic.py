"""Five alternating exit-sync samples per layout; separate HTTP-call trace."""
from pathlib import Path
common=Path(__file__).with_name('archive-proof.py').read_text()
exec(compile(common.split('bid=guest(')[0],'<retained QA helpers>','exec'))
import statistics
check(guest("sed -n 's/^BUILD_ID=//p' /etc/os-release").strip('"')=='57cbc9b981205328444d41f6c4237dc9f5736d7f','exact pixelelated BUILD_ID')
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
def sample(label,measured):
    time.sleep(1.15)  # Outside measurement: WebDAV upload-time precision is one second.
    configure(label)
    result=guest('head -c 2000 /dev/urandom > /storage/roms/nes/Bench.srm\ns=$(date +%s%N)\nset +e\n'+command+' > /tmp/m7-bench-last.log 2>&1\nr=$?\ne=$(date +%s%N)\nprintf "M7_SAMPLE=%s,%s\\n" "$(( (e-s)/1000000 ))" "$r"\nexit 0')
    m=re.search(r'M7_SAMPLE=(\d+),(\d+)',result);assert m,result
    row={'layout':label,'measured':measured,'milliseconds':int(m[1]),'rc':int(m[2])}
    assert row['rc']==0,row
    remote=data/('ROCKNIX' if label=='legacy' else 'pixelelated')/'Saves/nes/Bench.srm'
    row['sentinel_sha256']=sha('/storage/roms/nes/Bench.srm')
    assert hashlib.sha256(remote.read_bytes()).hexdigest()==row['sentinel_sha256'], 'sync did not transfer changed bytes'
    row['cloud_bytes_match']=True
    print('SAMPLE '+json.dumps(row),flush=True);return row



source=Path('/workspace/repos/rocknix.worktrees/m7-pixelelated-replacement06/projects/ROCKNIX/packages/network/rclone/sources/cloud_backup')
check(sha('/usr/bin/cloud_backup')==hashlib.sha256(source.read_bytes()).hexdigest(),'unchanged installed script before diagnostic')
results=[]
for batch in range(3):
 guest('rm -f /storage/.cache/cloud_sync/last-backup /storage/roms/nes/Bench.srm')
 warm=[sample(x,False) for x in ['legacy','current']]
 rows=[]
 j0=int(guest('journalctl -b -t cloud_migrate_layout --no-pager | wc -l'))
 for i in range(5):
  for label in (['legacy','current'] if (i+batch)%2==0 else ['current','legacy']):
   rows.append(sample(label,True))
 j1=int(guest('journalctl -b -t cloud_migrate_layout --no-pager | wc -l'))
 medians={x:statistics.median([r['milliseconds'] for r in rows if r['layout']==x]) for x in ['legacy','current']}
 result={'batch':batch+1,'warmup':warm,'measured':rows,'medians_ms':medians,'delta_ms':abs(medians['legacy']-medians['current']),'journal_delta':j1-j0}
 results.append(result);(out/'fixed-three-batches.json').write_text(json.dumps(results,indent=2)+'\n')
 check(j1==j0,'diagnostic batch has no migration preparation')
 print('DIAGNOSTIC BATCH '+json.dumps({k:v for k,v in result.items() if k not in ['warmup','measured']}),flush=True)
# Isolate the extra required listing's process/network cost without changing product bytes.
listing=guest('for i in 1 2 3 4 5 6 7 8 9 10; do s=$(date +%s%N); /usr/bin/rclone lsf --dirs-only qa-cloud:/ROCKNIX/ --contimeout 15s --timeout 30s --low-level-retries 3 --retries 1 >/dev/null; e=$(date +%s%N); echo $(( (e-s)/1000000 )); done')
(out/'isolated-parent-listing-ms.json').write_text(json.dumps({'milliseconds':[int(x) for x in listing.splitlines()]},indent=2)+'\n')
# Instrumented diagnostics are excluded from all timing batches; raw expanded commands stay private.
trace_summaries={}
for label in ['legacy','current']:
 configure(label)
 guest("umask 077; mkdir -p /storage/.cache/m7-timing-private; head -c 2000 /dev/urandom >/storage/roms/nes/Bench.srm\nPS4='+${EPOCHREALTIME} ${FUNCNAME[0]:-main}:${LINENO}: ' bash -x "+command+" >/tmp/m7-traced-outcome.log 2>/storage/.cache/m7-timing-private/trace-"+label+".log",record=False)
 code=r'''import pathlib,re,json
+p=pathlib.Path('/storage/.cache/m7-timing-private/trace-LABEL.log');s=p.read_text()
+rows=[]
+for line in s.splitlines():
+ m=re.match(r'^\++(\d+\.\d+) ([A-Za-z_][A-Za-z_0-9]*):([0-9]+): (.*)$',line)
+ if m:rows.append((float(m[1]),m[2],int(m[3]),m[4]))
+summary=[]
+for i,(stamp,fn,ln,cmd) in enumerate(rows):
+ if fn in ('rclone','logged_moved','bucket_dir_listed','superseded_saves_setting'):
+  duration=(rows[i+1][0]-stamp)*1000 if i+1<len(rows) else 0
+  summary.append({'function':fn,'line':ln,'next_trace_delta_ms':round(duration,3),'operation':cmd.split()[0] if cmd else ''})
+print(json.dumps({'raw_bytes':len(s),'parsed_rows':len(rows),'steps':summary}))
+'''.replace('\n+','\n').replace('LABEL',label)
 info=json.loads(guest('python3 - <<\'PY\'\n'+code+'\nPY',record=False));trace_summaries[label]=info
 check(info['parsed_rows']>0,'bash trace parsed for '+label)
(out/'safe-trace-summary.json').write_text(json.dumps(trace_summaries,indent=2)+'\n')
check(sha('/usr/bin/cloud_backup')==hashlib.sha256(source.read_bytes()).hexdigest(),'unchanged installed script after diagnostic')
print('COMPLETE predeclared diagnostic samples; assess every batch, not only the best',flush=True)

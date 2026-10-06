from pathlib import Path
from datetime import datetime,timezone
import argparse,hashlib,json,runpy
repo=Path.cwd();owner=Path('/workspace/tmp/pixelelated-m7-partial-record-control-01');owner.mkdir()
module=runpy.run_path(str(repo/'tools/rasteratops-cloud-layout-test'),run_name='qa_control')
args=argparse.Namespace(ref=None,rclone='/workspace/repos/rocknix.worktrees/m7-pixelelated-replacement15/build.pixelelated-GENERIC_X64.x86_64/image/system/usr/bin/rclone')
rows=[]
for stage in ['Backups','Content']:
    f=module['Fixture'](owner/stage,args)
    try:
        module['truncated_migration_retry'](f,stage=stage,kind='no-record')
        row=dict(stage=stage,result='REFUSAL PASS')
    except AssertionError as e:
        row=dict(stage=stage,result='REFUSAL FAIL',why=str(e))
    rows.append(row);print(json.dumps(row),flush=True)
assert rows[0]['result']=='REFUSAL PASS' and rows[1]['result']=='REFUSAL FAIL',rows
(owner/'control.json').write_text(json.dumps(dict(utc=datetime.now(timezone.utc).isoformat(),source_sha256=hashlib.sha256((repo/'projects/ROCKNIX/packages/network/rclone/sources/cloud_migrate_layout').read_bytes()).hexdigest(),rows=rows,scope='First source repair distinguishes active state but not a record loaded from a prior invocation. Content preflight follows begin-record creation, so it incorrectly admits a same-prefix destination without an earlier record. No deployed change; strengthen before integration.'),indent=2)+'\n')

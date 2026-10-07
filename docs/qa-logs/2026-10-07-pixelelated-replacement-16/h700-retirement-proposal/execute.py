#!/usr/bin/env python3
"""Fixed reviewed QA-file batch. Default is verification only; never root."""
from pathlib import Path
from datetime import datetime, timezone
import argparse, hashlib, json, os, stat, subprocess

ALLOWED = frozenset(('/workspace/tmp/pixelelated-m7-boot-qualification-06/clean-640.qcow2', '/workspace/tmp/pixelelated-m7-boot-qualification-07/clean-640.qcow2', '/workspace/tmp/pixelelated-m7-p4-build16-partial-retry-1280x800-02/guest-d.qcow2', '/workspace/tmp/pixelelated-m7-p4-build16-partial-retry-640x480-01/guest-d.qcow2', '/workspace/tmp/pixelelated-m7-p4-build16-partial-retry-640x480-02/guest-d.qcow2', '/workspace/tmp/pixelelated-m7-p4-build16-recovery-1280x800-01/guest-d.qcow2', '/workspace/tmp/pixelelated-m7-p4-build16-recovery-640x480-01/guest-d.qcow2', '/workspace/tmp/pixelelated-m7-p4-build16-root-reasons-1280x800-01/guest-d.qcow2', '/workspace/tmp/pixelelated-m7-p4-build16-root-reasons-640x480-01/guest-d.qcow2', '/workspace/tmp/pixelelated-m7-p4-cloud-ui-fixes-02/guest-d.qcow2', '/workspace/tmp/pixelelated-m7-p4-cloud-ui-fixes-04/guest-d.qcow2', '/workspace/tmp/pixelelated-m7-p4-coverage-ui-03/guest-d.qcow2', '/workspace/tmp/pixelelated-m7-p4-coverage-ui-04/guest-d.qcow2', '/workspace/tmp/pixelelated-m7-p4-coverage-ui-05/guest-d.qcow2', '/workspace/tmp/pixelelated-m7-p4-fresh-root-06/guest-d.qcow2', '/workspace/tmp/pixelelated-m7-p4-fresh-root-07/guest-d.qcow2', '/workspace/tmp/pixelelated-m7-p4-library-fixes-01/guest-d.qcow2', '/workspace/tmp/pixelelated-m7-p4-library-fixes-02/guest-d.qcow2', '/workspace/tmp/pixelelated-m7-p4-presentation-fixes-01/guest-d.qcow2', '/workspace/tmp/pixelelated-m7-p4-recovery-ui-fixes-03/guest-d.qcow2', '/workspace/tmp/pixelelated-m7-p4-recovery-ui-fixes-05/guest-d.qcow2', '/workspace/tmp/pixelelated-m7-p4-recovery-ui-fixes-06/guest-d.qcow2'))
parser=argparse.ArgumentParser(description=__doc__)
parser.add_argument('--owner',required=True,type=Path)
parser.add_argument('--apply',action='store_true')
parser.add_argument('--approved-plan-sha')
a=parser.parse_args();owner=a.owner.resolve(strict=True)
assert os.getuid()!=0 and owner.is_relative_to('/workspace/tmp')
proposal_path=Path(__file__).with_name('proposal.json')
def digest(p):
 with Path(p).open('rb') as f:return hashlib.file_digest(f,'sha256').hexdigest()
def identity(p):
 s=Path(p).lstat()
 return dict(device=s.st_dev,inode=s.st_ino,size=s.st_size,mtime_ns=s.st_mtime_ns,allocated_bytes=s.st_blocks*512,uid=s.st_uid,links=s.st_nlink,mode=s.st_mode)
def available():
 s=os.statvfs('/workspace');return s.f_bavail*s.f_frsize
proposal=json.loads(proposal_path.read_text());proposal_sha=digest(proposal_path)
assert {x['path'] for x in proposal['targets']}==ALLOWED and len(ALLOWED)==22
assert not (owner/'execution.json').exists()
report_path=Path(proposal['source_report'])
assert digest(report_path)==proposal['source_report_sha256']
plan=Path(proposal['plan']);assert digest(plan)==proposal['plan_sha256']
tool=Path('/workspace/repos/rocknix.worktrees/conflict-resolution/tools/host-maintenance/retention-report')
assert digest(tool)==proposal['report_tool_sha256']
if a.apply:
 assert a.approved_plan_sha==proposal_sha,'Separate explicit approval of this proposal is required'
 approval=json.loads((owner/'approval.json').read_text())
 assert approval['approved_plan_sha256']==proposal_sha and approval['source']=='explicit maintainer approval'
 # A fresh full-root read is required for mutation; an old report is not a reservation.
 report_path=owner/'fresh-report.json'
 subprocess.run(['python3','-I',str(tool),'--plan',str(plan),'--output',str(report_path)],check=True)
report=json.loads(report_path.read_text())
assert not report['inventory']['errors'] and not report['inventory']['active']
assert digest(tool)==report['tool_sha256'] and report['plan_sha256']==proposal['plan_sha256']
assert (datetime.now(timezone.utc)-datetime.fromisoformat(report['utc'])).total_seconds()<900
fresh={x['path']:x for x in report['candidates']}
for row in proposal['targets']:
 p=Path(row['path']);assert str(p.resolve())==row['path']
 assert fresh[row['path']]['eligible'] and fresh[row['path']]['sha256']==row['sha256']
 assert identity(p)==row['identity'] and digest(p)==row['sha256']
 assert stat.S_ISREG(p.lstat().st_mode) and p.lstat().st_nlink==1 and p.lstat().st_uid==os.getuid()
for kept in proposal['protected']:assert identity(kept['path'])==kept['identity']
for kept in proposal['held']:assert identity(kept['path'])==kept['identity'] and digest(kept['path'])==kept['sha256']
preserved_evidence={item['path']:item['sha256'] for c in json.loads(plan.read_text())['candidates'] if c['path'] in ALLOWED for item in c['evidence']}
for path,sha in preserved_evidence.items():assert digest(path)==sha
required=proposal['builds'][0]['required_bytes'];before=available()
assert before+proposal['expected_reclaim_bytes']>=required
(owner/'verification.json').write_text(json.dumps(dict(utc=datetime.now(timezone.utc).isoformat(),result='PASS',proposal_sha256=proposal_sha,files=22,report=str(report_path),report_sha256=digest(report_path),available_bytes=before,deletion_performed=False),indent=2)+'\n')
if not a.apply:
 print('PASS verification only: 22 exact disks, protected identities and held bases; no deletion')
 raise SystemExit(0)
removed=[]
try:
 for row in proposal['targets']:
  p=Path(row['path']);assert identity(p)==row['identity'];p.unlink();removed.append(row['path'])
finally:
 after=available()
 (owner/'execution.json').write_text(json.dumps(dict(utc=datetime.now(timezone.utc).isoformat(),approved_plan_sha256=proposal_sha,removed=removed,before_available_bytes=before,after_available_bytes=after,observed_recovery_bytes=after-before),indent=2)+'\n')
assert set(removed)==ALLOWED and all(not Path(p).exists() for p in ALLOWED)
for kept in proposal['protected']:assert identity(kept['path'])==kept['identity']
for kept in proposal['held']:assert identity(kept['path'])==kept['identity'] and digest(kept['path'])==kept['sha256']
for path,sha in preserved_evidence.items():assert digest(path)==sha
assert after>=required
print('PASS approved exact batch; protected roots and held bases unchanged; H700 arm budget available')

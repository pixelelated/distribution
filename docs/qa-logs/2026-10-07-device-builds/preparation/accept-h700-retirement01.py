from pathlib import Path
from datetime import datetime, timezone
import hashlib, json, os

owner = Path('/workspace/tmp/pixelelated-m7-h700-qa-retirement-01')
proposal_path = Path('docs/qa-logs/2026-10-07-pixelelated-replacement-16/h700-retirement-proposal/proposal.json')
proposal = json.loads(proposal_path.read_text())
verification = json.loads((owner / 'owner-verification.json').read_text())
assert verification['result'] == 'PASS' and verification['sealed_inputs'] == 7
execution = json.loads((owner / 'execution.json').read_text())
approval = json.loads((owner / 'approval.json').read_text())
sha = hashlib.sha256(proposal_path.read_bytes()).hexdigest()
assert approval['approved_plan_sha256'] == execution['approved_plan_sha256'] == sha
targets = {r['path'] for r in proposal['targets']}
assert len(targets) == 22 and set(execution['removed']) == targets
assert all(not os.path.lexists(p) for p in targets)
report = json.loads((owner / 'fresh-report.json').read_text())
assert not report['inventory']['errors'] and not report['inventory']['active']
assert all(r['eligible'] for r in report['candidates'] if r['path'] in targets)

def identity(p):
    s = Path(p).lstat()
    return dict(device=s.st_dev, inode=s.st_ino, size=s.st_size, mtime_ns=s.st_mtime_ns,
                allocated_bytes=s.st_blocks*512, uid=s.st_uid, links=s.st_nlink, mode=s.st_mode)

def digest(p):
    with Path(p).open('rb') as f:
        return hashlib.file_digest(f, 'sha256').hexdigest()

for kept in proposal['protected']:
    assert identity(kept['path']) == kept['identity']
for kept in proposal['held']:
    assert identity(kept['path']) == kept['identity'] and digest(kept['path']) == kept['sha256']
plan = json.loads(Path(proposal['plan']).read_text())
evidence = {r['path']: r['sha256'] for c in plan['candidates'] if c['path'] in targets for r in c['evidence']}
for p, expected in evidence.items():
    assert digest(p) == expected
fs = os.statvfs('/workspace'); available = fs.f_bavail * fs.f_frsize
assert available >= proposal['builds'][0]['required_bytes']
receipt = {'utc': datetime.now(timezone.utc).isoformat(), 'result': 'PASS',
    'proposal_sha256': sha, 'exact_files_removed': len(targets),
    'protected_identities_verified': len(proposal['protected']),
    'held_base_hashes_verified': len(proposal['held']),
    'independent_evidence_hashes_verified': len(evidence),
    'available_bytes': available, 'required_arm_bytes': proposal['builds'][0]['required_bytes'],
    'recorded_recovery_bytes': execution['observed_recovery_bytes'],
    'fresh_report_sha256': digest(owner / 'fresh-report.json'),
    'scope': 'Approved exact #491 batch only. H700 arm fit verified; no aarch64/SM8550 capacity claim.'}
with (owner / 'acceptance.json').open('x') as f:
    json.dump(receipt, f, indent=2); f.write('\n')
print(json.dumps(receipt))

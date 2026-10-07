from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import os
import subprocess
import sys

owner = Path(__file__).resolve().parent
repo = Path('/workspace/repos/rocknix.worktrees/conflict-resolution')
primary = Path('/workspace/repos/rocknix')
assert Path.cwd() == primary
(owner / 'run.path').write_text(str(primary / os.environ['RASTERATOPS_BUILD_RUN']) + '\n')
rc = 1
env = dict(os.environ, TMPDIR=str(owner / 'tmp'), ES_SRC='/home/max/Development/emulationstation-next.worktrees/qa-integration')

def git(where, *args):
    return subprocess.check_output(['git', '-C', str(where), *args], text=True).strip()

def run(label, cwd, command):
    with (owner / (label + '.log')).open('x') as out:
        result = subprocess.run(command, cwd=cwd, env=env, stdout=out, stderr=subprocess.STDOUT)
    assert result.returncode == 0, label + ' failed; read retained log'
    print('PASS ' + label, flush=True)

try:
    for path, sha in json.loads((owner / 'seal.json').read_text()).items():
        assert hashlib.sha256(Path(path).read_bytes()).hexdigest() == sha
    assert git(repo, 'rev-parse', 'HEAD') == '06e66dd1d6788f85c99fae0b53ad790b500c81f9'
    assert git(primary, 'rev-parse', 'HEAD') == '96c877f617d82a35cb09e93f6408b8fea76142ea'
    assert git(primary, 'branch', '--show-current') == 'next'
    assert not git(primary, 'status', '--porcelain')
    assert not git(repo, 'diff', '--cached', '--name-only')
    for tool in ['rules-check', 'register-check']:
        run(tool, repo, [str(repo / 'tools' / tool)])
    run('work-log-index', repo, [str(repo / 'tools/work-log-index'), '--check'])
    run('audit-resolution', repo, [str(repo / 'tools/lint-audit-artifacts'), 'docs/audits/2026_10_06-milestone-m7-p4-fixes-383', '--phase', 'resolution'])
    run('diff-check', repo, ['git', 'diff', '--check'])
    run('ceremony', repo, [str(repo / 'tools/ceremony-check')])
    paths = ['tools/ceremony-check', 'tools/host-maintenance', 'docs/qa-logs/2026-10-07-audit-cadence', 'docs/audits/2026_10_06-milestone-m7-p4-fixes-383/audit-completion.json', 'docs/audits/2026_10_06-milestone-m7-p4-fixes-383/08-installed-resolution.md', 'docs/audits/2026_10_06-milestone-m7-p4-fixes-383/10-closure-reconciliation.md', 'docs/audits/2026_10_06-milestone-m7-p4-fixes-383/evidence/remediation-host/build16-integration-commands.json', 'docs/audits/2026_10_06-milestone-m7-p4-fixes-383/05-punch-list.md', 'tools/pixelelated-vm-cloud-boundaries', 'docs/audits/2026_10_06-milestone-m7-p4-fixes-383/09-remaining-evidence.md', '.github/sessions/saved-session-state-next.md', '.github/sessions/saved-session-state-feature-conflict-resolution.md', '.github/sessions/archived', 'docs/audits/2026_10_06-milestone-m7-p4-fixes-383/00-running-log.md', 'docs/audits/2026_10_06-milestone-m7-p4-fixes-383/07-remediation-progress.md', 'docs/qa-logs/2026-10-07-pixelelated-replacement-16', 'docs/decision-register.md', 'docs/friction-log.md', 'docs/rasteratops/release-readiness.md', 'docs/work-logs/2026_10-work_logs/2026_10_07-work_log.md', 'docs/work-logs/2026_10-work_logs/2026-W40-summary.md', 'docs/work-logs/INDEX.md']
    subprocess.run(['git', '-C', str(repo), 'add', '--', *paths], check=True)
    changed = git(repo, 'diff', '--cached', '--name-only').splitlines()
    assert changed and all((p.startswith(('docs/', '.github/sessions/', 'tools/host-maintenance/')) or p in ['tools/pixelelated-vm-cloud-boundaries', 'tools/ceremony-check']) for p in changed)
    (owner / 'changed-paths.json').write_text(json.dumps(changed, indent=2) + '\n')
    run('commit', repo, ['git', 'commit', '-F', str(owner / 'message.txt')])
    feature = git(repo, 'rev-parse', 'HEAD')
    run('integration', primary, ['git', 'cherry-pick', '-x', feature])
    nex = git(primary, 'rev-parse', 'HEAD')
    for label, where, branch, sha in [('feature', repo, 'feature/conflict-resolution', feature), ('next', primary, 'next', nex)]:
        run(label + '-push', where, ['git', 'push', 'origin', sha + ':refs/heads/' + branch])
        assert git(where, 'ls-remote', 'origin', 'refs/heads/' + branch).split()[0] == sha
    def tree(sha):
        data = subprocess.check_output(['git', '-C', str(repo), 'ls-tree', '-r', '-z', sha])
        return {r.split(b'\t', 1)[1]: r.split(b'\t', 1)[0] for r in data.split(b'\0') if r}
    a, b = tree(feature), tree(nex)
    for name in changed:
        assert a.get(os.fsencode(name)) == b.get(os.fsencode(name)), name
    assert not list((owner / 'tmp').iterdir())
    receipt = dict(verified_utc=datetime.now(timezone.utc).isoformat(), feature=feature, next=nex, changed_paths=len(changed), changed_paths_equal=True, remote_refs_verified=True, normal_hooks=True, scope='Complete read-only retention reports, exact pinned source-fixture classification with nineteen controls, independent same-disk/evidence reconciliation and the guarded twenty-two-file cleanup proposal. Verification-only helper passes; no deletion or device build, separate approval required for #491.')
    (owner / 'publication.json').write_text(json.dumps(receipt, indent=2) + '\n')
    print(json.dumps(receipt), flush=True)
    rc = 0
finally:
    (owner / 'inner.rc').write_text(str(rc) + '\n')
    (owner / 'outer.rc').write_text(str(rc) + '\n')
sys.exit(rc)

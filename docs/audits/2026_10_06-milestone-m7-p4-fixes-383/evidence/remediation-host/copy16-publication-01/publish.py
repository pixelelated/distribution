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
    assert git(repo, 'rev-parse', 'HEAD') == '86f793ea3cc6e551e756175db38a64cd9830cffc'
    assert git(primary, 'rev-parse', 'HEAD') == '4b312e784f425947defd906a15650b5e0ec0f8ea'
    assert git(primary, 'branch', '--show-current') == 'next'
    assert not git(primary, 'status', '--porcelain')
    assert not git(repo, 'diff', '--cached', '--name-only')
    for tool in ['rules-check', 'register-check']:
        run(tool, repo, [str(repo / 'tools' / tool)])
    run('work-log-index', repo, [str(repo / 'tools/work-log-index'), '--check'])
    run('audit-pre-issue', repo, [str(repo / 'tools/lint-audit-artifacts'), 'docs/audits/2026_10_06-milestone-m7-p4-fixes-383', '--phase', 'pre-issue'])
    run('pkgcheck', repo, [str(repo / 'tools/pkgcheck'), 'emulationstation'])
    run('diff-check', repo, ['git', 'diff', '--check'])
    paths = ['projects/ROCKNIX/packages/network/rclone/sources/cloud_migrate_layout', 'projects/ROCKNIX/packages/ui/emulationstation/package.mk', 'tools/rasteratops-cloud-layout-test', 'docs/cloud-sync-changelog.md', '.github/sessions/saved-session-state-next.md', 'docs/audits/2026_10_06-milestone-m7-p4-fixes-383', 'docs/qa-logs/2026-10-06-pixelelated-replacement-15', 'docs/friction-log.md', 'docs/work-logs/2026_10-work_logs/2026_10_06-work_log.md', 'docs/work-logs/INDEX.md', 'docs/rasteratops/release-readiness.md', 'docs/qa-logs/2026-10-05-build-storage/failed-pair-retirement-proposal-20261006']
    subprocess.run(['git', '-C', str(repo), 'add', '--', *paths], check=True)
    changed = git(repo, 'diff', '--cached', '--name-only').splitlines()
    assert changed and all(p.startswith(('docs/', '.github/sessions/')) or p in paths[:3] for p in changed)
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
    receipt = dict(verified_utc=datetime.now(timezone.utc).isoformat(), feature=feature, next=nex, changed_paths=len(changed), changed_paths_equal=True, remote_refs_verified=True, normal_hooks=True, scope='Owner-requested interruption-copy English/French correction and full ES pin, exact source checks, retained fixture closures and reviewable two-file capacity proposal. No disk deletion/newbuild; installed16 proof and cleanup approval pending.')
    (owner / 'publication.json').write_text(json.dumps(receipt, indent=2) + '\n')
    print(json.dumps(receipt), flush=True)
    rc = 0
finally:
    (owner / 'inner.rc').write_text(str(rc) + '\n')
    (owner / 'outer.rc').write_text(str(rc) + '\n')
sys.exit(rc)

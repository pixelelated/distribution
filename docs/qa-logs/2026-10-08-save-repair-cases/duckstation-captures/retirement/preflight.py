#!/usr/bin/env python3
"""Bounded retirement readback for the one completed #523 build owner."""
from pathlib import Path
import datetime
import hashlib
import json
import os
import subprocess

owner = Path('/workspace/repos/rocknix.worktrees/m7-duckstation-deps01')
packet = Path(__file__).resolve().parents[1]
out = Path(__file__).resolve().parent
product = Path('/workspace/repos/rocknix.worktrees/m7-manual-cloud-folders')
assert owner.is_dir() and not owner.is_symlink()

def git(root, *args):
    return subprocess.check_output(['git', '-C', str(root), *args], text=True).strip()

def hashed(path):
    return {'path': str(path), 'sha256': hashlib.sha256(path.read_bytes()).hexdigest(),
            'bytes': path.stat().st_size, 'mode': oct(path.stat().st_mode & 0o777)}

skip = set()
pid = os.getpid()
while pid and pid not in skip:
    skip.add(pid)
    try:
        pid = int(next(line.split()[1] for line in Path(f'/proc/{pid}/status').read_text().splitlines()
                       if line.startswith('PPid:')))
    except (OSError, StopIteration):
        break
matches = []
unreadable = []
for proc in Path('/proc').iterdir():
    if not proc.name.isdigit() or int(proc.name) in skip:
        continue
    try:
        command = (proc / 'cmdline').read_bytes()
        cwd = (proc / 'cwd').resolve()
        executable = (proc / 'exe').resolve()
        prefix = str(owner) + '/'
        if str(owner).encode() in command or str(cwd).startswith(prefix) or cwd == owner or str(executable).startswith(prefix):
            matches.append({'pid': int(proc.name), 'comm': (proc / 'comm').read_text().strip(),
                            'cwd': str(cwd), 'executable': str(executable)})
    except PermissionError:
        unreadable.append(int(proc.name))
    except (OSError, RuntimeError):
        pass

watchers = {}
for run in sorted((owner / '.build-runs').iterdir()):
    if run.is_dir():
        watchers[run.name] = {name: (run / name).read_text().strip() for name in ['build.rc', 'build.status'] if (run / name).exists()}
protected = []
inputs = json.loads((packet / 'dependency-toolchain-inputs.json').read_text())
for row in inputs['files']:
    p = Path(row['path'])
    if owner not in p.parents:
        assert hashed(p)['sha256'] == row['sha256']
        protected.append(hashed(p))
    else:
        accepted = Path(str(p).replace(str(owner), '/workspace/repos/rocknix.worktrees/m7-pixelelated-replacement16', 1))
        protected.append(hashed(accepted))
protected.append(hashed(Path('/workspace/cache/rocknix-sources/libcom-err/libcom-err-1.47.4.tar.xz')))
protected.append(hashed(product / 'projects/ROCKNIX/packages/emulators/standalone/duckstation-sa/package.mk'))
artifacts = json.loads((packet / 'dependency-build/target-artifacts.json').read_text())
for row in artifacts['artifacts']:
    assert hashed(Path(row['path']))['sha256'] == row['sha256']
space = os.statvfs('/workspace')
result = {
    'utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
    'owner': str(owner), 'owner_realpath': str(owner.resolve()),
    'owner_commit': git(owner, 'rev-parse', 'HEAD'), 'owner_branch': git(owner, 'branch', '--show-current'),
    'tracked_changes': git(owner, 'status', '--porcelain', '--untracked-files=no'),
    'untracked': git(owner, 'ls-files', '--others', '--exclude-standard'),
    'retired_artifact_roots': [str(p) for p in sorted(owner.iterdir()) if p.name.startswith('build.') or p.name == 'sources'],
    'live_owner_processes': matches, 'unreadable_process_count': len(unreadable),
    'watchers': watchers, 'protected_inputs': protected,
    'target_artifact_hashes_verified': len(artifacts['artifacts']),
    'product_commit': git(product, 'rev-parse', 'HEAD'),
    'owner_allocated_bytes': int(subprocess.check_output(['du', '-s', '-B1', str(owner)], text=True, timeout=30).split()[0]),
    'workspace_available_bytes': space.f_bavail * space.f_frsize,
    'removal_command': ['tools/fork-worktree', 'remove', str(owner), '--force'],
}
(out / 'preflight.json').write_text(json.dumps(result, indent=2) + '\n')
assert not matches, 'live owner process found; do not remove'
assert result['owner_commit'] == 'dda2a04aaf411b8bc13aedf5ce44ff33ce4b3d3a'
assert result['owner_branch'] == 'build/m7-duckstation-deps01'
assert not result['tracked_changes']
assert result['untracked'] == 'dependency-owner.json'
assert all(v.get('build.rc') == '0' for v in watchers.values())
assert result['product_commit'] == '052771f05d841fb91fa818198f8f4e0ad83affb8'
print(json.dumps({'owner': str(owner), 'live_owner_processes': matches,
                  'watchers_terminal': len(watchers), 'target_artifacts_verified': 6,
                  'allocated_bytes': result['owner_allocated_bytes'], 'preflight': 'PASS'}))

#!/usr/bin/env python3
"""Create a source-only merge probe in a new private Git object store.

No shared reference, index, worktree, hook or accepted producer is changed.
The returned tree is NOT an accepted or publishable candidate, even when clean.
"""
import datetime
import hashlib
import json
import os
from pathlib import Path
import subprocess
import tempfile

COORDINATOR = '71bee11968b8a2f3b0165004f21c5498a47a6054'
NEXT = '8ebaf8daad8eaac6331dff6fc048fb4411d7decb'
M7 = '41b5287311476efd076bf6f9efca0cc94099fbec'
M7_PRODUCT = '1850362563dc02720f1910faa415ed96580fa7d2'
STORES = ['/workspace/repos/pixelelated/distribution/.git/objects',
          '/workspace/repos/rocknix/.git/objects']
PARENT = Path('/workspace/tmp/m6-coordinator')
OUT = Path(__file__).resolve().parent / 'candidate-probe'

def now():
    return datetime.datetime.now(datetime.timezone.utc).isoformat()

def sha(value):
    return hashlib.sha256(value).hexdigest()

def main():
    assert not OUT.exists(), 'Preserve the first run; use a separately named continuation.'
    assert PARENT.is_dir() and not PARENT.is_symlink()
    OUT.mkdir()
    env = dict(os.environ, GIT_CONFIG_NOSYSTEM='1', GIT_CONFIG_GLOBAL='/dev/null',
               GIT_NO_REPLACE_OBJECTS='1', GIT_TERMINAL_PROMPT='0', LC_ALL='C')
    for key in ('GIT_DIR', 'GIT_WORK_TREE', 'GIT_INDEX_FILE', 'GIT_OBJECT_DIRECTORY',
                'GIT_ALTERNATE_OBJECT_DIRECTORIES', 'GIT_CONFIG_COUNT'):
        env.pop(key, None)
    commands = []

    def run(argv, expected=(0,), timeout=180):
        started = now()
        result = subprocess.run(argv, capture_output=True, env=env, timeout=timeout)
        row = dict(argv=argv, started_utc=started, ended_utc=now(), exit=result.returncode,
                   stdout_sha256=sha(result.stdout), stderr_sha256=sha(result.stderr),
                   stdout_bytes=len(result.stdout), stderr_bytes=len(result.stderr))
        # Git plumbing output is metadata, never a source body.
        row['stdout_utf8'] = result.stdout.decode('utf8')
        row['stderr_utf8'] = result.stderr.decode('utf8')
        commands.append(row)
        (OUT / 'commands.json').write_text(json.dumps(commands, indent=2) + '\n')
        assert result.returncode in expected, (argv, result.returncode, result.stderr.decode())
        return result.stdout

    run(['df', '-B1', str(PARENT)])
    run(['df', '-i', str(PARENT)])
    scratch = Path(tempfile.mkdtemp(prefix='integration-probe-20261103-', dir=PARENT))
    os.chmod(scratch, 0o700)
    (OUT / 'owner.json').write_text(json.dumps(dict(created_utc=now(), scratch=str(scratch),
        owner='M6 coordinator wN:p2', purpose='new immutable integration probe; no runtime',
        retention='Retain until root has resolved or handed off this candidate.'), indent=2)+'\n')
    repository = scratch / 'distribution.git'
    run(['git', 'init', '--bare', '--template=', str(repository)])
    for store in STORES:
        assert Path(store).is_dir()
    (repository / 'objects/info/alternates').write_text('\n'.join(STORES)+'\n')
    git = ['git', '--no-replace-objects', '--git-dir='+str(repository)]
    for ref in (COORDINATOR, NEXT, M7, M7_PRODUCT):
        assert run(git + ['rev-parse', '--verify', ref+'^{commit}']).decode().strip() == ref
    for ref in (COORDINATOR, M7):
        run(git + ['merge-base', '--is-ancestor', NEXT, ref])
    run(git + ['diff', '--exit-code', '--quiet', M7_PRODUCT, M7, '--',
               'projects', 'packages', 'scripts', 'distributions', 'config'])
    package = 'projects/ROCKNIX/packages/ui/emulationstation'
    package_trees = {ref:run(git+['rev-parse', ref+':'+package]).decode().strip()
                     for ref in (M7_PRODUCT, M7, NEXT)}
    assert package_trees[M7_PRODUCT] == package_trees[M7] == 'adb10ce0720d571e913bc0a1c45a344518639fcd'
    base = run(git+['merge-base', M7, COORDINATOR]).decode().strip()
    raw = run(git+['merge-tree', '--write-tree', '-z', '--messages', M7, COORDINATOR], (0,1))
    code = commands[-1]['exit']
    parts = raw.split(b'\0')
    tree = parts[0].decode()
    assert len(tree)==40 and all(c in '0123456789abcdef' for c in tree)
    stages=[]
    index=1
    while index < len(parts) and parts[index]:
        header, path = parts[index].split(b'\t',1)
        mode, oid, stage = header.decode().split(' ')
        stages.append(dict(path=path.decode(), mode=mode, oid=oid, stage=int(stage)))
        index+=1
    result = dict(schema=1, observed_utc=now(), owner='M6 coordinator wN:p2',
                  inputs=dict(m7=M7, m7_product=M7_PRODUCT, coordinator=COORDINATOR, next=NEXT),
                  repository=str(repository), merge_base=base, package_trees=package_trees,
                  exit=code, probe_tree=tree, conflict_stages=stages,
                  conflict_paths=sorted({r['path'] for r in stages}),
                  scope='Private merge-tree probe only; no shared ref, checkout, integration, acceptance, runtime or publication.',
                  program_sha256=sha(Path(__file__).read_bytes()))
    (OUT/'result.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))

if __name__ == '__main__':
    main()

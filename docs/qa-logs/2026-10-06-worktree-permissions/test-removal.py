#!/usr/bin/env python3
"""Exercise actual Git removal in isolated temporary repositories; never builds."""
from pathlib import Path
import datetime
import hashlib
import json
import os
import shutil
import stat
import subprocess
import sys
import tempfile

source = Path(sys.argv[1]).resolve()
original = Path(sys.argv[2]).resolve()
output = Path(sys.argv[3]).resolve()
output.mkdir(parents=True, exist_ok=True)
root = Path(tempfile.mkdtemp(prefix='pixelelated-worktree-permissions-'))
cases = []

def call(args, cwd, **kwargs):
    return subprocess.run(args, cwd=cwd, text=True, capture_output=True, **kwargs)

def setup(name, tool):
    home = root / name
    home.mkdir()
    repo = home / 'repo'
    call(['git', 'init', '-q', str(repo)], home, check=True)
    call(['git', 'config', 'user.name', 'Local regression fixture'], repo, check=True)
    call(['git', 'config', 'user.email', 'fixture@example.invalid'], repo, check=True)
    (repo / 'tracked').write_text('retained source\n')
    call(['git', 'add', 'tracked'], repo, check=True)
    call(['git', 'commit', '-qm', 'fixture'], repo, check=True)
    (repo / 'tools').mkdir()
    helper = repo / 'tools/fork-worktree'
    shutil.copyfile(tool, helper)
    helper.chmod(0o755)
    tree = home / 'target'
    call(['git', 'worktree', 'add', '-qb', 'build/test', str(tree)], repo, check=True)
    locked = tree / 'build.fixture/readonly/deep'
    locked.mkdir(parents=True)
    (locked / 'module').write_text('unchanged bytes\n')
    (locked / 'module').chmod(0o444)
    locked.chmod(0o555)
    locked.parent.chmod(0o555)
    outside = home / 'outside'
    outside.mkdir()
    (outside / 'sentinel').write_text('outside retained\n')
    outside.chmod(0o555)
    (tree / 'build.fixture/external').symlink_to(outside, target_is_directory=True)
    return repo, helper, tree, locked, outside

def registered(repo, tree):
    return 'worktree ' + str(tree) + '\n' in call(['git', 'worktree', 'list', '--porcelain'], repo, check=True).stdout

def save(name, result, detail):
    (output / (name + '.stdout')).write_text(result.stdout)
    (output / (name + '.stderr')).write_text(result.stderr)
    cases.append({'case': name, 'rc': result.returncode, 'pass': True, 'verified': detail})
    print('PASS', name, flush=True)

repo, helper, tree, locked, outside = setup('original', original)
r = call([str(helper), 'remove', str(tree), '--force'], repo)
assert r.returncode != 0 and 'Permission denied' in r.stderr
assert tree.exists() and not registered(repo, tree)
save('original', r, 'Original actual permission failure leaves an unregistered partial directory')

repo, helper, tree, locked, outside = setup('corrected', source)
before = ((outside / 'sentinel').read_bytes(), stat.S_IMODE(outside.stat().st_mode))
head = call(['git', 'rev-parse', 'build/test'], repo, check=True).stdout
r = call([str(helper), 'remove', str(tree), '--force'], repo)
assert r.returncode == 0 and not tree.exists() and not registered(repo, tree), r.stderr
assert call(['git', 'rev-parse', 'build/test'], repo, check=True).stdout == head
assert ((outside / 'sentinel').read_bytes(), stat.S_IMODE(outside.stat().st_mode)) == before
save('corrected', r, 'Directory and registration absent; branch retained; external symlink target bytes and mode unchanged')

repo, helper, tree, locked, outside = setup('no-force', source)
r = call([str(helper), 'remove', str(tree)], repo)
assert r.returncode != 0 and registered(repo, tree) and (locked / 'module').is_file()
assert stat.S_IMODE(locked.stat().st_mode) == 0o555
save('no-force', r, 'Unapproved build-output deletion refuses without permission changes')

repo, helper, tree, locked, outside = setup('empty-readonly', source)
locked.chmod(0o755)
locked.parent.chmod(0o755)
shutil.rmtree(tree / 'build.fixture')
empty = tree / 'build.fixture/empty'
empty.mkdir(parents=True)
empty.chmod(0o555)
r = call([str(helper), 'remove', str(tree), '--force'], repo)
assert r.returncode == 0 and not tree.exists() and not registered(repo, tree)
assert '0 owner-write/search repairs' in r.stdout
save('empty-readonly', r, 'Empty read-only directories need no chmod: removal uses their writable parent')

repo, helper, tree, locked, outside = setup('unreadable', source)
blocked = tree / 'build.fixture/unreadable'
blocked.mkdir()
(blocked / 'sentinel').write_text('must remain\n')
blocked.chmod(0)
try:
    r = call([str(helper), 'remove', str(tree), '--force'], repo)
    assert r.returncode != 0 and 'permission preflight failed' in r.stderr
    assert registered(repo, tree) and (tree / 'tracked').read_text() == 'retained source\n'
    assert stat.S_IMODE(locked.stat().st_mode) == 0o555
finally:
    blocked.chmod(0o755)
assert (blocked / 'sentinel').read_text() == 'must remain\n'
save('unreadable', r, 'Incomplete inspection refuses before chmod/deletion/unregistration')

repo, helper, tree, locked, outside = setup('git-result', source)
real_git = shutil.which('git')
stub = repo.parent / 'stub'
stub.mkdir()
(stub / 'git').write_text('#!/usr/bin/env python3\nimport subprocess,sys\nr=subprocess.run(' + repr([real_git]) + '+sys.argv[1:])\nraise SystemExit(42 if sys.argv[1:3]==["worktree","remove"] and r.returncode==0 else r.returncode)\n')
(stub / 'git').chmod(0o755)
r = call([str(helper), 'remove', str(tree), '--force'], repo, env={**os.environ, 'PATH': str(stub) + os.pathsep + os.environ['PATH']})
assert r.returncode == 42 and not tree.exists() and not registered(repo, tree)
save('git-result', r, 'A nonzero Git result is propagated even if the directory is absent')

report = {'utc': datetime.datetime.now(datetime.timezone.utc).isoformat(), 'fixture_root': str(root),
          'source_sha256': hashlib.sha256(source.read_bytes()).hexdigest(),
          'original_sha256': hashlib.sha256(original.read_bytes()).hexdigest(), 'cases': cases, 'all_pass': True}
(output / 'result.json').write_text(json.dumps(report, indent=2) + '\n')
print(json.dumps(report, indent=2))

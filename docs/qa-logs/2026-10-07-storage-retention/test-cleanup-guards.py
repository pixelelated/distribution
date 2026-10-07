"""Exercise refusal and symlink boundaries on disposable fixtures only."""
from pathlib import Path
import importlib.util
import json
import os
import stat
import tempfile

source = Path(__file__).with_name('execute-cleanup.py')
spec = importlib.util.spec_from_file_location('cleanup', source)
cleanup = importlib.util.module_from_spec(spec)
spec.loader.exec_module(cleanup)
passed = []


def rejects(name, action):
    try:
        action()
    except (RuntimeError, OSError):
        passed.append(name)
    else:
        raise AssertionError('accepted invalid case: ' + name)


def inventory(root):
    rows = []
    for path in [root, *root.rglob('*')]:
        row = dict(path=str(path), identity=cleanup.identity(path))
        if path.is_symlink():
            row['target'] = os.readlink(path)
        rows.append(row)
    return rows


with tempfile.TemporaryDirectory(prefix='pixelelated-cleanup-controls-') as directory:
    root = Path(directory)
    rejects('loose firmware outside administrator directory scope refused',
            lambda: cleanup.check_root_coverage([str(root / 'loose.img.gz')], [str(root / 'child')]))
    cleanup.check_root_coverage([str(root / 'loose.img.gz'), str(root / 'child/disk')], [str(root)])
    passed.append('parent scope covers loose files and nested targets')
    sentinel = root / 'keep'
    sentinel.write_text('external record remains')
    payload = root / 'disk'
    payload.write_text('original')
    row = dict(path=str(payload), identity=cleanup.identity(payload), sha256=cleanup.sha(payload))
    cleanup.same(row, hashed=True)
    passed.append('exact file accepted')
    bad = dict(row, sha256='0' * 64)
    rejects('wrong digest refused', lambda: cleanup.same(bad, hashed=True))
    payload.write_text('changed')
    rejects('changed identity refused', lambda: cleanup.same(row))
    payload.unlink()
    payload.symlink_to(sentinel)
    rejects('replacement symlink refused', lambda: cleanup.same(row))

    tree = root / 'extracted'
    tree.mkdir()
    (tree / 'data').write_text('disposable')
    (tree / 'outside-link').symlink_to(sentinel)
    (tree / 'outside-dir').symlink_to(root, target_is_directory=True)
    entries = inventory(tree)
    (tree / 'unreviewed').write_text('must block deletion')
    rejects('extra entry refused before removal', lambda: cleanup.remove_tree(tree, entries))
    assert (tree / 'data').is_file() and sentinel.is_file()
    (tree / 'unreviewed').unlink()
    os.chmod(tree, 0o500)
    entries = inventory(tree)
    cleanup.remove_tree(tree, entries)
    assert not tree.exists() and sentinel.read_text() == 'external record remains'
    passed.append('read-only directory removed without following external file/directory links')

print(json.dumps(dict(result='PASS', controls=passed, count=len(passed)), indent=2))

#!/usr/bin/env python3
"""One explicitly admitted same-filesystem cache custody transfer; never copy/overwrite."""
import argparse
import ctypes
import hashlib
import json
import os
from pathlib import Path
import signal
import subprocess
import time

OLD = Path('/workspace/repos/rocknix.worktrees/m7-p5-build-20261014-02')
NEW = Path('/workspace/repos/rocknix.worktrees/m7-p5-build-20261015-01')
OLD_HEAD = 'fac608ff89940ce358ea9b8a95e9a08a6fe26568'

TEMPLATE_COMMIT = '956f9481872d3d64f3e33d495e5ab25dfd9aaefd'
PRODUCT_PATHS = ['projects/ROCKNIX/packages/emulators/standalone/dolphin-sa/package.mk', 'projects/ROCKNIX/packages/emulators/standalone/dolphin-sa/patches/018-nogui-achievements-lifecycle.patch', 'projects/ROCKNIX/packages/virtual/emulators/sources/Install Steam.sh']
PRODUCT_SHA256 = {'projects/ROCKNIX/packages/emulators/standalone/dolphin-sa/package.mk': '27ab9954ec5fb30aefb51555281c749aea416f2d3bb8fc0138d0964730e5a153', 'projects/ROCKNIX/packages/emulators/standalone/dolphin-sa/patches/018-nogui-achievements-lifecycle.patch': 'bc1d04f688f85ff3fc49a81fa40625d08c8f7839aa81e46baee6b50b443ee5f0', 'projects/ROCKNIX/packages/virtual/emulators/sources/Install Steam.sh': 'cefb22a50db915be1637e682dfba047789b276144bbe707220a2b4117c7a3264'}
PRODUCT_ROOTS = ['packages', 'projects', 'config', 'scripts', 'distributions', 'Makefile']
ROOT = 'build.pixelelated-GENERIC_X64.x86_64'
OLD_OWNER = Path('/workspace/tmp/pix-m7-engineering-build-20261014-02')


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write(path, value):
    with path.open('x') as stream:
        json.dump(value, stream, indent=2); stream.write('\n')
        stream.flush(); os.fsync(stream.fileno())


def identity(path):
    st = path.stat()
    return {'device': st.st_dev, 'inode': st.st_ino}


def git(tree, *args):
    return subprocess.check_output(['git', '-C', str(tree), *args], text=True, timeout=15).strip()


def within(path, parent):
    return path == parent or parent in path.parents


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--owner', type=Path, required=True)
    parser.add_argument('--commit', required=True, help='Exact final reviewed, committed source; must preserve the reviewed template product inputs')
    parser.add_argument('--dolphin-recipe-sha256', required=True, help='Independently reviewed final Dolphin recipe SHA256')
    parser.add_argument('--dependency-readback', type=Path, required=True)
    parser.add_argument('--dependency-sha256', required=True)
    args = parser.parse_args()
    assert len(args.commit) == 40 and all(c in '0123456789abcdef' for c in args.commit)
    new_head = args.commit
    assert len(args.dolphin_recipe_sha256) == 64 and all(c in '0123456789abcdef' for c in args.dolphin_recipe_sha256)
    product_sha256 = dict(PRODUCT_SHA256)
    product_sha256['projects/ROCKNIX/packages/emulators/standalone/dolphin-sa/package.mk'] = args.dolphin_recipe_sha256
    owner = args.owner.resolve(strict=True)
    assert owner.is_dir() and not (owner / 'transfer-result.json').exists()
    result = {'schema': 'pix572-atomic-cache-transfer-v1', 'status': 'FAIL',
              'method': 'same-filesystem-rename', 'copy_performed': False,
              'old': str(OLD / ROOT), 'new': str(NEW / ROOT),
              'source_head': OLD_HEAD, 'destination_head': new_head, 'product_sha256': product_sha256,
              'renamed': False, 'utc_start_epoch': time.time()}
    def timeout(_number, _frame):
        raise TimeoutError('120-second transfer owner bound reached')
    signal.signal(signal.SIGALRM, timeout)
    signal.alarm(120)
    try:
        assert os.getuid() != 0 and Path.cwd().resolve() == NEW
        assert git(OLD, 'rev-parse', 'HEAD') == OLD_HEAD
        assert git(NEW, 'rev-parse', 'HEAD') == new_head
        assert git(NEW, 'branch', '--show-current') == 'build/m7-p5-20261015-01'
        assert git(OLD, 'status', '--porcelain') == git(NEW, 'status', '--porcelain') == ''
        changed = git(NEW, 'diff', '--name-only', OLD_HEAD, new_head, '--',
                      'packages', 'projects', 'config', 'scripts', 'distributions', 'Makefile').splitlines()
        assert changed == PRODUCT_PATHS
        assert set(git(NEW, 'diff', '--name-only', TEMPLATE_COMMIT, new_head, '--', *PRODUCT_ROOTS).splitlines()) <= {'projects/ROCKNIX/packages/emulators/standalone/dolphin-sa/package.mk'}, 'review/reseal additional changed product inputs'
        assert all(sha(NEW / path) == digest for path, digest in product_sha256.items())
        active = NEW / os.environ['RASTERATOPS_BUILD_RUN']
        admission = json.loads((active / 'admission.json').read_text())
        assert admission['source']['head'] == new_head and admission['submission_owner'] == str(owner)
        assert admission['container_checkout'] == '/workspace/repos/rocknix.worktrees/m7-pixelelated'
        (owner / 'run.path').write_text(str(active) + '\n')
        result['watched_run'] = str(active)
        source, destination = OLD / ROOT, NEW / ROOT
        assert source.is_dir() and not source.is_symlink()
        assert not destination.exists() and not destination.is_symlink()
        assert identity(source)['device'] == NEW.stat().st_dev == OLD.stat().st_dev
        before = identity(source)
        result['before_identity'] = before
        dependency = args.dependency_readback.resolve(strict=True)
        assert sha(dependency) == args.dependency_sha256
        d = json.loads(dependency.read_text())
        assert d['status'] == 'CLEAR_WITH_STATED_SCOPE'
        assert d['host_pid_namespace'] == Path('/proc/self/ns/pid').stat().st_ino
        assert d['root'] == str(source) and d['root_identity'] == before
        assert 0 <= time.time() - d['utc_epoch'] <= 900
        assert not d['process_matches'] and not d['remaining_consumers'] and not d['active_admissions']
        assert d['prepared_consumers_resolved'] is True
        for mount in d['docker_all_mounts']:
            path = Path(mount.get('source', mount.get('Source', '')))
            assert path.is_absolute()
            assert not (within(path, source) or within(source, path))
        result['dependency_readback'] = {'path': str(dependency), 'sha256': sha(dependency),
                                         'readback': d}
        original = json.loads((OLD_OWNER / 'owner-result.json').read_text())
        consumed = json.loads((OLD_OWNER / 'consumption-evidence.json').read_text())
        assert original['status'] == 'PASS' and not original['signals']
        assert all(not pids for pids in original['surviving_host_command_groups'].values())
        assert consumed['disposition'] == 'qualified' and consumed['expected_rc'] == 0
        assert all(sha(Path(item['path'])) == item['sha256'] for item in consumed['evidence'])
        result['original_build_consumption'] = {'path': str(OLD_OWNER / 'consumption-evidence.json'),
                                                'sha256': sha(OLD_OWNER / 'consumption-evidence.json')}
        target_before = identity(OLD / 'target')
        result['old_target_identity'] = target_before
        write(owner / 'transfer-intent.json', result)
        # Linux renameat2(RENAME_NOREPLACE): one atomic operation, no EXDEV copy fallback.
        libc = ctypes.CDLL(None, use_errno=True)
        rename = libc.renameat2
        rename.argtypes = [ctypes.c_int, ctypes.c_char_p, ctypes.c_int, ctypes.c_char_p, ctypes.c_uint]
        rename.restype = ctypes.c_int
        rc = rename(-100, os.fsencode(source), -100, os.fsencode(destination), 1)
        if rc:
            number = ctypes.get_errno()
            raise OSError(number, os.strerror(number))
        result['renamed'] = True
        for directory in [OLD, NEW]:
            fd = os.open(directory, os.O_RDONLY | os.O_DIRECTORY)
            try:
                os.fsync(fd)
            finally:
                os.close(fd)
        result['after_identity'] = identity(destination)
        assert result['after_identity'] == before and not source.exists()
        assert identity(OLD / 'target') == target_before
        assert git(OLD, 'rev-parse', 'HEAD') == OLD_HEAD and git(OLD, 'status', '--porcelain') == ''
        assert git(NEW, 'rev-parse', 'HEAD') == new_head and git(NEW, 'status', '--porcelain') == ''
        result['status'] = 'PASS'
    except BaseException as error:
        result['error'] = type(error).__name__ + ': ' + str(error)
    finally:
        signal.alarm(0)
        result['utc_finish_epoch'] = time.time()
        write(owner / 'transfer-result.json', result)
        if result['status'] == 'PASS':
            write(owner / 'cache-ready.json', result)
        (owner / 'inner.rc').write_text('0\n' if result['status'] == 'PASS' else '1\n')
    return 0 if result['status'] == 'PASS' else 1


if __name__ == '__main__':
    raise SystemExit(main())

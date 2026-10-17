#!/usr/bin/env python3
"""Plan by default. --execute requires the coordinator's separate build allocation."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import shlex
import signal
import subprocess
import time

ROOT = Path(__file__).resolve().parent
CANONICAL = Path('/workspace/repos/rocknix.worktrees/m7-pixelelated')
BUILD = CANONICAL / 'build.pixelelated-GENERIC_X64.x86_64'
TOOLCHAIN = BUILD / 'toolchain'
TRIPLE = 'x86_64-rocknix-linux-gnu'
SYSROOT = TOOLCHAIN / TRIPLE / 'sysroot'


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output-dir', type=Path, required=True)
    parser.add_argument('--execute', action='store_true')
    args = parser.parse_args()
    source = ROOT / 'input-source/input-spike.c'
    receipt = json.loads((ROOT / 'input-source/preparation.json').read_text())
    source_hash = hashlib.sha256(source.read_bytes()).hexdigest()
    if source_hash != receipt['files']['input-spike.c']:
        raise SystemExit('source hash mismatch')
    output = args.output_dir.absolute()
    if output.exists() or not output.parent.is_dir():
        raise SystemExit('output directory must be new beneath an existing allocated parent')
    if output == CANONICAL or CANONICAL in output.parents:
        raise SystemExit('output must be outside the build checkout')
    explicit = {'PATH': str(TOOLCHAIN / 'bin') + ':/usr/bin:/bin', 'LC_ALL': 'C',
                'TMPDIR': str(output), 'CCACHE_DISABLE': '1',
                'PKG_CONFIG_PATH': '', 'PKG_CONFIG_LIBDIR': str(SYSROOT / 'usr/lib/pkgconfig') + ':' + str(SYSROOT / 'usr/share/pkgconfig'),
                'PKG_CONFIG_SYSROOT_DIR': str(SYSROOT), 'PKG_CONFIG_SYSROOT_BASE': str(BUILD),
                'PKG_CONFIG_ALLOW_SYSTEM_CFLAGS': '1', 'PKG_CONFIG_ALLOW_SYSTEM_LIBS': '1'}
    pkg_config = str(TOOLCHAIN / 'bin/pkg-config')
    cc = str(TOOLCHAIN / 'bin' / (TRIPLE + '-gcc'))
    base = [cc, '--sysroot=' + str(SYSROOT), '-std=c11', '-O2', '-Wall', '-Wextra', str(source)]
    tail = ['-latomic', '-o', str(output / 'input-spike')]
    plan = {'status': 'PLAN_ONLY', 'source': str(source), 'source_sha256': source_hash,
            'source_preparation': receipt, 'environment': explicit,
            'pkg_config_query': [pkg_config, '--cflags', '--libs', 'gtk4', 'webkitgtk-6.0'],
            'compiler_argv_before_pkg_config': base, 'compiler_argv_after_pkg_config': tail,
            'compiler_timeout_seconds': 60, 'runtime_invoked': False,
            'requirements': ['Run inside the admitted non-root pinned builder, with the isolated checkout mounted at the canonical path.',
                             'Mount this packet at the same absolute path, read-only; mount a separate writable output parent.',
                             'External owner enforces 1 CPU, 2GiB/no swap, 512MiB output and lifecycle monitoring.',
                             'Artifact closure must be qualified first; compiling does not authorize any guest launch.']}
    if not args.execute:
        print(json.dumps(plan, indent=2))
        return 0
    if os.getuid() == 0 or not Path('/.dockerenv').is_file():
        raise SystemExit('refusing: admitted non-root build container required')
    head = subprocess.check_output(['git', '-C', str(CANONICAL), 'rev-parse', 'HEAD'], text=True, timeout=10).strip()
    if head != '969354955741d6c0ca8ce816e1c59ad338b1605b':
        raise SystemExit('checkout commit mismatch')
    output.mkdir(mode=0o700)
    env = {'HOME': os.environ.get('HOME', '/tmp'), **explicit}
    plan.update(status='FAIL', original_compiler_rc=None, source_commit=head)
    started = time.monotonic()
    child = None
    try:
        versions = subprocess.check_output([pkg_config, '--modversion', 'gtk4', 'webkitgtk-6.0'],
                                           env=env, text=True, timeout=10).splitlines()
        if versions != ['4.24.1', '2.54.1']:
            raise ValueError('unexpected pkg-config versions: ' + repr(versions))
        flags = shlex.split(subprocess.check_output(plan['pkg_config_query'], env=env, text=True, timeout=10))
        command = base + flags + tail
        plan.update(pkg_config_versions=versions, compiler_argv=command)
        with (output / 'compiler.stdout').open('xb') as stdout, (output / 'compiler.stderr').open('xb') as stderr:
            child = subprocess.Popen(command, cwd=output, env=env, stdout=stdout, stderr=stderr, start_new_session=True)
            try:
                code = child.wait(timeout=60)
            except subprocess.TimeoutExpired:
                os.killpg(child.pid, signal.SIGKILL)
                child.wait(timeout=10)
                raise TimeoutError('compiler deadline exceeded')
        plan['original_compiler_rc'] = code
        if code:
            raise ValueError('compiler returned ' + str(code))
        binary = output / 'input-spike'
        plan.update(status='PASS_COMPILE_ONLY', binary_sha256=hashlib.sha256(binary.read_bytes()).hexdigest(),
                    binary_bytes=binary.stat().st_size)
    except Exception as error:
        plan['error'] = type(error).__name__ + ': ' + str(error)
    finally:
        if child is not None and child.poll() is None:
            os.killpg(child.pid, signal.SIGKILL)
            child.wait(timeout=10)
        if child is not None:
            plan['original_compiler_rc'] = child.returncode
        plan['elapsed_seconds'] = time.monotonic() - started
        (output / 'compile-result.json').write_text(json.dumps(plan, indent=2) + '\n')
    print(json.dumps(plan, indent=2))
    return 0 if plan['status'] == 'PASS_COMPILE_ONLY' else 1


if __name__ == '__main__':
    raise SystemExit(main())

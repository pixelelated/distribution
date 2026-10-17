#!/usr/bin/env python3
"""Materialize source-only GTK4 input compile owner after explicit qualification."""
import argparse
import ast
import datetime
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import subprocess

HERE = Path(__file__).resolve().parent
TREE = Path('/workspace/repos/rocknix.worktrees/m7-gtk4-build-20261017-01')
CANONICAL = Path('/workspace/repos/rocknix.worktrees/m7-pixelelated')
COMMON_GIT = Path('/workspace/repos/rocknix/.git')
OWNER = Path('/workspace/tmp/pix-gtk4-input-compile-20261017-01')
PACKET = Path('/tmp/pix-gtk4-postbuild-20261017')
COMMIT = '969354955741d6c0ca8ce816e1c59ad338b1605b'
IMAGE = 'ghcr.io/rocknix/rocknix-build@sha256:988c0ba586263caeba4be4c03bd16eee055c9d066657951e320087bb8226ee39'
BUILD = 'build.pixelelated-GENERIC_X64.x86_64'
TRIPLE = 'x86_64-rocknix-linux-gnu'
OLD = Path('/tmp/pix-m7-zerotier-generic-refresh-20261015')

def sha(path):
    with path.open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()

def write(path, value):
    with path.open('x') as stream:
        json.dump(value, stream, indent=2)
        stream.write('\n')

def main(qualification):
    assert not OWNER.exists() and not OWNER.is_symlink(), 'fresh owner required'
    assert os.getuid() != 0 and 4 in os.sched_getaffinity(0)
    assert os.readlink('/proc/self/ns/pid') == 'pid:[4026531836]', 'actual host required'
    for name, expected in json.loads((HERE / 'source-bindings.json').read_text())['input_sha256'].items():
        assert sha(Path(name)) == expected, name
    manifest = json.loads((HERE / 'prepared-files.json').read_text())
    for name, expected in manifest['files'].items():
        assert sha(HERE / name) == expected, name
    spec = importlib.util.spec_from_file_location('qualification', HERE / 'qualification.py')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    qualified = module.verify(qualification)
    assert subprocess.check_output(['git', '-C', str(TREE), 'rev-parse', 'HEAD'], text=True, timeout=10).strip() == COMMIT
    assert not subprocess.check_output(['git', '-C', str(TREE), 'status', '--porcelain', '--untracked-files=no'], text=True, timeout=10).strip()
    assert Path(subprocess.check_output(['git', '-C', str(TREE), 'rev-parse', '--git-common-dir'], text=True, timeout=10).strip()).resolve() == COMMON_GIT
    toolchain = TREE / BUILD / 'toolchain'
    driver = toolchain / 'bin' / (TRIPLE + '-gcc-15.2.0')
    wrapper = toolchain / 'bin' / (TRIPLE + '-gcc')
    assert driver.read_bytes()[:4] == b'\x7fELF'
    assert 'ccache' in wrapper.read_text(), 'reviewed wrapper changed'
    source_files = [PACKET / 'compile-input.py', *sorted((PACKET / 'input-source').glob('*'))]
    external = {str(path): sha(path) for path in source_files}
    external.update({str(path): sha(path) for path in [driver, wrapper, toolchain / 'bin/pkg-config', TREE / '.git']})
    for reference in [qualified['runtime_inventory'], *qualified['closure_evidence']]:
        external[reference['path']] = reference['sha256']
    scripts = {'compile.py': (HERE / 'compile-owner.py.in').read_text(),
               'qualification.py': (HERE / 'qualification.py').read_text(),
               'host-resources.py': (OLD / 'host-resources.py').read_text(),
               'inputs/inner-build.py': (OLD / 'inner-build.py').read_text()}
    for name, text in scripts.items():
        ast.parse(text, filename=name)
    os.umask(0o077)
    OWNER.mkdir(mode=0o700)
    for relative in ['inputs', 'out', 'scan', 'submit', 'stages', 'stages/compile']:
        (OWNER / relative).mkdir(mode=0o700)
    for relative, text in scripts.items():
        with (OWNER / relative).open('x') as stream:
            stream.write(text)
    (OWNER / 'qualification.json').write_bytes(qualification.read_bytes())
    mounts = [{'Source': str(OWNER / 'inputs'), 'Destination': '/inputs', 'RW': False},
              {'Source': str(OWNER / 'out'), 'Destination': str(OWNER / 'out'), 'RW': True},
              {'Source': str(OWNER / 'stages'), 'Destination': '/build-owner/stages', 'RW': True},
              {'Source': str(PACKET), 'Destination': str(PACKET), 'RW': False},
              {'Source': str(TREE), 'Destination': str(CANONICAL), 'RW': False},
              {'Source': str(COMMON_GIT), 'Destination': str(COMMON_GIT), 'RW': False},
              {'Source': str(driver), 'Destination': str(CANONICAL / BUILD / 'toolchain/bin' / (TRIPLE + '-gcc')), 'RW': False}]
    config = {'schema': 1, 'utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
              'checkout': str(TREE), 'canonical_checkout': str(CANONICAL), 'commit': COMMIT,
              'host_pid_namespace': os.readlink('/proc/self/ns/pid'), 'owner_label': OWNER.name,
              'image': IMAGE, 'source_packet': str(PACKET), 'mounts': mounts,
              'qualification_sha256': sha(OWNER / 'qualification.json'),
              'external_sha256': external,
              'compiler_override': {'source': str(driver), 'destination': mounts[-1]['Destination'],
                                    'sha256': sha(driver), 'reason': 'direct GCC ELF, bypass installed ccache wrapper without editing source'},
              'limits': {'cpu_ids': [4], 'cpus': 1, 'memory_mib': 2048, 'swap_bytes': 0,
                         'pids': 128, 'producer_seconds': 90, 'cleanup_seconds': 30, 'total_seconds': 120,
                         'tmpfs_bytes': 128 * 1024**2, 'output_limit_bytes': 512 * 1024**2,
                         'scratch_budget_bytes': 576 * 1024**2, 'compiler_log_bytes': 2 * 1024**2},
              'host_observer': {'minimum_host_available_bytes': 8 * 1024**3,
                                'minimum_volume_available_bytes': 100 * 1024**3,
                                'disk_scan_timeout_seconds': 5, 'disk_sample_interval_seconds': 5},
              'helper_sha256': {relative: sha(OWNER / relative) for relative in scripts},
              'source_preparation': {'path': str(HERE), 'preparer_sha256': sha(Path(__file__)),
                                     'runner_sha256': sha(HERE / 'compile-owner.py.in')},
              'runtime_authorized': False,
              'runtime_scope': 'single GTK4 input fixture compile; no target execution, display, browser, provider or VM'}
    write(OWNER / 'inputs.json', config)
    protected = [str(TREE), str(COMMON_GIT), str(PACKET), str(qualification),
                 *[str(OWNER / relative) for relative in ['inputs.json', 'qualification.json', *scripts]]]
    write(OWNER / 'retention-plan.json', {'volume': '/workspace', 'scan_roots': [str(OWNER / 'scan')],
          'reference_stores': [], 'protected': protected, 'candidates': [],
          'builds': [{'name': 'gtk4-input-compile-only', 'terms_bytes': {'outputs': 512 * 1024**2, 'owner_records': 64 * 1024**2},
                     'basis': 'One source-file compile against read-only completed isolated toolchain. No source/cache copy or package build. Output ceiling512MiB;64MiB conservative records. Tmpfs128MiB is within2GiB memory, not workspace output. CPU4, zero container swap/network,90s producer+30s cleanup budget; any total overrun fails. Only this fresh owner is scanned.',
                     'evidence': [{'path': str(OWNER / 'inputs.json'), 'sha256': sha(OWNER / 'inputs.json')}]}]})
    write(OWNER / 'admission-plan.json', {'checkout': str(TREE), 'container_checkout': str(CANONICAL),
          'retention_plan': str(OWNER / 'retention-plan.json'), 'retention_report': str(OWNER / 'retention-report.json'),
          'stage': 'gtk4-input-compile-only', 'profiles': [{'PROJECT': 'ROCKNIX', 'DEVICE': 'GENERIC_X64', 'ARCH': 'x86_64'}],
          'outputs': [{'path': str(OWNER), 'issue': 576, 'kind': 'qa-scratch',
                       'release_when': 'Preserve exact compiler/inner/Docker/resource/original owner receipts and compile-only binary; consume original admission before retiring superseded scratch. No runtime or production qualification.'}]})
    print(json.dumps({'status': 'PREPARED_UNRUN', 'owner': str(OWNER), 'runtime_authorized': False,
                      'admission_created': False, 'requires_owner_affinity': [4], 'total_seconds': 120}))

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--qualification', type=Path, default=Path('/tmp/pix-gtk4-compile-only-qualification-20261017.json'))
    main(parser.parse_args().qualification)

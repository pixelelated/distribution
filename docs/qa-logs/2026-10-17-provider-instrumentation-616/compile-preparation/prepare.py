#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-2.0
"""Materialize a fresh compile owner only; never launch Docker/compiler/VM."""
import argparse
import ast
import datetime
import hashlib
import json
import os
from pathlib import Path
import subprocess

ROOT = Path('/workspace/repos/rocknix.worktrees/m7-p5-build-20261015-03')
OWNER = Path('/workspace/tmp/pix-provider616-compile-20261017-01')
COMMIT = '077197e6cd3ea31f33b28aaf3882a694b3423b53'
CANDIDATE = Path('/tmp/pix-provider616-instrumentation-20261017/prepared/cloud-signin-window.c')
CANDIDATE_SHA = '63b8cf5725652874f361aa5fe04abe2b5f326b1cb9ae113590d5c422f9e16b6d'
OLD = Path('/tmp/pix-m7-zerotier-generic-refresh-20261015')
CHECKS = Path('/workspace/repos/rocknix.worktrees/m7-player-setup/docs/qa-logs/2026-10-17-browser-controls-616/config-checks.py')
HOST_SHA = '39a1b153e861cf3256b52567eb3e251412b9ab069e70ff72f4b5ac65e71fbaf1'
INNER_SHA = '2a33d9548e9adcb278bf75de230294eeb45e79263cecc355837b284d06ff4d98'
CHECKS_SHA = '03d94af94373b39387eb0b9deed4156eb94f029ea12f856a474444f359c268a7'
IMAGE = 'ghcr.io/rocknix/rocknix-build@sha256:988c0ba586263caeba4be4c03bd16eee055c9d066657951e320087bb8226ee39'
TREES = [
    ('/workspace/repos/rocknix.worktrees/m7-p5-build-20261015-03/build.pixelelated-GENERIC_X64.x86_64',
     '/workspace/repos/rocknix.worktrees/m7-pixelelated/build.pixelelated-GENERIC_X64.x86_64',
     'x86_64-rocknix-linux-gnu', 'GENERIC_X64'),
    ('/workspace/repos/rocknix.worktrees/m7-pixelelated-h700-03/build.pixelelated-H700.aarch64',
     '/workspace/repos/rocknix.worktrees/m7-pixelelated-h700-01/build.pixelelated-H700.aarch64',
     'aarch64-rocknix-linux-gnu', 'H700'),
]


def sha(path):
    with path.open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def verified(path, expected):
    if sha(path) != expected:
        raise ValueError('reviewed input hash mismatch')
    return path.read_text()


def replace_once(source, old, new):
    if source.count(old) != 1:
        raise ValueError('source anchor changed')
    return source.replace(old, new, 1)


def config_checks(original):
    changed = replace_once(original, '    ]\n    base = ',
        "        ('debug-present-empty', {'CLOUD_SIGNIN_DEBUG': ''}, 78, None),\n"
        "        ('debug-present-nonempty', {'CLOUD_SIGNIN_DEBUG': '1'}, 78, None),\n"
        '    ]\n    base = ')
    changed = replace_once(changed, "if not key.startswith('QA616_')}",
        "if not key.startswith('QA616_') and key != 'CLOUD_SIGNIN_DEBUG'}")
    changed = replace_once(changed, "and 'QA616_SAMPLE' not in process.stdout + process.stderr)",
        "and not any(item in process.stdout + process.stderr for item in\n"
        "                     ['QA616_SAMPLE', 'QA616_PROOF', 'QA616_REQUEST', 'QA616_DOM_BINDING', 'QA616_INPUT']))")
    ast.parse(changed)
    return changed


def compile_script(facts):
    script = '''#!/bin/bash
set -euo pipefail
export TMPDIR=/tmp
export LC_ALL=C
compile_one() {
  local base="$1" triple="$2" name="$3"
  export PATH="$base/toolchain/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"
  export PKG_CONFIG_SYSROOT_DIR="$base/toolchain/$triple/sysroot"
  export PKG_CONFIG_LIBDIR="$PKG_CONFIG_SYSROOT_DIR/usr/lib/pkgconfig:$PKG_CONFIG_SYSROOT_DIR/usr/share/pkgconfig"
  "$base/toolchain/bin/$triple-gcc" --sysroot="$PKG_CONFIG_SYSROOT_DIR" -O2 -Wall /inputs/diagnostic.c -o "/work/$name" $(pkg-config --cflags --libs gtk+-3.0 webkit2gtk-4.1) -latomic
  "$base/toolchain/bin/$triple-readelf" -h -d "/work/$name" > "/work/$name.elf.txt"
  sha256sum "/work/$name"
}
'''
    for row in facts:
        script += f"compile_one '{row['canonical']}' '{row['triple']}' 'cloud-signin-window-{row['device']}'\n"
    library = facts[0]['canonical'] + '/toolchain/' + facts[0]['triple'] + '/sysroot/usr/lib'
    script += f"python3 -I /inputs/config-checks.py -- '{library}/ld-linux-x86-64.so.2' --library-path '{library}' /work/cloud-signin-window-GENERIC_X64 > /work/config-checks.json\n"
    return script


def write(path, value):
    with path.open('x') as stream:
        json.dump(value, stream, indent=2)
        stream.write('\n')


def main(candidate):
    packet = Path(__file__).resolve().parent
    if OWNER.exists() or OWNER.is_symlink():
        raise ValueError('fresh owner already exists')
    candidate_text = verified(candidate, CANDIDATE_SHA)
    host = verified(OLD / 'host-resources.py', HOST_SHA)
    inner = verified(OLD / 'inner-build.py', INNER_SHA)
    checks = config_checks(verified(CHECKS, CHECKS_SHA))
    runner = (packet / 'compile-owner.py.in').read_text()
    for text in [host, inner, checks, runner]:
        ast.parse(text)
    if os.getuid() == 0 or 4 not in os.sched_getaffinity(0):
        raise ValueError('nonroot original host with CPU4 available required')
    if subprocess.check_output(['git', '-C', str(ROOT), 'rev-parse', 'HEAD'], text=True, timeout=10).strip() != COMMIT:
        raise ValueError('frozen checkout differs')
    if subprocess.check_output(['git', '-C', str(ROOT), 'status', '--porcelain', '--untracked-files=no'], text=True, timeout=10).strip():
        raise ValueError('frozen checkout tracked state is dirty')
    facts = []
    for host_path, canonical, triple, device in TREES:
        compiler = Path(host_path) / 'toolchain/bin' / (triple + '-gcc')
        reference = Path(host_path) / 'build/cloud-signin-window-/cloud-signin-window'
        facts.append({'host': host_path, 'canonical': canonical, 'triple': triple, 'device': device,
                      'compiler_sha256': sha(compiler), 'reference_bytes': reference.stat().st_size,
                      'reference_sha256': sha(reference)})
    scripts = {'compile.py': runner, 'host-resources.py': host, 'inputs/inner-build.py': inner,
               'inputs/config-checks.py': checks, 'inputs/diagnostic.c': candidate_text,
               'inputs/compile.sh': compile_script(facts)}
    os.umask(0o077)
    OWNER.mkdir(mode=0o700)
    for relative in ['inputs', 'out', 'scan', 'submit', 'stages', 'stages/compile']:
        (OWNER / relative).mkdir(mode=0o700)
    for relative, text in scripts.items():
        with (OWNER / relative).open('x') as stream:
            stream.write(text)
    config = {'schema': 1, 'utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
        'checkout': str(ROOT), 'commit': COMMIT, 'host_pid_namespace': os.readlink('/proc/self/ns/pid'),
        'owner_label': OWNER.name, 'candidate_source': str(candidate), 'candidate_sha256': CANDIDATE_SHA,
        'image': IMAGE, 'trees': facts,
        'limits': {'cpu_ids': [4], 'cpus': 1, 'memory_mib': 1024, 'swap_bytes': 0, 'pids': 128,
                   'seconds': 180, 'tmpfs_bytes': 128 * 1024**2, 'scratch_budget_bytes': 192 * 1024**2,
                   'compiler_log_bytes': 2 * 1024**2},
        'host_observer': {'minimum_host_available_bytes': 8 * 1024**3,
                          'minimum_volume_available_bytes': 100 * 1024**3,
                          'disk_scan_timeout_seconds': 5, 'disk_sample_interval_seconds': 5},
        'helper_sha256': {relative: sha(OWNER / relative) for relative in scripts},
        'source_preparation': {'preparer_path': str(Path(__file__).resolve()), 'preparer_sha256': sha(Path(__file__)),
            'runner_template_sha256': sha(packet / 'compile-owner.py.in'),
            'derived_from': '/tmp/pix-browser-controls-compile-prepare.py',
            'derived_from_sha256': 'b1eb41d194d301cdad2e83f7c8997d8b7ac93d1331d8f99a7586d6369fbcf61a',
            'host_observer_sha256': HOST_SHA, 'inner_cgroup_wrapper_sha256': INNER_SHA,
            'original_twelve_case_source_sha256': CHECKS_SHA},
        'runtime_scope': 'two helper compiles and fourteen pre-GTK parser cases; no display/provider/VM/device/service'}
    write(OWNER / 'inputs.json', config)
    protected = [str(ROOT), TREES[1][0], str(candidate)]
    protected += [str(OWNER / path) for path in ['inputs.json', *scripts]]
    write(OWNER / 'retention-plan.json', {'volume': '/workspace', 'scan_roots': [str(OWNER / 'scan')],
        'reference_stores': [], 'protected': protected, 'candidates': [],
        'builds': [{'name': 'provider-proof-helper', 'terms_bytes': {'compile_scratch': 128 * 1024**2, 'outputs_and_records': 64 * 1024**2},
                   'basis': 'Two single-file compiles against read-only accepted toolchains. Prior reference binaries measured; no toolchain/tree copy. CPU4 only, 1GiB/no swap/no network, 180s producer deadline plus bounded cleanup. Tmpfs128MiB; 192MiB conservative allowance. Host resource and cgroup observation retain original result channels.',
                   'evidence': [{'path': str(OWNER / 'inputs.json'), 'sha256': sha(OWNER / 'inputs.json')}]}]})
    write(OWNER / 'admission-plan.json', {'checkout': str(ROOT), 'retention_plan': str(OWNER / 'retention-plan.json'),
        'retention_report': str(OWNER / 'retention-report.json'), 'stage': 'provider-proof-helper',
        'profiles': [{'PROJECT': 'ROCKNIX', 'DEVICE': row['device'], 'ARCH': 'x86_64' if row['device'] == 'GENERIC_X64' else 'aarch64'} for row in facts],
        'outputs': [{'path': str(OWNER), 'issue': 616, 'kind': 'qa-scratch',
                     'release_when': 'Retain exact helpers only for the immediately queued diagnostic qualification. Preserve compact source, compiler/parser/resource and original lifecycle receipts; consume original admission and retire superseded helpers.'}]})
    print(json.dumps({'owner': str(OWNER), 'prepared_only': True, 'candidate_sha256': CANDIDATE_SHA,
                      'parser_cases': 14, 'cpu_ids': [4], 'memory_mib': 1024, 'seconds': 180}))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--candidate', type=Path, default=CANDIDATE)
    args = parser.parse_args()
    main(args.candidate)

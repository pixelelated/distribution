#!/usr/bin/env python3
"""Coordinator-only tiny synthetic control. No compiler, Docker, VM or network.

Uses the exact documentation functions and unchanged admission nested() guard.
Not executed by the source lane; requires a new private scratch directory.
"""
import argparse
import hashlib
import importlib.machinery
import importlib.util
import json
import os
import shlex
from pathlib import Path
import subprocess
import sys

sys.dont_write_bytecode = True
BASELINE_SHA = '3e4b73f55cafde6a53d8afab228b3881449e10428d2b3c8a267cd02b94c310ac'
CANDIDATE_SHA = 'e574a017b83e0da4d9360017ed14d1edcab86eb979efcad1b15fd4bc76407baa'
BODY = '''set -eu
. "$1"
clean_doc_cache
start_system_doc
mkdir -p "$DOCTMP"
printf '%s' '|Fixture|System|2026|`fixture`|.rom|' > "$DOCTMP/fixture:system.tmp"
printf '%s' '**fixture:** core (default)<br>' > "$DOCTMP/fixture:emulators.tmp"
mk_system_doc
'''


def digest(value):
    return hashlib.sha256(value).hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--checkout', type=Path, required=True)
    parser.add_argument('--scratch', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    a = parser.parse_args()
    a.checkout = a.checkout.resolve(strict=True)
    prerequisites = json.loads(Path(__file__).with_name('prerequisites.json').read_text())
    for relative, expected in prerequisites['checkout_files'].items():
        assert digest((a.checkout / relative).read_bytes()) == expected, relative
    for relative, expected in prerequisites['templates'].items():
        path = a.checkout / relative
        assert (digest(path.read_bytes()) if path.exists() else None) == expected, relative
    toolchain = Path(prerequisites['toolchain'])
    for relative, expected in prerequisites['toolchain_files'].items():
        assert digest((toolchain / relative).read_bytes()) == expected, relative
    baseline = (a.checkout / 'distributions/ROCKNIX/config/functions').read_bytes()
    candidate = Path(__file__).with_name('candidate-functions').read_bytes()
    assert digest(baseline) == BASELINE_SHA
    assert digest(candidate) == CANDIDATE_SHA
    a.scratch.mkdir()
    # The complete real functions file parses config.xml at source time.
    # Keep its XML tool real; scope the retained SDK library path to that tool.
    host_bin = a.scratch.absolute() / 'host-bin'
    host_bin.mkdir()
    xml_wrapper = host_bin / 'xmlstarlet'
    xml_wrapper.write_text('#!/bin/sh\nexec /usr/bin/env LD_LIBRARY_PATH=' +
                           shlex.quote(str(toolchain / 'lib')) + ' ' +
                           shlex.quote(str(toolchain / 'bin/xmlstarlet')) + ' "$@"\n')
    xml_wrapper.chmod(0o700)
    xml_checks = []
    for device, expected in prerequisites['xml_queries'].items():
        result = subprocess.run([str(xml_wrapper), 'sel', '-t', '-m',
            '//rocknix/' + device + '/*[@mkimage_options]', '-v', 'name()', '-n',
            str(a.checkout / 'projects/ROCKNIX/config.xml')],
            env={'PATH': '/usr/bin:/bin', 'LC_ALL': 'C'}, capture_output=True, text=True, timeout=10)
        # xmlstarlet may return 1 for an empty selection (GENERIC_X64).
        assert result.returncode in ([0] if expected else [0, 1]), result.stderr
        assert result.stdout == expected and not result.stderr, (device, result.stdout, result.stderr)
        xml_checks.append({'device': device, 'returncode': result.returncode,
                           'stdout': result.stdout, 'stderr': result.stderr})
    source = a.checkout / 'tools/host-maintenance/build-admission'
    loader = importlib.machinery.SourceFileLoader('actual_admission', str(source))
    spec = importlib.util.spec_from_loader(loader.name, loader)
    guard = importlib.util.module_from_spec(spec)
    loader.exec_module(guard)
    rows = []
    # Run the actual exporter with a deliberately tiny, non-secret environment.
    # A direct Docker target writes .env before arming its watcher; Makefile's
    # explicit -e additionally forwards the subsequently created marker.
    exported = subprocess.check_output(['bash', str(a.checkout / 'scripts/get_env')],
        env={'PATH': '/usr/bin:/bin', 'RASTERATOPS_BUILD_RUN': '.build-runs/fixture'}, text=True, timeout=10)
    assert 'RASTERATOPS_BUILD_RUN=.build-runs/fixture' in exported.splitlines()
    assert '--env-file .env -e RASTERATOPS_BUILD_RUN -e PROJECT -e DEVICE -e ARCH' in (a.checkout / 'Makefile').read_text()
    rows.append({'name': 'actual-environment-exporter', 'result': 'PASS', 'docker_executed': False})

    def run(name, contents, watched=True, device='GENERIC_X64', arch='x86_64', missing_build=False):
        root = (a.scratch / name).absolute()
        root.mkdir()
        env = dict(os.environ, GIT_CONFIG_NOSYSTEM='1', GIT_CONFIG_GLOBAL='/dev/null')
        for key in ['RASTERATOPS_BUILD_RUN', 'RASTERATOPS_WATCH_EXEC', 'PIXELELATED_BUILD_ADMISSION', 'BUILD']:
            env.pop(key, None)
        def git(*args):
            return subprocess.check_output(['git', '-c', 'core.hooksPath=/dev/null', '-C', str(root), *args], env=env)
        git('init', '-q')
        (root / '.gitignore').write_text('/build.*/\n/.build-runs/\n/.doc_cache/\n')
        (root / 'functions').write_bytes(contents)
        (root / 'product-input').write_text('unchanged\n')
        (root / 'templates').mkdir()
        for template in ['HEADER.md', 'SUPPORTED_EMULATORS_AND_CORES.md']:
            p = a.checkout / 'templates' / template
            if p.exists():
                (root / 'templates' / template).write_bytes(p.read_bytes())
        legacy = root / 'documentation/PER_DEVICE_DOCUMENTATION' / device
        legacy.mkdir(parents=True)
        doc = legacy / 'SUPPORTED_EMULATORS_AND_CORES.md'
        original_doc = b'original tracked document\n'
        doc.write_bytes(original_doc)
        git('add', '.')
        git('-c', 'user.name=Fixture', '-c', 'user.email=fixture@example.invalid', 'commit', '-qm', 'fixture')
        build = root / ('build.pixelelated-' + device + '.' + arch)
        run_dir = root / '.build-runs/fixture'
        run_dir.mkdir(parents=True)
        profile = {'PROJECT': 'ROCKNIX', 'DEVICE': device, 'ARCH': arch}
        initial = guard.source_state(root)
        (run_dir / 'admission.json').write_text(json.dumps({'source': initial, 'profiles': [profile]}))
        env.update(profile, ROOT=str(root), SYSDOCROOT=str(legacy), SYSDOC=str(doc.with_suffix('')),
                   PROJECT_DIR=str(a.checkout / 'projects'), PATH=str(host_bin) + ':/usr/bin:/bin')
        if not missing_build:
            env['BUILD'] = str(build)
        if watched:
            env['RASTERATOPS_BUILD_RUN'] = '.build-runs/fixture'
        result = subprocess.run(['bash', '-c', BODY, '--', str(root / 'functions')], cwd=root, env=env,
                                capture_output=True, text=True, timeout=10)
        if missing_build:
            assert result.returncode != 0
            assert 'Build output directory is required' in result.stderr
            assert doc.read_bytes() == original_doc
            rows.append({'name': name, 'result': 'PASS', 'generation_refused': True})
            return None
        assert result.returncode == 0, result.stderr
        refused = False
        try:
            guard.nested(root, run_dir, profile)
        except ValueError as error:
            assert 'nested source differs from admission' in str(error), str(error)
            refused = True
        expected = contents == baseline or not watched
        assert refused == expected
        generated = build / 'documentation/PER_DEVICE_DOCUMENTATION' / device / doc.name if watched and contents == candidate else doc
        assert generated.is_file()
        assert b'Fixture|System' in generated.read_bytes()
        if watched and contents == candidate:
            assert doc.read_bytes() == original_doc
            assert guard.source_state(root) == initial
            (root / 'product-input').write_text('real source change\n')
            try:
                guard.nested(root, run_dir, profile)
            except ValueError as error:
                assert 'nested source differs from admission' in str(error)
            else:
                raise AssertionError('real tracked-source mutation was accepted')
        rows.append({'name': name, 'result': 'PASS', 'nested_refused': refused,
                     'generated_sha256': digest(generated.read_bytes()), 'generated_relative_path': str(generated.relative_to(root))})
        return generated.read_bytes()

    baseline_output = run('baseline-watched', baseline)
    assert run('candidate-watched', candidate) == baseline_output
    assert run('candidate-direct', candidate, watched=False) == baseline_output
    assert run('candidate-h700-arm', candidate, device='H700', arch='arm') == baseline_output
    assert run('candidate-h700-aarch64', candidate, device='H700', arch='aarch64') == baseline_output
    run('candidate-missing-build', candidate, missing_build=True)
    with a.output.open('x') as f:
        json.dump({'result': 'PASS', 'controls': rows,
                   'admission_tool_sha256': digest(source.read_bytes()),
                   'real_xml_prerequisites': xml_checks,
                   'prerequisites_sha256': digest(Path(__file__).with_name('prerequisites.json').read_bytes()),
                   'full_build_executed': False}, f, indent=2)
        f.write('\n')
    print('PASS: seven generated-documentation/environment controls; no full build')


if __name__ == '__main__':
    main()

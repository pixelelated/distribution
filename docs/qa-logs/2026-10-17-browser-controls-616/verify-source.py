#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-2.0
"""Bounded pure preparation checks; no compilation or browser execution."""
import argparse
import ast
import hashlib
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import time

sys.dont_write_bytecode = True


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--base', type=Path, required=True)
    parser.add_argument('--scratch', type=Path, required=True)
    args = parser.parse_args()
    packet = Path(__file__).resolve().parent
    started = time.monotonic()
    args.scratch.mkdir(mode=0o700)
    spec = importlib.util.spec_from_file_location('prepare616', packet / 'prepare.py')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    original = args.base.read_bytes()
    provenance = module.prepare(args.base, args.scratch / 'prepared')
    generated = (args.scratch / 'prepared/cloud-signin-window.c').read_text()
    cases = {'exact_source_prepared': True}
    tampered = args.scratch / 'tampered.c'
    tampered.write_bytes(original + b'\n/* negative control */\n')
    try:
        module.prepare(tampered, args.scratch / 'must-not-exist')
    except ValueError:
        cases['tampered_source_refused_without_output'] = not (args.scratch / 'must-not-exist').exists()
    else:
        cases['tampered_source_refused_without_output'] = False
    before = (args.scratch / 'prepared/cloud-signin-window.c').read_bytes()
    try:
        module.prepare(args.base, args.scratch / 'prepared')
    except FileExistsError:
        cases['existing_output_refused_unchanged'] = before == (args.scratch / 'prepared/cloud-signin-window.c').read_bytes()
    else:
        cases['existing_output_refused_unchanged'] = False
    cases['base_unchanged'] = args.base.read_bytes() == original
    ast_files = sorted(packet.glob('*.py'))
    for path in ast_files:
        ast.parse(path.read_text(), filename=path.name)
    cases['python_asts'] = True
    node = subprocess.run(['node', '--check', str(packet / 'observer.js')],
                          capture_output=True, text=True, timeout=3)
    cases['observer_javascript_syntax'] = node.returncode == 0
    html = (packet / 'input-control.html').read_text()
    js = html.split('<script>')[1].split('</script>')[0]
    (args.scratch / 'fixture.js').write_text(js)
    node_fixture = subprocess.run(['node', '--check', str(args.scratch / 'fixture.js')],
                                  capture_output=True, text=True, timeout=3)
    cases['fixture_javascript_syntax'] = node_fixture.returncode == 0
    setup = generated.split('static gboolean qa616_setup(')[1].split('\nstatic const char *allowed_host')[0]
    cases['off_guard_precedes_observer_setup_source_only'] = (
        setup.index('if (!qa616_observe) return TRUE;') < setup.index('g_cancellable_new()')
        < setup.index('webkit_user_script_new_for_world') < setup.index('g_timeout_add_full'))
    result = {'schema': 1, 'status': 'static/source preparation only',
              'pass': all(cases.values()), 'cases': cases,
              'seconds': time.monotonic() - started,
              'base_sha256': hashlib.sha256(original).hexdigest(),
              'diagnostic_source_sha256': provenance['diagnostic_source_sha256'],
              'python_ast_count': len(ast_files),
              'javascript_syntax_exit_codes': [node.returncode, node_fixture.returncode],
              'scratch_bytes': sum(p.stat().st_size for p in args.scratch.rglob('*') if p.is_file()),
              'compile_runtime_config_observer_browser_provider_checks': 'UNRUN'}
    print(json.dumps(result, indent=2))
    return 0 if result['pass'] else 1


if __name__ == '__main__':
    raise SystemExit(main())

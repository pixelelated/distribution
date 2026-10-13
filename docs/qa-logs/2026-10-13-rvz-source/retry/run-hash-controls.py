#!/usr/bin/env python3
"""UNRUN: follow-up-bound execution of the original synthetic hash controls."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import signal
import subprocess


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--binary', type=Path, required=True)
    parser.add_argument('--fixtures', type=Path, required=True)
    parser.add_argument('--es-source', type=Path, required=True)
    parser.add_argument('--baseline', action='store_true')
    args = parser.parse_args()
    binding = json.loads(Path(__file__).with_name('source-review.json').read_text())
    version = 'baseline' if args.baseline else 'candidate'
    for relative, expected in binding['es_files'][version].items():
        if hashlib.sha256((args.es_source / relative).read_bytes()).hexdigest() != expected:
            raise SystemExit('Source binding mismatch: ' + relative)
    binary = args.binary.resolve(strict=True)
    binary_sha256 = hashlib.sha256(binary.read_bytes()).hexdigest()
    # This source check plus executable hash is a receipt, not a build-provenance
    # proof. The coordinator must retain the build log/source-to-binary binding.
    cases = json.loads((args.fixtures / 'manifest.json').read_text())
    failures = 0
    for case in cases:
        expected = case['baseline'] if args.baseline else case['expected']
        if args.baseline and expected is None:
            print(json.dumps(dict(case=case['name'], result='SKIP',
                                  reason='old malformed-input behavior has no asserted contract')))
            continue
        path = (args.fixtures / case['name']).resolve(strict=True)
        if path.parent != args.fixtures.resolve() or hashlib.sha256(path.read_bytes()).hexdigest() != case['sha256']:
            raise SystemExit('Fixture binding mismatch')
        process = subprocess.Popen([str(binary), case['console'], str(path)],
                                   stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                   start_new_session=True)
        timed_out = False
        out = err = b''
        try:
            out, err = process.communicate(timeout=10)
        except subprocess.TimeoutExpired:
            timed_out = True
        finally:
            try:
                os.killpg(process.pid, signal.SIGKILL)
            except ProcessLookupError:
                pass
            if process.poll() is None:
                process.wait(timeout=2)
            process.stdout.close()
            process.stderr.close()
        wanted = ('FAIL' if expected is None else expected) + '\n'
        wanted_rc = 2 if expected in (None, 'FAIL') else 0
        passed = not timed_out and process.returncode == wanted_rc and out == wanted.encode() and not err
        print(json.dumps(dict(case=case['name'], version=version, rc=process.returncode,
                              stdout=out.decode(errors='replace'), stderr=err.decode(errors='replace'),
                              timed_out=timed_out, binary_sha256=binary_sha256,
                              source_commit=binding['es_commits'][version], fixture_sha256=case['sha256'],
                              expected_rc=wanted_rc, expected_stdout=wanted,
                              result='PASS' if passed else 'FAIL')), flush=True)
        failures += not passed
    return 1 if failures else 0


if __name__ == '__main__':
    raise SystemExit(main())

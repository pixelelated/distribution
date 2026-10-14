#!/usr/bin/env python3
"""Validate exact source/AST only; optionally materialize a fresh candidate tree."""
import argparse
import ast
import difflib
import gzip
import hashlib
import json
from pathlib import Path

PACKET = Path(__file__).resolve().parent


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def checked_sources(prepared):
    binding = json.loads((PACKET / 'bindings.json').read_text())
    assert sha((prepared / 'source.json').read_bytes()) == binding['prepared_source_json_sha256']
    source = prepared / 'tree'
    assert not list(source.rglob('*.pyc')), 'unbound bytecode'
    manifest = binding['prepared_python_manifest']
    assert {str(p.relative_to(source)) for p in source.rglob('*.py')} == set(manifest)
    files = {}
    for name, digest in manifest.items():
        path = source / name
        assert not path.is_symlink()
        raw = path.read_bytes()
        assert sha(raw) == digest, name
        ast.parse(raw, filename=name)
        files[name] = raw
    name = binding['path']
    baseline = files[name].decode()
    assert sha(files[name]) == binding['baseline_sha256']
    candidate = baseline
    for row in binding['replacements']:
        assert candidate.count(row['before']) == 1
        candidate = candidate.replace(row['before'], row['after'])
    assert sha(candidate.encode()) == binding['candidate_sha256']
    patch = gzip.decompress((PACKET / 'startup-handoff.patch.gz').read_bytes())
    assert sha(patch) == binding['patch_sha256']
    expected = ''.join(difflib.unified_diff(
        baseline.splitlines(keepends=True), candidate.splitlines(keepends=True),
        fromfile='a/' + name, tofile='b/' + name)).encode()
    assert patch == expected

    old = ast.parse(baseline)
    new = ast.parse(candidate)
    dump = lambda node: ast.dump(node, include_attributes=False)
    assert len(old.body) == len(new.body)
    changed = []
    for before, after in zip(old.body, new.body):
        if dump(before) != dump(after):
            changed.append(before.name)
    assert changed == ['ConnectivityMonitor', 'run_proxy_service'], changed
    old_monitor = next(n for n in old.body if getattr(n, 'name', '') == 'ConnectivityMonitor')
    new_monitor = next(n for n in new.body if getattr(n, 'name', '') == 'ConnectivityMonitor')
    old_run = next(n for n in old_monitor.body if getattr(n, 'name', '') == 'run')
    new_run = next(n for n in new_monitor.body if getattr(n, 'name', '') == 'run')
    assert dump(old_run.body[-1]) == dump(new_run.body[-1]), 'periodic loop changed'
    old_main = next(n for n in old.body if getattr(n, 'name', '') == 'run_proxy_service')
    new_main = next(n for n in new.body if getattr(n, 'name', '') == 'run_proxy_service')
    old_try = next(n for n in old_main.body if isinstance(n, ast.Try))
    new_try = next(n for n in new_main.body if isinstance(n, ast.Try))
    assert [dump(n) for n in old_try.finalbody] == [dump(n) for n in new_try.finalbody]
    for fixture in PACKET.glob('*.py'):
        ast.parse(fixture.read_bytes(), filename=str(fixture))
    return binding, files, candidate


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--prepared', type=Path, required=True)
    parser.add_argument('--candidate-output', type=Path)
    args = parser.parse_args()
    binding, files, candidate = checked_sources(args.prepared.resolve(strict=True))
    if args.candidate_output:
        dest = args.candidate_output.absolute()
        assert not dest.exists() and not dest.is_symlink(), 'fresh destination required'
        assert any(dest.is_relative_to(p) for p in (Path('/tmp'), Path('/workspace/tmp'), Path('/run')))
        dest.mkdir(parents=True, mode=0o700)
        files[binding['path']] = candidate.encode()
        for name, raw in files.items():
            path = dest / 'tree' / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(raw)
        # Original preparation provenance, with the repaired file separately bound.
        (dest / 'source.json').write_bytes((args.prepared / 'source.json').read_bytes())
        (dest / 'manifest.json').write_text(json.dumps({n: sha(b) for n, b in files.items()}, indent=2) + '\n')
    print(json.dumps({'status': 'PASS', 'scope': 'source hashes and AST only',
                      'files': len(files), 'baseline': binding['baseline_sha256'],
                      'candidate': binding['candidate_sha256'],
                      'unchanged': ['periodic loop', 'shutdown', 'all other top-level definitions',
                                    '111 other Python files'],
                      'fixture_execution': 'UNRUN',
                      'materialized': str(args.candidate_output) if args.candidate_output else None}, indent=2))


if __name__ == '__main__':
    main()

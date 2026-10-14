#!/usr/bin/env python3
"""AST/bytes/receipt inspection only. Never import fixtures or open archive.zip."""
import ast
import collections
import copy
import difflib
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
PRIOR = HERE.parent / '2026-10-14-steam-client-host-download-source'


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def dump(node):
    return ast.dump(node, include_attributes=False)


def calls(tree, name):
    return collections.Counter(dump(n) for n in ast.walk(tree) if isinstance(n, ast.Call) and ast.unparse(n.func) == name)


def main():
    source = json.loads((HERE / 'source.json').read_bytes())
    for name, expected in source['prior_files'].items():
        assert sha(PRIOR / name) == expected, name
    assert sha(PRIOR / 'SHA256SUMS') == source['original_packet_manifest_sha256']
    unchanged = ['runner.py', 'hash_archive.py', 'verify_archive.py', 'vm-admission.schema.json', *source['bound_files']]
    for name in unchanged:
        assert (HERE / name).read_bytes() == (PRIOR / name).read_bytes(), name
    prior_source = json.loads((PRIOR / 'source.json').read_bytes())
    assert source['limits'] == prior_source['limits']
    trees = {f.name: ast.parse(f.read_text(), filename=str(f)) for f in sorted(HERE.glob('*.py'))}
    for f in HERE.glob('*.json'):
        if f.name != 'static-result.json':
            json.loads(f.read_bytes())
    old_text = (PRIOR / 'download.py').read_text()
    new_text = (HERE / 'download.py').read_text()
    assert old_text.count("metadata['request_size']") == 1
    assert new_text == old_text.replace("metadata['request_size']", "metadata['size_request']")
    old_download = ast.parse(old_text)
    assert calls(old_download, 'runner.require') == calls(trees['download.py'], 'runner.require')
    assert calls(old_download, 'runner.run') == calls(trees['download.py'], 'runner.run')
    expected = copy.deepcopy(old_download)
    changed = 0
    for node in ast.walk(expected):
        if isinstance(node, ast.Subscript) and isinstance(node.value, ast.Name) and node.value.id == 'metadata' and isinstance(node.slice, ast.Constant) and node.slice.value == 'request_size':
            node.slice.value = 'size_request'
            changed += 1
    assert changed == 1 and dump(expected) == dump(trees['download.py'])
    old_vm_text = (PRIOR / 'vm_verify.py').read_text()
    new_vm_text = (HERE / 'vm_verify.py').read_text()
    old_vm, new_vm = ast.parse(old_vm_text), trees['vm_verify.py']
    assert not calls(old_vm, 'runner.require') - calls(new_vm, 'runner.require'), 'Original VM predicate lost'
    for name in ('runner.run', 'runner.accepted', 'os.open', 'os.close', 'os.statvfs', 'signal.signal', 'libc.prctl'):
        assert calls(old_vm, name) == calls(new_vm, name), name
    for tree in (old_vm, new_vm):
        function = next(n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == 'load_runner')
        assert dump(function) == dump(next(n for n in old_vm.body if isinstance(n, ast.FunctionDef) and n.name == 'load_runner'))
    assert "if args.recovery is None:" in new_vm_text
    assert new_vm_text.index('recovery.accept_recovery(') < new_vm_text.index('child = runner.run(')
    recover = trees['recover.py']
    run_calls = [n for n in ast.walk(recover) if isinstance(n, ast.Call) and ast.unparse(n.func) == 'runner.run']
    assert len(run_calls) == 1 and ast.unparse(run_calls[0].args[0]) == "[sys.executable, '-I', '-S', '-B', str(HERE / 'hash_archive.py'), '--archive', str(archive)]"
    assert not any(isinstance(n, ast.Import) and any(a.name in ('socket', 'zlib', 'zipfile', 'urllib', 'subprocess') for a in n.names) for n in ast.walk(recover))
    for old, new, name, label in ((old_text, new_text, 'download.diff', 'download.py'), (old_vm_text, new_vm_text, 'vm-verify.diff', 'vm_verify.py')):
        expected_diff = ''.join(difflib.unified_diff(old.splitlines(True), new.splitlines(True), fromfile='sealed-6c27/' + label, tofile='correction/' + label))
        assert (HERE / name).read_text() == expected_diff
    count = 0
    for group in ('original_download', 'original_owner'):
        root = Path(source[group + '_dir'])
        for name, row in source[group + '_files'].items():
            assert name != 'archive.zip'
            assert (root / name).stat().st_size == row['bytes'] and sha(root / name) == row['sha256']
            count += 1
    directory = Path(source['original_download_dir'])
    original = json.loads((directory / 'result.json').read_bytes())
    assert original['status'] == 'FAIL' and original['error'] == "KeyError('request_size')"
    raw = (directory / 'transport.stdout').read_bytes()
    assert raw.count(b'\nPIX_INTAKE_CURL_JSON\n') == 1
    metadata = json.loads(raw.split(b'\nPIX_INTAKE_CURL_JSON\n', 1)[1])
    assert metadata['size_request'] == 221 and 'request_size' not in metadata
    assert metadata == original['curl_metadata']
    assert original['limits'] == source['limits']
    print(json.dumps({'passed': True, 'evidence_level': 'static AST/bytes and original small-receipt parse only',
        'runtime': 'UNRUN corrected download/recovery/VM adapter; no archive payload opened',
        'prior_packet_files_unchanged': len(source['prior_files']), 'unchanged_current_files': unchanged,
        'python_asts': sorted(trees), 'download_single_literal_change_only': True,
        'original_download_predicates_preserved': sum(calls(old_download, 'runner.require').values()),
        'original_download_child_invocations_unchanged': True,
        'original_VM_predicates_preserved': sum(calls(old_vm, 'runner.require').values()),
        'VM_decoder_invocation_fd_limits_admission_and_cleanup_unchanged': True,
        'recovery_child': 'one unchanged hash_archive.py child; no download or decoder invocation',
        'original_receipts_bound_and_unchanged': count,
        'observed_original_wrapper_status': 'FAIL1', 'observed_curl_size_request': metadata['size_request'],
        'limits': source['limits'], 'remaining': ['Coordinator recovery run and source-bound negative controls', 'Separate admitted offline VM verification before any archive-format conclusion']}, indent=2))


if __name__ == '__main__':
    main()

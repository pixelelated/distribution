#!/usr/bin/env python3
"""Read-only binding of the coordinator's compile-only qualification."""
import hashlib
import json
from pathlib import Path

COMMIT = '969354955741d6c0ca8ce816e1c59ad338b1605b'

def sha(path):
    with path.open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()

def verify(path):
    value = json.loads(path.read_text())
    assert value['schema'] == 1 and value['source_commit'] == COMMIT
    assert value['allowed_compile_only'] is True and value['runtime_authorized'] is False
    assert value['critical_pairs_match'] is True and value['missing_dependencies'] == []
    for reference in [value['runtime_inventory'], *value['closure_evidence']]:
        source = Path(reference['path'])
        assert source.is_absolute() and sha(source) == reference['sha256']
    inventory = json.loads(Path(value['runtime_inventory']['path']).read_text())
    assert inventory['source_commit'] == COMMIT and inventory['read_only'] is True
    assert inventory['target_code_executed'] is False
    assert len(inventory['closure']) == 94 and len(inventory['edges']) == 378
    assert all(row['resolved_layer'] and row['resolved_path'] for row in inventory['edges'])
    assert len(inventory['critical_artifacts']) == 11
    assert all(row['matching_normalized_load_bytes'] is True and
               row['package_load_identity'] == row['sysroot_load_identity']
               for row in inventory['critical_artifacts'])
    assert inventory['forbidden_search_paths'] == value['rpath_findings']
    assert len(value['rpath_findings']) == 6
    assert all(row['layer'] == 'accepted-runtime-image' for row in value['rpath_findings'])
    expected_errors = [row['reason'] + ': ' + row['search_path'] + ' from ' + row['path']
                       for row in value['rpath_findings']]
    assert inventory['errors'] == expected_errors and inventory['status'] == 'FAIL'
    return value

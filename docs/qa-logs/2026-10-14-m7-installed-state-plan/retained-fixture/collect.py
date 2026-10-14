#!/usr/bin/env python3
"""Validate serial transport, original guest exit marker and value-free report."""
import argparse
import json
from pathlib import Path
import re

p = argparse.ArgumentParser(description=__doc__)
p.add_argument('--phase', required=True, choices=['seed', 'before', 'after', 'backup'])
p.add_argument('--serial', required=True, type=Path)
p.add_argument('--transport-rc', required=True, type=Path)
p.add_argument('--output', required=True, type=Path)
a = p.parse_args()
result = {'schema': 1, 'phase': a.phase, 'result': 'FAIL'}
try:
    raw = a.serial.read_bytes()
    assert len(raw) <= 2 * 1024**2
    text = raw.decode().replace('\r\n', '\n')
    marker = 'PIX_INSTALLED_STATE_' + a.phase.upper() + '_RC='
    codes = re.findall(re.escape(marker) + r'([0-9]+)', text)
    assert text.count(marker) == 1 and codes == ['0']
    assert a.transport_rc.read_text().strip() == '0'
    rows = []
    for line in text.splitlines():
        if line.startswith('{'):
            row = json.loads(line)
            if row.get('schema') == 1 and row.get('phase') == a.phase:
                rows.append(row)
    assert len(rows) == 1 and rows[0]['result'] == 'PASS' and rows[0]['stage'] == 'complete'
    checks = rows[0]['checks']
    required = {'archive_credentials_absent', 'archive_user_identifiers_preserved',
                'archive_harmless_settings_preserved', 'archive_token_file_absent',
                'selected_runtime_bytes_unchanged', 'frontend_restored'} if a.phase == 'backup' else {
                'ra_fields_equal', 'screenscraper_fields_equal', 'automatic_operations_disabled',
                'history_fields_equal', 'activity_stamp_bytes_equal', 'standalone_token_equal',
                'loaded_recent_history'}
    if a.phase in {'before', 'after'}:
        required |= {'retained_policy_pass', 'expected_build_and_executing_es'}
    assert all(checks.get(key) is True for key in required)
    result = rows[0]
except Exception:
    result['error'] = 'original-transport-guest-result-or-assertion-failed'
with a.output.open('x') as stream:
    json.dump(result, stream, indent=2)
    stream.write('\n')
print(json.dumps({'phase': a.phase, 'result': result['result']}))
raise SystemExit(0 if result['result'] == 'PASS' else 1)

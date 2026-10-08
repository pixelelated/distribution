"""#524 PL-004: malformed JSON shapes reject without losing ceremony reports.

Host-only temporary fixtures and deterministic command/tracker stubs; no network,
VM, repository tracker writes or completion marker edits outside the fixture.
Run: python3 -I -B this-file.py /path/to/tools/ceremony-check
"""
import contextlib
import copy
import datetime as dt
import hashlib
import importlib.machinery
import importlib.util
import io
import json
import os
from pathlib import Path
import sys
import tempfile
from unittest.mock import patch

source = Path(sys.argv[1]).resolve()
loader = importlib.machinery.SourceFileLoader('ceremony_shapes', str(source))
spec = importlib.util.spec_from_loader(loader.name, loader)
mod = importlib.util.module_from_spec(spec)
loader.exec_module(mod)
now = dt.datetime(2026, 10, 8, 12, tzinfo=dt.timezone.utc)
ended = '2026-10-07T02:53:02.029760+00:00'
results = []


def control(name, operation):
    try:
        detail = operation()
    except Exception as error:
        results.append({'name': name, 'passed': False,
                        'error': type(error).__name__ + ': ' + str(error)})
    else:
        results.append({'name': name, 'passed': True, 'detail': detail})


with tempfile.TemporaryDirectory(prefix='audit-receipt-shapes-') as tmp:
    root = Path(tmp)
    audit = root / 'docs/audits/2026_10_07-shape-control'
    audit.mkdir(parents=True)
    marker = audit / 'audit-completion.json'
    files = {
        str((audit / '04-analysis.md').relative_to(root)): 'analysis',
        str((audit / '05-punch-list.md').relative_to(root)): 'resolved outcomes',
        'tracker.json': json.dumps(dict(number=524, state='closed',
                                       state_reason='completed', body='- [x] PL-004: resolved')),
        'completion.json': json.dumps(dict(result='PASS', exact_bodies_and_states=True,
                                          closed_completed=[524], verified_utc=ended)),
    }
    original = dict(schema=1, issue=524, completed_at=ended,
                    tracker_readback='tracker.json', tracker_completion='completion.json',
                    evidence={name: hashlib.sha256(text.encode()).hexdigest()
                              for name, text in files.items()})

    def prepare(position=None, value=None):
        for name, text in files.items():
            (root / name).write_text(text)
        data = copy.deepcopy(original)
        if position == 'marker':
            data = value
        elif position in ('evidence', 'completed_at'):
            data[position] = value
        elif position in ('tracker', 'completion'):
            name = position + '.json'
            text = json.dumps(value)
            (root / name).write_text(text)
            data['evidence'][name] = hashlib.sha256(text.encode()).hexdigest()
        marker.write_text(json.dumps(data))

    def valid_receipt():
        prepare()
        assert mod.completed_audit_marker(marker, root, now) == (dt.datetime.fromisoformat(ended), 524)
        return 'Exact completion time and issue retained.'

    def invalid_receipt(position, value):
        prepare(position, value)
        try:
            mod.completed_audit_marker(marker, root, now)
        except ValueError as error:
            assert str(error)
            return str(error)
        raise AssertionError('malformed shape was accepted')

    control('valid receipt keeps exact cadence cutoff', valid_receipt)
    shapes = [('null', None), ('boolean', False), ('number', 7), ('string', 'invalid'), ('list', [])]
    for position in ('marker', 'evidence', 'tracker', 'completion'):
        for label, value in shapes:
            # A full key list reaches the old .items() call; an empty list does not.
            if position == 'evidence' and label == 'list':
                value = list(original['evidence'])
            control(position + ': ' + label,
                    lambda position=position, value=value: invalid_receipt(position, value))
    for label, value in shapes:
        if label == 'string':
            label, value = 'object', {}
        control('completed_at: ' + label,
                lambda value=value: invalid_receipt('completed_at', value))

    (root / 'docs/friction-log.md').write_text('')
    weekly = root / 'docs/work-logs/2026_10-work_logs/2026-W40-summary.md'
    weekly.parent.mkdir(parents=True)
    weekly.write_text('summary')
    monthly = root / 'docs/work-logs/2026_09-work_logs/SUMMARY.md'
    monthly.parent.mkdir(parents=True)
    monthly.write_text('summary')

    def full_report(valid):
        prepare() if valid else prepare('marker', [])
        calls = []

        def command(args, timeout=120):
            calls.append(args)
            return 0, 'local deterministic control', ''

        def tracker(args):
            calls.append(['gh'] + args)
            return [], None

        output = io.StringIO()
        with patch.object(mod, 'ROOT', str(root)), patch.object(mod, 'sh', command), \
                patch.object(mod, 'gh_json', tracker), \
                patch.object(mod, 'issue_coverage', lambda: (True, 'fixture history')), \
                patch.object(sys, 'argv', ['ceremony-check']), \
                patch.dict(os.environ, {'CEREMONY_TODAY': '2026-10-08'}), \
                contextlib.redirect_stdout(output):
            rc = mod.main()
        text = output.getvalue()
        assert all(word in text for word in ['index', 'register', 'rules', 'futro', 'hygiene'])
        searches = [' '.join(call) for call in calls if 'number,closedAt' in call]
        assert len(searches) == 1
        if valid:
            assert rc == 0 and 'invalid completion marker' not in text
            assert 'closed:>=2026-10-07' in searches[0]
            assert 'via #524' in text and 'nothing overdue.' in text
        else:
            assert rc == 1 and 'invalid completion marker' in text
            assert 'closed:>=2026-09-21' in searches[0]
            assert '17 days since 2026-09-21' in text
            assert 'via #524' not in text and 'Traceback' not in text
        return {'exit_code': rc, 'closure_query': searches[0], 'report': text}

    control('full report: valid receipt resets cadence', lambda: full_report(True))
    control('full report: malformed receipt diagnosed without resetting cadence', lambda: full_report(False))

passed = all(row['passed'] for row in results)
print(json.dumps({'result': 'PASS' if passed else 'FAIL', 'controls': results,
                  'tool_sha256': hashlib.sha256(source.read_bytes()).hexdigest()}, indent=2))
sys.exit(0 if passed else 1)

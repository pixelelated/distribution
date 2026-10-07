"""#489 receipt integrity and exact-time controls; live resolution lint is separate."""
import copy
import datetime as dt
import hashlib
import importlib.machinery
import importlib.util
import json
from pathlib import Path
import sys
import tempfile

source = Path(sys.argv[1]).resolve()
loader = importlib.machinery.SourceFileLoader('ceremony', str(source))
spec = importlib.util.spec_from_loader(loader.name, loader)
mod = importlib.util.module_from_spec(spec); loader.exec_module(mod)
results = []
now = dt.datetime(2026, 10, 7, 3, tzinfo=dt.timezone.utc)
ended = '2026-10-07T02:53:02.029760+00:00'
with tempfile.TemporaryDirectory(prefix='audit-cadence-controls-') as tmp:
    root = Path(tmp); audit = root/'docs/audits/2026_10_06-example'; audit.mkdir(parents=True)
    files = {'docs/audits/2026_10_06-example/04-analysis.md':'analysis',
             'docs/audits/2026_10_06-example/05-punch-list.md':'resolved outcomes',
             'tracker.json':json.dumps(dict(number=471,state='closed',state_reason='completed',body='- [x] PL-001: resolved')),
             'completion.json':json.dumps(dict(result='PASS',exact_bodies_and_states=True,closed_completed=[471],verified_utc=ended))}
    original = dict(schema=1,issue=471,completed_at=ended,tracker_readback='tracker.json',
                    tracker_completion='completion.json',evidence={})
    for name, text in files.items():
        (root/name).write_text(text)
        original['evidence'][name] = hashlib.sha256(text.encode()).hexdigest()
    marker = audit/'audit-completion.json'
    def trial(name, mutate=None, valid=False):
        for path, text in files.items(): (root/path).write_text(text)
        data = copy.deepcopy(original)
        if mutate: mutate(data)
        marker.write_text(json.dumps(data))
        try:
            result = mod.completed_audit_marker(marker, root, now)
        except (ValueError,KeyError,TypeError,OSError):
            assert not valid,name
        else:
            assert valid,name
            assert result == (dt.datetime.fromisoformat(ended),471)
        results.append(dict(name=name,passed=True))
    def change_file(data, path, value):
        (root/path).write_text(json.dumps(value))
        data['evidence'][path] = hashlib.sha256((root/path).read_bytes()).hexdigest()
    trial('valid underscore-date phased audit',valid=True)
    trial('missing required evidence',lambda d:d['evidence'].pop('tracker.json'))
    trial('tampered evidence',lambda d:(root/'tracker.json').write_text('{}'))
    trial('future completion',lambda d:d.update(completed_at='2027-01-01T00:00:00Z'))
    trial('unbound completion timestamp',lambda d:d.update(completed_at='2026-10-07T02:54:00Z'))
    trial('naive timestamp',lambda d:d.update(completed_at='2026-10-07T02:53:02'))
    trial('wrong issue identity',lambda d:d.update(issue=472))
    trial('unchecked closed audit',lambda d:change_file(d,'tracker.json',dict(number=471,state='closed',state_reason='completed',body='- [x] Done\n- [ ] Pending')))
    trial('open audit',lambda d:change_file(d,'tracker.json',dict(number=471,state='open',state_reason=None,body='- [x] Done')))
    trial('unverified tracker completion',lambda d:change_file(d,'completion.json',dict(result='FAIL',exact_bodies_and_states=True,closed_completed=[471],verified_utc=ended)))
    trial('malformed schema',lambda d:d.update(schema=99))
    trial('unsafe absolute evidence',lambda d:d['evidence'].update({'/etc/passwd':'0'*64}))
    marker.write_text('{invalid')
    try: mod.completed_audit_marker(marker,root,now)
    except ValueError: results.append(dict(name='malformed JSON',passed=True))
    else: raise AssertionError('malformed JSON accepted')
cutoff=dt.datetime.fromisoformat(ended)
rows=[dict(closedAt=(cutoff+dt.timedelta(seconds=n)).isoformat()) for n in [-1,0,1]]
assert mod.closures_after(rows,cutoff)==1
results.append(dict(name='only later closures count, same-day and exact-time boundary',passed=True))
assert mod.AUDIT_CLOSED_ISSUES==12 and mod.AUDIT_DAYS==14
results.append(dict(name='existing 12-closure/14-day policy unchanged',passed=True))
print(json.dumps(dict(result='PASS',controls=results,tool_sha256=hashlib.sha256(source.read_bytes()).hexdigest()),indent=2))

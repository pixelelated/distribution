from pathlib import Path
import datetime, hashlib, json

owner = Path('/workspace/tmp/pixelelated-m7-ui-14')
root = owner / 'artifacts'
assert json.loads((owner / 'completion.json').read_text())['job_rc'] == 0
assert json.loads((owner / 'backend-cleanup.json').read_text())['owned_backend_absent']
rows = json.loads(Path('/tmp/pixelelated-ui14-reviewed.json').read_text())
actual = sorted(str(f) for f in root.rglob('*.png')
                if not f.relative_to(root).parts[0].startswith('boot-'))
assert len(rows) == len(actual) == 70
assert sorted(r['path'] for r in rows) == actual
for row in rows:
    assert row['passed'] and row['method'] == 'Direct view_image'
    assert hashlib.sha256(Path(row['path']).read_bytes()).hexdigest() == row['sha256']
lifetimes = []
for f in sorted(root.glob('*/*-lifecycle/result.json')):
    result = json.loads(f.read_text())
    before = json.loads(f.with_name('before.json').read_text())['processes']
    after = json.loads(f.with_name('after.json').read_text())['processes']
    assert len(before) == 1 and before == after
    assert result['passed'] and result['same_pid_and_start_ticks']
    assert result['journal_rc'] == 0 and result['walk_exception'] is None
    lifetimes.append(dict(path=str(f), sha256=hashlib.sha256(f.read_bytes()).hexdigest(),
                          process=before[0], result=result))
assert len(lifetimes) == 12
captures = []
for f in sorted(root.glob('*/result.json')):
    result = json.loads(f.read_text())
    assert result['dimensions_match']
    expected = 25 if f.parent.name == 'en_US-640x480' else 15
    assert result['frames'] == expected
    captures.append(result)
assert len(captures) == 4
renderers = []
for f in sorted(root.glob('renderer-ui-*.json')):
    r = json.loads(f.read_text())
    assert r['passed'] and r['mode'] == 'software'
    assert r['process']['graphics_env']['WLR_RENDERER'] == 'pixman'
    renderers.append(dict(path=str(f), sha256=hashlib.sha256(f.read_bytes()).hexdigest()))
assert len(renderers) == 2
result = dict(utc=datetime.datetime.now(datetime.timezone.utc).isoformat(), passed=True,
              method='Direct view_image of all70 menu/Tools frames; recomputed12 ES process lifetimes from original before/after records.',
              frames=rows, lifetimes=lifetimes, captures=captures, renderers=renderers,
              limitations=['Existing long-label marquees and description scrolling are preserved; one Tools frame does not show an entire long paragraph.',
                           'The English640 manual-update URL wraps across lines but retains the complete address and instructions.',
                           'This is software/Pixman UI proof. QA14 and memory12 separately cover accelerated graphics.',
                           'Boot05, not these unreviewed boot captures, supplies exact splash acceptance.'])
with (owner / 'visual-review.json').open('x') as f:
    f.write(json.dumps(result, indent=2) + '\n')
print(json.dumps(dict(passed=True, frames=len(rows), lifetimes=len(lifetimes))))

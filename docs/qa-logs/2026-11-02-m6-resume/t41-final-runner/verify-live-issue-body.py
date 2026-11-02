#!/usr/bin/env python3
"""Execute only the corrected T41 live-issue predicate; preserve the failed full run."""
import datetime
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parent
TIP = 'e481e4a4a5c296c8f12e9654b6a45c4fb27bd3b0'
COORD = 'afdec2bf8b88135befcb7ec56efb3a7ea327bd73'
DISPATCH = 'd7dd76665983cb87dba62397691500fcf409fafe'
sha = lambda b: hashlib.sha256(b).hexdigest()
stamp = lambda: datetime.datetime.now(datetime.timezone.utc).isoformat()

def main():
    out = ROOT / 'issue-body-live'
    out.mkdir(exist_ok=False)
    old = (ROOT / 't41-accept.sh').read_bytes()
    new = (ROOT / 'issue-body-correction/t41-accept.sh').read_bytes()
    before = b"need('reviewed-at-es:' not in t and 'fixed-at-es:' not in t,'ES header present')"
    after = br"need(not re.search(r'^[ \t*`-]*(?:reviewed-at-es|fixed-at-es)[*`]*[ \t]*:',t,re.M),'ES header present')"
    assert old.count(before) == 1 and old.replace(before, after) == new
    controls = json.loads((ROOT / 'issue-body-correction/issue-body-review/after.json').read_text())
    assert len(controls['results']) == 28 and all(x['ok'] for x in controls['results'])
    argv = ['gh', 'api', 'repos/pixelelated/distribution/issues/688']
    start = stamp(); clock = time.monotonic()
    p = subprocess.run(argv, capture_output=True, timeout=120)
    elapsed = time.monotonic() - clock
    command = {'argv': argv, 'start': start, 'end': stamp(), 'elapsed_seconds': elapsed,
               'rc': p.returncode, 'stdout_sha256': sha(p.stdout), 'stderr_sha256': sha(p.stderr)}
    (out / 'live-688.stdout').write_bytes(p.stdout)
    (out / 'live-688.stderr').write_bytes(p.stderr)
    (out / 'command.json').write_text(json.dumps(command, indent=2) + '\n')
    assert p.returncode == 0
    live = json.loads(p.stdout)
    previous = None
    for line in (ROOT / 'root-final-run/command-receipts.jsonl').open():
        row = json.loads(line)
        if row['file'] == '0001-live-688.json':
            previous = json.loads(row['outputs']['stdout']['text']); break
    assert previous is not None and live['title'] == previous['title'] and live['body'] == previous['body']
    os.environ['DIST_REPO'] = str(ROOT.parents[3])
    os.environ['DISPATCH_TIP'] = DISPATCH
    os.environ.pop('ACCEPT_FIXTURE_ROOT', None)
    ns = {'__name__': 'coordinator_narrow_live_gate'}
    source = (ROOT / 'issue-body-correction/t41_checks.py').read_bytes()
    assert sha(source) == 'dde98a45fca9fdf959e1c5544f81c5cdf78c7359427b57cb4474ea376be3c5da'
    exec(compile(source.decode().split("\nif __name__=='__main__':")[0], 't41_checks.py', 'exec'), ns)
    sys.argv = ['coordinator-narrow-live-gate', TIP, COORD]
    reader = ns['Reader']()
    calls = []
    def issue(n, comments=False):
        assert n == 688 and comments is False
        calls.append(n)
        return live
    reader.issues = issue
    reason = ns['check'](reader, 'issue-body')
    assert calls == [688]
    driver = json.loads((ROOT / 'root-final-run/driver-result.json').read_text())
    result = {'schema': 1, 'executor': driver['executor'], 'time': stamp(),
              'tip': TIP, 'coordinator': COORD, 'dispatch': DISPATCH,
              'scope': 'Only corrected live issue-body gate; not a new full-suite run.',
              'section': 'issue-body', 'state': 'PASS', 'reason': reason,
              'original_runner_sha256': sha(old), 'corrected_runner_sha256': sha(new),
              'all_other_predicate_code_unchanged': True, 'live_title_body_unchanged': True,
              'original_full_run_rc': driver['rc'], 'retained_other_passes': 53,
              'pure_controls_passed': 28, 'live_command': command}
    (out / 'result.json').write_text(json.dumps(result, indent=2) + '\n')
    print('PASS issue-body; prior 53 PASS retained unchanged; original full run remains rc1.')

if __name__ == '__main__':
    main()

#!/usr/bin/env python3
"""Continue only T42's failed log-merge seam and remaining new integration gates."""
import ast
import datetime
import hashlib
import json
import os
from pathlib import Path
import re
import signal
import subprocess
import sys
import time

REPO = Path('/workspace/repos/pixelelated/distribution.worktrees/m6-renovation-plan-346')
ROOT = Path('/workspace/tmp/m6-coordinator/t42-final-20261102T2101')
TIP = '4cf8c8820791624dbddad3eb3664101a03953a82'
COORD = '8b83e452459f6696ac959b4e4e5494701d5d2f93'
BASE = '07d01c898fba867e042342017fd8d5257508a28c'
LOG = 'docs/work-logs/2026_11-work_logs/2026_11_02-work_log.md'
INDEX = 'docs/work-logs/INDEX.md'
AUDIT = 'docs/audits/2026_11_02-epic-m6-patches-shipped'
PREFIX_HASH = 'cdd4e04f41743495de00b81bd2b034d9aa970e9d04451907ed4d3baaf790f964'
sha = lambda b: hashlib.sha256(b).hexdigest()
stamp = lambda: datetime.datetime.now(datetime.timezone.utc).isoformat()

def need(ok, message):
    if not ok:
        raise ValueError(message)

def main():
    previous = json.loads((ROOT / 'result.json').read_text())
    need(previous['state'] == 'FAIL' and previous['commands'] == 21 and
         previous['error'] == 'append suffix lacks whole entries or exact terminal newline', 'unexpected previous failure')
    old = json.loads((ROOT / 'commands.json').read_text())
    for record in old:
        for stream in ['stdout', 'stderr']:
            need(sha((ROOT / record[stream]).read_bytes()) == record[stream+'_masked_sha256'], 'old receipt changed')
    need(next(r for r in old if r['name'] == 'lane-final-byte-scan')['rc'] == 0, 'missing exact-final lane scan')
    out = ROOT / 'continuation'; out.mkdir(exist_ok=False)
    merged = ROOT / 'integration'; events = []
    src = (REPO / 'docs/qa-logs/2026-11-02-m6-resume/t41-final-runner/t41_execution.py').read_bytes()
    need(sha(src) == 'bab9838ac263f976ba73a73ab162614e132cf97a0dcfd8a781d1ed243e54bfd9', 'pure helper drift')
    nodes = [n for n in ast.parse(src).body if isinstance(n, ast.FunctionDef) and n.name in ['merge_append_bytes', 'mask_log']]
    ns = dict(need=need, Invalid=ValueError, re=re, datetime=datetime, sha=sha)
    exec(compile(ast.Module(body=nodes, type_ignores=[]), '<unchanged pure helpers>', 'exec'), ns)
    env = dict(os.environ, LC_ALL='C', GIT_CONFIG_GLOBAL='/dev/null', GIT_CONFIG_NOSYSTEM='1',
               GIT_OPTIONAL_LOCKS='0', GIT_TERMINAL_PROMPT='0', PYTHONDONTWRITEBYTECODE='1',
               GIT_CONFIG_COUNT='1', GIT_CONFIG_KEY_0='core.hooksPath', GIT_CONFIG_VALUE_0='/dev/null')
    env.pop('ES_SRC', None)
    (out / 'start.json').write_text(json.dumps({'time': stamp(), 'executor': previous['executor'],
        'tip': TIP, 'coordinator': COORD, 'original_result_sha256': sha((ROOT/'result.json').read_bytes()),
        'runner_sha256': sha(Path(__file__).read_bytes()), 'affinity': sorted(os.sched_getaffinity(0))}, indent=2)+'\n')

    def command(name, argv, expected=(0,), timeout=240):
        start = stamp(); clock = time.monotonic(); timed = False
        p = subprocess.Popen(argv, cwd=merged, env=env, stdout=subprocess.PIPE, stderr=subprocess.PIPE, start_new_session=True)
        try: stdout, stderr = p.communicate(timeout=timeout)
        except subprocess.TimeoutExpired:
            timed = True; os.killpg(p.pid, signal.SIGKILL); stdout, stderr = p.communicate()
        stem = f'{len(events)+1:03d}-{name}'
        item = {'name': name, 'argv': argv, 'cwd': str(merged), 'start': start, 'end': stamp(),
                'elapsed_seconds': time.monotonic()-clock, 'rc': p.returncode, 'timed_out': timed}
        for label, raw in [('stdout', stdout), ('stderr', stderr)]:
            masked = ns['mask_log'](raw); filename = stem+'.'+label
            (out / filename).write_bytes(masked); item[label] = filename
            item[label+'_sha256'] = sha(raw); item[label+'_masked_sha256'] = sha(masked)
        events.append(item); (out / 'commands.json').write_text(json.dumps(events, indent=2)+'\n')
        print(name, 'rc', p.returncode, flush=True)
        need(not timed and p.returncode in expected, name+' unexpected result')
        return stdout, p.returncode

    try:
        head, _ = command('head', ['git', 'rev-parse', 'HEAD']); need(head.decode().strip() == COORD, 'wrong coordinator')
        merge_head, _ = command('merge-head', ['git', 'rev-parse', 'MERGE_HEAD']); need(merge_head.decode().strip() == TIP, 'wrong lane')
        conflicts, _ = command('conflicts', ['git', 'ls-files', '-u', '-z'])
        paths = {x.split(b'\t')[1].decode() for x in conflicts.split(b'\0') if x}
        need(paths and paths <= {LOG, INDEX}, 'unexpected conflict scope')
        bodies = []
        for ref in [BASE, COORD, TIP]:
            b, _ = command('log-source', ['git', 'show', ref+':'+LOG]); bodies.append(b)

        def join(base, coordinator, lane):
            need(coordinator.startswith(base) and lane.startswith(base), 'pre-existing log bytes changed')
            suffix = coordinator[len(base):]; match = re.search(rb'^## ', suffix, re.M)
            need(match is not None and match.start() > 1, 'missing exact coordinator continuation')
            prefix = suffix[:match.start()-1]
            need(len(prefix) == 10620 and sha(prefix) == PREFIX_HASH, 'coordinator continuation identity differs')
            # This exact coordinator suffix continues the previous day's entry
            # before introducing its first timestamped heading. Preserve it in
            # place, then apply the already proved whole-entry parser unchanged.
            extended_base = base + prefix
            result, sequences = ns['merge_append_bytes'](extended_base, coordinator, extended_base+lane[len(base):])
            need(result.startswith(extended_base), 'coordinator continuation lost')
            return result, sequences

        combined, sequences = join(*bodies)
        controls = []
        mutations = [
            ('base-edited', (bodies[0]+b'x', bodies[1], bodies[2])),
            ('coordinator-prefix-edited', (bodies[0], bodies[1][:len(bodies[0])+1]+b'x'+bodies[1][len(bodies[0])+2:], bodies[2])),
            ('lane-old-bytes-edited', (bodies[0], bodies[1], b'x'+bodies[2][1:])),
            ('lane-no-final-newline', (bodies[0], bodies[1], bodies[2].rstrip(b'\n'))),
        ]
        for label, args in mutations:
            try: join(*args)
            except ValueError as e: controls.append({'name': label, 'rejected': True, 'reason': str(e)})
            else: raise ValueError('control accepted: '+label)
        (out / 'log-proof.json').write_text(json.dumps({'base': BASE, 'coordinator': COORD, 'lane': TIP,
            'coordinator_continuation_bytes': 10620, 'coordinator_continuation_sha256': PREFIX_HASH,
            'entry_sequences': sequences, 'merged_sha256': sha(combined), 'controls': controls,
            'scope': 'Exact coordinator continuation preserved plus unchanged whole-entry parser; no original gate relabelled.'}, indent=2)+'\n')
        (merged / LOG).write_bytes(combined)
        rendered, _ = command('index-render', ['tools/work-log-index'])
        command('index-write', ['tools/work-log-index', '--write'])
        need((merged / LOG).read_bytes() == combined and (merged / INDEX).read_bytes() == rendered, 'record bytes drift')
        other, _ = command('other-unstaged', ['git', 'diff', '--name-only', '-z', '--', '.', ':(exclude,literal)'+LOG, ':(exclude,literal)'+INDEX])
        need(not other, 'unexpected resolution edit')
        command('stage-log-index', ['git', 'add', '--', LOG, INDEX])
        protected, _ = command('protected-paths', ['git', 'diff', '--cached', '--name-only', COORD, '--', 'packages', 'projects', 'tools', 'scripts', '.claude', '.githooks', 'docs/reviews'])
        need(not protected, 'protected source/plan change in simulation')
        remaining, _ = command('unmerged', ['git', 'ls-files', '-u']); need(not remaining, 'unresolved conflict')
        _, whitespace = command('whitespace', ['git', 'diff', '--cached', '--check'], expected=(0, 2))
        for label, argv in [
            ('rules', ['tools/rules-check', '--quiet']), ('register', ['tools/register-check']),
            ('index', ['tools/work-log-index', '--check']), ('ceremony', ['tools/ceremony-check', '--gate']),
            ('hooks', ['.githooks/hooks-test']), ('forbidden', ['tools/forbidden-terms-check']),
            ('lint', ['tools/lint-audit-artifacts', AUDIT]),
            ('lint-issue', ['tools/lint-audit-artifacts', AUDIT, '--issue', '1411']),
            ('issue-check', ['tools/box-check', '--issue', '689']), ('audit-check', ['tools/box-check', '--issue', '1411']),
            ('bug-check', ['tools/box-check', '--issue', '1410'])]:
            b, _ = command(label, argv, timeout=1200 if label == 'forbidden' else 240)
            if label.startswith('lint'): need(b.decode().rstrip().endswith('PASS'), 'resolution PASS absent')
        result = {'state': 'PASS' if whitespace == 0 else 'REVIEW_WHITESPACE', 'time': stamp(),
                  'tip': TIP, 'coordinator': COORD, 'executor': previous['executor'],
                  'original_failure_preserved': True, 'lane_scan_reused': True,
                  'whitespace_rc': whitespace, 'commands': len(events), 'no_actual_integration': True}
    except Exception as e:
        result = {'state': 'FAIL', 'time': stamp(), 'error': str(e), 'commands': len(events)}
    (out / 'result.json').write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps(result), flush=True)
    return 0 if result['state'] == 'PASS' else 1

if __name__ == '__main__':
    sys.exit(main())

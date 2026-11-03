#!/usr/bin/env python3
"""New T43 disposable integration gates; accepted execution receipts are reconciled without replay."""
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
TIP = '8282cbcade3be32b437f7391be7e216d9a6b1074'
COORD = '749e5c7f2df2c8444b07f8521493d12b7f7a962b'
AUDIT = 'docs/audits/2026_11_02-epic-m6-patches-unshipped'
LOG = 'docs/work-logs/2026_11-work_logs/2026_11_02-work_log.md'
INDEX = 'docs/work-logs/INDEX.md'
sha = lambda b: hashlib.sha256(b).hexdigest()
stamp = lambda: datetime.datetime.now(datetime.timezone.utc).isoformat()

class Invalid(Exception):
    pass

def need(ok, reason):
    if not ok:
        raise Invalid(reason)

def main():
    root = Path(sys.argv[1]).absolute()
    need(root.parent == Path('/workspace/tmp/m6-coordinator') and not root.exists(), 'fresh owned output root required')
    root.mkdir()
    records = []
    executor = {'harness': 'Codex', 'model': 'GPT-6-Astra', 'effort': 'xhigh',
                'session': '01a19d11-f5c8-7bb0-80f3-49ad28732af2', 'pane': 'wN:p2',
                'identity_source': 'observed footer'}
    pure_path = REPO / 'docs/qa-logs/2026-11-02-m6-resume/t41-final-runner/t41_execution.py'
    pure = pure_path.read_bytes()
    need(sha(pure) == 'bab9838ac263f976ba73a73ab162614e132cf97a0dcfd8a781d1ed243e54bfd9', 'reviewed pure append/mask helper changed')
    nodes = [x for x in ast.parse(pure).body if isinstance(x, ast.FunctionDef) and x.name in ['merge_append_bytes', 'mask_log']]
    need(len(nodes) == 2, 'two pure helpers required')
    ns = dict(re=re, datetime=datetime, need=need, Invalid=Invalid, sha=sha)
    exec(compile(ast.Module(body=nodes, type_ignores=[]), '<reviewed pure helpers>', 'exec'), ns)
    import runpy
    resolver = Path(__file__).with_name('t43-merge-log.py')
    resolver_bytes = resolver.read_bytes()
    resolver_ns = runpy.run_path(str(resolver))
    original_merge = ns['merge_append_bytes']
    ns['merge_append_bytes'] = resolver_ns['merge_append_bytes']
    env = dict(os.environ, LC_ALL='C', GIT_CONFIG_GLOBAL='/dev/null', GIT_CONFIG_NOSYSTEM='1',
               GIT_OPTIONAL_LOCKS='0', GIT_TERMINAL_PROMPT='0', PYTHONDONTWRITEBYTECODE='1',
               GIT_AUTHOR_NAME='Codex M6 simulation', GIT_AUTHOR_EMAIL='noreply@openai.com',
               GIT_COMMITTER_NAME='Codex M6 simulation', GIT_COMMITTER_EMAIL='noreply@openai.com')
    env.update(GIT_CONFIG_COUNT='3', GIT_CONFIG_KEY_0='core.hooksPath', GIT_CONFIG_VALUE_0='/dev/null',
               GIT_CONFIG_KEY_1='commit.gpgsign', GIT_CONFIG_VALUE_1='false',
               GIT_CONFIG_KEY_2='core.fsmonitor', GIT_CONFIG_VALUE_2='false')
    env.pop('ES_SRC', None)
    (root / 'start.json').write_text(json.dumps({'start': stamp(), 'executor': executor,
        'lane': TIP, 'coordinator': COORD, 'scope': __doc__, 'affinity': sorted(os.sched_getaffinity(0)),
        'pure_helper_sha256': sha(pure), 'log_resolver_sha256': sha(resolver_bytes), 'runner_sha256': sha(Path(__file__).read_bytes())}, indent=2) + '\n')

    def command(label, argv, cwd=REPO, expected=(0,), timeout=180, data=None):
        start = stamp(); clock = time.monotonic(); timed_out = False
        p = subprocess.Popen(argv, cwd=cwd, env=env, stdin=subprocess.PIPE,
                             stdout=subprocess.PIPE, stderr=subprocess.PIPE, start_new_session=True)
        try:
            out, err = p.communicate(data, timeout=timeout)
        except subprocess.TimeoutExpired:
            timed_out = True; os.killpg(p.pid, signal.SIGKILL); out, err = p.communicate()
        stem = f'{len(records)+1:03d}-{label}'
        masked_out, masked_err = ns['mask_log'](out), ns['mask_log'](err)
        (root / (stem+'.stdout')).write_bytes(masked_out)
        (root / (stem+'.stderr')).write_bytes(masked_err)
        record = {'name': label, 'argv': argv, 'cwd': str(cwd), 'start': start, 'end': stamp(),
                  'elapsed_seconds': time.monotonic()-clock, 'rc': p.returncode, 'timeout': timed_out,
                  'stdout': stem+'.stdout', 'stderr': stem+'.stderr',
                  'stdout_sha256': sha(out), 'stderr_sha256': sha(err),
                  'stdout_masked_sha256': sha(masked_out), 'stderr_masked_sha256': sha(masked_err),
                  'stdin_sha256': sha(data) if data is not None else None}
        records.append(record)
        (root / 'commands.json').write_text(json.dumps(records, indent=2) + '\n')
        print(label, 'rc', p.returncode, flush=True)
        need(not timed_out and p.returncode in expected, label+' returned unexpected result')
        return out, p.returncode

    try:
        command('inode-capacity', ['df', '-i', '/workspace/tmp/m6-coordinator'])
        refs = {}
        for ref in ['refs/heads/next', 'refs/remotes/upstream/next']:
            b, _ = command('history-ref', ['git', 'rev-parse', '--verify', ref+'^{commit}'])
            refs[ref] = b.decode().strip()
        tools = ['tools/rules-check', 'tools/register-check', 'tools/work-log-index',
                 'tools/ceremony-check', 'tools/forbidden-terms-check', 'tools/lint-audit-artifacts',
                 'tools/box-check', '.githooks']
        left, _ = command('lane-tool-identities', ['git', 'ls-tree', '-rz', TIP, '--', *tools])
        right, _ = command('coordinator-tool-identities', ['git', 'ls-tree', '-rz', COORD, '--', *tools])
        need(left == right, 'final check tools differ; inspect before execution')
        lane = root / 'lane'; merged = root / 'integration'
        for path, ref in [(merged, COORD)]:
            command(path.name+'-clone', ['git', 'clone', '--quiet', '--shared', '--no-checkout', '--no-hardlinks', '--template=', str(REPO), str(path)])
            for name, value in refs.items(): command(path.name+'-history', ['git', 'update-ref', name, value], path)
            command(path.name+'-checkout', ['git', 'checkout', '--quiet', '--detach', ref], path)
            b, _ = command(path.name+'-head', ['git', 'rev-parse', 'HEAD'], path)
            need(b.decode().strip() == ref, 'wrong exact clone tip')
        # Exact final 159-path scan is already independently hash-reconciled.
        # Run a new whole merged-tree scan below, without replaying the producer.
        _, merge_rc = command('merge', ['git', 'merge', '--no-commit', '--no-ff', '--no-edit', TIP], merged, expected=(0, 1))
        raw, _ = command('unmerged', ['git', 'ls-files', '-u', '-z'], merged)
        conflicts = {x.split(b'\t', 1)[1].decode() for x in raw.split(b'\0') if x}
        need(conflicts <= {LOG, INDEX}, 'non-record integration conflict')
        if merge_rc:
            need(bool(conflicts), 'merge failed without expected record conflict')
            b, _ = command('merge-base', ['git', 'merge-base', '--all', COORD, TIP], merged)
            bases = b.decode().splitlines(); need(len(bases) == 1, 'multiple merge bases')
            bodies = []
            for ref in [bases[0], COORD, TIP]:
                b, _ = command('log-bytes', ['git', 'show', ref+':'+LOG], merged); bodies.append(b)
            original_failure = None
            try:
                original_merge(*bodies)
            except Exception as error:
                original_failure = str(error)
            need(original_failure == 'append entry heading/body/boundary invalid', 'unexpected old parser result')
            combined, sequences = ns['merge_append_bytes'](*bodies)
            controls = []
            bad = [
                ('old-bytes-edited', (bodies[0], bodies[1], b'x'+bodies[2][1:])),
                ('missing-terminal-newline', (bodies[0], bodies[1], bodies[2].rstrip(b'\n'))),
                ('legacy-body-edited', (bodies[0], bodies[1], bodies[2]+b'x\n')),
                ('invalid-seconds', (bodies[0], bodies[1].replace(b'22:12:19 UTC',b'22:12:99 UTC'), bodies[2])),
                ('unrecognized-legacy-heading', (bodies[0], bodies[1], bodies[2].replace(b'## 23:00 #690:',b'## 23:01 #690:'))),
                ('same-heading-conflict', (bodies[0], bodies[1], bodies[1].replace(b'T43 running;', b'T43 changed;'))),
            ]
            for label, args in bad:
                try: ns['merge_append_bytes'](*args)
                except ValueError as error: controls.append({'case':label,'refused':True,'reason':str(error)})
                else: raise Invalid('log control accepted '+label)
            (root/'log-preflight-and-controls.json').write_text(json.dumps({
                'original_failure':original_failure,'original_helper_unchanged':True,
                'resolver_sha256':sha(resolver_bytes),'controls':controls,
                'actual_positive_sha256':sha(combined),'scope':'time-only seconds accepted with range validation; one exact legacy T43 entry hash; all bytes/order preserved'},indent=2)+'\n')
            (merged / LOG).write_bytes(combined)
            rendered, _ = command('index-render', ['tools/work-log-index'], merged)
            command('index-write', ['tools/work-log-index', '--write'], merged)
            need((merged / LOG).read_bytes() == combined and (merged / INDEX).read_bytes() == rendered, 'log/index bytes changed unexpectedly')
            other, _ = command('other-unstaged', ['git', 'diff', '--name-only', '-z', '--', '.', ':(exclude,literal)'+LOG, ':(exclude,literal)'+INDEX], merged)
            need(not other, 'unexpected merge resolution change')
            command('stage-record-resolution', ['git', 'add', '--', LOG, INDEX], merged)
            (root / 'log-resolution.json').write_text(json.dumps({'base': bases[0], 'coordinator': COORD, 'lane': TIP,
                'entry_sequences': sequences, 'merged_sha256': sha(combined), 'index_sha256': sha(rendered)}, indent=2)+'\n')
        protected, _ = command('protected-paths', ['git','diff','--cached','--name-only',COORD,'--','packages','projects','tools','scripts','.claude','.githooks','docs/reviews','docs/decision-register.md'], merged)
        need(not protected, 'protected source/plan change in simulation')
        raw, _ = command('final-unmerged', ['git', 'ls-files', '-u'], merged); need(not raw, 'unresolved merge')
        _, whitespace = command('whitespace', ['git', 'diff', '--cached', '--check'], merged, expected=(0, 2))
        for label, argv in [
            ('rules', ['tools/rules-check', '--quiet']), ('register', ['tools/register-check']),
            ('index', ['tools/work-log-index', '--check']), ('ceremony', ['tools/ceremony-check', '--gate']),
            ('hooks', ['.githooks/hooks-test']), ('forbidden', ['tools/forbidden-terms-check']),
            ('lint', ['tools/lint-audit-artifacts', AUDIT]),
            ('lint-issue', ['tools/lint-audit-artifacts', AUDIT, '--issue', '1412']),
            ('issue-check', ['tools/box-check', '--issue', '690']),
            ('audit-check', ['tools/box-check', '--issue', '1412']),
            ('bug1408-check', ['tools/box-check', '--issue', '1408']),
            ('bug1410-check', ['tools/box-check', '--issue', '1410'])]:
            b, _ = command(label, argv, merged, timeout=1200 if label == 'forbidden' else 240)
            if label.startswith('lint'): need(b.decode().rstrip().endswith('PASS'), 'missing resolution PASS')
        result = {'state': 'PASS' if whitespace == 0 else 'REVIEW_WHITESPACE', 'end': stamp(),
                  'executor': executor, 'lane': TIP, 'coordinator': COORD, 'commands': len(records),
                  'whitespace_rc': whitespace, 'integration_gates_passed': True,
                  'no_actual_integration': True, 'accepted_producers_replayed': False}
    except Exception as e:
        result = {'state': 'FAIL', 'end': stamp(), 'error': str(e), 'executor': executor,
                  'lane': TIP, 'coordinator': COORD, 'commands': len(records)}
    (root / 'result.json').write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps(result), flush=True)
    return 0 if result['state'] == 'PASS' else 1

if __name__ == '__main__':
    sys.exit(main())

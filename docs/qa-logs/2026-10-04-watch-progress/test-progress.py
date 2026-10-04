#!/usr/bin/env python3
"""Exercise the real shared runner against mixed aggregate/package counters (#412)."""
import argparse
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

p = argparse.ArgumentParser()
p.add_argument('root', type=Path)
a = p.parse_args()
checks = []


def check(ok, name):
    checks.append(bool(ok))
    print(('PASS ' if ok else 'FAIL ') + name, flush=True)


with tempfile.TemporaryDirectory(prefix='watch-progress-412-') as temporary:
    base = Path(temporary)
    env = {'PATH': os.environ['PATH'], 'HOME': temporary, 'LC_ALL': 'C'}
    cases = [
        ('mixed', '\x1b[32m[603/642] [DONE] install sample:target\x1b[0m\n'
                  '[129/130] Compiling\n[130/130] Linking\n', '[603/642]', 0, False),
        ('package-only', '[130/130] Linking\n', 'none matched', 0, False),
        ('failed', '[604/642] [FAIL] build sample:target\n'
                   '[3/3] package cleanup\n', '[604/642]', 7, False),
        ('generic-qa', '[130/130] case\n', '[130/130]', 0, True),
        ('embedded-lookalike', '[603/642] [DONE] install sample:target\n'
                               'quoted [999/999] [DONE] build other\n'
                               '[700/700] [DONE] unrelated tool\n', '[603/642]', 0, False),
    ]
    for name, log, wanted, code, qa in cases:
        root = base / name
        (root / 'tools').mkdir(parents=True)
        for tool in ['watch-build', 'watch-job']:
            shutil.copy2(a.root / 'tools' / tool, root / 'tools' / tool)
        payload = root / 'emit.py'
        payload.write_text('import sys\nprint(' + repr(log) + ',end="",flush=True)\nsys.exit(' + str(code) + ')\n')
        command = [str(root / 'tools/watch-build'), '--interval', '1']
        if qa:
            (root / 'artifacts').mkdir()
            command += ['--activity-dir', str(root / 'artifacts')]
        command += ['--', sys.executable, str(payload)]
        result = subprocess.run(command, cwd=root, env=env, capture_output=True, text=True, timeout=15)
        runs = list((root / '.build-runs').glob('*/build.status'))
        status = runs[0].read_text() if len(runs) == 1 else ''
        check(result.returncode == code and 'outcome:     rc=' + str(code) in status,
              name + ': real command/result preserved')
        check('progress:    ' + wanted + '\n' in status, name + ': progress = ' + wanted)

    root = base / 'detached'
    root.mkdir()
    (root / 'log').write_text('[603/642] [DONE] build sample:target\n[130/130] Linking\n')
    (root / 'rc').write_text('0\n')
    result = subprocess.run([str((a.root / 'tools/watch-job').resolve()), '--log', str(root / 'log'),
                             '--rc', str(root / 'rc'), '--status', str(root / 'status'),
                             '--build-progress', '--detach'], env=env,
                            capture_output=True, text=True, timeout=10)
    status = (root / 'status').read_text() if (root / 'status').exists() else ''
    check(result.returncode == 0 and 'progress:    [603/642]\n' in status,
          'detached watcher preserves build-progress mode')

    (root / 'log').write_text('CASE 1\nCASE 2\n')
    result = subprocess.run([str((a.root / 'tools/watch-job').resolve()), '--log', str(root / 'log'),
                             '--rc', str(root / 'rc'), '--status', str(root / 'generic-status'),
                             '--pattern', 'CASE [0-9]+'], env=env,
                            capture_output=True, text=True, timeout=10)
    status = (root / 'generic-status').read_text()
    check(result.returncode == 0 and 'progress:    CASE 2\n' in status,
          'custom generic progress remains usable')

    (root / 'log').write_text('[603/642] [DONE] build sample:target\n[130/130] Linking\n')
    os.utime(root / 'log', (1, 1))
    (root / 'packages').mkdir()
    (root / 'packages/580.log').write_text('[7958/8578] Compiling WebKit\n')
    result = subprocess.run([str((a.root / 'tools/watch-job').resolve()), '--log', str(root / 'log'),
                             '--rc', str(root / 'rc'), '--status', str(root / 'activity-status'),
                             '--build-progress', '--activity-dir', str(root / 'packages')],
                            env=env, capture_output=True, text=True, timeout=10)
    status = (root / 'activity-status').read_text() if (root / 'activity-status').exists() else ''
    check(result.returncode == 0 and 'progress:    [603/642]\n' in status
          and 'activity_progress: [7958/8578]\n' in status,
          'structured overall and generic package counters remain separate')

print(f'{sum(checks)} PASS; {len(checks) - sum(checks)} FAIL', flush=True)
sys.exit(not all(checks))

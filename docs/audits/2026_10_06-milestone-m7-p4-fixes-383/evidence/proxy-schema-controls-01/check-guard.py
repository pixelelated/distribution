#!/usr/bin/env python3
"""CLI controls for #414; no build, network, guest or player data changes."""
import argparse
import contextlib
import importlib.machinery
import io
from pathlib import Path
import subprocess
import sys
import tempfile
from unittest import mock

ROOT = Path('/workspace/repos/rocknix.worktrees/conflict-resolution')
ap = argparse.ArgumentParser()
ap.add_argument('--tool', type=Path, default=ROOT/'tools/rc-preflight')
a = ap.parse_args()
rel = Path('projects/ROCKNIX/packages/network/raofflineproxy')
recipe = (ROOT/rel/'package.mk').read_text()
script = (ROOT/rel/'sources/raofflineproxy-ctl').read_text()
current = '879b158995d412af434301ebdae581f66b8b6d57'
old = '5866cd9ba784c13771a99c52dd6b6f2acc546842'
passed = failed = 0
with tempfile.TemporaryDirectory(prefix='proxy-schema-note-') as temp:
    tree = Path(temp)
    pkg = tree/rel
    (pkg/'sources').mkdir(parents=True)
    cases = [
        ('matching review', recipe, script, 0),
        ('stale review', recipe, script.replace(current, old), 1),
        ('missing review', recipe, script.replace('# package.mk pins', '# previous source'), 1),
        ('short review', recipe, script.replace(current, current[:10]), 1),
        ('duplicate review', recipe, script.replace('# package.mk pins', '# package.mk pins ('+current+', storage.py\n# package.mk pins'), 1),
        ('missing boundary', recipe, script.replace('\n. /etc/profile\n', '\n'), 1),
        ('claim only below header', recipe, script.replace('# package.mk pins ('+current+', storage.py\n', '')+'\n# package.mk pins ('+current+', storage.py\n', 1),
        ('missing recipe pin', recipe.replace('PKG_VERSION=', 'OLD_VERSION='), script, 1),
        ('short recipe pin', recipe.replace(current, current[:10]), script, 1),
        ('duplicate recipe pin', recipe+'\nPKG_VERSION="'+current+'"\n', script, 1),
        ('conflicting assignment', recipe+'\nPKG_VERSION="broken"\n', script, 1),
        ('missing script file', recipe, None, 2),
        ('missing recipe file', None, script, 2),
    ]
    for name, r, s, expected in cases:
        for path, data in ((pkg/'package.mk', r), (pkg/'sources/raofflineproxy-ctl', s)):
            if data is None:
                path.unlink(missing_ok=True)
            else:
                path.write_text(data)
        p = subprocess.run([str(a.tool.resolve()), '--only', 'proxy-schema', '--tree', str(tree)],
                           capture_output=True, text=True, timeout=10)
        verdict = ('PASS' if expected == 0 else 'FAIL' if expected == 1 else 'CANNOT')
        ok = p.returncode == expected and verdict in p.stdout and 'MAY BE CUT' not in p.stdout
        print(('PASS ' if ok else 'FAIL ')+name+' rc='+str(p.returncode))
        passed += ok
        failed += not ok
    # Exercise the ordinary (unscoped) dispatcher too. Unrelated network/RC
    # checks are doubles; only the schema-note guard and its verdict are real.
    module = importlib.machinery.SourceFileLoader('rc_preflight_fixture', str(a.tool)).load_module()
    (tree/'.git').mkdir()
    for name, text, expected in (('full dispatcher matching', script, 0),
                                 ('full dispatcher stale', script.replace(current, old), 1)):
        (pkg/'package.mk').write_text(recipe)
        (pkg/'sources/raofflineproxy-ctl').write_text(text)
        with contextlib.ExitStack() as stack:
            for func in ('check_packages', 'check_base', 'check_bugs', 'check_already_written', 'check_tool'):
                stack.enter_context(mock.patch.object(module, func))
            stack.enter_context(mock.patch.object(module, 'decided_ids', return_value=set()))
            stack.enter_context(mock.patch.object(module, 'acceptances', return_value=({}, [])))
            stack.enter_context(mock.patch.object(module, 'run', return_value=(0, '', '')))
            stack.enter_context(mock.patch.object(module, 'ES_PKG', str(rel/'package.mk')))
            stack.enter_context(mock.patch.object(sys, 'argv', [str(a.tool), '--tree', str(tree), '--es', str(tree), '--allow-unchecked', 'device-facts']))
            stack.enter_context(contextlib.redirect_stdout(io.StringIO()))
            actual = module.main()
        ok = actual == expected
        print(('PASS ' if ok else 'FAIL ')+name+' rc='+str(actual))
        passed += ok
        failed += not ok
print(f'{passed} PASS / {failed} FAIL')
raise SystemExit(bool(failed))

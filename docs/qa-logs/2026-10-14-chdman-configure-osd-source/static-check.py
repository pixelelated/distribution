#!/usr/bin/env python3
"""Static bytes/AST/patch/options/bash syntax only. Never import a runner."""
import ast
import difflib
import gzip
import hashlib
import json
from pathlib import Path
import re
import shlex
import subprocess
import sys

HERE = Path(__file__).resolve().parent
BASIS = Path('/workspace/repos/rocknix.worktrees/m7-player-setup/docs/qa-logs/2026-10-14-chdman-export-alias-source')


def sha(data):
    return hashlib.sha256(data).hexdigest()


def read(name):
    return json.loads((HERE / name).read_text())


def functions(path):
    return {n.name: ast.dump(n, include_attributes=False)
            for n in ast.parse(path.read_bytes()).body if isinstance(n, ast.FunctionDef)}


def main():
    assert sys.flags.optimize == 0, 'assertions disabled'
    binding = read('bindings.json')
    assert sha((BASIS/'SHA256SUMS').read_bytes()) == binding['source_basis_manifest_sha256']
    for line in (BASIS/'SHA256SUMS').read_text().splitlines():
        digest, name = line.split('  ', 1)
        assert sha((BASIS/name).read_bytes()) == digest, name
    trees = {p.name: ast.parse(p.read_bytes(), filename=str(p), feature_version=(3, 10))
             for p in HERE.glob('*.py')}
    exact = ['common.py', 'docker_owner.py', 'watchdog.py', 'run-stage.py', 'inner.py']
    for name in exact:
        assert (HERE/name).read_bytes() == (BASIS/name).read_bytes(), name
    old_f = functions(BASIS/'mame.py')
    new_f = functions(HERE/'mame.py')
    assert old_f.keys() == new_f.keys()
    assert all(old_f[n] == new_f[n] for n in old_f if n != 'inspect_source')
    assert (HERE/'plan.py').read_text() == (BASIS/'plan.py').read_text().replace(
        'wrong sealed1c0e93 plan', 'wrong prospective OSD-corrected plan')
    for name, row in read('changes.json').items():
        before, after = (BASIS/name).read_bytes(), (HERE/name).read_bytes()
        assert sha(before) == row['before_sha256'] and sha(after) == row['after_sha256'], name
        assert row['diff'] == ''.join(difflib.unified_diff(
            before.decode().splitlines(True), after.decode().splitlines(True),
            fromfile='26a527/'+name, tofile='owner03/'+name, n=3)), name
    inputs = read('plan/input-bindings.json')
    prior = json.loads((BASIS/'plan/input-bindings.json').read_text())
    delta = json.loads(json.dumps(inputs))
    osd = delta['chdman'].pop('private_osd_adjustment')
    assert delta == prior, 'unexpected source/feature/toolchain input change'
    assert inputs['chdman']['commit'] == '24cffe763621b164fc10be2ae3660f140be25182'
    members = read('evidence/source-members.json')
    source = {}
    for name, row in members['members'].items():
        raw = (HERE/row['packet_path']).read_bytes()
        assert sha(raw) == row['compressed_sha256'], name
        data = gzip.decompress(raw)
        assert sha(data) == row['sha256'] and len(data) == row['bytes'], name
        if name in inputs['chdman']['source_files']:
            expected = inputs['chdman']['source_files'][name]
            assert len(data) == expected['bytes'] and sha(data) == expected['sha256'], name
        source[name] = data.decode()
    assert members['archive_sha256'] == inputs['chdman']['archive']['sha256']
    before = source['scripts/toolchain.lua']
    assert sha(before.encode()) == osd['before_sha256']
    first = '\t\t-- libretro only supports the retro OSD\n'
    last = '\t\t_OPTIONS["NO_USE_MIDI"] = "1"\n'
    assert before.count(first) == before.count(last) == 1
    after = before.replace(first, '\tif _OPTIONS["osd"] == "retro" then\n'+first).replace(last, last+'\tend\n')
    assert sha(after.encode()) == osd['after_sha256']
    patch = (HERE/'plan'/osd['patch']).read_text()
    assert patch == ''.join(difflib.unified_diff(before.splitlines(True), after.splitlines(True),
        fromfile='a/scripts/toolchain.lua', tofile='b/scripts/toolchain.lua', n=0))
    # Exact hunk-position/source reconstruction, not external patch/Lua execution.
    assert patch == ('--- a/scripts/toolchain.lua\n+++ b/scripts/toolchain.lua\n'
        '@@ -643,0 +644 @@\n+\tif _OPTIONS["osd"] == "retro" then\n'
        '@@ -651,0 +653 @@\n+\tend\n')
    block = after.split('if _OPTIONS["osd"] == "retro" then\n', 1)[1].split('\tend\n', 1)[0]
    assert re.findall(r'_OPTIONS\["([^\"]+)"\]\s*=', block) == ['osd', 'NO_USE_BGFX', 'NO_USE_MIDI']
    assert 'trigger = "NO_USE_BGFX"' in source['scripts/src/osd/retro_modules.lua']
    assert 'trigger = "NO_USE_BGFX"' not in source['scripts/src/osd/modules.lua']
    old_stage = (BASIS/'plan/build-stage.sh').read_text()
    stage = (HERE/'plan/build-stage.sh').read_text()
    added = ('    # Require the separate exact scratch-only OSD selection correction.\n'
        '    [[ $(sha256sum "$mame/scripts/toolchain.lua" | cut -d \' \' -f 1) == '
        + osd['after_sha256'] + ' ]] || exit 64\n')
    assert stage.count(added) == 1 and stage.replace(added, '') == old_stage
    assert (HERE/'plan/chdman-shared-libstdcxx.patch').read_bytes() == (BASIS/'plan/chdman-shared-libstdcxx.patch').read_bytes()
    body = stage.split('  chdman-configure)\n', 1)[1].split('    ;;', 1)[0]
    args = shlex.split(body.split('    exec ', 1)[1].replace('\\\n', ' '))
    assignments = {a.split('=', 1)[0]: a.split('=', 1)[1] for a in args if '=' in a}
    review = read('option-review.json')
    assert assignments == {r['name']: r['value'] for r in review['unchanged_configure_make_assignments']}
    assert len(assignments) == 43
    observed = (HERE/'evidence/owner02/chdman-configure/logs/selected-stage.stdout').read_text()
    argv = shlex.split(next(s for s in observed.splitlines() if s.startswith('3rdparty/genie/bin/linux/genie ')))
    assert argv == review['observed_owner02_generator_argv'] and argv[-1] == 'gmake'
    assert len(argv[1:-1]) == 37
    assert [r['argv'] for r in review['all_observed_generator_options']] == argv[1:-1]
    for row in review['all_observed_generator_options']:
        name, _, value = row['argv'][2:].partition('=')
        dec = row['declaration']; data = source[dec['source']]
        line = data.splitlines()[dec['line']-1]
        assert re.search(r'trigger\s*=\s*[\'"]'+re.escape(name)+r'[\'"]', line), name
        if dec['allowed'] is not None:
            assert value in dec['allowed'], name
    for row in review['unchanged_configure_make_assignments']:
        for hit in row['makefile_uses']:
            assert source['makefile'].splitlines()[hit['line']-1] == hit['text']
    assert review['removed_make_or_genie_options'] == []
    for name, row in read('evidence/owner02-bindings.json').items():
        data = (HERE/name).read_bytes()
        assert len(data) == row['bytes'] and sha(data) == row['sha256'], name
    for kind in ('chdman-export', 'chdman-bootstrap'):
        result = read('evidence/owner02/'+kind+'/result.json')
        assert result['status'] == 'PASS'
        assert result['original_attach_exit'] == result['original_container_exit'] == result['watchdog_original_exit'] == 0
        assert read('evidence/owner02/'+kind+'/acceptance.json')['expected_rc'] == 0
    failure = read('evidence/owner02/chdman-configure/result.json')
    assert failure['status'] == 'FAIL' and failure['original_attach_exit'] == failure['original_container_exit'] == 1
    assert failure['cleanup']['status'] == 'PASS' and failure['watchdog_original_exit'] == 0
    assert not failure['cleanup']['survivors'] and not failure['cleanup']['remaining_cgroup_pids']
    assert read('evidence/owner02/chdman-configure/selected-stage.json')['original_exit'] == 2
    assert read('evidence/owner02/chdman-configure/submit/launcher-result.json')['runner_returncode'] == 1
    assert binding['family_seconds'] == 1800 and binding['compiler_jobs'] == 1
    assert binding['memory_bytes'] == 4*1024**3 and binding['cpus'] == 2 and binding['scratch_stop_bytes'] == 6*1024**3
    assert binding['sealed_plan_path'] == 'docs/qa-logs/2026-10-14-chdman-configure-osd-source/plan'
    assert sha((HERE/'plan/SHA256SUMS').read_bytes()) == binding['sealed_plan_manifest_sha256']
    for line in (HERE/'plan/SHA256SUMS').read_text().splitlines():
        digest, name = line.split('  ', 1)
        assert sha((HERE/'plan'/name).read_bytes()) == digest, name
    shell = subprocess.run(['bash', '-n', str(HERE/'plan/build-stage.sh')], capture_output=True, timeout=10)
    assert shell.returncode == 0, shell.stderr.decode()
    print(json.dumps({'status': 'STATIC_ONLY_PASS', 'python': sys.version, 'python_AST': sorted(trees),
        'unchanged_runner_files': exact, 'unchanged_make_assignments': 43,
        'observed_generator_options_source_checked': 37, 'source_members': len(source),
        'OSD_patch_only_two_added_lines': True, 'prior_failure_original_channels_preserved': True,
        'basis_manifest_sha256': binding['source_basis_manifest_sha256'],
        'plan_manifest_sha256': binding['sealed_plan_manifest_sha256'], 'bash_n_exit': shell.returncode,
        'runner_imported': False, 'archive_exported': False, 'Lua_GENie_compiler_container_VM_target_execution': False,
        'runtime': 'UNRUN; no generated-file/compile/format acceptance inferred'}, indent=2))


if __name__ == '__main__':
    main()

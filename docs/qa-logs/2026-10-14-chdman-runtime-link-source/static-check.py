#!/usr/bin/env python3
"""AST, exact bytes, retained receipts and bash syntax only; no runner imports."""
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
BASIS = HERE.parent / '2026-10-14-chdman-configure-osd-source'


def sha(data):
    return hashlib.sha256(data).hexdigest()


def read(name):
    return json.loads((HERE/name).read_text())


def original(name):
    return gzip.decompress((HERE/'evidence/owner03'/name).read_bytes())


def main():
    assert sys.flags.optimize == 0, 'assertions disabled'
    binding = read('bindings.json')
    assert sha((BASIS/'SHA256SUMS').read_bytes()) == binding['source_basis_manifest_sha256']
    for line in (BASIS/'SHA256SUMS').read_text().splitlines():
        digest, name = line.split('  ', 1)
        assert sha((BASIS/name).read_bytes()) == digest, name
    trees = {p.name: ast.parse(p.read_bytes(), filename=str(p), feature_version=(3, 10))
             for p in HERE.glob('*.py')}
    unchanged = ['common.py', 'docker_owner.py', 'watchdog.py', 'export.py',
                 'inner.py', 'plan.py', 'run-stage.py']
    for name in unchanged:
        assert (HERE/name).read_bytes() == (BASIS/name).read_bytes(), name
    old_mame = (BASIS/'mame.py').read_text()
    expected = old_mame.replace(
        "require('-static-libstdc++' not in block and '-flto' not in block,'forbidden static C++/LTO policy')",
        "require('-static-libstdc++' not in block and '-static-libgcc' not in block and '-flto' not in block,\n"
        "                'forbidden static C++/GCC or LTO policy')").replace(
        "require('-static-libgcc' in assignment(block,'ALL_LDFLAGS'),'static libgcc disappeared')",
        "require(assignment(block,'ALL_LDFLAGS').split().count('-shared-libgcc')==1,\n"
        "                    'explicit shared libgcc policy absent/ambiguous')")
    assert expected != old_mame and (HERE/'mame.py').read_text() == expected
    inputs = read('plan/input-bindings.json')
    prior = json.loads((BASIS/'plan/input-bindings.json').read_text())
    spec = inputs['chdman']['private_source_adjustment']
    assert spec['before_sha256'] == prior['chdman']['private_source_adjustment']['before_sha256']
    pristine = gzip.decompress((HERE/'evidence/source/scripts/genie.lua.gz').read_bytes())
    assert sha(pristine) == spec['before_sha256']
    assert pristine.count(b'"-static-libgcc -static-libstdc++"') == 1
    revised = pristine.replace(b'"-static-libgcc -static-libstdc++"', b'"-shared-libgcc"')
    assert sha(revised) == spec['after_sha256']
    patch = (HERE/'plan'/spec['patch']).read_text()
    assert patch == ''.join(difflib.unified_diff(pristine.decode().splitlines(True),
        revised.decode().splitlines(True), fromfile='a/scripts/genie.lua', tofile='b/scripts/genie.lua', n=0))
    assert patch == ('--- a/scripts/genie.lua\n+++ b/scripts/genie.lua\n@@ -1005 +1005 @@\n'
        '-\t\t\t"-static-libgcc -static-libstdc++"\n+\t\t\t"-shared-libgcc"\n')
    assert not (HERE/'plan/chdman-shared-libstdcxx.patch').exists(), 'do not stack replacement patches'
    assert (HERE/'plan/chdman-preserve-selected-osd.patch').read_bytes() == (BASIS/'plan/chdman-preserve-selected-osd.patch').read_bytes()
    assert (HERE/'plan/build-stage.sh').read_text() == (BASIS/'plan/build-stage.sh').read_text().replace(
        prior['chdman']['private_source_adjustment']['after_sha256'], spec['after_sha256'])
    delta = json.loads(json.dumps(inputs))
    delta['chdman']['private_source_adjustment'] = prior['chdman']['private_source_adjustment']
    runtime = delta['toolchain']['chdman_cxx_runtime']
    for label, tail in [('libgcc_shared_link', 'libgcc_s.so'), ('libgcc_shared_runtime', 'libgcc_s.so.1')]:
        row = runtime.pop(label)
        assert row['path'].endswith('/x86_64-rocknix-linux-gnu/lib/'+tail)
        assert row['bytes'] == 178640
        assert row['sha256'] == '421566e56262d76771c56578d1e87c80a2b33e702e4c21c29a4cf1e456fbe174'
        path = Path(row['path'])
        assert path.is_file() and not path.is_symlink() and sha(path.read_bytes()) == row['sha256']
    runtime.pop('prospective_linkage')
    assert delta == prior, 'unexpected pin/feature/input change'
    for name, row in read('changes.json').items():
        before = (BASIS/row['basis_path']).read_bytes()
        after = (HERE/name).read_bytes()
        assert sha(before) == row['before_sha256'] and sha(after) == row['after_sha256'], name
        assert row['diff'] == ''.join(difflib.unified_diff(before.decode().splitlines(True),
            after.decode().splitlines(True), fromfile='2608923/'+row['basis_path'],
            tofile='owner04/'+name, n=3)), name
    for name, row in read('evidence/owner03-bindings.json').items():
        if name.startswith('retired-input/'):
            assert row['retention'].startswith('Hash only;')
            continue
        raw = (HERE/name).read_bytes()
        assert sha(raw) == row['compressed_sha256'], name
        data = gzip.decompress(raw)
        assert sha(data) == row['sha256'] and len(data) == row['bytes'], name
    stages = ('chdman-export', 'chdman-bootstrap', 'chdman-configure', 'chdman-build')
    for stage in stages:
        failed = stage == 'chdman-build'
        receipt = json.loads(original(stage+'/result.json.gz'))
        inner = json.loads(original(stage+'/container-result.json.gz'))
        assert receipt['status'] == ('FAIL' if failed else 'PASS')
        assert receipt['original_attach_exit'] == receipt['original_container_exit'] == int(failed)
        assert receipt['watchdog_original_exit'] == 0
        assert receipt['cleanup']['status'] == 'PASS' and not receipt['cleanup']['forced_stop']
        assert not receipt['cleanup']['survivors'] and not receipt['cleanup']['remaining_cgroup_pids']
        assert json.loads(original(stage+'/submit/launcher-result.json.gz'))['runner_returncode'] == int(failed)
        assert inner['children'][0]['original_exit'] == (2 if failed else 0)
        assert inner['source_after']['converter_pristine'] is True
        assert inner['source_after']['files'] == 31411
    stdout = original('chdman-build/logs/selected-stage.stdout.gz').decode()
    lines = [line for line in stdout.splitlines() if 'g++ -o ../../../../../chdman ' in line]
    assert len(lines) == 1 and lines[0]+'\n' == (HERE/'evidence/original-link-argv.txt').read_text()
    argv = shlex.split(lines[0])
    assert argv.count('-static-libgcc') == 1 and '-static-libstdc++' not in argv and '-shared-libgcc' not in argv
    stderr = original('chdman-build/logs/selected-stage.stderr.gz').decode()
    assert 'warning: libgcc_s.so.1, needed by ' in stderr and ', not found ' in stderr
    unresolved = re.findall(r"undefined reference to `([^']+)'", stderr)
    assert len(unresolved) == 17 and '_Unwind_GetIPInfo@GCC_4.2.0' in unresolved
    # Preserve the accepted selected graph/source identity without invoking its checker.
    configured = json.loads(original('chdman-configure/configuration.json.gz'))
    before_build = json.loads(original('chdman-build/configuration-before.json.gz'))
    assert configured == before_build and configured['status'] == 'PASS'
    selected = {'chdman', 'utils', 'expat', '7z', 'ocore_sdl', 'zlib', 'zstd', 'flac', 'utf8proc'}
    assert set(configured['selected']) == set(configured['dependencies']) == selected
    for name, row in configured['selected'].items():
        data = gzip.decompress((HERE/'evidence/generated-owner03/build/projects/sdl/mame/gmake-linux'/(name+'.make.gz')).read_bytes())
        assert sha(data) == row['sha256'], name
        block = re.findall(r'^ifeq \(\$\(config\),release64\)\n(.*?)^endif$', data.decode(), re.M|re.S)
        assert block == [row['release64']], name
    for name, row in read('evidence/gcc15-source.json')['members'].items():
        raw = (HERE/row['packet_path']).read_bytes(); data = gzip.decompress(raw)
        assert sha(raw) == row['compressed_sha256'] and sha(data) == row['sha256'] and len(data) == row['bytes'], name
    source = gzip.decompress((HERE/'evidence/gcc15-source/gcc/cp/g++spec.cc.gz').read_bytes()).decode()
    assert 'case OPT_static_libgcc:\n\t  shared_libgcc = 0;' in source
    assert 'if (shared_libgcc && !static_link)\n    generate_option (OPT_shared_libgcc' in source
    assert binding['family_seconds'] == 1800 and binding['compiler_jobs'] == 1
    assert binding['memory_bytes'] == 4*1024**3 and binding['cpus'] == 2 and binding['scratch_stop_bytes'] == 6*1024**3
    assert binding['sealed_plan_path'] == 'docs/qa-logs/2026-10-14-chdman-runtime-link-source/plan'
    assert sha((HERE/'plan/SHA256SUMS').read_bytes()) == binding['sealed_plan_manifest_sha256']
    for line in (HERE/'plan/SHA256SUMS').read_text().splitlines():
        digest, name = line.split('  ', 1)
        assert sha((HERE/'plan'/name).read_bytes()) == digest, name
    shell = subprocess.run(['bash', '-n', str(HERE/'plan/build-stage.sh')], capture_output=True, timeout=10)
    assert shell.returncode == 0, shell.stderr.decode()
    print(json.dumps({'status': 'STATIC_ONLY_PASS', 'python': sys.version, 'Python_AST': sorted(trees),
        'unchanged_runner_files': unchanged, 'mame_only_two_linkage_assertions_changed': True,
        'all_make_configure_arguments_unchanged': True, 'prior_selected_graph_files_checked': 9,
        'original_unresolved_symbols': unresolved, 'prior_original_exits_preserved': True,
        'source_pin': inputs['chdman']['commit'], 'revised_genie_sha256': spec['after_sha256'],
        'explicit_linkage_delta': '-static-libgcc -> -shared-libgcc; shared libstdc++ retained',
        'bash_n_original_exit': shell.returncode, 'runner_imported': False,
        'export_GENie_compiler_linker_ELF_tools_container_VM_target_execution': False,
        'source_pins_verified': False, 'runtime': 'UNRUN'}, indent=2))


if __name__ == '__main__':
    main()

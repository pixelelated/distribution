#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-2.0
"""One admitted GTK4 input compile only; preserve compiler/Docker/owner results."""
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import re
import signal
import subprocess
import sys
import time

sys.dont_write_bytecode = True


def sha(path):
    with path.open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def record(path, value):
    with path.open('x') as stream:
        json.dump(value, stream, indent=2)
        stream.write('\n')


def read_command(arguments):
    return subprocess.check_output(arguments, text=True, timeout=10).strip()


def group_members(group):
    result = []
    for path in Path('/proc').glob('[0-9]*/stat'):
        try:
            fields = path.read_text().rsplit(')', 1)[1].split()
            if int(fields[2]) == group and fields[0] != 'Z':
                result.append(int(path.parent.name))
        except FileNotFoundError:
            continue
    return result


def output_bytes(root):
    total = 0
    for path in root.rglob('*'):
        try:
            if path.is_file():
                total += path.stat().st_size
        except FileNotFoundError:
            pass  # GCC may retire a temporary file between listing and stat.
    return total


def main():
    total_started = time.monotonic()
    owner = Path(__file__).resolve().parent
    config = json.loads((owner / 'inputs.json').read_text())
    tree = Path(config['checkout'])
    assert Path.cwd().resolve() == tree and os.getuid() != 0
    assert os.readlink('/proc/self/ns/pid') == config['host_pid_namespace']
    assert os.sched_getaffinity(0) == {4}, 'owner must be pinned to CPU4'
    active = tree / os.environ['RASTERATOPS_BUILD_RUN']
    admission = json.loads((active / 'admission.json').read_text())
    assert admission['source']['head'] == config['commit']
    assert admission['submission_owner'] == str(owner / 'submit')
    assert admission['checkout'] == str(tree) and admission['container_checkout'] == config['canonical_checkout']
    assert admission['required_bytes'] >= config['limits']['scratch_budget_bytes']
    for relative, expected in config['helper_sha256'].items():
        assert sha(owner / relative) == expected
    for path, expected in config['external_sha256'].items():
        assert sha(Path(path)) == expected
    sys.path.insert(0, str(owner))
    from qualification import verify as verify_qualification
    qualified = verify_qualification(owner / 'qualification.json')
    assert sha(owner / 'qualification.json') == config['qualification_sha256']
    def source_state():
        return (read_command(['git', 'rev-parse', 'HEAD']),
                read_command(['git', 'status', '--porcelain', '--untracked-files=no']))
    assert source_state() == (config['commit'], '')
    image_id = read_command(['docker', 'image', 'inspect', '--format', '{{.Id}}', config['image']])
    (owner / 'run.path').write_text(str(active) + '\n')
    record(owner / 'owner-start.json', {'pid': os.getpid(), 'start_ticks': Path('/proc/self/stat').read_text().rsplit(')', 1)[1].split()[19],
        'pid_namespace': os.readlink('/proc/self/ns/pid'), 'source_commit': config['commit'],
        'builder_image_id': image_id, 'utc_epoch': time.time(), 'inputs_sha256': sha(owner / 'inputs.json')})
    spec = importlib.util.spec_from_file_location('host_resources', owner / 'host-resources.py')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    resources = module.Resources(owner, dict(config['host_observer'],
        maximum_incremental_allocated_bytes=admission['required_bytes']), [owner])
    signalled = []
    for number in [signal.SIGTERM, signal.SIGINT, signal.SIGHUP]:
        signal.signal(number, lambda received, _frame: signalled.append(received))
    stage = owner / 'stages/compile'
    name = config['owner_label']
    container_id = None
    process = None
    launched = False
    observed = acknowledged = False
    result = {'status': 'FAIL', 'original_docker_rc': None, 'cleanup': [], 'signals': signalled}
    started = total_started

    def inspect(identifier):
        command = subprocess.run(['docker', 'inspect', identifier], capture_output=True, text=True, timeout=5)
        if command.returncode:
            if 'no such object' in command.stderr.casefold() or 'no such container' in command.stderr.casefold():
                return None
            raise RuntimeError('container inspection failed')
        return json.loads(command.stdout)[0]

    def identity(data):
        assert data['Config']['Labels'].get('pixelelated.build.owner') == name
        assert data['Config']['Labels'].get('pixelelated.build.stage') == 'compile'
        assert data['Config']['Image'] == config['image'] and data['Image'] == image_id

    def retire_container():
        if not launched:
            return
        data = inspect(container_id or name)
        if data is None:
            return
        identity(data)
        identifier = data['Id']
        if data['State']['Running']:
            command = subprocess.run(['docker', 'stop', '--time', '5', identifier],
                stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=10)
            result['cleanup'].append({'container_id': identifier, 'stop_rc': command.returncode})
        deadline = time.monotonic() + 10
        while inspect(identifier) is not None and time.monotonic() < deadline:
            time.sleep(.2)
        assert inspect(identifier) is None, 'owned container did not retire'

    try:
        assert inspect(name) is None, 'fresh owner container name already exists'
        resources.start()
        while not resources.ready.wait(.1):
            assert not signalled and time.monotonic() - started < config['limits']['producer_seconds']
        assert not resources.failed.is_set(), 'host observer failed before launch'
        arguments = ['docker', 'run', '--rm', '--pull=never', '--network=none', '--read-only',
            '--cpus=1', '--cpuset-cpus=4', '--memory=2g', '--memory-swap=2g', '--pids-limit=128',
            '--ulimit', 'fsize=536870912:536870912', '--workdir', config['canonical_checkout'],
            '--cap-drop=ALL', '--security-opt=no-new-privileges', '--user', str(os.getuid()) + ':' + str(os.getgid()),
            '--tmpfs', '/tmp:rw,nosuid,size=128m', '--name', name, '--cidfile', str(stage / 'container.cid'),
            '--label', 'pixelelated.build.owner=' + name, '--label', 'pixelelated.build.stage=compile',
            '-e', 'TMPDIR=/tmp', '-e', 'HOME=/tmp', '-e', 'LC_ALL=C', '-e', 'RASTERATOPS_BUILD_RUN=' + os.environ['RASTERATOPS_BUILD_RUN'],
        ]
        for mount in config['mounts']:
            arguments += ['-v', mount['Source'] + ':' + mount['Destination'] + (':rw' if mount['RW'] else ':ro')]
        arguments += [config['image'], 'python3', '-I', '/inputs/inner-build.py', '--stage', 'compile',
            '--cpus', '1', '--memory-bytes', '2147483648', '--', 'python3', '-I', '-B',
            config['source_packet'] + '/compile-input.py', '--execute', '--output-dir', str(owner / 'out/input')]
        # Pass no host environment variables into the container except the four
        # fixed values above. Docker CLI itself keeps its standard host socket environment.
        with (owner / 'compiler.log').open('xb') as log:
            process = subprocess.Popen(arguments, stdout=log, stderr=subprocess.STDOUT, start_new_session=True)
            launched = True
            record(stage / 'host-command.json', {'pid': process.pid, 'process_group': process.pid,
                'cpu_ids': [4], 'memory_bytes': 2147483648, 'producer_seconds': 90, 'cleanup_seconds': 30, 'total_seconds': 120})
            while process.poll() is None:
                if not observed:
                    data = inspect(name)
                    if data is not None and data['State']['Running']:
                        identity(data)
                        container_id = data['Id']
                        host = data['HostConfig']
                        assert host['Memory'] == host['MemorySwap'] == 2147483648
                        assert host['NanoCpus'] == 1000000000 and host['CpusetCpus'] == '4'
                        assert host['PidsLimit'] == 128 and host['NetworkMode'] == 'none' and host['ReadonlyRootfs']
                        assert data['Config']['User'] == str(os.getuid()) + ':' + str(os.getgid())
                        mounts = [{key: item[key] for key in ['Source', 'Destination', 'RW']} for item in data['Mounts'] if item['Type'] == 'bind']
                        expected = config['mounts']
                        assert data['Config']['WorkingDir'] == config['canonical_checkout']
                        assert any(row['Name']=='fsize' and row['Soft']==row['Hard']==536870912 for row in host['Ulimits'])
                        assert sorted(mounts, key=lambda item: item['Destination']) == sorted(expected, key=lambda item: item['Destination'])
                        record(stage / 'container-observed.json', {'id': container_id, 'image_id': image_id,
                            'image_reference': config['image'], 'user': data['Config']['User'], 'mounts': mounts,
                            'cpuset': host['CpusetCpus'], 'nano_cpus': host['NanoCpus'],
                            'memory': host['Memory'], 'memory_swap': host['MemorySwap'],
                            'network': host['NetworkMode'], 'read_only_root': host['ReadonlyRootfs']})
                        observed = True
                if observed and not acknowledged and (stage / 'inner-ready.json').exists():
                    ready = json.loads((stage / 'inner-ready.json').read_text())
                    assert ready['stage'] == 'compile' and re.fullmatch('[0-9a-f]{32}', ready['nonce'])
                    temporary = stage / 'host-observed.tmp'
                    temporary.write_text(json.dumps({'stage': 'compile', 'nonce': ready['nonce'], 'container_id': container_id}) + '\n')
                    temporary.replace(stage / 'host-observed.json')
                    acknowledged = True
                assert not resources.failed.is_set(), 'host observer failed'
                assert not signalled, 'owner interrupted'
                assert time.monotonic() - started < config['limits']['producer_seconds'], 'producer deadline reached'
                assert (owner / 'compiler.log').stat().st_size <= 2 * 1024**2, 'compiler log bound reached'
                assert output_bytes(owner / 'out') <= 512 * 1024**2, 'output ceiling crossed'
                time.sleep(.2)
            result['original_docker_rc'] = process.wait()
        record(stage / 'host-result.json', {'original_docker_rc': result['original_docker_rc'],
            'container_observed': observed, 'observation_handshake': acknowledged})
        assert result['original_docker_rc'] == 0 and observed and acknowledged
        inner = json.loads((stage / 'inner-result.json').read_text())
        assert inner['original_command_rc'] == inner['wrapper_rc'] == 0
        result['original_compile_wrapper_rc'] = inner['original_command_rc']
        compiled = json.loads((owner / 'out/input/compile-result.json').read_text())
        result['original_compiler_rc'] = compiled['original_compiler_rc']
        assert compiled['status'] == 'PASS_COMPILE_ONLY' and compiled['original_compiler_rc'] == 0
        assert compiled['source_commit'] == config['commit'] and compiled['pkg_config_versions'] == ['4.24.1', '2.54.1']
        assert compiled['binary_sha256'] == sha(owner / 'out/input/input-spike')
        assert compiled['runtime_invoked'] is False
        result['qualification'] = {'allowed_compile_only': True, 'runtime_authorized': False,
                                   'rpath_findings': qualified['rpath_findings'],
                                   'runtime_inventory': qualified['runtime_inventory']}
        verify_qualification(owner / 'qualification.json')
        for path, expected in config['external_sha256'].items():
            assert sha(Path(path)) == expected
        assert source_state() == (config['commit'], '')
        for relative, expected in config['helper_sha256'].items():
            assert sha(owner / relative) == expected
        result['status'] = 'PASS'
    except BaseException as error:
        result['error_class'] = type(error).__name__
        # Only our fixed assertion messages are retained; no argv/env/headers.
        if isinstance(error, AssertionError):
            result['assertion'] = str(error)
    finally:
        cleanup_started = time.monotonic()
        try:
            retire_container()
            result['container_absent'] = True
        except BaseException as error:
            result['cleanup_error_class'] = type(error).__name__
            result['container_absent'] = False
            result['status'] = 'FAIL'
        if process is not None:
            if group_members(process.pid):
                os.killpg(process.pid, signal.SIGTERM)
            if process.poll() is None:
                try:
                    process.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    os.killpg(process.pid, signal.SIGKILL)
                    process.wait(timeout=5)
            cleanup_deadline = time.monotonic() + 5
            while group_members(process.pid) and time.monotonic() < cleanup_deadline:
                time.sleep(.1)
            if group_members(process.pid):
                os.killpg(process.pid, signal.SIGKILL)
                cleanup_deadline = time.monotonic() + 5
                while group_members(process.pid) and time.monotonic() < cleanup_deadline:
                    time.sleep(.1)
            result['original_docker_rc'] = process.returncode
            result['surviving_host_command_group'] = group_members(process.pid)
            if result['surviving_host_command_group']:
                result['status'] = 'FAIL'
            if not (stage / 'host-result.json').exists():
                record(stage / 'host-result.json', {'original_docker_rc': process.returncode,
                    'container_observed': observed, 'observation_handshake': acknowledged, 'interrupted_owner': True})
        if not result.get('container_absent') or result.get('surviving_host_command_group'):
            resources.fail(RuntimeError('producer remains; final scan refused'))
        try:
            if not resources.finish():
                result['status'] = 'FAIL'
        except BaseException as error:
            result['resource_error_class'] = type(error).__name__
            result['status'] = 'FAIL'
        result['seconds'] = time.monotonic() - started
        result['outputs'] = {str(path.relative_to(owner / 'out')): {'bytes': path.stat().st_size, 'sha256': sha(path)}
            for path in (owner / 'out').rglob('*') if path.is_file()}
        if 'input/input-spike' not in result['outputs'] or sum(row['bytes'] for row in result['outputs'].values()) > 512 * 1024**2:
            result['status'] = 'FAIL'
        result['total_deadline_seconds'] = 120
        result['seconds'] = time.monotonic() - started
        result['cleanup_seconds'] = time.monotonic() - cleanup_started
        result['deadline_overrun'] = result['seconds'] > 120 or result['cleanup_seconds'] > 30
        if result['deadline_overrun'] or signalled:
            result['status'] = 'FAIL'
        result['runtime_authorized'] = False
        record(owner / 'result.json', result)
    print(json.dumps(result), flush=True)
    return 0 if result['status'] == 'PASS' else 1


if __name__ == '__main__':
    try:
        status = main()
    except Exception as error:
        record(Path(__file__).resolve().parent / 'owner-setup-failure.json',
               {'error_class': type(error).__name__, 'utc_epoch': time.time()})
        status = 1
    raise SystemExit(status)

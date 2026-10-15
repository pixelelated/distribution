#!/usr/bin/env python3
"""One admitted owner: narrow Dolphin clean/rebuild, then image; source-only derivative."""
import hashlib
import importlib.machinery
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
    return hashlib.sha256(path.read_bytes()).hexdigest()


def record(path, value):
    with path.open('x') as stream:
        json.dump(value, stream, indent=2); stream.write('\n')


def run_read(command):
    return subprocess.check_output(command, text=True, timeout=15).strip()


def main():
    owner = Path(__file__).resolve().parent
    config = json.loads((owner / 'build-inputs.json').read_text())
    tree = Path(config['checkout'])
    assert Path.cwd().resolve() == tree and os.getuid() != 0
    assert os.readlink('/proc/self/ns/pid') == config['host_pid_namespace']
    active = tree / os.environ['RASTERATOPS_BUILD_RUN']
    admission = json.loads((active / 'admission.json').read_text())
    assert admission['source']['head'] == config['commit']
    assert admission['submission_owner'] == str(owner)
    assert admission['container_checkout'] == config['container_checkout']
    assert sha(Path(config['cache_ready'])) == config['cache_ready_sha256']
    cache = json.loads(Path(config['cache_ready']).read_text())
    assert cache['schema'] == 'pix572-atomic-cache-transfer-v1' and cache['status'] == 'PASS'
    assert cache['method'] == 'same-filesystem-rename'
    assert cache['before_identity'] == cache['after_identity']
    assert cache['source_head'] == 'fac608ff89940ce358ea9b8a95e9a08a6fe26568'
    assert cache['destination_head'] == config['commit']
    assert cache['product_sha256'] == config['product_sha256']
    assert not Path(cache['old']).exists()
    live = (tree / config['build_root']).stat()
    assert {'device': live.st_dev, 'inode': live.st_ino} == cache['after_identity']
    assert cache['new'] == str(tree / config['build_root'])
    for name, expected in config['helper_sha256'].items():
        assert sha(owner / name) == expected
    assert all(sha(tree / path) == digest for path, digest in config['product_sha256'].items())
    assert sha(tree / 'distributions/ROCKNIX/config/functions') == config['generated_doc_candidate_sha256']
    env = os.environ.copy()
    for key in ['DIRTY', 'CLEAN_SOURCES', 'CUSTOM_VERSION', 'CUSTOM_IMAGE_NAME', 'CUSTOM_GIT_HASH', 'BUILD_DIR', 'TARGET_DIR']:
        env.pop(key, None)
    env.update(PROJECT='ROCKNIX', DEVICE='GENERIC_X64', ARCH='x86_64', BUILD_QUALIFIER='dev',
               BUILD_TIMESTAMP=config['build_timestamp'], DOCKER_WORK_DIR=config['container_checkout'])
    source_state = lambda: (run_read(['git', 'rev-parse', 'HEAD']), run_read(['git', 'status', '--porcelain']))
    assert source_state() == (config['commit'], '')
    recipe = tree / 'projects/ROCKNIX/packages/ui/emulationstation/package.mk'
    assert re.fullmatch('[0-9a-f]{40}', config['es_commit'])
    assert sha(recipe) == config['es_recipe_sha256']
    assert re.findall(r'^\s*PKG_VERSION=(.*)$', recipe.read_text(), re.M) == ['"' + config['es_commit'] + '"']
    image_id = run_read(['docker', 'image', 'inspect', '--format', '{{.Id}}', config['builder_image']])
    preflight = subprocess.run(['tools/build-preflight'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    (owner / 'host-preflight.txt').write_text(preflight.stdout)
    assert preflight.returncode == 0
    (owner / 'run.path').write_text(str(active) + '\n')
    record(owner / 'owner-start.json', {'pid': os.getpid(), 'start_ticks': Path('/proc/self/stat').read_text().rsplit(')', 1)[1].split()[19],
        'pid_namespace': os.readlink('/proc/self/ns/pid'), 'source_commit': config['commit'],
        'builder_image_id': image_id, 'utc_epoch': time.time(), 'input_sha256': sha(owner / 'build-inputs.json')})
    loader = importlib.machinery.SourceFileLoader('owner_resources', str(owner / 'host-resources.py'))
    spec = importlib.util.spec_from_loader(loader.name, loader)
    module = importlib.util.module_from_spec(spec); loader.exec_module(module)
    resource_config = dict(config, maximum_incremental_allocated_bytes=admission['required_bytes'])
    resources = module.Resources(owner, resource_config, [tree / config['build_root'], Path('/workspace/cache/rocknix-sources'), tree / 'target', tree / 'release', owner])
    stopped = []
    def signal_handler(number, _frame):
        stopped.append(number)
    for number in [signal.SIGTERM, signal.SIGINT, signal.SIGHUP]:
        signal.signal(number, signal_handler)
    result = {'status': 'FAIL', 'stages': [], 'cleanup': [], 'signals': stopped}
    started = time.monotonic()
    process = None
    stage_id = None
    container_id = None
    container_name = None
    command_groups = []

    def live_group_members(group):
        found = []
        for path in Path('/proc').glob('[0-9]*/stat'):
            try:
                fields = path.read_text().rsplit(')', 1)[1].split()
                if int(fields[2]) == group and fields[0] != 'Z':
                    found.append(int(path.parent.name))
            except FileNotFoundError:
                continue
        return found

    def inspect(identifier):
        r = subprocess.run(['docker', 'inspect', identifier], capture_output=True, text=True, timeout=10)
        if r.returncode:
            if 'no such object' in r.stderr.casefold() or 'no such container' in r.stderr.casefold():
                return None
            raise RuntimeError('container inspection unavailable: ' + r.stderr.strip())
        return json.loads(r.stdout)[0]

    def assert_owner(d):
        assert d['Config']['Labels'].get('pixelelated.build.owner') == config['owner_label']
        assert d['Config']['Labels'].get('pixelelated.build.stage') == stage_id
        assert d['Config']['Image'] == config['builder_image'] and d['Image'] == image_id

    def stop_owned_container():
        d = inspect(container_id or container_name) if container_name else None
        if d is None:
            return
        assert_owner(d)
        identifier = d['Id']
        if d['State']['Running']:
            r = subprocess.run(['docker', 'stop', '--time', '20', identifier], capture_output=True, text=True, timeout=35)
            result['cleanup'].append({'container_id': identifier, 'stop_rc': r.returncode})
        deadline = time.monotonic() + 20
        while time.monotonic() < deadline:
            if inspect(identifier) is None:
                return
            time.sleep(.2)
        raise RuntimeError('owned container still exists after bounded cleanup')

    def wait_retired(identifier):
        deadline = time.monotonic() + 20
        while time.monotonic() < deadline:
            if inspect(identifier) is None:
                return
            time.sleep(.2)
        raise RuntimeError('canonical container did not retire')

    try:
        resources.start()
        while not resources.ready.wait(.2):
            assert not stopped and time.monotonic() - started < config['family_timeout_seconds']
        assert not resources.failed.is_set(), resources.errors
        stages = [('clean-dolphin-sa', 'package-clean', 'dolphin-sa', True),
                  ('build-dolphin-sa', 'package', 'dolphin-sa', True),
                  ('image', 'GENERIC_X64', None, False)]
        (owner / 'stages').mkdir()
        for stage_id, target, package, narrow in stages:
            assert source_state() == (config['commit'], '')
            assert not resources.failed.is_set() and not stopped
            for name, expected in config['helper_sha256'].items():
                assert sha(owner / name) == expected
            stage = owner / 'stages' / stage_id; stage.mkdir()
            if stage_id == 'image':
                (tree / config['build_root'] / '.stamps/image/build_target').unlink(missing_ok=True)
            cpus = config['cold_cpu_ids'] if narrow else config['image_cpu_ids']
            memory = config['cold_memory_bytes'] if narrow else config['image_memory_bytes']
            container_name = config['owner_label'] + '-' + stage_id
            container_id = None
            assert inspect(container_name) is None, 'container name already exists'
            cidfile = stage / 'container.cid'
            extra = ['-v', '/workspace/repos/rocknix/.git:/workspace/repos/rocknix/.git',
                     '-v', '/workspace/cache/rocknix-sources:' + config['container_checkout'] + '/sources',
                     '-v', str(owner) + ':/build-owner', '-e', 'TMPDIR=/tmp',
                     '--cpuset-cpus=' + ','.join(map(str, cpus)), '--memory=' + str(memory), '--memory-swap=' + str(memory),
                     '--pids-limit=' + str(config['container_pids_limit']),
                     '--name', container_name, '--cidfile', str(cidfile),
                     '--label', 'pixelelated.build.owner=' + config['owner_label'],
                     '--label', 'pixelelated.build.stage=' + stage_id]
            assert all(not re.search(r'\s|[\x00\n`$]', x) for x in extra)
            stage_env = dict(env, DOCKER_EXTRA_OPTS=' '.join(extra))
            if narrow:
                stage_env['CONCURRENCY_MAKE_LEVEL'] = '4'
            else:
                stage_env.pop('CONCURRENCY_MAKE_LEVEL', None)
            if package:
                stage_env['PACKAGE'] = package
            else:
                stage_env.pop('PACKAGE', None)
            inner = f'python3 -I /build-owner/inner-build.py --stage {stage_id} --cpus {len(cpus)} --memory-bytes {memory} -- make {target}'
            command = ['make', 'docker-' + target, 'COMMAND=' + inner]
            observed = False
            acknowledged = False
            process = subprocess.Popen(command, env=stage_env, start_new_session=True)
            command_groups.append(process.pid)
            record(stage / 'host-command.json', {'pid': process.pid, 'process_group': process.pid,
                   'stage': stage_id, 'target': target, 'package': package, 'memory_bytes': memory, 'cpu_ids': cpus})
            while process.poll() is None:
                if not observed:
                    d = inspect(container_name)
                    if d is not None and d['State']['Running']:
                        assert_owner(d)
                        container_id = d['Id']
                        assert d['Config']['WorkingDir'] == config['container_checkout']
                        assert d['Config']['User'] == f'{os.getuid()}:{os.getgid()}'
                        assert d['HostConfig']['Memory'] == memory and d['HostConfig']['MemorySwap'] == memory
                        mounts = [{k: m[k] for k in ['Source', 'Destination', 'RW']} for m in d['Mounts']]
                        assert any(m['Source'] == str(tree) and m['Destination'] == config['container_checkout'] for m in mounts)
                        assert any(m['Source'] == str(owner) and m['Destination'] == '/build-owner' and m['RW'] for m in mounts)
                        record(stage / 'container-observed.json', {'id': container_id, 'image_id': image_id,
                               'image_reference': d['Config']['Image'], 'user': d['Config']['User'],
                               'workdir': d['Config']['WorkingDir'], 'mounts': mounts})
                        observed = True
                ready = stage / 'inner-ready.json'
                if observed and not acknowledged and ready.exists():
                    handshake = json.loads(ready.read_text())
                    assert handshake['stage'] == stage_id and re.fullmatch('[0-9a-f]{32}', handshake['nonce'])
                    temporary = stage / 'host-observed.tmp'
                    temporary.write_text(json.dumps({'stage': stage_id, 'nonce': handshake['nonce'], 'container_id': container_id}) + '\n')
                    temporary.replace(stage / 'host-observed.json')
                    acknowledged = True
                assert not resources.failed.is_set(), resources.errors
                assert not stopped, 'owner interrupted'
                assert time.monotonic() - started < config['family_timeout_seconds'], 'family deadline reached'
                time.sleep(.2)
            rc = process.wait()
            entry = {'stage': stage_id, 'original_host_make_rc': rc, 'container_observed': observed, 'observation_handshake': acknowledged}
            record(stage / 'host-result.json', entry)
            result['stages'].append(entry)
            assert not live_group_members(process.pid), 'host make process group still has descendants'
            process = None
            assert rc == 0 and observed and acknowledged, 'original stage failed or container observation missing'
            inner_result = json.loads((stage / 'inner-result.json').read_text())
            assert inner_result['original_command_rc'] == inner_result['wrapper_rc'] == 0
            wait_retired(container_id)
            container_name = container_id = None
        assert source_state() == (config['commit'], '')
        assert all(not live_group_members(group) for group in command_groups)
        result['status'] = 'PASS'
    except BaseException as error:
        result['error'] = type(error).__name__ + ': ' + str(error)
    finally:
        producers_quiescent = True
        try:
            stop_owned_container()
        except BaseException as error:
            result['cleanup_error'] = type(error).__name__ + ': ' + str(error)
            result['status'] = 'FAIL'
            producers_quiescent = False
        if process is not None:
            if live_group_members(process.pid):
                os.killpg(process.pid, signal.SIGTERM)
            try:
                process.wait(timeout=10)
            except subprocess.TimeoutExpired:
                os.killpg(process.pid, signal.SIGKILL); process.wait(timeout=10)
            deadline = time.monotonic() + 10
            while live_group_members(process.pid) and time.monotonic() < deadline:
                time.sleep(.2)
            if live_group_members(process.pid):
                os.killpg(process.pid, signal.SIGKILL)
                deadline = time.monotonic() + 10
                while live_group_members(process.pid) and time.monotonic() < deadline:
                    time.sleep(.2)
            result['interrupted_host_make_rc'] = process.returncode
            result['interrupted_stage'] = stage_id
            if stage_id and not (owner / 'stages' / stage_id / 'host-result.json').exists():
                record(owner / 'stages' / stage_id / 'host-result.json', {
                    'stage': stage_id, 'original_host_make_rc': process.returncode,
                    'interrupted_owner': True, 'owner_error': result.get('error')})
        result['surviving_host_command_groups'] = {str(group): live_group_members(group) for group in command_groups}
        if any(result['surviving_host_command_groups'].values()):
            producers_quiescent = False
        if not producers_quiescent:
            resources.fail(RuntimeError('producers did not become quiescent; final disk scan refused'))
        try:
            resources_ok = resources.finish()
        except BaseException as error:
            resources_ok = False
            result['resource_finish_error'] = type(error).__name__ + ': ' + str(error)
        if not resources_ok:
            result['status'] = 'FAIL'
        result['elapsed_seconds'] = time.monotonic() - started
        record(owner / 'owner-result.json', result)
        (owner / 'inner.rc').write_text('0\n' if result['status'] == 'PASS' else '1\n')
    return 0 if result['status'] == 'PASS' else 1


if __name__ == '__main__':
    try:
        code = main()
    except Exception as error:
        owner = Path(__file__).resolve().parent
        record(owner / 'owner-setup-failure.json', {'error': type(error).__name__ + ': ' + str(error), 'utc_epoch': time.time()})
        code = 1
    raise SystemExit(code)

#!/usr/bin/env python3
"""Pure read-only packet hash, lossless-gzip and original-result verification."""
import argparse
import gzip
import hashlib
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parent

def require(condition, message):
    if not condition:
        raise ValueError(message)

def digest(data):
    return hashlib.sha256(data).hexdigest()

def inside(name):
    path = Path(name)
    require(not path.is_absolute() and '..' not in path.parts and name != '.', 'unsafe packet path')
    target = ROOT / path
    require(target.is_file() and not target.is_symlink(), 'missing or linked packet member')
    require(all(not parent.is_symlink() for parent in target.parents if parent != ROOT.parent), 'linked parent')
    return target

def main(check_originals):
    expected = {}
    for line in (ROOT / 'SHA256SUMS').read_text().splitlines():
        match = re.fullmatch(r'([0-9a-f]{64})  (.+)', line)
        require(match is not None, 'invalid manifest row')
        value, name = match.groups()
        require(name not in expected and name != 'SHA256SUMS', 'duplicate/self manifest member')
        expected[name] = value
    actual = {str(path.relative_to(ROOT)) for path in ROOT.rglob('*') if path.is_file()}
    require(actual == set(expected) | {'SHA256SUMS'}, 'manifest membership differs')
    for name, value in expected.items():
        require(digest(inside(name).read_bytes()) == value, 'stored member hash differs: ' + name)
    index = json.loads(inside('originals.json').read_text())
    require(len(index) == 45, 'original member count changed')
    raw = {}
    total = 0
    for row in index:
        name = row['stored']
        require(name not in raw and row['compression'] in (None, 'gzip'), 'invalid original index')
        stored = inside(name).read_bytes()
        if row['compression'] == 'gzip':
            with gzip.open(inside(name), 'rb') as stream:
                data = stream.read(row['raw_bytes'] + 1)
                require(stream.read(1) == b'', 'decompressed member exceeds bound')
        else:
            data = stored
        require(len(data) == row['raw_bytes'] and digest(data) == row['raw_sha256'], 'lossless original binding differs: ' + name)
        require(not data.startswith(b'\x7fELF') and b'\0' not in data, 'unexpected executable/binary member')
        if check_originals:
            original = Path(row['source'])
            require(original.is_absolute() and original.is_file(), 'original unavailable')
            require(original.read_bytes() == data, 'current original bytes differ: ' + name)
        raw[name] = data
        total += len(data)
    def obj(name):
        return json.loads(raw['originals/' + name])
    owner = obj('owner-result.json')
    resource = obj('resource-result.json')
    inner = obj('stage/inner-result.json')
    host = obj('stage/host-result.json')
    runner = obj('run/runner-result.json')
    launcher = obj('launcher-result.json')
    consumed = obj('run/admission-consumed.json')
    config = obj('build-inputs.json')
    census = obj('terminal-host-census.json')
    require(config['commit'] == '969354955741d6c0ca8ce816e1c59ad338b1605b', 'source commit differs')
    require(owner['status'] == resource['status'] == 'PASS', 'owner/resource result not PASS')
    require(not owner['cleanup'] and not owner['signals'] and not any(owner['surviving_host_command_groups'].values()), 'owner cleanup differs')
    require(not resource['errors'] and resource['all_threads_exited'], 'resource watcher did not finish cleanly')
    require(host['original_host_make_rc'] == inner['original_command_rc'] == inner['wrapper_rc'] == 0, 'original build result nonzero')
    require(host['container_observed'] and host['observation_handshake'], 'container observation missing')
    require(runner['command_rc'] == runner['monitor_rc'] == runner['runner_rc'] == launcher['runner_returncode'] == 0, 'outer result nonzero')
    for name in ['inner.rc', 'tool-wrapper.rc', 'run/build.rc']:
        require(raw['originals/' + name].strip() == b'0', 'original return file nonzero')
    require(abs(owner['elapsed_seconds'] - 2155.3168819870334) < 1e-9, 'elapsed measurement differs')
    require(inner['after']['memory_peak'] == 14397218816, 'build cgroup peak differs')
    require(inner['before']['memory_swap_max'] == inner['after']['memory_swap_max'] == '0', 'container swap contract differs')
    require(inner['visible_cpus'] == 4 and config['cold_cpu_ids'] == [0, 1, 2, 3], 'build CPU allocation differs')
    for key in ['oom', 'oom_kill', 'oom_group_kill']:
        require(inner['before']['memory_events'][key] == inner['after']['memory_events'][key] == 0, 'cgroup OOM event recorded')
    group = [json.loads(line) for line in raw['originals/stage/cgroup.jsonl.gz'].splitlines()]
    require(max(row['memory_peak'] for row in group) == 14397218816, 'cgroup samples disagree with peak')
    host_samples = [json.loads(line) for line in raw['originals/host-resources.jsonl.gz'].splitlines()]
    require(len(host_samples) == resource['host_sample_count'] and len({row['vmstat_pages']['oom_kill'] for row in host_samples}) == 1, 'host OOM/sample evidence differs')
    container = obj('stage/container-observed.json')
    require(inner['host_observation_handshake'] == obj('stage/host-observed.json'), 'inner/host nonce receipt differs')
    require(inner['host_observation_handshake']['container_id'] == container['id'], 'container identity differs')
    require(raw['originals/stage/container.cid'].decode().strip() == container['id'], 'container ID file differs')
    require(consumed['state'] == 'consumed' and consumed['source']['head'] == config['commit']
            and consumed['original_result'] == runner and consumed['outputs_held'] is True, 'original admission consumption differs')
    require(census['pid_namespace'] == consumed['pid_namespace'] == 4026531836, 'terminal census namespace differs')
    require(census['container_census'] == {'rc': 0, 'exact_absent': True, 'stderr_empty': True}, 'terminal container census differs')
    for name in ['owner-start.json', 'launcher-start.json']:
        require(census['pids'].get(str(obj(name)['pid'])) is False, 'terminal owner census missing')
    return {'status': 'PASS_PACKET', 'stored_members': len(expected), 'original_members': len(index),
            'lossless_original_bytes': total, 'original_sources_compared': check_originals,
            'original_result_channels_zero': True, 'engine_owner_seconds': owner['elapsed_seconds'],
            'compilation_cgroup_memory_peak_bytes': inner['after']['memory_peak'],
            'oom_events': 0, 'admission_consumed': True,
            'terminal_owner_container_absence_recorded': True,
            'target_runtime_or_memory_savings_qualified': False,
            'verifier_actions': 'file reads, hashing, gzip decompression and JSON checks only'}

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check-originals', action='store_true', help='also compare indexed original files when still available')
    options = parser.parse_args()
    try:
        print(json.dumps(main(options.check_originals), indent=2))
    except Exception as error:
        print(json.dumps({'status': 'FAIL_PACKET', 'error_class': type(error).__name__, 'reason': str(error)}))
        raise SystemExit(1)

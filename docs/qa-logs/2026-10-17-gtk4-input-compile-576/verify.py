#!/usr/bin/env python3
"""Read-only hash, lossless-original and compilation-receipt verification."""
import argparse
import gzip
import hashlib
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parent
COMMIT = '969354955741d6c0ca8ce816e1c59ad338b1605b'
BINARY = '27908eb5badf203de53332c4e35ee96d8c7fbbb6afefd5d72d11c9d8068359f8'


def require(condition, message):
    if not condition:
        raise ValueError(message)


def digest(data):
    return hashlib.sha256(data).hexdigest()


def member(name):
    path = Path(name)
    require(not path.is_absolute() and '..' not in path.parts and name != '.', 'unsafe packet path')
    target = ROOT / path
    require(target.is_file() and not target.is_symlink(), 'missing or linked packet member')
    require(all(not part.is_symlink() for part in target.parents if part != ROOT.parent), 'linked parent')
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
        require(digest(member(name).read_bytes()) == value, 'stored hash differs: ' + name)
    index = json.loads(member('originals.json').read_text())
    require(len(index) == 60, 'original member count differs')
    raw, by_source = {}, {}
    for row in index:
        name = row['stored']
        require(row['compression'] in (None, 'gzip'), 'unknown compression')
        if row['compression'] == 'gzip':
            with gzip.open(member(name), 'rb') as stream:
                data = stream.read(row['raw_bytes'] + 1)
                require(stream.read(1) == b'', 'decompressed member exceeds bound')
            logical = name.removesuffix('.gz')
        else:
            data, logical = member(name).read_bytes(), name
        require(logical not in raw and row['source'] not in by_source, 'duplicate original')
        require(len(data) == row['raw_bytes'] and digest(data) == row['raw_sha256'], 'original binding differs: ' + name)
        require(not data.startswith(b'\x7fELF') and b'\0' not in data, 'unexpected binary original')
        if check_originals:
            original = Path(row['source'])
            require(original.is_absolute() and original.is_file(), 'original unavailable')
            require(original.read_bytes() == data, 'current original differs: ' + name)
        raw[logical], by_source[row['source']] = data, data

    def obj(name):
        return json.loads(raw[name])

    def owner(name):
        return obj('originals/owner/' + name)

    def check_bound(rows):
        for path, value in rows.items():
            require(path in by_source and digest(by_source[path]) == value, 'source binding differs: ' + path)

    result, resource, inputs = owner('result.json'), owner('resource-result.json'), owner('inputs.json')
    inner, host = owner('stages/compile/inner-result.json'), owner('stages/compile/host-result.json')
    compiler, container = owner('out/input/compile-result.json'), owner('stages/compile/container-observed.json')
    runner, consumed = obj('originals/run/runner-result.json'), obj('originals/run/admission-consumed.json')
    launcher, census = owner('submit/launcher-result.json'), owner('terminal-host-census.json')
    qualification = owner('qualification.json')
    require(inputs['commit'] == compiler['source_commit'] == qualification['source_commit'] == COMMIT, 'source commit differs')
    require(result['status'] == resource['status'] == 'PASS' and compiler['status'] == 'PASS_COMPILE_ONLY', 'compile not PASS')
    require(all(result[key] == 0 for key in ['original_docker_rc', 'original_compile_wrapper_rc', 'original_compiler_rc']), 'owner original return nonzero')
    require(inner['original_command_rc'] == inner['wrapper_rc'] == host['original_docker_rc'] == compiler['original_compiler_rc'] == 0, 'inner original return nonzero')
    require(runner['command_rc'] == runner['monitor_rc'] == runner['runner_rc'] == launcher['runner_returncode'] == 0, 'outer original return nonzero')
    for name in ['originals/run/build.rc', 'originals/owner/submit/tool-wrapper.rc']:
        require(raw[name].strip() == b'0', 'original return file nonzero')
    require(not result['cleanup'] and not result['signals'] and not result['surviving_host_command_group'] and not result['deadline_overrun'], 'unclean completion')
    require(not resource['errors'] and resource['all_threads_exited'], 'resource watcher failed')
    require(abs(result['seconds'] - 1.8460479939822108) < 1e-9, 'owner elapsed differs')
    require(inner['after']['memory_peak'] == 118661120 and inner['visible_cpus'] == inner['nproc'] == 1, 'compile resources differ')
    for sample in [inner['before'], inner['after']]:
        require(sample['memory_max'] == '2147483648' and sample['memory_swap_max'] == '0', 'cgroup limits differ')
        require(all(sample['memory_events'][key] == 0 for key in ['oom', 'oom_kill', 'oom_group_kill']), 'cgroup OOM event')
    require([json.loads(line) for line in raw['originals/owner/stages/compile/cgroup.jsonl'].splitlines()] == [inner['before'], inner['after']], 'cgroup sample binding differs')
    require(len(raw['originals/owner/host-resources.jsonl'].splitlines()) == resource['host_sample_count'], 'host sample count differs')
    require(inputs['limits']['cpu_ids'] == [4] and inputs['limits']['output_limit_bytes'] == 536870912, 'owner resource contract differs')
    require([inputs['limits'][key] for key in ['producer_seconds', 'cleanup_seconds', 'total_seconds']] == [90, 30, 120], 'lifecycle limits differ')
    require(container['cpuset'] == '4' and container['nano_cpus'] == 1000000000 and container['memory'] == container['memory_swap'] == 2147483648, 'Docker allocation differs')
    require(container['network'] == 'none' and container['read_only_root'] and container['user'] == '1000:1000', 'Docker isolation differs')
    require(sorted(container['mounts'], key=lambda x: x['Destination']) == sorted(inputs['mounts'], key=lambda x: x['Destination']), 'Docker mounts differ')
    require(host['container_observed'] and host['observation_handshake'], 'host observation missing')
    require(inner['host_observation_handshake'] == owner('stages/compile/host-observed.json'), 'nonce handshake differs')
    require(inner['host_observation_handshake']['container_id'] == container['id'] == census['container_id'], 'container identities differ')
    require(raw['originals/owner/stages/compile/container.cid'].decode().strip() == container['id'], 'container ID file differs')
    require(census['container_absent'] and census['all_absent'] and result['container_absent'], 'terminal absence not recorded')
    require(set(census['pids']) == {owner('owner-start.json')['pid'], owner('submit/launcher-start.json')['pid'], owner('stages/compile/host-command.json')['pid']}, 'terminal PID identities differ')
    require(consumed['state'] == 'consumed' and consumed['id'] == '9af04cefcbab47e6afaf83f15efd1039' and consumed['outputs_held'], 'admission not consumed')
    require(consumed['source']['head'] == COMMIT and consumed['original_result'] == runner and consumed['pid_namespace'] == 4026531836, 'admission result binding differs')
    require(digest(raw['originals/owner/retention-plan.json']) == consumed['retention_plan_sha256'] and digest(raw['originals/owner/retention-report.json']) == consumed['retention_report_sha256'], 'retention receipt differs')
    check_bound({row['path']: row['sha256'] for row in owner('acceptance.json')['evidence']})
    require(qualification['allowed_compile_only'] and not qualification['runtime_authorized'] and qualification['critical_pairs_match'] and not qualification['missing_dependencies'] and len(qualification['rpath_findings']) == 6, 'compile-only qualification differs')
    require(all(result['qualification'][key] == qualification[key] for key in result['qualification']), 'owner qualification differs')
    require(raw['originals/owner/qualification.json'] == raw['source/compile-only-qualification.json'] and digest(raw['source/compile-only-qualification.json']) == inputs['qualification_sha256'], 'qualification hash differs')
    require(not inputs['runtime_authorized'] and not result['runtime_authorized'] and not compiler['runtime_invoked'], 'runtime scope differs')
    require(compiler['binary_sha256'] == BINARY and compiler['binary_bytes'] == 27056 and result['outputs']['input/input-spike'] == {'bytes': 27056, 'sha256': BINARY}, 'excluded binary receipt differs')
    require(digest(raw['source/input-source/input-spike.c']) == compiler['source_sha256'], 'compiled source binding differs')
    for name, value in compiler['source_preparation']['files'].items():
        require(digest(raw['source/input-source/' + name]) == value, 'fixture source binding differs')
    for name, value in inputs['helper_sha256'].items():
        require(digest(raw['originals/owner/' + name]) == value, 'owner helper binding differs')
    for name, value in obj('source/owner-preparation/prepared-files.json')['files'].items():
        require(digest(raw['source/owner-preparation/' + name]) == value, 'preparer binding differs')
    check_bound({path: value for path, value in inputs['external_sha256'].items() if path.startswith(inputs['source_packet'] + '/')})
    return {'status': 'PASS_PACKET', 'stored_members': len(expected), 'original_members': len(index),
            'lossless_original_bytes': sum(len(data) for data in raw.values()),
            'original_sources_compared': check_originals, 'original_result_channels_zero': True,
            'owner_seconds': result['seconds'], 'compilation_cgroup_memory_peak_bytes': inner['after']['memory_peak'],
            'cgroup_oom_events': 0, 'admission_consumed': True, 'terminal_absence_recorded': True,
            'excluded_binary_verified': False, 'target_runtime_or_memory_savings_qualified': False,
            'verifier_actions': 'file reads, hashing, gzip decompression and JSON checks only'}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check-originals', action='store_true', help='also compare indexed original files when available')
    options = parser.parse_args()
    try:
        print(json.dumps(main(options.check_originals), indent=2))
    except Exception as error:
        print(json.dumps({'status': 'FAIL_PACKET', 'error_class': type(error).__name__, 'reason': str(error)}))
        raise SystemExit(1)

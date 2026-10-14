#!/usr/bin/env python3
"""Exact-owner cleanup recovery. No Docker calls, target execution, or result rewriting."""
import datetime
import hashlib
import json
from pathlib import Path
import re

HERE = Path(__file__).resolve().parent


def require(ok, message):
    if not ok:
        raise RuntimeError(message)


def sha(path):
    with path.open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def absent(code, stdout, stderr, cid):
    """Only a complete Docker not-found diagnostic for this full owned CID."""
    return (re.fullmatch(r'[0-9a-f]{64}', cid) is not None and code == 1
            and stdout in ('', '\n') and re.fullmatch(
                r'(?i:(?:error: |error response from daemon: )?no such (?:object|container): )'
                + re.escape(cid) + r'\n?', stderr) is not None)


def verify(root, hashes):
    for name, digest in hashes.items():
        path = root / name
        require(not Path(name).is_absolute() and '..' not in Path(name).parts,
                'unsafe evidence member')
        require(path.resolve() == path and path.is_file() and sha(path) == digest,
                'changed or missing bound member: ' + name)


def packet():
    known = json.loads((HERE / 'known-owner.json').read_text())
    for line in (HERE / 'SHA256SUMS').read_text().splitlines():
        digest, name = line.split('  ', 1)
        require(Path(name).name == name and sha(HERE / name) == digest,
                'recovery packet changed')
    return known


def validate_records(records, binding, known):
    outer, compiled = records['result.json'], records['compile-result.json']
    require(set(outer) == {'status','started','original_docker_exit','timed_out',
            'container_cleanup_error','sampler_exited','sampling','ended'},
            'unexpected outer result field (including forced stop)')
    require(outer['status'] == 'FAIL' and outer['original_docker_exit'] == 0
            and outer['timed_out'] is False and outer['sampler_exited'] is True
            and outer['sampling']['error'] is None and outer['sampling']['samples'] > 0
            and outer['container_cleanup_error'] == "RuntimeError('container absence is not established')",
            'not the exact cleanup-only failure')
    require(compiled['status'] == 'PASS' and 'resource_error' not in compiled,
            'inner compilation failed')
    require([s['label'] for s in compiled['stages']] == [
            'configure-baseline-repaired','compile-baseline-repaired',
            'configure-candidate','compile-candidate'] and all(
            s['original_exit'] == 0 and s['timed_out'] is False for s in compiled['stages']),
            'all four original stages must pass')
    require(compiled['input_binding_sha256'] == known['input_binding_sha256']
            and compiled['candidate_commit'] == binding['candidate']['commit']
            and compiled['baseline_repair'] == binding['baseline_repair'], 'source binding differs')
    require(compiled['artifacts'] == known['artifacts']
            and compiled['contract_reports'] == known['contracts'], 'artifact or contract identity differs')
    events = dict(line.split() for line in compiled['memory.events'].splitlines())
    require({'oom','oom_kill'} <= events.keys()
            and all(int(v) == 0 for k,v in events.items() if k.startswith('oom'))
            and 0 < int(compiled['memory.peak']) <= 4 * 1024**3, 'missing memory evidence or OOM')
    for name in known['contracts']:
        contract = records[name]
        require(contract['status'] == 'PASS' and not contract['uninstrumented_or_disabled']
                and contract['rvz_feature_contract'] is True
                and len(contract['direct_source_contracts']) == 2
                and all(not c['missing'] for c in contract['direct_source_contracts']),
                'compiler contract failed')
    cid = known['cid']
    original = records['records/container-final-inspect.json']
    require(absent(original['original_exit'], original['stdout'], original['stderr'], cid),
            'original cleanup error was not exact CID absence')
    proof = records['container-absence-readback.json']
    require(proof['exact_container_absent'] is True and len(proof['checks']) == 2,
            'missing independent absence readback')
    inspect, listing = proof['checks']
    require(inspect['argv'] == ['docker','inspect','--type','container','--format','{{.State.Running}}',cid]
            and absent(inspect['original_exit'], inspect['stdout'], inspect['stderr'], cid),
            'typed absence proof differs')
    require(listing['argv'] == ['docker','ps','-a','--no-trunc','--format','{{.ID}}']
            and listing['original_exit'] == 0 and listing['stderr'] == '',
            'Docker inventory failed (daemon errors do not prove absence)')
    ids = listing['stdout'].splitlines()
    require(all(re.fullmatch(r'[0-9a-f]{64}', item) for item in ids)
            and len(set(ids)) == len(ids) and cid not in ids, 'owned CID present or malformed inventory')
    require(datetime.datetime.fromisoformat(proof['utc']).timestamp() > outer['ended']
            and proof['host_pids_absent'] == known['exited_host_pids']
            and proof['original_wrapper_status'] == 1, 'post-failure cleanup readback differs')
    require(records['submit/launcher-result.json']['runner_returncode'] == 1,
            'original launcher failure must remain explicit')


def validate(root):
    known = packet()
    verify(root, known['evidence'])
    verify(root / 'packet', known['original_packet'])
    verify(root, known['artifacts'])
    binding = json.loads((root / 'packet/input-bindings.json').read_text())
    records = {name: json.loads((root / name).read_text()) for name in known['evidence']
               if name.endswith('.json')}
    validate_records(records, binding, known)
    require((root / 'container.cid').read_text().strip() == known['cid'], 'CID file differs')
    require((root / 'submit/tool-wrapper.rc').read_text().strip() == '1'
            and (root / 'evidence/watcher-build.rc').read_text().strip() == '1',
            'original wrapper/watcher exits must remain1')
    return {'schema':1, 'disposition':'ACCEPT_ARTIFACTS_AFTER_EXACT_CLEANUP_RECOVERY',
            'original_owner':known['owner'], 'original_packet_commit':known['original_packet_commit'],
            'known_owner_sha256':sha(HERE / 'known-owner.json'),
            'recovery_manifest_sha256':sha(HERE / 'SHA256SUMS'),
            'original_outer_status':'FAIL', 'original_launcher_wrapper_watcher_exit':1,
            'original_docker_exit':0, 'runtime_status':'UNRUN',
            'absence_proof_sha256':known['evidence']['container-absence-readback.json'],
            'source_binding_sha256':known['input_binding_sha256'],
            'source_snapshots_verified':known['source_snapshot_counts'],
            'artifacts':known['artifacts'], 'contracts':known['contracts']}


def validate_export(root):
    receipt = validate(root)
    require(json.loads((root / 'recovery-acceptance.json').read_text()) == receipt,
            'missing or altered explicit recovery receipt')
    return receipt

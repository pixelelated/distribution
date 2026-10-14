#!/usr/bin/env python3
"""UNRUN exact-owner recovery: preserve FAIL, validate receipts, rehash only; no network/decode."""
import argparse
import ctypes
import datetime
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import signal
import stat
import sys
import time
import traceback

HERE = Path(__file__).resolve().parent
RUNNER_SHA256 = 'bf548c63a08f1805b08cb267895af03c1468daacd23a104268dc05efa944dbf8'


def load_runner():
    path = HERE / 'runner.py'
    if hashlib.sha256(path.read_bytes()).hexdigest() != RUNNER_SHA256:
        raise RuntimeError('Shared runner identity changed; refuse before loading')
    spec = importlib.util.spec_from_file_location('sealed_public_intake_runner', path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)  # Only the hashed local runner, never archive content.
    return module


def identity(info):
    return tuple(getattr(info, 'st_' + field) for field in
                 ('dev', 'ino', 'mode', 'nlink', 'size', 'mtime_ns', 'ctime_ns'))


def read_receipt(path, cap=4 * 1024**2):
    """Bounded regular receipt bytes only. Never call this on the archive."""
    fd = os.open(path, os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK)
    with os.fdopen(fd, 'rb') as stream:
        before = os.fstat(stream.fileno())
        if not stat.S_ISREG(before.st_mode) or before.st_nlink != 1 or before.st_size > cap:
            raise ValueError('Receipt must be bounded, single-link and regular: ' + str(path))
        raw = stream.read(cap + 1)
        if len(raw) > cap or identity(before) != identity(os.fstat(stream.fileno())):
            raise ValueError('Receipt oversized or changed during read: ' + str(path))
        return raw


def checked_files(runner, directory, rows):
    runner.require(directory.is_absolute() and directory.resolve(strict=True) == directory and directory.is_dir(),
                   'Receipt directory must be canonical')
    result = {}
    for name, expected in rows.items():
        raw = read_receipt(directory / name)
        runner.require(len(raw) == expected['bytes'] and hashlib.sha256(raw).hexdigest() == expected['sha256'],
                       'Original receipt changed: ' + name)
        result[name] = raw
    return result


def original_contract(runner, source, directory):
    """Same fixed transfer/hash predicates, bound to the exact original failure."""
    raw = checked_files(runner, directory, source['original_download_files'])
    old = json.loads(raw['result.json'])
    selected = json.loads((HERE / 'bound/selected.json').read_bytes())
    limits = source['limits']
    runner.require(old['status'] == 'FAIL' and old['phase'] == 'download'
                   and old['error'] == "KeyError('request_size')", 'Not the known final metadata failure')
    runner.require(old['packet_manifest_sha256'] == source['original_packet_manifest_sha256']
                   and old['limits'] == limits and old['attempts'] == 1, 'Original source/limits/attempt mismatch')
    runner.require(old['archive_url'] == selected['url'] and old['expected_archive_bytes'] == selected['size'] == 110373661
                   and old['expected_archive_sha256'] == selected['sha256_from_manifest'], 'Original selected archive mismatch')
    required = selected['size'] + limits['host_report_allowance_bytes'] + limits['host_reserve_bytes']
    runner.require(old['preflight_required_bytes'] == required and old['preflight_free_bytes'] >= required,
                   'Original free-space admission failed')
    runner.require(0 <= old['elapsed_work_and_cleanup_seconds'] < limits['transport_seconds'], 'Original work deadline not satisfied')
    children = [json.loads(raw[label + '.result.json']) for label in ('curl-version', 'transport', 'sha256')]
    runner.require(old['children'] == children and all(runner.accepted(c) for c in children),
                   'Original child failed/intervened or retained processes')
    for label, child in zip(('curl-version', 'transport', 'sha256'), children):
        runner.require(child['argv'] == source['original_child_argv'][label], 'Original child argv mismatch')
        runner.require(child['cleanup_seconds'] <= limits['cleanup_seconds'], 'Original cleanup bound exceeded')
        runner.require(len(raw[label + '.stdout']) <= limits['log_bytes_each'] and len(raw[label + '.stderr']) <= limits['log_bytes_each'],
                       'Original log bound exceeded')
    runner.require(raw['transport.stdout'].count(runner.MARKER) == 1, 'Missing/ambiguous curl metadata marker')
    headers, data = raw['transport.stdout'].split(runner.MARKER, 1)
    metadata = json.loads(data)
    runner.require(metadata == old['curl_metadata'], 'Original curl metadata receipt mismatch')
    runner.require(metadata['http_code'] == 200 and metadata['num_redirects'] == 0 and metadata['url_effective'] == selected['url'],
                   'Unexpected HTTP status, redirect or URL')
    runner.require(metadata['ssl_verify_result'] == 0 and metadata['size_download'] == 110373661,
                   'TLS certificate verification or exact HTTP payload size mismatch')
    encodings = [line.split(b':', 1)[1].strip().lower() for line in headers.split(b'\r\n') if line.lower().startswith(b'content-encoding:')]
    runner.require(not encodings or encodings == [b'identity'], 'Unexpected HTTP Content-Encoding')
    runner.require(metadata['exitcode'] == 0 and metadata['num_retries'] == 0 and metadata['proxy_used'] == 0,
                   'Original metadata reports transport error/retry/proxy')
    runner.require(type(metadata['size_request']) is int and metadata['size_request'] >= 0
                   and type(metadata['size_header']) is int and metadata['size_header'] >= 0, 'Missing/invalid HTTP byte counters')
    hashed = json.loads(raw['sha256.stdout'])
    runner.require(hashed['status'] == 'PASS' and hashed['sha256'] == selected['sha256_from_manifest'] and hashed['bytes'] == 110373661,
                   'Original full-file identity receipt mismatch')
    return selected, metadata


def accept_recovery(runner, source, receipt_path, archive_directory):
    """Explicit VM receipt alternative; no network, archive hash or decoder here."""
    selected, metadata = original_contract(runner, source, archive_directory)
    receipt = json.loads(read_receipt(receipt_path))
    runner.require(receipt['status'] == 'PASS' and receipt['phase'] == 'metadata-recovery' and receipt['schema'] == 1,
                   'Need a separate successful metadata-recovery receipt')
    runner.require(receipt['packet_manifest_sha256'] == runner.sha(HERE / 'SHA256SUMS')
                   and receipt['original_packet_manifest_sha256'] == source['original_packet_manifest_sha256'], 'Recovery source mismatch')
    runner.require(receipt['original_status'] == 'FAIL' and receipt['original_wrapper_exit'] == 1
                   and receipt['original_result_sha256'] == source['original_download_files']['result.json']['sha256'],
                   'Recovery must retain original FAIL1 identity')
    runner.require(receipt['original_download_files'] == source['original_download_files']
                   and receipt['original_owner_files'] == source['original_owner_files'], 'Recovery original bindings mismatch')
    runner.require(receipt['limits'] == source['limits'] and receipt['attempts'] == 1 and receipt['new_download_attempts'] == 0,
                   'Recovery changed bounds or performed acquisition')
    runner.require(0 <= receipt['elapsed_work_and_cleanup_seconds'] < source['limits']['transport_seconds'], 'Recovery deadline exceeded')
    runner.require(receipt['archive_bytes'] == selected['size'] and receipt['archive_sha256'] == selected['sha256_from_manifest']
                   and receipt['full_hash_status'] == 'PASS', 'Recovered archive identity mismatch')
    runner.require(receipt['http_payload_bytes'] == metadata['size_download']
                   and receipt['http_reported_header_bytes'] == metadata['size_header']
                   and receipt['http_reported_request_bytes'] == metadata['size_request'], 'Recovered HTTP counters mismatch')
    runner.require(set(receipt['fresh_hash_files']) == {'sha256.result.json', 'sha256.stdout', 'sha256.stderr'}, 'Incomplete fresh hash bindings')
    raw = checked_files(runner, receipt_path.parent, receipt['fresh_hash_files'])
    child = json.loads(raw['sha256.result.json'])
    hashed = json.loads(raw['sha256.stdout'])
    runner.require(receipt['children'] == [child] and runner.accepted(child), 'Recovery hash child failed or needed intervention')
    runner.require(child['cleanup_seconds'] <= source['limits']['cleanup_seconds']
                   and len(raw['sha256.stdout']) <= source['limits']['log_bytes_each']
                   and len(raw['sha256.stderr']) <= source['limits']['log_bytes_each'], 'Recovery child bound exceeded')
    runner.require(hashed['status'] == 'PASS' and hashed['sha256'] == selected['sha256_from_manifest'] and hashed['bytes'] == 110373661,
                   'Recovery full-file hash receipt mismatch')
    return receipt


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--download', required=True, type=Path)
    parser.add_argument('--owner', required=True, type=Path)
    parser.add_argument('--output', required=True, type=Path)
    args = parser.parse_args()
    report = {'status': 'FAIL', 'phase': 'metadata-recovery', 'schema': 1, 'children': [],
              'started_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
              'evidence': 'New receipt: original transport/hash evidence plus fresh read-only full SHA256; no decoding',
              'new_download_attempts': 0,
              'wire_accounting': 'UNMEASURED; no aggregate TLS/TCP/DNS wire cap or quota claimed'}
    output, started = None, None
    try:
        runner = load_runner()
        source = runner.seal(); limits = source['limits']
        runner.require(args.download == Path(source['original_download_dir']) and args.owner == Path(source['original_owner_dir']),
                       'Recovery is scoped to the exact known failed owner')
        requested = args.output
        runner.require(requested.is_absolute() and requested.parent.resolve(strict=True) == requested.parent, 'Output parent must be canonical')
        runner.require(not requested.exists() and not requested.is_symlink(), 'Output exists; preserve original recovery')
        runner.require(not requested.is_relative_to('/storage') and not requested.is_relative_to(HERE.parents[2])
                       and not requested.is_relative_to(args.download) and not requested.is_relative_to(args.owner), 'Output overlaps original/source/storage')
        free = os.statvfs(requested.parent)
        minimum = limits['http_payload_bytes'] + limits['host_report_allowance_bytes'] + limits['host_reserve_bytes']
        runner.require(free.f_bavail * free.f_frsize >= minimum, 'Original ordinary free-space margin unavailable')
        requested.mkdir(mode=0o700); output = requested
        os.umask(0o077)
        started = time.monotonic()
        selected, metadata = original_contract(runner, source, args.download)
        owners = checked_files(runner, args.owner, source['original_owner_files'])
        runner.require(owners['tool-wrapper.rc'].strip() == b'1'
                       and json.loads(owners['launcher-result.json'])['runner_returncode'] == 1, 'Original wrapper/launcher result mismatch')
        archive = args.download / 'archive.zip'
        before = archive.lstat()
        runner.require(stat.S_ISREG(before.st_mode) and before.st_nlink == 1 and before.st_size == 110373661, 'Retained archive type/size/link mismatch')
        report.update(packet_manifest_sha256=runner.sha(HERE / 'SHA256SUMS'), limits=limits, attempts=1,
                      original_status='FAIL', original_wrapper_exit=1,
                      original_packet_manifest_sha256=source['original_packet_manifest_sha256'],
                      original_result_sha256=source['original_download_files']['result.json']['sha256'],
                      original_download_files=source['original_download_files'], original_owner_files=source['original_owner_files'],
                      archive_path=str(archive), python=sys.version, python_sha256=runner.sha(Path(sys.executable).resolve()),
                      preflight_free_bytes=free.f_bavail * free.f_frsize, preflight_required_bytes=minimum)
        libc = ctypes.CDLL(None, use_errno=True)
        runner.require(libc.prctl(36, 1, 0, 0, 0) == 0, 'Cannot arm unprivileged subreaper')
        runner.require(hasattr(os, 'pidfd_open') and hasattr(signal, 'pidfd_send_signal'), 'Linux pidfd support required')
        signal.signal(signal.SIGTERM, runner.stop_signal); signal.signal(signal.SIGINT, runner.stop_signal)
        remaining = limits['transport_seconds'] - (time.monotonic() - started)
        runner.require(remaining > 0, 'Recovery deadline reached')
        child = runner.run([sys.executable, '-I', '-S', '-B', str(HERE / 'hash_archive.py'), '--archive', str(archive)],
                           output, 'sha256', remaining, limits)
        report['children'].append(child)
        runner.require(runner.accepted(child), 'Fresh full-file hash failed/intervened; original bytes and failure preserved')
        hashed = json.loads(read_receipt(output / 'sha256.stdout', limits['log_bytes_each']))
        runner.require(hashed['status'] == 'PASS' and hashed['sha256'] == selected['sha256_from_manifest'] and hashed['bytes'] == 110373661,
                       'Fresh full-file identity receipt mismatch')
        runner.require(identity(before) == identity(archive.lstat()), 'Archive identity changed during recovery')
        original_contract(runner, source, args.download)
        checked_files(runner, args.owner, source['original_owner_files'])
        runner.require(time.monotonic() - started < limits['transport_seconds'], 'Recovery deadline reached')
        rows = {}
        for name in ('sha256.result.json', 'sha256.stdout', 'sha256.stderr'):
            raw = read_receipt(output / name)
            rows[name] = {'bytes': len(raw), 'sha256': hashlib.sha256(raw).hexdigest()}
        report.update(status='PASS', archive_bytes=hashed['bytes'], archive_sha256=hashed['sha256'], full_hash_status='PASS',
                      fresh_hash_files=rows, archive_identity=list(identity(before)),
                      http_payload_bytes=metadata['size_download'], http_reported_header_bytes=metadata['size_header'],
                      http_reported_request_bytes=metadata['size_request'], decoding='NOT PERFORMED; separately allocated offline VM only')
    except BaseException as error:
        report.update(error=repr(error), traceback=traceback.format_exc(limit=8))
    if started is not None:
        report['elapsed_work_and_cleanup_seconds'] = time.monotonic() - started
    report['finished_utc'] = datetime.datetime.now(datetime.timezone.utc).isoformat()
    if output is not None:
        (output / 'result.json').write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps(report, indent=2))
    return 0 if report['status'] == 'PASS' else 1


if __name__ == '__main__':
    sys.exit(main())

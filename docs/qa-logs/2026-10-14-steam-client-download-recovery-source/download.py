#!/usr/bin/env python3
"""UNRUN one-attempt public download with HTTP payload and ordinary disk bounds."""
import argparse
import ctypes
import datetime
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import shutil
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


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', required=True, type=Path)
    args = parser.parse_args()
    report = {'status': 'FAIL', 'phase': 'download', 'evidence': 'Public archive acquisition and full-file SHA256 only; no decoding',
              'started_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(), 'children': [],
              'wire_accounting': 'UNMEASURED; no aggregate TLS/TCP/DNS wire cap or quota claimed',
              'attempts': 0}
    output, started = None, None
    try:
        runner = load_runner()
        binding = runner.seal(); limits = binding['limits']
        selected = json.loads((HERE / 'bound/selected.json').read_bytes())
        runner.require(selected['size'] == limits['http_payload_bytes'] == 110373661, 'Exact advertised HTTP payload cap changed')
        requested = args.output
        runner.require(requested.is_absolute() and requested.parent.resolve(strict=True) == requested.parent, 'Output parent must be an existing canonical directory')
        runner.require(not requested.exists() and not requested.is_symlink(), 'Output already exists; preserve it, no retry/resume')
        runner.require(not requested.is_relative_to('/storage') and not requested.is_relative_to(HERE.parents[2]), 'Output overlaps storage/source')
        capacity = os.statvfs(requested.parent)
        minimum = selected['size'] + limits['host_report_allowance_bytes'] + limits['host_reserve_bytes']
        free = capacity.f_bavail * capacity.f_frsize
        runner.require(free >= minimum, f'Need archive + reports + 64MiB reserve: {minimum} bytes free; have {free}')
        # An ordinary exclusive private directory. No mount, quota, sudo or installation.
        requested.mkdir(mode=0o700)
        output = requested
        os.umask(0o077)
        report.update(packet_manifest_sha256=runner.sha(HERE / 'SHA256SUMS'), limits=limits,
                      archive_url=selected['url'], expected_archive_bytes=selected['size'],
                      expected_archive_sha256=selected['sha256_from_manifest'],
                      preflight_free_bytes=free, preflight_required_bytes=minimum,
                      python=sys.version, python_sha256=runner.sha(Path(sys.executable).resolve()))
        libc = ctypes.CDLL(None, use_errno=True)
        runner.require(libc.prctl(36, 1, 0, 0, 0) == 0, 'Cannot arm unprivileged subreaper')
        runner.require(hasattr(os, 'pidfd_open') and hasattr(signal, 'pidfd_send_signal'), 'Linux pidfd support required for managed cleanup')
        signal.signal(signal.SIGTERM, runner.stop_signal); signal.signal(signal.SIGINT, runner.stop_signal)
        tool = shutil.which('curl')
        runner.require(tool is not None, 'curl not installed; refuse without installation')
        resolved = Path(tool).resolve(strict=True)
        mode = resolved.stat().st_mode
        runner.require(stat.S_ISREG(mode) and not mode & (stat.S_ISUID | stat.S_ISGID), 'curl must be a regular non-setid executable')
        report['curl'] = {'invoke_path': tool, 'resolved_path': str(resolved), 'sha256': runner.sha(resolved)}
        started = time.monotonic()
        deadline = started + limits['transport_seconds']
        def remaining():
            seconds = deadline - time.monotonic()
            runner.require(seconds > 0, '180-second acquisition/hash work deadline reached')
            return seconds
        version = runner.run([tool, '-q', '--version'], output, 'curl-version', min(5, remaining()), limits)
        report['children'].append(version)
        runner.require(runner.accepted(version), 'Original curl version probe failed')
        archive = output / 'archive.zip'
        with archive.open('xb'):
            pass
        argv = [tool, '-q', '--fail', '--silent', '--show-error', '--http1.1', '--noproxy', '*',
                '--proto', '=https', '--proto-redir', '=https', '--max-redirs', '0', '--retry', '0',
                '--connect-timeout', '10', '--max-time', '180', '--max-filesize', '110373661',
                '--header', 'If-Match: "6ace8266-6942b1d"', '--header', 'Accept-Encoding: identity',
                '--dump-header', '-', '--output', str(archive),
                '--write-out', runner.MARKER.decode() + '%{json}\n', selected['url']]
        report['attempts'] = 1
        child = runner.run(argv, output, 'transport', remaining(), limits, file_cap=110373661)
        report['children'].append(child)
        runner.require(runner.accepted(child), 'Original transport failed/timed out; retain partial file and stop')
        runner.require(runner.sha(resolved) == report['curl']['sha256'], 'curl executable changed during acquisition')
        raw = (output / 'transport.stdout').read_bytes()
        runner.require(raw.count(runner.MARKER) == 1, 'Missing/ambiguous curl metadata marker')
        headers, data = raw.split(runner.MARKER, 1)
        metadata = json.loads(data)
        report['curl_metadata'] = metadata
        runner.require(metadata['http_code'] == 200 and metadata['num_redirects'] == 0 and metadata['url_effective'] == selected['url'], 'Unexpected HTTP status, redirect or URL')
        runner.require(metadata['ssl_verify_result'] == 0 and metadata['size_download'] == 110373661, 'TLS certificate verification or exact HTTP payload size mismatch')
        encodings = [line.split(b':', 1)[1].strip().lower() for line in headers.split(b'\r\n') if line.lower().startswith(b'content-encoding:')]
        runner.require(not encodings or encodings == [b'identity'], 'Unexpected HTTP Content-Encoding')
        runner.require(archive.stat().st_size == 110373661, 'Downloaded file has wrong exact size')
        hash_argv = [sys.executable, '-I', '-S', '-B', str(HERE / 'hash_archive.py'), '--archive', str(archive)]
        hashed = runner.run(hash_argv, output, 'sha256', remaining(), limits)
        report['children'].append(hashed)
        runner.require(runner.accepted(hashed), 'Original full-file SHA256 check failed/timed out; no decoding')
        identity = json.loads((output / 'sha256.stdout').read_bytes())
        runner.require(identity['status'] == 'PASS' and identity['sha256'] == selected['sha256_from_manifest'] and identity['bytes'] == 110373661, 'Full-file identity receipt mismatch')
        remaining()
        report.update(status='PASS', archive_path=str(archive), archive_bytes=identity['bytes'], archive_sha256=identity['sha256'],
                      full_hash_status='PASS', http_payload_bytes=metadata['size_download'],
                      http_reported_header_bytes=metadata['size_header'], http_reported_request_bytes=metadata['size_request'],
                      decoding='NOT PERFORMED; separately allocated offline VM only')
    except BaseException as error:
        report.update(error=repr(error), traceback=traceback.format_exc(limit=8))
    if started is not None:
        report['elapsed_work_and_cleanup_seconds'] = time.monotonic() - started
    report['finished_utc'] = datetime.datetime.now(datetime.timezone.utc).isoformat()
    if output is not None:
        report['retained_bytes_before_result'] = sum(p.stat().st_size for p in output.iterdir() if p.is_file())
        capacity = os.statvfs(output)
        report['free_bytes_after'] = capacity.f_bavail * capacity.f_frsize
        (output / 'result.json').write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps(report, indent=2))
    return 0 if report['status'] == 'PASS' else 1


if __name__ == '__main__':
    sys.exit(main())

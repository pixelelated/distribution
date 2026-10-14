#!/usr/bin/env python3
"""UNRUN receipt adapter for b393's unchanged verifier in a separate allocated VM."""
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
    parser.add_argument('--scratch-root', required=True, type=Path)
    parser.add_argument('--output', required=True, type=Path)
    parser.add_argument('--archive', required=True, type=Path)
    parser.add_argument('--admission', required=True, type=Path)
    parser.add_argument('--recovery', type=Path, help='Explicit separate recovery receipt; original download FAIL is retained')
    args = parser.parse_args()
    report = {'status': 'FAIL', 'phase': 'verify', 'evidence': 'Offline VM integrity/structure only; not native/product acceptance', 'children': []}
    output = None
    try:
        runner = load_runner()
        source = runner.seal(); limits = source['limits']
        root = args.scratch_root
        runner.require(root.is_absolute() and root.resolve(strict=True) == root and root.is_dir(), 'Scratch root must be canonical existing directory')
        runner.require(root != Path('/') and not root.is_relative_to('/storage') and not root.is_relative_to(HERE.parents[2]), 'Scratch overlaps system/storage/source')
        info = root.stat()
        runner.require(info.st_uid == os.getuid() and stat.S_IMODE(info.st_mode) == 0o700, 'VM scratch root must be caller-owned mode 0700')
        mounts = [line.split() for line in Path('/proc/self/mountinfo').read_text().splitlines()]
        exact = [row for row in mounts if row[4] == str(root)]
        runner.require(len(exact) == 1 and exact[0][exact[0].index('-') + 1] == 'tmpfs', 'Require the dedicated allocated VM tmpfs; no mount created here')
        runner.require({'noexec', 'nosuid', 'nodev'} <= set(exact[0][5].split(',')), 'VM scratch must be noexec,nosuid,nodev')
        capacity = os.statvfs(root)
        runner.require(capacity.f_blocks * capacity.f_frsize <= limits['scratch_bytes'], 'VM scratch hard capacity exceeds 768MiB')
        runner.require(capacity.f_bavail * capacity.f_frsize >= 16 * 1024**2, 'Need >=16MiB report headroom after archive staging')
        admission = json.loads(args.admission.read_bytes())
        runner.require(admission['packet_manifest_sha256'] == runner.sha(HERE / 'SHA256SUMS') and admission['scratch_mount'] == str(root), 'VM allocation source/scratch mismatch')
        runner.require(admission['scratch_max_bytes'] == limits['scratch_bytes'] and admission['coordinator'] == 'w4:p2', 'VM allocation bound/coordinator mismatch')
        expiry = datetime.datetime.fromisoformat(admission['expires_utc'])
        runner.require(expiry.tzinfo is not None and expiry > datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(seconds=limits['verification_seconds'] + limits['cleanup_seconds']), 'VM allocation must cover verification and cleanup')
        archive = args.archive
        runner.require(archive.is_absolute() and archive.resolve(strict=True) == archive and archive.parent.parent == root and archive.name == 'archive.zip', 'Stage the original download directory directly under VM scratch')
        selected = json.loads((HERE / 'bound/selected.json').read_bytes())
        if args.recovery is None:
            download = json.loads((archive.parent / 'result.json').read_bytes())
            runner.require(download['status'] == 'PASS' and download['phase'] == 'download' and download['packet_manifest_sha256'] == runner.sha(HERE / 'SHA256SUMS'), 'Need original successful revised-host receipt, not a rewritten b393 receipt')
        else:
            receipt = args.recovery
            runner.require(receipt.is_absolute() and receipt.resolve(strict=True) == receipt and receipt.name == 'result.json'
                           and receipt.parent.parent == root and receipt.parent != archive.parent and receipt.stat().st_dev == info.st_dev,
                           'Stage separate recovery owner directly under the same VM scratch')
            # runner.seal already verified this local adapter; no payload import.
            spec = importlib.util.spec_from_file_location('sealed_metadata_recovery', HERE / 'recover.py')
            recovery = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(recovery)
            download = recovery.accept_recovery(runner, source, receipt, archive.parent)
        runner.require(download['archive_sha256'] == selected['sha256_from_manifest'] and download['archive_bytes'] == selected['size'] and download['attempts'] == 1, 'Host receipt archive identity/attempt count mismatch')
        runner.require(archive.stat().st_dev == info.st_dev, 'Archive escaped VM scratch mount')
        requested = args.output
        runner.require(requested.is_absolute() and requested.parent == root and not requested.exists() and not requested.is_symlink(), 'VM output must be an unused direct child')
        requested.mkdir(mode=0o700); output = requested
        with (root / 'verify-attempt.json').open('x') as attempt:
            json.dump({'packet_manifest_sha256': runner.sha(HERE / 'SHA256SUMS'), 'output': str(output)}, attempt)
        report.update(packet_manifest_sha256=runner.sha(HERE / 'SHA256SUMS'), admission=admission, limits=limits,
                      python=sys.version, python_sha256=runner.sha(Path(sys.executable).resolve()),
                      original_host_receipt_sha256=runner.sha(archive.parent / 'result.json'),
                      recovery_receipt_sha256=runner.sha(args.recovery) if args.recovery is not None else None)
        libc = ctypes.CDLL(None, use_errno=True)
        runner.require(libc.prctl(36, 1, 0, 0, 0) == 0, 'Cannot arm subreaper')
        runner.require(hasattr(os, 'pidfd_open') and hasattr(signal, 'pidfd_send_signal'), 'Linux pidfd support required')
        signal.signal(signal.SIGTERM, runner.stop_signal); signal.signal(signal.SIGINT, runner.stop_signal)
        fd = os.open(archive, os.O_RDONLY | os.O_NOFOLLOW)
        try:
            argv = [sys.executable, '-I', '-S', '-B', str(HERE / 'verify_archive.py'), '--archive-fd', str(fd), '--receipt', str(output / 'inspection.json')]
            child = runner.run(argv, output, 'verification', limits['verification_seconds'], limits, pass_fds=(fd,))
        finally:
            os.close(fd)
        report['children'].append(child)
        runner.require(runner.accepted(child), 'Original VM verification failed/timed out; retain evidence, no retry')
        inspection = json.loads((output / 'inspection.json').read_bytes())
        runner.require(inspection['status'] == 'PASS', 'VM inspection did not pass')
        report.update(status='PASS', archive_sha256=inspection['archive_sha256'], members=len(inspection['members']),
                      decoded_bytes=inspection['decoded_bytes'], native_readiness='UNPROVEN')
    except BaseException as error:
        report.update(error=repr(error), traceback=traceback.format_exc(limit=8))
    if output is not None:
        (output / 'result.json').write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps(report, indent=2))
    return 0 if report['status'] == 'PASS' else 1


if __name__ == '__main__':
    sys.exit(main())

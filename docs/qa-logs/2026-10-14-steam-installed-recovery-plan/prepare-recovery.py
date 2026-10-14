#!/usr/bin/env python3
"""Prepare one additive source packet; never import or execute its fixtures."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import stat

ORIGINAL_SEAL = '6a6c3b255525f57c624dba32d55720e10d0e130c2ffeb564c4e2ae6881796c7d'
INSTALLER_SHA256 = 'fab7cdb4ad8adbcea147be54092bb7ce2005010447be4ab8192c94d8bbe9229d'
REMAINING = (
    'fresh-profile-dot', 'fresh-profile-dot-absent', 'valid-existing-alias',
    'existing-profile-dot', 'self-updated-client', 'partial-before-profile',
    'marker-missing-core', 'metadata-conflict-after-profile',
    'download-failure-retry', 'metadata-failure-retry',
    'interrupt-prepared-retry', 'unknown-stage-before-profile',
    'validation-failure-retry', 'publication-failure-retry',
)
ACCEPTED = (
    'fresh-client-real-root', 'fresh-profile-parent-alias',
    'existing-profile-parent-alias', 'detached-transfer-child',
    'proc-census-error', 'transport-timeout', 'interrupt-published-retry',
    'committed-self-update-retry', 'crc-failure-retry',
)


def require(value, message):
    if not value:
        raise RuntimeError(message)


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def read_regular(path):
    before = path.lstat()
    require(stat.S_ISREG(before.st_mode) and before.st_size <= 1024**2,
            'Unexpected packet member type or size: ' + str(path))
    with path.open('rb') as stream:
        opened = os.fstat(stream.fileno())
        raw = stream.read(1024**2 + 1)
        after = os.fstat(stream.fileno())
    identity = lambda s: (s.st_dev, s.st_ino, s.st_mode, s.st_size, s.st_mtime_ns, s.st_ctime_ns)
    require(len(raw) <= 1024**2 and identity(before) == identity(opened) == identity(after)
            == identity(path.lstat()), 'Packet changed during read: ' + str(path))
    return raw, stat.S_IMODE(before.st_mode)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--accepted-packet', required=True, type=Path)
    parser.add_argument('--output', required=True, type=Path)
    args = parser.parse_args()
    source = args.accepted_packet.resolve(strict=True)
    output = args.output.absolute()
    require(source.is_dir() and args.accepted_packet.absolute() == source, 'Aliased source directory')
    require(output.parent.resolve(strict=True) == output.parent and not output.exists()
            and not output.is_symlink() and not output.is_relative_to(source), 'Output must be a fresh sibling/private directory')
    manifest, _ = read_regular(source / 'SHA256SUMS')
    require(sha(manifest) == ORIGINAL_SEAL, 'Not the accepted 8f0eaf CRC event packet')
    files = {}
    for line in manifest.decode().splitlines():
        expected, name = line.split('  ', 1)
        relative = Path(name)
        require(not relative.is_absolute() and '..' not in relative.parts and name not in files,
                'Unsafe/duplicate source member')
        path = source / relative
        require(path.resolve(strict=True) == path, 'Aliased source member')
        raw, mode = read_regular(path)
        require(sha(raw) == expected, 'Source seal mismatch: ' + name)
        files[name] = (raw, mode)
    actual = set()
    for path in source.rglob('*'):
        require(not path.is_symlink(), 'Unexpected source symlink')
        if path.is_file() and path.name != 'SHA256SUMS':
            actual.add(str(path.relative_to(source)))
    require(actual == set(files) and len(files) <= 128
            and sum(len(raw) for raw, _ in files.values()) <= 4 * 1024**2,
            'Source packet member/size contract changed')
    binding = json.loads(files['source.json'][0])
    require(binding['cases'] == ['crc-failure-retry']
            and binding['installer_sha256'] == INSTALLER_SHA256, 'Unexpected accepted dispatch/source binding')
    require(len(REMAINING) == 14 and len(set(REMAINING)) == 14
            and set(REMAINING).isdisjoint(ACCEPTED), 'Repeated accepted case')
    binding['cases'] = list(REMAINING)
    original_source = files['source.json'][0]
    files['source.json'] = ((json.dumps(binding, indent=2) + '\n').encode(), 0o644)
    additions = {
        'original-SHA256SUMS': manifest,
        'original-source.json': original_source,
        'continuation.json': (json.dumps({
            'status': 'SOURCE_ONLY_UNRUN',
            'original_manifest_sha256': ORIGINAL_SEAL,
            'original_fixture_commit': '8f0eaf27ed539beeac4c117711601d78c9125d4a',
            'installer_sha256': INSTALLER_SHA256,
            'changed_original_member': 'source.json',
            'only_changed_binding_key': 'cases',
            'remaining_cases': list(REMAINING),
            'accepted_cases_excluded': list(ACCEPTED),
            'scope': 'Unchanged complete source caller in private chroot; no installed installer or native Steam claim',
            'historical_files': 'Original README/static-result/static-check describe their CRC-only source, not this continuation. Do not run the historical static-check against modified binding.',
        }, indent=2) + '\n').encode(),
    }
    require(not set(additions).intersection(files), 'New receipt name collides with original')
    output.mkdir(mode=0o700)
    for name, (raw, mode) in files.items():
        path = output / name
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open('xb') as stream:
            stream.write(raw)
        path.chmod(mode)
    for name, raw in additions.items():
        with (output / name).open('xb') as stream:
            stream.write(raw)
        files[name] = (raw, 0o644)
    sealed = ''.join(sha(raw) + '  ' + name + '\n' for name, (raw, _) in sorted(files.items())).encode()
    with (output / 'SHA256SUMS').open('xb') as stream:
        stream.write(sealed)
    print(json.dumps({'status': 'SOURCE_ONLY_PREPARED', 'output': str(output),
                      'manifest_sha256': sha(sealed), 'fixture_runtime': 'UNRUN',
                      'permitted_case_count': len(REMAINING)}))


if __name__ == '__main__':
    main()

#!/usr/bin/env python3
"""Prepare one offline guest for exact metadata helper plus unchanged fourteen cases."""
import argparse
import ast
import hashlib
import json
from pathlib import Path
import shutil
import stat
import subprocess

HERE = Path(__file__).resolve().parent
REMAINING_SEAL = '79dc1d57d8741b644e99cd8348c4c362fbef3a1c815c48f6fa23b84a6e201c34'
INSTALLER_SHA = 'fab7cdb4ad8adbcea147be54092bb7ce2005010447be4ab8192c94d8bbe9229d'
INSTALLER_PATH = 'projects/ROCKNIX/packages/virtual/emulators/sources/Install Steam.sh'

def sha(path):
    h = hashlib.sha256()
    with path.open('rb') as stream:
        for block in iter(lambda: stream.read(4 * 1024**2), b''):
            h.update(block)
    return h.hexdigest()

def save(path, value):
    with path.open('x') as stream:
        json.dump(value, stream, indent=2); stream.write('\n')

def sealed(directory, expected=None):
    assert directory.resolve(strict=True) == directory
    if expected:
        assert sha(directory / 'SHA256SUMS') == expected
    names = []
    for line in (directory / 'SHA256SUMS').read_text().splitlines():
        digest, name = line.split('  ', 1); p = directory / name
        assert not Path(name).is_absolute() and '..' not in Path(name).parts and name not in names
        assert p.resolve(strict=True) == p and p.is_file() and sha(p) == digest
        names.append(name)
    assert set(names) == {str(p.relative_to(directory)) for p in directory.rglob('*') if p.is_file() and p != directory / 'SHA256SUMS'}
    return names + ['SHA256SUMS']

p = argparse.ArgumentParser()
p.add_argument('--checkout', type=Path, required=True, help='Frozen distribution checkout of completed image')
p.add_argument('--image-verification', type=Path, required=True, help='Completed existing verify-image.py output directory')
p.add_argument('--remaining-packet', type=Path, default=HERE / 'remaining-source')
p.add_argument('--owner', type=Path, required=True)
p.add_argument('--vnc', type=int, required=True)
a = p.parse_args()
assert 100 <= a.vnc <= 199 and a.owner.parent == Path('/workspace/tmp') and not a.owner.exists()
assert a.checkout.is_absolute() and a.checkout.resolve(strict=True) == a.checkout
assert not subprocess.check_output(['git', 'status', '--porcelain'], cwd=a.checkout, timeout=30).strip()
commit = subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=a.checkout, text=True, timeout=30).strip()
sealed(HERE); names = sealed(a.remaining_packet, REMAINING_SEAL)
verified = json.loads((a.image_verification / 'result.json').read_text())
identity = json.loads((a.image_verification / 'inputs.json').read_text())
assert verified['status'] == 'PASS' and verified['source'] == identity['source'] == commit
assert identity['identity']['build_commit'] == commit
assert identity['identity']['device'] == 'GENERIC_X64' and identity['identity']['arch'] == 'x86_64'
images = [(Path(name), row) for name, row in identity['artifacts'].items() if name.endswith('.img.gz')]
assert len(images) == 1
image, record = images[0]
assert image.is_file() and not image.is_symlink() and image.stat().st_size == record['bytes'] and sha(image) == record['sha256']
raw_bytes = (a.image_verification / 'candidate.img').stat().st_size
assert 0 < raw_bytes <= 16 * 1024**3
assert sha(a.checkout / INSTALLER_PATH) == INSTALLER_SHA
binding = json.loads((a.remaining_packet / 'source.json').read_text())
assert binding['installer_sha256'] == INSTALLER_SHA
metadata = json.loads((HERE / 'metadata/source-binding.json').read_text())
assert metadata['frozen_installer_sha256'] == INSTALLER_SHA
assert sha(HERE / metadata['helper']) == metadata['helper_sha256'] == '68f298d4d23994ca9aebbab284dda2f8961b6c6d5569e2bee4f7574b78fe8355'
assert sha(HERE / metadata['candidate_source']) == metadata['candidate_source_sha256'] == 'cefb22a50db915be1637e682dfba047789b276144bbe707220a2b4117c7a3264'
assert sha(HERE / 'guest-stage.py') == metadata['original_guest_stage_sha256'] == '2f8896c92621a7e7f6079abe5a4d8332e0846e088baa04c6503d1f6fa3a51dad'
old = b'curl -fsSL "${api_url}"'
new = b'curl -q -fsSL --connect-timeout 10 --max-time 30 --max-filesize 1048576 "${api_url}"'
frozen = (a.checkout / INSTALLER_PATH).read_bytes()
assert frozen.count(old) == 1 and frozen.replace(old, new) == (HERE / metadata['candidate_source']).read_bytes()
system = Path(metadata['installed_dependency_provenance'])
assert system == a.checkout / 'build.pixelelated-GENERIC_X64.x86_64/image/system'
for name, expected in metadata['installed_dependencies'].items():
    path = system / name.lstrip('/'); resolved = path.resolve(strict=True)
    assert resolved.is_relative_to(system)
    observed = {'resolved': '/' + str(resolved.relative_to(system)), 'sha256': sha(resolved),
                'bytes': resolved.stat().st_size, 'mode': stat.S_IMODE(resolved.stat().st_mode),
                'symlink': str(path.readlink()) if path.is_symlink() else None}
    assert observed == expected, 'Installed dependency input changed: ' + name
# Literal AST read only. Do not import the guest wrapper or original fixture.
module = ast.parse((HERE / 'guest-stage.py').read_text())
cases = next(ast.literal_eval(n.value) for n in module.body if isinstance(n, ast.Assign)
             and len(n.targets) == 1 and isinstance(n.targets[0], ast.Name) and n.targets[0].id == 'CASES')
assert len(cases) == 14 and set(cases) == set(binding['cases'])
a.owner.mkdir()
for name in ('records', 'scan', 'vm', 'stages', 'lifecycle-owner', 'logs'):
    (a.owner / name).mkdir()
family = {'cases': list(cases), 'source_commit': commit, 'installer_path': INSTALLER_PATH,
          'installer_sha256': INSTALLER_SHA, 'scope': 'source chroot, not installed/native Steam',
          'remaining_packet_seal': REMAINING_SEAL, 'metadata': metadata}
save(a.owner / 'records/family.json', family)
files = []
for name in names:
    path = a.remaining_packet / name
    files.append({'path': str(path), 'destination': 'docs/qa-logs/2026-10-14-steam-remaining-source/' + name, 'sha256': sha(path)})
for path, destination in [(a.checkout / INSTALLER_PATH, INSTALLER_PATH),
                          (HERE / 'guest-stage.py', 'guest-stage.py'),
                          (HERE / 'metadata-stage.py', 'metadata-stage.py'),
                          (HERE / metadata['helper'], metadata['helper']),
                          (HERE / metadata['candidate_source'], metadata['candidate_source']),
                          (a.owner / 'records/family.json', 'family.json')]:
    files.append({'path': str(path), 'destination': destination, 'sha256': sha(path)})
helper_path = a.checkout / 'projects/ROCKNIX/devices/GENERIC_X64/vm/generic-x64-vm'
helper = {'path': str(helper_path), 'commit': commit, 'sha256': sha(helper_path)}
save(a.owner / 'records/inputs.json', {'files': files, 'helper': helper})
save(a.owner / 'records/image-size.json', {'image': str(image), 'compressed_bytes': record['bytes'],
      'raw_bytes_from_backup_lba': raw_bytes, 'sha256': record['sha256']})
runtime = {'checkout': str(a.checkout), 'commit': commit, 'panel': '640x480', 'cases': list(cases),
           'vnc': a.vnc, 'family_seconds': 3600, 'stage_seconds': 180, 'metadata_seconds': 150,
           'tool_hashes': {name: sha(a.checkout / name) for name in ('tools/vm-serial', 'tools/vm-stop')},
           'packet': str(HERE), 'packet_manifest_sha256': sha(HERE / 'SHA256SUMS'),
           'image_verification': {name: sha(a.image_verification / name) for name in ('inputs.json', 'result.json')}}
save(a.owner / 'records/runtime.json', runtime)
shutil.copyfile(HERE / 'vm-lifecycle.py', a.owner / 'vm-lifecycle.py')
terms = {'raw_image': raw_bytes, 'guest_disk': 16 * 1024**3,
         'input_media': 256 * 1024**2, 'output_media': 1280 * 1024**2, 'records_export': 1200 * 1024**2}
plan = {'volume': '/workspace', 'scan_roots': [str(a.owner / 'scan')], 'reference_stores': [],
        'protected': [str(HERE), str(a.checkout), str(image), str(a.remaining_packet)], 'candidates': [],
        'builds': [{'name': 'pix582-remaining14-metadata', 'terms_bytes': terms,
                    'basis': 'One no-NIC8GiB/4CPU guest,16GiB virtual disk; exact metadata helper then14 unchanged stages. Unchanged3600s family plus90s fail-stop cleanup. Metadata110+10s inner/150s serial; each stage must fit remaining time plus90s reserve. One active3GiB tmpfs;1280MiB output, combined evidence<=1100MiB. Installed curl/Bash metadata scope and separate source-chroot14; no Steam install/native claim.',
                    'evidence': [{'path': str(a.owner / name), 'sha256': sha(a.owner / name)} for name in
                                 ('records/image-size.json', 'records/inputs.json', 'records/runtime.json', 'vm-lifecycle.py')]}]}
save(a.owner / 'retention-plan.json', plan)
save(a.owner / 'admission-plan.json', {'checkout': str(a.checkout), 'retention_plan': str(a.owner / 'retention-plan.json'),
      'retention_report': str(a.owner / 'retention-report.json'), 'stage': 'pix582-remaining14-metadata',
      'profiles': [{'PROJECT': 'ROCKNIX', 'DEVICE': 'GENERIC_X64', 'ARCH': 'x86_64'}],
      'outputs': [{'path': str(a.owner / 'vm'), 'issue': 582, 'kind': 'qa-scratch',
                   'release_when': 'Original metadata and14 stage/family/watch channels exported and consumed, actual owners gone; retire disk/media/UEFI.'}]})
print(str(a.owner / 'admission-plan.json'))

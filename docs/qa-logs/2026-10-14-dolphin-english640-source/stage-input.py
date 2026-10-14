#!/usr/bin/env python3
"""UNRUN host preparation: new public input directory; no guest or product run.

The sealed fixture's stage-products operation renders complete recipe bytes.
No downloads, imports of fixtures, catalog builds, accounts, or real ROMs.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import shutil
import subprocess
import sys
import tarfile

HERE = Path(__file__).resolve().parent
PREFIX = 'docs/qa-logs/2026-10-13-dolphin-preservation-source/installed-flow/source-staged-v4/'


def require(ok, message):
    if not ok:
        raise RuntimeError(message)


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def git_bytes(repo, commit, name):
    return subprocess.run(['git','-C',str(repo),'show',commit + ':' + name], check=True, capture_output=True).stdout


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--repo', type=Path, required=True)
    parser.add_argument('--es-repo', type=Path, required=True)
    parser.add_argument('--input', type=Path, required=True, help='NEW public export root; guest mounts it at /tmp/pix-input read-only')
    parser.add_argument('--archive', type=Path, required=True)
    parser.add_argument('--receipt', type=Path, required=True)
    parser.add_argument('--allocation', type=Path, required=True)
    args = parser.parse_args()
    binding = json.loads((HERE / 'binding.json').read_text())
    allocation = json.loads(args.allocation.read_text())
    plan = subprocess.run([sys.executable, '-I', '-S', '-B', str(HERE / 'guest-batch.py'),
                           'plan', '--allocation', str(args.allocation)], capture_output=True, timeout=10, check=False)
    if plan.returncode != 0:
        sys.stderr.buffer.write(plan.stderr)
    require(plan.returncode == 0, 'selection planning refused; no staging or guest action performed')
    require(sha(args.archive) == binding['defaults_archive_sha256'], 'archive bytes mismatch')
    require(sha(args.receipt) == binding['defaults_receipt_sha256'], 'receipt bytes mismatch')
    require(allocation['renderer'] in ('Vulkan','OGL'), 'unsupported renderer')
    require(allocation['panel'] == [640,480], '640x480 allocation required')
    for name, expected in binding['es_boundary_reference_files'].items():
        require(hashlib.sha256(git_bytes(args.es_repo, allocation['es_source'], name)).hexdigest() == expected,
                'unreviewed ES boundary change: ' + name)
    require(not os.path.lexists(args.input), 'input root exists; never alter a staged allocation')
    args.input.mkdir(parents=False, mode=0o755)
    dolphin = args.input / 'dolphin'
    dolphin.mkdir()
    (dolphin / 'v4').mkdir()
    for name, digest in binding['v4_files'].items():
        data = git_bytes(args.repo, binding['fixture_commit'], PREFIX + name)
        require(hashlib.sha256(data).hexdigest() == digest, 'v4 source mismatch: ' + name)
        (dolphin / 'v4' / name).write_bytes(data)
    # Retain the exact sealed v4 export. The effective caller uses the same
    # executable bytes, with only source.json rebinding the display-only helper.
    (dolphin / 'caller').mkdir()
    for name, digest in binding['caller_files'].items():
        data = ((HERE / 'caller-source.json').read_bytes() if name == 'source.json'
                else (dolphin / 'v4' / name).read_bytes())
        require(hashlib.sha256(data).hexdigest() == digest, 'candidate caller bytes mismatch: ' + name)
        (dolphin / 'caller' / name).write_bytes(data)
    for name, digest in binding['distribution_files'].items():
        data = git_bytes(args.repo, binding['product_commit'], name)
        require(hashlib.sha256(data).hexdigest() == digest, 'distribution source mismatch: ' + name)
        target = dolphin / 'source' / name
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(data)
    (dolphin / 'batch').mkdir()
    names = [line.split('  ',1)[1] for line in (HERE / 'SHA256SUMS').read_text().splitlines()]
    for name in names + ['SHA256SUMS']:
        require(Path(name).name == name, 'unsafe packet name')
        shutil.copyfile(HERE / name, dolphin / 'batch' / name)
    shutil.copyfile(args.allocation, dolphin / 'allocation.json')
    (dolphin / 'selection-plan.stdout').write_bytes(plan.stdout)
    (dolphin / 'selection-plan.stderr').write_bytes(plan.stderr)
    (dolphin / 'selection-plan.exit').write_text(str(plan.returncode) + '\n')
    resources = dolphin / 'defaults'
    resources.mkdir()
    shutil.copyfile(args.receipt, resources / 'receipt.json')
    # Verified public archive, not firmware extraction. Preserve actual image
    # modes (including the 22 documented differences); reject links/specials.
    with tarfile.open(args.archive, 'r:gz') as archive:
        members = archive.getmembers()
        require(len(members) == 2735 and sum(m.size for m in members if m.isfile()) == 5821615,
                'unexpected defaults archive inventory')
        seen = set()
        for member in members:
            relative = PurePosixPath(member.name)
            require(not relative.is_absolute() and '..' not in relative.parts and relative.parts[0] == 'dolphin-emu', 'unsafe defaults member')
            require(member.isdir() or member.isfile(), 'non-regular defaults member')
            require(member.name not in seen, 'duplicate defaults member')
            seen.add(member.name)
            path = resources / member.name
            if member.isdir():
                path.mkdir(parents=True, exist_ok=True)
            else:
                path.parent.mkdir(parents=True, exist_ok=True)
                with archive.extractfile(member) as source, path.open('xb') as output:
                    shutil.copyfileobj(source, output)
            path.chmod(member.mode)
    argv = [sys.executable, '-I','-S','-B',str(dolphin / 'caller/installed_flow.py'),
            'stage-products','--repo',str(dolphin / 'source'),'--renderer',allocation['renderer'],
            '--output',str(dolphin / 'product')]
    result = subprocess.run(argv, check=False, capture_output=True)
    (dolphin / 'stage-products.stdout').write_bytes(result.stdout)
    (dolphin / 'stage-products.stderr').write_bytes(result.stderr)
    (dolphin / 'stage-products.exit').write_text(str(result.returncode) + '\n')
    require(result.returncode == 0, 'sealed recipe staging failed; retain original exits')
    (dolphin / 'stage-receipt.json').write_text(json.dumps({'status':'STAGED; NOT RUN',
        'fixture_commit':binding['fixture_commit'], 'product_commit':binding['product_commit'],
        'es_boundary_source':allocation['es_source'], 'es_boundary_files':binding['es_boundary_reference_files'],
        'defaults_archive_sha256':sha(args.archive), 'defaults_receipt_sha256':sha(args.receipt),
        'guest_mount':'/tmp/pix-input read-only', 'product_stage_original_exit':result.returncode}, indent=2) + '\n')
    print('STAGED ONLY: ' + str(dolphin))


if __name__ == '__main__':
    try:
        main()
    except Exception as exc:
        print('REFUSED: ' + str(exc), file=sys.stderr)
        sys.exit(1)

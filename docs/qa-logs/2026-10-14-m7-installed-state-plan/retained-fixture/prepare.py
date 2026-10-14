#!/usr/bin/env python3
"""Prepare four serial scripts from a frozen distribution and its final SYSTEM.

This host preparation reads SYSTEM through unsquashfs; it does not boot, seed,
run the guest fixture, start a service, update, reboot or publish anything.
"""
import argparse
import ast
import base64
import hashlib
import json
from pathlib import Path
import re
import subprocess
import tempfile

PREVIOUS_COMMIT = '1a026648442321609b2288c2c9c06803817f9df2'
PREVIOUS_ES_COMMIT = 'c8dc72cf9ec00ab00d6c4a9fcdcea1746c6f1f78'
PREVIOUS_ES_SHA = 'db136580f0a46442bb3fe7ac9e31606b38b816c78efc8f9b4e267284daca6502'


def digest(path):
    with Path(path).open('rb') as f:
        h = hashlib.sha256()
        for block in iter(lambda: f.read(1024 * 1024), b''):
            h.update(block)
        return h.hexdigest()


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--checkout', required=True, type=Path)
    p.add_argument('--system', required=True, type=Path)
    p.add_argument('--system-sha256', required=True)
    p.add_argument('--output', required=True, type=Path)
    p.add_argument('--id', required=True)
    a = p.parse_args()
    assert re.fullmatch('[a-z0-9][a-z0-9-]{0,47}', a.id)
    assert re.fullmatch('[0-9a-f]{64}', a.system_sha256)
    reviewed = json.loads(Path(__file__).with_name('source-bindings.json').read_text())['files']
    root = a.checkout.resolve(strict=True)
    system = a.system.resolve(strict=True)
    assert system.is_file() and not a.system.is_symlink()
    assert not a.output.exists()
    assert digest(system) == a.system_sha256
    def git(*args):
        return subprocess.check_output(['git', '-C', str(root), *args], text=True, timeout=10).strip()
    commit = git('rev-parse', 'HEAD')
    assert re.fullmatch('[0-9a-f]{40}', commit)
    assert not git('status', '--porcelain', '--untracked-files=no')
    recipe = (root / 'projects/ROCKNIX/packages/ui/emulationstation/package.mk').read_text()
    pin = re.findall(r'^PKG_VERSION="([0-9a-f]{40})"$', recipe, re.M)
    assert len(pin) == 1
    def installed(name, limit):
        # Bounded temporary stream: never print potential embedded developer data.
        with tempfile.TemporaryFile() as out:
            def bounded():
                import resource
                resource.setrlimit(resource.RLIMIT_FSIZE, (limit, limit))
            result = subprocess.run(['unsquashfs', '-processors', '1', '-mem', '64M',
                '-no-wildcards', '-cat', str(system), name], stdout=out,
                stderr=subprocess.DEVNULL, stdin=subprocess.DEVNULL, timeout=120,
                preexec_fn=bounded)
            assert result.returncode == 0 and out.tell() <= limit
            out.seek(0)
            return out.read(limit + 1)
    release = installed('etc/os-release', 16384).decode()
    assert re.findall(r'^BUILD_ID="([0-9a-f]{40})"$', release, re.M) == [commit]
    assert 'HW_DEVICE="GENERIC_X64"' in release and 'HW_ARCH="x86_64"' in release
    es = installed('usr/bin/emulationstation', 256 * 1024**2)
    assert es.startswith(b'\x7fELF')
    backup_path = 'projects/ROCKNIX/packages/rocknix/sources/scripts/backuptool'
    backup = (root / backup_path).read_bytes()
    assert installed('usr/bin/backuptool', 1024 * 1024) == backup
    gate = (root / 'tools/pixelelated-state-check').read_bytes()
    for name in ['tools/pixelelated-state-check', 'tools/vm-serial', backup_path]:
        assert digest(root / name) == reviewed[name]
    ast.parse(gate, feature_version=(3, 10))
    fixture = Path(__file__).with_name('guest-fixture.py').read_text()
    ast.parse(fixture, feature_version=(3, 10))
    config = {'id': a.id, 'candidate_commit': commit, 'candidate_es_commit': pin[0],
              'candidate_es_sha256': hashlib.sha256(es).hexdigest(),
              'candidate_system_sha256': a.system_sha256,
              'previous_commit': PREVIOUS_COMMIT, 'previous_es_commit': PREVIOUS_ES_COMMIT,
              'previous_es_sha256': PREVIOUS_ES_SHA,
              'backuptool_sha256': hashlib.sha256(backup).hexdigest(),
              'gate_sha256': hashlib.sha256(gate).hexdigest(),
              'gate_base64': base64.b64encode(gate).decode()}
    assert digest(system) == a.system_sha256 and git('rev-parse', 'HEAD') == commit
    assert not git('status', '--porcelain', '--untracked-files=no')
    a.output.mkdir(mode=0o700)
    for phase, seconds in {'seed': 300, 'before': 180, 'after': 180, 'backup': 420}.items():
        program = 'import json\nCONFIG = json.loads(' + repr(json.dumps(config)) + ')\nPHASE = ' + repr(phase) + '\n' + fixture
        ast.parse(program, feature_version=(3, 10))
        encoded = base64.b64encode(program.encode()).decode()
        script = ('#!/bin/sh\nset -u\ntimeout --signal=TERM --kill-after=10s ' + str(seconds) +
                  "s python3 -B -c 'import base64; exec(compile(base64.b64decode(\"" + encoded +
                  '\"), \"<installed-state-fixture>\", \"exec\"))' + "'\nrc=$?\nprintf 'PIX_INSTALLED_STATE_" +
                  phase.upper() + "_RC=%s\\n' \"$rc\"\nexit \"$rc\"\n")
        path = a.output / (phase + '.sh')
        path.write_text(script)
        path.chmod(0o500)
        subprocess.run(['sh', '-n', str(path)], check=True, timeout=10)
    # Public binding excludes the embedded checker; all identities refer to code/artifacts.
    binding = {k: v for k, v in config.items() if k != 'gate_base64'}
    binding.update({'vm_serial_sha256': digest(root / 'tools/vm-serial'),
                    'fixture_sha256': hashlib.sha256(fixture.encode()).hexdigest(),
                    'runtime_executed': False,
                    'scripts': {f.name: digest(f) for f in sorted(a.output.glob('*.sh'))}})
    (a.output / 'bindings.json').write_text(json.dumps(binding, indent=2) + '\n')
    print(json.dumps({'result': 'PREPARED_NOT_EXECUTED', 'candidate_commit': commit,
                      'candidate_es_commit': pin[0], 'output': str(a.output)}))


if __name__ == '__main__':
    main()

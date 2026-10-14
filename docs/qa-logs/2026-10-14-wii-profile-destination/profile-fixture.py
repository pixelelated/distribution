#!/usr/bin/env python3
"""UNRUN. Bounded no-NIC VM component check using installed stock profiles.

Executes only the verbatim profile-initialization block from the bound complete
launcher. This is not an emulator, actual caller, save, or gameplay proof.
Run alongside the new image's existing #581 native/installed checks.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path
import resource
import signal
import subprocess
import sys
import time

HERE = Path(__file__).resolve().parent
PROFILE_REL = 'projects/ROCKNIX/packages/emulators/standalone/dolphin-sa/config/controllers/WiiControllerProfiles'
START = '# Check if Wii controller dir exists in .config/dolphin-emu/WiiControllerProfiles\n'
END = '# Gamecube controller profile needed for hotkeys to work on SA\n'


def need(value, message):
    if not value:
        raise AssertionError(message)


def sha(data):
    return hashlib.sha256(data).hexdigest()


def inventory(root):
    return {str(p.relative_to(root)): sha(p.read_bytes())
            for p in sorted(root.rglob('*')) if p.is_file()}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--variant', choices=('baseline', 'candidate'), required=True)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--disposable-vm', action='store_true', required=True)
    args = parser.parse_args()
    need(os.environ.get('PIX581_PROFILE_VM') == 'allocated', 'coordinator VM allocation required')
    need({p.name for p in Path('/sys/class/net').iterdir()} == {'lo'}, 'no-NIC guest required')
    dmi = Path('/sys/class/dmi/id/product_name').read_text().lower()
    need(any(word in dmi for word in ('qemu', 'kvm', 'standard pc')), 'disposable QEMU VM required')
    out = args.output.absolute()
    need(out.parent.resolve() == Path('/run') and out.name.startswith('pix581-profile-'), 'fresh direct /run output required')
    need(not out.exists() and not out.is_symlink(), 'output already exists')
    binding = json.loads((HERE / 'bindings.json').read_text())
    for row in binding['source']:
        need(sha((HERE / 'source' / row['path']).read_bytes()) == row['sha256'], 'packet source changed: ' + row['path'])
    folder = 'source' if args.variant == 'baseline' else 'candidate'
    launcher = (HERE / folder / binding['path']).read_bytes()
    need(sha(launcher) == binding[args.variant + '_sha256'], 'launcher changed')
    text = launcher.decode()
    need(text.count(START) == text.count(END) == 1, 'initialization markers changed')
    block = text[text.index(START):text.index(END)]
    defaults = Path('/usr/config/dolphin-emu/WiiControllerProfiles')
    profile_hashes = {}
    for name in ('classic.ini', 'hremote.ini', 'nunchuck.ini', 'vremote.ini'):
        expected = (HERE / 'source' / PROFILE_REL / name).read_bytes()
        need((defaults / name).is_file(), 'installed profile absent: ' + name)
        need((defaults / name).read_bytes() == expected, 'installed profile changed: ' + name)
        profile_hashes[name] = sha(expected)
    installed = Path('/usr/bin/start_dolphin_wii.sh').read_bytes()
    candidate = (HERE / 'candidate' / binding['path']).read_bytes()
    rendered = (candidate.replace(b'@GRENDERER@', b'OGL')
                .replace(b'@DOLPHIN_BACKEND@', b'wayland')
                .replace(b'@EXPORTS@', b'export QT_QPA_PLATFORM=wayland'))
    need(installed == rendered, 'installed GENERIC_X64 launcher differs from complete corrected recipe bytes')
    helper_rel = 'projects/ROCKNIX/packages/emulators/standalone/dolphin-sa/scripts/dolphin-save-paths'
    helper = Path('/usr/bin/dolphin-save-paths').read_bytes()
    need(helper == (HERE / 'source' / helper_rel).read_bytes(), 'installed preservation helper changed')
    resource.setrlimit(resource.RLIMIT_AS, (256 * 1024**2,) * 2)
    resource.setrlimit(resource.RLIMIT_CPU, (15, 20))
    resource.setrlimit(resource.RLIMIT_FSIZE, (4 * 1024**2,) * 2)
    signal.signal(signal.SIGALRM, lambda *_: (_ for _ in ()).throw(TimeoutError('45-second deadline')))
    signal.alarm(45)
    out.mkdir(mode=0o700)
    report = {'status': 'FAIL', 'runtime_scope': 'verbatim initialization block with installed defaults',
              'variant': args.variant, 'launcher_sha256': sha(launcher),
              'block_sha256': sha(block.encode()), 'installed_launcher_sha256': sha(installed),
              'installed_helper_sha256': sha(helper), 'installed_profiles': profile_hashes,
              'cases': [], 'emulator_launched': False, 'actual_caller_executed': False}
    (out / 'executed-block.sh').write_text(block)
    started = time.monotonic()
    try:
        cases = ('retained-missing',) if args.variant == 'baseline' else (
            'retained-missing', 'retained-custom', 'stock-without-custom')
        for case in cases:
            case_root = out / case
            conf = case_root / 'dolphin-emu'
            conf.mkdir(parents=True)
            (conf / 'Dolphin.ini').write_text('[Core]\nFixtureRetained = True\n')
            if case != 'retained-missing':
                (conf / 'WiiControllerProfiles').mkdir()
                for name in profile_hashes:
                    (conf / 'WiiControllerProfiles' / name).write_bytes((defaults / name).read_bytes())
                if case == 'retained-custom':
                    (conf / 'WiiControllerProfiles/custom.ini').write_bytes(b'[Wiimote1]\nFixtureCustom = retained\n')
            before = inventory(conf)
            result = subprocess.run(['/bin/bash', '-c', 'CONF_DIR="$1"\n' + block,
                                     'bound-profile-initialization', str(conf)],
                                    env={'PATH': '/usr/bin:/bin', 'LC_ALL': 'C'},
                                    capture_output=True, timeout=10)
            (case_root / 'stdout').write_bytes(result.stdout)
            (case_root / 'stderr').write_bytes(result.stderr)
            after = inventory(conf)
            row = {'case': case, 'original_shell_exit': result.returncode,
                   'before': before, 'after': after}
            report['cases'].append(row)
            need(all(after.get(path) == digest for path, digest in before.items()), 'retained bytes changed')
            if args.variant == 'baseline':
                need(result.returncode != 0, 'baseline did not fail')
                need(not (conf / 'WiiControllerProfiles').exists(), 'baseline unexpectedly initialized intended directory')
                need(b'WiiControllerProfiles/vremote.ini' in result.stderr, 'baseline failure has a different cause')
                report['causal_reproduced'] = True
                report['original_failure_retained'] = True
                return 1
            need(result.returncode == 0, 'candidate shell failed')
            need(not result.stderr, 'candidate emitted diagnostics')
            need(not (conf / 'dolphin-emu').exists(), 'extra nested dolphin-emu directory created')
            for name, digest in profile_hashes.items():
                need(after.get('WiiControllerProfiles/' + name) == digest, 'stock profile missing or changed')
            custom = after.get('WiiControllerProfiles/custom.ini')
            expected_custom = before.get('WiiControllerProfiles/custom.ini', profile_hashes['vremote.ini'])
            need(custom == expected_custom, 'custom profile created incorrectly or overwritten')
        report['status'] = 'PASS'
        return 0
    except BaseException as error:
        report['error'] = repr(error)
        raise
    finally:
        report['elapsed_seconds'] = time.monotonic() - started
        (out / 'result.json').write_text(json.dumps(report, indent=2) + '\n')


if __name__ == '__main__':
    sys.exit(main())

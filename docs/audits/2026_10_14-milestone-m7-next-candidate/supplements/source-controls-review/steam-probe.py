#!/usr/bin/python3
"""#595: two bounded VM-only exact-function import-isolation controls."""
import argparse
import hashlib
import io
import json
import os
from pathlib import Path
import resource
import signal
import subprocess
import tarfile
import time

HERE = Path(__file__).resolve().parent


def digest(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def limits():
    resource.setrlimit(resource.RLIMIT_AS, (256 * 1024**2,) * 2)
    # The unchanged product downloader sets both limits to MAX_ARCHIVE. Keep
    # that hard ceiling available; the fixture transport copies only our tiny
    # sealed archive, and each parent command still has a 30-second deadline.
    resource.setrlimit(resource.RLIMIT_FSIZE, (8 * 1024**2, 2 * 1024**3))
    resource.setrlimit(resource.RLIMIT_CPU, (20, 20))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--out', type=Path, required=True)
    args = parser.parse_args()
    assert Path('/etc/os-release').read_text().find('pixelelated') >= 0
    assert sorted(p.name for p in Path('/sys/class/net').iterdir()) == ['lo']
    assert args.out.parent == Path('/run') and args.out.name.startswith('pix595-') and not args.out.exists()
    args.out.mkdir(parents=True)
    binding = json.loads((HERE / 'bindings.json').read_text())
    results = []
    runtime = 'steam-runtime-steamrt-arm64'
    for role in ('baseline', 'candidate'):
        source = HERE / (role + '-function.sh')
        assert digest(source) == next(r['function_sha256'] for r in binding['versions'] if r['role'] == role)
        case = args.out / role
        case.mkdir()
        root = case / 'steam'
        root.mkdir()
        cwd = case / 'cwd'
        cwd.mkdir()
        extra = case / 'pythonpath'
        extra.mkdir()
        tools = case / 'tools'
        tools.mkdir()
        poison = "from pathlib import Path\nPath('poison-ran').write_text('fixture-only import')\nraise SystemExit(91)\n"
        (cwd / 'ctypes.py').write_text(poison)
        (extra / 'ctypes.py').write_text(poison)
        (extra / 'sitecustomize.py').write_text(poison)
        payload = case / 'runtime.tar.xz'
        libraries = {}
        with tarfile.open(payload, 'w:xz') as archive:
            for name in ('libibus-1.0.so.5', 'libva.so.2'):
                relative = runtime + '/steamrt3c_platform_fixture/files/lib/aarch64-linux-gnu/' + name + '.fixture'
                data = b'\x7fELF\x02\x01' + b'\0' * 10 + b'\x03\x00\xb7\x00' + b'fixture-only never executable'
                item = tarfile.TarInfo(relative)
                item.size = len(data)
                item.mode = 0o644
                archive.addfile(item, io.BytesIO(data))
                libraries[name] = {'relative': relative, 'sha256': hashlib.sha256(data).hexdigest()}
        (tools / 'curl').write_text('#!/bin/sh\nprintf "curl\\n" >> "$PIX_CALLS"\nprintf "fixture-v1\\n"\n')
        (tools / 'wget').write_text('#!/bin/sh\nprintf "wget\\n" >> "$PIX_CALLS"\nwhile [ "$#" -gt 0 ]; do\n if [ "$1" = -O ]; then shift; exec /usr/bin/cp -- "$PIX_ARCHIVE" "$1"; fi\n shift\ndone\nexit 90\n')
        for tool in tools.iterdir():
            tool.chmod(0o755)
        driver = case / 'driver.sh'
        driver.write_text('log_info() { :; }\ndie() { printf "%s\\n" "$*" >&2; exit 1; }\n' + source.read_text() + '\ninstall_steam_runtime_arm64\n')
        env = {'PATH': str(tools) + ':/usr/bin:/bin', 'HOME': str(case), 'LANG': 'C',
               'PYTHONPATH': str(extra), 'STEAM': str(root), 'RUNTIME_TAR_VERSION_URL': 'https://fixture.invalid/version',
               'RUNTIME_TAR_BASE': 'https://fixture.invalid', 'PIX_ARCHIVE': str(payload), 'PIX_CALLS': str(case / 'transport.calls')}
        before = {str(p.relative_to(case)): digest(p) for p in case.rglob('*') if p.is_file()}
        start = time.monotonic()
        with (case / 'stdout').open('xb') as out, (case / 'stderr').open('xb') as err:
            child = subprocess.Popen(['/bin/bash', str(driver)], cwd=cwd, env=env, stdout=out, stderr=err,
                                     start_new_session=True, preexec_fn=limits)
            timed_out = False
            try:
                rc = child.wait(timeout=30)
            except subprocess.TimeoutExpired:
                timed_out = True
                os.killpg(child.pid, signal.SIGKILL)
                rc = child.wait(timeout=3)
        survivors = []
        for proc in Path('/proc').iterdir():
            if not proc.name.isdigit():
                continue
            try:
                fields = (proc / 'stat').read_text().rsplit(')', 1)[1].split()
                if int(fields[2]) == child.pid and fields[0] != 'Z':
                    survivors.append(int(proc.name))
            except FileNotFoundError:
                pass
        row = {'role': role, 'original_function_rc': rc, 'timed_out': timed_out,
               'remaining_process_group': survivors,
               'seconds': time.monotonic() - start, 'installed_python_sha256': digest(Path('/usr/bin/python3').resolve()),
               'function_sha256': digest(source), 'embedded_python_sha256': binding['versions'][0]['embedded_python_sha256'],
               'transport_calls': (case / 'transport.calls').read_text().splitlines() if (case / 'transport.calls').exists() else [],
               'poison_executed': (cwd / 'poison-ran').exists(), 'synthetic_libraries_never_executed': True}
        (case / 'command-result.json').write_text(json.dumps(row, indent=2) + '\n')
        assert not timed_out and not survivors
        for name, sha in before.items():
            assert digest(case / name) == sha, name
        if role == 'baseline':
            assert rc == 1 and row['poison_executed'] and row['transport_calls'] == []
            assert not list(root.iterdir())
        else:
            assert rc == 0 and not row['poison_executed'] and row['transport_calls'] == ['curl', 'wget']
            assert not list(case.rglob('__pycache__'))
            assert not (root / '.steam-runtime-update').exists()
            for name, data in libraries.items():
                installed = root / data['relative']
                assert digest(installed) == data['sha256']
                link = root / 'lib/aarch64-linux-gnu' / name
                assert link.is_symlink() and link.resolve() == installed
        results.append(row)
    (args.out / 'result.json').write_text(json.dumps({'passed': True, 'cases': results,
        'scope': 'exact extracted runtime function and installed interpreter; synthetic transports/archive, no client or native ARM execution'}, indent=2) + '\n')
    print('PASS #595: baseline import shadow reproduced; isolated complete runtime function succeeds.')


if __name__ == '__main__':
    main()

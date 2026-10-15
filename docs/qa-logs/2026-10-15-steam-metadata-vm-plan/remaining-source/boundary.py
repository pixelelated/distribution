#!/usr/bin/python3 -B
"""Prepared synthetic transport/engine boundaries; never accesses a provider."""
import hashlib
import json
import os
from pathlib import Path
import shutil
import socket
import subprocess
import sys
import time

sys.path.insert(0, '/qa')
import payload


from event_records import event


def main(command, args):
    case = json.loads(Path('/qa/case.json').read_text())
    assert case == {'name': case['name'], 'physical_root': str(payload.case_root(case['name'])), 'steam': str(payload.STEAM)}
    physical = payload.case_root(case['name'])
    assert payload.STEAM.resolve(strict=True) == physical
    attempt = json.loads(Path('/qa/attempt.json').read_text())['attempt']
    if command == 'exec-allowed':
        assert not args
        return 17
    if command == 'exec-many-syscalls':
        assert not args
        for _ in range(2000):
            assert os.getpid() > 0
        return 19
    if command == 'exec-blocked':
        assert not args
        event({'kind': 'guard-control-ready', 'point': 'blocked-wait'})
        time.sleep(600)
        raise RuntimeError('Exec guard deadline did not fire')
    if command == 'exec-denial':
        assert not args
        try:
            os.execv('/qa/guard-should-not-run', ['/qa/guard-should-not-run'])
        except PermissionError as error:
            assert error.errno == 13
            return 77
        raise RuntimeError('Exec denial did not happen')
    if command == 'profile':
        assert not args
        payload.put(Path('/storage/profile-ran'), 'profile effects are outside the client transaction\n')
        return
    if command == 'set_kill':
        assert args == ['set', '-9 steam FEX']
        payload.put(Path('/tmp/.process-kill-data'), '-9 steam FEX\n')
        return
    if command == 'FEXRootFSFetcher':
        assert args == ['--distro-name=arch', '--distro-version=rolling', '-y', '-x', '--force-ui=tty']
        work = Path('/storage/.local/share/fex-emu/.steam-fex-update')
        for key, suffix in (('FEX_APP_DATA_LOCATION', 'data'), ('FEX_APP_CONFIG_LOCATION', 'fetch-config'),
                            ('FEX_APP_CACHE_LOCATION', 'cache')):
            assert os.environ[key] == str(work / suffix) + '/'
        assert Path.cwd() == work / 'home' and os.environ['HOME'] == str(work / 'home')
        assert not (Path(os.environ['HOME']) / '.fex-emu').exists()
        assert 'FEX_APP_CONFIG' not in os.environ and 'STEAM_COMPAT_DATA_PATH' not in os.environ
        # Simulate only the fetcher's extracted-tree/config contract. No sqsh/EROFS extraction.
        payload.fex_tree(work / 'data/RootFS/ArchLinux', 'new-fex')
        payload.put(work / 'fetch-config/Config.json', '{"Config":{"RootFS":"ArchLinux"}}')
        return
    if command == 'curl':
        url = args[-1]
        if url == 'https://repo.steampowered.com/steamrt3c/images/latest-public-stable.txt':
            assert args[:-1] == ['-fsSL', '--connect-timeout', '10', '--max-time', '30', '--max-filesize', '128']
            print('qa-20261013')
        elif url.startswith('https://client-update.'):
            assert case['name'] not in payload.EXISTING and case['name'] not in payload.EARLY
            bad = case['name'] in ('crc-failure-retry', 'validation-failure-retry') and attempt == 1
            expected = json.loads(Path('/qa/client-' + ('bad' if bad else 'good') + '.json').read_text())
            manifest_url = 'https://client-update.fastly.steamstatic.com/steam_client_publicbeta_linuxarm64'
            seconds = '30' if url == manifest_url else '180'
            limit = str(2 * 1024**2) if url == manifest_url else str(expected['size'])
            assert args[:-1] == ['--disable', '--fail', '--silent', '--show-error', '--location',
                '--proto', '=https', '--proto-redir', '=https', '--max-redirs', '5',
                '--connect-timeout', '10', '--max-time', seconds, '--max-filesize', limit, '--output', '-']
            if url == manifest_url:
                print('"linuxarm64" { "version" "1" "bins_linuxarm64_linuxarm64" { "file" "' +
                      expected['filename'] + '" "size" "' + str(expected['size']) + '" "sha2" "' +
                      expected['sha256'] + '" "zipvz" "bins_linuxarm64_linuxarm64.zip.vz.decoy" } }')
            else:
                assert url == 'https://client-update.steamstatic.com/' + expected['filename']
                source = Path('/qa/payloads/client-' + ('bad' if bad else 'good') + '.zip')
                raw = source.read_bytes()
                assert len(raw) == expected['size'] and hashlib.sha256(raw).hexdigest() == expected['sha256']
                if case['name'] in ('transport-timeout', 'detached-transfer-child', 'proc-census-error'):
                    held = os.dup(sys.stdout.fileno())
                    try:
                        child = subprocess.Popen([sys.executable, '-I', '-S', '-B', '/qa/transfer-child.py',
                            str(held), case['name'], str(attempt)], pass_fds=(held,),
                            stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                    finally:
                        os.close(held)
                    ready = Path('/qa/detached-child-ready-1.json')
                    deadline = time.monotonic() + 5
                    while not ready.exists():
                        assert child.poll() is None and time.monotonic() < deadline, 'Detached child readiness failed'
                        time.sleep(0.01)
                    child_info = json.loads(ready.read_text())
                    assert child_info['pid'] == child.pid and child_info['case'] == case['name']
                    event({'kind': 'fault', 'point': 'detached-transfer-child', 'child_pid': child.pid,
                           'child_start_ticks': child_info['start_ticks'], 'attempt': attempt})
                    if case['name'] == 'transport-timeout':
                        time.sleep(600)
                        raise RuntimeError('Transport timeout did not happen')
                if case['name'] == 'download-failure-retry' and attempt == 1:
                    sys.stdout.buffer.write(raw[:len(raw)//2]);sys.stdout.buffer.flush()
                    event({'kind': 'fault', 'point': 'partial-transport', 'original_exit': 23, 'attempt': attempt})
                    return 23
                sys.stdout.buffer.write(raw);sys.stdout.buffer.flush()
                event({'kind': 'archive-copy', 'name': 'client.zip', 'sha256': expected['sha256'], 'attempt': attempt})
        else:
            assert args[:-1] == ['-fsSL']
            releases = {
                'https://api.github.com/repos/CachyOS/proton-cachyos/releases/latest': ('cachyos-qa', payload.CACHY + '.tar.xz'),
                'https://api.github.com/repos/GloriousEggroll/proton-ge-custom/releases/latest': ('qa', payload.GE + '.tar.gz'),
            }
            tag, name = releases[url]
            print(json.dumps({'tag_name': tag, 'assets': [{'browser_download_url': 'https://synthetic.invalid/' + name}]}))
        return
    if command == 'wget':
        assert args[:5] == ['-t', '3', '-T', '30', '-O'] and len(args) == 7
        dest, url = Path(args[5]), args[6]
        paths = {
            'https://repo.steampowered.com/steamrt3c/images/qa-20261013/' + payload.RUNTIME + '.tar.xz':
                ('runtime.tar.xz', physical / '.steam-runtime-update/runtime.tar.xz'),
            'https://synthetic.invalid/' + payload.CACHY + '.tar.xz':
                ('cachy.tar.xz', physical / '.proton-variant-stage/archive'),
            'https://synthetic.invalid/' + payload.GE + '.tar.gz':
                ('ge.tar.gz', physical / '.proton-variant-stage/archive'),
        }
        name, expected = paths[url]
        assert dest == expected and dest.parent.resolve(strict=True).is_relative_to(physical)
        assert not dest.exists() and not dest.is_symlink()
        source = Path('/qa/payloads') / name
        assert 0 < source.stat().st_size <= 1024**2
        shutil.copyfile(source, dest)
        event({'kind': 'archive-copy', 'name': name, 'sha256': hashlib.sha256(source.read_bytes()).hexdigest()})
        return
    if command == 'unzip':
        raise RuntimeError('Candidate unexpectedly used the old unzip path')
    if command == 'systemctl':
        assert args == ['restart', 'systemd-binfmt']
        return  # No service manager socket or operation.
    if command == 'swaymsg':
        raise RuntimeError('dual-screen branch is outside this one-case allocation')
    raise RuntimeError('unapproved boundary command: ' + command)


if __name__ == '__main__':
    sys.addaudithook(lambda e, a: (_ for _ in ()).throw(RuntimeError('network denied')) if e.startswith('socket.') else None)
    try:
        socket.socket()
    except RuntimeError:
        pass
    else:
        raise RuntimeError('network audit guard did not refuse')
    command, args = sys.argv[1], sys.argv[2:]
    code = 90
    try:
        result = main(command, args)
        code = 0 if result is None else result
    except BaseException as error:
        print('Synthetic boundary refused: ' + repr(error), file=sys.stderr)
    finally:
        event({'kind': 'boundary-exit', 'command': command, 'argv': args, 'original_exit': code})
    sys.exit(code)

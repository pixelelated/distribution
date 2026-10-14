#!/usr/bin/env python3
"""Read the completed engineering artifacts; no mount, VM, firmware execution or publication."""
import argparse
import gzip
import hashlib
import importlib.machinery
import importlib.util
import json
import os
from pathlib import Path, PurePosixPath
import resource
import stat
import struct
import subprocess
import sys
import tarfile
import time
import zlib

MAX_DISK = 16 * 1024**3
MAX_SYSTEM = 4 * 1024**3
MAX_KERNEL = 128 * 1024**2


def digest(path):
    h = hashlib.sha256()
    with path.open('rb') as f:
        for block in iter(lambda: f.read(4 * 1024**2), b''):
            h.update(block)
    return h.hexdigest()


def record(path, data):
    with path.open('x') as f:
        json.dump(data, f, indent=2); f.write('\n')


def git(tree, *args):
    return subprocess.check_output(['git', '-C', str(tree), *args], text=True, timeout=30).strip()


def process_gone(receipt):
    p = Path('/proc') / str(receipt['pid']) / 'stat'
    try:
        fields = p.read_text().rsplit(')', 1)[1].split()
    except FileNotFoundError:
        return True
    return fields[0] == 'Z' or fields[19] != str(receipt['start_ticks'])


def copy_bounded(src, target, ceiling):
    count = 0
    with target.open('xb') as out:
        while block := src.read(4 * 1024**2):
            count += len(block)
            assert count <= ceiling, 'payload exceeds declared ceiling'
            out.write(block)
    return count


def gpt(raw):
    size = raw.stat().st_size
    assert size % 512 == 0
    with raw.open('rb') as f:
        def header(lba):
            assert 0 < lba < size // 512
            f.seek(lba * 512); h = bytearray(f.read(512))
            assert h[:8] == b'EFI PART'
            length, expected = struct.unpack_from('<II', h, 12)
            assert 92 <= length <= 512
            h[16:20] = b'\0' * 4
            assert zlib.crc32(h[:length]) == expected
            current, backup = struct.unpack_from('<QQ', h, 24)
            assert current == lba
            entry_lba = struct.unpack_from('<Q', h, 72)[0]
            count, width, table_crc = struct.unpack_from('<III', h, 80)
            assert 0 < count <= 4096 and 128 <= width <= 1024
            assert count * width <= 1024**2
            assert 0 < entry_lba * 512 < size and entry_lba * 512 + count * width <= size
            f.seek(entry_lba * 512); table = f.read(count * width)
            assert len(table) == count * width and zlib.crc32(table) == table_crc
            return backup, table, width
        backup, table, width = header(1)
        assert backup == size // 512 - 1
        back, mirror, mirror_width = header(backup)
        assert back == 1 and mirror == table and mirror_width == width
        parts = []
        for offset in range(0, len(table), width):
            row = table[offset:offset + width]
            if row[:16] == bytes(16):
                continue
            first, last = struct.unpack_from('<QQ', row, 32)
            assert 1 < first <= last < backup
            parts.append((first, last))
        assert len(parts) == 2 and parts[0][0] == 8192
        assert parts[0][1] < parts[1][0]
        return parts


def link_chain(fs, path):
    pending = list(PurePosixPath(path).parts[1:]); done = []; links = []
    while pending:
        part = pending.pop(0)
        if part in ('', '.'):
            continue
        if part == '..':
            assert done, 'link escapes image root'
            done.pop(); continue
        candidate = '/' + '/'.join(done + [part])
        target = fs.link(candidate)
        if target is not None:
            links.append({'path': candidate, 'target': target})
            assert len(links) <= 40
            target_path = PurePosixPath(target)
            if target_path.is_absolute():
                done = []; pending = list(target_path.parts[1:]) + pending
            else:
                pending = list(target_path.parts) + pending
        else:
            done.append(part)
    return {'resolved': '/' + '/'.join(done), 'links': links}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--build-owner', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    a = parser.parse_args()
    owner = a.build_owner.resolve(strict=True)
    out = a.output.resolve(strict=True)
    assert out.is_dir() and not any(out.iterdir()), 'fresh empty result directory required'
    cfg = json.loads((owner / 'build-inputs.json').read_text())
    tree = Path(cfg['checkout']).resolve(strict=True)
    assert git(tree, 'rev-parse', 'HEAD') == cfg['commit']
    assert not git(tree, 'status', '--porcelain')
    branch = git(tree, 'branch', '--show-current')
    assert branch.startswith('build/')
    result = json.loads((owner / 'owner-result.json').read_text())
    assert result['status'] == 'PASS' and not any(result['surviving_host_command_groups'].values())
    assert json.loads((owner / 'resource-result.json').read_text())['status'] == 'PASS'
    assert json.loads((owner / 'launcher-result.json').read_text())['runner_returncode'] == 0
    assert (owner / 'tool-wrapper.rc').read_text().strip() == '0'
    active = Path((owner / 'run.path').read_text().strip())
    runner = json.loads((active / 'runner-result.json').read_text())
    assert runner['command_rc'] == runner['monitor_rc'] == runner['runner_rc'] == 0
    assert process_gone(json.loads((owner / 'owner-start.json').read_text()))
    assert process_gone(json.loads((owner / 'launcher-start.json').read_text()))
    consumed = json.loads((active / 'admission-consumed.json').read_text())
    assert consumed['state'] == 'consumed' and consumed['source']['head'] == cfg['commit']
    assert consumed['submission_owner'] == str(owner) and consumed['run'] == str(active)
    assert consumed['original_result'] == runner
    for entry in result['stages']:
        assert entry['original_host_make_rc'] == 0 and entry['observation_handshake']
        stage = owner / 'stages' / entry['stage']
        inner = json.loads((stage / 'inner-result.json').read_text())
        assert inner['original_command_rc'] == inner['wrapper_rc'] == 0
        cid = (stage / 'container.cid').read_text().strip()
        check = subprocess.run(['docker', 'inspect', cid], capture_output=True, text=True, timeout=15)
        assert check.returncode != 0 and 'no such' in check.stderr.casefold(), 'build container still present or inspection failed'
    identity_files = list((tree / 'target').glob('*.identity.json'))
    assert len(identity_files) == 1, 'ambiguous engineering output'
    identity_file = identity_files[0]
    meta = json.loads(identity_file.read_text())
    assert meta['schema'] == 1 and meta['name'] == 'pixelelated'
    assert meta['device'] == 'GENERIC_X64' and meta['arch'] == 'x86_64'
    assert meta['build_commit'] == cfg['commit'] and meta['dirty'] == 'no'
    assert meta['release_version'] == '0.0.1-dev' and meta['build_timestamp'] == cfg['build_timestamp']
    assert meta['build_version'] == '0.0.1-dev+' + cfg['build_timestamp'] + '.g' + cfg['commit'][:12]
    name = meta['image_name']; assert Path(name).name == name
    assert identity_file.name == name + '.identity.json'
    image, update = [tree / 'target' / (name + suffix) for suffix in ('.img.gz', '.tar')]
    files = [identity_file, image, update]
    for f in files:
        assert f.is_file() and not f.is_symlink()
    before = {str(f): {'bytes': f.stat().st_size, 'sha256': digest(f)} for f in files}
    record(out / 'inputs.json', {'schema': 1, 'build_inputs_sha256': digest(owner / 'build-inputs.json'),
                              'source': cfg['commit'], 'branch': branch, 'es_commit': cfg['es_commit'],
                              'identity': meta, 'artifacts': before, 'utc_epoch': time.time()})
    raw = out / 'candidate.img'
    with gzip.open(image, 'rb') as f:
        copy_bounded(f, raw, MAX_DISK)
    parts = gpt(raw)
    mcopy = tree / cfg['build_root'] / 'toolchain/bin/mcopy'
    assert mcopy.is_file()
    payload = {}
    with tarfile.open(update, 'r:') as archive:
        members = archive.getmembers()
        assert 0 < len(members) < 100000
        seen = set()
        for member in members:
            path = PurePosixPath(member.name)
            assert not path.is_absolute() and '..' not in path.parts
            assert str(path) not in seen and (member.isdir() or member.isfile())
            seen.add(str(path)); assert path.parts[0] == name
        for part, ceiling in [('SYSTEM', MAX_SYSTEM), ('KERNEL', MAX_KERNEL)]:
            target = out / part
            def bounded_reader():
                resource.setrlimit(resource.RLIMIT_FSIZE, (ceiling, ceiling))
            subprocess.run([str(mcopy), '-n', '-i', str(raw) + '@@' + str(parts[0][0] * 512),
                            '::/' + part, str(target)], check=True, timeout=180,
                           stdout=subprocess.DEVNULL, stderr=subprocess.PIPE, preexec_fn=bounded_reader)
            assert 0 < target.stat().st_size <= ceiling
            member = archive.getmember(name + '/target/' + part)
            assert member.isfile() and member.size == target.stat().st_size
            h = hashlib.sha256()
            with archive.extractfile(member) as stream:
                for block in iter(lambda: stream.read(4 * 1024**2), b''):
                    h.update(block)
            assert digest(target) == h.hexdigest(), part + ' update/install mismatch'
            payload[part] = {'bytes': target.stat().st_size, 'sha256': h.hexdigest()}
    # GENERIC_X64's actual install-image boot configuration is a separate
    # binder input; it is not inferred from current source or a previous guest.
    boot_config = out / 'syslinux.cfg'
    def bounded_boot_reader():
        resource.setrlimit(resource.RLIMIT_FSIZE, (64 * 1024, 64 * 1024))
    subprocess.run([str(mcopy), '-n', '-i', str(raw) + '@@' + str(parts[0][0] * 512),
                    '::/syslinux.cfg', str(boot_config)], check=True, timeout=30,
                   stdout=subprocess.DEVNULL, stderr=subprocess.PIPE, preexec_fn=bounded_boot_reader)
    assert 0 < boot_config.stat().st_size <= 64 * 1024
    payload['syslinux.cfg'] = {'bytes': boot_config.stat().st_size, 'sha256': digest(boot_config)}
    checker = tree / 'tools/pixelelated-state-check'
    assert digest(checker) == 'a0b03f17ed8493ec79a3dc33eefedeb7a00b20e06a70804b7653ee9f660e30a8'
    loader = importlib.machinery.SourceFileLoader('selected_state_reader', str(checker))
    spec = importlib.util.spec_from_loader(loader.name, loader)
    mod = importlib.util.module_from_spec(spec); loader.exec_module(mod)
    installed = mod.Local(tree / cfg['build_root'] / 'image/system')
    squash = mod.Squash(out / 'SYSTEM')
    paths = (tree / 'docs/qa-logs/2026-10-14-m7-installed-state-plan/installed-product-paths.txt').read_text().splitlines()
    # These changed script mappings are actual package copies. Only the two
    # Dolphin launchers receive the recorded GENERIC_X64 post-install substitutions.
    source_mappings = {
        'usr/bin/cloud_oauth': 'projects/ROCKNIX/packages/network/rclone/sources/cloud_oauth',
        'usr/bin/raofflineproxy-ctl': 'projects/ROCKNIX/packages/network/raofflineproxy/sources/raofflineproxy-ctl',
        'usr/bin/runemu.sh': 'projects/ROCKNIX/packages/rocknix/sources/scripts/runemu.sh',
        'usr/bin/wifictl': 'projects/ROCKNIX/packages/rocknix/sources/scripts/wifictl',
    }
    for name in ['start_dolphin_gc.sh', 'start_dolphin_wii.sh', 'cheevos_dolphin.sh', 'dolphin-save-paths']:
        source_mappings['usr/bin/' + name] = 'projects/ROCKNIX/packages/emulators/standalone/dolphin-sa/scripts/' + name
    paths.extend(source_mappings)
    paths.extend(['etc/profile', 'etc/profile.d/001-functions', 'usr/bin/python3',
                  'usr/lib/autostart/daemons/006-raofflineproxy', 'usr/bin/systemctl',
                  'usr/lib/systemd/systemd', 'usr/lib/libzstd.so.1',
                  'usr/lib/libcrypto.so.3', 'usr/lib/libsystemd.so.0',
                  'usr/bin/cloud-signin-window', 'usr/bin/rclone',
                  'usr/bin/gst-inspect-1.0', 'usr/lib/gstreamer-1.0/gst-plugin-scanner',
                  'usr/lib/gstreamer-1.0/libgstopengl.so',
                  'usr/lib/libgstcontroller-1.0.so.0', 'usr/lib/libgstreamer-1.0.so.0',
                  'usr/config/locale/fr/LC_MESSAGES/emulationstation2.mo',
                  'usr/config/locale/en_GB/LC_MESSAGES/emulationstation2.mo'])
    for target, source in source_mappings.items():
        expected = (tree / source).read_bytes()
        if Path(target).name in ['start_dolphin_gc.sh', 'start_dolphin_wii.sh']:
            expected = expected.replace(b'@DOLPHIN_BACKEND@', b'wayland').replace(b'@GRENDERER@', b'OGL').replace(b'@EXPORTS@', b'export QT_QPA_PLATFORM=wayland')
        assert installed.read('/' + target) == expected, target + ' frozen source/install mismatch'
    root = tree / cfg['build_root'] / 'image/system'
    for folder in ['usr/lib/python3.14/site-packages/raofflineproxy', 'usr/config/dolphin-emu/GamecubeControllerProfiles', 'usr/config/dolphin-emu/WiiControllerProfiles']:
        base = root / folder
        assert base.is_dir(), folder
        local_names = {str(f.relative_to(root)) for f in base.rglob('*') if f.is_file() and not f.is_symlink()}
        image_names = {name.lstrip('/') for name, (mode, target) in squash.nodes.items()
                       if name.startswith('/' + folder + '/') and mode[0] == '-'}
        assert local_names and local_names == image_names, folder + ' final path-set mismatch'
        paths.extend(sorted(local_names))
    assert not list((root / 'usr/lib/python3.14/site-packages/raofflineproxy').rglob('*.py'))
    products = {}
    for name in sorted(set(paths)):
        path = '/' + name
        left, right = installed.read(path, limit=256 * 1024**2), squash.read(path, limit=256 * 1024**2)
        assert left == right, name + ' final install/SYSTEM mismatch'
        local_links, image_links = link_chain(installed, path), link_chain(squash, path)
        assert local_links == image_links, name + ' installed/SYSTEM link-chain mismatch'
        mode = stat.filemode(installed.resolve(path).stat().st_mode)
        assert mode == squash.nodes[squash.resolve(path)][0], name + ' installed/SYSTEM mode mismatch'
        products[name] = {'bytes': len(left), 'sha256': hashlib.sha256(left).hexdigest(), 'mode': mode, 'link_chain': image_links}
    os_release = squash.read('/etc/os-release').decode()
    fields = {k: v.strip('"') for k,v in (line.split('=',1) for line in os_release.splitlines() if '=' in line)}
    assert fields['BUILD_ID'] == cfg['commit'] and fields['BUILD_VERSION'] == meta['build_version']
    assert fields['BUILD_BRANCH'] == branch and fields['BUILD_DIRTY'] == 'no'
    for f in files:
        assert digest(f) == before[str(f)]['sha256'] and f.stat().st_size == before[str(f)]['bytes']
    record(out / 'result.json', {'status': 'PASS', 'scope': 'completed-source/artifact/GPT/raw-update equality/selected installed mappings',
                              'runtime_qualified': False, 'payload': payload, 'products': products,
                              'partition_sectors': parts, 'source': cfg['commit'], 'es_commit': cfg['es_commit'],
                              'mcopy_sha256': digest(mcopy), 'state_reader_sha256': digest(checker), 'source_mappings': source_mappings})
    print('PASS actual completed engineering artifact identity, GPT, SYSTEM/KERNEL equality and selected installed bytes')


if __name__ == '__main__':
    sys.dont_write_bytecode = True
    main()

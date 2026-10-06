#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-2.0-or-later
# Copyright (C) 2026-present pixelelated
"""Focused installed-image cloud boundaries and real pair recovery (#356/#365).

Owns a fresh pair and local WebDAV backend. Run through watch-build-submit.
Every case resets both guests and the cloud. No production binary is replaced;
a selected rclone operation may be faulted through the supported profile path.
"""
import argparse
import datetime
import hashlib
import json
import os
from pathlib import Path
import re
import shlex
import signal
import subprocess
import sys
import time

CONF = '/storage/.config/cloud_sync.conf'
QA = '/tmp/pixelelated-cloud-boundaries'
SHIM = '/storage/.config/profile.d/999-cloud-boundaries-qa.sh'
SOURCES = 'projects/ROCKNIX/packages/network/rclone/sources'


def require(value, message):
    if not value:
        raise AssertionError(message)


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def save(path, value):
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + '\n')


class Proof:
    def __init__(self, args):
        self.args = args
        self.tree = args.tree.resolve(strict=True)
        self.owner = args.output.resolve(strict=True)
        require(not any(self.owner.iterdir()), 'output must be a fresh empty directory')
        self.pair = self.owner / 'pair'
        self.cloud = self.owner / 'cloud'
        self.data = self.cloud / 'data'
        self.logs = self.owner / 'artifacts'
        for p in (self.pair, self.cloud, self.logs):
            p.mkdir(mode=0o700)
        self.env = dict(os.environ, VM_PAIR_DIR=str(self.pair), CLOUD_QA_STATE=str(self.cloud),
                        CLOUD_QA_BACKEND='webdav', CLOUD_QA_PORT='9040', VM_GL='none')
        self.seq = 0
        self.results = []
        self.case = 'setup'
        self.backend_started = False
        self.original_scripts = {}

    def local(self, tool, *args, **kwargs):
        return subprocess.run([str(self.tree / 'tools' / tool), *args],
                              env=self.env, cwd=self.tree, check=True, **kwargs)

    def on(self, guest, command, allowed=(0,), data=None):
        port = {'a': '10022', 'b': '10023'}[guest]
        result = subprocess.run(['ssh', '-i', str(self.pair / 'qa-key'), '-p', port,
            '-o', 'BatchMode=yes', '-o', 'StrictHostKeyChecking=no',
            '-o', 'UserKnownHostsFile=/dev/null', '-o', 'LogLevel=ERROR',
            '-o', 'ConnectTimeout=8', 'root@127.0.0.1',
            '. /etc/profile >/dev/null 2>&1; ' + command],
            input=data, capture_output=True, text=True, timeout=180)
        self.seq += 1
        # Only synthetic QA state is used. Do not log setup stdin/config values.
        text = result.stdout + result.stderr
        text = '\n'.join(x for x in text.splitlines()
                         if not re.search(r'key|passw|token|user|psk', x, re.I)) + '\n'
        prefix = self.logs / f'{self.seq:04d}-{self.case}-{guest}'
        prefix.with_suffix('.log').write_text(text)
        prefix.with_suffix('.rc').write_text(str(result.returncode) + '\n')
        require(allowed is None or result.returncode in allowed,
                f'{self.case}/{guest}: rc{result.returncode}; see {prefix.name}.log')
        return result

    def pointers(self, guest='a'):
        text = self.on(guest, "grep -E '^(SAVES|SETTINGS|CONTENT)_REMOTE=|^LAYOUT_KEEP=' " + CONF).stdout
        return {k: v.strip('"') for k, v in (x.split('=', 1) for x in text.splitlines())}

    def conf(self, saves='/ROCKNIX/Saves', backups='/ROCKNIX/Backups', content='/ROCKNIX/Content', guest='a'):
        values = dict(SAVES_REMOTE=saves, SETTINGS_REMOTE=backups, CONTENT_REMOTE=content, LAYOUT_KEEP='')
        # Rewrite only named QA fields; None means genuinely omitted.
        script = "sed -i '/^SAVES_REMOTE=/d; /^SETTINGS_REMOTE=/d; /^CONTENT_REMOTE=/d; /^LAYOUT_KEEP=/d' " + CONF + '\n'
        for key, value in values.items():
            if value is not None:
                script += 'printf "%s\\n" ' + shlex.quote(f'{key}="{value}"') + ' >> ' + CONF + '\n'
        self.on(guest, 'set -e; ' + script)
        actual = self.pointers(guest)
        require(all(actual.get(k) == v for k, v in values.items()), 'fixture pointers did not persist')

    def put(self, relative, data=b'sentinel\n'):
        path = self.data / relative.lstrip('/')
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(data)
        return path

    def hashes(self):
        return {str(p.relative_to(self.data)): sha(p)
                for p in sorted(self.data.rglob('*')) if p.is_file()}

    def reset(self):
        self.cursors = {}
        for guest in ('a', 'b'):
            self.on(guest, f'set -e; rm -f {QA}/fault {QA}/fired /storage/.config/cloud-layout-migration.json; '
                    'rm -rf /storage/.cache/cloud_sync/scan')
            cursor = self.on(guest, 'journalctl -n 0 --show-cursor --no-pager').stdout
            self.cursors[guest] = next(x[11:] for x in cursor.splitlines() if x.startswith('-- cursor: '))
        self.local('cloud-test-backend', 'reset', stdout=subprocess.DEVNULL)
        for guest in ('a', 'b'):
            self.conf(guest=guest)
        save(self.logs / (self.case + '-reset.json'),
             {'cloud': self.hashes(), 'a': self.pointers(), 'b': self.pointers('b')})
        require(not self.hashes(), 'backend reset left payloads')

    def fault(self, operation, path):
        self.on('a', 'printf "%s\\n" ' + shlex.quote(operation + ' ' + path) + f' > {QA}/fault')

    def clear_fault(self):
        self.on('a', f'rm -f {QA}/fault')

    def migrate(self, mode='--apply', guest='a', allowed=(0,)):
        return self.on(guest, '/usr/bin/cloud_migrate_layout ' + shlex.quote(mode), allowed=allowed)

    def follower(self):
        before = self.hashes()
        self.on('b', 'test ! -e /storage/.config/cloud-layout-migration.json')
        cursor = self.on('b', "journalctl -n 0 --show-cursor --no-pager").stdout
        cursor = next(x[11:] for x in cursor.splitlines() if x.startswith('-- cursor: '))
        self.on('b', '/usr/bin/cloud_scan --folder')
        require(self.pointers('b')['SAVES_REMOTE'] == '/pixelelated/Saves', 'separate guest did not follow')
        self.on('b', 'grep -qx STATE=current /storage/.cache/cloud_sync/scan/state')
        self.migrate('--needs-step', guest='b', allowed=(1,))
        journal = self.on('b', 'journalctl -t cloud_migrate_layout --no-pager --after-cursor=' + shlex.quote(cursor)).stdout
        require('follow' in journal.lower(), 'separate guest has no follow journal')
        require(before == self.hashes(), 'separate follower changed cloud bytes')
        save(self.logs / (self.case + '-follower.json'),
             {'a': self.pointers(), 'b': self.pointers('b'), 'cloud': self.hashes(),
              'no_dialog_basis': 'folder state current and needs-step exit1', 'journal': journal})

    def migration_case(self, fault=None):
        payloads = {'Saves/gb/A.srm': b'save bytes\n', 'Backups/QA/settings.tar.gz': b'settings bytes\n',
                    'Saves-replaced/gb/A.srm': b'previous progress\n', 'Content/ROMs/gb/A.gb': b'game bytes\n'}
        for path, data in payloads.items():
            self.put('ROCKNIX/' + path, data)
        if fault is None:
            self.put('pixelelated/.layout', b'layout=1\n')
        save(self.logs / (self.case + '-initial.json'), {'cloud': self.hashes(), 'pointers': self.pointers()})
        if fault:
            operation, stage = fault
            path = self.remote + ('/pixelelated/.layout' if stage == 'marker' else '/ROCKNIX/' + stage)
            self.fault(operation, path)
            require(self.migrate(allowed=None).returncode != 0, 'faulted move reported success')
            self.on('a', f'test -s {QA}/fired')
            require(not (self.data / 'pixelelated/.layout').exists(), 'fault published success marker')
            for path, data in payloads.items():
                require(any((self.data / root / path).is_file() and (self.data / root / path).read_bytes() == data
                            for root in ('ROCKNIX', 'pixelelated')), 'fault lost ' + path)
            save(self.logs / (self.case + '-interrupted.json'), {'cloud': self.hashes(), 'pointers': self.pointers()})
            self.clear_fault()
        self.migrate()
        for path, data in payloads.items():
            require((self.data / 'pixelelated' / path).read_bytes() == data, 'moved payload changed: ' + path)
            require(not (self.data / 'ROCKNIX' / path).exists(), 'old duplicate: ' + path)
        require((self.data / 'pixelelated/.layout').read_bytes() == b'layout=2\n', 'exact layout2 marker missing')
        self.on('a', 'test ! -e /storage/.config/cloud-layout-migration.json')
        journal = self.on('a', 'journalctl -t cloud_migrate_layout --no-pager --after-cursor=' +
                          shlex.quote(self.cursors['a'])).stdout
        for stage in ['begin', 'backups', 'saves', 'discarded', 'content', 'complete']:
            require('migration step=1 from=1 to=2 stage=' + stage in journal,
                    'numbered journal stage missing from this case: ' + stage)
        before = (self.hashes(), self.pointers())
        self.migrate(allowed=(0, 3))
        require((self.hashes(), self.pointers()) == before, 'repeat changed bytes/pointers')
        self.follower()

    def backup_choice(self, mode, root, custom):
        saves = '/GAMES' if root == '/GAMES' else root + '/Saves'
        backups = '/Mine/Backups' if custom else root + ('/backup' if root == '/GAMES' else '/Backups')
        self.conf(saves, backups, root + '/Content')
        path = 'QA/2026_10_01-120000-QA-ROCKNIX_SETTINGS.tar.gz'
        self.put(backups + '/' + path, b'independent settings sentinel\n')
        (self.data / 'pixelelated/Saves').mkdir(parents=True)
        before = self.hashes()
        self.migrate(mode, allowed=(0, 3))
        pointer = self.pointers()['SETTINGS_REMOTE']
        require((self.data / pointer.lstrip('/') / path).read_bytes() == b'independent settings sentinel\n',
                'independent settings were abandoned')
        require(before == self.hashes(), 'pointer-only follow/settle changed payloads')

    def content_choice(self, mode, choice):
        saves = '/pixelelated/Saves' if mode == '--join' else '/ROCKNIX/Saves'
        self.conf(saves, '/ROCKNIX/Backups', choice)
        if mode == '--join':
            self.put('ROCKNIX/Saves/gb/A.srm')
        if mode == '--follow':
            (self.data / 'pixelelated/Saves').mkdir(parents=True)
        if choice == '':
            self.put('ROMs/gb/Root.gb', b'root content sentinel\n')
        self.migrate(mode, allowed=(0, 3))
        derived = '/ROCKNIX/Content' if mode == '--join' else '/pixelelated/Content'
        expected = derived if choice is None or choice == '/ROCKNIX/Content' else choice
        require(self.pointers().get('CONTENT_REMOTE') == expected, 'independent content choice changed')
        if choice == '':
            require((self.data / 'ROMs/gb/Root.gb').read_bytes() == b'root content sentinel\n', 'root content lost')

    def two_roots(self, configured):
        self.conf(configured, '/GAMES/backup' if configured == '/GAMES' else '/ROCKNIX/Backups', '')
        self.put('GAMES/gb/A.srm', b'games progress\n')
        self.put('ROCKNIX/Saves/gb/A.srm', b'rocknix progress\n')
        before = self.hashes()
        self.on('a', '/usr/bin/cloud_scan --folder')
        require(self.pointers()['SAVES_REMOTE'] == configured, 'configured-first choice changed')
        require(self.hashes() == before, 'discovery changed either populated root')

    def collision(self):
        self.put('ROCKNIX/Saves/gb/A.srm', b'local progress\n')
        self.put('ROCKNIX/Content/ROMs/gb/A.gb', b'old content\n')
        self.put('pixelelated/Content/ROMs/gb/A.gb', b'foreign content\n')
        require(self.migrate(allowed=None).returncode != 0, 'foreign content collision accepted')
        require((self.data / 'pixelelated/Content/ROMs/gb/A.gb').read_bytes() == b'foreign content\n', 'foreign content overwritten')
        require((self.data / 'ROCKNIX/Content/ROMs/gb/A.gb').read_bytes() == b'old content\n', 'old content lost')
        require((self.data / 'pixelelated/Saves/gb/A.srm').read_bytes() == b'local progress\n', 'completed save tier lost')
        require(not (self.data / 'pixelelated/.layout').exists(), 'collision marked complete')
        require(self.pointers()['CONTENT_REMOTE'] == '/ROCKNIX/Content', 'refused content pointer advanced')
        self.on('a', 'test -s /storage/.config/cloud-layout-migration.json')

    def restricted(self):
        self.conf('/pixelelated/Saves', '/pixelelated/Backups', '/pixelelated/Content')
        self.put('pixelelated/Saves/gb/A.srm')
        before = (self.hashes(), self.pointers())
        self.fault('lsf-root', self.remote)
        require(self.on('a', 'rclone lsf ' + shlex.quote(self.remote) + ' --dirs-only', allowed=None).returncode != 0,
                'parent-list fault is not armed')
        self.on('a', f'test -s {QA}/fired; rm -f {QA}/fired')
        self.on('a', 'rclone lsf ' + shlex.quote(self.remote + '/pixelelated/Saves') + ' --recursive')
        self.on('a', '/usr/bin/cloud_scan --folder')
        require((self.hashes(), self.pointers()) == before, 'restricted folder scan changed bytes/pointers')
        require(self.on('a', '/usr/bin/cloud_scan', allowed=None).returncode != 0, 'full chooser hid denied parent listing')
        self.on('a', f'test -s {QA}/fired')
        require((self.hashes(), self.pointers()) == before, 'restricted full scan changed bytes/pointers')

    def start(self):
        for p in Path('/proc').glob('[0-9]*/cmdline'):
            try:
                name = Path(p.read_bytes().split(b'\0', 1)[0].decode()).name
            except (FileNotFoundError, ProcessLookupError):
                continue
            require(not name.startswith('qemu-system-'), 'another QEMU owns VM resources')
        self.local('vm-pair', 'up', str(self.args.image.resolve(strict=True)))
        self.backend_started = True
        self.local('cloud-test-backend', 'up')
        config = self.local('cloud-test-backend', 'rclone-conf', capture_output=True, text=True).stdout
        identities = []
        for guest in ('a', 'b'):
            self.on(guest, 'set -e; systemctl stop essway; set_setting cloudsaves.startup 0; '
                    'set_setting cloudsaves.gameexit 0; mkdir -p /storage/.config/rclone; '
                    'cat > /storage/.config/rclone/rclone.conf; chmod 600 /storage/.config/rclone/rclone.conf', data=config)
            self.on(guest, '/usr/bin/cloud_sync_helper')
            build = self.on(guest, 'sed -n \'s/^BUILD_ID="\\(.*\\)"/\\1/p\' /etc/os-release').stdout.strip()
            require(build == self.args.build_id, 'guest BUILD_ID differs from frozen candidate')
            identities.append({'guest': guest, 'build': build, 'boot_id': self.on(guest, 'cat /proc/sys/kernel/random/boot_id').stdout.strip(),
                               'device_id': self.on(guest, '/usr/bin/cloud_device_id').stdout.strip()})
            for script in ['cloud_migrate_layout', 'cloud_scan', 'cloud_setup']:
                value = self.on(guest, 'sha256sum /usr/bin/' + script).stdout.split()[0]
                require(value == sha(self.tree / SOURCES / script), 'installed source mismatch: ' + script)
                self.original_scripts[guest + '/' + script] = value
            self.on(guest, f'test ! -e {QA} && test ! -e {SHIM}; mkdir -p {QA} /storage/.config/profile.d')
        require(identities[0]['boot_id'] != identities[1]['boot_id'] and
                identities[0]['device_id'] != identities[1]['device_id'], 'pair is not two independent devices')
        save(self.logs / 'identities.json', identities)
        self.remote = self.on('a', '/usr/bin/rclone listremotes').stdout.strip()
        require(re.fullmatch(r'[A-Za-z0-9_-]+:', self.remote), 'expected exactly one QA remote')
        shim = f'''#!/bin/sh
if [ -f {QA}/fault ]; then
 expected=$(cat {QA}/fault)
 matched=no
 [ "$1 $2" != "$expected" ] || matched=yes
 if [ "$1" = lsf ] && [ "$expected" = "lsf-root {self.remote}" ]; then
  for arg in "$@"; do [ "$arg" != "{self.remote}" ] || matched=yes; done
 fi
 if [ "$matched" = yes ]; then
  printf '%s\\n' "$*" >> {QA}/fired
  echo 'injected local QA provider refusal' >&2
  exit 5
 fi
fi
exec /usr/bin/rclone "$@"
'''
        self.on('a', f'cat > {QA}/rclone; chmod 755 {QA}/rclone', data=shim)
        self.on('a', 'printf "%s\\n" ' + shlex.quote(f'export PATH={QA}:$PATH') + f' > {SHIM}')
        require(self.on('a', 'command -v rclone').stdout.strip() == QA + '/rclone', 'provider shim not selected')

    def run_cases(self):
        cases = [('layout1-to2', lambda: self.migration_case())]
        for op, stages in [('copy', ['Backups', 'Saves', 'Saves-replaced', 'Content']),
                           ('delete', ['Backups', 'Saves', 'Saves-replaced', 'Content']), ('rcat', ['marker'])]:
            for stage in stages:
                cases.append((f'pair-{op}-{stage}', lambda o=op, s=stage: self.migration_case((o, s))))
        for mode in ['--follow', '--settle']:
            for root, custom in [('/ROCKNIX', False), ('/GAMES', False), ('/ROCKNIX', True)]:
                cases.append((f'T20-{mode[2:]}-{root[1:]}-{custom}', lambda m=mode, r=root, c=custom: self.backup_choice(m, r, c)))
        for mode in ['--join', '--follow', '--settle', '--apply']:
            for label, choice in [('missing', None), ('root', ''), ('derived', '/ROCKNIX/Content'), ('custom', '/Mine/ROMs')]:
                cases.append((f'T21-{mode[2:]}-{label}', lambda m=mode, c=choice: self.content_choice(m, c)))
        for root in ['/GAMES', '/ROCKNIX/Saves']:
            cases.append(('T22-' + root.replace('/', '_'), lambda r=root: self.two_roots(r)))
        cases += [('T23-content-collision', self.collision), ('T25-restricted-parent', self.restricted)]
        for name, action in cases:
            self.case = name
            print('START ' + name, flush=True)
            try:
                self.reset()
                action()
                save(self.logs / (name + '-final.json'), {'cloud': self.hashes(), 'a': self.pointers(), 'b': self.pointers('b')})
                self.results.append({'case': name, 'status': 'PASS'})
                print('PASS ' + name, flush=True)
            except (AssertionError, subprocess.SubprocessError, OSError, StopIteration) as error:
                self.results.append({'case': name, 'status': 'FAIL', 'reason': str(error)})
                print('FAIL ' + name + ': ' + str(error), flush=True)
            save(self.logs / 'results.json', self.results)
        self.case = 'final-custody'
        for key, value in self.original_scripts.items():
            guest, script = key.split('/')
            require(self.on(guest, 'sha256sum /usr/bin/' + script).stdout.split()[0] == value,
                    'installed script changed during proof')
        return 0 if all(x['status'] == 'PASS' for x in self.results) else 1

    def cleanup(self):
        # Stop only processes whose argv carries a disk beneath this fresh owner.
        stopped = []
        for p in Path('/proc').glob('[0-9]*/cmdline'):
            try:
                argv = p.read_bytes().split(b'\0')
            except (FileNotFoundError, ProcessLookupError):
                continue
            if Path(argv[0].decode()).name.startswith('qemu-system-') and any(str(self.pair).encode() in x for x in argv):
                pid = int(p.parent.name)
                os.kill(pid, signal.SIGTERM)
                stopped.append(pid)
        for _ in range(100):
            if all(not Path('/proc', str(pid)).exists() for pid in stopped):
                break
            time.sleep(.1)
        require(all(not Path('/proc', str(pid)).exists() for pid in stopped), 'owned guest failed to exit')
        if self.backend_started:
            self.local('cloud-test-backend', 'down')
        save(self.owner / 'cleanup.json', {'utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
                                        'qemu_pids': stopped, 'all_absent': True})


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--tree', type=Path)
    p.add_argument('--image', type=Path)
    p.add_argument('--build-id')
    p.add_argument('--output', type=Path)
    p.add_argument('--inject-failure', action='store_true')
    args = p.parse_args()
    if args.inject_failure:
        require(False, 'constructed failing assertion: expected exit1')
    require(all([args.tree, args.image, args.build_id, args.output]), 'tree, image, build-id and output required')
    proof = Proof(args)
    try:
        proof.start()
        return proof.run_cases()
    finally:
        proof.cleanup()


if __name__ == '__main__':
    try:
        sys.exit(main())
    except (AssertionError, OSError, subprocess.SubprocessError, StopIteration) as error:
        print('FAIL: ' + str(error), file=sys.stderr, flush=True)
        sys.exit(1)

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
import io
import json
import os
from pathlib import Path
import re
import shlex
import signal
import subprocess
import sys
import tarfile
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
            self.on(guest, f'set -e; rm -f {QA}/sed {QA}/mv {QA}/pointer-fired; '
                    f'cp {QA}/original-rclone.conf /storage/.config/rclone/rclone.conf; '
                    f'cp {QA}/original-sync.conf {CONF}')
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
        before = self.audit_snapshot()
        record = '/storage/.config/cloud-layout-migration.json'
        self.on('a', 'test ! -e ' + record)
        refusals = []
        for attempt in range(2):
            result = self.migrate(allowed=None)
            require(result.returncode != 0, 'foreign content collision accepted')
            require('>>> why THE NEW FOLDER ALREADY HAS FILES IN IT' in result.stdout,
                    'collision returned an unrelated refusal')
            require(self.audit_snapshot() == before, 'collision refusal changed cloud data or settings')
            self.on('a', 'test ! -e ' + record)
            refusals.append({'attempt': attempt + 1, 'returncode': result.returncode})
        require((self.data / 'pixelelated/Content/ROMs/gb/A.gb').read_bytes() == b'foreign content\n', 'foreign content overwritten')
        require((self.data / 'ROCKNIX/Content/ROMs/gb/A.gb').read_bytes() == b'old content\n', 'old content lost')
        require((self.data / 'ROCKNIX/Saves/gb/A.srm').read_bytes() == b'local progress\n', 'original save changed')
        require(not (self.data / 'pixelelated/.layout').exists(), 'collision marked complete')
        require(self.pointers()['CONTENT_REMOTE'] == '/ROCKNIX/Content', 'refused content pointer advanced')
        save(self.logs / 'content-collision-refusal.json',
             {'before': before, 'after': self.audit_snapshot(), 'refusals': refusals,
              'recovery_record_absent': True})

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
            for script in ['cloud_migrate_layout', 'cloud_scan', 'cloud_setup', 'cloud_content_restore']:
                value = self.on(guest, 'sha256sum /usr/bin/' + script).stdout.split()[0]
                require(value == sha(self.tree / SOURCES / script), 'installed source mismatch: ' + script)
                self.original_scripts[guest + '/' + script] = value
            self.on(guest, f'test ! -e {QA} && test ! -e {SHIM}; mkdir -p {QA} /storage/.config/profile.d')
            self.on(guest, f'set -e; cp {CONF} {QA}/original-sync.conf; '
                    f'cp /storage/.config/rclone/rclone.conf {QA}/original-rclone.conf')
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
 if [ "$1" = lsf ]; then
  case "$expected" in
   'lsf-path '*)
    path=${{expected#lsf-path }}
    for arg in "$@"; do [ "${{arg%/}}" != "${{path%/}}" ] || matched=yes; done ;;
  esac
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

    def audit_snapshot(self):
        return dict(cloud=self.hashes(), pointers=self.pointers(),
                    config_sha256=self.on('a', 'sha256sum ' + CONF).stdout.split()[0])

    def audit_current(self, content='/pixelelated/Content'):
        self.conf('/pixelelated/Saves', '/pixelelated/Backups', content)
        self.put('pixelelated/Saves/gb/current.srm', b'current progress\n')
        self.put('pixelelated/.layout', b'layout=2\n')

    def audit_atomic(self, mode, boundary):
        root = '/pixelelated' if mode == '--join' else '/ROCKNIX'
        self.conf(root + '/Saves', root + '/Backups', root + '/Content')
        if mode == '--join':
            self.put('ROCKNIX/Saves/gb/A.srm')
        elif mode == '--follow':
            self.put('pixelelated/Saves/gb/A.srm')
        self.on('a', 'chmod 640 ' + CONF)
        before = self.audit_snapshot()
        command = 'mv' if boundary == 'publish' else 'sed'
        match = '[ "${!#}" = ' + CONF + ' ]' if command == 'mv' else f'[[ "$*" == *"^{boundary}="* ]]'
        shim = f'#!/bin/bash\nif {match}; then echo fired > {QA}/pointer-fired; exit 1; fi\nexec /usr/bin/{command} "$@"\n'
        self.on('a', f'cat > {QA}/{command}; chmod 755 {QA}/{command}', data=shim)
        interrupted = self.migrate(mode, allowed=None)
        self.on('a', f'test -s {QA}/pointer-fired; rm -f {QA}/{command}')
        require(interrupted.returncode != 0, 'pointer-publication fault reported success')
        require(self.audit_snapshot() == before, 'partial pointer set became live')
        self.migrate(mode)
        target = '/ROCKNIX' if mode == '--join' else '/pixelelated'
        require(all(self.pointers()[k] == target + '/' + suffix for k, suffix in
                    [('SAVES_REMOTE', 'Saves'), ('SETTINGS_REMOTE', 'Backups'), ('CONTENT_REMOTE', 'Content')]),
                'retry left a mixed pointer set')
        require(self.hashes() == before['cloud'], 'pointer-only transition changed cloud bytes')
        require(self.on('a', "stat -c '%a' " + CONF).stdout.strip() == '640', 'config mode changed')
        save(self.logs / (self.case + '-publication.json'), dict(before=before, after=self.audit_snapshot()))

    def audit_sibling(self, content):
        self.audit_current(content)
        self.put('ROCKNIX/Saves/gb/kept.srm', b'sibling progress\n')
        self.put('ROCKNIX/Saves-replaced/stamp/gb/older.srm', b'sibling older progress\n')
        self.migrate('--keep', guest='b')
        before = self.audit_snapshot(), self.pointers('b')
        for _ in range(2):
            self.on('a', '/usr/bin/cloud_scan --folder')
            self.on('a', 'grep -qx STATE=current /storage/.cache/cloud_sync/scan/state')
            self.migrate(allowed=(0, 3))
            require((self.audit_snapshot(), self.pointers('b')) == before, 'active sibling shelf moved')

    def audit_binding(self, kind):
        self.put('ROCKNIX/Saves/gb/A.srm', b'save witness\n')
        self.put('ROCKNIX/Content/ROMs/gb/A.gb', b'content witness\n')
        self.fault('copy', self.remote + '/ROCKNIX/Content')
        if kind == 'legacy':
            ref = '7afa9efcfc0c1ce4b89774b38878fc1b9a9063d2'
            old = subprocess.check_output(['git', '-C', str(self.tree), 'show', ref + ':' + SOURCES + '/cloud_migrate_layout'])
            self.on('a', f'cat > {QA}/predecessor; chmod 755 {QA}/predecessor', data=old.decode())
            first = self.on('a', f'{QA}/predecessor --apply', allowed=None)
            save(self.logs / (self.case + '-predecessor.json'), dict(ref=ref, sha256=hashlib.sha256(old).hexdigest()))
        else:
            first = self.migrate(allowed=None)
        require(first.returncode != 0, 'copy interruption did not fire')
        record = '/storage/.config/cloud-layout-migration.json'
        self.on('a', f'test -s {QA}/fired; test -s {record}')
        self.clear_fault()
        config = '/storage/.config/rclone/rclone.conf'
        if kind == 'legacy':
            self.on('a', f"jq -e 'has(\"fingerprint_format\") | not' {record} >/dev/null")
        if kind == 'endpoint':
            self.put('other-cloud/foreign-witness.txt', b'other connection\n')
        before = self.audit_snapshot()
        record_hash = self.on('a', 'sha256sum ' + record).stdout.split()[0]
        if kind == 'comments':
            self.on('a', "printf '\\n# harmless QA comment\\n' >> " + config)
        elif kind == 'token':
            self.on('a', "printf '\\ntoken = synthetic-unused\\n' >> " + config)
        elif kind == 'format':
            self.on('a', 'python3 -', data=f'''from pathlib import Path
p=Path({config!r})
lines=p.read_text().splitlines()
header=[x for x in lines if x.startswith('[')]
fields=[x for x in lines if '=' in x and not x.lstrip().startswith(('#',';'))]
p.write_text('; harmless QA header\\n'+ '\\n'.join(header+list(reversed([x.replace(' = ', '=') for x in fields])))+'\\n')
''')
        elif kind == 'endpoint':
            self.on('a', 'python3 -', data=f'''from pathlib import Path
import re
p=Path({config!r})
text,n=re.subn(r'^url\\s*=\\s*(.*?)\\s*$', lambda m:'url = '+m[1].rstrip('/')+'/other-cloud/', p.read_text(), flags=re.M)
assert n==1
p.write_text(text)
''')
        state = self.migrate('--state', allowed=None)
        if kind == 'endpoint':
            require(state.returncode == 5 and 'NEEDS ITS ORIGINAL CONNECTION' in state.stdout,
                    'changed binding was not truthfully refused')
            for command in ['/usr/bin/cloud_migrate_layout --apply', '/usr/bin/cloud_setup --seed-folders']:
                result = self.on('a', command, allowed=None)
                require(result.returncode != 0 and 'NEEDS ITS ORIGINAL CONNECTION' in result.stdout,
                        'recovery entry point lost the binding reason')
            require(self.audit_snapshot() == before, 'binding refusal changed cloud/settings')
            require(self.on('a', 'sha256sum ' + record).stdout.split()[0] == record_hash, 'record was rebound')
            self.on('a', f'cp {QA}/original-rclone.conf {config}')
        else:
            require(state.returncode == 0 and 'STATE=migration-pending' in state.stdout,
                    'harmless rewrite stranded the move')
        self.migrate()
        self.on('a', 'test ! -e ' + record)
        require((self.data / 'pixelelated/Saves/gb/A.srm').read_bytes() == b'save witness\n', 'save lost')
        require((self.data / 'pixelelated/Content/ROMs/gb/A.gb').read_bytes() == b'content witness\n', 'content lost')

    def audit_reader(self, kind):
        self.audit_current()
        forms = {
            'escaped': r'SETTINGS_REMOTE="/Custom/My\$Backups"',
            'single': "SETTINGS_REMOTE='/Custom/Backups' # comment",
            'bare': 'SETTINGS_REMOTE=/Custom/Backups # comment',
            'double': 'SETTINGS_REMOTE="/Custom/Backups" # comment',
            'duplicate': 'SETTINGS_REMOTE="/Custom/Backups"\nSETTINGS_REMOTE="/Other/Backups"',
            'export': 'export SETTINGS_REMOTE="/Custom/Backups"',
            'trailing': 'SETTINGS_REMOTE="/Custom/Backups" invalid',
            'control': 'SETTINGS_REMOTE="/Custom/Backups"\r',
        }
        self.on('a', "sed -i '/^SETTINGS_REMOTE=/d' " + CONF + '; printf "%s\\n" ' +
                shlex.quote(forms[kind]) + ' >> ' + CONF)
        malformed = kind in ('export', 'trailing', 'control')
        expected = '/Custom/My$Backups' if kind == 'escaped' else '/Custom/Backups'
        if not malformed:
            label = self.on('a', '/usr/bin/cloud_device_id --label').stdout.strip()
            device = self.on('a', '/usr/bin/cloud_device_id').stdout.strip()
            require(re.fullmatch(r'[A-Za-z0-9_-]+', label) and
                    re.fullmatch(r'[A-Za-z0-9_-]+', device), 'unsafe fixture identity')
            archive = '2026_10_06-120000-' + label + '-ROCKNIX_SETTINGS.tar.gz'
            wrong_archive = '2026_10_06-130000-' + label + '-ROCKNIX_SETTINGS.tar.gz'
            payload = io.BytesIO()
            with tarfile.open(fileobj=payload, mode='w:gz') as tar:
                info = tarfile.TarInfo('storage/.config/reader-sentinel')
                witness = b'correct parsed settings directory\n'
                info.size = len(witness)
                tar.addfile(info, io.BytesIO(witness))
            self.put(expected + '/' + device + '/' + archive, payload.getvalue())
            wrong = '/Custom/My\\$Backups' if kind == 'escaped' else '/Other/Backups'
            self.put(wrong + '/' + device + '/' + wrong_archive, payload.getvalue())
        before = self.audit_snapshot()
        original_shim = None
        if malformed:
            # listremotes reads local rclone configuration. Faulting it made
            # prepare() stop before the malformed cloud config was read.
            # Observe calls without replacing their results; permit only that
            # local enumeration, and reject every provider operation.
            original_shim = self.on('a', f'cat {QA}/rclone').stdout
            observer = (f'#!/bin/sh\nprintf "%s\\n" "$1" >> {QA}/reader-calls\n'
                        'exec /usr/bin/rclone "$@"\n')
            self.on('a', f'cat > {QA}/rclone; chmod 755 {QA}/rclone; : > {QA}/reader-calls',
                    data=observer)
        try:
            if malformed:
                self.on('a', 'rclone lsf ' + shlex.quote(self.remote) + ' --max-depth 1 >/dev/null')
                control = self.on('a', f'cat {QA}/reader-calls').stdout.splitlines()
                require(control == ['lsf'], 'provider observer did not see its real negative control')
                self.on('a', f': > {QA}/reader-calls')
            for command in ['/usr/bin/cloud_migrate_layout --state', '/usr/bin/cloud_scan']:
                result = self.on('a', command, allowed=None)
                require((result.returncode != 0) == malformed, 'reader disagreement: ' + kind)
                if malformed:
                    require(">>> why YOUR CLOUD SYNC SETTINGS COULDN'T BE READ" in result.stdout,
                            'malformed config did not reach its own refusal: ' + kind)
                elif command.endswith('--state'):
                    facts = dict(line.split('=', 1) for line in result.stdout.splitlines() if '=' in line)
                    require(facts.get('BACKUPS') == expected, 'state decoded the wrong settings value')
            if not malformed:
                facts = dict(line.split('=', 1) for line in self.on(
                    'a', 'cat /storage/.cache/cloud_sync/scan/settings').stdout.splitlines() if '=' in line)
                require(facts.get('MINE') == archive and
                        facts.get('SOURCE', '').rstrip('/') == self.remote + expected + '/' + device,
                        'full scan selected the wrong parsed directory or duplicate assignment')
                save(self.logs / (self.case + '-value-selection.json'),
                     {'expected_directory': expected, 'expected_archive': archive,
                      'wrong_directory': wrong, 'wrong_archive': wrong_archive, 'scan': facts})
            require(self.audit_snapshot() == before, 'reader changed cloud/settings')
            if malformed:
                calls = self.on('a', f'cat {QA}/reader-calls').stdout.splitlines()
                require(all(call == 'listremotes' for call in calls),
                        'malformed configuration reached provider operations: ' + repr(calls))
                save(self.logs / (self.case + '-provider-observation.json'),
                     {'control_calls': control, 'malformed_calls': calls,
                      'allowed_local_operation': 'listremotes', 'cloud_and_config_unchanged': True})
        finally:
            if original_shim is not None:
                self.on('a', f'cat > {QA}/rclone; chmod 755 {QA}/rclone', data=original_shim)

    def audit_chooser(self, folder):
        self.audit_current()
        self.put(folder + '/ROMs/gb/Chosen.gb', b'chosen content\n')
        self.on('a', '/usr/bin/cloud_scan')
        listed = self.on('a', 'cat /storage/.cache/cloud_sync/scan/root-dirs').stdout.splitlines()
        require(folder in listed, 'ordinary folder not offered')
        before = self.hashes()
        self.on('a', '/usr/bin/cloud_setup --set-content-remote ' + shlex.quote('/' + folder))
        require(self.pointers()['CONTENT_REMOTE'] == '/' + folder, 'selection was not saved')
        self.on('a', '/usr/bin/cloud_scan --content')
        listing = self.on('a', 'cat /storage/.cache/cloud_sync/scan/scan').stdout
        require(re.search(r'^gb\|15\|', listing, re.M), 'chosen content missing from scan')
        require(self.hashes() == before, 'folder selection changed cloud bytes')
        selected = self.audit_snapshot()
        for invalid in ['/a/../b', '/a/./b', '/a//b', '/$HOME', '/`id`', '/two\nlines', '/trailing\n']:
            require(self.on('a', '/usr/bin/cloud_setup --set-content-remote ' + shlex.quote(invalid),
                            allowed=None).returncode != 0, 'unsafe name accepted')
            require(self.audit_snapshot() == selected, 'unsafe name changed settings')

    def audit_reason(self, kind):
        self.audit_current()
        expected = "YOUR CLOUD FOLDER COULDN'T BE READ"
        if kind in ('future', 'malformed'):
            self.put('pixelelated/.layout', b'layout=999\n' if kind == 'future' else b'layout=2\nextra\n')
        elif kind == 'record':
            self.on('a', "printf '{invalid' > /storage/.config/cloud-layout-migration.json")
        elif kind == 'config':
            self.on('a', "printf 'export SETTINGS_REMOTE=bad\\n' >> " + CONF)
            expected = "YOUR CLOUD SYNC SETTINGS COULDN'T BE READ"
        before = self.audit_snapshot()
        result = self.on('a', '/usr/bin/cloud_scan --folder', allowed=None)
        require(result.returncode != 0 and '>>> why ' + expected in result.stdout,
                'application refusal lost its reason')
        require("COULDN'T FIND YOUR CLOUD FOLDER" not in result.stdout, 'false missing-folder reason')
        require(self.audit_snapshot() == before, 'refusal changed cloud/settings')

    def audit_discovery(self, kind):
        layouts = {
            'empty': ('/Mine', [], 'empty', ''),
            'unrelated': ('/Mine', ['Mine/Photos/witness.jpg'], 'empty', ''),
            'fallback': ('/Mine', ['Mine/Photos/witness.jpg', 'pixelelated/Content/ROMs/gb/A.gb'], 'found-elsewhere', '/pixelelated/Content'),
            'tiered': ('/Mine', ['Mine/ROMs/gb/A.gb'], 'ok', ''),
            'root-tiered': ('', ['ROMs/gb/A.gb'], 'ok', ''),
            'root-flat': ('', ['gb/A.gb'], 'ok', ''),
            'root-unrelated': ('', ['Photos/witness.jpg'], 'empty', ''),
            'stranded': ('/Mine', ['gb/A.gb'], 'stranded-at-root', '/'),
            'refused': ('/Mine', ['Mine/ROMs/gb/A.gb'], 'unreadable', None),
        }
        content, paths, state, found = layouts[kind]
        self.audit_current(content)
        for path in paths:
            self.put(path, b'game\n')
        if kind == 'refused':
            self.fault('lsf-path', self.remote + 'Mine')
        before = self.audit_snapshot()
        result = self.on('a', '/usr/bin/cloud_setup --content-location', allowed=None)
        facts = dict(x.split('=', 1) for x in result.stdout.splitlines() if '=' in x)
        require(facts.get('STATE') == state and (found is None or facts.get('FOUND') == found),
                'content classification disagrees: ' + repr(facts))
        require((result.returncode != 0) == (kind == 'refused'), 'content listing refusal hidden')
        require(self.audit_snapshot() == before, 'classification changed state')
        if kind == 'refused':
            self.on('a', f'test -s {QA}/fired')
        if kind == 'stranded':
            self.on('a', '/usr/bin/cloud_setup --use-content-root')
            require(self.pointers()['CONTENT_REMOTE'] == '', 'root selection not retained')
        if kind in ('stranded', 'root-flat', 'root-tiered', 'tiered'):
            result = self.on('a', '/usr/bin/cloud_content_restore --scan')
            require(re.search(r'^gb\|5\|', result.stdout, re.M), 'supported game absent from next scan')
            require(self.hashes() == before['cloud'], 'selection or scan changed cloud bytes')

    def audit_inherited(self, stage):
        ref = '69e6039f8f'
        self.conf('/GAMES', '/GAMES/backup', '/GAMES/Content')
        payloads = {'GAMES/gb/A.srm': b'save\n', 'GAMES/backup/QA/settings.tar.gz': b'settings\n',
                    'GAMES/Content/ROMs/gb/A.gb': b'game\n'}
        for path, value in payloads.items():
            self.put(path, value)
        old = subprocess.check_output(['git', '-C', str(self.tree), 'show', ref + ':' + SOURCES + '/cloud_migrate_layout'])
        self.on('a', f'cat > {QA}/predecessor; chmod 755 {QA}/predecessor', data=old.decode())
        paths = {'backups': '/GAMES/backup', 'saves': '/GAMES', 'content': '/GAMES/Content'}
        if stage != 'complete':
            self.fault('copy', self.remote + paths[stage])
        result = self.on('a', f'{QA}/predecessor --apply', allowed=None)
        if stage != 'complete':
            require(result.returncode != 0, 'predecessor interruption did not fire')
            self.on('a', f'test -s {QA}/fired')
        self.on('a', 'test ! -e /storage/.config/cloud-layout-migration.json')
        save(self.logs / (self.case + '-predecessor.json'), dict(ref=ref, sha256=hashlib.sha256(old).hexdigest(),
             rc=result.returncode, state=self.audit_snapshot()))
        self.clear_fault()
        self.migrate(allowed=(0, 3))
        for path, value in [('Saves/gb/A.srm', b'save\n'), ('Backups/QA/settings.tar.gz', b'settings\n'),
                            ('Content/ROMs/gb/A.gb', b'game\n')]:
            require((self.data / 'pixelelated' / path).read_bytes() == value, 'inherited payload lost: ' + path)
        require((self.data / 'pixelelated/.layout').read_bytes() == b'layout=2\n', 'inherited move did not settle')
        before = self.audit_snapshot()
        self.migrate(allowed=(0, 3))
        require(self.audit_snapshot() == before, 'inherited repeat changed state')

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
        for kind in ['empty', 'unrelated', 'fallback', 'tiered', 'root-tiered', 'root-flat', 'root-unrelated', 'stranded', 'refused']:
            cases.append(('PL001-discovery-' + kind, lambda k=kind: self.audit_discovery(k)))
        for mode in ['--join', '--follow', '--settle']:
            for boundary in ['SAVES_REMOTE', 'SETTINGS_REMOTE', 'CONTENT_REMOTE', 'publish']:
                cases.append((f'PL002-{mode[2:]}-{boundary}', lambda m=mode, b=boundary: self.audit_atomic(m, b)))
        for label, content in [('root', ''), ('custom', '/Mine/Content'), ('current', '/pixelelated/Content')]:
            cases.append(('PL003-kept-sibling-' + label, lambda c=content: self.audit_sibling(c)))
        for stage in ['backups', 'saves', 'content', 'complete']:
            cases.append(('PL003-inherited-RC2-' + stage, lambda s=stage: self.audit_inherited(s)))
        for kind in ['comments', 'format', 'token', 'endpoint', 'legacy']:
            cases.append(('PL004-binding-' + kind, lambda k=kind: self.audit_binding(k)))
        for kind in ['future', 'malformed', 'config', 'record']:
            cases.append(('PL005-reason-' + kind, lambda k=kind: self.audit_reason(k)))
        for folder in ['MyGames', 'My Games', 'Games..old', "Kid's Games"]:
            cases.append(('PL006-chooser-' + folder, lambda f=folder: self.audit_chooser(f)))
        for kind in ['escaped', 'single', 'bare', 'double', 'duplicate', 'export', 'trailing', 'control']:
            cases.append(('PL008-reader-' + kind, lambda k=kind: self.audit_reader(k)))
        if self.args.case:
            cases = [(name, action) for name, action in cases if self.args.case in name]
        require(cases, 'no cases match the requested scope')
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
    p.add_argument('--case', help='run only cases containing this text; still owns a fresh pair')
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

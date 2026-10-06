#!/usr/bin/env python3
"""Challenge reviewer leads against unchanged candidate14, using synthetic clouds.

Observations are not audit verdicts. A zero exit means all requested experiments
completed with custody intact, including experiments demonstrating a defect.
"""
import argparse
import importlib.machinery
import importlib.util
from pathlib import Path
import shlex
import socket
import sys

owner = Path(__file__).resolve().parent
loader = importlib.machinery.SourceFileLoader('boundaries', str(owner / 'boundaries.py'))
spec = importlib.util.spec_from_loader(loader.name, loader)
mod = importlib.util.module_from_spec(spec)
loader.exec_module(mod)
QA = mod.QA
CONF = mod.CONF


class Probe(mod.Proof):
    def start(self):
        super().start()
        self.on('a', f'cp /storage/.config/rclone/rclone.conf {QA}/original-rclone.conf')

    def reset(self):
        self.on('a', f'rm -f {QA}/sed {QA}/sed-fired; '
                f'cp {QA}/original-rclone.conf /storage/.config/rclone/rclone.conf')
        super().reset()

    def snapshot(self):
        return {'cloud': self.hashes(), 'pointers': self.pointers()}

    def command(self, command):
        result = self.on('a', command, allowed=None)
        return {'rc': result.returncode, 'stdout': result.stdout, 'stderr': result.stderr}

    def current(self):
        self.conf('/pixelelated/Saves', '/pixelelated/Backups', '/pixelelated/Content')
        self.put('pixelelated/Saves/gb/current.srm', b'current save\n')
        self.put('pixelelated/.layout', b'layout=2\n')

    def kept_sibling(self):
        self.current()
        self.put('ROCKNIX/Saves/gb/kept.srm', b'kept sibling save\n')
        self.put('ROCKNIX/Saves-replaced/stamp/gb/older.srm', b'kept sibling older save\n')
        self.migrate('--keep', guest='b')
        before = self.snapshot()
        result = {'before': before, 'kept_b': self.pointers('b'),
                  'state': self.command('/usr/bin/cloud_migrate_layout --state'),
                  'apply': self.command('/usr/bin/cloud_migrate_layout --apply')}
        result['after'] = self.snapshot()
        result['kept_b_after'] = self.pointers('b')
        mod.require(result['kept_b'] == result['kept_b_after'], 'sibling pointers mutated')
        mod.require((self.data / 'ROCKNIX/Saves/gb/kept.srm').read_bytes() == b'kept sibling save\n',
                    'sibling live save changed')
        mod.require(any(p.read_bytes() == b'kept sibling older save\n'
                        for p in self.data.rglob('older.srm')), 'sibling older save lost')
        return result

    def record_fingerprint(self):
        self.put('ROCKNIX/Saves/gb/A.srm', b'migration save\n')
        self.put('ROCKNIX/Content/ROMs/gb/A.gb', b'migration game\n')
        self.fault('copy', self.remote + '/ROCKNIX/Content')
        initial = self.command('/usr/bin/cloud_migrate_layout --apply')
        mod.require(initial['rc'] != 0, 'fault did not interrupt migration')
        self.on('a', f'test -s {QA}/fired; test -s /storage/.config/cloud-layout-migration.json')
        before = self.snapshot()
        self.on('a', "printf '\n# harmless synthetic QA comment\n' >> /storage/.config/rclone/rclone.conf")
        changed = {mode: self.command('/usr/bin/cloud_migrate_layout ' + mode)
                   for mode in ('--state', '--apply')}
        changed['seed'] = self.command('/usr/bin/cloud_setup --seed-folders')
        mod.require(before == self.snapshot(), 'mismatched record mutated cloud or pointers')
        self.on('a', f'cp {QA}/original-rclone.conf /storage/.config/rclone/rclone.conf; '
                "printf '\ntoken = synthetic-QA-unused\n' >> /storage/.config/rclone/rclone.conf")
        token_control = self.command('/usr/bin/cloud_migrate_layout --state')
        mod.require(token_control['rc'] == 0, 'excluded credential field changed fingerprint')
        self.clear_fault()
        recovery = self.command('/usr/bin/cloud_migrate_layout --apply')
        mod.require(recovery['rc'] == 0, 'original configuration could not resume')
        self.on('a', 'test ! -e /storage/.config/cloud-layout-migration.json')
        mod.require((self.data / 'pixelelated/Content/ROMs/gb/A.gb').read_bytes() == b'migration game\n',
                    'recovered content changed')
        return {'initial': initial, 'before': before, 'changed_config': changed,
                'token_control': token_control, 'recovery': recovery, 'after': self.snapshot()}

    def pointer_failure(self, mode):
        if mode == '--join':
            self.conf('/pixelelated/Saves', '/pixelelated/Backups', '/pixelelated/Content')
            self.put('ROCKNIX/Saves/gb/A.srm', b'old fleet save\n')
            self.put('ROCKNIX/Backups/old_SETTINGS.tar.gz', b'synthetic archive witness\n')
        elif mode == '--follow':
            self.put('pixelelated/Saves/gb/A.srm', b'new fleet save\n')
            self.put('pixelelated/Backups/new_SETTINGS.tar.gz', b'synthetic archive witness\n')
        else:
            mod.require(mode == '--settle', 'unexpected transition')
        before = self.snapshot()
        shim = f'''#!/bin/sh
if [ "$1" = -i ]; then
 case "$2" in
  's|^SETTINGS_REMOTE='*) printf '%s\\n' "$2" >> {QA}/sed-fired; exit 5 ;;
 esac
fi
exec /usr/bin/sed "$@"
'''
        self.on('a', f'cat > {QA}/sed; chmod 755 {QA}/sed', data=shim)
        self.on('a', f'test "$(command -v sed)" = {QA}/sed')
        interrupted = self.command('/usr/bin/cloud_migrate_layout ' + mode)
        self.on('a', f'test -s {QA}/sed-fired; rm -f {QA}/sed')
        mod.require(interrupted['rc'] != 0, 'second-pointer fault not reported')
        partial = self.snapshot()
        retry = self.command('/usr/bin/cloud_migrate_layout ' + mode)
        scan = self.command('/usr/bin/cloud_scan --folder')
        state = self.command('cat /storage/.cache/cloud_sync/scan/state')
        after = self.snapshot()
        mod.require(before['cloud'] == after['cloud'], 'pointer-only transition changed cloud bytes')
        return {'before': before, 'interrupted': interrupted, 'partial': partial,
                'retry': retry, 'scan': scan, 'state': state, 'after': after}

    def parser(self, kind):
        self.current()
        self.put('pixelelated/Content/ROMs/gb/A.gb', b'content witness\n')
        if kind == 'export':
            replacement = 'export SETTINGS_REMOTE="/Custom/Backups"'
        else:
            replacement = r'SETTINGS_REMOTE="/Custom/My\$Backups"'
            self.put('Custom/My$Backups/witness.txt', b'custom backup witness\n')
        self.on('a', "sed -i '/^SETTINGS_REMOTE=/d' " + CONF +
                '; printf "%s\\n" ' + shlex.quote(replacement) + ' >> ' + CONF)
        before = self.snapshot()
        result = {'before': before, 'state': self.command('/usr/bin/cloud_migrate_layout --state'),
                  'scan': self.command('/usr/bin/cloud_scan'), 'after': self.snapshot()}
        mod.require(result['before'] == result['after'], 'parser challenge changed fixtures')
        return result

    def chooser(self, folder):
        self.current()
        self.put(folder + '/ROMs/gb/A.gb', b'chosen game\n')
        scan = self.command('/usr/bin/cloud_scan')
        mod.require(scan['rc'] == 0, 'chooser pre-scan failed')
        listed = self.command('cat /storage/.cache/cloud_sync/scan/root-dirs')
        mod.require(folder in listed['stdout'].splitlines(), 'folder was not offered by scan')
        before = self.snapshot()
        selected = self.command('/usr/bin/cloud_setup --set-content-remote ' + shlex.quote('/' + folder))
        after = self.snapshot()
        mod.require(before['cloud'] == after['cloud'], 'selection changed cloud bytes')
        return {'before': before, 'listed': listed, 'selected': selected, 'after': after}

    def run_cases(self):
        cases = [('B05-kept-sibling', self.kept_sibling),
                 ('B06-record-fingerprint', self.record_fingerprint)]
        cases += [('B07-' + mode[2:], lambda m=mode: self.pointer_failure(m))
                  for mode in ('--join', '--follow', '--settle')]
        cases += [('B09-' + kind, lambda k=kind: self.parser(k)) for kind in ('export', 'escaped')]
        cases += [('B14-' + label, lambda f=folder: self.chooser(f))
                  for label, folder in [('control', 'MyGames'), ('space', 'My Games'), ('dots', 'Games..old')]]
        for name, action in cases:
            self.case = name
            print('START ' + name, flush=True)
            self.reset()
            observation = action()
            observation['case'] = name
            mod.save(self.logs / (name + '-observation.json'), observation)
            self.results.append({'case': name, 'observation_complete': True})
            mod.save(self.logs / 'results.json', self.results)
            print('OBSERVED ' + name, flush=True)
        for key, value in self.original_scripts.items():
            guest, script = key.split('/')
            mod.require(self.on(guest, 'sha256sum /usr/bin/' + script).stdout.split()[0] == value,
                        'installed bytes changed: ' + key)
        mod.save(self.logs / 'installed-unchanged.json', self.original_scripts)
        return 0

    def cleanup(self):
        self.local('vm-pair', 'down')
        if self.backend_started:
            self.local('cloud-test-backend', 'down')
        for port in (9040, 10022, 10023, 5909, 5910):
            with socket.socket() as sock:
                mod.require(sock.connect_ex(('127.0.0.1', port)) != 0, 'owned port still open')
        mod.save(self.owner / 'cleanup.json', {'owned_guests_stopped': True, 'backend_stopped': True,
                                              'ports_unbound': [9040, 10022, 10023, 5909, 5910]})


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--tree', type=Path, required=True)
    parser.add_argument('--image', type=Path, required=True)
    parser.add_argument('--build-id', required=True)
    parser.add_argument('--output', type=Path, required=True)
    proof = Probe(parser.parse_args())
    try:
        proof.start()
        code = proof.run_cases()
    finally:
        proof.cleanup()
    sys.exit(code)

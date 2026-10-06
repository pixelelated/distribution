#!/usr/bin/env python3
"""Read the unchanged installed content classifier in isolated synthetic clouds."""
import argparse
import importlib.machinery
import importlib.util
import json
from pathlib import Path
import socket
import subprocess
import sys

owner = Path(__file__).resolve().parent
loader = importlib.machinery.SourceFileLoader('boundaries', str(owner / 'boundaries.py'))
spec = importlib.util.spec_from_loader(loader.name, loader)
mod = importlib.util.module_from_spec(spec)
loader.exec_module(mod)


class Probe(mod.Proof):
    def run_cases(self):
        cases = [
            ('empty-configured', '/Mine', {}, 'empty', ''),
            ('unrelated-configured', '/Mine', {'Mine/Photos/x.jpg': b'private photo fixture'}, 'empty', ''),
            ('unrelated-configured-fallback', '/Mine', {'Mine/Photos/x.jpg': b'private photo fixture', 'pixelelated/Content/ROMs/gb/A.gb': b'game fixture'}, 'found-elsewhere', '/pixelelated/Content'),
            ('tiered-configured', '/Mine', {'Mine/ROMs/gb/A.gb': b'game fixture', 'Mine/BIOS/qa.bin': b'bios fixture'}, 'ok', ''),
            ('tiered-explicit-root', '', {'ROMs/gb/A.gb': b'game fixture', 'BIOS/qa.bin': b'bios fixture'}, 'ok', ''),
            ('legacy-explicit-root', '', {'gb/A.gb': b'game fixture'}, 'ok', ''),
            ('unrelated-explicit-root', '', {'Photos/x.jpg': b'private photo fixture'}, 'empty', ''),
        ]
        for name, content, files, expected, found in cases:
            self.case = name
            print('START ' + name, flush=True)
            self.reset()
            self.conf('/pixelelated/Saves', '/pixelelated/Backups', content)
            self.on('a', 'mkdir -p /storage/roms/gb')
            for path, data in files.items():
                self.put(path, data)
            before = {'cloud': self.hashes(), 'pointers': self.pointers()}
            result = self.on('a', '/usr/bin/cloud_setup --content-location')
            facts = dict(line.split('=', 1) for line in result.stdout.splitlines() if '=' in line)
            after = {'cloud': self.hashes(), 'pointers': self.pointers()}
            mod.require(before == after, 'read-only classification mutated fixture')
            passed = facts.get('STATE') == expected and facts.get('FOUND') == found
            row = {'case': name, 'expected_state': expected, 'expected_found': found,
                   'facts': facts, 'before': before, 'after': after, 'rc': result.returncode,
                   'status': 'PASS' if passed else 'FAIL'}
            self.results.append(row)
            mod.save(self.logs / 'results.json', self.results)
            print(row['status'] + ' ' + name + ' expected=' + expected + ' actual=' + facts.get('STATE', '<missing>'), flush=True)
        for key, value in self.original_scripts.items():
            guest, script = key.split('/')
            mod.require(self.on(guest, 'sha256sum /usr/bin/' + script).stdout.split()[0] == value,
                        'installed bytes changed: ' + key)
        mod.save(self.logs / 'installed-unchanged.json', self.original_scripts)
        return 0 if all(x['status'] == 'PASS' for x in self.results) else 1

    def cleanup(self):
        # Current vm-pair down verifies exact owned disks with pidfds and waits.
        self.local('vm-pair', 'down')
        if self.backend_started:
            self.local('cloud-test-backend', 'down')
        for port in (9040, 10022, 10023, 5909, 5910):
            with socket.socket() as sock:
                mod.require(sock.connect_ex(('127.0.0.1', port)) != 0, 'owned port still open')
        mod.save(self.owner / 'cleanup.json', {'owned_guests_stopped': True, 'backend_stopped': True,
                                              'ports_unbound': [9040, 10022, 10023, 5909, 5910]})


if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('--tree', type=Path, required=True)
    p.add_argument('--image', type=Path, required=True)
    p.add_argument('--build-id', required=True)
    p.add_argument('--output', type=Path, required=True)
    proof = Probe(p.parse_args())
    try:
        proof.start()
        code = proof.run_cases()
    finally:
        proof.cleanup()
    sys.exit(code)

#!/usr/bin/env python3
"""Installed-image checks for the refutation packet's remaining bounded questions."""
import argparse
import importlib.machinery
import importlib.util
from pathlib import Path
import shlex
import sys
import time

owner = Path(__file__).resolve().parent
loader = importlib.machinery.SourceFileLoader('lead_base', str(owner / 'lead_base.py'))
spec = importlib.util.spec_from_loader(loader.name, loader)
base = importlib.util.module_from_spec(spec)
loader.exec_module(base)
mod = base.mod
QA = mod.QA


class Probe(base.Probe):
    def start(self):
        super().start()
        for script in ('cloud_sync_helper', 'cloud_content_restore'):
            digest = self.on('a', 'sha256sum /usr/bin/' + script).stdout.split()[0]
            mod.require(digest == mod.sha(self.tree / mod.SOURCES / script), 'installed script mismatch')
            self.original_scripts['a/' + script] = digest

    def stranded(self):
        self.current()
        self.put('gb/Root.gb', b'cloud root game\n')
        self.on('a', "mkdir -p /storage/roms/gb; printf 'local library witness\\n' > /storage/roms/gb/Local.gb")
        before = self.snapshot()
        facts = self.command('/usr/bin/cloud_setup --content-location')
        scan = self.command('/usr/bin/cloud_scan --content')
        listing = self.command('cat /storage/.cache/cloud_sync/scan/scan')
        after = self.snapshot()
        mod.require(before == after, 'read-only content scan mutated cloud/pointers')
        return {'before': before, 'facts': facts, 'scan': scan, 'listing': listing, 'after': after}

    def stock_helper(self):
        self.conf('/GAMES', '/GAMES/backup', None)
        self.put('gb/Root.gb', b'legacy root game\n')
        before = self.snapshot()
        helper = self.command('/usr/bin/cloud_sync_helper')
        mod.require(helper['rc'] == 0, 'helper failed')
        after = self.snapshot()
        mod.require(after['pointers']['CONTENT_REMOTE'] == '', 'top-level old layout did not retain root')
        mod.require(before['cloud'] == after['cloud'], 'helper changed cloud bytes')
        return {'before': before, 'helper': helper, 'after': after}

    def timeout_child(self):
        pidfile = QA + '/timeout-child.pid'
        child = 'sleep 30 & echo $! > ' + pidfile + '; wait'
        script = 'readlink -f "$(command -v timeout)"; timeout 1 sh -c ' + shlex.quote(child)
        script += '; result=$?; echo timeout_rc=$result; sleep 1; '
        script += f'pid=$(cat {pidfile}); echo child_pid=$pid; '
        script += 'if [ -r /proc/$pid/stat ]; then '
        script += 'cat /proc/$pid/stat; '
        script += 'if [ "$(cat /proc/$pid/comm)" = sleep ]; then kill -TERM "$pid" 2>/dev/null || :; fi; '
        script += 'else echo child_absent=yes; fi'
        result = self.command(script)
        mod.require('timeout_rc=124' in result['stdout'], 'timeout control did not fire')
        return result

    def outer_timeout(self):
        self.put('ROCKNIX/Saves/gb/A.srm', b'old save\n')
        self.put('pixelelated/.layout', b'layout=2\n')
        self.on('a', f'cp {QA}/rclone {QA}/rclone-original')
        shim = f'''#!/bin/sh
if [ "$1" = cat ] && [ "$2" = "{self.remote}/pixelelated/.layout" ]; then
 count=0
 [ ! -r {QA}/marker-read-count ] || read -r count < {QA}/marker-read-count
 count=$((count + 1))
 printf '%s\\n' "$count" > {QA}/marker-read-count
 if [ "$count" = 2 ]; then
  echo reached-second-marker-read > {QA}/outer-timeout-fired
  sleep 45
 fi
fi
exec {QA}/rclone-original "$@"
'''
        self.on('a', f'cat > {QA}/rclone; chmod 755 {QA}/rclone', data=shim)
        before = self.snapshot()
        start = time.monotonic()
        try:
            result = self.command('timeout 30 /usr/bin/cloud_scan --folder')
        finally:
            self.on('a', f'cp {QA}/rclone-original {QA}/rclone')
        elapsed = time.monotonic() - start
        self.on('a', f'test -s {QA}/outer-timeout-fired')
        mod.require(result['rc'] == 124, 'outer timeout boundary did not fire')
        after = self.snapshot()
        mod.require(before == after, 'stalled scan changed cloud/pointers')
        return {'before': before, 'result': result, 'seconds': elapsed, 'after': after}

    def run_cases(self):
        cases = [('R01-stranded-root', self.stranded), ('R02-stock-helper', self.stock_helper),
                 ('C03-timeout-child', self.timeout_child), ('R03-outer-timeout', self.outer_timeout)]
        for name, action in cases:
            self.case = name
            print('START ' + name, flush=True)
            self.reset()
            observation = action()
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

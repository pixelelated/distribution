"""Read-only, one-hour process snapshots for exactly five approved old trees.

No process/file/permission mutations. JSON lines go to stdout; the invoking
user's shell owns the redirected report. Stops when all five trees are gone,
after one hour, or when interrupted. This does not execute any removal.
"""
from pathlib import Path
import datetime
import hashlib
import json
import os
import time

ROOTS = ['/workspace/repos/rocknix.worktrees/m7-pixelelated-replacement' + n
         for n in ['03', '05', '06', '07', '08']]

def snapshot():
    hits, unreadable = [], []
    examined = kernel = gone = 0
    for p in Path('/proc').glob('[0-9]*'):
        try:
            fields = dict(line.split(':', 1) for line in (p / 'status').read_text().splitlines() if ':' in line)
        except FileNotFoundError:
            gone += 1
            continue
        if fields.get('Kthread', '').strip() == '1':
            kernel += 1
            continue
        examined += 1
        refs, failures = [], []
        for key in ['cwd', 'exe', 'root']:
            try:
                refs.append((key, os.readlink(p / key)))
            except FileNotFoundError:
                pass
            except PermissionError:
                failures.append(key)
        try:
            refs.extend(('argument', os.fsdecode(x)) for x in (p / 'cmdline').read_bytes().split(b'\0') if x)
        except FileNotFoundError:
            pass
        except PermissionError:
            failures.append('cmdline')
        try:
            for fd in (p / 'fd').iterdir():
                try:
                    refs.append(('fd', os.readlink(fd)))
                except FileNotFoundError:
                    pass
                except PermissionError:
                    failures.append('fd')
        except FileNotFoundError:
            pass
        except PermissionError:
            failures.append('fd-directory')
        try:
            for line in (p / 'maps').read_text().splitlines():
                parts = line.split(None, 5)
                if len(parts) == 6:
                    refs.append(('mapping', parts[5]))
        except FileNotFoundError:
            pass
        except PermissionError:
            failures.append('maps')
        matches = sorted({(kind, root) for kind, value in refs for root in ROOTS
                          if value == root or value.startswith(root + '/') or root + '/' in value})
        if matches:
            hits.append({'pid': int(p.name), 'references': [{'kind': k, 'tree': v} for k, v in matches]})
        if failures and p.exists():
            unreadable.append({'pid': int(p.name), 'fields': sorted(set(failures))})
    return {'utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
            'effective_uid': os.geteuid(), 'watcher_pid': os.getpid(),
            'roots': ROOTS, 'userspace_examined': examined,
            'kernel_threads_excluded': kernel, 'disappeared': gone,
            'matches': hits, 'unreadable': unreadable, 'readonly': True}

def main():
    if os.geteuid() != 0:
        raise SystemExit('This read-only process inspection requires sudo.')
    code_hash = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    deadline = time.monotonic() + 3600
    while time.monotonic() < deadline:
        report = snapshot()
        report['helper_sha256'] = code_hash
        report['all_five_directories_absent'] = not any(Path(p).exists() for p in ROOTS)
        print(json.dumps(report), flush=True)
        if report['all_five_directories_absent']:
            return
        time.sleep(5)
    raise SystemExit('Read-only watcher expired after one hour; refresh before any further removal.')

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        raise SystemExit(130)

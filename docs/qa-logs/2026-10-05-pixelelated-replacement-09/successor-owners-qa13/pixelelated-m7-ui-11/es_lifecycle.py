"""Candidate walk guard: retain actual ES lifetime and journal even on failure."""
from pathlib import Path
import json
import subprocess
import datetime


class Lifecycle:
    def __init__(self, ssh, output):
        self.ssh, self.output = ssh, Path(output)
        self.output.mkdir(parents=True, exist_ok=True)

    def snapshot(self, label):
        command = ('for p in /proc/[0-9]*/exe; do '
                   'case $(readlink "$p") in */emulationstation) '
                   'cat "${p%/exe}/stat";; esac; done')
        data = subprocess.check_output(self.ssh + [command], text=True, timeout=30)
        rows = data.splitlines()
        result = {'utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
                  'processes': []}
        for row in rows:
            prefix, fields = row.rsplit(') ', 1)
            result['processes'].append({'pid': int(prefix.split(' ', 1)[0]),
                                        'start_ticks': int(fields.split()[19])})
        (self.output / (label + '.json')).write_text(json.dumps(result, indent=2) + '\n')
        return result['processes']

    def __enter__(self):
        self.before = self.snapshot('before')
        assert len(self.before) == 1, 'expected exactly one installed ES process'
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        command = ("{ journalctl -b -u essway --no-pager -n 180; "
                   "tail -100 /var/log/es_log.txt 2>/dev/null; } "
                   "| grep -v -i -E 'key|pass|token|user|psk'")
        after = self.snapshot('after')
        log = subprocess.run(self.ssh + [command], text=True, capture_output=True, timeout=30)
        (self.output / 'journal.txt').write_text(log.stdout)
        same = after == self.before
        (self.output / 'result.json').write_text(json.dumps({
            'passed': same and exc_type is None and log.returncode == 0,
            'same_pid_and_start_ticks': same, 'journal_rc': log.returncode,
            'walk_exception': None if exc_type is None else exc_type.__name__
        }, indent=2) + '\n')
        assert same, 'ES restarted or disappeared during the menu walk; see lifecycle journal'
        assert log.returncode == 0, 'could not retain lifecycle journal'
        return False

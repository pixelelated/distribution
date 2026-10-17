#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-2.0
"""After admission/compile, run the actual diagnostic parser without GTK init.

Pass the target loader and its arguments before the binary when needed. These
checks do not load a provider, connect a display, or start the observer.
"""
import argparse
import json
import os
import subprocess
import time


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('command', nargs=argparse.REMAINDER,
                        help='[--] loader [loader args] binary OR binary')
    command = parser.parse_args().command
    if command[:1] == ['--']:
        command = command[1:]
    if not command:
        parser.error('a compiled diagnostic binary command is required')
    ua = ('Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/605.1.15 '
          '(KHTML, like Gecko) Version/60.5 Safari/605.1.15')
    cases = [
        ('defaults-off', {}, 0, 'ua=default observer=off'),
        ('desktop-off', {'QA616_UA': 'desktop'}, 0, 'ua=desktop observer=off'),
        ('observer-on', {'QA616_OBSERVER': 'on'}, 0, 'ua=default observer=on'),
        ('bounded-custom', {'QA616_UA': 'custom', 'QA616_CUSTOM_UA': ua}, 0, 'ua=custom observer=off'),
        ('invalid-mode', {'QA616_UA': 'unexpected'}, 78, None),
        ('invalid-observer', {'QA616_OBSERVER': 'true'}, 78, None),
        ('unknown-variable', {'QA616_OBSERVRE': 'on'}, 78, None),
        ('orphan-custom', {'QA616_CUSTOM_UA': ua}, 78, None),
        ('missing-custom', {'QA616_UA': 'custom'}, 78, None),
        ('oversize-custom', {'QA616_UA': 'custom', 'QA616_CUSTOM_UA': 'x' * 513}, 78, None),
        ('newline-custom', {'QA616_UA': 'custom', 'QA616_CUSTOM_UA': ua + '\n'}, 78, None),
        ('misstated-engine', {'QA616_UA': 'custom', 'QA616_CUSTOM_UA': ua.replace('Version/60.5', 'Chrome/143.0')}, 78, None),
    ]
    base = {key: value for key, value in os.environ.items()
            if not key.startswith('QA616_')}
    # Missing display deliberately proves validation runs before gtk_init.
    for name in ['DISPLAY', 'WAYLAND_DISPLAY']:
        base.pop(name, None)
    results = []
    started = time.monotonic()
    for name, values, expected, marker in cases:
        process = subprocess.run(command + ['--qa616-check'],
                                 env=base | values, capture_output=True,
                                 text=True, timeout=4)
        valid = (process.returncode == expected
                 and (marker is None or marker in process.stdout)
                 and ('QA616_CONFIG_ERROR ' in process.stderr if expected else not process.stderr)
                 and 'QA616_SAMPLE' not in process.stdout + process.stderr)
        results.append({'case': name, 'expected_exit': expected,
                        'actual_exit': process.returncode, 'pass': valid,
                        'stdout': process.stdout, 'stderr': process.stderr})
    print(json.dumps({'schema': 1, 'seconds': time.monotonic() - started,
                      'pass': all(item['pass'] for item in results),
                      'cases': results}, indent=2))
    return 0 if all(item['pass'] for item in results) else 1


if __name__ == '__main__':
    raise SystemExit(main())

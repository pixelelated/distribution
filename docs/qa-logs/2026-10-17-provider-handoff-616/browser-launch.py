#!/usr/bin/python3 -I
# SPDX-License-Identifier: GPL-2.0
"""UNRUN: temporary fresh-VM launcher; never install into a product image.

Bind this file over /usr/bin/cloud-signin-window only within the separately
admitted disposable guest. It execs the already verified helper with the exact
argv[0] the unchanged broker uses for its open/wait process detection.
"""
import hashlib
import json
import os
from pathlib import Path
import re
import stat
import sys
from urllib.parse import urlsplit

ROOT = Path('/storage/qa616-provider')
CONFIG = Path('/run/qa616-provider/current.json')
HELPER = ROOT / 'cloud-signin-window-GENERIC_X64'
HELPER_SHA256 = '530b0d2c7daf739eb061a415da4224a7affcec1b1837a452d182e97a03c16454'
BROKER_ARGV0 = '/usr/bin/cloud-signin-window'
HOSTS = {'dropbox': {'www.dropbox.com', 'dropbox.com'},
         'drive': {'accounts.google.com'},
         'onedrive': {'login.microsoftonline.com', 'login.live.com', 'onedrive.live.com'}}


def parse_case(raw):
    if len(raw) > 2048:
        raise ValueError('case configuration exceeds bound')
    value = json.loads(raw)
    if set(value) != {'id', 'provider', 'ua', 'observer'}:
        raise ValueError('unexpected case schema')
    if not isinstance(value['id'], str) or not re.fullmatch('[a-z0-9-]{1,64}', value['id']):
        raise ValueError('invalid fixed case identifier')
    if value['provider'] not in ['light', 'dropbox', 'drive', 'onedrive']:
        raise ValueError('unknown provider')
    if value['ua'] not in ['default', 'desktop'] or value['observer'] not in ['off', 'on']:
        raise ValueError('unsupported diagnostic mode')
    return value


def private_file(path, maximum):
    descriptor = os.open(path, os.O_RDONLY | os.O_NOFOLLOW)
    try:
        metadata = os.fstat(descriptor)
        if not stat.S_ISREG(metadata.st_mode) or metadata.st_uid != 0 or metadata.st_mode & 0o022:
            raise ValueError('input must be a root-owned non-writable regular file')
        if metadata.st_size > maximum:
            raise ValueError('input exceeds bound')
        with os.fdopen(descriptor, 'rb', closefd=False) as handle:
            return handle.read(maximum + 1)
    finally:
        os.close(descriptor)


def prepare_arguments(case, arguments):
    if len(arguments) < 2 or len(arguments) > 5 or len(arguments[0]) > 4096:
        raise ValueError('unexpected broker argument shape')
    url = urlsplit(arguments[0])
    backend = 'dropbox' if case['provider'] == 'light' else case['provider']
    if url.scheme != 'https' or url.hostname not in HOSTS[backend] or url.username or url.password:
        raise ValueError('authorization origin does not match the selected backend')
    # Keep the installed broker's optional hint and phone-keyboard arguments.
    # No shell expansion or reconstructed OAuth query is involved.
    tail = list(arguments[2:])
    if '--no-auto-keyboard' not in tail:
        raise ValueError('matrix requires the normal phone-keyboard route')
    index = 0
    while index < len(tail):
        if tail[index] == '--no-auto-keyboard':
            index += 1
        elif tail[index] == '--exit-hint' and index + 1 < len(tail) and len(tail[index + 1]) <= 128:
            index += 2
        else:
            raise ValueError('unexpected broker option')
    selected = list(arguments)
    if case['provider'] == 'light':
        # The real Dropbox authorize process still waits; only the page is
        # replaced by the fixed loopback control for this clearly named cell.
        selected[0] = 'http://127.0.0.1:18761/fixture?case=clean&case_id=' + case['id']
        selected[1] = '127.0.0.1'
    return [BROKER_ARGV0] + selected


def main(arguments):
    if os.geteuid() != 0 or os.uname().machine != 'x86_64':
        raise ValueError('fresh allocated x86_64 QA guest only')
    case = parse_case(private_file(CONFIG, 2048))
    helper = private_file(HELPER, 200000)
    if hashlib.sha256(helper).hexdigest() != HELPER_SHA256:
        raise ValueError('helper differs from compiled and qualified bytes')
    argv = prepare_arguments(case, arguments)
    launch_dir = ROOT / 'launches'
    metadata = launch_dir.lstat()
    if not stat.S_ISDIR(metadata.st_mode) or metadata.st_uid != 0 or metadata.st_mode & 0o077:
        raise ValueError('launch receipt directory must be private and root-owned')
    identity = Path('/proc/self/stat').read_text().rsplit(')', 1)[1].split()
    receipt = {'schema': 1, 'case': case, 'pid': os.getpid(), 'start': int(identity[19]),
               'helper_sha256': HELPER_SHA256, 'exec_argv0': BROKER_ARGV0,
               'private_oauth_url_recorded': False, 'page_replaced_for_light_control': case['provider'] == 'light'}
    # Exclusive receipt: a repeated launch needs a fresh explicit case ID.
    with (launch_dir / (case['id'] + '.json')).open('x') as handle:
        json.dump(receipt, handle, indent=2)
        handle.write('\n')
    environment = {key: value for key, value in os.environ.items() if not key.startswith('QA616_')}
    environment.update(QA616_UA=case['ua'], QA616_OBSERVER=case['observer'])
    os.execve(HELPER, argv, environment)


if __name__ == '__main__':
    try:
        main(sys.argv[1:])
    except (OSError, ValueError, TypeError, KeyError) as error:
        # Fixed validation messages only; no argv, URL, environment or body.
        print('QA616_LAUNCH_REFUSED ' + type(error).__name__, file=sys.stderr)
        raise SystemExit(78)

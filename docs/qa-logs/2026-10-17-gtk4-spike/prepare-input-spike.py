#!/usr/bin/env python3
"""Stage a tiny source-only native-input probe; never compile or launch it."""
import argparse
import ast
import hashlib
import json
from pathlib import Path
import subprocess

PACKET = Path(__file__).resolve().parent

def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--repo', type=Path, required=True)
    ap.add_argument('--output', type=Path, required=True)
    args = ap.parse_args()
    inputs = json.loads((PACKET / 'inputs.json').read_text())
    path = 'projects/ROCKNIX/packages/network/rclone/sources/cloud_oauth'
    source = subprocess.check_output(['git', '-C', str(args.repo), 'show', inputs['source_ref'] + ':' + path])
    if hashlib.sha256(source).hexdigest() != inputs['source_sha256'][path]:
        raise SystemExit('source binding mismatch')
    text = source.decode()
    parsed = ast.parse(text)
    keyboard = next(n for n in parsed.body if isinstance(n, ast.ClassDef) and n.name == 'RemoteKeyboard')
    start = text.index('EV_SYN, EV_KEY =')
    end = text.index('\n\nclass RemoteMouse:', start)
    constants = text[start:end]
    # No product module import: this retains only literal mappings and one class.
    body = ('# SPDX-License-Identifier: GPL-2.0-only\n'
            '# Derived from pixelelated cloud_oauth; original ROCKNIX credits retained.\n'
            '# Copyright (C) 2026-present ROCKNIX (https://github.com/ROCKNIX)\n'
            'import os, fcntl, struct, time\n'
            'UINPUT = "/dev/uinput"\n'
            'def log(message):\n    print("native keyboard status event", flush=True)\n\n'
            + constants + '\n\n' + ast.get_source_segment(text, keyboard) + '\n')
    ast.parse(body)
    output = args.output.absolute()
    if output.exists() or not output.parent.is_dir():
        raise SystemExit('output must be a new directory under an existing allocated parent')
    output.mkdir(mode=0o700)
    files = {'native_keyboard.py': body.encode(), 'input-spike.c': (PACKET / 'input-spike.c').read_bytes(),
             'run-input-spike.py': (PACKET / 'run-input-spike.py').read_bytes()}
    for name, data in files.items():
        (output / name).write_bytes(data)
    receipt = {'source_ref': inputs['source_ref'], 'producer_sha256': hashlib.sha256(source).hexdigest(),
               'files': {name: hashlib.sha256(data).hexdigest() for name, data in files.items()},
               'compiler_invoked': False, 'runtime_invoked': False}
    (output / 'preparation.json').write_text(json.dumps(receipt, indent=2) + '\n')
    print(json.dumps(receipt))

if __name__ == '__main__':
    main()

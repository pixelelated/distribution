#!/usr/bin/env python3
"""Configure the disposable guest's existing Dolphin INI with an exact-input backup."""
import argparse
import configparser
import hashlib
import io
import os
from pathlib import Path

p = argparse.ArgumentParser(description=__doc__)
p.add_argument('ini', type=Path)
p.add_argument('sd_image', type=Path)
p.add_argument('--expected-ini-sha256', required=True)
a = p.parse_args()
if a.ini.is_symlink() or not a.ini.is_file():
    p.error('expected a regular existing INI inside disposable storage')
raw = a.ini.read_bytes()
if hashlib.sha256(raw).hexdigest() != a.expected_ini_sha256:
    p.error('INI input changed')
if a.sd_image.is_symlink() or not a.sd_image.is_file() or a.sd_image.stat().st_size != 134217728:
    p.error('expected prepared regular 128 MiB SD image')
c = configparser.ConfigParser(interpolation=None, strict=True)
c.optionxform = str
c.read_string(raw.decode())
for section, values in {
    'General': {'WiiSDCardPath': str(a.sd_image.resolve())},
    'Core': {'WiiSDCard': 'True', 'WiiSDCardAllowWrites': 'True',
             'WiiSDCardEnableFolderSync': 'False'},
}.items():
    if not c.has_section(section):
        c.add_section(section)
    for key, value in values.items():
        c.set(section, key, value)
backup = a.ini.with_name(a.ini.name + '.before-m7-homebrew')
with backup.open('xb') as f:
    f.write(raw)
os.chmod(backup, 0o600)
out = io.StringIO()
c.write(out)
a.ini.write_text(out.getvalue())
print('INI configured; exact original retained at', backup)

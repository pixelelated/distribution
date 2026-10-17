#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-2.0
"""Prepare diagnostic source only. Does not compile, run, or contact a provider."""
import argparse
import hashlib
import json
from pathlib import Path

BASE_SHA256 = '39af3e041d9871c4fb636cff71934ddf3ea13c690002e77af5ea6d82d8fff4f8'
BASE_COMMIT = '077197e6cd3ea31f33b28aaf3882a694b3423b53'


def digest(data):
    return hashlib.sha256(data).hexdigest()


def prepare(base, output):
    packet = Path(__file__).resolve().parent
    original = base.read_bytes()
    if digest(original) != BASE_SHA256:
        raise ValueError('base source hash differs from reviewed frozen source')
    instrument = (packet / 'diagnostic.c.in').read_text()
    observer = (packet / 'observer.js').read_text()
    if instrument.count('@OBSERVER_JS@') != 1:
        raise ValueError('observer insertion marker changed')
    instrument = instrument.replace('@OBSERVER_JS@', json.dumps(observer, ensure_ascii=True))
    text = original.decode('utf-8')
    replacements = [
        ('static const char *allowed_host = NULL;',
         instrument + '\nstatic const char *allowed_host = NULL;'),
        ('int main(int argc, char **argv)\n{\n',
         'int main(int argc, char **argv)\n{\n'
         '    if (!qa616_config()) return 78;\n'
         '    if (argc == 2 && !strcmp(argv[1], "--qa616-check")) {\n'
         '        g_print("QA616_CONFIG_VALID ua=%s observer=%s\\n",\n'
         '            qa616_ua_mode, qa616_observe ? "on" : "off");\n'
         '        return 0;\n'
         '    }\n'),
        ('    webkit_web_view_load_uri(view, argv[1]);',
         '    if (!qa616_setup(view)) return 78;\n'
         '    webkit_web_view_load_uri(view, argv[1]);')
    ]
    for anchor, replacement in replacements:
        if text.count(anchor) != 1:
            raise ValueError('source insertion anchor is not unique')
        text = text.replace(anchor, replacement, 1)
    source = text.encode('utf-8')
    # Exclusive directory prevents silently replacing an admitted/running input.
    output.mkdir(mode=0o700)
    (output / 'cloud-signin-window.c').write_bytes(source)
    provenance = {
        'schema': 1, 'issue': 616, 'status': 'source-prepared; compile/runtime unrun',
        'base_commit': BASE_COMMIT, 'base_source_sha256': BASE_SHA256,
        'diagnostic_source_sha256': digest(source),
        'inputs': {name: digest((packet / name).read_bytes())
                   for name in ['prepare.py', 'diagnostic.c.in', 'observer.js']},
        'changes': ['configuration validation before GTK initialization',
                    'diagnostic definitions before original globals',
                    'UA/optional observer setup before original first navigation'],
        'defaults': {'ua': 'default', 'observer': 'off'},
        'unchanged': ['viewport', 'zoom', 'native OSK', 'popups', 'handoff',
                      'ephemeral context', 'navigation restrictions', 'DMABuf environment policy']
    }
    (output / 'provenance.json').write_text(json.dumps(provenance, indent=2) + '\n')
    return provenance


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--base', type=Path, required=True)
    parser.add_argument('--out', type=Path, required=True,
                        help='new directory under an owned scratch root; must not exist')
    args = parser.parse_args()
    try:
        result = prepare(args.base, args.out)
    except (OSError, ValueError, UnicodeError) as error:
        parser.exit(2, f'preparation refused: {error}\n')
    print(json.dumps(result, indent=2))

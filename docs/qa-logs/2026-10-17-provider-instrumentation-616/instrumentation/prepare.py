#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-2.0
"""Generate exact-source candidate only; no compiler, target or network execution."""
import argparse
import hashlib
import json
from pathlib import Path

PRODUCT = '39af3e041d9871c4fb636cff71934ddf3ea13c690002e77af5ea6d82d8fff4f8'
TEMPLATE = '5dcb8a9a2b5e3d07b0481c194654d8c5cba9c600388d23a91884d6e182d81454'
OBSERVER = '54b3dfd60756fc00c65ca3f31d0e0fa306d2822adc3548d269687148f654f63d'
PRIOR_DIAGNOSTIC = 'c892ba759c81c9083512017c56aca240929e8afaa2db40f97be26fb87eb60202'


def digest(data):
    return hashlib.sha256(data).hexdigest()


def checked(path, expected):
    data = path.read_bytes()
    if digest(data) != expected:
        raise ValueError('reviewed source hash mismatch')
    return data.decode()


def replace_once(source, old, new):
    if source.count(old) != 1:
        raise ValueError('source anchor is not unique')
    return source.replace(old, new, 1)


def prepare(repo, output):
    packet = Path(__file__).resolve().parent
    old = repo / 'docs/qa-logs/2026-10-17-browser-controls-616'
    base = checked(repo / 'projects/ROCKNIX/packages/network/cloud-signin-window/sources/cloud-signin-window.c', PRODUCT)
    template = checked(old / 'diagnostic.c.in', TEMPLATE)
    observer = checked(old / 'observer.js', OBSERVER)
    instrumentation = replace_once(template, '@OBSERVER_JS@', json.dumps(observer, ensure_ascii=True))
    prior = replace_once(base, 'static const char *allowed_host = NULL;', instrumentation + '\nstatic const char *allowed_host = NULL;')
    prior = replace_once(prior, 'int main(int argc, char **argv)\n{\n',
        'int main(int argc, char **argv)\n{\n'
        '    if (!qa616_config()) return 78;\n'
        '    if (argc == 2 && !strcmp(argv[1], "--qa616-check")) {\n'
        '        g_print("QA616_CONFIG_VALID ua=%s observer=%s\\n",\n'
        '            qa616_ua_mode, qa616_observe ? "on" : "off");\n'
        '        return 0;\n'
        '    }\n')
    prior = replace_once(prior, '    webkit_web_view_load_uri(view, argv[1]);',
                         '    if (!qa616_setup(view)) return 78;\n    webkit_web_view_load_uri(view, argv[1]);')
    if digest(prior.encode()) != PRIOR_DIAGNOSTIC:
        raise ValueError('prior diagnostic reconstruction differs from compiled input')
    proof = replace_once((packet / 'proof.c.in').read_text(), '@PROOF_JS@',
                         json.dumps((packet / 'proof.js').read_text(), ensure_ascii=True))
    candidate = replace_once(prior, 'static gboolean qa616_setup(WebKitWebView *view)\n',
                              proof + '\nstatic gboolean qa616_setup(WebKitWebView *view)\n')
    candidate = replace_once(candidate, '    if (!qa616_observe) return TRUE;',
                             '    if (!qa616_proof_setup(view)) return FALSE;\n    if (!qa616_observe) return TRUE;')
    candidate = replace_once(candidate, '    if (!qa616_config()) return 78;',
        '    if (g_getenv("CLOUD_SIGNIN_DEBUG")) {\n'
        '        qa616_refuse("product debug logging must be unset");\n'
        '        return 78;\n'
        '    }\n'
        '    if (!qa616_config()) return 78;')
    result = {'schema': 1, 'status': 'source prepared; compile/runtime UNRUN',
              'product_source_sha256': PRODUCT, 'prior_diagnostic_sha256': PRIOR_DIAGNOSTIC,
              'candidate_sha256': digest(candidate.encode()),
              'input_hashes': {name: digest((packet / name).read_bytes())
                              for name in ['prepare.py', 'proof.c.in', 'proof.js']},
              'changed_scope': ['main-document request/response/error callbacks',
                                'always-on isolated-world one-shot DOM UA proof',
                                'up to eight numeric trusted/untrusted input probes per document',
                                'refuse product debug mode before GTK initialization'],
              'unchanged': ['UA modes', 'periodic observer flag and code', 'viewport/zoom',
                            'native input/OSK', 'ephemeral context', 'broker argv protocol',
                            'navigation restrictions', 'product sources/pins']}
    output.mkdir(mode=0o700)
    (output / 'cloud-signin-window.c').write_text(candidate)
    (output / 'provenance.json').write_text(json.dumps(result, indent=2) + '\n')
    return result


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--repo', type=Path, required=True)
    parser.add_argument('--out', type=Path, required=True)
    args = parser.parse_args()
    try:
        print(json.dumps(prepare(args.repo, args.out), indent=2))
    except (OSError, ValueError, UnicodeError) as error:
        parser.exit(2, 'source preparation refused: ' + str(error) + '\n')

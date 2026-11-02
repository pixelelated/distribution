#!/usr/bin/env python3
"""T44 immutable input binding. Reads Git objects; writes metadata, never sources.

Selector grammar independently reproduced by P1's retained derive.py. This
reader does not execute renovation-inventory, a recipe, or an accepted test.
"""
import argparse
import collections
import functools
import hashlib
import json
from pathlib import Path
import re
import subprocess

P1 = '2174265e9cc1b248c0fbe27fa101875984d46d6b'
SURVEY = '16dbac5211eea7e70db7394372033be2be7df829'
PRIMARY = '55158d2a64c69fe295fb4e67fd174424a71b1b4d'
ACCEPTED = {
    'T21': '3ae9610b0f3fb61d23eb6a2c3459ad19f962e2b1',
    'T34': '52f0ff5128cf96bfcdec9082ded75347ecea11e6',
    'T35': 'b7fdb3a24c859ce91f9fd381bb0956901b8d23cb',
    'T36': '9c1bd5f093cfc1ccd42640282226b7b970442ef1',
}
INPUTS = ['docs/reviews/areas.json', 'docs/reviews/slices.json',
          'docs/reviews/inventory.json', 'docs/reviews/inventory.md',
          'docs/reviews/order.md', 'tools/renovation-inventory']
RECIPE = 'projects/ROCKNIX/packages/ui/emulationstation/package.mk'
FR = 'locale/lang/fr/LC_MESSAGES/emulationstation2.po'
ADDITIONS = ['tests/launch-play-through.py', 'tests/main-parse-args.py',
             'tests/system-scan-assets.py']
PREP = Path(__file__).parent / 't44-preparation' / 'membership'


def sha(data):
    return hashlib.sha256(data).hexdigest()


def git(repo, *args):
    return subprocess.check_output(['git', '-C', str(repo), *args])


def blob(repo, ref, path):
    return git(repo, 'show', ref + ':' + path)


def tree(repo, ref):
    result = {}
    for row in git(repo, 'ls-tree', '-r', '-z', ref).split(b'\0'):
        if row:
            meta, path = row.split(b'\t', 1)
            mode, kind, oid = meta.decode().split()
            result[path.decode()] = dict(mode=mode, object_type=kind, oid=oid)
    return result


def expand(glob):
    if '{' not in glob:
        return [glob]
    left = glob.index('{')
    right = glob.index('}', left)
    return [p for alt in glob[left + 1:right].split(',')
            for p in expand(glob[:left] + alt + glob[right + 1:])]


@functools.lru_cache(None)
def regex(glob):
    output = ''
    i = 0
    while i < len(glob):
        if glob[i:i + 3] == '**/':
            output += '(?:.*/)?'
            i += 3
        elif glob[i:i + 2] == '**':
            output += '.*'
            i += 2
        elif glob[i] == '*':
            output += '[^/]*'
            i += 1
        elif glob[i] == '?':
            output += '[^/]'
            i += 1
        else:
            output += re.escape(glob[i])
            i += 1
    return re.compile(output + r'\Z')


def globmatch(glob, row):
    source = 'es' if glob.startswith('es:') else 'distribution'
    if source == 'es':
        glob = glob[3:]
    return source == row['tree'] and any(regex(g).match(row['path']) for g in expand(glob))


def match(select, sliced, row):
    if row['area'] not in select.get('areas', [sliced['area']]):
        return False
    for key in ['reach', 'tier']:
        if select.get(key) and row[key] not in select[key]:
            return False
    globs = select.get('globs')
    return globs is None or (
        any(globmatch(g, row) for g in globs if not g.startswith('!')) and
        not any(globmatch(g[1:], row) for g in globs if g.startswith('!')))


def derive(args):
    inputs = {}
    for path in [*INPUTS, RECIPE]:
        expected = blob(args.repo, P1, path)
        assert blob(args.repo, args.ref, path) == expected, 'distribution input drift: ' + path
        inputs[path] = sha(expected)
    inv = json.loads(blob(args.repo, P1, INPUTS[2]))
    slices = json.loads(blob(args.repo, P1, INPUTS[1]))['slices']
    selectors = [(s, x) for s in slices for x in
                 (s['select'] if isinstance(s['select'], list) else [s['select']])]
    native = []
    excluded = []
    for raw in inv['rows']:
        row = dict(zip(inv['columns'], raw))
        if row['area'] != 'interface':
            continue
        direct = {s['id'] for s, x in selectors if not x.get('rest') and match(x, s, row)}
        owners = direct or {s['id'] for s, x in selectors if x.get('rest') and match(x, s, row)}
        assert len(owners) == 1, ('ambiguous ownership', row['path'], owners)
        if owners == {'es-vendored-and-data'}:
            native.append(row)
        elif row['tree'] == 'es' and not row['path'].startswith(('es-app/', 'es-core/')):
            excluded.append(dict(path=row['path'], owners=sorted(owners)))
    native.sort(key=lambda r: r['path'])
    assert len(native) == 594 and len(excluded) == 9
    survey_manifest_bytes = (PREP / 'manifest.json').read_bytes()
    assert sha(survey_manifest_bytes) == '16b1da3ad4a7e4b3c7a6aadbd901c2502c940d20da697136babc27474d767965'
    survey_manifest = {r['path']: r for r in json.loads(survey_manifest_bytes)['entries']}
    assert [r['path'] for r in native] == sorted(survey_manifest)
    s = tree(args.es_repo, SURVEY)
    p = tree(args.es_repo, PRIMARY)
    expected_es_tree = git(args.es_repo, 'rev-parse', PRIMARY + '^{tree}').decode().strip()
    actual_es_tree = git(args.es_repo, 'rev-parse', args.es_ref + '^{tree}').decode().strip()
    assert actual_es_tree == expected_es_tree, 'ES root tree differs from accepted T2 primary'
    actual = tree(args.es_repo, args.es_ref)
    assert actual == p, 'ES seed tree differs from accepted T2 primary'
    result = []
    for row in native:
        path = row['path']
        old = survey_manifest[path]
        assert all(old[k] == s[path][k] for k in ['mode', 'object_type', 'oid']), path
        assert all(old[k] == row[k] for k in ['tier', 'tier_note', 'language']), path
        assert old['inventory_lines'] == row['lines'], path
        assert p[path]['mode'] == s[path]['mode'], path
        data = None if p[path]['object_type'] == 'commit' else blob(args.es_repo, PRIMARY, path)
        text = data is not None and old['kind'] == 'text'
        result.append(dict(path=path, survey=old, primary={**p[path],
            'sha256': sha(data) if data is not None else None,
            'bytes': len(data) if data is not None else None,
            'text_logical_lines': data.count(b'\n') + int(bool(data) and not data.endswith(b'\n')) if text else None,
            'newline_bytes': data.count(b'\n') if text else None},
            changed_since_survey=s[path] != p[path]))
    outside = lambda t: {k: v for k, v in t.items() if not k.startswith(('es-app/', 'es-core/'))}
    outside_s = outside(s)
    outside_p = outside(p)
    assert sorted(outside_p.keys() - outside_s.keys()) == ADDITIONS
    assert not outside_s.keys() - outside_p.keys()
    changed = [r['path'] for r in result if r['changed_since_survey']]
    assert len(changed) == 40
    assert {k for k in outside_s if outside_s[k] != outside_p[k]} == set(changed)
    additions = []
    for path in ADDITIONS:
        data = blob(args.es_repo, PRIMARY, path)
        additions.append(dict(path=path, owner='T2 #649; T44 table coverage only', **p[path],
            sha256=sha(data), bytes=len(data), text_logical_lines=data.count(b'\n') + int(not data.endswith(b'\n'))))
    companions = []
    for owner, ref in ACCEPTED.items():
        t = tree(args.es_repo, ref)
        o = outside(t)
        assert o.keys() == outside_s.keys(), owner
        differences = sorted(k for k in o if o[k] != outside_s[k])
        assert differences == ([] if owner == 'T36' else [FR]), owner
        ancestor = subprocess.run(['git', '-C', str(args.es_repo), 'merge-base', '--is-ancestor', PRIMARY, ref], capture_output=True)
        assert ancestor.returncode == 1, 'accepted branch ancestry changed'
        data = blob(args.es_repo, ref, FR)
        companions.append(dict(owner=owner, ref=ref, native_different_from_survey=differences,
            contains_primary=False, french={**t[FR], 'sha256': sha(data), 'bytes': len(data)},
            external_tree=git(args.es_repo, 'rev-parse', ref + ':external').decode().strip()))
        assert git(args.es_repo, 'rev-parse', ref + ':external') == git(args.es_repo, 'rev-parse', SURVEY + ':external')
    assert git(args.es_repo, 'rev-parse', PRIMARY + ':external') == git(args.es_repo, 'rev-parse', SURVEY + ':external')
    source_lines = sum(r['primary']['text_logical_lines'] or 0 for r in result)
    summary = dict(distribution_ref=args.ref, es_ref=args.es_ref, P1=P1, survey=SURVEY,
        primary=PRIMARY, primary_tree=expected_es_tree, actual_es_tree=actual_es_tree,
        distribution_inputs=inputs, native_paths=len(result), inventory_lines=sum(r['lines'] or 0 for r in native),
        survey_text_lines=sum(r['survey']['text_logical_lines'] or 0 for r in result),
        primary_text_lines=source_lines, primary_newline_bytes=sum(r['primary']['newline_bytes'] or 0 for r in result),
        primary_blob_bytes=sum(r['primary']['bytes'] or 0 for r in result),
        survey_tiers=dict(collections.Counter(r['tier'] for r in native)),
        modes=dict(collections.Counter(r['primary']['mode'] for r in result)),
        kinds=dict(collections.Counter(r['survey']['kind'] for r in result)),
        changed_native=len(changed), unchanged_native=len(result)-len(changed), changed_paths=changed,
        additions=len(additions), addition_text_lines=sum(r['text_logical_lines'] for r in additions),
        excluded_nonrest=excluded, companion_branches=len(companions),
        limits='No combined accepted tree, installed behavior, current upstream release or completed source audit is asserted.')
    return {'native.json': result, 'additions.json': additions,
            'companions.json': companions, 'summary.json': summary}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--repo', type=Path, required=True)
    parser.add_argument('--ref', required=True)
    parser.add_argument('--es-repo', type=Path, required=True)
    parser.add_argument('--es-ref', default=PRIMARY)
    parser.add_argument('--out', type=Path, required=True)
    args = parser.parse_args()
    assert not args.out.exists(), 'output must be a new directory'
    outputs = derive(args)
    args.out.mkdir(parents=True)
    for name, value in outputs.items():
        (args.out / name).write_text(json.dumps(value, sort_keys=True, indent=2) + '\n')
    print(json.dumps(outputs['summary.json'], sort_keys=True, indent=2))


if __name__ == '__main__':
    main()

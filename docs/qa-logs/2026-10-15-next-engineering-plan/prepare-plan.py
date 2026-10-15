#!/usr/bin/env python3
"""Materialize small plans only. Does not reserve, copy, compile, or submit work."""
import argparse
import datetime
import hashlib
import json
from pathlib import Path
import re
import subprocess

PARENT = Path('/workspace/repos/rocknix.worktrees/m7-p5-build-20261014-02')
ROOT = 'build.pixelelated-GENERIC_X64.x86_64'
CONTAINER = '/workspace/repos/rocknix.worktrees/m7-pixelelated'
GIB = 1024 ** 3

TEMPLATE_COMMIT = '956f9481872d3d64f3e33d495e5ab25dfd9aaefd'
PRODUCT_PATHS = ['projects/ROCKNIX/packages/emulators/standalone/dolphin-sa/package.mk', 'projects/ROCKNIX/packages/emulators/standalone/dolphin-sa/patches/018-nogui-achievements-lifecycle.patch', 'projects/ROCKNIX/packages/virtual/emulators/sources/Install Steam.sh']
PRODUCT_SHA256 = {'projects/ROCKNIX/packages/emulators/standalone/dolphin-sa/package.mk': '27ab9954ec5fb30aefb51555281c749aea416f2d3bb8fc0138d0964730e5a153', 'projects/ROCKNIX/packages/emulators/standalone/dolphin-sa/patches/018-nogui-achievements-lifecycle.patch': 'bc1d04f688f85ff3fc49a81fa40625d08c8f7839aa81e46baee6b50b443ee5f0', 'projects/ROCKNIX/packages/virtual/emulators/sources/Install Steam.sh': 'cefb22a50db915be1637e682dfba047789b276144bbe707220a2b4117c7a3264'}
PRODUCT_ROOTS = ['packages', 'projects', 'config', 'scripts', 'distributions', 'Makefile']


def git(root, *args):
    return subprocess.check_output(['git', '-C', str(root), *args], text=True).strip()


def write(path, value):
    with path.open('x') as f:
        json.dump(value, f, indent=2)
        f.write('\n')


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--checkout', type=Path, required=True)
    p.add_argument('--commit', required=True)
    p.add_argument('--dolphin-recipe-sha256', required=True, help='Independently reviewed final Dolphin recipe SHA256; only this product input may differ from the template')
    p.add_argument('--expected-es', required=True, help='Exact reviewed ES commit required in the frozen distribution recipe')
    p.add_argument('--measurement', type=Path, required=True)
    p.add_argument('--owner', type=Path, required=True)
    p.add_argument('--stage', choices=['transfer', 'build'], required=True)
    a = p.parse_args()
    tree = a.checkout.resolve(strict=True)
    owner = a.owner.resolve(strict=True)
    measurement = a.measurement.resolve(strict=True)
    assert str(tree) == '/workspace/repos/rocknix.worktrees/m7-p5-build-20261015-01'
    assert re.fullmatch('[0-9a-f]{40}', a.commit)
    assert re.fullmatch('[0-9a-f]{64}', a.dolphin_recipe_sha256)
    product_sha256 = dict(PRODUCT_SHA256)
    product_sha256['projects/ROCKNIX/packages/emulators/standalone/dolphin-sa/package.mk'] = a.dolphin_recipe_sha256
    assert re.fullmatch('[0-9a-f]{40}', a.expected_es)
    assert git(tree, 'rev-parse', 'HEAD') == a.commit
    assert git(tree, 'branch', '--show-current') == 'build/m7-p5-20261015-01'
    assert not git(tree, 'status', '--porcelain'), 'freeze a clean source first'
    assert set(git(tree, 'diff', '--name-only', TEMPLATE_COMMIT, a.commit, '--', *PRODUCT_ROOTS).splitlines()) <= {'projects/ROCKNIX/packages/emulators/standalone/dolphin-sa/package.mk'}, 'additional product inputs changed: review/reseal first'
    assert git(tree, 'diff', '--name-only', 'fac608ff89940ce358ea9b8a95e9a08a6fe26568', a.commit, '--', *PRODUCT_ROOTS).splitlines() == PRODUCT_PATHS
    assert all(hashlib.sha256((tree / path).read_bytes()).hexdigest() == digest for path, digest in product_sha256.items())
    assert git(tree, 'merge-base', '--is-ancestor', a.commit, 'origin/next') == ''
    recipe = tree / 'projects/ROCKNIX/packages/ui/emulationstation/package.mk'
    recipe_bytes = recipe.read_bytes()
    assert re.findall(r'^\s*PKG_VERSION=(.*)$', recipe_bytes.decode(), re.M) == ['"' + a.expected_es + '"'], 'expected exact ES pin missing or ambiguous'
    es_recipe_sha256 = hashlib.sha256(recipe_bytes).hexdigest()
    for patch in ['020-rvz-padding-preserve-partial-word.patch', '021-flush-reconnect-during-startup.patch']:
        assert (tree / 'projects/ROCKNIX/packages/network/raofflineproxy/patches' / patch).is_file()
    assert owner.is_dir() and owner.stat().st_dev == tree.stat().st_dev
    m = json.loads(measurement.read_text())
    age = datetime.datetime.now(datetime.timezone.utc) - datetime.datetime.fromisoformat(m['utc_finish'])
    assert 0 <= age.total_seconds() <= 86400, 'refresh current allocation measurement'
    allocated = {r['path']: r['allocated_bytes'] for r in m['measurements']}
    base = allocated[str(PARENT / ROOT)]
    assert m['parent_head'] == 'fac608ff89940ce358ea9b8a95e9a08a6fe26568'
    assert hashlib.sha256(Path(m['original_allocation_log']).read_bytes()).hexdigest() == m['original_allocation_log_sha256']
    assert base > 0 and str(PARENT / 'target') in allocated
    assert '/workspace/cache/rocknix-sources' in allocated
    scan = owner / 'empty-retention-scan'
    scan.mkdir()
    terms = ({'custody_receipts_and_metadata': 1 * GIB, 'operating_margin': 64 * GIB}
             if a.stage == 'transfer' else
             {'additional_warm_package_growth': max(base // 3, 32 * GIB),
              'source_download_growth': 8 * GIB, 'firmware_outputs': 16 * GIB,
              'immediate_clean_and_upgrade_qa': 32 * GIB, 'operating_margin': 64 * GIB})
    stage = 'm7-dolphin018-' + a.stage
    retention = {'volume': '/workspace', 'scan_roots': [str(scan)], 'reference_stores': [],
                 'protected': [str(PARENT), str((PARENT if a.stage == 'transfer' else tree) / ROOT), str(PARENT / 'target'),
                               '/workspace/cache/rocknix-sources', str(measurement)],
                 'candidates': [], 'builds': [{'name': stage, 'terms_bytes': terms,
                     'basis': 'Completed predecessor final quiescent allocation sample plus explicit growth/QA/margin allowances. '
                              'Existing source cache and parent payloads already reduce f_bavail; no reclamation counted. '
                              'No deletion candidates; the empty explicit scan is not historical-volume classification.',
                     'evidence': [{'path': str(measurement), 'sha256': hashlib.sha256(measurement.read_bytes()).hexdigest()},
                                  {'path': m['original_allocation_log'], 'sha256': m['original_allocation_log_sha256']}]}]}
    outputs = [{'path': str(tree / ROOT), 'issue': 584, 'kind': 'build-cache',
                'release_when': 'Immediately queued assembled-image qualification and required corresponding-source custody accepted'}]
    if a.stage == 'build':
        outputs += [{'path': str(tree / n), 'issue': 584, 'kind': 'firmware',
                     'release_when': 'Clean and retained-storage engineering qualification and compact image/source record accepted; review next immediate consumer'}
                    for n in ['release', 'target']]
        outputs += [{'path': str(tree / n), 'issue': 493, 'kind': 'qa-scratch',
                     'release_when': 'Original results consumed and compact build records retained; generated staging no longer needed'}
                    for n in ['.doc_cache', '.es_cache', '.build-runs']]
    outputs += [{'path': str(owner), 'issue': 493, 'kind': 'qa-scratch',
                 'release_when': 'Original results consumed and compact evidence retained; preserve required corresponding-source inputs'}]
    admission = {'checkout': str(tree), 'container_checkout': CONTAINER,
                 'retention_plan': str(owner / 'retention-plan.json'),
                 'retention_report': str(owner / 'retention-report.json'), 'stage': stage,
                 'profiles': [{'PROJECT': 'ROCKNIX', 'DEVICE': 'GENERIC_X64', 'ARCH': 'x86_64'}],
                 'outputs': outputs}
    write(owner / 'retention-plan.json', retention)
    write(owner / 'admission-plan.json', admission)
    write(owner / 'planning-inputs.json', {'commit': a.commit, 'tree': git(tree, 'rev-parse', 'HEAD^{tree}'),
          'es_commit': a.expected_es, 'es_recipe_sha256': es_recipe_sha256, 'product_sha256': product_sha256,
          'warm_parent': str(PARENT), 'container_checkout': CONTAINER,
          'stage': stage, 'required_bytes': sum(terms.values()), 'admission_prepared': False})
    print(json.dumps({'owner': str(owner), 'required_bytes': sum(terms.values()),
                      'next': 'watched retention-report, then fresh admission prepare and submit'}))


if __name__ == '__main__':
    main()

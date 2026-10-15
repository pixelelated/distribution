#!/usr/bin/env python3
"""Materialize small plans only. Does not reserve, copy, compile, or submit work."""
import argparse
import datetime
import hashlib
import json
from pathlib import Path
import re
import subprocess

PARENT = Path('/workspace/repos/rocknix.worktrees/m7-p5-build-20261014-01')
ROOT = 'build.pixelelated-GENERIC_X64.x86_64'
CONTAINER = '/workspace/repos/rocknix.worktrees/m7-pixelelated'
GIB = 1024 ** 3


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
    p.add_argument('--expected-es', required=True, help='Exact reviewed ES commit required in the frozen distribution recipe')
    p.add_argument('--measurement', type=Path, required=True)
    p.add_argument('--owner', type=Path, required=True)
    p.add_argument('--stage', choices=['transfer', 'build'], required=True)
    a = p.parse_args()
    tree = a.checkout.resolve(strict=True)
    owner = a.owner.resolve(strict=True)
    measurement = a.measurement.resolve(strict=True)
    assert str(tree) == '/workspace/repos/rocknix.worktrees/m7-p5-build-20261014-02'
    assert a.commit == 'fac608ff89940ce358ea9b8a95e9a08a6fe26568'
    assert re.fullmatch('[0-9a-f]{40}', a.commit)
    assert re.fullmatch('[0-9a-f]{40}', a.expected_es)
    assert git(tree, 'rev-parse', 'HEAD') == a.commit
    assert git(tree, 'branch', '--show-current').startswith('build/')
    assert not git(tree, 'status', '--porcelain'), 'freeze a clean source first'
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
    assert m['parent_head'] == 'd6a87f05c1935516115b2cca1af22151a0209224'
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
    stage = 'm7-gstnet-' + a.stage
    retention = {'volume': '/workspace', 'scan_roots': [str(scan)], 'reference_stores': [],
                 'protected': [str(PARENT), str((PARENT if a.stage == 'transfer' else tree) / ROOT), str(PARENT / 'target'),
                               '/workspace/cache/rocknix-sources', str(measurement)],
                 'candidates': [], 'builds': [{'name': stage, 'terms_bytes': terms,
                     'basis': 'Completed predecessor final quiescent allocation sample plus explicit growth/QA/margin allowances. '
                              'Existing source cache and parent payloads already reduce f_bavail; no reclamation counted. '
                              'No deletion candidates; the empty explicit scan is not historical-volume classification.',
                     'evidence': [{'path': str(measurement), 'sha256': hashlib.sha256(measurement.read_bytes()).hexdigest()},
                                  {'path': m['original_allocation_log'], 'sha256': m['original_allocation_log_sha256']}]}]}
    outputs = [{'path': str(tree / ROOT), 'issue': 572, 'kind': 'build-cache',
                'release_when': 'Immediately queued assembled-image qualification and required corresponding-source custody accepted'}]
    if a.stage == 'build':
        outputs += [{'path': str(tree / n), 'issue': 572, 'kind': 'firmware',
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
          'es_commit': a.expected_es, 'es_recipe_sha256': es_recipe_sha256,
          'warm_parent': str(PARENT), 'container_checkout': CONTAINER,
          'stage': stage, 'required_bytes': sum(terms.values()), 'admission_prepared': False})
    print(json.dumps({'owner': str(owner), 'required_bytes': sum(terms.values()),
                      'next': 'watched retention-report, then fresh admission prepare and submit'}))


if __name__ == '__main__':
    main()

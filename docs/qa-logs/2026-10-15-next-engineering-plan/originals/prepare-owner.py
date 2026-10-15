#!/usr/bin/env python3
"""Materialize one reviewed build owner. Writes only small config/helpers; no launch."""
import argparse
import datetime
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--checkout', required=True, type=Path)
    p.add_argument('--commit', required=True)
    p.add_argument('--expected-es', required=True, help='Exact reviewed ES commit required in the frozen distribution recipe')
    p.add_argument('--owner', required=True, type=Path)
    p.add_argument('--cache-ready', required=True, type=Path)
    p.add_argument('--timestamp', required=True)
    p.add_argument('--family-seconds', type=int, default=7200)
    a = p.parse_args()
    tree, owner, cache = a.checkout.resolve(strict=True), a.owner.resolve(strict=True), a.cache_ready.resolve(strict=True)
    assert re.fullmatch('[0-9a-f]{40}', a.commit)
    assert re.fullmatch('[0-9a-f]{40}', a.expected_es)
    assert re.fullmatch('[0-9]{8}T[0-9]{6}Z', a.timestamp)
    datetime.datetime.strptime(a.timestamp, '%Y%m%dT%H%M%SZ')
    assert 600 <= a.family_seconds <= 21600
    assert not re.search(r'\s|[\x00\n`$]', str(owner) + str(tree))
    assert subprocess.check_output(['git', '-C', str(tree), 'rev-parse', 'HEAD'], text=True).strip() == a.commit
    assert subprocess.check_output(['git', '-C', str(tree), 'branch', '--show-current'], text=True).strip().startswith('build/')
    assert not subprocess.check_output(['git', '-C', str(tree), 'status', '--porcelain'], text=True).strip()
    recipe = tree / 'projects/ROCKNIX/packages/ui/emulationstation/package.mk'
    recipe_bytes = recipe.read_bytes()
    assert re.findall(r'^\s*PKG_VERSION=(.*)$', recipe_bytes.decode(), re.M) == ['"' + a.expected_es + '"'], 'expected exact ES pin missing or ambiguous'
    es_recipe_sha256 = hashlib.sha256(recipe_bytes).hexdigest()
    assert not (owner / 'build-inputs.json').exists()
    assert not (owner / 'launcher-submission.json').exists()
    cpus = sorted(os.sched_getaffinity(0))
    # Never exceed the completed predecessor's admitted 24-CPU image budget.
    assert set(range(24)).issubset(cpus)
    cpus = list(range(24))
    assert str(tree) == '/workspace/repos/rocknix.worktrees/m7-p5-build-20261014-02'
    assert a.commit == 'fac608ff89940ce358ea9b8a95e9a08a6fe26568'
    gst = tree / 'projects/ROCKNIX/packages/multimedia/gstreamer/gstreamer/package.mk'
    assert sha(gst) == '55e7905444569c9adf9e0739dfebb078b7de417a0cc3f1ae438f0493ea84714c'
    transfer = json.loads(cache.read_text())
    assert transfer['schema'] == 'pix572-atomic-cache-transfer-v1' and transfer['status'] == 'PASS'
    assert transfer['new'] == str(tree / 'build.pixelelated-GENERIC_X64.x86_64')
    assert transfer['destination_head'] == a.commit
    helpers = ['build-owner.py', 'host-resources.py', 'inner-build.py']
    for name in helpers:
        target = owner / name
        assert not target.exists()
        shutil.copyfile(Path(__file__).with_name(name), target)
        target.chmod(0o400)
    config = {'schema': 1, 'checkout': str(tree), 'commit': a.commit,
        'container_checkout': '/workspace/repos/rocknix.worktrees/m7-pixelelated',
        'build_root': 'build.pixelelated-GENERIC_X64.x86_64',
        'es_commit': a.expected_es, 'es_recipe_sha256': es_recipe_sha256,
        'gstreamer_recipe_sha256': sha(gst),
        'generated_doc_candidate_sha256': 'e574a017b83e0da4d9360017ed14d1edcab86eb979efcad1b15fd4bc76407baa',
        'builder_image': 'ghcr.io/pixelelated/build@sha256:988c0ba586263caeba4be4c03bd16eee055c9d066657951e320087bb8226ee39',
        'owner_label': 'pix-m7-' + a.timestamp.lower(), 'build_timestamp': a.timestamp,
        'host_pid_namespace': os.readlink('/proc/self/ns/pid'),
        'cache_ready': str(cache), 'cache_ready_sha256': sha(cache),
        'helper_sha256': {name: sha(owner / name) for name in helpers},
        'cold_cpu_ids': cpus[:4], 'image_cpu_ids': cpus,
        'cold_memory_bytes': 24 * 1024 ** 3, 'image_memory_bytes': 40 * 1024 ** 3,
        'container_pids_limit': 2048, 'family_timeout_seconds': a.family_seconds,
        'minimum_host_available_bytes': 8 * 1024 ** 3,
        'minimum_volume_available_bytes': 64 * 1024 ** 3,
        'disk_sample_interval_seconds': 600, 'disk_scan_timeout_seconds': 180,
        'limits_are_proposed_operating_bounds_not_measured_requirements': True}
    with (owner / 'build-inputs.json').open('x') as f:
        json.dump(config, f, indent=2); f.write('\n')
    (owner / 'build-inputs.json').chmod(0o400)
    print(json.dumps({'owner': str(owner), 'input_sha256': sha(owner / 'build-inputs.json'),
                      'cold_cpu_ids': cpus[:4], 'image_cpu_ids': cpus, 'launched': False}))


if __name__ == '__main__':
    main()

"""Bind existing unchanged-library proofs to candidate16 without replaying them."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import subprocess

root = Path('/workspace/repos/rocknix.worktrees/conflict-resolution')
dest = root / 'docs/qa-logs/2026-10-07-pixelelated-replacement-16/unchanged-dependency-custody'
assert not dest.exists()
image = Path('/workspace/tmp/pixelelated-m7-image-16/root')
prior = root / 'docs/qa-logs/2026-10-06-pixelelated-replacement-15/p4-library-fixes-02/artifacts'
sha = lambda data: hashlib.sha256(data).hexdigest()
before = (prior / 'installed-before.json').read_bytes()
assert before == (prior / 'installed-after.json').read_bytes()
hashes = json.loads(before)
assert len(hashes) == 46
for name, wanted in hashes.items():
    path = image / name.lstrip('/')
    assert path.resolve().is_relative_to(image), name
    assert sha(path.read_bytes()) == wanted, name

manifests = {}
manifest_hashes = {}
for n in [14, 16]:
    data = Path(f'/workspace/tmp/pixelelated-m7-replacement-{n}/inputs.json').read_bytes()
    manifests[n] = json.loads(data)
    manifest_hashes[n] = sha(data)
recipes = {n: {p: h for p, h in d['source_files'].items() if p.endswith('/package.mk')}
           for n, d in manifests.items()}
assert len(recipes[14]) == len(recipes[16]) == 1608
changed = [p for p in sorted(set(recipes[14]) | set(recipes[16]))
           if recipes[14].get(p) != recipes[16].get(p)]
assert changed == ['projects/ROCKNIX/packages/ui/emulationstation/package.mk'], changed
checker = 'tools/fork-package-freshness'
assert manifests[14]['qa_source_files'][checker] == manifests[16]['qa_source_files'][checker]
assert manifests[14]['proxy_commit'] == manifests[16]['proxy_commit'] == '879b158995d412af434301ebdae581f66b8b6d57'
prefix = 'projects/ROCKNIX/packages/network/raofflineproxy/'
proxy_sources = {n: {p: h for p, h in d['source_files'].items() if p.startswith(prefix)}
                 for n, d in manifests.items()}
assert proxy_sources[14] and proxy_sources[14] == proxy_sources[16]
freshness_path = root / 'docs/qa-logs/2026-10-06-pixelelated-replacement-14/preparation/freshness-completion.json'
freshness = json.loads(freshness_path.read_text())
assert set(freshness['result_channels'].values()) == {0} and len(freshness['absent_pids']) == 4

es = '/home/max/Development/emulationstation-next.worktrees/qa-integration'
surface = 'es-app/src/guis/GuiRetroAchievementsSettings.cpp'
commands = []
for ref in ['bab4df649f48847cc43d21c77c058107ad902754', '72494bc72e3d64d4dcfeb4e6478052bbdf166c5b']:
    command = ['git', '-C', es, 'show', ref + ':' + surface]
    data = subprocess.check_output(command)
    commands.append(dict(command=command, returncode=0, source_sha256=sha(data)))
assert commands[0]['source_sha256'] == commands[1]['source_sha256']
result = dict(verified_utc=datetime.now(timezone.utc).isoformat(), result='PASS',
              candidate16=manifests[16]['distribution_commit'], manifest_sha256=manifest_hashes,
              prior_installed_hash_receipt=str(prior / 'installed-before.json'),
              prior_installed_hash_receipt_sha256=sha(before),
              candidate16_image_root=str(image), installed_proxy_files_unchanged=hashes,
              proxy_sources_unchanged=len(proxy_sources[16]),
              recipes_compared=1608, recipe_differences=changed,
              freshness_checker_sha256=manifests[16]['qa_source_files'][checker],
              original_freshness_completed_utc=freshness['utc'],
              original_freshness_receipt_sha256=sha(freshness_path.read_bytes()),
              unchanged_achievement_surface_commands=commands,
              scope='Byte and source custody for retaining earlier dependency, offline-library and explanation-page evidence. Not a new upstream freshness query, new 125-game run, new award, or completion of QA20/protocol qualification.')
dest.mkdir()
(dest / 'verification.json').write_text(json.dumps(result, indent=2) + '\n')
(dest / 'verify.py').write_bytes(Path(__file__).read_bytes())
print('PASS: 46 installed proxy files, proxy source inputs and 1607 library recipes unchanged; ES pin change explicitly isolated. Earlier runtime proof retained, not replayed.')

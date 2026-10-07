"""Read-only #494 custody sizing; no copy or removal of candidate trees."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib, json, os, runpy, stat, subprocess, time

owner = Path(__file__).resolve().parent
classify = runpy.run_path(str(owner / 'elf-header.py'))['classify']
stores = [Path('/workspace/artifacts/pixelelated-build-custody') / n / 'objects'
          for n in ['issue-456-es-logs-01', 'issue-456-runtime-01', 'issue-456-runtime-02']]
assert all(p.is_dir() for p in stores)
inventory = json.loads(Path('/workspace/tmp/pixelelated-m7-storage-sizing-02/artifacts/report.json').read_text())
allocated = {r['path']: r['allocated_bytes'] for r in inventory['rows']}
expected = {'09': 'cf511ce79b83cba7fea8b14cfa3d04fb13e4b4fb',
            '10': 'd6e8390c93bed87efe2dcc23cd402a271cacd1c7',
            '12': '55d8ee8f75965a560f75d187e34c9beaa93133f1',
            '14': '7afa9efcfc0c1ce4b89774b38878fc1b9a9063d2'}
objects, verified_reuse, summaries = {}, set(), []
visited = selected = 0
last = time.monotonic()

def digest(p):
    with p.open('rb') as f:
        return hashlib.file_digest(f, 'sha256').hexdigest()

def identity(s):
    return (s.st_dev, s.st_ino, s.st_size, s.st_mtime_ns, s.st_ctime_ns)

def git(tree, *args):
    return subprocess.check_output(['git', '-C', str(tree), *args], text=True).strip()

def keep(p, tree, rows):
    global selected
    s = p.lstat()
    row = {'path': str(p.relative_to(tree)), 'mode': stat.S_IMODE(s.st_mode),
           'mtime_ns': s.st_mtime_ns}
    if stat.S_ISLNK(s.st_mode):
        row.update(kind='symlink', target=os.readlink(p))
    elif stat.S_ISDIR(s.st_mode):
        row.update(kind='directory')
    else:
        assert stat.S_ISREG(s.st_mode), str(p)
        sha = digest(p)
        assert identity(s) == identity(p.lstat()), str(p)
        if sha not in objects:
            prior = next((d / sha for d in stores if (d / sha).is_file()), None)
            if prior:
                assert digest(prior) == sha
                assert prior.stat().st_ino != s.st_ino or prior.stat().st_dev != s.st_dev
                verified_reuse.add(str(prior))
            objects[sha] = {'bytes': s.st_size, 'source': str(p),
                            'source_identity': list(identity(s)),
                            'verified_prior_object': str(prior) if prior else None}
        row.update(kind='file', sha256=sha, bytes=s.st_size)
    rows.append(row); selected += 1

for number, head in expected.items():
    tree = Path('/workspace/repos/rocknix.worktrees/m7-pixelelated-replacement' + number)
    build = tree / 'build.pixelelated-GENERIC_X64.x86_64'
    assert git(tree, 'rev-parse', 'HEAD') == head and build.is_dir()
    dirty = git(tree, 'status', '--porcelain')
    assert dirty == 'M documentation/PER_DEVICE_DOCUMENTATION/GENERIC_X64/SUPPORTED_EMULATORS_AND_CORES.md', dirty
    patch = subprocess.check_output(['git', '-C', str(tree), 'diff', '--binary'])
    (owner / 'artifacts' / (number + '-tracked.diff')).write_bytes(patch)
    inputs_path = Path('/workspace/tmp/pixelelated-m7-replacement-' + number) / 'inputs.json'
    inputs = json.loads(inputs_path.read_text())
    assert inputs['distribution_commit'] == head
    for name, sha in inputs['source_files'].items():
        assert digest(tree / name) == sha, name
    for name, target in inputs['source_symlinks'].items():
        assert os.readlink(tree / name) == target
    rows = []
    es = list(build.glob('build/emulationstation-*')); assert len(es) == 1
    selected_roots = es + [build / '.threads', build / '.stamps', tree / '.build-runs']
    for root in selected_roots:
        assert root.is_dir(), str(root)
        keep(root, tree, rows)
        for base, dirs, files in os.walk(root, followlinks=False):
            for name in dirs + files:
                keep(Path(base) / name, tree, rows)
    errors, runtime, hardlinks = [], 0, {}
    for base, dirs, files in os.walk(build, followlinks=False, onerror=lambda e: errors.append(str(e))):
        for name in files:
            p = Path(base) / name; visited += 1
            s = p.lstat()
            if stat.S_ISREG(s.st_mode) and s.st_nlink > 1:
                key = str((s.st_dev, s.st_ino))
                entry = hardlinks.setdefault(key, {'nlink': s.st_nlink, 'paths': []})
                assert entry['nlink'] == s.st_nlink
                entry['paths'].append(str(p.relative_to(tree)))
            if not stat.S_ISREG(s.st_mode):
                continue
            if not (s.st_mode & 0o111 or '.so' in name or name.endswith(('.ko', '.debug')) or name == 'vmlinux'):
                continue
            with p.open('rb') as f:
                header = f.read(20)
            kind = classify(header)
            if kind is None:
                continue
            if kind['kind'] != 'opaque-ELF-fixture' and kind['elf_type'] not in (2, 3) and not (kind['elf_type'] == 1 and name.endswith(('.ko', '.debug'))):
                continue
            keep(p, tree, rows); runtime += 1
            if time.monotonic() - last > 10:
                print('Inspected', visited, 'filenames; selected', selected, 'custody entries', flush=True)
                last = time.monotonic()
    assert not errors, errors
    assert git(tree, 'rev-parse', 'HEAD') == head and git(tree, 'status', '--porcelain') == dirty
    manifest = owner / 'artifacts' / (number + '-custody-plan.json')
    manifest.write_text(json.dumps({'tree': str(tree), 'head': head, 'entries': rows,
        'hardlinks': hardlinks, 'scope': 'Read-only selected custody; no preservation copy or removal yet'}, indent=2) + '\n')
    summaries.append({'tree': str(tree), 'head': head, 'branch': git(tree, 'branch', '--show-current'),
        'allocated_bytes_at_storage_report': allocated[str(tree)],
        'source_files_verified': len(inputs['source_files']),
        'source_symlinks_verified': len(inputs['source_symlinks']),
        'inputs_sha256': digest(inputs_path), 'tracked_diff_sha256': hashlib.sha256(patch).hexdigest(),
        'runtime_elf_files': runtime, 'hardlink_groups': len(hardlinks),
        'unaccounted_hardlink_groups': sum(v['nlink'] != len(v['paths']) for v in hardlinks.values()),
        'custody_plan': str(manifest), 'custody_plan_sha256': digest(manifest)})
    print('PASS read-only source and custody plan', tree.name, flush=True)

(owner / 'artifacts/objects.json').write_text(json.dumps(objects, indent=2) + '\n')
report = {'utc': datetime.now(timezone.utc).isoformat(), 'result': 'READ_ONLY_PLAN_COMPLETE',
    'trees': summaries, 'files_inspected': visited, 'unique_objects': len(objects),
    'new_unique_copy_bytes': sum(v['bytes'] for v in objects.values() if not v['verified_prior_object']),
    'prior_verified_objects': len(verified_reuse),
    'gross_allocated_bytes': sum(s['allocated_bytes_at_storage_report'] for s in summaries),
    'preservation_performed': False, 'deletion_performed': False,
    'remaining': 'Source-archive inventory, full live/backing/reference review, independent preservation, measured net proposal and explicit deletion approval'}
(owner / 'artifacts/report.json').write_text(json.dumps(report, indent=2) + '\n')
print(json.dumps({k: v for k, v in report.items() if k != 'trees'}), flush=True)

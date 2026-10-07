"""Bind accepted storage reviews into a retirement plan; never delete anything."""
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from pathlib import Path
import hashlib
import json
import os
import stat
import subprocess
import sys


def digest(path):
    with Path(path).open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def identity(path):
    s = Path(path).lstat()
    return dict(device=s.st_dev, inode=s.st_ino, size=s.st_size,
                allocated_bytes=s.st_blocks * 512, mtime_ns=s.st_mtime_ns,
                uid=s.st_uid, mode=s.st_mode, links=s.st_nlink)


def read(path):
    return json.loads(Path(path).read_text())


def git(tree, *args):
    return subprocess.check_output(['git', '-C', str(tree), *args], text=True).strip()


def prepare(owner):
    base = Path('/workspace/tmp')
    selection = base / 'pixelelated-m7-broad-retention-classification-02/selection.json'
    selected = read(selection)
    candidates = {row['path']: row for row in selected['candidates']}
    assert len(candidates) == 850
    payloads, records, receipts = {}, {}, []
    for suffix in ['01', '02']:
        job = base / ('pixelelated-m7-broad-retention-hashes-' + suffix)
        accepted = job / 'owner-verification.json'
        assert read(accepted)['result'] == 'PASS'
        report = job / 'artifacts/result.json'
        data = read(report)
        assert not data['errors'] and not data['deletion_performed']
        receipts.append(dict(path=str(report), sha256=digest(report),
                             acceptance=str(accepted), acceptance_sha256=digest(accepted)))
        for row in data['payloads']:
            assert row['path'] not in payloads
            assert candidates[row['path']]['identity'] == row['identity']
            assert identity(row['path']) == row['identity']
            assert stat.S_ISREG(row['identity']['mode']) and row['identity']['links'] == 1
            assert str(Path(row['path']).resolve()) == row['path']
            payloads[row['path']] = row
        for row in data['retained_records']:
            if row['path'] in candidates:
                continue  # A small disk from the supplemental set is not a kept record.
            if row['path'] in records:
                assert records[row['path']] == row
            records[row['path']] = row
    assert set(payloads) == set(candidates)

    # Remove children before their backing files. Every runtime disk was selected;
    # source fixtures outside this set remain covered by the previous dependency review.
    disks = {p for p, row in payloads.items() if 'chain' in row}
    assert len(disks) == 263
    edges = set()
    for p in disks:
        for row in payloads[p]['chain']:
            child = Path(row['filename'])
            if not child.is_absolute():
                child = Path(p).parent / child
            backing = row.get('full-backing-filename') or row.get('backing-filename')
            if backing:
                parent = Path(backing)
                if not parent.is_absolute():
                    parent = child.parent / parent
                assert str(child.resolve()) in disks and str(parent.resolve()) in disks
                edges.add((str(child.resolve()), str(parent.resolve())))
    order, remaining = [], set(disks)
    while remaining:
        ready = sorted(remaining - {parent for child, parent in edges if child in remaining})
        assert ready, 'Cycle in disk backing graph'
        order.extend(ready)
        remaining.difference_update(ready)
    order.extend(sorted(set(payloads) - disks))

    def verify_hold(row):
        assert identity(row['path']) == row['identity']
        result = dict(row, sha256=digest(row['path']))
        assert identity(row['path']) == row['identity']
        assert row['test'] and row['issue'] and row['release']
        return result

    with ThreadPoolExecutor(max_workers=3) as pool:
        held = list(pool.map(verify_hold, selected['protected']))
    store = Path('/workspace/artifacts/pixelelated-build-custody/issue-494-device-capacity-01')
    preservation = read(store / 'receipt.json')
    acceptance = base / 'pixelelated-m7-device-preservation-acceptance-01/owner-verification.json'
    assert read(acceptance)['result'] == 'PASS'
    review = read(base / 'pixelelated-m7-device-retention-review-01/artifacts/report.json')
    trees = []
    for row in review['trees']:
        path = Path(row['tree'])
        assert git(path, 'rev-parse', 'HEAD') == row['head']
        assert git(path, 'branch', '--show-current') == row['branch']
        diff = subprocess.check_output(['git', '-C', str(path), 'diff', '--binary', 'HEAD'])
        assert hashlib.sha256(diff).hexdigest() == row['tracked_diff_sha256']
        preserved = next(r for r in preservation['trees'] if r['tree'] == str(path))
        assert digest(preserved['source_inventory']) == preserved['source_inventory_sha256']
        assert not read(preserved['source_inventory'])['errors']
        trees.append(dict(row, root_identity=identity(path), preservation=preserved,
                          remove_command=['tools/fork-worktree', 'remove', str(path), '--force']))

    # The two consumers finished; preserve their status and exact source commit,
    # rather than treating old symlinks as a reason to keep compiled output.
    classified = []
    previous = read(base / 'pixelelated-m7-device-dependency-classification-01/artifacts/classification.json')
    for row in previous['held_source_dependencies']:
        link = Path(row['source'])
        assert link.is_symlink() and str(link.resolve()) == row['target']
        qa = next(p for p in link.parents if p.name in ['pixelelated-m7-qa-16', 'pixelelated-m7-qa-17'])
        completion = read(qa / 'completion.json')
        assert completion['qemu_absent'] and len(set(completion['result_channels'].values())) == 1
        assert all(not Path('/proc', str(pid)).exists() for pid in completion['absent_pids'])
        tree = next(r for r in trees if r['tree'].endswith('replacement12'))
        relative = str(Path(row['target']).relative_to(tree['tree']))
        git(tree['tree'], 'cat-file', '-e', tree['head'] + ':' + relative)
        classified.append(dict(source=row['source'], target=row['target'],
                               literal_target=os.readlink(link), source_commit=tree['head'],
                               source_path=relative, completion=str(qa / 'completion.json'),
                               completion_sha256=digest(qa / 'completion.json'),
                               outcome=completion['job_rc'],
                               classification='Historical input to a completed run; preserve commit, diff and custody. Not a live runtime dependency.'))

    record_file = owner / 'retained-records.json'
    record_file.write_text(json.dumps(list(records.values()), indent=2) + '\n')
    plan = dict(created_utc=datetime.now(timezone.utc).isoformat(), decision='D-INFRA-022',
                status='PREPARED_REQUIRES_ROOT_READBACK_AND_FINAL_EXECUTION_GUARDS',
                selection=str(selection), selection_sha256=digest(selection),
                hash_receipts=receipts, payloads=[payloads[p] for p in order],
                qcow_backing_edges=sorted(edges), protected_test_firmware=held,
                retained_records=str(record_file), retained_records_sha256=digest(record_file),
                retained_record_count=len(records), worktrees=trees,
                historical_source_links=classified,
                custody_store=str(store), custody_receipt_sha256=digest(store / 'receipt.json'),
                payload_allocated_bytes=sum(r['identity']['allocated_bytes'] for r in payloads.values()),
                tree_potential_net_bytes=preservation['estimated_net_recovery_bytes'],
                deletion_performed=False,
                prerequisites=['Fresh complete administrator process readback and match classification',
                               'Current user-process and container checks; all payload/record identities unchanged',
                               'Guarded watched execution; children before backing files; standard helper for worktrees',
                               'Post-action absence, kept input and compact-record verification; measured actual recovery'],
                scope='Exact reviewed payload order and source-link classification. Extraction copies are separately reviewed. This preparer never deletes and is not the execution guard.')
    (owner / 'plan.json').write_text(json.dumps(plan, indent=2) + '\n')
    print(json.dumps({k: plan[k] for k in ['status', 'retained_record_count', 'payload_allocated_bytes', 'tree_potential_net_bytes', 'deletion_performed']}), flush=True)


if __name__ == '__main__':
    owner = Path(sys.argv[1]).resolve(strict=True)
    assert not (owner / 'plan.json').exists()
    prepare(owner)

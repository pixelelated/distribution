#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-2.0
"""Verify publication custody and descriptive arithmetic only; no runtime."""
import gzip
import hashlib
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parent
FRAMES={'initial-frame.png','light-actual.png','drive-open.png','drive-settled.png','dropbox-loaded.png','dropbox-later.png'}


def sha(data):return hashlib.sha256(data).hexdigest()

def local(name):
    path=ROOT/name
    if path.is_symlink() or not path.resolve(strict=True).is_relative_to(ROOT):raise ValueError('nonlocal artifact')
    return path


def main():
    count=0
    for line in (ROOT/'SHA256SUMS').read_text().splitlines():
        expected,name=line.split('  ',1)
        if sha(local(name).read_bytes())!=expected:raise ValueError('stored artifact mismatch')
        count+=1
    copied=json.loads((ROOT/'provenance.json').read_text())['copied']
    for row in copied:
        data=local(row['stored']).read_bytes()
        if sha(data)!=row['stored_sha256']:raise ValueError('stored provenance mismatch')
        raw=gzip.decompress(data) if row['encoding']=='gzip' else data
        if sha(raw)!=row['source_sha256'] or len(raw)!=row['source_bytes']:raise ValueError('original byte mismatch')
        if raw.startswith(b'\x7fELF'):raise ValueError('ELF payload excluded')
    if {p.name for p in (ROOT/'frames').iterdir()}!=FRAMES:raise ValueError('unreviewed frame')
    for p in ROOT.rglob('*'):
        if p.is_file() and ('private' in p.relative_to(ROOT).parts or p.name in {'window.log','vm-result.json'}):raise ValueError('private artifact')
    metrics=json.loads((ROOT/'descriptive-observations.json').read_text())
    raw=gzip.decompress((ROOT/'originals/guard-samples.jsonl.gz').read_bytes())
    if sha(raw)!=metrics['guard_samples_source_sha256']:raise ValueError('sample binding')
    samples=[json.loads(line) for line in raw.splitlines()]
    if max(sum(bool(c['owned_live']) for c in s['cases']) for s in samples)!=1:raise ValueError('overlapping tracked cases')
    for case in metrics['cases']:
        live=[s for s in samples if any(c['id']==case['case'] and c['owned_live'] for c in s['cases'])]
        if len(live)!=case['live_sample_count']:raise ValueError('sample count')
        if min(s['mem']['MemAvailable'] for s in live)!=case['minimum_guest_mem_available_kib_while_owned_live']:raise ValueError('memory arithmetic')
        if live[-1]['at']-live[0]['at']!=case['observed_owned_live_span_seconds']:raise ValueError('span arithmetic')
    local_analysis=json.loads((ROOT/'local-calibration-analysis.json').read_text())
    if local_analysis['local_original_redirect_header_calibration']!='matched' or local_analysis['provider_wire_ua_guaranteed']:raise ValueError('calibration scope')
    print(json.dumps({'status':'PASS','stored_files':count,'originals_verified':len(copied),'reviewed_frames':len(FRAMES),
        'scope':'file hashes, lossless copies and descriptive arithmetic only; no new runtime'}))


if __name__=='__main__':main()

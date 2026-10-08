#!/usr/bin/env python3
"""Validate this review packet's schema, references and PNG identities (not semantics)."""
import collections
import hashlib
import json
from pathlib import Path
import re
import struct
import sys

repo = Path(sys.argv[1]).resolve()
packet = repo / 'docs/qa-logs/2026-10-07-cloud-validator/ui'
index_path = packet / 'evidence-index.json'
raw = index_path.read_bytes()
index = json.loads(raw)
assert index['schema_version'] == 1
assert isinstance(index['entries'], list) and index['entries']
counts = collections.Counter()
frames = set()
for number, entry in enumerate(index['entries'], 1):
    context = f'entry {number} {entry.get("branch_id", "?")}'
    for field in ('flow_id', 'branch_id', 'document', 'anchor', 'trigger', 'expected_state', 'source', 'locale', 'width', 'height', 'status', 'review'):
        assert entry.get(field), f'{context}: absent {field}'
    assert entry['status'] in ('reviewed', 'rejected', 'pending'), context
    counts[entry['status']] += 1
    assert isinstance(entry['source'], dict), context
    assert entry['review'].get('reviewer') and entry['review'].get('observed'), context
    doc_path = repo / entry['document']
    assert not Path(entry['document']).is_absolute() and repo in doc_path.resolve().parents, context
    document = doc_path.read_text()
    anchors = []
    for line in document.splitlines():
        if line.startswith('#'):
            text = re.sub(r'^#+\s+', '', line).lower()
            anchors.append(re.sub(r'[^\w\- ]', '', text).replace(' ', '-'))
    assert entry['anchor'] in anchors, f'{context}: unknown document anchor'
    assert entry['branch_id'] in document, f'{context}: branch missing from canonical reference'
    if 'carried_forward_from' in entry:
        assert entry['carried_forward_from'].get('justification'), f'{context}: no reuse reason'
    if entry['status'] == 'pending' and not entry.get('frame'):
        assert not entry.get('sha256'), f'{context}: digest without frame'
        continue
    frame = Path(entry['frame'])
    assert not frame.is_absolute() and '..' not in frame.parts, f'{context}: not a packet-relative path'
    path = packet / frame
    assert packet.resolve() in path.resolve().parents, context
    assert path.is_file(), f'{context}: unresolved packet-relative frame {frame}'
    png = path.read_bytes()
    assert png[:8] == b'\x89PNG\r\n\x1a\n' and png[12:16] == b'IHDR', f'{context}: not PNG'
    assert struct.unpack('>II', png[16:24]) == (entry['width'], entry['height']), f'{context}: dimensions'
    assert re.fullmatch(r'[a-f0-9]{64}', entry['sha256']), context
    assert hashlib.sha256(png).hexdigest() == entry['sha256'], f'{context}: frame digest'
    frames.add(str(frame))
print(json.dumps({'result':'PASS','index_sha256':hashlib.sha256(raw).hexdigest(),'entries':len(index['entries']),'statuses':dict(counts),'unique_frames':len(frames),'limits':'Schema, reference and PNG identity only; human/agent semantic review and source binding remain separate.'}, indent=2))

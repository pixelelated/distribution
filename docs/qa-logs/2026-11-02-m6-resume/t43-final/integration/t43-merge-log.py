"""Pure T43 integration log resolver; preserves exact whole-entry bytes."""
import datetime
import hashlib
import re

SPECIAL = b'## 23:00 #690: T43 S1 outcome custody under accepted D\n'
SPECIAL_SHA = '753ad20a13fbf8e0fbe28289e4867cc880ba8c04b61a539a4360f5980783b6a6'

def need(ok, reason):
    if not ok:
        raise ValueError(reason)

def merge_append_bytes(base, coordinator, lane):
    need(base.endswith(b'\n'), 'base lacks line boundary')
    heading = re.compile(rb'^## (?P<stamp>(?:[0-9]{2}:[0-9]{2}(?::[0-9]{2})? UTC|[0-9]{4}-[0-9]{2}-[0-9]{2} [0-9]{2}:[0-9]{2}:[0-9]{2} UTC|[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}(?:\.[0-9]{1,6})?(?:Z|\+00:00))) (?:--|\xe2\x80\x94|\xe2\x80\x93|-)+ .+\n')
    def stamp(raw):
        value = raw.decode('ascii')
        if re.fullmatch(r'[0-9]{2}:[0-9]{2}(?::[0-9]{2})? UTC', value):
            datetime.datetime.strptime(value, '%H:%M:%S UTC' if value.count(':') == 2 else '%H:%M UTC')
        elif value.endswith(' UTC'):
            datetime.datetime.strptime(value, '%Y-%m-%d %H:%M:%S UTC')
        else:
            need(datetime.datetime.fromisoformat(value.replace('Z', '+00:00')).utcoffset() == datetime.timedelta(0), 'non-UTC timestamp')
    def parse(raw):
        if not raw:
            return []
        starts = [m.start() for m in re.finditer(rb'^## ', raw, re.M)]
        need(starts and raw[:starts[0]] and not raw[:starts[0]].strip(b'\n') and raw.endswith(b'\n') and not raw.endswith(b'\n\n'), 'not whole append entries')
        boundaries = [0]
        for i in starts[1:]:
            j = i
            while j and raw[j-1:j] == b'\n':
                j -= 1
            need(i-j >= 2, 'no entry separator')
            boundaries.append(j+1)
        blocks = [raw[a:b] for a,b in zip(boundaries,boundaries[1:]+[len(raw)])]
        for block in blocks:
            body = block.lstrip(b'\n')
            need(len(block) > len(body), 'entry lacks leading separator')
            if body.startswith(SPECIAL):
                # Exact immutable legacy entry only. No broader missing-UTC
                # heading exception and no rewriting of the original bytes.
                need(hashlib.sha256(block).hexdigest() == SPECIAL_SHA, 'legacy entry bytes changed')
                remainder = body[len(SPECIAL):]
            else:
                match = heading.match(body)
                need(match is not None, 'unrecognized entry heading')
                stamp(match.group('stamp'))
                remainder = body[match.end():]
            need(remainder.strip() and block.endswith(b'\n'), 'empty entry or missing newline')
        return blocks
    old = {x for x in base.splitlines() if x.startswith(b'## ')}
    entries = {}; sequences = []
    for tip in (coordinator, lane):
        need(tip.startswith(base), 'existing log bytes changed')
        keys = []
        for block in parse(tip[len(base):]):
            key = block.lstrip(b'\n').splitlines()[0]
            need(key not in old and key not in keys, 'duplicate heading')
            need(key not in entries or entries[key] == block, 'same heading has conflicting bytes')
            entries[key] = block; keys.append(key)
        sequences.append(keys)
    edges = {k:set() for k in entries}; degree = dict.fromkeys(entries,0)
    for sequence in sequences:
        for a,b in zip(sequence,sequence[1:]):
            if b not in edges[a]:
                edges[a].add(b); degree[b] += 1
    ordered = []
    while degree:
        ready = sorted(k for k,v in degree.items() if not v)
        need(ready, 'inconsistent entry order')
        key = ready[0]; ordered.append(key); degree.pop(key)
        for child in edges[key]: degree[child] -= 1
    for sequence in sequences:
        need([k for k in ordered if k in sequence] == sequence, 'branch order lost')
    merged = base+b''.join(entries[k] for k in ordered)
    need(parse(merged[len(base):]) == [entries[k] for k in ordered], 'entry bytes lost')
    return merged, [[k.decode() for k in sequence] for sequence in sequences]

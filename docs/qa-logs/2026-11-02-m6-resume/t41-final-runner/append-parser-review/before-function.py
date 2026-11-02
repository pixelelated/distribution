def merge_append_bytes(base,coordinator,lane):
    need(base.endswith(b'\n'),'append base must end at a line boundary')
    heading=rb'^## ([0-2][0-9]:[0-5][0-9]) UTC (?:--|\xe2\x80\x94|\xe2\x80\x93|-)+ .+\n'
    def parse(raw):
        if not raw:return []
        starts=[m.start() for m in re.finditer(rb'^## ',raw,re.M)]
        need(starts and raw[:starts[0]] and not raw[:starts[0]].strip(b'\n') and raw.endswith(b'\n') and not raw.endswith(b'\n\n'),'append suffix lacks whole entries or exact terminal newline')
        boundaries=[0]
        for i in starts[1:]:
            j=i
            while j>0 and raw[j-1:j]==b'\n':j-=1
            need(i-j>=2,'appended entries lack blank-line separation')
            boundaries.append(j+1)  # retain one newline on the preceding body
        blocks=[raw[a:b] for a,b in zip(boundaries,boundaries[1:]+[len(raw)])]
        for block in blocks:
            body=block.lstrip(b'\n');m=re.match(heading,body)
            need(len(block)>len(body) and m is not None and int(m.group(1)[:2])<24 and block.endswith(b'\n') and body[len(m.group(0)):].strip(),'append entry heading/body/boundary invalid')
        return blocks
    base_headings={x for x in base.splitlines() if x.startswith(b'## ')}
    allblocks={};seqs=[]
    for tip in [coordinator,lane]:
        need(tip.startswith(base),'work-log changed pre-existing bytes instead of whole append')
        blocks=parse(tip[len(base):]);keys=[]
        for b in blocks:
            key=b.lstrip(b'\n').splitlines()[0];need(key not in base_headings and key not in keys,'duplicate append/base heading')
            need(key not in allblocks or allblocks[key]==b,'same append heading has conflicting entry bytes')
            allblocks[key]=b;keys.append(key)
        seqs.append(keys)
    edges={k:set() for k in allblocks};degree={k:0 for k in allblocks}
    for seq in seqs:
        for a,b in zip(seq,seq[1:]):
            if b not in edges[a]:edges[a].add(b);degree[b]+=1
    ordered=[]
    while degree:
        ready=sorted(k for k,v in degree.items() if v==0);need(ready,'append entry orders conflict')
        k=ready[0];ordered.append(k);degree.pop(k)
        for b in edges[k]:degree[b]-=1
    for seq in seqs:need([k for k in ordered if k in seq]==seq,'append sequence not preserved')
    merged=base+b''.join(allblocks[k] for k in ordered)
    need(parse(merged[len(base):])==[allblocks[k] for k in ordered],'whole append bytes lost')
    return merged,[[sha(allblocks[k]) for k in seq] for seq in seqs]

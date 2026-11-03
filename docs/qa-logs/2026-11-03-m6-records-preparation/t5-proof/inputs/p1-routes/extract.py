#!/usr/bin/env python3
"""Finite syntax extraction from TEN allowlisted immutable entrypoints only.
Never executes repository code or reads target blob contents. Metadata is
looked up only for exact literal target paths; no directory traversal.
"""
import collections,hashlib,json,os,pathlib,posixpath,re,subprocess
ROOT=pathlib.Path(__file__).parent
REPO='/workspace/repos/pixelelated/distribution.worktrees/m6-renovation-plan-346'
REF='d707c82ab8c48b674acc1f95a9571f0cb24d226a'
ENTRYPOINTS=['README.md','AGENTS.md','CLAUDE.md','.claude/rules/instruction-files.md','docs/reviews/README.md','docs/audits/README.md','docs/retros/README.md','docs/futros/README.md','docs/work-logs/INDEX.md','.github/sessions/saved-session-state-feature-m6-renovation-plan-346.md']
# Root classification comes solely from coordinator's supplied selector excerpt.
CONFIG=ROOT/'records-roots.json'
CALLS=[]
def digest(b):return hashlib.sha256(b).hexdigest()
def git(*args,input=None):
    env=os.environ.copy();env['GIT_LITERAL_PATHSPECS']='1';env['GIT_OPTIONAL_LOCKS']='0'
    argv=['git','-C',REPO,*args];CALLS.append({'argv':argv,'stdin':input.decode() if input else None})
    return subprocess.check_output(argv,input=input,env=env)
def save(n,x):(ROOT/n).write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
SENSITIVE=re.compile(r'(?i)(credential|secret|password|passphrase|auth[-_]?token|token[-_]?store|\.aws(?:/|$)|\.ssh(?:/|$)|rclone\.conf(?:$|[.#]))')
# Token syntax deliberately does not interpret shell quoting, variables or globbing.
TOKENS=re.compile(r'''(?:https?://|mailto:)[^\s`"'<>]+|(?:/|~/)?(?:[.$~A-Za-z0-9_<>{}*?+-]+/)+[^\s`"'|;,()]*|[A-Za-z0-9_.<>{}*?+-]+\.(?:md|json|jsonl|tsv|txt|csv|yml|yaml|py|sh|mk|conf)(?::[0-9]+(?:[-:][0-9]+)?)?(?:\#[^\s`"'|;,()]*)?''')
MDLINK=re.compile(r'!?\[[^\]\n]*(?:\][^\[\n]*)?\]\(([^\n]*)')
INLINE=re.compile(r'(`+)(.*?)\1')
RULE_NAMES=set()
def overlap(a,b,spans):return any(a<d and b>c for c,d in spans)
def destination(line,start):
    """Single-line Markdown destination: escaped chars, balanced parentheses,
    angle destination, optional quoted title. Returns raw destination,end,limit.
    """
    i=start
    while i<len(line) and line[i].isspace():i+=1
    if i==len(line):return '',len(line),'unclosed-markdown'
    if line[i]=='<':
        end=line.find('>',i+1)
        if end<0:return line[i:],len(line),'unclosed-angle-destination'
        close=line.find(')',end+1)
        return line[i+1:end],close+1 if close>=0 else len(line),'angle-destination'
    first=i;depth=0
    while i<len(line):
        ch=line[i]
        if ch=='\\':i+=2;continue
        if ch=='(':depth+=1
        elif ch==')':
            if depth==0:return line[first:i],i+1,'plain-destination'
            depth-=1
        elif ch.isspace() and depth==0:
            close=line.find(')',i)
            return line[first:i],close+1 if close>=0 else len(line),'destination-with-title-or-space'
        i+=1
    return line[first:],len(line),'unclosed-markdown'

def extract(path,text):
    rows=[];headers=[];fence=None;heading='';sensitive=[]
    lines=text.splitlines()
    def add(spelling,lineno,column,syntax,context,limit=None):
        spelling=spelling.rstrip('.,;')
        if not spelling:return
        if SENSITIVE.search(spelling) or re.search(r'(?i)credential|secret',lines[lineno-1]):
            sensitive.append({'entrypoint':path,'line':lineno,'syntax':syntax,'spelling_sha256':digest(spelling.encode())});return
        rows.append({'entrypoint':path,'line':lineno,'column':column+1,'spelling':spelling,'syntax':syntax,'context':context,'heading':heading,'syntax_note':limit})
    for n,line in enumerate(lines,1):
        fm=re.match(r'^\s*(`{3,}|~{3,})(.*)$',line)
        if fm:
            if fence is None:fence=fm.group(1)[0]
            elif fence==fm.group(1)[0]:fence=None
            continue
        hm=re.match(r'^(#{1,6})\s+(.*)$',line)
        if hm:
            # For INDEX preserve structural headings, never entry-description prose.
            heading=hm.group(2)
            if not SENSITIVE.search(heading):headers.append({'line':n,'level':len(hm.group(1)),'text':heading})
            else:heading='[suppressed]'
        index_only=path=='docs/work-logs/INDEX.md'
        spans=[]
        if not fence:
            for m in re.finditer(r'!?\[[^\]\n]*\]\(',line):
                if overlap(m.start(),m.end(),spans):continue
                target,end,note=destination(line,m.end());spans.append((m.start(),end))
                add(target,n,m.end(),'markdown-link','heading-link' if hm else 'prose-link',note)
            dm=re.match(r'^\s*\[([^\]]+)\]:\s*(\S+)',line)
            if dm:
                spans.append((dm.start(),dm.end()));add(dm.group(2).strip('<>'),n,dm.start(2),'reference-definition','definition-only')
            for m in re.finditer(r'<((?:https?://|mailto:)[^<>\s]+)>',line):
                if not overlap(m.start(),m.end(),spans):spans.append((m.start(),m.end()));add(m.group(1),n,m.start(1),'autolink','prose-link')
        if index_only:continue
        if not fence:
            for m in INLINE.finditer(line):
                if overlap(m.start(),m.end(),spans):continue
                spans.append((m.start(),m.end()))
                for t in TOKENS.finditer(m.group(2)):
                    add(t.group(),n,m.start(2)+t.start(),'inline-code','code-span')
        for m in TOKENS.finditer(line):
            if not overlap(m.start(),m.end(),spans):add(m.group(),n,m.start(),'fenced-token' if fence else 'plain-token','fenced-example' if fence else 'prose-token')
    return rows,headers,sensitive

def resolve(row,roots):
    s=row['spelling'];base=s;anchor='';suffix='';kind='literal';basis=''
    if re.match(r'^[A-Za-z][A-Za-z0-9+.-]*://',s) or s.startswith('mailto:'):
        row.update(classification='external-url',resolved_path=None);return
    if row['syntax'] not in ['markdown-link','reference-definition','autolink'] and '/' in s and not (s.startswith(('/', './','../','~/','.github/','.claude/','.githooks/','docs/','plans/','tools/','packages/','projects/','scripts/','config/','distributions/','research/')) or s.endswith('/') or re.search(r'\.(?:md|json|jsonl|tsv|txt|csv|yml|yaml|py|sh|mk|conf)(?:[:#]|$)',s)):
        row.update(classification='slash-separated-context',resolved_path=None);return
    if '#' in base:base,anchor=base.split('#',1)
    m=re.search(r'(:[0-9]+(?:[-:][0-9]+)?)$',base)
    if m:suffix=m.group();base=base[:m.start()]
    row.update(anchor=anchor,line_suffix=suffix)
    if base.startswith(('/', '~')):
        row.update(classification='absolute-nonrepository-context',resolved_path=None);return
    if re.search(r'[<>*?{}$]|\.\.\.|YYYY|yyyy|<scope',base):
        row.update(classification='dynamic-or-glob-example',resolved_path=None);return
    if row['entrypoint']=='docs/audits/README.md' and row['context']=='fenced-example':
        row.update(classification='schematic-layout-example',resolved_path=None);return
    if not base:
        if anchor:row.update(classification='same-file-anchor',resolved_path=row['entrypoint'],resolution_basis='same-entrypoint');return
        row.update(classification='ambiguous-syntax',resolved_path=None);return
    if row['syntax'] in ['markdown-link','reference-definition']:
        path=posixpath.normpath(posixpath.join(posixpath.dirname(row['entrypoint']),base));basis='markdown-source-relative'
    elif base.startswith(('docs/','.github/','.claude/','plans/','tools/','packages/','projects/','distributions/','scripts/','config/','research/','.githooks/')):
        path=posixpath.normpath(base);basis='explicit-repository-prefix'
    elif base.startswith('./'):
        path=posixpath.normpath(base);basis='shell-repository-relative-example' if row['context']=='fenced-example' else 'ambiguous-dot-relative'
    elif '/' not in base and row['entrypoint'] in ['README.md','AGENTS.md','CLAUDE.md'] and base in ['AGENTS.md','CLAUDE.md','NAMING.md','LICENSE.md','TRADEMARK.md']:
        path=base;basis='named-root-entry'
    elif '/' not in base and base in RULE_NAMES:
        path=posixpath.join('.claude/rules',base);basis='canonical-rule-name-listed-in-AGENTS'
    elif '/' not in base and row['entrypoint'].startswith('.claude/rules/') and base.endswith('.md') and base not in ['AGENTS.md','CLAUDE.md']:
        path=posixpath.join('.claude/rules',base);basis='local-rule-basename-context'
    elif '/' not in base and row['entrypoint']=='docs/reviews/README.md' and base in ['plan-for-the-plan.md','order.md','inventory.json','inventory.md','assessment.md','cross-reference.md','slices.json','areas.json','p1-tracking.md','status.md','drift.md']:
        path=posixpath.join('docs/reviews',base);basis='local-review-basename-context'
    else:
        row.update(classification='ambiguous-relative-or-context',resolved_path=None);return
    if path=='..' or path.startswith('../'):
        row.update(classification='outside-repository-relative',resolved_path=None);return
    if row['entrypoint']=='docs/audits/README.md' and row['context']=='fenced-example':
        row.update(classification='schematic-layout-example',resolved_path=None);return
    inroots=next((r for r in roots if path==r.rstrip('/') or path.startswith(r.rstrip('/')+'/')),None)
    row.update(resolved_path=path.rstrip('/'),resolution_basis=basis,records_root=inroots,classification='literal-records-route' if inroots else ('literal-context-outside-records' if roots else 'literal-root-classification-pending'))
    if row['context']=='fenced-example':row['example']=True

def main():
    os.umask(0o077);roots=json.loads(CONFIG.read_text())['roots'] if CONFIG.exists() else []
    identities=[];rows=[];headers={};redacted=[]
    for p in ENTRYPOINTS:
        data=git('show',REF+':'+p) # ONLY allowlisted ten bodies
        if p=='AGENTS.md':RULE_NAMES.update(re.findall(r'^- `([^`/]+\.md)` --',data.decode(),re.M))
        part,h,hidden=extract(p,data.decode('utf-8'))
        identities.append({'path':p,'sha256':digest(data),'bytes':len(data),'lines':len(data.splitlines())})
        rows.extend(part);headers[p]=h;redacted.extend(hidden)
    for row in rows:resolve(row,roots)
    targets=sorted({x['resolved_path'] for x in rows if x.get('resolved_path')}|set(ENTRYPOINTS))
    assert all(not SENSITIVE.search(p) and not p.startswith(('../','/')) for p in targets)
    metadata={}
    # Exact named paths, nonrecursive ls-tree: directory targets are tree entries.
    for i in range(0,len(targets),100):
        requested=targets[i:i+100]
        for record in git('ls-tree','-z','-l',REF,'--',*requested).split(b'\0'):
            if not record:continue
            m,p=record.split(b'\t',1);mode,typ,oid,size=m.decode().split();p=p.decode()
            # Git may emit an ancestor tree if both ancestor and descendant were
            # requested: only save exact keys, and query missing keys individually.
            if p in targets:metadata[p]={'mode':mode,'type':typ,'oid':oid,'bytes':None if size=='-' else int(size)}
    for p in targets:
        if p not in metadata:
            records=git('ls-tree','-z','-l',REF,'--',p).split(b'\0')
            for record in records:
                if not record:continue
                m,q=record.split(b'\t',1);mode,typ,oid,size=m.decode().split()
                if q.decode()==p:metadata[p]={'mode':mode,'type':typ,'oid':oid,'bytes':None if size=='-' else int(size)}
        if p not in metadata:metadata[p]={'missing':True}
    trees={v['oid'] for v in metadata.values() if v.get('type')=='tree'}
    if trees:
        sizes={}
        for line in git('cat-file','--batch-check=%(objectname) %(objecttype) %(objectsize)',input=('\n'.join(sorted(trees))+'\n').encode()).decode().splitlines():
            oid,typ,size=line.split();assert typ=='tree';sizes[oid]=int(size)
        for v in metadata.values():
            if v.get('type')=='tree':v['tree_object_bytes']=sizes[v['oid']]
    for x in identities:x['git']=metadata[x['path']]
    for i,x in enumerate(rows,1):x['id']=i
    unique=sorted({x['resolved_path'] for x in rows if x['classification']=='literal-records-route'})
    groups={}
    for root in roots:
        rr=[x for x in rows if x.get('records_root')==root];ps={x['resolved_path'] for x in rr}
        groups[root]={'occurrences':len(rr),'unique_targets':len(ps),'ordinary_files':sum(metadata[p].get('mode') in ['100644','100755'] for p in ps),'trees':sum(metadata[p].get('type')=='tree' for p in ps),'missing':sum(metadata[p].get('missing',False) for p in ps),'unique_target_blob_bytes':sum(metadata[p].get('bytes') or 0 for p in ps)}
    summary={'ref':REF,'entrypoint_count':len(identities),'entrypoint_bytes':sum(x['bytes'] for x in identities),'occurrences':len(rows),'by_class':dict(collections.Counter(x['classification'] for x in rows)),'by_entrypoint':dict(collections.Counter(x['entrypoint'] for x in rows)),'records_groups':groups if roots else None,'records_unique_paths':len(unique) if roots else None,'records_unique_path_sha256':digest(('\n'.join(unique)+'\n').encode()) if roots else None,'metadata_named_targets':len(metadata),'suppressed_occurrences':len(redacted),'suppressed_metadata_sha256':digest(json.dumps(redacted,sort_keys=True,separators=(',',':')).encode()),'limits':'Ten bodies only; generated INDEX links/headers only. All target bytes/bodies unread; no anchor validation, recursive links, glob expansion, shell evaluation, fetch or lane producer execution. Counts describe this extractor syntax, not a final reading floor or slice recut.'}
    save('entrypoints.json',identities);save('routes.json',rows);save('target-metadata.json',metadata);save('index-headers.json',headers['docs/work-logs/INDEX.md']);save('summary.json',summary);save('commands.json',CALLS)
    # Credential-labelled occurrences stay aggregate-only, never path/name exports.
    print(json.dumps(summary,indent=2))

if __name__=='__main__':main()

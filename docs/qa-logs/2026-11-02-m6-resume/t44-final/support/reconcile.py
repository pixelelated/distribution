#!/usr/bin/env python3
"""Bounded immutable E-H record comparisons; never imports/executes lane code."""
import collections,hashlib,json,os,pathlib,re,stat,subprocess
ROOT=pathlib.Path(__file__).parent
REPO='/workspace/repos/pixelelated/distribution.worktrees/m6-es-vendored-and-data-691'
ES='/home/max/Development/emulationstation-next.worktrees/m6-es-vendored-and-data-691'
FINAL='f01abd480f4e0b337a9fcdde2cec9bc1746b525d'
D='923dd5371ded83fa965449a83f7a16d15a174772'
SEED='48a335700d05a733703e1b58536877b91b921259'
STREAM='821de9d39378b091c9d55a2f68734d8a36d65613'
ESREF='55158d2a64c69fe295fb4e67fd174424a71b1b4d'
ESTREE='64b90eb8cb07bdfcd690c74ff6bc980ae490657c'
AUDIT='docs/audits/2026_11_02-epic-m6-es-vendored-and-data/'
PUB='/tmp/m6-t44-eh-publication-qhf1l0l6'
OBS={};COMMANDS=[]
def sha(data):return hashlib.sha256(data).hexdigest()
def git(*args,repo=REPO):
    argv=['git','-C',repo,*args];COMMANDS.append(argv);return subprocess.check_output(argv)
def blob(path,ref=FINAL):
    data=git('show',ref+':'+path);OBS[ref+':'+path]={'bytes':len(data),'sha256':sha(data)};return data
def b(rel,ref=FINAL):return blob(AUDIT+rel,ref)
def j(rel,ref=FINAL):return json.loads(b(rel,ref))
def confined(rel):
    parts=rel.split('/');assert all(x not in ('','.','..') for x in parts)
    fd=os.open('/',os.O_RDONLY|os.O_DIRECTORY)
    try:
        for part in PUB.strip('/').split('/')+parts[:-1]:
            nxt=os.open(part,os.O_RDONLY|os.O_DIRECTORY|os.O_NOFOLLOW,dir_fd=fd);os.close(fd);fd=nxt
        f=os.open(parts[-1],os.O_RDONLY|os.O_NOFOLLOW|os.O_NONBLOCK,dir_fd=fd)
        try:
            info=os.fstat(f);assert stat.S_ISREG(info.st_mode) and info.st_size<50000000
            chunks=[]
            while True:
                data=os.read(f,65536)
                if not data:break
                chunks.append(data)
            data=b''.join(chunks);assert len(data)==info.st_size
        finally:os.close(f)
    finally:os.close(fd)
    OBS[PUB+'/'+rel]={'bytes':len(data),'sha256':sha(data),'regular_nofollow_confined':True};return data
def save(name,v):(ROOT/name).write_text(json.dumps(v,sort_keys=True,indent=2)+'\n')
def journal():
    p=ROOT/'observed-hashes.json';old=json.loads(p.read_text()) if p.exists() else {};old.update(OBS);save(p.name,old)
    with (ROOT/'commands.jsonl').open('a') as f:
        for c in COMMANDS:f.write(json.dumps(c)+'\n')
def batch(paths,ref=FINAL):
    argv=['git','-C',REPO,'cat-file','--batch'];COMMANDS.append({'argv':argv,'ref':ref,'stdin_paths':list(paths)})
    p=subprocess.Popen(argv,stdin=subprocess.PIPE,stdout=subprocess.PIPE);data,_=p.communicate(''.join(ref+':'+x+'\n' for x in paths).encode());assert p.returncode==0
    pos=0;out={}
    for path in paths:
        end=data.index(b'\n',pos);head=data[pos:end].split();assert head[1]==b'blob';size=int(head[2]);out[path]=data[end+1:end+1+size];assert data[end+1+size:end+2+size]==b'\n';pos=end+2+size
        OBS[ref+':'+path]={'bytes':size,'sha256':sha(out[path])}
    assert pos==len(data);return out

def tree(ref):
    out={}
    for row in git('ls-tree','-r','-z',ref).split(b'\0'):
        if row:
            meta,path=row.split(b'\t',1);mode,kind,oid=meta.decode().split();out[path.decode()]={'mode':mode,'kind':kind,'oid':oid}
    return out

def main():
    failures=[];facts={};checks=[]
    def check(label,value,detail=None):
        checks.append({'check':label,'pass':bool(value),'detail':detail})
        if not value:failures.append({'check':label,'detail':detail})
    pins={'RETURN.md':'81f3c07211ccac2871130a1fc962a128afa7d4eb8aaa3cbce8a8fb61cab381e6','SHA256SUMS':'07d40168cb238a2f3fc667766499fab6332965145469d70fbf138e751685a1e0','publication-readback.json':'e3fbe551a5af2f0b131ee0c9b82d75f99f32836972adc4b8e1506c6cc0ac359a'}
    pub={n:confined(n) for n in pins}
    for n,h in pins.items():check('pinned publication '+n,sha(pub[n])==h)
    manifest={}
    for line in pub['SHA256SUMS'].decode().splitlines():
        h,n=line.split(None,1);n=n.lstrip('*');assert re.fullmatch('[0-9a-f]{64}',h) and n not in manifest
        manifest[n]=h
    for n,h in manifest.items():
        if n not in pub:pub[n]=confined(n)
        check('confined publication file '+n,sha(pub[n])==h)
    facts['publication_manifest_entries']=len(manifest)
    td,tf=tree(D),tree(FINAL)
    ad={p:v for p,v in td.items() if p.startswith(AUDIT)};af={p:v for p,v in tf.items() if p.startswith(AUDIT)}
    # Named artifact bytes only, in memory. No source tree export or producer execution.
    fb=batch(list(af));db=batch(list(ad),D)
    allow=json.loads(fb[AUDIT+'stage-e/allowlist.json']);editable=set(allow['editable']);frozen=set(ad)-editable
    check('D/final artifact counts',len(ad)==274 and len(af)==440 and len(frozen)==268)
    check('268 frozen mode/blob identities',all(td[p]==tf[p] for p in frozen))
    commits=git('rev-list','--reverse',D+'..'+FINAL).decode().splitlines();facts['new_commits']=commits
    prior=D;changes=[]
    def allowed(p):return p in editable|set(allow['new_tools'])|set(allow['exact_paths'])|{AUDIT+'README.md'} or any(p.startswith(AUDIT+s+'/') for s in ['stage-e','stage-f','stage-g','stage-h'])
    for c in commits:
        parents=git('show','-s','--format=%P',c).decode().strip().split();check('single-parent continuation '+c,parents==[prior])
        t=tree(c);prev=td if prior==D else tree(prior)
        changed=[p for p in set(t)|set(prev) if t.get(p)!=prev.get(p)]
        bad=[p for p in changed if not allowed(p) or p not in t or t[p]['mode']!='100644' or t[p]['kind']!='blob' or p in frozen]
        check('per-commit exact records/modes '+c,not bad,bad)
        changes.append({'commit':c,'paths':sorted(changed)});prior=c
    changed=[p for p in set(td)|set(tf) if td.get(p)!=tf.get(p)]
    facts['changed_audit']=sum(p.startswith(AUDIT) for p in changed);facts['outside_audit']=sorted(p for p in changed if not p.startswith(AUDIT));facts['per_commit_changes']=changes
    check('whole ES immutable root',git('show','-s','--format=%T',ESREF,repo=ES).decode().strip()==ESTREE)
    art=json.loads(pub['exact-final-artifacts.json'])
    for label,rows,t,bs in [('D',art['D_artifacts'],td,db),('final',art['current_audit_records'],tf,fb)]:
        check(label+' artifact manifest keyset',set(v['path'] for v in rows)==set(bs) and len(rows)==len(bs))
        mismatches=[v['path'] for v in rows if any(v[k]!=t[v['path']][k] for k in ['mode','oid']) or v['sha256']!=sha(bs[v['path']]) or v['bytes']!=len(bs[v['path']])]
        check(label+' artifact manifest mode/blob/bytes/SHA256',not mismatches,mismatches)
    oldman=[p for p in ad if p.endswith('payload-sha256.json') or p.endswith('payload-manifest.json')]
    facts['D_manifest_named_candidates']=oldman
    dmanifest=db[AUDIT+'stage-d/payload-manifest.json'];dm=json.loads(dmanifest)['files']
    check('original D payload manifest SHA/keyset',sha(dmanifest)=='67b7001b027e7ffbaa9afa840b0554bb391de2c07459d33808119bc1c5d08509' and len(dm)==273 and set(dm)=={p.removeprefix(AUDIT) for p in ad}-{ 'stage-d/payload-manifest.json'})
    check('original D 273 payload byte/hash bindings',all(x['bytes']==len(db[AUDIT+p]) and x['sha256']==sha(db[AUDIT+p]) for p,x in dm.items()))
    check('stream exact published v2',fb[AUDIT+'stage-e/stream-v2.md']==blob('docs/reviews/briefs/t44-streams.md',STREAM))
    binding=json.loads(fb[AUDIT+'stage-e/current-program-binding.json'])
    for k in ['old','current']:check('frozen records.py '+k,sha(db[binding[k]['path']])==binding[k]['sha256'])
    check('records.py sole heading change',db[binding['old']['path']].replace(b'## Acceptance criteria Scorecard',b'## Acceptance-criteria scorecard')==db[binding['current']['path']])
    raw_transport=json.loads(fb[AUDIT+'stage-e/raw-transport.json']);decoded={}
    for x in raw_transport['files']:
        encoded=json.loads(fb[AUDIT+x['lossless_json']]);data=encoded['raw'].encode();decoded[AUDIT+x['path']]=data
        check('lossless transport '+x['path'],sha(data)==x['sha256']==encoded['sha256'] and data==pub[x['external_raw'].removeprefix(PUB+'/')])
    oldrunner=sha(fb[AUDIT+'stage-e/runner-attempt-1/final-record-runner.py']);newrunner=sha(fb[AUDIT+'tools/final-record-runner.py']);guard=sha(fb[AUDIT+'tools/final-confinement.py'])
    facts['programs']={'old_runner':oldrunner,'current_runner':newrunner,'guard':guard,'controls':sha(fb[AUDIT+'tools/final-confinement-controls.py'])}
    check('external runner is retained old version',sha(pub['final-record-runner.py'])==oldrunner and oldrunner!=newrunner)
    for p in ['final-confinement.py','final-confinement-controls.py']:
        check('external current '+p,pub[p]==fb[AUDIT+'tools/'+p])
    recs={};scope_drift={};input_bindings=[]
    allrecordbytes=dict(fb);allrecordbytes.update(decoded)
    def read_repo(p):
        if p not in allrecordbytes:allrecordbytes[p]=blob(p)
        return allrecordbytes[p]
    def receipt_group(label,collection):
        for p,data in collection.items():
            if not p.endswith('/receipt.json'):continue
            rec=json.loads(data);directory=p.rsplit('/',1)[0];recs[label+p]=rec
            errors=[]
            for stream in ['stdout','stderr']:
                q=directory+'/'+stream
                if q not in collection or sha(collection[q])!=rec.get(stream+'_sha256'):errors.append(stream)
            q=directory+'/input-scope.json'
            if q not in collection or sha(collection[q])!=rec.get('scope_sha256'):errors.append('scope')
            if rec.get('runner_sha256') not in [oldrunner,newrunner]:errors.append('runner')
            if not rec.get('argv') or rec.get('cpus')!=list(range(8,24)) or not rec.get('ended_at') or not isinstance(rec.get('rc'),int):errors.append('command/time/exit/CPU')
            check('receipt streams/scope/program '+label+p,not errors,errors)
            # Historical snapshot scope differences are preserved, not relabeled final.
            rows=json.loads(collection[q]);diff=[]
            for row in rows:
                path=row['path']
                if path in tf and tf[path]['kind']=='blob':
                    actual=sha(read_repo(path))
                    if actual!=row['sha256']:diff.append(path)
                else:diff.append(path)
            scope_drift[label+p]={'head':rec['head'],'entries':len(rows),'different_from_final':diff}
            for path,ident in rec.get('inputs',{}).items():
                actual=None
                if path.startswith(REPO+'/'):
                    rel=path.removeprefix(REPO+'/')
                    if rel in tf and tf[rel]['kind']=='blob':actual=read_repo(rel)
                elif path.startswith(PUB+'/') and path.removeprefix(PUB+'/') in pub:actual=pub[path.removeprefix(PUB+'/')]
                input_bindings.append({'receipt':label+p,'path':path,'expected':ident,'actual_sha256':sha(actual) if actual is not None else None,'matches_current':actual is not None and sha(actual)==ident['sha256'] and len(actual)==ident['bytes']})
    # Only NEW E/F receipt groups. Accepted A-D historical checks are not replayed.
    newbytes={p:v for p,v in allrecordbytes.items() if any(p.startswith(AUDIT+s+'/') for s in ['stage-e','stage-f','stage-g','stage-h'])}
    receipt_group('git:',newbytes);receipt_group('publication:',pub)
    facts['receipt_count']=len(recs);facts['receipt_exit_histogram']=dict(collections.Counter(str(x['rc']) for x in recs.values()))
    facts['receipt_bindings']=[{'location':p,'rc':v['rc'],'head':v['head'],'runner_sha256':v['runner_sha256'],'argv':v['argv'],'stdout_sha256':v['stdout_sha256'],'stderr_sha256':v['stderr_sha256']} for p,v in recs.items()]
    save('scope-comparisons.json',scope_drift);save('explicit-inputs.json',input_bindings)
    ctl=json.loads(fb[AUDIT+'stage-e/controls/results.json'])
    check('11 controls 74 commands 102 retained files',len(ctl['controls'])==11 and len(ctl['commands'])==74 and len(ctl['final_files'])==102)
    for x in ctl['controls']:
        check('guard control '+x['name'],x['rc']==x['expected_rc'] and x['program_sha256']==guard and all(sha(fb[AUDIT+'stage-e/controls/'+x['name']+'.'+s])==x[s+'_sha256'] for s in ['stdout','stderr']) and x['expected_reason'] in fb[AUDIT+'stage-e/controls/'+x['name']+'.stdout'].decode())
    check('74 inline command stdout/stderr SHA bindings',all(sha(x[s].encode())==x[s+'_sha256'] for x in ctl['commands'] for s in ['stdout','stderr']))
    # Metadata serialization only: reconcile the recorded fixture-config digest from
    # literal program schema and retained Git-event identities, without any fixture read/run.
    identity_events=[x for x in ctl['commands'][:15] if x['argv'][-2]=='rev-parse']
    cfg={'seed':identity_events[0]['stdout'].strip(),'accepted_d':identity_events[1]['stdout'].strip(),'audit':'docs/audits/t44','editable':['docs/audits/t44/00-running-log.md'],'new_tools':['docs/audits/t44/tools/final-confinement.py'],'exact_paths':['docs/retros/2026-11-03-m6-es-vendored-and-data.md','docs/work-logs/2026_11-work_logs/2026_11_03-work_log.md','docs/work-logs/INDEX.md'],'es_head':identity_events[2]['stdout'].strip(),'es_tree':identity_events[3]['stdout'].strip()}
    fixture_cfg=(json.dumps(cfg,indent=2)+'\n').encode()
    check('recorded fixture-config metadata SHA',all(x['allowlist_sha256']==sha(fixture_cfg) for x in ctl['controls']) and any(x['path']==ctl['fixture_root']+'/allowlist.json' and x['sha256']==sha(fixture_cfg) and x['bytes']==len(fixture_cfg) for x in ctl['final_files']))
    for label,expected in [('runner-failure-control',7),('runner-positive-control',0),('diff-2',2),('diff-3',0)]:
        check('new retained exit '+label,recs['git:'+AUDIT+'stage-e/'+label+'/receipt.json']['rc']==expected)
    facts['partial_scopes_no_receipt']=[p for p in newbytes if p.endswith('/input-scope.json') and p.rsplit('/',1)[0]+'/receipt.json' not in newbytes]
    check('four first-attempt missing receipts preserved',len(facts['partial_scopes_no_receipt'])==4)
    for prefix,gates in [('git:',json.loads(fb[AUDIT+'stage-f/gate-readback.json'])['checks']),('publication:',json.loads(pub['exact-final-gates.json'])['gates'])]:
        for name,g in gates.items():
            path=(AUDIT+'stage-f/' if prefix=='git:' else '')+name+'/receipt.json';collection=allrecordbytes if prefix=='git:' else pub;rec=recs[prefix+path]
            check('gate summary actual receipt '+prefix+name,sha(collection[path])==g['receipt_sha256'] and rec['rc']==g['rc']==0 and all(rec[s+'_sha256']==g[s+'_sha256'] for s in ['stdout','stderr']))
            if prefix=='publication:':check('exact-final gate scope '+name,rec['head']==FINAL and not scope_drift[prefix+path]['different_from_final'])
    publication=json.loads(pub['publication-readback.json'])
    for x in publication['command_receipts']:
        rec=recs['publication:'+x['path']]
        check('publication readback '+x['path'],sha(pub[x['path']])==x['sha256'] and rec['rc']==x['rc'] and rec['head']==x['head'])
    facts['publication_command_receipts']=len(publication['command_receipts'])
    check('final failed issue attempt remains rc1',recs['publication:final-resolution-issue/receipt.json']['rc']==1)
    check('exact final raw normal/issue PASS',all(pub[n+'/stdout'].decode().endswith('\nPASS\n') for n in ['final-resolution','final-resolution-issue-network']))
    for n in ['stage-e/resolution','stage-e/resolution-issue']:
        check('S1 actual resolution '+n,fb[AUDIT+n+'/stdout'].decode().endswith('\nPASS\n') and recs['git:'+AUDIT+n+'/receipt.json']['ended_at'] < recs['publication:s1-commit/receipt.json']['started_at'])
    names=sorted(tf,key=lambda x:x.encode());enumeration=b''.join(p.encode()+b'\0' for p in names)
    entries=b''.join((tf[p]['mode']+' '+tf[p]['oid']+' 0\t'+p).encode()+b'\0' for p in names)
    scan=json.loads(pub['exact-final-scan-scope.json']);ordinary=sum(v['mode'] in ['100644','100755'] for v in tf.values())
    check('exact-final immutable enumeration SHA',sha(enumeration)==scan['enumeration_sha256'])
    check('exact-final immutable index entries SHA',sha(entries)==recs['publication:final-forbidden/receipt.json']['index_entries_sha256'])
    check('scan ordinary-file count',pub['final-forbidden/stdout'].decode()==f'forbidden-terms-check: 0 hits in {ordinary} tracked files\n')
    facts['scan']={'all_keys':len(tf),'ordinary':ordinary,'modes':dict(collections.Counter(v['mode'] for v in tf.values())),'enumeration_sha256':sha(enumeration),'index_entries_sha256':sha(entries),'scope_rows':len(json.loads(pub['final-forbidden/input-scope.json']))}
    check('head/tree readback',pub['published-head/stdout'].decode().splitlines()==[FINAL,git('show','-s','--format=%T',FINAL).decode().strip()])
    check('remote readback exact final branch',pub['remote-tip/stdout'].decode()==FINAL+'\trefs/heads/feature/m6-es-vendored-and-data-691\n')
    check('clean publication statuses',pub['published-status/stdout']==pub['final-es-status/stdout']==b'')
    check('ES readback exact seed/root',pub['final-es-identity/stdout'].decode().splitlines()==[ESREF,ESTREE])
    custody=json.loads(fb[AUDIT+'stage-h/custody-plan.json']);census=json.loads(fb[AUDIT+'stage-d/owned-scratch-census.json'])
    check('retained-only H counts',len(custody['retained_old'])==49 and len(custody['retained_new_fixture'])==102 and custody['eligible']==custody['deleted']==[])
    check('old census SHA frozen',sha(fb[AUDIT+custody['old_census']['path']])==custody['old_census']['sha256'])
    ctlmap={x['path']:x for x in ctl['final_files']}
    check('new retained fixture metadata matches controls',all(x['original_content']==ctlmap[x['path']] and x['current']['sha256']==ctlmap[x['path']]['sha256'] and x['disposition']=='RETAIN' and 'future explicit' in x['next_owner'] for x in custody['retained_new_fixture']))
    check('old retain never grants eligibility',all(x['disposition']=='RETAIN' and 'future explicit' in x['next_owner'] and 'lacks original' in x['reason'] for x in custody['retained_old']))
    old_census_map={x['path']:x for x in census['files']}
    old_census_map.update({census['tiny_git']['path']+'/'+x['path']:x for x in census['tiny_git']['files']})
    check('49 old retained rows equal accepted census metadata',set(old_census_map)=={x['path'] for x in custody['retained_old']} and all(x['original_content']==old_census_map[x['path']] and x['current']['sha256']==old_census_map[x['path']]['sha256'] and x['current']['bytes']==old_census_map[x['path']]['bytes'] for x in custody['retained_old']))
    facts['old_census_keys']=list(census)
    retro=blob('docs/retros/2026-11-03-m6-es-vendored-and-data.md');ret=json.loads(pub['retro-readback.json'])
    check('retro immutable/external/posted binding',retro==pub['retro.md']==ret['comment']['body'].encode() and pub['retro-readback.json']==fb[AUDIT+'stage-g/retro-readback.json'])
    comp=json.loads(fb[AUDIT+'stage-f/separate-companions.json']);check('four companions copied accepted context',len(comp['companions'])==4 and sha(db[comp['source_path']])==comp['source_sha256'])
    decision=json.loads(fb[AUDIT+'stage-e/decision-readback.json'])
    for p,h in decision['inputs'].items():check('decision input binding '+p,sha(fb[p])==h)
    live=json.loads((ROOT/'live-issues.json').read_text());recorded=json.loads(pub['final-live-issues.json'])
    header_values={'reviewed-at':SEED,'fixed-at':FINAL,'reviewed-at-es':ESREF,'fixed-at-es':ESREF}
    def without_headers(s):return re.sub(r'^(reviewed-at|fixed-at|reviewed-at-es|fixed-at-es):[^\n]*',r'\1:',s,flags=re.M)
    for item in recorded['headers']:
        number=item['issue_number'];current=live['issue'+str(number)]['issue'];after=item['after']['body']
        check('live body matches final retained #'+str(number),current['body']==after and current['state']=='open' and current['milestone']==6)
        check('only four header replacements #'+str(number),without_headers(item['before']['body'])==without_headers(after))
        check('exact four header pins #'+str(number),all(re.findall('^'+re.escape(k)+r':\s*([^\n]*)',after,flags=re.M)==[v] for k,v in header_values.items()))
    check('live backlog exact retained body',live['issue1414']['issue']['body']==recorded['backlog']['body'] and live['issue1414']['issue']['state']=='open' and live['issue1414']['issue']['milestone']==6)
    task_counts={}
    for n in [691,1413,1414]:
        body=live['issue'+str(n)]['issue']['body'];task_counts[str(n)]={'unchecked':len(re.findall(r'^- \[ \]',body,re.M)),'checked':len(re.findall(r'^- \[[xX]\]',body,re.M))}
    check('tracker checkbox counts',task_counts=={'691':{'unchecked':20,'checked':0},'1413':{'unchecked':0,'checked':1},'1414':{'unchecked':5,'checked':0}})
    facts['tracker_counts']=task_counts
    parents=json.loads((ROOT/'live-parents.json').read_text());check('actual parent/milestone readbacks',{x['child']:x['parent'] for x in parents}=={691:700,1413:691,1414:700} and all(x['milestone']==6 and x['state']=='open' for x in parents))
    comments={int(x['id']):x for x in live['issue691']['comments']}
    check('posted retro body equals current owning thread',comments[6591747066]['body'].encode()==retro)
    facts['authority_comments']=[6591982620,6591582676];check('complete support and dispatch retained',all(x in comments for x in facts['authority_comments']))
    facts['live_shapes']={k:list(v) for k,v in live.items()}
    facts['explicit_input_unmatched']=[x for x in input_bindings if not x['matches_current']]
    save('results.json',{'identity':{'harness':'Codex','provider':'OpenAI','agent':'/root','lane':'historical P1 / wN:p3','session':'01a19d11-dda5-72e3-86f9-416f36341c24'},'scope':'Immutable E-H comparison only, no accepted producer/checker replay or final acceptance','facts':facts,'checks':checks,'failures':failures})
    journal();print(json.dumps({'checks':len(checks),'failures':failures,'facts':{k:v for k,v in facts.items() if k in ['publication_manifest_entries','new_commits','changed_audit','outside_audit','receipt_count','receipt_exit_histogram','publication_command_receipts','scan','old_census_keys','live_shapes','explicit_input_unmatched']}},indent=2))

if __name__=='__main__':main()

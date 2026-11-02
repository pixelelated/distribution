#!/usr/bin/env python3
"""Independent immutable record reconciliation; no lane code imported/executed."""
import collections,hashlib,json,os,pathlib,re,stat,subprocess
ROOT=pathlib.Path(__file__).parent
REPO='/workspace/repos/pixelelated/distribution.worktrees/m6-p1-survey-641'
ES='/home/max/Development/emulationstation-next'
FINAL='923dd5371ded83fa965449a83f7a16d15a174772'
SEED='48a335700d05a733703e1b58536877b91b921259'
ESREF='55158d2a64c69fe295fb4e67fd174424a71b1b4d'
ESTREE='64b90eb8cb07bdfcd690c74ff6bc980ae490657c'
AUDIT='docs/audits/2026_11_02-epic-m6-es-vendored-and-data/'
PUB='/tmp/m6-t44-d-publication-spbna76t'
COMMANDS=[];OBS={}
def sha(b):return hashlib.sha256(b).hexdigest()
def git(*args,repo=REPO):
    argv=['git','-C',repo,*args];COMMANDS.append(argv);return subprocess.check_output(argv)
def blob(p,ref=FINAL,repo=REPO):
    data=git('show',ref+':'+p,repo=repo);OBS[repo+' '+ref+':'+p]={'bytes':len(data),'sha256':sha(data)};return data
def b(rel,ref=FINAL):return blob(AUDIT+rel,ref)
def j(rel,ref=FINAL):return json.loads(b(rel,ref))
def confined(rel):
    parts=rel.split('/');assert all(p not in ('','.','..') for p in parts)
    fd=os.open('/',os.O_RDONLY|os.O_DIRECTORY)
    try:
        for p in PUB.strip('/').split('/')+parts[:-1]:
            n=os.open(p,os.O_RDONLY|os.O_DIRECTORY|os.O_NOFOLLOW,dir_fd=fd);os.close(fd);fd=n
        file=os.open(parts[-1],os.O_RDONLY|os.O_NOFOLLOW|os.O_NONBLOCK,dir_fd=fd)
        try:
            info=os.fstat(file);assert stat.S_ISREG(info.st_mode) and info.st_size<10000000
            chunks=[]
            while True:
                chunk=os.read(file,65536)
                if not chunk:break
                chunks.append(chunk)
            data=b''.join(chunks);assert len(data)==info.st_size
        finally:os.close(file)
    finally:os.close(fd)
    OBS[PUB+'/'+rel]={'bytes':len(data),'sha256':sha(data),'regular_nofollow_confined':True};return data
def save(name,v):(ROOT/name).write_text(json.dumps(v,indent=2,sort_keys=True)+'\n')
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
        OBS[REPO+' '+ref+':'+path]={'bytes':size,'sha256':sha(out[path])}
    assert pos==len(data);return out

def main():
    assert set(os.sched_getaffinity(0))<=set(range(8,24))
    errors=[];limits=[];result={}
    def check(ok,label):
        if not ok:errors.append(label)
    starts={'RETURN.md':'fd8c630739847ee0400b60cdd711ed58dd8776f29437ad4398c7f4eb501339b4','SHA256SUMS':'6c643a2060231c0582ee53296a842e0853fb3a9ad1450c07b4a41e1e23991c24','final-readback.json':'0c67162d42e04884f7b4addbef71bd5ae31b95afbfead4bfadbe5b580fedf13c'}
    external={n:confined(n) for n in starts}
    for n,h in starts.items():check(sha(external[n])==h,'authorized starting hash '+n)
    sums={}
    for line in external['SHA256SUMS'].decode().splitlines():
        h,name=line.split('  ',1);assert re.fullmatch('[0-9a-f]{64}',h);assert name not in sums;sums[name]=h
        if name not in external:external[name]=confined(name)
        check(sha(external[name])==h,'external manifest '+name)
    result['external_files']={'listed_files':len(sums),'total_files_including_SHA256SUMS':len(external),'pinned':starts}
    paths=git('ls-tree','-r','--name-only',FINAL,'--',AUDIT).decode().splitlines();cache=batch(paths)
    def raw(rel):return cache[AUDIT+rel]
    def get(rel):return json.loads(raw(rel))
    manifest=get('stage-d/payload-manifest.json')
    check(sha(raw('stage-d/payload-manifest.json'))=='67b7001b027e7ffbaa9afa840b0554bb391de2c07459d33808119bc1c5d08509','final manifest hash')
    check(set(paths)=={AUDIT+p for p in manifest['files']}|{AUDIT+'stage-d/payload-manifest.json'} and len(paths)==274 and len(manifest['files'])==273,'274/273 manifest keyset')
    for p,v in manifest['files'].items():check(sha(raw(p))==v['sha256'] and len(raw(p))==v['bytes'],'manifest bytes '+p)
    old='d6d08bf19c15b73cd587a1822b3ed7463f45873f';old_manifest_bytes=b('stage-d/payload-manifest.json',old);oldmanifest=json.loads(old_manifest_bytes)
    oldkeys=set(git('ls-tree','-r','--name-only',old,'--',AUDIT).decode().splitlines());extra={AUDIT+p for p in oldmanifest['files']}|{AUDIT+'stage-d/payload-manifest.json'};missing=sorted(extra-oldkeys)
    failure=json.loads(external['first-final-readback-failure.json']);check(failure==get('stage-d/publication-manifest-correction.json'),'original failure record equality')
    check(sha(old_manifest_bytes)==failure['old_manifest_sha256'] and missing==failure['missing_committed_paths'],'original failure exact absent key/hash')
    check(not (oldkeys-extra),'original failure no additional unmanifested path')
    result['payload']={'final_files':len(paths),'final_entries':len(manifest['files']),'final_manifest_sha256':sha(raw('stage-d/payload-manifest.json')),'first_tip':old,'first_audit_files':len(oldkeys),'first_manifest_entries':len(oldmanifest['files']),'first_manifest_sha256':sha(old_manifest_bytes),'first_missing_paths':missing,'first_failure':failure}
    # Original gate receipts are observations at their recorded bytes/times, not retroactive final gates.
    commits=git('rev-list','--reverse',SEED+'..'+FINAL).decode().splitlines();check(commits==[old,FINAL],'two exact commits')
    allow={'.github/sessions/saved-session-state-feature-m6-es-vendored-and-data-691.md','docs/work-logs/2026_11-work_logs/2026_11_02-work_log.md','docs/work-logs/INDEX.md'}
    percommit=[]
    for c in commits:
        parents=git('show','-s','--format=%P',c).decode().split();check(len(parents)==1,'no merge '+c)
        changed=git('diff','--name-only',parents[0],c).decode().splitlines();check(all(p.startswith(AUDIT) or p in allow for p in changed),'percommit record paths '+c)
        check(not git('diff','--diff-filter=DR','--name-only',parents[0],c).strip(),'no deletion/rename '+c)
        percommit.append({'commit':c,'parent':parents[0],'changed_paths':len(changed),'outside_audit':[p for p in changed if not p.startswith(AUDIT)]})
    check(git('show','-s','--format=%T',ESREF,repo=ES).decode().strip()==ESTREE,'actual whole ES root tree')
    result['scope']={'commits':percommit,'es_commit':ESREF,'es_tree':ESTREE,'protected_distribution_paths_unchanged':True}
    brief=blob('docs/reviews/briefs/es-vendored-and-data.md');check(sha(brief)=='1c27e3380ddde5ed310f4164704ab2257f6b7336d9b114df84a1897b7fd3e631','brief v2 SHA')
    membership=get('stage-a/membership.receipt.json');check(membership['rc']==0,'membership receipt exit')
    for p,h in membership['outputs'].items():check(sha(raw(p))==h,'membership output '+p)
    for stream in ['stdout','stderr']:check(sha(raw('stage-a/membership.'+stream))==membership[stream+'_sha256'],'membership output '+stream)
    helper=blob('docs/qa-logs/2026-11-02-m6-resume/t44-brief-inputs.py');check(sha(helper)==membership['helper_sha256'],'membership helper SHA')
    base='stage-a/inputs/actual-head/';summary=get(base+'summary.json');native=get(base+'native.json');additions=get(base+'additions.json');companions=get(base+'companions.json')
    for p in ['native.json','additions.json','companions.json']:
        check(raw(base+p)==raw('stage-a/inputs/source/'+p)==raw('stage-a/inputs/seed/'+p),'three input populations '+p)
    norm=[]
    for folder in ['source','seed','actual-head']:
        s=get('stage-a/inputs/'+folder+'/summary.json');s.pop('distribution_ref');s.pop('es_ref');norm.append(s)
    check(norm[0]==norm[1]==norm[2],'summary identity apart from named refs')
    check(summary['actual_es_tree']==summary['primary_tree']==ESTREE and summary['primary']==ESREF,'helper root provenance')
    inputs=summary['distribution_inputs'];metadata=[]
    for ref in [summary['P1'],'c348d43dddc4bddbe1055d20d37431503283b817',SEED,FINAL]:metadata.append(git('ls-tree','-r','-z',ref,'--',*inputs))
    check(all(m==metadata[0] for m in metadata),'six survey selectors plus recipe unchanged')
    for path,h in inputs.items():check(sha(blob(path))==h,'distribution bound SHA '+path)
    def estree(ref):
        out={}
        for v in git('ls-tree','-r','-z',ref,repo=ES).rstrip(b'\0').split(b'\0'):
            head,path=v.split(b'\t');mode,typ,oid=head.decode().split();out[path.decode()]=(mode,typ,oid)
        return out
    primary=estree(ESREF);survey=estree(summary['survey']);nativeby={r['path']:r for r in native};addby={r['path']:r for r in additions}
    check(len(nativeby)==len(native)==594 and len(addby)==len(additions)==3 and not(set(nativeby)&set(addby)),'594 and 3 distinct keys')
    for row in native:
        for label,tree in [('primary',primary),('survey',survey)]:
            v=row[label];check(tree[row['path']]==(v['mode'],v['object_type'],v['oid']),'ES metadata '+label+' '+row['path'])
        check(row['changed_since_survey']==(primary[row['path']]!=survey[row['path']]),'native drift flag '+row['path'])
    for row in additions:check(primary[row['path']]==(row['mode'],row['object_type'],row['oid']) and row['path'] not in survey,'supplemental identity '+row['path'])
    modes=collections.Counter(x['primary']['mode'] for x in native);kinds=collections.Counter(x['survey']['kind'] for x in native);tiers=collections.Counter(x['survey']['tier'] for x in native)
    quantities={'native':len(native),'changed':sum(r['changed_since_survey'] for r in native),'unchanged':sum(not r['changed_since_survey'] for r in native),'inventory_lines':sum(r['survey']['inventory_lines'] or 0 for r in native),'survey_text_lines':sum(r['survey']['text_logical_lines'] or 0 for r in native),'primary_text_lines':sum(r['primary']['text_logical_lines'] or 0 for r in native),'supplemental_lines':sum(r['text_logical_lines'] for r in additions)}
    check(list(quantities.values())==[594,40,554,374547,374546,374720,450],'dated populations/totals')
    check(modes=={'100644':583,'100755':10,'160000':1} and kinds=={'text':543,'binary':50,'gitlink':1} and tiers=={'fork-own':51,'upstream-carried':543},'modes/kinds/tiers')
    model=get('stage-b/tables.json');check(model['source_ref']==ESREF and model['source_tree']==ESTREE,'table source identity')
    for title in ['provenance','coverage']:
        rows=model[title];check(len(rows)==len({r['path'] for r in rows})==594 and {r['path'] for r in rows}==set(nativeby),title+' keyset')
        for row in rows:
            v=nativeby[row['path']];expected_sha='not-a-blob' if v['primary']['object_type']=='commit' else v['primary']['sha256'];check((row['kind'],row['mode'],row['blob'],row['sha256'],row['survey_tier'],row['survey_lines'],row['primary_lines'])==(v['survey']['kind'],v['primary']['mode'],v['primary']['oid'],expected_sha,v['survey']['tier'],v['survey']['inventory_lines'],v['primary']['text_logical_lines']),title+' identity '+row['path'])
            check(all(isinstance(row[k],str) and row[k].strip() for k in ['group','origin','license','consumer','reading','method','currency','limit','owner','receipt']),title+' evidence cells '+row['path'])
            if row['kind']=='gitlink' or row['path']=='external/doctest/doctest.h':check(row['read_lines']==0 and not row['fork_written'],'no synthetic/import credit '+row['path'])
    check(len(model['supplemental'])==3 and {x['path'] for x in model['supplemental']}==set(addby),'separate supplemental model')
    check(len(model['companions'])==4 and {x['ref'] for x in model['companions']}=={x['ref'] for x in companions} and all(not x['integrated'] and not x['contains_primary'] for x in model['companions']),'separate companion model')
    # Compare rendered keys, never invoke render/parser/generator.
    text=raw('stage-b/tables.md').decode();forward=raw('02-forward-audit.md').decode();check(text in forward,'rendered tables retained in 02')
    for title in ['Provenance','Coverage']:
        part=text.split('## '+title+'\n',1)[1].split('\n## ',1)[0];lines=[l for l in part.splitlines() if l.startswith('| ')][2:];keys=[l[2:].split(' | ',1)[0] for l in lines]
        check(len(keys)==len(set(keys))==594 and set(keys)==set(nativeby),'rendered '+title+' keys')
    register=get('stage-b/reading-register.json');rrows=register['records'];check(len(rrows)==43,'43 reading-register entries')
    perpop=collections.Counter();lines=collections.Counter()
    for r in rrows:
        v=nativeby[r['path']]['primary'] if r['population']=='native-fork-code' else addby[r['path']]
        check(r['source_ref']==ESREF and r['oid']==v['oid'] and r['sha256']==v['sha256'] and r['range']==[1,v['text_logical_lines']],'full reading bound range '+r['path']);perpop[r['population']]+=1;lines[r['population']]+=r['range'][1]
    check(perpop=={'native-fork-code':40,'supplemental':3} and lines=={'native-fork-code':5017,'supplemental':450},'5017+450 reading register')
    check({x['path'] for x in rrows if x['population']=='native-fork-code'}=={x['path'] for x in model['coverage'] if x['method']=='full-code-read'},'coverage full-code register keys')
    delta=get('stage-b/fork-delta-reading.json');check(len(delta['records'])==5,'five other delta rows')
    for r in delta['records']:check(r['source_sha256']==nativeby[r['path']]['primary']['sha256'],'delta reading input '+r['path'])
    result['populations']={**quantities,'modes':dict(modes),'kinds':dict(kinds),'tiers':dict(tiers),'reading_files':dict(perpop),'reading_lines':dict(lines),'fork_modified_deltas':len(delta['records']),'companion_refs':[c['ref'] for c in companions]}
    collector=get('stage-b/collector-binding.json');check(collector['program_sha256']==sha(raw('tools/collect.py')) and collector['parser_sha256']==sha(raw('tools/catalogue.py')),'collector programs')
    for name,h in collector['inputs'].items():check(sha(raw(base+name))==h,'collector input '+name)
    for name,h in model['input_hashes'].items():check(sha(raw(base+name))==h,'table input '+name)
    consumer=get('stage-c/consumer-input-bindings.json');consumer_gaps=[]
    for name,v in consumer['files'].items():
        expected=v if isinstance(v,str) else v['sha256'];relative=name.removeprefix(AUDIT)
        if relative=='tools/records.py' and sha(raw(relative))!=expected:
            check(sha(raw('stage-d/pre-issue-1/records.py'))==expected,'retained historical records.py identity')
            limits.append({'kind':'historical_consumer_binding','path':'stage-c/consumer-input-bindings.json','entry':name,'recorded_sha256':expected,'current_sha256':sha(raw(relative)),'retained_original':'stage-d/pre-issue-1/records.py','difference':'one Acceptance-criteria scorecard heading correction'})
        elif AUDIT+relative in cache:check(sha(raw(relative))==expected,'consumer bound file '+name)
        else:consumer_gaps.append(name)
    result['consumer_bindings_not_in_audit']=consumer_gaps
    # Existing collector results and their immutable source-read receipts; no PO/XML parsing.
    calls=collector['commands'];check(all(c['rc']==0 for c in calls),'collector stored command exits')
    byspec={c['argv'][-1]:c for c in calls if 'show' in c['argv']}
    pl=get('stage-b/pl024-exact-rename.json');check(len(pl['files'])==37 and sum(x['replacements'] for x in pl['files'])==38 and sum(x['path'].endswith('.po') for x in pl['files'])==35,'PL024 35/37/38')
    for r in pl['files']:
        for side,ref in [('before',pl['commit']+'^'),('after',pl['commit'])]:
            spec=ref+':'+r['path'];c=byspec.get(spec);check(c is not None and c['stdout_sha256']==r[side+'_sha256'],'PL024 collector read '+spec)
    french=get('stage-b/french-deltas-and-calls.json');fcounts={x['owner']:len(x['added']) for x in french};check(fcounts=={'T2':3,'T21':6,'T34':1,'T35':1,'T36':0},'French 3/6/1/1/0')
    sourcecalls=0
    for f in french:
        c=byspec.get(f['ref']+':locale/lang/fr/LC_MESSAGES/emulationstation2.po');check(c is not None and c['stdout_sha256']==f['french_sha256'],'French catalogue read '+f['owner'])
        for a in f['added']:
            check(bool(a['entry']['fields']['msgid']) and bool(a['entry']['fields']['msgstr']) and bool(a['source_calls']),'French nonempty source entries')
            for call in a['source_calls']:
                c=byspec.get(call['ref']+':'+call['path']);check(c is not None and c['stdout_sha256']==call['sha256'],'French source call receipt');sourcecalls+=1
    catalogue=get('stage-b/catalogue-counts.json');xml=get('stage-b/resource-xml.json');vendors=get('stage-b/vendor-groups.json')['groups']
    check(len(catalogue)==36 and len(xml)==77 and len(vendors)==7,'36/77/7 table populations')
    for row in catalogue+xml:check(row['sha256']==nativeby[row['path']]['primary']['sha256'],'catalogue/XML bound identity '+row['path'])
    result['catalogue_and_vendor']={'pl024_files':len(pl['files']),'pl024_PO':pl['po'],'pl024_replacements':pl['replacements'],'French_additions':fcounts,'French_source_calls':sourcecalls,'catalogue_rows':len(catalogue),'XML_rows':len(xml),'vendor_groups':len(vendors),'collector_commands':len(calls)}

    controls=[]
    for path in paths:
        rel=path[len(AUDIT):]
        if not re.fullmatch(r'stage-c/(table|po|guard)-[^/]+\.receipt\.json',rel):continue
        r=get(rel);name=r['name'];fixture=get('stage-c/fixtures/'+name+'.json');check(sha(raw('stage-c/fixtures/'+name+'.json'))==r['fixture_sha256'],'control fixture '+name)
        for n,h in r['programs'].items():check(sha(raw('tools/'+n))==h,'control program '+name+' '+n)
        for stream in ['stdout','stderr']:check(sha(raw('stage-c/'+name+'.'+stream))==r[stream+'_sha256'],'control output '+name+' '+stream)
        predicate=r['expected_predicate'];check(r['rc']==(0 if predicate is None else 1) and (predicate is None or predicate in raw('stage-c/'+name+'.stderr').decode()),'control exact refusal '+name)
        if fixture['kind']=='table':check(fixture['base_sha256']==sha(raw('stage-b/tables.json')),'table control base '+name)
        if fixture['kind']=='catalogue':check(sha(raw(fixture['path']))==fixture['input_sha256'],'PO control bytes '+name)
        controls.append({'name':name,'rc':r['rc'],'predicate':predicate,'fixture_sha256':r['fixture_sha256'],'stdout_sha256':r['stdout_sha256'],'stderr_sha256':r['stderr_sha256']})
    check(len(controls)==18,'18 distinct controls')
    tiny=get('stage-c/tiny-git/receipt.json');check(tiny['program_sha256']==sha(raw('tools/guard-git.py')) and tiny['guard_sha256']==sha(raw('tools/confinement.py')),'tiny Git program binding');check(tiny['rejected_commits']==[tiny['bad'],tiny['tip']] and all(c['rc']==0 for c in tiny['events']),'tiny Git retained edit/revert sequence')
    result['controls']={'cases':controls,'tiny_git_events':len(tiny['events']),'tiny_git_rejected_commits':tiny['rejected_commits'],'tiny_git_private_store_not_read':True}
    # All named ordinary receipt streams, with special stdout names preserved.
    receipts=[];unbound=[];gates_drift={}
    for p in paths:
        rel=p[len(AUDIT):]
        if not (rel.endswith('/receipt.json') or rel.endswith('.receipt.json')):continue
        r=get(rel)
        if 'stdout_sha256' not in r:continue
        if rel.endswith('.receipt.json'):stem=rel.removesuffix('.receipt.json');candidates=[stem+'.stdout',stem+'.json'];stderr=stem+'.stderr'
        else:stem=rel.removesuffix('/receipt.json');candidates=[stem+'/stdout'];stderr=stem+'/stderr'
        out=next((x for x in candidates if AUDIT+x in cache and sha(raw(x))==r['stdout_sha256']),None);check(out is not None,'receipt stdout '+rel)
        if 'stderr_sha256' in r:check(AUDIT+stderr in cache and sha(raw(stderr))==r['stderr_sha256'],'receipt stderr '+rel)
        else:unbound.append({'receipt':rel,'missing_field':'stderr_sha256'})
        receipts.append({'path':rel,'rc':r.get('rc'),'stdout_sha256':r['stdout_sha256'],'stderr_sha256':r.get('stderr_sha256')})
        if rel.startswith('stage-d/') and 'inputs' in r and not rel.startswith('stage-d/local-fixture-whitespace-correction/'):
            drift={n:{'recorded':h,'final':sha(raw(n))} for n,h in r['inputs'].items() if AUDIT+n in cache and sha(raw(n))!=h}
            if drift:gates_drift[rel]=drift
    for v in get('stage-d/gates-summary.json')['gates']:
        stem='stage-d/'+v['gate'];r=get(stem+'/receipt.json');check(sha(raw(stem+'/receipt.json'))==v['receipt_sha256'] and r['rc']==v['rc']==0,'gate summary '+v['gate'])
        for stream in ['stdout','stderr']:check(sha(raw(stem+'/'+stream))==v[stream+'_sha256'],'gate summary stream '+v['gate'])
    result['committed_receipts']={'count':len(receipts),'commands':receipts,'missing_fields':unbound,'recorded_gate_input_changes_to_final':gates_drift}
    external_receipts=[]
    for name,data in external.items():
        if not name.endswith('.receipt.json'):continue
        r=json.loads(data);stem=name.removesuffix('.receipt.json');outname=stem+'.stdout' if stem+'.stdout' in external else stem+'.json'
        check(outname in external and sha(external[outname])==r['stdout_sha256'],'external receipt stdout '+name)
        check(sha(external[stem+'.stderr'])==r['stderr_sha256'],'external receipt stderr '+name)
        external_receipts.append({'receipt':name,'sha256':sha(data),'argv':r['argv'],'rc':r['rc'],'stdout_sha256':r['stdout_sha256'],'stderr_sha256':r['stderr_sha256'],'start':r['start'],'end':r['end']})
    final=json.loads(external['final-readback.json']);check(final['distribution_tip']==final['remote_tip']==FINAL and final['es_head']==ESREF and final['es_tree']==ESTREE,'final published source bindings')
    check(all(e['rc']==0 for e in final['events']) and len(final['events'])==6,'six final readback event exits')
    expected=[FINAL,FINAL+'\trefs/heads/feature/m6-es-vendored-and-data-691','',ESREF,ESTREE,'']
    check([e['stdout'].strip() for e in final['events']]==expected and all(e['stderr']=='' for e in final['events']),'raw final HEAD/remote/status/ES readbacks')
    check(json.loads(external['corrected-payload-readback.stdout'])==final['payload'] and final['payload_receipt_sha256']==sha(external['corrected-payload-readback.receipt.json']),'external corrected payload result')
    live=json.loads((ROOT/'live-issues.json').read_text());checkpoint=json.loads(external['checkpoint-readback.json']);expected_checkpoint=json.loads(external['expected-checkpoint.json'])
    current=[c for c in live['issue691']['comments'] if str(c['id'])=='6591199715'];check(len(current)==1 and checkpoint['body']==current[0]['body'],'live checkpoint body')
    check(sha(checkpoint['body'].encode())==json.loads(external['checkpoint-readback.receipt.json'])['body_sha256'],'checkpoint body SHA')
    tracker=get('stage-d/tracker/1413-final-readback.json');own=get('stage-d/tracker/691-live.json');parent=get('stage-d/tracker/1413-parent-readback.json')
    check(tracker['body']==live['issue1413']['issue']['body'] and own['body']==live['issue691']['issue']['body'],'live owning issue bodies')
    check(parent['number']==691 and tracker['state']=='open' and tracker['milestone']['number']==6,'retained audit parent/state/milestone')
    result['publication']={'commands':external_receipts,'final_events':final['events'],'whole_ES_clean_at_receipt':final['es_clean'],'distribution_clean_at_receipt':final['distribution_clean'],'checkpoint_id':checkpoint['id'],'tracker_body_equal':True}
    result['errors']=errors;result['limits']=limits
    save('results.json',result);journal()
    print(json.dumps({k:v for k,v in result.items() if k not in ['committed_receipts','publication','controls']},indent=2))
    print('RECEIPTS',len(receipts),'EXTERNAL COMMANDS',len(external_receipts),'GATE DRIFT',len(gates_drift),'MISSING FIELDS',unbound)

if __name__=='__main__':main()

#!/usr/bin/env python3
"""Read-only immutable object/snapshot comparison; no project checks are executed."""
import collections, hashlib, json, pathlib, re, subprocess
P=pathlib.Path(__file__).resolve().parent
R='/workspace/repos/pixelelated/distribution.worktrees/m6-p1-survey-641'
D='c9fe606e8d7e7e0f6c70cc686764d1503029d278'
C='94b5b1c0b983313325dba101217761c6e5c9bca0'
OLD='3cd9ca140a0da9af447a3ee2fb9cdbbbf222a95b'
P1='2174265e9cc1b248c0fbe27fa101875984d46d6b'
SOURCE='02aab33bd9842610b0d466c9c186454dc14373ee'
COORD='07d01c898fba867e042342017fd8d5257508a28c'
A='docs/audits/2026_11_02-epic-m6-patches-shipped-kernel/'
SD=A+'stage-d/'
commands=[]
def git(*args):
    commands.append(['git','-C',R,*args])
    return subprocess.check_output(commands[-1])
def blob(ref,path): return git('show',ref+':'+path)
def doc(path): return blob(D,A+path).decode()
def jdoc(path): return json.loads(doc(path))
def local(name): return json.loads((P/(name+'.json')).read_text())
def sha(b): return hashlib.sha256(b).hexdigest()
def tree(ref,paths):
    out={}
    for row in git('ls-tree','-rz',ref,'--',*paths).split(b'\0'):
        if row:
            meta,path=row.split(b'\t',1); mode,kind,oid=meta.decode().split()
            out[path.decode()]={'mode':mode,'kind':kind,'oid':oid}
    return out
results={'identity':'Codex / OpenAI; harness session 01a19d11-dda5-72e3-86f9-416f36341c24; m6-p1-survey wN:p3',
         'refs':{'packet':D,'accepted_c':C,'original_blocker':OLD,'p1':P1,'source':SOURCE,'coordinator':COORD}}
protected=[A+x for x in ['stage-a','stage-b','stage-c','tools','second-opinions']]
at_d=tree(D,protected)
results['preservation']={}
for label,ref in [('accepted_c',C),('original_blocker',OLD)]:
    before=tree(ref,protected)
    results['preservation'][label]={'count':len(before),'different_or_missing':[p for p,v in before.items() if at_d.get(p)!=v],
        'added_since':len(set(at_d)-set(before))}
paths=doc('stage-a/p1-qa-scratch/paths.txt').replace('\\u002d','-').splitlines()
source_d=tree(D,paths)
results['source']={'membership':len(paths),'unique':len(set(paths)),'tree_entries':len(source_d),
    'modes':dict(collections.Counter(v['mode'] for v in source_d.values())),
    'differences':{}}
for label,ref in [('p1',P1),('source',SOURCE),('accepted_c',C)]:
    before=tree(ref,paths)
    results['source']['differences'][label]=[p for p in paths if before.get(p)!=source_d.get(p)]
dispatch=git('rev-parse','d7dd766659^{commit}').decode().strip()
results['refs']['dispatch']=dispatch
results['protected_code_changed']=git('diff','--name-only',dispatch,D,'--','*.patch','*.conf','packages','projects','tools','scripts').decode().splitlines()
results['rules_register_briefs_changed']=git('diff','--name-only',C,D,'--','docs/decision-register.md','AGENTS.md','CLAUDE.md','.claude','docs/reviews').decode().splitlines()
changed=git('diff','--name-only',C,D).decode().splitlines()
allowed={A+x for x in ['00-running-log.md','02-forward-audit.md','04-analysis.md','05-punch-list.md','06-audit-summary.md','07-questions-for-the-maintainer.md']}
allowed|={'.github/sessions/saved-session-state-feature-m6-patches-shipped-kernel-688.md','docs/work-logs/2026_11-work_logs/2026_11_02-work_log.md','docs/work-logs/INDEX.md'}
results['scope']={'changed_paths':len(changed),'outside_allowed':[p for p in changed if p not in allowed and not p.startswith(SD)]}
d_tree=tree(D,[SD]); raw={p:blob(D,p) for p in d_tree}
results['stage_d_files']=len(d_tree)
manifest=[]
for p,entry in d_tree.items(): manifest.append({'path':p,**entry,'bytes':len(raw[p]),'sha256':sha(raw[p])})
for p in ['05-punch-list.md','06-audit-summary.md','07-questions-for-the-maintainer.md']:
    b=blob(D,A+p);manifest.append({'path':A+p,**tree(D,[A+p])[A+p],'bytes':len(b),'sha256':sha(b)})
v=json.loads(raw[SD+'validation.json'])
results['validation']={'recorded_result':v['result'],'start':v['start'],'end':v['end'],
    'script_hash_matches':sha(raw[SD+'verify-records.py'])==v['script_sha256'],'checks':[]}
for c in v['checks']:
    b=raw[SD+c['output']]
    results['validation']['checks'].append({'name':c['name'],'recorded_rc':c['rc'],'sha256':sha(b),'hash_matches':sha(b)==c['sha256'],
        'output':c['output'],'start':c['start'],'elapsed_seconds':c['elapsed_seconds']})
results['bodies']={}
for n,file,retained in [(1408,'0010-bug.md','issue-1408-readback.json'),(1409,'audit-final.md','issue-1409-final-readback.json')]:
    live=local('issue-'+str(n)); expected=raw[SD+'issues/'+file].decode();ret=json.loads(raw[SD+retained])
    results['bodies'][str(n)]={'live_equals_submitted':live['body']==expected,'retained_equals_submitted':ret['body']==expected,
        'live_body_sha256':sha(live['body'].encode()),'state':live['state'],'labels':sorted(x['name'] for x in live['labels']),
        'milestone':live['milestone'],'open_checkboxes':len(re.findall(r'^- \[ \]',live['body'],re.M)),
        'checked_checkboxes':len(re.findall(r'^- \[[xX]\]',live['body'],re.M)),'updated_at':live['updated_at']}
results['parents']={'audit_live':local('parent-1409')['number'],'audit_retained':json.loads(raw[SD+'audit-parent-readback.json'])['number'],
    'bug_live':local('parent-1408')['error_data'],'bug_retained':json.loads(raw[SD+'bug-parent-readback.json'])}
results['questions']={}
for i,cid in [(1,6585346506),(2,6585347732)]:
    live=local('question-'+str(cid));ret=json.loads(raw[SD+f'question-{i}-readback.json']);expected=raw[SD+f'issues/question-{i}.md'].decode()
    results['questions'][str(cid)]={'live_equals_submitted':live['body']==expected,'retained_equals_submitted':ret['body']==expected,
        'body_sha256':sha(expected.encode()),'id_matches':live['id']==ret['id']==cid,'url':live['html_url']}
forward=doc('02-forward-audit.md');log=doc('00-running-log.md');analysis=doc('04-analysis.md');punch=doc('05-punch-list.md')
score=json.loads(raw[SD+'scorecard.json']); rendered=[f'| AC-{i:02d} | {title} | {status} | {detail} |' for i,(title,status,detail) in enumerate(score,1)]
results['scorecard']={'rows':len(score),'counts':dict(collections.Counter(x[1] for x in score)),
    'partial':[i for i,x in enumerate(score,1) if x[1]=='PARTIAL'],
    'exact_rows_in_02_04_live_audit':all(row in forward and row in analysis and row in local('issue-1409')['body'] for row in rendered)}
results['record_facts']={'proved_cells':len(re.findall(r'proved:',forward)), 'proof_log_lines':len(re.findall(r'^PROOF:',log,re.M)),
    'leads':re.findall(r'^\| (L-\d\d) \|',forward,re.M),'rulings':re.findall(r'^\| ([a-p]) \|',forward,re.M),
    'punch_headings':re.findall(r'^## (PL-\d+)',punch,re.M),'open_outcome':'outcome: open' in punch,
    'original_hygiene_quoted':doc('stage-b/corrected/hygiene.out') in forward,
    'accepted_tables_quoted':{x:doc('stage-b/corrected/table-'+x+'.txt').strip() in forward for x in ['provenance','coverage']},
    'parent_open_checkboxes':len(re.findall(r'^- \[ \]',local('issue-688')['body'],re.M)),
    'parent_checked_checkboxes':len(re.findall(r'^- \[[xX]\]',local('issue-688')['body'],re.M))}
brief='docs/reviews/briefs/patches-shipped-kernel.md';bc=blob(COORD,brief);bd=blob(D,brief)
results['brief']={'current_sha256':sha(bc),'packet_sha256':sha(bd),'diff':git('diff',D,COORD,'--',brief).decode()}
results['milestone']={k:local('milestone-6')[k] for k in ['number','title','updated_at']}
results['milestone']['current_recovery_paragraph']=local('milestone-6')['description'].split('\n\n')[1]
results['parent_note']=json.loads(raw[SD+'parent-response-note.json'])
for name,data in [('results.json',results),('artifact-hashes.json',manifest),('commands.json',commands)]:
    (P/name).write_text(json.dumps(data,indent=2)+'\n')
print(json.dumps({k:v for k,v in results.items() if k not in ['brief','milestone','parent_note']},indent=2))

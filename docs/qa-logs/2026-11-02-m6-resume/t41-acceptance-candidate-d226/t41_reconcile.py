"""D226 accepted-producer reconciliation: object reads only, no replay.
Immutable anchors bind commands, fixtures and observations. New measurements are
limited to stored bytes; historical archive/tree digests remain observations.
"""
STAGE_A='cffe3f869c5ced124e26befa36505350b4964f77'
STAGE_A_PROGRAM='f03b64419fa656fb3af61cbc8d174284020d439c'
STAGE_B='7e5d1546712df2eb79c585fce663186770d1ceb9'
STAGE_C='94b5b1c0b983313325dba101217761c6e5c9bca0'
P1='2174265e9c'
T4='6ec78bbf8c'
T4_FOLDER='docs/audits/2026_10_24-epic-m6-doctrine-rules'
BLOCK_SHA='4d300124a6bf116f9c0177712e8f0a824b35db45cc5a042acbd4cc58445192a3'

def unchanged(r,path,ref):
    a=r.tree(ref,path);b=r.tree(r.tip,path)
    if not a:raise Absent('accepted identity absent: '+path+' at '+ref)
    need(a==b,'changed accepted input/program/mode: '+fmt(path)+' (anchor '+ref[:12]+')')
    return r.blob(path,ref)

def frozen_receipt(r,path,ref):
    expected=r.blob(r.af+'/'+path,ref)
    actual=r.audit(path)
    need(expected==actual,'accepted receipt changed: '+path)
    return actual

def reconcile_membership(r):
    brief=r.blob(BRIEF,AUTH).decode()
    def extract(name,lang):
        a='<!-- t41 '+name+' begin -->';b='<!-- t41 '+name+' end -->'
        need(brief.count(a)==brief.count(b)==1,'membership brief marker shape')
        chunk=brief.split(a,1)[1].split(b,1)[0]
        m=re.search(r'\n```'+lang+r'\n(.*?)\n```\n',chunk,re.S)
        need(m is not None,'membership brief fence shape');return (m.group(1)+'\n').encode()
    block=extract('block.sh','bash');expected=extract('block expected','')
    need(sha(block)==BLOCK_SHA or (r.fixture and block==r.blob(r.af+'/stage-a/p1-qa-scratch/block.sh',STAGE_A)),'membership block SHA mismatch')
    need(len(block.splitlines())==148 and len(expected.splitlines())==99,'membership 148/99 shape differs')
    for p in ['block.out','block-tip.out','p1-qa-scratch/block-expected.txt']:
        need(dec(frozen_receipt(r,'stage-a/'+p,STAGE_A).decode())==dec(expected.decode()),'retained 99-line output differs')
    need(frozen_receipt(r,'stage-a/p1-qa-scratch/block.sh',STAGE_A)==block,'retained block differs from authority')
    for name in ['slices','inventory','areas']:
        path='docs/reviews/'+name+'.json';unchanged(r,path,P1)
    paths=None
    for side in ['p1','tip']:
        for name in ['paths','text']:
            b=frozen_receipt(r,f'stage-a/{side}-qa-scratch/{name}.txt',STAGE_A)
            ps=dec(b.decode()).splitlines()
            need(len(ps)==len(set(ps))==107 and ps==sorted(ps),'membership paths not 107 sorted unique')
            if paths is None:paths=ps
            need(ps==paths,'P1/tip/text selected paths differ')
    need(paths==sorted(dec(x['path']) for x in r.inventory()),'corrected inventory membership differs')
    # Modes and objects, not a re-execution of the historical membership program.
    all_p1=r.tree(P1,'');all_tip=r.tree(r.tip,'')
    for p in paths:
        need(p in all_p1 and all_p1[p].split()[0] in ['100644','100755'],'selected path is not a regular blob')
        need(all_tip.get(p)==all_p1[p],'selected immutable mode/blob changed: '+fmt(p))
    check(r,'tree-counts')
    combined=frozen_receipt(r,'stage-a/run/stage-a.out',STAGE_A).decode()
    for t in ['block rc=0','block at the tip rc=0','block = the brief\'s expected lines','the same lines at the tip']:need(t in combined,'membership command/exit evidence absent')
    return 'D226: 148-line retained block, identical 99-line outputs, three P1 inputs, 107 selected modes/blobs/counts reconciled; no replay'

def reconcile_lint(r):
    # The accepted command names an immutable full T4 folder plus one exact JSON
    # deletion. This identifies the fixture without opening its retired scratch.
    brief=r.blob(BRIEF,AUTH).decode()
    for text in ['F=$(git ls-tree -d --name-only 6ec78bbf8c','d.pop("tier_exception",None)','tools/lint-audit-artifacts "$L/pass/$F"','tools/lint-audit-artifacts "$L/fail/$F"']:
        need(text in brief,'historical Local fixture command identity changed')
    unchanged(r,'tools/lint-audit-artifacts',STAGE_A_PROGRAM)
    tree=r.tree(T4,T4_FOLDER+'/');need(bool(tree),'T4 fixture identity absent')
    # No archive/export: hash selected committed blobs, including the plan, in memory.
    for p in tree:unchanged(r,p,T4)
    plan=json.loads(r.blob(T4_FOLDER+'/second-opinions/review-plan.json',T4))
    need(plan.get('depth')=='local' and plan.get('tier_exception')=='D-WORKFLOW-184' and plan.get('reviewers')==[],'historical Local fixture has wrong plan')
    positive=frozen_receipt(r,'stage-a/lint-local-pass.out',STAGE_A).decode()
    negative=frozen_receipt(r,'stage-a/lint-local-fail.out',STAGE_A).decode()
    raw=frozen_receipt(r,'stage-a/run/stage-a.out',STAGE_A).decode()
    need(positive.rstrip().endswith('\nPASS'),'historical Local positive lacks PASS')
    need('FAIL  second-opinions/review-plan.json or its call evidence is invalid: local-only cannot satisfy Epic/Milestone' in negative and negative.rstrip().endswith('1 CONTRACT FAILURE(S)'),'historical Local refusal differs')
    for t in ['t4 plan: local D-WORKFLOW-184 0','lint, a Local plan, rc=0','lint, tier_exception removed, rc=1']:need(t in raw,'historical Local exit/fixture receipt absent')
    return 'D226: exact unchanged lint/T4 immutable fixture, tier_exception deletion command, positive/refusal and rc receipts reconciled; no replay'

def reconcile_generator(r):
    # Read-only Stage-C promotion packet. It does not certify newly changed inputs.
    validation=json.loads(frozen_receipt(r,'stage-c/validation.json',STAGE_C))
    promotion=json.loads(frozen_receipt(r,'stage-c/promotion.json',STAGE_C))
    program=unchanged(r,r.af+'/tools/t41-tables.py',STAGE_C)
    need(sha(program)==validation['checked_program_sha256']==promotion['formal_sha256'],'formal generator identity differs')
    draft=unchanged(r,r.af+'/stage-b/corrected/t41-tables.py',STAGE_B)
    need(sha(draft)==promotion['draft_sha256'],'draft generator identity differs')
    # All retained corrected inputs/source bytes must still be identical. No private
    # negative-fixture directory is opened and no historical generator is invoked.
    for p in r.tree(STAGE_C,r.af+'/stage-b/corrected/'):
        unchanged(r,p,STAGE_C)
    for row in r.inventory():unchanged(r,dec(row['path']),SOURCE)
    checks=validation['checks']
    modes=['stats','provenance','coverage','currency','json']
    names=['formal-generator-negative-'+x for x in ['drop','reach','header']]+['formal-generator-'+x for x in modes]
    selected=[x for x in checks if x.get('name') in names]
    need([x['name'] for x in selected]==names,'three negatives must precede five positives')
    assertions=['membership: expected 107 rows','reach: expected shipped 103/test 4','From header census: expected 87']
    for i,x in enumerate(selected):
        out=frozen_receipt(r,'stage-c/'+relpath(x['output']),STAGE_C)
        need(sha(out)==x['sha256'],'formal generator output hash differs')
        need(x['argv'][:3]==['python3','-I',r.af+'/tools/t41-tables.py'],'formal generator command differs')
        need(x['start'] and x['elapsed_seconds']>=0,'generator command timing absent')
        if i<3:
            kind=['drop','reach','header'][i];opt='--bytes-from' if kind=='header' else '--rows-from'
            suffix='/bytes' if kind=='header' else '/'+kind+'.json'
            need(x['rc']==1 and x['argv'][3:5]==['stats',opt] and len(x['argv'])==6 and x['argv'][5].endswith(suffix),'negative control command/exit differs')
            need(out.decode().splitlines()[-1]=='AssertionError: '+assertions[i],'negative control assertion differs')
        else:
            mode=modes[i-3];need(x['rc']==0 and x['argv'][3:]==[mode],'positive command/exit differs')
            need(out==r.corrected('table-'+mode+'.txt'),'positive not equal to accepted corrected table')
    need(validation['outputs_equal_accepted_tables'] is True,'formal output comparison absent')
    # The published packet binds program and OUTPUT hashes, but not exact negative
    # INPUT bytes. D226 explicitly requires those identities. Do not infer them
    # from an absolute argv path or recreate fixtures. Await coordinator disposition.
    missing=[x['name'] for x in selected[:3] if not x.get('input_identity')]
    if missing:raise Cannot('D226 exact negative input identities absent in accepted stage-c/validation.json: '+', '.join(missing)+'; paths and assertions do not identify bytes; coordinator evidence/ruling required, no replay')
    # Reserved executable seam for a future coordinator-authorized identity record.
    # No current producer supplies one, so a foreign shape cannot silently pass.
    raise Cannot('D226 negative input identity record now present but its schema/authority is not ruled; coordinator integration required, no replay')

def reconcile_check(r,s):
    if s=='membership':return reconcile_membership(r)
    if s=='lint-proof':return reconcile_lint(r)
    if s=='checker-run':return reconcile_generator(r)
    if s=='runs':
        validate_applications(r);check(r,'tarball-hashes');check(r,'runs-record')
        return 'D226: accepted 120/106 normal-application receipts, log/source hashes, prefix links/control and H700-011 reconciled; archive/tree digests are retained observations'
    raise Invalid('unknown reconciliation gate')

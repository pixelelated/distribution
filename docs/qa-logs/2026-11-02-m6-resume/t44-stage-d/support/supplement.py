"""Named metadata/receipt joins only; no source parser or producer execution."""
from reconcile import *
def main():
    errors=[];out={}
    def check(ok,label):
        if not ok:errors.append(label)
    native=j('stage-a/inputs/actual-head/native.json');by={r['path']:r for r in native};companions=j('stage-a/inputs/actual-head/companions.json')
    ext_oid=git('rev-parse',ESREF+':external',repo=ES).decode().strip()
    for c in companions:
        check(git('rev-parse',c['ref']+':external',repo=ES).decode().strip()==c['external_tree']==ext_oid,'companion external tree '+c['owner'])
        mode,typ,oid=git('ls-tree',c['ref'],'--','locale/lang/fr/LC_MESSAGES/emulationstation2.po',repo=ES).decode().split()[:3]
        check((mode,typ,oid)==(c['french']['mode'],c['french']['object_type'],c['french']['oid']),'companion French identity '+c['owner'])
    doctest='external/doctest/doctest.h';import_ref='324f9c483d9b4a11249c47888b40fb5cc691be7f'
    check(git('ls-tree',ESREF,'--',doctest,repo=ES)==git('ls-tree',import_ref,'--',doctest,repo=ES),'doctest import same mode/OID')
    out['metadata']={'companion_external_tree':ext_oid,'companions_bound':4,'doctest_import':import_ref,'doctest_unchanged':True}
    negative=j('stage-d/payload-reader-negative/receipt.json');check(negative['program_sha256']==sha(b('tools/payload-readback.py')) and negative['rc']==1,'payload negative exact program/exit')
    for stream in ['stdout','stderr']:check(sha(b('stage-d/payload-reader-negative/'+stream))==negative[stream+'_sha256'],'payload negative '+stream)
    out['manifest_failure']={'original_record_lacks_full_argv_times_raw_streams':True,'subsequent_bound_negative_rc':negative['rc'],'negative_program_sha256':negative['program_sha256'],'negative_stderr_sha256':negative['stderr_sha256']}
    document=j('stage-d/document-readback.json')
    for n,h in document['inputs'].items():
        rel=n if n=='02-forward-audit.md' else 'stage-b/'+n
        check(sha(b(rel))==h,'document reader current binding '+n)
    # Read selected outputs as text to establish the scope of their PASS.
    gate_text={n:b('stage-d/'+n+'/stdout').decode() for n in ['pre-issue-2','issue-lint-1','issue-check-1','forbidden-1','index-2','syntax-3','diff-3']}
    check(all('PASS pre-issue artifacts (does not certify resolution)' in gate_text[n] for n in ['pre-issue-2','issue-lint-1']),'both lint receipts are pre-issue only')
    check('0 fail' in gate_text['issue-check-1'] and '1 open checkbox' in gate_text['issue-check-1'],'audit box check')
    check('0 hits in 134259 tracked files' in gate_text['forbidden-1'],'recorded forbidden population')
    out['gate_output_scope']=gate_text
    for n in ['index-2','syntax-3','diff-3']:
        r=j('stage-d/'+n+'/receipt.json');check(r['rc']==0 and all(sha(b(p))==h for p,h in r['inputs'].items()),'current final document inputs '+n)
    out['current_document_bound_gates']=['index-2','syntax-3','diff-3']
    # Historical frozen program version remains exactly recoverable, with only one heading changed.
    old=b('stage-d/pre-issue-1/records.py');new=b('tools/records.py')
    check(old.replace(b'## Acceptance criteria Scorecard',b'## Acceptance-criteria scorecard')==new,'only records.py heading changed')
    out['historical_consumer_binding']={'old':sha(old),'current':sha(new),'only_heading_correction':True}
    # Disposition, identity and source boundaries remain record facts.
    plan=j('second-opinions/review-plan.json');out['review_plan']=plan
    check(plan['depth']=='local' and plan['reviewers']==[],'Local reviewers empty')
    snapshot=j('stage-d/owned-scratch-census.json');out['scratch_census_shape']={'keys':list(snapshot),'files':len(snapshot.get('files',[])),'all_paths_left_unread':True}
    out['errors']=errors;save('supplement-results.json',out);journal();print(json.dumps(out,indent=2))
if __name__=='__main__':main()

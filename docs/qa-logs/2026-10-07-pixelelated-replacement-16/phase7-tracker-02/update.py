from pathlib import Path
from datetime import datetime, timezone
import hashlib, json, os, subprocess, sys

owner = Path(__file__).resolve().parent
repo = Path.cwd()
(owner/'run.path').write_text(str(repo/os.environ['RASTERATOPS_BUILD_RUN'])+'\n')
def save(name, value):
    p = owner/'artifacts'/name
    with p.open('x') as f: json.dump(value, f, indent=2); f.write('\n')
    return p
def api(path, data=None, label=None):
    cmd=['gh','api','repos/pixelelated/distribution/'+path]
    if data is not None: cmd+=['--method','PATCH','--input',str(save(label+'-request.json',data))]
    return json.loads(subprocess.check_output(cmd,text=True))
rc=1
try:
    for path,digest in json.loads((owner/'seal.json').read_text()).items():
        assert hashlib.sha256(Path(path).read_bytes()).hexdigest()==digest
    for number in [468,479]:
        original=api('issues/'+str(number));save(str(number)+'-before.json',original)
        body=original['body'].replace('1280×720','1280×800')
        assert body!=original['body'] and original['state']=='closed'
        api('issues/'+str(number),{'body':body},str(number)+'-body')
        final=api('issues/'+str(number));assert final['body']==body and final['state']=='closed'
        save(str(number)+'-after.json',final)
        old=json.loads(Path('/workspace/tmp/pixelelated-m7-phase7-tracker-01/artifacts',str(number)+'-comment.json').read_text())
        comment=api('issues/comments/'+str(old['id']));save(str(number)+'-comment-before.json',comment)
        revised=comment['body'].replace('1280×720','1280×800')
        api('issues/comments/'+str(old['id']),{'body':revised},str(number)+'-comment')
        after=api('issues/comments/'+str(old['id']));assert after['body']==revised
        save(str(number)+'-comment-after.json',after)
    original=api('issues/461');save('461-before.json',original)
    heading='## Current execution — 2026-10-07 01:51 UTC'
    start=original['body'].index(heading)
    body=original['body'][:start]+'''## Current execution — after candidate 16 qualification

Candidate 16's VM qualification and eight audit resolutions are complete.
The audit and compound software issues are closed with exact tracker readbacks.
This review now precedes H700 DDR4 RG35XX SP arm, then aarch64, in M7.P5.
It remains infrastructure work outside the software RC acceptance criteria.

Current available space is about 149 GiB. Existing H700 build roots allocate
27.98 GiB (arm) and 109.74 GiB (aarch64); those measurements alone do not
establish headroom for independent build, artifact and verification copies.
Prepare a repeatable read-only report with actual identities, retained inputs,
backing chains, cross-store references, active use, preservation cost and a
separate capacity result for each architecture. Test refusal controls in
isolated host fixtures. No candidate disk, build tree or cache is deleted by
the planner.

Can this be done on the VM? No: host allocation, active host/container use and
cross-compilation workspace ownership are host facts. Planner controls use
temporary host fixtures; production inspection is read-only.

The first later batch was the exact two standalone QA files in D-INFRA-019,
already completed: 9.98 GiB recovered, 53 evidence hashes and 15 protected
identities unchanged. No wider cleanup or reserve change is authorized.
The repeatable report and rejection controls remain the two open criteria.

Published software evidence: next `7f293a22d97317d1632952a5cf2e9d4a45bd2cb2`,
`docs/audits/2026_10_06-milestone-m7-p4-fixes-383/08-installed-resolution.md`.
'''
    api('issues/461',{'title':'M7.P5: Review build retention before device builds','milestone':7,'body':body},'461')
    final=api('issues/461');assert final['body']==body and final['milestone']['number']==7 and final['state']=='open'
    save('461-after.json',final)
    save('completion.json',{'utc':datetime.now(timezone.utc).isoformat(),'result':'PASS','corrected_dimensions':[468,479],'scheduled_retention_issue':461,'no_product_change':True})
    print('PASS corrected tracker dimensions to actual 1280×800; #461 scheduled under M7.P5 with exact readbacks',flush=True)
    rc=0
finally:
    (owner/'inner.rc').write_text(str(rc)+'\n');(owner/'outer.rc').write_text(str(rc)+'\n')
sys.exit(rc)

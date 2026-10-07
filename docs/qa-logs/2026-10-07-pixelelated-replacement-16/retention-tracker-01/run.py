from pathlib import Path
from datetime import datetime, timezone
import hashlib,json,os,subprocess,sys
owner=Path(__file__).resolve().parent
(owner/'run.path').write_text(str(Path.cwd()/os.environ['RASTERATOPS_BUILD_RUN'])+'\n')
publication=Path('/workspace/tmp/pixelelated-m7-retention-publication-09')
assert json.loads((publication/'owner-verification.json').read_text())['result']=='PASS'
pub=json.loads((publication/'publication.json').read_text());head=pub['next']
root='https://github.com/pixelelated/distribution/tree/'+head+'/'
qa='docs/qa-logs/2026-10-07-pixelelated-replacement-16/'
def save(name,data):
 p=owner/'artifacts'/name
 with p.open('x') as f:json.dump(data,f,indent=2);f.write('\n')
 return p
def api(path,data=None,label=None):
 cmd=['gh','api','repos/pixelelated/distribution/'+path]
 if data is not None:cmd+=['--method','PATCH','--input',str(save(label+'-request.json',data))]
 return json.loads(subprocess.check_output(cmd,text=True))
def snapshot(row):return {k:row.get(k) for k in ['number','title','body','state','state_reason','updated_at','html_url']}
rc=1
try:
 for path,sha in json.loads((owner/'seal.json').read_text()).items():assert hashlib.sha256(Path(path).read_bytes()).hexdigest()==sha
 for number,expected in [(461,2),(490,3),(491,3)]:
  row=api('issues/'+str(number));save(str(number)+'-before.json',snapshot(row));assert row['state']=='open' and row['body'].count('- [ ]')==expected
  if number==491:
   body=row['body'].replace('- [ ]','- [x]',1)
   body+='\n\nVerification-only completed with all four result channels zero, four seals and actual owner exits. [Exact proposal, file list and fixed-scope helper]('+root+qa+'h700-retirement-proposal); [verification receipt]('+root+qa+'retirement-verification-01). No --apply or approval record was supplied; nothing was removed. Separate explicit approval of this exact batch is still required.\n'
  else:
   body=row['body'].replace('- [ ]','- [x]')
   if number==461:
    i=body.index('## Current execution');body=body[:i]
   body+='\n\n## Completed read-only reporting\n\nPublished on next `'+head+'`. The fresh report inspects 3,722,420 directories and the same 311 disk chains as the original report. All 24 original QA disk hashes/identities and protected-root identities are unchanged. Sixty-four exact source samples match the pinned shared-mime-info archive; nineteen controls pass. There are zero unresolved dependencies, 22 eligible files and two held referenced bases. The original conservative refusal remains retained.\n\n'
   body+='[Report and source provenance]('+root+qa+'retention-review-02); [independent reconciliation and exact proposal]('+root+qa+'h700-retirement-proposal). No deletion occurred. The earlier D-INFRA-019 batch remains the completed first later batch. New execution is separately tracked in #491 and awaits its own explicit authorization; the report does not extend the earlier approval.\n'
  check=api('issues/'+str(number));assert check['body']==row['body'] and check['state']=='open'
  api('issues/'+str(number),{'body':body},str(number)+'-body')
  if number!=491:api('issues/'+str(number),{'state':'closed','state_reason':'completed'},str(number)+'-close')
  final=api('issues/'+str(number));assert final['body']==body and final['state']==('open' if number==491 else 'closed')
  save(str(number)+'-after.json',snapshot(final));print('PASS tracker #'+str(number),flush=True)
 m=api('milestones/7');save('milestone-before.json',m)
 body=m['description'][m['description'].index('## Ordered critical path'):]
 body=body.replace('**NEXT: capacity review #461 → H700 DDR4 RG35XX SP arm → aarch64**. Then named physical and publication gates.','**CURRENT: approval/execution of exact cleanup #491 → H700 arm compatibility build → renewed aarch64 capacity review and firmware build**. Then named physical and publication gates.')
 body=body.replace('complete above; build and installed behavior proof remain.','complete; candidate16 installed behavior proof is accepted.')
 body=body.replace("#327's implemented explanation-page change is now a P3 frame/docs verification item.","#327's explanation-page source/frame/asset criteria are completed; public site publication remains P5.")
 body=body.replace('The fixes review belongs to #383. #375/#382 are the completed initial review and dispositions; do not restart them. Use the approved cross-lab depth and verified receipts. Resolve findings, renew affected artifact evidence, then make the RC readiness call.','The fixes review #383/#471 is complete, with all eight findings resolved on rebuilt and qualified candidate16. #375/#382 are the completed initial review and dispositions; do not restart any completed audit. Verified cross-lab receipts and installed resolutions remain retained.')
 top='''## Current priority — exact cleanup approval before H700

P3 GENERIC_X64 qualification and P4 fixes audit are complete on candidate16.
All eight findings and compound software gates are closed. The completed-audit
cadence correction #489 is published and hosted checks pass.

1. **#491: separate approval and guarded execution of the exact22-file QA
   disk proposal.** Read-only review #461 and source classification #490 are
   complete. The 42.05GiB batch excludes two referenced bases and preserves
   candidate/fallback, ROCKNIX baseline, source/cache and independent evidence.
   Verification-only passed; no deletion has occurred. Prior two-file approval
   is fully consumed and does not cover this batch.
2. **H700 DDR4 RG35XX SP arm compatibility build**, under the standard watcher
   with active result delivery after verified capacity and build preflight.
   Its conservative budget is185.98GiB including100GiB operating allowance;
   the batch would increase available space from149.25GiB to191.29GiB.
3. **Remeasure capacity for H700 aarch64, then build the firmware.** Its
   conservative combined forecast is353.72GiB; this first batch does not
   establish that fit. Preserve the old device/fallback tree.
4. **Named physical/P5 gates:** artifact verification, device adoption/smoke
   facts, corresponding source,14known licence metadata gaps, public docs and
   manifest-bound release assets. Device actions and publication retain their
   named scope. No RC designation or release publication is claimed.

The fresh host review inspected3,722,420directories and311disk chains with no
unresolved dependencies. All24original QA file hashes/identities and protected
root identities are unchanged;64source samples match the pinned archive and
19controls pass. No new RA reset or Dropbox credential is needed.

Can this be done on the VM? Software qualification is already complete there.
Capacity, file dependencies and compilation ownership are host facts. Physical
smoke gates retain their named hardware facts and separate action scope.

Watchers record status; the primary consumes results. Off-session alerts#395,
FOSS observability#432 and automated RA reset#464 retain their later scope.

'''
 for old,new in [('exact22','exact 22'),('42.05GiB','42.05 GiB'),('is185.98GiB','is 185.98 GiB'),('including100GiB','including 100 GiB'),('from149.25GiB to191.29GiB','from 149.25 GiB to 191.29 GiB'),('is353.72GiB','is 353.72 GiB'),('source,14known','source, 14 known'),('inspected3,722,420directories and311disk','inspected 3,722,420 directories and 311 disk'),('All24original','All 24 original'),('unchanged;64source','unchanged; 64 source'),('19controls','19 controls'),('alerts#395','alerts #395'),('observability#432','observability #432'),('reset#464','reset #464')]:top=top.replace(old,new)
 body=top+'[Exact proposal and file list]('+root+qa+'h700-retirement-proposal).\n\n'+body
 check=api('milestones/7');assert check['description']==m['description']
 api('milestones/7',{'description':body},'milestone')
 final=api('milestones/7');assert final['description']==body;save('milestone-after.json',final)
 save('completion.json',dict(result='PASS',utc=datetime.now(timezone.utc).isoformat(),closed=[461,490],awaiting_separate_approval=491,publication=pub))
 print('PASS milestone ordered around exact #491 approval and H700 stages',flush=True);rc=0
finally:
 (owner/'inner.rc').write_text(str(rc)+'\n');(owner/'outer.rc').write_text(str(rc)+'\n')
sys.exit(rc)

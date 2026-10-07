"""Publish evidence-backed issue outcomes after verified ordinary evidence push."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import os
import re
import subprocess
import sys

owner=Path(__file__).resolve().parent
repo=Path('/workspace/repos/rocknix.worktrees/conflict-resolution')
publication=Path('/workspace/tmp/pixelelated-m7-phase7-publication-07')
assert json.loads((publication/'owner-verification.json').read_text())['result']=='PASS'
pub=json.loads((publication/'publication.json').read_text())
head=pub['next'];base='repos/pixelelated/distribution';url='https://github.com/pixelelated/distribution/blob/'+head+'/'
audit='docs/audits/2026_10_06-milestone-m7-p4-fixes-383/'
qa='docs/qa-logs/2026-10-07-pixelelated-replacement-16/'
assert (repo/audit/'05-punch-list.md').read_text().count('  outcome: resolved')==8
assert not (owner/'qa.start').exists()
(owner/'qa.start').write_text(datetime.now(timezone.utc).isoformat()+'\n')
(owner/'run.path').write_text(str(repo/os.environ['RASTERATOPS_BUILD_RUN'])+'\n')
for path,wanted in json.loads((owner/'seal.json').read_text()).items():assert hashlib.sha256(Path(path).read_bytes()).hexdigest()==wanted,path

def save(name,value):
    p=owner/'artifacts'/name
    with p.open('x') as f:json.dump(value,f,indent=2);f.write('\n')
    return p

def api(endpoint,method='GET',payload=None,label=None):
    command=['gh','api',base+'/'+endpoint,'--method',method]
    if payload is not None:
        p=save(label+'-request.json',payload);command+=['--input',str(p)]
    r=subprocess.run(command,capture_output=True,text=True)
    assert r.returncode==0,(endpoint,method,r.stderr)
    return json.loads(r.stdout)

def snapshot(row):
    return {k:row.get(k) for k in ['number','title','body','state','state_reason','updated_at','html_url']}

evidence={
 467:('Discovery and capability fixes, installed legacy/tiered/BIOS restores, unsupported controls, and actual EN/FR automatic/default and manual chooser paths all pass. Original source/config/cloud bytes are preserved; clean/actual RC2 upgrade and all three protocols pass.','content-routing01-acceptance/acceptance.json'),
 468:('Actual future/malformed/config/record/write/network/missing outcomes are truthful. Four stock outer timeouts preserve state and retire children. English/French at 640×480 and 1280×720 reasons and the full French rclone config/E direction fit; actual original-connection repair/UI retry passes.','recovery-640x480-acceptance/acceptance.json'),
 478:('Four real partial copies are killed after 258,048 of 8,391,392 bytes. Actual UI retry restores all originals; the next backup preserves the displaced save in the current shelf. Fresh-root07 separately proves settings/content backups and automatic save receive/send with exact witnesses.','partial640-02-acceptance/acceptance.json'),
 479:('The validated-record/source-prefix repair passes actual English/French at 640×480 and 1280×720 partial-file retry and next-backup preservation, with 32 directly reviewed frames. Host positive/negative/refusal controls and final clean/actual RC2 upgrade/protocol qualification pass.','partial1280-02-acceptance/acceptance.json'),
 361:('The independent audit proves AC-I361-L123 from upstream/fork controls, exact equality of 219 Linux and 53 native source files source equality, cold compilation lineage, real RA33 ordinary offline award/flush/API/relaunch and UI proof. Library02 supplies 415 assertions and 879 requests; candidate 16 retains all 46 installed proxy files. No new 818-test run, award/reset or live freshness lookup is claimed.','unchanged-dependency-custody/verification.json'),
 386:('Exact archives, parent-coupled SPIR-V disposition, actual 752-byte Vulkan shader compile/link, cbindgen 0.29.4 compatibility, six Codeberg controls, recipe lints, cold target consumers and frozen-cut freshness are accepted. Candidate16 retains 1,607 unchanged recipes; only the qualified ES pin changes. Source-current evidence retains its original timestamp.','unchanged-dependency-custody/parent-criterion-readback.json'),
 327:('Before and English/French at 640×480 explanation frames show the approved separated paragraphs without clipping. French/menu/vocabulary checks pass. Local website asset commit 4f6df54 matches the reviewed a40331aa screenshot hash; the current ES page source is unchanged. This closes the retaken-asset criterion; website publication remains P5.','unchanged-dependency-custody/327-site-frame-readback.json'),
 487:('The exact owned rewritten sshd listener title is accepted; wrong-owner/config/executable controls are rejected. All three actual backend identities and exact container image are retained, with verified PID/container disappearance and318 passing protocol assertions. The original failed observer is preserved.','cloud02-observer-correction/controls.json'),
 488:('The offline validator now requires the actual pointers field and empty root, all three downloaded hashes, unsupported flag, unchanged original snapshots and verified four-result/seal/cleanup evidence. Missing/wrong-root controls fail. The original validator failure is retained; the four passing VM cases were not replayed.','selected-content01-acceptance/acceptance.json'),
 409:('The lowercase transition is qualified on candidate 16: configured legacy state survives, actual RC2 adoption passes 26 checks, the current init retains the source-defined future filename predicate, consumed container/source custody is verified, and identity/manual-update/brand/localisation/default/visual/timing proofs pass. All eight independent-review findings are resolved. P5 licences/source publication and future fork-to-fork runtime proof retain their original gates.','qa20-acceptance/acceptance.json'),
 383:('All four ordered software criteria are now evidenced: source/fixture children, refreshed inputs and carry-forward software gates, one exact candidate 16 input set with full clean/upgrade/pair/visual/timing/protocol proof, and the approved cross-lab audit with all eight findings resolved. H700 builds, physical facts and release publication remain the separately ordered milestone route.','phase7-source-readback/final-acceptance-receipts.json'),
}
expected={467:(5,0),468:(6,0),478:(1,2),479:(1,2),361:(1,6),386:(3,1),327:(2,1),487:(3,0),488:(3,0),409:(4,6),383:(3,1),471:(4,4)}
completed=[];rc=1
try:
    for number in [467,468,478,479,361,386,327,487,488,471,409,383]:
        original=api('issues/'+str(number));save(f'{number}-before.json',snapshot(original))
        assert original['state']=='open',number
        body=original['body']
        assert (body.count('- [ ]'),body.count('- [x]'))==expected[number],number
        if number==471:
            titles=re.findall(r'^- \[[ x]\] (PL-\d{3}: .+)$',body,re.M);assert len(titles)==8
            outcome='All eight findings are resolved after candidate 16 rebuild and installed qualification. No finding is deferred or withdrawn. The audit began on candidate14; its original grades and failed runs remain historical evidence.'
            body='## Completed fixes audit\n\n'+outcome+'\n\n'+'\n'.join('- [x] '+title for title in titles)+'\n\n'
            body+='Candidate: `ee014909137e03706e0b3020b8396be589aaa705`; ES `72494bc72e3d64d4dcfeb4e6478052bbdf166c5b`; immutable bundle `7f98f2d22985d11fe9c150015457894caf460104c9ce44abd16074167f23815a`.\n\n'
            body+='[Full findings and commit outcomes]('+url+audit+'05-punch-list.md), [installed resolutions and Already written dispositions]('+url+audit+'08-installed-resolution.md), [criterion reconciliation]('+url+audit+'10-closure-reconciliation.md).\n\n'
            body+='Final qualification: all 15 default suites, 78 comparison screens with zero unclaimed differences, 26 actual ROCKNIX RC2 upgrade assertions, and 318 local WebDAV/SFTP/S3 checks. Changed migration/discovery/recovery/timeout/EN-FR UI proofs have exact source/input hashes, direct frames and actual cleanup. The two approved Fable passes are complete; no third call was made.\n\n'
            body+='This completes the software fixes audit. Capacity review #461, H700 DDR4 RG35XX SP arm then aarch64 builds, physical facts and P5 publication gates remain. No RC designation or release publication is claimed.\n'
        else:
            outcome,path=evidence[number]
            body=body.replace('- [ ]','- [x]')
            body='## Accepted on candidate 16\n\n'+outcome+'\n\n[Primary acceptance]('+url+qa+path+'); [criterion reconciliation]('+url+audit+'10-closure-reconciliation.md); [fix commits and existing-state dispositions]('+url+audit+'08-installed-resolution.md).\n\nAlready written: '+(
                'existing player/cloud data is preserved under the explicit migration, refusal and retry dispositions in audit 08; actual old states and corrected installed behavior are retained.' if number in [467,468,479,409] else
                'this closure records verified evidence and changes no player files or cloud data; the original runtime failures and prior source states remain retained.')+'\n\n## Historical request and execution record\n\n'+body
        assert '- [ ]' not in body
        (owner/'artifacts'/f'{number}-body.md').write_text(body)
        check=api('issues/'+str(number));assert check['body']==original['body'] and check['state']=='open',number
        edited=api('issues/'+str(number),'PATCH',{'body':body},str(number)+'-body')
        reread=api('issues/'+str(number));assert reread['body']==body and reread['state']=='open',number
        comment='Completed with published evidence at `'+head+'` and qualified candidate `ee014909137e03706e0b3020b8396be589aaa705`. '+outcome+'\n\n[Final audit record]('+url+audit+'08-installed-resolution.md). Device testing and release publication retain their separate gates.'
        response=api('issues/'+str(number)+'/comments','POST',{'body':comment},str(number)+'-comment')
        save(f'{number}-comment.json',{k:response[k] for k in ['id','html_url','body']})
        api('issues/'+str(number),'PATCH',{'state':'closed','state_reason':'completed'},str(number)+'-close')
        final=api('issues/'+str(number));assert final['body']==body and final['state']=='closed' and final['state_reason']=='completed',number
        save(f'{number}-after.json',snapshot(final));completed.append(number)
        print('PASS closed completed #'+str(number)+'; exact body/state readback',flush=True)
    m=api('milestones/7');save('milestone-before.json',{k:m[k] for k in ['number','title','description','state','updated_at','html_url']})
    assert m['title']=='M7: pixelelated 0.0.1'
    original=m['description'];start=original.index('## Ordered critical path');body=original[start:]
    lines=body.splitlines()
    for i,line in enumerate(lines):
        if line.startswith('| **M7.P2 '):lines[i]='| **M7.P2 — Qualified release inputs** | **COMPLETE** — #361/#362/#386 input and unchanged-source preservation criteria reconciled; #310/#327/#332 software gates accepted. | Source manifests, actual consumers/runtime proof and explicit cut-time freshness evidence retained. |'
        if line.startswith('| **M7.P3 '):lines[i]='| **M7.P3 — Build and qualify the image** | **COMPLETE FOR GENERIC_X64 CANDIDATE16** — all 15 default suites, 78 screens, 26 actual RC2 upgrade checks, and 318 protocol assertions; affected installed recovery/UI and exact unchanged-input carry-forward accepted. | Frozen product/input identity, preserved original state and independent completion/cleanup receipts. Device artifacts retain their own build/smoke gates. |'
        if line.startswith('| **M7.P4 '):lines[i]='| **M7.P4 — Independent fixes audit** | **COMPLETE** — approved primary plus both Fable passes; all eight findings resolved in #471; repaired candidate 16 rebuilt and requalified. | Published audit 05/08/10 and exact checked/closed issue readbacks. No further external audit call required. |'
        if line.startswith('| **M7.P5 '):lines[i]='| **M7.P5 — Device builds and release staging** | **NEXT: capacity review #461 → H700 DDR4 RG35XX SP arm → aarch64**. Then named physical and publication gates. | Each device artifact verified before its authorized smoke/migration actions; source/licence/public docs and manifest-bound assets before release publication. |'
    body='\n'.join(lines)+'\n'
    body=body.replace('#409 remains open through P4, so only its source/build portion precedes that audit; old candidate evidence stays historical.','#409 is completed after final candidate 16 qualification and the P4 audit; old candidate evidence stays historical.')
    top='''## Current priority — qualified software to H700 device builds

P3 GENERIC_X64 qualification and P4 fixes audit are complete on candidate 16.
All eight findings are resolved with published commits, installed evidence and exact
tracker readbacks. #471/#467/#468/#478/#479 and the compound software gates
#361/#386/#327/#409/#383 are completed. Original failed runs remain retained.

1. **#461: read-only capacity/retention review.** Remeasure free space, next
   build/copy/artifact/QA footprint and protected transitive dependencies.
   The previous exact two-disk retirement is complete; no wider deletion is
   authorized. An unreadable or referenced dependency cannot be proposed away.
2. **H700 DDR4 RG35XX SP arm**, from qualified product inputs, under the
   standard build watcher with active result delivery; verify the exact asset.
3. **H700 aarch64**, with its own measured capacity and artifact verification.
4. **Named physical/P5 gates:** device adoption/smoke facts, corresponding
   source and 14 known licence metadata gaps, public docs and manifest-bound
   release assets. Physical actions and publication require their named scope.

Candidate16: ee014909137e03706e0b3020b8396be589aaa705; ES 72494bc72e3d64d4dcfeb4e6478052bbdf166c5b;
bundle 7f98f2d22985d11fe9c150015457894caf460104c9ce44abd16074167f23815a.
All 15 default suites, 78 comparison frames with zero unclaimed differences,
26 actual ROCKNIX RC2 upgrade checks, and 318 local WebDAV/SFTP/S3 assertions pass. No new RA reset or Dropbox
credential is needed. Unchanged proxy/library proof has explicit byte/source
custody; no new live upstream-freshness query is claimed.

This is software qualification, not RC designation or release publication.
Watchers record status; the primary consumes results. Off-session alerts #395,
FOSS observability #432 and automated RA reset #464 retain their later scope.
Can this be done on the VM? Software qualification is complete on the VM.
Storage capacity and device compilation are host facts; physical smoke gates
retain their named hardware facts and separate action scope.

'''
    body=top+'[Final audit resolutions]('+url+audit+'08-installed-resolution.md), [criterion reconciliation]('+url+audit+'10-closure-reconciliation.md).\n\n'+body
    (owner/'artifacts/milestone-body.md').write_text(body)
    check=api('milestones/7');assert check['description']==original
    api('milestones/7','PATCH',{'description':body},'milestone')
    final=api('milestones/7');assert final['description']==body and final['title']==m['title']
    save('milestone-after.json',{k:final[k] for k in ['number','title','description','state','updated_at','html_url']})
    print('PASS milestone7 exact ordered body readback',flush=True)
    save('tracker-completion.json',dict(verified_utc=datetime.now(timezone.utc).isoformat(),result='PASS',closed_completed=completed,exact_bodies_and_states=True,milestone=7,milestone_exact_readback=True,publication=pub))
    rc=0
finally:
    (owner/'inner.rc').write_text(str(rc)+'\n');(owner/'outer.rc').write_text(str(rc)+'\n')
sys.exit(rc)

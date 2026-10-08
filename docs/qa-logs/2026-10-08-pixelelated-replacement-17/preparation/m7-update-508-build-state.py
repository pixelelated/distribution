import datetime,json,pathlib,subprocess
repo='pixelelated/distribution'
out=pathlib.Path('/workspace/repos/rocknix.worktrees/conflict-resolution/docs/qa-logs/2026-10-08-pixelelated-replacement-17/tracking')
out.mkdir(exist_ok=True)
def api(*args):return json.loads(subprocess.check_output(['gh','api',*args]))
j=api('repos/'+repo+'/issues/508');(out/'508-before.json').write_text(json.dumps({k:j[k] for k in ['number','title','state','body','updated_at']},indent=2)+'\n')
b=j['body']
a=b.index('## Source integration published');z=b.index('## Current scope')
b=b[:a]+'''## Current execution — 2026-10-08

Source integration and independent #507 review are complete. All four #524 findings are resolved; both issues are closed completed. The accepted product/delivery input is distribution `3756fde50e52b71b101a892a5b2862b708ad7b32` with ES `1d76b3da7da75794066df1c089931b890304da7a`. Both approved Fable passes and exact-head hosted delivery checks completed; do not repeat them.

The engineering GENERIC_X64 replacement17 worktree is frozen at those inputs. Its independent cache copy is actively watched; checksum/inode verification precedes compilation. No new firmware or VM acceptance is claimed. [Frozen inputs and harness](https://github.com/pixelelated/distribution/tree/2f2ec5af52f6aa0281dfcfae9b1262157efc929a/docs/qa-logs/2026-10-08-pixelelated-replacement-17/freeze) retain exact source identity and manifest custody.

Remaining order: engineering GENERIC_X64 build → CF10 clean/public ROCKNIX configuration adoption and actual inclusion → affected H700 followed by SM8550 builds → source/licence/physical/release gates. #519 separately gates the owner's next update transfer/reboot. The source and historical device evidence below is not new firmware qualification.

'''+b[z:]
b=b.replace('#515 owns concrete progress-file repairs.', '#515 owns the completed source-derived placement disposition and save/capture coverage fixes; no safe generic relocation mapping was demonstrated.')
b=b.replace('**#515 — targeted save-folder repair cases and qualification (next implementation task).** Read public ROCKNIX filters/config and actual emulator writers; distinguish valid layouts from source-proven misplaced saves/states/screenshots. Define exact plans, bounds, collision/source-retention and consent; implement and prove supported actions. Unsupported/ambiguous cases retain instructions. If no safe automatic case exists, retain the case evidence and explicit disposition; never claim an unimplemented repair passed or silently drop a demonstrated requested case.', '**#515 — COMPLETE: finite placement disposition and coverage qualification.** Public-source/writer evidence supports preserving valid layouts and instructions for ambiguous locations; no demonstrable generic relocation mapping or repair API/screens is claimed. Children #520/#521 and runtime prerequisites #522/#523 are qualified and closed, with retained original failures and complete preservation proof.')
b=b.replace('**#508 — coordinated final integration and pins.** Include the qualified foundation and #515\'s result, remove automatic move/follow and startup/tidy paths, and retain public config/credential preservation. Carry canonical references and proof with the source.', '**#508 — SOURCE INTEGRATED; firmware inclusion pending.** The qualified foundation, #515 result and reviewed follow-up fixes are integrated and pinned. Canonical references and sealed source/UI proof accompany the exact product inputs above.')
b=b.replace('**#507 — freeze and independently audit the resulting P5 delta.** Required primary and cross-lab stages; no replay of the accepted candidate16 audit.', '**#507/#524 — COMPLETE.** Primary and both approved cross-lab passes, four resolved findings, publication and exact-head delivery checks are accepted. No audit job remains active.')
b=b.replace('Both product branches remain local/unintegrated; the product pin is unchanged.', 'These historical source inputs were integrated and published; the current audited ES pin is1d76b3da7.')
b=b.replace('No build, VM or audit job is running in this lane.', 'The replacement17 cache-copy/build owner is active as recorded above; no audit or VM job is active yet.')
b=b.replace('supported bounded progress repairs are separate #515 actions.', '#515 concluded an evidence-backed instructions-only relocation disposition and qualified in-place save/capture coverage fixes.')
b=b.replace('Local draft evidence exists; integrated source/install inclusion is still required.', 'Integrated source and package proof exists; actual assembled installation inclusion remains required.')
b=b.replace('## Active source-coverage fix — #520', '## Completed source-coverage fix — #520 (firmware inclusion pending)')
b=b.replace('#520 is a child of #515 and must qualify before #508 integration and #507 scope freeze.', '#520 is a completed child of #515, qualified before the completed #508 source integration and #507 audit freeze.')
b=b.replace('Synthetic old-source failure and fixed-source byte-preservation controls plus affected actual VM presentation proof are in progress.', 'Synthetic old-source failure, fixed-source byte-preservation controls and affected VM presentation proof are accepted and retained.')
b=b.replace('## Additional confirmed writer gap — #521', '## Completed writer fix — #521 (firmware inclusion pending)')
b=b.replace('Child #521 qualifies DuckStation default screenshot placement.', 'Completed child #521 qualifies DuckStation default screenshot placement.')
b=b.replace('## DuckStation runtime prerequisite — #522', '## Completed DuckStation runtime prerequisite — #522')
b=b.replace('It precedes #521 screenshot runtime acceptance.', 'It enabled the accepted #521 actual runtime screenshot proof; #523 also supplies target libcom_err for the installed dependency closure.')
request=out/'508-request.json';request.write_text(json.dumps({'body':b})+'\n')
api('repos/'+repo+'/issues/508','--method','PATCH','--input',str(request))
after=api('repos/'+repo+'/issues/508');assert after['body']==b and after['state']=='open'
(out/'508-after.json').write_text(json.dumps({k:after[k] for k in ['number','title','state','body','updated_at']},indent=2)+'\n')
(out/'508-readback.json').write_text(json.dumps({'at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'exact_body_readback':True,'state':'open','audit':'closed completed','image_acceptance':'pending'},indent=2)+'\n')
print('PASS #508 complete current-body reconciliation, exact readback; image criteria remain open')

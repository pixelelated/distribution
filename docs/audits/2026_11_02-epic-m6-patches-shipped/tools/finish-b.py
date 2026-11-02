import pathlib,json,subprocess,hashlib,datetime,re,collections
R=pathlib.Path('/workspace/repos/pixelelated/distribution.worktrees/m6-patches-shipped-689');A=R/'docs/audits/2026_11_02-epic-m6-patches-shipped';B=A/'stage-b';SEED='9dd0716033f8831ffbd0b5ee8efbb5e5a066cfb1';UP='651150fc88';BASE='c445081a59518f37d9776e5412dd7b14910696f7'
def sha(x):return hashlib.sha256(x).hexdigest()
def dump(p,x):p.write_text(json.dumps(x,indent=2,sort_keys=True)+'\n')
def git(ref,p):
 q=subprocess.run(['git','show',ref+':'+p],cwd=R,capture_output=True);return q
now=datetime.datetime.now(datetime.timezone.utc).isoformat()
recipes=json.loads((B/'recipes.json').read_text());currency=[]
for path in recipes:
 versions={}
 for label,ref in [('seed',SEED),('fixed_upstream',UP),('fixed_base',BASE)]:
  q=git(ref,path); body=q.stdout.decode() if q.returncode==0 else ''
  versions[label]={'ref':ref,'rc':q.returncode,'sha256':sha(q.stdout) if q.returncode==0 else None,'pin_assignments':[{'line':i,'text':l} for i,l in enumerate(body.splitlines(),1) if re.match(r'\s*PKG_VERSION=',l)],'includes':[{'line':i,'text':l} for i,l in enumerate(body.splitlines(),1) if re.match(r'\s*\. .*package.mk',l)]}
 currency.append({'recipe':path,'versions':versions,'scope':'All literal pin assignments and source includes; conditional/dynamic values are not executed. Per-plan resolved inputs are in selection.json; absent path is not a package-removal claim.'})
dump(B/'recipe-currency.json',currency)
C=B/'source-context';C.mkdir(exist_ok=True); receipts=[]
def capture(name,argv,cwd=R,expected=(0,)):
 q=subprocess.run(argv,cwd=cwd,capture_output=True);assert q.returncode in expected,(name,q.stderr.decode()[:300]);(C/(name+'.stdout')).write_bytes(q.stdout);(C/(name+'.stderr')).write_bytes(q.stderr);receipts.append(dict(name=name,argv=argv,cwd=str(cwd),rc=q.returncode,utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),stdout_sha256=sha(q.stdout),stderr_sha256=sha(q.stderr)))
for name,path in [('ppsspp-recipe','projects/ROCKNIX/packages/emulators/standalone/ppsspp-sa/package.mk'),('ppsspp-patch','projects/ROCKNIX/packages/emulators/standalone/ppsspp-sa/patches/007-disable-home-pause.patch'),('unpack','scripts/unpack')]:capture(name,['git','show',SEED+':'+path])
capture('ppsspp-upstream',['git','show',UP+':projects/ROCKNIX/packages/emulators/standalone/ppsspp-sa/patches/007-disable-home-pause.patch'])
capture('seatd-consumers',['rg','-n','seatd-launch','projects/ROCKNIX/packages','--glob','!*.patch','--glob','!package.mk'],expected=(1,))
fex='e869aa644a16e4332cdc15c1ea0b4d13d482385d';dolphin='6094cfcf7b8fba733b3116fdf3414d51c1c0e4a4'
capture('fex-thunk-cmake',['git','show',fex+':ThunkLibs/GuestLibs/CMakeLists.txt'],pathlib.Path('/workspace/cache/rocknix-sources/fex-emu/fex-emu-'+fex))
for name,path in [('dolphin-scopeguard','Source/Core/Common/ScopeGuard.h'),('dolphin-mainnogui','Source/Core/DolphinNoGUI/MainNoGUI.cpp')]:capture(name,['git','show',dolphin+':'+path],pathlib.Path('/workspace/cache/rocknix-sources/dolphin-sa/dolphin-sa-'+dolphin))
capture('prior-t30-punch',['git','show','f8a0f35931:docs/audits/2026_10_24-epic-m6-emulators-standalone/05-punch-list.md'])
capture('ppsspp-issue-search',['gh','issue','list','--repo','pixelelated/distribution','--state','all','--search','ppsspp pause','--json','number,title,state'])
capture('ppsspp-archaeology',['tools/archaeology','ppsspp pause'])
capture('issue-689',['gh','issue','view','689','--repo','pixelelated/distribution','--json','id,title,body,comments,milestone,labels,state'])
capture('dispatch',['gh','api','repos/pixelelated/distribution/issues/comments/6585520800'])
dump(C/'receipts.json',receipts)
(A/'03-retrospective.md').write_text('''# T42 retrospective reading

Primary: Codex / GPT-6-Astra / xhigh, OpenAI, Local. Reviewed-at `9dd0716033f8831ffbd0b5ee8efbb5e5a066cfb1`. This is Stage B's backward/conformance pass; the final outcome retro belongs to G after coordinator disposition.

## Conformance

The seed/source/P1 bindings establish the actual 384 native members, including four links, and keep T40's 50 patch/override keys separate. All twelve fork-written members / 498 lines were read in full. The other 372 members received path/header/target/currency and recipe reading, with individual source comparisons where retained; this does not certify 71,387 lines of component code. Independent first observations were committed as `35a3eaa13a08842b7d7242467464f13248fd3e86` before the retained prior verdicts were read.

The method follows `scripts/unpack:126–196`: C-ordered package, architecture, extra, version, project and device paths; x86_64 becomes PATCH_ARCH=x86. A matching survey reach is not enough to execute an uncertain selection. Ordinary input uses the immutable referent and DEVICE substitution. Unknown pre-patch transformations remain open. Every admitted stack used a separate target projection and actual normal rc for promotion. No shell recipe/configuration was evaluated.

## Interactions and prior evidence

T40 `88a648da0d` supplies the frozen inherited questions. T8 `f50a031158` keeps its 22 recipe pins on the base-merge path, without deciding patch adoption. T22 `cbab6483dc` names busybox/util-linux additions and a separate gettext question; the additions are symlink-bound exact changed-line counterparts here, while gettext remains I45. #997 is a test identity/shimming bug, not the busybox version owner. T27 `0ac98afe43` owns the H700 recipe question: both DDR3/DDR4 sources are v2026.01, and SWIG is 4.5.0; wrapper 1.0 is not the source version. Raw preimage matches do not exercise pylibfdt/SWIG. All immutable prior files and hashes are retained under stage-b/prior-context/.

Systemd state-path design remains #1104. Existing #1048/#346 class-removal work, #1056/#1071/#1072, #559/#563 integration, T41's 107 members, T3's 21 and T17's 18 are unchanged. T43 owns its 432 paths and MangoHud's SM8750 referent. Contributions are draft text here for #585; none was sent there. PPSSPP's prior T30 punch list and issue search do not record the nested-patch defect; they do not prove that no other report exists.

## Refutation and limits

- **“Normal patch success proves the hotkey fix.” Refuted.** The PPSSPP outer patch creates `package/batocera/emulators/ppsspp/007-disable-home-pause.patch`; its SDL hunk is payload text. A constructed fixture returns normal rc 0 while SDLJoystick.cpp stays byte-identical. No recipe hook applies that nested file. The fixture is not an applies-at-pin receipt.
- **“Copy fixed upstream's replacement.” Not established.** Fixed upstream 651150fc88 patches SDL directly but returns NKCODE_GUIDE; the nested seed payload returns NKCODE_UNKNOWN. The implementation owner must preserve or explicitly decide intended mapping before a source fix.
- **“A missing generic counterpart is a missing fix.” Refuted.** LLVM disables benchmarks in options; fluidsynth uses shared libraries; Android mkbootimg has no Dragonboard dtbTool; seatd's -p request has no retained non-recipe caller. Each inherited row carries its own feature/pin evidence, not a group verdict.
- **“libsndfile's newer pin absorbed the CMake fix.” Refuted.** The qualified source still has a two-dot range (`3.5..3.26`). The generic three-dot change and CMake 4 interpretation require I04's targeted owner proof.
- **“Archive filenames or partial substrings prove source identity/adoption.” Refuted.** Admission binds actual bytes to recipe and sidecar SHA256; hunk/pair reports preserve whole changed sequences and explicitly leave ambiguous comparisons unresolved.
- **“The runner certified every selected path.” Refuted.** Unknown hooks/branches, missing SHA/cache, duplicate WebKit/Samba members and the G202/G203 regular-file snapshot guard create explicit open items. The two UCM groups have no serialized normal rc for the link-creating candidate. That missing exit is not reconstructed. Diagnostic/normal output for earlier completed rows remains authoritative.

## Learning and custody

A successful patch tool can install a patch as inert data; inspect outer targets as well as exit codes. The sibling scan found one product-path hit and 23 historical product-diff evidence hits, which are legitimate audit records. A future owning fix can add a narrowly scoped guard against that shape rather than rejecting every .patch file in evidence. The enforcement ladder proposal is recorded with PL-01, not installed into global tools during this audit.

Runner limits are named where they occur rather than backfilled as failures or passes. `selection.json` hook numeric positions are character offsets, while recipes.json retains actual line numbers. Source projections are not full trees. Scratch under /workspace/tmp/m6-t42 remains owned and retained through acceptance; only the later H disposition may retire it. No time-to-play, memory, boot, compile or player-step measurement was performed.
''')
(A/'04-analysis.md').write_text('''# T42 analysis — patches shipped outside the kernel table

Primary reader: Codex / GPT-6-Astra / xhigh, OpenAI. Reviewed-at `9dd0716033f8831ffbd0b5ee8efbb5e5a066cfb1`; Local D-WORKFLOW-184/225. Stage D is a review packet, not final slice acceptance.

## Executive summary

One confirmed Medium defect: PPSSPP's selected 007 patch adds a nested patch file instead of changing SDLJoystick.cpp (F-T42-01 / PL-01). No Critical or High finding is established. No product change is made. The native provenance and coverage tables each have exactly 384 keys; the separate inherited table has 50 keys / 26 overrides. All twelve fork-written patches / 498 lines were read in full.

| Native application classification | Paths |
| --- | --- |
| applies | 151 |
| offset | 38 |
| fuzz | 22 |
| open-item | 173 |
| **Total** | **384** |

These counts take each path's worst per-plan result, not the number of tool invocations. The 542 package/plan groups include context siblings; they are not the coverage denominator. A source projection applying is not a code-correctness or runtime PASS.

| Inherited conclusion | Keys |
| --- | --- |
| already-carried, with the exact current-pin intent stated | 21 |
| not-applicable-with-reason | 7 |
| unresolved-with-specific-evidence-needed | 22 |
| **Total** | **50** |

## Acceptance-criteria scorecard

Numbers match brief v2 and #689's twenty final criteria. No final issue checkbox is ticked by this packet. Stage D records, issue readbacks and checks complete the named D portions; E–H and coordinator integration are deliberately pending.

| Criterion | Stage D evidence / limit |
| --- | --- |
| 1 | 00–07, A–D receipts, audit-local tools and one-file Local plan; no build/guest artifact. |
| 2 | stage-a source/seed summaries, comparison.out and identity hashes: 384 / 71,387 logical lines. |
| 3 | 02 native Provenance/Coverage and tables.json; exact-key/field/receipt assertions. |
| 4 | 02 Fork-written reading, full 1–N ranges for twelve / 498, including Dolphin. |
| 5 | Four mode/literal/referent bindings; T43 referent only context; other slice ownership explicit. |
| 6 | 50 frozen keys / 26 overrides; 24 exclusions retained, not recounted. |
| 7 | Individual inherited decisions and source/pair/hunk evidence; 22 specific unresolved inputs with owner actions. |
| 8 | Fixed upstream/base patch identities plus recipe-currency.json literal pin assignments/includes; no live-ref or external-URL claim. |
| 9 | Application/group/archive receipts, projection hashes, rendering, stdout/stderr, normal rc; explicit gaps and fail/non-promotion fixture. |
| 10 | Four fail-first assertions then positive table validation; independent population sums. |
| 11 | This Q1–Q7 face, 03 conformance/interactions/refutation, classified proofs in running log. |
| 12 | Actual primary, OpenAI, reviewers [], D-WORKFLOW-184; no external review. |
| 13 | Pre-issue lint belongs to C/D; Phase-7 disposition and final resolution lint remain E/F. |
| 14 | One reactive bug with source trace, Already written, VM rationale and observable acceptance; issue readback/checks in D. Bug remains open. |
| 15 | Protected-path tree/commit guards and planted source-edit failure; no product/rule/ledger change. |
| 16 | Per-row owner/action; #585 drafts only; class removal #1048/#346. |
| 17 | Per-group source-only process census; scratch retained; no allocation or build/config/fetch action. |
| 18 | Final D check receipts and normal commit/push records; check outputs are written only after process exit. |
| 19 | Final retro and final accepted hand-back remain G/H; D summary is not a substitute. |
| 20 | Immutable reviewed-at preserved; source-preserving D tip published for disposition. Final fixed-at/integration acceptance remains coordinator-owned. |

## Risk assessment

F-T42-01 is a silent intended-change failure: the outer patch can succeed while the intended guide-button source change never occurs. Severity Medium reflects incorrect intended input behavior without a demonstrated data-loss/security impact. The current input mapping and any runtime symptom have not been measured here. Unknown application inputs are coverage limits, not invented product bugs. Fuzz/offset results warrant owner review before later pin changes; they are not runtime failures.

## Coverage boundary

384 native paths / 71,387 logical Git-blob lines; 71,378 newline bytes; 380 regular files and four symlinks; 379 shipped/five test. Resolving each selected link yields a different 71,477-line quantity. Full line reading is claimed only for twelve fork-written members / 498 lines. Native dispositions: 199 keep, 172 open-item, four #585 drafts, seven upstream-changed, one upstream-moved, one bug. Fixed upstream path identity: 307 same, 24 changed, 52 absent, one identical blob elsewhere; fixed base: 372 same, eleven absent, one changed. Whole path absence does not prove feature removal.

Application copies contain only required target members from a validated cached archive, plus patch-created files. Whole-component correctness, configured compiler behavior, binary integration, image upgrades, runtime efficiency, real controller behavior, provider or device facts are outside this source-only packet. Unknown dynamic/conditional pins remain explicit even when raw pin assignments are retained. No shell configuration/recipe, package build, external web/provider review or fetch was executed.

## Renovation face

### Q1 — Modernization

02 records target interfaces, current recipe pins and why the recorded intent is still carried. Modern compiler/header fixes, cross-compilation paths, lifecycle cleanup and device policies are distinct purposes. woff2 adds explicit cstdint includes; FEX excludes rebased system headers from guest thunks; shaderc avoids clobbering the prepared dependency tree. Newer pins are not sufficient proof of supersession. The inherited source/hunk/pair comparisons retain the exact version-specific question, including libsndfile's still-two-dot CMake range and changed FFmpeg request API series.

### Q2 — Standards and attribution

Literal mail headers and last path commits are preserved separately from source identity. 235 native identities have no From header; a missing mail header is not itself an attribution violation or a legal verdict. Existing upstream credits remain unchanged. Header dates, authors and URLs are recorded claims; no external integration verification or legal opinion is offered. The fabricated-attribution negative control checks literal header identity, not trust in the claimed author.

### Q3 — Defects

F-T42-01 follows outer patch lines 11–16, nested SDL payload 17–29, recipe hook source and unpack 191–196 to a created inert patch. The constructed fixture reproduces normal success with unchanged sentinel source. Fixed upstream has a direct source diff with a different desired key code; it supplies a comparison, not authorization to replace the seed. PL-01 is the single new reactive defect. No “missing counterpart” bug is invented for an unresolved inherited row.

### Q4 — Currency

All 384 native paths compare to fixed 651150fc88 and fixed base c445081a59518f37d9776e5412dd7b14910696f7. Recipe assignments/includes at all three refs are retained in recipe-currency.json; static resolved per-plan inputs stay in selection.json. Busybox/util-linux upstream additions resolve through their symlinks to exact generic changed-line counterparts; util-linux gettext remains its separate I45 question. Systemd's three intent comparisons stay separate and #1104 owns their design collision. External component-upstream claims are unverified. No “latest release” claim is made.

### Q5 — Efficiency

Source-visible cost changes include SDL display-mode frees, Mesa executable-heap and empty virgl-cache teardown, and Dolphin achievement-manager lifecycle. Qualified SDL/Mesa source context supports their stated cleanup paths; cached Dolphin ScopeGuard::Exit clears the finalizer, so explicit Exit does not invoke shutdown again at destruction. Historical launch-memory and image-delta evidence retains its original pins and limits. **No new boot, memory, player-step, runtime-efficiency or either time-to-play measurement exists.** Runtime owners must qualify any such claim in their own allocated scope.

### Q6 — Dead ends and reach

Native membership uses the residual P1 selector after explicit owners. Reach is a survey fact, not an executed plan. Four symlinks retain both path and referent identity; MangoHud's SM8750 source remains T43. No source is removed. #1048/#346 own class removal, and existing #1056/#1071/#1072 own adjacent selection/provenance work. The PPSSPP nested target is reachable by patch application but inert as source transformation; the sibling scan distinguishes the one product hit from 23 historical patch-record hits.

### Q7 — Clarity and structure

The separate tables expose literal provenance, exact recipe/context, application limits and remaining owner actions. Generic filenames or a single Subject in an aggregate patch cannot substitute for source reading. Inherited glibc, FFmpeg, BlueZ and systemd questions remain individual rows. Draft contribution text retains ownership and requires focused upstream qualification before submission. A future nested-target guard should examine product patch targets and explicit intentional exceptions, not reject audit product-diff files.

## Second opinion

Local, one actual reader: Codex / GPT-6-Astra / xhigh (OpenAI), own wN:p7 footer, session 01a19d12-3d7a-7642-9108-ae06a719cdd7. reviewers: []. D-WORKFLOW-184 permits Local at this epic tier. The sole second-opinions/review-plan.json and A's real validator controls record that contract. No council, provider call, external reviewer or independent second perspective is claimed. Earlier T38 identity/results remain historical.

## Quality self-check

First observations preceded prior-verdict reading. Counts are machine-asserted against frozen keys, while conclusions name their evidence and limitations. The four corrupted-data controls each fail their named assertion before the positive dataset passes. The separate protected-path guard must reject both working-tree and committed fixture edits before accepting this branch. Receipt validation checks recorded output hashes and equivalent diagnostic input projections. Assertions do not prove a complete semantic audit of vendor code. The brief's final resolution/integration requirements remain pending at D, and the one product bug remains open.
''')
with (A/'00-running-log.md').open('a') as f:f.write(f'''\n### {now} — B complete source review\n\nPROOF: B-02 (source-read) — all 384 digest/recipe rows, 50 individual inherited comparisons and twelve full-line fork-written readings are in 02 and stage-b/tables.json. recipe-currency.json binds literal pins/includes at seed, fixed upstream and base. Prior verdicts were read after the committed first analysis, with original source identities retained.\n\nPROOF: B-03 (tool-run) — 542 separate package/plan groups; source-target projections only. Native worst-per-plan statuses: 151 applies, 38 offset, 22 fuzz, 173 open items. Partial-failure control preserves prefix and blocks successor. G202/G203's missing serialized normal rc remains unclaimed.\n\nPROOF: B-04 (tool-run and source-read) — nested-patch/receipt.json reproduces the PPSSPP inert nested target in a constructed fixture, not at-pin. One confirmed Medium defect; no new Critical/High. Source/recipe/hook and sibling/duplicate search evidence retained.\n\nFriction: duplicate-member archives and a link-producing patch exceeded conservative runner support. Their affected claims remain open rather than silently broadening extraction or inventing exits; no product fix or global-tool change was made.\n''')
with (A/'01-research-notes.md').open('a') as f:f.write('\n## Completed B evidence\n\n02–04 now record all declared tables, independent reading and backward comparison. Application scope and gaps are explicit in 03/04; the earlier “not yet completed” statement above is the original A checkpoint, not the current status. Source-only receipts and fixed-ref recipe currency are in stage-b/. One confirmed nested-patch defect proceeds to C/D; all other open inputs retain their individual owners.\n')
p=A/'tools/tables.py';txt=p.read_text().replace('validator_rc=1','rejected=True,exception_type="AssertionError"');p.write_text(txt)
(A/'tools/finish-b.py').write_bytes(pathlib.Path(__file__).read_bytes())
print('PASS B narrative and source/currency supplements; no product writes')

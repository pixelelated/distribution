"""Compose T44 records from retained metadata; read named immutable history only."""
import pathlib,json,hashlib,subprocess,datetime,collections
D=pathlib.Path('/workspace/repos/pixelelated/distribution.worktrees/m6-es-vendored-and-data-691')
E=pathlib.Path('/home/max/Development/emulationstation-next.worktrees/m6-es-vendored-and-data-691')
A=D/'docs/audits/2026_11_02-epic-m6-es-vendored-and-data'
S='48a335700d05a733703e1b58536877b91b921259';P='55158d2a64c69fe295fb4e67fd174424a71b1b4d';BASE='cada856d86e3115fbbf0bce09dd761b0ee8fa9fd'
def sha(b):return hashlib.sha256(b).hexdigest()
def read(p):return json.loads((A/p).read_bytes())
def put(p,s):q=A/p;q.parent.mkdir(parents=True,exist_ok=True);q.write_text(s)
def js(p,x):put(p,json.dumps(x,ensure_ascii=False,indent=2)+'\n')
def git(repo,*args):return subprocess.check_output(['git','-C',str(repo),*args])
def cell(s):return str(s).replace('|','&#124;').replace('\n','<br>')
now=datetime.datetime.now(datetime.timezone.utc).isoformat()
identity=dict(harness='Codex',model='openai/gpt-6-astra',lab='openai',effort='xhigh',identity_source='Own visible Herdr footer GPT-6-Astra xhigh; UI observation, not provider attestation',session='01a19d12-1c5f-7022-8053-102f6a94b7fe',lane='m6-t2-es-launch',pane='wN:p5')
js('second-opinions/review-plan.json',dict(schema_version=1,depth='local',primary=identity,reviewers=[],tier_exception='D-WORKFLOW-184',reason='T44 table under plan section6c, proved v2/D-WORKFLOW-232; actual primary only, no independent reviewer or provider call.'))
# Complete delta reads are recorded as review coverage, not rendered source exports.
delta=[]
for p in ['.gitignore','CMakeLists.txt','locale/emulationstation2.pot','locale/lang/en_GB/LC_MESSAGES/emulationstation2.po','locale/lang/fr/LC_MESSAGES/emulationstation2.po']:
    argv=['diff','--no-ext-diff','--no-textconv',BASE,P,'--',p];b=git(E,*argv)
    assert b,('EMPTY_DELTA',p)
    delta.append(dict(path=p,base=BASE,tip=P,argv=['git','-C',str(E),*argv],diff_sha256=sha(b),diff_lines=len(b.splitlines()),coverage='complete displayed delta read; French 3014 diff lines in bounded chunks including re-read of truncated middle; structure and inherited ownership, not translation quality',source_sha256=sha(git(E,'show',P+':'+p))))
js('stage-b/fork-delta-reading.json',dict(recorded_at=now,identity=identity,records=delta,friction='Two guessed locale paths produced empty diffs; corrected from native metadata to locale/lang/... before claiming coverage. An over-broad immutable audit listing and matching read were truncated; the named sections were read again. No historical file was written.'))
prior=[]
refs=[('T2','7041b0d710363ddac7ae1b047ebae3e182548631','2026_10_23-epic-m6-es-launch-path'),('T21','82c67e99c5726e6980605790642e798c196e421c','2026_10_26-epic-m6-es-state-and-bridge'),('T34','49c6b43f2708f46c9d2f147c609d7d9f702c2557','2026_10_30-epic-m6-es-core-components'),('T35','d828355e0ac3b9c639c394adbcf9aeb65c0db22c','2026_10_31-epic-m6-es-core-window-input'),('T36','4127382d34db90298a9fd1e0c2ef185ad03b84ea','2026_10_31-epic-m6-es-core-utils-resources')]
for owner,ref,folder in refs:
    for name in ['02-forward-audit.md','05-punch-list.md']:
        p='docs/audits/'+folder+'/'+name;b=git(D,'show',ref+':'+p)
        prior.append(dict(owner=owner,ref=ref,path=p,sha256=sha(b),lines=len(b.splitlines()),read_scope='named catalogue/build/fake/allowed-failure ownership context only; original full report is not re-audited or replayed'))
r20=git(D,'rev-parse','780827c5ba^{commit}').decode().strip();folders=git(D,'ls-tree','-d','--name-only',r20+':docs/audits/').decode().splitlines();f20=next(p for p in folders if p.endswith('m6-es-achievements-pages'))
p20='docs/audits/'+f20+'/02-forward-audit.md';b=git(D,'show',r20+':'+p20)
prior.append(dict(owner='T20',ref=r20,path=p20,sha256=sha(b),read_scope='The library lines169-189: nine excluded rows; R13 dual-version marker explicitly assigned to T44; upstream patch comparisons remain CANNOT without source; no replay'))
js('stage-b/prior-record-identities.json',prior)
g=read('stage-b/vendor-groups.json');m=read('stage-b/tables.json');summ=read('stage-a/inputs/actual-head/summary.json');rr=read('stage-b/reading-register.json')['records']
assert len(m['provenance'])==len(m['coverage'])==594
assert sum(r['read_lines'] for r in m['coverage'])==5017
assert sum(r['read_lines'] for r in m['supplemental'])==450
intro=(A/'02-forward-audit.md').read_text().split('## Coverage boundary')[0]
intro+='''## Scope and evidence semantics

The native source contract is accepted T2 ES `55158d2a64c69fe295fb4e67fd174424a71b1b4d`, actual tree `64b90eb8cb07bdfcd690c74ff6bc980ae490657c`. Distribution seed is `48a335700d05a733703e1b58536877b91b921259`. Survey `16dbac5211eea7e70db7394372033be2be7df829`, P1 `2174265e9cc1b248c0fbe27fa101875984d46d6b`, fork base `cada856d86e3115fbbf0bce09dd761b0ee8fa9fd`, fixed upstream `e282b05627c0d2193c19d7cc526176e047530c3d` remain separate identities.

PROOF membership | tool-run | stage-a/membership.receipt.json, three helper outputs and explicit actual HEAD/root-tree equality.
PROOF native source | tree | stage-a/inputs/actual-head/native.json, collector-binding.json, every blob rehashed against the bound helper rows.
PROOF full-code reading | tree | stage-b/reading-register.json (40 native/5017 lines and 3 supplemental/450 lines); stage-b/fork-delta-reading.json (five other fork-modified deltas, completely read).
PROOF native tables | tool-run | stage-b/table-generation-2/receipt.json; stage-c/table-positive.receipt.json and seven separate refusal receipts.

Each keyed row below is table/provenance coverage. Reading methods distinguish complete fork-code reading, syntactic parsing and metadata. Neither 143710 generated CODE lines nor 11989 fork-own survey CODE lines is a completed semantic reading budget. Binary rows have zero source credit. Gitlink inventory contributes one synthetic line and zero source lines; its source is unavailable and was not fetched. Doctest's 7134 lines remain unchanged vendor import, with zero authored-code or full semantic-read credit. Survey fork-own means dated survey membership, not authorship.

Counts below are derived from the keyed model and bound helper: native594, 593 blobs/one gitlink, modes583x100644/10x100755/one160000; kinds543 text/50 binary/one gitlink; zero symlinks. Survey inventory374547 versus text374546; primary text374720/newline bytes374704/blob bytes40999100. Changed identities40, unchanged554. Supplement3/450 and companion4 are never added to the native count. An empty mp3 fixture is text with zero lines.

'''
body=intro+(A/'stage-b/tables.md').read_text()
body+='\n## Vendored groups\n\nSeparate import/version, local delta, license marker, consumer, carrying reason and dated upstream evidence. No package update or removal is authorized. `stage-b/history.json` and `source-header-markers.json` bind exact source/history reads.\n\n| Group | Import/version | Local delta | License evidence | Consumer/carry reason | Dated upstream evidence | Specific missing input/disposition |\n| --- | --- | --- | --- | --- | --- | --- |\n'
for r in g['groups']:
    body+='| '+' | '.join(cell(x) for x in [r['group'],r['import_evidence']+'; '+r['version'],r['local_delta'],r['license'],r['consumer']+'; '+r['carry_reason'],r['upstream']+'; '+r['upstream_result'],r['missing']+'; '+r['disposition']])+' |\n'
body+='''
The dated web read is release metadata, not source compatibility proof. The displayed GitHub dates omit a year; none is invented. Cached/no-release pages do not establish the latest upstream commit. Pugixml1.16 matches the selected system recipe's version, not an installed library. `src/rc_version.c` being absent from the explicit CMake list does not establish that every version marker is unreachable. T20 already assigned the dual rcheevos marker to T44 (02:183); this is inherited context, not a second newly discovered bug. Upstream applicability of T20's excluded hash changes remains with that owner.

## Catalogue coverage

35 PO catalogues plus one POT. The new `tools/catalogue.py` parses complete blob bytes, active context/msgid keys, continuation strings and plural indices. Counts exclude the empty-msgid header. `untranslated` means at least one active msgstr is empty, not a missing source translation. `format_flagged` means a positive `*-format` flag, not format-argument equivalence. No gettext producer runs, no linguistic quality or runtime layout is certified. The synthetic positive exercises context/plural/format/fuzzy/empty/obsolete/escaped-backslash forms; malformed missing-msgstr, duplicate, bad-quote and plural-gap inputs each refuse (stage-c/po-*).

| Path | Blob SHA256 | Entries | Headers | Plural | Context | Format flagged | Fuzzy | Untranslated | Obsolete lines |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
'''
for r in read('stage-b/catalogue-counts.json'):
    c=r['counts'];body+='| '+' | '.join(cell(x) for x in [r['path'],r['sha256'],*[c[k] for k in ['entries','headers','plural','context','format_flagged','fuzzy','untranslated','obsolete_lines']]])+' |\n'
body+='''
## Accepted catalogue deltas and integration obligations

PROOF PL-024 | history | stage-b/pl024-exact-rename.json: commit a1cbc0ccd96cbd95f3355375609f71f1b50c7113, 35 PO + POT + FileData.cpp = 37 files; 38 exact UKNOWN→UNKNOWN replacements, including en_GB msgstr. Other translation bytes equal the before text after this exact substitution. The actual key is UNKNOWN ERROR. Earlier 36-catalogue/37-line notes are historical errors.

`stage-b/french-deltas-and-calls.json` retains every exact msgid/msgstr and `_()` call with owner pin/source path/line/SHA256. Adjacent C++ string literals are concatenated lexically; this is not preprocessing or integration proof.

| Owner | Added French entries excluding PL-024 | Exact source-call locations | Limit/next owner |
| --- | --- | --- | --- |
| T2 #649 | 3 | primary main.cpp:972,357,365 | PL-025 accepted; no reopening |
| T21 #668 | 6 | 3ae9610b0 StatusText.cpp:59,61,47,38,36 and GuiWifi.cpp:399 | separate accepted branch, old spelling key retained |
| T34 #681 | 1 | 52f0ff512 RatingComponent.cpp:266, ADD STAR | separate accepted branch, old spelling key retained |
| T35 #682 | 1 | b7fdb3a24 GuiInputConfig.cpp:137, GAMEPAD | separate accepted branch, old spelling key retained |
| T36 #683 | 0 | no outside-app/core delta | no catalogue addition claimed |

All five external tree OIDs equal `03e88868d18b35b057a4de88d66b73c1f3703587`. None of the four companion refs contains the T2 tip. #700 owns combining accepted branches, retaining the corrected shared key and all branch additions, with new exact integration evidence. This table chooses no execution/image pin and creates no combined source.

## Build, resource and test interfaces

PROOF interfaces | tree | stage-b/interfaces.json, consumer-lines.json; exact file SHA256 and line references; source-only conditions.

| Interface | Writer/reader and exact condition | What remains unproved / owner |
| --- | --- | --- |
| System pugixml | root CMake:393-396 find_package; external/CMake:5-7 bundled subdirectory only when NOT USE_SYSTEM_PUGIXML; distribution ES recipe:24 sets1; packages/textproc/pugixml/package.mk pins1.16 | gitlink source not read; installed selection and compiler compatibility T37 #684/#700 |
| Vendor integration | root CMake:606 adds external; external/CMake:1-10 adds nanosvg, libcheevos, id3v2lib and conditional pugixml | library list is static reach, not configured/linked/installed proof |
| Windows dependency fallback | root CMake:40-78, WIN32-only FetchContent with origin/master fallback | moving Windows reference is a source fact; no Linux fetch or current Windows support failure inferred |
| Locale generation | locale/CMake:1-33 xgettext/msgmerge/msgfmt targets write template/catalogue/MO outputs; root:614-616 gates gettext tools and Intl; recipe:67-68 copies locale output | source parser cannot prove gettext or installed translation; no generator run |
| Root pure tests | tests/app-unit/CMakeLists.txt:24-106 standalone target, copied app sources and fake include directory | tests/hook files read in full, not executed; behavior owners T2/T18/T20/T21/T26 remain |
| App unit selection | root:610-612 ES_BUILD_TESTS defaultOFF selects es-app/tests/unit only | that subtree is T18 #665; not recut into T44 |
| Core CMake | T35 owns es-core/CMakeLists.txt; T21 adds five registrations at its accepted ref | integration obligation #700; primary lacks that combined branch |
| id3 test target | id3 root CMake:9 always adds test; test/CMake:29 main_test and :38-40 copies four assets | no inference that assets or executable ship; future configuration/removal requires owner scope |
| Resource copy | ES recipe:81-85 copies directory, then replaces DroidSansFallbackFull.ttf with system Noto CJK link | 147 source keys (101 text/46 binary), eight fonts; source and installed bytes differ |
| Dynamic resources | ResourceManager.cpp:34-76 ordered theme/user/ES/executable/cwd resource search; :79-122 handles :/ and caches result | basename grep absence is not deadness; T36 #683 owns behavior |
| XML/SVG structure | stage-b/resource-xml.json contains77 whole-document parses, all well formed | parsing is not rendering, safety/semantic correctness, image/font decoding or reachability |
| Resource checker | root CMake:581-588 POST_BUILD invokes resources/checkWheelGunGamesResources.py with Python and NOT MSVC | script read only, no invocation; this condition is not every build path |
| Public Git hooks | .githooks full code reads, guard-lib public interface and pattern-file metadata | ES hooks never run; installation/private inputs not inspected; distribution's new record gates are separate |

The full resource population and each source-reference lookup are keyed in Coverage. Directory-copy reach is recorded even when no literal basename was found. The only gitlink has metadata credit; the 50 native binary files are not rendered or decoded.

## Findings index

| ID | Question | Severity | Finding | Current owner/disposition |
| --- | --- | --- | --- | --- |
| T44-CUR-01 | Q4 | Low | The imported doctest2.4.12 has no dated carry/update decision against observed2.5.3 in the named import/accepted test records | PL-001, coordinator disposition; test ownership remains T18 and existing harness owners |

## Verification and self-refutation

T44-CUR-01 is a currency decision gap, not a confirmed product defect, security advisory or assertion that the new version builds here. The source header remains byte-identical to import324f9c483d9b4a11249c47888b40fb5cc691be7f, SHA25694029a7d32da24a56249658147dbd2b33ff0b9ed665295cbbaf19aafff5b0ced. The import records a then-current2.4-line choice. Primary release metadata now shows2.5.3. Historical accepted harness runs prove their own pins, not a prospective version upgrade. A dated carry decision with rationale/retirement trigger could resolve this without any source change; an update requires its own brief. See05.

Inherited R13 from T20 is separately recorded in05 with the original owner and exact source markers; no duplicate bug. Unconditional id3 test registration, unused-looking asset names, moving WIN32 fallback, and parser translation counts remain qualified observations. No failure trace establishes a new runtime bug, no resource is proposed for removal, and no reactive bug was filed.

## Evidence controls and limitations

PROOF table refusals | fixture | stage-c/table-*.receipt.json: missing native, gitlink credit, doctest authorship, missing supplemental, missing companion, false integrated companion and changed source identity each rc1 at its own predicate; positive rc0 against hash-bound actual inputs.
PROOF parser | fixture | stage-c/po-*.receipt.json: positive rc0 and four malformed cases rc1.
PROOF confinement | fixture | stage-c/guard-*.receipt.json and confinement-live-1: planted product path, prefix neighbor, traversal and symlink refuse; positive passes; whole ES seed/tree/status unchanged. Every later distribution commit uses the same path guard.

Literal failed attempts remain under stage-b/collection-attempt-{1,2,3}/ and table-generation-1/. The final collector is attempt4, final renderer generation2. Failures were in new consumers (escaped backslash scanning, wrong rename filter, adjacent literal call matching, nullable binary line totals), never accepted producers. No failed result is relabelled as PASS.

Local actual Codex/openai/gpt-6-astra/xhigh, UI-observed footer, reviewers[]. No independent review claim. Both interface→first-frame and exit→next-first-frame are unmeasured. Final installed, merged, compiler, translator, renderer, guest and physical/cloud behavior remain outside this table. Stage D is a checkpoint for root disposition, not final acceptance.
'''
put('02-forward-audit.md',body)
put('03-retrospective.md','''# T44 retrospective comparison

## Conformance

The source contract is v2/D-WORKFLOW-232 at coordinator817bb999f27a22c1ef33485b886663eb8b07a074, dispatched #691 comment6590429015 after #700 kickoff6590229420. Actual root-tree equality, bound inputs and separate populations were verified before source reading. The entire ES worktree remains read-only. No reviewer/provider, compiler, build, guest, accepted producer or configuration ran. New metadata controls run on CPUs8–23.

## Doctrine and interactions

D-WORKFLOW-184 permits Local table review; no old primary identity is copied into new receipts. D-WORKFLOW-187/188/189 preserve order, brief ownership and root acceptance. D-WORKFLOW-209/225 preserve accepted evidence; new tooling and readback do not turn accepted tests into fresh proof. Blindspots13/47/51/75 are addressed by bytes/root identity, source-versus-installed limits, explicit future obligations and separate source populations. T43's independent record work may proceed under D-WORKFLOW-190; T46 remains last. #700 owns eventual integration; M7 ownership is not selected here.

## Prior-evidence comparison

First independent observations were written before reopening accepted verdicts in this execution. This executor prepared inherited context earlier, so this is neither blind nor independent review. stage-b/prior-record-identities.json binds named02/05 full hashes and the narrow portions read; no report/test was rerun.

| Accepted owner | Comparison and surviving obligation |
| --- | --- |
| T2 #649, distribution7041b0d710 / ES55158d2a6 | PL-024 resolved by a1cbc0ccd and PL-025 by4d4ae7060. 35PO/37files/38replacements verified directly; French3 additions have exact calls. Old count errors corrected as context, no reopened defect. |
| T21 #668, distribution82c67e99 / ES3ae9610b0 | French6 additions retained; recovery/BIOS/scraper/Wi-Fi behaviors stay T21. Historical generated build dependency choices are not current installed evidence. |
| T34 #681, distribution49c6b43f / ES52f0ff512 | ADD STAR/AJOUTER UNE ÉTOILE retained separately. 02:434,451 assigns fake AsyncNotification behavior to T18; current root fake membership in T44 does not transfer it. Historical allowed failures remain two may_fail cases/three assertions, not all-assertions-pass. |
| T35 #682, distributiond828355e / ESb7fdb3a24 | GAMEPAD/MANETTE retained; 02:663,686 names T21's five core CMake registrations and integration debt. Historical may_fail:1 remains allowed failure, not a fresh PASS. |
| T36 #683, distribution4127382d / ES9c1bd5f09 | No outside-app/core delta. zip_file.hpp/han.h are core paths, not T44 external rows. 02:436 assigns vendored-header license work to #256. Historical rapidjson1.1.0/GCC15 workaround remains historical, not invoked. |
| T20 #667, exact ref in prior-record-identities.json | 02:169-189 covers nine excluded fork files and explicitly assigns dual rcheevos markers to T44. Upstream12.5 applicability and three-hasher RVZ proof remain that owner's qualified prior evidence; no re-audit. |

## Self-refutation

A whole-source byte identity says nothing about installed compatibility. A parser can count a translation it cannot judge. An absent literal asset caller does not exclude dynamic theme/resource lookup. A stale-looking version header does not identify the entire linked library; the rcheevos12.2.1 and10.7.0 markers coexist. A new release does not establish a security issue or justify upgrading without a brief. Standalone fake tests do not simulate real Window scheduling, localization or font metrics. These limits prevented new bug/removal claims.

## Friction captured

New consumer attempts exposed escaped-backslash handling, a wrong assumed rename key, adjacent C++ literal matching and None binary line totals. Original failures and program bytes remain in stage-b; corrected positives are separately bound. Wrong guessed locale/evidence paths and one over-broad truncated read were corrected from the immutable path inventory; no empty/truncated read earns coverage. No source normalization, source export or historical edit was used.

Both time-to-play quantities are unmeasured. The post-disposition retro, final resolution lints, scratch retirement and root integration acceptance belong to E–H, not this D checkpoint.
''')
scores={1:'D artifacts present, tracker readback follows in stage-d',2:'PASS stage-a bound helper/root identities',3:'PASS keyed totals and explicit gitlink distinction',4:'PASS two594 tables plus3/450 and4 separate',5:'PASS exclusions/owner table and prior-record identities',6:'PASS complete5467-line register; doctest unchanged import',7:'PASS exact rename and French deltas/source calls',8:'PASS qualified seven-group table; precise currency inputs open',9:'PASS static interfaces,36 catalogue counts,77 XML parses and malformed controls',10:'PASS Q1–Q7, retrospective and self-refutation; no latest-version invention',11:'PASS table positive and seven independent refusals',12:'PASS actual Local identity/reviewers[]',13:'D pre-issue gate recorded; resolution/outcomes await root disposition',14:'No new reactive bugs; audit issue checker/readback at D',15:'D guard controls/live unchanged; final per-commit check bound externally',16:'D owned audit scratch listed; retirement is H',17:'D record/publication gates recorded; root final gates later',18:'Future G/H retro and final handback, not yet due',19:'Reviewed distribution seed/unchanged ES recorded; final distribution binding at H',20:'Root-owned integration/acceptance/marker/closure, not delegated'}
analysis='''# T44 analysis

## Executive Summary

The bounded table reconciles594 native keys, three450-line supplemental tests and four separate accepted companion branches. Full fork-code reading is5467 lines; vendored bodies are provenance coverage. One Low currency decision gap (doctest, PL-001) is ready for root disposition. The dual rcheevos marker is an inherited T20→T44 lead. No new product bug, fix, dependency removal or integrated image is claimed.

## Acceptance criteria Scorecard

These are artifact-level D observations against live #691's20 criteria, not ticks or final acceptance. Future-stage obligations are left explicit.

| Criterion | D observation / artifact |
| --- | --- |
'''
analysis+=''.join(f'| {i} | {s} |\n' for i,s in scores.items())
analysis+='''
## Risk assessment

The material risk is misusing table coverage as semantic or installed proof. The keyed methods, unchanged gitlink/import credits, companion separation and refusal controls prevent those claims in this packet. Version observations require applicability/carry decisions before any source update. No runtime defect severity is inferred from a newer release. Dynamic assets and unconditional vendor test targets remain retained.

## Coverage boundary

Primary ES55158d2a6 only, source/tree and metadata. 40 native fork-own code files/5017 lines and3/450 supplemental lines completely read; five fork-modified non-CODE deltas read; build/license/resource interfaces and named owner context read directly. 594 native tables do not mean143710 lines semantically reviewed. Binary/gitlink metadata and77 XML structure parses are not rendering. Both time-to-play quantities unmeasured. No combined companion source, source export, runtime, build, config sourcing, accepted test/producer, model-provider, device or cloud operation.

## Quality self-check

Bound input hashes prevent two equally tampered outputs becoming a positive. Seven independent table mutations refuse at specific assertions; parser malformed inputs refuse; confinement rejects source paths and deceptive path shapes. Source-call matching acknowledges lexical/preprocessor limits. Program/fixture/argv/time/rc/stdout/stderr hashes are retained, including failed consumer attempts. No frozen accepted receipt changed. Table totals derive from keyed rows. Historical allowed failures are named explicitly. New source defects were not established, so no speculative reactive bug was filed.

## Second opinion

Local under D-WORKFLOW-184/plan6c, actual Codex/openai/gpt-6-astra/openai/xhigh, observed in own Herdr footer (UI observation, not provider attestation), session01a19d12-1c5f-7022-8053-102f6a94b7fe/wN:p5. reviewers[]. No external or independent reviewer; prior preparation knowledge disclosed. The Local-lint positive and reviewer-count negative are stage-a/local-lint-controls, not a second opinion.

## Renovation face

### Q1 — Modernization

No product modernization is authorized. Seven vendor groups distinguish imports, local deltas and missing upstream mappings. PL-001 asks for a dated doctest carry/update decision. Any future update needs a scoped owner brief and must preserve the known accepted test semantics.

### Q2 — Standards

License and attribution markers are recorded per group and per native source header; mixed libretro notices are not flattened into MIT. No legal-completeness claim. PO syntax is checked in memory; translation meaning and format equivalence are not. Source test/build separation is documented, including id3's unconditional test target. PL-024's accepted catalogue spelling stays resolved.

### Q3 — Defects

No new behavioral defect has a complete trace/consequence/refutation in this bounded table. Existing T2/T18/T20/T21/T34/T35/T36/T37 behavior stays owned there. The failures during this audit belonged to new metadata consumers and were corrected with retained before/after evidence. No bug or fix is invented from counts, suffixes, age or unused-looking source.

### Q4 — Package currency

Doctest2.4.12 is exact unchanged import; observed primary release2.5.3 requires PL-001 disposition. rcheevos has12.2.1 and10.7.0 markers; current12.5.0 metadata is not compiled-subset proof and the inherited R13 lead stays explicit. libretro-common/id3v2lib/NanoSVG lack a sufficiently established current commit comparison; precise missing inputs are in vendor-groups.json. System pugixml1.16 matches its official release version; gitlink source/tag and installed identity remain unknown. No fetched source or build.

### Q5 — Efficiency

N/A for this provenance table: no runtime efficiency audit or measurement is proposed. Interface-to-first-frame and exit-to-next-first-frame both remain unmeasured. Metadata parsing durations are audit costs, not product performance.

### Q6 — Reachability

Root/external/locale CMake, resource copy/lookup and standalone test interfaces are statically traced. Distribution selects system pugixml and replaces the fallback font; source/installed distinctions remain. Binary metadata, a missing literal caller or an unconditional test target cannot authorize removal. Nine T20 rows excluded, es-app/tests T18, es-core/CMake T35; #700 integration later.

### Q7 — Clarity

Survey tier is not authorship, gitlink synthetic line is not source, companion branch is not integration. Failed consumers and corrected records remain separate. One new currency decision and inherited provenance inputs go to root with exact evidence, no execution pin or policy chosen here.
'''
put('04-analysis.md',analysis)
put('05-punch-list.md','''# T44 punch list — D checkpoint

One Low currency/documentation item; no Critical, High or Medium item and no new reactive bug. Root retains stream disposition and planning. Outcomes remain Open until that disposition.

## PL-001: Record the doctest carry-or-update decision against the observed release

- **Severity:** Low
- **Category:** Documentation Gap
- **Question:** Q4
- **Source Finding:** T44-CUR-01
- **Owner area:** #700 coordinator disposition; T18 and existing test owners for any later executable compatibility proof. T44 supplies this provenance decision input only.
- **What:** The exact unchanged doctest2.4.12 import is now compared with the primary release page showing2.5.3 on2026-11-02. The import explains its then-current2.4 choice but the named accepted records supply no current carry/update decision for2.5.3.
- **Where:** external/doctest/doctest.h:7-51 at ES55158d2a6; import324f9c483d9b4a11249c47888b40fb5cc691be7f; stage-b/history.json and vendor-groups.json.
- **proved:** tree/history/design
- **PROOF:** Unchanged header SHA25694029a7d32da24a56249658147dbd2b33ff0b9ed665295cbbaf19aafff5b0ced; https://github.com/doctest/doctest/releases/tag/v2.5.3 (dated read; displayed date year not inferred).
- **Already written:** Existing #649/#681/#682 accepted test records mention doctest and allowed failures, not a prospective2.5.3 decision. Narrow live issue searches for doctest/release references returned accepted owner issues; this is not an exhaustive global absence claim. No existing behavior finding is refiled and no reactive bug is opened.
- **Consequence/refutation:** A future updater lacks a current rationale/retirement condition. Newer release alone proves neither incompatibility nor security harm. A justified retain decision may be correct; existing test results must retain their original pins and allowed failures.
- **Can this be done on the VM?** No runtime is required to decide/document carrying policy. A later update's compatibility proof belongs to a separately dispatched owner and GENERIC_X64/its authorized pure tests. No such run is proposed here.
- **Ladder:** source/history and dated primary metadata; no executable compatibility or installed-image rung claimed.
- **Next mechanism:** Root records a scoped carry decision with rationale and revisit trigger, or creates a follow-up brief naming exact update target, consumers, negative controls and source/permission boundaries. No update is selected by this item.
- **Acceptance:** The Phase7 outcome cites the coordinator's exact decision/comment or a numbered follow-up, identifies2.4.12/observed2.5.3 and all affected test owners, and states the rationale plus revisit trigger or the bounded next brief. No accepted receipt is replayed or rewritten.

## Pre-existing tracked scope (NOT punch items — exempt from Phase 7 gate)

- T20 #667 R13→T44 #691: rcheevos12.2.1/10.7.0 dual markers, 02:183 at the exact T20 ref in stage-b/prior-record-identities.json. Current12.5.0 metadata does not settle import mapping or applicability. Root retains disposition; excluded hash/RVZ source changes and three-hasher obligations stay T20. No duplicate bug.
- T2 #649 PL-024/025 resolved: exact shared key and French3; companion additions6/1/1/0 remain #700's integration obligation.
- T18 #665 root AsyncNotification fake behavior; T35 #682 core CMake and T21 #668 five-registration integration debt; T36 #683 core zip_file/han and #256 vendored-header bucket; T37 #684 recipe/installed context. No owner transfer.
- libretro-common/NanoSVG exact upstream mapping and id3v2lib current revision are explicit missing currency inputs in the group table, not inferred bugs. Retain until root defines any further scope.

## Phase 7 resolution gate

| Item | Outcome | Evidence / next owner |
| --- | --- | --- |
| PL-001 | Open | D checkpoint; coordinator #700 disposition pending; no source action authorized |

## Machine-readable index

```yaml
punch_index:
- id: PL-001
  severity: Low
  category: Documentation Gap
  question: Q4
  source_finding: T44-CUR-01
  owner_area: interface; coordinator #700 with T18 and existing harness owners
  where: external/doctest/doctest.h:7-51 at 55158d2a64c69fe295fb4e67fd174424a71b1b4d
  ladder: source/history and dated primary metadata; compatibility and installed proof absent
  next_mechanism: coordinator carry decision with revisit trigger or separately scoped update brief
  acceptance: exact dated decision or numbered follow-up binds versions, rationale, trigger and owners without accepted replay
  outcome: open
```
''')
put('06-audit-summary.md','''# T44 Stage D summary

Source table over accepted T2 ES55158d2a6, distribution seed48a335700d. Two594-key tables,3 supplemental tests/450 lines,4 separate companion records; full native fork-code5017 lines plus450 supplemental lines read. PL-024 reconciles35PO/37files/38replacements; exact French3/6/1/1/0 and source calls retained. Seven vendor groups,36 catalogue rows and77 XML structure parses remain qualified source evidence.

New table positive and7 refusals, PO positive and4 malformed refusals, confinement positive and4 refusals all passed. Literal new-consumer failures are preserved. Exact receipts and hashes are under stage-a/b/c; stage-d carries lint/tracker/check receipts. One Low PL-001 asks for a dated doctest carry/update decision; inherited rcheevos R13 stays separately owned. No new runtime bug, source edit, dependency removal or combined ES tree.

Actual primary Codex/openai/gpt-6-astra/openai/xhigh, UI-observed Herdr footer; reviewers[]. Both time-to-play quantities unmeasured. No accepted replay, source export, config sourcing, build/guest/runtime/model-provider/physical/cloud action. All commands/children CPUs8–23. Whole ES stays at its clean seed. Historical T2 launch checkout remains untouched.

Root owns D disposition, any E–H brief, final integration/acceptance and closure. The new audit issue and clean published D tip are bound by stage-d/tracker records and the external final publication receipt reported to wN:p2. A D checkpoint does not satisfy future resolution/retro/retirement/acceptance criteria.
''')
put('07-questions-for-the-maintainer.md','''# T44 questions for root disposition

1. **PL-001, doctest carry/update:** retain unchanged2.4.12 with a dated rationale and revisit trigger, or scope a later update evaluation against observed2.5.3? Either decision must preserve accepted test identities and T18/other harness ownership. No upgrade or compatibility result is proposed by this table.
2. **Inherited T20 R13:** what bounded owner/action should carry the unresolved mapping of top12.2.1 and nested10.7.0 to the compiled subset and observed12.5.0? T20 already assigned the marker context to T44; its excluded patch applicability and RVZ behavior stay with T20. An exact-upstream source comparison would need separately authorized source acquisition; this run performed none.
3. **Remaining provenance inputs:** retain the explicit unknown current commit mappings for libretro-common/NanoSVG/id3v2lib in this table, or scope a later owner investigation? No published-release page establishes those current source identities. This question asks for disposition, not permission to fetch or remove anything now.

Settled and not reopened: Local review, accepted primary pin,594+3+4 separate populations, existing behavior owners, source-only limits, unchanged whole ES, no dependency removal, #700 integration later, T43 parallel records and T46 last. No routine approval relay or new policy is requested.
''')
# Manifest binds the annotations actually consumed by the final table/record composition.
files=[p for p in (A/'stage-b').glob('*.json')]+[A/'stage-b/tables.md']+[p for p in (A/'tools').glob('*.py')]
js('stage-c/consumer-input-bindings.json',dict(recorded_at=now,files={str(p.relative_to(A)):sha(p.read_bytes()) for p in sorted(files)},limits='Freeze of actual table and annotation inputs; this does not turn annotations into independent source review.'))
with (A/'00-running-log.md').open('a') as f:f.write('\n## '+now+' — B/C complete, D preparation\n\nFull source/delta/interface reads and keyed tables retained. Seven table refusals, four malformed PO refusals and four confinement refusals each failed as expected, complete positives passed. One Low doctest currency decision item; inherited rcheevos R13 preserved separately. Failed new-consumer attempts retained. No ES/source write or accepted replay. Root disposition follows clean published D.\n')
print('PASS composed02–07; exact native594 x2, full-code5017+450; one Low open PL; Local reviewers[]')

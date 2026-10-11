# Retrospective — M7 network/cloud feedback

Date:2026-10-11. Frozen source in inputs/source-manifest.json.

## Architectural coherence and spec fidelity

The shared connection module deliberately introduces one selected account, not
simultaneous multi-cloud sync. Missing sidecar preserves legacy alphabetical
first selection; empty tombstone prevents accidental fallback after removal.
Config staging/verification/publication and OAuth cancellation use compatible
lock order (connection lock then state lock); existing ownership tests exercise
cancel/supersede/success-publication failures. No new cloud relocation appears.

The gaps are consumers outside the new identity/exclusion contract: scan stamps,
folder seed writer and destructive preview. These are integration defects.

## Project conformance

| Rule area | Relevance | Finding |
| --- | --- | --- |
| engineering-practices / es-code-traps | all changed sources and UI lifetime | stack-copy fix and sanitizer negative control; actual target tests retained |
| rclone-cloud-sync / least-surprise / time-to-play | one active account, explicit actions, bounded calls | F-01–03 violate identity/consent/exclusion; staged credential verification bounded |
| vm-first / generic-x64-vm-testing / device-testing-policy | runtime proof | owned guest only; nmcli/authorize fixtures named; actual WebKit/rclone used where available |
| es-native-ui / es-ui-style-guide / es-player-text / player-language | manager/editor/retry/cancel | reviewed EN/FR layouts; no missing expiry inference; final frame-index/pin delivery still pending |
| packaging-and-patches | Python module installed beside CLI | pkgcheck rclone exit0; Python available in image and guest tests execute it |
| upgrade-and-install / release-candidates / bugs-are-agent-first | next installed image | no release claim; image qualification stays #537/#344 |
| documentation-accuracy / change-log | public and canonical flows | local docs updated; separate public-site follow-up must accompany delivery |
| fork-workflow / worktrees / milestone-phase-naming | isolated work and ordered plan | feature worktrees, unchanged next; M7 body lists #535–539 then #528 |
| decision-register / learning-capture / ceremonies | decisions and findings | D-CLOUD-184, D-UI-125, timestamped log and friction entries; final ceremony gate still owed |
| instruction-files / working-principles | canonical rules | next rules loaded, stale harness untouched; rules/register/index gates exit0 |
| adversarial-council / substrate-integrity | independent Epic audit | external phase follows settled primary findings through Facilitator only |
| handheld-evidence | docs/runtime evidence | no personal device action or unredacted private capture published |

## Blindspot review

Applied the register's recurring failure classes: summary versus artifact,
subshell failure loss, no-op assertions, first-source versus final-source proof,
real target tools versus host tools, callback lifetime, inherited lock ownership,
already-written data, default-name drift, watcher completion and seat identity.
The three new findings were proved with actual target scripts; hypothetical
account changes are no longer the only evidence. Rejected frames and failed
fixtures remain rejected. Credentials/private owner images never enter this packet.
No prior audit PASS was imported as proof of this new selected-account seam.

## Interaction: connection manager × scans

**State shared:** active-connection and rclone.conf. **Wipe risk:** stale options
describe a different account. **Test coverage:** TESTED. **Finding:** broken F-01.
cloud_setup validation_context includes the sidecar but cloud_scan does not.

## Interaction: connection manager × cloud writers

**State shared:** config and cloud_sync.lock. **Wipe risk:** changing/removing
credentials during a multi-command operation. **Test coverage:** TESTED seed
writer plus transactional busy refusal. **Finding:** broken F-02 at seed writer;
saved-data/content transfers already hold the shared lock during transfers.

## Interaction: destructive preview × selected account

**State shared:** match plan, config/selection/paths. **Wipe risk:** local content
removed/downloaded from an account not described by the confirmed preview.
**Test coverage:** TESTED two actual local aliases. **Finding:** broken F-03.

## Sibling-site search

Commands: `rg -n 'listremotes.*head|first_remote|active-connection|cloud_sync.lock'
projects/ROCKNIX/packages/network/rclone/sources/*`; `rg -n 'MATCH_PLAN|context_id|validation_context|take_cloud_lock'`
in the same tree; `git log -S active-connection --all --oneline -- projects/ROCKNIX/packages/network/rclone`.

| Class / site | Disposition | Basis |
| --- | --- | --- |
| F-01 scan context | FIX-NOW | add selection presence/bytes to fingerprint |
| Adjacent setup validation context | SAFE-AS-TESTED/code-read | already hashes active selection; unchanged-context tests needed after repair |
| F-02 seed writer | FIX-NOW | hold shared transfer lock before resolving target through final write/readback |
| Adjacent saves backup/restore | SAFE-AS-TESTED/code-read | resolve first_remote inside locked transfer body; staged connection tests refuse same lock |
| F-03 match preview/apply | FIX-NOW | bind plan to configuration identity, reject old unbound plans |
| Adjacent content copy preflight | FIX-NOW | current name-only recheck misses same-name account/credential edits; bind full context across preflight/lock |
| Adjacent settings backup/restore | SAFE-AS-TESTED/code-read | resolves selected remote under cloud lock; active-connection is device-only backup exclusion |
| External manual rclone config | BY-DESIGN boundary | outside cooperative lock protocol; writer compares current config before publication; no global process ban promised |

## Missing artifacts and tracked scope

Final whole-flow index, public documentation follow-up and installed-image
qualification were already open delivery work in #535–539/#344, not newly
discovered punch items. Search `rg --files docs/qa-logs/2026-10-11-network-cloud-management`
finds receipts/editor/browser and rejected frames; no final whole-flow index yet.

## Instruction File Recommendations

No new rule required: current shared-state, consent and exact-source evidence
rules already cover all three findings. Add executable target controls to avoid
another general prose rule. This is one issue chain, not evidence of three
independent process violations warranting a new instruction.

## Tier B visual-QA consolidation

Editor8-mode final review passed. Manager/form/refusal/source receipts and final
browser3-frame review exist. Original FR RESET overlap, stale name reopen and
long form hint are retained as rejected. Wi-Fi guard and manager flows keep
their actual es07/es08 sources, with final es11 editor delta stated separately.
Final index must not relabel old captures as the new binary.

## Retrospective Summary

Architecture is coherent but incomplete at three shared-state boundaries.
No extra provider or firmware scope is introduced. Resolve these defects,
then finish final proof/delivery and the already-tracked assembled-image gate.

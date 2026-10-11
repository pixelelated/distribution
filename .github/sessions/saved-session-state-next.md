# Saved Session State

> Updated: 2026-10-11T03:46:10.609983+00:00

> Previous checkpoint: 2026-10-11T03:38:29.104777+00:00
> Branch: feature/m7-p5-owner-observations
> Repository: pixelelated/distribution

## Start here — release policy/reconciliation delivered; owner reports recorded

This repo builds an immutable handheld OS. Read primary next's AGENTS.md,
every-session rules and relevant scoped rules before work. M7's live body owns
the queue. docs/releases/next-candidate-scope.md carries the full original18-issue
reconciliation, source/build budget and remaining release gates. Canonical UI:
docs/es-menu-map.md, docs/conflict-wizard-ia.md and cloud-folder-flow-review.md;
device authority: docs/device-testing-policy.md. Brand lowercase pixelelated.

Latest user requested #532 then #533, then reported red RG SP power LED at97%
while running on battery and requested an improvement issue to skip passwords
for open Wi-Fi networks. Those follow-ups are #534/#535. Later reports #536/#537 concern Dropbox phone clicks and missing clear connection management. The latest task is to triage and define these flows before the next build.

## Completed, with exact boundaries

#532 source40bc5469b9 and #533 reconciliation761da422dc are delivered to next
and origin. Original hosted wordlist job114376623135 and record114376622901
passed. Original watched consumer exited0, actual owners absent. Final receipt
/tmp/pix532-533-final-readback.json has remote equality, clean worktrees and
issue readbacks. #352/#510/#533 closed completed; #353/#354 not planned into
current owners. #529/#530/#531/#532 remain open for installed-image proof.
D-WORKFLOW-159 selects public rc.N/release, dev default, never-reused counter
per new frozen set and separately assembled/qualified release. Host57 controls
pass; original failed fixture retained. No allocation/tag/draft/publication.

#534 diagnosis: live/recovery led.color=red, also red in the pre-update receipt.
Actual red1/green0, triggers none, Discharging, USB offline, raw battery100,
warning threshold25. Owner saw97%; a later cache read94, shared reader prefers
cache. Dispatcher and actual H700 handler were separately identified, hashes
match source. Expected fixed selection; original writer unknown. No device
setting, screenshot, input, restart, reboot or cloud operation. Sanitized
docs/qa-logs/2026-10-11-rgsp-led/readback.json binds this. The only potential
follow-up is an owner's deliberate LED choice, requiring named authority if
an agent does it. Do not assume that permission.

#535/D-UI-125 is improvement backlog: unsaved open Wi-Fi skips password;
protected prompts remain; unknown security never inferred open; saved/connected/
forget mechanics preserved. Captive portal is separate. It is not implemented
and is not silently a new M7 freeze gate. Future ES change needs actual VM
EN/FR happy/branch frames, canonical flow/menu update and syntax-before-pin.

## New cloud reports — active source/design work

#536: owner specified Dropbox first screen and authorized one screenshot.
Captured via device-act, rc0, same boot id; reviewed720×480 at
/tmp/pix536-screen.png. It shows a hand over Continue with Google. Private
image remains local. A bounded read of /var/run/cloud_oauth/window.log counts
three refused login.microsoftonline.com navigations. Source filters gesture
cross-host navigation. This proves that branch was refused, not that every
click fails for that reason. No explicit tablet UA override in source;
tablet_pad is controller classification. No runtime UA sampled.
Phone moved<8 tap classification and60ms timer/independent move queue need
synthetic ordering tests; no cause assigned. Pending user question: does every
control fail or only Google/Apple/Microsoft, and does separate tap work?
Screenshot permission is consumed; no input or sign-in submission authorized.

#537/D-CLOUD-183: repeat native Dropbox setup requests fixed name dropbox;
existing same name is refused, different name may allow another connection.
No automatic dropbox2 or native reauthorization. Existing list/repair is buried
under Use a computer instead and SSH. Define visible connection lifecycle,
add vs sign-in-again/edit/remove, selected-reference and active-operation
handling, cancellation/rollback and preservation before implementation.
Exact ES checkout: /home/max/Development/emulationstation-next.worktrees/qa-integration,
HEAD1d76b3da7da75794066df1c089931b890304da7a; no modifications. GuiMenu.cpp
openCloudAddRemote/openCloudSetup and cloudOAuthStart are the entrypoints.
Distro cloud_oauth, cloud-signin-window.c and cloud_remote own backend behavior.
Sanitized hashes/trace: docs/qa-logs/2026-10-11-cloud-owner-feedback/.
No product fix or new runtime proof yet; no agent build/VM/audit job running.
Owner's sign-in may remain open and belongs to them; do not close it.

## Later code-pairing failure clarification — #537

Owner asks whether OK and EXIT do the same after code pairing fails. Exact
ES cloudOAuthShowSignIn failed branch: OK/null dismisses only GuiMsgBox;
EXIT closes s, whose session finalizer calls cloud_oauth cancel. Neither
retries; CONTINUE from failed returns to the same failure. User was told this.
Both verbatim reports and trace are appended to #537. Proposed TRY AGAIN /
CANCEL SIGN-IN must actually start fresh owned state vs cancel, preserve old
configuration, handle duplicate-name explicitly and distinguish specific
expiry from generic failure. No implementation or extra device action yet.

## Delivery boundary for the new records

The first owner-observation docs/register/log commit f304e7e5db34d41e04901aa919bd637f9722a464 is on next/origin. A later #537 clarification record is being delivered from
/workspace/repos/rocknix.worktrees/m7-p5-owner-observations,
feature/m7-p5-owner-observations, based on next761da422dc. Read
**/tmp/pix534-535-final-readback.json** and actual git/GitHub state before
assuming this later documentation delivery or #534 closure is complete.
No agent build/VM/audit/device job is running. The owner may still have their own sign-in open. The first docs CI consumer is in .build-runs/20261011T034236Z-7cf63892 (original runs38109210029/38109210083); if it or the later clarification-record consumer is active,
consume its original results; no rerun or firmware build needed.

Primary /workspace/repos/rocknix stays on next. Harness conflict-resolution
is historically divergent: never merge wholesale. Only fast-forward this
isolated branch's reviewed commits. Current sandbox requires escalation for
feature/primary writes and GitHub reads. Never print credentials/private config.
Use bounded parsed allowlists before displaying private JSON; raw grep of a
JSON line can expose unrelated fields. User devices remain in normal use;
previous three transfer/reboot authorities are consumed. RG SP Dropbox relink
is the owner's action with autosync off, not new agent permission.

## Next work

1. Verify the new-record receipt/current tracker; continue #536 VM diagnosis and #537 lifecycle design before freezing. #534 can close as explained
   expected behavior after evidence delivery; #535 stays Backlog. Prior #532/#533
   is already delivered and must not be re-run.
2. #528 firmware-affecting source/component choices proceed independently;
   #536/#537 decisions and changes also precede final freeze:
  17 declaration gaps, shader/per-file/vendor/prebuilt and ABL implementation.
  13 scoped notices are not13 cleared components. See corrected notice basis
   and #528. ABL implementation4588733123554b1f7bf935b04e494e4284894546 returned404;
   owner source/contact question is in the issue; no upstream outreach authorized.
3. Under #344, freeze all final commits/pins/container/time/qualifier/source index;
   proposed40bc5469b9 is not a final manifest and must include subsequent docs
   and #528 deltas. ES1d76b3da7da75794066df1c089931b890304da7a,
   splash8c71126ceef702528c87a4c49625e64988609f26 and pinned Makefile digest
   remain; verify at freeze. Recheck #493 capacity (previous about1.31TB free;
   conservative incremental generic budget554GiB including100GiB reserve), RAM/
   swap. Main agent actively supervises tools/watch-build/watch-job and announces
   original result/actual exit. Disconnected delivery remains #395 backlog.
4. GENERIC_X64 installed #529 readiness, #531 USB, #530/#532 identity, clean/
   public-config/real retained-storage tests, standard suites and missing #349
   same-model/foreign paired rows, #350 running/dead-endpoint scan branches,
   reviewed exact-source frames and applicable delta review precede RC claim.
5. #528/#344/#265/#337/#359 retain final inventory, corresponding-source/licence,
   independent retrieval/off-host custody, bot/runner readbacks, channel separation,
   support/adoption/recovery/SSH/branding/cloud/source notes, per-asset physical
   smoke and named publication authority. #511 full site stays separate.

Prior replacement18 composed qualification (#527),324 local protocol assertions,
31 real upgrade checks, CF10, RA and #471/#507/#524 audits remain accepted for
their exact source. Original qa21 failure stays failed. No replay to resume.
Large disks/firmware are immediate-test-only; retire after accepted proof using
guarded tooling, retain compact evidence and required source custody.

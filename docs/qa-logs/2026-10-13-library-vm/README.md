# M7 library, capability, and preservation VM evidence

**Qualification is partial; this disposable VM is complete and retired.** This record
keeps exact-source component results and selected reviewed frames. It does not
qualify a new firmware image or promote an EmulationStation pin.

ES `bb9e2785f88c2b9de979022a2a9ded2cbce2f954` was independently compiled;
[compiler evidence](../2026-10-13-library-compile/README.md) binds the target
binary and both catalogs. The private VM uses accepted replacement20, first
640×480 and then 1280×800, standard 8GiB/4CPU. All content and settings are
synthetic. No owner device, cloud, account, game save, or ROM was accessed.

## Completed evidence

- RVZ: candidate30 cases PASS; old reader7 PASS/23 explicit unsupported or
  malformed-case skips. Retry27 PASS. This is not sanitizer, independent
  format-oracle, or actual achievement-index acceptance.
- Capability: ten cases at each size, EN/FR, resolve AUTO, RetroArch and
  standalone overrides; all20 runners return0 and each verifies12 literal
  stored preferences unchanged. The selection-refresh and Favorites-source
  cases return0. No game was launched. A canonical GameCube declaration was
  injected for UI proof only; VM20 contains no native Dolphin engine.
- Global descriptions: runners return0, but French visual review rejects
  wrapping descriptions. Per-game French RetroArch descriptions also wrap at
  1280×800. Separate local ES09afa4893a6a fixes three catalog entries;
  compilation and replacement screenshots remain due. A runner0 does not
  override a rejected visual result.
- French Wi-Fi hints: small/large branch runners0; the larger refresh/failure
  frames show translated help prompts. Actual association is not exercised.
- Steam components: first combined run is **FAIL** at a fixture /dev/null guard,
  after root35/runtime39/Proton56 passed. Additive corrected FEX fixture735226
  passes43original+39guard controls with no remaining descendants. These are
  composed component results. Separately repaired c6240ed3984a with route-corrected
  fixture422955707938 now passes the complete synthetic caller: all nine steps,
  all12 preservation roots, final success and binfmt assertions, original installer0,
  no guard intervention/descendants (10.969s). Real payload/native ARM64, fresh-client
  and allowed-alias caller cases remain separate qualification.
- Dolphin: b2868 components123 PASS, plus8 original-source expected preservation
  failures. Actual mount/rename helper proof passes8 scenarios and6 synthetic card
  writes. Localized90cd follow-up51 PASS. The separate v4 complete-caller fixture now passes three1280×800 cases:
  GameCube retained-state refusal in French, Wii fresh setup in English, and Wii
  card conflict in French. Original ES/unshare/session/frontend exits are0;
  refusals preserve managed trees and show real native dialogs. Fresh setup
  creates correct state/card links and reaches the recording engine once.
  [Eight reviewed frames](dolphin-frame-index.json) accompany these exact scripts.
  The remaining matrix,640frames,package/upgrade and native-engine proof are due.

[frame-index.json](frame-index.json) lists only selected individually reviewed
frames. Rejected copy frames are labelled explicitly. Other raw frame captures
are not an accepted baseline. The exact injected configuration and rebinding
receipts are in records/source/.

## Original failures and limits

Initial setup/RVZ wrappers refused before payload. Capability probe/02 used the
wrong readback API; corrected03 uses literal keys. Those failed owners remain.
The system-level selection run returns1 because it demanded byte-identical
empty entries after AUTO→RetroArch→AUTO. Normal SystemConf persistence removes
empty emulator/core keys. Additive readback0 confirms the same frontend/boot,
no game launch and unchanged five explicit preferences; reviewed frames show
AUTO restored. The original assertion failure is preserved, not reclassified0.

Steam caller attempts before the accepted route-corrected run remain failures:
BusyBox dispatch127, then empty-route-oracle1. Both installer exits were null.
Dolphin v2 refuses missing external `false` before frontend stop; v3 reaches the
correct French native error but fails its trace-prefix oracle. The original
failed session remains1; its [three reviewed frames](dolphin-initial-frame-index.json)
are presentation observations, not a passing complete flow. V4 changes only
three exact trace matchers, with12 guest parser controls passing.

The final process readback initially matched its own observer shell. The second
readback excludes its recorded observer PIDs and finds no fixture processes; both
original observations are retained. [Lifecycle consumption](lifecycle/consumption.json)
checks all31 submitted owners, original failures and both QEMU exits. The parent
lifecycle returns0; that is not an aggregate suite PASS. Admission is consumed.
[Retirement](lifecycle/retirement.json) removes2,377,891,840 allocated bytes of
disposable disk/UEFI/temporary keys. No runtime remains from this owner. Stored .tar.gz
receipts are lossless compression of the original compact .tar results; no
synthetic game/archive payload or VM disk/private key is retained here.

Four original status records with trailing whitespace and two console logs with
extra terminal newlines are also losslessly gzipped;
no recorded bytes were normalized to satisfy the source whitespace check.

# #603 refutation addendum: AC-53 and hardcore Off

Read-only supplement to the immutable five-lead note sealed f638849f56e8b4bc0652381a4ff082280663f330c83a15f5a7079e1af066d370. No provider call, source/shared edit, archive expansion, runtime, device or fixture execution.

## AC-53: defensible aggregate PARTIAL; preserve accepted subclaims

Prior #596 `02-forward-audit.md:779–791` AC-064 and current #603 `02-forward-audit.md:813–823` AC-53 have the identical literal criterion:

> Document and verify behavior for RetroArch, standalone Dolphin and standalone Flycast using disposable VM fixtures: ordinary in-game save, manual state, exit auto-state and manager visibility are separate observations.

Prior AC-064 is PARTIAL, recorded2026-10-15T00:41:58.121231+00:00. Its exact remaining-scope sentence is:

> Native RetroArch/Dolphin/Flycast ordinary save, manual-state and exit/load observations remain UNRUN in this audit evidence set; parent owns serialization and new runtime.

Thus the prior PARTIAL was explicitly broader than just Dolphin/Flycast. It did not specifically identify a missing #196 transcript at that time; avoid rewriting that history as if it did.

Later native03 evidence accepts ordinary Wii entered-cell save/cold continuation and Dreamcast VMU score164 persistence only. Native-state02's `PASS_SCOPED_NATIVE_STATE_PROOF` and four first-frame records are Wii manual and three Dreamcast manual/native-auto launches. Those originals close the named Dolphin/Flycast seams. They contain no RetroArch launch. Final #596 reconciliation retains its original frozen score (80 PASS/16 PARTIAL/16 SKIP/3 FAIL) and scopes the native supplement; it does not retroactively turn every original native criterion into PASS.

Current AC-53 independently adds actual RetroArch ordinary-save baseline .srm/runemu evidence and current launcher controls, and the before/after #196 manager frames. Preserve all of that accepted evidence. It also explicitly acknowledges that the historical full raw RetroArch launch/stat transcript is not recovered and relies on a dated ledger for which process loaded/exited and caused the auto-state update. The later Dolphin/Flycast originals do not close that causality/source/process binding.

Recommendation: aggregate AC-53 PARTIAL for the remaining process-bound RetroArch exit-auto-state observation, with the delivered native Dolphin/Flycast legs and independently evidenced RetroArch subclaims enumerated. This is an evidence limitation, not a newly observed RetroArch product defect. A blanket “later evidence resolves original gap” PASS overstates the unchanged #196 boundary. Do not rerun successful Dolphin/Flycast work or perform an exhaustive archive hunt.

Smallest later proof, if root allocates it: one disposable RetroArch session under the existing qualified lifecycle, retaining exact image/core/launcher and process identity, selected auto-save/load inputs, numbered-state preservation, pre/post auto-state bytes/stat, normal exit original status and corresponding manager frames. This note allocates or executes none of it.

## G-05 deciding save line: hardcore Off writes literal0

At exact ES16dbac:

- `GuiRetroAchievementsSettings.cpp:621` creates HARDCORE MODE via `addSwitch(...,"global.retroachievements.hardcore",false,nullptr)`.
- `GuiSettings.cpp:408–414` registers the save callback and calls `SystemConf::setBool(localSettingsID,comp->getState())` for that non-Settings switch.
- `SystemConf.cpp:477–482` implements setBool via `set(name,value ? "1" : "0")`. It does not write the empty-string Off representation used by the unrelated global-autosave custom callback.
- The offline page invokes `raofflineproxy-ctl enable` at479; successful result handling at498–501 updates the parent switch and mirrors hardcore0. The ctl itself writes and reads back0 before publishing offlineproxy1 (473–478). The parent switch save also uses literal0.

Therefore the reviewer's specific “hardcore Off may write empty like global.autosave” hypothesis is refuted by the actual save callback. Missing/unknown raw values still deliberately fall back; that remains a supported negative control, not a claim that arbitrary retained/manual configurations always contain0. No new UI/runtime evidence is manufactured.

G-04 remains the previously reported deliberate interruption refusal. The blind claim that its stage contains only immutable shipped resources is too broad: the source is retained /storage/.config/dolphin-emu/GC and only selected managed names are excluded. Clear recovery guidance may be a useful follow-up; unconditional deletion ownership after a restart is not already proved.

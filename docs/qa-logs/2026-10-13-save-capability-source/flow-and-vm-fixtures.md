# Proposed canonical flow and prepared VM branches — UNRUN

Can this be done on the VM? **Yes.** Emulator selection, settings inheritance,
manager visibility, native save paths, and EN/FR presentation have no physical
dependency. Coordinator owns compilation, admission, runtime, and fixture media.
Nova's actual selected emulator is a separate unknown, not a reason to stop VM work.

## Canonical menu/copy proposal

Coordinator should update the Game Settings and save-state sections of
`docs/es-menu-map.md`, with an exact-source frame index, after qualification:

- GAME SETTINGS → SAVE STATES retains the same controls/values/order. AUTO
  SAVE/LOAD now explains “Supported emulators only. Save on exit and load on
  launch.” SHOW SAVE STATE MANAGER explains “RetroArch only. Show the manager
  before launching a game.” Its ALWAYS and IF NOT EMPTY choices are unchanged.
- GAME SETTINGS → system configuration, and a game's ADVANCED GAME OPTIONS,
  show **SAVE STATE SUPPORT** after Emulator and before SYSTEM OPTIONS only
  when the effective emulator is `dolphin` or `flycast`. AUTO follows the existing
  resolved selection. Choosing another emulator rebuilds the page as before.
- Opening that row shows one informational dialog, dismissed with OK/back. It
  does not launch a game or reopen itself and is never an extra launch prompt.
  Exact text: “THE AUTO SAVE/LOAD SETTING AND SAVE STATE MANAGER DO NOT APPLY TO
  THIS EMULATOR.\n\nUSE THE EMULATOR'S OWN SAVE OPTIONS. IN-GAME SAVES ARE SEPARATE.”
- Existing manager/help-bar gates remain: only eligible RetroArch games expose
  save states. A standalone native state is not a frontend-manager entry. Preserve
  the current START NEW GAME/auto/numbered-slot contract in the existing reference.

[copy.fr.po](copy.fr.po) supplies the four exact new EN/FR pairs. The existing FR
AUTO SAVE/LOAD label is **SAUV./CHARG. AUTO**, which the dialog references. No
catalog, shared map, change log, work log, or issue was edited by this worker.

## Next-source visual/control fixture

After the coordinator's existing immutable composition finishes, compose this
ES commit and the proposed catalog entries in a new candidate. Qualify EN/FR at
640×480 and 1280×800, with a source receipt for the executable, catalogs,
`es_systems.cfg`, `es_features.cfg`, and `es_savestates.cfg`. Suggested frames:

| Branch | Action and evidence |
| --- | --- |
| Global settings | Frame both changed descriptions; toggle neither merely to inspect. Back out and compare synthetic explicit preferences with pre-entry values |
| System AUTO → Dolphin | Disposable system default selects Dolphin; verify support row plus dialog/OK and safe back |
| System AUTO → Flycast | Verify same limits, native Flycast auto options not described as impossible |
| Per-game RetroArch override | System default standalone; game selects RetroArch. Support row absent; existing supported-core auto option and manager present |
| Per-game standalone override | System default RetroArch; game selects Dolphin/Flycast. Support row present; auto override absent per shipped features; existing manager/help-bar action absent |
| Selection refresh | Switch between those choices on the synthetic page; support row follows the rebuilt page once, without stale callbacks |
| Retained preferences | Seed global on/system off/game auto, and inverse overrides. Visit help/return; settings retain their meaning and no native auto option changes |
| Collection item | Same standalone game through a collection uses its source system. No platform-name inference |

Every changed row/dialog needs EN/FR small/large reviewed frames. Include the
absence branches, not only the dialog. A compiled fixture pass is not rendering
proof; text overflow, French wrapping, focus/back behavior, and page rebuilding
remain open until those frames and interactions exist.

## Disposable emulator-state matrix

Use separate disposable guest state per row, with coordinator-selected legal
homebrew/test content capable of an ordinary save and a distinguishable running
state. No content or BIOS is supplied here, and an invalid ROM stub cannot prove
engine save/load. Bind the actual emulator/core, final command, binary hash, and
effective configuration; record only the necessary synthetic settings, not account
values. No accounts or provider traffic are needed for ordinary branches.

| Control | Expected observation / failure signal |
| --- | --- |
| RetroArch supported core; global 1, inherited values | Existing #196 auto-state and manager behavior. Reuse the established section-v regression; record ordinary save independently |
| RetroArch per-game 0 with global 1 | Explicit off retained; no plain-launch exit auto-state. Existing numbered-state entry remains separately governed by #196 |
| RetroArch START NEW GAME with retained auto file | Existing auto file preserved, no new auto-state; do not introduce a new implementation to satisfy this control |
| Dolphin nogui GC; global 0 then 1 | Global flag alone changes no native auto wiring or ES manager eligibility. Separately create ordinary game save and manual state, observe orderly exit/relaunch |
| Dolphin Qt GC / Wii as available | Qualify frontend-specific manual-state/exit paths separately; nogui success is not Qt/Wii evidence |
| Flycast native auto options off; global 0 then 1 | ES preference alone does not enable native automatic states; ordinary VMU save and manual state remain separate observations |
| Flycast native auto options on; ES global 0 | On a supported offline content/slot and orderly unload, observe native auto save/load independent of ES setting; frontend manager still absent |
| Flycast native auto options on; forced exit path | Record whether unload runs and whether a state reaches disk. Do not equate process termination with successful auto save |
| Retained standalone state paths | Seed synthetic bytes at canonical state paths and legacy config directories/links; retain type, link target and byte manifests. Any unintended removal is a failure, never cleanup noise |
| Hardcore restriction | Use an existing coordinator-approved synthetic hardcore seam, verify the engine's **effective** hardcore state, then prove load refusal without weakening it. A flag with no active engine restriction is not PASS; account-dependent proof stays unverified |

For each engine observation retain four distinct results: ordinary game save,
manual state, exit auto-state/restoration, and manager visibility. Record slot,
path, old/new synthetic hashes, relevant launcher exit method, process exit and
frame. A synthetic hash is appropriate for disposable save bytes only, never an
owner credential or unknown private file. Assert untargeted synthetic save/state
files and explicit settings unchanged across both clean and retained cases.

No new standalone bridge should be added without proving orderly exit versus
kill, native load choice, file/slot naming, clean/retained paths and all applicable
hardcore restrictions. The inherited Dolphin directory replacement is a concrete
retained-path branch to inspect, not a finding this UI patch claims to repair.

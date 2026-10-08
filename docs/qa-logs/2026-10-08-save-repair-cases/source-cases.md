# #515: source-supported save placement cases

2026-10-08. Bounded source investigation, before implementation. No personal inventory,
device, cloud, emulator, VM, or test was run by this investigation. The follow-up
below reads existing synthetic qualification receipts. Names below are synthetic. This is a
finite case set, not an exhaustive emulator audit or #507's formal audit.

The important distinction is **a valid writer path omitted by cloud filters** versus
**a path that restore would place somewhere its intended emulator does not read**.
Moving ordinary standalone saves into `savefiles` would break several supported
writers. Conversely, the old tidier's wrapper handling and the actual restore mapping
provide stronger evidence for some conditional repair cases than filenames alone.

## Source identities and notation

- **P**, public ROCKNIX `release20261001`: distribution
  `c445081a59518f37d9776e5412dd7b14910696f7`.
- **D**, unintegrated replacement distribution snapshot:
  `6f89bc7cecee5972909828103689e2c7c0711c30`. This table describes that snapshot;
  subsequent #520 changes need their own evidence. Its paired ES source is
  `4e410dc9a816cc947f16235ad2b24824b29dd84e`.
- **T**, historical, unmerged tidy implementation:
  `4c83ebede40af27a375ced4cac72983be5715944`. Evidence of old algorithms, not a
  claim that public ROCKNIX shipped them or a requirement to reinstate migration.
- Coordination `next` at investigation start:
  `22571b47d21d6cb0736ffaa3a49b51ded36cc31f`.
- **R** = `projects/ROCKNIX/packages/network/rclone/sources/`.
- **E** = `projects/ROCKNIX/packages/emulators/`.
- **S** = `projects/ROCKNIX/packages/rocknix/sources/scripts/`.

Paths in the cases are relative to `/storage/roms`, or equivalently to the selected
saves cloud root under ordinary restore. Where another root is meant, it is explicit.
Every `commit:path:line` citation below identifies the inspected source bytes.

## Concrete case table

| Case and synthetic path | Writer, expected consumer and source | Actual P / D save rules | Detection, unique destination or ambiguity | Disposition |
| --- | --- | --- | --- | --- |
| C1: `nes/Example.srm` | RetroArch with the shipped content-directory setting keeps SRAM beside its content. P and D `E/libretro/retroarch/sources/H700/retroarch.cfg:659–667`; upstream RA `bdba046fa6766380bc2457532f38e589df769aaf:runloop.c:8510–8555`, especially 8533–8540. | Included by P `R/cloud_sync-rules.txt:10`, D `:23`. | Valid if the launch content is `nes/Example.*` with these effective settings. A basename alone does not identify a system, core, or override. | Preserve. Do not move into `savefiles`. |
| C2: `savestates/nes/Example.state`, `savestates/nes/Example.state.auto` | Launch configuration supplies `/storage/roms/savestates/<platform>`: P `S/setsettings.sh:16–20,790–824`; D same file `:882–916`, assignment at 903. RA emits `.state` paths (`runloop.c:8473–8479` at the pinned commit). | Entire `savestates/**` included, P `:6`, D `:19`; `.state*` is also included. | Valid with the corresponding launch platform. Existing per-game/core settings and emulator version remain part of compatibility; path correctness is not loadability. | Preserve. A state in another folder is only a repair candidate after its intended platform/core is established. |
| C3: `screenshots/Example.png` versus `nes/images/Example.png` or `nes/screenshots/Example.png` | RetroArch's player captures use `~/roms/screenshots` with content-directory screenshots disabled, P/D H700 cfg `:672–673`; Mupen64Plus shipped `ScreenshotPath` is `/storage/roms/screenshots`, D `E/standalone/mupen64plus-sa/mupen64plus-sa-core/config/H700/mupen64plus.cfg:56–57`. The content validator also recognizes per-system `screenshots` as media, D `R/cloud_folder_validate:25,163–169`. | First path included by P `:7`, D `:20`. The other `.png` paths are not included by the saves allowlist. | A PNG outside the capture root might be scraper media, artwork, or an intentional player copy. Neither extension nor `screenshots` at arbitrary depth proves it needs relocation. | Preserve known capture root; instructions/inspection for ambiguous media. Do not sweep PNGs into the saves tier. |
| C4: `n64/Example.eep`, `.mpk`, `.sra`, `.fla` | Mupen64Plus stores SRAM beside ROMs: D config `:59–61`; upstream `5340dafcc0f5e8284057ab931dd5c66222d3d49e:src/main/main.c:187–252,347–356`. Runtime chain is detailed below. | Public P excludes these at this depth; its `:18–20` only match `n64/save/`, and `.fla` has no include. D `:38–41` includes all four. | Valid standalone layout. This public gap was already fixed by #89 / D-CLOUD-086, documented in D rules `:30–37`. | Preserve; historical gap, **not a new current defect** and not a reason to move into `n64/save`. |
| C5: `n64/Example.st0` | Native Mupen64Plus slot state. The same installed runtime config sets `SaveStatePath=/storage/roms/n64`; pinned upstream `src/main/savestates.c:80–115` formats `.st%d` at 96/100. | Excluded by P and D: `.state*` does not match `.st0`, and neither has a `n64/**` include. D content exclusions also omit `.st0`, `R/cloud_content_restore:564–571`. | Valid writer path; ordinary slot is 0–9, config `:54–55`. Native filename identity comes from the emulator, not a generic ROM basename rule. | Current coverage defect reported to root and #520 worker before reproduction/fix. Correct filters/classification; **do not relocate**. Alternate `.pj0` / `.pj0.zip` formats are source-visible at `savestates.c:103–107`, but their runtime reachability is a separate control before broadening a fix. |
| C6: `psp/PSP/SAVEDATA/ULES00000TEST/PARAM.SFO`, `.../DATA.BIN`, `.../ICON0.PNG` | PPSSPP ordinary savedata: virtual `ms0:/PSP/SAVEDATA/<game-name><save-name>/...` mounted under `/storage/roms/psp`. Full pinned-source and patch chain below. `DATA.BIN` is a synthetic game-provided payload filename, not a universal filename. | Excluded by both P and D. `psp/PPSSPP/**` at P `:25` / D `:51` does not match. These names match no broad save-extension include; uppercase `DATA.BIN` reaches the catch-all (lowercase `data.bin` also hits the explicit `.bin` exclusion). A `.sav` payload could be included individually while companion SFO/PNG files are omitted. | Valid group, not a wrongly placed folder. A partial suffix-only backup is not proof of a complete save. Default files are depth 5 relative to the saves root. | Current coverage defect tracked under #520. Preserve the full supported savedata group and ordinary layout; do not move it into `psp/PPSSPP` or directly into `psp`. |
| C7: `psx/duckstation/memcards/Example_1.mcd`, `.../shared_card_1.mcd` | DuckStation packaged config selects per-game title cards; launcher redirects its `memcards` directory here. P/D `E/standalone/duckstation-sa/config/AMD64/settings.ini:169–173`; `scripts/start_duckstation.sh:12–45`. Exact packaged binary evidence below verifies native `.mcd` templates. | Excluded by P/D: the only `.mcd` include is **one directory shallower**, `psx/memcards/*.mcd` at P `:22` / D `:48`; there is no global `.mcd` include. D content excludes `.mcd` at `cloud_content_restore:568`, so the demonstrated issue here is missing saves backup, not that exact suffix leaking into content. | Valid default layout; depth 4. Per-game/card configuration and playlist title affect identity. `.mcr` is supported import evidence, not established as the default native writer extension. | Current #520 coverage defect. Do not move into `psx/memcards`; changing card names or selecting among cards needs effective settings, not guessed title matching. |
| C8: DS emulator directories | DraStic redirects `backup` to `/storage/roms/nds` and `savestates` to `/storage/roms/savestates/nds`: P/D `E/standalone/drastic-sa/scripts/start_drastic.sh:51–62`. melonDS seed separately names the same save/state directories, `E/standalone/melonds-sa/config/RK3566/melonDS.ini:143–144`. | Synthetic `nds/Example.dsv` and `nds/Example.sav` match P `:11,15` / D `:24,28`; all paths under `savestates/nds/` match the directory include. This row verifies launcher/config directory destinations; it does not claim that both suffixes are written by both emulators. | The directories themselves are valid standalone layouts. The misleading DraStic comment says `nds/saves`, but the actual `ln` target is `nds`. | Preserve. Do not use the comment or a preferred tidy structure to move saves into a new subdirectory. |
| C9: selected saves root contains `saves/nes/Example.srm` and `saves/savestates/nes/Example.state` | Older tidy code documents accidental `Saves/saves/` wrapping: T `R/cloud_migrate_layout:649–677`; the actual earlier defect/fix is identified below. Ordinary restore preserves the full relative path. If the intended effective consumers are C1/C2, restoring from the outer root produces wrong local paths. | Both suffixes can still be included by global extension rules. Inclusion does **not** prove correct placement. | Hypothesized destinations are `nes/Example.srm` and `savestates/nes/Example.state`, but current selected-root/configuration identity does not establish wrapper provenance or intended consumers. No product receipt proves this was the historical defect. Public P backup did not introduce this wrapper. | Historical wrong-layout example, **not a demonstrated implementable repair from current context alone**. Explicit selection of an owner-identified correct nested root remains available without moving files. A future repair must first establish unique consumers and collision-free mapping. Never auto-flatten by repeated-name detection. |
| C10: flat `Example.srm`, `Example.state`, `Example.png`, or a card copied into `savefiles/` | Actual consumers in C1–C8 require system/emulator paths and sometimes title/card identity. The permissive allowlist is a transfer policy, not a writer schema. | `.srm` and `.state` are included at arbitrary depth; arbitrary files in `savefiles/**` are included subject to D's earlier database exclusions. A flat PNG is excluded. | Multiple games, systems, emulator versions and card slots can share names. No unique destination is supplied by the path alone. A separately established launch/config identity can turn an individual file into a conditional candidate; this investigation has no such personal observations. | Instructions or narrowly scoped identification first. Do not implement a generic extension-to-directory sorter. This is not a claim that every possible repair is unsafe. |

## Runtime chains and filter boundaries

**PPSSPP.** P/D package `E/standalone/ppsspp-sa/package.mk:5` pins
`afbc66a318b86432642b532c575241f3716642ef`. At that upstream commit:

- `Core/Dialog/SavedataParam.cpp:49` fixes the virtual root at
  `ms0:/PSP/SAVEDATA/`; `:226–261` forms the game/save subdirectory; `:441–448`
  creates it; `:490–506` creates `PARAM.SFO` and records `SAVEDATA_DIRECTORY`.
- `Core/HLE/sceIo.cpp:658–670` mounts `ms0:` at `g_Config.memStickDirectory`.
  Stripping the `PSP` prefix only happens when `DIRECTORY_PSP` equals that root.
- Distribution `patches/004-set-paths.patch:30–31,105–110` sets the memory-stick
  root to `/storage/roms/psp/` and the configuration PSP directory to
  `/storage/.config/ppsspp/PSP/`. Those differ, so this chain retains `PSP/SAVEDATA`.
  The same patch's `DIRECTORY_SAVEDATA` getter at `:38–40` is **not sufficient
  evidence to conclude ordinary savedata is written directly under `psp/`**.
- The packaged `scripts/psp_save_mover.sh:4–11` independently corroborates the
  actual old-to-new targets: configuration `PSP/SAVEDATA` goes into
  `/storage/roms/psp/PSP/`; old states go into `savestates/psp/ppsspp-sa`.
- Save states and screenshots already have included roots:
  `patches/004-set-paths.patch:41–52` names `/storage/roms/screenshots/` and
  `/storage/roms/savestates/psp/ppsspp-sa`.

**DuckStation.** D `E/standalone/duckstation-sa/package.mk:5,12–32` installs
the versioned AppImage, launcher and device configuration. The ARM artifact in the
source cache has SHA-256
`f92319a0484e67bb62bfab7b0e56dac46165b50e45b51293038d9344a6288440`, exactly the
recipe's ARM hash at line 19. The filesystem starts at byte 667904. Reading
`usr/bin/duckstation-qt` with `unsquashfs -cat` and `strings -t x` (no execution,
no extraction to disk) finds these offsets within that binary:

| Offset | Exact string |
| --- | --- |
| `0xd0d11` | `shared_card_{}.mcd` |
| `0x112e8a` | `{}_{}.mcd` |
| `0xf8c4a` | `shared_card_1.mcd` |
| `0xdd0b8` | `PerGameTitle` |
| `0x118a90` | `DuckStation Memory Card (*.mcd)` |
| `0x118adb` | `All Importable Memory Card Types (*.mcd *.mcr *.mc *.gme *.srm *.psm *.ps *.ddf *.mem *.vgs *.psx)` |

The packaged launcher links `.local/share/duckstation` to `.config/duckstation`
at lines 24–27, and links `memcards` to `psx/duckstation/memcards` at lines 34–45.
It seeds settings only if absent (18–22); its later settings edits do not reset
memory-card settings. The #520 worker subsequently obtained the exact
`v0.1-10998` source; this investigation read that receipt as well. In upstream
`src/core/settings.cpp`, `:2489–2510` constructs shared/per-game `.mcd` names;
`:2698,2730` resolves the card directory relative to the data root.
`GetSharedMemoryCardPath` at `:2494–2503` explicitly accepts configured relative
or absolute card paths. In `src/core/system.cpp`, `:4085–4110` opens the resolved
card; `:6054–6126` chooses serial/title/playlist identity and prefers an existing
disc-specific card where appropriate. These exact-tag primary source receipts
corroborate the pinned ARM binary. A real per-game override or custom card
selection must be inspected before relocating any card.

**DuckStation screenshots: confirmed source defect, reported before any fix.**
This is normal player behavior, not merely an unused setting. P/D AMD64
`settings.ini:301` binds the screenshot hotkey to the controller; `:231` sets its
folder to relative `screenshots`. D's GENERIC_X64 config is a symlink to
`InputPlumber`; that seed binds the screenshot hotkey at line 94 and leaves the
folder unset, selecting the same upstream default. H700 also binds the action
at line 82 with no folder override.

At exact upstream tag `v0.1-10998`,
[`src/core/hotkeys.cpp:127–131`](https://github.com/stenzek/duckstation/blob/v0.1-10998/src/core/hotkeys.cpp#L127)
calls `System::SaveScreenshot()` on release. `src/core/system.h:421–424`
defaults the path to null; `src/core/system.cpp:5629–5661` chooses a sanitized
game title plus timestamp under `EmuFolders::Screenshots` and submits it to
`GPUBackend::RenderScreenshotToFile`. `src/core/gpu_backend.cpp:732–819`
renders and saves the image to that exact path. Save-state thumbnails use a
separate state-container path and do not explain away this standalone capture.

`src/core/settings.cpp:2709–2718,2733` resolves relative `screenshots` against
the data root. On Linux,
[`src/core/core.cpp:165–182`](https://github.com/stenzek/duckstation/blob/v0.1-10998/src/core/core.cpp#L165)
uses the configured XDG config root, or `HOME/.local/share/duckstation` otherwise.
D `packages/sysutils/busybox/profile.d/98-busybox.conf:5` sets HOME to `/storage`.
The launcher at `:24–27` redirects the latter directory to
`/storage/.config/duckstation`; it redirects states and cards but has no screenshot
symlink or screenshot setting override. Thus the ordinary default player capture
lands at `/storage/.config/duckstation/screenshots/<title timestamp>.<format>`,
outside `SAVESPATH=/storage/roms` (`D:R/cloud_sync.conf:22–24`). The saves tier
cannot cover that capture through its `/screenshots/**` rule. Custom absolute
folders may differ; this finding concerns the installed defaults. Root and the
#520 worker were informed before any change. This is source confirmation, not
an executed screenshot, a verified repair, or authority to move existing captures.

**Mupen64Plus.** D `E/standalone/mupen64plus-sa/mupen64plus-sa-core/package.mk:5–9`
pins upstream `5340dafcc0f5e8284057ab931dd5c66222d3d49e`; `:56–68` installs its
device config and launcher. H700 and GENERIC_X64 seeds have the save paths at
lines 59/61. `scripts/start_mupen64plus.sh:39–42` seeds only absent settings,
`:69–70` copies the effective config into its temporary config directory, and
`:96–211` builds runtime arguments and launches with that directory. None of
those runtime arguments overrides `SaveStatePath` or `SaveSRAMPath`; the scoped
package patches also do not change the state filename/path logic. Public P has
the same save-path behavior; D's added GENERIC_X64 repair only removes a malformed
controller configuration block. Upstream `src/main/savestates.c:118–124,141–145`
limits ordinary slots to 0–9. `src/main/main.c:163–184,359–363` constructs and
sanitizes the new native filename, replacing directory separators; the older
existing-file probe at `savestates.c:96` has separate legacy naming. PJ format
uses the raw trimmed ROM header (`src/main/rom.c:177–179`), and an explicitly
supplied filename bypasses the default mapping (`savestates.c:83–85`); the
ordinary root does not describe every malformed/custom path. Existing owner
customizations can select another directory and are not evidence of corruption.

**Shallow classification is incomplete.** D `R/cloud_folder_validate:213–228`
lists to depth 3. Normal PPSSPP savedata files are depth 5 and DuckStation cards
depth 4. The current `progress()` also lacks their ordinary paths (`:116–123`).
For an otherwise empty recognition result with unchecked depth-3 directories,
the script returns `unreadable/deeper-folders-not-checked`, not a proven empty
folder. Presence of another recognizable shallow file still proves only that
some recognized path exists; it cannot establish coverage or integrity of the
deeper standalone saves. #520 needs explicit bounded handling and paired
filter/validator controls, without interpreting directory names as verified saves.

## Old tidy and restore mapping: what can establish a repair

P `R/cloud_sync.conf:7–10` starts backup and restore at `/storage/roms`.
`cloud_backup:422–427` copies from that local root into the selected remote root;
`cloud_restore:481–486` reverses it. Neither changes a per-emulator relative path.
D `cloud_sync.conf:22–30` retains local `/storage/roms`, and
`cloud_restore:1910–1915` restores the selected `SAVES_REMOTE` directly into it.

T `R/cloud_migrate_layout:364–416` recursively enumerates and copies the selected
source tree preserving relative paths, verifies the copy, updates its pointer,
then deletes the copied source names. It did **not** reinterpret every `.srm`,
normalize standalone cards, or relocate all saves into `savefiles`. Its
`:649–677` wrapper logic excludes nested other tiers and selects a nested
`saves/` only when root-file checks establish that shape. Those old routines are
retired behavior, not a safe repair mechanism to reuse.

The concrete historical wrong-wrapper defect is recorded by fork commit
`9c4d9ed1b9f4125643ace3a2d0a4d49acc798923` (F-CS-23): before that fix,
`417dcd8610`'s root-presence check counted `/GAMES/Content` files as saves at the
root, so an already tidied `/GAMES/saves/` subtree could be copied into
`/ROCKNIX/Saves/saves/`. This is source/history evidence of an actual bad mapping,
not evidence that public P emitted it. With only the current selected root and
names, the product cannot distinguish that history from intentional per-content
nesting. No current receipt identifies the intended original consumer path, and
the broad extension allowlist deliberately accepts deeper valid paths. Therefore
C9 does not yet satisfy #515's implementable repair criterion.

D content restore has a different mapping: `R/cloud_content_restore:391–409`
maps selected content `ROMs/<system>` to local `<system>` and `BIOS` to `bios`;
`:1454–1455` chooses the corresponding local target. Its save exclusions at
`:564–571` are meant to prevent content restore from replacing live saves. A
save in `Content/ROMs/nes/Example.srm` is therefore not restored by current content
restore even though its relative system path is recognizable. Moving such a
file into the saves root requires established provenance, current save identity,
and conflict handling; a matching filename cannot select the authoritative copy.

For this finite source-supported set, no relocation can yet be derived safely
from the current selected-root/configuration context alone: C1–C8 are valid
writer layouts, C9 lacks distinguishing provenance, and C10 lacks unique consumer
identity. This is an evidence-backed scope disposition, not a claim that no safe
repair could ever exist. The next #515 controls should prove valid-layout
preservation and the ambiguous/wrapper no-action result, while #520 fixes the
demonstrated coverage defects. Any later supported repair case must add actual
distinguishing evidence rather than manufacture a success fixture from a guessed
mapping. Reflect the current instructions-only relocation disposition explicitly
in #510, the flow reference and M7; do not mark repair UI as implemented.

Before proposing any write, apply D-CLOUD-181's scoped manifest protocol from
`docs/cloud-save-integrity.md`: byte preservation, structural placement, and game
compatibility are separate conclusions. Keep an existing correct tree usable
through explicit folder selection where possible. Any eventual repair must show
exact source/destination paths and preserve source bytes until its separately
authorized completion policy is satisfied. No automatic root migration, legacy
joining, whole-account scan, or destructive tidy follows from these cases.

## Mapping C1–C10 to retained synthetic evidence

Read back after `coverage/final03/summary.json` recorded **39 PASS, zero FAIL**,
against product commit `1ee8e5199da0bc02e6aa4ebff94b951f5e8b4804`.
The actual validator SHA-256 is `c6eb5c3efc8c62df1c3f4f321ccff1bf9033305c83b53e6667a846d9305fd173`.
The summary distinguishes actual source hashes from the named `cloud_device_id`
fixture override. This is host qualification, not an installed-image or game
compatibility claim. `fixed01` failures remain failed history.

Earlier **V04** below means
`../2026-10-07-cloud-validator/validator/runs/final04.json` and its
`final04-summary.json`: 30 PASS on D. Its consolidated JSON retains raw outputs,
argv, synthetic input hashes, and snapshot checks. **F03** means this packet's
`coverage/final03/`: readback included each newly requested case's
`02-validator-call.log`, `ctl/argv`, and the implementing harness at
`tools/pixelelated-save-layout-test:321–366`. Its `validate()` asserts identical
cloud/storage before-and-after snapshots, allows only listing/context argv,
requires every listing inside the selected saves root, and retains the existing
listing count, depth, byte, entry, and time bounds. Fixture bytes are transport
sentinels, not valid emulator saves.

| Source case | Retained control and actual result | Disposition and limit |
| --- | --- | --- |
| C1, SRAM beside a ROM | V04 `populated-read-only`: `gb/progress.srm` is present/not verified; listing/context only, snapshots unchanged. | Valid layout preserved; no game-load claim. |
| C2, ordinary RetroArch states | F03 `validator-canonical-state` (`savestates/nes/Example.state`) and `validator-canonical-auto-state` (`savestates/nes/Example.auto`) both present/not verified, unchanged. | Covers ordinary state and `.auto` suffix classification. The literal automatic-state fixture uses `Example.auto`, not `Example.state.auto`; no emulator-generated state claim. |
| C3, captures versus per-system media | F03 `validator-canonical-screenshot` recognizes `screenshots/Example.png`. `validator-system-image-ambiguous` and `validator-system-screenshot-ambiguous` leave the respective `nes/images/Example.png` and `nes/screenshots/Example.png` unrecognized and unchanged. | No PNG relocation inferred. DuckStation's separate local default-root defect is #521, qualified in the sibling `duckstation-captures/` packet. |
| C4, N64 SRAM | V04 `ordinary-progress-allowlist` includes `.eep/.mpk/.sra/.fla` and reports present without writes. F03 `save-backup-restore` preserves `n64/Legacy.eep` through real-rclone backup/restore. | Valid-layout claim covered. Grouped V04 is not isolated suffix-by-suffix proof. |
| C5, N64 native states | F03 `filter-n64-st0`, `filter-n64-st9`, `validator-n64-state`, `save-backup-restore`, and `n64-system-root-scope` pass. PJ alternate and content/removed-system controls are named in its summary. | Default path/slot scope covered. Custom filenames and malformed ROM-header PJ paths remain outside this claim. |
| C6, PPSSPP savedata | F03 `filter-psp`, `validator-psp-depth5`, `save-backup-restore`, and content upload/restore/match controls pass. `PARAM.SFO`, `DATA.BIN`, and `ICON0.PNG` retain original relative paths. | Recognition and transport covered, without a container/game-compatibility claim. |
| C7, DuckStation cards | F03 `filter-duckstation`, `validator-duck-depth4`, and `save-backup-restore` pass for `psx/duckstation/memcards/Example_1.mcd`; imported `.mcr` remains in the round-trip fixture. | Default card recognition/preservation covered; custom card identity and card validity are separate. |
| C8, DS saves/states | F03 `validator-nds-dsv` and `validator-nds-sav` individually recognize `nds/Example.dsv` and `nds/Example.sav`, preserving snapshots and using listing-only argv. | Save suffix cases covered. C2 covers the shared state directory; neither control executes a DS emulator. |
| C9, double wrapper | V04 `content-misplaced-progress-preserved` retains `Saves/Saves/gb/progress.srm`, reports present, and does not flatten it. F03 `validator-nested-state-unseen` leaves `saves/savestates/nes/Example.state` unchanged and reports unreadable/deeper-folders-not-checked. | Repeated directory names do not authorize repair. The explicit PSP/card probes do not create permission for arbitrary deeper scans. |
| C10, flat or ambiguous names | F03 `validator-flat-srm` and `validator-flat-state` recognize flat progress extensions; `validator-flat-image-ambiguous` leaves flat `Example.png` unrecognized; `validator-card-in-savefiles` recognizes `savefiles/Example_1.mcd`. Every case is unchanged with listing-only argv. | Presence does not prove correct placement. No unique consumer or safe relocation follows from these names. |

The requested finite classification/no-action controls have now been received and
read back; none of those controls remains missing. This closes the host evidence
mapping only. Existing instruction-flow UI evidence keeps its own source
provenance. There is no implemented relocation action or repair screen to claim.
Root owns canonical references and tracker disposition.

## Defects handed off before changes

Root filed #520 for the PPSSPP/DuckStation ordinary-layout coverage mismatch;
the additional native Mupen64Plus `.st0` source finding was sent to root and the
#520 implementation worker before reproduction or code changes. C4's N64 SRAM
omission is already fixed in D. This source investigation did not implement #520. Its later bounded receipt
readback is recorded above. Root subsequently assigned the separate #521/#522
DuckStation implementation and qualification in `duckstation-captures/`; those
changes do not turn this source case table into a formal audit or a personal-state
inventory.

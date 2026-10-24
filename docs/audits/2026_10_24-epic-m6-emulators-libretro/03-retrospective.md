# Retrospective Audit — M6.P2 T3, RetroArch and the libretro cores

**Auditor:** Code Auditor skill (v1.13.0), primary Claude Opus 5.5 at high effort
**Date:** 2026-10-24
**Subject:** #650 (`M6.P2 E798/T3`), read at `reviewed-at: d606301784` (the slice's bytes equal to `8ebaf8daad`)
**Spec:** `docs/reviews/briefs/emulators-libretro.md` version 2; #650

---

## Running Notes

### 3.1 Architectural coherence

The slice is three mechanisms that meet at one file, `/usr/bin/runemu.sh`:

1. **What the image carries.** The core recipes, chosen per device by the metapackage's lists, with RetroArch and its 21 patches beside them. The lists are assembled from three variables (`LIBRETRO_CORES`, `EMUS_32BIT`, `PKG_EMUS`), an eleven-arm device `case`, an aarch64 addition and a GENERIC_X64 subtraction (`X64_SKIP_CORES`). That is coherent but opaque: what a device carries is a computation, and Q6 Table 1 is the first place it is written out.
2. **What the interface offers.** The launch table, 583 `add_emu_core` and 142 `add_es_system` calls in one 1,630-line function. It is produced by T5's `functions` through `xmlstarlet`, and the regeneration proves it is the build's own (byte-identical on three images).
3. **How RetroArch starts.** The per-device profile, the core options and the patches, composed at run time by T1's `setsettings.sh`.

The incoherence is at the joints, where each mechanism assumes the others agree:

- the table names a core the image may not carry where the launcher loads it (#802);
- the table may carry a system with no emulator (`st-v` on four built devices) or no default (`psx` on the VM);
- the profile carries keys RetroArch no longer reads (F-12).

### 3.2 Project conformance

| Face | Row | Verdict |
| --- | --- | --- |
| `packaging-and-patches.md` | late binding | ⚠ `sameboy-lr` (F-02): the one `pkgcheck` FAIL in 152 runs |
| | full-hash pin | ⚠ `wildmidi` (F-16) |
| | patches per device | ✓ (`batteryplus` under `PKG_PATCH_DIRS`; the device patch sets of `mupen64plus-lr`) |
| | a shipped script's CLI tools declared | ✗ `Install Steam.sh` needs `grep -P`, which grep's recipe does not guarantee (F-19, #806) |
| `device-builds.md` | § Late binding bites hardest in a merge | ✓ `ppsspp-lr`'s fix holds; ⚠ the next base merge brings two `${DISTRO}` copies (F-09) |
| | § A build that fetches its own dependency | ✗ `melonds-ds-lr` (F-15) |
| `upgrade-and-install.md` | every fix answers *Already written* | carried into every punch item (`05`) |
| `engineering-practices.md` | § Guards must fail closed | ✓ the generators' floor, the recipe's `sources/<DEVICE>` guard; ✗ `retroarch32`'s silent skip (F-11) and `mk_es_systems`' silent `fo` failure (F-06, T5's) |
| | § A name is not a behaviour | ✗ the README comment's "build failure" claim (F-06); `X64_SKIP_CORES`' "tracked in issue #16" (F-18); `content_history_dir` (F-12) |
| | § Change stays inside the fork's lanes (D-UI-079) | the player-visible items are routed through the coordinator (F-07, F-12's profile edits, F-14's options) |
| `time-to-play.md` | the two numbers on the image | ✓ 0.62 / 1.01 s (P2), beside T1's and #336's |
| `vm-first.md` | the VM question before each proof | ✓ (`02` § Guest proofs; #802's load failure named as what only a device shows) |
| `fork-workflow.md` | D-WORKFLOW-024, fork packages current | ✓ `fork-package-freshness` covers none of the slice (its one emulators path is T30's) |

**Blindspot register:**

| Blindspot | What happened here | Seen as |
| --- | --- | --- |
| 47 (a dependency the build fetched for itself) | **committed here**: `melonds-ds-lr` | F-15 |
| 39 (a table of dashes) | guarded: the Q4 scan's assertion fired once on two errored rows and was fixed, not bypassed | |
| 48 (an option changed without reading the log) | applied: every recipe's `git log -p` was read before its lines | |
| 50 and 55 (a log line is this run's) | guarded: each P3 launch removed `exec.log` first | |
| 54 and 63 (the renderer) | read on every launch: `virgl`; surface `889x800`, not scaled | |
| 65 (a substitute input) | named: `time-to-play`'s probe ROM | |
| 74 (a fixture that did not engage) | **committed and caught in this lane**: P3's first launch put `-state_slot` inside `--controllers=`. The log named what `setsettings` received, and P3b is the corrected run | the running log, § P3 |
| 13 and 46 (assumed done; a name read as a behaviour) | the shape of F-06, F-12 and F-18 | |

### 3.3 Spec fidelity

The brief's claims re-derived, with the deltas recorded:

- **No delta** on the 344 / 31,961 / tier counts (`01` § Scope).
- **Delta:** the table's `500 <core` elements are 348 `<core>` plus 152 `<cores>`.
- **Delta:** the brief's 131 `*-lr` recipes in the membership are 132 by suffix (`neocd_lr`).
- **Correction:** `6101242e14` is not on `origin`; `origin/feature/m7-player-setup` is ahead only by `d9054efc46`, whose `Install Steam.sh` equals `next`'s.
- **Gap:** the host regeneration needs the build's host `xmlstarlet` for every core, not only for formatting; it was closed with the build root's own copy.
- **Delta:** the H700 root is `m7-signin-h700-build-20261023-06`, not `-05`.
- **Wording:** #650's criterion 9 asks `git apply --check` where the brief § 4 says `patch --dry-run`; both were run.

### 3.4 Platform architecture conformance

The fork's five built devices against upstream's fifteen profiles:

- **Fork devices with an upstream-shaped profile:** H700, RK3326, RK3566, SM8550.
- **The fork's own:** GENERIC_X64.
- **Kept for upstream:** the other ten profiles (Table 4).

The VM image is a faithful stand-in for the installed set (P1), and not for the 32-bit path (no `retroarch32` on x86_64), which is exactly where #802 sits.

### 3.5 Cross-system interaction audit

### Interaction: the launch table × `runemu.sh` (T1's #648; #730 open)

- **`-P%SYSTEM%` after `%ROM%`:** `RUNCMD` places `-P%SYSTEM%` directly after `%ROM%`, and `runemu.sh` reads the system as `${ARGUMENTS##*-P}`, the last `-P` on the line. A ROM path holding `-P` reaches #730's territory. The table side is fixed text (`functions:128`), and T1's #730 owns the parse. Lead only, not changed here.
- **The save-state flags after `--controllers=`:** these are a contract between the interface and the launcher that the table does not state (the table's template ends at `--controllers="%CONTROLLERSCONFIG%"`; the interface appends the words).
- **Seen engaging (P3b):** the flags are read only as separate words. P3's first launch, which packed them inside the value, showed what a third writer of that line would get wrong.
- **#802:** the table names `pcsx_rearmed32`, and the launcher loads it through `/tmp/cores` over `/usr/lib/libretro` (P1 shows the overlay on the guest), where the image does not put it.

### Interaction: the launch table × `SystemData` (T2's #649)

Read at the interface's pin `16dbac5211` (`SystemData.cpp` 2179 to 2213):

- **No default** (F-05, `psx` on GENERIC_X64): `getDefaultEmulator` falls back to the first emulator, so on the VM `psx` launches **DuckStation standalone** (`duckstation-sa`, first in the table) without a word. It is a VM-only behaviour, but it is the VM every change is QA'd on first.
- **No emulator** (F-05, `st-v` on H700, RK3326, RK3566 and the VM): `getDefaultEmulator` returns `""`, so a launch has no command to build.
- **Two defaults** (F-06's case B, latent): `getDefaultCore` returns the first core marked default in table order, which is **the core listed `false`**. The latent defect would launch the wrong core.
- **The overlays** (`es_systems_custom.cfg`, `es_systems_*.cfg`) are read before the table, and one unparseable overlay skips every later one (T2's SD-3, reproduced there as G-5). The table this slice generates is the base the overlays modify, so its correctness is the floor under them.
- **The tokens:** the table emits five tokens; the interface also expands `%BASENAME%`, `%ROM_RAW%`, `%GAMENAME%`, `%SYSTEMNAME%` and `%GAMEINFOXML%`, raw (T2's FD-3). No shipped system emits them (`grep -c` over the five regenerated tables: 0), so they are reachable only by a player's own `es_systems_custom.cfg`.

### Interaction: the per-device `retroarch.cfg` × `setsettings.sh` (T1's)

- **Copied once, then layered:** the profile is copied once to `/storage/.config/retroarch/retroarch.cfg` (9fd73da845's note), then `setsettings.sh` writes its keys into the append config for every launch (`Added setting: state_slot = "-1"` in P3b).
- **Which keys it manages:** of the Q5 keys, `setsettings.sh` manages `video_shader_enable`, `rewind_enable`, `run_ahead_enabled`, `audio_latency`, `cheevos_*`, `netplay_*`, `menu_driver` and `savestate_auto_*` (grep counts in `04` § Q5). The profile's values for those are the defaults the per-game settings override.
- **Which it does not:** `log_verbosity`, `video_threaded`, `video_font_path` and `content_history_size` are not managed, so the profile alone decides them. That is why F-14 (the font) and P4 (the logging) are the profile's.
- **Upgrade consequence:** an upgraded device keeps its first copy of the profile, so a profile fix (F-12) reaches only fresh installs and keys `setsettings.sh` rewrites. Each such fix carries that line as its `Already written:`.

### Interaction: the cores' saves × the cloud sync's layout

- **Core pins:** the metapackage's `core-pins` (byte-identical to the images' on three devices) is what the capture step records as a save's `core_build` (#21, D-CLOUD-017).
- **A core bump moves that pin:** Q4 (a) row 14 (`np2kai-lr`) and Q4 (b)'s 102 `behind-project` rows are each a possible state-format change. Every `to merge` of a core bump cites #10, and the reading of its range is the stream's.
- **#802's fix and the save layout:** #802's fix adds a file under `/usr/lib/libretro` and changes no save path. Whether a state written by the 32-bit `pcsx_rearmed32` loads in the 64-bit `pcsx_rearmed`, which a player using the workaround meanwhile would rely on, is #10's question, unchanged by #802 and not read here.

### Interaction: the widget and cheevos patches × the proxy (#163)

- **0013 depends on the proxy:** 0013 reads `X-RA-Proxy` and `X-RA-Offline`, which the proxy's own patch 011 writes, so the toast's correctness rests on the proxy writing them. That is a cross-repository contract with no test in this tree; a lead for the offline-achievements area.
- **The widgets draw the proxy's banners:** 0014, 0016 and 0019 draw the toasts the proxy causes. On the shipped profile they draw M+ 1p (F-14), not the Inter that 0016 and 0017 were measured on.

### 3.6 What's missing?

- **A check that the table's cores exist where the launcher loads them.** #802 is a table-versus-image mismatch that no check catches: the regeneration proves the table is the build's, and nothing proves the build put each named core at `/usr/lib/libretro/<core>_libretro.so`. A host check over an install tree (every `<core>` of `es_systems.cfg` against the `.so` files, with the known non-libretro emulators excluded) would have caught it. It is a tool recommendation for `04`.
- **A check that a build's optional features are what they were last time.** grep's PCRE (#806) changed between two images of one source with no message. A list of `config.h` feature defines, or binary feature strings, compared across device roots is the class of check.
- **A full-hash rule and a no-fetch rule for cmake cores** (F-15, F-16). `pkgcheck` checks neither.
- **`tools/retroarch-wrapper-test` covers 0015 only:** 0011's poster lock has no driving case, and `--gated` asserts nothing (F-01).

### 3.6.5 Audit-prescription verification: the shapes, every site

| Shape | Every site |
| --- | --- |
| A `${DISTRO}` ARM-root copy | `git grep -F 'build.${DISTRO}-' next`: none; on the merged preview, two (F-09) |
| A `grep -P` consumer | two (`Install Steam.sh`; RK3566's `volumealign`) |
| A not-read profile key | 24 to 25 per profile, all fifteen (F-12; the list in `q6-retroarch-cfg-keys-not-read.txt`) |
| A late-binding reference | `pkgcheck` over all 152 recipes, one site (F-02) |
| A short pin | seven non-full pins read; one is a defect (F-16) |
| A fetch-at-configure | four grep hits read; one fetches (F-15) |

### 3.7 Retrospective Summary

## Retrospective Summary

### Architectural Assessment

Coherent within each mechanism, fragile at the joints (§ 3.1). The table is proven to be the build's own, and the images to be the tree's, so every finding is a finding about what ships.

### Cornerstone Alignment

Good on the fork's own lines (the rotation hooks, `idtech-lr`'s pinned data, the patches' headers). Weaker where upstream's lines met the fork's changes: F-09, #806, F-15.

### Cross-System Interactions

Five seams. Two carry live defects:

- the table against the image, #802;
- the build order against a script's tool, #806.

One carries latent defects: the table against `SystemData` (no default, no emulator, two defaults).

### Spec Drift

Seven brief deltas, recorded in § 3.3, none a stop.

### Missing Artifacts

These are recommendations, not this slice's to build (`04` § Instruction File Recommendations):

- a table-against-image core check;
- a build-feature drift check;
- a no-fetch guard for cmake cores.

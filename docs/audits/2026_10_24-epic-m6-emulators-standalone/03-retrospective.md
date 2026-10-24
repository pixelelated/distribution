# Retrospective Audit — M6.P2 T30, the standalone emulators (#677)

Written 2026-10-24 09:08 UTC (`date -u`), at stage B, after `02`. Phase 3 of the code-auditor skill over the 543 paths, with the renovation face in `04`. Leads are `02`'s F-NN.

## Running Notes

### 3.1 Architectural coherence

The 35 recipes share one architecture, and it is upstream's: a recipe installs a binary (built, an AppImage, or a vendor tarball), a config seed under `/usr/config/<emulator>`, and one or more `start_<core>.sh` scripts. `runemu.sh` runs the script by the table's core name (`start_${CORE%-*}.sh`, `runemu.sh:391`); the script copies the seed into `/storage/.config` on first run, links the emulator's save and state folders into `/storage/roms`, writes the interface's per-game settings into the emulator's config with `sed`, names its kill target, and runs the emulator. That shape is coherent and repeated 40 times by hand. Its weakness is the repetition: the same five steps written forty ways, with defects that recur by shape rather than by emulator (F-06, F-09, F-10, F-11, F-12). The fork's own additions (`dolphin-save-paths`, `duckstation_screenshot_path`, the cheevos scripts' session publication, the GENERIC_X64 repair block) are in a different register: guarded, fail-closed, commented with their reasons.

### 3.2 Project conformance

- `packaging-and-patches.md`: the 47 recipes pass `tools/pkgcheck`; every archive URL has a `PKG_SHA256` (D-WORKFLOW-193). The fork's changes to thirteen recipes each carry their reason in a comment beside the change (`engineering-practices.md` § A constraint lives beside the thing it constrains).
- `engineering-practices.md` § Guards must fail closed: the fork's scripts do (`dolphin-save-paths` exit 250; `cheevos_dolphin.sh`'s `settings_failed`); upstream's do not (F-11's comparisons fall through as true; F-10's unquoted test falls through as enabled; F-12's `rm -rf` runs whatever the copy did).
- `upgrade-and-install.md` § Migrating data: "copy, verify, then delete" -- F-12 deletes without copying, and DuckStation's memory-card migration runs only when the target is absent.
- `time-to-play.md`: nothing a start script does before `exec` measured above 0.07 s (G11); `runemu.sh` to the emulator's process 0.52-0.67 s (G12).
- `least-surprise.md`: an exit hotkey that works in one emulator and not the next (F-01, F-02, F-03) is the shape it names.

### 3.3 Spec fidelity

The brief's figures held: 543/157,365/55/10,695/35/47/thirteen. Three claims needed correction from the artifacts: the install trees' `os-release` is `etc/os-release` (the brief: `usr/lib`); the "41 start scripts" counts `Start Duckstation.sh`; and two of the GENERIC_X64 arms' fifteen recipes are dropped by their own `PKG_ARCH`, so the image carries thirteen, as the brief's version 2 says.

### 3.4 Platform architecture conformance

Three devices are in play (D-WORKFLOW-185): H700 builds 17 of the 35, SM8550 all 35, GENERIC_X64 13 (15 named, two dropped by `PKG_ARCH`). Per-device config directories exist for devices the fork does not ship (RK3566, S922X, SM6115 and the rest); the coverage table marks each as T25's unshipped table, and none is removed here.

### 3.5 Cross-system interaction audit

### Interaction: start scripts × `runemu.sh`'s arms × `input_sense`'s kill

The three halves agree on a contract nobody wrote down: the script must name, in `set_kill set`, the process name its emulator runs as, because `runemu.sh:179` clears the target before every launch and `input_sense:180-224` kills only what the file says. Four emulators break it (F-01 to F-04); `runemu.sh:128` then writes `emulationstation` as the target after the game, which is what made P1's fixture fault possible. The guard the ladder asks for is a check that every name a start script writes is an executable in the image (`tools/t30-routes.py` already resolves it; it is a test, not yet a gate).

### Interaction: the launch table (T3's `mk_es_systems`) × the recipes' `PKG_ARCH`

The table is generated from the device's lists; a recipe can drop itself from a device with `PKG_ARCH`; the two never meet. So GENERIC_X64's table offers five emulators its image does not build, two as defaults (F-05). T3's S2 `core_built` closes this for libretro cores listed and not built only because it reads the same lists. The seam belongs to T3's file.

### Interaction: the cheevos scripts × the interface's sign-in state × the offline proxy (D-RA-*)

The interface keeps the switch on and clears the token when an account changes offline or a sign-in is refused (`GuiRetroAchievementsSettings.cpp:767,780` at `16dbac52`). Two scripts were written for that state (dolphin, melonDS); five were not (F-09). The proxy routing in ppsspp's and dolphin's scripts (`proxy_listening`) is correct and identical in both, as `raofflineproxy-ctl`'s. #825's class does not reach the cheevos scripts: none builds a command from a value.

### Interaction: the configs × the save layout (#520) × the cloud sync

#520 qualified the standalone writers' save paths (PSP `SAVEDATA`, DuckStation's `psx/duckstation/memcards`, Mupen64Plus's `.stN`). This slice's F-12 is on the same paths from the other side: the link step that puts DuckStation's memory cards under `/storage/roms` (where the sync can see them) is the step that deletes a real directory without copying. F-29's `--configdir /tmp/mupen64plus` does not move the saves: `SaveSRAMPath` and `SaveStatePath` stay under `/storage/roms/n64` in the copied config.

### Interaction: `duckstation-sa` × T3's S2 (`psx`'s default on GENERIC_X64)

Since S2, `duckstation-sa` is the VM's default PSX emulator, so F-01 moves from an alternative route to the default one on the test image.

### 3.6 What's missing?

- A test that drives a standalone emulator's exit: `tools/emulator-exit-test` drives RetroArch only (`grep -o retroarch` finds it, no standalone name). This slice's P1/P2 are the first standalone exit runs on the VM, by hand. The harness gap is proposed for the coordinator (`bugs-are-agent-first.md` rule 3).
- Free content for the guest: five emulators exited on synthetic inputs before their kill could be observed (G1).
- shellcheck on the host: it would have found F-10 and F-11 (SC2086, SC2071) without a reader.

### 3.6.5 Audit-prescription verification: the shapes, every site

| Shape | Sites found | Hunt |
| --- | ---: | --- |
| kill target not the process | 4 recipes (F-01 to F-04) | every `set_kill` line of the 41 start scripts against the route tool and the guest |
| eval / xargs of player or device data | 3 (F-07, F-08, F-19) | the #825-class grep's 318 hits, read |
| session kept on sign-out | 5 (F-09) | the eight cheevos scripts, read whole |
| unquoted enabled test | 4 (F-10) | the eight cheevos scripts |
| comparison as redirection | 10 sites in 5 scripts (F-11) | `grep -E '\[ [^]]*[^-]( <>\| >\| <) [^]]*\]'` over the 55 shell files |
| delete then link | 9 scripts (F-12) | the 41 start scripts, read |
| loose `.zip` test | 3 scripts (F-06) | `grep -n 'grep -i .zip'` |

### 3.7 Retrospective Summary

## Retrospective Summary

### Architectural Assessment

Coherent and hand-repeated; the defects are shapes, not one-offs, so the remediation that lasts is a shared helper (link a storage directory safely; publish an emulator's achievements session) and a lint (comparisons, quoting), not forty edits.

### Cornerstone Alignment

The fork's own code meets the cornerstones; the upstream-carried scripts are where fail-open and delete-without-copy live. Change stays inside the lanes (D-UI-079): the launch path, game saves and the offline achievements are this fork's lanes, so F-01 to F-12 are in scope even where the code is upstream's (`bugs-are-agent-first.md` rule 6).

### Cross-System Interactions

Four seams, each with an unwritten contract: the kill name, the table's reach, the sign-in state, the save links. The first and the third are where the defects cluster.

### Spec Drift

None in the fork's own files. Upstream has fixed six of this slice's defects after the base (F-01, F-03, F-04, F-06's first half, F-16, `azahar-sa`'s pin), all class 1 with the base merge.

### Missing Artifacts

A standalone exit test; free guest content; shellcheck. The futro's predictions, checked: (1) a black screen read as a defect -- avoided, the synthetic inputs are named and the five early exits are "not tested", not defects; (2) the data files read line by line -- not done (provenance only); (3) the cheevos scripts graded from a grep -- not done, all eight read whole; (4) a `get_setting` value printed -- not done, values counted (G9) and the log read masked; (5) `aethersx2-sa` fixed -- not done, every row `deferred: base merge`; (6) a kill mismatch on an unshipped emulator graded High -- the route tool's classes separate them; (7) a guest while M7 held the host -- not done, the host file read before the boot; (8) time to play once with no n -- n=3, and named as launch-to-process, not first frame. One the futro did not predict: the probe killing the interface (P1's fault, fixed in P2).

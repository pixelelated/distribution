# Second opinion on a code audit -- M6.P2 T30, the standalone emulators, epic tier

You are a second reader of a code audit at the end of its reading stage. You cannot run commands or open the repository; everything you may cite is in the packet below, and every claim you make names the packet's `file:line` or the command output it rests on. The first reader's verdicts are in the packet; do not take them as given.

The scope: 543 paths of a handheld Linux distribution's standalone emulators -- 35 recipes (47 `package.mk`), their 40 start scripts that the launcher `runemu.sh` runs when a player presses a game, eight scripts that write the player's RetroAchievements session into an emulator's config, and their per-device configs -- read at one commit (`8ebaf8daad`). Behaviour claims were proven on a QEMU guest of the x86_64 test image (13 of the 35 emulators ship there) with synthetic inputs, and on the host against the install trees of three images. The first reader is Claude Opus 5.5 (Anthropic); you are a reviewer from another lab, and a second reviewer from a third lab reads the same packet independently. The audit is a renovation: besides defects, findings answer seven questions (Q1 modernize, Q2 standards, Q3 bugs, Q4 package currency, Q5 efficiency, Q6 dead ends, Q7 clarity); this slice's spine is Q3 (the launch path: the exit hotkey's kill target, and any command built from a ROM's name, a file's content or a server's answer) and Q4.

The first reader's draft grades (they become the punch list after your pass): **Medium** -- F-01 (DuckStation's kill target), F-02 (OpenBOR's none), F-04 (hatarisa's route), F-05 (the table's missing scripts on the test image), F-06 (zipped N64 ROMs), F-07 (`.scummvm` through eval, as root; Security), F-08 (gzdoom's xargs), F-09 (the previous RetroAchievements session kept), F-12 (a real directory deleted before linking), F-13 (portaudio's source gone; already filed); **Low** -- every other F-NN; **withdrawn** -- F-18.

Answer in three parts, in this order:

1. **Your own findings first.** Read the packet's evidence -- the scripts in full, the excerpts, the guest outputs, the tables -- and list every defect, gap or unsafe seam you find that is not already one of the first reader's findings. One line each: an id (G-01, G-02, ...), a severity (Critical / High / Medium / Low), the packet's `file:line`, what fails and when. Look especially at: kill targets against the binary each script runs; any `eval`, `xargs`, unquoted expansion or `sed` replacement fed by a ROM name, a file's content, a device's name or a sign-in value; anything that deletes or overwrites the player's saves or settings; anything that writes a credential where it should not.
2. **Refute the first reader.** For every finding at Medium, and any Low you think mis-graded: agree, disagree, re-grade or narrow, and in each case say what would make the finding false and whether the packet shows it. Say also whether the Q4 dispositions (`q4a-dispositions.md`: 33 to merge, 5 conflicts) and the exit sweep's 35 rows hold on the packet's own evidence.
3. **What you could not judge.** The claims the packet does not let you verify, so the orchestrator knows where its evidence was thin.

# The packet

## 02-forward-audit.md (whole, except the generated coverage table's 543 rows)

# Forward audit — M6.P2 T30, the standalone emulators (#677)

Written 2026-10-24 09:07 UTC (`date -u`) at stage B, from the read tree `8ebaf8daad` (the export `.qa-scratch/t30/at-hash/`). Line numbers are that tree's. Every finding is a lead until `04` § Finding Verification and § Second opinion grade it; the punch list (`05`) takes them from there.

## Phase 2: #677's checklist at stage B

| # | Criterion (short) | State at stage B | Artifact |
| ---: | --- | --- | --- |
| 1 | the folder holds 00 to 05 | 00, 01, 02 written; 03 and 04 next; 05 at stage D | this folder |
| 2 | the lint PASS (pre-issue before D, resolution at close) | not yet run | stage C to D |
| 3 | review-plan.json, Extended, both seats' provenance | not yet run | stage C |
| 4 | every punch item at a Phase 7 outcome | stage F | the audit issue |
| 5 | reviewed-at and fixed-at | `c7e3dfcc87` candidate; fixed-at at hand-back | #677's body |
| 6 | 01 § Scope: hash, filter output, counts, the diff, device × recipe | **done** | `01-research-notes.md` § Scope |
| 7 | the coverage table, 543 rows, Q1 to Q7 answered | **done** (generated, asserted 543 and no empty cell) | § Coverage below; `tools/coverage-table.py` |
| 8 | § Mechanical checks, each with command, exit, summary | **done** | § Mechanical checks |
| 9 | 04 Q3: the exit sweep (35 rows) and the shell-line sweep | the evidence is here (G1-G9, H1, H5); the tables are `04`'s | `04` § Q3 |
| 10 | 04 Q4: the two currency tables, no empty cell | `q4-pins.json`, `q4a-dispositions.md` | `04` § Q4 |
| 11 | 04 Q5 measurements; Q6 reachability; aethersx2's rows | G11, G12; the device × recipe table | `04` § Q5, § Q6 |
| 12 | the proof cells in § Proofs = the proof lines in 00 | 18 = 18 | § Proofs; `grep -c` |
| 13 | every item question:, bugs pass box-check, ladder named, no member edited | stage D; `git status --short -- <membership>` empty | `05` |
| 14 | census, vm-stop, census; pidfile under /workspace/tmp/m6-t30 | **done** for the one cycle (08:51:30-09:01:08) | 00's guest-cycle entry; `docs/vm-qa-log.md` |
| 15 | the retro | stage G | |
| 16 | the six checkers on the branch | stage H | |

## Mechanical checks

| Check | Command (at the hash unless marked) | Exit | Summary |
| --- | --- | ---: | --- |
| pkgcheck over the 47 recipes | `for r in $(git ls-tree … grep package.mk$); do tools/pkgcheck "$n"; done` | 0 ×47 | 47 rc 0; each run processed exactly its own `package.mk` (`checks/pkgcheck-coverage.txt`: `processed=1 self=1 warnfail=0` ×47); `tools/pkgcheck jre.zulu` rc 1 shows the exit status works |
| bash -n over the 55 shell files | `while IFS= read -r f; do bash -n "at-hash/$f"; done < shell.txt` | 0 ×55 | 55 ok; three files without `.sh`; control `if then` fails |
| shellcheck | `command -v shellcheck` | - | **not runnable**: not on the host (as T3 recorded) |
| PKG_SHA256 per branch | the brief's loop: URL count against checksum count per recipe | 0 | 16 short lines: 14 `.git` URLs (commit pins), 2 empty-URL metapackages; `heroic` has no URL line; `duckstation-sa`'s two branches each carry both. No archive URL without a checksum |
| the `.process-kill-data` writers | `git grep -n -F '.process-kill-data' 8ebaf8daad -- <001-functions> <runemu.sh> <standalone>` | 0 | `set_kill` at `001-functions:509-521` writes its argument verbatim; `runemu.sh:179` `set_kill stop`; `runemu.sh` sets targets for mednafen (235) and RetroArch (264) only; 38 of 41 start scripts call `set_kill set`; readers `input_sense:180-181`, `rocknix-fake-suspend:226` |
| the three install trees' start scripts | `ls <tree>/usr/bin \| grep '^start_.*\.sh$'` (BUILD_IDs from `etc/os-release`) | 0 | GENERIC_X64 `069fc27044` 21, H700 `08cc7ff6cd` 25, SM8550 `08cc7ff6cd` 48; against the hash by `cmp`: 16 differing pairs, all install-time `@NAME@` lines (H4) |
| the #825-class grep | `find … -name '*.sh' \| xargs grep -n -E 'eval\|\$\(\|\`' \| grep -i -E 'ROMNAME\|title\|name\|game'` | 0 | 318 hits (`checks/grep825.txt`), read file by file, not graded by the grep; the sweep's verdicts are `04` § Q3 |
| the cheevos logging grep | `find … -name 'cheevos_*.sh' \| xargs grep -n -E 'LOG_FILE\|>>\|tee'` | 0 | saved masked (`checks/cheevos-log.txt`); every line logs a fixed sentence, none a value |
| upstream's commits on the membership | `git log --oneline 8ebaf8daad..upstream/next -- <standalone>` | 0 | 38 (upstream/next `e0f9deb899`); `q4a-dispositions.md` |
| the fork against upstream | `git diff --stat upstream/next 8ebaf8daad -- <standalone> \| tail -1` | 0 | 144 files, +71,085 / -1,034 (most of it `aethersx2-sa`) |
| the routes (a tool of this slice) | `python3 -I tools/t30-routes.py … GENERIC_X64=… H700=… SM8550=…` | 0 | 37 / 72 / 145 standalone routes; no script: 11 / 5 / 6; fail-closed control rc 1 (H5) |
| Q4 pins | `python3 -I tools/q4-pins.py <tree> 8ebaf8daad upstream/next …` | 0 | 47 rows, no empty cell; `q4-pins.json`, `q4-pins-table.md` |
| the moving tarballs | `curl -L` into `/workspace/tmp/m6-t30/fetch/`, `sha256sum` | 0 | `aethersx2-sa` and `drastic-sa` match `PKG_SHA256` (08:47:53) |
| portaudio's source | `curl -sS -L -w %{http_code}` the recipe's URL; `gh api repos/PortAudio/portaudio/commits/64d1bf9…` | 0 | **http=404**; the commit is absent upstream (422); only the shared cache holds the bytes (F-13) |

## The leads the brief named, and what became of each

- **T3's PL-010 generalised (the exit sweep).** Every start script's `set_kill` line read beside the route tool's resolution and the guest's processes: F-01 (DuckStation), F-02 (OpenBOR), F-03 (Mupen64Plus simplecore), F-04 (hatarisa). The brief's figure "nine shipped" became thirteen with the stranger's proof; twelve binaries and `pico-8`'s script are confirmed in the GENERIC_X64 tree.
- **#825's class (the shell-line sweep).** F-07 (`start_scummvm.sh`'s `eval`), F-19 (`start_yabasanshiro.sh`'s `eval`), F-08 (`xargs` in `start_gzdoom.sh`); the cheevos scripts build no command from a server's answer (their values go into INI lines through heredocs and `sed`): F-21's delimiter is the one seam.
- **`aethersx2-sa` deleted upstream** (`c4d353449e`): F-26, class 1.
- **`eeb33c5a37` touching `start_mupen64plus.sh`**: F-03.
- **The hatari rename** (`2e7041d273`): F-04, proven on the guest (G2).
- **The moving-tarball pins**: both match today; the checksum is the pin and #844's empty-cache check the guard (F-27's note).
- **T1's `runemu.sh` arms**: read as context; no finding in T1's files.
- **`docs/reviews/build-path-read.md` (#644)**: none of its 26 findings is this slice's.
- **A lead this reading added:** the table (T3's file) offers emulators the image does not build, two of them as defaults on GENERIC_X64 (F-05).

## Findings (leads, graded in 04)

| ID | Q | Where (at `8ebaf8daad`) | What | Evidence |
| --- | --- | --- | --- | --- |
| F-01 | Q3 | `duckstation-sa/scripts/start_duckstation.sh:9`, `sources/Start Duckstation.sh:9` | the kill target `AppRun.wrapped` names no process: the pinned AppImages run `AppRun -> usr/bin/duckstation-qt`; the exit hotkey does nothing in DuckStation on any image; upstream `4a6415c033` | H1, G1, G7 |
| F-02 | Q3 | `openbor/scripts/start_OpenBOR.sh` | no `set_kill` at all (and no `/etc/profile`): after `runemu.sh:179`'s `set_kill stop` the exit hotkey kills nothing; upstream the same | G1 |
| F-03 | Q3 | `mupen64plus-sa-core/scripts/start_mupen64plus.sh:9` | `-9 mupen64plus` misses `mupen64plus-simple` (`:211`); upstream `eeb33c5a37` | G6 |
| F-04 | Q3, Q1 | `hatarisa/package.mk`, `hatarisa/scripts/start_hatari.sh` | the table's `atarist`/`hatarisa` route runs `start_${CORE%-*}.sh` = `start_hatarisa.sh`, which no image has; the script installed sets no kill target; upstream `2e7041d273` | G2, H5 |
| F-05 | Q3, Q6 | `virtual/emulators/package.mk` (T3's file) | GENERIC_X64's table offers `drastic-sa` (the `nds` default), `yabasanshiro-sa` (the `saturn` default), `amiberry`, `dsperate-sa` and `melonds-sa`, none of which the image builds; `core_built` (T3's S2) reads the device's lists, which name amiberry and yabasanshiro-sa before their recipes' `PKG_ARCH` drop them | G2, H5 |
| F-06 | Q3 | `start_mupen64plus.sh:78,81`; the same loose test in `start_hatari.sh:37`, `start_amiberry.sh:76` | `unzip -Zl -1` is Info-ZIP's zipinfo; the image's `unzip` is busybox: zipped N64 ROMs fail; `echo $1 \| grep -i .zip` takes any name containing "<char>zip" for an archive; upstream `195a8eba4b` fixes the first | G5 |
| F-07 | Q3 (security) | `scummvm-sa/scripts/start_scummvm.sh:68-70` | `GAME=$(cat "${GAME}")` then `eval /usr/bin/scummvm … "${GAME}"`: the `.scummvm` file's content runs as shell, as root; the file is ROM-library content (the tier the cloud restores); `runemu.sh:310` parses the same file with `awk` | G3 |
| F-08 | Q3 | `gzdoom-sa/scripts/start_gzdoom.sh:96` | `echo ${params} \| xargs /usr/bin/gzdoom`: a path with a space is split; an apostrophe stops `xargs` before gzdoom runs | G4 |
| F-09 | Q3 | `cheevos_ppsspp.sh:30-33`, `cheevos_flycast.sh:27-30`, `cheevos_armsx2.sh:37-40`, `cheevos_aethersx2.sh:27-30`, `cheevos_skyemu.sh:16-28` | with achievements on and the token empty (the interface's state after an offline account change or a refused sign-in, ES `GuiRetroAchievementsSettings.cpp:767,780` at `16dbac52`), the script exits leaving the previous account's token and enabled flag; skyemu also leaves `ra_token.txt` when achievements are off; `cheevos_dolphin.sh` and `cheevos_melonds.sh` clear them | G9 |
| F-10 | Q2 | `cheevos_armsx2.sh:30`, `cheevos_aethersx2.sh:20`, `cheevos_duckstation.sh:20`, `cheevos_flycast.sh:20` | `[ ! ${enabled} = 1 ]` unquoted: an empty key falls through as enabled; the fork quoted only `cheevos_ppsspp.sh`'s (#186 PL-31, `3d8e8044ee`) | G9 |
| F-11 | Q3 | `start_aethersx2.sh:102`, `start_armsx2.sh:113`, `start_daedalusx64.sh:48`, `start_mednafen.sh:82,89,144,157,187`, `start_melonds.sh:93,100` | a comparison written as a redirection (`>`, `<>`): each creates a file in the launch's cwd, `/storage`, and tests only non-emptiness | H3, G10, G13 |
| F-12 | Q3 (state) | `start_duckstation.sh:28,33,37-47`, `start_rpcs3.sh:14-29`, `start_azahar.sh:28,32,37,226`, `start_drastic.sh:57,61`, `start_ares.sh:24`, `start_skyemu.sh:30`, `start_bigpemu.sh:17`, `start_hatari.sh:18-21`, `start_cemu.sh:40-81` | a link step removes a real directory with `rm -rf` before linking it; only cemu copies first, without checking the copy; DuckStation copies memory cards only when the target is absent | G8 |
| F-13 | Q4, Q3 | `hatarisa/portaudio/package.mk:9` | the archive URL (`github.com/zhang-ray/portaudio`) returns 404 and the commit is not in PortAudio/portaudio; builds pass only from the host's cache; #841's class | the Q4 entry in 00 |
| F-14 | Q3 | `nanoboyadvance-sa/scripts/start_nanoboyadvance.sh:21-22` | `cp -r /usr/config/nanoboyadvance …/bios/gba/gba_bios.bin` makes a directory where the player's BIOS file belongs | read (a fixture at stage E) |
| F-15 | Q3 | `amiberry/scripts/start_amiberry.sh:34,62,70-71` | the resolution keys deleted (H2), `grep -e 'AGA\|CD32'` without `-E` (literal), the player's `conf/*` overwritten every launch | H2 |
| F-16 | Q3 | `supermodel-sa/scripts/start_supermodel.sh:87` | `"${OPTIONS}"` passes every option as one argument; upstream fixed after the base (`0c43a50420`) | read |
| F-17 | Q3, Q7 | `mednafen/scripts/start_mednafen.sh:175,8` | `-vb.3dmode` is given `${CE}`, not `${DM}`; `set -x` on every launch | read |
| F-18 | Q3 | `melonds-sa/scripts/start_melonds.sh:112-113,130,133` | `sed '/^X=/d$ a X=1'`: **withdrawn**, the image's busybox `sed` deletes and appends as meant (GNU `sed` rejects it: a portability note only) | the fixture at `/workspace/tmp/m6-t30/fx/mel/` |
| F-19 | Q3 (security) | `yabasanshiro-sa/scripts/start_yabasanshiro.sh:46-55` | `eval echo $GAMEPAD`, the name of a pad as it reports itself, inside `'…'`: a quote in that name runs as root on the first launch | read |
| F-20 | Q3 (security) | `gopher64-sa/scripts/start_gopher64.sh:104,125` | the RetroAchievements password on gopher64's argv for the whole session, unquoted | read |
| F-21 | Q3 (security), Q2 | `melonds-sa/scripts/cheevos_melonds.sh:79-104` | the password written plain into `melonDS.ini` every launch (the patch logs in with it, `000-retro-achievements.patch:992-1004`; `backuptool:707,1246-1256` blanks it in backups); `escape_sed` escapes `/` and `&` for a `\|`-delimited `sed` | read |
| F-22 | Q2 | `ppsspp-sa/scripts/cheevos_ppsspp.sh:35,105` | the token file written twice, with the default umask, not by temp-and-rename | read |
| F-23 | Q6 | `virtual/emulators/package.mk` (T3's file) | `AdvanceMame` (cps1 to cps3) and `moonlight` table rows have no script on any image (neither is a member) | H5 |
| F-24 | Q6, Q7 | `start_dolphin_gc.sh:436`, the gc/wii pair | `CMD="${CMD} -v $GRENDERER"` overwritten before use; the two scripts share 282 unique lines | read |
| F-25 | Q6, Q7 | `psp_save_mover.sh` (no caller), `cheevos_duckstation.sh` (call commented out), the six unused password reads, `start_touchhle.sh:71` | dead code and copy-paste | read |
| F-26 | Q4, Q6 | `aethersx2-sa/**` | deleted upstream (`c4d353449e`, licensing): every row deferred to the base merge, class 1 | q4a |
| F-27 | Q4 | the behind-project pins | DuckStation, dsperate, ScummVM, VICE, BigPEmu, the Steam launcher and others behind their projects (`04` § Q4) | q4-pins |
| F-28 | Q4 | `supermodel-sa`, `yabasanshiro-sa` | the pinned commit is on no default branch of its repository | q4-pins |
| F-29 | Q5, Q3 | `start_mupen64plus.sh:35,70,83` | the ROM copied into `/tmp` (tmpfs, RAM) before every launch; the config copied there and run with `--configdir /tmp/mupen64plus`, so an in-emulator setting is lost | read |
| F-30 | Q3 | `flycast-sa/scripts/start_flycast.sh:25-35,149` | `mv` then `ln -sf` over a path the `mv` may have made a directory; `kill -9 "$(pidof gptokeyb)"` quotes a multi-PID answer and kills every `gptokeyb` | read |

## Proofs

Each row's input is named; a synthetic one says so (blindspot 65). The time is the proof line's in `00`.

| ID | What it shows | Input | Artifact | proved |
| --- | --- | --- | --- | --- |
| H1 | the DuckStation AppImages' AppRun is duckstation-qt; no AppRun.wrapped | the pinned AppImages (real) | `/workspace/tmp/m6-t30/duck/` | proved: image-set |
| H2 | amiberry's substitution deletes the key | a fixture line (synthetic) | `the command in 00` | proved: fixture |
| H3 | [ a <> b ] reads true and creates b | bash, two strings (synthetic) | `/workspace/tmp/m6-t30/fx/daed/` | proved: fixture |
| H4 | the install trees carry the hash's start scripts, template-filled | the three M7 trees (real) | `.qa-scratch/t30/checks/start-cmp.txt` | proved: image-set |
| H5 | the routes each table offers, resolved, against each tree | the three tables (real) | `.qa-scratch/t30/routes.json` | proved: image-set |
| G1 | DuckStation and OpenBOR survive the exit kill; ppsspp and x64sc end | synthetic ROM files | `p1-exit-sweep.out` | proved: guest |
| G2 | four table routes exit 127 with no script | synthetic ROM files | `p2-cases.out, t30/p2/*.exec.log` | proved: guest |
| G3 | a .scummvm file runs shell as root | a crafted .scummvm (synthetic) and a plain control | `p2-cases.out` | proved: guest |
| G4 | an apostrophe in a WAD's name stops gzdoom | two junk WADs (synthetic), one control | `p2-cases.out` | proved: guest |
| G5 | a zipped ROM fails under busybox unzip | a zipped junk .z64 (synthetic) | `p2-cases.out` | proved: guest |
| G6 | busybox killall matches long names; mupen64plus-simple survives killall mupen64plus | renamed copies of python3 (substitutes) | `p2-cases.out` | proved: guest |
| G7 | the real AppImage survives AppRun.wrapped and ends on duckstation-qt | a junk .cue (synthetic) | `p2-cases.out` | proved: guest |
| G8 | a real memcards directory is deleted uncopied; the control migrates | a synthetic card | `p2-cases.out` | proved: guest |
| G9 | ppsspp and flycast keep the old session; dolphin clears it | synthetic token strings, counted | `p2-cases.out` | proved: guest |
| G10 | a comparison as redirection in /storage creates /storage/0 | the image's bash, two values | `p2-cases.out` | proved: guest |
| G11 | the Python helpers and the pk3 hash cost 0.02-0.07 s | the image's own files | `p2-cases.out` | proved: guest |
| G12 | runemu.sh to the emulator's process 0.52-0.67 s, n=3 | synthetic ROM files | `p2-cases.out` | proved: guest |
| G13 | the interface runs in /storage, writable | the running interface | `00's G13 line` | proved: guest |

## Coverage

(543 generated rows omitted from the packet for size; one per path, each cell a finding, a proof or `n/a` with a reason.)

## 03-retrospective.md (whole)

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

## 04-analysis.md (whole; its § Second opinion is what your pass fills)

# Analysis — M6.P2 T30, the standalone emulators (#677)

Written 2026-10-24 09:10 UTC (`date -u`), stage B, from `02` and `03`; § Second opinion follows Phase 4.6.

## Executive summary

The 35 standalone recipes (543 paths; 55 fork-own) are upstream's architecture, repeated by hand forty times, with the fork's own additions (Dolphin's save paths, DuckStation's screenshot default, the achievements sessions, the GENERIC_X64 repair) written to a higher standard. The defects cluster by **shape** on the launch path:

- **the exit hotkey does nothing** in four emulators (F-01 to F-04), DuckStation's among them, now the VM's default for PSX;
- **a ROM-library file or a name runs as shell** in three (F-07 as root from a `.scummvm` file, F-08's apostrophe, F-19's pad name);
- **the previous RetroAchievements account stays signed in** in five achievements scripts (F-09) on a state the interface creates;
- **a real directory is deleted before it is linked** in nine (F-12), memory cards included;
- **comparisons written as redirections** in five (F-11).

Six of these are fixed upstream after our base and arrive with the base merge (class 1). One currency finding is not code: `portaudio`'s source exists nowhere public (F-13, #849). 30 leads, 1 withdrawn (F-18), 13 guest proofs and 5 host proofs. Nothing in the membership was edited.

## Acceptance-criteria scorecard

Criteria 6, 7, 8, 12 and 14 are met at stage B (`02` § Phase 2); 9, 10 and 11 are met by this file's § Renovation face; 2, 3 and 13 at stages C and D; 1, 4, 5, 15 and 16 at F to H.

## Code Quality Assessment

### Strengths

- The fork's own scripts fail closed with a reason a player can read (`dolphin-save-paths`, `cheevos_dolphin.sh`'s `settings_failed`), write by temp and rename, and say in a comment why each line is there.
- `runemu.sh` and `input_sense` (T1's) are sound; the defects are in what each start script hands them.

### Concerns

- One unwritten contract (the kill name) broken four ways; one shape (`rm -rf` then `ln -sf`) copied nine times.
- `eval` and `xargs` over data the player supplies.
- Five achievements scripts that never learned what dolphin's knows.

### Complexity Hotspots

`start_dolphin_gc.sh`/`_wii.sh` (478/442 lines, 282 shared), `start_cemu.sh` (335), `start_steam.sh` (281), `start_vita3k.sh` (255).

## Cornerstone Conformance

`engineering-practices.md` § Guards must fail closed (F-10, F-11), `upgrade-and-install.md` § Migrating data (F-12), `least-surprise.md` (F-01 to F-04), `time-to-play.md` (G11, G12: nothing measured on the path above 0.07 s).

## Spec Fidelity

### Aligned

The brief's counts, the membership, the five pin shapes, and its leads (all six pursued, `02` § The leads).

### Diverged

The install trees' `os-release` path; the 41 start scripts; the table's reach (F-05) widens the brief's GENERIC_X64 picture.

## Missing Artifacts

A standalone exit test in `tools/emulator-exit-test`; free guest content for flycast, Dolphin, Mupen64Plus, touchHLE and ScummVM; shellcheck.

## Risk Assessment

| Risk | Where | Likelihood | Consequence |
| --- | --- | --- | --- |
| The player cannot leave a game with the hotkey | F-01, F-02 (every image), F-03, F-04 | every DuckStation and OpenBOR session | the emulator's own menu is the only exit; least surprise |
| Root shell from a ROM-library file | F-07 | a crafted file in a ROM pack or a shared cloud library | code as root on the handheld |
| Awards sent to the wrong account | F-09 | after an offline account change or a refused sign-in | the previous account earns them |
| A memory card or a PS3 save deleted | F-12 | a real directory where the link belongs (an old archive restored, the file manager) | the player's saves |
| A fresh build fails | F-13 (#849) | any host without this cache | no image |

## Coverage Boundary

Read at `8ebaf8daad`; the guest is the M7 image `069fc27044`, whose start scripts are the hash's (H4). Not covered: the 22 members the GENERIC_X64 image lacks, beyond reading and the image-set; first frames (no real content); the live kill of five emulators that exited on synthetic inputs; the 80 patches (T42/T43); the data files' contents (provenance only); `libdrastouch.c` beyond a skim.

## Finding Verification (Phase 4.5)

Each lead was re-read at its artifact before grading, and refuted where it could be:

- **F-01** could have been a stale name from an older AppImage layout. Refuted by the pinned bytes (H1) and by the live process (G7). Stands.
- **F-05** could have been the image predating T3's S2. At T3's tip, `core_built` still passes `amiberry` (the device's lists name it), and the `nds` and `saturn` defaults are unguarded. Stands, as T3's file.
- **F-07**: does `runemu.sh` reach `start_scummvm.sh`'s `eval` arm? Yes: the generic arm, then `*)` (G3). Stands.
- **F-09**: does the interface ever leave switch on, token empty? Yes (`GuiRetroAchievementsSettings.cpp:767,780`). Stands.
- **F-11** depends on the cwd. It is `/storage`, writable (G13). Stands.
- **F-12** needs a real directory to occur. Rare: current backups carry no symlink content (`backuptool:813-822`). Stands, graded by trigger.
- **F-18** is refuted by the image's busybox `sed`. Withdrawn.
- **The steam route's "no kill target"** is refuted by `start_steam.sh:262-281`. Not a finding.
- **`amiberry` and `yabasanshiro-sa` absent on GENERIC_X64** are by design (`PKG_ARCH`). Not a finding; their table rows are F-05.
- **The Python helpers' launch cost** measured negligible (G11). Not a finding.

## Renovation face

### Q1 Modernize

The fork's code is current: Python 3 stdlib, `renameat2`, `mktemp` with `umask 077`. The upstream-carried scripts write against busybox without knowing it: `unzip -Zl` (F-06), `grep -i .zip` regexes, and `echo -e` with unquoted arguments. One retired mechanism is still carried: `cheevos_duckstation.sh` ships though `start_duckstation.sh:130` no longer calls it (F-25), and `backuptool:705` still lists DuckStation's settings for blanking, correctly, because DuckStation signs itself in. The `testunofficial` fallback is read by `cheevos_dolphin.sh` and `cheevos_melonds.sh` as the pre-2026-09 spelling; upstream's `f8844ab04e` adds the same to `cheevos_armsx2.sh` (a q4a conflict row). The interface writes `.unofficial`, so the fallback is a compatibility read with no retirement condition (NAMING.md's shape), a Renovation note, not a defect.

### Q2 Standards and best practices

- `tools/pkgcheck`: 47/47 rc 0.
- `bash -n`: 55/55.
- shellcheck: not runnable (recorded).
- `PKG_SHA256` per branch: complete.
- The fork's header is kept on the thirteen changed recipes. Each change carries a comment with its reason.

Standards defects:

- F-10, the unquoted test, in four scripts.
- F-22, the PPSSPP token written with the default umask, twice.
- F-21's `sed` escaping.
- `start_OpenBOR.sh` sources no `/etc/profile`.
- The heroic, dsperate and steam scripts use arrays; most others build strings.

### Q3 Bugs

#### The exit sweep (35 recipes)

The name each start script writes to `/tmp/.process-kill-data` (`set_kill set`), against the executables of that name in the three install trees, and the guest's process for those it carries. *Row* reads `matches`, **differs** (a bug) or `not shipped on any built image`.

| Recipe | Start script(s) | Kill names written | Devices that build it | Executable of that name in the trees | Guest (GENERIC_X64) | Row |
| --- | --- | --- | --- | --- | --- | --- |
| `aethersx2-sa` | start_aethersx2.sh | aethersx2 | SM8550 | aethersx2: SM8550 | not on the guest | matches; class 1 (deleted upstream, F-26) |
| `amiberry` | start_amiberry.sh | amiberry | GENERIC_X64, H700, SM8550 | amiberry: H700,SM8550 | not built for GENERIC_X64; the table's route exits 127 (G2) | matches |
| `ares-sa` | start_ares.sh | ares | SM8550 | ares: SM8550 | not on the guest | matches |
| `armsx2-sa` | start_armsx2.sh | armsx2-qt | SM8550 | armsx2-qt: SM8550 | not on the guest | matches |
| `azahar-sa` | start_azahar.sh | azahar | SM8550 | azahar: SM8550 | not on the guest | matches |
| `bigpemu-sa` | start_bigpemu.sh | bigpemu | SM8550 | bigpemu: SM8550 | not on the guest | matches |
| `cemu-sa` | start_cemu.sh | cemu | SM8550 | cemu: SM8550 | not on the guest | matches |
| `daedalusx64-sa` | start_daedalusx64.sh | daedalus | SM8550 | daedalus: SM8550 | not on the guest | matches |
| `dolphin-sa` | start_dolphin_gc.sh, start_dolphin_wii.sh | ${DOLPHIN_CORE} | GENERIC_X64, SM8550 | ${DOLPHIN_CORE}: runtime/variable | exited on the synthetic input (G1); dolphin-emu-nogui's 17-char name matched by busybox killall (G6, substitute) | matches |
| `drastic-sa` | start_drastic.sh | drastic | H700, SM8550 | drastic: H700,SM8550 | not on the guest | matches |
| `dsperate-sa` | start_dsperate.sh | dsperate | H700, SM8550 | dsperate: H700,SM8550 | not on the guest | matches |
| `duckstation-sa` | Start Duckstation.sh, start_duckstation.sh | AppRun.wrapped | GENERIC_X64, H700, SM8550 | AppRun.wrapped: runtime/variable | comm AppRun, exe duckstation-qt: SURVIVED (G1, G7) | **differs** (F-01) |
| `flycast-sa` | start_flycast.sh | flycast | GENERIC_X64, H700, SM8550 | flycast: GENERIC_X64,H700,SM8550 | exited on the synthetic input before the kill (G1): not tested | matches |
| `gopher64-sa` | start_gopher64.sh | gopher64 | SM8550 | gopher64: SM8550 | not on the guest | matches |
| `gzdoom-sa` | start_gzdoom.sh | gzdoom | GENERIC_X64, H700, SM8550 | gzdoom: GENERIC_X64,H700,SM8550 | not run to a live process (G4's inputs) | matches |
| `hatarisa` | start_hatari.sh | **none** | GENERIC_X64, H700, SM8550 | - | the route's script absent: exit 127 (G2) | **differs**: no target, and the route's script is absent (F-04) |
| `heroic` | start_heroic_authenticate.sh, start_heroic_play.sh, start_heroic_play_gamescope.sh | Heroic heroic | SM8550 | Heroic: runtime/variable; heroic: runtime/variable | not on the guest | matches (runtime binaries: the player's or downloaded) |
| `hypseus-singe` | start_hypseus.sh | hypseus | GENERIC_X64, H700, SM8550 | hypseus: GENERIC_X64,H700,SM8550 | not run (no laserdisc content) | matches |
| `mednafen` | start_mednafen.sh | mednafen | H700, SM8550 | mednafen: H700,SM8550 | not on the guest | matches |
| `melonds-sa` | start_melonds.sh | melonDS | SM8550 | melonDS: SM8550 | not on the guest | matches |
| `mupen64plus-sa` | start_mupen64plus.sh | mupen64plus | GENERIC_X64, H700, SM8550 | mupen64plus: GENERIC_X64,H700,SM8550 | simple: the substitute SURVIVED (G6); the binary exited on its input | **differs** for the simple core (F-03) |
| `nanoboyadvance-sa` | start_nanoboyadvance.sh | NanoBoyAdvance | SM8550 | NanoBoyAdvance: SM8550 | not on the guest | matches |
| `openbor` | start_OpenBOR.sh | **none** | GENERIC_X64, H700, SM8550 | - | no kill data: SURVIVED (G1) | **differs**: no target (F-02) |
| `pico-8` | start_pico8.sh | ${STATIC_BIN} start_pico8.sh | GENERIC_X64, H700, SM8550 | ${STATIC_BIN}: runtime/variable; start_pico8.sh: GENERIC_X64,H700,SM8550 | not run (the player's binary) | matches (runtime binaries: the player's or downloaded) |
| `ppsspp-sa` | start_ppsspp.sh | ppsspp | GENERIC_X64, H700, SM8550 | ppsspp: GENERIC_X64,H700,SM8550 | comm ppsspp: ended (G1) | matches |
| `rpcs3-sa` | start_rpcs3.sh | rpcs3-sa | SM8550 | rpcs3-sa: SM8550 | not on the guest | matches |
| `scummvm-sa` | start_scummvm.sh | scummvm | GENERIC_X64, H700, SM8550 | scummvm: GENERIC_X64,H700,SM8550 | exited on the synthetic input (G1): not tested | matches |
| `skyemu-sa` | start_skyemu.sh | SkyEmu | SM8550 | SkyEmu: SM8550 | not on the guest | matches |
| `steam` | start_steam.sh, start_steam_arm64.sh, start_steam_x86.sh | FEX gamescope steam | SM8550 | FEX: SM8550; gamescope: SM8550; steam: SM8550 | not on the guest | matches (runtime binaries: the player's or downloaded) |
| `supermodel-sa` | start_supermodel.sh | supermodel | SM8550 | supermodel: SM8550 | not on the guest | matches |
| `touchhle-sa` | start_touchhle.sh | touchHLE | GENERIC_X64, H700, SM8550 | touchHLE: GENERIC_X64,H700,SM8550 | exited on the synthetic input (G1): not tested | matches |
| `vice-sa` | start_vice.sh | @EMU@ | GENERIC_X64, H700, SM8550 | @EMU@: runtime/variable | comm x64sc: ended (G1) | matches |
| `vita3k-sa` | start_vita3k.sh | vita3k-sa | SM8550 | vita3k-sa: SM8550 | not on the guest | matches |
| `xemu-sa` | start_xemu.sh | xemu | SM8550 | xemu: SM8550 | not on the guest | matches |
| `yabasanshiro-sa` | start_yabasanshiro.sh | yabasanshiro | GENERIC_X64, H700, SM8550 | yabasanshiro: H700,SM8550 | not built for GENERIC_X64; the default saturn route exits 127 (G2) | matches |

35 rows.


Every written name resolves to an executable in each tree that builds the recipe, or is a run-time name (the AppImage's, the player's binary, Steam's and Heroic's own), except DuckStation's, which names no process at all (H1, G7). Three of the four **differs** rows are fixed upstream after the base (`4a6415c033`, `eeb33c5a37`, `2e7041d273`); OpenBOR's is not.

#### The shell-line sweep (#825's class): every start and achievements script

| Script | Built from | Verdict |
| --- | --- | --- |
| `aethersx2-sa/cheevos_aethersx2.sh` | the sign-in settings | values into the emulator's config by heredoc or sed; no command built from a value |
| `aethersx2-sa/start_aethersx2.sh` | the ROM path | the ROM quoted to the emulator; GAME and PLATFORM used only as get_setting keys |
| `amiberry/start_amiberry.sh` | the ROM path | floppy names into the temp config through echo -e ${ARGS} unquoted; the zip test unquoted (F-06); a pad name into sed's replacement |
| `ares-sa/start_ares.sh` | the ROM path | the ROM quoted to the emulator; GAME and PLATFORM used only as get_setting keys |
| `armsx2-sa/cheevos_armsx2.sh` | the sign-in settings | the token passed to awk through ENVIRON (no interpolation); the username into sed's replacement |
| `armsx2-sa/start_armsx2.sh` | the ROM path | the ROM quoted to the emulator; GAME and PLATFORM used only as get_setting keys |
| `azahar-sa/start_azahar.sh` | the ROM path | the ROM quoted to the emulator; GAME and PLATFORM used only as get_setting keys |
| `bigpemu-sa/start_bigpemu.sh` | the ROM path | the ROM quoted to the emulator; GAME and PLATFORM used only as get_setting keys |
| `cemu-sa/start_cemu.sh` | the ROM path | "$@" passed whole (the platform argument too); controller names through xmlstarlet -v (no shell) |
| `daedalusx64-sa/start_daedalusx64.sh` | the ROM path | the ROM quoted to the emulator; GAME and PLATFORM used only as get_setting keys |
| `dolphin-sa/cheevos_dolphin.sh` | the sign-in settings | values into the emulator's config by heredoc or sed; no command built from a value |
| `dolphin-sa/start_dolphin_gc.sh` | the ROM path | the ROM quoted to the emulator; GAME and PLATFORM used only as get_setting keys |
| `dolphin-sa/start_dolphin_wii.sh` | the ROM path | the ROM quoted to the emulator; GAME and PLATFORM used only as get_setting keys |
| `drastic-sa/start_drastic.sh` | the ROM path | the ROM quoted to the emulator; GAME and PLATFORM used only as get_setting keys |
| `dsperate-sa/start_dsperate.sh` | the ROM path | the ROM quoted to the emulator; GAME and PLATFORM used only as get_setting keys |
| `duckstation-sa/cheevos_duckstation.sh` | the sign-in settings | values into the emulator's config by heredoc or sed; no command built from a value |
| `duckstation-sa/start_duckstation.sh` | the ROM path | the ROM quoted to the emulator; GAME and PLATFORM used only as get_setting keys |
| `duckstation-sa/Start Duckstation.sh` | the ROM path | the ROM quoted to the emulator; GAME and PLATFORM used only as get_setting keys |
| `flycast-sa/cheevos_flycast.sh` | the sign-in settings | values into the emulator's config by heredoc or sed; no command built from a value |
| `flycast-sa/start_flycast.sh` | the ROM path | the ROM quoted to the emulator; GAME and PLATFORM used only as get_setting keys |
| `gopher64-sa/start_gopher64.sh` | the ROM path | the ROM quoted; the RetroAchievements password on argv, unquoted (F-20) |
| `gzdoom-sa/start_gzdoom.sh` | the ROM path | **unsafe**: the WAD path through echo and xargs, split and quote-parsed (F-08; G4) |
| `hatarisa/start_hatari.sh` | the ROM path | the floppy names through echo -e ${ARGS} unquoted (spaces collapse, globs expand); the zip test unquoted (F-06) |
| `heroic/start_heroic_authenticate.sh` | the ROM path | arguments as an array |
| `heroic/start_heroic_play.sh` | the ROM path | arguments as an array |
| `heroic/start_heroic_play_gamescope.sh` | the ROM path | the compositor's numeric geometry through eval (:33); arguments as an array |
| `hypseus-singe/start_hypseus.sh` | the ROM path | the .commands file word-split into $params without eval (globs expand; no command) |
| `mednafen/start_mednafen.sh` | the ROM path | the ROM quoted to the emulator; GAME and PLATFORM used only as get_setting keys |
| `melonds-sa/cheevos_melonds.sh` | the sign-in settings | credentials into an INI through sed with an incomplete escape (F-21); no command built |
| `melonds-sa/start_melonds.sh` | the ROM path | the ROM quoted to the emulator; GAME and PLATFORM used only as get_setting keys |
| `mupen64plus-sa/start_mupen64plus.sh` | the ROM path | the ROM quoted to the emulator; the zip test reads $1 unquoted through echo and grep (F-06); unzip's name list reaches the path (F-06) |
| `nanoboyadvance-sa/start_nanoboyadvance.sh` | the ROM path | the ROM quoted to the emulator; GAME and PLATFORM used only as get_setting keys |
| `openbor/start_OpenBOR.sh` | the ROM path | the pak quoted |
| `pico-8/start_pico8.sh` | the ROM path | the ROM quoted to the emulator; GAME and PLATFORM used only as get_setting keys |
| `ppsspp-sa/cheevos_ppsspp.sh` | the sign-in settings | values into the emulator's config by heredoc or sed; no command built from a value |
| `ppsspp-sa/start_ppsspp.sh` | the ROM path | the ROM quoted, backslashes stripped (:105) |
| `rpcs3-sa/start_rpcs3.sh` | the ROM path | the .psn/.m3u first line into a quoted path |
| `scummvm-sa/start_scummvm.sh` | the ROM path | **unsafe**: the .scummvm file's content through eval, as root (F-07; G3) |
| `skyemu-sa/cheevos_skyemu.sh` | the sign-in settings | values into the emulator's config by heredoc or sed; no command built from a value |
| `skyemu-sa/start_skyemu.sh` | the ROM path | the ROM quoted to the emulator; GAME and PLATFORM used only as get_setting keys |
| `steam/start_steam.sh` | the ROM path | the compositor's numeric geometry through eval (:81); the game URI quoted |
| `steam/start_steam_arm64.sh` | the ROM path | the ROM quoted to the emulator; GAME and PLATFORM used only as get_setting keys |
| `steam/start_steam_x86.sh` | the ROM path | the ROM quoted to the emulator; GAME and PLATFORM used only as get_setting keys |
| `supermodel-sa/start_supermodel.sh` | the ROM path | the ROM quoted; the options as one argument (F-16) |
| `touchhle-sa/start_touchhle.sh` | the ROM path | the ROM quoted to the emulator; GAME and PLATFORM used only as get_setting keys |
| `vice-sa/start_vice.sh` | the ROM path | the ROM quoted, backslashes stripped (:15) |
| `vita3k-sa/start_vita3k.sh` | the ROM path | the zRIF from "$(cat ...)" quoted; .psvita content quoted |
| `xemu-sa/start_xemu.sh` | the ROM path | the ROM quoted to the emulator; GAME and PLATFORM used only as get_setting keys |
| `yabasanshiro-sa/start_yabasanshiro.sh` | the ROM path | **unsafe** (Low): a pad's self-reported name through eval (F-19); the ROM quoted |

49 scripts: three **unsafe** (F-07, F-08, F-19), the rest quoted or word-split without a shell.

#### The defects (each a `bug` at stage D unless noted)

F-01 to F-04 (the exit), F-05 (T3's file: the coordinator routes it), F-06, F-07, F-08, F-09 with F-10, F-11, F-12, F-13 (filed as #849 by the coordinator; a Medium row, no tree change), F-14, F-15, F-16 (class 1), F-17, F-19, F-20, F-21, F-29, F-30. F-22 is a standards item; F-24 and F-25 Renovation; F-26 to F-28 currency.

### Q4 Package currency

#### Q4 (a) behind-upstream: the fork against ROCKNIX

The thirteen fork-own recipes' pins equal upstream's (`q4a-dispositions.md` § The thirteen). What the fork changed in each is a dependency, an architecture guard or a comment, never the pin. Upstream's 38 commits on the membership since the base:

| Commit | Kind | Files | Overlap with fork changes | Subject | Disposition |
| --- | --- | ---: | --- | --- | --- |
| `0c43a50420` | commit | 20 | `dolphin-sa/scripts/start_dolphin_gc.sh`, `dolphin-sa/scripts/start_dolphin_wii.sh`, `duckstation-sa/scripts/start_duckstation.sh`, `mupen64plus-sa/mupen64plus-sa-core/scripts/start_mupen64plus.sh` | Merge pull request #3377 from sunshineinabox/PR_RotScaling | conflicts: rotation/scaling across the two Dolphin scripts, DuckStation's and Mupen64Plus's, all fork-changed (save paths, #521, the repair block); carries supermodel's array fix (`b6fcd2ca4f`'s base). Resolve hunk by hunk at the base merge. |
| `6679670966` | commit | 2 | `dolphin-sa/package.mk` | Merge pull request #3415 from sunshineinabox/WIP_gcc-glibc | conflicts: read at the base merge |
| `ca67c5f1dd` | commit | 1 | none | dolphin-sa: read wayland events in the nogui loop | to merge (no overlap) |
| `c92afac014` | commit | 1 | none | systemd: restore 255 parity for 261 | to merge (no overlap) |
| `bb9e42e2a0` | commit | 1 | none | rocknix: run games in games.slice with oomd and freeze on suspend | to merge (no overlap) |
| `b6fcd2ca4f` | commit | 1 | none | supermodel-sa: use the screen size for full resolution | to merge (no overlap) |
| `74c46ddbb9` | merge | 2 | none | Merge pull request #3435 from sunshineinabox/WIP_SystemD261 | merge: its content is its parents' rows |
| `32ebcdbf1b` | commit | 1 | none | rocknix: keep Steam alive when one of its processes is OOM-killed | to merge (no overlap) |
| `4a6415c033` | commit | 2 | `duckstation-sa/scripts/start_duckstation.sh` | duckstation-sa: point the quit hotkey at duckstation-qt | to merge, class 1: DuckStation's kill target `duckstation-qt` (this slice's exit sweep, confirmed by the AppImages' listing). The overlap is the fork's `duckstation_screenshot_path` call (#521), a different hunk: merges. |
| `eeb33c5a37` | commit | 1 | `mupen64plus-sa/mupen64plus-sa-core/scripts/start_mupen64plus.sh` | emulators: fix quit hotkey targets for RPCS3, AetherSX2 and mupen64plus | to merge, class 1: the kill targets (`mupen64plus-simple`; `Start RPCS3.sh` and `Start AetherSX2.sh` are T3's files, T3's PL-010). The overlap is the fork's GENERIC_X64 repair block (47-67), a different hunk: merges. |
| `2e7041d273` | commit | 3 | none | hatarisa: rename the start script to match the core name | to merge, class 1: `start_hatari.sh` -> `start_hatarisa.sh` and its kill target; the table's `hatarisa` route needs it. |
| `48b98a02d7` | commit | 5 | none | sm6115: initial Retroid Pocket Duo Lite support | to merge (no overlap) |
| `f610969ba1` | commit | 18 | none | dsperate-sa: bump to v3.0.1, refresh configs + es opts | to merge (no overlap) |
| `bc4db4f0e7` | commit | 1 | none | dsperate-sa: bump to v3.0.2 | to merge (no overlap) |
| `f8844ab04e` | commit | 1 | `armsx2-sa/scripts/cheevos_armsx2.sh` | armsx2-sa: read the testunofficial key like the other launchers | conflicts: upstream adds the `testunofficial` fallback to `cheevos_armsx2.sh`, whose token block the fork rewrote (#170, #308); keep the fork's block and take the one line. |
| `d74fde77e0` | commit | 1 | none | flycast-sa: read the auto frame skipping key ES writes | to merge (no overlap) |
| `2d34256719` | merge | 30 | `duckstation-sa/scripts/start_duckstation.sh`, `mupen64plus-sa/mupen64plus-sa-core/scripts/start_mupen64plus.sh` | Merge pull request #3464 from sunshineinabox/PR_QuitHotkey | to merge: overlap in a different hunk; read at the base merge |
| `195a8eba4b` | commit | 3 | `mupen64plus-sa/mupen64plus-sa-core/scripts/start_mupen64plus.sh` | mupen64plus-sa: fix zipped ROMs and DualSense controls | to merge, class 1: `unzip -Zl` -> `unzip -qql` (zipped N64 ROMs under busybox). Overlap: the fork's repair block, a different hunk. |
| `99870f0449` | commit | 8 | none | azahar-sa: async_shader_compilation feature | to merge (no overlap) |
| `5675ab7b28` | commit | 8 | none | azahar-sa: bump to v2126.2 | to merge (no overlap) |
| `e0bf3a55b0` | commit | 1 | none | azahar-sa: SM4450: symlink to InputPlumber config | to merge (no overlap) |
| `115a89be2b` | merge | 18 | `armsx2-sa/scripts/cheevos_armsx2.sh`, `duckstation-sa/scripts/start_duckstation.sh`, `mupen64plus-sa/mupen64plus-sa-core/scripts/start_mupen64plus.sh` | Merge pull request #3468 from qzydustin/setting-keys | to merge: overlap in a different hunk; read at the base merge |
| `7af4b5bcf3` | merge | 11 | `armsx2-sa/scripts/cheevos_armsx2.sh` | Merge pull request #3478 from porschemad911/azahar-v2126.2 | to merge: overlap in a different hunk; read at the base merge |
| `6103571f67` | commit | 1 | none | Merge pull request #3470 from sunshineinabox/WIP_core-updates | to merge (no overlap) |
| `a1ea79474b` | commit | 20 | `duckstation-sa/config/RK3566`, `duckstation-sa/config/RK3566/settings.ini` | rk3566: port to inputplumber | conflicts: RK3566's InputPlumber port touches `duckstation-sa/config/RK3566/settings.ini`, a fork-own file (#521's screenshot key). RK3566 is not a shipped device (D-WORKFLOW-185): take upstream's and re-apply the one key. |
| `2e85dcde25` | commit | 1 | none | melonds-sa: fix broken launch script (libmali) | to merge (no overlap) |
| `8c8800dc01` | commit | 1 | none | sm4450: add Retroid Pocket Classic 6 Rev Q | to merge (no overlap) |
| `ac844389f4` | commit | 1 | none | dsperate-sa: bump to v3.0.4 | to merge (no overlap) |
| `693632077e` | merge | 2 | none | Merge pull request #3498 from Jacob-Matthew-Cook/sm4450-rpclassic-sgb | merge: its content is its parents' rows |
| `075a7c303b` | commit | 2 | `dolphin-sa/package.mk` | Merge pull request #3513 from sunshineinabox/WIP_multimedia | conflicts: read at the base merge |
| `38cc9c7e7d` | commit | 3 | none | rk3566: fix some inputplumber issues | to merge (no overlap) |
| `c4d353449e` | commit | 17 | `aethersx2-sa/package.mk` | aethersx2: drop package due to licensing concern | to merge, class 1: deletes `aethersx2-sa` (licensing). The fork's 4 commits on the recipe (`PKG_ARCH`) go with it; `Already written:` in `04` § Q6. |
| `09ce29c548` | merge | 20 | `aethersx2-sa/package.mk` | Merge pull request #3534 from sunshineinabox/PR_ASX2 | merge of `c4d353449e`'s branch: as `c4d353449e`. |
| `abcb61ec9b` | commit | 1 | none | armsx2-sa: add patch to fix Vulkan backend on mali | to merge (no overlap) |
| `d91679afb8` | commit | 1 | none | dsperate-sa: bump to v3.0.5 | to merge (no overlap) |
| `62da3f7e23` | commit | 1 | none | dsperate-sa: S922X: use 'renderer' sink | to merge (no overlap) |
| `861c9ce4ea` | commit | 3 | none | ppsspp: change menu button combo | to merge (no overlap) |
| `3df05945a7` | commit | 5 | none | ppsspp-sa: remove the guide and misc swap patch | to merge (no overlap) |


38 rows: 33 to merge, 5 conflicts, 0 superseded. Every row is taken by the base merge (the coordinator's); this branch cherry-picks none.

#### Q4 (b) behind-project: the 47 pins against their projects, by shape

| Recipe | Shape | Pin | Against its project | q4-pins class | Disposition |
| --- | --- | --- | --- | --- | --- |
| `aethersx2-sa` | moving tarball | `1.5-3606` | matches PKG_SHA256 today | pin-not-on-project | deferred: base merge, class 1 (F-26) |
| `amiberry` | hash | `5c54536997c0` | behind-project; default branch head 2026-10-24 | behind-project | informational (upstream-carried; ROCKNIX's to take) |
| `ares-sa` | hash | `0aafd8578921` | behind-project; default branch head 2026-10-22 | behind-project | informational (upstream-carried; ROCKNIX's to take) |
| `armsx2-sa` | hash | `19c83bf065ed` | behind-project; default branch head 2026-10-23 | behind-project | informational (upstream-carried; ROCKNIX's to take) |
| `azahar-sa` | hash (tag 2126.0) | `fbd3fb02f71e` | behind-upstream: ROCKNIX pins 219d743a1e (v2126.2) | behind-upstream | to merge with the base (q4a), class 1 |
| `bigpemu-sa` | release asset | `v119` | v119 against v1221 on the download page | by-hand | bump proposed (F-27) |
| `cemu-sa` | hash | `6f6c1299e29f` | behind-project; default branch head 2026-10-22 | behind-project | informational (upstream-carried; ROCKNIX's to take) |
| `daedalusx64-sa` | hash | `f17e9ed86f38` | behind-project; default branch head 2026-10-10 | behind-project | informational (upstream-carried; ROCKNIX's to take) |
| `dolphin-sa` | hash | `6094cfcf7b8f` | behind-project; default branch head 2026-10-22 | behind-project | informational (upstream-carried; ROCKNIX's to take) |
| `drastic-sa` | moving tarball | `1.0` | matches PKG_SHA256 today | pin-not-on-project | kept: the checksum is the pin; #844's check is the guard |
| `dsperate-sa` | release asset | `2.0.1` | 2.0.1 against v3.0.5; ROCKNIX already at 3.0.5 | pin-not-on-project | to merge with the base (q4a), class 1 |
| `duckstation-sa` | release asset | `0.1-10998` | v0.1-10998 against v0.1-11894 (latest 2026-10-13) | pin-not-on-project | bump proposed (F-27), F-01's target re-checked with it |
| `flycast-sa` | hash | `5aa091fde632` | behind-project; default branch head 2026-10-24 | behind-project | informational (upstream-carried; ROCKNIX's to take) |
| `gopher64-sa` | hash | `ca4a20f52403` | behind-project; default branch head 2026-10-22 | behind-project | informational (upstream-carried; ROCKNIX's to take) |
| `gzdoom-sa` | tag | `g4.14.2` | g4.14.2 = the latest release (2025-05-03) | pin-not-on-project | current |
| `zmusic` | tag | `1.1.14` | 1.1.14 | behind-project | informational (upstream-carried) |
| `hatarisa` | hash | `6da06056d89b` | behind-project; default branch head 2026-10-24 | behind-project | informational (upstream-carried; ROCKNIX's to take) |
| `portaudio` | hash | `64d1bf913433` | repository 404; the commit is not in PortAudio/portaudio | repo-missing | deferred: #849 (F-13); the hosting choice via #346 |
| `heroic` | no project | `1.0` | metapackage; Heroic is installed by the player | by-hand | n/a |
| `hypseus-singe` | hash | `b353e1728bf5` | behind-project; default branch head 2026-08-30 | behind-project | informational (upstream-carried; ROCKNIX's to take) |
| `mednafen` | tag (a fork's) | `1.32.1` | 1.32.1-chd, the fork's only tag | pin-not-on-project | current |
| `melonds-sa` | hash | `906e9ebb27da` | behind-project; default branch head 2026-10-21 | behind-project | informational (upstream-carried; ROCKNIX's to take) |
| `mupen64plus-sa-audio-sdl` | hash | `cec70e42b453` | behind-project; default branch head 2026-10-20 | behind-project | informational (upstream-carried; ROCKNIX's to take) |
| `mupen64plus-sa-core` | hash | `5340dafcc0f5` | behind-project; default branch head 2026-10-20 | behind-project | informational (upstream-carried; ROCKNIX's to take) |
| `mupen64plus-sa-input-sdl` | hash | `3698a2b12b1d` | behind-project; default branch head 2026-06-23 | behind-project | informational (upstream-carried; ROCKNIX's to take) |
| `mupen64plus-sa-rsp-cxd4` | hash | `f6ff3719cb68` | behind-project; default branch head 2026-06-23 | behind-project | informational (upstream-carried; ROCKNIX's to take) |
| `mupen64plus-sa-rsp-hle` | hash | `9d13986f764b` | behind-project; default branch head 2026-06-23 | behind-project | informational (upstream-carried; ROCKNIX's to take) |
| `mupen64plus-sa-simplecore` | hash | `5340dafcc0f5` | behind-project; default branch head 2024-11-03 | behind-project | informational (upstream-carried; ROCKNIX's to take) |
| `mupen64plus-sa-ui-console` | hash | `1340c4bdfc9e` | behind-project; default branch head 2026-06-23 | behind-project | informational (upstream-carried; ROCKNIX's to take) |
| `mupen64plus-sa-video-glide64mk2` | hash | `992b5942078f` | behind-project; default branch head 2026-06-23 | behind-project | informational (upstream-carried; ROCKNIX's to take) |
| `mupen64plus-sa-video-gliden64` | hash | `85bdd452d709` | behind-project; default branch head 2026-10-11 | behind-project | informational (upstream-carried; ROCKNIX's to take) |
| `mupen64plus-sa-video-rice` | hash | `470865c6c64b` | behind-project; default branch head 2026-09-15 | behind-project | informational (upstream-carried; ROCKNIX's to take) |
| `mupen64plus-sa` | no project | `1.0` | metapackage over its ten sub-recipes | by-hand | n/a |
| `nanoboyadvance-sa` | hash | `3bb6f478f977` | behind-project; default branch head 2026-06-21 | behind-project | informational (upstream-carried; ROCKNIX's to take) |
| `openbor` | hash | `b8303cce992a` | behind-project; default branch head 2026-10-18 | behind-project | informational (upstream-carried; ROCKNIX's to take) |
| `pico-8` | no project | `95cb4d4f28e1` | the player's own binary | by-hand | n/a |
| `ppsspp-sa` | hash | `afbc66a318b8` | behind-project; default branch head 2026-10-24 | behind-project | informational (upstream-carried; ROCKNIX's to take) |
| `rpcs3-sa` | hash | `2f4034590f26` | behind-project; default branch head 2026-10-24 | behind-project | informational (upstream-carried; ROCKNIX's to take) |
| `scummvm-sa` | tag | `2026.1.0` | 2026.1.0 against v2026.4.0 (2026-10-11) | pin-not-on-project | bump proposed (F-27) |
| `skyemu-sa` | hash | `46efbcbdb3b9` | behind-project; default branch head 2026-10-13 | behind-project | informational (upstream-carried; ROCKNIX's to take) |
| `steam` | release .deb | `1.0.0.85` | 1.0.0.85 against 1.0.0.87 in the pool (not the recipe's stable path: approximate) | by-hand | informational; Steam updates itself |
| `supermodel-sa` | hash | `b13fdd5029a2` | the pin is on no default branch | pin-not-on-project | F-28: the pin's branch named in the recipe |
| `touchhle-sa` | hash | `3c5850585ba5` | behind-project; default branch head 2026-10-13 | behind-project | informational (upstream-carried; ROCKNIX's to take) |
| `vice-sa` | tag | `3.8` | 3.8 against 3.10 (SourceForge) | by-hand | bump proposed (F-27) |
| `vita3k-sa` | hash | `ba5c2029c96a` | behind-project; default branch head 2026-10-24 | behind-project | informational (upstream-carried; ROCKNIX's to take) |
| `xemu-sa` | hash | `cbffb57d084c` | behind-project; default branch head 2026-10-22 | behind-project | informational (upstream-carried; ROCKNIX's to take) |
| `yabasanshiro-sa` | hash | `a40dace1ae0a` | the pin is on no default branch (master pushed 2024-12-28) | pin-not-on-project | F-28 |

47 rows: hash 33, tag 5, release 4, moving tarball 2, no project 3. No empty cell.

### Q5 Efficiency

- **Time to play, standalone.** `runemu.sh` start to the emulator's process (G12, n=3 each, synthetic inputs): ppsspp 0.61/0.63/0.63 s, x64sc 0.62/0.67/0.56 s, DuckStation 0.62/0.53/0.52 s. This is not interface to first frame. T3's RetroArch numbers on the same image are interface to first frame 0.62 s and game to game 1.01 s; T1's are in its retro. A first frame needs real content, which is the second guest cycle's job.
- **Before `exec`:**
  - Dolphin runs two Python helpers (0.03-0.05 s each) and some forty `sed -i` passes.
  - DuckStation runs one helper (0.04-0.07 s) and five `sed` passes.
  - gzdoom hashes its 3 MB pk3 twice (0.02 s each).
  - Mupen64Plus copies the whole ROM into tmpfs (F-29: up to 64 MB of RAM, plus the copy's time).
  - DaedalusX64 copies its binary on every launch (F-11's `<>`).
  - amiberry copies its configs on every launch (F-15).
  - Measured: none above 0.07 s on the VM. Mupen64Plus's copy grows with the ROM and was not measured with a real one.
- **Configs:** read once at launch; not measured.

### Q6 Dead ends

#### Q6: the reachability table (35 recipes)

| Recipe | Devices that build it | Start scripts | Per-device config directories | Of those, for a device not shipped | On the guest |
| --- | --- | --- | ---: | ---: | --- |
| `aethersx2-sa` | SM8550 | start_aethersx2.sh | 12 | 10 (RK3399, RK3566, RK3576, RK3588, S922X, SM4450, SM6115, SM8250, SM8650, SM8750) | no: not in GENERIC_X64's arms |
| `amiberry` | GENERIC_X64, H700, SM8550 | start_amiberry.sh | 0 | 0 (-) | no: not built for GENERIC_X64 (PKG_ARCH) |
| `ares-sa` | SM8550 | start_ares.sh | 0 | 0 (-) | no: not in GENERIC_X64's arms |
| `armsx2-sa` | SM8550 | start_armsx2.sh | 1 | 1 (S922X) | no: not in GENERIC_X64's arms |
| `azahar-sa` | SM8550 | start_azahar.sh | 12 | 10 (AMD64, RK3566, RK3576, RK3588, S922X, SM4450, SM6115, SM8250, SM8650, SM8750) | no: not in GENERIC_X64's arms |
| `bigpemu-sa` | SM8550 | start_bigpemu.sh | 1 | 1 (S922X) | no: not in GENERIC_X64's arms |
| `cemu-sa` | SM8550 | start_cemu.sh | 7 | 5 (AMD64, SM4450, SM8250, SM8650, SM8750) | no: not in GENERIC_X64's arms |
| `daedalusx64-sa` | SM8550 | start_daedalusx64.sh | 0 | 0 (-) | no: not in GENERIC_X64's arms |
| `dolphin-sa` | GENERIC_X64, SM8550 | start_dolphin_gc.sh, start_dolphin_wii.sh | 13 | 11 (AMD64, RK3399, RK3566, RK3576, RK3588, S922X, SM4450, SM6115, SM8250, SM8650, SM8750) | yes |
| `drastic-sa` | H700, SM8550 | start_drastic.sh | 12 | 9 (RK3326, RK3399, RK3566, RK3576, RK3588, S922X, SM4450, SM6115, SM8250) | no: not in GENERIC_X64's arms |
| `dsperate-sa` | H700, SM8550 | start_dsperate.sh | 6 | 5 (RK3326, RK3399, RK3566, RK3588, S922X) | no: not in GENERIC_X64's arms |
| `duckstation-sa` | GENERIC_X64, H700, SM8550 | Start Duckstation.sh, start_duckstation.sh | 15 | 12 (AMD64, RK3326, RK3399, RK3566, RK3576, RK3588, S922X, SM4450, SM6115, SM8250, SM8650, SM8750) | yes |
| `flycast-sa` | GENERIC_X64, H700, SM8550 | start_flycast.sh | 15 | 12 (AMD64, RK3326, RK3399, RK3566, RK3576, RK3588, S922X, SM4450, SM6115, SM8250, SM8650, SM8750) | yes |
| `gopher64-sa` | SM8550 | start_gopher64.sh | 0 | 0 (-) | no: not in GENERIC_X64's arms |
| `gzdoom-sa` | GENERIC_X64, H700, SM8550 | start_gzdoom.sh | 0 | 0 (-) | yes |
| `hatarisa` | GENERIC_X64, H700, SM8550 | start_hatari.sh | 0 | 0 (-) | yes |
| `heroic` | SM8550 | start_heroic_authenticate.sh, start_heroic_play.sh, start_heroic_play_gamescope.sh | 0 | 0 (-) | no: not in GENERIC_X64's arms |
| `hypseus-singe` | GENERIC_X64, H700, SM8550 | start_hypseus.sh | 0 | 0 (-) | yes |
| `mednafen` | H700, SM8550 | start_mednafen.sh | 0 | 0 (-) | no: not in GENERIC_X64's arms |
| `melonds-sa` | SM8550 | start_melonds.sh | 13 | 11 (AMD64, RK3399, RK3566, RK3576, RK3588, S922X, SM4450, SM6115, SM8250, SM8650, SM8750) | no: not in GENERIC_X64's arms |
| `mupen64plus-sa` | GENERIC_X64, H700, SM8550 | start_mupen64plus.sh | 15 | 12 (AMD64, RK3326, RK3399, RK3566, RK3576, RK3588, S922X, SM4450, SM6115, SM8250, SM8650, SM8750) | yes |
| `nanoboyadvance-sa` | SM8550 | start_nanoboyadvance.sh | 10 | 8 (AMD64, RK3326, RK3399, RK3588, SM4450, SM8250, SM8650, SM8750) | no: not in GENERIC_X64's arms |
| `openbor` | GENERIC_X64, H700, SM8550 | start_OpenBOR.sh | 0 | 0 (-) | yes |
| `pico-8` | GENERIC_X64, H700, SM8550 | start_pico8.sh | 0 | 0 (-) | yes |
| `ppsspp-sa` | GENERIC_X64, H700, SM8550 | start_ppsspp.sh | 15 | 13 (AMD64, PSP, RK3326, RK3399, RK3566, RK3576, RK3588, S922X, SM4450, SM6115, SM8250, SM8650, SM8750) | yes |
| `rpcs3-sa` | SM8550 | start_rpcs3.sh | 5 | 3 (SM8250, SM8650, SM8750) | no: not in GENERIC_X64's arms |
| `scummvm-sa` | GENERIC_X64, H700, SM8550 | start_scummvm.sh | 0 | 0 (-) | yes |
| `skyemu-sa` | SM8550 | start_skyemu.sh | 0 | 0 (-) | no: not in GENERIC_X64's arms |
| `steam` | SM8550 | start_steam.sh, start_steam_arm64.sh, start_steam_x86.sh | 0 | 0 (-) | no: not in GENERIC_X64's arms |
| `supermodel-sa` | SM8550 | start_supermodel.sh | 8 | 6 (RK3588, SM4450, SM6115, SM8250, SM8650, SM8750) | no: not in GENERIC_X64's arms |
| `touchhle-sa` | GENERIC_X64, H700, SM8550 | start_touchhle.sh | 0 | 0 (-) | yes |
| `vice-sa` | GENERIC_X64, H700, SM8550 | start_vice.sh | 0 | 0 (-) | yes |
| `vita3k-sa` | SM8550 | start_vita3k.sh | 0 | 0 (-) | no: not in GENERIC_X64's arms |
| `xemu-sa` | SM8550 | start_xemu.sh | 7 | 5 (AMD64, SM4450, SM8250, SM8650, SM8750) | no: not in GENERIC_X64's arms |
| `yabasanshiro-sa` | GENERIC_X64, H700, SM8550 | start_yabasanshiro.sh | 0 | 0 (-) | no: not built for GENERIC_X64 (PKG_ARCH) |

Per-file rows where a file's reach differs from its recipe's are the coverage table's Q6 cells (`per-device file for <DEVICE>, a device the fork does not ship`). They are T25's unshipped table, named and not removed (plan § 5). Other dead ends:

- `psp_save_mover.sh` has no caller (F-25).
- `cheevos_duckstation.sh` is not called (F-25).
- Six achievements scripts read the password and never use it (F-25).
- `start_steam_x86.sh` is reached only through `start_steam.sh`'s `steam_version` setting.
- **`aethersx2-sa`:** every row is `deferred: base merge, class 1` (F-26). **Already written:** on SM8550, `/storage/.config/aethersx2/` (configs, and `inis/PCSX2.ini`'s `Token =`, which `backuptool:708` already blanks), `/storage/roms/bios/aethersx2/` (the player's BIOS) and the PS2 save states under `/storage/roms/savestates/ps2`, which ARMSX2 shares. After the deletion nothing launches AetherSX2, and nothing removes those files. The player's data stays where it was, and ARMSX2 (the remaining PS2 emulator) reads the same save-state folder. Nothing is to be migrated; the token in `PCSX2.ini` stays at rest, as for any emulator the player stops using.

### Q7 Clarity and structure

- **The Dolphin pair:** `start_dolphin_gc.sh` and `_wii.sh` share 282 of their unique lines; 128 lines differ. A shared library would hold the common part (F-24).
- **The eight achievements scripts:** one shape, three generations. `cheevos_dolphin.sh`'s publish-whole-file is the model the other seven should share (F-09, F-25).
- **The forty start scripts:** the five steps (seed, link, settings, kill target, run) are written by hand each time. Two helpers would remove F-12 and F-01's class: `link_storage_dir` and a kill target derived from the binary run.
- **DuckStation's nine per-device `settings.ini`** (200-323 lines) are per-device seeds; the fork changed one key in each (#521).
- **Comments against code:** `start_touchhle.sh:71` echoes a variable it never sets (F-25); `start_daedalusx64.sh:44`'s "Always grab the latest daedalus bin" is literally true, every launch, because of F-11.

## Instruction File Recommendations

### Coverage Gaps (would-have-prevented)

- *A kill target names a process the image runs* is a contract in no rule and no test. `tools/emulator-exit-test` drives RetroArch only. The ladder's tool (`05`): every name a start script writes resolves to an executable the image carries, or is a declared run-time name.
- shellcheck's absence leaves SC2071 and SC2086 to readers (F-10, F-11).

### Codification Gaps (needs-new-rule)

- `upgrade-and-install.md`'s "copy, verify, then delete" is written for cloud migrations. A local link step is the same act, and F-12 shows nine scripts that skip it. The rule could say so; the coordinator's call.

### Recommended Action Sequence

Proposals for the coordinator: the exit fixes first (F-01 to F-04, three of them class 1), then F-07 and F-09 (security, accounts), then F-12 and F-11, then the rest.

## Second opinion (Phase 4.6)

**Pending:** the two seats (GPT-6 Astra `max`, Gemini 4 Argon `high`) run next, probes first. This section is filled from their outputs and graded item by item.

## Quality Self-Check

- **Every verdict names its artifact:** a line at the hash, a proof (G1-G13, H1-H5), or a command's output in `00`.
- **Every substitute input is named** (blindspot 65): G1-G12's inputs are synthetic and G6's binaries are renamed copies. No verdict about a real game is drawn from them.
- **What was not checked is said:**
  - five live kills;
  - first frames;
  - the 22 members the guest lacks, beyond reading;
  - `libdrastouch.c`, skimmed only;
  - the Steam launcher's version, read from the pool listing, not the recipe's path.
- **No value from an achievements log or config was printed;** G9 counted synthetic strings.
- **Times are from the clock or from artifacts' mtimes.** Two typed times were corrected (`00`; the friction line of 08:46).


## q4a-dispositions.md (whole)

# Q4a -- upstream's commits on the membership since the base

Generated 2026-10-24 08:49 UTC (`date -u`) from `git log --reverse 8ebaf8daad..upstream/next -- projects/ROCKNIX/packages/emulators/standalone` (`upstream/next` = `e0f9deb899`): 38 commits, all after the read hash (the base `c445081a59` gives the same 38). **Overlap** is each touched file that exists at `8ebaf8daad` and that the fork changed since the base (`git diff --quiet c445081a59 8ebaf8daad -- <file>` false). For a merge commit the files are its first-parent diff. Dispositions: `to merge` (no overlap, or a different hunk -- taken with the base merge, class 1), `conflicts` (the same lines; resolved at the base merge as noted), `superseded` (none: no upstream commit here is already in the fork's tree by other means). Every row is taken by the base merge; none is cherry-picked by this slice (D-WORKFLOW-187: the base merge is the coordinator's).

| Commit | Kind | Files | Overlap with fork changes | Subject | Disposition |
| --- | --- | ---: | --- | --- | --- |
| `0c43a50420` | commit | 20 | `dolphin-sa/scripts/start_dolphin_gc.sh`, `dolphin-sa/scripts/start_dolphin_wii.sh`, `duckstation-sa/scripts/start_duckstation.sh`, `mupen64plus-sa/mupen64plus-sa-core/scripts/start_mupen64plus.sh` | Merge pull request #3377 from sunshineinabox/PR_RotScaling | conflicts: rotation/scaling across the two Dolphin scripts, DuckStation's and Mupen64Plus's, all fork-changed (save paths, #521, the repair block); carries supermodel's array fix (`b6fcd2ca4f`'s base). Resolve hunk by hunk at the base merge. |
| `6679670966` | commit | 2 | `dolphin-sa/package.mk` | Merge pull request #3415 from sunshineinabox/WIP_gcc-glibc | conflicts: read at the base merge |
| `ca67c5f1dd` | commit | 1 | none | dolphin-sa: read wayland events in the nogui loop | to merge (no overlap) |
| `c92afac014` | commit | 1 | none | systemd: restore 255 parity for 261 | to merge (no overlap) |
| `bb9e42e2a0` | commit | 1 | none | rocknix: run games in games.slice with oomd and freeze on suspend | to merge (no overlap) |
| `b6fcd2ca4f` | commit | 1 | none | supermodel-sa: use the screen size for full resolution | to merge (no overlap) |
| `74c46ddbb9` | merge | 2 | none | Merge pull request #3435 from sunshineinabox/WIP_SystemD261 | merge: its content is its parents' rows |
| `32ebcdbf1b` | commit | 1 | none | rocknix: keep Steam alive when one of its processes is OOM-killed | to merge (no overlap) |
| `4a6415c033` | commit | 2 | `duckstation-sa/scripts/start_duckstation.sh` | duckstation-sa: point the quit hotkey at duckstation-qt | to merge, class 1: DuckStation's kill target `duckstation-qt` (this slice's exit sweep, confirmed by the AppImages' listing). The overlap is the fork's `duckstation_screenshot_path` call (#521), a different hunk: merges. |
| `eeb33c5a37` | commit | 1 | `mupen64plus-sa/mupen64plus-sa-core/scripts/start_mupen64plus.sh` | emulators: fix quit hotkey targets for RPCS3, AetherSX2 and mupen64plus | to merge, class 1: the kill targets (`mupen64plus-simple`; `Start RPCS3.sh` and `Start AetherSX2.sh` are T3's files, T3's PL-010). The overlap is the fork's GENERIC_X64 repair block (47-67), a different hunk: merges. |
| `2e7041d273` | commit | 3 | none | hatarisa: rename the start script to match the core name | to merge, class 1: `start_hatari.sh` -> `start_hatarisa.sh` and its kill target; the table's `hatarisa` route needs it. |
| `48b98a02d7` | commit | 5 | none | sm6115: initial Retroid Pocket Duo Lite support | to merge (no overlap) |
| `f610969ba1` | commit | 18 | none | dsperate-sa: bump to v3.0.1, refresh configs + es opts | to merge (no overlap) |
| `bc4db4f0e7` | commit | 1 | none | dsperate-sa: bump to v3.0.2 | to merge (no overlap) |
| `f8844ab04e` | commit | 1 | `armsx2-sa/scripts/cheevos_armsx2.sh` | armsx2-sa: read the testunofficial key like the other launchers | conflicts: upstream adds the `testunofficial` fallback to `cheevos_armsx2.sh`, whose token block the fork rewrote (#170, #308); keep the fork's block and take the one line. |
| `d74fde77e0` | commit | 1 | none | flycast-sa: read the auto frame skipping key ES writes | to merge (no overlap) |
| `2d34256719` | merge | 30 | `duckstation-sa/scripts/start_duckstation.sh`, `mupen64plus-sa/mupen64plus-sa-core/scripts/start_mupen64plus.sh` | Merge pull request #3464 from sunshineinabox/PR_QuitHotkey | to merge: overlap in a different hunk; read at the base merge |
| `195a8eba4b` | commit | 3 | `mupen64plus-sa/mupen64plus-sa-core/scripts/start_mupen64plus.sh` | mupen64plus-sa: fix zipped ROMs and DualSense controls | to merge, class 1: `unzip -Zl` -> `unzip -qql` (zipped N64 ROMs under busybox). Overlap: the fork's repair block, a different hunk. |
| `99870f0449` | commit | 8 | none | azahar-sa: async_shader_compilation feature | to merge (no overlap) |
| `5675ab7b28` | commit | 8 | none | azahar-sa: bump to v2126.2 | to merge (no overlap) |
| `e0bf3a55b0` | commit | 1 | none | azahar-sa: SM4450: symlink to InputPlumber config | to merge (no overlap) |
| `115a89be2b` | merge | 18 | `armsx2-sa/scripts/cheevos_armsx2.sh`, `duckstation-sa/scripts/start_duckstation.sh`, `mupen64plus-sa/mupen64plus-sa-core/scripts/start_mupen64plus.sh` | Merge pull request #3468 from qzydustin/setting-keys | to merge: overlap in a different hunk; read at the base merge |
| `7af4b5bcf3` | merge | 11 | `armsx2-sa/scripts/cheevos_armsx2.sh` | Merge pull request #3478 from porschemad911/azahar-v2126.2 | to merge: overlap in a different hunk; read at the base merge |
| `6103571f67` | commit | 1 | none | Merge pull request #3470 from sunshineinabox/WIP_core-updates | to merge (no overlap) |
| `a1ea79474b` | commit | 20 | `duckstation-sa/config/RK3566`, `duckstation-sa/config/RK3566/settings.ini` | rk3566: port to inputplumber | conflicts: RK3566's InputPlumber port touches `duckstation-sa/config/RK3566/settings.ini`, a fork-own file (#521's screenshot key). RK3566 is not a shipped device (D-WORKFLOW-185): take upstream's and re-apply the one key. |
| `2e85dcde25` | commit | 1 | none | melonds-sa: fix broken launch script (libmali) | to merge (no overlap) |
| `8c8800dc01` | commit | 1 | none | sm4450: add Retroid Pocket Classic 6 Rev Q | to merge (no overlap) |
| `ac844389f4` | commit | 1 | none | dsperate-sa: bump to v3.0.4 | to merge (no overlap) |
| `693632077e` | merge | 2 | none | Merge pull request #3498 from Jacob-Matthew-Cook/sm4450-rpclassic-sgb | merge: its content is its parents' rows |
| `075a7c303b` | commit | 2 | `dolphin-sa/package.mk` | Merge pull request #3513 from sunshineinabox/WIP_multimedia | conflicts: read at the base merge |
| `38cc9c7e7d` | commit | 3 | none | rk3566: fix some inputplumber issues | to merge (no overlap) |
| `c4d353449e` | commit | 17 | `aethersx2-sa/package.mk` | aethersx2: drop package due to licensing concern | to merge, class 1: deletes `aethersx2-sa` (licensing). The fork's 4 commits on the recipe (`PKG_ARCH`) go with it; `Already written:` in `04` § Q6. |
| `09ce29c548` | merge | 20 | `aethersx2-sa/package.mk` | Merge pull request #3534 from sunshineinabox/PR_ASX2 | merge of `c4d353449e`'s branch: as `c4d353449e`. |
| `abcb61ec9b` | commit | 1 | none | armsx2-sa: add patch to fix Vulkan backend on mali | to merge (no overlap) |
| `d91679afb8` | commit | 1 | none | dsperate-sa: bump to v3.0.5 | to merge (no overlap) |
| `62da3f7e23` | commit | 1 | none | dsperate-sa: S922X: use 'renderer' sink | to merge (no overlap) |
| `861c9ce4ea` | commit | 3 | none | ppsspp: change menu button combo | to merge (no overlap) |
| `3df05945a7` | commit | 5 | none | ppsspp-sa: remove the guide and misc swap patch | to merge (no overlap) |

38 rows: 33 to merge, 5 conflicts, 0 superseded.

## The thirteen fork-own recipes against upstream's

| Recipe | Fork's pin | Upstream's pin | Pin | What the fork changed (none of it the pin) |
| --- | --- | --- | --- | --- |
| `aethersx2-sa` | `1.5-3606` | (absent upstream) | differs | `PKG_ARCH=aarch64` (audit #258 PL-010); upstream deletes the recipe |
| `amiberry` | `5c54536997c0` | `5c54536997c0` | same | not built for GENERIC_X64 |
| `bigpemu-sa` | `v119` | `v119` | same | `PKG_ARCH=aarch64` |
| `daedalusx64-sa` | `f17e9ed86f38` | `f17e9ed86f38` | same | `DISTRONAME` for `DISTRO` in the arm root path |
| `dolphin-sa` | `6094cfcf7b8f` | `6094cfcf7b8f` | same | Python3 dep (dolphin-save-paths), GENERIC_X64 GL backend, the `sys` link, patch 018's note |
| `drastic-sa` | `1.0` | `1.0` | same | `PKG_ARCH=aarch64` |
| `duckstation-sa` | `0.1-10998` | `0.1-10998` | same | Python3/libcom-err deps; `install -m 0755` |
| `mupen64plus-sa-audio-sdl` | `cec70e42b453` | `cec70e42b453` | same | speexdsp dependency |
| `mupen64plus-sa-video-gliden64` | `85bdd452d709` | `85bdd452d709` | same | GENERIC_X64 arms, `-DNOHQ=On` |
| `openbor` | `b8303cce992a` | `b8303cce992a` | same | `PKG_LICENSE` (#528) |
| `ppsspp-sa` | `afbc66a318b8` | `afbc66a318b8` | same | per-device sources guarded |
| `steam` | `1.0.0.85` | `1.0.0.85` | same | Python3 dependency |
| `yabasanshiro-sa` | `a40dace1ae0a` | `a40dace1ae0a` | same | not built for GENERIC_X64 |

No fork-own recipe's pin differs from upstream's except `aethersx2-sa`'s, which upstream no longer has. The one `behind-upstream` pin in the membership is `azahar-sa` (upstream-carried: `fbd3fb02f7` against upstream's `219d743a1e`, v2126.2 by `5675ab7b28`), taken with the base merge. `dsperate-sa` differs too (2.0.1 against upstream's 3.0.5, four bumps); the scan classes it by its tag shape.

## The code, in full, at `8ebaf8daad` (line-numbered)

### `projects/ROCKNIX/packages/emulators/standalone/aethersx2-sa/scripts/cheevos_aethersx2.sh`

```
1	#! /bin/bash
2	
3	# SPDX-License-Identifier: GPL-2.0-or-later
4	# Copyright (C) 2022-present Hector Calvarro (https://github.com/kelvfimer)
5	# Copyright (C) 2024-present ROCKNIX (https://github.com/ROCKNIX)
6	
7	. /etc/profile
8	
9	AETHERSX2_CFG="/storage/.config/aethersx2/inis/PCSX2.ini"
10	LOG_FILE="/var/log/cheevos.log"
11	
12	# Extract username, password, token, if enabled, and hardcore mode from system.cfg
13	username=$(get_setting "global.retroachievements.username")
14	password=$(get_setting "global.retroachievements.password")
15	token=$(get_setting "global.retroachievements.token")
16	enabled=$(get_setting "global.retroachievements")
17	hardcore="false"
18	
19	# Check if RetroAchievements are enabled in Emulation Station
20	if [ ! ${enabled} = 1 ]; then
21	    echo "RetroAchievements are not enabled, please turn them on in Emulation Station." > ${LOG_FILE}
22	    sed -i '/\[Achievements\]/,/^\s*$/s/Enabled =.*/Enabled = false/' ${AETHERSX2_CFG}
23	    exit 1
24	fi
25	
26	# Check if api token is present in system.cfg
27	if [ -z "${token}" ]; then
28	    echo "RetroAchievements token is empty, please log in with your RetroAchievements credentials in Emulation Station." > ${LOG_FILE}
29	    exit 1
30	fi
31	
32	# Update emulator config with RetroAchievements settings
33	zcheevos=$(grep -Fx "[Achievements]" ${AETHERSX2_CFG})
34	datets=$(date +%s%N | cut -b1-13)
35	
36	if [ -z "${zcheevos}" ]; then
37	    sed -i "\$a [Achievements]\nEnabled = true\nUsername = ${username}\nToken = ${token}\nChallengeMode = ${hardcore}\nLoginTimestamp = ${datets}" ${AETHERSX2_CFG}
38	else
39	    sed -i '/\[Achievements\]/,/^\s*$/s/Enabled =.*/Enabled = true/' ${AETHERSX2_CFG}
40	
41	    if ! grep -q "^Username = " ${AETHERSX2_CFG}; then
42	        sed -i "/^\[Achievements\]/a Username = ${username}" ${AETHERSX2_CFG}
43	    else
44	        sed -i "/^\[Achievements\]/,/^\[/{s/^Username = .*/Username = ${username}/;}" ${AETHERSX2_CFG}
45	    fi
46	
47	    if ! grep -q "^Token = " ${AETHERSX2_CFG}; then
48	        sed -i "/^\[Achievements\]/a Token = ${token}" ${AETHERSX2_CFG}
49	    else
50	        sed -i "/^\[Achievements\]/,/^\[/{s/^Token = .*/Token = ${token}/;}" ${AETHERSX2_CFG}
51	    fi
52	
53	    if ! grep -q "^ChallengeMode = " ${AETHERSX2_CFG}; then
54	        sed -i "/^\[Achievements\]/a ChallengeMode = ${hardcore}" ${AETHERSX2_CFG}
55	    else
56	        sed -i "/^\[Achievements\]/,/^\[/{s/^ChallengeMode = .*/ChallengeMode = ${hardcore}/;}" ${AETHERSX2_CFG}
57	    fi
58	
59	    sed -i "/^\[Achievements\]/,/^\[/{s/^LoginTimestamp = .*/LoginTimestamp = ${datets}/;}" ${AETHERSX2_CFG}
60	fi
```

### `projects/ROCKNIX/packages/emulators/standalone/aethersx2-sa/scripts/start_aethersx2.sh`

```
1	#!/bin/bash
2	
3	# SPDX-License-Identifier: GPL-2.0-or-later
4	# Copyright (C) 2022-present JELOS (https://github.com/JustEnoughLinuxOS)
5	
6	. /etc/profile
7	
8	#Check if aethersx2 exists in .config
9	if [ ! -d "/storage/.config/aethersx2" ]; then
10	    mkdir -p "/storage/.config/aethersx2"
11	        cp -r "/usr/config/aethersx2" "/storage/.config/"
12	fi
13	
14	#Make Aethersx2 bios folder
15	if [ ! -d "/storage/roms/bios/aethersx2" ]; then
16	    mkdir -p "/storage/roms/bios/aethersx2"
17	fi
18	
19	#Create PS2 savestates folder
20	if [ ! -d "/storage/roms/savestates/ps2" ]; then
21	    mkdir -p "/storage/roms/savestates/ps2"
22	fi
23	
24	#Emulation Station Features
25	GAME=$(echo "${1}"| sed "s#^/.*/##")
26	PLATFORM=$(echo "${2}"| sed "s#^/.*/##")
27	ASPECT=$(get_setting aspect_ratio "${PLATFORM}" "${GAME}")
28	FILTER=$(get_setting bilinear_filtering "${PLATFORM}" "${GAME}")
29	FPS=$(get_setting show_fps "${PLATFORM}" "${GAME}")
30	RATE=$(get_setting ee_cycle_rate "${PLATFORM}" "${GAME}")
31	SKIP=$(get_setting ee_cycle_skip "${PLATFORM}" "${GAME}")
32	HWDOWNLOAD=$(get_setting hw_download_mode "${PLATFORM}" "${GAME}")
33	GRENDERER=$(get_setting graphics_backend "${PLATFORM}" "${GAME}")
34	IRES=$(get_setting internal_resolution "${PLATFORM}" "${GAME}")
35	VSYNC=$(get_setting vsync "${PLATFORM}" "${GAME}")
36	ENABLE_WIDESCREEN_PATCHES=$(get_setting enable_widescreen_patches "${PLATFORM}" "${GAME}")
37	
38	#Set the cores to use
39	CORES=$(get_setting "cores" "${PLATFORM}" "${GAME}")
40	if [ "${CORES}" = "little" ]
41	then
42	  EMUPERF="${SLOW_CORES}"
43	elif [ "${CORES}" = "big" ]
44	then
45	  EMUPERF="${FAST_CORES}"
46	else
47	  #All..
48	  unset EMUPERF
49	fi
50	
51	  #Aspect Ratio
52		if [ "$ASPECT" = "0" ]
53		then
54	  		sed -i '/^AspectRatio =/c\AspectRatio = 4:3' /storage/.config/aethersx2/inis/PCSX2.ini
55		fi
56		if [ "$ASPECT" = "1" ]
57		then
58	  		sed -i '/^AspectRatio =/c\AspectRatio = 16:9' /storage/.config/aethersx2/inis/PCSX2.ini
59		fi
60		if [ "$ASPECT" = "2" ]
61		then
62	  		sed -i '/^AspectRatio =/c\AspectRatio = Stretch' /storage/.config/aethersx2/inis/PCSX2.ini
63		fi
64	
65	  #Bilinear Filtering
66	        if [ "$FILTER" = "0" ]
67	        then
68	                sed -i '/^filter =/c\filter = 0' /storage/.config/aethersx2/inis/PCSX2.ini
69	        fi
70	        if [ "$FILTER" = "1" ]
71	        then
72	                sed -i '/^filter =/c\filter = 1' /storage/.config/aethersx2/inis/PCSX2.ini
73	        fi
74	        if [ "$FILTER" = "2" ]
75	        then
76	                sed -i '/^filter =/c\filter = 2' /storage/.config/aethersx2/inis/PCSX2.ini
77	        fi
78	        if [ "$FILTER" = "3" ]
79	        then
80	                sed -i '/^filter =/c\filter = 3' /storage/.config/aethersx2/inis/PCSX2.ini
81	        fi
82	
83	  #Graphics Backend
84		if [ "$GRENDERER" = "0" ]
85		then
86	  		sed -i '/^Renderer =/c\Renderer = -1' /storage/.config/aethersx2/inis/PCSX2.ini
87		fi
88		if [ "$GRENDERER" = "1" ]
89		then
90	  		sed -i '/^Renderer =/c\Renderer = 12' /storage/.config/aethersx2/inis/PCSX2.ini
91		fi
92		if [ "$GRENDERER" = "2" ]
93		then
94	  		sed -i '/^Renderer =/c\Renderer = 14' /storage/.config/aethersx2/inis/PCSX2.ini
95		fi
96	        if [ "$GRENDERER" = "3" ]
97	        then
98	                sed -i '/^Renderer =/c\Renderer = 13' /storage/.config/aethersx2/inis/PCSX2.ini
99	        fi
100	
101	  #Internal Resolution
102	        if [ "$IRES" > "0" ]
103	        then
104	                sed -i "/^upscale_multiplier =/c\upscale_multiplier = $IRES" /storage/.config/aethersx2/inis/PCSX2.ini
105	        else
106	                sed -i '/^upscale_multiplier =/c\upscale_multiplier = 1' /storage/.config/aethersx2/inis/PCSX2.ini
107	        fi
108	
109	  #Show FPS
110		if [ "$FPS" = "false" ]
111		then
112	  		sed -i '/^OsdShowFPS =/c\OsdShowFPS = false' /storage/.config/aethersx2/inis/PCSX2.ini
113		fi
114		if [ "$FPS" = "true" ]
115		then
116	  		sed -i '/^OsdShowFPS =/c\OsdShowFPS = true' /storage/.config/aethersx2/inis/PCSX2.ini
117		fi
118	
119	  #EE Cycle Rate
120	        sed -i '/^EECycleRate =/c\EECycleRate = 0' /storage/.config/aethersx2/inis/PCSX2.ini
121	        if [ "$RATE" = "0" ]
122	        then
123	                sed -i '/^EECycleRate =/c\EECycleRate = -3' /storage/.config/aethersx2/inis/PCSX2.ini
124	        fi
125	        if [ "$RATE" = "1" ]
126	        then
127	                sed -i '/^EECycleRate =/c\EECycleRate = -2' /storage/.config/aethersx2/inis/PCSX2.ini
128	        fi
129	        if [ "$RATE" = "2" ]
130	        then
131	                sed -i '/^EECycleRate =/c\EECycleRate = -1' /storage/.config/aethersx2/inis/PCSX2.ini
132	        fi
133	        if [ "$RATE" = "3" ]
134	        then
135	                sed -i '/^EECycleRate =/c\EECycleRate = 0' /storage/.config/aethersx2/inis/PCSX2.ini
136	        fi
137	        if [ "$RATE" = "4" ]
138	        then
139	                sed -i '/^EECycleRate =/c\EECycleRate = 1' /storage/.config/aethersx2/inis/PCSX2.ini
140	        fi
141	        if [ "$RATE" = "5" ]
142	        then
143	                sed -i '/^EECycleRate =/c\EECycleRate = 2' /storage/.config/aethersx2/inis/PCSX2.ini
144	        fi
145	        if [ "$RATE" = "6" ]
146	        then
147	                sed -i '/^EECycleRate =/c\EECycleRate = 3' /storage/.config/aethersx2/inis/PCSX2.ini
148	        fi
149	
150	  #EE Cycle Skip
151	        sed -i '/^EECycleSkip =/c\EECycleSkip = 0' /storage/.config/aethersx2/inis/PCSX2.ini
152	        if [ "$SKIP" = "0" ]
153	        then
154	                sed -i '/^EECycleSkip =/c\EECycleSkip = 0' /storage/.config/aethersx2/inis/PCSX2.ini
155	        fi
156	        if [ "$SKIP" = "1" ]
157	        then
158	                sed -i '/^EECycleSkip =/c\EECycleSkip = 1' /storage/.config/aethersx2/inis/PCSX2.ini
159	        fi
160	        if [ "$SKIP" = "2" ]
161	        then
162	                sed -i '/^EECycleSkip =/c\EECycleSkip = 2' /storage/.config/aethersx2/inis/PCSX2.ini
163	        fi
164	        if [ "$SKIP" = "3" ]
165	        then
166	                sed -i '/^EECycleSkip =/c\EECycleSkip = 3' /storage/.config/aethersx2/inis/PCSX2.ini
167	        fi
168	
169	#HW download mode
170	        sed -i '/^HWDownloadMode =/c\HWDownloadMode = 0' /storage/.config/aethersx2/inis/PCSX2.ini
171	        if [ "$HWDOWNLOAD" = "0" ]
172	        then
173	                sed -i '/^HWDownloadMode =/c\HWDownloadMode = 0' /storage/.config/aethersx2/inis/PCSX2.ini
174	        fi
175	        if [ "$HWDOWNLOAD" = "1" ]
176	        then
177	                sed -i '/^HWDownloadMode =/c\HWDownloadMode = 1' /storage/.config/aethersx2/inis/PCSX2.ini
178	        fi
179	        if [ "$HWDOWNLOAD" = "2" ]
180	        then
181	                sed -i '/^HWDownloadMode =/c\HWDownloadMode = 2' /storage/.config/aethersx2/inis/PCSX2.ini
182	        fi
183	        if [ "$HWDOWNLOAD" = "3" ]
184	        then
185	                sed -i '/^HWDownloadMode =/c\HWDownloadMode = 3' /storage/.config/aethersx2/inis/PCSX2.ini
186	        fi
187	
188	#Widescreen patches
189		if [ "$ENABLE_WIDESCREEN_PATCHES" = "true" ]
190		then
191	  		sed -i '/^EnableWideScreenPatches =/c\EnableWideScreenPatches = true' /storage/.config/aethersx2/inis/PCSX2.ini
192	        else
193	                sed -i '/^EnableWideScreenPatches =/c\EnableWideScreenPatches = false' /storage/.config/aethersx2/inis/PCSX2.ini
194	        fi
195	
196	#Retroachievements
197	  /usr/bin/cheevos_aethersx2.sh
198	
199	#Graphic driver fixes
200	@GRAPHICS@
201	
202	#Set QT enviornment to wayland
203	  export QT_QPA_PLATFORM=wayland
204	
205	# Extra Libs needed to run
206	  export LD_LIBRARY_PATH=/usr/share/aethersx2-sa/libs
207	
208	#Run Aethersx2 emulator
209	  export SDL_AUDIODRIVER=pulseaudio
210	  set_kill set "-9 aethersx2"
211	  ${EMUPERF} /usr/share/aethersx2-sa/aethersx2 -bigpicture -fullscreen "${1}"
```

### `projects/ROCKNIX/packages/emulators/standalone/amiberry/package.mk`

```
1	# SPDX-License-Identifier: GPL-2.0
2	# Copyright (C) 2024-present ROCKNIX (https://github.com/ROCKNIX)
3	
4	PKG_NAME="amiberry"
5	PKG_VERSION="5c54536997c0039aaa72bb0552cefdc3c967ad8d"
6	PKG_LICENSE="GPL-3.0-or-later"
7	PKG_SITE="https://github.com/midwan/amiberry"
8	PKG_URL="${PKG_SITE}.git"
9	PKG_DEPENDS_TARGET="toolchain linux glibc bzip2 zlib SDL2 SDL2_image SDL2_ttf capsimg freetype libxml2 flac libogg mpg123 libpng libmpeg2 libserialport"
10	PKG_LONGDESC="Amiberry is an optimized Amiga emulator for ARM-based boards."
11	# Not built for GENERIC_X64, the fork's QA device: PKG_EMUS lists amiberry
12	# for every device and its Makefile's platform block is written for ARM
13	# boards. Every other device, AMD64 included, builds it as upstream does
14	# since its cleanup (28e750db32) dropped the aarch64-only restriction.
15	if [ "${DEVICE}" = "GENERIC_X64" ]; then
16	  PKG_ARCH="aarch64"
17	fi
18	PKG_TOOLCHAIN="make"
19	
20	if [ ! "${OPENGL}" = "no" ]; then
21	  PKG_PATCH_DIRS+=" opengl"
22	fi
23	
24	PKG_MAKE_OPTS_TARGET+=" PLATFORM=${DEVICE} all SDL_CONFIG=${SYSROOT_PREFIX}/usr/bin/sdl2-config"
25	
26	post_unpack() {
27	  sed -i "s|AS     = as|AS     \?= as|" ${PKG_BUILD}/Makefile
28	}
29	
30	pre_configure_target() {
31	  export LDFLAGS="${LDFLAGS} -logg"
32	  cd ${PKG_BUILD}
33	}
34	
35	makeinstall_target() {
36	  mkdir -p ${INSTALL}/usr/bin
37	    cp -a amiberry* ${INSTALL}/usr/bin/amiberry
38	    cp -a ${PKG_DIR}/scripts/* ${INSTALL}/usr/bin
39	
40	  mkdir -p ${INSTALL}/usr/config/amiberry
41	    cp -a ${PKG_DIR}/config/* ${INSTALL}/usr/config/amiberry
42	    cp -a {data,savestates,screenshots,whdboot} ${INSTALL}/usr/config/amiberry
43	    ln -s /storage/roms/bios ${INSTALL}/usr/config/amiberry/kickstarts
44	    ln -s /usr/share/libretro/autoconfig ${INSTALL}/usr/config/amiberry/controller
45	    ln -sf /usr/lib/libcapsimage.so.5.1 ${INSTALL}/usr/config/amiberry/capsimg.so
46	}
```

### `projects/ROCKNIX/packages/emulators/standalone/amiberry/scripts/start_amiberry.sh`

```
1	#!/bin/sh
2	# SPDX-License-Identifier: GPL-2.0-or-later
3	# Copyright (C) 0riginally created by Escalade (https://github.com/escalade)
4	# Copyright (C) 2018-present 5schatten (https://github.com/5schatten)
5	# Copyright (C) 2023 JELOS (https://github.com/JustEnoughLinuxOS)
6	
7	. /etc/profile
8	
9	set_kill set "-9 amiberry"
10	
11	# Set some common variables
12	AMIBERRY_DIR="/storage/.config/amiberry"
13	AMIBERRY_CONFIG_DIR="${AMIBERRY_DIR}/conf"
14	AMIBERRY_TMP_DIR="/tmp/emulation/amiberry"
15	AMIBERRY_TMP_CONFIG="${AMIBERRY_TMP_DIR}/.amiberry_conf.uae"
16	AMIBERRY_LOG="/var/log/amiberry.log"
17	BIOS_PATH="/storage/roms/bios"
18	MAX_DRIVES=4
19	i=0
20	
21	echo "Amiberry Log" > "${AMIBERRY_LOG}"
22	
23	if [ ! -d "${AMIBERRY_TMP_DIR}" ]
24	then
25	  mkdir -p "${AMIBERRY_TMP_DIR}"
26	fi
27	
28	if [ ! -d "${AMIBERRY_DIR}" ]
29	then
30	  cp -rf /usr/config/amiberry ${AMIBERRY_DIR}
31	fi
32	
33	### Refresh the configs so we can manage them.
34	cp -f /usr/config/amiberry/conf/* ${AMIBERRY_DIR}/conf
35	
36	find_gamepad() {
37	  # Check for js0 first, else fall back to joypad
38	  if grep -q "js0" /proc/bus/input/devices; then
39	    GAMEPAD=$(grep -b4 js0 /proc/bus/input/devices | awk 'BEGIN {FS="\""}; /Name/ {printf $2}')
40	  else
41	    GAMEPAD=$(grep -b4 joypad /proc/bus/input/devices | awk 'BEGIN {FS="\""}; /Name/ {printf $2}')
42	  fi
43	  sed -i "s|joyport1_friendlyname=.*|joyport1_friendlyname=${GAMEPAD}|" "${AMIBERRY_TMP_CONFIG}"
44	  echo "Gamepad used ${GAMEPAD}" >> "${AMIBERRY_LOG}"
45	}
46	
47	# Which file should amiberry load?
48	echo "Trying to boot this game:" "$1" >> ${AMIBERRY_LOG}
49	
50	# Change working directory cause amiberry loads assets from there
51	cd ${AMIBERRY_DIR}
52	
53	# Create a clean working directory
54	if [ -d "${AMIBERRY_TMP_DIR}" ]; then
55	  echo "Clean up old working directory." >> ${AMIBERRY_LOG}
56	  rm -rf "${AMIBERRY_TMP_DIR}"
57	fi
58	mkdir -p "${AMIBERRY_TMP_DIR}"
59	
60	# Check if the file is an Amiga 1200/CD32 game and set configuration options for an Amiga 1200
61	AMIBERRY_SET_CONF() {
62	  if [ `echo $1 | grep -E 'AGA|CD32' | wc -l` -eq 1 -o `echo "${AMIBERRY_TMP_DIR}"/* | grep -e 'AGA|CD32' | wc -l` -eq 1 ]; then
63	    echo "Loading Amiga 1200/CD32 config." >> ${AMIBERRY_LOG}
64	    cp ${AMIBERRY_CONFIG_DIR}/AmigaA1200-default.uae "${AMIBERRY_TMP_CONFIG}"
65	  else
66	    echo "Loading Amiga 500 config." >> ${AMIBERRY_LOG}
67	    cp ${AMIBERRY_CONFIG_DIR}/AmigaA500-default.uae "${AMIBERRY_TMP_CONFIG}"
68	  fi
69	  sed -i "s#@BIOS_PATH@#${BIOS_PATH}#g" ${AMIBERRY_TMP_CONFIG}
70	  sed -i "s#gfx_width=.*\$#$(fbwidth)#g" ${AMIBERRY_TMP_CONFIG}
71	  sed -i "s#gfx_height=.*\$#$(fbheight)#g" ${AMIBERRY_TMP_CONFIG}
72	  find_gamepad 
73	}
74	
75	# Check if we are loading a .zip file
76	if [ `echo $1 | grep -i .zip | wc -l` -eq 1 ]; then
77	  
78	  # Unpack the zip file
79	  unzip -q -o "$1" -d "${AMIBERRY_TMP_DIR}"
80	  
81	  if [ -f "${AMIBERRY_TMP_DIR}"/*.*nfo ] && [ -f "${AMIBERRY_TMP_DIR}"/*/*.*lave ]; then
82	
83	    # WHDLoad file detected
84	    echo "Loading a WHDLoad (.zip) file..." >> ${AMIBERRY_LOG}
85	
86	    # Set default config
87	    AMIBERRY_SET_CONF "$1"
88	
89	    # Add amiberry.uae conf & start amiberry with WHDLoad
90	    amiberry -f "${AMIBERRY_TMP_CONFIG}" --autoload "$1" >> ${AMIBERRY_LOG} 2>&1
91	
92	  else
93	    # .zip file detected
94	    echo "Loading a .zip file..." >> ${AMIBERRY_LOG}
95	
96	    # Set default config
97	    AMIBERRY_SET_CONF "$1"
98	  
99	    # Assign files to floppy0-3
100	    for FILE in "${AMIBERRY_TMP_DIR}"/*
101	    do
102	      ARGS="${ARGS}\nfloppy$i="${FILE}""
103	      i=$(($i+1))
104	      # This emulator supports 4 floppies max
105	      if [ $i -eq ${MAX_DRIVES} ]; then
106	        break;
107	      fi
108	    done
109	  
110	    # Add game files as floppies 0-3 to amiberry.uae & start amiberry
111	    echo -e ";" >> "${AMIBERRY_TMP_CONFIG}"
112	    echo -e "; *** temporary added Floppy Drives" >> "${AMIBERRY_TMP_CONFIG}"
113	    echo -e ";" >> "${AMIBERRY_TMP_CONFIG}"
114	    echo -e ${ARGS} >> "${AMIBERRY_TMP_CONFIG}"
115	    echo -e "\nAssigned floppy drives:" ${ARGS} "\n" >> "${AMIBERRY_LOG}"
116	    amiberry -f "${AMIBERRY_TMP_CONFIG}" >> ${AMIBERRY_LOG} 2>&1
117	  fi
118	
119	# Check for WHDload files (.lha)
120	elif [ `echo $1 | grep -i .lha | wc -l` -eq 1 ]; then
121	    
122	  #.lha file detected
123	  echo "Loading a WHDLoad (.lha) file..." >> ${AMIBERRY_LOG}
124	
125	  # Set default config
126	  AMIBERRY_SET_CONF "$1"
127	
128	  # Add amiberry.uae conf & start amiberry with WHDLoad
129	  amiberry -f "${AMIBERRY_TMP_CONFIG}" --autoload "$1" >> ${AMIBERRY_LOG} 2>&1
130	
131	# Check for .uae config file
132	elif [ `echo $1 | grep -i .uae | wc -l` -eq 1 ]; then
133	
134	  # .uae file detected
135	  echo "Loading an .uae file..." >> ${AMIBERRY_LOG}
136	
137	  # Load .uae config file
138	  amiberry -f "$1" >> ${AMIBERRY_LOG} 2>&1
139	
140	# All other files (.adf .adz .ipf)
141	else
142	
143	  #.adf or .adz or .ipf file detected
144	  echo "Loading a single .adf or .adz or .ipf file..." >> ${AMIBERRY_LOG}
145	
146	  # Set default config
147	  AMIBERRY_SET_CONF "$1"
148	
149	  # Add game file as floppy0 to amiberry.uae & start amiberry
150	  echo -e ";" >> "${AMIBERRY_TMP_CONFIG}"
151	  echo -e "; *** temporary added Floppy Drives" >> "${AMIBERRY_TMP_CONFIG}"
152	  echo -e ";" >> "${AMIBERRY_TMP_CONFIG}"
153	  echo -e "\nfloppy0=$1" >> "${AMIBERRY_TMP_CONFIG}"
154	  echo -e "\nAssigned floppy drive:\nfloppy0=$1\n" >> "${AMIBERRY_LOG}"
155	  amiberry -f "${AMIBERRY_TMP_CONFIG}" >> ${AMIBERRY_LOG} 2>&1
156	fi
157	
158	# Remove temporary dir
159	rm -rf "${AMIBERRY_TMP_DIR}"
```

### `projects/ROCKNIX/packages/emulators/standalone/ares-sa/scripts/start_ares.sh`

```
1	#!/bin/bash
2	
3	# SPDX-License-Identifier: GPL-2.0-or-later
4	# Copyright (C) 2026-present ROCKNIX (https://github.com/ROCKNIX)
5	
6	. /etc/profile
7	
8	set_kill set "-9 ares"
9	
10	CONF_DIR="/storage/.config/ares"
11	ARES_INI="settings.bml"
12	
13	# Check if ares exists in .config
14	if [ ! -d "${CONF_DIR}" ]; then
15	  cp -r "/usr/config/ares" "/storage/.config/"
16	fi
17	
18	# Check if settings.bml exists in .config/ares/
19	if [ ! -f "${CONF_DIR}/${ARES_INI}" ]; then
20	  cp -r "/usr/config/ares/${ARES_INI}" "${CONF_DIR}/"
21	fi
22	
23	# Link  .config/ares to .local
24	rm -rf /storage/.local/share/ares
25	ln -sf /storage/.config/ares /storage/.local/share/ares
26	
27	# Emulation Station Features
28	GAME=$(echo "${1}"| sed "s#^/.*/##")
29	PLATFORM=$(echo "${2}"| sed "s#^/.*/##")
30	
31	# Set the cores to use
32	CORES=$(get_setting "cores" "${PLATFORM}" "${GAME}")
33	if [ "${CORES}" = "little" ]
34	then
35	  EMUPERF="${SLOW_CORES}"
36	elif [ "${CORES}" = "big" ]
37	then
38	  EMUPERF="${FAST_CORES}"
39	else
40	  ### All..
41	  unset EMUPERF
42	fi
43	
44	${EMUPERF} /usr/bin/ares --fullscreen "${1}"
```

### `projects/ROCKNIX/packages/emulators/standalone/armsx2-sa/scripts/cheevos_armsx2.sh`

```
1	#! /bin/bash
2	
3	# SPDX-License-Identifier: GPL-2.0-or-later
4	# Copyright (C) 2026-present ROCKNIX (https://github.com/ROCKNIX)
5	
6	. /etc/profile
7	
8	ARMSX2_CFG="/storage/.config/ARMSX2/inis/PCSX2.ini"
9	ARMSX2_TOKEN="/storage/.config/ARMSX2/inis/secrets.ini"
10	LOG_FILE="/var/log/cheevos.log"
11	
12	# Extract username, password, token, if enabled, and hardcore mode from system.cfg
13	username=$(get_setting "global.retroachievements.username")
14	password=$(get_setting "global.retroachievements.password")
15	token=$(get_setting "global.retroachievements.token")
16	enabled=$(get_setting "global.retroachievements")
17	hardcore=$(get_setting "global.retroachievements.hardcore")
18	encore=$(get_setting "global.retroachievements.encore")
19	leaderboards=$(get_setting "global.retroachievements.leaderboards")
20	unofficial=$(get_setting "global.retroachievements.unofficial")
21	
22	# Convert values from 0/1 to true/false
23	to_bool() { [ "${1}" = "1" ] && echo "true" || echo "false"; }
24	hardcore=$(to_bool "${hardcore}")
25	encore=$(to_bool "${encore}")
26	leaderboards=$(to_bool "${leaderboards}")
27	unofficial=$(to_bool "${unofficial}")
28	
29	# Check if RetroAchievements are enabled in Emulation Station
30	if [ ! ${enabled} = 1 ]; then
31	    echo "RetroAchievements are not enabled, please turn them on in Emulation Station." > ${LOG_FILE}
32	    sed -i '/\[Achievements\]/,/^\s*$/s/Enabled =.*/Enabled = false/' ${ARMSX2_CFG}
33	    exit 1
34	fi
35	
36	# Check if api token is present in system.cfg
37	if [ -z "${token}" ]; then
38	    echo "RetroAchievements token is empty, please log in with your RetroAchievements credentials in Emulation Station." > ${LOG_FILE}
39	    exit 1
40	fi
41	
42	# Update emulator config with RetroAchievements settings
43	zcheevos=$(grep -Fx "[Achievements]" ${ARMSX2_CFG})
44	datets=$(date +%s%N | cut -b1-13)
45	
46	if [ -z "${zcheevos}" ]; then
47	    sed -i "\$a [Achievements]\nEnabled = true\nUsername = ${username}\nChallengeMode = ${hardcore}\nLoginTimestamp = ${datets}" ${ARMSX2_CFG}
48	else
49	    sed -i '/\[Achievements\]/,/^\s*$/s/Enabled =.*/Enabled = true/' ${ARMSX2_CFG}
50	
51	    if ! grep -q "^Username = " ${ARMSX2_CFG}; then
52	        sed -i "/^\[Achievements\]/a Username = ${username}" ${ARMSX2_CFG}
53	    else
54	        sed -i "/^\[Achievements\]/,/^\[/{s/^Username = .*/Username = ${username}/;}" ${ARMSX2_CFG}
55	    fi
56	
57	    if ! grep -q "^ChallengeMode = " ${ARMSX2_CFG}; then
58	        sed -i "/^\[Achievements\]/a ChallengeMode = ${hardcore}" ${ARMSX2_CFG}
59	    else
60	        sed -i "/^\[Achievements\]/,/^\[/{s/^ChallengeMode = .*/ChallengeMode = ${hardcore}/;}" ${ARMSX2_CFG}
61	    fi
62	
63	    if ! grep -q "^EncoreMode = " ${ARMSX2_CFG}; then
64	        sed -i "/^\[Achievements\]/a EncoreMode = ${encore}" ${ARMSX2_CFG}
65	    else
66	        sed -i "/^\[Achievements\]/,/^\[/{s/^EncoreMode = .*/EncoreMode = ${encore}/;}" ${ARMSX2_CFG}
67	    fi
68	
69	    if ! grep -q "^LeaderboardNotifications = " ${ARMSX2_CFG}; then
70	        sed -i "/^\[Achievements\]/a LeaderboardNotifications = ${leaderboards}" ${ARMSX2_CFG}
71	    else
72	        sed -i "/^\[Achievements\]/,/^\[/{s/^LeaderboardNotifications = .*/LeaderboardNotifications = ${leaderboards}/;}" ${ARMSX2_CFG}
73	    fi
74	
75	    if ! grep -q "^UnofficialTestMode = " ${ARMSX2_CFG}; then
76	        sed -i "/^\[Achievements\]/a UnofficialTestMode = ${unofficial}" ${ARMSX2_CFG}
77	    else
78	        sed -i "/^\[Achievements\]/,/^\[/{s/^UnofficialTestMode = .*/UnofficialTestMode = ${unofficial}/;}" ${ARMSX2_CFG}
79	    fi
80	
81	    sed -i "/^\[Achievements\]/,/^\[/{s/^LoginTimestamp = .*/LoginTimestamp = ${datets}/;}" ${ARMSX2_CFG}
82	fi
83	
84	# The token lives in secrets.ini, whatever PCSX2.ini holds (fork #170: testing
85	# PCSX2.ini never matched, and a Token line was appended at every launch). One
86	# [Achievements] section holding one Token line, whatever the file held
87	# before: the shipped seed's bare "Token =" (no value, no trailing space); the
88	# lines a pre-#170 image appended at every launch; a second [Achievements]
89	# header, which that image's no-section branch appended to a file that
90	# already had one -- a delete bounded by the next "[" line stopped at that
91	# header and never reached the Token lines under it, and the insert then put
92	# one after every header (#308 F-EM-03); an empty file, where sed's "$a" has
93	# no last line to append after, and no file at all (#308 F-EM-05, F-EM-09).
94	# ARMSX2 reads the first Token line of the section, so duplicates were
95	# harmless; they were still wrong, and an empty file launched logged out.
96	#
97	# So the file is rewritten whole, by one awk that reads it twice: the first
98	# pass keeps every line of every [Achievements] section but its header and
99	# Token lines; the second writes the file with the first such section
100	# holding the one Token and those lines, the later [Achievements] sections
101	# dropped (their lines already written) and every other line as it was; a
102	# file with no section, or no lines, gains the section. To a temp file with
103	# the owner's permissions only, then renamed over the old one, so a launch
104	# killed part-way leaves the file as it was.
105	mkdir -p "${ARMSX2_TOKEN%/*}"
106	[ -e "${ARMSX2_TOKEN}" ] || : > "${ARMSX2_TOKEN}"
107	ARMSX2_TOKEN_TMP="${ARMSX2_TOKEN}.tmp.$$"
108	if ( umask 077; TOKEN="${token}" awk '
109	    FNR == 1 { pass++; section = 0 }
110	    /^\[/ { section = ($0 ~ /^\[Achievements\][[:space:]]*$/) }
111	    pass == 1 { if (section && $0 !~ /^\[/ && $0 !~ /^Token[[:space:]]*=/) keep[++kept] = $0; next }
112	    section {
113	        if (!written && $0 ~ /^\[/) {
114	            print "[Achievements]"; print "Token = " ENVIRON["TOKEN"]
115	            for (i = 1; i <= kept; i++) print keep[i]
116	            written = 1
117	        }
118	        next
119	    }
120	    { print }
121	    END { if (!written) { print "[Achievements]"; print "Token = " ENVIRON["TOKEN"] } }
122	' "${ARMSX2_TOKEN}" "${ARMSX2_TOKEN}" > "${ARMSX2_TOKEN_TMP}" ) && [ -s "${ARMSX2_TOKEN_TMP}" ] \
123	    && mv -f "${ARMSX2_TOKEN_TMP}" "${ARMSX2_TOKEN}"; then
124	    :
125	else
126	    # The rewrite, the check and the rename are one operation: whichever
127	    # fails, the temp goes and secrets.ini is as it was (audit of the
128	    # fixes, gpt G-F2-07: the rename sat outside this branch).
129	    rm -f "${ARMSX2_TOKEN_TMP}"
130	    echo "ARMSX2's secrets.ini could not be rewritten; its token was left as it was." >> ${LOG_FILE}
131	fi
```

### `projects/ROCKNIX/packages/emulators/standalone/armsx2-sa/scripts/start_armsx2.sh`

```
1	#!/bin/bash
2	
3	# SPDX-License-Identifier: GPL-2.0-or-later
4	# Copyright (C) 2022-present JELOS (https://github.com/JustEnoughLinuxOS)
5	
6	. /etc/profile
7	
8	#Check if ARMSX2 exists in .config
9	if [ ! -d "/storage/.config/ARMSX2" ]; then
10	    mkdir -p "/storage/.config/ARMSX2"
11	        cp -r "/usr/config/ARMSX2" "/storage/.config/"
12	fi
13	
14	#Check if ARMSX2 ini exists in .config
15	if [ ! -f "/storage/.config/ARMSX2/inis/PCSX2.ini" ]; then
16	        cp -r "/usr/config/ARMSX2/inis/PCSX2.ini" "/storage/.config/ARMSX2/inis/"
17	fi
18	
19	#Check if secrets ini exists in .config
20	if [ ! -f "/storage/.config/ARMSX2/inis/secrets.ini" ]; then
21	        cp -r "/usr/config/ARMSX2/inis/secrets.ini" "/storage/.config/ARMSX2/inis/"
22	fi
23	
24	#Make ARMSX2 bios folder
25	if [ ! -d "/storage/roms/bios/armsx2" ]; then
26	    mkdir -p "/storage/roms/bios/armsx2"
27	fi
28	
29	#Create PS2 savestates folder
30	if [ ! -d "/storage/roms/savestates/ps2" ]; then
31	    mkdir -p "/storage/roms/savestates/ps2"
32	fi
33	
34	#Emulation Station Features
35	GAME=$(echo "${1}"| sed "s#^/.*/##")
36	PLATFORM=$(echo "${2}"| sed "s#^/.*/##")
37	ASPECT=$(get_setting aspect_ratio "${PLATFORM}" "${GAME}")
38	FILTER=$(get_setting bilinear_filtering "${PLATFORM}" "${GAME}")
39	FPS=$(get_setting show_fps "${PLATFORM}" "${GAME}")
40	RATE=$(get_setting ee_cycle_rate "${PLATFORM}" "${GAME}")
41	SKIP=$(get_setting ee_cycle_skip "${PLATFORM}" "${GAME}")
42	HWDOWNLOAD=$(get_setting hw_download_mode "${PLATFORM}" "${GAME}")
43	GRENDERER=$(get_setting graphics_backend "${PLATFORM}" "${GAME}")
44	IRES=$(get_setting internal_resolution "${PLATFORM}" "${GAME}")
45	VSYNC=$(get_setting vsync "${PLATFORM}" "${GAME}")
46	ENABLE_WIDESCREEN_PATCHES=$(get_setting enable_widescreen_patches "${PLATFORM}" "${GAME}")
47	VKDRIVER=$(get_setting vulkan_driver "${PLATFORM}" "${GAME}")
48	
49	#Set the cores to use
50	CORES=$(get_setting "cores" "${PLATFORM}" "${GAME}")
51	if [ "${CORES}" = "little" ]
52	then
53	  EMUPERF="${SLOW_CORES}"
54	elif [ "${CORES}" = "big" ]
55	then
56	  EMUPERF="${FAST_CORES}"
57	else
58	  #All..
59	  unset EMUPERF
60	fi
61	
62	  #Aspect Ratio
63		if [ "$ASPECT" = "0" ]
64		then
65	  		sed -i '/^AspectRatio =/c\AspectRatio = 4:3' /storage/.config/ARMSX2/inis/PCSX2.ini
66		fi
67		if [ "$ASPECT" = "1" ]
68		then
69	  		sed -i '/^AspectRatio =/c\AspectRatio = 16:9' /storage/.config/ARMSX2/inis/PCSX2.ini
70		fi
71		if [ "$ASPECT" = "2" ]
72		then
73	  		sed -i '/^AspectRatio =/c\AspectRatio = Stretch' /storage/.config/ARMSX2/inis/PCSX2.ini
74		fi
75	
76	  #Bilinear Filtering
77	        if [ "$FILTER" = "0" ]
78	        then
79	                sed -i '/^filter =/c\filter = 0' /storage/.config/ARMSX2/inis/PCSX2.ini
80	        fi
81	        if [ "$FILTER" = "1" ]
82	        then
83	                sed -i '/^filter =/c\filter = 1' /storage/.config/ARMSX2/inis/PCSX2.ini
84	        fi
85	        if [ "$FILTER" = "2" ]
86	        then
87	                sed -i '/^filter =/c\filter = 2' /storage/.config/ARMSX2/inis/PCSX2.ini
88	        fi
89	        if [ "$FILTER" = "3" ]
90	        then
91	                sed -i '/^filter =/c\filter = 3' /storage/.config/ARMSX2/inis/PCSX2.ini
92	        fi
93	
94	  #Graphics Backend
95		if [ "$GRENDERER" = "0" ]
96		then
97	  		sed -i '/^Renderer =/c\Renderer = -1' /storage/.config/ARMSX2/inis/PCSX2.ini
98		fi
99		if [ "$GRENDERER" = "1" ]
100		then
101	  		sed -i '/^Renderer =/c\Renderer = 12' /storage/.config/ARMSX2/inis/PCSX2.ini
102		fi
103		if [ "$GRENDERER" = "2" ]
104		then
105	  		sed -i '/^Renderer =/c\Renderer = 14' /storage/.config/ARMSX2/inis/PCSX2.ini
106		fi
107	        if [ "$GRENDERER" = "3" ]
108	        then
109	                sed -i '/^Renderer =/c\Renderer = 13' /storage/.config/ARMSX2/inis/PCSX2.ini
110	        fi
111	
112	  #Internal Resolution
113	        if [ "$IRES" > "0" ]
114	        then
115	                sed -i "/^upscale_multiplier =/c\upscale_multiplier = $IRES" /storage/.config/ARMSX2/inis/PCSX2.ini
116	        else
117	                sed -i '/^upscale_multiplier =/c\upscale_multiplier = 1' /storage/.config/ARMSX2/inis/PCSX2.ini
118	        fi
119	
120	  #Show FPS
121		if [ "$FPS" = "false" ]
122		then
123	  		sed -i '/^OsdShowFPS =/c\OsdShowFPS = false' /storage/.config/ARMSX2/inis/PCSX2.ini
124		fi
125		if [ "$FPS" = "true" ]
126		then
127	  		sed -i '/^OsdShowFPS =/c\OsdShowFPS = true' /storage/.config/ARMSX2/inis/PCSX2.ini
128		fi
129	
130	  #EE Cycle Rate
131	        sed -i '/^EECycleRate =/c\EECycleRate = 0' /storage/.config/ARMSX2/inis/PCSX2.ini
132	        if [ "$RATE" = "0" ]
133	        then
134	                sed -i '/^EECycleRate =/c\EECycleRate = -3' /storage/.config/ARMSX2/inis/PCSX2.ini
135	        fi
136	        if [ "$RATE" = "1" ]
137	        then
138	                sed -i '/^EECycleRate =/c\EECycleRate = -2' /storage/.config/ARMSX2/inis/PCSX2.ini
139	        fi
140	        if [ "$RATE" = "2" ]
141	        then
142	                sed -i '/^EECycleRate =/c\EECycleRate = -1' /storage/.config/ARMSX2/inis/PCSX2.ini
143	        fi
144	        if [ "$RATE" = "3" ]
145	        then
146	                sed -i '/^EECycleRate =/c\EECycleRate = 0' /storage/.config/ARMSX2/inis/PCSX2.ini
147	        fi
148	        if [ "$RATE" = "4" ]
149	        then
150	                sed -i '/^EECycleRate =/c\EECycleRate = 1' /storage/.config/ARMSX2/inis/PCSX2.ini
151	        fi
152	        if [ "$RATE" = "5" ]
153	        then
154	                sed -i '/^EECycleRate =/c\EECycleRate = 2' /storage/.config/ARMSX2/inis/PCSX2.ini
155	        fi
156	        if [ "$RATE" = "6" ]
157	        then
158	                sed -i '/^EECycleRate =/c\EECycleRate = 3' /storage/.config/ARMSX2/inis/PCSX2.ini
159	        fi
160	
161	  #EE Cycle Skip
162	        sed -i '/^EECycleSkip =/c\EECycleSkip = 0' /storage/.config/ARMSX2/inis/PCSX2.ini
163	        if [ "$SKIP" = "0" ]
164	        then
165	                sed -i '/^EECycleSkip =/c\EECycleSkip = 0' /storage/.config/ARMSX2/inis/PCSX2.ini
166	        fi
167	        if [ "$SKIP" = "1" ]
168	        then
169	                sed -i '/^EECycleSkip =/c\EECycleSkip = 1' /storage/.config/ARMSX2/inis/PCSX2.ini
170	        fi
171	        if [ "$SKIP" = "2" ]
172	        then
173	                sed -i '/^EECycleSkip =/c\EECycleSkip = 2' /storage/.config/ARMSX2/inis/PCSX2.ini
174	        fi
175	        if [ "$SKIP" = "3" ]
176	        then
177	                sed -i '/^EECycleSkip =/c\EECycleSkip = 3' /storage/.config/ARMSX2/inis/PCSX2.ini
178	        fi
179	
180	#HW download mode
181	        sed -i '/^HWDownloadMode =/c\HWDownloadMode = 0' /storage/.config/ARMSX2/inis/PCSX2.ini
182	        if [ "$HWDOWNLOAD" = "0" ]
183	        then
184	                sed -i '/^HWDownloadMode =/c\HWDownloadMode = 0' /storage/.config/ARMSX2/inis/PCSX2.ini
185	        fi
186	        if [ "$HWDOWNLOAD" = "1" ]
187	        then
188	                sed -i '/^HWDownloadMode =/c\HWDownloadMode = 1' /storage/.config/ARMSX2/inis/PCSX2.ini
189	        fi
190	        if [ "$HWDOWNLOAD" = "2" ]
191	        then
192	                sed -i '/^HWDownloadMode =/c\HWDownloadMode = 2' /storage/.config/ARMSX2/inis/PCSX2.ini
193	        fi
194	        if [ "$HWDOWNLOAD" = "3" ]
195	        then
196	                sed -i '/^HWDownloadMode =/c\HWDownloadMode = 3' /storage/.config/ARMSX2/inis/PCSX2.ini
197	        fi
198	
199	#Widescreen patches
200		if [ "$ENABLE_WIDESCREEN_PATCHES" = "true" ]
201		then
202	  		sed -i '/^EnableWideScreenPatches =/c\EnableWideScreenPatches = true' /storage/.config/ARMSX2/inis/PCSX2.ini
203	        else
204	                sed -i '/^EnableWideScreenPatches =/c\EnableWideScreenPatches = false' /storage/.config/ARMSX2/inis/PCSX2.ini
205	        fi
206	
207	#Retroachievements
208	  /usr/bin/cheevos_armsx2.sh
209	
210	#Graphic driver fixes
211	@GRAPHICS@
212	
213	#Vulkan driver: Adreno 6xx/7xx builds ship ARMSX2's own Turnip. Point the
214	#loader at it for this process only, unless the system driver was chosen.
215	ARMSX2_ICD="/usr/share/armsx2-sa/turnip/freedreno_icd.aarch64.json"
216	if [ -f "${ARMSX2_ICD}" ] && [ "${VKDRIVER}" != "system" ]; then
217	  export VK_DRIVER_FILES="${ARMSX2_ICD}"
218	fi
219	
220	#Set QT enviornment to wayland
221	  export QT_QPA_PLATFORM=wayland
222	
223	#Run ARMSX2 emulator
224	  export SDL_AUDIODRIVER=pulseaudio
225	  set_kill set "-9 armsx2-qt"
226	  ${EMUPERF} /usr/share/armsx2-sa/armsx2-qt -bigpicture -fullscreen "${1}"
```

### `projects/ROCKNIX/packages/emulators/standalone/azahar-sa/scripts/start_azahar.sh`

```
1	#!/bin/bash
2	
3	# SPDX-License-Identifier: GPL-2.0-or-later
4	# Copyright (C) 2024-present ROCKNIX (https://github.com/ROCKNIX)
5	
6	. /etc/profile
7	set_kill set "-9 azahar"
8	
9	# Load gptokeyb support files
10	control-gen_init.sh
11	source /storage/.config/gptokeyb/control.ini
12	get_controls
13	
14	# Filesystem vars
15	IMMUTABLE_CONF_DIR="/usr/config/azahar"
16	CONF_DIR="/storage/.config/azahar"
17	CONF_FILE="${CONF_DIR}/qt-config.ini"
18	ROMS_DIR="/storage/roms/3ds"
19	SAVESTATES_DIR="/storage/roms/savestates/3ds"
20	SWAY_CONFIG="/storage/.config/sway/config"
21	
22	# Make sure azahar config directory exists
23	[ ! -d ${CONF_DIR} ] && cp -r ${IMMUTABLE_CONF_DIR} /storage/.config
24	[ ! -d ${CONF_DIR}/log ] && mkdir -p ${CONF_DIR}/log
25	
26	# Move sdmc & nand to 3ds roms folder
27	[ ! -d /storage/roms/3ds/azahar/sdmc ] && mkdir -p ${ROMS_DIR}/azahar/sdmc
28	rm -rf ${CONF_DIR}/sdmc
29	ln -sf ${ROMS_DIR}/azahar/sdmc ${CONF_DIR}/sdmc
30	
31	[ ! -d ${ROMS_DIR}/azahar/nand ] && mkdir -p ${ROMS_DIR}/azahar/nand
32	rm -rf ${CONF_DIR}/nand
33	ln -sf ${ROMS_DIR}/azahar/nand ${CONF_DIR}/nand
34	
35	# Move states to savestates folder
36	[ ! -d ${SAVESTATES_DIR} ] && mkdir -p ${SAVESTATES_DIR}
37	rm -rf ${CONF_DIR}/states
38	ln -sf ${SAVESTATES_DIR} ${CONF_DIR}/states
39	
40	# RK3588 - handle different config files for ACE / CM5
41	if [ "${HW_DEVICE}" = "RK3588" ] && [ ! -f "${CONF_FILE}" ]; then
42	  if echo ${QUIRK_DEVICE} | grep CM5; then
43	    cp ${IMMUTABLE_CONF_DIR}/qt-config_CM5.ini ${CONF_FILE}
44	  else
45	    cp ${IMMUTABLE_CONF_DIR}/qt-config_ACE.ini ${CONF_FILE}
46	  fi
47	fi
48	
49	# Make sure QT config file exists
50	[ ! -f "${CONF_FILE}" ] && cp ${IMMUTABLE_CONF_DIR}/qt-config.ini ${CONF_DIR}
51	
52	# Make sure gptokeyb mapping files exist
53	[ ! -f "${CONF_DIR}/azahar.gptk" ] && cp ${IMMUTABLE_CONF_DIR}/azahar.gptk ${CONF_DIR}
54	[ ! -f "${CONF_DIR}/azahar_mouse_addon.gptk" ] && cp ${IMMUTABLE_CONF_DIR}/azahar_mouse_addon.gptk ${CONF_DIR}
55	
56	# Emulation Station Features
57	GAME=$(echo "${1}"| sed "s#^/.*/##")
58	PLATFORM=$(echo "${2}"| sed "s#^/.*/##")
59	CPU=$(get_setting cpu_speed "${PLATFORM}" "${GAME}")
60	EMOUSE=$(get_setting emulate_mouse "${PLATFORM}" "${GAME}")
61	RENDERER=$(get_setting graphics_backend "${PLATFORM}" "${GAME}")
62	RES=$(get_setting resolution_scale "${PLATFORM}" "${GAME}")
63	INTEGER_SCALING=$(get_setting integer_scaling "${PLATFORM}" "${GAME}")
64	ROTATE=$(get_setting rotate_screen "${PLATFORM}" "${GAME}")
65	SLAYOUT=$(get_setting screen_layout "${PLATFORM}" "${GAME}")
66	CSHADERS=$(get_setting cache_shaders "${PLATFORM}" "${GAME}")
67	HSHADERS=$(get_setting hardware_shaders "${PLATFORM}" "${GAME}")
68	ACCURATE_HW_SHADERS=$(get_setting accurate_hardware_shaders "${PLATFORM}" "${GAME}")
69	DISABLE_RIGHT_EYE_RENDER=$(get_setting disable_right_eye_render "${PLATFORM}" "${GAME}")
70	SIMULATE_3DS_GPU_TIMINGS=$(get_setting simulate_3ds_gpu_timings "${PLATFORM}" "${GAME}")
71	SIMULATE_HEADPHONES_PLUGGED=$(get_setting simulate_headphones_plugged "${PLATFORM}" "${GAME}")
72	
73	#Set the cores to use
74	CORES=$(get_setting "cores" "${PLATFORM}" "${GAME}")
75	unset EMUPERF
76	[ "${CORES}" = "little" ] && EMUPERF="${SLOW_CORES}"
77	[ "${CORES}" = "big" ] && EMUPERF="${FAST_CORES}"
78	
79	# CPU Underclock - default to 100% CPU speed
80	sed -i '/^cpu_clock_percentage\\default=/c\cpu_clock_percentage\\default=false' ${CONF_FILE}
81	
82	case "${CPU}" in
83	  1) sed -i '/^cpu_clock_percentage=/c\cpu_clock_percentage=90' ${CONF_FILE};;
84	  2) sed -i '/^cpu_clock_percentage=/c\cpu_clock_percentage=80' ${CONF_FILE};;
85	  3) sed -i '/^cpu_clock_percentage=/c\cpu_clock_percentage=70' ${CONF_FILE};;
86	  4) sed -i '/^cpu_clock_percentage=/c\cpu_clock_percentage=60' ${CONF_FILE};;
87	  5) sed -i '/^cpu_clock_percentage=/c\cpu_clock_percentage=50' ${CONF_FILE};;
88	  *) sed -i '/^cpu_clock_percentage=/c\cpu_clock_percentage=100' ${CONF_FILE};;
89	esac
90	
91	# Resolution Scale - default to Native 3DS
92	sed -i '/^resolution_factor\\default=/c\resolution_factor\\default=false' ${CONF_FILE}
93	
94	case "${RES}" in
95	  0) sed -i '/^resolution_factor=/c\resolution_factor=0' ${CONF_FILE};;
96	  2) sed -i '/^resolution_factor=/c\resolution_factor=2' ${CONF_FILE};;
97	  3) sed -i '/^resolution_factor=/c\resolution_factor=3' ${CONF_FILE};;
98	  *) sed -i '/^resolution_factor=/c\resolution_factor=1' ${CONF_FILE};;
99	esac
100	
101	# Integer scaling - default to false
102	sed -i '/^use_integer_scaling\\default=/c\use_integer_scaling\\default=false' ${CONF_FILE}
103	
104	case "${INTEGER_SCALING}" in
105	  1) sed -i '/^use_integer_scaling=/c\use_integer_scaling=true' ${CONF_FILE};;
106	  *) sed -i '/^use_integer_scaling=/c\use_integer_scaling=false' ${CONF_FILE};;
107	esac
108	
109	# Rotate Screen - default to false
110	sed -i '/^upright_screen\\default=/c\upright_screen\\default=false' ${CONF_FILE}
111	
112	case "${ROTATE}" in
113	  1) sed -i '/^upright_screen=/c\upright_screen=true' ${CONF_FILE};;
114	  *) sed -i '/^upright_screen=/c\upright_screen=false' ${CONF_FILE};;
115	esac
116	
117	# Cache Shaders - default to true
118	sed -i '/^use_disk_shader_cache\\default=/c\use_disk_shader_cache\\default=false' ${CONF_FILE}
119	
120	case "${CSHADERS}" in
121	  0) sed -i '/^use_disk_shader_cache=/c\use_disk_shader_cache=false' ${CONF_FILE};;
122	  *) sed -i '/^use_disk_shader_cache=/c\use_disk_shader_cache=true' ${CONF_FILE};;
123	esac
124	
125	# Hardware Shaders - default to true
126	sed -i '/^use_hw_shader\\default=/c\use_hw_shader\\default=false' ${CONF_FILE}
127	
128	case "${HSHADERS}" in
129	  0) sed -i '/^use_hw_shader=/c\use_hw_shader=false' ${CONF_FILE};;
130	  *) sed -i '/^use_hw_shader=/c\use_hw_shader=true' ${CONF_FILE};;
131	esac
132	
133	# Use accurate multiplication in hardware shaders - default to true
134	sed -i '/^shaders_accurate_mul\\default=/c\shaders_accurate_mul\\default=false' ${CONF_FILE}
135	
136	case "${ACCURATE_HW_SHADERS}" in
137	  0) sed -i '/^shaders_accurate_mul=/c\shaders_accurate_mul=false' ${CONF_FILE};;
138	  *) sed -i '/^shaders_accurate_mul=/c\shaders_accurate_mul=true' ${CONF_FILE};;
139	esac
140	
141	# Screen Layout - default to Top / Bottom, swap = false
142	sed -i '/^layout_option\\default=/c\layout_option\\default=false' ${CONF_FILE}
143	sed -i '/^swap_screen\\default=/c\swap_screen\\default=false' ${CONF_FILE}
144	
145	case "${SLAYOUT}" in
146	  1a)
147	    # Single Screen (TOP)
148	    sed -i '/^layout_option=/c\layout_option=1' ${CONF_FILE}
149	    sed -i '/^swap_screen=/c\swap_screen=false' ${CONF_FILE}
150	    ;;
151	  1b)
152	    # Single Screen (BOTTOM)
153	    sed -i '/^layout_option=/c\layout_option=1' ${CONF_FILE}
154	    sed -i '/^swap_screen=/c\swap_screen=true' ${CONF_FILE}
155	    ;;
156	  2)
157	    # Large Screen, Small Screen
158	    sed -i '/^layout_option=/c\layout_option=2' ${CONF_FILE}
159	    sed -i '/^swap_screen=/c\swap_screen=false' ${CONF_FILE}
160	    ;;
161	  3)
162	    # Side by Side
163	    sed -i '/^layout_option=/c\layout_option=3' ${CONF_FILE}
164	    sed -i '/^swap_screen=/c\swap_screen=false' ${CONF_FILE}
165	    ;;
166	  5)
167	    # Separate windows
168	    sed -i '/^layout_option=/c\layout_option=4' "${CONF_FILE}"
169	    sed -i '/^swap_screen=/c\swap_screen=false' "${CONF_FILE}"
170	    ;;
171	  *)
172	    if [ "${DEVICE_HAS_DUAL_SCREEN}" = "true" ]; then
173	      # Separate windows by default on dual-screen
174	      sed -i '/^layout_option=/c\layout_option=4' "${CONF_FILE}"
175	    else
176	      # Top / Bottom
177	      sed -i '/^layout_option=/c\layout_option=0' "${CONF_FILE}"
178	    fi
179	    sed -i '/^swap_screen=/c\swap_screen=false' "${CONF_FILE}"
180	    ;;
181	esac
182	
183	# Force Disable Shader JIT
184	sed -i '/^use_shader_jit=/c\use_shader_jit=false' ${CONF_FILE}
185	sed -i '/^use_shader_jit\\default=/c\use_shader_jit\\default=false' ${CONF_FILE}
186	
187	# Video Backend - default to Vulkan
188	sed -i '/^graphics_api\\default=/c\graphics_api\\default=false' ${CONF_FILE}
189	
190	case "${RENDERER}" in
191	  1) sed -i '/^graphics_api=/c\graphics_api=1' ${CONF_FILE};;
192	  *) sed -i '/^graphics_api=/c\graphics_api=2' ${CONF_FILE};;
193	esac
194	
195	# Disable Right Eye Rendering - default to false
196	sed -i '/^disable_right_eye_render\\default=/c\disable_right_eye_render\\default=false' ${CONF_FILE}
197	
198	case "${DISABLE_RIGHT_EYE_RENDER}" in
199	  1) sed -i '/^disable_right_eye_render=/c\disable_right_eye_render=true' ${CONF_FILE};;
200	  *) sed -i '/^disable_right_eye_render=/c\disable_right_eye_render=false' ${CONF_FILE};;
201	esac
202	
203	# Simulate 3DS GPU Timings - default to false
204	sed -i '/^simulate_3ds_gpu_timings\\default=/c\simulate_3ds_gpu_timings\\default=false' ${CONF_FILE}
205	
206	case "${SIMULATE_3DS_GPU_TIMINGS}" in
207	  1) sed -i '/^simulate_3ds_gpu_timings=/c\simulate_3ds_gpu_timings=true' ${CONF_FILE};;
208	  *) sed -i '/^simulate_3ds_gpu_timings=/c\simulate_3ds_gpu_timings=false' ${CONF_FILE};;
209	esac
210	
211	# Simulate Headphones Plugged - default to false
212	sed -i '/^simulate_headphones_plugged\\default=/c\simulate_headphones_plugged\\default=false' ${CONF_FILE}
213	
214	case "${SIMULATE_HEADPHONES_PLUGGED}" in
215	  1) sed -i '/^simulate_headphones_plugged=/c\simulate_headphones_plugged=true' ${CONF_FILE};;
216	  *) sed -i '/^simulate_headphones_plugged=/c\simulate_headphones_plugged=false' ${CONF_FILE};;
217	esac
218	
219	# QT platform - some device / screen combinations need xcb
220	case ${HW_DEVICE} in
221	    SM8550|SM8250)
222	        [[ "${DEVICE_HAS_DUAL_SCREEN}" = "true" ]] && export QT_QPA_PLATFORM=xcb
223	    ;;
224	esac
225	
226	rm -rf /storage/.local/share/azahar
227	ln -sf ${CONF_DIR} /storage/.local/share/azahar
228	
229	# Run Azahar Emulator
230	if [ "${EMOUSE}" = "0" ]; then
231	  # Use base gptk file
232	  ${GPTOKEYB} azahar -c ${CONF_DIR}/azahar.gptk &
233	else
234	  # Combine base gptk file with mouse control gptk file, inserting line break in between
235	  cat ${CONF_DIR}/azahar.gptk <(echo) ${CONF_DIR}/azahar_mouse_addon.gptk > /tmp/azahar.gptk
236	  ${GPTOKEYB} azahar -c /tmp/azahar.gptk &
237	fi
238	
239	${EMUPERF} /usr/bin/azahar "${1}"
240	kill -9 $(pidof gptokeyb)
```

### `projects/ROCKNIX/packages/emulators/standalone/bigpemu-sa/scripts/start_bigpemu.sh`

```
1	#!/bin/bash
2	
3	# SPDX-License-Identifier: GPL-2.0-or-later
4	# Copyright (C) 2025-present ROCKNIX (https://github.com/ROCKNIX)
5	
6	. /etc/profile
7	
8	set_kill set "-9 bigpemu"
9	
10	#Check if bigpemu exists in .config
11	if [ ! -d "/storage/.config/bigpemu/userdata" ]; then
12	  mkdir -p "/storage/.config/bigpemu/userdata"
13	  cp -r "/usr/config/bigpemu/userdata" "/storage/.config/bigpemu"
14	fi
15	
16	# Link bigpemu userdata to .config/bigemu
17	rm -r /storage/.bigpemu_userdata
18	ln -sf /storage/.config/bigpemu/userdata /storage/.bigpemu_userdata
19	
20	#Emulation Station Features
21	GAME=$(echo "${1}"| sed "s#^/.*/##")
22	PLATFORM=$(echo "${2}"| sed "s#^/.*/##")
23	
24	#Set the cores to use
25	CORES=$(get_setting "cores" "${PLATFORM}" "${GAME}")
26	if [ "${CORES}" = "little" ]
27	then
28	  EMUPERF="${SLOW_CORES}"
29	elif [ "${CORES}" = "big" ]
30	then
31	  EMUPERF="${FAST_CORES}"
32	else
33	  #All..
34	  unset EMUPERF
35	fi
36	
37	# libmali GPU driver needs gl4es
38	if [ -x "/usr/bin/gpudriver" ] && [ $(/usr/bin/gpudriver) = "libmali" ]; then
39	  export LD_PRELOAD=/usr/lib/gl4es/libGL.so.1
40	fi
41	
42	${EMUPERF} /usr/share/bigpemu/bigpemu "${1}"
```

### `projects/ROCKNIX/packages/emulators/standalone/cemu-sa/scripts/start_cemu.sh`

```
1	#!/bin/sh
2	# SPDX-License-Identifier: GPL-2.0
3	# Copyright (C) 2022-present Frank Hartung (supervisedthinking (@) gmail.com)
4	# Copyright (C) 2023 JELOS (https://github.com/JustEnoughLinuxOS)
5	
6	# Source environment variables
7	. /etc/profile
8	
9	# Ensure we're using pulseaudio
10	export SDL_AUDIODRIVER=pulseaudio
11	set_kill set "-9 cemu"
12	
13	if [ -z "${PASINK}" ]
14	then
15	  PASINK=$(pactl info | grep 'Default Sink:' | cut -d ' ' -f 3)
16	fi
17	
18	# Set up mime db
19	mkdir -p /storage/.local/share/mime/packages
20	cp -rf /usr/share/mime/packages/* /storage/.local/share/mime/packages
21	update-mime-database /storage/.local/share/mime
22	
23	# Set common paths
24	CEMU_CONFIG_ROOT="/storage/.config/Cemu"
25	CEMU_CACHE_LOG="${CEMU_CONFIG_ROOT}/share/log.txt"
26	CEMU_VAR_LOG="/var/log/Cemu.log"
27	CEMU_HOME_CONFIG="${CEMU_CONFIG_ROOT}/share"
28	CEMU_HOME_LOCAL="/storage/.local/share/Cemu"
29	CEMU_HOME_ONLINE="${CEMU_HOME_CONFIG}/online"
30	CEMU_HOME_MLC01="${CEMU_HOME_CONFIG}/mlc01"
31	CEMU_HOME_KEYS="${CEMU_HOME_CONFIG}/keys"
32	CEMU_BIOS="/storage/roms/bios/cemu"
33	
34	# create link to config directory
35	if [ ! -d ${CEMU_HOME_CONFIG} ]; then
36	  mkdir -p ${CEMU_HOME_CONFIG}
37	  echo created ${CEMU_HOME_CONFIG}
38	fi
39	
40	if [ -d ${CEMU_HOME_LOCAL} ] && [ ! -L ${CEMU_HOME_LOCAL} ]; then
41	    cp -rf ${CEMU_HOME_LOCAL}/* ${CEMU_HOME_CONFIG}
42	    rm -rf ${CEMU_HOME_LOCAL}
43	    echo moved ${CEMU_HOME_LOCAL} to ${CEMU_HOME_CONFIG}
44	fi
45	
46	if [ ! -L ${CEMU_HOME_LOCAL} ]; then
47	  ln -sf ${CEMU_HOME_CONFIG} ${CEMU_HOME_LOCAL}
48	  echo created symlink from ${CEMU_HOME_CONFIG} to ${CEMU_HOME_LOCAL}
49	fi
50	
51	# create symlink to online directory
52	mkdir -p "${CEMU_BIOS}/online"
53	if [ -d ${CEMU_HOME_ONLINE} ] && [ ! -L ${CEMU_HOME_ONLINE} ]; then
54	    mv ${CEMU_HOME_ONLINE}/* ${CEMU_BIOS}/online
55	    rm -rf ${CEMU_HOME_ONLINE}
56	    echo moved ${CEMU_HOME_ONLINE} to ${CEMU_BIOS}/online
57	fi
58	
59	if [ ! -L ${CEMU_HOME_ONLINE} ]; then
60	  ln -sf ${CEMU_BIOS}/online ${CEMU_HOME_ONLINE}
61	  echo created symlink from ${CEMU_HOME_ONLINE} to ${CEMU_BIOS}/online
62	fi
63	
64	# create symlink to mlc01 directory
65	mkdir -p "${CEMU_BIOS}/mlc01"
66	if [ -d ${CEMU_HOME_MLC01} ] && [ ! -L ${CEMU_HOME_MLC01} ]; then
67	    mv ${CEMU_HOME_MLC01}/* ${CEMU_BIOS}/mlc01
68	    rm -rf ${CEMU_HOME_MLC01}
69	    echo moved ${CEMU_HOME_MLC01} to ${CEMU_BIOS}/mlc01
70	fi
71	
72	if [ ! -L ${CEMU_HOME_MLC01} ]; then
73	  ln -sf ${CEMU_BIOS}/mlc01 ${CEMU_HOME_MLC01}
74	  echo created symlink from ${CEMU_HOME_MLC01} to ${CEMU_BIOS}/mlc01
75	fi
76	
77	# create symlink to keys directory
78	mkdir -p "${CEMU_BIOS}/keys"
79	if [ -d ${CEMU_HOME_KEYS} ] && [ ! -L ${CEMU_HOME_KEYS} ]; then
80	    mv ${CEMU_HOME_KEYS}/* ${CEMU_BIOS}/keys
81	    rm -rf ${CEMU_HOME_KEYS}
82	    echo moved ${CEMU_HOME_KEYS} to ${CEMU_BIOS}/keys
83	fi
84	
85	if [ ! -L ${CEMU_HOME_KEYS} ]; then
86	  ln -sf ${CEMU_BIOS}/keys ${CEMU_HOME_KEYS}
87	  echo created symlink from ${CEMU_HOME_KEYS} to ${CEMU_BIOS}/keys
88	fi
89	
90	# Create symlink to logfile
91	if [ ! -L ${CEMU_VAR_LOG} ]; then
92	  ln -sf ${CEMU_CACHE_LOG} ${CEMU_VAR_LOG}
93	fi
94	
95	# Make sure CEMU settings exist, and set the audio output.
96	if [ ! -f "${CEMU_CONFIG_ROOT}/settings.xml" ]
97	then
98	  cp -f /usr/config/Cemu/settings.xml ${CEMU_CONFIG_ROOT}/settings.xml
99	fi
100	
101	# Make sure the basic controller profiles exist.
102	if [ ! -d "${CEMU_CONFIG_ROOT}/controllerProfiles" ]
103	then
104	  cp -R /usr/config/Cemu/controllerProfiles ${CEMU_CONFIG_ROOT}/
105	fi
106	
107	FILE=$(echo $1 | sed "s#^/.*/##g")
108	CON=$(get_setting wiiu_controller_profile wiiu "${FILE}")
109	CON_LAYOUT=$(get_setting wiiu_controller_layout wiiu "${FILE}")
110	ONLINE=$(get_setting online_enabled wiiu "${FILE}")
111	GAMEPAD=$(get_setting gamepad_enabled wiiu "${FILE}")
112	
113	RENDERER=$(get_setting graphics_backend wiiu "${FILE}")
114	BACKEND=$(get_setting gdk_backend wiiu "${FILE}")
115	VSYNC=$(get_setting vsync wiiu "${FILE}")
116	GX2_DRAW_DONE_SYNC=$(get_setting gx2_draw_done_sync wiiu "${FILE}")
117	UPSCALE_FILTER=$(get_setting upscale_filter wiiu "${FILE}")
118	DOWNSCALE_FILTER=$(get_setting downscale_filter wiiu "${FILE}")
119	FULLSCREEN_SCALING=$(get_setting fullscreen_scaling wiiu "${FILE}")
120	ASYNC_SHADER_COMPILE=$(get_setting async_shader_compile wiiu "${FILE}")
121	VK_ACCURATE_BARRIER=$(get_setting vk_accurate_barriers wiiu "${FILE}")
122	
123	OVERLAY_POSITION=$(get_setting overlay_position wiiu "${FILE}")
124	OVERLAY_TEXT_SCALE=$(get_setting overlay_text_scale wiiu "${FILE}")
125	OVERLAY_TEXT_COLOR=$(get_setting overlay_text_color wiiu "${FILE}")
126	OVERLAY_TEXT_TRANPARENCY=$(get_setting overlay_text_transparency wiiu "${FILE}")
127	OVERLAY_SHOW_FPS=$(get_setting overlay_show_fps wiiu "${FILE}")
128	OVERLAY_DRAW_CALLS=$(get_setting overlay_draw_calls wiiu "${FILE}")
129	OVERLAY_SHOW_CPU_USAGE=$(get_setting overlay_show_cpu_usage wiiu "${FILE}")
130	OVERLAY_SHOW_CPU_PER_CORE_USAGE=$(get_setting overlay_show_cpu_per_core_usage wiiu "${FILE}")
131	OVERLAY_SHOW_RAM_USAGE=$(get_setting overlay_show_ram_usage wiiu "${FILE}")
132	OVERLAY_SHOW_VRAM_USAGE=$(get_setting overlay_show_vram_usage wiiu "${FILE}")
133	
134	NOTIFICATION_POS=$(get_setting notification_position wiiu "${FILE}")
135	NOTIFICATION_TEXT_SCALE=$(get_setting notification_text_scale wiiu "${FILE}")
136	NOTIFICATION_TEXT_COLOR=$(get_setting notification_text_color wiiu "${FILE}")
137	NOTIFICATION_TEXT_TRANPARENCY=$(get_setting notification_text_transparency wiiu "${FILE}")
138	
139	#
140	# Control
141	#
142	
143	# WiiU controller profile
144	case ${CON} in
145	  "Wii U Pro Controller")
146	     CONFILE="wii_u_pro_controller.xml"
147	     CON="Wii U Pro Controller"
148	  ;;
149	  *)
150	     ### Break these out when possible.
151	     ### "Wii U GamePad"|"Wii U Classic Controller"|"Wiimote"
152	     CONFILE="wii_u_gamepad.xml"
153	     CON="Wii U GamePad"
154	  ;;
155	esac
156	
157	for CONTROLLER in ${CEMU_CONFIG_ROOT}/controllerProfiles/*
158	do
159	  LOCALFILE="$(basename ${CONTROLLER})"
160	  if [ "${CONFILE}" = "${LOCALFILE}" ]
161	  then
162	      cp "${CONTROLLER}" "${CEMU_CONFIG_ROOT}/controllerProfiles/controller0.xml"
163	  fi
164	done
165	
166	UUID0="0_$(control-gen | awk 'BEGIN {FS="\""} /^DEVICE/ {print $2;exit}')"
167	# Check for js0, else fall back to joypad
168	if grep -q "js0" /proc/bus/input/devices; then
169	  CONTROLLER0=$(grep -b4 js0 /proc/bus/input/devices | awk 'BEGIN {FS="\""}; /Name/ {printf $2}')
170	else
171	  CONTROLLER0=$(grep -b4 joypad /proc/bus/input/devices | awk 'BEGIN {FS="\""}; /Name/ {printf $2}')
172	fi
173	
174	xmlstarlet ed --inplace -u "//emulated_controller/type" -v "${CON}" ${CEMU_CONFIG_ROOT}/controllerProfiles/controller0.xml
175	xmlstarlet ed --inplace -u "//emulated_controller/controller/uuid" -v "${UUID0}" ${CEMU_CONFIG_ROOT}/controllerProfiles/controller0.xml
176	xmlstarlet ed --inplace -u "//emulated_controller/controller/display_name" -v "${CONTROLLER0}" ${CEMU_CONFIG_ROOT}/controllerProfiles/controller0.xml
177	
178	# WiiU controller layout
179	if [[ "$CON_LAYOUT" = "xbox" ]]; then
180		mapping1=$(xmlstarlet sel -t -v "//entry[mapping='1']/button" ${CEMU_CONFIG_ROOT}/controllerProfiles/controller0.xml)
181		mapping2=$(xmlstarlet sel -t -v "//entry[mapping='2']/button" ${CEMU_CONFIG_ROOT}/controllerProfiles/controller0.xml)
182		mapping3=$(xmlstarlet sel -t -v "//entry[mapping='3']/button" ${CEMU_CONFIG_ROOT}/controllerProfiles/controller0.xml)
183		mapping4=$(xmlstarlet sel -t -v "//entry[mapping='4']/button" ${CEMU_CONFIG_ROOT}/controllerProfiles/controller0.xml)
184		xmlstarlet ed --inplace \
185	  -u "//entry[mapping='1']/button" -v "$mapping2" \
186	  -u "//entry[mapping='2']/button" -v "$mapping1" \
187	  -u "//entry[mapping='3']/button" -v "$mapping4" \
188	  -u "//entry[mapping='4']/button" -v "$mapping3" \
189		${CEMU_CONFIG_ROOT}/controllerProfiles/controller0.xml
190	fi
191	
192	#
193	# Online
194	#
195	
196	# Online enable
197	xmlstarlet ed --inplace -u "//Account/OnlineEnabled" -v "${ONLINE}" ${CEMU_CONFIG_ROOT}/settings.xml
198	
199	#
200	# Graphic
201	#
202	
203	# Graphic backend
204	# Assume Vulkan
205	case ${RENDERER} in
206	  opengl)
207	    RENDERER=0
208	  ;;
209	  *)
210	    RENDERER=1
211	  ;;
212	esac
213	
214	xmlstarlet ed --inplace -u "//Graphic/api" -v "${RENDERER}" ${CEMU_CONFIG_ROOT}/settings.xml
215	
216	# GDK backend
217	case ${BACKEND} in
218	  x11)
219	    export GDK_BACKEND=x11
220	  ;;
221	  *)
222	    export GDK_BACKEND=wayland
223	  ;;
224	esac
225	
226	# Vsync
227	[[ -z $VSYNC ]] && VSYNC="1"
228	
229	# GX2 draw done sync
230	[[ -z $GX2_DRAW_DONE_SYNC ]] && GX2_DRAW_DONE_SYNC="true"
231	xmlstarlet ed --inplace -u "//Graphic/GX2DrawdoneSync" -v "$GX2_DRAW_DONE_SYNC" ${CEMU_CONFIG_ROOT}/settings.xml
232	
233	# Upscale filter
234	[[ -z $UPSCALE_FILTER ]] && UPSCALE_FILTER="1"
235	xmlstarlet ed --inplace -u "//Graphic/UpscaleFilter" -v "$UPSCALE_FILTER" ${CEMU_CONFIG_ROOT}/settings.xml
236	
237	# Downscale filter
238	[[ -z $DOWNSCALE_FILTER ]] && DOWNSCALE_FILTER="0"
239	xmlstarlet ed --inplace -u "//Graphic/DownscaleFilter" -v "$DOWNSCALE_FILTER" ${CEMU_CONFIG_ROOT}/settings.xml
240	
241	# Fullscreen scaling
242	[[ -z $FULLSCREEN_SCALING ]] && FULLSCREEN_SCALING="0"
243	xmlstarlet ed --inplace -u "//Graphic/FullscreenScaling" -v "$FULLSCREEN_SCALING" ${CEMU_CONFIG_ROOT}/settings.xml
244	
245	# Async shader compile
246	[[ -z $ASYNC_SHADER_COMPILE ]] && ASYNC_SHADER_COMPILE="true"
247	xmlstarlet ed --inplace -u "//Graphic/AsyncCompile" -v "$ASYNC_SHADER_COMPILE" ${CEMU_CONFIG_ROOT}/settings.xml
248	
249	# VK accurate barrier
250	[[ -z $VK_ACCURATE_BARRIER ]] && VK_ACCURATE_BARRIER="true"
251	xmlstarlet ed --inplace -u "//Graphic/vkAccurateBarriers" -v "$VK_ACCURATE_BARRIER" ${CEMU_CONFIG_ROOT}/settings.xml
252	
253	#
254	# Overlay
255	#
256	
257	# Overlay position
258	[[ -z $OVERLAY_POSITION ]] && OVERLAY_POSITION="0"
259	xmlstarlet ed --inplace -u "//Overlay/Position" -v "${OVERLAY_POSITION}" ${CEMU_CONFIG_ROOT}/settings.xml
260	
261	# Overlay text scale
262	[[ -z $OVERLAY_TEXT_SCALE ]] && OVERLAY_TEXT_SCALE="100"
263	xmlstarlet ed --inplace -u "//Overlay/TextScale" -v "${OVERLAY_TEXT_SCALE}" ${CEMU_CONFIG_ROOT}/settings.xml
264	
265	# Overlay text color and transparency
266	[[ -z $OVERLAY_TEXT_COLOR ]] && OVERLAY_TEXT_COLOR="FFFFFF"
267	[[ -z $OVERLAY_TEXT_TRANPARENCY ]] && OVERLAY_TEXT_TRANPARENCY="FF"
268	
269	TEXT_COLOR=`echo "ibase=16; ${OVERLAY_TEXT_TRANPARENCY}${OVERLAY_TEXT_COLOR}" | bc`
270	xmlstarlet ed --inplace -u "//Overlay/TextColor" -v "${TEXT_COLOR}" ${CEMU_CONFIG_ROOT}/settings.xml
271	
272	# Overlay show fps
273	[[ -z $OVERLAY_SHOW_FPS ]] && OVERLAY_SHOW_FPS="true"
274	xmlstarlet ed --inplace -u "//Overlay/FPS" -v "${OVERLAY_SHOW_FPS}" ${CEMU_CONFIG_ROOT}/settings.xml
275	
276	# Overlay draw calls
277	[[ -z $OVERLAY_DRAW_CALLS ]] && OVERLAY_DRAW_CALLS="false"
278	xmlstarlet ed --inplace -u "//Overlay/DrawCalls" -v "${OVERLAY_DRAW_CALLS}" ${CEMU_CONFIG_ROOT}/settings.xml
279	
280	# Overlay show cpu usage
281	[[ -z $OVERLAY_SHOW_CPU_USAGE ]] && OVERLAY_SHOW_CPU_USAGE="true"
282	xmlstarlet ed --inplace -u "//Overlay/CPUUsage" -v "${OVERLAY_SHOW_CPU_USAGE}" ${CEMU_CONFIG_ROOT}/settings.xml
283	
284	# Overlay show cpu per core usage
285	[[ -z $OVERLAY_SHOW_CPU_PER_CORE_USAGE ]] && OVERLAY_SHOW_CPU_PER_CORE_USAGE="true"
286	xmlstarlet ed --inplace -u "//Overlay/CPUPerCoreUsage" -v "${OVERLAY_SHOW_CPU_PER_CORE_USAGE}" ${CEMU_CONFIG_ROOT}/settings.xml
287	
288	# Overlay show ram usage
289	[[ -z $OVERLAY_SHOW_RAM_USAGE ]] && OVERLAY_SHOW_RAM_USAGE="true"
290	xmlstarlet ed --inplace -u "//Overlay/RAMUsage" -v "${OVERLAY_SHOW_RAM_USAGE}" ${CEMU_CONFIG_ROOT}/settings.xml
291	
292	# Overlay show vram usage
293	[[ -z $OVERLAY_SHOW_VRAM_USAGE ]] && OVERLAY_SHOW_VRAM_USAGE="true"
294	xmlstarlet ed --inplace -u "//Overlay/VRAMUsage" -v "${OVERLAY_SHOW_VRAM_USAGE}" ${CEMU_CONFIG_ROOT}/settings.xml
295	
296	#
297	# Notification
298	#
299	
300	# Notification position
301	[[ -z $NOTIFICATION_POSITION ]] && NOTIFICATION_POSITION="0"
302	xmlstarlet ed --inplace -u "//Notification/Position" -v "${NOTIFICATION_POSITION}" ${CEMU_CONFIG_ROOT}/settings.xml
303	
304	# Overlay text scale
305	[[ -z $NOTIFICATION_TEXT_SCALE ]] && NOTIFICATION_TEXT_SCALE="100"
306	xmlstarlet ed --inplace -u "//Notification/TextScale" -v "${NOTIFICATION_TEXT_SCALE}" ${CEMU_CONFIG_ROOT}/settings.xml
307	
308	# Overlay text color and transparency
309	[[ -z $NOTIFICATION_TEXT_COLOR ]] && NOTIFICATION_TEXT_COLOR="FFFFFF"
310	[[ -z $NOTIFICATION_TEXT_TRANPARENCY ]] && NOTIFICATION_TEXT_TRANPARENCY="FF"
311	
312	TEXT_COLOR=`echo "ibase=16; ${NOTIFICATION_TEXT_TRANPARENCY}${NOTIFICATION_TEXT_COLOR}" | bc`
313	xmlstarlet ed --inplace -u "//Notification/TextColor" -v "${TEXT_COLOR}" ${CEMU_CONFIG_ROOT}/settings.xml
314	
315	#
316	# Misc
317	#
318	
319	xmlstarlet ed --inplace -u "//fullscreen" -v "true" ${CEMU_CONFIG_ROOT}/settings.xml
320	xmlstarlet ed --inplace -u "//Audio/TVDevice" -v "${PASINK}" ${CEMU_CONFIG_ROOT}/settings.xml
321	
322	#
323	# Dual screen gamepad
324	#
325	
326	if [ -z "${GAMEPAD}" ]; then
327	  if [ "${DEVICE_HAS_DUAL_SCREEN}" = "true" ]; then
328	    xmlstarlet ed --inplace -u "//open_pad" -v "true" ${CEMU_CONFIG_ROOT}/settings.xml
329	  fi
330	else
331	  xmlstarlet ed --inplace -u "//open_pad" -v "${GAMEPAD}" ${CEMU_CONFIG_ROOT}/settings.xml
332	fi
333	
334	# Run the emulator
335	cemu -g "$@"
```

### `projects/ROCKNIX/packages/emulators/standalone/daedalusx64-sa/scripts/start_daedalusx64.sh`

```
1	#!/bin/bash
2	
3	# SPDX-License-Identifier: GPL-2.0-or-later
4	# Copyright (C) 2025-present ROCKNIX (https://github.com/ROCKNIX)
5	
6	. /etc/profile
7	set_kill set "-9 daedalus"
8	
9	#Check if DaedalusX64 exists in .config
10	if [ ! -d "/storage/.config/DaedalusX64" ]; then
11	  cp -r "/usr/config/DaedalusX64" "/storage/.config/"
12	fi
13	
14	#Check if n64 save state folders exist
15	if [ ! -d "/storage/roms/savestates/n64/daedalus" ]; then
16	    mkdir -p "/storage/roms/savestates/n64/daedalus"
17	fi
18	
19	# Link Roms, Saves, and SaveStates to correct dir
20	rm "/storage/.config/DaedalusX64/Roms"
21	ln -sf "/storage/roms/n64" "/storage/.config/DaedalusX64/Roms"
22	rm "/storage/.config/DaedalusX64/SavesGames"
23	ln -sf "/storage/roms/n64" "/storage/.config/DaedalusX64/SavesGames"
24	rm "/storage/.config/DaedalusX64/SaveStates"
25	ln -sf "/storage/roms/savestates/n64/daedalus" "/storage/.config/DaedalusX64/SaveStates"
26	
27	#Emulation Station Features
28	GAME=$(echo "${1}"| sed "s#^/.*/##")
29	PLATFORM=$(echo "${2}"| sed "s#^/.*/##")
30	
31	#Set the cores to use
32	CORES=$(get_setting "cores" "${PLATFORM}" "${GAME}")
33	if [ "${CORES}" = "little" ]
34	then
35	  EMUPERF="${SLOW_CORES}"
36	elif [ "${CORES}" = "big" ]
37	then
38	  EMUPERF="${FAST_CORES}"
39	else
40	  ### All..
41	  unset EMUPERF
42	fi
43	
44	#Always grab the latest daedalus bin
45	shasum1=$(sha1sum /usr/config/DaedalusX64/daedalus | awk '{print $1}')
46	shasum2=$(sha1sum /storage/.config/DaedalusX64/daedalus | awk '{print $1}')
47	
48	if [ "$shasum1" <> "$shasum2" ]; then
49	  cp -r "/usr/config/DaedalusX64/daedalus" "/storage/.config/DaedalusX64/daedalus"
50	fi
51	
52	cd /storage/.config/DaedalusX64/
53	
54	${EMUPERF} /storage/.config/DaedalusX64/daedalus "${1}"
```

### `projects/ROCKNIX/packages/emulators/standalone/dolphin-sa/scripts/cheevos_dolphin.sh`

```
1	#! /bin/bash
2	
3	# SPDX-License-Identifier: GPL-2.0-or-later
4	# Copyright (C) 2024-present ROCKNIX (https://github.com/ROCKNIX)
5	
6	. /etc/profile
7	
8	LOG_FILE="/var/log/cheevos.log"
9	
10	# Extract username, password, token, if enabled, and hardcore mode from system.cfg
11	username=$(get_setting "global.retroachievements.username")
12	password=$(get_setting "global.retroachievements.password")
13	token=$(get_setting "global.retroachievements.token")
14	enabled=$(get_setting "global.retroachievements")
15	hardcore=$(get_setting "global.retroachievements.hardcore")
16	encore=$(get_setting "global.retroachievements.encore")
17	unofficial=$(get_setting "global.retroachievements.unofficial")
18	[ -z "${unofficial}" ] && unofficial=$(get_setting "global.retroachievements.testunofficial")  # the spelling before 2026-09; EmulationStation writes .unofficial
19	hosturl=$(get_setting "global.retroachievements.customhost")
20	
21	# Publish the generated session as one file so disabling or signing out cannot
22	# reuse an earlier active session. Saved ES account settings are read-only here.
23	INI_FILE="/storage/.config/dolphin-emu/RetroAchievements.ini"
24	temporary=""
25	trap '[ -z "${temporary}" ] || rm -f -- "${temporary}"' EXIT
26	
27	settings_failed() {
28	  echo "Dolphin achievements settings could not be written; refusing launch." >> "${LOG_FILE}"
29	  local language="${LANGUAGE:-${LC_ALL:-${LC_MESSAGES:-${LANG:-en}}}}"
30	  language="${language,,}"
31	  local title="DOLPHIN DID NOT START"
32	  local message="Achievements settings could not be updated. Check the game storage and folder permissions, then try again."
33	  case "${language}" in
34	    fr|fr_*|fr-*|fr.*|fr@*|fr:*)
35	      title="DOLPHIN N’A PAS DÉMARRÉ"
36	      message="Les paramètres des succès n’ont pas pu être mis à jour. Vérifiez le stockage des jeux et les permissions des dossiers, puis réessayez."
37	      ;;
38	  esac
39	  printf 'DOLPHIN DID NOT START\n%s\n\n%s\n' "${title}" "${message}" > /tmp/launch_error.log
40	  exit 250
41	}
42	
43	publish_settings() {
44	  temporary=$(umask 077; mktemp "${INI_FILE}.XXXXXX") || return 1
45	  if ! cat > "${temporary}" <<EOF
46	[Achievements]
47	DiscordPresenceEnabled = False
48	Enabled = ${enabled}
49	EncoreEnabled = ${encore}
50	HardcoreEnabled = ${hardcore}
51	ProgressEnabled = False
52	SpectatorEnabled = False
53	UnofficialEnabled = ${unofficial}
54	Username = ${username}
55	ApiToken = ${token}
56	HostUrl = ${hosturl}
57	EOF
58	  then
59	    return 1
60	  fi
61	  # -T refuses a destination directory instead of moving a token file into it.
62	  mv -fT -- "${temporary}" "${INI_FILE}" || return 1
63	  temporary=""
64	}
65	
66	publish_disabled() {
67	  enabled="False"
68	  encore="False"
69	  hardcore="False"
70	  unofficial="False"
71	  username=""
72	  token=""
73	  hosturl=""
74	  publish_settings || settings_failed
75	}
76	
77	# Check if RetroAchievements are enabled in Emulation Station
78	if [ "${enabled}" = 1 ]; then
79	  enabled="True"
80	else
81	  echo "RetroAchievements are not enabled, please turn them on in Emulation Station." > ${LOG_FILE}
82	  publish_disabled
83	  exit 1
84	fi
85	
86	# Check if api token is present in system.cfg
87	if [ -z "${token}" ]; then
88	    echo "RetroAchievements token is empty, please log in with your RetroAchievements credentials in Emulation Station." > ${LOG_FILE}
89	    publish_disabled
90	    exit 1
91	fi
92	
93	# Set hardcore mode
94	hardcore_raw="${hardcore}"
95	if [ "${hardcore}" = 1 ]; then
96	  hardcore="True"
97	else
98	  hardcore="False"
99	fi
100	
101	# Set encore mode
102	if [ "${encore}" = 1 ]; then
103	  encore="True"
104	else
105	  encore="False"
106	fi
107	
108	# Set unofficial mode
109	if [ "${unofficial}" = 1 ]; then
110	  unofficial="True"
111	else
112	  unofficial="False"
113	fi
114	
115	# The offline toggle routes only a known casual session to a listening proxy
116	# (#584, D-RA-002). Keep the configured custom host for every fallback; never
117	# change saved settings or credentials here. An empty/unknown hardcore read
118	# is not permission to use a service that cannot queue hardcore awards.
119	# Dolphin2606 passes HostUrl to rc_client_set_host; its bundled rcheevos adds
120	# http:// to a host without a scheme. The bare host below therefore uses HTTP.
121	# Match PPSSPP's read-only IPv4-capable listener check (0 listening, 1 absent,
122	# 2 unreadable). A listening socket is not proof of proxy identity or readiness.
123	proxy_listening() {
124	  local proc="${RAOFFLINEPROXY_PROC_NET:-/proc/net}" f readable=0 sl addr rem st rest
125	  for f in "${proc}/tcp" "${proc}/tcp6"; do
126	    [ -r "${f}" ] || continue
127	    readable=1
128	    while read -r sl addr rem st rest; do
129	      [ "${st}" = "0A" ] || continue
130	      case "${addr}" in
131	        0100007F:1F90|00000000:1F90|0000000000000000FFFF00000100007F:1F90) return 0 ;;
132	      esac
133	    done < "${f}"
134	  done
135	  [ "${readable}" -eq 1 ] && return 1
136	  return 2
137	}
138	
139	if [ "$(get_setting "global.retroachievements.offlineproxy")" = 1 ] && [ "${hardcore_raw}" = "0" ]; then
140	  proxy_listening
141	  case $? in
142	    0) hosturl="127.0.0.1:8080" ;;
143	    1) echo "Offline RetroAchievements is on but nothing is listening on 127.0.0.1:8080; keeping the configured achievements host." >> "${LOG_FILE}" ;;
144	    *) echo "Offline RetroAchievements is on but the listener tables could not be read; keeping the configured achievements host." >> "${LOG_FILE}" ;;
145	  esac
146	fi
147	
148	publish_settings || settings_failed
```

### `projects/ROCKNIX/packages/emulators/standalone/dolphin-sa/scripts/dolphin-save-paths`

```
1	#!/usr/bin/python3
2	# SPDX-License-Identifier: GPL-2.0-or-later
3	# Copyright (C) 2026 ROCKNIX (https://github.com/ROCKNIX)
4	"""Prepare Dolphin's known save links without converting retained real data."""
5	import argparse
6	import ctypes
7	import fcntl
8	import os
9	from pathlib import Path
10	import re
11	import shutil
12	import signal
13	import stat
14	import sys
15	import tempfile
16	
17	REGIONS = ("EUR", "JAP", "USA")
18	MAX_COPY_FILES = 4096
19	MAX_COPY_BYTES = 64 * 1024 * 1024
20	
21	
22	# The first line is a fixed ownership discriminator consumed by runemu, not UI.
23	ERROR_OWNER = "DOLPHIN DID NOT START"
24	MESSAGES_FR = {
25	    'Existing Dolphin data needs attention. Back up these locations, then use the file manager to choose and arrange the saved data before trying again. No saved data was removed.':
26	        'Les données Dolphin existantes nécessitent votre attention. Sauvegardez ces emplacements, puis utilisez le gestionnaire de fichiers pour choisir et organiser les données à conserver avant de réessayer. Aucune donnée sauvegardée n’a été supprimée.',
27	    'Dolphin storage path is outside its expected root.':
28	        'L’emplacement de stockage Dolphin se trouve hors du dossier prévu.',
29	    'Dolphin save storage is not writable. Check the game storage and folder permissions, then try again.':
30	        'Impossible d’écrire dans le stockage des sauvegardes Dolphin. Vérifiez le stockage des jeux et les permissions des dossiers, puis réessayez.',
31	    'Game storage is not ready. Reconnect it and try again. No saved data was removed.':
32	        'Le stockage des jeux n’est pas prêt. Reconnectez-le et réessayez. Aucune donnée sauvegardée n’a été supprimée.',
33	    'A Dolphin save path is separately mounted. Check the storage layout before trying again.':
34	        'Un emplacement de sauvegarde Dolphin possède un montage distinct. Vérifiez l’organisation du stockage avant de réessayer.',
35	    "Dolphin's retained GC resources exceed the preparation limit. Arrange them in the file manager before trying again.":
36	        'Les ressources GameCube conservées dépassent la limite de préparation. Organisez-les dans le gestionnaire de fichiers avant de réessayer.',
37	    'Dolphin configuration is missing. Check the installed defaults before trying again.':
38	        'La configuration Dolphin est absente. Vérifiez la configuration fournie avec le système avant de réessayer.',
39	    'Dolphin save preparation was interrupted. Saved data was kept. Try again.':
40	        'La préparation des sauvegardes Dolphin a été interrompue. Les données sauvegardées ont été conservées. Réessayez.',
41	    'Dolphin save preparation lock is unavailable. Try again after the other launch finishes.':
42	        'La préparation des sauvegardes Dolphin est indisponible. Réessayez après la fin de l’autre lancement.',
43	    'Dolphin save preparation is already running. Wait for it to finish, then try again.':
44	        'La préparation des sauvegardes Dolphin est déjà en cours. Attendez sa fin, puis réessayez.',
45	    'Dolphin could not prepare save storage. Check the storage connection and permissions, then try again. Saved data was kept.':
46	        'Dolphin n’a pas pu préparer le stockage des sauvegardes. Vérifiez la connexion du stockage et les permissions, puis réessayez. Les données sauvegardées ont été conservées.',
47	}
48	
49	
50	def message_language():
51	    # ES exports LANGUAGE; use the same precedence as the cloud companion page.
52	    value = next((os.environ[key] for key in ("LANGUAGE", "LC_ALL", "LC_MESSAGES", "LANG")
53	                  if os.environ.get(key)), "en")
54	    primary = value.split(":", 1)[0].replace("-", "_").split("_", 1)[0].split(".", 1)[0].split("@", 1)[0].lower()
55	    return "fr" if primary == "fr" else "en"
56	
57	
58	def visible_path(path):
59	    # The native message wraps only at whitespace. Keep this known long card
60	    # path intact except for a display line break at its final slash.
61	    prefix = "/storage/.config/dolphin-emu/GC/"
62	    leaf = path.removeprefix(prefix)
63	    if path.startswith(prefix) and re.fullmatch(r"MemoryCard[AB]\.(EUR|JAP|USA)\.raw", leaf):
64	        return prefix + "\n" + leaf
65	    return path
66	
67	
68	def visible_error(message):
69	    language = message_language()
70	    title = "DOLPHIN N’A PAS DÉMARRÉ" if language == "fr" else "DOLPHIN DID NOT START"
71	    # Translate only the known sentence, never player data paths below it.
72	    sentence, separator, paths = message.partition("\n")
73	    if language == "fr":
74	        sentence = MESSAGES_FR.get(sentence, sentence)
75	    paths = "\n".join(visible_path(path) for path in paths.split("\n"))
76	    return title + "\n\n" + sentence + separator + paths + "\n"
77	
78	
79	class Refused(Exception):
80	    pass
81	
82	
83	def kind(path):
84	    try:
85	        mode = path.lstat().st_mode
86	    except FileNotFoundError:
87	        return "absent"
88	    if stat.S_ISLNK(mode):
89	        return "link"
90	    if stat.S_ISDIR(mode):
91	        return "dir"
92	    if stat.S_ISREG(mode):
93	        return "file"
94	    return "other"
95	
96	
97	def link_target(path):
98	    return Path(os.path.abspath(path.parent / os.readlink(path)))
99	
100	
101	def reject(path, destination=None):
102	    detail = "\n" + str(path)
103	    if destination is not None:
104	        detail += "\n" + str(destination)
105	    raise Refused("Existing Dolphin data needs attention. Back up these locations, then use the file manager "
106	                  "to choose and arrange the saved data before trying again. No saved data was removed." + detail)
107	
108	
109	def directories(path, boundary):
110	    # Missing descendants are fine; existing parents must not redirect traversal.
111	    if not path.is_relative_to(boundary):
112	        raise Refused("Dolphin storage path is outside its expected root.")
113	    for item in (boundary, *reversed(path.relative_to(boundary).parents)):
114	        if item == boundary:
115	            current = boundary
116	        else:
117	            current = boundary / item
118	        if kind(current) not in ("dir", "absent"):
119	            reject(current)
120	    if kind(path) not in ("dir", "absent"):
121	        reject(path)
122	
123	
124	def mounts():
125	    result = set()
126	    for line in Path("/proc/self/mountinfo").read_text().splitlines():
127	        field = line.split()[4]
128	        result.add(Path(re.sub(r"\\([0-7]{3})", lambda m: chr(int(m[1], 8)), field)))
129	    return result
130	
131	
132	def writable(path):
133	    current = path
134	    while kind(current) == "absent":
135	        current = current.parent
136	    # Mode check also catches a read-only player directory when the launcher is root.
137	    mode = current.stat().st_mode
138	    if not mode & 0o222 or not os.access(current, os.W_OK):
139	        raise Refused("Dolphin save storage is not writable. Check the game storage and folder permissions, then try again.\n" + str(path))
140	
141	
142	def plan(storage, system):
143	    conf = storage / ".config/dolphin-emu"
144	    roms = storage / "roms"
145	    shared = storage / ".local/share/dolphin-emu"
146	    mounted = mounts()
147	    if kind(storage) != "dir" or kind(roms) != "dir" or roms not in mounted:
148	        raise Refused("Game storage is not ready. Reconnect it and try again. No saved data was removed.")
149	    for path in (conf, roms / "savestates", roms / "bios/GC", shared.parent):
150	        directories(path, storage)
151	    # Do not rewrite a save path hidden behind a nested/bind mount.
152	    for mount in mounted:
153	        if any(mount == path or path in mount.parents for path in (conf, shared, roms / "savestates", roms / "bios")):
154	            raise Refused("A Dolphin save path is separately mounted. Check the storage layout before trying again.\n" + str(mount))
155	    directories(conf / "GC", storage)
156	    for temporary in (roms / "bios/.GC.dolphin-new", roms / "bios/GC/.Triforce.dolphin-new"):
157	        if kind(temporary) != "absent":
158	            reject(temporary)
159	    links = [(conf / "StateSaves", roms / "savestates" / system,
160	              (roms / "savestates/gamecube", roms / "savestates/wii")),
161	             (shared, conf, (conf,))]
162	    dirs = [roms / "savestates" / system, roms / "bios/GC", conf / "GC", shared.parent]
163	    for name in ("gamecube", "wii"):
164	        directories(roms / "savestates" / name, storage)
165	    for region in REGIONS:
166	        canonical = roms / "bios/GC" / region
167	        directories(canonical, storage)
168	        dirs.append(canonical)
169	        links.append((conf / "GC" / region, canonical, (canonical,)))
170	        for slot in ("A", "B"):
171	            card = "MemoryCard" + slot + "." + region + ".raw"
172	            canonical = roms / "bios/GC" / card
173	            if kind(canonical) not in ("absent", "file"):
174	                reject(canonical)
175	            if kind(canonical) == "file":
176	                writable(canonical)
177	            links.append((conf / "GC" / card, canonical, (canonical,)))
178	    directories(conf / "GC", storage)
179	    directories(roms / "bios/GC/Triforce", storage)
180	    for source, destination, allowed in links:
181	        value = kind(source)
182	        if value == "link":
183	            if link_target(source) not in allowed:
184	                reject(source, destination)
185	        elif value != "absent":
186	            # A real StateSaves tree has no reliable GC/Wii ownership tag. Even
187	            # equal-looking region/card copies need an explicit retention choice.
188	            reject(source, destination)
189	    pending = conf / ".dolphin-state-link"
190	    if kind(pending) != "absent" and (kind(pending) != "link" or link_target(pending) not in links[0][2]):
191	        reject(pending, conf / "StateSaves")
192	    for path in (*dirs, conf, shared.parent):
193	        writable(path)
194	    return conf, roms, dirs, links, pending
195	
196	
197	def copy_new_tree(source, target, skip=()):
198	    # Historical GC/Triforce seeding is copy-only and only to an absent target.
199	    # A killed copy leaves one reserved stage and refuses retry until reviewed.
200	    # Canonical data is never replaced, and the original config tree stays intact.
201	    # Shipped resources are real files; refuse retained redirects before copying.
202	    if kind(source) == "absent":
203	        target.mkdir()
204	        return
205	    if kind(source) != "dir":
206	        reject(source, target)
207	    count = total = 0
208	    def unreadable(error):
209	        raise error
210	
211	    for base, dirs, files in os.walk(source, followlinks=False, onerror=unreadable):
212	        if Path(base) == source:
213	            dirs[:] = [name for name in dirs if name not in skip]
214	            files = [name for name in files if name not in skip]
215	        for name in dirs + files:
216	            path = Path(base) / name
217	            if kind(path) not in ("dir", "file"):
218	                reject(path, target)
219	            count += 1
220	            if kind(path) == "file":
221	                total += path.lstat().st_size
222	            if count > MAX_COPY_FILES or total > MAX_COPY_BYTES:
223	                raise Refused("Dolphin's retained GC resources exceed the preparation limit. Arrange them in the file manager before trying again.")
224	    temporary = target.parent / ("." + target.name + ".dolphin-new")
225	    temporary.mkdir(mode=0o700)
226	    owned = temporary.lstat()
227	    try:
228	        shutil.copytree(source, temporary, symlinks=True, dirs_exist_ok=True,
229	                        ignore=lambda base, names: set(skip) if Path(base) == source else set())
230	        rename(temporary, target, 1)  # RENAME_NOREPLACE: canonical data wins a race.
231	    finally:
232	        if kind(temporary) != "absent":
233	            current = temporary.lstat()
234	            if (current.st_dev, current.st_ino) != (owned.st_dev, owned.st_ino) or kind(temporary) != "dir":
235	                reject(temporary)
236	            if any(m == temporary or temporary in m.parents for m in mounts()):
237	                reject(temporary)
238	            shutil.rmtree(temporary)  # Only this invocation's private, unactivated copy.
239	
240	
241	def rename(first, second, flags):
242	    libc = ctypes.CDLL(None, use_errno=True)
243	    operation = libc.renameat2
244	    operation.argtypes = [ctypes.c_int, ctypes.c_char_p, ctypes.c_int, ctypes.c_char_p, ctypes.c_uint]
245	    operation.restype = ctypes.c_int
246	    if operation(-100, os.fsencode(first), -100, os.fsencode(second), flags):
247	        raise OSError(ctypes.get_errno(), "Could not switch Dolphin's save-state link")
248	
249	
250	def apply(storage, system):
251	    conf, roms, dirs, links, pending = plan(storage, system)
252	    if kind(conf) != "dir":
253	        raise Refused("Dolphin configuration is missing. Check the installed defaults before trying again.")
254	    # Seed only an absent GC root, retaining the existing launchers' resource copy.
255	    (roms / "bios").mkdir(exist_ok=True)
256	    if kind(roms / "bios/GC") == "absent":
257	        managed = (*REGIONS, *("MemoryCard" + slot + "." + region + ".raw"
258	                              for region in REGIONS for slot in ("A", "B")))
259	        copy_new_tree(conf / "GC", roms / "bios/GC", skip=managed)
260	    if system == "gamecube" and kind(roms / "bios/GC/Triforce") == "absent":
261	        copy_new_tree(conf / "GC/Triforce", roms / "bios/GC/Triforce")
262	    for directory in dirs:
263	        directory.mkdir(parents=True, exist_ok=True)
264	    if kind(pending) == "link":
265	        if link_target(pending) not in links[0][2]:
266	            reject(pending, conf / "StateSaves")
267	        pending.unlink()  # Only a recognized leftover symlink; never its target.
268	    for source, destination, allowed in links:
269	        value = kind(source)
270	        if value == "absent":
271	            source.symlink_to(destination)  # Exclusive creation; never overwrites a racing entry.
272	        elif value == "link" and link_target(source) == destination:
273	            continue
274	        elif source == conf / "StateSaves" and value == "link" and link_target(source) in allowed:
275	            previous = source.lstat()
276	            pending.symlink_to(destination)
277	            rename(pending, source, 2)  # RENAME_EXCHANGE keeps the displaced object.
278	            moved = pending.lstat()
279	            if (moved.st_dev, moved.st_ino) != (previous.st_dev, previous.st_ino) or kind(pending) != "link":
280	                # Keep the unexpected object; do not delete data moved by a race.
281	                # Refusal identifies the reserved path for explicit recovery.
282	                reject(pending, source)
283	            pending.unlink()
284	        else:
285	            reject(source, destination)
286	
287	
288	def write_error(path, message):
289	    # ES already consumes this native launch-error file on exit 250.
290	    fd, temporary = tempfile.mkstemp(prefix=".dolphin-launch-error-", dir=path.parent)
291	    try:
292	        with os.fdopen(fd, "w", encoding="utf-8", errors="backslashreplace") as stream:
293	            stream.write(ERROR_OWNER + "\n" + visible_error(message))
294	        os.replace(temporary, path)
295	    finally:
296	        if os.path.lexists(temporary):
297	            os.unlink(temporary)
298	
299	
300	def interrupted(signum, frame):
301	    raise Refused("Dolphin save preparation was interrupted. Saved data was kept. Try again.")
302	
303	
304	def main():
305	    parser = argparse.ArgumentParser(description=__doc__)
306	    parser.add_argument("phase", choices=("check", "prepare"))
307	    parser.add_argument("system", choices=("gamecube", "wii"))
308	    parser.add_argument("--storage", type=Path, default=Path("/storage"))
309	    parser.add_argument("--lock", type=Path, default=Path("/run/dolphin-save-paths.lock"))
310	    parser.add_argument("--error-file", type=Path, default=Path("/tmp/launch_error.log"))
311	    args = parser.parse_args()
312	    try:
313	        for sig in (signal.SIGINT, signal.SIGTERM, signal.SIGHUP, signal.SIGALRM):
314	            signal.signal(sig, interrupted)
315	        signal.alarm(30)
316	        storage = Path(os.path.abspath(args.storage))
317	        fd = os.open(args.lock, os.O_CREAT | os.O_RDWR | os.O_NOFOLLOW | os.O_NONBLOCK, 0o600)
318	        try:
319	            if not stat.S_ISREG(os.fstat(fd).st_mode):
320	                raise Refused("Dolphin save preparation lock is unavailable. Try again after the other launch finishes.")
321	            try:
322	                fcntl.flock(fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
323	            except BlockingIOError:
324	                raise Refused("Dolphin save preparation is already running. Wait for it to finish, then try again.") from None
325	            if args.phase == "check":
326	                plan(storage, args.system)
327	            else:
328	                apply(storage, args.system)
329	        finally:
330	            os.close(fd)
331	        return 0
332	    except Exception as error:
333	        message = str(error) if isinstance(error, Refused) else "Dolphin could not prepare save storage. Check the storage connection and permissions, then try again. Saved data was kept."
334	        print(message, file=sys.stderr)
335	        print("Dolphin preparation detail: " + str(error), file=sys.stderr)
336	        try:
337	            write_error(args.error_file, message)
338	        except OSError:
339	            print("Could not write the native launch error message.", file=sys.stderr)
340	        return 250
341	    finally:
342	        signal.alarm(0)
343	
344	
345	if __name__ == "__main__":
346	    sys.exit(main())
```

### `projects/ROCKNIX/packages/emulators/standalone/dolphin-sa/scripts/start_dolphin_gc.sh`

```
1	#!/bin/bash
2	
3	# SPDX-License-Identifier: GPL-2.0-or-later
4	# Copyright (C) 2024-present ROCKNIX (https://github.com/ROCKNIX)
5	
6	. /etc/profile
7	
8	# Detect version of Dolphin
9	DOLPHIN_CORE=$(echo "${3}"| sed "s#^/.*/##")
10	if [ "${DOLPHIN_CORE}" = 'dolphin-qt-gc' ]; then
11	  DOLPHIN_CORE="dolphin-emu"
12	else
13	  DOLPHIN_CORE="dolphin-emu-nogui"
14	fi
15	
16	set_kill set "-9 ${DOLPHIN_CORE}"
17	
18	# control-gen supplies param_device and the SDL controller database
19	control-gen_init.sh
20	source /storage/.config/gptokeyb/control.ini
21	get_controls
22	
23	# Conf files vars
24	CONF_DIR="/storage/.config/dolphin-emu"
25	DOLPHIN_INI="Dolphin.ini"
26	GFX_INI="GFX.ini"
27	CONTROLLER_INI="GCPadNew.ini"
28	
29	# Refuse ambiguous retained save paths before any configuration preparation.
30	if ! /usr/bin/python3 -I -S -B /usr/bin/dolphin-save-paths check gamecube; then
31	  exit 250
32	fi
33	
34	# Dolphin writes its shader and pipeline caches here but will not create the
35	# directory itself, so an orderly shutdown had nothing to flush into.
36	mkdir -p "/storage/.cache/dolphin-emu"
37	
38	# Check if dolphin-emu exists in .config
39	if [ ! -d "${CONF_DIR}" ]; then
40	        cp -r "/usr/config/dolphin-emu" "/storage/.config/"
41	fi
42	
43	# Check if Hotkeys.ini exists
44	if [ "${DOLPHIN_CORE}" = 'dolphin-emu' ]; then
45	  if [ ! -f "${CONF_DIR}/Hotkeys.ini" ]; then
46	        cp -r "/usr/config/dolphin-emu/Hotkeys.ini" "${CONF_DIR}/"
47	  fi
48	fi
49	
50	# Check if GC controller dir exists in .config/dolphin-emu/GamecubeControllerProfiles
51	if [ ! -d "${CONF_DIR}/GamecubeControllerProfiles" ]; then
52	        cp -r "/usr/config/dolphin-emu/GamecubeControllerProfiles" "${CONF_DIR}/"
53	fi
54	
55	# Check if each stock profile exists in .config/dolphin-emu/GamecubeControllerProfiles
56	for PROFILE in east.stacked east.inline south.stacked south.inline; do
57	        if [ ! -f "${CONF_DIR}/GamecubeControllerProfiles/GCPadNew.ini.${PROFILE}" ]; then
58	                cp -r "/usr/config/dolphin-emu/GamecubeControllerProfiles/GCPadNew.ini.${PROFILE}" "${CONF_DIR}/GamecubeControllerProfiles/GCPadNew.ini.${PROFILE}"
59	        fi
60	done
61	
62	# Check if GC custom controller profile exists in .config/dolphin-emu/GamecubeControllerProfiles
63	if [ ! -f "${CONF_DIR}/GamecubeControllerProfiles/GCPadNew.ini.custom" ]; then
64	        cp -r "/usr/config/dolphin-emu/GamecubeControllerProfiles/GCPadNew.ini.south.stacked" "${CONF_DIR}/GamecubeControllerProfiles/GCPadNew.ini.custom"
65	fi
66	
67	# Prepare only known save links; retained real data requires an explicit choice.
68	if ! /usr/bin/python3 -I -S -B /usr/bin/dolphin-save-paths prepare gamecube; then
69	  exit 250
70	fi
71	
72	# Make sure all Triforce Gecko codes are copied to GameSettings
73	for f in /usr/config/dolphin-emu/triforce_gecko_codes/*; do
74	  [ -e "/storage/.config/dolphin-emu/GameSettings/$(basename "$f")" ] || cp -fH "$f" "/storage/.config/dolphin-emu/GameSettings/"
75	done
76	rm -rf "/storage/.config/dolphin-emu/triforce_gecko_codes"
77	
78	# Emulation Station Features
79	GAME=$(echo "${1}"| sed "s#^/.*/##")
80	PLATFORM=$(echo "${2}"| sed "s#^/.*/##")
81	AA=$(get_setting anti_aliasing "${PLATFORM}" "${GAME}")
82	ASPECT=$(get_setting aspect_ratio "${PLATFORM}" "${GAME}")
83	AUDIOBE=$(get_setting audio_backend "${PLATFORM}" "${GAME}")
84	ASWAPDISCS=$(get_setting auto_swap_discs "${PLATFORM}" "${GAME}")
85	CLOCK=$(get_setting clock_speed "${PLATFORM}" "${GAME}")
86	ENBCHEATS=$(get_setting enable_cheats "${PLATFORM}" "${GAME}")
87	GRENDERER=$(get_setting graphics_backend "${PLATFORM}" "${GAME}")
88	IRES=$(get_setting internal_resolution "${PLATFORM}" "${GAME}")
89	FPS=$(get_setting show_fps "${PLATFORM}" "${GAME}")
90	CON=$(get_setting gamecube_controller_profile "${PLATFORM}" "${GAME}")
91	SWAPSHOULDER=$(get_setting swap_shoulders "${PLATFORM}" "${GAME}")
92	HKEY=$(get_setting hotkey_enable_button "${PLATFORM}" "${GAME}")
93	SAVETYPE=$(get_setting save_type "${PLATFORM}" "${GAME}")
94	SAVEREG=$(get_setting save_gci_region "${PLATFORM}" "${GAME}")
95	SHADERM=$(get_setting shader_mode "${PLATFORM}" "${GAME}")
96	SHADERP=$(get_setting shader_precompile "${PLATFORM}" "${GAME}")
97	VSYNC=$(get_setting vsync "${PLATFORM}" "${GAME}")
98	SKIPBIOS=$(get_setting use_bios "${PLATFORM}" "${GAME}")
99	EFBACCESS=$(get_setting skip_efb_cpu_access "${PLATFORM}" "${GAME}")
100	EFBTEXTURE=$(get_setting store_efb_to_texture_only "${PLATFORM}" "${GAME}")
101	XFBTEXTURE=$(get_setting store_xfb_to_texture_only "${PLATFORM}" "${GAME}")
102	TEXTURE_CACHE_ACCURACY=$(get_setting texture_cache_accuracy "${PLATFORM}" "${GAME}")
103	SYNC_GPU_THREAD=$(get_setting sync_gpu_thread "${PLATFORM}" "${GAME}")
104	RUMBLE=$(get_setting rumble "${PLATFORM}" "${GAME}")
105	WHACK=$(get_setting widescreen_hack "${PLATFORM}" "${GAME}")
106	WPC=$(get_setting write_protect_configs "${PLATFORM}" "${GAME}")
107	
108	# Grab clean config files during boot, unless disabled in emulationstation
109	if [ "$WPC" != "false" ]; then
110	  cp -r /usr/config/dolphin-emu/GFX.ini ${CONF_DIR}/${GFX_INI}
111	  cp -r /usr/config/dolphin-emu/Dolphin.ini ${CONF_DIR}/${DOLPHIN_INI}
112	fi
113	
114	# Set the cores to use
115	CORES=$(get_setting "cores" "${PLATFORM}" "${GAME}")
116	if [ "${CORES}" = "little" ]
117	then
118	  EMUPERF="${SLOW_CORES}"
119	elif [ "${CORES}" = "big" ]
120	then
121	  EMUPERF="${FAST_CORES}"
122	else
123	  ### All..
124	  unset EMUPERF
125	fi
126	
127	### Emulation Station features:
128	  # Anti-Aliasing
129	  if [ "$AA" = "2m" ]; then
130	    sed -i '/MSAA/c\MSAA = 2' ${CONF_DIR}/${GFX_INI}
131	    sed -i '/SSAA/c\SSAA = False' ${CONF_DIR}/${GFX_INI}
132	  elif [ "$AA" = "2s" ]; then
133	    sed -i '/MSAA/c\MSAA = 2' ${CONF_DIR}/${GFX_INI}
134	    sed -i '/SSAA/c\SSAA = True' ${CONF_DIR}/${GFX_INI}
135	  elif [ "$AA" = "4m" ]; then
136	    sed -i '/MSAA/c\MSAA = 4' ${CONF_DIR}/${GFX_INI}
137	    sed -i '/SSAA/c\SSAA = False' ${CONF_DIR}/${GFX_INI}
138	  elif [ "$AA" = "4s" ]; then
139	    sed -i '/MSAA/c\MSAA = 4' ${CONF_DIR}/${GFX_INI}
140	    sed -i '/SSAA/c\SSAA = True' ${CONF_DIR}/${GFX_INI}
141	  elif [ "$AA" = "8m" ]; then
142	    sed -i '/MSAA/c\MSAA = 8' ${CONF_DIR}/${GFX_INI}
143	    sed -i '/SSAA/c\SSAA = False' ${CONF_DIR}/${GFX_INI}
144	  elif [ "$AA" = "8s" ]; then
145	    sed -i '/MSAA/c\MSAA = 8' ${CONF_DIR}/${GFX_INI}
146	    sed -i '/SSAA/c\SSAA = True' ${CONF_DIR}/${GFX_INI}
147	  else
148	    sed -i '/MSAA/c\MSAA = 0' ${CONF_DIR}/${GFX_INI}
149	    sed -i '/SSAA/c\SSAA = False' ${CONF_DIR}/${GFX_INI}
150	  fi
151	
152	  # Aspect Ratio
153	  if [ "$ASPECT" = "1" ]; then
154	    sed -i '/AspectRatio/c\AspectRatio = 1' ${CONF_DIR}/${GFX_INI}
155	  elif [ "$ASPECT" = "2" ]; then
156	    sed -i '/AspectRatio/c\AspectRatio = 2' ${CONF_DIR}/${GFX_INI}
157	  elif [ "$ASPECT" = "3" ]; then
158	    sed -i '/AspectRatio/c\AspectRatio = 3' ${CONF_DIR}/${GFX_INI}
159	  else
160	    sed -i '/AspectRatio/c\AspectRatio = 0' ${CONF_DIR}/${GFX_INI}
161	  fi
162	
163	  # Audio Backend
164	  if [ "$AUDIOBE" = "lle" ]; then
165	    AUDIO_BACKEND="LLE"
166	  else
167	    AUDIO_BACKEND="HLE"
168	  fi
169	
170	  # Auto Swap Discs
171	  if [ "$ASWAPDISCS" = "0" ]; then
172	    sed -i '/AutoDiscChange/c\AutoDiscChange = False' ${CONF_DIR}/${DOLPHIN_INI}
173	  else
174	    sed -i '/AutoDiscChange/c\AutoDiscChange = True' ${CONF_DIR}/${DOLPHIN_INI}
175	  fi
176	
177	  # Clock Speed
178	  if [ "$CLOCK" = "050" ]; then
179	    sed -i '/^Overclock =/c\Overclock = 0.5' ${CONF_DIR}/${DOLPHIN_INI}
180	    sed -i '/^OverclockEnable =/c\OverclockEnable = True' ${CONF_DIR}/${DOLPHIN_INI}
181	  elif [ "$CLOCK" = "075" ]; then
182	    sed -i '/^Overclock =/c\Overclock = 0.75' ${CONF_DIR}/${DOLPHIN_INI}
183	    sed -i '/^OverclockEnable =/c\OverclockEnable = True' ${CONF_DIR}/${DOLPHIN_INI}
184	  elif [ "$CLOCK" = "100" ]; then
185	    sed -i '/^Overclock =/c\Overclock = 1.0' ${CONF_DIR}/${DOLPHIN_INI}
186	    sed -i '/^OverclockEnable =/c\OverclockEnable = False' ${CONF_DIR}/${DOLPHIN_INI}
187	  elif [ "$CLOCK" = "125" ]; then
188	    sed -i '/^Overclock =/c\Overclock = 1.25' ${CONF_DIR}/${DOLPHIN_INI}
189	    sed -i '/^OverclockEnable =/c\OverclockEnable = True' ${CONF_DIR}/${DOLPHIN_INI}
190	  elif [ "$CLOCK" = "150" ]; then
191	    sed -i '/^Overclock =/c\Overclock = 1.5' ${CONF_DIR}/${DOLPHIN_INI}
192	    sed -i '/^OverclockEnable =/c\OverclockEnable = True' ${CONF_DIR}/${DOLPHIN_INI}
193	  elif [ "$CLOCK" = "200" ]; then
194	    sed -i '/^Overclock =/c\Overclock = 2.0' ${CONF_DIR}/${DOLPHIN_INI}
195	    sed -i '/^OverclockEnable =/c\OverclockEnable = True' ${CONF_DIR}/${DOLPHIN_INI}
196	  elif [ "$CLOCK" = "300" ]; then
197	    sed -i '/^Overclock =/c\Overclock = 3.0' ${CONF_DIR}/${DOLPHIN_INI}
198	    sed -i '/^OverclockEnable =/c\OverclockEnable = True' ${CONF_DIR}/${DOLPHIN_INI}
199	  elif [ "$CLOCK" = "400" ]; then
200	    sed -i '/^Overclock =/c\Overclock = 4.0' ${CONF_DIR}/${DOLPHIN_INI}
201	    sed -i '/^OverclockEnable =/c\OverclockEnable = True' ${CONF_DIR}/${DOLPHIN_INI}
202	  else
203	    sed -i '/^OverclockEnable =/c\OverclockEnable = False' ${CONF_DIR}/${DOLPHIN_INI}
204	  fi
205	
206	  # Enable Cheats
207	  if [ "$ENBCHEATS" = "1" ]; then
208	    sed -i '/EnableCheats/c\EnableCheats = True' ${CONF_DIR}/${DOLPHIN_INI}
209	  else
210	    sed -i '/EnableCheats/c\EnableCheats = False' ${CONF_DIR}/${DOLPHIN_INI}
211	  fi
212	
213	  # Graphics Backend
214	  if [ "$GRENDERER" = "vulkan" ]; then
215	    sed -i '/GFXBackend/c\GFXBackend = Vulkan' ${CONF_DIR}/${DOLPHIN_INI}
216	  elif [ "$GRENDERER" = "opengl" ]; then
217	    sed -i '/GFXBackend/c\GFXBackend = OGL' ${CONF_DIR}/${DOLPHIN_INI}
218	  else
219	    sed -i '/GFXBackend/c\GFXBackend = @GRENDERER@' ${CONF_DIR}/${DOLPHIN_INI}
220	  fi
221	
222	  # Sync GPU thread
223	  if [ "$SYNC_GPU_THREAD" = "true" ]; then
224	    sed -i '/SyncGPU =/c\SyncGPU = True' ${CONF_DIR}/${DOLPHIN_INI}
225	  else
226	    sed -i '/SyncGPU =/c\SyncGPU = False' ${CONF_DIR}/${DOLPHIN_INI}
227	  fi
228	
229	  # Internal Resolution
230	  if [ "$IRES" = "1" ]; then
231	    sed -i '/InternalResolution/c\InternalResolution = 1' ${CONF_DIR}/${GFX_INI}
232	  elif [ "$IRES" = "3" ]; then
233	    sed -i '/InternalResolution/c\InternalResolution = 3' ${CONF_DIR}/${GFX_INI}
234	  elif [ "$IRES" = "4" ]; then
235	    sed -i '/InternalResolution/c\InternalResolution = 4' ${CONF_DIR}/${GFX_INI}
236	  elif [ "$IRES" = "6" ]; then
237	    sed -i '/InternalResolution/c\InternalResolution = 6' ${CONF_DIR}/${GFX_INI}
238	  else
239	    sed -i '/InternalResolution/c\InternalResolution = 2' ${CONF_DIR}/${GFX_INI}
240	  fi
241	
242	  # Save Type
243	  if [ "$SAVETYPE" = "8" ]; then
244	    sed -i '/SlotA/c\SlotA = 8' ${CONF_DIR}/${DOLPHIN_INI}
245	  else
246	    sed -i '/SlotA/c\SlotA = 1' ${CONF_DIR}/${DOLPHIN_INI}
247	  fi
248	
249	  # Save Reg
250	  if [ "$SAVEREG" = "eur" ]; then
251	    sed -i '/GCIFolderAPath/c\GCIFolderAPath = \/storage\/roms\/bios\/GC\/EUR' ${CONF_DIR}/${DOLPHIN_INI}
252	  elif [ "$SAVEREG" = "jap" ]; then
253	    sed -i '/GCIFolderAPath/c\GCIFolderAPath = \/storage\/roms\/bios\/GC\/JAP' ${CONF_DIR}/${DOLPHIN_INI}
254	  else
255	    sed -i '/GCIFolderAPath/c\GCIFolderAPath = \/storage\/roms\/bios\/GC\/USA' ${CONF_DIR}/${DOLPHIN_INI}
256	  fi
257	
258	  # Shader Mode
259	  if [ "$SHADERM" = "0" ]; then
260	    sed -i '/ShaderCompilationMode =/c\ShaderCompilationMode = 0' ${CONF_DIR}/${GFX_INI}
261	  elif [ "$SHADERM" = "1" ]; then
262	    sed -i '/ShaderCompilationMode =/c\ShaderCompilationMode = 1' ${CONF_DIR}/${GFX_INI}
263	  elif [ "$SHADERM" = "2" ]; then
264	    sed -i '/ShaderCompilationMode =/c\ShaderCompilationMode = 2' ${CONF_DIR}/${GFX_INI}
265	  elif [ "$SHADERM" = "3" ]; then
266	    sed -i '/ShaderCompilationMode =/c\ShaderCompilationMode = 3' ${CONF_DIR}/${GFX_INI}
267	  fi
268	
269	  #Shader Precompile
270	  if [ "$SHADERP" = "false" ]; then
271	    sed -i '/WaitForShadersBeforeStarting =/c\WaitForShadersBeforeStarting = False' ${CONF_DIR}/${GFX_INI}
272	  elif [ "$SHADERP" = "true" ]; then
273	    sed -i '/WaitForShadersBeforeStarting =/c\WaitForShadersBeforeStarting = True' ${CONF_DIR}/${GFX_INI}
274	  fi
275	
276	  # Show FPS
277	  if [ "$FPS" = "true" ]; then
278	    sed -i '/ShowFPS/c\ShowFPS = True' ${CONF_DIR}/${GFX_INI}
279	  else
280	    sed -i '/ShowFPS/c\ShowFPS = False' ${CONF_DIR}/${GFX_INI}
281	  fi
282	
283	  # Skip Bios
284	  if [ "$SKIPBIOS" = "false" ]; then
285	    sed -i '/SkipIPL/c\SkipIPL = False' ${CONF_DIR}/${DOLPHIN_INI}
286	  else
287	    sed -i '/SkipIPL/c\SkipIPL = True' ${CONF_DIR}/${DOLPHIN_INI}
288	  fi
289	
290	  # Skip EFB CPU Access
291	  if [ "$EFBACCESS" = "false" ]; then
292	    sed -i '/EFBAccessEnable =/c\EFBAccessEnable = False' ${CONF_DIR}/${GFX_INI}
293	  else
294	    sed -i '/EFBAccessEnable =/c\EFBAccessEnable = True' ${CONF_DIR}/${GFX_INI}
295	  fi
296	
297	  # Store EFB to texture only
298	  if [ "$EFBTEXTURE" = "false" ]; then
299	    sed -i '/EFBToTextureEnable =/c\EFBToTextureEnable = False' ${CONF_DIR}/${GFX_INI}
300	  else
301	    sed -i '/EFBToTextureEnable =/c\EFBToTextureEnable = True' ${CONF_DIR}/${GFX_INI}
302	  fi
303	
304	  # Store XFB to texture only
305	  if [ "$XFBTEXTURE" = "false" ]; then
306	    sed -i '/XFBToTextureEnable =/c\XFBToTextureEnable = False' ${CONF_DIR}/${GFX_INI}
307	  else
308	    sed -i '/XFBToTextureEnable =/c\XFBToTextureEnable = True' ${CONF_DIR}/${GFX_INI}
309	  fi
310	
311	  # Texture cache accuracy
312	  if [ "$TEXTURE_CACHE_ACCURACY" = "0" ]; then
313	    sed -i '/SafeTextureCacheColorSamples =/c\SafeTextureCacheColorSamples = 0' ${CONF_DIR}/${GFX_INI}
314	  elif [ "$TEXTURE_CACHE_ACCURACY" = "512" ]; then
315	    sed -i '/SafeTextureCacheColorSamples =/c\SafeTextureCacheColorSamples = 512' ${CONF_DIR}/${GFX_INI}
316	  else
317	    # Default to 128 = fast
318	    sed -i '/SafeTextureCacheColorSamples =/c\SafeTextureCacheColorSamples = 128' ${CONF_DIR}/${GFX_INI}
319	  fi
320	
321	  # Widescreen Hack
322	  if [ "$WHACK" = "true" ]; then
323	    sed -i '/wideScreenHack =/c\wideScreenHack = True' ${CONF_DIR}/${GFX_INI}
324	  else
325	    sed -i '/wideScreenHack =/c\wideScreenHack = False' ${CONF_DIR}/${GFX_INI}
326	  fi
327	
328	  # GC Controller Profile
329	  # Devices with inline shoulders want L/R on the bumpers and Z on the analog
330	  # trigger, which is the reverse of the stacked layout actual hardware uses.
331	  if [ "$SWAPSHOULDER" = "true" ]; then
332	    SHOULDERS="inline"
333	  else
334	    SHOULDERS="stacked"
335	  fi
336	
337	  if [ "$CON" = "east" ]; then
338	    cp -r ${CONF_DIR}/GamecubeControllerProfiles/GCPadNew.ini.east.${SHOULDERS} ${CONF_DIR}/${CONTROLLER_INI}
339	  elif [ "$CON" = "custom" ]; then
340	    cp -r ${CONF_DIR}/GamecubeControllerProfiles/GCPadNew.ini.custom ${CONF_DIR}/${CONTROLLER_INI}
341	  else
342	    cp -r ${CONF_DIR}/GamecubeControllerProfiles/GCPadNew.ini.south.${SHOULDERS} ${CONF_DIR}/${CONTROLLER_INI}
343	  fi
344	
345	  # GC Controller Rumble
346	  if [ "$RUMBLE" = "false" ]; then
347	    sed -i '/^Rumble/d' ${CONF_DIR}/${CONTROLLER_INI}
348	  fi
349	
350	  # GC Controller Hotkey Enable
351	  if [ "$HKEY" = "mode" ]; then
352	    sed -i '/^Buttons\/Hotkey =/c\Buttons\/Hotkey = Guide' ${CONF_DIR}/${CONTROLLER_INI}
353	  else
354	    sed -i '/^Buttons\/Hotkey =/c\Buttons\/Hotkey = Back' ${CONF_DIR}/${CONTROLLER_INI}
355	  fi
356	
357	  # Qt reads its combos from Hotkeys.ini instead of Buttons/Hotkey, so the same
358	  # setting has to be swapped into the modifier half of every binding there.
359	  if [ -f "${CONF_DIR}/Hotkeys.ini" ]; then
360	    if [ "$HKEY" = "mode" ]; then
361	      sed -i 's/`Back`/`Guide`/g' ${CONF_DIR}/Hotkeys.ini
362	    else
363	      sed -i 's/`Guide`/`Back`/g' ${CONF_DIR}/Hotkeys.ini
364	    fi
365	  fi
366	
367	  # Vsync
368	  if [ "$VSYNC" = "1" ]; then
369	    sed -i '/VSync =/c\VSync = True' ${CONF_DIR}/${GFX_INI}
370	  else
371	    sed -i '/VSync =/c\VSync = False' ${CONF_DIR}/${GFX_INI}
372	  fi
373	
374	# SDL names a gamepad after the mapping it resolves, which is not always the
375	# joystick name control-gen reports.
376	SDL_DB="${SDL_GAMECONTROLLERCONFIG_FILE:-/storage/.config/gptokeyb/gamecontrollerdb.txt}"
377	SDL_DEVICE="${param_device}"
378	MAPLINE=""
379	if [ -n "${DEVICE}" ] && [ -f "${SDL_DB}" ]; then
380	  GUID_KEY="$(echo "${DEVICE}" | cut -c1-4)0000$(echo "${DEVICE}" | cut -c9-)"
381	  MAPLINE="$(awk -F, -v d="${DEVICE}" -v k="${GUID_KEY}" '!/^#/ && NF>1 {
382	      if ($1 == d) { exact = $0; exit }
383	      if (loose == "" && substr($1,5,4) == "0000") {
384	        g = substr($1,1,4) "0000" substr($1,9)
385	        if (g == k) { loose = $0 }
386	      }
387	    }
388	    END { print (exact != "" ? exact : loose) }' "${SDL_DB}")"
389	  MAPPED="$(echo "${MAPLINE}" | cut -d, -f2)"
390	  [ -n "${MAPPED}" ] && SDL_DEVICE="${MAPPED}"
391	fi
392	
393	# Some SDL strings are set for XBox-style, even though they're physically Nintendo-style
394	# so we need to check for that and set a flag if so.
395	FACE_SWAP="no"
396	if [ -n "${MAPLINE}" ]; then
397	  A_BTN="$(echo "${MAPLINE}" | tr ',' '\n' | sed -n 's/^a:b\([0-9]\{1,\}\)$/\1/p')"
398	  B_BTN="$(echo "${MAPLINE}" | tr ',' '\n' | sed -n 's/^b:b\([0-9]\{1,\}\)$/\1/p')"
399	  if [ -n "${A_BTN}" ] && [ -n "${B_BTN}" ] && [ "${A_BTN}" -gt "${B_BTN}" ]; then
400	    FACE_SWAP="yes"
401	  fi
402	fi
403	
404	for CFG in "${CONF_DIR}/Hotkeys.ini" "${CONF_DIR}/GCPadNew.ini" "${CONF_DIR}/WiimoteNew.ini"; do
405	  [ -f "${CFG}" ] || continue
406	  sed -i "/^Device = /c\\Device = SDL/0/${SDL_DEVICE}" "${CFG}"
407	
408	  # A custom profile is whatever the user bound in Dolphin's own UI, which
409	  # already records what the pad really reports; only the shipped profiles are
410	  # written positionally and need correcting.
411	  if [ "${FACE_SWAP}" = "yes" ] && \
412	     ! { [ "${CON}" = "custom" ] && [ "${CFG}" = "${CONF_DIR}/${CONTROLLER_INI}" ]; }; then
413	    sed -i -e 's/`Button S`/`Button %`/g' \
414	           -e 's/`Button E`/`Button S`/g' \
415	           -e 's/`Button %`/`Button E`/g' \
416	           -e 's/`Button W`/`Button %`/g' \
417	           -e 's/`Button N`/`Button W`/g' \
418	           -e 's/`Button %`/`Button N`/g' "${CFG}"
419	  fi
420	done
421	
422	# The shared Dolphin data link was checked and prepared before settings writes.
423	
424	@EXPORTS@
425	
426	# Retroachievements
427	  /usr/bin/cheevos_dolphin.sh
428	  CHEEVOS_STATUS=$?
429	  # Disabled/logged-out is a valid launch only after the inactive INI is written.
430	  case "${CHEEVOS_STATUS}" in
431	    0|1) ;;
432	    *) exit "${CHEEVOS_STATUS}" ;;
433	  esac
434	
435	# Set video and audio backend
436	  CMD="${CMD} -v $GRENDERER"
437	
438	if [ ${DOLPHIN_CORE} = "dolphin-emu" ]; then
439	  CMD="-b -a ${AUDIO_BACKEND}"
440	else
441	  CMD="-p @DOLPHIN_BACKEND@ -a ${AUDIO_BACKEND}"
442	fi
443	
444	# Debugging info:
445	  echo "GAME set to: ${GAME}"
446	  echo "PLATFORM set to: ${PLATFORM}"
447	  echo "CPU CORES set to: ${EMUPERF}"
448	  echo "AA set to: ${AA}"
449	  echo "ASPECT set to: ${ASPECT}"
450	  echo "AUDIOBE set to: ${AUDIOBE}"
451	  echo "ASWAPDISCS set to: ${ASWAPDISCS}"
452	  echo "CLOCK set to: ${CLOCK}"
453	  echo "DOLPHIN_BACKEND set to: ${DOLPHIN_BACKEND}"
454	  echo "ENBCHEATS set to: ${ENBCHEATS}"
455	  echo "GRENDERER set to: ${GRENDERER}"
456	  echo "IRES set to: ${IRES}"
457	  echo "FPS set to: ${FPS}"
458	  echo "CON set to: ${CON}"
459	  echo "SWAPSHOULDER set to: ${SWAPSHOULDER}"
460	  echo "HKEY set to: ${HKEY}"
461	  echo "SAVETYPE set to: ${SAVETYPE}"
462	  echo "SAVEREG set to: ${SAVEREG}"
463	  echo "SHADERM set to: ${SHADERM}"
464	  echo "SHADERP set to: ${SHADERP}"
465	  echo "VSYNC set to: ${VSYNC}"
466	  echo "SKIPBIOS set to: ${SKIPBIOS}"
467	  echo "EFBACCESS set to: ${EFBACCESS}"
468	  echo "EFBTEXTURE set to: ${EFBTEXTURE}"
469	  echo "XFBTEXTURE set to: ${XFBTEXTURE}"
470	  echo "TEXTURE_CACHE_ACCURACY set to: ${TEXTURE_CACHE_ACCURACY}"
471	  echo "SYNC_GPU_THREAD set to: ${SYNC_GPU_THREAD}"
472	  echo "RUMBLE set to: ${RUMBLE}"
473	  echo "WHACK set to: ${WHACK}"
474	  echo "WPC set to: ${WPC}"
475	  echo "Launching /usr/bin/${DOLPHIN_CORE} ${CMD} -e ${1}"
476	
477	# Run Dolphin emulator
478	  ${EMUPERF} /usr/bin/${DOLPHIN_CORE} ${CMD} -e "${1}"
```

### `projects/ROCKNIX/packages/emulators/standalone/dolphin-sa/scripts/start_dolphin_wii.sh`

```
1	#!/bin/bash
2	
3	# SPDX-License-Identifier: GPL-2.0-or-later
4	# Copyright (C) 2024-present ROCKNIX (https://github.com/ROCKNIX)
5	
6	. /etc/profile
7	
8	# Detect version of Dolphin
9	DOLPHIN_CORE=$(echo "${3}"| sed "s#^/.*/##")
10	if [ "${DOLPHIN_CORE}" = 'dolphin-qt-wii' ]; then
11	  DOLPHIN_CORE="dolphin-emu"
12	else
13	  DOLPHIN_CORE="dolphin-emu-nogui"
14	fi
15	
16	set_kill set "-9 ${DOLPHIN_CORE}"
17	
18	# control-gen supplies param_device and the SDL controller database
19	control-gen_init.sh
20	source /storage/.config/gptokeyb/control.ini
21	get_controls
22	
23	# Conf files vars
24	CONF_DIR="/storage/.config/dolphin-emu"
25	DOLPHIN_INI="Dolphin.ini"
26	GFX_INI="GFX.ini"
27	GC_CONTROLLER_INI="GCPadNew.ini"
28	
29	# Refuse ambiguous retained save paths before any configuration preparation.
30	if ! /usr/bin/python3 -I -S -B /usr/bin/dolphin-save-paths check wii; then
31	  exit 250
32	fi
33	
34	# Dolphin writes its shader and pipeline caches here but will not create the
35	# directory itself, so an orderly shutdown had nothing to flush into.
36	mkdir -p "/storage/.cache/dolphin-emu"
37	
38	# Check if dolphin-emu exists in .config
39	if [ ! -d "${CONF_DIR}" ]; then
40	        cp -r "/usr/config/dolphin-emu" "/storage/.config/"
41	fi
42	
43	# Check if Hotkeys.ini exists
44	if [ "${DOLPHIN_CORE}" = 'dolphin-emu' ]; then
45	  if [ ! -f "${CONF_DIR}/Hotkeys.ini" ]; then
46	        cp -r "/usr/config/dolphin-emu/Hotkeys.ini" "${CONF_DIR}/"
47	  fi
48	fi
49	
50	# Check if GC controller dir exists in .config/dolphin-emu/GamecubeControllerProfiles
51	if [ ! -d "${CONF_DIR}/GamecubeControllerProfiles" ]; then
52	        cp -r "/usr/config/dolphin-emu/GamecubeControllerProfiles" "${CONF_DIR}/"
53	fi
54	
55	# Check if Wii controller dir exists in .config/dolphin-emu/WiiControllerProfiles
56	if [ ! -d "${CONF_DIR}/WiiControllerProfiles" ]; then
57	        cp -r "/usr/config/dolphin-emu/WiiControllerProfiles" "${CONF_DIR}/"
58	fi
59	
60	# Check if Wii custom controller profile exists in .config/dolphin-emu
61	if [ ! -f "${CONF_DIR}/WiiControllerProfiles/custom.ini" ]; then
62	        cp -r "${CONF_DIR}/WiiControllerProfiles/vremote.ini" "${CONF_DIR}/WiiControllerProfiles/custom.ini"
63	fi
64	
65	# Gamecube controller profile needed for hotkeys to work on SA
66	if [ "${DOLPHIN_CORE}" = 'dolphin-emu-nogui' ]; then
67	  cp -r "/storage/.config/dolphin-emu/GamecubeControllerProfiles/GCPadNew.ini.south.stacked" "/storage/.config/dolphin-emu/GCPadNew.ini"
68	else
69	  rm -r "/storage/.config/dolphin-emu/GCPadNew.ini"
70	fi
71	
72	# Prepare only known save links; retained real data requires an explicit choice.
73	if ! /usr/bin/python3 -I -S -B /usr/bin/dolphin-save-paths prepare wii; then
74	  exit 250
75	fi
76	
77	# Emulation Station Features
78	GAME=$(echo "${1}"| sed "s#^/.*/##")
79	PLATFORM=$(echo "${2}"| sed "s#^/.*/##")
80	AA=$(get_setting anti_aliasing "${PLATFORM}" "${GAME}")
81	ASPECT=$(get_setting aspect_ratio "${PLATFORM}" "${GAME}")
82	AUDIOBE=$(get_setting audio_backend "${PLATFORM}" "${GAME}")
83	CLOCK=$(get_setting clock_speed "${PLATFORM}" "${GAME}")
84	ENBCHEATS=$(get_setting enable_cheats "${PLATFORM}" "${GAME}")
85	GRENDERER=$(get_setting graphics_backend "${PLATFORM}" "${GAME}")
86	IRES=$(get_setting internal_resolution "${PLATFORM}" "${GAME}")
87	FPS=$(get_setting show_fps "${PLATFORM}" "${GAME}")
88	CON=$(get_setting wii_controller_profile "${PLATFORM}" "${GAME}")
89	HKEY=$(get_setting hotkey_enable_button "${PLATFORM}" "${GAME}")
90	SHADERM=$(get_setting shader_mode "${PLATFORM}" "${GAME}")
91	SHADERP=$(get_setting shader_precompile "${PLATFORM}" "${GAME}")
92	VSYNC=$(get_setting vsync "${PLATFORM}" "${GAME}")
93	EFBACCESS=$(get_setting skip_efb_cpu_access "${PLATFORM}" "${GAME}")
94	EFBTEXTURE=$(get_setting store_efb_to_texture_only "${PLATFORM}" "${GAME}")
95	XFBTEXTURE=$(get_setting store_xfb_to_texture_only "${PLATFORM}" "${GAME}")
96	TEXTURE_CACHE_ACCURACY=$(get_setting texture_cache_accuracy "${PLATFORM}" "${GAME}")
97	SYNC_GPU_THREAD=$(get_setting sync_gpu_thread "${PLATFORM}" "${GAME}")
98	RUMBLE=$(get_setting rumble "${PLATFORM}" "${GAME}")
99	WHACK=$(get_setting widescreen_hack "${PLATFORM}" "${GAME}")
100	WPC=$(get_setting write_protect_configs "${PLATFORM}" "${GAME}")
101	
102	# Grab clean config files during boot, unless disabled in emulationstation
103	if [ "$WPC" != "false" ]; then
104	  cp -r /usr/config/dolphin-emu/GFX.ini ${CONF_DIR}/${GFX_INI}
105	  cp -r /usr/config/dolphin-emu/Dolphin.ini ${CONF_DIR}/${DOLPHIN_INI}
106	fi
107	
108	# Set the cores to use
109	CORES=$(get_setting "cores" "${PLATFORM}" "${GAME}")
110	if [ "${CORES}" = "little" ]
111	then
112	  EMUPERF="${SLOW_CORES}"
113	elif [ "${CORES}" = "big" ]
114	then
115	  EMUPERF="${FAST_CORES}"
116	else
117	  ### All..
118	  unset EMUPERF
119	fi
120	
121	### Emulation Station features:
122	  # Anti-Aliasing
123	  if [ "$AA" = "2m" ]; then
124	    sed -i '/MSAA/c\MSAA = 2' ${CONF_DIR}/${GFX_INI}
125	    sed -i '/SSAA/c\SSAA = False' ${CONF_DIR}/${GFX_INI}
126	  elif [ "$AA" = "2s" ]; then
127	    sed -i '/MSAA/c\MSAA = 2' ${CONF_DIR}/${GFX_INI}
128	    sed -i '/SSAA/c\SSAA = True' ${CONF_DIR}/${GFX_INI}
129	  elif [ "$AA" = "4m" ]; then
130	    sed -i '/MSAA/c\MSAA = 4' ${CONF_DIR}/${GFX_INI}
131	    sed -i '/SSAA/c\SSAA = False' ${CONF_DIR}/${GFX_INI}
132	  elif [ "$AA" = "4s" ]; then
133	    sed -i '/MSAA/c\MSAA = 4' ${CONF_DIR}/${GFX_INI}
134	    sed -i '/SSAA/c\SSAA = True' ${CONF_DIR}/${GFX_INI}
135	  elif [ "$AA" = "8m" ]; then
136	    sed -i '/MSAA/c\MSAA = 8' ${CONF_DIR}/${GFX_INI}
137	    sed -i '/SSAA/c\SSAA = False' ${CONF_DIR}/${GFX_INI}
138	  elif [ "$AA" = "8s" ]; then
139	    sed -i '/MSAA/c\MSAA = 8' ${CONF_DIR}/${GFX_INI}
140	    sed -i '/SSAA/c\SSAA = True' ${CONF_DIR}/${GFX_INI}
141	  else
142	    sed -i '/MSAA/c\MSAA = 0' ${CONF_DIR}/${GFX_INI}
143	    sed -i '/SSAA/c\SSAA = False' ${CONF_DIR}/${GFX_INI}
144	  fi
145	
146	  # Aspect Ratio
147	  if [ "$ASPECT" = "1" ]; then
148	    sed -i '/AspectRatio/c\AspectRatio = 1' ${CONF_DIR}/${GFX_INI}
149	  elif [ "$ASPECT" = "2" ]; then
150	    sed -i '/AspectRatio/c\AspectRatio = 2' ${CONF_DIR}/${GFX_INI}
151	  elif [ "$ASPECT" = "3" ]; then
152	    sed -i '/AspectRatio/c\AspectRatio = 3' ${CONF_DIR}/${GFX_INI}
153	  else
154	    sed -i '/AspectRatio/c\AspectRatio = 0' ${CONF_DIR}/${GFX_INI}
155	  fi
156	
157	  # Audio Backend
158	  if [ "$AUDIOBE" = "lle" ]; then
159	    AUDIO_BACKEND="LLE"
160	  else
161	    AUDIO_BACKEND="HLE"
162	  fi
163	
164	  # Clock Speed
165	  if [ "$CLOCK" = "050" ]; then
166	    sed -i '/^Overclock =/c\Overclock = 0.5' ${CONF_DIR}/${DOLPHIN_INI}
167	    sed -i '/^OverclockEnable =/c\OverclockEnable = True' ${CONF_DIR}/${DOLPHIN_INI}
168	  elif [ "$CLOCK" = "075" ]; then
169	    sed -i '/^Overclock =/c\Overclock = 0.75' ${CONF_DIR}/${DOLPHIN_INI}
170	    sed -i '/^OverclockEnable =/c\OverclockEnable = True' ${CONF_DIR}/${DOLPHIN_INI}
171	  elif [ "$CLOCK" = "100" ]; then
172	    sed -i '/^Overclock =/c\Overclock = 1.0' ${CONF_DIR}/${DOLPHIN_INI}
173	    sed -i '/^OverclockEnable =/c\OverclockEnable = False' ${CONF_DIR}/${DOLPHIN_INI}
174	  elif [ "$CLOCK" = "125" ]; then
175	    sed -i '/^Overclock =/c\Overclock = 1.25' ${CONF_DIR}/${DOLPHIN_INI}
176	    sed -i '/^OverclockEnable =/c\OverclockEnable = True' ${CONF_DIR}/${DOLPHIN_INI}
177	  elif [ "$CLOCK" = "150" ]; then
178	    sed -i '/^Overclock =/c\Overclock = 1.5' ${CONF_DIR}/${DOLPHIN_INI}
179	    sed -i '/^OverclockEnable =/c\OverclockEnable = True' ${CONF_DIR}/${DOLPHIN_INI}
180	  elif [ "$CLOCK" = "200" ]; then
181	    sed -i '/^Overclock =/c\Overclock = 2.0' ${CONF_DIR}/${DOLPHIN_INI}
182	    sed -i '/^OverclockEnable =/c\OverclockEnable = True' ${CONF_DIR}/${DOLPHIN_INI}
183	  elif [ "$CLOCK" = "300" ]; then
184	    sed -i '/^Overclock =/c\Overclock = 3.0' ${CONF_DIR}/${DOLPHIN_INI}
185	    sed -i '/^OverclockEnable =/c\OverclockEnable = True' ${CONF_DIR}/${DOLPHIN_INI}
186	  elif [ "$CLOCK" = "400" ]; then
187	    sed -i '/^Overclock =/c\Overclock = 4.0' ${CONF_DIR}/${DOLPHIN_INI}
188	    sed -i '/^OverclockEnable =/c\OverclockEnable = True' ${CONF_DIR}/${DOLPHIN_INI}
189	  else
190	    sed -i '/^OverclockEnable =/c\OverclockEnable = False' ${CONF_DIR}/${DOLPHIN_INI}
191	  fi
192	
193	  # Enable Cheats
194	  if [ "$ENBCHEATS" = "1" ]; then
195	    sed -i '/EnableCheats/c\EnableCheats = True' ${CONF_DIR}/${DOLPHIN_INI}
196	  else
197	    sed -i '/EnableCheats/c\EnableCheats = False' ${CONF_DIR}/${DOLPHIN_INI}
198	  fi
199	
200	  # Graphics Backend
201	  if [ "$GRENDERER" = "vulkan" ]; then
202	    sed -i '/GFXBackend/c\GFXBackend = Vulkan' ${CONF_DIR}/${DOLPHIN_INI}
203	  elif [ "$GRENDERER" = "opengl" ]; then
204	    sed -i '/GFXBackend/c\GFXBackend = OGL' ${CONF_DIR}/${DOLPHIN_INI}
205	  else
206	    sed -i '/GFXBackend/c\GFXBackend = @GRENDERER@' ${CONF_DIR}/${DOLPHIN_INI}
207	  fi
208	
209	  # Sync GPU thread
210	  if [ "$SYNC_GPU_THREAD" = "true" ]; then
211	    sed -i '/SyncGPU =/c\SyncGPU = True' ${CONF_DIR}/${DOLPHIN_INI}
212	  else
213	    sed -i '/SyncGPU =/c\SyncGPU = False' ${CONF_DIR}/${DOLPHIN_INI}
214	  fi
215	
216	  # Internal Resolution
217	  if [ "$IRES" = "1" ]; then
218	    sed -i '/InternalResolution/c\InternalResolution = 1' ${CONF_DIR}/${GFX_INI}
219	  elif [ "$IRES" = "3" ]; then
220	    sed -i '/InternalResolution/c\InternalResolution = 3' ${CONF_DIR}/${GFX_INI}
221	  elif [ "$IRES" = "4" ]; then
222	    sed -i '/InternalResolution/c\InternalResolution = 4' ${CONF_DIR}/${GFX_INI}
223	  elif [ "$IRES" = "6" ]; then
224	    sed -i '/InternalResolution/c\InternalResolution = 6' ${CONF_DIR}/${GFX_INI}
225	  else
226	    sed -i '/InternalResolution/c\InternalResolution = 2' ${CONF_DIR}/${GFX_INI}
227	  fi
228	
229	  # Shader Mode
230	  if [ "$SHADERM" = "0" ]; then
231	    sed -i '/ShaderCompilationMode =/c\ShaderCompilationMode = 0' ${CONF_DIR}/${GFX_INI}
232	  elif [ "$SHADERM" = "1" ]; then
233	    sed -i '/ShaderCompilationMode =/c\ShaderCompilationMode = 1' ${CONF_DIR}/${GFX_INI}
234	  elif [ "$SHADERM" = "2" ]; then
235	    sed -i '/ShaderCompilationMode =/c\ShaderCompilationMode = 2' ${CONF_DIR}/${GFX_INI}
236	  elif [ "$SHADERM" = "3" ]; then
237	    sed -i '/ShaderCompilationMode =/c\ShaderCompilationMode = 3' ${CONF_DIR}/${GFX_INI}
238	  fi
239	
240	  #Shader Precompile
241	  if [ "$SHADERP" = "false" ]; then
242	    sed -i '/WaitForShadersBeforeStarting =/c\WaitForShadersBeforeStarting = False' ${CONF_DIR}/${GFX_INI}
243	  elif [ "$SHADERP" = "true" ]; then
244	    sed -i '/WaitForShadersBeforeStarting =/c\WaitForShadersBeforeStarting = True' ${CONF_DIR}/${GFX_INI}
245	  fi
246	
247	  # Show FPS
248	  if [ "$FPS" = "true" ]; then
249	    sed -i '/ShowFPS/c\ShowFPS = True' ${CONF_DIR}/${GFX_INI}
250	  else
251	    sed -i '/ShowFPS/c\ShowFPS = False' ${CONF_DIR}/${GFX_INI}
252	  fi
253	
254	  # Wii Controller Profile
255	  if [ "$CON" = "classic" ]; then
256	    cp -r ${CONF_DIR}/WiiControllerProfiles/classic.ini ${CONF_DIR}/WiimoteNew.ini
257	  elif [ "$CON" = "vremote" ]; then
258	    cp -r ${CONF_DIR}/WiiControllerProfiles/vremote.ini ${CONF_DIR}/WiimoteNew.ini
259	  elif [ "$CON" = "nunchuck" ]; then
260	    cp -r ${CONF_DIR}/WiiControllerProfiles/nunchuck.ini ${CONF_DIR}/WiimoteNew.ini
261	  elif [ "$CON" = "custom" ]; then
262	    cp -r ${CONF_DIR}/WiiControllerProfiles/custom.ini ${CONF_DIR}/WiimoteNew.ini
263	  else
264	    cp -r ${CONF_DIR}/WiiControllerProfiles/hremote.ini ${CONF_DIR}/WiimoteNew.ini
265	  fi
266	
267	  # Wii Controller Rumble
268	  if [ "$RUMBLE" = "false" ]; then
269	    sed -i '/^Rumble/d' ${CONF_DIR}/WiimoteNew.ini
270	  fi
271	
272	  # Wii Controller Hotkey Enable
273	  if [ "$HKEY" = "mode" ]; then
274	    sed -i '/^Buttons\/Hotkey =/c\Buttons\/Hotkey = Guide' ${CONF_DIR}/GCPadNew.ini
275	  else
276	    sed -i '/^Buttons\/Hotkey =/c\Buttons\/Hotkey = Back' ${CONF_DIR}/GCPadNew.ini
277	  fi
278	  # Skip EFB CPU Access
279	  if [ "$EFBACCESS" = "false" ]; then
280	    sed -i '/EFBAccessEnable =/c\EFBAccessEnable = False' ${CONF_DIR}/${GFX_INI}
281	  else
282	    sed -i '/EFBAccessEnable =/c\EFBAccessEnable = True' ${CONF_DIR}/${GFX_INI}
283	  fi
284	
285	  # Store EFB to texture only
286	  if [ "$EFBTEXTURE" = "false" ]; then
287	    sed -i '/EFBToTextureEnable =/c\EFBToTextureEnable = False' ${CONF_DIR}/${GFX_INI}
288	  else
289	    sed -i '/EFBToTextureEnable =/c\EFBToTextureEnable = True' ${CONF_DIR}/${GFX_INI}
290	  fi
291	
292	  # Store XFB to texture only
293	  if [ "$XFBTEXTURE" = "false" ]; then
294	    sed -i '/XFBToTextureEnable =/c\XFBToTextureEnable = False' ${CONF_DIR}/${GFX_INI}
295	  else
296	    sed -i '/XFBToTextureEnable =/c\XFBToTextureEnable = True' ${CONF_DIR}/${GFX_INI}
297	  fi
298	
299	  # Texture cache accuracy
300	  if [ "$TEXTURE_CACHE_ACCURACY" = "0" ]; then
301	    sed -i '/SafeTextureCacheColorSamples =/c\SafeTextureCacheColorSamples = 0' ${CONF_DIR}/${GFX_INI}
302	  elif [ "$TEXTURE_CACHE_ACCURACY" = "512" ]; then
303	    sed -i '/SafeTextureCacheColorSamples =/c\SafeTextureCacheColorSamples = 512' ${CONF_DIR}/${GFX_INI}
304	  else
305	    # Default to 128 = fast
306	    sed -i '/SafeTextureCacheColorSamples =/c\SafeTextureCacheColorSamples = 128' ${CONF_DIR}/${GFX_INI}
307	  fi
308	
309	  # Widescreen Hack
310	  if [ "$WHACK" = "true" ]; then
311	    sed -i '/wideScreenHack =/c\wideScreenHack = True' ${CONF_DIR}/${GFX_INI}
312	  else
313	    sed -i '/wideScreenHack =/c\wideScreenHack = False' ${CONF_DIR}/${GFX_INI}
314	  fi
315	
316	# Skip bios always, it's untested for Wii
317	sed -i '/SkipIPL/c\SkipIPL = True' ${CONF_DIR}/${DOLPHIN_INI}
318	
319	  # GC Controller Hotkey Enable
320	  if [ "$HKEY" = "mode" ]; then
321	    sed -i '/^Buttons\/Hotkey =/c\Buttons\/Hotkey = Guide' ${CONF_DIR}/${GC_CONTROLLER_INI}
322	  else
323	    sed -i '/^Buttons\/Hotkey =/c\Buttons\/Hotkey = Back' ${CONF_DIR}/${GC_CONTROLLER_INI}
324	  fi
325	
326	  # Qt reads its combos from Hotkeys.ini instead of Buttons/Hotkey, so the same
327	  # setting has to be swapped into the modifier half of every binding there.
328	  if [ -f "${CONF_DIR}/Hotkeys.ini" ]; then
329	    if [ "$HKEY" = "mode" ]; then
330	      sed -i 's/`Back`/`Guide`/g' ${CONF_DIR}/Hotkeys.ini
331	    else
332	      sed -i 's/`Guide`/`Back`/g' ${CONF_DIR}/Hotkeys.ini
333	    fi
334	  fi
335	
336	  # Vsync
337	  if [ "$VSYNC" = "1" ]; then
338	    sed -i '/VSync =/c\VSync = True' ${CONF_DIR}/${GFX_INI}
339	  else
340	    sed -i '/VSync =/c\VSync = False' ${CONF_DIR}/${GFX_INI}
341	  fi
342	
343	# SDL names a gamepad after the mapping it resolves, which is not always the
344	# joystick name control-gen reports.
345	SDL_DB="${SDL_GAMECONTROLLERCONFIG_FILE:-/storage/.config/gptokeyb/gamecontrollerdb.txt}"
346	SDL_DEVICE="${param_device}"
347	MAPLINE=""
348	if [ -n "${DEVICE}" ] && [ -f "${SDL_DB}" ]; then
349	  GUID_KEY="$(echo "${DEVICE}" | cut -c1-4)0000$(echo "${DEVICE}" | cut -c9-)"
350	  MAPLINE="$(awk -F, -v d="${DEVICE}" -v k="${GUID_KEY}" '!/^#/ && NF>1 {
351	      if ($1 == d) { exact = $0; exit }
352	      if (loose == "" && substr($1,5,4) == "0000") {
353	        g = substr($1,1,4) "0000" substr($1,9)
354	        if (g == k) { loose = $0 }
355	      }
356	    }
357	    END { print (exact != "" ? exact : loose) }' "${SDL_DB}")"
358	  MAPPED="$(echo "${MAPLINE}" | cut -d, -f2)"
359	  [ -n "${MAPPED}" ] && SDL_DEVICE="${MAPPED}"
360	fi
361	
362	# Some SDL strings are set for XBox-style, even though they're physically Nintendo-style
363	# so we need to check for that and set a flag if so.
364	FACE_SWAP="no"
365	if [ -n "${MAPLINE}" ]; then
366	  A_BTN="$(echo "${MAPLINE}" | tr ',' '\n' | sed -n 's/^a:b\([0-9]\{1,\}\)$/\1/p')"
367	  B_BTN="$(echo "${MAPLINE}" | tr ',' '\n' | sed -n 's/^b:b\([0-9]\{1,\}\)$/\1/p')"
368	  if [ -n "${A_BTN}" ] && [ -n "${B_BTN}" ] && [ "${A_BTN}" -gt "${B_BTN}" ]; then
369	    FACE_SWAP="yes"
370	  fi
371	fi
372	
373	for CFG in "${CONF_DIR}/Hotkeys.ini" "${CONF_DIR}/GCPadNew.ini" "${CONF_DIR}/WiimoteNew.ini"; do
374	  [ -f "${CFG}" ] || continue
375	  sed -i "/^Device = /c\\Device = SDL/0/${SDL_DEVICE}" "${CFG}"
376	
377	  # A custom profile is whatever the user bound in Dolphin's own UI, which
378	  # already records what the pad really reports; only the shipped profiles are
379	  # written positionally and need correcting.
380	  if [ "${FACE_SWAP}" = "yes" ] && \
381	     ! { [ "${CON}" = "custom" ] && [ "${CFG}" = "${CONF_DIR}/WiimoteNew.ini" ]; }; then
382	    sed -i -e 's/`Button S`/`Button %`/g' \
383	           -e 's/`Button E`/`Button S`/g' \
384	           -e 's/`Button %`/`Button E`/g' \
385	           -e 's/`Button W`/`Button %`/g' \
386	           -e 's/`Button N`/`Button W`/g' \
387	           -e 's/`Button %`/`Button N`/g' "${CFG}"
388	  fi
389	done
390	
391	# The shared Dolphin data link was checked and prepared before settings writes.
392	
393	@EXPORTS@
394	
395	# Retroachievements
396	  /usr/bin/cheevos_dolphin.sh
397	  CHEEVOS_STATUS=$?
398	  # Disabled/logged-out is a valid launch only after the inactive INI is written.
399	  case "${CHEEVOS_STATUS}" in
400	    0|1) ;;
401	    *) exit "${CHEEVOS_STATUS}" ;;
402	  esac
403	
404	# Set video and audio backend
405	  CMD="${CMD} -v $GRENDERER"
406	
407	if [ ${DOLPHIN_CORE} = "dolphin-emu" ]; then
408	  CMD="-b -a ${AUDIO_BACKEND}"
409	else
410	  CMD="-p @DOLPHIN_BACKEND@ -a ${AUDIO_BACKEND}"
411	fi
412	
413	# Debugging info:
414	  echo "GAME set to: ${GAME}"
415	  echo "PLATFORM set to: ${PLATFORM}"
416	  echo "CPU CORES set to ${EMUPERF}"
417	  echo "AA set to: ${AA}"
418	  echo "ASPECT set to: ${ASPECT}"
419	  echo "AUDIOBE set to: ${AUDIOBE}"
420	  echo "CLOCK set to: ${CLOCK}"
421	  echo "DOLPHIN_BACKEND set to: ${DOLPHIN_BACKEND}"
422	  echo "ENBCHEATS set to: ${ENBCHEATS}"
423	  echo "GRENDERER set to: ${GRENDERER}"
424	  echo "IRES set to: ${IRES}"
425	  echo "FPS set to: ${FPS}"
426	  echo "CON set to: ${CON}"
427	  echo "HKEY set to: ${HKEY}"
428	  echo "SHADERM set to: ${SHADERM}"
429	  echo "SHADERP set to: ${SHADERP}"
430	  echo "VSYNC set to: ${VSYNC}"
431	  echo "EFBACCESS set to: ${EFBACCESS}"
432	  echo "EFBTEXTURE set to: ${EFBTEXTURE}"
433	  echo "XFBTEXTURE set to: ${XFBTEXTURE}"
434	  echo "TEXTURE_CACHE_ACCURACY set to: ${TEXTURE_CACHE_ACCURACY}"
435	  echo "SYNC_GPU_THREAD set to: ${SYNC_GPU_THREAD}"
436	  echo "RUMBLE set to: ${RUMBLE}"
437	  echo "WHACK set to: ${WHACK}"
438	  echo "WPC set to: ${WPC}"
439	  echo "Launching /usr/bin/${DOLPHIN_CORE} ${CMD} -e ${1}"
440	
441	# Run Dolphin emulator
442	  ${EMUPERF} /usr/bin/${DOLPHIN_CORE} ${CMD} -e "${1}"
```

### `projects/ROCKNIX/packages/emulators/standalone/drastic-sa/scripts/start_drastic.sh`

```
1	#!/bin/bash
2	
3	# SPDX-License-Identifier: GPL-2.0-or-later
4	# Copyright (C) 2022-present JELOS (https://github.com/JustEnoughLinuxOS)
5	
6	. /etc/profile
7	. /etc/os-release
8	
9	set_kill set "-9 drastic"
10	
11	#Get game/platform info
12	GAME=$(echo "${1}"| sed "s#^/.*/##")
13	PLATFORM="nds"
14	
15	#Get ES feature settings
16	HIRES3D=$(get_setting hires_3d "${PLATFORM}" "${GAME}")
17	THREADED3D=$(get_setting threaded_3d "${PLATFORM}" "${GAME}")
18	FOLLOW3D=$(get_setting follow_3d_renderer "${PLATFORM}" "${GAME}")
19	MICTHRESH=$(get_setting microphone_sensitivity "${PLATFORM}" "${GAME}")
20	SHADER=$(get_setting shader "${PLATFORM}" "${GAME}")
21	
22	#load gptokeyb support files
23	control-gen_init.sh
24	source /storage/.config/gptokeyb/control.ini
25	get_controls
26	
27	#Copy drastic files to .config
28	if [ ! -d "/storage/.config/drastic" ]; then
29	  mkdir -p /storage/.config/drastic/
30	  cp -r /usr/config/drastic/* /storage/.config/drastic/
31	fi
32	
33	if [ ! -d "/storage/.config/drastic/system" ]; then
34	  mkdir -p /storage/.config/drastic/system
35	fi
36	
37	for bios in nds_bios_arm9.bin nds_bios_arm7.bin
38	do
39	  if [ ! -e "/storage/.config/drastic/system/${bios}" ]; then
40	     if [ -e "/storage/roms/bios/${bios}" ]; then
41	       ln -sf /storage/roms/bios/${bios} /storage/.config/drastic/system
42	     fi
43	  fi
44	done
45	
46	#Copy drastic files to .config
47	if [ ! -f "/storage/.config/drastic/drastic.gptk" ]; then
48	  cp -r /usr/config/drastic/drastic.gptk /storage/.config/drastic/
49	fi
50	
51	#Make drastic savestate folder
52	if [ ! -d "/storage/roms/savestates/nds" ]; then
53	  mkdir -p /storage/roms/savestates/nds
54	fi
55	
56	#Link savestates to roms/savestates/nds
57	rm -rf /storage/.config/drastic/savestates
58	ln -sf /storage/roms/savestates/nds /storage/.config/drastic/savestates
59	
60	#Link saves to roms/nds/saves
61	rm -rf /storage/.config/drastic/backup
62	ln -sf /storage/roms/nds /storage/.config/drastic/backup
63	
64	#Apply ES features to config
65	if [ "${HIRES3D}" = "1" ]; then
66	    sed -i 's/^hires_3d = .*/hires_3d = 1/' /storage/.config/drastic/config/drastic.cfg
67	else
68	    sed -i 's/^hires_3d = .*/hires_3d = 0/' /storage/.config/drastic/config/drastic.cfg
69	fi
70	
71	if [ "${THREADED3D}" = "1" ]; then
72	    sed -i 's/^threaded_3d = .*/threaded_3d = 1/' /storage/.config/drastic/config/drastic.cfg
73	else
74	    sed -i 's/^threaded_3d = .*/threaded_3d = 0/' /storage/.config/drastic/config/drastic.cfg
75	fi
76	
77	if [ "${FOLLOW3D}" = "1" ]; then
78	    sed -i 's/^fix_main_2d_screen = .*/fix_main_2d_screen = 1/' /storage/.config/drastic/config/drastic.cfg
79	else
80	    sed -i 's/^fix_main_2d_screen = .*/fix_main_2d_screen = 0/' /storage/.config/drastic/config/drastic.cfg
81	fi
82	
83	cd /storage/.config/drastic/
84	@HOTKEY@
85	
86	$GPTOKEYB "drastic" -c "drastic.gptk" &
87	# Fix actual touch inputs by replacing touch->mouse translation and add hw mic support
88	export LD_PRELOAD="/usr/lib/libdrastouch.so"
89	export SDL_TOUCH_MOUSE_EVENTS="0"
90	export DSHOOK_MIC_THRESH="${MICTHRESH}"
91	export DSHOOK_SHADER="${SHADER:-none}"
92	./drastic "$1"
93	kill -9 $(pidof gptokeyb)
```

### `projects/ROCKNIX/packages/emulators/standalone/dsperate-sa/scripts/start_dsperate.sh`

```
1	#!/bin/bash
2	
3	# SPDX-License-Identifier: GPL-2.0-or-later
4	# Copyright (C) 2026-present ROCKNIX (https://github.com/ROCKNIX)
5	
6	. /etc/profile
7	
8	set_kill set "-9 dsperate"
9	
10	CONF_DIR="/storage/.config/dsperate"
11	DSPERATE_INI="${CONF_DIR}/dsperate.ini"
12	
13	if [ ! -d "${CONF_DIR}" ]; then
14		mkdir -p "${CONF_DIR}"
15	fi
16	
17	#Seed config
18	if [ ! -f "${DSPERATE_INI}" ]; then
19		cp -f "/usr/config/dsperate/dsperate.ini" "${DSPERATE_INI}"
20	fi
21	
22	if [ ! -d "/storage/roms/savestates/nds" ]; then
23		mkdir -p "/storage/roms/savestates/nds"
24	fi
25	
26	if [ ! -d "/storage/.cache/dsperate" ]; then
27		mkdir -p "/storage/.cache/dsperate"
28	fi
29	
30	#Ini key helper
31	set_ini_key() {
32		if grep -q "^[[:space:]]*${1}[[:space:]]*=" "${DSPERATE_INI}"; then
33			sed -i "s|^[[:space:]]*${1}[[:space:]]*=.*|${1} = ${2}|" "${DSPERATE_INI}"
34		else
35			sed -i "/^\[emu\]/a ${1} = ${2}" "${DSPERATE_INI}"
36		fi
37	}
38	
39	#Emulation Station Features
40	GAME=$(echo "${1}" | sed "s#^/.*/##")
41	PLATFORM=$(echo "${2}" | sed "s#^/.*/##")
42	SLAYOUT=$(get_setting screen_layout "${PLATFORM}" "${GAME}")
43	SCREEN=$(get_setting main_screen "${PLATFORM}" "${GAME}")
44	SMOOTH=$(get_setting smooth_scaling "${PLATFORM}" "${GAME}")
45	CHUNKY=$(get_setting chunky_pixels "${PLATFORM}" "${GAME}")
46	LCDGRID=$(get_setting lcd_grid "${PLATFORM}" "${GAME}")
47	VSYNC=$(get_setting vsync "${PLATFORM}" "${GAME}")
48	FRAMESKIP=$(get_setting frameskip "${PLATFORM}" "${GAME}")
49	SPEEDHACK=$(get_setting speed_hack "${PLATFORM}" "${GAME}")
50	AA=$(get_setting anti_aliasing "${PLATFORM}" "${GAME}")
51	ISCALE=$(get_setting integer_scale "${PLATFORM}" "${GAME}")
52	AUTOSAVE=$(get_setting autosave "${PLATFORM}" "${GAME}")
53	
54	OPTS=("--fullscreen")
55	
56	#Default layout
57	case "${SLAYOUT}" in
58		vertical|horizontal|single|pip|dominant_v|dominant_h)
59			OPTS+=("--layout" "${SLAYOUT}")
60			;;
61	esac
62	
63	#Primary/larger screen
64	case "${SCREEN}" in
65		top|bottom)
66			OPTS+=("--screen" "${SCREEN}")
67			;;
68	esac
69	
70	#Scaler options
71	if [ "${SMOOTH}" = "1" ]; then
72		OPTS+=("--linear")
73	else
74		#Chunky pixels (purposely low-res)
75		[ "${CHUNKY}" = "1" ] && OPTS+=("--chunky" "mean")
76	
77		#LCD pixel grid
78		case "${LCDGRID}" in
79			0|"")
80				;;
81			*)
82				OPTS+=("--lcd-grid" "${LCDGRID}")
83				;;
84		esac
85	fi
86	
87	#Vsync
88	[ "${VSYNC}" = "0" ] && OPTS+=("--no-vsync")
89	
90	#Frameskip
91	case "${FRAMESKIP}" in
92		[0-9]*)
93			OPTS+=("--frameskip" "${FRAMESKIP}")
94			;;
95	esac
96	
97	#Speed hacks
98	case "${SPEEDHACK}" in
99		cpu_uc)
100			OPTS+=("--cpu-uc")
101			;;
102		fast_load)
103			OPTS+=("--fast-load")
104			;;
105		cpu_oc)
106			OPTS+=("--fast-load" "--cpu-oc")
107			;;
108		timing_oc)
109			OPTS+=("--fast-load" "--cpu-oc" "--timing-oc")
110			;;
111	esac
112	
113	#Forced integer scale
114	case "${ISCALE}" in
115		under|over)
116			OPTS+=("--integer-scale" "${ISCALE}")
117			;;
118	esac
119	
120	#Dual screen handling
121	[ "${DEVICE_HAS_DUAL_SCREEN}" = "true" ] && OPTS+=("--dual-window")
122	
123	#3D anti-aliasing
124	[ "${AA}" = "1" ] && OPTS+=("--aa")
125	
126	#RetroAchievements
127	#Casual mode only: DSperate does not support hardcore (yet?).
128	if [ "$(get_setting "global.retroachievements")" = "1" ]; then
129		RA_USER=$(get_setting "global.retroachievements.username")
130		if [ -n "${RA_USER}" ]; then
131			OPTS+=("--cheevos" "--cheevos-user" "${RA_USER}")
132		fi
133	fi
134	
135	#Auto Save/Load
136	case "${AUTOSAVE}" in
137		[1-3])
138			OPTS+=("--autoload")
139			set_ini_key autosave true
140			;;
141		*)
142			OPTS+=("--no-autoload")
143			set_ini_key autosave false
144			;;
145	esac
146	
147	#7z compression handling
148	ROM="${1}"
149	if [[ "${ROM}" == *.7z ]]; then
150		TEMP="/tmp/dsperate"
151		rm -rf "${TEMP}"
152		mkdir -p "${TEMP}"
153		7z x -y -o"${TEMP}" "${ROM}"
154		ROM=$(find "${TEMP}" -maxdepth 1 -type f -name "*.nds" | head -n 1)
155	fi
156	
157	#Performance handling
158	CORES=$(get_setting "cores" "${PLATFORM}" "${GAME}")
159	unset EMUPERF
160	[ "${CORES}" = "little" ] && EMUPERF="${SLOW_CORES}"
161	[ "${CORES}" = "big" ] && EMUPERF="${FAST_CORES}"
162	
163	${EMUPERF} /usr/bin/dsperate --config "${DSPERATE_INI}" "${OPTS[@]}" "${ROM}"
```

### `projects/ROCKNIX/packages/emulators/standalone/duckstation-sa/package.mk`

```
1	# SPDX-License-Identifier: GPL-2.0
2	# Copyright (C) 2024-present ROCKNIX (https://github.com/ROCKNIX)
3	
4	PKG_NAME="duckstation-sa"
5	PKG_VERSION="0.1-10998"
6	PKG_LICENSE="CC-BY-NC-ND-4.0"
7	PKG_SITE="https://github.com/stenzek/duckstation"
8	PKG_DEPENDS_TARGET="toolchain Python3 libcom-err"
9	PKG_LONGDESC="Fast PlayStation 1 emulator for x86-64/AArch32/AArch64 "
10	PKG_TOOLCHAIN="manual"
11	
12	case ${TARGET_ARCH} in
13	  x86_64)
14	    PKG_URL="${PKG_SITE}/releases/download/v${PKG_VERSION}/DuckStation-x64.AppImage"
15	    PKG_SHA256="b204886bb498ede1a290215fc2efb521c0c2f26b964788df697b4fc2cb3f7f7b"
16	    ;;
17	  aarch64)
18	    PKG_URL="${PKG_SITE}/releases/download/v${PKG_VERSION}/DuckStation-arm64.AppImage"
19	    PKG_SHA256="f92319a0484e67bb62bfab7b0e56dac46165b50e45b51293038d9344a6288440"
20	    ;;
21	esac
22	
23	makeinstall_target() {
24	  # Redefine strip or the AppImage will be stripped rendering it unusable.
25	  export STRIP=true
26	
27	  mkdir -p ${INSTALL}/usr/bin
28	    install -m 0755 ${PKG_BUILD}/${PKG_NAME}-${PKG_VERSION}.AppImage ${INSTALL}/usr/bin/duckstation-sa
29	    cp -a ${PKG_DIR}/scripts/* ${INSTALL}/usr/bin
30	
31	  mkdir -p ${INSTALL}/usr/config/duckstation
32	    cp -a ${PKG_DIR}/config/${DEVICE}/* ${INSTALL}/usr/config/duckstation
33	
34	  mkdir -p ${INSTALL}/usr/config/modules
35	    cp -a ${PKG_DIR}/sources/"Start Duckstation.sh" ${INSTALL}/usr/config/modules
36	}
```

### `projects/ROCKNIX/packages/emulators/standalone/duckstation-sa/scripts/cheevos_duckstation.sh`

```
1	#! /bin/bash
2	
3	# SPDX-License-Identifier: GPL-2.0-or-later
4	# Copyright (C) 2022-present Hector Calvarro (https://github.com/kelvfimer)
5	# Copyright (C) 2024-present ROCKNIX (https://github.com/ROCKNIX)
6	
7	. /etc/profile
8	
9	DUCK_CFG="/storage/.config/duckstation/settings.ini"
10	LOG_FILE="/var/log/cheevos.log"
11	
12	# Extract username, password, token, if enabled, and hardcore mode from system.cfg
13	username=$(get_setting "global.retroachievements.username")
14	password=$(get_setting "global.retroachievements.password")
15	token=$(get_setting "global.retroachievements.token")
16	enabled=$(get_setting "global.retroachievements")
17	hardcore=$(get_setting "global.retroachievements.hardcore")
18	
19	# Check if RetroAchievements are enabled in Emulation Station
20	if [ ! ${enabled} = 1 ]; then
21	    echo "RetroAchievements are not enabled, please turn them on in Emulation Station." > ${LOG_FILE}
22	    sed -i '/\[Cheevos\]/,/^\s*$/s/Enabled =.*/Enabled = false/' ${DUCK_CFG}
23	    exit 1
24	fi
25	
26	# Check if api token is present in system.cfg
27	if [ -z "${token}" ]; then
28	    echo "RetroAchievements token is empty, please log in with your RetroAchievements credentials in Emulation Station." > ${LOG_FILE}
29	    exit 1
30	fi
31	
32	# Set hardcore mode
33	if [ "${hardcore}" = 1 ]; then
34	  hardcore="true"
35	else
36	  hardcore="false"
37	fi
38	
39	# Update emulator config with RetroAchievements settings
40	zcheevos=$(grep -Fx "[Cheevos]" ${DUCK_CFG})
41	datets=$(date +%s%N | cut -b1-13)
42	
43	if [ -z "${zcheevos}" ]; then
44	    sed -i "\$a [Cheevos]\nEnabled = true\nUsername = ${username}\nToken = ${token}\nLoginTimestamp = ${datets}\nChallengeMode = ${hardcore}" ${DUCK_CFG}
45	else
46	    sed -i '/\[Cheevos\]/,/^\s*$/s/Enabled =.*/Enabled = true/' ${DUCK_CFG}
47	    if ! grep -q "^Username = " ${DUCK_CFG}; then
48	        sed -i "/^\[Cheevos\]/a Username = ${username}" ${DUCK_CFG}
49	    else
50	        sed -i "/^\[Cheevos\]/,/^\[/{s/^Username = .*/Username = ${username}/;}" ${DUCK_CFG}
51	    fi
52	
53	    if ! grep -q "^Token = " ${DUCK_CFG}; then
54	        sed -i "/^\[Cheevos\]/a Token = ${token}" ${DUCK_CFG}
55	    else
56	        sed -i "/^\[Cheevos\]/,/^\[/{s/^Token = .*/Token = ${token}/;}" ${DUCK_CFG}
57	    fi
58	
59	    if ! grep -q "^ChallengeMode = " ${DUCK_CFG}; then
60	        sed -i "/^\[Cheevos\]/a ChallengeMode = ${hardcore}" ${DUCK_CFG}
61	    else
62	        sed -i "/^\[Cheevos\]/,/^\[/{s/^ChallengeMode = .*/ChallengeMode = ${hardcore}/;}" ${DUCK_CFG}
63	    fi
64	
65	   sed -i "/^\[Cheevos\]/,/^\[/{s/^LoginTimestamp = .*/LoginTimestamp = ${datets}/;}" ${DUCK_CFG}
66	fi
```

### `projects/ROCKNIX/packages/emulators/standalone/duckstation-sa/scripts/duckstation_screenshot_path`

```
1	#!/usr/bin/python3
2	# SPDX-License-Identifier: GPL-2.0-or-later
3	# Copyright (C) 2026-present ROCKNIX (https://github.com/ROCKNIX)
4	"""Keep the shipped screenshot default in the saves tree; never move captures."""
5	import os
6	from pathlib import Path
7	import re
8	import stat
9	import sys
10	import tempfile
11	
12	TARGET = Path('/storage/roms/screenshots')
13	MAX_CONFIG_BYTES = 1024 * 1024
14	
15	
16	def read_config(path):
17	    info = path.lstat()
18	    if not stat.S_ISREG(info.st_mode):
19	        raise ValueError('nonregular configuration')
20	    with path.open('rb') as stream:
21	        raw = stream.read(MAX_CONFIG_BYTES + 1)
22	    if len(raw) > MAX_CONFIG_BYTES or b'\0' in raw:
23	        raise ValueError('unreadable configuration')
24	    return info, raw
25	
26	
27	def updated_config(raw):
28	    text = raw.decode('utf-8')
29	    lines = text.splitlines(keepends=True)
30	    section = ''
31	    folders = []
32	    keys = []
33	    for index, line in enumerate(lines):
34	        content = line.strip().lstrip('\ufeff')
35	        if not content or content.startswith(('#', ';')):
36	            continue
37	        if content.startswith('['):
38	            match = re.fullmatch(r'\[([^\]\r\n]+)\]', content)
39	            if not match:
40	                raise ValueError('ambiguous section')
41	            section = match[1].strip().casefold()
42	            if section == 'folders':
43	                folders.append(index)
44	        elif section == 'folders' and '=' in content:
45	            name, value = content.split('=', 1)
46	            if name.strip().casefold() == 'screenshots':
47	                keys.append((index, value.strip()))
48	    if len(folders) > 1 or len(keys) > 1:
49	        raise ValueError('ambiguous screenshot configuration')
50	    value = keys[0][1] if keys else ''
51	    if value == str(TARGET):
52	        return raw
53	    # Only absent, empty, or the exact shipped default is ours to change.
54	    # Quoted, alternate, absolute and other custom values remain untouched.
55	    if value not in ('', 'screenshots'):
56	        return None
57	    newline = '\r\n' if '\r\n' in text else '\n'
58	    setting = 'Screenshots = ' + str(TARGET) + newline
59	    if keys:
60	        lines[keys[0][0]] = setting
61	    elif folders:
62	        index = folders[0]
63	        if not lines[index].endswith(('\n', '\r')):
64	            lines[index] += newline
65	        lines.insert(index + 1, setting)
66	    else:
67	        if lines and not lines[-1].endswith(('\n', '\r')):
68	            lines[-1] += newline
69	        lines.extend([newline, '[Folders]' + newline, setting])
70	    return ''.join(lines).encode('utf-8')
71	
72	
73	def prepare(path):
74	    original, raw = read_config(path)
75	    replacement = updated_config(raw)
76	    if replacement is None:
77	        return
78	    # An owner may have redirected the old default with a directory symlink.
79	    # Keep that choice as well as explicit custom configuration values.
80	    if replacement != raw and (path.parent / 'screenshots').is_symlink():
81	        return
82	    created = False
83	    staged = None
84	    try:
85	        if TARGET.is_symlink():
86	            raise ValueError('screenshot target is a symlink')
87	        if not TARGET.exists():
88	            TARGET.mkdir()
89	            created = True
90	        if not TARGET.is_dir():
91	            raise ValueError('screenshot target is not a directory')
92	        # Verify actual writes before changing the setting, including read-only
93	        # mounts and full storage. The temporary byte is always removed.
94	        with tempfile.TemporaryFile(dir=TARGET) as probe:
95	            probe.write(b'\0')
96	            probe.flush()
97	            os.fsync(probe.fileno())
98	        if replacement == raw:
99	            return
100	        descriptor, staged = tempfile.mkstemp(prefix='.screenshots-', dir=path.parent)
101	        with os.fdopen(descriptor, 'wb') as output:
102	            os.fchmod(output.fileno(), stat.S_IMODE(original.st_mode))
103	            os.fchown(output.fileno(), original.st_uid, original.st_gid)
104	            output.write(replacement)
105	            output.flush()
106	            os.fsync(output.fileno())
107	        current, observed = read_config(path)
108	        identity = lambda info: (info.st_dev, info.st_ino, info.st_size, info.st_mtime_ns, info.st_ctime_ns)
109	        if identity(current) != identity(original) or observed != raw:
110	            raise ValueError('configuration changed during preparation')
111	        os.replace(staged, path)
112	        staged = None
113	    except Exception:
114	        if created:
115	            try:
116	                TARGET.rmdir()
117	            except OSError:
118	                pass
119	        raise
120	    finally:
121	        if staged is not None:
122	            os.unlink(staged)
123	
124	
125	def main():
126	    if len(sys.argv) != 2:
127	        return 2
128	    try:
129	        prepare(Path(sys.argv[1]))
130	    except (OSError, UnicodeError, ValueError):
131	        print("Couldn't prepare the screenshot folder. Screenshot preparation moved no existing captures.", file=sys.stderr)
132	        return 1
133	    return 0
134	
135	
136	if __name__ == '__main__':
137	    sys.exit(main())
```

### `projects/ROCKNIX/packages/emulators/standalone/duckstation-sa/scripts/start_duckstation.sh`

```
1	#!/bin/bash
2	
3	# SPDX-License-Identifier: GPL-2.0-or-later
4	# Copyright (C) 2022-present JELOS (https://github.com/JustEnoughLinuxOS)
5	
6	# Copyright (C) 2026-present ROCKNIX (https://github.com/ROCKNIX)
7	
8	. /etc/profile
9	set_kill set "-9 AppRun.wrapped"
10	
11	# Filesystem vars
12	IMMUTABLE_CONF_DIR="/usr/config/duckstation"
13	IMMUTABLE_CONF_FILE="${IMMUTABLE_CONF_DIR}/settings.ini"
14	APPIMAGE_CONF_DIR="/storage/.local/share/duckstation"
15	CONF_DIR="/storage/.config/duckstation"
16	CONF_FILE="${CONF_DIR}/settings.ini"
17	SAVESTATES_DIR="/storage/roms/savestates/psx"
18	MEMCARDS_DIR="/storage/roms/psx/duckstation/memcards"
19	
20	#Init config dir if required
21	[ ! -d "${CONF_DIR}" ] && cp -r "${IMMUTABLE_CONF_DIR}" /storage/.config
22	
23	#Init config file if required
24	[ ! -f "${CONF_FILE}" ] && cp ${IMMUTABLE_CONF_FILE} ${CONF_FILE}
25	
26	#Link config dir to where appimage can find it
27	mkdir -p /storage/.local/share
28	rm -rf "${APPIMAGE_CONF_DIR}"
29	ln -sfv "${CONF_DIR}" "${APPIMAGE_CONF_DIR}"
30	
31	#Link savestates to roms/savestates
32	[ ! -d "${SAVESTATES_DIR}" ] && mkdir -p "${SAVESTATES_DIR}"
33	[ -d "${CONF_DIR}/savestates" ] && rm -rf "${CONF_DIR}/savestates"
34	ln -sfv "${SAVESTATES_DIR}" "${CONF_DIR}/savestates"
35	
36	# Link memcards to roms
37	if [ ! -d "${MEMCARDS_DIR}" ]; then
38	    mkdir -p ${MEMCARDS_DIR}
39	
40	    # Migrate any existing memcards
41	    if [ -d "${CONF_DIR}/memcards" ]; then
42	        cp -rf ${CONF_DIR}/memcards/* ${MEMCARDS_DIR}
43	    fi
44	fi
45	
46	[ -d "${CONF_DIR}/memcards" ] && rm -rf ${CONF_DIR}/memcards
47	ln -sfv ${MEMCARDS_DIR} ${CONF_DIR}/memcards
48	
49	# Keep default captures in the backed-up screenshots tree (#521). Explicit
50	# custom paths and historical captures stay where the player left them.
51	/usr/bin/duckstation_screenshot_path "${CONF_FILE}" || :
52	
53	#Link gamecontrollerdb.txt
54	ln -sf /usr/config/SDL-GameControllerDB/gamecontrollerdb.txt "${CONF_DIR}/gamecontrollerdb.txt"
55	
56	#Emulation Station Features
57	GAME=$(echo "${1}"| sed "s#^/.*/##")
58	PLATFORM=$(echo "${2}"| sed "s#^/.*/##")
59	ASPECT=$(get_setting aspect_ratio "${PLATFORM}" "${GAME}")
60	FPS=$(get_setting show_fps "${PLATFORM}" "${GAME}")
61	IRES=$(get_setting internal_resolution "${PLATFORM}" "${GAME}")
62	RENDERER=$(get_setting graphics_backend "${PLATFORM}" "${GAME}")
63	VSYNC=$(get_setting vsync "${PLATFORM}" "${GAME}")
64	
65	#Set the cores to use
66	CORES=$(get_setting "cores" "${PLATFORM}" "${GAME}")
67	if [ "${CORES}" = "little" ]
68	then
69	  EMUPERF="${SLOW_CORES}"
70	elif [ "${CORES}" = "big" ]
71	then
72	  EMUPERF="${FAST_CORES}"
73	else
74	  ### All..
75	  unset EMUPERF
76	fi
77	
78	  #Aspect Ratio
79	  if [ "$ASPECT" = "1" ]; then
80	    sed -i '/^AspectRatio/c\AspectRatio = 16:9' ${CONF_FILE}
81	  elif [ "$ASPECT" = "2" ]; then
82	    sed -i '/^AspectRatio/c\AspectRatio = Stretch To Fill' ${CONF_FILE}
83	  else
84	    #Default to 4:3 aspect ratio
85	    sed -i '/^AspectRatio/c\AspectRatio = 4:3' ${CONF_FILE}
86	  fi
87	
88	  #Show FPS
89	  if [ "$FPS" = "true" ]; then
90	    sed -i '/^ShowFPS/c\ShowFPS = true' ${CONF_FILE}
91	  else
92	    #Default to not show FPS
93	    sed -i '/^ShowFPS/c\ShowFPS = false' ${CONF_FILE}
94	  fi
95	
96	  #Internal Resolution
97	  if [ "$IRES" = "2" ]; then
98	    sed -i '/^ResolutionScale =/c\ResolutionScale = 2' ${CONF_FILE}
99	  elif [ "$IRES" = "3" ]; then
100	    sed -i '/^ResolutionScale =/c\ResolutionScale = 3' ${CONF_FILE}
101	  elif [ "$IRES" = "4" ]; then
102	    sed -i '/^ResolutionScale =/c\ResolutionScale = 4' ${CONF_FILE}
103	  elif [ "$IRES" = "5" ]; then
104	    sed -i '/^ResolutionScale =/c\ResolutionScale = 5' ${CONF_FILE}
105	  else
106	    #Default to native resolution
107	    sed -i '/^ResolutionScale =/c\ResolutionScale = 1' ${CONF_FILE}
108	  fi
109	
110	  #Video Backend
111		if [ "$RENDERER" = "opengl" ]; then
112	    sed -i '/^Renderer =/c\Renderer = OpenGL' ${CONF_FILE}
113	  elif [ "$RENDERER" = "vulkan" ]; then
114	    sed -i '/^Renderer =/c\Renderer = Vulkan' ${CONF_FILE}
115	  else
116	    #Default to software renderer
117	    sed -i '/^Renderer =/c\Renderer = Software' ${CONF_FILE}
118	  fi
119	
120	  #VSYNC
121	  if [ "$VSYNC" = "off" ]; then
122	    sed -i '/^VSync =/c\VSync = false' ${CONF_FILE}
123	  else
124	    #Default to vsync on
125	    sed -i '/^VSync =/c\VSync = true' ${CONF_FILE}
126	  fi
127	
128	#Retroachievements
129	# Disabled, not working. Seems like Duckstation changed the token encruption...
130	# /usr/bin/cheevos_duckstation.sh
131	sed -i '/\[Cheevos\]/,/^\s*$/s/Enabled =.*/Enabled = false/' ${CONF_FILE}
132	
133	
134	#Run Duckstation
135	${EMUPERF} duckstation-sa -fullscreen -bigpicture -nogui -- "${1}" > /dev/null 2>&1
```

### `projects/ROCKNIX/packages/emulators/standalone/duckstation-sa/sources/Start Duckstation.sh`

```
1	#!/bin/bash
2	
3	# SPDX-License-Identifier: GPL-2.0-or-later
4	# Copyright (C) 2024-present ROCKNIX (https://github.com/ROCKNIX)
5	
6	# Copyright (C) 2026-present ROCKNIX (https://github.com/ROCKNIX)
7	
8	. /etc/profile
9	set_kill set "-9 AppRun.wrapped"
10	
11	# Filesystem vars
12	IMMUTABLE_CONF_DIR="/usr/config/duckstation"
13	IMMUTABLE_CONF_FILE="${IMMUTABLE_CONF_DIR}/settings.ini"
14	APPIMAGE_CONF_DIR="/storage/.local/share/duckstation"
15	CONF_DIR="/storage/.config/duckstation"
16	CONF_FILE="${CONF_DIR}/settings.ini"
17	
18	#Init config dir if required
19	[ ! -d "${CONF_DIR}" ] && cp -r "${IMMUTABLE_CONF_DIR}" /storage/.config
20	
21	#Link config dir to where appimage can find it
22	mkdir -p /storage/.local/share
23	rm -rf "${APPIMAGE_CONF_DIR}"
24	ln -sfv "${CONF_DIR}" "${APPIMAGE_CONF_DIR}"
25	
26	#Init config file if required
27	[ ! -f "${CONF_FILE}" ] && cp ${IMMUTABLE_CONF_FILE} ${CONF_FILE}
28	
29	# Keep default captures in the backed-up screenshots tree (#521). Explicit
30	# custom paths and historical captures stay where the player left them.
31	/usr/bin/duckstation_screenshot_path "${CONF_FILE}" || :
32	
33	#Link gamecontrollerdb.txt
34	ln -sf /usr/config/SDL-GameControllerDB/gamecontrollerdb.txt "${CONF_DIR}/gamecontrollerdb.txt"
35	
36	/usr/bin/duckstation-sa -fullscreen -bigpicture
```

### `projects/ROCKNIX/packages/emulators/standalone/flycast-sa/scripts/cheevos_flycast.sh`

```
1	#! /bin/bash
2	
3	# SPDX-License-Identifier: GPL-2.0-or-later
4	# Copyright (C) 2022-present Hector Calvarro (https://github.com/kelvfimer)
5	# Copyright (C) 2024-present ROCKNIX (https://github.com/ROCKNIX)
6	
7	. /etc/profile
8	
9	FLYCAST_CFG="/storage/.config/flycast/emu.cfg"
10	LOG_FILE="/var/log/cheevos.log"
11	
12	# Extract username, password, token, if enabled, and hardcore mode from system.cfg
13	username=$(get_setting "global.retroachievements.username")
14	password=$(get_setting "global.retroachievements.password")
15	token=$(get_setting "global.retroachievements.token")
16	enabled=$(get_setting "global.retroachievements")
17	hardcore=$(get_setting "global.retroachievements.hardcore")
18	
19	# Check if RetroAchievements are enabled in Emulation Station
20	if [ ! ${enabled} = 1 ]; then
21	    echo "RetroAchievements are not enabled, please turn them on in Emulation Station." > ${LOG_FILE}
22	    sed -i '/\[achievements\]/,/^\s*$/s/Enabled =.*/Enabled = no/' ${FLYCAST_CFG}
23	    exit 1
24	fi
25	
26	# Check if api token is present in system.cfg
27	if [ -z "${token}" ]; then
28	    echo "RetroAchievements token is empty, please log in with your RetroAchievements credentials in Emulation Station." > ${LOG_FILE}
29	    exit 1
30	fi
31	
32	# Set hardcore mode
33	if [ "${hardcore}" = 1 ]; then
34	  hardcore="true"
35	else
36	  hardcore="false"
37	fi
38	
39	# Update emulator config with RetroAchievements settings
40	zcheevos=$(grep -Fx "[achievements]" ${FLYCAST_CFG})
41	
42	if [ -z "${zcheevos}" ]; then
43	    sed -i "\$a [achievements]\nEnabled = yes\nHardcoreMode = ${hardcore}\nUserName = ${username}\nToken = ${token}" ${FLYCAST_CFG}
44	else
45	    sed -i '/\[achievements\]/,/^\s*$/s/Enabled =.*/Enabled = yes/' ${FLYCAST_CFG}
46	    if ! grep -q "^HardcoreMode = " ${FLYCAST_CFG}; then
47	        sed -i "/^\[achievements\]/a HardcoreMode = ${hardcore}" ${FLYCAST_CFG}
48	    else
49	        sed -i "/^\[achievements\]/,/^\[/{s/^HardcoreMode = .*/HardcoreMode = ${hardcore}/;}" ${FLYCAST_CFG}
50	    fi
51	
52	    if ! grep -q "^UserName = " ${FLYCAST_CFG}; then
53	        sed -i "/^\[achievements\]/a UserName = ${username}" ${FLYCAST_CFG}
54	    else
55	        sed -i "/^\[achievements\]/,/^\[/{s/^UserName = .*/UserName = ${username}/;}" ${FLYCAST_CFG}
56	    fi
57	
58	    if ! grep -q "^Token = " ${FLYCAST_CFG}; then
59	        sed -i "/^\[achievements\]/a Token = ${token}" ${FLYCAST_CFG}
60	    else
61	        sed -i "/^\[achievements\]/,/^\[/{s/^Token = .*/Token = ${token}/;}" ${FLYCAST_CFG}
62	    fi
63	fi
```

### `projects/ROCKNIX/packages/emulators/standalone/flycast-sa/scripts/start_flycast.sh`

```
1	#!/bin/bash
2	
3	# SPDX-License-Identifier: GPL-2.0-or-later
4	# Copyright (C) 2022-present JELOS (https://github.com/JustEnoughLinuxOS)
5	
6	. /etc/profile
7	set_kill set "-9 flycast"
8	
9	#load gptokeyb support files
10	control-gen_init.sh
11	source /storage/.config/gptokeyb/control.ini
12	get_controls
13	
14	# Conf files vars
15	SOURCE_DIR="/usr/config/flycast"
16	CONF_DIR="/storage/.config/flycast"
17	FLYCAST_INI="emu.cfg"
18	
19	#Check if flycast exists in .config
20	if [ ! -d "/storage/.config/flycast" ]; then
21	  cp -r "${SOURCE_DIR}" "${CONF_DIR}"
22	fi
23	
24	#Move save file storage/roms
25	if [ -d "${CONF_DIR}/data" ]; then
26	  mv "${CONF_DIR}/data" "/storage/roms/dreamcast/"
27	fi
28	
29	#Make flycast bios folder
30	if [ ! -d "/storage/roms/bios/dc" ]; then
31	  mkdir -p "/storage/roms/bios/dc"
32	fi
33	
34	#Link  .config/flycast to .local
35	ln -sf "/storage/roms/bios/dc" "/storage/roms/dreamcast/data"
36	
37	
38	#Make sure flycast gptk config exists
39	if [ ! -f "${CONF_DIR}/flycast.gptk" ]; then
40	  cp -r "/usr/config/flycast/flycast.gptk" "${CONF_DIR}/flycast.gptk"
41	fi
42	
43	#Make sure flycast gptk SDL_Keyboard.cfg exists
44	if [ ! -f "${CONF_DIR}/mappings/SDL_Keyboard.cfg" ]; then
45	  cp -r "/usr/config/flycast/mappings/SDL_Keyboard.cfg" "${CONF_DIR}/mappings/SDL_Keyboard.cfg"
46	fi
47	
48	#Emulation Station Features
49	GAME=$(echo "${1}"| sed "s#^/.*/##")
50	PLATFORM=$(echo "${2}"| sed "s#^/.*/##")
51	ASPECT=$(get_setting aspect_ratio "${PLATFORM}" "${GAME}")
52	ASKIP=$(get_setting auto_frame_skip "${PLATFORM}" "${GAME}")
53	FPS=$(get_setting show_fps "${PLATFORM}" "${GAME}")
54	IRES=$(get_setting internal_resolution "${PLATFORM}" "${GAME}")
55	GRENDERER=$(get_setting graphics_backend "${PLATFORM}" "${GAME}")
56	VSYNC=$(get_setting vsync "${PLATFORM}" "${GAME}")
57	
58	#Set the cores to use
59	CORES=$(get_setting "cores" "${PLATFORM}" "${GAME}")
60	if [ "${CORES}" = "little" ]
61	then
62	  EMUPERF="${SLOW_CORES}"
63	elif [ "${CORES}" = "big" ]
64	then
65	  EMUPERF="${FAST_CORES}"
66	else
67	  ### All..
68	  unset EMUPERF
69	fi
70	
71	  #AspectRatio
72	        if [ "$ASPECT" = "w" ]; then
73	                sed -i '/^rend.WideScreen =/c\rend.WideScreen = yes' "${CONF_DIR}/${FLYCAST_INI}"
74	                sed -i '/^rend.SuperWideScreen =/c\rend.SuperWideScreen = no' "${CONF_DIR}/${FLYCAST_INI}"
75	        elif [ "$ASPECT" = "sw" ]; then
76	                sed -i '/^rend.WideScreen =/c\rend.WideScreen = yes' "${CONF_DIR}/${FLYCAST_INI}"
77	                sed -i '/^rend.SuperWideScreen =/c\rend.SuperWideScreen = yes' "${CONF_DIR}/${FLYCAST_INI}"
78		else
79			sed -i '/^rend.WideScreen =/c\rend.WideScreen = no' "${CONF_DIR}/${FLYCAST_INI}"
80			sed -i '/^rend.SuperWideScreen =/c\rend.SuperWideScreen = no' "${CONF_DIR}/${FLYCAST_INI}"
81	        fi
82	
83	  #AutoFrameSkip
84	        if [ "$ASKIP" = "normal" ]; then
85	                sed -i '/^pvr.AutoSkipFrame =/c\pvr.AutoSkipFrame = 1' "${CONF_DIR}/${FLYCAST_INI}"
86	        elif [ "$ASKIP" = "max" ]; then
87	                sed -i '/^pvr.AutoSkipFrame =/c\pvr.AutoSkipFrame = 2' "${CONF_DIR}/${FLYCAST_INI}"
88		else
89			sed -i '/^pvr.AutoSkipFrame =/c\pvr.AutoSkipFrame = 0' "${CONF_DIR}/${FLYCAST_INI}"
90	        fi
91	
92	  #Internal Resolution
93	        if [ "$IRES" = "0" ]; then
94	                sed -i '/rend.Resolution =/c\rend.Resolution = 240' "${CONF_DIR}/${FLYCAST_INI}"
95	        elif [ "$IRES" = "2" ]; then
96	                sed -i '/rend.Resolution =/c\rend.Resolution = 720' "${CONF_DIR}/${FLYCAST_INI}"
97	        elif [ "$IRES" = "3" ]; then
98	                sed -i '/rend.Resolution =/c\rend.Resolution = 960' "${CONF_DIR}/${FLYCAST_INI}"
99	        elif [ "$IRES" = "4" ]; then
100	                sed -i '/rend.Resolution =/c\rend.Resolution = 1200' "${CONF_DIR}/${FLYCAST_INI}"
101	        elif [ "$IRES" = "5" ]; then
102	                sed -i '/rend.Resolution =/c\rend.Resolution = 1440' "${CONF_DIR}/${FLYCAST_INI}"
103	        else
104	                sed -i '/rend.Resolution =/c\rend.Resolution = 480' "${CONF_DIR}/${FLYCAST_INI}"
105	        fi
106	
107	  #Graphics Renderer
108	        if [ "$GRENDERER" = "opengl" ]; then
109	                sed -i '/^pvr.rend =/c\pvr.rend = 0' "${CONF_DIR}/${FLYCAST_INI}"
110	        elif [ "$GRENDERER" = "vulkan" ]; then
111	                sed -i '/^pvr.rend =/c\pvr.rend = 4' "${CONF_DIR}/${FLYCAST_INI}"
112	        else
113			sed -i '/^pvr.rend =/c\pvr.rend = @GRENDERER@' "${CONF_DIR}/${FLYCAST_INI}"
114		fi
115	
116	  #ShowFPS
117	        if [ "$FPS" = "1" ]; then
118	                sed -i '/^rend.ShowFPS =/c\rend.ShowFPS = yes' "${CONF_DIR}/${FLYCAST_INI}"
119		else
120			sed -i '/^rend.ShowFPS =/c\rend.ShowFPS = no' "${CONF_DIR}/${FLYCAST_INI}"
121	        fi
122	
123	  #Vsync
124	        if [ "$VSYNC" = "1" ];then
125	                sed -i '/^rend.vsync =/c\rend.vsync = yes' "${CONF_DIR}/${FLYCAST_INI}"
126		else
127			sed -i '/^rend.vsync =/c\rend.vsync = no' "${CONF_DIR}/${FLYCAST_INI}"
128	        fi
129	
130	#Retroachievements
131	/usr/bin/cheevos_flycast.sh
132	
133	# Debugging info:
134	  echo "GAME set to: ${GAME}"
135	  echo "PLATFORM set to: ${PLATFORM}"
136	  echo "CONF DIR: ${CONF_DIR}/${FLYCAST_INI}"
137	  echo "CPU CORES set to: ${EMUPERF}"
138	  echo "ASPECT RATIO set to: ${ASPECT}"
139	  echo "AUTO FRAME SKIP set to: ${ASKIP}"
140	  echo "INTERNAL RESOLUTION set to: ${IRES}"
141	  echo "GRAPHICS RENDERER set to: ${GRENDERER}"
142	  echo "FPS set to: ${FPS}"
143	  echo "VSYNC set to: ${VSYNC}"
144	  echo "Launching /usr/bin/flycast ${1}"
145	
146	#Run flycast emulator
147	$GPTOKEYB "flycast" -c "${CONF_DIR}/flycast.gptk" &
148	${EMUPERF} /usr/bin/flycast "${1}"
149	kill -9 "$(pidof gptokeyb)"
```

### `projects/ROCKNIX/packages/emulators/standalone/gopher64-sa/scripts/start_gopher64.sh`

```
1	#!/bin/bash
2	
3	# SPDX-License-Identifier: GPL-2.0-or-later
4	# Copyright (C) 2026-present ROCKNIX (https://github.com/ROCKNIX)
5	
6	. /etc/profile
7	set_kill set "-9 gopher64"
8	
9	# Conf files vars
10	SOURCE_DIR="/usr/config/gopher64"
11	CONF_DIR="/storage/.config/gopher64"
12	GOPHER64_JSON="config.json"
13	
14	#Check if gopher64 exists in /storage/.config
15	if [ ! -d "${CONF_DIR}" ]; then
16	  cp -r "${SOURCE_DIR}" "/storage/.config/"
17	fi
18	
19	#Check if config.json exists in .config/gopher64
20	if [ ! -f "${CONF_DIR}/${GOPHER64_JSON}" ]; then
21	  cp -r "${SOURCE_DIR}/${GOPHER64_JSON}" "${CONF_DIR}"
22	fi
23	
24	#Emulation Station Features
25	GAME=$(echo "${1}"| sed "s#^/.*/##")
26	PLATFORM=$(echo "${2}"| sed "s#^/.*/##")
27	UPSCALE=$(get_setting upscale "${PLATFORM}" "${GAME}")
28	INTEGERSCALING=$(get_setting integer_scaling "${PLATFORM}" "${GAME}")
29	WIDESCREEN=$(get_setting wide_screen "${PLATFORM}" "${GAME}")
30	CRTFILTER=$(get_setting crt_filter "${PLATFORM}" "${GAME}")
31	OVERCLOCKN64=$(get_setting overclock_n64 "${PLATFORM}" "${GAME}")
32	VSYNC=$(get_setting vsync "${PLATFORM}" "${GAME}")
33	
34	# Upscaling
35	if [[ "$UPSCALE" =~ ^[1-4]$ ]]; then
36	  sed -Ei "s/^([[:space:]]*)\"upscale\":.*/\1\"upscale\": $UPSCALE,/" "${CONF_DIR}/${GOPHER64_JSON}"
37	else
38	  sed -Ei "s/^([[:space:]]*)\"upscale\":.*/\1\"upscale\": 1,/" "${CONF_DIR}/${GOPHER64_JSON}"
39	fi
40	
41	# Integer Scaling
42	if [[ "$INTEGERSCALING" =~ ^(true|false)$ ]]; then
43	  sed -Ei "s/^([[:space:]]*)\"integer_scaling\":.*/\1\"integer_scaling\": $INTEGERSCALING,/" "${CONF_DIR}/${GOPHER64_JSON}"
44	else
45	  sed -Ei "s/^([[:space:]]*)\"integer_scaling\":.*/\1\"integer_scaling\": false,/" "${CONF_DIR}/${GOPHER64_JSON}"
46	fi
47	
48	# Widescreen
49	if [[ "$WIDESCREEN" =~ ^(true|false)$ ]]; then
50	  sed -Ei "s/^([[:space:]]*)\"widescreen\":.*/\1\"widescreen\": $WIDESCREEN,/" "${CONF_DIR}/${GOPHER64_JSON}"
51	else
52	  sed -Ei "s/^([[:space:]]*)\"widescreen\":.*/\1\"widescreen\": false,/" "${CONF_DIR}/${GOPHER64_JSON}"
53	fi
54	
55	# CRT Filter
56	if [[ "$CRTFILTER" =~ ^(true|false)$ ]]; then
57	  sed -Ei "s/^([[:space:]]*)\"crt\":.*/\1\"crt\": $CRTFILTER/" "${CONF_DIR}/${GOPHER64_JSON}"
58	else
59	  sed -Ei "s/^([[:space:]]*)\"crt\":.*/\1\"crt\": false/" "${CONF_DIR}/${GOPHER64_JSON}"
60	fi
61	
62	# Overclock N64
63	if [[ "$OVERCLOCKN64" =~ ^(true|false)$ ]]; then
64	  sed -Ei "s/^([[:space:]]*)\"overclock\":.*/\1\"overclock\": $OVERCLOCKN64,/" "${CONF_DIR}/${GOPHER64_JSON}"
65	else
66	  sed -Ei "s/^([[:space:]]*)\"overclock\":.*/\1\"overclock\": false,/" "${CONF_DIR}/${GOPHER64_JSON}"
67	fi
68	
69	# Vsync
70	if [[ "$VSYNC" =~ ^(true|false)$ ]]; then
71	  sed -Ei "s/^([[:space:]]*)\"vsync\":.*/\1\"vsync\": $VSYNC,/" "${CONF_DIR}/${GOPHER64_JSON}"
72	else
73	  sed -Ei "s/^([[:space:]]*)\"vsync\":.*/\1\"vsync\": false,/" "${CONF_DIR}/${GOPHER64_JSON}"
74	fi
75	
76	#Set the cores to use
77	CORES=$(get_setting "cores" "${PLATFORM}" "${GAME}")
78	if [ "${CORES}" = "little" ]
79	then
80	  EMUPERF="${SLOW_CORES}"
81	elif [ "${CORES}" = "big" ]
82	then
83	  EMUPERF="${FAST_CORES}"
84	else
85	  ### All..
86	  unset EMUPERF
87	fi
88	
89	#Set correct input device
90	GAMEPAD="/dev/hidraw0"
91	sed -Ei "/\"controller_assignment\": \[/ { n; s#\"[^\"]*\"#\"$GAMEPAD\"#; }" "${CONF_DIR}/${GOPHER64_JSON}"
92	
93	# Cheevos
94	CHEEVOS_LOG_FILE="/var/log/cheevos.log"
95	
96	# Extract username, password, if enabled, and hardcore mode from system.cfg
97	ra_username=$(get_setting "global.retroachievements.username")
98	ra_password=$(get_setting "global.retroachievements.password")
99	ra_enabled=$(get_setting "global.retroachievements")
100	
101	# Check if RetroAchievements are enabled in Emulation Station
102	if [ "${ra_enabled}" = 1 ]; then
103	  echo "RetroAchievements enabled." > ${CHEEVOS_LOG_FILE}
104	  CHEEVOS="--ra-username $ra_username --ra-password $ra_password"
105	else
106	  echo "RetroAchievements are disabled, please turn them on in Emulation Station." > ${CHEEVOS_LOG_FILE}
107	  CHEEVOS=""
108	fi
109	
110	# Debugging info:
111	  echo "GAME set to: ${GAME}"
112	  echo "PLATFORM set to: ${PLATFORM}"
113	  echo "CONF DIR: ${CONF_DIR}/${GOPHER64_JSON}"
114	  echo "CPU CORES set to: ${EMUPERF}"
115	  echo "UPSCALE set to: ${UPSCALE}"
116	  echo "INTEGER SCALING set to: ${INTEGERSCALING}"
117	  echo "WIDESCREEN set to: ${WIDESCREEN}"
118	  echo "CRT FILTER set to: ${CRTFILTER}"
119	  echo "OVERCLOCK N64 set to: ${OVERCLOCKN64}"
120	  echo "VSYNC set to: ${VSYNC}"
121	  echo "GAMEPAD set to: ${GAMEPAD}"
122	  echo "Launching /usr/bin/gopher64 ${1}"
123	
124	# Start Gopher64
125	${EMUPERF} /usr/bin/gopher64 --fullscreen --assign-controller 0 --port 1 ${CHEEVOS} "${1}"
```

### `projects/ROCKNIX/packages/emulators/standalone/gzdoom-sa/scripts/start_gzdoom.sh`

```
1	#!/usr/bin/bash
2	
3	# SPDX-License-Identifier: GPL-2.0-or-later
4	# Copyright (C) 2021-present 351ELEC (https://github.com/351ELEC)
5	
6	. /etc/profile
7	set_kill set "-9 gzdoom"
8	
9	RUN_DIR="/storage/roms/doom"
10	CONFIG="/storage/.config/gzdoom/gzdoom.ini"
11	SAVE_DIR="/storage/roms/gzdoom"
12	
13	#Emulation Station Features
14	GAME=$(echo "${1}"| sed "s#^/.*/##")
15	PLATFORM=$(echo "${2}"| sed "s#^/.*/##")
16	VSYNC=$(get_setting vsync "${PLATFORM}" "${GAME}")
17	
18	
19	if [ ! -d "/storage/.config/gzdoom/" ]; then
20	  cp -rf /usr/config/gzdoom /storage/.config/
21	fi
22	
23	if [ ! -f "/storage/.config/gzdoom/gzdoom.ini" ]; then
24	  cp -rf /usr/config/gzdoom/gzdoom.ini /storage/.config/gzdoom/
25	fi
26	
27	# Check for newer pk3 files
28	SHASUMSRC=$(sha256sum "/usr/config/gzdoom/gzdoom.pk3" | awk '{print $1}')
29	SHASUMDST=$(sha256sum "/storage/.config/gzdoom/gzdoom.pk3" | awk '{print $1}')
30	
31	if [ $SHASUMSRC != $SHASUMDST ]; then
32	  cp /usr/config/gzdoom/*.pk3 /storage/.config/gzdoom/
33	fi
34	
35	# set resolution
36	sed -i '/vid_defheight=/c\vid_defheight='$(fbheight) /storage/.config/gzdoom/gzdoom.ini
37	sed -i '/vid_defwidth=/c\vid_defwidth='$(fbwidth) /storage/.config/gzdoom/gzdoom.ini
38	
39	if [ ! -d "/storage/roms/doom/iwads" ]; then
40	  mkdir /storage/roms/doom/iwads
41	fi
42	
43	if [ ! -d "/storage/roms/doom/mods" ]; then
44	  mkdir /storage/roms/doom/mods
45	fi
46	
47	mkdir -p ${SAVE_DIR}
48	
49	params=" -config ${CONFIG} -savedir ${SAVE_DIR}"
50	params+=" +gl_es 1 +vid_preferbackend 3 +cl_capfps 0 +vid_fps 0"
51	
52	if [ "$VSYNC" = "false" ]; then
53	  params+=" +vid_vsync 0"
54	else
55	  params+=" +vid_vsync 1"
56	fi
57	
58	# EXT can be wad, WAD, iwad, IWAD, pwad, PWAD or doom
59	EXT=${1##*.}
60	
61	# If its not a simple wad (extension .doom) read the file and parse the data
62	if [ ${EXT} == "doom" ]; then
63	  dos2unix "${1}"
64	  local_savedir=""
65	  while IFS== read -r key value; do
66	    if [ "$key" == "IWAD" ]; then
67	      params+=" -iwad $value"
68	    fi
69	    if [ "$key" == "MOD" ]; then
70	      params+=" -file $value"
71	    fi
72	    if [ "$key" == "SAVEDIR" ]; then
73	      local_savedir="$value"
74	    fi
75	  done <"${1}"
76	  if [ -n "$local_savedir" ]; then
77	    mkdir -p "$local_savedir"
78	    params="${params/-savedir ${SAVE_DIR}/-savedir ${local_savedir}}"
79	  fi
80	else
81	  params+=" -iwad ${1}"
82	fi
83	
84	#Set the cores to use
85	CORES=$(get_setting "cores" "${PLATFORM}" "${GAME}")
86	if [ "${CORES}" = "little" ]; then
87	  EMUPERF="${SLOW_CORES}"
88	elif [ "${CORES}" = "big" ]; then
89	  EMUPERF="${FAST_CORES}"
90	else
91	  ### All..
92	  unset EMUPERF
93	fi
94	
95	cd "${RUN_DIR}"
96	echo ${params} | ${EMUPERF} xargs /usr/bin/gzdoom >/var/log/gzdoom.log 2>&1
```

### `projects/ROCKNIX/packages/emulators/standalone/hatarisa/package.mk`

```
1	# SPDX-License-Identifier: GPL-2.0
2	# Copyright (C) 2024-present ROCKNIX (https://github.com/ROCKNIX)
3	
4	PKG_NAME="hatarisa"
5	PKG_VERSION="6da06056d89bb39777063388d82d065d9e2e31fd"
6	PKG_SHA256="282eb1536e1bfd9c87ac8cad79b5b5761ca7ade5a5c7ed5498508c768fb352fc"
7	PKG_LICENSE="GPL-2.0-or-later"
8	PKG_SITE="https://github.com/hatari/hatari"
9	PKG_URL="https://github.com/hatari/hatari/archive/${PKG_VERSION}.tar.gz"
10	PKG_DEPENDS_TARGET="toolchain linux glibc systemd alsa-lib SDL2 portaudio zlib capsimg libpng"
11	PKG_DEPENDS_UNPACK="capsimg"
12	PKG_LONGDESC="Hatari is an Atari ST/STE/TT/Falcon emulator"
13	
14	post_unpack() {
15	  sed -i "s|COMMAND cc|COMMAND ${TOOLCHAIN}/bin/host-gcc|g" ${PKG_BUILD}/src/cpu/CMakeLists.txt
16	
17	  # copy IPF Support Library include files
18	  mkdir -p ${PKG_BUILD}/src/includes/caps
19	    cp -a $(get_build_dir capsimg)/LibIPF/* ${PKG_BUILD}/src/includes/caps
20	    cp -a $(get_build_dir capsimg)/Core/CommonTypes.h ${PKG_BUILD}/src/includes/caps
21	    cp -a $(get_install_dir capsimg)/usr/lib/libcapsimage.so.5.1 ${PKG_BUILD}
22	}
23	
24	pre_configure_target() {
25	  PKG_CMAKE_OPTS_TARGET="-DCMAKE_SKIP_RPATH=ON \
26	                         -DDATADIR="/usr/config/hatari" \
27	                         -DBIN2DATADIR="../../storage/.config/hatari" \
28	                         -DCAPSIMAGE_INCLUDE_DIR=${PKG_BUILD}/src/include \
29	                         -DCAPSIMAGE_LIBRARY=${PKG_BUILD}/libcapsimage.so.5.1"
30	
31	  # add library search path for loading libcapsimage library
32	  LDFLAGS="${LDFLAGS} -Wl,-rpath='${PKG_BUILD}'"
33	}
34	
35	makeinstall_target() {
36	  mkdir -p ${INSTALL}/usr/bin
37	    cp -a src/hatari ${INSTALL}/usr/bin/hatarisa
38	    cp -a ${PKG_DIR}/scripts/start_hatari.sh ${INSTALL}/usr/bin
39	
40	  mkdir -p ${INSTALL}/usr/config/hatari
41	    touch ${INSTALL}/usr/config/hatari/hatari.nvram
42	    cp -a ${PKG_DIR}/config/* ${INSTALL}/usr/config/hatari
43	}
```

### `projects/ROCKNIX/packages/emulators/standalone/hatarisa/portaudio/package.mk`

```
1	# SPDX-License-Identifier: GPL-2.0
2	# Copyright (C) 2024-present ROCKNIX (https://github.com/ROCKNIX)
3	
4	PKG_NAME="portaudio"
5	PKG_VERSION="64d1bf913433d7a2835526b80a93487d5038cb8e"
6	PKG_SHA256="c33e48217a844cca3b66ab88571b90beefb8fcb6967177951d4dc283587bf834"
7	PKG_LICENSE="ISC"
8	PKG_SITE="https://portaudio.com"
9	PKG_URL="https://github.com/zhang-ray/portaudio/archive/${PKG_VERSION}.tar.gz"
10	PKG_DEPENDS_TARGET="toolchain alsa-lib"
11	PKG_LONGDESC="PortAudio is a free, cross-platform, open-source, audio I/O library."
12	
13	PKG_CMAKE_OPTS_TARGET="-DCMAKE_POLICY_VERSION_MINIMUM=3.5"
```

### `projects/ROCKNIX/packages/emulators/standalone/hatarisa/scripts/start_hatari.sh`

```
1	#!/bin/sh
2	# SPDX-License-Identifier: GPL-2.0-or-later
3	# Copyright (C) 2018-present 5schatten (https://github.com/5schatten)
4	
5	. /etc/profile
6	
7	# Set some common variables
8	HATARI_DIR_HOME=/storage/.hatari
9	HATARI_DIR=/storage/.config/hatari
10	HATARI_CONFIG_DIR=$HATARI_DIR/conf
11	HATARI_TMP_DIR=/tmp/hatari
12	HATARI_TMP_CONFIG="$HATARI_TMP_DIR"/.hatari-temp.cfg
13	HATARI_LOG="/var/log/hatari.log"
14	MAX_DRIVES=2
15	i=0
16	
17	# create symlink to hatari config dir
18	if [ ! -L $HATARI_DIR_HOME ]; then
19	  rm -rf $HATARI_DIR_HOME
20	  ln -s $HATARI_DIR $HATARI_DIR_HOME
21	fi
22	
23	# Which file should hatari load?
24	echo "Trying to boot this game:" "$1" >> $HATARI_LOG
25	
26	# Create a clean working directory
27	if [ -d "$HATARI_TMP_DIR" ]; then
28	  echo "Clean up old working directory." >> $HATARI_LOG
29	  rm -rf "$HATARI_TMP_DIR"
30	fi
31	mkdir -p "$HATARI_TMP_DIR"
32	
33	# copy default config file to tmp
34	cp $HATARI_CONFIG_DIR/Atari-ST-default.cfg "$HATARI_TMP_CONFIG"
35	
36	# Check if we are loading a .zip file
37	if [ `echo $1 | grep -i .zip | wc -l` -eq 1 ]; then
38	
39	  #unpack the zip file
40	  unzip -q -o "$1" -d "$HATARI_TMP_DIR"
41	
42	  # Assign files to floppy 1 & 2
43	  for FILE in "$HATARI_TMP_DIR"/*
44	  do
45	    i=$(($i+1))
46	    case "$i" in
47	    1)
48	      ARGS="\nszDiskAFileName = "$FILE""
49	      ;;
50	    2)
51	      ARGS="${ARGS}\nszDiskBFileName = "$FILE""
52	      ;;
53	    esac
54	
55	    # This emulator supports 2 floppies max
56	    if [ $i -eq $MAX_DRIVES ]; then
57	      break;
58	    fi
59	  done
60	
61	    # Add game files as floppy 1 & 2 to .hatari-temp.cfg & start hatari
62	    echo -e ${ARGS} >> "$HATARI_TMP_CONFIG"
63	    echo -e "\nAssigned floppy drives:" ${ARGS} "\n" >> "$HATARI_LOG"
64	    nice -n -19 hatarisa --configfile "$HATARI_TMP_CONFIG" >> $HATARI_LOG 2>&1
65	
66	# Check for .cfg config file
67	elif [ `echo $1 | grep -i .cfg | wc -l` -eq 1 ]; then
68	  nice -n -19 hatarisa --configfile "$1" >> $HATARI_LOG 2>&1
69	# All other files
70	else
71	  nice -n -19 hatarisa --configfile "$HATARI_TMP_CONFIG" --disk-a "$1" >> $HATARI_LOG 2>&1
72	fi
73	# Remove temporary dir
74	rm -rf "$HATARI_TMP_DIR"
```

### `projects/ROCKNIX/packages/emulators/standalone/heroic/scripts/start_heroic_authenticate.sh`

```
1	#!/bin/bash
2	# SPDX-License-Identifier: GPL-2.0-or-later
3	# Copyright (C) 2026-present ROCKNIX (https://github.com/ROCKNIX)
4	
5	source /etc/profile
6	set_kill set "-9 heroic Heroic"
7	
8	HEROIC_BASE="/storage/.local/share/heroic-arm64"
9	HEROIC_BIN=""
10	WVKBD_PID=""
11	TOUCHKB_WAS_ACTIVE=0
12	
13	resolve_heroic_bin() {
14	  HEROIC_BIN=""
15	  for candidate in "${HEROIC_BASE}"/Heroic*/heroic "${HEROIC_BASE}"/heroic; do
16	    [ -x "${candidate}" ] || continue
17	    HEROIC_BIN="${candidate}"
18	    return 0
19	  done
20	  return 1
21	}
22	
23	cleanup_keyboard() {
24	  if [ -n "${WVKBD_PID}" ]; then
25	    kill "${WVKBD_PID}" 2>/dev/null || true
26	  fi
27	  if [ "${TOUCHKB_WAS_ACTIVE}" = "1" ]; then
28	    systemctl start touchkeyboard.service >/dev/null 2>&1 || true
29	  fi
30	  if [ "${DEVICE_HAS_DUAL_SCREEN}" = "true" ]; then
31	    swaymsg 'seat seat1 fallback false' >/dev/null 2>&1 || true
32	  fi
33	}
34	
35	if ! resolve_heroic_bin; then
36	  echo "Heroic: launcher binary not found under ${HEROIC_BASE}. Run 'Install Heroic Games Launcher.sh' first." >&2
37	  exit 1
38	fi
39	
40	trap 'cleanup_keyboard' EXIT
41	
42	cd "$(dirname "${HEROIC_BIN}")" || exit 1
43	if [ "${DEVICE_HAS_DUAL_SCREEN}" = "true" ]; then
44	  swaymsg 'seat seat1 fallback true'
45	fi
46	swaymsg for_window [app_id="heroic"] fullscreen disable
47	swaymsg for_window [class="heroic"] fullscreen disable
48	
49	if systemctl is-active --quiet touchkeyboard.service; then
50	  TOUCHKB_WAS_ACTIVE=1
51	  systemctl stop touchkeyboard.service >/dev/null 2>&1 || true
52	fi
53	killall wvkbd-mobintl >/dev/null 2>&1 || true
54	sleep 0.2
55	
56	WVKBD_OUT="$(swaymsg -t get_outputs -r 2>/dev/null | jq -r '.[] | select(.focused == true) | .name' | head -n1)"
57	WVKBD_ARGS=(
58	  -L 500
59	  -fg 6b6b75 -fg-sp 6b6b75 -bg 1d1d1d --text ffffff --text-sp ffffff -press 000000 --press-sp 000000 -fn 48 -l simple
60	)
61	[ -n "${WVKBD_OUT}" ] && WVKBD_ARGS+=(--output "${WVKBD_OUT}")
62	/usr/bin/wvkbd-mobintl "${WVKBD_ARGS[@]}" >/dev/null 2>&1 &
63	WVKBD_PID=$!
64	sleep 0.25
65	kill -USR2 "${WVKBD_PID}" 2>/dev/null || true
66	
67	export ELECTRON_OZONE_PLATFORM_HINT=wayland
68	"${HEROIC_BIN}" --no-sandbox --ozone-platform=wayland "$@"
```

### `projects/ROCKNIX/packages/emulators/standalone/heroic/scripts/start_heroic_play.sh`

```
1	#!/bin/bash
2	# SPDX-License-Identifier: GPL-2.0-or-later
3	# Copyright (C) 2026-present ROCKNIX (https://github.com/ROCKNIX)
4	
5	source /etc/profile
6	set_kill set "-9 heroic Heroic"
7	
8	HEROIC_BASE="/storage/.local/share/heroic-arm64"
9	HEROIC_BIN=""
10	
11	resolve_heroic_bin() {
12	  HEROIC_BIN=""
13	  for candidate in "${HEROIC_BASE}"/Heroic*/heroic "${HEROIC_BASE}"/heroic; do
14	    [ -x "${candidate}" ] || continue
15	    HEROIC_BIN="${candidate}"
16	    return 0
17	  done
18	  return 1
19	}
20	
21	if ! resolve_heroic_bin; then
22	  echo "Heroic: launcher binary not found under ${HEROIC_BASE}. Run 'Install Heroic Games Launcher.sh' first." >&2
23	  exit 1
24	fi
25	
26	if [ "${DEVICE_HAS_DUAL_SCREEN}" = "true" ]; then
27	  swaymsg 'seat seat1 fallback true'
28	fi
29	trap '[ "${DEVICE_HAS_DUAL_SCREEN}" = "true" ] && swaymsg "seat seat1 fallback false" || true' EXIT
30	swaymsg for_window [app_id="heroic"] fullscreen enable
31	swaymsg for_window [class="heroic"] fullscreen enable
32	
33	export ELECTRON_OZONE_PLATFORM_HINT=wayland
34	HEROIC_ARGS=(--no-sandbox --ozone-platform=wayland)
35	if [ "${1:-}" = "--no-gui" ]; then
36	  HEROIC_ARGS=(--no-gui "${HEROIC_ARGS[@]}")
37	  shift
38	fi
39	[ "$#" -gt 0 ] && HEROIC_ARGS+=("$@")
40	
41	cd "$(dirname "${HEROIC_BIN}")" || exit 1
42	"${HEROIC_BIN}" "${HEROIC_ARGS[@]}"
```

### `projects/ROCKNIX/packages/emulators/standalone/heroic/scripts/start_heroic_play_gamescope.sh`

```
1	#!/bin/bash
2	# SPDX-License-Identifier: GPL-2.0-or-later
3	# Copyright (C) 2026-present ROCKNIX (https://github.com/ROCKNIX)
4	
5	source /etc/profile
6	set_kill set "-9 heroic Heroic"
7	
8	HEROIC_BASE="/storage/.local/share/heroic-arm64"
9	HEROIC_BIN=""
10	
11	resolve_heroic_bin() {
12	  HEROIC_BIN=""
13	  for candidate in "${HEROIC_BASE}"/Heroic*/heroic "${HEROIC_BASE}"/heroic; do
14	    [ -x "${candidate}" ] || continue
15	    HEROIC_BIN="${candidate}"
16	    return 0
17	  done
18	  return 1
19	}
20	
21	if ! resolve_heroic_bin; then
22	  echo "Heroic: launcher binary not found under ${HEROIC_BASE}. Run 'Install Heroic Games Launcher.sh' first." >&2
23	  exit 1
24	fi
25	
26	if [ "${DEVICE_HAS_DUAL_SCREEN}" = "true" ]; then
27	  swaymsg 'seat seat1 fallback true'
28	fi
29	trap '[ "${DEVICE_HAS_DUAL_SCREEN}" = "true" ] && swaymsg "seat seat1 fallback false" || true' EXIT
30	swaymsg for_window [app_id="heroic"] fullscreen enable
31	swaymsg for_window [class="heroic"] fullscreen enable
32	
33	eval "$(swaymsg -t get_outputs | jq -r '
34	  .[] | select(.focused == true) |
35	  "W=\(.current_mode.width) H=\(.current_mode.height) TRANSFORM=\(.transform)"
36	')"
37	if [[ "${TRANSFORM:-}" == "90" || "${TRANSFORM:-}" == "270" || "${TRANSFORM:-}" == "flipped-90" || "${TRANSFORM:-}" == "flipped-270" ]]; then
38	  WIDTH="${H}"
39	  HEIGHT="${W}"
40	else
41	  WIDTH="${W}"
42	  HEIGHT="${H}"
43	fi
44	
45	if ! command -v gamescope >/dev/null 2>&1; then
46	  command -v mako-notify >/dev/null 2>&1 && mako-notify "Heroic: gamescope not installed." -no-es
47	  exit 1
48	fi
49	
50	if [ -z "${WIDTH:-}" ]; then
51	  command -v mako-notify >/dev/null 2>&1 && mako-notify "Heroic: display size not found." -no-es
52	  exit 1
53	fi
54	
55	cd "$(dirname "${HEROIC_BIN}")" || exit 1
56	gamescope -f -W "${WIDTH}" -H "${HEIGHT}" -- "${HEROIC_BIN}" --no-sandbox "$@"
```

### `projects/ROCKNIX/packages/emulators/standalone/hypseus-singe/scripts/start_hypseus.sh`

```
1	#!/bin/bash
2	
3	# SPDX-License-Identifier: GPL-2.0-or-later
4	# Copyright (C) 2021-present Shanti Gilbert (https://github.com/shantigilbert)
5	# Copyright (C) 2023 JELOS (https://github.com/JustEnoughLinuxOS)
6	
7	. /etc/profile
8	set_kill set "-9 hypseus"
9	
10	dir="${1}"
11	name=${dir##*/}
12	name=${name%.*}
13	config="/storage/.config/game/configs/hypseus"
14	configfile="${config}/hypinput.ini"
15	
16	# Attempt to auto configure gamepad
17	GAMEPADINFO="$(sdljoytest -skip_loop)"
18	JOYNAME=$(echo "${GAMEPADINFO}" | grep "Joystick 0 name " | sed "s|Joystick 0 name ||" | sed "s|'||g")
19	
20	GPFILE="/usr/share/libretro/autoconfig/${JOYNAME}.cfg"
21	
22	if [[ -f "${GPFILE}" ]]; then
23	        # Other keys to consider KEY_SCREENSHOT KEY_QUIT KEY_PAUSE
24	        for key in KEY_UP KEY_DOWN KEY_LEFT KEY_RIGHT KEY_BUTTON1 KEY_BUTTON2 KEY_BUTTON3 KEY_START1 KEY_COIN1; do
25	            case ${key} in
26	            "KEY_UP")
27	                button=$(cat "${GPFILE}" | grep -E '^input_up_btn\b' | cut -d '"' -f2)
28	                keyboard="1073741906 0"
29	                ;;
30	            "KEY_DOWN")
31	                button=$(cat "${GPFILE}" | grep -E '^input_down_btn\b' | cut -d '"' -f2)
32	                keyboard="1073741905 0"
33	                ;;
34	            "KEY_LEFT")
35	                button=$(cat "${GPFILE}" | grep -E '^input_left_btn\b' | cut -d '"' -f2)
36	                keyboard="1073741904 0"
37	                ;;
38	            "KEY_RIGHT")
39	                button=$(cat "${GPFILE}" | grep -E '^input_right_btn\b' | cut -d '"' -f2)
40	                keyboard="1073741903 0"
41	                ;;
42	            "KEY_BUTTON1")
43	                button=$(cat "${GPFILE}" | grep -E '^input_a_btn\b' | cut -d '"' -f2)
44	                keyboard="1073742048 0"
45	                ;;
46	            "KEY_BUTTON2")
47	                button=$(cat "${GPFILE}" | grep -E '^input_b_btn\b' | cut -d '"' -f2)
48	                keyboard="1073742050 0"
49	                ;;
50	            "KEY_BUTTON3")
51	                button=$(cat "${GPFILE}" | grep -E '^input_x_btn\b' | cut -d '"' -f2)
52	                keyboard="32 0"
53	                ;;
54	            "KEY_START1")
55	                button=$(cat "${GPFILE}" | grep -E '^input_start_btn\b' | cut -d '"' -f2)
56	                keyboard="49 0"
57	                ;;
58	            "KEY_COIN1")
59	                button=$(cat "${GPFILE}" | grep -E '^input_select_btn\b' | cut -d '"' -f2)
60	                keyboard="53 54"
61	                ;;
62	            esac
63	
64	            # if the button is in fact a hat extract the number, else use the button number+1
65	            if [[ "${button}" == "h"* ]]; then
66	                button="0 ${button:1:1}"
67	            else
68	                button="$((${button} + 1))"
69	            fi
70	
71	            sed -i "s|${key}.*|${key} = ${keyboard} ${button} |" ${configfile}
72	        done
73	fi # finish auto gamepad
74	
75	if [[ -f "${dir}/${name}.commands" ]]; then
76	    params=$(<"${dir}/${name}.commands")
77	fi
78	
79	cd "${config}"
80	
81	if [[ -f "${dir}/${name}.singe" ]]; then
82	    hypseus singe vldp -framefile "${dir}/${name}.txt" -script "${dir}/${name}.singe" -fullscreen -useoverlaysb 2 $params
83	else
84	    hypseus "${name}" vldp -framefile "${dir}/${name}.txt" -fullscreen -useoverlaysb 2 $params
85	fi
```

### `projects/ROCKNIX/packages/emulators/standalone/mednafen/scripts/mednafen_gen_config.sh`

```
1	#!/bin/bash
2	# SPDX-License-Identifier: GPL-2.0-or-later
3	# Copyright (C) 2023 JELOS (https://github.com/JustEnoughLinuxOS)
4	
5	. /etc/profile
6	
7	# Generate controller config
8	# Set controller guid, just take the first one mednafen lists
9	GUID1="$(mednafen --list-joysticks | grep ID | awk 'NR==1 {print $2}')"
10	sed -e "s/@GUID1@/${GUID1}/g" ${MEDNAFEN_CONFIG} >> $MEDNAFEN_HOME/mednafen.cfg
11	
12	NAME="$(mednafen --list-joysticks | grep ID | awk 'NR==1 {print $5$6}')"
13	if [[ "$(mednafen --list-joysticks | grep ID | awk 'NR==1 {print $4}')" = "8BitDo" ]]
14	then
15	NAME="X-Box360"
16	fi
17	
18	if [[ "${NAME}" = "X-Box360" ]]
19	then
20	export DEVICE_FUNC_KEYA_MODIFIER="BTN_THUMBL"
21	export DEVICE_FUNC_KEYB_MODIFIER="BTN_THUMBR"
22	fi
23	
24	# explcitly override d-pad that are hats, they are somehow randomly mapped as analog in mednafen
25	if [[ "${NAME}" = "X-Box360" ]]
26	then
27	DEVICE_BTN_DPAD_UP="7-"
28	DEVICE_BTN_DPAD_DOWN="7+"
29	DEVICE_BTN_DPAD_LEFT="6-"
30	DEVICE_BTN_DPAD_RIGHT="6+"
31	elif [[ "${NAME}" = "OSHPB" ]]
32	then
33	DEVICE_BTN_DPAD_UP="6-"
34	DEVICE_BTN_DPAD_DOWN="6+"
35	DEVICE_BTN_DPAD_LEFT="5-"
36	DEVICE_BTN_DPAD_RIGHT="5+"
37	fi
38	
39	# Replace modifiers with actual buttons
40	for MOD in DEVICE_FUNC_KEYA_MODIFIER DEVICE_FUNC_KEYB_MODIFIER
41	do
42	    sed -i -e "s/${MOD}/DEVICE_${!MOD}/g" $MEDNAFEN_HOME/mednafen.cfg
43	done
44	
45	# If not trigger minus axes, default to same as trigger button
46	if [[ -z "${DEVICE_BTN_TL2_MINUS}" ]]; then
47	DEVICE_BTN_TL2_MINUS=${DEVICE_BTN_TL2}
48	fi
49	if [[ -z "${DEVICE_BTN_TR2_MINUS}" ]]; then
50	DEVICE_BTN_TR2_MINUS=${DEVICE_BTN_TR2}
51	fi
52	# General case our 098-controller is right, we just need prefixes. First axes that are prefixed with abs_
53	for CONTROL in DEVICE_BTN_AL_DOWN DEVICE_BTN_AL_UP DEVICE_BTN_AL_LEFT    \
54	               DEVICE_BTN_AL_RIGHT DEVICE_BTN_AR_DOWN DEVICE_BTN_AR_UP   \
55	               DEVICE_BTN_AR_LEFT DEVICE_BTN_AR_RIGHT                    \
56	    	       DEVICE_BTN_SOUTH DEVICE_BTN_EAST DEVICE_BTN_NORTH         \
57	               DEVICE_BTN_WEST DEVICE_BTN_TL DEVICE_BTN_TR               \
58	               DEVICE_BTN_TL2 DEVICE_BTN_TR2 DEVICE_BTN_SELECT           \
59	               DEVICE_BTN_START DEVICE_BTN_MODE DEVICE_BTN_THUMBL        \
60	               DEVICE_BTN_THUMBR DEVICE_BTN_DPAD_UP DEVICE_BTN_DPAD_DOWN \
61	               DEVICE_BTN_DPAD_LEFT DEVICE_BTN_DPAD_RIGHT                \
62	               DEVICE_BTN_TL2_MINUS DEVICE_BTN_TR2_MINUS
63	
64	do
65	    # Detect axes, and treat appropriately. Default is button
66	    if [[ ${!CONTROL} =~ [+|-]$ ]]; then
67	        sed -i -e "s/@${CONTROL}@/abs_${!CONTROL}/g" $MEDNAFEN_HOME/mednafen.cfg
68	    elif [[ ${!CONTROL} =~ ^[0-9]+$ ]]; then
69	        # if it's just a number its a button
70	        sed -i -e "s/@${CONTROL}@/button_${!CONTROL}/g" $MEDNAFEN_HOME/mednafen.cfg
71	    else
72	        # unidentifiable buttons or non-existent on this pad
73	        # Set a non-consequential value so that we don't get a syntax error in mednafen config
74	        # I randomly picked button_99 here.
75	        sed -i -e "s/@${CONTROL}@/button_99/g" $MEDNAFEN_HOME/mednafen.cfg
76	    fi
77	done
```

### `projects/ROCKNIX/packages/emulators/standalone/mednafen/scripts/start_mednafen.sh`

```
1	#!/bin/bash
2	# SPDX-License-Identifier: GPL-2.0-or-later
3	# Copyright (C) 2023 JELOS (https://github.com/JustEnoughLinuxOS)
4	
5	. /etc/profile
6	. /etc/os-release
7	
8	set -x
9	set_kill set "-9 mednafen"
10	
11	export MEDNAFEN_HOME=/storage/.config/mednafen
12	export MEDNAFEN_CONFIG=/usr/config/mednafen/mednafen.template
13	
14	if [ ! -d "$MEDNAFEN_HOME" ]
15	then
16	  mkdir /storage/.config/mednafen
17	fi
18	
19	if [ ! -f "$MEDNAFEN_HOME/mednafen.cfg" ]
20	then
21	    /usr/bin/bash /usr/bin/mednafen_gen_config.sh
22	fi
23	
24	#Emulation Station Features
25	GAME=$(echo "${1}"| sed "s#^/.*/##")
26	CORE=$(echo "${2}"| sed "s#^/.*/##")
27	PLATFORM=$(echo "${3}"| sed "s#^/.*/##")
28	STRETCH=$(get_setting stretch "${PLATFORM}" "${GAME}")
29	SHADER=$(get_setting shader "${PLATFORM}" "${GAME}")
30	
31	#Set the cores to use
32	CORES=$(get_setting "cores" "${PLATFORM}" "${GAME}")
33	FEATURES_CMDLINE=""
34	if [ "${CORES}" = "little" ]
35	then
36	  EMUPERF="${SLOW_CORES}"
37	elif [ "${CORES}" = "big" ]
38	then
39	  EMUPERF="${FAST_CORES}"
40	  if [ "${HW_DEVICE}" = "RK3588" ]; then
41	    FEATURES_CMDLINE+=" -affinity.emu 0x30 "
42	    FEATURES_CMDLINE+=" -ss.affinity.vdp2 0xc0 "
43	  elif [ "${HW_DEVICE}" = "RK3399" ]; then
44	    FEATURES_CMDLINE+=" -affinity.emu 0x10 "
45	    FEATURES_CMDLINE+=" -ss.affinity.vdp2 0x20 "
46	  fi
47	else
48	  ### All..
49	  unset EMUPERF
50	fi
51	
52	#Set Save paths
53	sed -i "s/filesys.path_sav .*/filesys.path_sav \/storage\/roms\/${PLATFORM}/g" $MEDNAFEN_HOME/mednafen.cfg
54	sed -i "s/filesys.path_savbackup.*/filesys.path_savbackup \/storage\/roms\/${PLATFORM}/g" $MEDNAFEN_HOME/mednafen.cfg
55	sed -i "s/filesys.path_state.*/filesys.path_state \/storage\/roms\/savestates\/${PLATFORM}/g" $MEDNAFEN_HOME/mednafen.cfg
56	
57	# Get command line switches
58	CORRECT_ASPECT=$(get_setting correct_aspect ${PLATFORM} "${GAME}")
59	CR=""
60	if [ ! -z "${CORRECT_ASPECT}" ] 
61	then
62	    CR=" -${CORE}.correct_aspect ${CORRECT_ASPECT}"
63	fi
64	if [[ "${CORE}" =~ pce[_fast] ]]
65	then
66	    if [ "$(get_setting nospritelimit ${PLATFORM} "${GAME}")" = "1" ]
67	    then
68	        FEATURES_CMDLINE+=" -${CORE}.nospritelimit 1"
69	    else
70	        FEATURES_CMDLINE+=" -${CORE}.nospritelimit 0"
71	    fi
72	    if [ "$(get_setting forcesgx ${PLATFORM} "${GAME}")" = "1" ]
73	    then
74	        FEATURES_CMDLINE+=" -${CORE}.forcesgx 1"
75	    else
76	        FEATURES_CMDLINE+=" -${CORE}.forcesgx 0"
77	    fi
78	    if [ "${CORE}" = pce_fast ]
79	    then
80	        FEATURES_CMDLINE+=$CR
81	        OCM=$(get_setting ocmultiplier ${PLATFORM} "${GAME}")
82	        if [ ${OCM} > 1 ]
83	        then
84	            FEATURES_CMDLINE+=" -${CORE}.ocmultiplier ${OCM}"
85	        else
86	            FEATURES_CMDLINE+=" -${CORE}.ocmultiplier 1"
87	        fi
88	        CDS=$(get_setting cdspeed ${PLATFORM} "${GAME}")
89	        if [ ${CDS} > 1 ]
90	        then
91	            FEATURES_CMDLINE+=" -${CORE}.cdspeed ${CDS}"
92	        else
93	            FEATURES_CMDLINE+=" -${CORE}.cdspeed 1"
94	        fi
95	    fi
96	elif [ "${CORE}" = "gb" ]
97	then
98	    ST=$(get_setting system_type "${PLATFORM}" "${GAME}")
99	    if [[ "${ST}" =~ auto|dmg|cgb|agb  ]]
100	    then
101	        FEATURES_CMDLINE+=" -${CORE}.system_type ${ST}"
102	    else
103	        FEATURES_CMDLINE+=" -${CORE}.system_type auto"
104	    fi
105	elif [ "${CORE}" = "gba" ]
106	then
107	    if [ $(get_setting tblur "${PLATFORM}" "${GAME}") = "1" ]
108	    then
109	        FEATURES_CMDLINE+=" -${CORE}.tblur 1"
110	    else
111	        FEATURES_CMDLINE+=" -${CORE}.tblur 0"
112	    fi
113	elif [ "${CORE}" = "nes" ]
114	then
115	    FEATURES_CMDLINE+=$CR
116	    if [ $(get_setting clipsides "${PLATFORM}" "${GAME}") = "1" ]
117	    then
118	        FEATURES_CMDLINE+=" -${CORE}.clipsides 1"
119	    else
120	        FEATURES_CMDLINE+=" -${CORE}.clipsides 0"
121	    fi
122	    if [ $(get_setting no8lim "${PLATFORM}" "${GAME}") = "1" ]
123	    then
124	        FEATURES_CMDLINE+=" -${CORE}.no8lim 1"
125	    else
126	        FEATURES_CMDLINE+=" -${CORE}.no8lim 0"
127	    fi
128	elif [ "${CORE}" = "snes_faust" ]
129	then
130	    FEATURES_CMDLINE+=$CR
131	    if [ $(get_setting spex "${PLATFORM}" "${GAME}") = "1" ]
132	    then
133	        FEATURES_CMDLINE+=" -${CORE}.spex 1"
134	    else
135	        FEATURES_CMDLINE+=" -${CORE}.spex 0"
136	    fi
137	    if [ $(get_setting spex.sound "${PLATFORM}" "${GAME}") = "1" ]
138	    then
139	        FEATURES_CMDLINE+=" -${CORE}.spex.sound 1"
140	    else
141	        FEATURES_CMDLINE+=" -${CORE}.spex.sound 0"
142	    fi
143	    SFXCR=$(get_setting superfx.clock_rate ${PLATFORM} "${GAME}")
144	    if [ ${SFXCR} > 1 ]
145	    then
146	        FEATURES_CMDLINE+=" -${CORE}.superfx.clock_rate ${SFXCR}"
147	    else
148	        FEATURES_CMDLINE+=" -${CORE}.superfx.clock_rate 100"
149	    fi
150	    if [[ "$(get_setting superfx.icache ${PLATFORM} "${GAME}")" == "1" ]]
151	    then
152	        FEATURES_CMDLINE+=" -${CORE}.superfx.icache 1"
153	    else
154	        FEATURES_CMDLINE+=" -${CORE}.superfx.icache 0"
155	    fi
156	    CX4CR=$(get_setting cx4.clock_rate ${PLATFORM} "${GAME}")
157	    if [ ${CX4CR} > 1 ]
158	    then
159	        FEATURES_CMDLINE+=" -${CORE}.cx4.clock_rate ${CX4CR}"
160	    else
161	        FEATURES_CMDLINE+=" -${CORE}.cx4.clock_rate 100"
162	    fi
163	elif [ "${CORE}" = "vb" ]
164	then
165	    CE=$(get_setting cpu_emulation "${PLATFORM}" "${GAME}")
166	    if [[ "${CE}" =~ fast|accurate  ]]
167	    then
168	        FEATURES_CMDLINE+=" -${CORE}.cpu_emulation ${CE}"
169	    else
170	        FEATURES_CMDLINE+=" -${CORE}.cpu_emulation fast"
171	    fi
172	    DM=$(get_setting 3dmode "${PLATFORM}" "${GAME}")
173	    if [[ "${DM}" =~ anaglyph|cscope|sidebyside|vli|hli|left|right]  ]]
174	    then
175	        FEATURES_CMDLINE+=" -${CORE}.3dmode ${CE}"
176	    fi
177	elif [ "${CORE}" = "pcfx" ]
178	then
179	    CE=$(get_setting cpu_emulation "${PLATFORM}" "${GAME}")
180	    if [[ "${CE}" =~ auto|fast|accurate  ]]
181	    then
182	        FEATURES_CMDLINE+=" -${CORE}.cpu_emulation ${CE}"
183	    else
184	        FEATURES_CMDLINE+=" -${CORE}.cpu_emulation auto"
185	    fi
186	    CS=$(get_setting cdspeed "${PLATFORM}" "${GAME}")
187	    if [ CS > 2]
188	    then
189	        FEATURES_CMDLINE+=" -${CORE}.cdspeed ${CS}"
190	    else
191	        FEATURES_CMDLINE+=" -${CORE}.cdspeed 2"
192	    fi
193	elif [ "${CORE}" = "ss" ]
194	then
195	    FEATURES_CMDLINE+=$CR
196	    IP1=$(get_setting input.port1 "${PLATFORM}" "${GAME}")
197	    if [[ "${IP1}" =~ gamepad|3dpad|gun  ]]
198	    then
199	        FEATURES_CMDLINE+=" -${CORE}.input.port1 ${IP1}"
200	    else
201	        FEATURES_CMDLINE+=" -${CORE}.input.port1 gamepad"
202	    fi
203	    IP13DMODE=$(get_setting input.port1.3dpad.mode.defpos "${PLATFORM}" "${GAME}")
204	    if [[ "${IP13DMODE}" =~ digital|analog  ]]
205	    then
206	        FEATURES_CMDLINE+=" -${CORE}.input.port1.3dpad.mode.defpos ${IP13DMODE}"
207	    else
208	        FEATURES_CMDLINE+=" -${CORE}.input.port1.3dpad.mode.defpos analog"
209	    fi
210	    CART=$(get_setting cart "${PLATFORM}" "${GAME}")
211	    if [[ "${CART}" =~ auto|none|backup|extram1|extram4|cs1ram16  ]]
212	    then
213	        FEATURES_CMDLINE+=" -${CORE}.cart ${CART}"
214	    else
215	        FEATURES_CMDLINE+=" -${CORE}.cart auto"
216	    fi
217	    CARTAD=$(get_setting cart.auto_default "${PLATFORM}" "${GAME}")
218	    if [[ "${CARTAD}" =~ none|backup|extram1|extram4|cs1ram16  ]]
219	    then
220	        FEATURES_CMDLINE+=" -${CORE}.cart.auto_default ${CARTAD}"
221	    else
222	        FEATURES_CMDLINE+=" -${CORE}.cart.auto_default none"
223	    fi
224	elif [ "${CORE}" = "md" ]
225	then
226	    FEATURES_CMDLINE+=$CR
227	elif [ "${CORE}" = "psx" ]
228	then
229	    FEATURES_CMDLINE+=$CR
230	    IP1=$(get_setting input.port1 "${PLATFORM}" "${GAME}")
231	    if [[ "${IP1}" =~ gamepad|dualshock  ]]
232	    then
233	        FEATURES_CMDLINE+=" -${CORE}.input.port1 ${IP1}"
234	    else
235	        FEATURES_CMDLINE+=" -${CORE}.input.port1 gamepad"
236	    fi
237	fi
238	
239	#Run mednafen
240	${EMUPERF} /usr/bin/mednafen -force_module ${CORE} -${CORE}.stretch ${STRETCH:="aspect"} -${CORE}.shader ${SHADER:="ipsharper"} ${FEATURES_CMDLINE} "${1}"
```

### `projects/ROCKNIX/packages/emulators/standalone/melonds-sa/scripts/cheevos_melonds.sh`

```
1	#!/bin/bash
2	
3	# SPDX-License-Identifier: GPL-2.0-or-later
4	# Copyright (C) 2026-present ROCKNIX (https://github.com/ROCKNIX)
5	
6	. /etc/profile
7	
8	MELONDS_CFG="/storage/.config/melonDS/melonDS.ini"
9	LOG_FILE="/var/log/cheevos.log"
10	
11	: > "${LOG_FILE}"
12	
13	log() {
14	  printf '%s - %s\n' "$(date '+%Y-%m-%d %H:%M:%S')" "$*" >> "${LOG_FILE}"
15	}
16	
17	# Extract username, password, token, if enabled, and hardcore mode from system.cfg
18	username=$(get_setting "global.retroachievements.username")
19	password=$(get_setting "global.retroachievements.password")
20	token=$(get_setting "global.retroachievements.token")
21	enabled=$(get_setting "global.retroachievements")
22	hardcore=$(get_setting "global.retroachievements.hardcore")
23	encore=$(get_setting "global.retroachievements.encore")
24	unofficial=$(get_setting "global.retroachievements.unofficial")
25	[ -z "${unofficial}" ] && unofficial=$(get_setting "global.retroachievements.testunofficial")  # the spelling before 2026-09; EmulationStation writes .unofficial
26	
27	# Check if RetroAchievements are enabled in Emulation Station
28	if [ "${enabled}" = 1 ]; then
29	  enabled="1"
30	else
31	  log "RetroAchievements are not enabled, please turn them on in Emulation Station."
32	  enabled="0"
33	fi
34	
35	# Check if username is present in system.cfg
36	if [ -z "${username}" ]; then
37	    log "RetroAchievements username is empty, please log in with your RetroAchievements credentials in Emulation Station."
38	    enabled="0"
39	    username="null"
40	fi
41	
42	# Check if password is present in system.cfg
43	if [ -z "${password}" ]; then
44	    log "RetroAchievements password is empty, please log in with your RetroAchievements credentials in Emulation Station."
45	    enabled="0"
46	    password="null"
47	fi
48	
49	# Check if api token is present in system.cfg
50	if [ -z "${token}" ]; then
51	    log "RetroAchievements token is empty, please log in with your RetroAchievements credentials in Emulation Station."
52	    enabled="0"
53	    token="null"
54	fi
55	
56	# Set hardcore mode
57	if [ "${hardcore}" = 1 ]; then
58	  hardcore="1"
59	else
60	  hardcore="0"
61	fi
62	
63	# Set encore mode
64	if [ "${encore}" = 1 ]; then
65	  encore="1"
66	else
67	  encore="0"
68	fi
69	
70	# Set unofficial mode
71	if [ "${unofficial}" = 1 ]; then
72	  unofficial="1"
73	else
74	  unofficial="0"
75	fi
76	
77	# Clean up any special characters
78	escape_sed() {
79	  printf '%s\n' "$1" | sed 's/[\/&]/\\&/g'
80	}
81	
82	username_esc=$(escape_sed "${username}")
83	password_esc=$(escape_sed "${password}")
84	token_esc=$(escape_sed "${token}")
85	
86	# Update emulator config with RetroAchievements settings
87	set_key() {
88	  key="$1"
89	  value="$2"
90	
91	  if grep -q "^[[:space:]]*${key}[[:space:]]*=" "${MELONDS_CFG}"; then
92	    sed -i "s|^[[:space:]]*${key}[[:space:]]*=.*|${key}=${value}|g" "${MELONDS_CFG}"
93	  else
94	    printf '%s=%s\n' "${key}" "${value}" >> "${MELONDS_CFG}"
95	  fi
96	}
97	
98	set_key RA_Enabled "${enabled}"
99	set_key RA_Username "${username_esc}"
100	set_key RA_Password "${password_esc}"
101	set_key RA_Token "${token_esc}"
102	set_key RA_HardcoreMode "${hardcore}"
103	set_key RA_EncoreMode "${encore}"
104	set_key RA_Unofficial "${unofficial}"
```

### `projects/ROCKNIX/packages/emulators/standalone/melonds-sa/scripts/start_melonds.sh`

```
1	#!/bin/bash
2	
3	# SPDX-License-Identifier: GPL-2.0-or-later
4	# Copyright (C) 2022-present JELOS (https://github.com/JustEnoughLinuxOS)
5	
6	. /etc/profile
7	
8	set_kill set "-9 melonDS"
9	
10	#load gptokeyb support files
11	control-gen_init.sh
12	source /storage/.config/gptokeyb/control.ini
13	get_controls
14	
15	CONF_DIR="/storage/.config/melonDS"
16	MELONDS_INI="melonDS.ini"
17	SWAY_CONFIG="/storage/.config/sway/config"
18	
19	if [ ! -d "${CONF_DIR}" ]; then
20		cp -r "/usr/config/melonDS" "/storage/.config/"
21	fi
22	
23	if [ ! -d "/storage/roms/savestates/nds" ]; then
24		mkdir -p "/storage/roms/savestates/nds"
25	fi
26	
27	#Make sure melonDS gptk config exists
28	if [ ! -f "${CONF_DIR}/melonDS.gptk" ]; then
29		cp -r "/usr/config/melonDS/melonDS.gptk" "${CONF_DIR}/melonDS.gptk"
30	fi
31	
32	#Make sure melonDS config exists
33	if [ ! -f "${CONF_DIR}/${MELONDS_INI}" ]; then
34		cp -r "/usr/config/melonDS/melonDS.ini" "${CONF_DIR}/${MELONDS_INI}"
35	fi
36	
37	#Emulation Station Features
38	GAME=$(echo "${1}" | sed "s#^/.*/##")
39	PLATFORM=$(echo "${2}"| sed "s#^/.*/##")
40	CONTYPE=$(get_setting console_type "${PLATFORM}" "${GAME}")
41	DBOOT=$(get_setting direct_boot "${PLATFORM}" "${GAME}")
42	GRENDERER=$(get_setting graphics_backend "${PLATFORM}" "${GAME}")
43	IRES=$(get_setting internal_resolution "${PLATFORM}" "${GAME}")
44	SORIENTATION=$(get_setting screen_orientation "${PLATFORM}" "${GAME}")
45	SLAYOUT=$(get_setting screen_layout "${PLATFORM}" "${GAME}")
46	SWAP=$(get_setting screen_swap "${PLATFORM}" "${GAME}")
47	SROTATION=$(get_setting screen_rotation "${PLATFORM}" "${GAME}")
48	VSYNC=$(get_setting vsync "${PLATFORM}" "${GAME}")
49	
50	#Set the cores to use
51	CORES=$(get_setting "cores" "${PLATFORM}" "${GAME}")
52	unset EMUPERF
53	[ "${CORES}" = "little" ] && EMUPERF="${SLOW_CORES}"
54	[ "${CORES}" = "big" ] && EMUPERF="${FAST_CORES}"
55	
56	#Console Type
57	if [ "$PLATFORM" = "ndsiware" ]; then
58	    sed -i '/^ConsoleType=/c\ConsoleType=1' /storage/.config/melonDS/melonDS.ini
59	else
60	    if [ "$CONTYPE" = "1" ]; then
61	        sed -i '/^ConsoleType=/c\ConsoleType=1' /storage/.config/melonDS/melonDS.ini
62	    else
63	        sed -i '/^ConsoleType=/c\ConsoleType=0' /storage/.config/melonDS/melonDS.ini
64	    fi
65	fi
66	
67	#Direct Boot
68	if [ "$PLATFORM" = "ndsiware" ]; then
69	    sed -i '/^DirectBoot=/c\DirectBoot=0' /storage/.config/melonDS/melonDS.ini
70	else
71	    if [ "$DBOOT" = "0" ]; then
72	        sed -i '/^DirectBoot=/c\DirectBoot=0' /storage/.config/melonDS/melonDS.ini
73	        sed -i '/^ExternalBIOSEnable=/c\ExternalBIOSEnable=1' /storage/.config/melonDS/melonDS.ini
74	    else
75	        sed -i '/^DirectBoot=/c\DirectBoot=1' /storage/.config/melonDS/melonDS.ini
76	        sed -i '/^ExternalBIOSEnable=/c\ExternalBIOSEnable=0' /storage/.config/melonDS/melonDS.ini
77	    fi
78	fi
79	
80	#Graphics Backend
81	case "$GRENDERER" in
82	  "1"|"2")
83	    sed -i "/^ScreenUseGL=/c\ScreenUseGL=1" "${CONF_DIR}/${MELONDS_INI}"
84	    sed -i "/^3DRenderer=/c\3DRenderer=$GRENDERER" "${CONF_DIR}/${MELONDS_INI}"
85	  ;;
86	  *)
87	    sed -i '/^ScreenUseGL=/c\ScreenUseGL=0' "${CONF_DIR}/${MELONDS_INI}"
88	    sed -i '/^3DRenderer=/c\3DRenderer=0' "${CONF_DIR}/${MELONDS_INI}"
89	  ;;
90	esac
91	
92	#Internal Resolution
93	if [ "$IRES" > "0" ]; then
94	        sed -i "/^GL_ScaleFactor=/c\GL_ScaleFactor=$IRES" "${CONF_DIR}/${MELONDS_INI}"
95	else
96	        sed -i '/^GL_ScaleFactor=/c\GL_ScaleFactor=1' "${CONF_DIR}/${MELONDS_INI}"
97	fi
98	
99	#Screen Orientation
100	if [ "$SORIENTATION" > "0" ]; then
101		sed -i "/^ScreenLayout=/c\ScreenLayout=$SORIENTATION" "${CONF_DIR}/${MELONDS_INI}"
102	else
103		sed -i '/^ScreenLayout=/c\ScreenLayout=2' "${CONF_DIR}/${MELONDS_INI}"
104	fi
105	
106	#Screen Layout
107	# Screen Layout
108	sed -i '/^Screen1Enabled=/c\Screen1Enabled=0' "${CONF_DIR}/${MELONDS_INI}"
109	
110	enable_second_screen() {
111	    sed -i '/^ScreenSizing=/c\ScreenSizing=4' "${CONF_DIR}/${MELONDS_INI}"
112	    sed -i '/^Screen1Enabled=/d$ a Screen1Enabled=1' "${CONF_DIR}/${MELONDS_INI}"
113	    sed -i '/^Screen1Layout=/d$ a Screen1Layout=2' "${CONF_DIR}/${MELONDS_INI}"
114	}
115	
116	if [ "$SLAYOUT" = "6" ]; then
117	    enable_second_screen
118	elif [ -n "$SLAYOUT" ] && [ "$SLAYOUT" != "0" ]; then
119	    sed -i "/^ScreenSizing=/c\ScreenSizing=$SLAYOUT" "${CONF_DIR}/${MELONDS_INI}"
120	elif [ "${DEVICE_HAS_DUAL_SCREEN}" = "true" ]; then
121	    enable_second_screen
122	else
123	    sed -i '/^ScreenSizing=/c\ScreenSizing=0' "${CONF_DIR}/${MELONDS_INI}"
124	fi
125	
126	# Screen Swap
127	if [[ "${DEVICE_HAS_DUAL_SCREEN}" = "true" && ( -z "$SLAYOUT" || "$SLAYOUT" = "6" ) ]]; then
128	    if [ "$SWAP" = "1" ]; then
129	        sed -i '/^ScreenSizing=/c\ScreenSizing=5' "${CONF_DIR}/${MELONDS_INI}"
130	        sed -i '/^Screen1Sizing=/d$ a Screen1Sizing=4' "${CONF_DIR}/${MELONDS_INI}"
131	    else
132	        sed -i '/^ScreenSizing=/c\ScreenSizing=4' "${CONF_DIR}/${MELONDS_INI}"
133	        sed -i '/^Screen1Sizing=/d$ a Screen1Sizing=5' "${CONF_DIR}/${MELONDS_INI}"
134	    fi
135	else
136	    sed -i "/^ScreenSwap=/c\ScreenSwap=${SWAP:-0}" "${CONF_DIR}/${MELONDS_INI}"
137	fi
138	
139	#Screen Rotation
140	if [ "$SROTATION" ] >"0"; then
141		sed -i "/^ScreenRotation=/c\ScreenRotation=$SROTATION" "${CONF_DIR}/${MELONDS_INI}"
142	else
143		sed -i '/^ScreenRotation=/c\ScreenRotation=0' "${CONF_DIR}/${MELONDS_INI}"
144	fi
145	
146	#Vsync
147	if [ "$VSYNC" = "1" ]; then
148		sed -i '/^ScreenVSync=/c\ScreenVSync=1' "${CONF_DIR}/${MELONDS_INI}"
149	else
150		sed -i '/^ScreenVSync=/c\ScreenVSync=0' "${CONF_DIR}/${MELONDS_INI}"
151	fi
152	
153	# Extract archive to /tmp/melonds
154	TEMP="/tmp/melonds"
155	rm -rf "${TEMP}"
156	mkdir -p "${TEMP}"
157	if [[ "${1}" == *.zip ]]; then
158	    unzip -o "${1}" -d "${TEMP}"
159	    ROM=$(find "${TEMP}" -maxdepth 1 -type f -name "*.nds" | head -n 1)
160	elif [[ "${1}" == *.7z ]]; then
161	    7z x -y -o"${TEMP}" "${1}"
162	    ROM=$(find "${TEMP}" -maxdepth 1 -type f -name "*.nds" | head -n 1)
163	else
164	    ROM="${1}"
165	fi
166	
167	# QT platform - default to xcb
168	export QT_QPA_PLATFORM=xcb
169	
170	# QT platform - some device / driver combinations need wayland
171	case ${HW_DEVICE} in
172	    RK3566|RK3588|S922X)
173	        [[ $(/usr/bin/gpudriver) == "libmali" ]] && export QT_QPA_PLATFORM=wayland
174	    ;;
175	esac
176	
177	@PANFROST@
178	@HOTKEY@
179	@LIBMALI@
180	
181	#Generate a new MelonDS.toml each run (temporary hack)
182	rm -rf "${CONF_DIR}/melonDS.toml"
183	
184	#Retroachievements
185	/usr/bin/cheevos_melonds.sh
186	
187	#Run MelonDS emulator
188	$GPTOKEYB "melonDS" -c "${CONF_DIR}/melonDS.gptk" &
189	${EMUPERF} /usr/bin/melonDS -f "${ROM}"
190	kill -9 "$(pidof gptokeyb)"
```

### `projects/ROCKNIX/packages/emulators/standalone/mupen64plus-sa/mupen64plus-sa-core/scripts/start_mupen64plus.sh`

```
1	#!/bin/bash
2	
3	# SPDX-License-Identifier: GPL-2.0-or-later
4	# Copyright (C) 2021-present 351ELEC (https://github.com/351ELEC)
5	# Copyright (C) 2022-present JELOS (https://github.com/JustEnoughLinuxOS)
6	
7	. /etc/profile
8	
9	set_kill set "-9 mupen64plus"
10	
11	# Emulation Station features
12	GAME=$(echo "${1}"| sed "s#^/.*/##")
13	PLATFORM=$(echo "${2}"| sed "s#^/.*/##")
14	SCREENWIDTH=$(fbwidth)
15	SCREENHEIGHT=$(fbheight)
16	ASPECT=$(get_setting game_aspect_ratio "${PLATFORM}" "${GAME}")
17	IRES=$(get_setting internal_resolution "${PLATFORM}" "${GAME}")
18	RSP=$(get_setting rsp_plugin "${PLATFORM}" "${GAME}")
19	SIMPLECORE=$(get_setting core_plugin "${PLATFORM}" "${GAME}")
20	FPS=$(get_setting show_fps "${PLATFORM}" "${GAME}")
21	PAK=$(get_setting controller_pak "${PLATFORM}" "${GAME}")
22	CON=$(get_setting input_configuration "${PLATFORM}" "${GAME}")
23	VPLUGIN=$(get_setting video_plugin "${PLATFORM}" "${GAME}")
24	CORES=$(get_setting "cores" "${PLATFORM}" "${GAME}")
25	GLIDEN64CONF=$(get_setting gliden64_profiles "${PLATFORM}" "${GAME}")
26	
27	# File locations
28	SHARE="/usr/local/share/mupen64plus"
29	GAMEDATA="/storage/.config/mupen64plus"
30	M64PCONF="${GAMEDATA}/mupen64plus.cfg"
31	CUSTOMINP="${GAMEDATA}/custominput.ini"
32	TMP="/tmp/mupen64plus"
33	
34	# Clean and create directories
35	rm -rf ${TMP}
36	mkdir -p ${TMP}
37	mkdir -p ${GAMEDATA}
38	
39	# Copy files to GAMEDATA
40	if [[ ! -f "${M64PCONF}" ]]; then
41	    cp ${SHARE}/mupen64plus.cfg* ${GAMEDATA}
42	fi
43	if [[ ! -f "${CUSTOMINP}" ]]; then
44	    cp ${SHARE}/default.ini ${CUSTOMINP}
45	fi
46	
47	# ROCKNIX: GENERIC_X64 repair begin
48	# GENERIC_X64's seed carried six lines of an InputAutoCfg.ini block inside
49	# [Input-SDL-Control1] until the fork fixed it (a "; Retroid Pocket Gamepad"
50	# comment, a [Retroid Pocket Gamepad] header and four settings), so a copy
51	# made from it holds Control1's mappings in a section nothing reads. Those
52	# six lines, and nothing else, leave such a copy -- written to a temporary
53	# file and moved over the old one only when it has content; the player's
54	# other settings stay. Other devices' copies are not touched.
55	if [ "${HW_DEVICE}" = "GENERIC_X64" ] && grep -qx '\[Retroid Pocket Gamepad\]' "${M64PCONF}" 2>/dev/null; then
56	    awk 'BEGIN { b[1] = "; Retroid Pocket Gamepad - default.ini"; b[2] = "[Retroid Pocket Gamepad]"
57	                 b[3] = "plugged = True"; b[4] = "mouse = False"; b[5] = "AnalogDeadzone = 0,0"; b[6] = "AnalogPeak = 32768,32768" }
58	         { l[NR] = $0 }
59	         END { for (i = 1; i <= NR; i++) {
60	                   m = (i + 5 <= NR)
61	                   for (j = 1; m && j <= 6; j++) if (l[i + j - 1] != b[j]) m = 0
62	                   if (m) { i += 5; continue }
63	                   print l[i] } }' "${M64PCONF}" > "${M64PCONF}.repair" \
64	      && [ -s "${M64PCONF}.repair" ] && mv -f "${M64PCONF}.repair" "${M64PCONF}" \
65	      || rm -f "${M64PCONF}.repair"
66	fi
67	# ROCKNIX: GENERIC_X64 repair end
68	
69	# Copy files to TMP
70	cp ${M64PCONF} ${TMP}
71	if [ "${CON}" = "custom" ]; then
72	    cp ${CUSTOMINP} ${TMP}/InputAutoCfg.ini
73	elif [ "${CON}" = "standard" ]; then
74	    cp ${SHARE}/default.ini ${TMP}/InputAutoCfg.ini
75	else
76	    cp ${SHARE}/default.ini ${TMP}/InputAutoCfg.ini
77	fi
78	if [ $(echo $1 | grep -i .zip | wc -l) -eq 1 ]; then
79	    # Unzip the game ROM if needed
80	    unzip -q -o "$1" -d ${TMP}
81	    ROM=$(unzip -Zl -1 "$1")
82	else
83	    cp "$1" ${TMP}
84	    ROM="${GAME}"
85	fi
86	
87	# CPU core settings
88	if [ "${CORES}" = "little" ]; then
89	    EMUPERF="${SLOW_CORES}"
90	elif [ "${CORES}" = "big" ]; then
91	    EMUPERF="${FAST_CORES}"
92	else
93	    unset EMUPERF
94	fi
95	
96	# Configure Mupen64Plus-SA parameters
97	SET_PARAMS=""
98	
99	# Emulator core settings
100	SET_PARAMS+=" --set Core[SharedDataPath]=${TMP}"
101	if [ "${SIMPLECORE}" = "simple" ]; then
102	    SIMPLESUFFIX="-simple"
103	    SET_PARAMS+=" --set Core[R4300Emulator]=1"
104	else
105	    SIMPLESUFFIX=""
106	    SET_PARAMS+=" --set Core[R4300Emulator]=2"
107	fi
108	
109	# Input settings
110	SET_PARAMS+=" --set Input-SDL-Control1[plugin]=${PAK}"
111	SET_PARAMS+=" --set Input-SDL-Control2[plugin]=${PAK}"
112	SET_PARAMS+=" --set Input-SDL-Control3[plugin]=${PAK}"
113	SET_PARAMS+=" --set Input-SDL-Control4[plugin]=${PAK}"
114	
115	# Video settings
116	SET_PARAMS+=" --set Video-General[ScreenHeight]=${SCREENHEIGHT}"
117	SET_PARAMS+=" --set Video-Parallel[ScreenWidth]=${SCREENWIDTH}"
118	SET_PARAMS+=" --set Video-Parallel[ScreenHeight]=${SCREENHEIGHT}"
119	SET_PARAMS+=" --set Video-Parallel[Upscaling]=${IRES}"
120	SET_PARAMS+=" --set Video-GLideN64[UseNativeResolutionFactor]=${IRES}"
121	SET_PARAMS+=" --set Video-Rice[ResolutionWidth]=${SCREENWIDTH}"
122	if [ "${ASPECT}" = "fullscreen" ]; then
123	    SET_PARAMS+=" --set Video-General[ScreenWidth]=${SCREENWIDTH}"
124	    SET_PARAMS+=" --set Video-Parallel[WidescreenStretch]=False"
125	    SET_PARAMS+=" --set Video-GLideN64[AspectRatio]=3"
126	    SET_PARAMS+=" --set Video-Glide64mk2[aspect]=2"
127	else
128	    if [ -z "${VPLUGIN}" ] || [ "${VPLUGIN}" = "rice" ]; then
129	        GAMEWIDTH=$(((SCREENHEIGHT * 4) / 3))
130	        SET_PARAMS+=" --set Video-General[ScreenWidth]=${GAMEWIDTH}"
131	    else
132	        SET_PARAMS+=" --set Video-General[ScreenWidth]=${SCREENWIDTH}"
133	    fi
134	    SET_PARAMS+=" --set Video-Parallel[WidescreenStretch]=False"
135	    SET_PARAMS+=" --set Video-GLideN64[AspectRatio]=1"
136	    SET_PARAMS+=" --set Video-Glide64mk2[aspect]=0"
137	fi
138	if [ "${FPS}" = "true" ]; then
139	    export LIBGL_SHOW_FPS="1"
140	    export GALLIUM_HUD="cpu+GPU-load+fps"
141	    SET_PARAMS+=" --set Video-GLideN64[ShowFPS]=True"
142	    SET_PARAMS+=" --set Video-Glide64mk2[show_fps]=1"
143	    SET_PARAMS+=" --set Video-Rice[ShowFPS]=True"
144	else
145	    export LIBGL_SHOW_FPS="0"
146	    export GALLIUM_HUD="off"
147	    SET_PARAMS+=" --set Video-GLideN64[ShowFPS]=False"
148	    SET_PARAMS+=" --set Video-Glide64mk2[show_fps]=0"
149	    SET_PARAMS+=" --set Video-Rice[ShowFPS]=False"
150	fi
151	
152	# GLideN64 Profiles
153	if [ "${GLIDEN64CONF}" = "performance" ]; then
154		SET_PARAMS+=" --set Video-GLideN64[EnableLOD]=False"
155		SET_PARAMS+=" --set Video-GLideN64[EnableLegacyBlending]=True"
156		SET_PARAMS+=" --set Video-GLideN64[EnableHybridFilter]=False"
157		SET_PARAMS+=" --set Video-GLideN64[EnableInaccurateTextureCoordinates]=True"
158		SET_PARAMS+=" --set Video-GLideN64[EnableCopyColorToRDRAM]=0"
159		SET_PARAMS+=" --set Video-GLideN64[EnableCopyDepthToRDRAM]=0"
160		SET_PARAMS+=" --set Video-GLideN64[BackgroundsMode]=0"
161		SET_PARAMS+=" --set Video-GLideN64[RDRAMImageDitheringMode]=0"
162		SET_PARAMS+=" --set Video-GLideN64[CorrectTexrectCoords]=0"
163	else
164		SET_PARAMS+=" --set Video-GLideN64[EnableLOD]=True"
165		SET_PARAMS+=" --set Video-GLideN64[EnableLegacyBlending]=False"
166		SET_PARAMS+=" --set Video-GLideN64[EnableHybridFilter]=False"
167		SET_PARAMS+=" --set Video-GLideN64[EnableInaccurateTextureCoordinates]=False"
168		SET_PARAMS+=" --set Video-GLideN64[EnableCopyColorToRDRAM]=2"
169	fi
170	
171	# Set the video plugin
172	case ${VPLUGIN} in
173	    "rmg_parallel")
174	        SET_PARAMS+=" --gfx mupen64plus-video-parallel${SIMPLESUFFIX}.so"
175	        RSP="parallel"
176	    ;;
177	    "gliden64")
178	        SET_PARAMS+=" --gfx mupen64plus-video-GLideN64${SIMPLESUFFIX}.so"
179	    ;;
180	    "gl64mk2")
181	        SET_PARAMS+=" --gfx mupen64plus-video-glide64mk2${SIMPLESUFFIX}.so"
182	    ;;
183	    "rice")
184	        SET_PARAMS+=" --gfx mupen64plus-video-rice${SIMPLESUFFIX}.so"
185	    ;;
186	    *)
187	        SET_PARAMS+=" --gfx mupen64plus-video-rice${SIMPLESUFFIX}.so"
188	    ;;
189	esac
190	
191	# Set the RSP plugin
192	case "${RSP}" in
193	    "parallel")
194	        SET_PARAMS+=" --rsp mupen64plus-rsp-parallel${SIMPLESUFFIX}.so"
195	    ;;
196	    "hle")
197	        SET_PARAMS+=" --rsp mupen64plus-rsp-hle${SIMPLESUFFIX}.so"
198	    ;;
199	    *)
200	        SET_PARAMS+=" --rsp mupen64plus-rsp-cxd4${SIMPLESUFFIX}.so"
201	    ;;
202	esac
203	
204	# Set the remaining plugins
205	SET_PARAMS+=" --input mupen64plus-input-sdl${SIMPLESUFFIX}.so"
206	SET_PARAMS+=" --audio mupen64plus-audio-sdl${SIMPLESUFFIX}.so"
207	
208	# Echo the command line options to the log for debugging
209	echo ${SET_PARAMS}
210	
211	${EMUPERF} /usr/local/bin/mupen64plus${SIMPLESUFFIX} --configdir ${TMP} ${SET_PARAMS} "${TMP}/${ROM}"
```

### `projects/ROCKNIX/packages/emulators/standalone/nanoboyadvance-sa/scripts/start_nanoboyadvance.sh`

```
1	#!/bin/bash
2	
3	# SPDX-License-Identifier: GPL-2.0-or-later
4	# Copyright (C) 2022-present JELOS (https://github.com/JustEnoughLinuxOS)
5	
6	. /etc/profile
7	set_kill set "-9 NanoBoyAdvance"
8	
9	#Check if nanoboyadvance exists in .config
10	if [ ! -d "/storage/.config/nanoboyadvance" ]; then
11	    mkdir -p "/storage/.config/nanoboyadvance"
12	        cp -r "/usr/config/nanoboyadvance" "/storage/.config/"
13	fi
14	
15	#Make nanoboyadvance bios folder
16	if [ ! -d "/storage/roms/bios/gba" ]; then
17	    mkdir -p "/storage/roms/bios/gba"
18	fi
19	
20	#Copy open source bios if no other bios exists
21	if [ ! -f "/storage/roms/bios/gba/gba_bios.bin" ]; then
22	  cp -r "/usr/config/nanoboyadvance" "/storage/roms/bios/gba/gba_bios.bin"
23	fi
24	
25	#Set the cores to use
26	GAME=$(echo "${1}"| sed "s#^/.*/##")
27	PLATFORM=$(echo "${2}"| sed "s#^/.*/##")
28	CORES=$(get_setting "cores" "${PLATFORM}" "${GAME}")
29	if [ "${CORES}" = "little" ]
30	then
31	  EMUPERF="${SLOW_CORES}"
32	elif [ "${CORES}" = "big" ]
33	then
34	  EMUPERF="${FAST_CORES}"
35	else
36	  ### All..
37	  unset EMUPERF
38	fi
39	
40	#Run nanoboyadvance emulator
41	${EMUPERF} /usr/bin/NanoBoyAdvance "${1}"
```

### `projects/ROCKNIX/packages/emulators/standalone/openbor/scripts/start_OpenBOR.sh`

```
1	#!/bin/sh
2	# SPDX-License-Identifier: GPL-2.0-or-later
3	# Copyright (C) 2019-present Shanti Gilbert (https://github.com/shantigilbert)
4	# Copyright (C) 2021-present 351ELEC (https://github.com/351ELEC)
5	# Copyright (C) 2023 JELOS (https://github.com/JustEnoughLinuxOS)
6	
7	# OpenBOR only works with Pak files, if you have an extracted game you will need to create a pak first.
8	
9	pakname=$(basename "$1")
10	pakname="${pakname%.*}"
11	
12	CONFIGDIR="/storage/openbor"
13	PAKS="${CONFIGDIR}/Paks"
14	SAVES="${CONFIGDIR}/Saves"
15	
16	# Make sure the folders exists
17	  mkdir -p "${CONFIGDIR}"
18	  mkdir -p "${PAKS}"
19	  mkdir -p "${SAVES}"
20	
21	# Check if master.cfg exists
22	  if [ ! -f "${CONFIGDIR}/master.cfg" ]; then
23	    cp -f "/usr/config/openbor/master.cfg" "${CONFIGDIR}/"
24	  fi
25	
26	# Clear PAKS folder to avoid getting the launcher on next run
27	  rm -rf ${PAKS}/*
28	
29	# make a symlink to the pak
30	  ln -sf "$1" "${PAKS}"
31	
32	# only create symlink to master.cfg if its the first time running the pak
33	  if [ ! -f "${SAVES}/${pakname}.cfg" ]; then
34	    ln -sf "${CONFIGDIR}/master.cfg" "${SAVES}/${pakname}.cfg"
35	  fi
36	
37	# We start the fake keyboard
38	  gptokeyb openbor &
39	
40	# Run OpenBOR in the config folder
41	  cd "${CONFIGDIR}"
42	  OpenBOR
43	
44	# We stop the fake keyboard
45	  killall gptokeyb &
```

### `projects/ROCKNIX/packages/emulators/standalone/pico-8/scripts/start_pico8.sh`

```
1	#!/bin/bash
2	# SPDX-License-Identifier: GPL-2.0-or-later
3	# Copyright (C) 2023 JELOS (https://github.com/JustEnoughLinuxOS)
4	
5	# Source predefined functions and variables
6	. /etc/profile
7	
8	GAME_DIR="/storage/roms/pico-8/"
9	
10	case ${HW_ARCH} in
11	  aarch64)
12	    STATIC_BIN="pico8_64"
13	  ;;
14	  *)
15	    STATIC_BIN="pico8_dyn"
16	  ;;
17	esac
18	
19	# check if the file being launched contains "Splore" and if so launch Pico-8 Splore otherwise run the game directly
20	shopt -s nocasematch
21	if [[ "${1}" == *splore* ]]; then
22	  OPTIONS="-splore"
23	else
24	  OPTIONS="-run"
25	  CART="${1}"
26	fi
27	shopt -u nocasematch
28	
29	INTEGER_SCALE=$(get_setting pico-8.integerscale)
30	if [ "${INTEGER_SCALE}" = "1" ]
31	then
32	  OPTIONS="${OPTIONS} -pixel_perfect 1"
33	fi
34	
35	if [ -d "${GAME_DIR}/${HW_ARCH}" ]
36	then
37	  LAUNCH_DIR="${GAME_DIR}/${HW_ARCH}"
38	else
39	  LAUNCH_DIR="${GAME_DIR}"
40	fi
41	
42	# store sdl_controllers in root directory so its shared across devices - will look to revisit this with controller refactor work
43	cp -f /usr/config/SDL-GameControllerDB/gamecontrollerdb.txt ${GAME_DIR}/sdl_controllers.txt
44	
45	# mark the binary executable to cover cases where the user adding the binaries doesn't know or forgets.
46	chmod 0755 ${LAUNCH_DIR}/${STATIC_BIN}
47	set_kill set "-9 ${STATIC_BIN} start_pico8.sh"
48	${LAUNCH_DIR}/${STATIC_BIN} -home -root_path ${GAME_DIR} -joystick 0 ${OPTIONS} "${CART}"
```

### `projects/ROCKNIX/packages/emulators/standalone/ppsspp-sa/scripts/cheevos_ppsspp.sh`

```
1	#! /bin/bash
2	
3	# SPDX-License-Identifier: GPL-2.0-or-later
4	# Copyright (C) 2022-present Hector Calvarro (https://github.com/kelvfimer)
5	# Copyright (C) 2024-present ROCKNIX (https://github.com/ROCKNIX)
6	
7	. /etc/profile
8	
9	PPSSPP_ACHIEVEMENTS="/storage/.config/ppsspp/PSP/SYSTEM/ppsspp_retroachievements.dat"
10	PPSSPP_INI="/storage/.config/ppsspp/PSP/SYSTEM/ppsspp.ini"
11	LOG_FILE="/var/log/cheevos.log"
12	
13	# Extract username, password, token, if enabled, and hardcore mode from system.cfg
14	username=$(get_setting "global.retroachievements.username")
15	password=$(get_setting "global.retroachievements.password")
16	token=$(get_setting "global.retroachievements.token")
17	enabled=$(get_setting "global.retroachievements")
18	hardcore=$(get_setting "global.retroachievements.hardcore")
19	
20	# Check if RetroAchievements are enabled in Emulation Station. Quoted: an
21	# empty read used to make the test a syntax error that fell through to
22	# "enabled" (audit #186 PL-31).
23	if [ "${enabled}" != "1" ]; then
24	    echo "RetroAchievements are not enabled, please turn them on in Emulation Station." > ${LOG_FILE}
25	    sed -i '/^AchievementsEnable =/c\AchievementsEnable = False' ${PPSSPP_INI}
26	    exit 1
27	fi
28	
29	# Check if api token is present in system.cfg
30	if [ -z "${token}" ]; then
31	    echo "RetroAchievements token is empty, please log in with your RetroAchievements credentials in Emulation Station." > ${LOG_FILE}
32	    exit 1
33	fi
34	
35	echo "${token}" > ${PPSSPP_ACHIEVEMENTS}
36	
37	# Set hardcore mode
38	hardcore_raw="${hardcore}"
39	if [ "${hardcore}" = 1 ]; then
40	  hardcore="True"
41	else
42	  hardcore="False"
43	fi
44	
45	# OFFLINE RETROACHIEVEMENTS (fork #165, D-RA-002): PPSSPP's own achievements
46	# client behind AchievementsHost, pointed at the RAOfflineProxy service on
47	# loopback when the toggle is on, hardcore is off (the proxy refuses hardcore
48	# awards) and the port answers -- a host with nothing behind it would disable
49	# achievements for the session. Empty otherwise, which is PPSSPP's default
50	# host: this file travels in a settings backup, so a restored device with the
51	# toggle off must find the line cleared, not pointing at a dead port.
52	# PPSSPP reads the key from ppsspp.ini's [Achievements] (Core/Config.cpp:376
53	# at the pinned v1.20.2, afbc66a3) and, when it is not empty, hands it to
54	# rcheevos as the host (rc_client_set_host, Core/RetroAchievements.cpp:650-652)
55	# -- "a custom host, only useful for debugging against non-prod RA
56	# environments" in its own words, which is what the proxy is (#308 F-EM-07).
57	# Routed only when hardcore READ as off ("0" -- raofflineproxy-ctl enable
58	# writes the key), never when it read as nothing: an empty answer is a key
59	# that could not be read as much as one that is unset, and the proxy
60	# refuses hardcore awards, so unknown keeps the direct path (#186 PL-31).
61	#
62	# Whether the proxy is listening is read from the kernel's socket tables with
63	# bash's own read, not from netstat, which nothing PPSSPP ships declares and
64	# whose absence read as "nothing answers" (#308 F-EM-04): 127.0.0.1, 0.0.0.0
65	# or ::ffff:127.0.0.1 on port 8080 (1F90) in state LISTEN (0A) -- the
66	# listeners that take the IPv4 connection to 127.0.0.1:8080 PPSSPP is
67	# given. ::1 does not take it, and :: may be IPv6-only, which the table does
68	# not say, so neither counts (audit of the fixes, gpt G-D-02, gpt G-F2-02).
69	# That turns the proxy away never: its sockets are IPv4 (AF_INET in the
70	# client's proxy_service.py and boot.py), and the scripts suite holds this
71	# check and raofflineproxy-ctl's to the pinned client's own socket (audit of
72	# the fix round, claude G2-D-01, PL-033).
73	# 0 listening, 1 not, 2 when neither table could be read -- said apart in the
74	# log, since "couldn't tell" is not "nothing there". RAOFFLINEPROXY_PROC_NET
75	# stands in for /proc/net in the scripts suite, as it does for
76	# raofflineproxy-ctl listening.
77	proxy_listening() {
78	  local proc="${RAOFFLINEPROXY_PROC_NET:-/proc/net}" f readable=0 sl addr rem st rest
79	  for f in "${proc}/tcp" "${proc}/tcp6"; do
80	    [ -r "${f}" ] || continue
81	    readable=1
82	    while read -r sl addr rem st rest; do
83	      [ "${st}" = "0A" ] || continue
84	      case "${addr}" in
85	        0100007F:1F90|00000000:1F90|0000000000000000FFFF00000100007F:1F90) return 0 ;;
86	      esac
87	    done < "${f}"
88	  done
89	  [ "${readable}" -eq 1 ] && return 1
90	  return 2
91	}
92	
93	host=""
94	if [ "$(get_setting "global.retroachievements.offlineproxy")" = 1 ] && [ "${hardcore_raw}" = "0" ]; then
95	  proxy_listening
96	  case $? in
97	    0) host="127.0.0.1:8080" ;;
98	    1) echo "Offline RetroAchievements is on but nothing is listening on 127.0.0.1:8080; launching direct." >> ${LOG_FILE} ;;
99	    *) echo "Offline RetroAchievements is on but this device couldn't tell whether the offline service is listening; launching direct." >> ${LOG_FILE} ;;
100	  esac
101	fi
102	
103	# Update emulator config with RetroAchievements settings
104	zcheevos=$(grep -Fx "[Achievements]" ${PPSSPP_INI})
105	echo "${token}" > ${PPSSPP_ACHIEVEMENTS}
106	
107	if [ -z "${zcheevos}" ]
108	then
109	    echo -e "[Achievements]\nAchievementsEnable = True\nAchievementsUserName = ${username}\nAchievementsChallengeMode = ${hardcore}\nAchievementsHost = ${host}" >> ${PPSSPP_INI}
110	else
111	    sed -i '/^AchievementsEnable =/c\AchievementsEnable = True' ${PPSSPP_INI}
112	    if ! grep -q "^AchievementsUserName = " ${PPSSPP_INI}; then
113	        sed -i "/^\[Achievements\]/a AchievementsUserName = ${username}" ${PPSSPP_INI}
114	    else
115	        sed -i "/^\[Achievements\]/,/^\[/{s/^AchievementsUserName = .*/AchievementsUserName = ${username}/;}" ${PPSSPP_INI}
116	    fi
117	
118	    if ! grep -q "^AchievementsChallengeMode = " ${PPSSPP_INI}; then
119	        sed -i "/^\[Achievements\]/a AchievementsChallengeMode = ${hardcore}" ${PPSSPP_INI}
120	    else
121	        sed -i "/^\[Achievements\]/,/^\[/{s/^AchievementsChallengeMode = .*/AchievementsChallengeMode = ${hardcore}/;}" ${PPSSPP_INI}
122	    fi
123	
124	    # Matched up to the "=", not past it: an empty value is written as
125	    # "AchievementsHost = " and PPSSPP may save it back without the space.
126	    if ! grep -q "^AchievementsHost =" ${PPSSPP_INI}; then
127	        sed -i "/^\[Achievements\]/a AchievementsHost = ${host}" ${PPSSPP_INI}
128	    else
129	        sed -i "/^\[Achievements\]/,/^\[/{s/^AchievementsHost =.*/AchievementsHost = ${host}/;}" ${PPSSPP_INI}
130	    fi
131	fi
```

### `projects/ROCKNIX/packages/emulators/standalone/ppsspp-sa/scripts/psp_save_mover.sh`

```
1	#!/bin/bash
2	
3	#This will copy saves to the correct directory after making changes to PPSSPP
4	if [ ! -d "/storage/roms/psp/PSP" ]; then
5	  mkdir -p "/storage/roms/psp/PSP"
6	  cp -r /storage/.config/ppsspp/PSP/SAVEDATA /storage/roms/psp/PSP/
7	fi
8	
9	if [ ! -d "/storage/roms/savestates/psp/ppsspp-sa" ]; then
10	  mkdir -p /storage/roms/savestates/psp/ppsspp-sa
11	  cp -r /storage/.config/ppsspp/PSP/PPSSPP_STATE/* /storage/roms/savestates/psp/ppsspp-sa/
12	fi
```

### `projects/ROCKNIX/packages/emulators/standalone/ppsspp-sa/scripts/start_ppsspp.sh`

```
1	#!/bin/sh
2	# SPDX-License-Identifier: GPL-2.0
3	# Copyright (C) 2023 JELOS (https://github.com/JustEnoughLinuxOS)
4	
5	. /etc/profile
6	set_kill set "-9 ppsspp"
7	
8	SOURCE_DIR="/usr/config/ppsspp"
9	CONF_DIR="/storage/.config/ppsspp"
10	PPSSPP_INI="PSP/SYSTEM/ppsspp.ini"
11	
12	# Check if conf dir exists
13	if [ ! -d "${CONF_DIR}" ]
14	then
15	  cp -rf ${SOURCE_DIR} ${CONF_DIR}
16	fi
17	
18	# Check if savestate dir exists
19	if [ ! -d "/storage/roms/savestates/psp/ppsspp-sa" ]; then
20	  mkdir -p "/storage/roms/savestates/psp/ppsspp-sa"
21	fi
22	
23	#Emulation Station Features
24	GAME=$(echo "${1}"| sed "s#^/.*/##")
25	PLATFORM=$(echo "${2}"| sed "s#^/.*/##")
26	ASKIP=$(get_setting auto_frame_skip "${PLATFORM}" "${GAME}")
27	FPS=$(get_setting show_fps "${PLATFORM}" "${GAME}")
28	IRES=$(get_setting internal_resolution "${PLATFORM}" "${GAME}")
29	GRENDERER=$(get_setting graphics_backend "${PLATFORM}" "${GAME}")
30	SKIPB=$(get_setting skip_buffer_effects "${PLATFORM}" "${GAME}")
31	VSYNC=$(get_setting vsync "${PLATFORM}" "${GAME}")
32	CLOCK_SPEED=$(get_setting clock_speed "${PLATFORM}" "${GAME}")
33	
34	#Set the cores to use
35	CORES=$(get_setting "cores" "${PLATFORM}" "${GAME}")
36	if [ "${CORES}" = "little" ]; then
37	  EMUPERF="${SLOW_CORES}"
38	elif [ "${CORES}" = "big" ]; then
39	  EMUPERF="${FAST_CORES}"
40	else
41	  ### All..
42	  unset EMUPERF
43	fi
44	
45	  #Auto Frame Skip
46		if [ "${ASKIP}" = "1" ]; then
47			sed -i '/AutoFrameSkip =/c\AutoFrameSkip = True' ${CONF_DIR}/${PPSSPP_INI}
48		else
49			sed -i '/^AutoFrameSkip =/c\AutoFrameSkip = False' ${CONF_DIR}/${PPSSPP_INI}
50	        fi
51	
52	  #Graphics Backend
53	        if [ "${GRENDERER}" = "opengl" ]; then
54	                sed -i '/^GraphicsBackend =/c\GraphicsBackend = 0 (OPENGL)' ${CONF_DIR}/${PPSSPP_INI}
55	        elif [ "${GRENDERER}" = "vulkan" ]; then
56	                sed -i '/^GraphicsBackend =/c\GraphicsBackend = 3 (VULKAN)' ${CONF_DIR}/${PPSSPP_INI}
57	        else
58			sed -i '/^GraphicsBackend =/c\GraphicsBackend = @GRENDERER@' ${CONF_DIR}/${PPSSPP_INI}
59		fi
60	
61	  #Internal Resolution
62		if [ "${IRES}" = "2" ]; then
63			sed -i '/^InternalResolution/c\InternalResolution = 2' ${CONF_DIR}/${PPSSPP_INI}
64		elif [ "${IRES}" = "3" ]; then
65			sed -i '/^InternalResolution/c\InternalResolution = 3' ${CONF_DIR}/${PPSSPP_INI}
66		elif [ "${IRES}" = "4" ]; then
67	                sed -i '/^InternalResolution/c\InternalResolution = 4' ${CONF_DIR}/${PPSSPP_INI}
68		else
69			sed -i '/^InternalResolution/c\InternalResolution = 1' ${CONF_DIR}/${PPSSPP_INI}
70	        fi
71	
72	  #Show FPS
73		if [ "${FPS}" = "1" ]; then
74			sed -i '/^iShowStatusFlags =/c\iShowStatusFlags = 2' ${CONF_DIR}/${PPSSPP_INI}
75		else
76			sed -i '/^iShowStatusFlags =/c\iShowStatusFlags = 0' ${CONF_DIR}/${PPSSPP_INI}
77		fi
78	
79	  #Skip Buffer Effects
80		if [ "${SKIPB}" = "1" ]; then
81			sed -i '/^SkipBufferEffects =/c\SkipBufferEffects = True' ${CONF_DIR}/${PPSSPP_INI}
82		else
83			sed -i '/^SkipBufferEffects =/c\SkipBufferEffects = False' ${CONF_DIR}/${PPSSPP_INI}
84		fi
85	
86	  #VSYNC
87		if [ "${VSYNC}" = "1" ]; then
88			sed -i '/^VSyncInterval =/c\VSyncInterval = True' ${CONF_DIR}/${PPSSPP_INI}
89		else
90			sed -i '/^VSyncInterval =/c\VSyncInterval = False' ${CONF_DIR}/${PPSSPP_INI}
91		fi
92	
93	  #Clock Speed
94		if [ "${CLOCK_SPEED}" = "222" ]; then
95			sed -i '/^CPUSpeed =/c\CPUSpeed = 222' ${CONF_DIR}/${PPSSPP_INI}
96	  elif [ "${CLOCK_SPEED}" = "333" ]; then
97			sed -i '/^CPUSpeed =/c\CPUSpeed = 333' ${CONF_DIR}/${PPSSPP_INI}
98		else
99			sed -i '/^CPUSpeed =/c\CPUSpeed = 0' ${CONF_DIR}/${PPSSPP_INI}
100		fi
101	
102	#Retroachievements
103	/usr/bin/cheevos_ppsspp.sh
104	
105	ARG=${1//[\\]/}
106	
107	# Debugging info:
108	  echo "GAME set to: ${GAME}"
109	  echo "PLATFORM set to: ${PLATFORM}"
110	  echo "CONF DIR: ${CONF_DIR}/${PPSSPP_INI}"
111	  echo "CPU CORES set to: ${EMUPERF}"
112	  echo "AUTO FRAME SKIP set to: ${ASKIP}"
113	  echo "GRAPHICS RENDERER set to: ${GRENDERER}"
114	  echo "INTERNAL RESOLUTION set to: ${IRES}"
115	  echo "FPS set to: ${FPS}"
116	  echo "SKIP BUFFER EFFECTS set to: ${SKIPB}"
117	  echo "VSYNC set to: ${VSYNC}"
118	  echo "Launching /usr/bin/ppsspp ${ARG}"
119	
120	${EMUPERF} ppsspp --pause-menu-exit "${ARG}"
```

### `projects/ROCKNIX/packages/emulators/standalone/rpcs3-sa/scripts/start_rpcs3.sh`

```
1	#!/bin/bash
2	
3	# SPDX-License-Identifier: GPL-2.0-or-later
4	# Copyright (C) 2022-present JELOS (https://github.com/JustEnoughLinuxOS)
5	
6	. /etc/profile
7	
8	# Check if rpcs3 exists in .config
9	if [ ! -d "/storage/.config/rpcs3" ]; then
10	  cp -r "/usr/config/rpcs3" "/storage/.config/"
11	fi
12	
13	# Link certain RPCS3 folders to a location in /storage/roms/bios
14	FOLDER_LINKS=("dev_flash" "dev_hdd0" "dev_hdd1" "custom_configs")
15	for FOLDER_LINK in "${FOLDER_LINKS[@]}"; do
16	  TARGET_FOLDER="/storage/roms/bios/rpcs3/$FOLDER_LINK"
17	  SOURCE_FOLDER="/storage/.config/rpcs3/$FOLDER_LINK"
18	
19	  # Create the target folder if it doesn't exist
20	  if [ ! -d "$TARGET_FOLDER" ]; then
21	      mkdir -p "$TARGET_FOLDER"
22	  fi
23	
24	  # Remove existing source folder
25	  rm -rf "$SOURCE_FOLDER"
26	
27	  # Create symbolic link
28	  ln -sf "$TARGET_FOLDER" "$SOURCE_FOLDER"
29	done
30	
31	#Emulation Station Features
32	GAME=$(echo "${1}"| sed "s#^/.*/##")
33	PLATFORM=$(echo "${2}"| sed "s#^/.*/##")
34	ASPECT=$(get_setting aspect_ratio "${PLATFORM}" "${GAME}")
35	ATEXTURE=$(get_setting async_texture_streaming "${PLATFORM}" "${GAME}")
36	FLIMIT=$(get_setting frame_limit "${PLATFORM}" "${GAME}")
37	GRENDERER=$(get_setting graphics_backend "${PLATFORM}" "${GAME}")
38	IPS3RES=$(get_setting internal_ps3_resolution "${PLATFORM}" "${GAME}")
39	IRES_SCALE=$(get_setting internal_resolution_scale "${PLATFORM}" "${GAME}")
40	MULTIRSX=$(get_setting multithreaded_rsx "${PLATFORM}" "${GAME}")
41	PERFOVERLAY=$(get_setting performance_overlay "${PLATFORM}" "${GAME}")
42	SPREC=$(get_setting shader_precision "${PLATFORM}" "${GAME}")
43	SPUXFLOAT=$(get_setting spu_xfloat_accuracy "${PLATFORM}" "${GAME}")
44	VSYNC=$(get_setting vsync "${PLATFORM}" "${GAME}")
45	WCOLORB=$(get_setting write_color_buffers "${PLATFORM}" "${GAME}")
46	ZCULLA=$(get_setting zcull_accuracy "${PLATFORM}" "${GAME}")
47	SUI=$(get_setting start_ui "${PLATFORM}" "${GAME}")
48	CONFIG_YML="/storage/.config/rpcs3/config.yml"
49	
50	#Aspect Ratio
51	if [ "${ASPECT}" = "4x3" ]; then
52	  sed -i "s#Aspect ratio:.*\$#Aspect ratio: 4:3#g" "${CONFIG_YML}"
53	else
54	  sed -i "s#Aspect ratio:.*\$#Aspect ratio: 16:9#g" "${CONFIG_YML}"
55	fi
56	
57	#Asynchronous Texture Streaming
58	if [ "${ATEXTURE}" = "true" ]; then
59	  sed -i "s#Asynchronous Texture Streaming 2:.*\$#Asynchronous Texture Streaming 2: true#g" "${CONFIG_YML}"
60	else
61	  sed -i "s#Asynchronous Texture Streaming 2:.*\$#Asynchronous Texture Streaming 2: false#g" "${CONFIG_YML}"
62	fi
63	
64	#Graphics Backend
65	if [ "$GRENDERER" = "vulkan" ]; then
66	  sed -i '/Video:/ {n; s/Renderer: .*/Renderer: Vulkan/}' "${CONFIG_YML}"
67	else
68	  sed -i '/Video:/ {n; s/Renderer: .*/Renderer: OpenGL/}' "${CONFIG_YML}"
69	fi
70	
71	#Internal Resolution
72	if [ "${FLIMIT}" = "30" ]; then
73	  sed -i "s#Frame limit:.*\$#Frame limit: 30#g" "${CONFIG_YML}"
74	elif [ "${FLIMIT}" = "60" ]; then
75	  sed -i "s#Frame limit:.*\$#Frame limit: 60#g" "${CONFIG_YML}"
76	else
77	  sed -i "s#Frame limit:.*\$#Frame limit: Auto#g" "${CONFIG_YML}"
78	fi
79	
80	#Internal Resolution
81	if [ "${IPS3RES}" = "576" ]; then
82	  sed -i "s#Resolution:.*\$#Resolution: 720x576#g" "${CONFIG_YML}"
83	elif [ "${IPS3RES}" = "720" ]; then
84	  sed -i "s#Resolution:.*\$#Resolution: 1280x720#g" "${CONFIG_YML}"
85	elif [ "${IPS3RES}" = "1080" ]; then
86	  sed -i "s#Resolution:.*\$#Resolution: 1920x1080#g" "${CONFIG_YML}"
87	elif [ "${IPS3RES}" = "native" ]; then
88	  sed -i "s#Resolution:.*\$#Resolution: $(fbwidth)x$(fbheight)#g" "${CONFIG_YML}"
89	else
90	  sed -i "s#Resolution:.*\$#Resolution: 720x480#g" "${CONFIG_YML}"
91	fi
92	
93	#Internal Resolution Scale
94	if [ "${IRES_SCALE}" = "25" ]; then
95	  sed -i "s#Resolution Scale:.*\$#Resolution Scale: 25#g" "${CONFIG_YML}"
96	elif [ "${IRES_SCALE}" = "75" ]; then
97	  sed -i "s#Resolution Scale:.*\$#Resolution Scale: 75#g" "${CONFIG_YML}"
98	elif [ "${IRES_SCALE}" = "100" ]; then
99	  sed -i "s#Resolution Scale:.*\$#Resolution Scale: 100#g" "${CONFIG_YML}"
100	else
101	  sed -i "s#Resolution Scale:.*\$#Resolution Scale: 50#g" "${CONFIG_YML}"
102	fi
103	
104	#Multithreaded RSX
105	if [ "${MULTIRSX}" = "true" ]; then
106	  sed -i "s#Multithreaded RSX:.*\$#Multithreaded RSX: true#g" "${CONFIG_YML}"
107	else
108	  sed -i "s#Multithreaded RSX:.*\$#Multithreaded RSX: false#g" "${CONFIG_YML}"
109	fi
110	
111	#Shader Precision
112	if [ "$SPREC" = "ultra" ]; then
113	  sed -i "s#Shader Precision:.*\$#Shader Precision: Ultra#g" "${CONFIG_YML}"
114	elif [ "$SPREC" = "high" ]; then
115	  sed -i "s#Shader Precision:.*\$#Shader Precision: High#g" "${CONFIG_YML}"
116	else
117	  sed -i "s#Shader Precision:.*\$#Shader Precision: Low#g" "${CONFIG_YML}"
118	fi
119	
120	#SPU XFloat Accuracy
121	if [ "$SPUXFLOAT" = "accurate" ]; then
122	  sed -i "s#XFloat Accuracy:.*\$#XFloat Accuracy: Accurate#g" "${CONFIG_YML}"
123	elif [ "$SPUXFLOAT" = "relaxed" ]; then
124	  sed -i "s#XFloat Accuracy:.*\$#XFloat Accuracy: Relaxed#g" "${CONFIG_YML}"
125	else
126	  sed -i "s#XFloat Accuracy:.*\$#XFloat Accuracy: Approximate#g" "${CONFIG_YML}"
127	fi
128	
129	#Write Color Buffers
130	if [ "${WCOLORB}" = "true" ]; then
131	  sed -i "s#Write Color Buffers:.*\$#Write Color Buffers: true#g" "${CONFIG_YML}"
132	else
133	  sed -i "s#Write Color Buffers:.*\$#Write Color Buffers: false#g" "${CONFIG_YML}"
134	fi
135	
136	#Vsync
137	if [ "${VSYNC}" = "true" ]; then
138	  sed -i "s#VSync:.*\$#VSync: true#g" "${CONFIG_YML}"
139	else
140	  sed -i "s#VSync:.*\$#VSync: false#g" "${CONFIG_YML}"
141	fi
142	
143	#Zcull Accuracy
144	if [ "$ZCULLA" = "precise" ]; then
145	  sed -i "s#Relaxed ZCULL Sync:.*\$#Relaxed ZCULL Sync: false#g" "${CONFIG_YML}"
146	  sed -i "s#Accurate ZCULL stats:.*\$#Accurate ZCULL stats: true#g" "${CONFIG_YML}"
147	elif [ "$ZCULLA" = "approximate" ]; then
148	  sed -i "s#Relaxed ZCULL Sync:.*\$#Relaxed ZCULL Sync: true#g" "${CONFIG_YML}"
149	  sed -i "s#Accurate ZCULL stats:.*\$#Accurate ZCULL stats: false#g" "${CONFIG_YML}"
150	else
151	  sed -i "s#Relaxed ZCULL Sync:.*\$#Relaxed ZCULL Sync: false#g" "${CONFIG_YML}"
152	  sed -i "s#Accurate ZCULL stats:.*\$#Accurate ZCULL stats: false#g" "${CONFIG_YML}"
153	fi
154	
155	# Performance Overlay
156	if [ "${PERFOVERLAY}" = "true" ]; then
157	  sed -i '/Performance Overlay:/ {n; s/Enabled: .*/Enabled: true/}' "${CONFIG_YML}"
158	else
159	  sed -i '/Performance Overlay:/ {n; s/Enabled: .*/Enabled: false/}' "${CONFIG_YML}"
160	fi
161	
162	#Set the cores to use
163	CORES=$(get_setting "cores" "${PLATFORM}" "${GAME}")
164	if [ "${CORES}" = "little" ]
165	then
166	  EMUPERF="${SLOW_CORES}"
167	elif [ "${CORES}" = "big" ]
168	then
169	  EMUPERF="${FAST_CORES}"
170	else
171	  ### All..
172	  unset EMUPERF
173	fi
174	
175	#Check if its a PSN game
176	GAME_PATH=""
177	PSNID=""
178	if [[ "${1}" == *.psn ]]; then
179	  # Hardcoded now for testing
180	  read -r PSNID < "${1}"
181	  GAME_PATH="/storage/.config/rpcs3/dev_hdd0/game/${PSNID}/USRDIR/EBOOT.BIN"
182	elif [[ "${1}" == *.m3u ]]; then
183	  #check if path is M3U
184	  read -r M3UPATH < "${1}"
185	  echo ${M3UPATH}
186	  GAME_PATH="/roms/ps3/${M3UPATH}"
187	else
188	  GAME_PATH="${1}"
189	fi
190	
191	#Log Settings
192	cat <<EOF >/var/log/rpcs3-sa.log
193	GAME: ${GAME}
194	PLATFORM: ${PLATFORM}
195	ASPECT RATIO: ${ASPECT}
196	GRU BACKEND: ${GRENDERER}
197	INTERNAL RESOLUTION: ${IRES}
198	INTERNAL RESOLUTION SCALE: ${IRES_SCALE}
199	MULTITHREADED RSX: ${MULTIRSX}
200	PERFORMANCE OVERLAY: ${PERFOVERLAY}
201	SHADER PRECISION: ${SPREC}
202	SPU XFLOAT ACCURACY: ${SPUXFLOAT}
203	WRITE COLOR BUFFERS: ${WCOLORB}
204	ZCULL ACCURACY: ${ZCULLA}
205	ASYNC TEXTURE STREAMING: ${ATEXTURE}
206	VSYNC: ${VSYNC}
207	SHOW UI: ${SUI}
208	CONFIG_YML: ${CONFIG_YML}
209	EOF
210	
211	# Run rpcs3
212	if [ "$SUI" = "true" ]; then
213	  export QT_QPA_PLATFORM=wayland
214	  set_kill set "-9 rpcs3-sa"
215	  ${EMUPERF} /usr/bin/rpcs3-sa
216	else
217	  export QT_QPA_PLATFORM=xcb
218	  set_kill set "-9 rpcs3-sa"
219	  ${EMUPERF} /usr/bin/rpcs3-sa --no-gui "$GAME_PATH"
220	fi
```

### `projects/ROCKNIX/packages/emulators/standalone/scummvm-sa/scripts/start_scummvm.sh`

```
1	#!/bin/bash
2	
3	# SPDX-License-Identifier: GPL-2.0-or-later
4	# Copyright (C) 2019-present Shanti Gilbert (https://github.com/shantigilbert)
5	
6	# Source predefined functions and variables
7	. /etc/profile
8	
9	CONFIG_DIR="/storage/.config/scummvm"
10	ROMSPATH="/storage/roms"
11	BIOSPATH="${ROMSPATH}/bios"
12	RATMPCONF="/storage/.config/retroarch/retroarch.cfg"
13	
14	shopt -s extglob
15	if [[ "$1" =~ ^(add|create|libretro)$ ]]
16	then
17	  GAME="$2"
18	else
19	  GAME="$1"
20	fi
21	
22	if [ ! -d "${CONFIG_DIR}/games" ]
23	then
24	  mkdir -p "${CONFIG_DIR}/games"
25	fi
26	
27	create_svm(){
28	  /usr/bin/scummvm --list-targets | tail -n +3 | cut -d " " -f 1 | \
29	  while read line
30	  do
31	    id=($line);
32	    filename=$(sed -n "/^\[$id\]/,/^\[/{s/^description=//p}" ${CONFIG_DIR}/scummvm.ini | \
33	      sed -e 's# (.*)# ('${id}')#g' -e "s#'##g" -e "s#: # - #g" \
34	    )
35	
36	    SVMPATH="$(sed -n "/^\[$id\]/,/^\[/{s/^path=//p}" ${CONFIG_DIR}/scummvm.ini)"
37	    echo '--path="'${SVMPATH}'" '${id} >"${CONFIG_DIR}/games/${filename}.scummvm"
38	  done
39	}
40	
41	if [ ! -d "${CONFIG_DIR}" ]; then
42	 mkdir -p ${CONFIG_DIR}
43	 cp -rf /usr/config/scummvm/* ${CONFIG_DIR}/
44	fi
45	
46	case $1 in
47	  "libretro")
48	    GAME=$(cat "${GAME}" | awk 'BEGIN {FS="\""}; {print $2}')
49	    cd "${GAME}"
50	    /usr/bin/retroarch -L /tmp/cores/scummvm_libretro.so --config ${RATMPCONF} .
51	  ;;
52	
53	  "add")
54	    if [ ! -d "${ROMSPATH}/scummvm" ]; then
55	      mkdir "${ROMSPATH}/scummvm"
56	    fi
57	    /usr/bin/scummvm --add --path="${ROMSPATH}/scummvm" --recursive
58	    mkdir -p ${BIOSPATH}
59	    cp ${CONFIG_DIR}/scummvm.ini ${BIOSPATH}/scummvm.ini
60	  ;;
61	
62	  "create")
63	    create_svm
64	  ;;
65	
66	  *)
67	    set_kill set "-9 scummvm"
68	    GAME=$(cat "${GAME}")
69	    systemctl start fluidsynth
70	    eval /usr/bin/scummvm --fullscreen --joystick=0 --themepath=/usr/config/scummvm/themes "${GAME}"
71	    systemctl stop fluidsynth
72	  ;;
73	esac
```

### `projects/ROCKNIX/packages/emulators/standalone/skyemu-sa/scripts/cheevos_skyemu.sh`

```
1	#! /bin/bash
2	
3	# SPDX-License-Identifier: GPL-2.0-or-later
4	# Copyright (C) 2025-present ROCKNIX (https://github.com/ROCKNIX)
5	
6	. /etc/profile
7	
8	LOG_FILE="/var/log/cheevos.log"
9	
10	# Extract username, password, token, if enabled, and hardcore mode from system.cfg
11	username=$(get_setting "global.retroachievements.username")
12	token=$(get_setting "global.retroachievements.token")
13	enabled=$(get_setting "global.retroachievements")
14	
15	# Check if RetroAchievements are enabled in Emulation Station
16	if [ "${enabled}" = 1 ]; then
17	  enabled="True"
18	else
19	  echo "RetroAchievements are not enabled, please turn them on in Emulation Station." > ${LOG_FILE}
20	  enabled="False"
21	  exit 1
22	fi
23	
24	# Check if api token is present in system.cfg
25	if [ -z "${token}" ]; then
26	    echo "RetroAchievements token is empty, please log in with your RetroAchievements credentials in Emulation Station." > ${LOG_FILE}
27	    exit 1
28	fi
29	
30	cat <<EOF >/storage/.config/SkyEmu/ra_token.txt
31	${username}
32	${token}
33	EOF
```

### `projects/ROCKNIX/packages/emulators/standalone/skyemu-sa/scripts/start_skyemu.sh`

```
1	#!/bin/bash
2	
3	# SPDX-License-Identifier: GPL-2.0-or-later
4	# Copyright (C) 2025-present ROCKNIX (https://github.com/ROCKNIX)
5	
6	. /etc/profile
7	set_kill set "-9 SkyEmu"
8	
9	#load gptokeyb support files
10	control-gen_init.sh
11	source /storage/.config/gptokeyb/control.ini
12	get_controls
13	
14	#Check if SkyEmu dir exists in .config
15	if [ ! -d "/storage/.config/SkyEmu" ]; then
16	  cp -rf "/usr/config/SkyEmu" "/storage/.config/"
17	fi
18	
19	#Check if SkyEmu savestate dir exists in .config
20	if [ ! -d "/storage/roms/savestates/SkyEmu" ]; then
21	  mkdir "/storage/roms/savestates/SkyEmu"
22	fi
23	
24	#Make sure SkyEmu gptk config exists
25	if [ ! -f "/storage/.config/SkyEmu/SkyEmu.gptk" ]; then
26	  cp -r "/usr/config/SkyEmu/SkyEmu.gptk" "/storage/.config/SkyEmu/SkyEmu.gptk"
27	fi
28	
29	# Link  .config/dolphin-emu to .local
30	rm -rf /storage/.local/share/Sky/SkyEmu
31	ln -sf /storage/.config/SkyEmu /storage/.local/share/Sky/SkyEmu
32	
33	# Retroachievements
34	/usr/bin/cheevos_skyemu.sh
35	
36	#Emulation Station Features
37	GAME=$(echo "${1}"| sed "s#^/.*/##")
38	PLATFORM=$(echo "${2}"| sed "s#^/.*/##")
39	
40	#Set the cores to use
41	CORES=$(get_setting "cores" "${PLATFORM}" "${GAME}")
42	if [ "${CORES}" = "little" ]
43	then
44	  EMUPERF="${SLOW_CORES}"
45	elif [ "${CORES}" = "big" ]
46	then
47	  EMUPERF="${FAST_CORES}"
48	else
49	  ### All..
50	  unset EMUPERF
51	fi
52	
53	# Run SkyEmu
54	$GPTOKEYB "SkyEmu" -c "/storage/.config/SkyEmu/SkyEmu.gptk" &
55	${EMUPERF} /usr/bin/SkyEmu "${1}"
56	kill -9 "$(pidof gptokeyb)"
```

### `projects/ROCKNIX/packages/emulators/standalone/steam/scripts/start_steam.sh`

```
1	#!/bin/bash
2	
3	# SPDX-License-Identifier: GPL-2.0-or-later
4	# Copyright (C) 2026-present ROCKNIX (https://github.com/ROCKNIX)
5	
6	steam_ensure_fex_config_template() {
7	  if [ ! -d "/storage/.config/fex-emu" ]; then
8	    cp -r "/usr/config/fex-emu" "/storage/.config/"
9	  fi
10	}
11	
12	steam_prepare_storage_and_vdf() {
13	  mkdir -p /storage/roms/steam/steamapps
14	  local vdf="/storage/.local/share/Steam/steamapps/libraryfolders.vdf"
15	  if [ -f "$vdf" ]; then
16	    grep -q '"/storage/roms/steam"' "$vdf" || sed -i '$ s/}/\t"1" {"path" "\/storage\/roms\/steam"}\n}/' "$vdf"
17	  fi
18	}
19	
20	steam_load_es_thunk_settings() {
21	  GAME=$(echo "${1}" | sed "s#^/.*/##")
22	  PLATFORM=$(echo "${2}" | sed "s#^/.*/##")
23	  LSFG_ENABLE=$(get_setting lsfg_enable "${PLATFORM}" "${GAME}")
24	  LSFG_ENABLE=${LSFG_ENABLE:-0}
25	  LSFG_MULTIPLIER=$(get_setting lsfg_multiplier "${PLATFORM}" "${GAME}")
26	  LSFG_MULTIPLIER=${LSFG_MULTIPLIER:-2}
27	  LSFG_FLOW_SCALE=$(get_setting lsfg_flow_scale "${PLATFORM}" "${GAME}")
28	  LSFG_FLOW_SCALE=${LSFG_FLOW_SCALE:-0.30}
29	  LSFG_PERFORMANCE_MODE=$(get_setting lsfg_performance_mode "${PLATFORM}" "${GAME}")
30	  LSFG_PERFORMANCE_MODE=${LSFG_PERFORMANCE_MODE:-1}
31	  FPS_LIMIT=$(get_setting fps_limit "${PLATFORM}" "${GAME}")
32	  FPS_LIMIT=${FPS_LIMIT:-0}
33	}
34	
35	steam_apply_fps_limit() {
36	  if [ "${FPS_LIMIT}" != "0" ]; then
37	    export DXVK_CONFIG="dxgi.maxFrameRate = ${FPS_LIMIT}"
38	    export VKD3D_FRAME_RATE=${FPS_LIMIT}
39	  fi
40	}
41	
42	steam_apply_lsfg_settings() {
43	  if [ "${LSFG_ENABLE}" = "1" ]; then
44	    unset DISABLE_LSFGVK
45	    export LSFGVK_ENV=1
46	    export LSFGVK_DLL_PATH="/storage/.local/share/Steam/steamapps/common/Lossless Scaling/Lossless.dll"
47	    export LSFGVK_MULTIPLIER="${LSFG_MULTIPLIER}"
48	    export LSFGVK_FLOW_SCALE="${LSFG_FLOW_SCALE}"
49	    export LSFGVK_PERFORMANCE_MODE="${LSFG_PERFORMANCE_MODE}"
50	    export ENABLE_GAMESCOPE_WSI=0
51	  else
52	    export DISABLE_LSFGVK=1
53	  fi
54	}
55	
56	steam_set_cpu_affinity() {
57	  local cores
58	  cores=$(get_setting "cores" "${PLATFORM}" "${GAME}")
59	  if [ "${cores}" = "little" ]; then
60	    EMUPERF="${SLOW_CORES}"
61	  elif [ "${cores}" = "big" ]; then
62	    EMUPERF="${FAST_CORES}"
63	  else
64	    unset EMUPERF
65	  fi
66	}
67	
68	steam_debug_print() {
69	  echo "GAME set to: ${GAME}"
70	  echo "PLATFORM set to: ${PLATFORM}"
71	  echo "CPU CORES set to: ${EMUPERF}"
72	  echo "LSFG ENABLE set to: ${LSFG_ENABLE}"
73	  echo "LSFG MULTIPLIER set to: ${LSFG_MULTIPLIER}"
74	  echo "LSFG FLOW SCALE set to: ${LSFG_FLOW_SCALE}"
75	  echo "LSFG PERFORMANCE MODE set to: ${LSFG_PERFORMANCE_MODE}"
76	  echo "LSFG FPS LIMIT set to: ${FPS_LIMIT}"
77	  echo "VSYNC set to: ${VSYNC}"
78	}
79	
80	steam_read_sway_geometry() {
81	  eval "$(swaymsg -t get_outputs | jq -r '
82	    .[] | select(.focused == true) |
83	    "W=\(.current_mode.width) H=\(.current_mode.height) TRANSFORM=\(.transform) REFRESH=\(.current_mode.refresh // 60000)"
84	  ')"
85	  # Round to nearest (119990 mHz -> 120) to match the mode's integer vrefresh,
86	  # which gamescope's -r must hit exactly or it falls back to the preferred mode.
87	  REFRESH_HZ=$(((REFRESH + 500) / 1000))
88	}
89	
90	steam_setup_environment() {
91	  TZ=$(timedatectl status | grep 'Time zone' | awk '{print $3}')
92	  [ -n "${TZ}" ] && export TZ
93	}
94	
95	steam_touch_calibration_begin() {
96	  local orientation="$1"
97	  local model=""
98	  local name_path
99	
100	  STEAM_TOUCH_EVENT=""
101	  STEAM_TOUCH_RULE=""
102	
103	  [ "${orientation}" = "upsidedown" ] || return 0
104	  if [ -r /proc/device-tree/model ]; then
105	    model=$(tr -d '\000' </proc/device-tree/model)
106	  fi
107	  [ "${model}" = "AYANEO Pocket S Mini" ] || return 0
108	
109	  for name_path in /sys/class/input/event*/device/name; do
110	    if [ "$(cat "${name_path}" 2>/dev/null)" = "Hynitron CST66xx Touchscreen" ]; then
111	      STEAM_TOUCH_EVENT="${name_path%/device/name}"
112	      break
113	    fi
114	  done
115	  [ -n "${STEAM_TOUCH_EVENT}" ] || return 0
116	
117	  STEAM_TOUCH_RULE="/run/udev/rules.d/99-steam-touch-calibration.rules"
118	  mkdir -p "${STEAM_TOUCH_RULE%/*}"
119	  printf '%s\n' \
120	    'ACTION!="remove", SUBSYSTEM=="input", KERNEL=="event*", ATTRS{name}=="Hynitron CST66xx Touchscreen", ENV{LIBINPUT_CALIBRATION_MATRIX}="-1 0 1 0 -1 1"' \
121	    >"${STEAM_TOUCH_RULE}"
122	  udevadm control --reload
123	  udevadm trigger --action=change "${STEAM_TOUCH_EVENT}"
124	  udevadm settle --timeout=3 >/dev/null 2>&1 || true
125	}
126	
127	steam_touch_calibration_end() {
128	  [ -n "${STEAM_TOUCH_RULE:-}" ] || return 0
129	
130	  rm -f "${STEAM_TOUCH_RULE}"
131	  udevadm control --reload >/dev/null 2>&1 || true
132	  if [ -n "${STEAM_TOUCH_EVENT:-}" ]; then
133	    udevadm trigger --action=change "${STEAM_TOUCH_EVENT}" \
134	      >/dev/null 2>&1 || true
135	  fi
136	  STEAM_TOUCH_RULE=""
137	  STEAM_TOUCH_EVENT=""
138	}
139	
140	steam_scope_reexec_if_needed() {
141	  if [ -z "$_STEAM_SCOPE" ]; then
142	    systemctl stop steam-bigpicture.scope 2>/dev/null || true
143	    exec systemd-run \
144	      --scope \
145	      --slice=system.slice \
146	      --unit=steam-bigpicture \
147	      --collect \
148	      -E _STEAM_SCOPE=1 \
149	      -E HOME="$HOME" \
150	      -E USER="$USER" \
151	      -E TZ="$TZ" \
152	      -- "${STEAM_MAIN_SCRIPT}" "$@"
153	  fi
154	}
155	
156	steam_dual_screen_begin() {
157	  if [ "${DEVICE_HAS_DUAL_SCREEN}" = "true" ]; then
158	    swaymsg 'seat seat1 fallback true'
159	    PREFER_OUTPUT="--prefer-output $SDL_VIDEO_DISPLAY_PRIORITY"
160	  fi
161	}
162	
163	steam_dual_screen_end() {
164	  if [ "${DEVICE_HAS_DUAL_SCREEN}" = "true" ]; then
165	    swaymsg 'seat seat1 fallback false'
166	  fi
167	}
168	
169	steam_arm64_binfmt_and_proton_prep() {
170	  echo 0 >/proc/sys/fs/binfmt_misc/x86
171	  echo 0 > /proc/sys/fs/binfmt_misc/box32
172	  echo 0 > /proc/sys/fs/binfmt_misc/box64
173	  rm "/storage/.local/share/Steam/compatibilitytools.d/compatibilitytool.vdf"
174	}
175	
176	steam_launch_bigpicture() {
177	  local game_uri=""
178	  local force_orientation="normal"
179	  local gamescope_mode_file="/storage/.config/gamescope/modes.cfg"
180	  local steam_exit_code=0
181	  local gamescope_exit_code=0
182	  local steam_exit_code_file=""
183	  if [ "${TRANSFORM}" = "90" ]; then
184	    force_orientation="right"
185	  elif [ "${TRANSFORM}" = "180" ]; then
186	    force_orientation="upsidedown"
187	  elif [ "${TRANSFORM}" = "270" ]; then
188	    force_orientation="left"
189	  fi
190	
191	  # The DPU inline rotator caps the pre-rotation source at 1088 lines, but the plane advertises
192	  # ROTATE_90 as a static capability it cannot qualify per mode. On a rotated panel wider than
193	  # that (1440x2560) gamescope keeps scanout rotation, every atomic commit is rejected and the
194	  # panel stays black. Render the session at 1080p instead and let the same plane upscale it back
195	  # to the mode. The flag only exists in our patched gamescope (patches/0008), and gamescope
196	  # exits on an unknown argument, so it must be dropped here if that patch ever goes away.
197	  local rotate_clamp=""
198	  if [[ "${TRANSFORM}" = "90" || "${TRANSFORM}" = "270" ]] && [ "${W}" -gt 1088 ]; then
199	    rotate_clamp="--rotated-output-max-height 1080"
200	  fi
201	
202	  if [[ "$1" == *.desktop && -f "$1" && "$(basename "$1")" != "Steam.desktop" ]]; then
203	    local exec_line
204	    exec_line=$(grep -m1 '^Exec=' "$1" | cut -d'=' -f2-)
205	    game_uri="${exec_line#steam } -silent"
206	  fi
207	
208	  # SM4450 Steam UI requires wayland gamescope backend
209	  local gamescope_backend="drm"
210	  if [[ "${HW_DEVICE}" == "SM4450" ]]; then
211	    gamescope_backend="wayland"
212	  fi
213	
214	  mkdir -p "$(dirname "$gamescope_mode_file")"
215	  touch "$gamescope_mode_file"
216	  unset MESA_LOADER_DRIVER_OVERRIDE
217	
218	  # drm gamescope backend needs wayland socket unset and compositer stopped
219	  if [ "${gamescope_backend}" = "drm" ]; then
220	    unset WAYLAND_DISPLAY
221	    systemctl stop sway
222	  fi
223	
224	  if [ "${STEAM_FLAVOR}" = "arm64" ]; then
225	    export STEAM_COMPAT_GRAPHICS_PROVIDER=/storage/.local/share/fex-emu/RootFS/ArchLinux/graphics_provider.json
226	    steam_exit_code_file=$(mktemp /tmp/steam-exit-code.XXXXXX)
227	    steam_touch_calibration_begin "${force_orientation}"
228	    trap steam_touch_calibration_end EXIT
229	    while true; do
230	      rm -f "${steam_exit_code_file}"
231	      GAMESCOPE_MODE_SAVE_FILE="${gamescope_mode_file}" GAMESCOPE_FAKE_OUTPUT_MM=508x286 \
232	      LD_LIBRARY_PATH=/storage/.local/share/Steam/lib/aarch64-linux-gnu/ ${EMUPERF} \
233	      gamescope $PREFER_OUTPUT -W "$W" -H "$H" -r "$REFRESH_HZ" --xwayland-count 2 --mangoapp --backend "${gamescope_backend}" --force-orientation "${force_orientation}" ${rotate_clamp} -e -- \
234	      /bin/bash -c '
235	        exit_file="$1"
236	        shift
237	        "$@"
238	        printf "%s\n" "$?" >"${exit_file}"
239	      ' _ "${steam_exit_code_file}" \
240	      /storage/.local/share/Steam/steamrtarm64/steam -deckard -steamos3 -gamepadui -noshaders ${game_uri:+"$game_uri"}
241	      gamescope_exit_code=$?
242	      if [ -f "${steam_exit_code_file}" ]; then
243	        steam_exit_code=$(cat "${steam_exit_code_file}")
244	      else
245	        steam_exit_code=${gamescope_exit_code}
246	      fi
247	      [ "${steam_exit_code}" = "42" ] || break
248	    done
249	    rm -f "${steam_exit_code_file}"
250	    steam_touch_calibration_end
251	    trap - EXIT
252	    systemctl start essway
253	    exit 0
254	  else
255	    FEX /usr/bin/steam -exitsteam
256	    steam_touch_calibration_begin "${force_orientation}"
257	    trap steam_touch_calibration_end EXIT
258	    GAMESCOPE_MODE_SAVE_FILE="${gamescope_mode_file}" GAMESCOPE_FAKE_OUTPUT_MM=508x286 ${EMUPERF} \
259	      gamescope $PREFER_OUTPUT -W "$W" -H "$H" -r "$REFRESH_HZ" --xwayland-count 2 --backend "${gamescope_backend}" --force-orientation "${force_orientation}" ${rotate_clamp} -- \
260	      FEX /usr/bin/steam -nobigpicture -noverifyfiles -nobootstrapupdate -skipinitialbootstrap -norepairfiles -noshaders ${game_uri:+"$game_uri"}
261	    steam_touch_calibration_end
262	    trap - EXIT
263	    systemctl start essway
264	    exit 0
265	  fi
266	}
267	
268	# Entry point from EmulationStation (not used when this file is sourced).
269	if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
270	  source /etc/profile
271	  GAME=$(echo "${1}" | sed "s#^/.*/##")
272	  PLATFORM=$(echo "${2}" | sed "s#^/.*/##")
273	  STEAM_VERSION=$(get_setting steam_version "${PLATFORM}" "${GAME}")
274	  STEAM_VERSION=${STEAM_VERSION:-"arm64"}
275	  echo "STEAM_VERSION set to: ${STEAM_VERSION}"
276	  if [ "${STEAM_VERSION}" = "arm64" ]; then
277	    exec /usr/bin/start_steam_arm64.sh "$@"
278	  else
279	    exec /usr/bin/start_steam_x86.sh "$@"
280	  fi
281	fi
```

### `projects/ROCKNIX/packages/emulators/standalone/steam/scripts/start_steam_arm64.sh`

```
1	#!/bin/bash
2	
3	# SPDX-License-Identifier: GPL-2.0-or-later
4	# Copyright (C) 2026-present ROCKNIX (https://github.com/ROCKNIX)
5	
6	STEAM_MAIN_SCRIPT=${0}
7	STEAM_FLAVOR=arm64
8	
9	source /etc/profile
10	set_kill set "gamescope steam FEX"
11	
12	# shellcheck source=start_steam.sh
13	. /usr/bin/start_steam.sh
14	
15	steam_ensure_fex_config_template
16	steam_prepare_storage_and_vdf
17	steam_load_es_thunk_settings "$@"
18	steam_apply_lsfg_settings
19	steam_apply_fps_limit
20	steam_set_cpu_affinity
21	steam_debug_print
22	
23	steam_arm64_binfmt_and_proton_prep
24	steam_read_sway_geometry
25	steam_setup_environment
26	steam_scope_reexec_if_needed "$@"
27	steam_dual_screen_begin
28	steam_launch_bigpicture "$@"
29	steam_dual_screen_end
30	systemctl restart systemd-binfmt
```

### `projects/ROCKNIX/packages/emulators/standalone/steam/scripts/start_steam_x86.sh`

```
1	#!/bin/bash
2	
3	# SPDX-License-Identifier: GPL-2.0-or-later
4	# Copyright (C) 2026-present ROCKNIX (https://github.com/ROCKNIX)
5	
6	STEAM_MAIN_SCRIPT=${0}
7	STEAM_FLAVOR=x86
8	
9	source /etc/profile
10	set_kill set "-9 FEX"
11	
12	# shellcheck source=start_steam.sh
13	. /usr/bin/start_steam.sh
14	
15	steam_ensure_fex_config_template
16	steam_prepare_storage_and_vdf
17	steam_load_es_thunk_settings "$@"
18	steam_apply_lsfg_settings
19	steam_apply_fps_limit
20	steam_set_cpu_affinity
21	steam_debug_print
22	
23	steam_read_sway_geometry
24	steam_setup_environment
25	steam_scope_reexec_if_needed "$@"
26	systemctl stop systemd-binfmt
27	steam_dual_screen_begin
28	steam_launch_bigpicture "$@"
29	steam_dual_screen_end
30	systemctl start systemd-binfmt
```

### `projects/ROCKNIX/packages/emulators/standalone/supermodel-sa/scripts/start_supermodel.sh`

```
1	#!/bin/bash
2	
3	# SPDX-License-Identifier: GPL-2.0-or-later
4	# Copyright (C) 2024-present ROCKNIX (https://github.com/ROCKNIX)
5	
6	# Source predefined functions and variables
7	. /etc/profile
8	set_kill set "-9 supermodel"
9	
10	CONFIG_DIR="/storage/.config/supermodel"
11	SOURCE_DIR="/usr/config/supermodel"
12	
13	#Check if supermodel exists in .config
14	if [ ! -d "${CONFIG_DIR}" ]; then
15	    mkdir -p "${CONFIG_DIR}"
16	        cp -r "${SOURCE_DIR}" "/storage/.config/"
17	fi
18	
19	if [ ! -d "${CONFIG_DIR}/NVRAM" ]; then
20	    mkdir -p "${CONFIG_DIR}/NVRAM"
21	fi
22	
23	if [ ! -d "${CONFIG_DIR}/Saves" ]; then
24	    mkdir -p "${CONFIG_DIR}/Saves"
25	fi
26	
27	if [ ! -d "${CONFIG_DIR}/LocalConfig" ]; then
28	    mkdir -p "${CONFIG_DIR}/LocalConfig"
29	fi
30	
31	#Emulation Station Features
32	GAME=$(echo "${1}"| sed "s#^/.*/##")
33	PLATFORM=$(echo "${2}"| sed "s#^/.*/##")
34	VSYNC=$(get_setting vsync "${PLATFORM}" "${GAME}")
35	RESOLUTION=$(get_setting resolution "${PLATFORM}" "${GAME}")
36	ENGINE=$(get_setting rendering_engine "${PLATFORM}" "${GAME}")
37	
38	#Set the cores to use
39	CORES=$(get_setting "cores" "${PLATFORM}" "${GAME}")
40	if [ "${CORES}" = "little" ]
41	then
42	  EMUPERF="${SLOW_CORES}"
43	elif [ "${CORES}" = "big" ]
44	then
45	  EMUPERF="${FAST_CORES}"
46	else
47	  ### All..
48	  unset EMUPERF
49	fi
50	
51	OPTIONS=" -fullscreen"
52	
53	#VSYNC
54	if [ "$VSYNC" = "true" ]
55	then
56	  OPTIONS+=" -vsync"
57	elif [ "$VSYNC" = "false" ]
58	then
59	  OPTIONS+=" -no-vsync"
60	fi
61	
62	#ENGINE
63	if [ "$ENGINE" = "1" ]
64	then
65	  OPTIONS+=" -new3d"
66	elif [ "$ENGINE" = "0" ]
67	then
68	  OPTIONS+=" -legacy3d"
69	fi
70	
71	#RESOLUTION
72	if [ "$RESOLUTION" = "0" ]
73	then
74	  OPTIONS+=" -res=1920,1080"
75	elif [ "$RESOLUTION" = "1" ]
76	then
77	  OPTIONS+=" -res=496,384"
78	elif [ "$RESOLUTION" = "2" ]
79	then
80	  OPTIONS+=" -res=992,768"
81	fi
82	
83	sway_fullscreen supermodel &
84	
85	cd ${CONFIG_DIR}
86	echo "Command: supermodel ${1} ${OPTIONS}" >/var/log/exec.log 2>&1
87	${EMUPERF} supermodel "${1}" "${OPTIONS}" >>/var/log/exec.log 2>&1 ||:
```

### `projects/ROCKNIX/packages/emulators/standalone/touchhle-sa/scripts/start_touchhle.sh`

```
1	#!/bin/bash
2	
3	# SPDX-License-Identifier: GPL-2.0-or-later
4	# Copyright (C) 2026-present ROCKNIX (https://github.com/ROCKNIX)
5	
6	. /etc/profile
7	set_kill set "-9 touchHLE"
8	
9	# Conf files vars
10	SOURCE_DIR="/usr/config/touchHLE"
11	CONF_DIR="/storage/.config/touchHLE"
12	TOUCHHLE_CONF="touchHLE_options.txt"
13	
14	# Check if touchHLE exists in /storage/.config
15	if [ ! -d "${CONF_DIR}" ]; then
16	  cp -r "${SOURCE_DIR}" "/storage/.config/"
17	fi
18	
19	# Check if touchHLE_options.txt exists in .config/touchHLE
20	if [ ! -f "${CONF_DIR}/${TOUCHHLE_CONF}" ]; then
21	  cp -r "${SOURCE_DIR}/${TOUCHHLE_CONF}" "${CONF_DIR}"
22	fi
23	
24	# Check if touchHLE_wallpaper.* exists in .config/touchHLE
25	if ! compgen -G "${CONF_DIR}/touchHLE_wallpaper.*" > /dev/null; then
26	printf \
27	'\x89PNG\r\n\x1a\n'\
28	'\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x02\x00\x00\x00\x90wS\xde'\
29	'\x00\x00\x00\x0cIDAT\x08\xd7c\x60\x60\x60\x00\x00\x00\x04\x00\x01\xf6\x17\x38\x55'\
30	'\x00\x00\x00\x00IEND\xaeB`\x82' \
31	> "${CONF_DIR}/touchHLE_wallpaper.png"
32	fi
33	
34	# Link roms/ios to touchHLE_apps
35	ln -snf "/storage/roms/ios" "${CONF_DIR}/touchHLE_apps"
36	
37	#Emulation Station Features
38	GAME=$(echo "${1}"| sed "s#^/.*/##")
39	PLATFORM=$(echo "${2}"| sed "s#^/.*/##")
40	DEVICE=$(get_setting device_type "${PLATFORM}" "${GAME}")
41	UPSCALE=$(get_setting upscale "${PLATFORM}" "${GAME}")
42	
43	# Set device type
44	if [ "${DEVICE}" != "ipad" ]; then
45	  DEVICE="iphone"
46	fi
47	
48	# Set upscaling
49	if [[ "${UPSCALE}" =~ ^[1-4]$ ]]; then
50	  UPSCALE="${UPSCALE}"
51	else
52	  UPSCALE=1
53	fi
54	
55	#Set the cores to use
56	CORES=$(get_setting "cores" "${PLATFORM}" "${GAME}")
57	if [ "${CORES}" = "little" ]
58	then
59	  EMUPERF="${SLOW_CORES}"
60	elif [ "${CORES}" = "big" ]
61	then
62	  EMUPERF="${FAST_CORES}"
63	else
64	  ### All..
65	  unset EMUPERF
66	fi
67	
68	# Debugging info:
69	  echo "GAME set to: ${GAME}"
70	  echo "PLATFORM set to: ${PLATFORM}"
71	  echo "CONF DIR: ${CONF_DIR}/${GOPHER64_JSON}"
72	  echo "CPU CORES set to: ${EMUPERF}"
73	  echo "DEVICE TYPE set to: ${DEVICE}"
74	  echo "Launching /usr/bin/touchHLE --fullscreen=${DEVICE} ${1}"
75	
76	# Start touchHLE
77	${EMUPERF} /usr/bin/touchHLE --fullscreen --scale-hack=${UPSCALE} --device-family=${DEVICE} "${1}"
```

### `projects/ROCKNIX/packages/emulators/standalone/vice-sa/package.mk`

```
1	# SPDX-License-Identifier: GPL-2.0
2	# Copyright (C) 2024-present ROCKNIX (https://github.com/ROCKNIX)
3	
4	PKG_NAME="vice-sa"
5	PKG_VERSION="3.8"
6	PKG_SHA256="1d7dc4d0f2bbcc2a871bb954ff4a5df63048dea9c16f5f1e9bc8260fa41a1004"
7	PKG_LICENSE="GPL-2.0-or-later"
8	PKG_SITE="https://sourceforge.net/projects/vice-emu"
9	PKG_URL="${PKG_SITE}/files/releases/vice-${PKG_VERSION}.tar.gz"
10	PKG_DEPENDS_TARGET="toolchain xa:host SDL2 SDL2_image ncurses readline busybox:host"
11	PKG_LONGDESC="Commodore 8-bit Emulator"
12	
13	PKG_CONFIGURE_OPTS_TARGET+=" --disable-pdf-docs --enable-gtk3ui=no --without-alsa --with-pulse --enable-sdl2ui"
14	
15	if [ ! "${OPENGL}" = "no" ]; then
16	  PKG_DEPENDS_TARGET+=" ${OPENGL} glu libglvnd"
17	fi
18	
19	if [ "${OPENGLES_SUPPORT}" = yes ]; then
20	  PKG_DEPENDS_TARGET+=" ${OPENGLES}"
21	fi
22	
23	pre_configure_target() {
24	  export LDFLAGS="${LDFLAGS} -lreadline -lncursesw -ltinfow"
25	  export CFLAGS="${CFLAGS} -fcommon"
26	}
27	
28	post_makeinstall_target() {
29	  mkdir -p ${INSTALL}/usr/config/vice
30	    cp -a ${PKG_DIR}/config/* ${INSTALL}/usr/config/vice
31	
32	  for sc in x128 x64sc xplus4 xvic; do
33	    cp -a ${PKG_DIR}/scripts/start_vice.sh ${INSTALL}/usr/bin/start_${sc}.sh
34	    sed -i "s~@EMU@~${sc}~g" ${INSTALL}/usr/bin/start_${sc}.sh
35	  done
36	}
```

### `projects/ROCKNIX/packages/emulators/standalone/vice-sa/scripts/start_vice.sh`

```
1	#!/bin/sh
2	# SPDX-License-Identifier: GPL-2.0
3	# Copyright (C) 2023 JELOS (https://github.com/JustEnoughLinuxOS)
4	
5	. /etc/profile
6	
7	set_kill set "-9 @EMU@"
8	
9	CONFIG_PATH="/storage/.config/vice"
10	SOURCE_PATH="/usr/config/vice"
11	
12	EMU="@EMU@"
13	
14	### Get the game we want to start.
15	GAME=${1//[\\]/}
16	
17	if [ ! -d "/storage/.config/vice" ]
18	then
19	  mkdir -p /storage/.config/vice
20	fi
21	
22	case ${EMU} in
23	  x128)
24	    EMU="C128"
25	  ;;
26	  x64sc)
27	    EMU="C64SC"
28	  ;;
29	  xplus4)
30	    EMU="PLUS4"
31	  ;;
32	  xvic)
33	    EMU="VIC20"
34	  ;;
35	esac
36	
37	if [ ! -e "${CONFIG_PATH}/sdl-hotkeys-${EMU}.vhk" ]
38	then
39	  cat <<EOF >${CONFIG_PATH}/sdl-hotkeys-${EMU}.vhk
40	!CLEAR
41	EOF
42	fi
43	
44	if [ ! -e "${CONFIG_PATH}/sdl-joymap-${EMU}.vjm" ]
45	then
46	  cat <<EOF >${CONFIG_PATH}/sdl-joymap-${EMU}.vjm
47	!CLEAR
48	
49	0 0 0 0
50	0 0 1 0
51	0 0 2 0
52	0 0 3 0
53	0 0 4 0
54	0 0 5 0
55	0 0 6 0
56	0 0 7 0
57	
58	0 1 0 1 0 16
59	0 1 1 1 0 32
60	0 1 2 1 0 64
61	0 1 3 0
62	0 1 4 0
63	0 1 ${DEVICE_BTN_SELECT} 5 Virtual keyboard
64	0 1 ${DEVICE_BTN_START} 4
65	EOF
66	
67	  if [[ ! "${DEVICE_BTN_DPAD_UP}" =~ [a-z] ]]
68	  then
69	    cat <<EOF >>${CONFIG_PATH}/sdl-joymap-${EMU}.vjm
70	0 1 ${DEVICE_BTN_DPAD_UP} 1 0 1
71	0 1 ${DEVICE_BTN_DPAD_DOWN} 1 0 2
72	0 1 ${DEVICE_BTN_DPAD_LEFT} 1 0 4
73	0 1 ${DEVICE_BTN_DPAD_RIGHT} 1 0 8
74	EOF
75	  else
76	    cat <<EOF >>${CONFIG_PATH}/sdl-joymap-${EMU}.vjm
77	0 2 0 1 0 1
78	0 2 1 1 0 2
79	0 2 2 1 0 4
80	0 2 3 1 0 8
81	EOF
82	  fi
83	fi
84	
85	@EMU@ -joymenucontrol "${GAME}"
```

### `projects/ROCKNIX/packages/emulators/standalone/vita3k-sa/scripts/start_vita3k.sh`

```
1	#!/bin/bash
2	
3	# SPDX-License-Identifier: GPL-2.0-or-later
4	# Copyright (C) 2026 ROCKNIX (https://github.com/ROCKNIX)
5	
6	GAME="${1}"
7	CONFIG_FILE="/storage/.config/Vita3K/config.yml"
8	
9	. /etc/profile
10	set_kill set "-9 vita3k-sa"
11	
12	# Bail on error, especially since .pkg installation calls can fail if the ZRIF is wrong,
13	# and that could cause data loss/confusion with the second call on Vita3K...
14	set -e
15	
16	# Check if config vita3k folder exists
17	if [ ! -d "/storage/.config/Vita3K" ]; then
18	    mkdir -p "/storage/.config/Vita3K"
19	fi
20	
21	# Apply default config if it isn't there yet.
22	if [ ! -f "${CONFIG_FILE}" ]; then
23	    cp "/usr/config/vita3k/config.yml" "${CONFIG_FILE}"
24	fi
25	
26	# Copy vita-gamelist for game scanning if not already there.
27	if [ ! -f "/storage/.config/Vita3K/vita-gamelist.txt" ]; then
28	    cp "/usr/config/vita3k/vita-gamelist.txt" "/storage/.config/Vita3K/"
29	fi
30	
31	# EmulationStation options
32	ROMNAME=$(echo "${1}" | sed "s#^/.*/##")
33	PLATFORM="${2}"
34	RENDERER=$(get_setting graphics_backend "${PLATFORM}" "${ROMNAME}")
35	PSTVMODE=$(get_setting pstv_mode "${PLATFORM}" "${ROMNAME}")
36	IRES=$(get_setting internal_resolution "${PLATFORM}" "${ROMNAME}")
37	FILTER=$(get_setting bilinear_filtering "${PLATFORM}" "${ROMNAME}")
38	ACCURACY=$(get_setting high_accuracy "${PLATFORM}" "${ROMNAME}")
39	MEMMAPPING=$(get_setting memory_mapping "${PLATFORM}" "${ROMNAME}")
40	VSYNC=$(get_setting vsync "${PLATFORM}" "${ROMNAME}")
41	ANISO=$(get_setting anisotropic_filtering "${PLATFORM}" "${ROMNAME}")
42	FPSHACK=$(get_setting fps_hack "${PLATFORM}" "${ROMNAME}")
43	NGSENABLE=$(get_setting ngs_audio "${PLATFORM}" "${ROMNAME}")
44	DISABLEMOTION=$(get_setting disable_gyro "${PLATFORM}" "${ROMNAME}")
45	DISABLESURFACESYNC=$(get_setting disable_surface_sync "${PLATFORM}" "${ROMNAME}")
46	SYSBUTTON=$(get_setting confirm_button "${PLATFORM}" "${ROMNAME}")
47	FILELOADINGDELAY=$(get_setting file_loading_delay "${PLATFORM}" "${ROMNAME}")
48	SPIRVSHADER=$(get_setting spirv_shader "${PLATFORM}" "${ROMNAME}")
49	HASHLESSTEXCACHE=$(get_setting hashless_texture_cache "${PLATFORM}" "${ROMNAME}")
50	HTTPENABLE=$(get_setting network_features "${PLATFORM}" "${ROMNAME}")
51	
52	# Graphics Backend
53	if [ "${RENDERER}" = "opengl" ]; then
54	  sed -i "/^backend-renderer:/c\backend-renderer: OpenGL" /storage/.config/Vita3K/config.yml
55	else
56	  sed -i "/^backend-renderer:/c\backend-renderer: Vulkan" /storage/.config/Vita3K/config.yml
57	fi
58	
59	# Internal Resolution
60	if [ "$IRES" = "0.5" ]; then
61	  sed -i "/^resolution-multiplier:/c\resolution-multiplier: 0.5" /storage/.config/Vita3K/config.yml
62	elif [ "$IRES" = "0.75" ]; then
63	  sed -i "/^resolution-multiplier:/c\resolution-multiplier: 0.75" /storage/.config/Vita3K/config.yml
64	elif [ "$IRES" = "1.25" ]; then
65	  sed -i "/^resolution-multiplier:/c\resolution-multiplier: 1.25" /storage/.config/Vita3K/config.yml
66	elif [ "$IRES" = "1.5" ]; then
67	  sed -i "/^resolution-multiplier:/c\resolution-multiplier: 1.5" /storage/.config/Vita3K/config.yml
68	elif [ "$IRES" = "1.75" ]; then
69	  sed -i "/^resolution-multiplier:/c\resolution-multiplier: 1.75" /storage/.config/Vita3K/config.yml
70	elif [ "$IRES" = "2" ]; then
71	  sed -i "/^resolution-multiplier:/c\resolution-multiplier: 2" /storage/.config/Vita3K/config.yml
72	else
73	  sed -i "/^resolution-multiplier:/c\resolution-multiplier: 1" /storage/.config/Vita3K/config.yml
74	fi
75	
76	# PSTV Mode
77	if [ "${PSTVMODE}" = "true" ]; then
78	  sed -i "/^pstv-mode:/c\pstv-mode: true" /storage/.config/Vita3K/config.yml
79	else
80	  sed -i "/^pstv-mode:/c\pstv-mode: false" /storage/.config/Vita3K/config.yml
81	fi
82	
83	# Bilinear Filtering
84	if [ "${FILTER}" = "0" ]; then
85	  sed -i '/^screen-filter:/c\screen-filter: Nearest' /storage/.config/Vita3K/config.yml
86	elif [ "${FILTER}" = "2" ]; then
87	  sed -i '/^screen-filter:/c\screen-filter: Bicubic' /storage/.config/Vita3K/config.yml
88	elif [ "${FILTER}" = "3" ]; then
89	  sed -i '/^screen-filter:/c\screen-filter: FXAA' /storage/.config/Vita3K/config.yml
90	elif [ "${FILTER}" = "4" ]; then
91	  sed -i '/^screen-filter:/c\screen-filter: FSR' /storage/.config/Vita3K/config.yml
92	else
93	  sed -i '/^screen-filter:/c\screen-filter: Bilinear' /storage/.config/Vita3K/config.yml
94	fi
95	
96	# Renderer Accuracy
97	if [ "${ACCURACY}" = "true" ]; then
98	  sed -i "/^high-accuracy:/c\high-accuracy: true" /storage/.config/Vita3K/config.yml
99	else
100	  sed -i "/^high-accuracy:/c\high-accuracy: false" /storage/.config/Vita3K/config.yml
101	fi
102	
103	# Memory Mapping
104	if [ -n "${MEMMAPPING}" ]; then
105	  sed -i "/^memory-mapping:/c\memory-mapping: ${MEMMAPPING}" /storage/.config/Vita3K/config.yml
106	else
107	  sed -i "/^memory-mapping:/c\memory-mapping: double-buffer" /storage/.config/Vita3K/config.yml
108	fi
109	
110	# Vsync
111	if [ "${VSYNC}" = "false" ]; then
112	  sed -i "/^v-sync:/c\v-sync: false" /storage/.config/Vita3K/config.yml
113	else
114	  sed -i "/^v-sync:/c\v-sync: true" /storage/.config/Vita3K/config.yml
115	fi
116	
117	# Anisotropic Filtering
118	if [ -n "${ANISO}" ]; then
119	  sed -i "/^anisotropic-filtering:/c\anisotropic-filtering: ${ANISO}" /storage/.config/Vita3K/config.yml
120	else
121	  sed -i "/^anisotropic-filtering:/c\anisotropic-filtering: 1" /storage/.config/Vita3K/config.yml
122	fi
123	
124	# FPS Hack
125	if [ "${FPSHACK}" = "true" ]; then
126	  sed -i "/^fps-hack:/c\fps-hack: true" /storage/.config/Vita3K/config.yml
127	else
128	  sed -i "/^fps-hack:/c\fps-hack: false" /storage/.config/Vita3K/config.yml
129	fi
130	
131	# NGS Audio Engine
132	if [ "${NGSENABLE}" = "false" ]; then
133	  sed -i "/^ngs-enable:/c\ngs-enable: false" /storage/.config/Vita3K/config.yml
134	else
135	  sed -i "/^ngs-enable:/c\ngs-enable: true" /storage/.config/Vita3K/config.yml
136	fi
137	
138	# Disable Motion Controls
139	if [ "${DISABLEMOTION}" = "true" ]; then
140	  sed -i "/^disable-motion:/c\disable-motion: true" /storage/.config/Vita3K/config.yml
141	else
142	  sed -i "/^disable-motion:/c\disable-motion: false" /storage/.config/Vita3K/config.yml
143	fi
144	
145	# Disable Surface Sync
146	if [ "${DISABLESURFACESYNC}" = "false" ]; then
147	  sed -i "/^disable-surface-sync:/c\disable-surface-sync: false" /storage/.config/Vita3K/config.yml
148	else
149	  sed -i "/^disable-surface-sync:/c\disable-surface-sync: true" /storage/.config/Vita3K/config.yml
150	fi
151	
152	# System Confirm Button
153	if [ "${SYSBUTTON}" = "0" ]; then
154	  sed -i "/^sys-button:/c\sys-button: 0" /storage/.config/Vita3K/config.yml
155	else
156	  sed -i "/^sys-button:/c\sys-button: 1" /storage/.config/Vita3K/config.yml
157	fi
158	
159	# File Loading Delay
160	if [ -n "${FILELOADINGDELAY}" ]; then
161	  sed -i "/^file-loading-delay:/c\file-loading-delay: ${FILELOADINGDELAY}" /storage/.config/Vita3K/config.yml
162	else
163	  sed -i "/^file-loading-delay:/c\file-loading-delay: 0" /storage/.config/Vita3K/config.yml
164	fi
165	
166	# SPIR-V Shader Path
167	if [ "${SPIRVSHADER}" = "true" ]; then
168	  sed -i "/^spirv-shader:/c\spirv-shader: true" /storage/.config/Vita3K/config.yml
169	else
170	  sed -i "/^spirv-shader:/c\spirv-shader: false" /storage/.config/Vita3K/config.yml
171	fi
172	
173	# Hashless Texture Cache
174	if [ "${HASHLESSTEXCACHE}" = "true" ]; then
175	  sed -i "/^hashless-texture-cache:/c\hashless-texture-cache: true" /storage/.config/Vita3K/config.yml
176	else
177	  sed -i "/^hashless-texture-cache:/c\hashless-texture-cache: false" /storage/.config/Vita3K/config.yml
178	fi
179	
180	# HTTP Networking
181	if [ "${HTTPENABLE}" = "true" ]; then
182	  sed -i "/^http-enable:/c\http-enable: true" /storage/.config/Vita3K/config.yml
183	else
184	  sed -i "/^http-enable:/c\http-enable: false" /storage/.config/Vita3K/config.yml
185	fi
186	
187	# Check if system vita3k folder exists, which needs to be populated by Vita3K before we can do anything.
188	if [ ! -d "/storage/roms/psvita/vita3k" ]; then
189	    text_viewer -w -f 64 -t "Vita3K Setup Required" -m "Please launch Vita3K from the Tools menu first to initialize its data folder."
190	    exit 1
191	fi
192	
193	# If there aren't any installed firmware files, let the user know that it's gonna be weird...
194	if ! compgen -G "/storage/roms/bios/vita3k/*.PUP.installed" > /dev/null; then
195	    mako-notify "No firmware has been installed yet! Emulation may be unstable..." -no-es
196	fi
197	
198	# Handle file types depending on extension
199	# .pkg: Check for a matching .txt with the same name and hope it contains the required ZRIF,
200	#       then install the game, scan to create the .psvita entry, then rename the now
201	#       redundant .pkg file since the game is now in the vita3k system folder.
202	# .zip: Pass directly to Vita3K since no decryption is needed, then scan on exit to create
203	#       the .psvita entry, and also rename the redundant .zip file. Same reasoning as .pkg files.
204	# .psvita: This game is already installed, just pass the ID contained in it to Vita3K.
205	# TODO: Maybe add a cleanup script for .installed GAME files (not firmware since we need to be able to
206	#       tell if they've been installed yet), if the user wants to reclaim space?
207	#       Probably not polite to just delete them automatically, even if they aren't needed anymore.
208	
209	# Snapshot the installed games, so we can see if one was just installed for later.
210	APPS_BEFORE=$(ls /storage/roms/psvita/vita3k/ux0/app/ 2>/dev/null)
211	NEW_ID=""
212	
213	case "$GAME" in
214	    *.pkg)
215	        # Check for the matching .txt file with the ZRIF, and if it's not there, bail since we literally can't install a .pkg without it.
216	        if [ ! -f "${GAME%.pkg}.txt" ]; then
217	            text_viewer -w -f 64 -t "ZRIF Required" -m "A .txt file with the same name as the .pkg and containing the ZRIF string is required to install and play this game. Please place it next to the .pkg file and try again."
218	            exit 1
219	        fi
220	
221	        # Install the requested game and scan so the next gamelist update catches it.
222	        # Spawn with foot so that output displays as the game is installed, letting the user know something is happening.
223	        foot /usr/bin/vita3k-sa -F --pkg "${GAME}" --zrif "$(cat "${GAME%.pkg}.txt")"
224	        /usr/bin/scan_vita3k.sh
225	
226	        # Get the newly installed game's ID and run it!
227	        NEW_ID=$(grep -vxFf <(echo "$APPS_BEFORE") <(ls /storage/roms/psvita/vita3k/ux0/app/) | head -1)
228	        /usr/bin/vita3k-sa -F -E -r "${NEW_ID}"
229	
230	        # Mark them as installed so they don't get caught by any other scans or get put in the gamelist more than once.
231	        mv "${GAME}" "${GAME}.installed"
232	        mv "${GAME%.pkg}.txt" "${GAME%.pkg}.txt.installed"
233	        ;;
234	    *.zip)
235	        # Vita3K needs to be run in the folder of the game to install if it's a .zip... for some reason.
236	        cd "/storage/roms/psvita"
237	
238	        # Otherwise, reasoning applies similarly for .zip files, but they're packaged with a ZRIF and actually run immediately.
239	        foot /usr/bin/vita3k-sa -F -E "${ROMNAME}"
240	        /usr/bin/scan_vita3k.sh
241	
242	        # Store the new game's ID for the check later.
243	        NEW_ID=$(grep -vxFf <(echo "$APPS_BEFORE") <(ls /storage/roms/psvita/vita3k/ux0/app/) | head -1)
244	        mv "${GAME}" "${GAME%.zip}.installed"
245	        ;;
246	    *.psvita)
247	        /usr/bin/vita3k-sa -F -E -r "$(cat "${GAME}")"
248	        ;;
249	esac
250	
251	# Check if we got a new game, or just launched one that was already installed to forcefully update the gamelist.
252	if [ -n "${NEW_ID}" ]; then
253	    # TODO: Don't do this. Find a better way if possible.
254	    killall emulationstation || true
255	fi
```

### `projects/ROCKNIX/packages/emulators/standalone/xemu-sa/scripts/start_xemu.sh`

```
1	# SPDX-License-Identifier: GPL-2.0-or-later
2	# Copyright (C) 2022-present JELOS (https://github.com/JustEnoughLinuxOS)
3	# Copyright (C) 2025-present ROCKNIX (https://github.com/ROCKNIX)
4	
5	. /etc/profile
6	set_kill set "-9 xemu"
7	
8	SOURCE_DIR="/usr/config/xemu"
9	CONF_DIR="/storage/.config/xemu"
10	BIOS_DIR="/storage/roms/bios/xemu"
11	XEMU_INI="xemu.toml"
12	
13	#Check if xemu exists in .config
14	if [ ! -d "${CONF_DIR}" ]; then
15	        cp -r "${SOURCE_DIR}" "${CONF_DIR}"
16	fi
17	
18	#Copy Xemu config at script launch
19	cp -r "${SOURCE_DIR}/${XEMU_INI}" "${CONF_DIR}/${XEMU_INI}"
20	
21	#Make xemu bios folder
22	if [ ! -d "${BIOS_DIR}/bios" ]; then
23	    mkdir -p "${BIOS_DIR}/bios"
24	fi
25	
26	#Make xemu eeprom folder
27	if [ ! -d "${BIOS_DIR}/eeprom" ]; then
28	    mkdir -p "${BIOS_DIR}/eeprom"
29	fi
30	
31	#Make xemu hdd folder
32	if [ ! -d "${BIOS_DIR}/hdd" ]; then
33	    mkdir -p "${BIOS_DIR}/hdd"
34	fi
35	
36	#Check if HDD image exists
37	if [ ! -f "${BIOS_DIR}/hdd/xbox_hdd.qcow2" ]; then
38	    unzip -o "${SOURCE_DIR}/hdd.zip" -d "${BIOS_DIR}/hdd/"
39	fi
40	
41	#Emulation Station Features
42	GAME=$(echo "${1}"| sed "s#^/.*/##")
43	PLATFORM=$(echo "${2}"| sed "s#^/.*/##")
44	ASPECT=$(get_setting aspect_ratio "${PLATFORM}" "${GAME}")
45	FIT=$(get_setting fit "${PLATFORM}" "${GAME}")
46	CLOCK=$(get_setting cpu_clock_speed "${PLATFORM}" "${GAME}")
47	CSHADERS=$(get_setting cache_shaders_to_disk "${PLATFORM}" "${GAME}")
48	IRES=$(get_setting internal_resolution "${PLATFORM}" "${GAME}")
49	GRENDERER=$(get_setting graphics_backend "${PLATFORM}" "${GAME}")
50	SHOWFPS=$(get_setting show_fps "${PLATFORM}" "${GAME}")
51	SKIPBOOT=$(get_setting skip_boot_animation "${PLATFORM}" "${GAME}")
52	SMEM=$(get_setting system_memory "${PLATFORM}" "${GAME}")
53	VSYNC=$(get_setting vsync "${PLATFORM}" "${GAME}")
54	
55	# Set the cores to use
56	CORES=$(get_setting "cores" "${PLATFORM}" "${GAME}")
57	if [ "${CORES}" = "little" ]
58	then
59	  EMUPERF="${SLOW_CORES}"
60	elif [ "${CORES}" = "big" ]
61	then
62	  EMUPERF="${FAST_CORES}"
63	else
64	  ### All..
65	  unset EMUPERF
66	fi
67	
68	  #Aspect Ratio
69		if [ "$ASPECT" = "0" ]; then
70	  		sed -i "/aspect_ratio =/c\aspect_ratio = '4x3'" "${CONF_DIR}/${XEMU_INI}"
71	        elif [ "$ASPECT" = "1" ]; then
72	                sed -i "/aspect_ratio =/c\aspect_ratio = '16x9'" "${CONF_DIR}/${XEMU_INI}"
73	        else
74	                sed -i "/aspect_ratio =/c\aspect_ratio = 'native'" "${CONF_DIR}/${XEMU_INI}"
75	        fi
76	
77	  #Fit
78		if [ "$FIT" = "center" ]; then
79	                sed -i "/fit =/c\fit = 'center'" "${CONF_DIR}/${XEMU_INI}"
80	        elif [ "$FIT" = "stretch" ]; then
81	                sed -i "/fit =/c\fit = 'stretch'" "${CONF_DIR}/${XEMU_INI}"
82	        elif [ "$FIT" = "scale" ]; then
83	                sed -i "/fit =/c\fit = 'scale'" "${CONF_DIR}/${XEMU_INI}"
84	        else
85	                sed -i "/fit =/c\fit = 'integer'" "${CONF_DIR}/${XEMU_INI}"
86	        fi
87	
88	  #Cache shaders to disk
89	        if [ "$CSHADERS" = "false" ]; then
90	                sed -i "/cache_shaders =/c\cache_shaders = false" "${CONF_DIR}/${XEMU_INI}"
91	        else
92	                sed -i "/cache_shaders =/c\cache_shaders = true" "${CONF_DIR}/${XEMU_INI}"
93	        fi
94	
95	  #CPU Clock Speed
96	        if [ "$CLOCK" = "050" ]; then
97	                sed -i "/override_clockspeed =/c\override_clockspeed = true" "${CONF_DIR}/${XEMU_INI}"
98	                sed -i "/cpu_clockspeed_scale =/c\cpu_clockspeed_scale = 0.500000" "${CONF_DIR}/${XEMU_INI}"
99	        elif [ "$CLOCK" = "060" ]; then
100	                sed -i "/override_clockspeed =/c\override_clockspeed = true" "${CONF_DIR}/${XEMU_INI}"
101	                sed -i "/cpu_clockspeed_scale =/c\cpu_clockspeed_scale = 0.600000" "${CONF_DIR}/${XEMU_INI}"
102	        elif [ "$CLOCK" = "070" ]; then
103	                sed -i "/override_clockspeed =/c\override_clockspeed = true" "${CONF_DIR}/${XEMU_INI}"
104	                sed -i "/cpu_clockspeed_scale =/c\cpu_clockspeed_scale = 0.700000" "${CONF_DIR}/${XEMU_INI}"
105	        elif [ "$CLOCK" = "080" ]; then
106	                sed -i "/override_clockspeed =/c\override_clockspeed = true" "${CONF_DIR}/${XEMU_INI}"
107	                sed -i "/cpu_clockspeed_scale =/c\cpu_clockspeed_scale = 0.800000" "${CONF_DIR}/${XEMU_INI}"
108	        elif [ "$CLOCK" = "090" ]; then
109	                sed -i "/override_clockspeed =/c\override_clockspeed = true" "${CONF_DIR}/${XEMU_INI}"
110	                sed -i "/cpu_clockspeed_scale =/c\cpu_clockspeed_scale = 0.900000" "${CONF_DIR}/${XEMU_INI}"
111	        elif [ "$CLOCK" = "110" ]; then
112	                sed -i "/override_clockspeed =/c\override_clockspeed = true" "${CONF_DIR}/${XEMU_INI}"
113	                sed -i "/cpu_clockspeed_scale =/c\cpu_clockspeed_scale = 1.100000" "${CONF_DIR}/${XEMU_INI}"
114	        elif [ "$CLOCK" = "120" ]; then
115	                sed -i "/override_clockspeed =/c\override_clockspeed = true" "${CONF_DIR}/${XEMU_INI}"
116	                sed -i "/cpu_clockspeed_scale =/c\cpu_clockspeed_scale = 1.200000" "${CONF_DIR}/${XEMU_INI}"
117	        elif [ "$CLOCK" = "130" ]; then
118	                sed -i "/override_clockspeed =/c\override_clockspeed = true" "${CONF_DIR}/${XEMU_INI}"
119	                sed -i "/cpu_clockspeed_scale =/c\cpu_clockspeed_scale = 1.300000" "${CONF_DIR}/${XEMU_INI}"
120	        elif [ "$CLOCK" = "140" ]; then
121	                sed -i "/override_clockspeed =/c\override_clockspeed = true" "${CONF_DIR}/${XEMU_INI}"
122	                sed -i "/cpu_clockspeed_scale =/c\cpu_clockspeed_scale = 1.400000" "${CONF_DIR}/${XEMU_INI}"
123	        elif [ "$CLOCK" = "150" ]; then
124	                sed -i "/override_clockspeed =/c\override_clockspeed = true" "${CONF_DIR}/${XEMU_INI}"
125	                sed -i "/cpu_clockspeed_scale =/c\cpu_clockspeed_scale = 1.500000" "${CONF_DIR}/${XEMU_INI}"
126		else
127	                sed -i "/override_clockspeed =/c\override_clockspeed = false" "${CONF_DIR}/${XEMU_INI}"
128		fi
129	
130	  #Graphics Backend
131		if [ "$GRENDERER" = "vulkan" ]; then
132			sed -i "/renderer =/c\renderer = 'VULKAN'" "${CONF_DIR}/${XEMU_INI}"
133	        elif [ "$GRENDERER" = "opengl" ]; then
134	                sed -i "/renderer =/c\renderer = 'OPENGL'" "${CONF_DIR}/${XEMU_INI}"
135		else
136			sed -i "/renderer =/c\renderer = '@GRENDERER@'" "${CONF_DIR}/${XEMU_INI}"
137	  	fi
138	
139	  #Internal Resolution
140	        if [ "$IRES" = "2" ]; then
141	                sed -i "/surface_scale =/c\surface_scale = 2" "${CONF_DIR}/${XEMU_INI}"
142	        elif [ "$IRES" = "3" ]; then
143	                sed -i "/surface_scale =/c\surface_scale = 3" "${CONF_DIR}/${XEMU_INI}"
144	        elif [ "$IRES" = "4" ]; then
145	                sed -i "/surface_scale =/c\surface_scale = 4" "${CONF_DIR}/${XEMU_INI}"
146	        else
147	                sed -i "/surface_scale =/c\surface_scale = 1" "${CONF_DIR}/${XEMU_INI}"
148	        fi
149	
150	  #Show FPS
151		if [ "$SHOWFPS" = "1" ]
152		then
153			export GALLIUM_HUD="simple,fps"
154		fi
155	
156	  #Skip boot animation
157	        if [ "$SKIPBOOT" = "false" ]; then
158	                sed -i "/skip_boot_anim =/c\skip_boot_anim = false" "${CONF_DIR}/${XEMU_INI}"
159	        else
160	                sed -i "/skip_boot_anim =/c\skip_boot_anim = true" "${CONF_DIR}/${XEMU_INI}"
161	        fi
162	
163	  #System memory
164	        if [ "$SMEM" = "128" ]; then
165	                sed -i "/mem_limit =/c\mem_limit = '128'" "${CONF_DIR}/${XEMU_INI}"
166	        else
167	                sed -i "/mem_limit =/c\mem_limit = '64'" "${CONF_DIR}/${XEMU_INI}"
168	        fi
169	
170	  #Vsync
171	        if [ "$VSYNC" = "false" ]; then
172	                sed -i "/vsync =/c\vsync = false" "${CONF_DIR}/${XEMU_INI}"
173	        else
174	                sed -i "/vsync =/c\vsync = true" "${CONF_DIR}/${XEMU_INI}"
175	        fi
176	
177	# Debugging info:
178	  echo "GAME set to: ${GAME}"
179	  echo "PLATFORM set to: ${PLATFORM}"
180	  echo "CPU CORES set to: ${EMUPERF}"
181	  echo "ASPECT set to: ${ASPECT}"
182	  echo "SCREEN FIT set to: ${FIT}"
183	  echo "CLOCK set to: ${CLOCK}"
184	  echo "CACHE SHADERS set to: ${CSHADERS}"
185	  echo "INTERNAL RESOLUTION set to: ${IRES}"
186	  echo "GRAPHICS REDNERER set to: ${GRENDERER}"
187	  echo "SHOW FPS set to: ${SHOWFPS}"
188	  echo "SKIP BOOT SCREEN set to: ${SKIPBOOT}"
189	  echo "SYSTEM MEMORY set to: ${SMEM}"
190	  echo "VSYNC set to: ${VSYNC}"
191	  echo "CONF DIR set to: ${CONF_DIR}"
192	  echo "SOURCE DIR set to: ${SOURCE_DIR}"
193	  echo "INI set to: ${XEMU_INI}"
194	  echo "BIOS DIR set to: ${BIOS_DIR}"
195	  echo "Launching /usr/bin/xemu -fullscreen -config_path {CONF_DIR}/${XEMU_INI} -dvd_path ${1}"
196	
197	# Run Xemu emulator
198	  ${EMUPERF} /usr/bin/xemu -full-screen -config_path "${CONF_DIR}/${XEMU_INI}" -dvd_path "${1}"
```

### `projects/ROCKNIX/packages/emulators/standalone/yabasanshiro-sa/package.mk`

```
1	# SPDX-License-Identifier: GPL-2.0
2	# Copyright (C) 2024-present ROCKNIX (https://github.com/ROCKNIX)
3	
4	PKG_NAME="yabasanshiro-sa"
5	PKG_VERSION="a40dace1ae0af3ebd45848549fdf396f40e3930f"
6	PKG_LICENSE="GPL-2.0-or-later"
7	PKG_SITE="https://github.com/sydarn/yabause"
8	PKG_URL="${PKG_SITE}.git"
9	PKG_DEPENDS_TARGET="toolchain SDL2 boost openal-soft zlib"
10	PKG_LONGDESC="Yabause is a Sega Saturn emulator and took over as Yaba Sanshiro"
11	# Not built for GENERIC_X64, the fork's QA device: PKG_EMUS lists
12	# yabasanshiro-sa for every device, and on x86_64 its CMake configuration
13	# selects the qt port rather than retro_arena, so makeinstall_target's
14	# retro_arena/yabasanshiro is never built and the install fails (a cold
15	# GENERIC_X64 build, 2026-09-19). Every other device builds it as upstream
16	# does since its cleanup (28e750db32) dropped the aarch64-only restriction;
17	# AMD64 meets the same CMake choice, which is upstream's to see.
18	if [ "${DEVICE}" = "GENERIC_X64" ]; then
19	  PKG_ARCH="aarch64"
20	fi
21	PKG_TOOLCHAIN="cmake-make"
22	PKG_BUILD_FLAGS="+speed"
23	
24	if [ ! "${OPENGL}" = "no" ]; then
25	  PKG_DEPENDS_TARGET+=" ${OPENGL} glu libglvnd"
26	  PKG_CMAKE_OPTS_TARGET+=" -DUSE_EGL=ON -DUSE_OPENGL=ON"
27	fi
28	
29	if [ "${OPENGLES_SUPPORT}" = yes ]; then
30	  PKG_DEPENDS_TARGET+=" ${OPENGLES}"
31	  PKG_CMAKE_OPTS_TARGET+=" -DUSE_EGL=ON -DUSE_OPENGL=OFF"
32	fi
33	
34	if [ "${VULKAN_SUPPORT}" = "yes" ]; then
35	  PKG_DEPENDS_TARGET+=" ${VULKAN}"
36	fi
37	
38	PKG_CMAKE_OPTS_TARGET+=" -DCMAKE_SYSTEM_PROCESSOR=x86_64
39	                         -DOPENGL_INCLUDE_DIR=${SYSROOT_PREFIX}/usr/include \
40	                         -DOPENGL_opengl_LIBRARY=${SYSROOT_PREFIX}/usr/lib \
41	                         -DOPENGL_glx_LIBRARY=${SYSROOT_PREFIX}/usr/lib \
42	                         -DLIBPNG_LIB_DIR=${SYSROOT_PREFIX}/usr/lib \
43	                         -Dpng_STATIC_LIBRARIES=${SYSROOT_PREFIX}/usr/lib/libpng16.so \
44	                         -DCMAKE_BUILD_TYPE=Release \
45	                         -DCMAKE_VERBOSE_MAKEFILE:BOOL=ON"
46	
47	post_unpack() {
48	  # use host versions
49	  sed -i "s|COMMAND m68kmake|COMMAND ${PKG_BUILD}/m68kmake_host|" ${PKG_BUILD}/yabause/src/musashi/CMakeLists.txt
50	  sed -i "s|COMMAND ./bin2c|COMMAND ${PKG_BUILD}/bin2c_host|" ${PKG_BUILD}/yabause/src/retro_arena/nanogui-sdl/CMakeLists.txt
51	  find ${PKG_BUILD} -type f -name "CMakeLists.txt" -exec sed -i 's/^\s*cmake_minimum_required.*$/cmake_minimum_required(VERSION 3.5)/' {} +
52	}
53	
54	configure_package() {
55	  PKG_CMAKE_SCRIPT="${PKG_BUILD}/yabause/CMakeLists.txt"
56	}
57	
58	pre_configure_target() {
59	  case ${ARCH} in
60	    aarch64)
61	      PKG_CMAKE_OPTS_TARGET+=" -DYAB_WANT_ARM7=ON \
62	                               -DYAB_WANT_DYNAREC_DEVMIYAX=ON \
63	                               -DYAB_PORTS=retro_arena \
64	                               -DCMAKE_PROJECT_INCLUDE=${PKG_BUILD}/yabause/src/retro_arena/n2.cmake"
65	      ;;
66	  esac
67	}
68	
69	pre_make_target() {
70	  # runs on host so make them manually if package is not crosscompile friendly
71	  ${HOST_CC} ${PKG_BUILD}/yabause/src/retro_arena/nanogui-sdl/resources/bin2c.c -o ${PKG_BUILD}/bin2c_host
72	  ${HOST_CC} ${PKG_BUILD}/yabause/src/musashi/m68kmake.c -o ${PKG_BUILD}/m68kmake_host
73	}
74	
75	makeinstall_target() {
76	  mkdir -p ${INSTALL}/usr/bin
77	    cp -a ${PKG_BUILD}/.${TARGET_NAME}/src/retro_arena/yabasanshiro ${INSTALL}/usr/bin
78	    cp -a ${PKG_DIR}/scripts/start_yabasanshiro.sh ${INSTALL}/usr/bin
79	
80	  mkdir -p ${INSTALL}/usr/config/yabasanshiro
81	    cp -a ${PKG_DIR}/config/config ${INSTALL}/usr/config/yabasanshiro/.config
82	    cp -a ${PKG_DIR}/config/devices ${INSTALL}/usr/config/yabasanshiro
83	}
```

### `projects/ROCKNIX/packages/emulators/standalone/yabasanshiro-sa/scripts/start_yabasanshiro.sh`

```
1	#!/bin/bash
2	
3	# SPDX-License-Identifier: GPL-2.0-or-later
4	# Copyright (C) 2021-present Shanti Gilbert (https://github.com/shantigilbert)
5	# Copyright (C) 2023 JELOS (https://github.com/JustEnoughLinuxOS)
6	
7	# Source predefined functions and variables
8	. /etc/profile
9	set_kill set "-9 yabasanshiro"
10	
11	ROM_DIR="/storage/roms/saturn/yabasanshiro"
12	CONFIG_DIR="/storage/.config/yabasanshiro"
13	SOURCE_DIR="/usr/config/yabasanshiro"
14	BIOS_BACKUP="/storage/roms/bios/yabasanshiro"
15	SAVESTATE_DIR="/storage/roms/savestates/saturn/yabasanshiro/"
16	
17	if [ ! -d "${ROM_DIR}" ]
18	then
19	  mkdir -p "${ROM_DIR}"
20	fi
21	
22	if [ ! -d "${BIOS_BACKUP}" ]
23	then
24	  mkdir -p "${BIOS_BACKUP}"
25	fi
26	
27	if [ ! -d "${CONFIG_DIR}" ]
28	then
29	  mkdir -p "${CONFIG_DIR}"
30	fi
31	
32	if [ ! -d "${SAVESTATE_DIR}" ]
33	then
34	  mkdir -p "${SAVESTATE_DIR}"
35	fi
36	
37	if [ ! -e "${CONFIG_DIR}/input.cfg" ]
38	then
39	  rm -f ${CONFIG_DIR}/keymapv2.json
40	
41	  # Handle inputplumber platforms first
42	  if [[ "${HW_DEVICE}" =~ RK3576|SM6115|SM4450|SM8550|SM8650|SM8750|SM8250 ]]; then
43	    GAMEPAD="'Sony Interactive Entertainment DualSense Wireless Controller'"
44	  else
45	    # Check for js0, else fall back to joypad
46	    if grep -q "js0" /proc/bus/input/devices; then
47	      GAMEPAD="'$(grep -b4 js0 /proc/bus/input/devices | awk 'BEGIN {FS="\""}; /Name/ {printf $2}')'"
48	    else
49	      GAMEPAD="'$(grep -b4 joypad /proc/bus/input/devices | awk 'BEGIN {FS="\""}; /Name/ {printf $2}')'"
50	    fi
51	  fi
52	
53	  GAMEPADCONFIG=$(xmlstarlet sel -t -c "//inputList/inputConfig[@deviceName=${GAMEPAD}]" -n /storage/.emulationstation/es_input.cfg)
54	
55	  MAPPING_FILE="/usr/config/yabasanshiro/devices/keymapv2_$(eval echo $GAMEPAD).json"
56	  if [ -e "${MAPPING_FILE}" ]; then
57	    cp ${MAPPING_FILE} ${CONFIG_DIR}/keymapv2.json
58	  fi
59	
60	  if [ ! -z "${GAMEPADCONFIG}" ]
61	  then
62	    cat <<EOF >${CONFIG_DIR}/input.cfg
63	<?xml version="1.0"?>
64	<inputList>
65	${GAMEPADCONFIG}
66	</inputList>
67	EOF
68	  fi
69	fi
70	
71	BIOS=""
72	GAME=$(echo "${1}"| sed "s#^/.*/##")
73	PLATFORM=$(echo "${2}"| sed "s#^/.*/##")
74	USE_BIOS=$(get_setting use_hlebios "${PLATFORM}" "${GAME}")
75	if [ ! "${USE_BIOS}" = 1 ]
76	then
77	  USE_BIOS=$(get_setting use_hlebios "${PLATFORM}")
78	fi
79	
80	if [ "$USE_BIOS" = 1 ]
81	then
82	  for BIOS in saturn_bios.bin sega_101.bin mpr-17933.bin mpr-18811-mx.ic1 mpr-19367-mx.ic1 stvbios.zip
83	  do
84	    BIOS=$(find /storage/roms/bios -name ${BIOS} -print 2>/dev/null)
85	    if [ ! -z "${BIOS}" ]
86	    then
87	      BIOS="-b ${BIOS}"
88	      break
89	    fi
90	  done
91	fi
92	
93	if [ ! -e "${CONFIG_DIR}/${GAME}.config" ]
94	then
95	  cp -f ${SOURCE_DIR}/.config "${CONFIG_DIR}/${GAME}.config"
96	fi
97	
98	#Set the cores to use
99	CORES=$(get_setting "cores" "${PLATFORM}" "${GAME}")
100	if [ "${CORES}" = "little" ]
101	then
102	  EMUPERF="${SLOW_CORES}"
103	elif [ "${CORES}" = "big" ]
104	then
105	  EMUPERF="${FAST_CORES}"
106	else
107	  ### All..
108	  unset EMUPERF
109	fi
110	
111	echo "Command: yabasanshiro -r 2 -i "${1}" ${BIOS}" >>/var/log/exec.log 2>&1
112	${EMUPERF} yabasanshiro -r 2 -i "${1}" ${BIOS} >>/var/log/exec.log 2>&1 ||:
```

## Excerpts outside the membership (read-only context), line-numbered

### `projects/ROCKNIX/packages/rocknix/sources/scripts/runemu.sh` lines 18-32 at `8ebaf8daad`

```
18	# $4 = Emulator
19	
20	ARGUMENTS="$@"
21	### The platform is the first -P<platform> argument after the ROM, taken
22	### whole. ${ARGUMENTS##*-P} read from the LAST "-P" anywhere in the joined
23	### line, so a netplay nick such as My-Player made the platform "layer"
24	### (#308, stream E2's reading of the launch command).
25	PLATFORM=""
26	for ARG in "${@:2}"; do case "${ARG}" in -P?*) PLATFORM="${ARG#-P}"; break ;; esac; done
27	CORE="${ARGUMENTS##*--core=}"  # read from --core= onwards
28	CORE="${CORE%% *}"  # until a space is found
29	EMULATOR="${ARGUMENTS##*--emulator=}"  # read from --emulator= onwards
30	EMULATOR="${EMULATOR%% *}"  # until a space is found
31	ROMNAME="$1"
32	BASEROMNAME=${ROMNAME##*/}
```

### `projects/ROCKNIX/packages/rocknix/sources/scripts/runemu.sh` lines 120-132 at `8ebaf8daad`

```
120	                : >${LOG_DIRECTORY}/${LOG_FILE}
121	                log $0 "Emulation Run Log - Started at $(date)"
122	        fi
123	}
124	
125	function quit() {
126	        ${VERBOSE} && log $0 "Cleaning up and exiting"
127	        bluetooth enable
128	        set_kill set "emulationstation"
129	        clear_screen
130	        DEVICE_CPU_GOVERNOR=$(get_setting system.cpugovernor)
131	        ${DEVICE_CPU_GOVERNOR}
132	        exit $1
```

### `projects/ROCKNIX/packages/rocknix/sources/scripts/runemu.sh` lines 170-182 at `8ebaf8daad`

```
170	  *)
171	    LOG=true
172	  ;;
173	esac
174	
175	### Prepare to load our emulator and game.
176	loginit "$1" "$2" "$3" "$4"
177	clear_screen
178	bluetooth disable
179	set_kill stop
180	
181	### Determine which emulator we're launching and make appropriate adjustments before launching.
182	${VERBOSE} && log $0 "Configuring for ${EMULATOR}"
```

### `projects/ROCKNIX/packages/rocknix/sources/scripts/runemu.sh` lines 230-240 at `8ebaf8daad`

```
230	  fi
231	}
232	
233	case ${EMULATOR} in
234	  mednafen)
235	    set_kill set "-9 mednafen"
236	    RUNTHIS='${RUN_SHELL} /usr/bin/start_mednafen.sh "${ROMNAME}" "${CORE}" "${PLATFORM}"'
237	  ;;
238	  retroarch)
239	    # Make sure NETWORK_PLAY isn't defined before we start our tests/configuration.
240	    del_setting netplay.mode
```

### `projects/ROCKNIX/packages/rocknix/sources/scripts/runemu.sh` lines 350-400 at `8ebaf8daad`

```
350	      rm -f ${SET_SETTINGS_TMP}
351	      ${VERBOSE} && log $0 "Extra Options: ${EXTRAOPTS}"
352	    fi
353	
354	    if [[ ${EXTRAOPTS} != 0 ]]; then
355	      RUNTHIS=$(echo ${RUNTHIS} | sed "s|--config|${EXTRAOPTS} --config|")
356	    fi
357	  ;;
358	  *)
359	    case ${PLATFORM} in
360	      "setup")
361	        RUNTHIS='${RUN_SHELL} "${ROMNAME}"'
362	      ;;
363	      "gamecube"|"triforce")
364	        DOLPHIN_LAUNCH=true
365	        RUNTHIS='${RUN_SHELL} /usr/bin/start_dolphin_gc.sh "${ROMNAME}" "${PLATFORM}" "${CORE}"'
366	      ;;
367	      "wii"|"wiiware")
368	        DOLPHIN_LAUNCH=true
369	        RUNTHIS='${RUN_SHELL} /usr/bin/start_dolphin_wii.sh "${ROMNAME}" "${PLATFORM}" "${CORE}"'
370	      ;;
371	      "ports")
372	      if [[ "${ROMNAME,,}" == *".appimage" ]]; then
373	        RUNTHIS='${EMUPERF} "${ROMNAME}"'
374	      else
375	        RUNTHIS='${EMUPERF} ${RUN_SHELL} "${ROMNAME}"'
376	      fi
377	        chmod +x "${ROMNAME}"
378	        sed -i "/^ACTIVE_GAME=/c\ACTIVE_GAME=\"${ROMNAME}\"" /storage/.config/PortMaster/mapper.txt
379	        sed -i "/^ACTIVE_PLATFORM=/c\ACTIVE_PLATFORM=\"${PLATFORM}\"" /storage/.config/PortMaster/mapper.txt
380	      ;;
381	      "windows")
382	        RUNTHIS='${EMUPERF} ${RUN_SHELL} "${ROMNAME}"'
383	        # Hook into Portmaster control mapping
384	        sed -i "/^ACTIVE_GAME=/c\ACTIVE_GAME=\"${ROMNAME}\"" /storage/.config/PortMaster/mapper.txt
385	        sed -i "/^ACTIVE_PLATFORM=/c\ACTIVE_PLATFORM=\"${PLATFORM}\"" /storage/.config/PortMaster/mapper.txt
386	      ;;
387	      "shell")
388	        RUNTHIS='${RUN_SHELL} "${ROMNAME}"'
389	      ;;
390	      *)
391	        RUNTHIS='${RUN_SHELL} "/usr/bin/start_${CORE%-*}.sh" "${ROMNAME}" "${PLATFORM}"'
392	      ;;
393	    esac
394	  ;;
395	esac
396	
397	### Execution time.
398	clear_screen
399	${VERBOSE} && log $0 "executing game: ${ROMNAME}"
400	${VERBOSE} && log $0 "script to execute: ${RUNTHIS}"
```

### `projects/ROCKNIX/packages/rocknix/sources/scripts/runemu.sh` lines 480-505 at `8ebaf8daad`

```
480	### Clear the exit hotkey marker on the way into the emulator, so a press
481	### left over from an earlier launch -- or from the carousel, where the same
482	### hotkey kills EmulationStation -- can never be read as this launch ending
483	### (fork #92). Both dispatch paths below run through here, and nothing above
484	### it starts an emulator; keep it that way.
485	rm -f "${EXIT_HOTKEY_MARKER}"
486	
487	# If the rom is a shell script just execute it, useful for DOSBOX and ScummVM scan scripts
488	if [[ "${ROMNAME}" == *".sh" ]] && [ ! "${PLATFORM}" = "ports" ] && [ ! "${PLATFORM}" = "windows" ]; then
489	        ${VERBOSE} && log $0 "Executing shell script ${ROMNAME}"
490	        DOLPHIN_LAUNCH=false
491	        "${ROMNAME}" &>>${OUTPUT_LOG}
492	        ret_error=$?
493	else
494	        ${VERBOSE} && log $0 "Executing $(eval echo ${RUNTHIS})"
495	        # A Dolphin preparation refusal owns only this launch's native message.
496	        # Other emulator exit codes must not acquire a stale custom error.
497	        if [ "${DOLPHIN_LAUNCH}" = true ]; then
498	                rm -f /tmp/launch_error.log || quit 1
499	        fi
500	        eval ${RUNTHIS} &>>${OUTPUT_LOG}
501	        ret_error=$?
502	fi
503	
504	### Switch back to performance mode to clean up
505	performance
```

### `projects/ROCKNIX/packages/sysutils/system-utils/sources/scripts/input_sense` lines 176-226 at `8ebaf8daad`

```
176	}
177	
178	### Simple functions to execute button actions, including global kill.
179	execute_kill() {
180	  if [ -e "/tmp/.process-kill-data" ]; then
181	    TO_KILL="$(cat /tmp/.process-kill-data)"
182	    ### Say that the player asked to leave, before the signal goes out. runemu.sh
183	    ### maps 137/143 to a clean exit already, which covers every emulator that
184	    ### dies on the signal -- but RetroArch catches SIGTERM and ends with its own
185	    ### exit(1), the same status as "Failed to load content", so the exit code
186	    ### alone cannot tell a forced quit from a failed launch (fork #92,
187	    ### D-LAUNCH-002). The marker sits beside the kill data this function already
188	    ### reads, in /tmp, because /tmp is a tmpfs: a power cut wipes it, and a
189	    ### marker that outlived the boot would make the next launch's failure read
190	    ### as clean. runemu.sh clears it on the way into the emulator and consumes
191	    ### it at exit; both it and this service run as root.
192	    touch "/tmp/.process-kill-requested" 2>/dev/null
193	
194	    ### One press, one signal. The combo re-fires this on every further B or C
195	    ### press while A is held, and RetroArch takes about half a second to shut
196	    ### down -- so a player who holds the combo a moment too long, or presses
197	    ### again because the game has not vanished yet, delivers a second SIGTERM
198	    ### into that window. RetroArch answers the second one with exit(1) and
199	    ### WITHOUT flushing SRAM: measured on the VM with a battery-backed
200	    ### cartridge, one press wrote the .srm and two left none at all, losing
201	    ### everything since the last autosave (fork #117). The first press already
202	    ### ends it cleanly in ~0.5 s, so a repeat inside the window is the player
203	    ### waiting, not asking again -- it is dropped. A deliberate second attempt
204	    ### after the window still goes through, which is what a genuinely stuck
205	    ### emulator needs.
206	    ###
207	    ### date +%s, not a sub-second clock: busybox date has no %N on every
208	    ### build, and a whole second of granularity is plenty against a window
209	    ### measured in seconds.
210	    ###
211	    ### The state is a shell variable rather than a file because there is one
212	    ### reader to remember it: the several evtest processes started above all
213	    ### pipe into the single `while read line` loop below, and both callers of
214	    ### this function are inside that loop. A file would need the same
215	    ### power-cut reasoning as the marker above and buy nothing.
216	    now="$(date +%s)"
217	    if [ -n "${LAST_KILL_AT}" ] && [ "$((now - LAST_KILL_AT))" -lt 3 ]; then
218	      ${DEBUG} && log $0 "Ignoring a repeat kill $((now - LAST_KILL_AT))s after the last one; the emulator is still shutting down"
219	      return 0
220	    fi
221	    LAST_KILL_AT="${now}"
222	
223	    ${DEBUG} && log $0 "Execute: killall ${TO_KILL}"
224	    killall ${TO_KILL} 2>/dev/null
225	  fi
226	}
```

### `projects/ROCKNIX/packages/rocknix/profile.d/001-functions` lines 505-523 at `8ebaf8daad`

```
505	  return ${rc}
506	}
507	
508	function set_kill() {
509	  if [ "${1}" = "set" ]
510	  then
511	    cat <<EOF >/tmp/.process-kill-data
512	${2}
513	EOF
514	  elif [ "${1}" = "stop" ]
515	  then
516	    if [ -e "/tmp/.process-kill-data" ]
517	    then
518	      rm -f "/tmp/.process-kill-data"
519	    fi
520	  fi
521	}
522	
523	# The device name in the only form the network accepts: letters, digits and
```

### `projects/ROCKNIX/packages/rocknix/sources/scripts/backuptool` lines 128-145 at `8ebaf8daad`

```
128	DEVICE_LABEL="$(device_label)"
129	# tar, not zip.
130	#
131	# zip does not carry a symlink as a symlink, and this OS is full of them: the
132	# config tree links into /usr for OS-shipped content. Backups written before
133	# 358eb53d3f stored those targets' bytes as regular files, and busybox unzip
134	# then aborts the *whole* restore rather than overwrite a live symlink
135	# ("exists but is not a regular file"). That cost a restore, needed a second
136	# fix on the read side (02297b9c07), and left a skip-list in this script to
137	# work around archives already in the wild.
138	#
139	# tar stores a symlink as a symlink, preserves permissions and ownership, and
140	# extracts cleanly over an existing one. Verified on-device, because Info-ZIP
141	# on a desktop and busybox on a handheld disagree, which is how the original
142	# bug stayed invisible.
143	# Archive names are a persisted compatibility contract, not OS display text.
144	ARCHIVE_OS_NAME=ROCKNIX
145	BACKUPFILE="${SETTINGS_BACKUPS}/${BACKUP_STAMP}-${DEVICE_LABEL:+${DEVICE_LABEL}-}${ARCHIVE_OS_NAME}_SETTINGS.tar.gz"
```

### `projects/ROCKNIX/packages/rocknix/sources/scripts/backuptool` lines 686-712 at `8ebaf8daad`

```
686	# the token that write_archive deletes from the archived system.cfg would
687	# come back into the archive under another name (#169; D-INFRA-010: no keys
688	# travel). Two shapes. RATOKENFILES hold the token and nothing of the
689	# player's -- PPSSPP's .dat is the bare token, Dolphin's RetroAchievements.ini
690	# and SkyEmu's ra_token.txt are rewritten whole from system.cfg, ARMSX2's
691	# secrets.ini is the shipped seed plus the token -- so they are held back
692	# like rclone.conf and skipped on restore, and the emulator writes them
693	# again from system.cfg the first time it starts after a restore, once the
694	# player has signed in again. RATOKENSETTINGS are the emulator's whole
695	# settings file with a token line in it; those travel with the value
696	# blanked, as retroarch.cfg does. Only PPSSPP's is in the default LOCATIONS;
697	# the rest are reached by a custom list such as /storage/.config.
698	RATOKENFILES=(
699	    /storage/.config/ppsspp/PSP/SYSTEM/ppsspp_retroachievements.dat  # cheevos_ppsspp.sh
700	    /storage/.config/dolphin-emu/RetroAchievements.ini               # cheevos_dolphin.sh
701	    /storage/.config/SkyEmu/ra_token.txt                             # cheevos_skyemu.sh
702	    /storage/.config/gopher64/retroachievements.json                 # written by gopher64 itself after --ra-password (#169's trace, #273)
703	    /storage/.config/ARMSX2/inis/secrets.ini                         # cheevos_armsx2.sh
704	)
705	RATOKENSETTINGS=(
706	    /storage/.config/duckstation/settings.ini   # Token =   (DuckStation's own sign-in; cheevos_duckstation.sh is disabled upstream)
707	    /storage/.config/melonDS/melonDS.ini        # RA_Token= RA_Password=   (cheevos_melonds.sh)
708	    /storage/.config/flycast/emu.cfg            # Token =   (cheevos_flycast.sh)
709	    /storage/.config/aethersx2/inis/PCSX2.ini   # Token =   (cheevos_aethersx2.sh)
710	)
711	# The offline RetroAchievements proxy's own folder (#165; D-RA-002,
712	# D-INFRA-010). Its cache holds the RetroAchievements token three ways -- the
```

### `projects/ROCKNIX/packages/rocknix/sources/scripts/backuptool` lines 1232-1262 at `8ebaf8daad`

```
1232	        then
1233	            mkdir -p "${STAGING}/storage/.config/retroarch"
1234	            to_log sed -E 's/^([a-z_]*(password|token|stream_key)) = ".*"$/\1 = ""/' "${RACFG}" \
1235	                > "${STAGING}/storage/.config/retroarch/retroarch.cfg" || SANITISE_RC=1
1236	            keep_meta "${RACFG}" "${STAGING}/storage/.config/retroarch/retroarch.cfg" || SANITISE_RC=1
1237	            SANITISED=$((SANITISED + 1))
1238	        fi
1239	
1240	        # The standalone emulators' settings files carry the token as a
1241	        # line of their own -- `Token = ` in DuckStation's, flycast's and
1242	        # AetherSX2's, `RA_Token=` and `RA_Password=` in melonDS's. Blank
1243	        # the value and keep the key, as for retroarch.cfg: the cheevos_*.sh
1244	        # script finds the line and writes the token back at the next
1245	        # launch. No other key in those files ends in Token or Password
1246	        # (checked against the shipped seeds, 2026-09-13; #169).
1247	        BLANKED=0
1248	        for CANDIDATE in "${RATOKENSETTINGS[@]}"
1249	        do
1250	            if grep -qxF "${CANDIDATE}" "${SECRETLIST}"
1251	            then
1252	                mkdir -p "${STAGING}${CANDIDATE%/*}"
1253	                to_log sed -E 's/^([A-Za-z_]*(Token|Password)[[:space:]]*=[[:space:]]*).*$/\1/' "${CANDIDATE}" \
1254	                    > "${STAGING}${CANDIDATE}" || SANITISE_RC=1
1255	                keep_meta "${CANDIDATE}" "${STAGING}${CANDIDATE}" || SANITISE_RC=1
1256	                BLANKED=$((BLANKED + 1))
1257	            fi
1258	        done
1259	        [ "${BLANKED}" -gt 0 ] && logger -t backuptool "blanked the RetroAchievements token in ${BLANKED} emulator settings file(s) (#169)"
1260	        SANITISED=$((SANITISED + BLANKED))
1261	    fi
1262	    # The list of what was left out as the image's own, for a backup that
```

### `projects/ROCKNIX/packages/virtual/emulators/package.mk` lines 12-15 at `8ebaf8daad`

```
12	PKG_EMUS="amiberry duckstation-sa flycast-sa gzdoom-sa hatarisa hypseus-singe moonlight mupen64plus-sa openbor pico-8   \
13	          ppsspp-sa scummvm-sa touchhle-sa vice-sa wine yabasanshiro-sa"
14	
15	EMUS_32BIT=""
```

### `projects/ROCKNIX/packages/virtual/emulators/package.mk` lines 35-46 at `8ebaf8daad`

```
35	  LIBRETRO_CORES+=" duckstation-lr flycast2021-lr ppsspp-lr"
36	  PKG_EMUS+=" box64 dsperate-sa portmaster"
37	fi
38	
39	### Emulators or cores for specific devices
40	case "${DEVICE}" in
41	  H700|RK3326)
42	    [ "${ENABLE_32BIT}" == "true" ] && EMUS_32BIT="box86 desmume-lr gpsp-lr pcsx_rearmed-lr"
43	    PKG_DEPENDS_TARGET+=" common-shaders glsl-shaders"
44	    PKG_EMUS+=" drastic-sa mednafen"
45	    LIBRETRO_CORES+=" uae4arm-lr"
46	    ;;
```

### `projects/ROCKNIX/packages/virtual/emulators/package.mk` lines 96-105 at `8ebaf8daad`

```
96	    ;;
97	  GENERIC_X64)
98	    # Native standalone Dolphin supports the developer VM qualification path.
99	    PKG_EMUS+=" dolphin-sa"
100	    ;;
101	  AMD64)
102	    PKG_EMUS+=" ares-sa azahar-sa cemu-sa dolphin-sa gopher64-sa mednafen melonds-sa nanoboyadvance-sa \
103	                xemu-sa skyemu-sa vita3k-sa armsx2-sa"
104	    LIBRETRO_CORES+=" beetle-psx-lr beetle-saturn-lr bsnes-lr bsnes-hd-lr dolphin-lr"
105	esac
```

### `projects/ROCKNIX/packages/virtual/emulators/package.mk` lines 205-215 at `8ebaf8daad`

```
205	    *)
206	      add_emu_core amiga retroarch puae true
207	      add_emu_core amiga retroarch puae2021 false
208	    ;;
209	  esac
210	  add_emu_core amiga amiberry amiberry false
211	  add_es_system amiga
212	
213	  ### Commodore Amiga CD32
214	  case ${DEVICE} in
215	    H700|RK3326|RK3399|RK3576|RK3566|RK3588|SM4450|SM6115|SM8250|SM8550|SM8650|SM8750)
```

### `projects/ROCKNIX/packages/virtual/emulators/package.mk` lines 975-1062 at `8ebaf8daad`

```
975	      add_emu_core n64dd ares ares-sa false
976	      ;;
977	  esac
978	  add_es_system n64dd
979	
980	  ### Nintendo DS
981	  case ${DEVICE} in
982	    H700|RK3326)
983	      add_emu_core nds drastic drastic-sa true
984	      add_emu_core nds retroarch melonds false
985	      add_emu_core nds retroarch melondsds false
986	      add_emu_core nds retroarch desmume false
987	      add_emu_core nds retroarch skyemu false
988	      add_emu_core nds dsperate dsperate-sa false
989	      ;;
990	    RK3399|RK3566|RK3576|RK3588|SM6115)
991	      add_emu_core nds drastic drastic-sa true
992	      add_emu_core nds retroarch melonds false
993	      add_emu_core nds retroarch melondsds false
994	      add_emu_core nds melonds melonds-sa false
995	      add_emu_core nds retroarch desmume false
996	      add_emu_core nds retroarch skyemu false
997	      add_emu_core nds dsperate dsperate-sa false
998	      install_script "Start MelonDS.sh"
999	      ;;
1000	    SM4450|SM8250|SM8550)
1001	      add_emu_core nds melonds melonds-sa true
1002	      add_emu_core nds drastic drastic-sa false
1003	      add_emu_core nds skyemu skyemu-sa false
1004	      add_emu_core nds retroarch melonds false
1005	      add_emu_core nds retroarch melondsds false
1006	      add_emu_core nds retroarch desmume false
1007	      add_emu_core nds retroarch skyemu false
1008	      add_emu_core nds dsperate dsperate-sa false
1009	      install_script "Start MelonDS.sh"
1010	      ;;
1011	    SM8650|SM8750)
1012	      add_emu_core nds melonds melonds-sa true
1013	      add_emu_core nds skyemu skyemu-sa false
1014	      add_emu_core nds retroarch melonds false
1015	      add_emu_core nds retroarch melondsds false
1016	      add_emu_core nds retroarch skyemu false
1017	      add_emu_core nds dsperate dsperate-sa false
1018	      install_script "Start MelonDS.sh"
1019	      ;;
1020	    AMD64)
1021	      add_emu_core nds melonds melonds-sa true
1022	      add_emu_core nds skyemu skyemu-sa false
1023	      add_emu_core nds retroarch melonds false
1024	      add_emu_core nds retroarch melondsds false
1025	      add_emu_core nds retroarch skyemu false
1026	      install_script "Start MelonDS.sh"
1027	      ;;
1028	    S922X)
1029	      add_emu_core nds drastic drastic-sa true
1030	      add_emu_core nds retroarch melonds false
1031	      add_emu_core nds retroarch melondsds false
1032	      add_emu_core nds melonds melonds-sa false
1033	      add_emu_core nds retroarch skyemu false
1034	      add_emu_core nds dsperate dsperate-sa false
1035	      install_script "Start MelonDS.sh"
1036	      ;;
1037	    *)
1038	      add_emu_core nds drastic drastic-sa true
1039	      add_emu_core nds retroarch melonds false
1040	      add_emu_core nds retroarch melondsds false
1041	      add_emu_core nds retroarch skyemu false
1042	      add_emu_core nds dsperate dsperate-sa false
1043	      ;;
1044	  esac
1045	  add_es_system nds
1046	
1047	  ### Nintendo DSiWare
1048	  case ${DEVICE} in
1049	    H700|RK3326)
1050	      add_emu_core ndsiware retroarch melondsds true
1051	      add_emu_core ndsiware dsperate dsperate-sa false
1052	      ;;
1053	    AMD64)
1054	      add_emu_core ndsiware retroarch melondsds true
1055	      add_emu_core ndsiware melonds melonds-sa false
1056	      ;;
1057	    *)
1058	      add_emu_core ndsiware retroarch melondsds true
1059	      add_emu_core ndsiware melonds melonds-sa false
1060	      add_emu_core ndsiware dsperate dsperate-sa false
1061	      ;;
1062	  esac
```

### `projects/ROCKNIX/packages/virtual/emulators/package.mk` lines 1370-1380 at `8ebaf8daad`

```
1370	  add_es_system megadriveh
1371	
1372	  ### Welback Holdings Mega Duck
1373	  add_emu_core megaduck retroarch sameduck true
1374	  add_es_system megaduck
1375	
1376	  ### Sega Saturn
1377	  add_emu_core saturn yabasanshiro yabasanshiro-sa true
1378	  add_emu_core saturn retroarch yabasanshiro false
1379	  case ${DEVICE} in
1380	    RK3588|SM6115)
```

### `projects/ROCKNIX/packages/emulators/standalone/melonds-sa/patches/000-retro-achievements.patch` lines 985-1010 at `8ebaf8daad`

```
985	+}
986	+void RAContext::Reset() {
987	+    if (client)
988	+        rc_client_reset(client);
989	+        ResetGameState();
990	+}
991	+
992	+void RAContext::LoginWithPassword(const char* username, const char* password, bool hardcore)
993	+{
994	+    if (!client) return;
995	+
996	+    rc_client_set_hardcore_enabled(client, hardcore ? 1 : 0);
997	+
998	+    rc_client_begin_login_with_password(
999	+        client,
1000	+        username,
1001	+        password,
1002	+        &LoginPasswordCallback,
1003	+        this
1004	+    );
1005	+}
1006	+void RAContext::SetCredentials(const char* user, const char* password, bool hardcore) {
1007	+    m_user = user;
1008	+    m_password = password;
1009	+    m_hardcore = hardcore;
1010	+}
```

### `projects/ROCKNIX/packages/emulators/standalone/melonds-sa/patches/000-retro-achievements.patch` lines 7515-7525 at `8ebaf8daad`

```
7515	     {"Camera1_CamDeviceName", 2, "DSi.Camera1.DeviceName", false},
7516	     {"Camera1_XFlip", 1, "DSi.Camera1.XFlip", false},
7517	-
7518	+#ifdef RETROACHIEVEMENTS_ENABLED
7519	+    {"RA_Enabled", 1, "RetroAchievements.Enabled", true},
7520	+    {"RA_Username", 2, "RetroAchievements.Username", true},
7521	+    {"RA_Password", 2, "RetroAchievements.Password", true},
7522	+    {"RA_Token", 2, "RetroAchievements.Token", true},
7523	+    {"RA_HardcoreMode", 1, "RetroAchievements.HardcoreMode", true},
7524	+    {"RA_EncoreMode", 1, "RetroAchievements.EncoreMode", true},
7525	+    {"RA_Unofficial", 1, "RetroAchievements.Unofficial", true},
```

### EmulationStation `es-app/src/guis/GuiRetroAchievementsSettings.cpp` lines 745-805 at the pin `16dbac52`

```
745			bool newState = retroachievements_enabled->getState();
746			std::string newUsername = SystemConf::getInstance()->get("global.retroachievements.username");
747			std::string newPassword = SystemConf::getInstance()->get("global.retroachievements.password");
748			std::string token = SystemConf::getInstance()->get("global.retroachievements.token");
749	
750			bool accountChanged = !retroachievementsEnabled || username != newUsername || password != newPassword;
751			// On the interface thread only for a change the player made and an
752			// address to send it from (#308 1-raoffline claude F-RA-19): nothing
753			// changed and no token was a sign-in at every close while offline,
754			// the screen waiting on the request -- its connect timeout on a
755			// hotspot with a route and no DNS (#242). That case is the token
756			// check's, on the watchers' thread, which retries when the network
757			// comes up; CheevosRetry::saveSignIn decides.
758			const CheevosRetry::SaveSignIn signIn = CheevosRetry::saveSignIn(newState, accountChanged, token.empty(),
759				!Utils::Platform::queryIPAddress().empty());
760			if (signIn == CheevosRetry::SaveSignIn::InBackground)
761				LOG(LogInfo) << "retroachievements: no token; the token check is asked to sign in, off the interface thread";
762			else if (signIn == CheevosRetry::SaveSignIn::Offline)
763			{
764				// The account changed and there is nowhere to send it from: the
765				// old token is not this account's, and the answer is the one a
766				// request would have come back with, without the wait.
767				SystemConf::getInstance()->set("global.retroachievements.token", "");
768				window->pushGui(new GuiMsgBox(window,
769					_("COULDN'T REACH RETROACHIEVEMENTS TO SIGN YOU IN.\n\nRETROACHIEVEMENTS STAYS ON. IT'LL SIGN IN WHEN YOU'RE ONLINE."),
770					_("OK")));
771			}
772			else if (signIn == CheevosRetry::SaveSignIn::Now)
773			{
774				std::string tokenOrError;
775				bool refused = false;
776				if (RetroAchievements::testAccount(newUsername, newPassword, tokenOrError, &refused))
777					SystemConf::getInstance()->set("global.retroachievements.token", tokenOrError);
778				else
779				{
780					SystemConf::getInstance()->set("global.retroachievements.token", "");
781	
782					if (refused)
783						window->pushGui(new GuiMsgBox(window,
784							_("RETROACHIEVEMENTS DIDN'T ACCEPT YOUR SIGN-IN:") + "\n" + tokenOrError + "\n\n"
785							+ _("RETROACHIEVEMENTS STAYS ON. CHECK YOUR USERNAME AND PASSWORD, THEN TRY AGAIN."),
786							_("OK"), nullptr, GuiMsgBoxIcon::ICON_ERROR));
787					else if (accountChanged)
788						window->pushGui(new GuiMsgBox(window,
789							_("COULDN'T REACH RETROACHIEVEMENTS TO SIGN YOU IN.\n\nRETROACHIEVEMENTS STAYS ON. IT'LL SIGN IN WHEN YOU'RE ONLINE."),
790							_("OK")));
791					else
792						LOG(LogWarning) << "retroachievements: could not reach RetroAchievements for a token (" << tokenOrError << "); the switch stays as set, and the sign-in runs when the network is up";
793				}
794			}
795			else if (!newState)
796				SystemConf::getInstance()->set("global.retroachievements.token", "");
797	
798			if (SystemConf::getInstance()->setBool("global.retroachievements", newState))
799				if (!ThreadedHasher::isRunning() && newState)
800					ThreadedHasher::start(window, ThreadedHasher::HASH_CHEEVOS_MD5, false, true);
801	
802			// After the switch is written: the check reads it, and one that ran
803			// before a switch just turned on would find it off and do nothing
804			// -- nor retry when the network comes up.
805			if (signIn == CheevosRetry::SaveSignIn::InBackground || signIn == CheevosRetry::SaveSignIn::Offline)
```

## The guest outputs (every input synthetic; no credential value: G9 counts synthetic strings)

### `p1-exit-sweep.sh`

```
#!/bin/bash
# M6 T30 (#677) guest proof P1: the exit sweep on the GENERIC_X64 guest.
# Each route is launched through /usr/bin/runemu.sh with the table's own
# arguments and a SYNTHETIC input (a junk file; blindspot 65: a substitute,
# not a game). Then: the kill data, the emulator's comm and exe, the cwd of
# the launch, the exact line input_sense's execute_kill runs (killall
# ${TO_KILL}, the hotkey's substitute), whether the emulator survived it,
# and cleanup by PID. Times from /proc/uptime (centiseconds).
. /etc/profile >/dev/null 2>&1
OUT=/storage/t30/p1
mkdir -p "$OUT"
up() { cut -d' ' -f1 /proc/uptime; }
desc() {  # all descendants of $1
  local root=$1 changed=1 set=" $1 "
  while [ $changed = 1 ]; do changed=0
    for s in /proc/[0-9]*/status; do
      p=${s#/proc/}; p=${p%/status}
      case "$set" in *" $p "*) continue ;; esac
      pp=$(awk '/^PPid:/{print $2}' "$s" 2>/dev/null)
      case "$set" in *" $pp "*) set="$set$p "; changed=1 ;; esac
    done
  done
  echo $set | tr ' ' '\n' | grep -v "^$root$"
}
emu_pids() {  # descendants whose exe is not a shell or a busybox applet
  for p in $(desc $1); do
    e=$(readlink /proc/$p/exe 2>/dev/null) || continue
    case "$e" in */bash|*/busybox|*/sh|*/python3*|*/sleep|*/gptokeyb*|*/control-gen*|*/xargs|*/sdljoytest*) continue ;; esac
    echo $p
  done
}
probe() {
  local label=$1 sys=$2 emu=$3 core=$4 rom=$5
  echo "=== $label sys=$sys emu=$emu core=$core input=$(basename "$rom") (synthetic)"
  rm -f /tmp/.process-kill-data
  t0=$(up)
  nohup /usr/bin/runemu.sh "$rom" -P$sys --core=$core --emulator=$emu --controllers="" >"$OUT/$label.runemu.out" 2>&1 &
  RP=$!
  first=""
  for i in $(seq 1 120); do
    e=$(emu_pids $RP | head -1)
    if [ -n "$e" ]; then first=$e; t1=$(up); break; fi
    kill -0 $RP 2>/dev/null || break
    sleep 0.1
  done
  sleep 4
  echo "kill-data: $(cat /tmp/.process-kill-data 2>/dev/null || echo '<absent>')"
  if [ -n "$first" ]; then
    echo "launch-to-process: $(awk -v a=$t0 -v b=$t1 'BEGIN{printf "%.2f", b-a}') s"
  else
    echo "launch-to-process: no emulator process within 12 s"
  fi
  for p in $(emu_pids $RP); do
    echo "proc pid=$p comm=$(cat /proc/$p/comm 2>/dev/null) exe=$(readlink /proc/$p/exe 2>/dev/null)"
  done
  for p in $RP $(desc $RP | head -3); do
    [ -d /proc/$p ] && echo "cwd pid=$p comm=$(cat /proc/$p/comm) cwd=$(readlink /proc/$p/cwd)"
  done
  before=$(emu_pids $RP | tr '\n' ' ')
  TO_KILL="$(cat /tmp/.process-kill-data 2>/dev/null)"
  if [ -n "$TO_KILL" ]; then
    k0=$(up); killall ${TO_KILL} 2>/dev/null; echo "killall ${TO_KILL}: rc=$?"
  else
    k0=$(up); echo "killall: nothing to kill (no kill data), as execute_kill"
  fi
  sleep 3
  after=""; for p in $before; do [ -d /proc/$p ] && after="$after$p "; done
  if [ -z "$before" ]; then echo "verdict: no emulator process to test"
  elif [ -z "$after" ]; then echo "verdict: the kill ended the emulator"
  else echo "verdict: the emulator SURVIVED the kill (pids $after)"; fi
  for i in $(seq 1 50); do kill -0 $RP 2>/dev/null || break; sleep 0.1; done
  kill -0 $RP 2>/dev/null && echo "runemu still running at kill+8 s" || echo "runemu ended at about kill+$(awk -v a=$k0 -v b=$(up) 'BEGIN{printf "%.1f", b-a}') s"
  # cleanup by PID: whatever is left of this launch
  for p in $(desc $RP) $RP; do kill -9 $p 2>/dev/null; done
  wait $RP 2>/dev/null
  echo "runemu tail: $(tail -3 "$OUT/$label.runemu.out" | tr '\n' '|' | cut -c1-300)"
  sleep 2
}
mk() { mkdir -p "$(dirname "$1")"; head -c ${2:-4096} /dev/urandom > "$1"; }
echo "P1 start uptime=$(up) build=$(grep ^BUILD_ID= /etc/os-release)"
mk /storage/roms/psx/t30-synthetic.cue 300
mk /storage/roms/psp/t30-synthetic.iso 65536
mk /storage/roms/dreamcast/t30-synthetic.gdi 300
mk /storage/roms/gamecube/t30-synthetic.iso 65536
mk /storage/roms/openbor/t30-synthetic.pak 4096
mk /storage/roms/c64/t30-synthetic.d64 174848
mk /storage/roms/n64/t30-synthetic.z64 65536
mk /storage/roms/ios/t30-synthetic.ipa 4096
mk /storage/roms/atarist/t30-synthetic.st 4096
mk /storage/roms/nds/t30-synthetic.nds 4096
mk /storage/roms/saturn/t30-synthetic.cue 300
mkdir -p /storage/roms/scummvm; printf -- '--path="/storage/roms/scummvm" t30-no-such-game\n' > /storage/roms/scummvm/t30-synthetic.scummvm
probe duckstation psx duckstation duckstation-sa /storage/roms/psx/t30-synthetic.cue
probe ppsspp psp ppsspp ppsspp-sa /storage/roms/psp/t30-synthetic.iso
probe flycast dreamcast flycast flycast-sa /storage/roms/dreamcast/t30-synthetic.gdi
probe dolphin-gc gamecube dolphin dolphin-sa-gc /storage/roms/gamecube/t30-synthetic.iso
probe dolphin-qt-gc gamecube dolphin dolphin-qt-gc /storage/roms/gamecube/t30-synthetic.iso
probe openbor openbor OpenBOR OpenBOR /storage/roms/openbor/t30-synthetic.pak
probe vice-x64sc c64 vicesa x64sc /storage/roms/c64/t30-synthetic.d64
probe mupen64plus n64 mupen64plus mupen64plus-sa /storage/roms/n64/t30-synthetic.z64
probe touchhle ios touchhle touchhle-sa /storage/roms/ios/t30-synthetic.ipa
probe scummvm scummvm scummvm-sa scummvm /storage/roms/scummvm/t30-synthetic.scummvm
probe hatarisa atarist hatarisa hatarisa /storage/roms/atarist/t30-synthetic.st
probe drastic-nds nds drastic drastic-sa /storage/roms/nds/t30-synthetic.nds
probe yabasanshiro saturn yabasanshiro yabasanshiro-sa /storage/roms/saturn/t30-synthetic.cue
echo "P1 end uptime=$(up)"

```

### `p1-exit-sweep.out`

```
P1 start uptime=128.62 build=BUILD_ID="069fc270442134fe771258418adf4e666e0473fb"
=== duckstation sys=psx emu=duckstation core=duckstation-sa input=t30-synthetic.cue (synthetic)
kill-data: -9 AppRun.wrapped
launch-to-process: 0.89 s
proc pid=3133 comm=AppRun exe=/tmp/.mount_ducksthMOdbO/usr/bin/duckstation-qt
cwd pid=2571 comm=runemu.sh cwd=/storage
cwd pid=2828 comm=bash cwd=/storage
cwd pid=3133 comm=AppRun cwd=/storage
killall -9 AppRun.wrapped: rc=1
verdict: the emulator SURVIVED the kill (pids 3133 )
runemu still running at kill+8 s
runemu tail: runemu.sh: /usr/bin/runemu.sh Configure big.little ()|runemu.sh: /usr/bin/runemu.sh Set emulation performance mode to ()|runemu.sh: /usr/bin/runemu.sh Executing /usr/bin/bash /usr/bin/start_duckstation.sh /storage/roms/psx/t30-synthetic.cue psx|
=== ppsspp sys=psp emu=ppsspp core=ppsspp-sa input=t30-synthetic.iso (synthetic)
kill-data: -9 ppsspp
launch-to-process: 0.67 s
proc pid=7460 comm=ppsspp exe=/usr/bin/ppsspp
cwd pid=6950 comm=runemu.sh cwd=/storage
cwd pid=7197 comm=bash cwd=/storage
cwd pid=7460 comm=ppsspp cwd=/storage
killall -9 ppsspp: rc=0
verdict: the kill ended the emulator
runemu ended at about kill+3.0 s
runemu tail: runemu.sh: /usr/bin/runemu.sh Enabling BT|runemu.sh: /usr/bin/runemu.sh Clearing screen|[H[J
=== flycast sys=dreamcast emu=flycast core=flycast-sa input=t30-synthetic.gdi (synthetic)
kill-data: emulationstation
launch-to-process: 0.64 s
killall emulationstation: rc=0
verdict: no emulator process to test
runemu ended at about kill+3.0 s
runemu tail: runemu.sh: /usr/bin/runemu.sh Enabling BT|runemu.sh: /usr/bin/runemu.sh Clearing screen|[H[J
=== dolphin-gc sys=gamecube emu=dolphin core=dolphin-sa-gc input=t30-synthetic.iso (synthetic)
kill-data: emulationstation
launch-to-process: 0.81 s
killall emulationstation: rc=0
verdict: no emulator process to test
runemu ended at about kill+3.0 s
runemu tail: runemu.sh: /usr/bin/runemu.sh Enabling BT|runemu.sh: /usr/bin/runemu.sh Clearing screen|[H[J
=== dolphin-qt-gc sys=gamecube emu=dolphin core=dolphin-qt-gc input=t30-synthetic.iso (synthetic)
kill-data: emulationstation
launch-to-process: no emulator process within 12 s
killall emulationstation: rc=0
verdict: no emulator process to test
runemu ended at about kill+3.0 s
runemu tail: runemu.sh: /usr/bin/runemu.sh Enabling BT|runemu.sh: /usr/bin/runemu.sh Clearing screen|[H[J
=== openbor sys=openbor emu=OpenBOR core=OpenBOR input=t30-synthetic.pak (synthetic)
kill-data: <absent>
launch-to-process: 0.64 s
proc pid=21178 comm=OpenBOR exe=/usr/bin/OpenBOR
cwd pid=20900 comm=runemu.sh cwd=/storage
cwd pid=21156 comm=bash cwd=/storage/openbor
cwd pid=21177 comm=gptokeyb cwd=/storage
cwd pid=21178 comm=OpenBOR cwd=/storage/openbor
killall: nothing to kill (no kill data), as execute_kill
verdict: the emulator SURVIVED the kill (pids 21178 )
runemu still running at kill+8 s
runemu tail: runemu.sh: /usr/bin/runemu.sh Configure big.little ()|runemu.sh: /usr/bin/runemu.sh Set emulation performance mode to ()|runemu.sh: /usr/bin/runemu.sh Executing /usr/bin/bash /usr/bin/start_OpenBOR.sh /storage/roms/openbor/t30-synthetic.pak openbor|
=== vice-x64sc sys=c64 emu=vicesa core=x64sc input=t30-synthetic.d64 (synthetic)
kill-data: -9 x64sc
launch-to-process: 0.61 s
proc pid=25455 comm=x64sc exe=/usr/bin/x64sc
cwd pid=25183 comm=runemu.sh cwd=/storage
cwd pid=25428 comm=bash cwd=/storage
cwd pid=25455 comm=x64sc cwd=/storage
killall -9 x64sc: rc=0
verdict: the kill ended the emulator
runemu ended at about kill+3.0 s
runemu tail: runemu.sh: /usr/bin/runemu.sh Enabling BT|runemu.sh: /usr/bin/runemu.sh Clearing screen|[H[J
=== mupen64plus sys=n64 emu=mupen64plus core=mupen64plus-sa input=t30-synthetic.z64 (synthetic)
kill-data: emulationstation
launch-to-process: no emulator process within 12 s
killall emulationstation: rc=0
verdict: no emulator process to test
runemu ended at about kill+3.0 s
runemu tail: runemu.sh: /usr/bin/runemu.sh Enabling BT|runemu.sh: /usr/bin/runemu.sh Clearing screen|[H[J
=== touchhle sys=ios emu=touchhle core=touchhle-sa input=t30-synthetic.ipa (synthetic)
kill-data: emulationstation
launch-to-process: no emulator process within 12 s
killall emulationstation: rc=0
verdict: no emulator process to test
runemu ended at about kill+3.0 s
runemu tail: runemu.sh: /usr/bin/runemu.sh Enabling BT|runemu.sh: /usr/bin/runemu.sh Clearing screen|[H[J
=== scummvm sys=scummvm emu=scummvm-sa core=scummvm input=t30-synthetic.scummvm (synthetic)
kill-data: emulationstation
launch-to-process: no emulator process within 12 s
killall emulationstation: rc=0
verdict: no emulator process to test
runemu ended at about kill+3.0 s
runemu tail: runemu.sh: /usr/bin/runemu.sh Enabling BT|runemu.sh: /usr/bin/runemu.sh Clearing screen|[H[J
=== hatarisa sys=atarist emu=hatarisa core=hatarisa input=t30-synthetic.st (synthetic)
kill-data: emulationstation
launch-to-process: no emulator process within 12 s
killall emulationstation: rc=0
verdict: no emulator process to test
runemu ended at about kill+3.0 s
runemu tail: runemu.sh: /usr/bin/runemu.sh Enabling BT|runemu.sh: /usr/bin/runemu.sh Clearing screen|[H[J
=== drastic-nds sys=nds emu=drastic core=drastic-sa input=t30-synthetic.nds (synthetic)
kill-data: emulationstation
launch-to-process: no emulator process within 12 s
killall emulationstation: rc=0
verdict: no emulator process to test
runemu ended at about kill+3.0 s
runemu tail: runemu.sh: /usr/bin/runemu.sh Enabling BT|runemu.sh: /usr/bin/runemu.sh Clearing screen|[H[J
=== yabasanshiro sys=saturn emu=yabasanshiro core=yabasanshiro-sa input=t30-synthetic.cue (synthetic)
kill-data: emulationstation
launch-to-process: no emulator process within 12 s
killall emulationstation: rc=0
verdict: no emulator process to test
runemu ended at about kill+3.0 s
runemu tail: runemu.sh: /usr/bin/runemu.sh Enabling BT|runemu.sh: /usr/bin/runemu.sh Clearing screen|[H[J
P1 end uptime=273.83

```

### `p2-cases.sh`

```
#!/bin/bash
# M6 T30 (#677) guest proof P2: the constructed cases. Every input is
# SYNTHETIC (blindspot 65) and named. RetroAchievements values are synthetic
# strings, counted with grep -c, never printed. The kill runs only while the
# emulator is alive (P1 killed the interface where the emulator had already
# exited: a fixture fault, fixed here).
. /etc/profile >/dev/null 2>&1
OUT=/storage/t30/p2; mkdir -p "$OUT"
up() { cut -d' ' -f1 /proc/uptime; }
desc() { local root=$1 changed=1 set=" $1 "
  while [ $changed = 1 ]; do changed=0
    for s in /proc/[0-9]*/status; do p=${s#/proc/}; p=${p%/status}
      case "$set" in *" $p "*) continue ;; esac
      pp=$(awk '/^PPid:/{print $2}' "$s" 2>/dev/null)
      case "$set" in *" $pp "*) set="$set$p "; changed=1 ;; esac
    done; done; echo $set | tr ' ' '\n' | grep -v "^$root$"; }
emu_pids() { for p in $(desc $1); do e=$(readlink /proc/$p/exe 2>/dev/null) || continue
    case "$e" in */bash|*/busybox|*/sh|*/python3*|*/gptokeyb*|*/control-gen*|*/xargs|*/sdljoytest*) continue ;; esac; echo $p; done; }
launch() {  # label sys emu core rom [seconds]
  local label=$1 sys=$2 emu=$3 core=$4 rom=$5 wait=${6:-5}
  echo "=== $label sys=$sys emu=$emu core=$core input=$(basename "$rom") (synthetic)"
  rm -f /tmp/.process-kill-data
  t0=$(up); nohup /usr/bin/runemu.sh "$rom" -P$sys --core=$core --emulator=$emu --controllers="" >"$OUT/$label.runemu.out" 2>&1 &
  RP=$!; first=""
  for i in $(seq 1 100); do e=$(emu_pids $RP | head -1); [ -n "$e" ] && { first=$e; t1=$(up); break; }; kill -0 $RP 2>/dev/null || break; sleep 0.1; done
  [ -n "$first" ] && echo "launch-to-process: $(awk -v a=$t0 -v b=$t1 'BEGIN{printf "%.2f", b-a}') s comm=$(cat /proc/$first/comm 2>/dev/null) exe=$(readlink /proc/$first/exe 2>/dev/null)" || echo "launch-to-process: none"
  sleep $wait
}
finish() {  # kill only a live emulator; then clean up by PID; keep exec.log
  local label=$1 alive=$(emu_pids $RP | tr '\n' ' ')
  echo "kill-data: $(cat /tmp/.process-kill-data 2>/dev/null || echo '<absent>') | emulator alive: ${alive:-none}"
  for p in $(desc $RP) $RP; do kill -9 $p 2>/dev/null; done; wait $RP 2>/dev/null; echo "runemu rc=$?"
  cp /var/log/exec.log "$OUT/$label.exec.log" 2>/dev/null
  grep -E 'No such file|Executing|exiting with|rror|not found|Unable|unmatched' "$OUT/$label.exec.log" | sed -E 's/((token|key|passw[a-z]*|psk|user)[=:])[^ ]*/\1***/Ig' | head -6 | sed 's/^/  log: /'
  sleep 2
}
mk() { mkdir -p "$(dirname "$1")"; head -c ${2:-4096} /dev/urandom > "$1"; }
echo "P2 start uptime=$(up) build=$(grep ^BUILD_ID= /etc/os-release)"

echo "##### C1 the routes the table offers with no script (atarist hatarisa default? no; nds drastic default; saturn in P1)"
launch hatarisa atarist hatarisa hatarisa /storage/roms/atarist/t30-synthetic.st 2; finish hatarisa
launch drastic-nds nds drastic drastic-sa /storage/roms/nds/t30-synthetic.nds 2; finish drastic-nds
mk /storage/roms/amiga/t30-synthetic.adf 4096
launch amiberry amiga amiberry amiberry /storage/roms/amiga/t30-synthetic.adf 2; finish amiberry

echo "##### C2 start_scummvm.sh's eval: a crafted .scummvm (control first: a plain file)"
rm -f /tmp/t30-svm-injected
printf -- '--path="/storage/roms/scummvm" t30-no-such-game\n' > /storage/roms/scummvm/t30-control.scummvm
launch scummvm-control scummvm scummvm-sa scummvm /storage/roms/scummvm/t30-control.scummvm 3; finish scummvm-control
echo "control marker: $( [ -e /tmp/t30-svm-injected ] && echo PRESENT || echo absent)"
printf -- '--path="/storage/roms/scummvm" t30-no-such-game; touch /tmp/t30-svm-injected\n' > /storage/roms/scummvm/t30-crafted.scummvm
launch scummvm-crafted scummvm scummvm-sa scummvm /storage/roms/scummvm/t30-crafted.scummvm 3; finish scummvm-crafted
echo "crafted marker: $( [ -e /tmp/t30-svm-injected ] && echo "PRESENT (owner $(stat -c %U /tmp/t30-svm-injected))" || echo absent)"

echo "##### C3 start_gzdoom.sh's xargs: an apostrophe in the WAD's name (control: none)"
mk "/storage/roms/doom/t30 control.wad" 4096
launch gzdoom-control doom gzdoom gzdoom-sa "/storage/roms/doom/t30 control.wad" 2; finish gzdoom-control
grep -c . /var/log/gzdoom.log >/dev/null 2>&1; echo "control gzdoom.log: $(head -c 300 /var/log/gzdoom.log 2>/dev/null | tr '\n' '|' )"
mk "/storage/roms/doom/t30 Hell's Gate.wad" 4096
launch gzdoom-apostrophe doom gzdoom gzdoom-sa "/storage/roms/doom/t30 Hell's Gate.wad" 2; finish gzdoom-apostrophe
echo "apostrophe gzdoom.log: $(head -c 300 /var/log/gzdoom.log 2>/dev/null | tr '\n' '|' )"

echo "##### C4 start_mupen64plus.sh: a zipped ROM under busybox unzip (control: the same ROM unzipped, in P1)"
cd /tmp && rm -rf t30z && mkdir t30z && head -c 65536 /dev/urandom > t30z/t30-zipped.z64 && (cd t30z && zip -q /storage/roms/n64/t30-zipped.zip t30-zipped.z64 2>/dev/null || echo "no zip applet"); cd /storage
ls -la /storage/roms/n64/t30-zipped.zip 2>&1 | sed 's/^/  /'
unzip -Zl -1 /storage/roms/n64/t30-zipped.zip >/dev/null 2>&1; echo "unzip -Zl -1 rc=$? (busybox: $(readlink -f $(command -v unzip)))"
echo "unzip -qql first entry: $(unzip -qql /storage/roms/n64/t30-zipped.zip 2>/dev/null | head -n1 | cut -c31-)"
launch mupen-zip n64 mupen64plus mupen64plus-sa /storage/roms/n64/t30-zipped.zip 2; finish mupen-zip
grep -n -E 'mupen64plus(-simple)? --configdir' "$OUT/mupen-zip.exec.log" "$OUT/mupen-zip.runemu.out" 2>/dev/null | tail -1 | sed -E 's/.*(\/tmp\/mupen64plus\/[^ ]*)"?$/  rom argument: \1/'
grep -o '"/tmp/mupen64plus/[^"]*"\|/tmp/mupen64plus/[^ ]*$' "$OUT/mupen-zip.exec.log" | tail -2 | sed 's/^/  path: /'

echo "##### C5 busybox killall against long and suffixed names (substitutes: copies of a real ELF, python3, renamed)"
mkdir -p /tmp/t30k; for n in dolphin-emu-nogui mupen64plus-simple duckstation-qt; do cp /usr/bin/python3 /tmp/t30k/$n; done
for pair in "dolphin-emu-nogui dolphin-emu-nogui" "mupen64plus-simple mupen64plus" "mupen64plus-simple mupen64plus-simple"; do
  set -- $pair; /tmp/t30k/$1 -c 'import time; time.sleep(30)' & K=$!; sleep 0.5
  echo "running $1 as pid $K comm=$(cat /proc/$K/comm)"; killall -9 $2 2>/dev/null; echo "killall -9 $2 rc=$?"; sleep 0.5
  [ -d /proc/$K ] && { echo "  -> $1 SURVIVED killall $2"; kill -9 $K; } || echo "  -> $1 ended by killall $2"; wait $K 2>/dev/null
done

echo "##### C6 the real DuckStation AppImage: AppRun.wrapped against duckstation-qt"
for target in AppRun.wrapped duckstation-qt; do
  launch duck-$target psx duckstation duckstation-sa /storage/roms/psx/t30-synthetic.cue 4
  alive=$(emu_pids $RP | head -1)
  if [ -n "$alive" ]; then killall -9 $target 2>/dev/null; echo "killall -9 $target rc=$?"; sleep 2
    [ -d /proc/$alive ] && echo "  -> pid $alive SURVIVED killall -9 $target" || echo "  -> pid $alive ended by killall -9 $target"
  fi; finish duck-$target
done

echo "##### C7 the memory cards: CONF_DIR/memcards a real directory (control: the target absent)"
C=/storage/.config/duckstation; M=/storage/roms/psx/duckstation/memcards
echo "before: $(ls -ld $C/memcards | cut -c1-60) | target $( [ -d $M ] && echo exists || echo absent)"
mv $M /storage/t30/memcards-target-aside 2>/dev/null; rm -f $C/memcards; mkdir -p $C/memcards; printf 'T30-CONTROL-CARD' > $C/memcards/t30-control.mcd
launch memcard-control psx duckstation duckstation-sa /storage/roms/psx/t30-synthetic.cue 2; finish memcard-control
echo "control (target absent): $(find /storage -name t30-control.mcd 2>/dev/null | tr '\n' ' ') | memcards $(ls -ld $C/memcards | cut -c1-12)"
rm -f $C/memcards; mkdir -p $C/memcards; printf 'T30-CONSTRUCTED-CARD' > $C/memcards/t30-constructed.mcd; mkdir -p $M
echo "constructed: target $( [ -d $M ] && echo exists ), real dir with $(ls $C/memcards | wc -l) card"
launch memcard-constructed psx duckstation duckstation-sa /storage/roms/psx/t30-synthetic.cue 2; finish memcard-constructed
echo "after constructed: copies of t30-constructed.mcd on /storage: $(find /storage -name t30-constructed.mcd 2>/dev/null | wc -l) | memcards $(ls -ld $C/memcards | cut -c1-12)"

echo "##### C8 the RetroAchievements session on 'on, token empty' (synthetic values; counts only)"
for k in global.retroachievements global.retroachievements.token global.retroachievements.username; do echo "was-set $k: $( [ -n "$(get_setting $k)" ] && echo yes || echo no)"; done
set_setting global.retroachievements 1; set_setting global.retroachievements.username t30synthetic; del_setting global.retroachievements.token 2>/dev/null || set_setting global.retroachievements.token ""
echo "state: switch=$(get_setting global.retroachievements) token-empty=$( [ -z "$(get_setting global.retroachievements.token)" ] && echo yes || echo no)"
PI=/storage/.config/ppsspp/PSP/SYSTEM; mkdir -p $PI; printf 'T30-SYNTHETIC-OLD\n' > $PI/ppsspp_retroachievements.dat; grep -q '^AchievementsEnable' $PI/ppsspp.ini 2>/dev/null && sed -i '/^AchievementsEnable =/c\AchievementsEnable = True' $PI/ppsspp.ini || printf '[Achievements]\nAchievementsEnable = True\n' >> $PI/ppsspp.ini
/usr/bin/cheevos_ppsspp.sh >/dev/null 2>&1; echo "ppsspp: rc=$? old-token-lines=$(grep -c T30-SYNTHETIC-OLD $PI/ppsspp_retroachievements.dat) $(grep '^AchievementsEnable' $PI/ppsspp.ini)"
FC=/storage/.config/flycast/emu.cfg; mkdir -p ${FC%/*}; grep -q '^\[achievements\]' $FC 2>/dev/null || printf '\n[achievements]\nEnabled = yes\nToken = x\n' >> $FC; sed -i '/^\[achievements\]/,/^\[/{s/^Token = .*/Token = T30-SYNTHETIC-OLD/;s/^Enabled = .*/Enabled = yes/}' $FC
/usr/bin/cheevos_flycast.sh >/dev/null 2>&1; echo "flycast: rc=$? old-token-lines=$(grep -c T30-SYNTHETIC-OLD $FC) $(sed -n '/^\[achievements\]/,/^\[/p' $FC | grep '^Enabled')"
DI=/storage/.config/dolphin-emu/RetroAchievements.ini; mkdir -p ${DI%/*}; printf '[Achievements]\nEnabled = True\nApiToken = T30-SYNTHETIC-OLD\n' > $DI
/usr/bin/cheevos_dolphin.sh >/dev/null 2>&1; echo "dolphin (control): rc=$? old-token-lines=$(grep -c T30-SYNTHETIC-OLD $DI) $(grep '^Enabled' $DI)"
echo "unquoted test, key unset: flycast's [ ! \${enabled} = 1 ] with enabled empty -> $(enabled=''; [ ! ${enabled} = 1 ] && echo 'disabled branch' || echo 'falls through as enabled')"
del_setting global.retroachievements 2>/dev/null; del_setting global.retroachievements.username 2>/dev/null
for k in global.retroachievements global.retroachievements.username; do echo "restored $k: $( [ -n "$(get_setting $k)" ] && echo still-set || echo unset)"; done

echo "##### C9 a comparison written as a redirection, in the interface's cwd (/storage), with the image's bash"
cd /storage; rm -f /storage/0; IRES=2; [ "$IRES" > "0" ] && echo "[ \"\$IRES\" > \"0\" ] with IRES=2: true"; IRES=; [ "$IRES" > "0" ] && echo "with IRES empty: true" || echo "with IRES empty: false"; ls -la /storage/0 2>&1 | cut -c1-60; rm -f /storage/0

echo "##### C10 the Python helpers on the launch path (n=5 each)"
for i in 1 2 3 4 5; do a=$(up); /usr/bin/python3 -I -S -B /usr/bin/dolphin-save-paths check gamecube >/dev/null 2>&1; r=$?; b=$(up); /usr/bin/duckstation_screenshot_path /storage/.config/duckstation/settings.ini >/dev/null 2>&1; c=$(up); echo "dolphin-save-paths check rc=$r $(awk -v a=$a -v b=$b 'BEGIN{printf "%.2f", b-a}') s | duckstation_screenshot_path $(awk -v a=$b -v b=$c 'BEGIN{printf "%.2f", b-a}') s"; done
a=$(up); sha256sum /usr/config/gzdoom/gzdoom.pk3 >/dev/null; b=$(up); echo "gzdoom.pk3 one sha256: $(awk -v a=$a -v b=$b 'BEGIN{printf "%.2f", b-a}') s, size $(stat -c %s /usr/config/gzdoom/gzdoom.pk3)"

echo "##### C11 launch-to-process n=3 (the emulators that stay up on a synthetic input)"
for n in 1 2 3; do
  launch ttp-ppsspp-$n psp ppsspp ppsspp-sa /storage/roms/psp/t30-synthetic.iso 1; finish ttp-ppsspp-$n
  launch ttp-vice-$n c64 vicesa x64sc /storage/roms/c64/t30-synthetic.d64 1; finish ttp-vice-$n
  launch ttp-duck-$n psx duckstation duckstation-sa /storage/roms/psx/t30-synthetic.cue 1; finish ttp-duck-$n
done
mv /storage/t30/memcards-target-aside/* /storage/roms/psx/duckstation/memcards/ 2>/dev/null
echo "P2 end uptime=$(up); interface pid $(pidof emulationstation)"

```

### `p2-cases.out`

```
P2 start uptime=410.53 build=BUILD_ID="069fc270442134fe771258418adf4e666e0473fb"
##### C1 the routes the table offers with no script (atarist hatarisa default? no; nds drastic default; saturn in P1)
=== hatarisa sys=atarist emu=hatarisa core=hatarisa input=t30-synthetic.st (synthetic)
launch-to-process: none
kill-data: emulationstation | emulator alive: none
runemu rc=1
  log: runemu.sh: /usr/bin/runemu.sh Executing /usr/bin/bash /usr/bin/start_hatarisa.sh /storage/roms/atarist/t30-synthetic.st atarist
  log: /usr/bin/bash: /usr/bin/start_hatarisa.sh: No such file or directory
  log: runemu.sh: /usr/bin/runemu.sh Checking errors: 127 
  log: runemu.sh: /usr/bin/runemu.sh exiting with 127
=== drastic-nds sys=nds emu=drastic core=drastic-sa input=t30-synthetic.nds (synthetic)
launch-to-process: none
kill-data: emulationstation | emulator alive: none
runemu rc=1
  log: runemu.sh: /usr/bin/runemu.sh Executing /usr/bin/bash /usr/bin/start_drastic.sh /storage/roms/nds/t30-synthetic.nds nds
  log: /usr/bin/bash: /usr/bin/start_drastic.sh: No such file or directory
  log: runemu.sh: /usr/bin/runemu.sh Checking errors: 127 
  log: runemu.sh: /usr/bin/runemu.sh exiting with 127
=== amiberry sys=amiga emu=amiberry core=amiberry input=t30-synthetic.adf (synthetic)
launch-to-process: none
kill-data: emulationstation | emulator alive: none
runemu rc=1
  log: runemu.sh: /usr/bin/runemu.sh Executing /usr/bin/bash /usr/bin/start_amiberry.sh /storage/roms/amiga/t30-synthetic.adf amiga
  log: /usr/bin/bash: /usr/bin/start_amiberry.sh: No such file or directory
  log: runemu.sh: /usr/bin/runemu.sh Checking errors: 127 
  log: runemu.sh: /usr/bin/runemu.sh exiting with 127
##### C2 start_scummvm.sh's eval: a crafted .scummvm (control first: a plain file)
=== scummvm-control sys=scummvm emu=scummvm-sa core=scummvm input=t30-control.scummvm (synthetic)
launch-to-process: none
kill-data: emulationstation | emulator alive: none
runemu rc=0
  log: runemu.sh: /usr/bin/runemu.sh Executing /usr/bin/bash /usr/bin/start_scummvm.sh /storage/roms/scummvm/t30-control.scummvm scummvm
  log: runemu.sh: /usr/bin/runemu.sh Checking errors: 0 
control marker: absent
=== scummvm-crafted sys=scummvm emu=scummvm-sa core=scummvm input=t30-crafted.scummvm (synthetic)
launch-to-process: none
kill-data: emulationstation | emulator alive: none
runemu rc=0
  log: runemu.sh: /usr/bin/runemu.sh Executing /usr/bin/bash /usr/bin/start_scummvm.sh /storage/roms/scummvm/t30-crafted.scummvm scummvm
  log: runemu.sh: /usr/bin/runemu.sh Checking errors: 0 
crafted marker: PRESENT (owner root)
##### C3 start_gzdoom.sh's xargs: an apostrophe in the WAD's name (control: none)
=== gzdoom-control sys=doom emu=gzdoom core=gzdoom-sa input=t30 control.wad (synthetic)
launch-to-process: none
kill-data: emulationstation | emulator alive: none
runemu rc=1
  log: runemu.sh: /usr/bin/runemu.sh Executing /usr/bin/bash /usr/bin/start_gzdoom.sh /storage/roms/doom/t30 control.wad doom
  log: runemu.sh: /usr/bin/runemu.sh Checking errors: 124 
  log: runemu.sh: /usr/bin/runemu.sh exiting with 124
control gzdoom.log: GZDoom rc1-20260929-185-gb137d8c373 - 2026-10-04 03:15:26 +0000 - SDL version|Compiled on Oct  4 2026||OS: pixelelated 0.0.1-dev, Linux 7.1.2 on x86_64|GZDoom version rc1-20260929-185-gb137d8c373||Cannot find a game IWAD (doom.wad, doom2.wad, heretic.wad, etc.).|Did you install GZDoom properly? You 
=== gzdoom-apostrophe sys=doom emu=gzdoom core=gzdoom-sa input=t30 Hell's Gate.wad (synthetic)
launch-to-process: none
kill-data: emulationstation | emulator alive: none
runemu rc=1
  log: runemu.sh: /usr/bin/runemu.sh Executing /usr/bin/bash /usr/bin/start_gzdoom.sh /storage/roms/doom/t30 Hell's Gate.wad doom
  log: runemu.sh: /usr/bin/runemu.sh Checking errors: 1 
  log: runemu.sh: /usr/bin/runemu.sh exiting with 1
apostrophe gzdoom.log: xargs: unmatched single quote|
##### C4 start_mupen64plus.sh: a zipped ROM under busybox unzip (control: the same ROM unzipped, in P1)
  -rw-r--r--    1 root     root         65724 Oct 24 04:59 /storage/roms/n64/t30-zipped.zip
unzip -Zl -1 rc=1 (busybox: /usr/bin/busybox)
unzip -qql first entry: t30-zipped.z64
=== mupen-zip sys=n64 emu=mupen64plus core=mupen64plus-sa input=t30-zipped.zip (synthetic)
launch-to-process: none
kill-data: emulationstation | emulator alive: none
runemu rc=1
  log: runemu.sh: /usr/bin/runemu.sh Executing /usr/bin/bash /usr/bin/start_mupen64plus.sh /storage/roms/n64/t30-zipped.zip n64
  log: UI-Console Error: core failed to open ROM image file '/tmp/mupen64plus/'.
  log: runemu.sh: /usr/bin/runemu.sh Checking errors: 10 
  log: runemu.sh: /usr/bin/runemu.sh exiting with 10
  path: /tmp/mupen64plus/'.
##### C5 busybox killall against long and suffixed names (substitutes: copies of a real ELF, python3, renamed)
running dolphin-emu-nogui as pid 53773 comm=dolphin-emu-nog
killall -9 dolphin-emu-nogui rc=0
  -> dolphin-emu-nogui ended by killall dolphin-emu-nogui
running mupen64plus-simple as pid 53778 comm=mupen64plus-sim
killall -9 mupen64plus rc=1
  -> mupen64plus-simple SURVIVED killall mupen64plus
running mupen64plus-simple as pid 53790 comm=mupen64plus-sim
killall -9 mupen64plus-simple rc=0
  -> mupen64plus-simple ended by killall mupen64plus-simple
##### C6 the real DuckStation AppImage: AppRun.wrapped against duckstation-qt
=== duck-AppRun.wrapped sys=psx emu=duckstation core=duckstation-sa input=t30-synthetic.cue (synthetic)
launch-to-process: 0.71 s comm=AppRun exe=/tmp/.mount_duckstPlKMmP/usr/bin/duckstation-qt
killall -9 AppRun.wrapped rc=1
  -> pid 54308 SURVIVED killall -9 AppRun.wrapped
kill-data: -9 AppRun.wrapped | emulator alive: 54308 
runemu rc=137
  log: runemu.sh: /usr/bin/runemu.sh Executing /usr/bin/bash /usr/bin/start_duckstation.sh /storage/roms/psx/t30-synthetic.cue psx
=== duck-duckstation-qt sys=psx emu=duckstation core=duckstation-sa input=t30-synthetic.cue (synthetic)
launch-to-process: 0.61 s comm=AppRun exe=/tmp/.mount_duckstepJkAa/usr/bin/duckstation-qt
killall -9 duckstation-qt rc=0
  -> pid 57749 ended by killall -9 duckstation-qt
kill-data: emulationstation | emulator alive: none
runemu rc=0
  log: runemu.sh: /usr/bin/runemu.sh Executing /usr/bin/bash /usr/bin/start_duckstation.sh /storage/roms/psx/t30-synthetic.cue psx
  log: runemu.sh: /usr/bin/runemu.sh Checking errors: 137 
##### C7 the memory cards: CONF_DIR/memcards a real directory (control: the target absent)
before: lrwxrwxrwx    1 root     root            38 Oct 24 04:59 /st | target exists
=== memcard-control sys=psx emu=duckstation core=duckstation-sa input=t30-synthetic.cue (synthetic)
launch-to-process: 0.62 s comm=AppRun exe=/tmp/.mount_duckstGjlFpo/usr/bin/duckstation-qt
kill-data: -9 AppRun.wrapped | emulator alive: 60558 
runemu rc=137
  log: runemu.sh: /usr/bin/runemu.sh Executing /usr/bin/bash /usr/bin/start_duckstation.sh /storage/roms/psx/t30-synthetic.cue psx
control (target absent): /storage/roms/psx/duckstation/memcards/t30-control.mcd /storage/games-internal/roms/psx/duckstation/memcards/t30-control.mcd  | memcards lrwxrwxrwx  
constructed: target exists, real dir with 1 card
=== memcard-constructed sys=psx emu=duckstation core=duckstation-sa input=t30-synthetic.cue (synthetic)
launch-to-process: 0.60 s comm=AppRun exe=/tmp/.mount_duckstIOEEgO/usr/bin/duckstation-qt
kill-data: -9 AppRun.wrapped | emulator alive: 63291 
runemu rc=137
  log: runemu.sh: /usr/bin/runemu.sh Executing /usr/bin/bash /usr/bin/start_duckstation.sh /storage/roms/psx/t30-synthetic.cue psx
after constructed: copies of t30-constructed.mcd on /storage: 0 | memcards lrwxrwxrwx  
##### C8 the RetroAchievements session on 'on, token empty' (synthetic values; counts only)
was-set global.retroachievements: yes
was-set global.retroachievements.token: no
was-set global.retroachievements.username: no
state: switch=1 token-empty=yes
ppsspp: rc=1 old-token-lines=1 AchievementsEnable = True
flycast: rc=1 old-token-lines=1 Enabled = yes
dolphin (control): rc=1 old-token-lines=0 Enabled = False
unquoted test, key unset: flycast's [ ! ${enabled} = 1 ] with enabled empty -> falls through as enabled
restored global.retroachievements: unset
restored global.retroachievements.username: unset
##### C9 a comparison written as a redirection, in the interface's cwd (/storage), with the image's bash
[ "$IRES" > "0" ] with IRES=2: true
with IRES empty: false
-rw-r--r--    1 root     root             0 Oct 24 04:59 /st
##### C10 the Python helpers on the launch path (n=5 each)
dolphin-save-paths check rc=0 0.05 s | duckstation_screenshot_path 0.07 s
dolphin-save-paths check rc=0 0.04 s | duckstation_screenshot_path 0.04 s
dolphin-save-paths check rc=0 0.04 s | duckstation_screenshot_path 0.05 s
dolphin-save-paths check rc=0 0.03 s | duckstation_screenshot_path 0.04 s
dolphin-save-paths check rc=0 0.04 s | duckstation_screenshot_path 0.04 s
gzdoom.pk3 one sha256: 0.02 s, size 3124583
##### C11 launch-to-process n=3 (the emulators that stay up on a synthetic input)
=== ttp-ppsspp-1 sys=psp emu=ppsspp core=ppsspp-sa input=t30-synthetic.iso (synthetic)
launch-to-process: 0.61 s comm=ppsspp exe=/usr/bin/ppsspp
kill-data: -9 ppsspp | emulator alive: 66265 
runemu rc=137
  log: runemu.sh: /usr/bin/runemu.sh Executing /usr/bin/bash /usr/bin/start_ppsspp.sh /storage/roms/psp/t30-synthetic.iso psp
  log: 59:50:900 Vulkan/VulkanLoader.cpp:548 E[G3D]: Surface extension not found
=== ttp-vice-1 sys=c64 emu=vicesa core=x64sc input=t30-synthetic.d64 (synthetic)
launch-to-process: 0.62 s comm=x64sc exe=/usr/bin/x64sc
kill-data: -9 x64sc | emulator alive: 68765 
runemu rc=137
  log: runemu.sh: /usr/bin/runemu.sh Executing /usr/bin/bash /usr/bin/start_x64sc.sh /storage/roms/c64/t30-synthetic.d64 c64
  log: DriveROM: Error - 2000 ROM image not found. Hardware-level 2000 emulation is not available.
  log: DriveROM: Error - 4000 ROM image not found. Hardware-level 4000 emulation is not available.
  log: DriveROM: Error - CMDHD ROM image not found. Hardware-level CMDHD emulation is not available.
  log: AUTOSTART: Error - Turned off.
  log: AUTOSTART: Error
=== ttp-duck-1 sys=psx emu=duckstation core=duckstation-sa input=t30-synthetic.cue (synthetic)
launch-to-process: 0.62 s comm=AppRun exe=/tmp/.mount_duckstKGgNhd/usr/bin/duckstation-qt
kill-data: -9 AppRun.wrapped | emulator alive: 71651 
runemu rc=137
  log: runemu.sh: /usr/bin/runemu.sh Executing /usr/bin/bash /usr/bin/start_duckstation.sh /storage/roms/psx/t30-synthetic.cue psx
=== ttp-ppsspp-2 sys=psp emu=ppsspp core=ppsspp-sa input=t30-synthetic.iso (synthetic)
launch-to-process: 0.63 s comm=ppsspp exe=/usr/bin/ppsspp
kill-data: -9 ppsspp | emulator alive: 74333 
runemu rc=137
  log: runemu.sh: /usr/bin/runemu.sh Executing /usr/bin/bash /usr/bin/start_ppsspp.sh /storage/roms/psp/t30-synthetic.iso psp
  log: 00:03:919 Vulkan/VulkanLoader.cpp:548 E[G3D]: Surface extension not found
=== ttp-vice-2 sys=c64 emu=vicesa core=x64sc input=t30-synthetic.d64 (synthetic)
launch-to-process: 0.67 s comm=x64sc exe=/usr/bin/x64sc
kill-data: -9 x64sc | emulator alive: 76834 
runemu rc=137
  log: runemu.sh: /usr/bin/runemu.sh Executing /usr/bin/bash /usr/bin/start_x64sc.sh /storage/roms/c64/t30-synthetic.d64 c64
  log: DriveROM: Error - 2000 ROM image not found. Hardware-level 2000 emulation is not available.
  log: DriveROM: Error - 4000 ROM image not found. Hardware-level 4000 emulation is not available.
  log: DriveROM: Error - CMDHD ROM image not found. Hardware-level CMDHD emulation is not available.
  log: AUTOSTART: Error - Turned off.
  log: AUTOSTART: Error
=== ttp-duck-2 sys=psx emu=duckstation core=duckstation-sa input=t30-synthetic.cue (synthetic)
launch-to-process: 0.53 s comm=AppRun exe=/tmp/.mount_duckstPCaifC/usr/bin/duckstation-qt
kill-data: -9 AppRun.wrapped | emulator alive: 79685 
runemu rc=137
  log: runemu.sh: /usr/bin/runemu.sh Executing /usr/bin/bash /usr/bin/start_duckstation.sh /storage/roms/psx/t30-synthetic.cue psx
=== ttp-ppsspp-3 sys=psp emu=ppsspp core=ppsspp-sa input=t30-synthetic.iso (synthetic)
launch-to-process: 0.63 s comm=ppsspp exe=/usr/bin/ppsspp
kill-data: -9 ppsspp | emulator alive: 82381 
runemu rc=137
  log: runemu.sh: /usr/bin/runemu.sh Executing /usr/bin/bash /usr/bin/start_ppsspp.sh /storage/roms/psp/t30-synthetic.iso psp
  log: 00:16:708 Vulkan/VulkanLoader.cpp:548 E[G3D]: Surface extension not found
=== ttp-vice-3 sys=c64 emu=vicesa core=x64sc input=t30-synthetic.d64 (synthetic)
launch-to-process: 0.56 s comm=x64sc exe=/usr/bin/x64sc
kill-data: -9 x64sc | emulator alive: 84881 
runemu rc=137
  log: runemu.sh: /usr/bin/runemu.sh Executing /usr/bin/bash /usr/bin/start_x64sc.sh /storage/roms/c64/t30-synthetic.d64 c64
  log: DriveROM: Error - 2000 ROM image not found. Hardware-level 2000 emulation is not available.
  log: DriveROM: Error - 4000 ROM image not found. Hardware-level 4000 emulation is not available.
  log: DriveROM: Error - CMDHD ROM image not found. Hardware-level CMDHD emulation is not available.
  log: AUTOSTART: Error - Turned off.
  log: AUTOSTART: Error
=== ttp-duck-3 sys=psx emu=duckstation core=duckstation-sa input=t30-synthetic.cue (synthetic)
launch-to-process: 0.52 s comm=AppRun exe=/tmp/.mount_duckstikhijI/usr/bin/duckstation-qt
kill-data: -9 AppRun.wrapped | emulator alive: 87772 
runemu rc=137
  log: runemu.sh: /usr/bin/runemu.sh Executing /usr/bin/bash /usr/bin/start_duckstation.sh /storage/roms/psx/t30-synthetic.cue psx
P2 end uptime=520.62; interface pid 42194

```

## 00-running-log.md (the proof lines)

```
PROOF: 08:35:40 UTC (the arm64 copy's mtime; the listing followed it) -- H1, the DuckStation AppImages listed (the x64 and arm64 copies from the M7 trees, sha256 = the recipe's two PKG_SHA256; unsquashfs -o 696608 / 667904 -l): AppRun -> usr/bin/duckstation-qt, no AppRun.wrapped in either; /workspace/tmp/m6-t30/duck/
PROOF: 08:38:37 UTC (run in the same command as H3; H3's file mtime) -- H2, start_amiberry.sh:70-71's substitution on a fixture line: gfx_width=720 becomes a bare 640 (the key deleted)
PROOF: 08:38:37 UTC (bbbb1111's mtime) -- H3, start_daedalusx64.sh:48's shape: bash -c '[ "$0" <> "$1" ] && echo "test true"' aaaa bbbb1111 in an empty directory printed "test true" and created a file named bbbb1111; /workspace/tmp/m6-t30/fx/daed
PROOF: 08:25:55 UTC (start-cmp.txt's mtime) -- H4, the three install trees' 40 start scripts against the hash by cmp: 16 differing pairs, every changed source line an @NAME@ placeholder, no add/delete hunk; control: a real edit is reported (.qa-scratch/t30/checks/start-cmp.txt)
PROOF: 08:28:16 UTC (routes.json's mtime) -- H5, tools/t30-routes.py over the three images' tables: GENERIC_X64 37 routes (11 no script), H700 72 (5), SM8550 145 (6); fail-closed control rc 1 (.qa-scratch/t30/routes.json)
GUEST-PROOF: 08:56:22 UTC (p1-exit-sweep.out's mtime) -- G1, P1 the exit sweep through runemu.sh (synthetic inputs): DuckStation kill-data "-9 AppRun.wrapped", process comm AppRun exe .../usr/bin/duckstation-qt, killall rc 1, SURVIVED; OpenBOR no kill data, SURVIVED; ppsspp and x64sc ended by their kill; flycast and dolphin started (0.64 s, 0.81 s) and exited on the synthetic input before the sample, so their kill names were not tested live; /workspace/artifacts/m6-t30-20261024/p1-exit-sweep.sh, /workspace/artifacts/m6-t30-20261024/p1-exit-sweep.out
GUEST-PROOF: 09:00:29 UTC (p2-cases.out's mtime) -- G2, P2 C1 and P1: the table's hatarisa (atarist), drastic-sa (nds, the default) and amiberry (amiga) routes and P1's yabasanshiro-sa (saturn, the default): "No such file or directory", runemu exit 127; /workspace/artifacts/m6-t30-20261024/p2-cases.sh, /workspace/artifacts/m6-t30-20261024/p2-cases.out, exec logs in /workspace/artifacts/m6-t30-20261024/t30/p2/
GUEST-PROOF: 09:00:29 UTC (p2-cases.out's mtime) -- G3, P2 C2: a .scummvm holding '--path="..." id; touch /tmp/t30-svm-injected' (crafted, synthetic) launched through runemu.sh left /tmp/t30-svm-injected owned by root; the plain control file left none
GUEST-PROOF: 09:00:29 UTC (p2-cases.out's mtime) -- G4, P2 C3: a WAD named "t30 Hell's Gate.wad" (synthetic): gzdoom.log "xargs: unmatched single quote", gzdoom never started, runemu exit 1; control "t30 control.wad": gzdoom ran (its banner, then its own missing-IWAD error)
GUEST-PROOF: 09:00:29 UTC (p2-cases.out's mtime) -- G5, P2 C4: a zipped synthetic .z64: busybox unzip -Zl -1 rc 1; Mupen64Plus "core failed to open ROM image file '/tmp/mupen64plus/'", runemu exit 10; unzip -qql names the entry
GUEST-PROOF: 09:00:29 UTC (p2-cases.out's mtime) -- G6, P2 C5: busybox killall on renamed copies of python3 (substitutes): dolphin-emu-nogui (comm dolphin-emu-nog) ended by killall -9 dolphin-emu-nogui; mupen64plus-simple SURVIVED killall -9 mupen64plus, ended by killall -9 mupen64plus-simple
GUEST-PROOF: 09:00:29 UTC (p2-cases.out's mtime) -- G7, P2 C6: the real DuckStation AppImage (synthetic .cue) SURVIVED killall -9 AppRun.wrapped (rc 1) and ended on killall -9 duckstation-qt (rc 0)
GUEST-PROOF: 09:00:29 UTC (p2-cases.out's mtime) -- G8, P2 C7: /storage/.config/duckstation/memcards a real directory holding a synthetic card, the target present: after the launch, 0 copies of the card anywhere on /storage; control (target absent): the card was migrated
GUEST-PROOF: 09:00:29 UTC (p2-cases.out's mtime) -- G9, P2 C8: switch 1 and token empty, synthetic old token pre-seeded: cheevos_ppsspp.sh and cheevos_flycast.sh exit 1 leaving the old token line (1) and AchievementsEnable = True / Enabled = yes; cheevos_dolphin.sh (control) leaves 0 and Enabled = False; flycast's unquoted test with the key empty falls through as enabled
GUEST-PROOF: 09:00:29 UTC (p2-cases.out's mtime) -- G10, P2 C9: in /storage with the image's bash, [ "$IRES" > "0" ] is true for IRES=2 and creates /storage/0 (0 bytes); false for IRES empty
GUEST-PROOF: 09:00:29 UTC (p2-cases.out's mtime) -- G11, P2 C10 (Q5): dolphin-save-paths check 0.03-0.05 s, duckstation_screenshot_path 0.04-0.07 s (n=5 each); one sha256 of gzdoom.pk3 (3,124,583 bytes) 0.02 s
GUEST-PROOF: 09:00:29 UTC (p2-cases.out's mtime) -- G12, P2 C11 (Q5): runemu.sh start to the emulator's process, n=3 each: ppsspp 0.61/0.63/0.63 s, x64sc 0.62/0.67/0.56 s, DuckStation 0.62/0.53/0.52 s (not first frames: synthetic inputs)
GUEST-PROOF: between 08:56:22 and 08:58:39 UTC (P1's recorded end and P2's recorded start; no artifact of its own) -- G13, the interface's working directory: emulationstation pid 42194 cwd /storage, writable, from essway.service WorkingDirectory=/storage (what a launch inherits)
```

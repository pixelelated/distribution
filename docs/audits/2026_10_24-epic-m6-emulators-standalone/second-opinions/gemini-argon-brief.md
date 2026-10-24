# Second opinion on a code audit -- M6.P2 T30, the standalone emulators, epic tier (Gemini seat, trimmed packet)

You are a second reader of a code audit at the end of its reading stage. You cannot run commands or open the repository; everything you may cite is in the packet below, and every claim you make names the packet's `file:line` or the command output it rests on. The first reader's verdicts are in the packet; do not take them as given.

The scope: 543 paths of a handheld Linux distribution's standalone emulators -- 35 recipes (47 `package.mk`), their 40 start scripts that the launcher `runemu.sh` runs when a player presses a game, eight scripts that write the player's RetroAchievements session into an emulator's config, and their per-device configs -- read at one commit (`8ebaf8daad`). Behaviour claims were proven on a QEMU guest of the x86_64 test image (13 of the 35 emulators ship there) with synthetic inputs, and on the host against the install trees of three images. The first reader is Claude Opus 5.5 (Anthropic); you are a reviewer from another lab, and a second reviewer from a third lab reads the same packet independently. The audit is a renovation: besides defects, findings answer seven questions (Q1 modernize, Q2 standards, Q3 bugs, Q4 package currency, Q5 efficiency, Q6 dead ends, Q7 clarity); this slice's spine is Q3 (the launch path: the exit hotkey's kill target, and any command built from a ROM's name, a file's content or a server's answer) and Q4.

The first reader's draft grades (they become the punch list after your pass): **Medium** -- F-01 (DuckStation's kill target), F-02 (OpenBOR's none), F-04 (hatarisa's route), F-05 (the table's missing scripts on the test image), F-06 (zipped N64 ROMs), F-07 (`.scummvm` through eval, as root; Security), F-08 (gzdoom's xargs), F-09 (the previous RetroAchievements session kept), F-12 (a real directory deleted before linking), F-13 (portaudio's source gone; already filed); **Low** -- every other F-NN; **withdrawn** -- F-18.

**This packet is trimmed** (D-WORKFLOW-195, after a first attempt on the full packet ran out of output budget): the eight achievements scripts are whole; the other 41 start scripts are line-numbered excerpts -- every line the audit cites with 20 lines either side, plus each script's kill-target line -- headed by path and range. Where you rely on an excerpt, say so. Context excerpts outside the membership are not included; the audit's own quotations of them stand as the first reader's claims.

**Bound your answer:** one line per item; parts 1 and 2 before part 3; at most 6,000 words in all.

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


## The achievements scripts, in full, at `8ebaf8daad` (line-numbered)

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

## The other 41 start scripts, as line-numbered excerpts at `8ebaf8daad` (every cited line +/- 20, and the kill-target line +/- 20)

### `projects/ROCKNIX/packages/emulators/standalone/aethersx2-sa/scripts/start_aethersx2.sh` lines 82-122 (of 211)

```
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
```

### `projects/ROCKNIX/packages/emulators/standalone/aethersx2-sa/scripts/start_aethersx2.sh` lines 190-211 (of 211)

```
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

### `projects/ROCKNIX/packages/emulators/standalone/amiberry/scripts/start_amiberry.sh` lines 1-96 (of 159)

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
```

### `projects/ROCKNIX/packages/emulators/standalone/ares-sa/scripts/start_ares.sh` lines 1-44 (of 44)

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

### `projects/ROCKNIX/packages/emulators/standalone/armsx2-sa/scripts/start_armsx2.sh` lines 93-133 (of 226)

```
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
```

### `projects/ROCKNIX/packages/emulators/standalone/armsx2-sa/scripts/start_armsx2.sh` lines 205-226 (of 226)

```
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

### `projects/ROCKNIX/packages/emulators/standalone/azahar-sa/scripts/start_azahar.sh` lines 1-57 (of 240)

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
```

### `projects/ROCKNIX/packages/emulators/standalone/azahar-sa/scripts/start_azahar.sh` lines 206-240 (of 240)

```
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

### `projects/ROCKNIX/packages/emulators/standalone/bigpemu-sa/scripts/start_bigpemu.sh` lines 1-37 (of 42)

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
```

### `projects/ROCKNIX/packages/emulators/standalone/cemu-sa/scripts/start_cemu.sh` lines 1-101 (of 335)

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
```

### `projects/ROCKNIX/packages/emulators/standalone/daedalusx64-sa/scripts/start_daedalusx64.sh` lines 1-54 (of 54)

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

### `projects/ROCKNIX/packages/emulators/standalone/dolphin-sa/scripts/start_dolphin_gc.sh` lines 1-36 (of 478)

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
```

### `projects/ROCKNIX/packages/emulators/standalone/dolphin-sa/scripts/start_dolphin_gc.sh` lines 416-456 (of 478)

```
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
```

### `projects/ROCKNIX/packages/emulators/standalone/dolphin-sa/scripts/start_dolphin_wii.sh` lines 1-36 (of 442)

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
```

### `projects/ROCKNIX/packages/emulators/standalone/drastic-sa/scripts/start_drastic.sh` lines 1-29 (of 93)

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
```

### `projects/ROCKNIX/packages/emulators/standalone/drastic-sa/scripts/start_drastic.sh` lines 37-81 (of 93)

```
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
```

### `projects/ROCKNIX/packages/emulators/standalone/dsperate-sa/scripts/start_dsperate.sh` lines 1-28 (of 163)

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
```

### `projects/ROCKNIX/packages/emulators/standalone/duckstation-sa/scripts/start_duckstation.sh` lines 1-67 (of 135)

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
```

### `projects/ROCKNIX/packages/emulators/standalone/duckstation-sa/scripts/start_duckstation.sh` lines 110-135 (of 135)

```
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

### `projects/ROCKNIX/packages/emulators/standalone/duckstation-sa/sources/Start Duckstation.sh` lines 1-29 (of 36)

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
```

### `projects/ROCKNIX/packages/emulators/standalone/flycast-sa/scripts/start_flycast.sh` lines 1-55 (of 149)

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
```

### `projects/ROCKNIX/packages/emulators/standalone/flycast-sa/scripts/start_flycast.sh` lines 129-149 (of 149)

```
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

### `projects/ROCKNIX/packages/emulators/standalone/gopher64-sa/scripts/start_gopher64.sh` lines 1-27 (of 125)

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
```

### `projects/ROCKNIX/packages/emulators/standalone/gopher64-sa/scripts/start_gopher64.sh` lines 84-125 (of 125)

```
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

### `projects/ROCKNIX/packages/emulators/standalone/gzdoom-sa/scripts/start_gzdoom.sh` lines 1-27 (of 96)

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
```

### `projects/ROCKNIX/packages/emulators/standalone/gzdoom-sa/scripts/start_gzdoom.sh` lines 76-96 (of 96)

```
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

### `projects/ROCKNIX/packages/emulators/standalone/hatarisa/scripts/start_hatari.sh` lines 1-57 (of 74)

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
```

### `projects/ROCKNIX/packages/emulators/standalone/heroic/scripts/start_heroic_authenticate.sh` lines 1-26 (of 68)

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
```

### `projects/ROCKNIX/packages/emulators/standalone/heroic/scripts/start_heroic_play.sh` lines 1-26 (of 42)

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
```

### `projects/ROCKNIX/packages/emulators/standalone/heroic/scripts/start_heroic_play_gamescope.sh` lines 1-26 (of 56)

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
```

### `projects/ROCKNIX/packages/emulators/standalone/hypseus-singe/scripts/start_hypseus.sh` lines 1-28 (of 85)

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
```

### `projects/ROCKNIX/packages/emulators/standalone/mednafen/scripts/start_mednafen.sh` lines 1-29 (of 240)

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
```

### `projects/ROCKNIX/packages/emulators/standalone/mednafen/scripts/start_mednafen.sh` lines 62-109 (of 240)

```
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
```

### `projects/ROCKNIX/packages/emulators/standalone/mednafen/scripts/start_mednafen.sh` lines 124-207 (of 240)

```
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
```

### `projects/ROCKNIX/packages/emulators/standalone/melonds-sa/scripts/start_melonds.sh` lines 1-28 (of 190)

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
```

### `projects/ROCKNIX/packages/emulators/standalone/melonds-sa/scripts/start_melonds.sh` lines 73-153 (of 190)

```
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
```

### `projects/ROCKNIX/packages/emulators/standalone/mupen64plus-sa/mupen64plus-sa-core/scripts/start_mupen64plus.sh` lines 1-103 (of 211)

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
```

### `projects/ROCKNIX/packages/emulators/standalone/nanoboyadvance-sa/scripts/start_nanoboyadvance.sh` lines 1-41 (of 41)

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

### `projects/ROCKNIX/packages/emulators/standalone/openbor/scripts/start_OpenBOR.sh` lines 1-21 (of 45)

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
```

### `projects/ROCKNIX/packages/emulators/standalone/pico-8/scripts/start_pico8.sh` lines 27-48 (of 48)

```
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

### `projects/ROCKNIX/packages/emulators/standalone/ppsspp-sa/scripts/start_ppsspp.sh` lines 1-26 (of 120)

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
```

### `projects/ROCKNIX/packages/emulators/standalone/rpcs3-sa/scripts/start_rpcs3.sh` lines 1-49 (of 220)

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
```

### `projects/ROCKNIX/packages/emulators/standalone/rpcs3-sa/scripts/start_rpcs3.sh` lines 194-220 (of 220)

```
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

### `projects/ROCKNIX/packages/emulators/standalone/scummvm-sa/scripts/start_scummvm.sh` lines 47-73 (of 73)

```
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

### `projects/ROCKNIX/packages/emulators/standalone/skyemu-sa/scripts/start_skyemu.sh` lines 1-50 (of 56)

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
```

### `projects/ROCKNIX/packages/emulators/standalone/steam/scripts/start_steam.sh` lines 242-281 (of 281)

```
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

### `projects/ROCKNIX/packages/emulators/standalone/steam/scripts/start_steam_arm64.sh` lines 1-30 (of 30)

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

### `projects/ROCKNIX/packages/emulators/standalone/steam/scripts/start_steam_x86.sh` lines 1-30 (of 30)

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

### `projects/ROCKNIX/packages/emulators/standalone/supermodel-sa/scripts/start_supermodel.sh` lines 1-28 (of 87)

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
```

### `projects/ROCKNIX/packages/emulators/standalone/supermodel-sa/scripts/start_supermodel.sh` lines 67-87 (of 87)

```
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

### `projects/ROCKNIX/packages/emulators/standalone/touchhle-sa/scripts/start_touchhle.sh` lines 1-27 (of 77)

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
```

### `projects/ROCKNIX/packages/emulators/standalone/touchhle-sa/scripts/start_touchhle.sh` lines 51-77 (of 77)

```
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

### `projects/ROCKNIX/packages/emulators/standalone/vice-sa/scripts/start_vice.sh` lines 1-27 (of 85)

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
```

### `projects/ROCKNIX/packages/emulators/standalone/vita3k-sa/scripts/start_vita3k.sh` lines 1-30 (of 255)

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
```

### `projects/ROCKNIX/packages/emulators/standalone/xemu-sa/scripts/start_xemu.sh` lines 1-26 (of 198)

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
```

### `projects/ROCKNIX/packages/emulators/standalone/yabasanshiro-sa/scripts/start_yabasanshiro.sh` lines 1-75 (of 112)

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

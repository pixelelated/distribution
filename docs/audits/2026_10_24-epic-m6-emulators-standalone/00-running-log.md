# Epic Audit Running Log — M6.P2 T30, the standalone emulators

**Auditor:** Code Auditor skill (v1.13.0, identical to `next`'s copy: `diff -q` against `git show next:.claude/skills/code-auditor/SKILL.md`, no output), with the renovation face of `docs/reviews/plan-for-the-plan.md` § 4
**Primary model:** Claude Opus 5.5 (`claude-opus-5-5`, lab Anthropic) at high effort, in Claude Code. Identity sources: the coordinator's dispatch on #677 (issuecomment-6381895209, 2026-10-24T08:16:35Z) and the session's own metadata
**Session:** herdr agent `m6-t3-emulators`, session `a6d65411-5a44-4596-9a6c-337855905c17`, pane `wN:p6` (the T3 session; its T3 worktree is idle beside this one, written nowhere)
**Started:** 2026-10-24 08:17 UTC (`date -u` 08:17:51 at the first commands)
**Scope:** slice `emulators-standalone` (#677, `M6.P2 E798/T30`), area epic #798 (the emulators and cores), renovation epic #339, milestone M6. The membership is the inventory's `k: 30` rules (brief § 2): 543 paths
**Spec:** `docs/reviews/briefs/emulators-standalone.md` version 2 (`b81fc193a1`; its § 7 is #677's checklist, and #677 wins where they differ); `docs/reviews/plan-for-the-plan.md`
**Depth:** Extended (two reviewers from two other labs: GPT-6 Astra `--member gpt` at `max`, Gemini 4 Argon `--member gemini-argon` at `high`; probes first, then one refutation packet to each independently)
**Branch / worktree:** `feature/m6-emulators-standalone-677` at `/workspace/repos/pixelelated/distribution.worktrees/m6-emulators-standalone-677`
**Read hash:** the slice's bytes are `next`'s `8ebaf8daad`; `reviewed-at` is the branch `HEAD` at stage A, recorded below
**Proof tokens:** a line in this log begins with the guest token or the host token only to record a proof (criterion 12 counts them against the `proved:` cells of `02-forward-audit.md`); this header names them without starting a line with either

---

## Log Entries

### [Phase 0] 08:17-08:18 — The brief's first commands (`date -u` 08:17:51, 08:18:32)

- `git fetch origin`, `git fetch upstream --no-tags`: both exit 0.
- Branch `feature/m6-emulators-standalone-677`, `HEAD` `c7e3dfcc87411ab3c92c41ce49539a7e9328d84b` (the dispatch's hash); `git merge-base --is-ancestor 2174265e9c HEAD` exit 0: stacked on the P1 tip. `docs/reviews/inventory.json` and `slices.json` present; `tools/renovation-{inventory,status,drift}` present.
- `git diff --stat next -- .claude CLAUDE.md AGENTS.md tools/lint-audit-artifacts`: seven files (115+/11-): `engineering-practices.md`, `fork-workflow.md`, `generic-x64-vm-testing.md`, `instruction-files.md`, `code-auditor/references/templates.md`, `council/IMPORTED-FROM.md`, `tools/lint-audit-artifacts`. Exactly the seven paths brief § 1 names; nothing stale.
- `grep -c 'Renovation face' tools/lint-audit-artifacts` 4; `grep -c gemini-argon scripts/council-invoke.ts` 7.
- `next` = `8ebaf8daad8eaac6331dff6fc048fb4411d7decb`. **`upstream/next` = `e0f9deb89926f0febd81084dc947ad93d52db132`** (Q4's upstream, fetched now; T3 read `3421d7d178`). `git merge-base next upstream/next` = `c445081a59518f37d9776e5412dd7b14910696f7`.
- The read tree: `git archive 8ebaf8daad projects/ROCKNIX/packages/emulators/standalone | tar -x -C .qa-scratch/t30/at-hash` rc 0, 623 files (543 members + 80 patches, brief § 2). `.qa-scratch/` is ignored (`.gitignore:63`).
- `git diff --stat 8ebaf8daad HEAD -- projects/ROCKNIX/packages/emulators/standalone`: **empty**. The slice's bytes are `next`'s.
- `tools/rules-check` rc 0; `tools/register-check` rc 0 (662 IDs, each once); `tools/ceremony-check` rc 1, its one overdue line `weekly OVERDUE: 2026-W42 summary missing`: M7's week, noted, not this lane's (the coordinator's 08:16 note on T3).
- `git push -u origin feature/m6-emulators-standalone-677`: up to date, tracking set. `core.hooksPath` lists `pre-push`.
- The brief is in the tree. The host file's last M7 block is the **05:42:07 resource return** (line 106); the M6 blocks after it (07:13, 07:21) open no hold. **M6 holds the host.** Census: `pgrep -c -x qemu-system-x86` 0, `pgrep -fc 'make docker-[A-Z]'` 0; `free -g` 41 G available, swap 3 of 7 G used; `/workspace` 1.7 T free.
- `df -i /tmp` 40 % (633,260 inodes free); `df -i /workspace` 19 %. Exports go under `/workspace/tmp/m6-t30/`.
- `~/.config/council/env` present (not read). `node` v24.21.0, `npm` 11.19.0; `tools/council/node_modules` absent (the install comes before Phase 4.6).

### [Stage A] 08:19-08:22 — Scope re-derived; T3's tools copied

- **Counts** (brief § 2's filter, `python3 -I`, 08:19:07): 543 paths, 157,365 lines; 55 fork-own / 7,421 lines; 488 upstream-carried; all `shipped`; 105 code-class files / 10,695 lines, 3,104 fork-own (shell 55 / 6,635, recipe 47 / 2,651, python 2 / 483, c 1 / 926); 35 recipes; thirteen fork-own `package.mk`. **No delta** from the brief or #677. Recorded in `01` § Scope with the fork-own table (55 rows).
- **Tree against membership:** `git ls-tree` 623 = 543 + 80 `.patch`; `comm -3` in the C locale prints nothing. In the session's `en_US` locale `comm` refused the input as unsorted, which is T3's S2 trap again; re-run under `LC_ALL=C`.
- **Start scripts:** 40 `start_*.sh`. The 41 at `order.md:787` is the same set plus `Start Duckstation.sh` (a case-insensitive count gives 41). Recorded; no disagreement.
- **Upstream:** 38 commits on `standalone/` since the base, all after `8ebaf8daad`; `git diff --stat upstream/next 8ebaf8daad` 144 files, +71,085/-1,034. The fork has 41 commits on the membership since the base. Exit-sweep leads before reading: `eeb33c5a37`, `4a6415c033` (duckstation-sa → `duckstation-qt`).
- **Device × recipe:** the metapackage's arms evaluated per device under `env -i` from a copy in `.qa-scratch/t30/meta/`, and the inventory's `reachable_by` per `package.mk`; the two agree. **H700 17, SM8550 35, GENERIC_X64 15** by the arms. The brief's image list is thirteen, so `amiberry` and `yabasanshiro-sa` are a Q6 lead for the image-set check.
- **Tools** copied by path from T3's folder at `b3cb4ec8c5` into `docs/audits/2026_10_24-epic-m6-emulators-standalone/tools/`, each with a provenance comment after its copyright line: `q4-pins.py`, `q4c-patches.sh`, `regen-es-systems.sh`, `s2-regen-check.sh`, `punch-items.py`, `coverage-table.py`, `audit-issue-body.py`, `set-outcome.py`, `write-completion.py`. One change so far: `q4-pins.py` lines 64-65 (T3's 59-60) read `standalone/`. `diff` against T3's file shows only the header and those two lines; `py_compile` passes. The first `sed` used `#` as its delimiter on a comment and failed. A line count off by one left line 65 at `libretro`; the diff caught it and it was fixed before commit.
- **`reviewed-at` candidate:** `c7e3dfcc87` (HEAD at stage A; the membership's bytes are `8ebaf8daad`'s). Final at hand-back.

### [Stage B] 08:23-08:30 — The host-side checks of brief § 5

- **`tools/pkgcheck` over the 47 recipes** (08:23:31): 47 of 47 rc 0. I first took a no-argument run's whole-tree output as a scan for one argument. A bare `tools/pkgcheck` checks every package, and that run's `jre.zulu` FAIL is outside the slice. The tool was not at fault; I misread my own command. Proved per name: each argument processed exactly one `package.mk`, its own (`pkgcheck-coverage.txt`: 47 × `processed=1 self=1 warnfail=0`). Exit status checked: `tools/pkgcheck jre.zulu` rc 1 on its FAIL.
- **`bash -n` over the inventory's 55 shell files** (08:24:55, the at-hash export, read by `while IFS= read -r`): 55 ok. Three do not end in `.sh` (`010-pico8`, `steamos-set-timezone`, `steamos-session-select`). Control: a file holding `if then` fails `bash -n`. shellcheck is not on the host (`command -v shellcheck` empty), as T3 recorded.
- **`PKG_SHA256` per branch** (08:24:55): 16 lines where the URL count exceeds the checksum count. Fourteen are `.git` URLs pinned by commit, and two are the empty-URL metapackages `mupen64plus-sa` and `pico-8`. `heroic` has no `PKG_URL` line. The one multi-branch recipe, `duckstation-sa` (x86_64 and aarch64 AppImages), has a URL and a checksum in each branch. **No archive URL without `PKG_SHA256`.**
- **The `.process-kill-data` writer** (08:25:21): `set_kill` in `001-functions:509-521` writes its second argument, verbatim, as one line. `runemu.sh:179` runs `set_kill stop` before every launch. `runemu.sh` names a target only for mednafen (235) and RetroArch (264). 38 of the 41 start scripts call `set_kill set` themselves (`git grep -c`). The other readers are `input_sense:180-181` and `rocknix-fake-suspend:226`.
- **The three install trees' `start_*.sh`** (08:25:21; BUILD_IDs from `etc/os-release`, since `usr/lib/os-release`, the brief's path, exists in none): GENERIC_X64 `069fc27044` 21, H700 `08cc7ff6cd` 25, SM8550 `08cc7ff6cd` 48. Those counts include the non-member scripts `start_es`, `start_gmu`, `start_mplayer`, `start_syncthing` and `start_portmaster`. The build commits are not in this clone, so the trees were checked against the hash by `cmp` rather than by running git in M7's repository. Of the 40 source `start_*.sh`: GENERIC_X64 9 same, 4 differ, 27 absent; H700 13 / 3 / 24; SM8550 30 / 9 / 1. All 16 differing pairs differ only on lines whose source side carries an install-time `@NAME@` placeholder, with no add or delete hunk. Control: a pair with a real edit is reported. **The trees carry the hash's start scripts, template-filled.**
- **The #825-class grep** (08:26:28): 318 hits (`checks/grep825.txt`). The pattern matches every `$(get_setting ... "${GAME}")`, so the hits are an index for the reading, not grades.
- **The cheevos scripts' logging grep** (08:26:28): saved masked to `checks/cheevos-log.txt`, not printed.
- **The two upstream greps** (stage A): 38 commits; 144 files +71,085/-1,034.
- **A tool for the routes** (08:28:14): `tools/t30-routes.py` resolves every standalone route in each image's `es_systems.cfg` the way `runemu.sh` does, and reads the installed script's kill names against the tree's executables. GENERIC_X64 37 routes (11 no script, 1 no kill target, 5 unmatched names); H700 72 (5, 1, 1); SM8550 145 (6, 2, 9). Its fail-closed control, a root with no table, exits 1. I first read it as 0 through a `| tail -1` pipe, which is the pipeline-status trap of `engineering-practices.md`; re-run bare, it is 1.
- **Read from the routes before the scripts:** `atarist`'s `hatarisa` route asks for `start_hatarisa.sh`, absent on all three trees (the recipe installs `start_hatari.sh`, which sets no kill target either; upstream's `2e7041d273` renames it and adds `-9 hatarisa`). `start_OpenBOR.sh` and `start_steam.sh` set no kill target (upstream's `start_OpenBOR.sh` sets none either). `heroic` and `moonlight` are `.sh`-ROM systems, which `runemu.sh:488` runs itself, so their table rows are not routes. GENERIC_X64's table offers `amiberry`, `drastic`, `dsperate`, `melonds` and `yabasanshiro` with no script in the image. `AdvanceMame` (cps1 to cps3) and `moonlight` have no script on any tree; neither is a member. Upstream's `eeb33c5a37` adds `mupen64plus-simple` to mupen64plus's targets, and `4a6415c033` moves duckstation's from `AppRun.wrapped` to `duckstation-qt`.

### [Stage B] 08:30-08:43 — Phase 1 and 3 reading: the 55 shell files, two Python, one C

- **Read whole:** the eight `cheevos_*.sh`; the fork-own start scripts (`start_dolphin_gc.sh`, `start_dolphin_wii.sh` and their diff, `start_duckstation.sh`, `Start Duckstation.sh` and their diff, `start_mupen64plus.sh`); `dolphin-save-paths`; `duckstation_screenshot_path`. **Read, with the plain one-key `sed` config lines elided** (`sed -i '/KEY/c\KEY = VALUE' $CONF`, which carry no variable but the config path): the other 34 start scripts, `mednafen_gen_config.sh`, `psp_save_mover.sh`, `scan_vita3k.sh`, `010-pico8` and the two `steamos-*` helpers. `libdrastouch.c` was skimmed for string copies, `system` and `getenv`, of which it has none unsafe. 55 + 2 + 1 = the 58 code-class files that are not recipes.
- **Interface source read for one question** (does the interface leave the switch on with the token empty?): `GuiRetroAchievementsSettings.cpp:750-805` at the ES pin `16dbac52`, with `git -C ~/Development/emulationstation-next show`, read only. Yes, at 767 and 780.
- **Upstream commits read in full:** `eeb33c5a37`, `4a6415c033`, `2e7041d273`, `195a8eba4b`, `b6fcd2ca4f` (with `0c43a50420`).
- **The DuckStation AppImages** were copied out of the GENERIC_X64 and H700 trees into `/workspace/tmp/m6-t30/duck/` (`df -i /workspace/tmp` 19 %) and listed with `unsquashfs -o <offset> -l`. Their sha256 equal the recipe's two `PKG_SHA256`, and the SM8550 copy is byte-equal to H700's. The first offset, the first `hsqs` match at 157729, was not a superblock; the second was.
- **Two host fixtures** (bash and the host's GNU sed for the shapes; the image's busybox sed is checked where it matters): `start_amiberry.sh:70-71`'s substitution turns `gfx_width=720` into a bare `640`; `start_daedalusx64.sh:48`'s `[ "$a" <> "$b" ]` reads true and creates a file named `$b`. Their proof lines follow in the proofs entry with their commands.
- The findings are in `.qa-scratch/t30/notes.md` (scratch) until `02`, `03` and `04` are written from them. `git status --short -- projects/ROCKNIX/packages/emulators/standalone`: empty.

### [Stage B] 08:46 — Checkpoint on #677; a typed time corrected

- Checkpoint posted on #677: issuecomment-6382133893, `created_at` **08:43:29Z**. Its heading said "08:53 UTC", which I typed rather than read from the clock (#843's class). The coordinator caught it at 08:46. The heading has been edited to 08:43 with a note.
- The previous entry's start, written as 08:28, came from the route tool's output, not from when the reading began. It is now 08:30, the end of the host-checks entry before it; its end, 08:43, came from `date -u`.
- A friction line was written. From here every stamp in this log, on #677 and in the friction and work logs comes from `date -u` in the same command that writes it.

### [Stage B] 08:44-09:01 — Q4 by hand; the guest cycle

- **Q4.** `q4-pins.py` exited 1 at first. The cause was T3's hardcoded row count (151); the copy's line 143 now reads 47, the second named change in its header, and from its cache it gives rc 0 with 47 rows (behind-project 30, behind-upstream 1, by-hand 6, pin-not-on-project 9, repo-missing 1). For a tag or release pin, `pin-not-on-project` means only "not an ancestor of the default branch"; those rows are graded by shape in `04`.
  - **`portaudio`'s repository answers 404.** `curl` of its archive URL returned `http=404` at 08:47:29. Commit `64d1bf9` is not in PortAudio/portaudio (HTTP 422). The host's cache holds the bytes (`c33e4821…` = `PKG_SHA256`, 2026-08-26), and upstream carries the same URL. #841's class.
  - The moving tarballs (08:47:53): `aethersx2-sa` and `drastic-sa` both match their `PKG_SHA256` today.
  - The asset and tag pins against each project's latest release (08:48:05, 08:48:27) are tabled in `04`.
  - `q4a-dispositions.md`: 38 upstream commits, 33 to merge, 5 conflicts, 0 superseded; with the thirteen fork-own recipes' pins.
- **The guest cycle.** Disk `/workspace/artifacts/m6-t30-20261024/t30.qcow2` made from the verified image (`sha256sum -c` OK; `build_commit` `069fc27044`, `dirty: no`; 16 GiB). The host file's last M7 block is still the 05:42 return. Census before: 0 QEMU, 0 builds. My first `run` gave `--monitor` QEMU's `unix:` spec; the tool refused before QEMU started (path too long), census still 0. The second boot at 08:51:30, QEMU pid 75319, `--pidfile /workspace/tmp/m6-t30/qemu.pid`, VNC 24, SSH 10037; `vm-serial wait` ready at 08:52:03. Key provisioned over serial. Guest `BUILD_ID` `069fc270442134fe771258418adf4e666e0473fb`. Stopped with `tools/vm-stop` rc 0 at 09:01:08, census after 0.
  - **A fixture fault in P1.** Where an emulator had already exited on its synthetic input, the kill data was already `emulationstation` (`runemu.sh:128`) and P1 ran `killall emulationstation`, eight times; the interface restarted under its service. P2 kills only a live emulator. P1's verdicts are kept only for the rows where the emulator was alive at the kill.
  - **A fixture side effect in P2:** C8's restore deleted `global.retroachievements`, which the image sets to 0 (`/usr/config/system/configs/system.cfg:77`); it was put back to 0 before the stop.
  - The guest's clock reads four hours behind the host (exec.log 04:56 at 08:56 host). The proof times below are the host's.
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
- **Times corrected before commit:** this entry's proof lines were first written with estimated times (the 08:46 friction line's class, again within minutes). Each was replaced by its artifact's `mtime` (`date -u -r`), or by the bracketing recorded times where none exists, in the same command; the heading's start is Q4's recorded 08:44:24.

### [Stage C] 09:13-09:16 — Phase 4.6: the Facilitator, the probes, the refutation passes started

- 09:13:26 `npm install --prefix tools/council` rc 0. `tools/council/run verify-pins`: "OK - verifier pins match current files and every re-pin is accountable." `tools/council/run test`: 39/39, 127/127 and 19/19 pass, 0 fail. `run` sources `~/.config/council/env` itself (`tools/council/run:21-27`); the file was not read here.
- `second-opinions/review-plan.json`: Extended; `gpt` (`openai/gpt-6-astra`, max), `gemini-argon` (`google/gemini-4-argon`, high); primary `anthropic/claude-opus-5-5`.
- **Probes** 09:14:49 to 09:15:02 (`--provider openrouter`, T3's one-line prompt):
  - `gpt`: served `openai/gpt-6-astra` by OpenAI, effort max, identity source `provider_response`, all three verifications PASS. Its own reply named itself "unknown"; the provider's field is the identity.
  - `gemini-argon`: served `google/gemini-4-argon` by Google, effort high, all PASS.
- **The packet:** one, built by a script from `02` (less the 543 generated coverage rows), `03`, `04`, `q4a-dispositions.md`, all 49 start and achievements scripts plus ten more files in full, line-numbered excerpts of `runemu.sh`, `input_sense`, `001-functions`, `backuptool`, `virtual/emulators`, melonDS's patch and ES's `GuiRetroAchievementsSettings.cpp` (at `16dbac52`), the two guest scripts with their outputs, and the proof lines. 438,502 bytes; the two briefs are identical (sha256 `4c24f7cc03c9…`). `tools/forbidden-terms-check --stdin` rc 0; no credential-shaped line. The synthetic strings of P2 are present by design.
- **Refutation passes started 09:15:57** (the background task's first line), both seats in parallel. The harness task `bb94w72xv` waits on both and delivers their end. Its silent mode: a seat that hangs is ended only by the Facilitator's timeouts, 1 h per attempt and 4 h in total (the code's defaults, `scripts/council-invoke.ts:2731-2732`; its `--help` text still says 360000 and 1800000 ms, which I copied first and corrected from the code). The coordinator's failed-seat rule (#650) holds: hold, diagnose, one same-slug retry on a transient cause, never one seat.

### [Stage C] 09:18-09:22 — The second guest cycle, during the seats' passes (named on #677 at 09:17, issuecomment-6382442735)

- The host file's last M7 block is still the 05:42 return; the newest line is the coordinator's 09:08 retention note. Census 0 QEMU, 0 builds. The content was unpacked under `/workspace/tmp/m6-t30/content/x` (`df -i` 19 %). Boot at 09:18:46, QEMU pid 380639, the same disk, VNC 24, SSH 10037, pidfile `/workspace/tmp/m6-t30/qemu.pid`; ready at 09:19:06. Content copied by `scp` with matching sha256 on both sides (`freedoom1.wad` `7323bcc168c5…`, `queen.1` `fefa653808b3…`). Stopped with `tools/vm-stop` rc 0 at 09:21:44, census after 0.
- **The harness** `/workspace/artifacts/m6-t30-20261024/c2-frames.py` takes frames through `tools/vm-visual-qa`'s `Monitor` (loaded as a module, not copied), and kills only a live emulator. The SSH no-op round trip, median 0.09 s, is the error bar on "launch call".
- **What the frames are, read by opening them:** gzdoom's first frame is Freedoom's title (`c2-frames/gzdoom-2-first.png`). ScummVM's is ScummVM's own splash, at 640×400 in a corner of the 1280×800 screen (`scummvm-2-first.png`), not the game's first frame. The "back" frame is the carousel, which never left the screen, because an SSH launch leaves EmulationStation rendering. So "kill to interface" is the emulator's window closing, not the interface's return path.
GUEST-PROOF: 09:19:55 UTC (c2-gzdoom.out's mtime) -- G14, gzdoom with Freedoom 0.13.0 (real free content) through runemu.sh, n=3: kill data "-9 gzdoom", process comm gzdoom exe /usr/bin/gzdoom, killall -9 gzdoom rc 0 and the emulator gone each time; launch call to the first frame (Freedoom's title) 3.13 / 1.03 / 1.11 s; window gone 0.15-0.17 s after the kill; /workspace/artifacts/m6-t30-20261024/c2-frames.py, /workspace/artifacts/m6-t30-20261024/c2-gzdoom.out, /workspace/artifacts/m6-t30-20261024/c2-frames/
GUEST-PROOF: 09:20:27 UTC (c2-scummvm.out's mtime) -- G15, ScummVM with Flight of the Amazon Queen (real freeware) through runemu.sh, n=3: kill data "-9 scummvm", process comm scummvm exe /usr/bin/scummvm, killall -9 scummvm rc 0 and the emulator gone each time; launch call to the first frame (ScummVM's splash, not the game's) 1.08 / 0.64 / 0.64 s; window gone 0.16-0.17 s after the kill; /workspace/artifacts/m6-t30-20261024/c2-scummvm.out, /workspace/artifacts/m6-t30-20261024/c2-frames/

### [Stage C] 09:32-10:03 — The seats: GPT succeeded; Gemini failed and the stage holds

- **`gpt`**: ended 09:32:03 (rc 0), served `openai/gpt-6-astra` by OpenAI, effort max verified, identity PASS. Output `second-opinions/gpt-audit.md`, 35,592 bytes, with its provenance file.
- **`gemini-argon`**: ended 10:02:20, rc 2, `retries_exhausted_empty_content`, 2,783 s over 4 attempts; provenance `second-opinions/gemini-argon-audit.md.provenance.json`; no output file. From its log (`.qa-scratch/t30/gemini-audit.log`):
  - Attempts 1 to 3: http 200, served `google/gemini-4-argon` by Google, `finish=length`. Reasoning 57,822 / 57,141 / 56,784 tokens, content 21,464 / 22,825 / 23,507 bytes, truncated. The Facilitator's bump stayed at the ceiling, "max_tokens 65536 → 65536 (ceiling 65536)".
  - Attempt 4: `finish=error`, empty content.
  - Identity and provider PASS; effort unverifiable, since no completed attempt reported it.
- **Diagnosis: not transient.** The packet (438,502 bytes) drives Argon's high-effort reasoning to about 57,000 tokens of a 65,536 ceiling, which leaves too little for the answer. Three attempts on the same input ended the same way. T3's 308 KB packet took Argon 30,337 reasoning tokens.
- **The coordinator's failed-seat rule (#650), applied:** hold; the failure recorded; diagnosed; **no same-slug retry**, the cause not being transient; never one seat; the way forward is the coordinator's. Posted on #677 with options. The GPT output is read while the stage holds, its items re-read at their artifacts, but nothing is graded into `04` § Second opinion until the second seat returns.

### [Stage C] 10:11 — The Gemini seat again, on a trimmed packet (D-WORKFLOW-195, the coordinator's answer on #677)

- The first attempt's provenance is kept as `second-opinions/gemini-argon-audit-run1-truncated.md.provenance.json` (`git mv`).
- **The packets, side by side:**
  - GPT's: `gpt-brief.md`, 438,502 bytes, sha256 `4c24f7cc03c94eec8a13a1e6…`. Gemini's run 1 had the same bytes; its brief file was overwritten by run 2's.
  - Gemini's run 2: `gemini-argon-brief.md`, **237,403 bytes, sha256 `adfc1f750b629faa1b121313…`**.
- **What run 2's packet holds:**
  - `02`, `03`, `04` and q4a **verbatim from GPT's packet**, so that only the trimming differs, not the later cycle-2 updates to the live files;
  - the guest scripts, outputs and proof lines as GPT had them;
  - the eight achievements scripts whole;
  - the other 41 start scripts as line-numbered excerpts headed by path and range: every line `02`, `03` or `04` cites, and each `set_kill` line, with 20 lines either side. That is 2,240 of 5,752 lines in 56 ranges (`.qa-scratch/t30/gemini-trim-stats.txt`).
  - No context excerpts outside the membership: they are not in D-WORKFLOW-195's list.
  - The ask is bounded: one line per item, parts 1 and 2 before 3, at most 6,000 words.
- `tools/forbidden-terms-check --stdin` rc 0. The run started in the background (harness task `b8sicheu7`), on the same model, effort and provider.

### [Stage C] 10:10-10:23 — Gemini run 2 succeeded; the third guest cycle (named on #677, issuecomment-6383042792)

- **Gemini run 2** (trimmed packet): 10:10:57-10:19:34, rc 0, first attempt; served `google/gemini-4-argon` by Google, effort high, provider and identity PASS; 41,141 reasoning tokens, `finish=stop`; `second-opinions/gemini-argon-audit.md`, 22,666 bytes, 2,672 words.
- **Cycle 3:** the host file unchanged (the last M7 block 05:42); census 0; boot 10:21:55, QEMU pid 910037, the T30 disk; `vm-serial wait` ready about 20 s later; script hash equal on both sides (`1b3558fb968e…`); `tools/vm-stop` rc 0 at 10:22:49, census after 0.
GUEST-PROOF: 10:22:49 UTC (p3-tools-then-game.out's mtime) -- G16, Gemini's G-03 tested: with DuckStation's two links removed, the Tools launcher's Start Duckstation.sh (run 8 s) left /storage/.config/duckstation/savestates a REAL directory created by DuckStation (memcards: not created); a synthetic state there, then a game launch through runemu.sh: 0 copies of the state remain, in the constructed run (targets present) and in the control (targets absent). A synthetic card placed by the script in a real memcards directory: 0 copies with the target present, migrated with it absent. /workspace/artifacts/m6-t30-20261024/p3-tools-then-game.sh, /workspace/artifacts/m6-t30-20261024/p3-tools-then-game.out

### [Stage C-D] 10:23-10:33 — Phase 4.6 graded; the punch list, 19 bugs and the audit issue

- **Phase 4.6 graded** into `04` § Second opinion, both seats, item by item, each with its artifact. The seats saw different evidence (D-WORKFLOW-195); Gemini's excerpt-only items are marked.
  - **Re-graded:** F-07 and F-12 to High (F-12 on G16); F-03, F-14, F-20 and F-21 to Medium.
  - **Kept, with reasons:** F-10, F-11, F-15, F-16, F-19, F-29 and F-30.
  - **Wording corrected:** F-09 (melonDS disables and keeps the credentials), F-11 (11 sites), F-30 (the quoted multi-PID form kills none), F-02, F-08, F-13 and F-26.
  - **New:** F-31 to F-42 from the seats' items.
  - **Refuted:** Gemini's G-09 (`runemu.sh:263-264`), and GPT's G-45 as provenance (`git describe --tags b137d8c373`). Narrowed: Gemini's G-08 and GPT's G-28 (no keymap seed with a space).
  - The coverage table was regenerated (543 rows, 0 empty) with F-31 to F-42 at their paths.
- **`05-punch-list.md`**: 41 items (2 High, 17 Medium, 22 Low), generated by `tools/punch-items.py` (T3's generator, its items replaced). Every item has its `question:`; outcomes are `open`, except `deferred` for PL-013 (#849), PL-016 (class 1) and PL-025 (class 1).
- **Bugs filed (19), `#853` to `#871`**, each with a code trace, `Already written:`, the VM line and agent-verifiable criteria (31 checkboxes). `tools/box-check --issue` gives 0 fail on each. 17 cover one item each (PL-010 inside #861, PL-022 inside #857). #870 groups the Low achievements items PL-021 and PL-039; #871 groups ten Low launch-script items. No bug for #849's row, the class-1 deferrals, the Renovation and currency items, or PL-034 and PL-035, whose classification is the coordinator's.
- **The audit issue #872** (labels `audit`, `punch-list`, milestone M6, a sub-issue of #677): 41 checkboxes, `box-check` 0 fail. `tools/lint-audit-artifacts --phase pre-issue --issue 872`: `PASS pre-issue artifacts`.
- `git diff --stat 8ebaf8daad HEAD -- projects/ROCKNIX/packages/emulators/standalone`: empty. **The stage-D pause starts here**: the lane waits for the coordinator's stream briefs, edits nothing of the 543, and drafts the retro meanwhile.

## Stage D, 10:37:53 UTC: F-13 re-graded Low (the coordinator's correction on #677)

- The coordinator: ROCKNIX's source mirror serves portaudio's archive with the recipe's sha256, so an empty-cache build succeeds; F-13 is Low (dead primary URL, mirror-covered).
- Read: `scripts/get_archive:23` builds `PACKAGE_MIRROR="${DISTRO_MIRROR}/${PKG_SOURCE_NAME}"` and `:35` adds it after `PKG_URL`; the loop accepts the first URL whose sha256 matches. `DISTRO_MIRROR` is `https://github.com/ROCKNIX/distribution-sources/releases/download/sources-v2` (`distributions/ROCKNIX/options:186`).
- Checked: the mirror's `portaudio-64d1bf913433d7a2835526b80a93487d5038cb8e.tar.gz` fetched to `/workspace/tmp/m6-t30/fetch/mirror-849/` (not the shared cache): http 200, 1,451,821 bytes, sha256 `c33e48217a844cca3b66ab88571b90beefb8fcb6967177951d4dc283587bf834` = `PKG_SHA256` (10:36:26 by `date -u` in the fetch's command).
- Changed: PL-013 Medium to Low in `tools/punch-items.py` and `05` regenerated (2 High, 16 Medium, 23 Low); F-13's rows in `02` and the coverage row regenerated; `04`'s summary, risk row, Q3 list, Q4(b) row and grading row; #872's body regenerated. The stage-D entry above keeps its counts as written then.
- What missed it: the stage-B check read the primary URL and the commit and never `get_archive`'s fallback; a fetch check for #841's class must test the primary and the mirror.

## Stage E, S0 (11:08:58 UTC): commands built from data (PL-007 #859, PL-008 #860, PL-018, PL-019 #865, PL-031)

- **Brief:** `docs/reviews/briefs/t30-streams.md` at `bf8184e494` (on `feature/m6-renovation-plan-346`, read with `git show`, not merged).
- **The test first:** `tools/s0-fixtures.sh` (`787daa65bd`) lifts each script's lines by marker from a commit or `WORKTREE` and runs them under the GENERIC_X64 image's bash, GNU grep and busybox applets (the M7 root `m7-pixelelated-replacement20`, read only; nothing started there). At the unfixed `4c581e492f`: 8 FAIL, with the 6 controls PASS. On the fixed tree: 14 PASS.
- **The changes**, one commit each:
  - `dfa9a5a694` scummvm: the `.scummvm` line parsed without a shell.
  - `9b56828bf8` yabasanshiro: the pad's name kept as text.
  - `46b6601e98` gzdoom: an argument array, and `doom_value` for a `.doom` file's values.
  - `861bdbe82b` gopher64: an argument array, no empty password, gopher64's own `retroachievements.json` token preferred (read from its source at the pin, `src/retroachievements.rs:45-68`, `src/main.rs:194-212`).
  - `6894bfd3cd` Steam: the URI and `-silent` as two elements. The brief named lines 205, 240 and 260; the declaration at 177 changed with them.
  - Three scripts gained a ROCKNIX copyright line.
  - `bash -n` passes on all five.
- **A difference from the brief, said:** the brief wrote gzdoom's prefix as `"${EMUPERF[@]}"`. `EMUPERF` is a string (`${SLOW_CORES}`, `runemu.sh:407`), and quoting it would pass "taskset -c …" as one word, so it stays unquoted, as every other start script has it.
- **The guest cycle S0**, named on #677 at 11:03:52 (the comment's created_at):
  - Host file: last M7 block 05:42. Census 0.
  - Boot at 11:04:05, QEMU pid 1421088, the T30 disk, pidfile `/workspace/tmp/m6-t30/qemu.pid`.
  - The two fixed scripts were copied by `ssh` with matching sha256 (`840f3c7a5e15…`, `6a4f3cb1a453…`), and bind-mounted over `/usr/bin` for part B only. They were unbound before the stop; the image's hashes (`fd85e7b56f39…`, `55f441e4467f…`) are back.
  - The crafted file and the renamed copy were removed.
  - `tools/vm-stop` rc 0 at 11:07:41. Census after: 0.
- **A fixture fault, recorded:** the guest script's helper block was copied from P2 by line range (7-44) and took P2's C1 lines with it. Three route launches ran again (hatarisa, drastic, amiberry: exit 127, as in G2) and changed nothing.

PROOF: 11:08:03 UTC (s0-fixtures-WORKTREE.out's mtime; the 4c581e492f run's at 11:08:02) -- S0-F1, tools/s0-fixtures.sh at 4c581e492f: 8 FAIL (gopher64: empty password's slot, spaced password, token not used; Steam: URI and -silent one argument; yabasanshiro: the crafted name's marker created; gzdoom: apostrophe, gzdoom calls 0; gzdoom: .doom values; scummvm: the crafted marker created) and 6 controls PASS; WORKTREE: 14 PASS, each stub's call count printed; /workspace/artifacts/m6-t30-20261024/s0-fixtures-4c581e492f.out, /workspace/artifacts/m6-t30-20261024/s0-fixtures-WORKTREE.out
GUEST-PROOF: 11:05:13 UTC (s0-guest.out's mtime) -- S0-G1, PL-007 and PL-008 on the guest. The image's scripts: the crafted .scummvm marker PRESENT (owner root); "Free Doom's Gate.wad" stops at "xargs: unmatched single quote". The fixed scripts bind-mounted: the crafted file's marker absent, and ScummVM answers "Stray argument 't30-no-such-game;'" (svm-crafted-fixed.exec.log). FOTAQ's argv is "--path=/storage/roms/scummvm/FOTAQ queen". The renamed WAD's argv is "-iwad /storage/roms/doom/Free Doom's Gate.wad", with 0 "unmatched" lines; /workspace/artifacts/m6-t30-20261024/s0-guest.sh, /workspace/artifacts/m6-t30-20261024/s0-guest.out, /workspace/artifacts/m6-t30-20261024/t30/s0/
GUEST-PROOF: 11:07:01 UTC (s0-gzdoom-renamed.out's mtime; s0-scummvm.out 11:05:57, s0-gzdoom.out 11:06:29) -- S0-G2, first frames with the fixed scripts through G14/G15's harness, n=3 each. FOTAQ (ScummVM's splash) +0.59 / 0.66 / 0.69 s. Freedoom 0.94 / 0.99 / 1.00 s. "Free Doom's Gate.wad" 0.92 / 0.99 / 0.95 s, its frame Freedoom 0.13.0's title (opened: gzdoom-renamed-fixed-2-first.png). killall ended each run, the window gone 0.15-0.17 s after; /workspace/artifacts/m6-t30-20261024/s0-scummvm.out, /workspace/artifacts/m6-t30-20261024/s0-gzdoom.out, /workspace/artifacts/m6-t30-20261024/s0-gzdoom-renamed.out, /workspace/artifacts/m6-t30-20261024/s0-frames/

## Stage E, S1 (11:26:44 UTC): the link step keeps what is there (PL-012 #863, PL-029, PL-036, PL-014 #864)

- **The rocknix recipe installs the helper:** `projects/ROCKNIX/packages/rocknix/package.mk:81` is `cp ${PKG_DIR}/sources/scripts/* ${INSTALL}/usr/bin`. A new file there restamps `rocknix`; no recipe changed.
- **The test first:** `tools/s1-fixtures.sh` (`0f592f6da9`) runs the helper and lifts each script's plain variables and link region by marker, under the image's bash, GNU grep and busybox, with `/storage` rewritten to a fixture root. At `6efdc07c2c`: 20 FAIL, 2 controls PASS. On the fixed tree: 22 PASS.
  - **What it caught first:** busybox `cp -a -n src/. tgt/` into an existing target copies nothing, because busybox applies `-n` to the top-level `.`. The helper's first cut used it, and `helper-merge` and all ten sites failed. It now copies file by file. A host GNU `cp` would have hidden this.
  - **Tightened:** two helper cases now require rc 1, because a missing command's 127 passed them vacuously at the base.
- **The changes:**
  - `ce27f80fa2` the helper.
  - The nine F-12 sites: `019020d579` DuckStation's three links, `419c7bfd50` rpcs3, `f3189eb3ad` azahar's four, `ab73a67061` drastic, `7a337f717f` ares, `499d73c342` skyemu, `16b8621e3d` bigpemu, `9e53c110c2` hatari, `6da932bc1f` cemu's four.
  - `a3c443166e` flycast: the old `dc` link inside a real `dreamcast/data` is dropped before the merge, and only the launch's own gptokeyb is killed.
  - `ee1ecc0a88` OpenBOR: only links are removed from `Paks`.
  - `0cd4cafc92` NanoBoyAdvance.
  - `342cbe9670` adds a ROCKNIX line to seven headers. It was missed in the per-script commits and added after them.
  - `bash -n` passes on all thirteen.
- **The brief's premise for NanoBoyAdvance is not what the pin does.** The brief said the emulator runs its HLE BIOS when the file is absent. At `3bb6f478f977`, the SDL frontend prints "Cannot open BIOS" and exits (`src/platform/sdl/main.cpp:180-185`; no ROCKNIX patch changes it).
  - The removed copy was never read: `config.toml`'s `bios_path` is `/storage/roms/bios/gba_bios.bin`.
  - The change is safe either way, and the brief's acceptance is met.
  - The real gap: the image ships an open BIOS at `/usr/config/nanoboyadvance/bios/gba_bios.bin` that nothing points at. It goes to #677 as a finding.
- **The guest cycle S1:**
  - Named on #677 at 11:20:37 (the comment's `created_at`). Host file: last M7 block 05:42. Census 0.
  - Boot at 11:20:49, QEMU pid 1847284.
  - The three fixed scripts and the helper were copied with matching sha256 into an overlay's upper layer (`/storage/t30/s1/upper`), and mounted over `/usr/bin` for part B.
  - `umount /usr/bin` answered "busy": three `evtest` children of `input_sense`, started during part B, held it. It was detached with `umount -l`. Afterwards `/usr/bin` has no helper and the image's `start_duckstation.sh` hash is back.
  - `tools/vm-stop` rc 0 at 11:25:06. Census after: 0.
- **G16 needed a second run.** The P3 script on the guest disk had become 0 bytes since cycle 3, so the first G16 printed nothing. It was copied again (sha256 `1b3558fb968e…` on both sides) and run with the overlay still mounted.
- **P3's control run nested the targets' earlier contents one level down when it restored them** (`…/memcards/memcards/`, `…/savestates/psx/psx/`, at 07:22:39 guest time).
  - The helper run alone on the guest merged and linked flat (`/storage/t30/s1/htest`).
  - No set-aside folder was left from cycle 3. I have not established why P3's `mv` nested this time.
  - The constructed run's lines were read before that step. Its card and state are each one inode, with their bytes, seen under two mount paths (`/storage/roms` and `/storage/games-internal/roms`, inode 210 checked for G8 B).

PROOF: 11:19:37 UTC (s1-fixtures-WORKTREE.out's mtime; the 6efdc07c2c run's at 11:19:35) -- S1-F1, tools/s1-fixtures.sh at 6efdc07c2c: 20 FAIL (the helper absent; all ten sites lose the folder's files, cemu its hidden file; flycast leaves a real data folder; the old kill misses its own gptokeyb; OpenBOR's pak deleted; NanoBoyAdvance makes and keeps the directory), 2 controls PASS; WORKTREE: 22 PASS -- the helper's merge, already-linked, failed copy (rc 1, one line), conflict (both kept) and absent-source cases; ten sites each keep a file and a hidden file and become the link; flycast's two runs; OpenBOR's pak kept; NanoBoyAdvance's four cases; /workspace/artifacts/m6-t30-20261024/s1-fixtures-6efdc07c2c.out, /workspace/artifacts/m6-t30-20261024/s1-fixtures-WORKTREE.out
GUEST-PROOF: 11:21:47 UTC (s1-guest.out's mtime) -- S1-G1, on the guest. With the image's scripts: G8 lost its card (0 copies anywhere); OpenBOR deleted the real pak; flycast left dreamcast/data a real folder, and its kill -9 "$(pidof gptokeyb)" killed the unrelated gptokeyb. With the fixed scripts and the helper (overlay on /usr/bin): G8's card was found under the target only (one inode, two mount paths), memcards a link; the real pak kept; after two launches dreamcast/data -> /storage/roms/bios/dc, the VMU file in bios/dc, no dc link inside it, and the unrelated gptokeyb alive with none of the launches' left; /workspace/artifacts/m6-t30-20261024/s1-guest.sh, /workspace/artifacts/m6-t30-20261024/s1-guest.out, /workspace/artifacts/m6-t30-20261024/t30/s1/
GUEST-PROOF: 11:23:03 UTC (s1-g16.out's mtime) -- S1-G2, G16 with the fixed scripts: the Tools launcher made savestates a real folder; a synthetic card and state were placed; after the game launch memcards -> /storage/roms/psx/duckstation/memcards and savestates -> /storage/roms/savestates/psx, the card and the state kept, each one file seen under two mount paths (cycle 3, unfixed: 0 and 0); /workspace/artifacts/m6-t30-20261024/p3-tools-then-game.sh, /workspace/artifacts/m6-t30-20261024/s1-g16.out

## Stage E, S2 (11:38:34 UTC): every kill target names a process (PL-001 #853, PL-002 #854, PL-003 #855, PL-004 #856, PL-030 #867)

- **The test first:** `tools/s2-fixtures.sh` (`511370b0e7`, Steam) sources the real `start_steam.sh` and runs each wrapper's real lines with stubs recording their calls. At `017d8f921d`: 2 FAIL; neither `steam_dual_screen_end` nor the binfmt restore runs. Fixed: 2 PASS.
  - Its first cut lifted the x86 wrapper only to its first `systemd-binfmt` line, the `stop` before the launch, so it never reached the session. It now lifts to the restore line.
- **The changes**, one commit per package:
  - `3ba3eef736` DuckStation's two kill lines (upstream `4a6415c033`).
  - `9598a24df5` OpenBOR: sources the profile, `set_kill set "-9 OpenBOR"`, and kills gptokeyb by PID. `runemu.sh` runs it with bash, so its `/bin/sh` (dash on the image) shebang doesn't matter.
  - `827f93d13a` Mupen64Plus (upstream `eeb33c5a37`), plus a ROCKNIX header line.
  - `a149cc76d5` hatarisa's rename and kill target (upstream `2e7041d273`). The recipe line restamps `hatarisa`; `tools/pkgcheck hatarisa` rc 0, unpiped.
  - `b0ae783c5e` Steam: `return "${steam_exit_code}"` in both branches, and the x86 kill target `-9 FEX gamescope steam`. `start_steam_arm64.sh` needed no edit, because its restore runs once the function returns.
  - The first hatarisa commit failed (`git add` of the renamed-away path). It was recut by directory pathspec, with nothing else staged.
- **The guest cycle S2:**
  - Named on #677 at 11:34:07 (`created_at`). Host file: last M7 block 05:42. Census 0.
  - Boot at 11:34:20, QEMU pid 1943861.
  - EmuTOS 1.4 192k US (`/workspace/tmp/m6-t30/content/emutos/`) was copied as `tos.img`. Its zip's sha1 `6f146a126065…` matches SourceForge's listing; the image's sha256 is `8fbbf8b44fc3…` on both sides.
  - The four fixed scripts and the helper went into an overlay on `/usr/bin`, detached with `umount -l` after the frames.
  - `tos.img` and the substitute were removed.
  - `tools/vm-stop` rc 0 at 11:37:08. Census after: 0.
- **G6 in the kill cases could not test.** The synthetic ROM makes Mupen64Plus exit (rc 10) before a kill can be sent, and `runemu.sh` then restores `emulationstation` as the target. G6 therefore ran each version's own `set_kill` line, then `killall`, against a **substitute** process named `mupen64plus-simple` (a renamed python3). The fixed version ran first, then the image's after the overlay came off.
- **hatarisa exited between +4 s and +6 s in the three frame runs.** The kill case had caught it alive at +4 s and ended it. Its log names no reason. Not explained.

PROOF: 11:32:25 UTC (s2-fixtures-WORKTREE.out's mtime; the 017d8f921d run's at 11:32:25) -- S2-F1, tools/s2-fixtures.sh at 017d8f921d: x86 and arm64 FAIL (gamescope 1, essway start 1, dual_screen_end 0, binfmt 0); WORKTREE: both PASS, steam_dual_screen_end and then the binfmt start (x86) or restart (arm64) recorded after the session returns, each once; /workspace/artifacts/m6-t30-20261024/s2-fixtures-017d8f921d.out, /workspace/artifacts/m6-t30-20261024/s2-fixtures-WORKTREE.out
GUEST-PROOF: 11:35:39 UTC (s2-guest.out's mtime) -- S2-G1, the kill cases through runemu.sh with input_sense's killall ${TO_KILL}. The image's scripts: DuckStation kill data "-9 AppRun.wrapped", killall rc 1, AppRun ALIVE; OpenBOR no kill data; hatarisa exit 127 ("No such file"). The fixed scripts: DuckStation "-9 duckstation-qt" rc 0, ended; OpenBOR "-9 OpenBOR" rc 0, ended; hatarisa started on EmuTOS, "-9 hatarisa" rc 0, ended; /workspace/artifacts/m6-t30-20261024/s2-guest.sh, /workspace/artifacts/m6-t30-20261024/s2-guest.out, /workspace/artifacts/m6-t30-20261024/t30/s2/
GUEST-PROOF: 11:36:35 UTC (s2-g6.out's mtime) -- S2-G2, G6 with a SUBSTITUTE named mupen64plus-simple (a renamed python3, comm "mupen64plus-sim"): the fixed kill line "-9 mupen64plus mupen64plus-simple" ended it; the image's "-9 mupen64plus" left it ALIVE; /workspace/artifacts/m6-t30-20261024/s2-g6.sh, /workspace/artifacts/m6-t30-20261024/s2-g6.out
GUEST-PROOF: 11:36:30 UTC (s2-hatarisa.out's mtime) -- S2-G3, hatarisa's first frame through the cycle-2 harness, n=3: 0.39 / 0.42 / 0.36 s after the launch call, the frame EmuTOS drawing its banner (opened: hatarisa-fixed-2-first.png); hatarisa had exited by +6 s each time, so no kill was sent there; /workspace/artifacts/m6-t30-20261024/s2-hatarisa.out, /workspace/artifacts/m6-t30-20261024/s2-frames/

## Stage E, S3 (11:48:28 UTC): achievements, the session and the credentials (PL-009, PL-010 #861, PL-021, PL-039 #870, PL-020 #866, PL-034, PL-037)

- **The test first:** `tools/s3-fixtures.sh` (`a64fd36cf4`) runs ppsspp's, flycast's, ARMSX2's, SkyEmu's and DuckStation's achievements scripts whole, plus melonDS's `set_key` lines, under the image's bash, GNU grep and busybox. `get_setting` answers from a fixture file. Every sign-in value is synthetic, and the checks count lines rather than print values; `grep` for the synthetic values in both outputs gives 0. At `03141ed056`: 15 FAIL. Fixed: 15 PASS.
  - **Tightened:** DuckStation's switch-unset case passed vacuously at the base. The unquoted test, with an empty value, compares `"!"` and `"1"`, which is false, so the script reached rc 1 through the token check instead. The case now requires the disabled branch's own log line.
- **The changes:**
  - ppsspp `619e20ced8`, flycast `fd23630624`, armsx2 `ff6f4d9c1e`: a disabled session is published when the switch is off or the token empty (dolphin's `publish_disabled` shape), and the achievements keys are written by `write_section`. That is an awk writer reading the values from the environment, ending the section at the next header, keeping every other key, and replacing the file by temp and rename.
  - armsx2: its token writer is unchanged inside but wrapped as `write_token`, which is also used to clear the token.
  - skyemu `d0f95815a1`: `write_private`, temp and rename, mode 0600.
  - DuckStation `974866ef81`: the quoted test, and PL-037's comment above the disabling line (upstream's `0c3c2b6818`).
  - melonDS `c4367e12a0`: `set_key` takes raw values and escapes `|`, `\` and `&` only for sed.
  - aethersx2's script is not touched (PL-025, class 1).
- **PL-034, decided by reading: confirmed.** Filed as **#887**, for the cloud area.
  1. `start_melonds.sh:182` deletes `melonDS.toml` on every launch.
  2. At the pin `906e9ebb27da`, `Config::Load()` then calls `LoadLegacy()`. (`src/frontend/qt_sdl/Config.cpp` was fetched into `/workspace/tmp/m6-t30/fetch/melonds-906e9eb/`, sha256 `3d766f24f684…`; the shared cache holds only `bdd85c9c`.)
  3. The patch maps `RA_Password` and `RA_Token` into `RetroAchievements.Password` and `.Token` (`000-retro-achievements.patch:7520-7522`).
  4. The patch's `main.cpp` calls `Config::Save()` every 60 s of a game with an achievements ID (patch line 9879), and `RASettingsDialog.cpp` calls it on accept (line 8851).
  5. `backuptool:705-710`'s `RATOKENSETTINGS` lists `melonDS.ini` but not `melonDS.toml`.
- **No guest cycle for S3,** as the brief names: these scripts' emulators are fixture-proved.

PROOF: 11:47:27 UTC (s3-fixtures-WORKTREE.out's mtime; the 03141ed056 run's at 11:47:27) -- S3-F1, tools/s3-fixtures.sh at 03141ed056: 15 FAIL (each of the four scripts keeps the old token signed out and off; flycast's and ARMSX2's empty switch key falls through as enabled, DuckStation's too; the token file keeps its mode and is written twice; a token holding / & and a backslash is mangled; ARMSX2's first section lacks three keys; melonDS's set_key mangles | and \\ on both paths); WORKTREE: 15 PASS, 0 old-token lines and a disabled flag in each, ppsspp's token file mode 600 with one temp write, the bytes intact everywhere, the other keys and sections kept; /workspace/artifacts/m6-t30-20261024/s3-fixtures-03141ed056.out, /workspace/artifacts/m6-t30-20261024/s3-fixtures-WORKTREE.out

## Stage E, S4 (12:09:06 UTC): the launch scripts do what they say (PL-006 #858, PL-011 #862, PL-015, PL-017, PL-028, PL-032 #868, PL-033 #869, PL-038, PL-040, PL-041 #871; PL-014b #886)

- **The test first:** `tools/s4-fixtures.sh` (`fb5e1ce22c`, file loop fixed in `09586ffbbf`), 20 cases. At `3429d4f29e`: 18 FAIL, plus 2 controls PASS (Dolphin's GameSettings, and a player BIOS the old config already named). On the fixed tree: 19 PASS and 1 FAIL, the melonDS TOML question below. Earlier on #677 I said 21 PASS; that was a miscount, and the case count is 20.
  - **Fixture faults found and fixed:** the path rewrite hit the fixture root, which lives under `/workspace/tmp`, until `/tmp` was rewritten first. The VDF case rewrote an escaped `\/storage` inside a sed replacement. The redirection grep split `Start Duckstation.sh` on its space.
- **The changes**, one commit per package:
  - `819e2397bf` Mupen64Plus: upstream's `unzip -qql` line (ROCKNIX `195a8eba4b`), checked under the image's busybox for 8- and 9-digit sizes; the ROM run in place; `--configdir` in `/storage`.
  - `49d8a87f2b` amiberry.
  - `156971040a`, `78efb93d77`, `f8b777c353`, `3e4eac7f8b`: the ten redirection tests. No option in the tree offers `screen_orientation`, `internal_resolution` or `screen_rotation`, so the numeric reading changes only a value of exactly `0` or a non-number, both of which take the default.
  - `b30dc0a66b` Dolphin's swap, once, in both scripts.
  - `e0e9f6d167` DraStic.
  - `e942dbdf12` xemu.
  - `5771c915ec` ScummVM.
  - `6b646ac212` NanoBoyAdvance (PL-014b). The recipe's check is a trust-on-first-use sha256 `661a9afb…`, equal in a fresh fetch and two SM8550 build roots, and it restamps the package (pkgcheck rc 0).
  - `cfb1c0ff48` hatarisa.
  - `8047c0794d` the other F-42 sites.
  - Seven ROCKNIX header lines went in with their scripts. `bash -n` passes on all.
- **PL-038:**
  - xemu: fixed.
  - Dolphin: F-39's claim does not hold at `reviewed-at`, because lines 72-76 already copy only what is absent; withdrawn, with the fixture's control showing it.
  - **melonDS: open.** `start_melonds.sh:181-182` deletes the TOML on purpose ("temporary hack"), so that melonDS rebuilds it from `melonDS.ini`, where the script writes EmulationStation's settings. Keeping the TOML would stop those settings applying. Put to the coordinator on #677.
- **PL-041, the F-42 rows, each fixed or withdrawn:**
  1. hypseus: the device-name path and the arithmetic, fixed (fixture). `.commands` read as words, fixed [tree].
  2. `cheevos_armsx2.sh` and `cheevos_dolphin.sh`, publication failures and temp files: withdrawn. Dolphin already refuses a launch it cannot configure, and ARMSX2 logs and launches as the other emulators do. The temp file sits beside its target so the rename is atomic on one filesystem, and `.$$` is unique per launch.
  3. Daedalus `rm` without `-r`: fixed by `link_storage_dir` [tree].
  4. amiberry and Hatari floppies: `printf` lines from disk images only, fixed [tree]. Writes to the deleted temp tree are withdrawn: keeping an unzipped disk's writes needs a decision about where unzipped disks live.
  5. DS archives (dsperate, melonDS): extraction checked, `-iname` at any depth, fixed [tree].
  6. Backslashes stripped (ppsspp, vice): fixed [tree]. EmulationStation passes paths unescaped: S0's `exec.log` `ARG1` was `/storage/roms/scummvm/Flight of the Amazon Queen.scummvm`.
  7. VSync read but not applied (armsx2, cemu; aethersx2 is class 1): withdrawn. Applying it changes rendering on devices the VM cannot show; it's a feature gap, and no data is lost.
  8. cemu forwards the platform: fixed [tree].
  9. gzdoom's pk3 test: quoted, fixed [tree].
  10. pico-8's splore match: fixed (fixture).
  11. Vita3K: the zip installed from its own folder, no `-r ""`, `mv -n`; fixed [tree].
  12. RPCS3's M3U: fixed (fixture).
  13. Emulator status discarded: withdrawn. Propagating it would make every hotkey exit (SIGKILL, 137) a failure in `runemu.sh`'s error check, which is T1's file.
  14. melonDS's last line: fixed (fixture).
  15. Steam's VDF index: fixed (fixture).
  16. `input_sense`'s debounce: withdrawn; T1's file, noted for its owner.
  17. Compositor replies evaluated: withdrawn as a note. It's a trust seam, and the fields are numbers and sway's own transform keyword.
  18. gzdoom's banner: withdrawn. It's cosmetic, the build's `git describe`.
  19. Hatari's config seed: fixed [tree].
  20. yabasanshiro's `cp`: quoted, fixed [tree].
- **The guest cycle S4:**
  - Named on #677 at 12:06:26 (`created_at`). Host file: last M7 block 05:42. Census 0.
  - Boot at 12:06:39, QEMU pid 2329855.
  - The fixed scripts went into an overlay on `/usr/bin`, detached with `umount -l`. ScummVM's config was set aside and restored.
  - `tools/vm-stop` rc 0 at 12:08:12. Census after: 0.
  - The guest's pad does not need the face swap, so Dolphin's flip can't show there. The fixture proves it with a pad row where a>b.

PROOF: 12:05:39 UTC (s4-fixtures-WORKTREE.out's mtime; the 3429d4f29e run's at 12:05:38) -- S4-F1, tools/s4-fixtures.sh at 3429d4f29e: 18 FAIL, 2 controls PASS; WORKTREE: 19 PASS (Mupen64Plus's zip member and in-place ROM with the config in /storage; the ten tests make no file and the acceptance grep is empty; amiberry's keys and kept config; mednafen [tree]; DraStic's refresh; Dolphin's swap once and the normalisation; xemu's and GameSettings' settings kept; NanoBoyAdvance's BIOS choice and the recipe's check; the F-42 cases), 1 FAIL (melonDS.toml, open); /workspace/artifacts/m6-t30-20261024/s4-fixtures-3429d4f29e.out, /workspace/artifacts/m6-t30-20261024/s4-fixtures-WORKTREE.out
GUEST-PROOF: 12:07:56 UTC (s4-guest.out's mtime) -- S4-G1, on the guest. The image's scripts: the zipped ROM never got a launch line; "Zippy Race.z64" was taken for a zip (nothing to run); mupen64plus.cfg copied into /tmp/mupen64plus; ScummVM with its config dir absent got only what ScummVM writes itself (games, scummvm.ini), no seed. The fixed scripts: "Launching mupen64plus with /tmp/mupen64plus/Wave Race.z64"; "Launching mupen64plus with /storage/roms/n64/Zippy Race.z64" with no copy in /tmp/mupen64plus; ScummVM seeded from /usr/config/scummvm (themes present); Dolphin's Hotkeys.ini identical across two launches (sha1 1147e8789eed, no swap wanted by this pad); /workspace/artifacts/m6-t30-20261024/s4-guest.sh, /workspace/artifacts/m6-t30-20261024/s4-guest.out, /workspace/artifacts/m6-t30-20261024/t30/s4/

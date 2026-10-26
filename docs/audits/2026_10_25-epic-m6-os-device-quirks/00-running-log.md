# Running log — M6.P2 T29, the per-handheld quirks (#676)

- **Executor:** Opus 5.5 (`claude-opus-5-5`) at high effort, the T5 session (`m6-t5-build-engine`), after T28's close-out.
- **Brief:** `docs/reviews/briefs/os-device-quirks.md`, version 2 (`feefe8fd13`). **Dispatch:** the coordinator's comment on #676, 11:47 UTC on 2026-10-25 (issuecomment-6397234711).
- **Depth:** Independent, with one seat (GPT-6 Astra at `max`) over a trimmed, scanned packet (D-WORKFLOW-195).
  - **Exactly one keyed `tools/council/run invoke` pair:** the probe and the refutation, at stage C.
  - Every other `tools/council/run` call runs with `COUNCIL_ENV_FILE=/nonexistent`.
- **`reviewed-at`:** `5ee0dfefcf`, the dispatch tip. The read is of `8ebaf8daad`'s bytes: the branch-vs-hash diff over the 333 is empty (r03, path-safe with `xargs -0`), and so is `git diff --stat 8ebaf8daad HEAD -- packages projects`. Upstream is read at `651150fc88` and the base at `c445081a59`, locally. No fetch.
- **Can this be done on the VM? Yes, on the host, with no network.**
  - Every read and count runs on the build host at `8ebaf8daad`, with `651150fc88` read locally.
  - A `bin/` helper's behaviour is proven with `tools/nova-led-test`'s fixture shape (sysfs under a scratch root), never on the Nova.
  - The VM's two files' control flow is T22's guest record, cited.
  - A boot-only behaviour the lane names can ask for one window on #676. **No guest is planned.** Nothing runs on a person's device (D-QA-015).
- **What never runs here:** a build, a compiler, a plan generation, a fetch, a network read of any upstream, a guest outside a window granted on #676, a command against a handheld, an M7 build root read, a keyed `tools/council/run` call beyond the seat's two, or a change under `packages/`, `projects/` or `tools/` at stages A to D.
- **Counts are taken unfiltered.** The credential filter drops lines carrying `user` or `key`; only a quoted line goes through the mask.
- **The host:** the host file's last line at 11:48 is the coordinator's 10:24 UTC *T22 SECOND GUEST WINDOW RETURN ... M6 runs no guest now*. Census: qemu live 0; `/tmp` inodes 41 %.
- **Scratch:** `TMPDIR=/workspace/tmp/m6-t29/tmp`, `.qa-scratch/t29/`; copies in `stage-a/`.
- **Proofs:** each proof in `02`'s § Proofs has one numbered proof line here, in its stage.

## [Stage A] 11:48:01 to 11:50 UTC — the first commands, the block, the runs

- **The first commands** (brief § 1), 11:48:01:
  - the status is clean (0);
  - the tip is `5ee0dfefcf`, on `453e25a000` and `feefe8fd13`;
  - stacked on `8ebaf8daad` and on P1's `2174265e9c`;
  - `651150fc88` is present; T22's `02` is reachable (994 table rows); `register-check` ok.
  - **Delta:** `git diff --stat 8ebaf8daad HEAD -- packages projects tools` is not empty but `15 files changed, 2130 insertions(+), 8 deletions(-)`. All 15 are P1's own files under `tools/` (`renovation-inventory` and the lint's renovation fixtures, `9966dbcd12` to `61d1d016eb`, #641). Under `packages projects` the diff is empty, so the 333 are untouched.
- **The runs:** `stage-a/runs.sh`, 22 steps, each with its exit and wall time (`stage-a/runs.tsv`). **All exit 0.**
  - The brief's three Python blocks are copied verbatim (`scope.sh`, `tiers.sh`, `shape.sh`).
  - r21 and r22 are the lane's additions: the four `model` strings patch `0154` carries, and the board count.
- **The block** (r01, r02):
  - `paths 333 lines 10175 {'shipped': 333} {'upstream-carried': 328, 'fork-own': 5}`;
  - `{'symlink': 48, 'shell': 266, 'none': 12, 'other': 7}`;
  - `read 266 9327 fork-own 5` (the brief's "fork-own 389" is lines; the block prints the five paths);
  - `entries 88 of which top-level symlinks 23`; `paths.txt` 333, `entries.tsv` 88.
- r03 `[]`. r04: 88 entries, 23 top-level symlinks, 48 symlinks in all.
- **The selection lines** (r05 to r08): `002-autostart:6-12`, `autostart:31-43` (its `-f` at the window's line 8), `package.mk:15-20`, and the wrapper's `exec ... $*`.
- **The boards** (r09 to r11, r21, r22):
  - 28 `model =` lines in all: 24 in the fork trees and 4 in patch `0154`'s context. One is the `AYN-Thor` sub-node, and `Anbernic RG34XX-SP` appears twice.
  - **26 distinct boards: 15 HAS, 11 NONE.** NONE are RG28XX, RG34XX, RG34XX-SP, RG35XX Pro, RG-SP, AYANEO Pocket S 1K, AYN Odin 2 Mini, and `0154`'s RG35XX 2024, H, Plus and SP.
  - **`Anbernic RG35XX SP` and `Anbernic RG-SP`, the two owned H700 units, select no device entry.** The QEMU DMI pair HAS.
  - **Delta:** the brief's "29 `model =` strings ... of the 28 boards" counts lines (28) and boards wrongly. Its loop read only the trees, so the four `0154` strings were added as r21.
- r12 **the tiers:** `A (6, 396, 5)`, `B (70, 2885, 5)`, `rest 263`.
- **History:**
  - r13, over the 333: 6 fork commits since the base; since June 28 non-merge, 6 the fork's.
  - r14, over the directory: 9; 32, 9 the fork's.
- **The delta:**
  - r15: `16 A 3 D 12 M`, 18 commits pending, 12 without merges.
  - r16: `AYN Thor/040-panel_calibration` and `Retroid Pocket 6/040-panel_calibration`.
- **The shape** (r17):
  - modes `120000 48, 100755 214, 100644 71`, 285 blobs;
  - shebangs `#!/bin/sh` 256, `#!/bin/bash` 10, 266 shell files;
  - over the blobs: `/storage` 156, `DEVICE_` 104, `/etc/profile` 89, `set_setting` 46, `/sys` writers 32, guard 1;
  - over the shell: 145, 101, 89, 46, 32, 1.
- r18: `050-game-configs` 16, `050-game_configs` 12. r19: `tools/nova-led-test` 68 lines, naming the Nova's `bin` (`:16`). r20: `[]` against the dispatch tip.
- **Nothing of the never-run list ran.**
- PROOF: P1, the membership: r01, r02, r04.
- PROOF: P2, the history and the delta: r13 to r16.

## [Stage B] 2026-10-25 11:52 to 11:57 UTC, cut; resumed 2026-10-26 04:50 to 04:55 UTC — the tier-B read, the generator, the findings

- **The cut.** An API rate limit cut the session at 11:57 UTC on the 25th, while `02` was being written. The worktree stayed at `e8dcd0ace5`, with `tools/` untracked (the two generators) and the scratch intact. Resumed at 04:50 UTC on the 26th on the coordinator's prompt.
- **The host** was handed to M7 for a bounded window (the host file's 04:47 blocks). This lane did host-only reads and Python. The live QEMU on the host is T16's (pid 4160936), not touched.
- **The tier-B read:** 70 paths as 26 distinct blobs, 1,692 lines, each read once with its sharers noted. The fork-own five were read whole.
- **The fixture:** `tools/t29-battery-unset.py`, run at 11:54:26 on the 25th and again in b04. The Nova's `battery_led_status` with `led.color` unset lights all eight LEDs green at 255. The `rgb` control stays unlit, and upstream's RP6 copy behaves the same.
- **The reads:** `stage-b/reads.sh`, 16 steps, all rc 0 (`stage-b/runs.tsv`). b03 found 4 `led.color` lines outside the quirks, all reads (`led_flash:7`, `rocknix-fake-suspend:140`, `powerstate.sh:16`, a comment), so nothing seeds a default.
- **The generator:** `tools/t29-tables.py`, sections `entries` (88, asserting 333 / 88 / 65 / 23), `boards` (28 / 26 / 15), `delta` (31: 16 A 3 D 12 M), `coverage` (333), `runs` (22) and `counts`; `check` same.
- **Deltas found at stage B:**
  - `AYN Thor/touchcontrol` is a file the loop runs;
  - `rocknix-info:12` has the `/` → `-` sed the brief says is absent.
- **Corrected before commit:**
  - F-03's tier-B count (four, not five) and F-01's (seven tier-B copies, not four), against b07 and b02;
  - `03`'s restore seam, which said a backup carries `profile.d`. `backuptool:288` carries `retroarch/*`, and `profile.d` is not in its list.
- **Findings:** ten. F-01 (a candidate bug, fork-own), F-03 and F-04 Low; seven Info.
- **Nothing of the never-run list ran.** `git diff --stat 5ee0dfefcf HEAD -- packages projects tools` is empty.
- PROOF: P3, the branch and the removal rule: r03, r20.
- PROOF: P4, the selection lines: r05 to r08.
- PROOF: P5, 26 boards, 15 HAS, 11 NONE: r09 to r11, r21, r22, `boards`.
- PROOF: P6, the tiers: r12, b01.
- PROOF: P7, the fork-own five read whole: b15 and the files.
- PROOF: P8, the battery loop at boot: b02, b03, b04 (fixture).
- PROOF: P9, the owned H700 units: b05, b06.
- PROOF: P10, tier B's Q2 shapes: b07 to b11.
- PROOF: P11, the shape and the weight: r17, r18, b12.
- PROOF: P12, the delta's 31 paths and 18 commits: `delta`, b13.
- PROOF: P13, `rocknix-info`'s derivation: b14.
- PROOF: P14, the tables regenerated: `check` 0.

## [Stage C] 2026-10-26 04:57 UTC onward — the packet, its scan, the seat

- **The packet** (`stage-c/packet.py`, from `stage-c/ask.md`), `second-opinions/gpt-brief.md`: 53 sources, 178,989 bytes, sha256 `cd419005518031bc...`. Built 04:57:11 UTC.
  - **Contents:** the ask; `02` whole but for its 333-row coverage table, trimmed to a note (D-WORKFLOW-195); `03` and `04` whole; four context sections (the order's § T29, the brief's § 2 and § 4, 8 register rows, device facts L14, L16, L27 and L31).
  - **Line-numbered:** tier B's symlinks and its 26 distinct blobs, each with the paths that share it; the fixture and its output; 16 excerpts (the selection lines, the wrappers, the unit, `platforms/H700`'s three files and `bin/ledcontrol`, `call_achievements_hooks.sh`, `rocknix-info`, `backuptool:278-310`, `powerstate.sh`, the x55's guard, Odin 3's `050-game-configs`).
  - **Masking:** 1 line masked, the brief's `key=lambda`.
- **The scan** (04:57:19): `forbidden-terms-check --stdin` 0 hits. `SECRET_PATTERNS`: 0 lines under the three sets, each matching a run-time fake line. Recorded in `packet-manifest.json`.
- **The plan:** `second-opinions/review-plan.json`, independent, one reviewer (`gpt`, `openai/gpt-6-astra`, `max`, pinned to OpenAI), written before the first call.
- **The runner:** `tools/council/node_modules` was copied from the T28 worktree (gitignored; the tracked `tools/council` is identical). `COUNCIL_ENV_FILE=/nonexistent tools/council/run verify-pins`: `OK`.
- **The probe**, 04:57:41 to 04:57:52 (keyed; **the first of the seat's two calls**): `http=200 model=openai/gpt-6-astra providers=["OpenAI"] effort=max finish=stop outcome=success`. Verification, effort and provider `PASS`; `council-facilitator@1.14.1-pixelelated.2`.
- **The refutation**, started 04:57:57 UTC (keyed; **the second and last call**), runs as a harness background task. It writes `second-opinions/gpt-audit.md` and `/workspace/tmp/m6-t29/refutation.rc`.

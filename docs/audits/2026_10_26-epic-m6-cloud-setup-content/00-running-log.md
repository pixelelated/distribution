# Running log — M6.P2 T17, cloud setup, sign-in, connections, content and settings backups (#664)

- **Executor:** Opus 5.5 (`claude-opus-5-5`) at high effort, the T5 session (`m6-t5-build-engine`), after T29's close-out.
- **Brief:** `docs/reviews/briefs/cloud-setup-content.md`, version 2 (`71ded3ac40`). **Dispatch:** the coordinator's comment on #664, 06:12:10 UTC on 2026-10-26.
- **Depth:** Extended. Two seats over a trimmed, scanned packet (D-WORKFLOW-195): GPT-6 Astra at `max`, then Gemini 4 Argon at `high`, each a probe then one refutation.
  - **Exactly four keyed `tools/council/run invoke` calls**, at stage C.
  - Every other `tools/council/run` call runs with `COUNCIL_ENV_FILE=/nonexistent`, `--help` included; the runtime comes from `npm install --offline`, with no fetch.
- **`reviewed-at`:** the dispatch tip `f3803436b8`. The read is of `8ebaf8daad`'s bytes: the branch-against-read diff over the 14 is empty (r40, with `xargs -0`).
- **Can this be done on the VM? Yes -- the host first, then one guest, after two other windows.**
  - Every read, count and fixture runs on the host, with no network. The five fork tools run with synthetic real-rclone controls, each recording which rclone it ran.
  - The GENERIC_X64 guest runs the same scripts, busybox, rclone 1.75.2, sway and webkitgtk as a handheld, against `tools/cloud-test-backend`'s WebDAV, SFTP and MinIO/S3 (D-QA-058: no hosted account; a provider's real OAuth page is an unverified follow-up, not a "no").
  - The window is asked for on #664 after stage B. It runs only after M7's guest RETURN on the host file and after T16's re-granted window.
  - Nothing runs on a person's device or cloud (D-QA-015; blindspot 38 is this slice's own history).
  - The phone page from the host is `CANNOT`, with the gap named, unless the harness can reach it.
- **What never runs here:** a build, a compiler, a plan generation, a fetch, a network read beyond the four seat calls, a hosted or offsite cloud account, a provider's sign-in page with an account behind it, `--real-roms`, `cloud-census`, a command against a handheld or a person's cloud, a read of an M7 build root or worktree, a guest outside the one granted window or before M7's RETURN, a keyed `tools/council/run` call beyond the four, a credential-shaped literal written to any file at rest, and a change under `packages/`, `projects/` or `tools/` at stages A to D.
- **The read filter.** Counts of `key`, `pass`, `token`, `user`, `psk` and `secret` are taken unfiltered. Every run that prints source lines passes them through `grep -v -i -E 'key|pass|token|user|psk'` (D-QA-021), and a finding names file:line and the shape, never the line (D-WORKFLOW-061).
- **Scratch:** `TMPDIR=/workspace/tmp/m6-t17/tmp`, `.qa-scratch/t17/` (gitignored); copies in `stage-a/`. `/workspace` inodes 24 % used at 06:12.
- **Proofs:** each proof in `02`'s § Proofs has one numbered proof line here, in its stage.

## [Stage A] 06:12 to 06:20 UTC — the first commands, the block, the runs

- **The host** at 06:12:51 UTC:
  - the host file's last line is M7's `2026-10-26T06:06:11 ... native-stage RETURN: three changed ES objects compiled and cached binary relinked ...`, after the coordinator's 05:58 acknowledgement of M7's native checks under the 04:47 handoff;
  - census: qemu live 1 (T16's idle guest, awaiting the owner's stop; not this lane's), compilers 0.
  - This lane started no process on the host but `git`, `python3 -I` and the shell.
- **The first commands** (brief § 1):
  - the status is clean (0); the tip is `f3803436b8`, on `3c8a28918f` (the coordinator's `608315f65f` merged);
  - stacked on `8ebaf8daad` and on P1's `2174265e9c`;
  - `packages/` and `projects/` against `8ebaf8daad`: empty;
  - `tools/` against `8ebaf8daad`: `15 files changed, 2130 insertions(+), 8 deletions(-)`, P1's own files, as the brief says;
  - `651150fc88` is present, read locally;
  - T13's `04` is reachable (124 table rows); `register-check` ok.
- **The rules.** `git diff --quiet next -- .claude CLAUDE.md AGENTS.md` reports a difference, but `git log HEAD..next -- .claude CLAUDE.md AGENTS.md` is empty. The branch's rules are `next`'s plus M6's edits, not older than `next`'s.
- **The runs:** `stage-a/runs.sh`, 40 steps, each with its exit and wall time (`stage-a/out/runs.tsv`). **All exit 0.** The brief's § 2 block is copied verbatim as `stage-a/scope.py`.
- **What held** (brief § 2 and § 5, every figure):
  - 14 paths, 11,180 lines, shipped 14, fork-own 14; the rclone directory's 25 rows, 11 of them this slice's;
  - modes 10 × `100755` and 4 × `100644`;
  - shell functions 112 strict and 147 loose; python 124 defs, 9 classes;
  - `set -o pipefail` global only at `cloud_log_scrub:63`, with local subshells at `cloud_setup:556` and `backuptool:492/504/537/1177`; no global `set -e` or `set -u`;
  - the writers: `cloud_connections.py:20/74/80/160/241`, `cloud_oauth:193`; `cloud_setup`'s six non-comment `rclone config` lines are two reads, the `pkill` and three echoes;
  - the deleting statements: `cloud_content_restore:750` (the dry run), `:1015`, `:1046`; `--delete-excluded` one hit, the comment at `:528`;
  - 12 `rm -rf` sites; the pattern kills at `cloud_setup:775-776` and `cloud_oauth:357/2819` (`:861` a docstring); the five unquoted sites;
  - the OAuth constants and bounds; `backuptool`'s lists, `ARCHIVE_KEEP=3`, the `5)` arm, 37 `logger -t backuptool` lines;
  - the history, 284 non-merge (265 / 12 / 7), 2026-07-25 to 2026-10-13, the same since June, `backuptool` 79;
  - upstream: only `backuptool` in `651150fc88` and `c445081a59`, 68 lines, identical; `14 files changed, 26 insertions(+), 11138 deletions(-)`;
  - 19 callers; the install lines; T13's rows naming these scripts: 5; `BACK UP` 7, `BACKUP` 38;
  - each file's sourced files.
- **Deltas found at stage A** (`01` § Deltas):
  1. **15 `.$$` lines in the 14, not 14** (r16). `cloud_content_restore:819` carries the name on the `printf` line that opens the plan's temp write.
  2. **One of `backuptool`'s ten `rm -rf` is not on `${STAGING}`:** `:224` sweeps `"${STAGING_PREFIX}"*`. That is `/storage/.cache/backuptool-staging.` (`:762`), the script's own staging prefix. It is defined below the function that uses it, which is called later (blindspot 24's shape; safe here).
  3. **r07 reads the whole directory**, as the brief writes it, so it also prints T16's files (`cloud_backup:20`, `cloud_capture:221`, `cloud_net_ready:54`, `cloud_restore:21`). Within the 14 it is as the brief says.
  4. **`tools/vocabulary-check`'s default EmulationStation checkout exists** on the host (`~/Development/emulationstation-next.worktrees/qa-integration`), and `ES_SRC` is unset. The lane did not read it: whose worktree it is, M7's or the lane's to read, is the coordinator's to say. r37 records `CANNOT` as the brief prescribes.
- **Nothing of the never-run list ran.** `git diff --stat f3803436b8 HEAD -- packages projects tools` is empty (r39).
- PROOF: P1, the membership: r01 (14 / 11,180 / fork-own 14 / shipped 14; the directory's 25 of which 11).
- PROOF: P2, the lines, modes and functions: r02 to r05.
- PROOF: P3, the history with the three identities: r25 to r28.
- PROOF: P4, the upstream relation: r29 to r31.
- PROOF: P5, the callers and the tools' invoking counts: r32 to r35.
- PROOF: P6, the branch and the removal rule: r39, r40.

## [Stage B] 2026-10-26 06:16 UTC onward — the read of the 14, the tables

- **Stage A accepted** (the coordinator, 06:2x UTC). The deltas go into the brief's errata. **`tools/vocabulary-check` against the ES checkout is allowed as a read**, with its provenance recorded first.
- **The ES checkout's provenance**, 06:17:44 UTC: `~/Development/emulationstation-next.worktrees/qa-integration` is at `HEAD` `16dbac5211eea7e70db7394372033be2be7df829` on `test/qa-integration`, with `git status --short` 0 lines. `emulationstation/package.mk` at `8ebaf8daad` pins `PKG_VERSION="16dbac5211..."` on the same branch, so **the HEAD is the pin and the tree is clean**: the verdict stands as the image's. No git command that writes ran there; status read 0 lines again after the run.
- **`tools/vocabulary-check --es <that path>`**, 06:17:50 UTC: **exit 0**, `163 string(s) with back up / backup, save state or Wi-Fi judged, 0 wrong`, and one allowed string (upstream's hidden `GuiBackupStart`). The output, masked, is `stage-b/vocabulary-check.txt`.
  - It reads `cloud_content_backup`, `cloud_content_restore`, `cloud_setup` and `backuptool` from this slice. The other ten are read by hand against `es-player-text.md`; that row stays `CANNOT` for the tool.

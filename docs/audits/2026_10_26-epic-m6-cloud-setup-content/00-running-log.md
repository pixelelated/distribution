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
- **The read:** all 14 files whole, in the brief's lens order, 11,180 lines; the reading record is `stage-b/read-notes.md`.
- **The five fork tools** (`stage-b/tools.sh`, 06:25:41 to 06:26:17 UTC): `cloud-connections-test` 26 OK and `cloud-input-test` 9 OK on the host's rclone 1.60.1-DEV (hard-coded by the first); `pixelelated-save-layout-test` 39 PASS on the donor's rclone 1.75.2; `pixelelated-content-scope-test` 19 PASS and 2 FAIL that are the test's own (an argv file a refused run never writes); `pixelelated-cloud-validator-test` refused to run on the tree's pinned 1.75.2 (it hard-codes 1.75.1). No network beyond loopback.
- **The fixtures** (`tools/t17-*-fixture.py`; outputs `stage-b/fixture-*.txt`), each running the product's own code:
  - pin: icon requests spend the ten PIN attempts and lock the right PIN out (F-01); a non-ASCII PIN raises `TypeError` (F-09);
  - archive: a symlink member passes `foreign_member` and is refused by the image's busybox `tar` (F-04; a candidate refuted);
  - content: `cloud_content_backup '../.config'` copies from outside `/storage/roms` (F-03); `--delete-excluded` in `RCLONE_NET_OPTS` reaches the deleting `sync`, and with the donor's real rclone the apply deletes a save (F-02);
  - mode: the writers' modes under umask 022.
  - The content fixture's absolute paths are rewritten into a scratch root and its rclone is a recording stub, or the donor's real rclone over a local-backend cloud: named substitutes, the guest repeats them.
- **Two first drafts corrected before commit:** F-17 said the rule names `cloud_setup` as a writer (it does not; it names no writer of `rclone.conf` at all), and F-16 claimed a recount not yet run (run: no shell function named once; three framework-called python methods).
- **The generator** `tools/t17-tables.py` writes coverage (14), runs (40), tools (5), writers (31 anchored rows), secrets (28 rows and the scrubber's three families) and deletions (12 `rm -rf`, 1 delete, 3 sync statements, the refusals); every anchor must match its asserted count at `8ebaf8daad`; `check` same.
- **Nothing of the never-run list ran.** No guest; `git diff --stat f3803436b8 HEAD -- packages projects tools` empty.
- PROOF: P7, § The writers, generated and anchored.
- PROOF: P8, § The secrets' paths, generated and anchored.
- PROOF: P9, § The deletions and the refusals.
- PROOF: P10, the five fork tools on the host: `stage-b/tools-out/`.
- PROOF: P11, the PIN attempts and the non-ASCII PIN: `stage-b/fixture-pin.txt`.
- PROOF: P12, the symlink member: `stage-b/fixture-archive.txt`.
- PROOF: P13, the backup's names and the flag into the deleting sync: `stage-b/fixture-content.txt`.
- PROOF: P14, the writers' modes: `stage-b/fixture-mode.txt`.
- PROOF: P15, `tools/vocabulary-check` at the ES pin: `stage-b/vocabulary-check.txt`.
- PROOF: P16, the why sentences against the interface's table: `stage-b/why-lines.txt`, `stage-b/es-why-sentences.txt`.
- PROOF: P17, the tables regenerated: `check` same.

## [Stage C] 2026-10-26 06:41 UTC onward (after the stage-B pointer `59b0cb19db`) — 03, 04, the packet, the two seats, 05

- **Stage B accepted** (the coordinator, 06:5x UTC).
  - The two tool problems are #1127 (Backlog under #1047), cited in `02` and `05`.
  - The guest plan is in scope with F-01 to F-04, on two conditions. F-02's flag goes into the guest's conf only, over the seeded synthetic root, and the conf is put back. F-03 runs against the QA backend only, its data directory listed before and after.
  - The window's start waits for M7's guest RETURN only, no longer for T16's re-grant.
- **`03` and `04` written** before the packet.
- **The packet** (`stage-c/packet.py`; `second-opinions/packet.md`, 294,779 bytes, sha256 `4e95aaff…`; `second-opinions/manifest.json`):
  - The first build was 437,469 bytes, the size at which Argon failed on T30, so it was trimmed before any seat read it (D-WORKFLOW-195): four of the 14 whole, the other ten as line-numbered excerpts of every cited line with eight lines of context, the fixtures as their docstrings, and the brief's § 4 only.
  - **The three-way scan:** `forbidden-terms-check --stdin` found 0 hits in 94 sections and on the whole file. `SECRET_PATTERNS` found 0 lines, proven to fire on a run-time fake line. The mask changed 20 lines, and 343 credential-word hits were classed.
  - 16 hits, read by shape only (length and edge characters, never the text), were dispositioned by name in `packet.py`: prose naming keys, code, and the fixtures' synthetic percent-encoded PIN. **No value.**
  - The first scan stopped the build on 22 unreviewed hits, which is what it is for.
- **The plan:** `second-opinions/review-plan.json`, extended, two reviewers, written 06:50Z, before the first call.
- **The runner:** `COUNCIL_ENV_FILE=/nonexistent tools/council/run verify-pins`: `OK`. The runtime is from stage A's `npm install --offline`.
- **The four keyed calls, and no others:**
  1. Astra's probe, 06:51:29 to 06:51:46 UTC: PASS, `openai/gpt-6-astra` by OpenAI.
  2. Astra's refutation, 06:52:05 to 07:11:33 UTC, as a harness background task: rc 0, PASS, one attempt, `finish=stop`; 50 items, A-1 to A-50.
  3. Argon's probe, 07:18:19 to 07:18:31 UTC: PASS, `google/gemini-4-argon` by Google.
  4. Argon's refutation, 07:18:36 to 07:27:05 UTC, as a background task: rc 0, PASS, one attempt, `finish=stop`; 49 items, R-1 to R-49.
  - Argon's brief was the packet plus the lane's grades of Astra (302,486 bytes).
  - **`tools/council/run summary` and `verify-seals`** were run with `COUNCIL_ENV_FILE=/nonexistent` and refused: there is no `council-run-manifest.json`, because these are audit invokes, not a council run. The provenance was read directly instead (`stage-c/provenance-read.txt`): all four `verification=PASS`, served model and provider the seat's, one attempt, each output's sha256 matching.
  - The files carry `facilitator_version` (`council-facilitator@1.14.1-pixelelated.2`), not a `facilitator` block. Checkbox 3 names both; that is put to the coordinator.
- **The re-reads** (`stage-c/rereads/rereads.sh`, `c01` to `c12`, `c14`, `c15`, all rc 0): every seat item was re-read at its lines at `8ebaf8daad`, through the mask.
- **One fixture added:** `tools/t17-option-key-fixture.py` (`c13`, 07:13:39 UTC), the product's own split and `save()` with the donor's rclone over a local backend. `--config=<path>` writes the new connection into `<path>` and the save refuses; `--log-file=` is honoured; the control saves. **F-20, found by both seats independently.**
- **What the seats changed:**
  - **New findings:** F-20 (Low, a `bug` candidate), F-21, F-22 and F-23 (Info).
  - **Corrected first-draft claims:**
    - F-05: the `lsd` argv carries no secret.
    - F-07: nothing masks rclone's ERROR text. A-4 refuted *"the URL, not its secret"*.
    - F-10: a partial selection is installed.
    - F-12: any value of `CLOUD_SIGNIN_DEBUG` turns it on.
    - F-18: the scrubber runs at boot.
    - The writers table: the `phone-keyboard` marker added (32 rows), and the scan modes relabelled *by construction*.
    - The secrets table: the phone keyboard carries a sign-in page password, a sixth kind.
    - The plan's order: read, then spent.
    - `03` § 3.1: `select()` is a third writer.
  - **Two of the lane's grades of Astra reversed by Argon:** A-49 and A-23 are Info hardenings in F-10.
  - **Both seats propose Medium for F-02 and F-03.** The coordinator rules.
- **`05`:** 22 items, 4 of them `bug` candidates (PL-01 to PL-04), all `Open`.
- **Nothing of the never-run list ran.** No guest, and no build. `git diff --stat f3803436b8 HEAD -- packages projects tools` is empty. The one new rclone run was the donor's, over a local backend in scratch.
- PROOF: P18, every seat item re-read at its lines: `stage-c/rereads/`.
- PROOF: P19, an option-shaped key honoured as an rclone flag: `stage-c/rereads/c13_option_key.out`.

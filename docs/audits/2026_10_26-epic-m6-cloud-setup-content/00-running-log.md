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

## [Stage D] 2026-10-26 07:41 UTC — six bugs, the audit issue, the dispositions

- **Stage C accepted and stage D ruled** (the coordinator, 07:5x UTC).
  - **Six `bug`s:** PL-01 (with PL-14), PL-02 and PL-03 (both **Medium**), PL-04 (with PL-08), PL-05's `cloud_setup:797`, and PL-06's `--set-systems`. The rest are recorded or deferred as `05` now says.
  - **PL-02's seam:** this slice's scripts only, under **D-CLOUD-185** (a row on the coordinator's branch). T16's twins go to #663.
  - **Checkbox 3:** the direct provenance read is the evidence, and #664's wording changed.
  - **Yes** to Argon's filter-flag case as S2's second fixture case.
  - **Stage E** runs under `docs/reviews/briefs/t17-streams.md` at `f59f7cbbc1`.
- **Filed**, each with its trace, `Already written:` line and VM line, and `tools/box-check --issue N` at 0 fail:
  - #1128 S1, PL-01 and PL-14, Low;
  - #1129 S2, PL-02, Medium;
  - #1130 S3, PL-03, Medium;
  - #1131 S4, PL-04 and PL-08, Low;
  - #1132 S5, PL-06, Low;
  - #1133 S6, PL-05, Low.
  - The bodies were scanned before they left: `forbidden-terms-check` 0, `SECRET_PATTERNS` 0.
- **The audit issue:** #1134, *Audit: M6 T17 cloud setup, sign-in, connections and settings backups -- 22 findings (0 critical, 0 high, 2 medium, 4 low, 16 info)*, labelled `audit` and `punch-list` on M6, attached as a sub-issue of #664. `box-check`: 22 open, 0 fail.
- **`05`:** every item's disposition note and its Phase 7 row carry the ruling; PL-02 and PL-03 are Medium and PL-06 Low. `tools/lint-audit-artifacts --phase pre-issue`: PASS. `tools/register-check`: PASS.
- **Nothing under `packages/`, `projects/` or `tools/` changed at stages A to D:** `git diff --stat f3803436b8 HEAD -- packages projects tools` is empty.

## [Stage E] 2026-10-26 07:41 UTC onward (after the stage-D tip `045cc316ea`) — six streams, the guest window, the disk retired

- **The streams**, under `docs/reviews/briefs/t17-streams.md` at `f59f7cbbc1` (read whole), one commit each, each fixture failing on the unfixed file before the fix landed (`02` § The streams):
  - S1 `59a5a8860e` (#1128);
  - S2 `1def91bdfc` (#1129);
  - S3 `f8feb15bb4` (#1130);
  - S4 `0ffe7cd94f` (#1131);
  - S5 `1d8271a1f3` (#1132);
  - S6 `3e95bf18f4` (#1133).
- **The tools, named:** the donor's rclone 1.75.2 at `/workspace/artifacts/m6-donor/1a0266484423/image/system/usr/bin/rclone`, sha256 `ed887da83d3e2c07ff8acc60cb5b56dbe7bb4d73cc445b6ff71988f164c0558a`, matching the donor's `SHA256SUMS` (its `RECORD.txt` names the version, not the hash); the donor's busybox 1.36.1 (`79e7b20d…`); host Python 3.14.4 and GNU bash 5.3.9. Each fixture's command is at the head of its `stage-e/s<N>-*.txt`.
- **Fixtures added or extended:**
  - `tools/t17-pin-fixture.py` (`paste-html`);
  - `tools/t17-content-fixture.py` (`match-include-real`, `backup-unknown`, the argv and log checks, `--only`);
  - `tools/t17-option-key-fixture.py` (`--sources`, `--expect`, `sigkill`, `sweep`);
  - `tools/t17-selection-fixture.py` (new). Its `ulimit -f 1` with SIGXFSZ ignored is a file-size limit standing in for a full card.
- **`tools/register-check` fails on exactly four lines from S2 on:** the code comments citing D-CLOUD-185, a row on the coordinator's branch at `f59f7cbbc1`, which only the coordinator merges here. I did not chain the check into S2's commit, so the commit went in with the failure known only afterwards. From S3 on, each commit was preceded by the check showing no other failure.
- **S6's premise did not hold:** neither `ANOTHER CLOUD SYNC IS RUNNING` nor the rule's `A SYNC IS ALREADY RUNNING` is a `whySentences` row at the pin. #1133's first criterion is put to the coordinator.
- **The guest window** (granted 07:5x UTC; START 07:59:26, RETURN 08:06:04, both posted on #664 with census 0):
  - `guest-cycle/run.sh`, its stages' outputs whole and masked, and `pl18.out`.
  - The image's `.sha256` OK; `BUILD_ID=069fc27044…`.
  - 12 installed files hashed: 11 same, `cloud_oauth` different (M7's sign-in build), with no hunk in F-01's or F-09's lines.
  - Five fixtures met `--expect unfixed` under the image's python, busybox and rclone. **F-02 and F-03 were proved on the real paths against the QA backend**, under the stage-B conditions: the conf put back `cmp`-identical, and the 3,418-file upload listed before and after, then removed.
  - PL-18 through a full restore gave **F-24**.
  - My setup errors: two scratch roots the fixture's own path rewrite caught. Recorded in `guest-cycle/fixtures.out`.
  - I typed START wrong in the RETURN comment (07:59:20); corrected from `/workspace/tmp/m6-t17/start-time`, with the correction stated in the comment.
- **Not run in the window, put to the coordinator:** the match's refusal, `backuptool`'s exit 5, `atomic()`'s mode, `tools/signin-memory`; and the phone page, `CANNOT`.
- **Retired, D-INFRA-022:** no stream's guest proof is owed; the guest runs the unfixed image by design.
  - The disk: `/workspace/tmp/m6-t17/vm-pair/vm-a.qcow2`, 2,312,699,904 bytes, sha256 `efe34c1bea85faae7e0e5f99b663d4e94cf1c5b77683c1dd503d8c214f5d836b`, removed with its directory (`vm-pair/`, 2,313,241,064 bytes in all), recovering about 2.3 GB.
  - The backend's state (`cloud-qa/`, 138 bytes after the upload's removal) is kept until the hand-back, then retired with the scratch.
  - The hash is provenance: it makes no claim that the file still exists.
- **Nothing ran on a handheld, a person's cloud or a hosted account. No build, no fetch, no keyed council call.**
- PROOF: P20, the six streams' before and after: `stage-e/`.
- PROOF: P21, the guest window: `guest-cycle/`.
- PROOF: S1's row in `02` § The streams: `stage-e/s1-*.txt`.
- PROOF: S2's row: `stage-e/s2-*.txt`.
- PROOF: S3's row: `stage-e/s3-*.txt`.
- PROOF: S4's row: `stage-e/s4-*.txt`.
- PROOF: S5's row: `stage-e/s5-*.txt`.
- PROOF: S6's row: `stage-e/s6-*.txt`.

## [Stage E, after the hand-back] 2026-10-26 08:18 UTC onward — the second window, S7, the S3 correction

- **The coordinator's answers at the hand-back** (08:2x UTC):
  - #1133's first criterion is reworded to the script's line, and the table's pair goes to T18 (#665).
  - F-24 / PL-23 is a `bug`, Low: S7, under the stream brief at `8e6c990a1f`.
  - A second window of 15 minutes for the five the first did not reach.
  - `register-check`'s four lines are the reading wanted; they pass after the hand-back merge.
  - S5's exit 1 is right.
- **The second window:** START 08:18:14 and RETURN 08:21:22 UTC, both posted on #664 with census 0 and the time in the first line.
  - `guest-cycle/run2.sh` and `w2-*.out`. The guest was rebuilt from the same checked image.
  - **The proofs:** the match's refusal (`previewed sync|1, now sync|3`, nothing removed); the credential refusal (why *"A SIGN-IN WAS FOUND IN THE BACKUP"*, the archive the same hash, the process exit 1 by the command's own mapping of 5 at `backuptool:1858`); `atomic()`'s mode (600 on the real save, `0o600` under the image's python, including over 0644); `signin-memory` PASS (104, 98 and 42 MB; 245 together) on a host-local static page; the phone page `CANNOT`.
  - `signin-memory`'s first page, the QA WebDAV root, answered 401, so the window never finished loading and the tool reported FAIL; that output is kept. The static page was served by `python3 -m http.server` on 127.0.0.1:9091 and stopped by its recorded PID.
- **Retired, D-INFRA-022:** the second disk, `/workspace/tmp/m6-t17/vm-pair/vm-a.qcow2`, 2,309,029,888 bytes, sha256 `b9a15bbdd7efa63e5ceaf6cb7f4214f6c0613d40dca7f2552eeeba54f2624955`, removed with its directory (2,309,571,048 bytes in all). The hash is provenance.
- **S7** (`479cd96c24`, #1136, filed first with its trace and `Already written:`):
  - The fixture runs the real `backuptool restore --no-restart` unmodified, in an unprivileged bubblewrap sandbox with `/storage` a scratch directory, under the donor's busybox `tar`.
  - Its first run failed every case on *"COULDN'T KEEP A COPY"*: bwrap passed the host's `TMPDIR` into the sandbox, where that path does not exist (#549's lesson). The sandbox now starts from `--clearenv`.
  - **On the busybox listing:** busybox prints a hard link as `-` with ` -> target` after its name, so the type check pairs `tar -tv`'s lines with `tar -t`'s names.
- **`tools/last-good-scripts-test`** (`QA_SYSTEM_ROOT` the donor), first run at S7, failed four checks.
  - **PL-006** was S7's first cut: the listing went to a temporary file, which moved the suite's numbered `mktemp` fault onto it. `foreign_type` now reads from a pipe.
  - **Three `cloud_content_backup` checks** were S3's (`f8feb15bb4`): the check applied to every form's names and refused every name with no `es_systems.cfg`. Corrected in `c3e260861b`.
  - After both, the suite PASSED: 1,379 PASS lines, exit 0. I had not run it at S1 to S6, which is how S3's regression stood for an hour.
- **Typed times corrected before commit:** RETURN `08:21:3x` (it is 08:21:22, from the comment), and the suite's `08:3x-09:0x` (now its output file's time, 09:04:19Z).
- PROOF: P22, the second window: `guest-cycle/w2-*.out`.
- PROOF: S7's row in `02` § The streams: `stage-e/s7-*.txt`.

## [Stages F to H] 2026-10-26 09:17 UTC — the outcomes, the retro, the checkers, from the coordinator's merge `8592f91054`

- **The coordinator's reading of the second hand-back** (09:1x UTC):
  - `964795e9b4` merged here at `8592f91054`, and the worktree fast-forwarded to it; `register-check` passes there;
  - stages F to H owed before acceptance;
  - yes to the suite rule, now in `docs/reviews/plan-for-the-plan.md` § 6b.
- **Stage F:** `05`'s 23 rows at their outcomes, read back from the tracker at 09:11:37 UTC (#1127, #1117, #909, #665, #663, #1128 to #1133, #1136 and #1134 open).
  - **21 Resolved:** 10 with their fixing commits, PL-18 and PL-23 by S7 among them; 11 recorded at `3a7fdb0ec2`.
  - **2 Deferred:** #1127 (with #1117) and #909.
  - The index's outcomes match. `tools/lint-audit-artifacts` in its default phase: **`PASS`**.
- **Stage G:** the retro at `docs/retros/2026-10-26-m6-cloud-setup-content.md` (`022254810d`), posted on #664 (issuecomment-6412393587).
  - Its futro check was first written from memory and corrected before commit against the addendum's text (`:255-301`).
  - So was `04`'s count of Resolved rows, 19 before the count showed 21.
- **Stage H, the five checkers at 09:14:31 UTC on `022254810d`:** `register-check` rc 0 (682 IDs); `work-log-index --check` rc 0; `rules-check --quiet` rc 0; `forbidden-terms-check` rc 0 (0 hits in 133,581 tracked files); `.githooks/hooks-test` rc 0 (`PASS`).
- `reviewed-at: f3803436b8` and `fixed-at: 479cd96c24`, read back from #664's body for the hand-back.

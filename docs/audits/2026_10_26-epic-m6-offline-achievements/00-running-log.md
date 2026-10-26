# Running log: M6.P2 T19, the offline achievements proxy (#666)

- **Brief:** `docs/reviews/briefs/offline-achievements-proxy.md`, version 2 (`110943c58c`). **Dispatch:** the coordinator's comment on #666, 12:09 UTC on 2026-10-26.
- **Model and effort:** Opus 5.5 (`claude-opus-5-5`) at high effort, the session `m6-t5-build-engine` the dispatch names.
- **Worktree:** `/workspace/repos/pixelelated/distribution.worktrees/m6-offline-achievements-666` on `feature/m6-offline-achievements-666`. It is stacked on `feature/m6-p1-survey-641` at `2174265e9c`, with the coordinator's `42623ac083` merged at `30654cd701`. **Dispatch tip:** `7de4ece06d`.
- **`reviewed-at`:** the dispatch tip `7de4ece06d`, with **`8ebaf8daad`** beside it: the read is of `8ebaf8daad`'s bytes for the 27 (R1 below; `git diff --stat 8ebaf8daad HEAD -- packages projects` empty).
- **Depth:** Extended -- two seats, GPT-6 Astra at `max` then Gemini 4 Argon at `high`, a probe and one refutation each over a trimmed, scanned packet; exactly four keyed invokes, every other council call keyless.
- **Can this be done on the VM? Yes -- the host first, then one guest window granted on #666** (the brief's § 5.1; #666's body line 16). Every read, count and table runs on the host. The upstream source comes from the cache's tarball named by the pin, unpacked and patched under `/workspace/tmp/m6-t19/`. The service runs only on the guest, and the RetroAchievements server is reached only by `ra-offline-test` with the QA account. Nothing on a handheld.

## [Stage A] 12:09 to 12:25 UTC — the first commands, the block, the runs, the unpack, the suites

- **The host at 12:09** (the dispatch's census; read again at 12:22:31Z): qemu 0, compilers 0, listeners on `:8080` 0. The host file `/tmp/m7-m6-host-coordination-20261023.txt` last reads the coordinator's T18 RETURN lines (10:23 and 10:24 UTC: *"T18 GUEST RETURN ACKNOWLEDGED (RETURN 10:23:21, inside its 10:36 bound ...)"*). No M7 line after them; no window is held, and none is asked for before stage B's end.
- **The first commands (§ 1):**
  - the pointer is seeded; the status is clean (0); the tip is `7de4ece06d` on `30654cd701` and `42623ac083`;
  - `8ebaf8daad` is an ancestor (`stacked`);
  - `git diff --stat 8ebaf8daad HEAD -- packages projects` is empty, and the `tools` diff is P1's own (15 files, 2,130 insertions);
  - `651150fc88` (upstream `next`) resolves locally;
  - T2's punch list is reachable (36 items);
  - `register-check` ok;
  - the rules: `git diff --quiet next -- .claude CLAUDE.md AGENTS.md` reports a difference, but `git log HEAD..next` over those paths is empty, so the branch is ahead of `next`, not behind.
- **The membership block (§ 2):** `selects 2 paths 27 lines 5369 {'shipped': 27} {'fork-own': 9, 'vendor-carried': 18}`; `patch-and-config rows 18 1703`. This is **the brief's figures exactly**; the output is in `01` § Scope. `.qa-scratch/t19/paths.txt` has 27 lines and is gitignored.
- **The § 5 runs:** `tools/t19-runs.sh 7de4ece06d`, output in `stage-a/runs.txt`. That file has eighteen runs, R0 to R17, each with its exit and wall time; all exit 0 except R3, R5 and R14, whose final `grep -c` counts 0 as expected (the hardening directives, `umask|chmod|chown`, `have_account` in the dispatch). The figures and their deltas are in `01` § The runs at stage A. `02` § The runs takes them at stage B.
- **The unpack** (`stage-a/unpack.txt`):
  - **the tarball:** the cache's tarball named by the pin, sha256 `88eef31a...898b`, equal to `PKG_SHA256`, unpacked to `/workspace/tmp/m6-t19/src/`;
  - **the patches:** the eighteen applied with GNU patch 2.8, `-p1 --fuzz=0` in name order (the build's order: the recipe sets no `PKG_PATCH_DIRS`). **All 18 rc 0, 75 hunks, 0 rejects**; offsets but no fuzz in 002 (+3), 008 (+43, +43, +54), 010 (+1) and 015 (-14, +1, -6).
- **`tools/raofflineproxy-integration-test`:**
  - `--source` is the patched pin;
  - `--predecessor-source` is the previous shipped pin `879b158995` (the recipe at `7afa9efcfc`, 2026-10-06), from the same cache, sha256 equal to that commit's `PKG_SHA256`, with that commit's 16 patches at fuzz 0, all rc 0. No fetch was made; the earlier runs' predecessors were a 248ce tree and an M7 build root, which this lane does not read.
  - **Result:** 12 tests, `OK`, rc 0, 8 s, on the host's python 3.14.
- **`tools/last-good-scripts-test`** with `QA_SYSTEM_ROOT=/workspace/artifacts/m6-donor/1a0266484423/image/system`:
  - **Result:** rc 0, 523 s, 1,379 PASS, 0 FAIL (`stage-a/last-good-scripts-test.txt`, which names the proxy cases).
  - **The stage-A read § 1 asked for: the suite runs the ctl itself.** Groups p and t (`tools/last-good-scripts-test:1612-1621`, `:2239-2246`, and the background runs at `:2485`, `:2524`, `:2565`, `:6661`) execute the real ctl. They run it inside `bwrap`, with a tmpfs root, `/storage` and `/run` bound to fixture directories, `systemctl` and `logger` shimmed, and the client's network verbs (`probe-online`, `run-smart-cache`) answered by a `python3` shim from `/run`. Nothing reaches the host's `system.cfg`, units or network.
- **The ctl and the proxy:** the ctl is shown never to have run on the host outside `tools/last-good-scripts-test`'s bubblewrap sandbox (the coordinator's wording, #666, 12:35 UTC); the proxy (`raofflineproxy.main`) did not run at all.
- **Nothing of the never-run list:** no build, no compiler, no fetch, no guest, no handheld, no account, no keyed council call, no M7 root read.

## [Stage B] 12:25 to 12:40 UTC — the 27 read whole, the patched modules, `02`

- **Read whole at `8ebaf8daad`** (`stage-b/reading-notes.md`, the reading's leads by line):
  - the ctl (2,455 lines), the three helpers, the recipe, the unit, the daemon file, the two sibling recipes;
  - all 18 patches;
  - in the patched pin: `proxy_service.py`'s request path, the offline login and the upload callers; `auth.py`, `log_uploader.py`, `usage_report.py`, `storage.py`'s `_initialize_sqlite`, `es_export.py`, and `network.py`'s `http_get`/`http_post`;
  - for the protocol, EmulationStation's `CloudText.h` parsers and `CloudText.cpp`'s `scanWhy`/`topUpWhy` at `16dbac5211`.
- **`02-forward-audit.md`:**
  - § Coverage (27), § The listener, § The credential's paths and § The patches (18);
  - § The writers, generated by `tools/t19-writers.py`: 77 rows; its drift control at `87d9969bbb` exits 1 with 49 (`stage-b/writers-runs.txt`);
  - § The bounds, § The runs, § What T20 inherits, § Positives.
- **The first fixture:** `tools/t19-listing-fixture.py` runs the listing's python from the ctl, unchanged, against the patched pin with a scratch store. One ROM name with byte 0xff fails the whole listing (rc 1, `UnicodeEncodeError`), where the decodable library lists (rc 0): **reproduced** (`stage-b/listing-fixture.txt`). It does not run the ctl.
- **The leads for `04`** (each read at its lines; none is called anything until stage C's grades):
  - the offline login serving the cached sign-in body, `Token` in it, to any client naming the account (`proxy_service.py:491-505`);
  - the readiness check accepting a foreign listener;
  - the scan lock that fails open;
  - `count_ready`'s 0;
  - the undecodable name;
  - the top-up mark ahead of the clock;
  - the ignored `write_stamp` status;
  - `list_jobs` writing the store through `Storage()`;
  - `http_post` marking no 429 pause;
  - the IDAT inflate and the lookup threads unbounded;
  - the refresh's `done` field meaning two things;
  - `scanWhy`'s row for a token no producer emits.
- **The criterion's wording** (the coordinator, 12:35 UTC): the ctl is shown never to have run on the host outside `tools/last-good-scripts-test`'s bubblewrap sandbox.
- **Census at 12:37:11Z:** qemu 0, compilers 0, `:8080` 0. No guest has been started; the window is asked for on #666 with this entry's commit.

## [Stage C, the window] 12:41 to 12:58 UTC — the guest, two boots

- **The grant and the posts:** granted on #666 at 12:41 UTC. **START 12:43:49 and RETURN 12:53:37 UTC**, both posted with census 0 (qemu, `:8080`, compilers). The record is `02` § The guest cycle and `guest-cycle/`.
- **The image:** the M6 copy, its `.sha256` OK; two fresh disks of the lane's own. **Its scripts are M7's** (`BUILD_BRANCH=build/m7-signin-20261022-07`): the ctl differs from `8ebaf8daad` by 233 diff lines, each helper by 7; the unit and the daemon file are equal. So **`8ebaf8daad`'s four scripts ran from `/storage/t19/bin/`** (sha256 equal), against the image's client and service. The question is put on #666 at RETURN.
- **Boot 1** (user-mode NIC, ssh 10026, 640x480, headless):
  - the service runs as root, umask `0022`; every file written `644 root` (F-25);
  - the six positives fall as read: F-01, F-03, F-06, F-12, F-16, F-17;
  - `raofflineproxy-installed-native-test` runs 18 with 4 failures, on the image's M7 client: a lead outside the slice;
  - `ra-offline-test` is **CANNOT** (D-RA-006: the QA account's reachable achievements are spent); nothing launched, nothing spent;
  - `qa-accounts clear` rc 1, leaving the proxy's folder on the retired disk.
- **Boot 2** (`-nic none`): the consent test, 30 checks, rc 0.
- **Both stopped by pidfile** (`tools/vm-stop` rc 0 ×2). The leftover check: qemu 0, `:8080` 0, sockets 0.
- **Retired (D-INFRA-022):** both disks, with their path, size and sha in `guest-cycle/retired.txt` (boot1 2,312,372,224 B `ddb5a7f6...`; boot2 2,310,471,680 B `e4731d56...`), removed with their firmware vars and the run's QA key.
- **The RetroAchievements server** was reached by the QA account's sign-in, the scan and the top-up the plan named, and by `ra-offline-test`'s API read at its step 2. The owner's account was never named or used.
- **The ctl on the host:** the ctl ran only on the guest (the tree's copy) and in the suite's `bwrap`.

## [Stage C, the seats] 12:58 to 13:45 UTC — the packet, four keyed calls, 94 items graded, the pre-issue lint

- **The runtime:** `npm install --offline` in `tools/council/` (`esbuild`'s install script left unapproved, as T18's); `COUNCIL_ENV_FILE=/nonexistent tools/council/run verify-pins`: `OK`.
- **The packet** (`stage-c/packet.py`, T18's builder adapted): 340,476 bytes, 51 sections, trimmed from 407 KB and then 372 KB before any seat saw it (D-WORKFLOW-195). The three-way scan: 0 forbidden terms; 0 secret-pattern lines, proven on a fake; 0 review; 48 hits read at their lines and dispositioned by name.
- **`review-plan.json`** was written at 13:01 UTC, before the first call.
- **The four keyed calls, and no others** (`/workspace/tmp/m6-t19/keyed-calls.txt`; the refutations ran with `--max-retries 1 --per-attempt-timeout-ms 1800000 --total-timeout-ms 2400000`):
  1. Astra's probe, 13:01:36 to 13:01:48 UTC.
  2. Astra's refutation, 13:02:05 to 13:24:03 UTC: 55 items.
  3. Argon's probe, 13:26:06 to 13:26:14 UTC.
  4. Argon's refutation, 13:26:22 to 13:34:47 UTC: 39 items.
  - Each took one attempt and ended `finish=stop`.
- **The provenance, read directly** (`stage-c/provenance-read.txt`): all four `verification=PASS`, served model and provider the seat's, the output hashes matching, `facilitator_version council-facilitator@1.14.1-pixelelated.2`.
- **The grades** (`stage-c/astra-grades.md`, `argon-grades.md`, the re-reads in `stage-c/rereads/`):
  - Astra: 51 accepted, 1 in part, 3 plausible, 0 rejected.
  - Argon: 35 accepted, 2 in part, 2 plausible, 0 rejected.
- **The first reader's claims the seats refuted or narrowed**, each corrected in `02`, `03` and `04`, saying so:
  - the loopback peer check missed (`proxy_service.py:290-292`, A-2), which narrows F-02;
  - F-03 narrowed by A-6, then made plausible again by R-6;
  - F-05's rule is the listing's (A-5);
  - `TOPUP_TIMEOUT` is a soft deadline (A-18);
  - `03`'s "undoes every step" (A-47).
  - **One of Argon's claims refuted at its line:** `list_jobs` does close its `Storage` (ctl :1564).
- **New findings:** F-26 to F-35 from Astra, F-36 to F-41 from Argon.
- **`05`:** 23 items covering all 41 findings: eight `bug`s proposed, all Low (PL-01 to PL-08); fifteen Info.
- **The lint:** `tools/lint-audit-artifacts docs/audits/2026_10_26-epic-m6-offline-achievements --phase pre-issue`: `PASS pre-issue artifacts (does not certify resolution)`.
- **Nothing of the never-run list ran.** No keyed call beyond the four. No guest outside the window.

## [Stage D] 13:48 to 13:55 UTC — the dispositions, the audit issue, the bugs

- **The ruling:** #666, 13:48 UTC. The streams are `docs/reviews/briefs/t19-streams.md` at `6064579a3f`, with sections added at `22caaa375a` (14:33, the suite), `648dadebf1` (15:15, #1166 into S5) and `dccd82138d` (15:50, S7's fixture).
- **The audit issue:** #1156, a sub-issue of #666, with 23 items, then 24 with PL-24.
- **The nine bugs, all Low:** #1157 to #1165. `tools/box-check` 0 fail on all ten issues. Committed at `715f39a0fd`.

## [Stage E] 13:55 to 16:30 UTC — ten streams and #1166, one commit each

- **Versions:** every fixture ran under the host's bash 5.3.9 (the tree pins 5.3) and python 3.14.4 (the image's recipe: 3.14.7). The ctl's applets came from a copy of the retained donor's busybox 1.36.1 (`/workspace/artifacts/m6-donor/1a0266484423/image/system/usr/bin/busybox`), wrapped only for the applets it provides: it has no `grep` or `sort`, which the image takes from packages of their own.
- **Every fixture ran in `bwrap --clearenv`,** its scratch root asserted under `/workspace/tmp/m6-t19/` and no real prefix rewritten. Each is in the audit folder's `tools/`; nothing of the lane's is under the repository's `tools/`. Arguments are given only where they differ from the stream's scratch:
  - S1: the patch's test, `python3 -B -m unittest linux.tests.test_linux_offline_login` (`env -i`); `tools/t19-s1-service.py <tree> <scratch>`, the real service in `--unshare-net`.
  - S2: `tools/t19-s2-modes.sh <ctl> <unit> <scratch>`.
  - S3: `tools/t19-s3-listening.sh <ctl> <scratch>`, a python stand-in on `0.0.0.0:8080` in `--unshare-net`.
  - S4: `tools/t19-s4-disable.sh <ctl> <scratch>`, each case in `--unshare-pid`.
  - S5: `tools/t19-s5-writers.sh <ctl> <client> <scratch>`, its case 6 #1166's positive.
  - S6: `tools/t19-s6-topup-mark.sh <ctl> <scratch>`.
  - S7: `tools/t19-s7-not-clean.sh <ctl> <cache-images> <client> <scratch>`.
  - S8: `tools/t19-s8-counts.sh <ctl> <client> <scratch>`.
  - S9: `python3 -I -B tools/t19-listing-fixture.py <tree> <scratch> --ctl <ctl> --helper <cache-indexed> --expect unfixed|fixed`.
  - S10: `patch --dry-run -p1 --fuzz=0` of 020 and 021; `tools/pkgcheck raofflineproxy`.
  - The shared harness is `tools/t19-ctl-sandbox.sh`. The client is the pin's tarball from the cache with the series applied, under `/workspace/tmp/m6-t19/s1/fresh/`.
- **`tools/last-good-scripts-test`** (`QA_SYSTEM_ROOT` the retained donor) before every commit that touched a covered script: 1313 PASS at every stream's commit.
  - Its checks changed only as ruled (14:33, 15:50; D-WORKFLOW-210/211): S1's 011 check; S3's D12b check and D36's runner; S7's and S9's fixture completions. Each is named in `02` § The streams.
- **The commits:**

  | Commit | Stream |
  | --- | --- |
  | `57c5e8c4ec` | S1 |
  | `5810eff004` | S1's suite carry-over |
  | `76658dd062` | S2 |
  | `6aca961c00` | S3 |
  | `fdcd576e99` | S4 |
  | `44120e2e17` | S5, with #1166 |
  | `7239b1adc1` | S6 |
  | `54ab8c6c10` | S7 |
  | `72f0f3e3dd` | S8 |
  | `09b204153d` | S9 |
  | `49f3dc8679` | S10 |

- **Two of the lane's slips, each corrected:**
  - `register-check` FAILED at S1 behind `| tail -1`; the unpushed commit was amended, with a friction line.
  - The 15:49 post called #188's top-up check reversed; it is a fixture completion, corrected on #666 and in `02`.

## [Stage F] 16:30 UTC — every row at its outcome

- **`05`:** all 24 rows at an outcome: 14 resolved with their commits, 5 deferred (#667 three, #585 two), 5 withdrawn as recorded. `tools/lint-audit-artifacts docs/audits/2026_10_26-epic-m6-offline-achievements`: `PASS` (the default `resolution` phase).
- **#1156:** 24 checkboxes ticked at their outcomes; `tools/box-check --issue 1156`: 0 fail.

## Closing census

- **Never ran:**
  - no build;
  - no compiler beyond python's own byte-compiling;
  - no plan generation;
  - no fetch: the upstream proxy came from the cache's tarball, and the council runtime from `npm install --offline`;
  - no handheld;
  - the owner's RetroAchievements account was never named or used;
  - no hosted account (no `ra-offline-test` run this cycle: CANNOT, D-RA-006);
  - no M7 root or worktree;
  - no keyed council call beyond the four of stage C.
- **The one guest window:** 12:43:49 to 12:53:37 UTC. Both disks were retired, recorded in `guest-cycle/retired.txt`.
- **The ctl and the proxy on the host:** the proxy's service ran on the host only at stage E, inside `bwrap --clearenv --unshare-net`, as S1's stream brief directs (`tools/t19-s1-service.py`), and in the suite's own D36 case. The ctl ran on the host only at stage E, inside the stream fixtures' sandboxes and the suite's. Before stage E neither ran on the host.
- **Under `packages/`, `projects/` and `tools/`:** nothing changed at stages A to D (`git diff --stat 7de4ece06d 715f39a0fd -- packages projects tools` is empty). At stage E: the package's own files under `projects/ROCKNIX/packages/network/raofflineproxy/` (patch 022 new; the ctl, `cache-images` and `cache-indexed`; the unit; `package.mk`'s comment; 020's and 021's headers), and `tools/last-good-scripts-test` as ruled.

## [Close-out] 17:05 UTC — accepted at `c0af666edf`; the completion marker; the temporaries retired

- **Accepted:** on #666 at the merged tip `c0af666edf`; #1156 closed as completed.
- **The marker:** `tools/write-completion.py` (T18's, adapted) read #1156 back closed and completed, 24 ticked, 0 open. It wrote `tracker-final-readback.json`, `tracker-completion.json` and `audit-completion.json` (`completed_at` 2026-10-26T17:05:43Z).
- **The lints:** `tools/lint-audit-artifacts <folder> --issue 1156` and the default phase both PASS. `tools/ceremony-check` reads the audit's last completion from this marker.
- **Retired (D-INFRA-022):**
  - the three scratch worktrees `wt-check`, `wt-check2` and `wt-check3`, through `tools/fork-worktree remove`, their trial edits discarded first (each was a copy of what the branch carries);
  - then `/workspace/tmp/m6-t19/` itself: 130 MB of scratch, the unpacked pin trees and the suite logs, whose counts are in `stage-e/`.
  - `git worktree list` shows none of them.

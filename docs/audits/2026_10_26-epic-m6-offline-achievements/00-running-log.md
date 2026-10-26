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

# Mini Retro: M6.P2 T17, cloud setup, sign-in, connections, content and settings backups (#664)

**Completed:** 2026-10-26
**Scope of this retro:** the T17 lane at Extended depth, from stage A to the second hand-back:
- the read of 14 files (11,180 lines) at `8ebaf8daad`, under a security lens, with two seats (GPT-6 Astra at `max`, Gemini 4 Argon at `high`);
- seven bugs, #1128 to #1133 and #1136, and the audit issue #1134 (23 items);
- seven streams and one correction;
- two guest windows.

Not retro'd here: the coordinator's acceptance; T16's twins of S2 (#663); the why table's pairs (T18, #665); #909's line; #1127 and #1117.

**Commits:**
- `reviewed-at`: `f3803436b8` (the dispatch tip; the 14 at `8ebaf8daad`'s bytes).
- `fixed-at`: `479cd96c24` (S7, the last fix). The others: S1 `59a5a8860e`, S2 `1def91bdfc`, S3 `f8feb15bb4` corrected at `c3e260861b`, S4 `0ffe7cd94f`, S5 `1d8271a1f3`, S6 `3e95bf18f4`.

## What the slice did to the two time-to-play numbers

**Nothing, on either number. These scripts are off the launch path, and the fixes change no line that runs between a press and a game's first frame, or between a game's exit and the next first frame.**
- The last recorded numbers are `docs/vm-qa-log.md:170`, the 2026-10-06 replacement image: 0.603 s to first pixels, 1.33 s exit backup, 1.017 s rapid relaunch. No image was built from this slice, so there is no new measurement, and none is claimed.
- **Where each fix runs:**
  - S1, the phone sign-in page, and S4, a connection's save, run from the cloud setup pages.
  - S2's allowlist runs in the content scripts, from the transfer and systems pages. S2 adds one function call per run, a split of a short string.
  - S3 runs on an explicit backup; S5 on the systems page; S6 on the setup page's folder seeding.
  - S7 runs on a settings restore, from its menu.
  - The automatic syncs at a game's exit and at startup are T16's scripts, which this slice did not change.
- **The one boot-time script here**, `cloud_log_scrub`, is a read once a device has recorded it (F-18), and it was not changed.

## What the ES slices inherit (T18, #665, and the interface's lane)

- **The why table's gaps.**
  - `CloudText::whySentences` at the ES pin `16dbac5211` holds neither `ANOTHER CLOUD SYNC IS RUNNING` nor `A SYNC IS ALREADY RUNNING`. S6 moved the script to the rule's word (D-UI-031), which is a translated msgid elsewhere at the pin (`ThreadedCloudSync.cpp:92`) but not a table row.
  - `backuptool:1495`'s D-UI-117 sentence has no pair either. `localizedWhy` returns an unpaired sentence as written, so a French screen reads English.
  - S3's refusal prints `SOMETHING WENT WRONG`, which the table knows, because no sentence there fits.
- **The sign-in window's contract.**
  - `CLOUD_SIGNIN_DEBUG` is read with `g_getenv`, so any value, `0` included, logs every key, and `cloud_oauth` passes its environment through (F-12).
  - Only gesture navigations are filtered, and the allowed host is the last two labels.
  - The window's memory on a host-local page is 104, 98 and 42 MB, 245 MB together (`guest-cycle/w2-signin.out`). The tool's default page, `example.org`, is a network read this slice's rule forbids; a page on the host carried the load, and the QA WebDAV root's 401 was kept as the FAIL it was.
- **The phone page's states after S1:**
  - an icon request answers 404 and spends nothing;
  - anything but four ASCII digits gets the PIN prompt and spends nothing;
  - a wrong four-digit PIN spends one of ten, and ten lock the serve with 403;
  - the paste flow's failure text is escaped.
  - From the host the page is `CANNOT` under user-mode NAT (only ssh is forwarded). That is a harness gap: a `hostfwd` for the serve's port, or a second guest.
- **S5's exit 1.** `cloud_content_restore --set-systems` now exits 1, *"Nothing was changed: the selection couldn't be saved."*, when its write fails, where it exited 0 with a short `OK`. How the systems page shows that exit is T18's read: the page has only ever seen 0.
- **S7's refusal** reuses *"THIS BACKUP HOLDS FILES A RESTORE CAN'T PUT BACK"* for a link, device or fifo member, and the log names the member. Settings restore's pages see one more way to reach it.

## What worked well

- **Two seats, each worth its call.** Both found F-20, the option-shaped key, independently (A-45, R-40), and the fixture confirmed it with the donor's rclone.
  - Astra corrected nine first-draft claims, among them *"rclone's error carries the URL, not its secret"*.
  - Argon, given the lane's grades of Astra, reversed two of them (A-49, A-23), and the artifact supported its narrow form.
  - All 99 items were re-read at their lines (`stage-c/rereads/`).
- **The packet was trimmed before it left.** It went from 437 KB, the size at which Argon failed on T30, to 295 KB. The scan stopped the build on 22 unreviewed hits; each was read by shape only and dispositioned by name, and none was a value.
- **The guest made the findings real.** On the image's own paths and the QA backend:
  - `--delete-excluded`, and on its own `--include=*` (R-9), deleted a save;
  - `../.config` sent 3,418 files of `/storage/.config`, `rclone.conf` among them, to the cloud;
  - a full restore planted a symlink and left a revert's mark, which became F-24 and S7.
- **The product unmodified in a sandbox.** S7's fixture ran the real `backuptool restore` in an unprivileged bubblewrap sandbox with `/storage` on scratch. No path rewriting, so no fixture artifact could stand in for the product.

## What was harder than expected

- **S3's regression stood for an hour.** S3's check held every backup form, and refused every name where `es_systems.cfg` could not be read. My own fixture passed, because it wrote an `es_systems.cfg`. `tools/last-good-scripts-test`, run first at S7, failed three checks, and `c3e260861b` corrected it. The coordinator has written the rule: a stream that changes a script the suite covers runs the suite before its commit.
- **Fixtures that rewrite paths have to live outside them.**
  - On the guest, the content fixture's scratch root sat under `/storage`, then `/tmp`. Its own rewrite caught the root twice, and the scripts failed for the fixture's reasons (a missing lock directory read as "held"); `/var/tmp` worked.
  - S7's sandbox inherited the host's `TMPDIR`, and `mktemp` failed inside it (#549's lesson); `--clearenv` fixed it.
- **A brief's claim about another repository's table** (S6: *"which the table knows"*) did not hold at the pin. It was read only during the stream; #1133's criterion was reworded.
- **A numbered fault injection moved.** The suite breaks the Nth `mktemp`. S7's first cut added a temporary file in front of it, and PL-006 failed; the fix without the temporary was also the cleaner code.
- **My slips, each caught before it stood:**
  - `register-check` was not chained into S2's commit (its four lines were the coordinator's row, as ruled);
  - three typed times (a heading's `06:3x`, RETURN's START `07:59:20`, the suite's `08:3x-09:0x`), each replaced from a command or a comment;
  - a `return` inside the revert's loop that would have skipped the copy, rewritten before any run;
  - a `sed` with the wrong indentation, which matched nothing.

## What we discovered

- **busybox `tar -tv` prints a hard link as `-`**, with ` -> <target>` after the name. A type check that reads only the mode column passes it.
- **`--max-delete` is fed, not bypassed.** The preview takes the same flags as the apply, so it counts what they make it count, and the apply deletes exactly that many.
- **rclone joins `ROMs/../.config`** to the content root's `.config` on WebDAV, so a traversal in the source became a traversal in the cloud.
- **The installed `cloud_oauth` on M7's sign-in image differs from `8ebaf8daad`'s**, outside every line F-01 and F-09 rest on (`guest-cycle/hashes.out`).
- **`backuptool backup`'s credential refusal exits 1, not 5:** `write_archive` returns 5, which the command maps to its why at `:1858`. The brief's wording was the function's.

## Adjustments, Instruction-Recommendations mode

These are proposals for the coordinator.

1. **A fixture that rewrites absolute paths in the product's scripts asserts that its scratch root is outside every prefix it rewrites.** A one-line check would have saved two guest re-runs. Better still is the sandbox shape S7 used, where nothing is rewritten.
2. **A host sandbox starts from an empty environment** (`--clearenv`), because #549's lesson applies to every execution boundary, not only Docker.
3. **A brief that cites another repository's table names the read that shows it**, so the stream does not discover the premise wrong.
4. **The rule written today** (a stream runs `last-good-scripts-test` when it changes a script the suite covers) is the coordinator's, in `docs/reviews/plan-for-the-plan.md` § 6b. No further change.

## Scoped audit (the close-out's own checks)

- **AC conformance:** #664's seventeen criteria against their artifacts: `04` § Acceptance-criteria scorecard and the hand-back's list. Checkbox 3 was reworded by the coordinator. PASS.
- **Cornerstone spot-check:** nothing under `packages/`, `projects/` or `tools/` changed at stages A to D (`git diff --stat f3803436b8 045cc316ea`). Stage E changed only the seven fork-own files its brief names. Nothing ran on a unit or a person's cloud. PASS.
- **Interaction-defect scan:** `03` § 3.5's seams. T16's `RCLONE_NET_OPTS` twins are routed to #663 under D-CLOUD-185. The ES table's gaps go to #665. S5's exit and S7's refusal are T18's to read. PASS, with the two routes open.
- **Futro verification** (`docs/futros/2026-10-25-m6-cloud-sync-and-saves.md` § T17 kickoff addendum, `:255-301`):
  - **The assumptions:**
    - thirteen fork-own and `backuptool` the fork's rewrite: held;
    - `--match --apply` the only deleting path, under the preview's count: held, and F-02 showed the count is fed by the same flags;
    - M7's work cited by number and never read from its worktrees: held (#1117 at F-13);
    - *"two writers through `rclone config` (`cloud_setup`, `cloud_remote`)"* did not hold. The brief's version 2 corrected it (`cloud_setup` writes none), and F-20 found `cloud_remote`'s keys reaching rclone's flags.
  - **The four known unknowns, each answered:**
    - (1) what the scripts source: stage A's `r38`, `01` § Scope's table;
    - (2) `read_state` and the per-session log: Astra's A-2 (the state's `error` carries only `_write_config`'s fixed sentences) and F-12 (`window.log`);
    - (3) the phone page from the host: `CANNOT`, with the gap named (`guest-cycle/w2-phone.out`);
    - (4) T16's *"15 oracle rows"*: 5 name this slice's scripts (`01`, r35).
  - **What could be missed:** no credential-shaped line quoted; `rclone.conf`'s 0600 observed, not assumed (`fixture-mode.txt`, `w2-mode.out`); M7's work not filed as a bug; `--max-delete` read as a cap; nothing asked of a unit. None of those happened.
  - **Not foreseen:** F-03's upload, F-20's option key and F-24's restore, found by the guest and the seats. PASS, with that gap noted.
- **Housekeeping:** no `package.mk` in the slice. `tools/last-good-scripts-test` PASSED over the fixed tree (1,379 PASS lines). PASS.
- **Harness self-coverage (check 7):** every fixture fails on `8ebaf8daad`'s bytes and passes on the fix. The two fixture defects met in the guest window are recorded, and the sandbox now clears its environment. PASS.
- **Documentation freshness:**
  - no new proper noun;
  - `docs/cloud-sync-changelog.md` takes the player-visible changes (S1's phone page, S5's and S7's refusals) the day they land on `next` (`change-log.md`), which is at the coordinator's merge;
  - the rocknix.org page's drift (#42) is untouched, since nothing here changes a setting a player sets.
  - PASS.

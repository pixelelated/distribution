# Futro: the cloud sync and saves area epic (#1047), at T13's kickoff (#660)

**Prepared:** 2026-10-25, by the M6 coordinator lane (D-WORKFLOW-189),
before T13's dispatch to the T1 session; the area's three slices are T13
(the cloud test harness, Independent), T16 (the sync core, Extended) and
T17 (setup, sign-in, connections and content, Extended). The inputs: plan
§ 4 to § 6, order § T13, § T16 and § T17 at `2174265e9c`, the nine harness
tools at `8ebaf8daad`, `rclone-cloud-sync.md` on the working tree, the
register rows D-QA-058, D-CLOUD-181, D-WORKFLOW-186, blindspot 31, and a
read-only research pass over the nine tools (churn, callers, recorded runs,
the backends, the rule) whose notes carry every figure's command.

## 1. What do we know and what are we assuming?

**The plan, in the order's words:** T13 is *the cloud test harness*, lens
brittleness, Independent: `tools/cloud-round-trip` (7,808 lines) and the
backends that prove the cloud slices; *a harness that agrees with itself is
blindspot 31; read before the code it proves*. Closing evidence: the audit
folder, the lint, **each guard's positive recorded**, the punch list through
Phase 7.

**Nine paths, 10,165 lines, all fork-own, reach `n/a`** (the inventory at
`2174265e9c`): `cloud-round-trip` 7,808 (77% of the slice), `cloud-test-backend`
920, `cloud-connections-test` 307, `cloud-census` 306, `cloud-pair-migration`
243, `cloud-save-integrity` 219, `cloud-input-test` 132,
`cloud-capture-stamp-test` 116, `cloud-save-integrity-test` 114; 108 fork
commits since the base, none on `upstream/next`; the nine are byte-equal
between `8ebaf8daad` and the coordinator's tip.

**Assumptions the plan leans on and does not state:**

- *That the nine are live.* One is not: `cloud-pair-migration` refuses with
  exit 2 before doing anything (lines 58-63) because the script it needs,
  `cloud_migrate_layout`, was deleted on 2026-10-08 (`e6645cb5ea`,
  D-CLOUD-175/#508). Its 243 lines are counted as read.
- *That what the harness asserts can run.* The pair registry's apply step
  calls `cloud_reconcile` (line 1771), a device script that has never been
  added to the tree; the code says so in a comment.
- *That the harness is run.* `vm-qa` at the hash runs the single-device suite
  and the opt-in LINK cells of `cloud-round-trip` and calls
  `cloud-test-backend`; the other seven tools have no caller, and five have
  never been named in `docs/vm-qa-log.md`. CAP (14), KILL (12) and PAIR (9)
  cells run by hand.
- *That "each guard's positive recorded" has a record to point at.* No
  work-log line since 2026-09-01 pairs `cloud-round-trip` with the word
  *positive*; what the log holds is the suite failing on its own state (two
  guests on one QA folder, 2026-09-15; the `/GAMES` default, 2026-10-02; *has
  never run end to end* two weeks after its first commit). Two tools carry
  their own control: `cloud-capture-stamp-test` (the old `finish()`),
  `cloud-save-integrity-test` (synthetic corruption against rclone's hash).
- *That the rule a reader is told to read is current.* `rclone-cloud-sync.md`
  is under an open drift bug (#909: five stale rclone facts, one of them
  this slice's: the no-network step's exit), and its `paths:` loads it for
  three of the nine tools only.
- *That the standing baseline is pinned.* D-QA-058's MinIO/S3 and the SMB
  backend run `:latest` images; FTP installs `pyftpdlib` by `pip` at first
  `up`.
- *That the host is the device.* The rule says the host's rclone is not the
  device's; two tools run the host's rclone (`cloud-connections-test` through
  the module's choice of binary; `cloud-save-integrity-test` as its hash
  oracle, by design).

**Substrate preconditions, and how each was verified:** `rclone`, `sshd`,
`ssh-keygen`, `python3` and a usable `docker` are on the host (checked
2026-10-25); `xmlstarlet` is not, which is why a host-generated H700 plan
lacks its bootloader chain (T23's finding) and may matter to any tool that
reads `SUBDEVICES`. The M7 lane holds the host's guest windows; an M6 guest
cycle runs only in a window the coordinator grants after M7's FINAL RETURN.

**Build-vs-adopt:** not applicable; the harness is the fork's own.

**Base divergence:** the coordinator's branch ends at D-WORKFLOW-209; the
lane's worktree stacks on `2174265e9c` with that branch merged in; the nine
are unchanged across all three.

## 2. What known unknowns need investigation?

1. What the two `cloud_reconcile` fixtures (A5 and the retention-ordering
   kill) report today: FAIL every run, or skipped, and whether any recorded
   PASS line ever covered them.
2. Whether every "reached the cloud" assertion in `cloud-round-trip` goes
   through `epath()` and the existence-checking `cat` (blindspot 31's fix),
   and whether `caps()` marks rather than skips on every backend where a
   step cannot hold.
3. How many assertions a PASS line certifies: `vm-qa` says *27 steps*, the
   tool has 46 `step()` and 461 `check()` calls, the 2026-10-08 log says
   *108 checks*.
4. Whether the 38 `time.sleep` waits around SSH, serial and monitor actions
   carry blindspot 32's shape (an order assumed from wall-clock time).
5. What the vendored copy of the whole tool under
   `docs/qa-logs/2026-10-07-cloud-validator/` is, and whether a reader could
   mistake it for the tool.
6. Where a harness defect is filed: no issue has ever been titled after a
   harness tool; the 19 bug issues naming `cloud-round-trip` are product
   bugs it proved.

## 3. What patterns from prior work apply that we haven't named?

T14's brief (the state tests, Independent): the brittleness table with one
row per test (dependencies and their failure modes, the last catch, the
caller or `nobody`, the positive or `none`), the seat's packet scanned before
it is sent, the busybox rule for anything that runs the scripts. T15's: a
suite judged by whose tools ran it (D-QA-063's lattice; `--host-diagnostic`).
T45's: a tool's own column is a claim, the second command is the evidence.
The 2026-09-15 and 2026-10-02 failures: the harness's own state (a shared
QA folder, a stale default) is the brittleness, not the product.

## 4. What could we be missing?

**Agent-execution simulation, a fresh lane with the brief:** it reads
`cloud-census`'s header, sees `--host root@192.168.1.81`, and runs it to
"see what a game exit writes" -- against the maintainer's handheld. The brief
forbids every device and every person's cloud by name, and `cloud-census` is
read, never run. It starts a guest for the round trip during M7's window:
the brief holds the guest cycle behind a coordinator-granted window and
makes the host-side tests stage A's whole work. It reads a round-trip PASS
as proof of the product: blindspot 31 is the lens, and the brief asks for the
assertion shapes, not the verdict. It fixes the harness at stage A because
it is the fork's own: fixes are stage E's, under stream briefs. It counts
`cloud-pair-migration`'s 243 lines as read and finds nothing: the brief says
the tool exits 2 and asks for its disposition. It sends the seat a packet
with the backends' credential-shaped lines (`rclone obscure`, the sshd
key): the packet is scanned first, and a hit is redacted.

**Pre-mortem.** A month on, T16 closes on a round-trip PASS whose two pair
fixtures never ran, whose no-network step faked `ip`, and whose MinIO `cat`
of a missing key exits 0 -- the harness agreed with itself and the product
shipped a regression the harness could not see. The guard is T13's
assertion-shape table, written before T16 is dispatched, and the epic's
criterion that names it.

**Blindspot check.** 31 directly (the lens); 32 (wall-clock ordering: the
sleeps); 71 (a stale fixture name; its guard was re-pointed at a script
that then vanished -- a T15 lead); 22 (a probe that cannot report absence:
MinIO's `cat`); 38 (a device used without a yes: `cloud-census`). New: a
harness whose closing evidence names a positive that nobody recorded.

**Replaced mechanism.** None: a read slice replaces nothing. The retired
`cloud-pair-migration` is a replaced mechanism of an earlier phase; the
futro asks what it guarded (the mixed-installation gate, D-CLOUD-158) and
whether anything guards that now.

**Honesty check.** The archetype was the fresh lane; a second, the M7 root
reading the slice's bugs, found one more: a harness bug filed on the fork
with a `bug` label counts against the candidate's step 0 like a product bug
-- the brief says where a harness defect lives.

## 5. What adjustments or investigations must happen BEFORE execution?

**Written into version 1 of the brief:** the retired tool named with its
disposition question; `cloud_reconcile` as a stage-A read; the device ban
by tool name; the guest cycle held behind a granted window; the assertion-
shape table as a criterion; the packet scan; the count question; the rule's
drift bug and its `paths:` as leads for the coordinator; the unpinned images
as Q4 rows; the order's two reading directions reconciled (T13 reads the
assertions first; T16 inherits the table).

**Filed or posted now:** the epic #1047 with these as context. **Left for
the stranger's proof:** every figure above.

### Errata from the stranger's proof of T13's brief (version 2, 2026-10-25)

A read-only reader with no context checked 76 rows of version 1 (62
verified, 6 wrong, 8 partial; 7 API calls). What version 2 corrects, each at
the place it lands:

1. **"46 `step()` calls in the single-device suite" was the whole file's
   count.** By AST, `run_steps` (lines 623-1716) holds 32, `prepare_device`
   adds 2 per device, and 12 are the registry runners' headers. The
   assertion-shape criterion now asks the generator to assert its count
   against the AST at the hash, with 32 + 2 and the cells as the
   coordinator's figures, not a bare 46.
2. **`PAIR_FIXTURES` has 10 cells, not 9** (`RETENTION` is the tenth), so the
   cells are 44 with SOLO, not 42.
3. **The rule's `paths:` names four of the nine**, `cloud-capture-stamp-test`
   among them; the other five load no rule.
4. **#909 is open with all six checkboxes ticked while the rule on this tree
   carries all five stale sentences**: a tick without the fix here, for the
   coordinator to trace.
5. Smaller: the registries are at 181 and 2458 onward, not 309-1714 (that is
   the step span); the file grew from 4,953 to 6,989 lines on 2026-09-10,
   not to 6,700; the 2026-09-15 quotation is a work-log heading, not a
   friction line; the ledger holds about 55 round-trip verdict lines, the
   newest including 2026-10-06's *106 PASS* -- a fourth count for one suite;
   D-CLOUD-051 is an open decision, not a decided row; `vm-qa` also calls
   the backend's `caps`; the T1 worktree is `m6-os-launch-control-state-648`;
   D-INFRA-032 became the M7 lane's at 04:47, so M6's next is 033.

Not checked by the proof, and left to the lane's stage A: the four bare
tests' runs, the backends' `up`/`down`, the seat.

### T16 kickoff addendum (written with the brief's version 1, 2026-10-25)

Read with the brief `docs/reviews/briefs/cloud-sync-core.md`; the research
digest behind it was taken read-only at `2174265e9c` (lead, not evidence).

- **What we know.** 14 paths, 8,316 lines, every one the fork's own (145
  commits since June, all fork identities; upstream carries the directory
  at the base's bytes and brings nothing); two 2,300-2,500-line copy-twins
  (`cloud_backup`, `cloud_restore`) and a 1,704-line capture carry 6,538
  of the 7,827 read lines; T13's assertion table (79 rows: 24 both ends,
  46 synthetic, 8 device report) is the oracle, and three of the nine
  scripts are named by no row (`cloud_net_ready`,
  `rasteratops-settings-archive`, `cloud_sync_cleanup_duplicates.sh`).
  Three stamp families with three owners, one `flock`, exits 69 and 75, a
  90 s bound. The order's area figures (+28,279 lines, 451 commits, 19
  blindspots, 47 bugs) are not the slice's (+6,976 / -338, 145, 15 entries
  about these scripts, 32 closed bugs for "cloud sync").
- **Assumptions named.** The guest is the M7 candidate image: the installed
  scripts are diffed against the read tree before any guest verdict is
  used (T22's PL-05). The rule `rclone-cloud-sync.md` is under #909's
  drift (exit 4 against the script's 69): the scripts are read as the
  truth. D-CLOUD-076 is superseded by 109/130: the lane states which the
  tree implements and files no bug for the superseded design.
- **Known unknowns.** (1) How many of the twins' 92 functions are identical
  by copy, and which divergences are deliberate; (2) which functions no
  oracle row reaches (the `unrowed` column); (3) whether the exit sync's
  median on the current image still meets D-CLOUD-119's 3 s (cited from
  `docs/vm-qa-log.md`, measured once if the window allows).
- **Patterns.** T22's Extended recipe and guest-cycle conditions; T13's
  twelve drivers and their `unfixed|fixed` shape for any stream; the
  `rc=$?` rule and the fixture rule (#307); blindspots 10, 22, 28, 31, 33,
  38, 39 as questions put to each script.
- **What could be missed.** A reader taking a device-report row's PASS as
  a verdict on the code; a reader re-filing the harness's own defects
  (#1057-#1070 are `tools/`, fixed) as this slice's; a reader running a
  cell against a person's cloud (blindspot 38: never); a reader reading
  the twins twice and the small scripts never; a reader measuring time to
  play on a guest whose RetroArch driver cannot draw (blindspot 39:
  `tools/time-to-play --vm` puts the guest in the state it needs).
- **Before execution.** The stranger's proof of version 1; the worktree cut
  from `2174265e9c` with the coordinator's tip merged; #663's body rewritten
  with the seventeen criteria and the VM line (Yes: the host, then one
  guest window); the dispatch to the idle T1 session, which ran T13 and
  knows the harness.

### Errata from the stranger's proof of T16's brief (version 2, 2026-10-25)

- A slice's `!` exclusions in `slices.json` are brace globs; a membership
  block that stands in for `slice_of` must expand braces or it excludes
  nothing (version 1 wrote 25 paths for a 14-path slice). The block's own
  count is checked against the order's before anything reads `paths.txt`.
- An oracle's class list is quoted from the oracle's own record (T13's
  `04` `:228`), never reconstructed from memory: version 1's both-ends list
  was wrong in most of its entries.
- A stamp name is grepped before it is written down: `last-restore` does
  not exist; the twins write `last-settings-restore` and `last-run`.
- A lock's holders are read from the files: the capture never takes
  `cloud_sync.lock`.
- A `readonly A=1 B=2` line is missed by `^A=`; the exits grep allows the
  prefix. `comm` and `sort` run under `LC_ALL=C` in every block.
- A blindspot is glossed by its own title, not by the lesson the author
  remembers from it (31 and 33 were glossed by other entries' lessons).

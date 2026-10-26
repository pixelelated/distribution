# Futro: the offline achievements area epic, at T19's kickoff (#666)

**Prepared:** 2026-10-26, by the M6 coordinator lane (D-WORKFLOW-189),
before T19's dispatch; the area's two slices are T19 (the proxy, Extended)
and T20 (the RetroAchievements and offline pages in EmulationStation,
Extended, under the interface epic #700). The inputs: plan § 4 to § 6,
order § T19 and § T20 at `2174265e9c`, the 27 paths at `8ebaf8daad`, the
EmulationStation callers at `16dbac5211`, the fifty `D-RA-*` rows,
blindspots 43, 44, 46, 64 and 65, the proxy's own epic audit (#186), and
four read-only research passes (the sources, the eighteen patches against
the cached pin, the record and the tools, the neighbours) whose notes carry
every figure's command. The brief is
`docs/reviews/briefs/offline-achievements-proxy.md`.

## 1. What do we know and what are we assuming?

**The plan, in the order's words:** T19 is *the offline achievements
proxy*, lens security and new functionality, Extended: *a network listener
holding the player's account token, all fork-own (+3,666), and the
cheapest product area to finish; its 18 fork-written patches to the
upstream proxy are read here, not in the patch tables*. Closing evidence:
the audit folder, the lint, `tools/ra-offline-test` and the proxy's suites
on the VM, the punch list through Phase 7, `reviewed-at` and `fixed-at`.

**Twenty-seven paths, 5,369 lines** (the inventory at `2174265e9c`): nine
fork-own files, 3,666 lines -- the ctl 2,455, the three python helpers
951, the recipe 157, the unit 46, the daemon file 10, the two sibling
recipes 47 -- and eighteen vendor-carried patches, 1,703 lines, against
upstream RAOfflineProxy at `c7ebd1b6e7`. The service's own code is not in
the tree; it is the cached tarball's, read with the patches applied.

**Assumptions the plan leans on and does not state:**

- *That the tarball is in the download cache.* The patches digest read it
  there and matched its sha256 to `PKG_SHA256`; the stranger's proof checks
  the file still exists. Without it the patches are read as diffs alone and
  the service's bind, validation and export code stay unread (a `CANNOT`,
  not a fetch).
- *That the service runs as upstream wrote it to run.* It runs as root with
  no hardening directive in the unit, on a port shared with the sign-in
  serve (`cloud_oauth`, T17's), answering the account's data to any local
  client. The order's "cheapest product area to finish" rests on the code
  being fork-own; its exposure is the unit's, which no earlier slice read
  (T22's audit has no proxy row).
- *That the host can run the proxy's suites.* It can run one
  (`raofflineproxy-integration-test`, synthetic HTTP) and the syntax checks;
  the other three need the image's installed modules on a guest, and the
  award proof needs the live server and the QA account, which spends an
  achievement each run (D-RA-006 open). The host's python is 3.14 against
  the image's 3.10.
- *That the window fits.* Two boots (one with a NIC, one without) and five
  proofs plus four constructed positives; the award proof is last and falls
  to `CANNOT in this window` with the 2026-10-06 run cited if the bound is
  reached.
- *That "the patches are the fork's" means "the fork fixes them".* A defect
  on a patch's `+` side is; a defect in upstream's unpatched code is a
  contained fix here and a #585 line (D-WORKFLOW-164), never a submission
  (D-WORKFLOW-165). Nothing has been sent upstream from this package: ten
  drafts, every base older than the pin.
- *That the ctl's protocol and the pages agree.* The pages parse the last
  stdout line and a handful of stamps; the ctl's `>>> ` vocabulary is
  larger, `have_account` is named by a page comment and absent from the
  dispatch, and the refresh's notes go to stdout. T20 reads the pages; T19
  writes the table T20 inherits.
- *That the base is fresh.* The lane branch is cut from the P1 tip
  `2174265e9c` with the coordinator's tip merged; the register's highest
  Decided row on the coordinator's branch is D-CLOUD-185 (D-WORKFLOW-188 on
  the P1 branch only).

**Substrate preconditions, each with its verification:** the cached
tarball (`ls`, `sha256sum`); the M6 image copy `/workspace/artifacts/m6-t2-20261023/`
(`ls`; its `069fc2704421` is the M7 candidate); the QA account file
`~/.ROCKNIX/qa-accounts` present (mode read, never its values); the
retained donor's busybox for `last-good-scripts-test`; GNU `patch` on the
host; `tools/raofflineproxy-*` answering `--help`; the host file free for
a grant. A build-vs-adopt answer: adopt -- the proxy is upstream's, carried
with patches; unchanged.

## 2. What known unknowns need investigation?

- The service's bind address and request validation, `state.py`'s probe
  cadence against the pages' *no file means online* reading
  (`OfflineAchievements.cpp:179-186`), and `es_export.py`'s write of
  `cached_game_ids.txt`: read from the patched tarball at stage A.
- The upload endpoint in `log_uploader.py` and what the bundle carries:
  read at stage A; the consent test on the no-NIC boot proves nothing
  leaves without an explicit `true`.
- Whether `tools/last-good-scripts-test` holds a positive for any ctl path,
  or only setsettings' `cheevos_custom_host`: a count at stage A.
- Whether the retired patches 006, 014 and 017 were replaced by upstream
  behaviour that keeps what they guarded (eviction of a game row;
  connection reuse; subset awards): the replaced-mechanism question,
  answered from the tarball.
- Whether the proxy's `-nt` comparisons and the topup mark's mtime behave
  on a device without a clock: a design read; the guest has a clock, so
  the proof is the code's, recorded as `design`.
- How long `ra-offline-test` takes end to end on this host: the
  2026-10-06 record's timings decide whether it fits a 60-minute window
  after the other proofs.

## 3. What patterns from prior work apply that we haven't named?

- **T17's shape, one port over.** A listener holding a credential: T17
  found the sign-in's phone page bounded (16 connections, 15 s, 64 KiB) and
  the pin gate (#1128); the proxy's port has none of those by the digests'
  read and no identity at all. The same tables (§ The listener, § The
  credential's paths) and the same stream shape apply.
- **T22's unit table.** The services slice read every unit under the
  Extended recipe; the proxy's unit is compared directive by directive
  against that table rather than against the ideal.
- **T30's token files.** The per-emulator credential handling was fixed
  there (PL-009/010/020/021); T19 does not re-find it and cites it.
- **Blindspot 44.** The top-up was once proven at fixture size and failed
  at the device's numbers; T19 reads the bounds, and where a stream touches
  one, the positive is at a number the record names, not three games.
- **Blindspot 65.** The ctl was once shimmed in a proof; nothing is shimmed
  here -- the real ctl, the real unit, on the guest.
- **Blindspot 46.** Four unobserved claims in one day about this very
  subsystem: a name read as a behaviour (`have_account` on a page comment
  is this shape today). Every claim in `04` cites a line that does the
  thing.

## 4. What could we be missing?

**Agent-execution simulation.** A fresh lane with the brief:

- *runs the ctl on the host "for its usage"* -- the ctl writes `system.cfg`
  and calls `systemctl`; the brief says it never runs on the host, and the
  runs block's syntax check reads it from `git show` into scratch;
- *reads the tarball from M7's prep directory* because it is nearer than
  the cache -- the brief names the cache's path and forbids M7's roots;
- *calls patch 001's 429 passthrough a bug* without reading
  `forward_to_upstream_result` in the tarball -- Q4 says what to read first;
- *spends the QA account's cheap achievements on repeated award runs* --
  the award proof runs once, last, and D-RA-006 is cited;
- *files the root user and the empty hardening as a bug with a
  `ProtectSystem=` fix* that breaks the writes under `/storage` -- a stream
  would prove any directive on the guest with the scan and the flush, and
  the coordinator rules at stage D whether hardening is this slice's change
  or a design row;
- *treats the port shared with `cloud_oauth` as T17's* -- T17 is closed;
  the seam is recorded here and becomes a coordinator's Backlog if
  confirmed;
- *takes the eighteen patches as the fork's code to rewrite* -- they are
  diffs against upstream's functions; a change is a patch's change, and
  the fuzz-0 apply is the test that it still fits.

**Pre-mortem.** A month on, the proxy is found to have served the account's
unlocks to a process that was not an emulator, or a stamp written 0644 by
root under systemd carried the account name into a settings backup -- the
digests' reads make both plausible, and neither is proven until the guest
window reads the modes and the port. The second failure: the window ran
long on the award proof and the consent test on the no-NIC boot never ran;
the ordering and the `CANNOT in this window` form exist for that.

**Blindspot check.** 43 (a credential in a log: the client's own logging
is in the tarball; read it), 44 and 65 (above), 22 (a probe that cannot
report absence: `count_ready` printing 0), 39 (a tool judged by whether it
ran: the integration test's own summary line is the verdict), 75 (counts
from the wrong tree: every figure here names its hash).

**Replaced mechanisms.** Patches 006, 014 and 017 were retired as
upstreamed; what they guarded is listed in § 2 as a known unknown.
`cloud_oauth`'s serve and the proxy share a port by design nobody wrote
down; the record of the choice is the row to look for before calling it a
defect.

## 5. What adjustments or investigations must happen BEFORE execution?

Carried into the brief: the window's two boots and the order of its
proofs with the award proof last; `--fuzz=0` on the hand-applied patches;
the four constructed positives named with what falls; the host-only tools
listed with their `CANNOT` forms; the username-on-argv and the readiness
check named as the digests' leads, to be read before they are called
anything; the T20 inheritance table as an output, not an edit. A stranger's
proof of the brief runs before dispatch; version 2 records what it finds.

**Streams predicted: two** -- the username moved from argv to the
environment at the four sites, and the readiness check narrowed to the
loopback forms -- with the unit's hardening and the shared port put to the
coordinator as design questions rather than streams. The addendum below is
written with the brief's version 1.

### T19 kickoff addendum (written with the brief's version 1, 2026-10-26)

The five questions above are T19's; T20's addendum is written with its own
brief under #700's futro, where the interface's lane reads it.

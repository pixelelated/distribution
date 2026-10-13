# #577 Wi-Fi picker source proposal — October 13, 2026

**Evidence level: static source inspection only.** The scoped ES proposal is
prepared on `feature/m7-wifi-picker-577`, based exactly on accepted
`c8dc72cf9ec00ab00d6c4a9fcdcea1746c6f1f78`. See `source-review.json` for its
commit, file hashes, actual checks and unchanged-function comparisons. No
compiler, test suite, subprocess fixture, browser, service, container or VM was
launched. No product pin, translation catalogue or shared record was edited.
This packet does not close an acceptance checkbox or claim source readiness.

ES commit: `2e84879d488e22a312b5a3e179836f927c448738`.

Coordinator: Herdr w4:p2, `m7-player-setup`, published `0ea6eaf74a` at assignment.
The previous GTK4 direction and ES allocator trim are independent and unchanged.

## Source result

- The native `MenuComponent` reserves its final dimensions at construction:
  full-screen where ES normally uses full-screen menus, otherwise 75% of screen
  height at the existing 15% top offset. The native scrolling `ComponentList`
  and footer keep their bounds when answers arrive. A permanent two-line status
  band occupies the top of the original list region, using native
  `TextComponent` and a background-free `BusyComponent` spinner. Busy exists only
  while scanning; it cannot keep PowerSaver paused after completion or close.
- Initial search and refresh use this band. Old rows remain visible during a
  pending refresh. A successful empty answer uses existing no-networks copy;
  command/read/signal/timeout failures have separate retry copy. A failed range
  query retains prior network names, while saved/current metadata is queried
  again and guarded as unknown if those queries fail. Partial failed output is
  discarded. REFRESH remains the retry action.
- Identical answers keep the actual row objects and scroll offset. Changed
  answers restore the selected SSID, or clamp the former index to a valid row
  if it vanished. The native list then keeps that selection in view. Footer
  focus is retained. An empty result focuses REFRESH. Changed answers use the
  native cursor-centred scroll calculation; exact mouse-drag pixel anchoring
  across a changed result is not a new capability and still needs frame review.
- One weak registry on the UI thread identifies the pending scan. A reopened
  picker attaches to that job. The detached worker captures only its shared
  result and scan mode, with release/acquire publication. There is no posted
  `this` callback, window pointer or API singleton in the scan worker. BACK can
  delete a pending picker immediately. No worker join blocks that destructor.
- Controller activation/navigation is held while scanning; BACK still works.
  Mouse/touch hit testing exposes only the native BACK button during that time,
  preventing a press during loading from activating a refreshed row on release.
  Existing captures and list repeat are stopped at the scan boundary. Buttons
  are never rebuilt inside a callback.
- `WifiScanProcess.h` supplies the necessary isolated process helper. It starts
  each fixed `wifictl` operation in a new process group with `posix_spawnp`, reads
  stdout without blocking indefinitely, limits it to 256 KiB, retains exit
  status, and kills the group on every completion/error path. Command deadlines
  are 30/45 seconds for list/scanlist, 15 for saved, and 10 for current, plus up
  to two seconds per command for direct-child reaping. No shell or timeout
  wrapper is needed. Descendants are reaped by their parents/init. Escaped
  process groups, uninterruptible kernel tasks and frontend termination still
  require the coordinator's outer job/guest cleanup; this is not cgroup control.

Both `wifictl list` and `scanlist` already request a scan. The old automatic
second scan after an empty initial result is removed: one initial request now
produces one outcome, and another request requires REFRESH. Reopening while the
old request is pending reuses it; a later explicit refresh starts a fresh job.

Saved/connected/profile-choice/forget, security-check/open/protected/unknown and
manual-input routing retain their existing functions. Offline achievements,
sign-in and allocator-trim source is untouched. These are source comparisons,
not behavioral regression proof.

## Early blocker outside the assigned source

The production `wifictl` still loses some real backend failures. At coordinator
source `0ea6eaf74a`, `projects/ROCKNIX/packages/rocknix/sources/scripts/wifictl`,
`list_wifi` (line 82) does not check `wait_for_wifi` or the first rescan status;
its final `nmcli | nm_unescape | sed | sort` pipeline can report the last
command's success when nmcli failed. `scanlist` (line 513) also ignores its
first rescan result. The script does not enable pipefail itself (it sources
`/etc/profile`), and its early missing-adapter/missing-nmcli guards return0 for
enumeration. A GUI cannot recover a failure that its backend already reported
as exit0. These are source findings; no synthetic-nmcli reproduction ran here.

The proposal distinguishes the explicit exit2 reproduced by the baseline and
failures detected by its process runner. Full production failure/empty
distinction needs a coordinator-owned backend correction and its own negative
controls. This worker was assigned only GuiWifi and its necessary helper, so
the script remains unchanged. No real-radio observation is needed to test the
script's error propagation: a VM can substitute a failing synthetic nmcli.

## Inputs and upstream applicability

The complete live [owning issue](https://github.com/pixelelated/distribution/issues/577)
and all three comments were read and retained in `issue.json` and
`issue-comments.json`. The issue body corrects its earlier comment: populated
refresh retains dimmed rows. All twelve original baseline frames were opened
and reviewed, including both panel sizes and the byte-identical empty/failure
completion frames; their original index and transcripts are hash-bound in
`source-review.json`. They remain defect evidence for the accepted source, not
evidence for this proposal. No baseline fixture was replayed.

The current `next` checkpoint and rule changes were read without merging them
into this evidence worktree. Source and native menu/list/busy/input APIs were
read at the accepted ES pin. The official upstream file history was checked
again on October 13 and is retained in `upstream-history.json`: its latest
entry is still [cada856d86e3115fbbf0bce09dd761b0ee8fa9fd](https://github.com/ROCKNIX/emulationstation-next/commit/cada856d86e3115fbbf0bce09dd761b0ee8fa9fd),
September 28, already an ancestor of the accepted pin. This bounded file-history
check found no newer upstream picker patch; it makes no exhaustive issue-search
or release-wide claim.

## Coordinator handoff

[Flow and exact EN/FR copy](flow-and-copy.md) are proposals for the coordinator's
canonical map/catalogue edits. [Acceptance matrix](acceptance.md) maps all six
issue criteria to source and **UNRUN** controls. `fixtures/` contains a guarded
synthetic command fixture, a process-runner control, deterministic inputs and
initial-search walk; none was executed here. No reviewed fixed-source frame
exists yet, and the two French additions are deliberately not installed.

Can this be done on the VM? **Yes** — delayed synthetic enumeration and actual
ES rendering prove layout/input/lifetime without a radio or owner credentials.
The live issue already records that decision. The coordinator owns the new
allocation/admission, compiler syntax/build checks, exact executable hashes,
EN/FR frames, regression/lifetime checks, backend repair, canonical references,
public setup-doc follow-up, shared records and integration. Preserve original
failure receipts and record actual process exits before retiring the new owner.
No runtime or build allocation is requested or consumed by this source packet.

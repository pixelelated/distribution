# M7 browser experiment coordination

Updated 2026-10-13T05:55:07.035885+00:00. Owning issues: #570 and #576. The user explicitly
requested separate worktrees, branches and Herdr sessions; the exact request is in
[#570](https://github.com/pixelelated/distribution/issues/570#issuecomment-6138746073).
Source preparation is parallel. Low-memory runtime measurements, full builds,
accepted-cache access and integration remain serialized under the coordinator.

| Scope | Herdr owner / pane | Worktree and branch | Current deliverable / evidence level |
| --- | --- | --- | --- |
| Integration and actual page/script evidence | Existing coordinator w4:p2 | m7-player-setup / feature/m7-player-setup | 22 browser controls plus bytecode/listener comparison complete and retired; integrate evidence, then page/script attribution |
| GTK4 compatibility #576 | pix-gtk4 / w4:p7, tab M7 GTK4 experiment | m7-gtk4-576 / feature/m7-gtk4-576 | COMPLETE: da0ecd8 +10f9b16, reviewed dependency/API/keyboard feasibility and static timeout correction; no build/runtime proof |
| Safe memory reductions #570 | pix-memory / w4:p8, tab M7 Memory budget | m7-browser-memory-570 / feature/m7-browser-memory-570 | COMPLETE: f1987b6 +914b0ad; host-only allocation consumed; coordinator VM measures390KiB import-only saving, component readiness passes |

All three worktrees live under `/workspace/repos/rocknix.worktrees/`.
The two workers start from verified next/origin-next `4a1274ab806bf583c78646d01fb82bb6fb8f9ef7`;
read the newly prepared UA/breakpoint records in the coordinator's checkout read-only.
Their scope overrides old checkpoint next commands. Both prompts were delivered
and actual working activity was observed; these are live sessions, not empty tabs.
Optional startup update notices were dismissed without installing an update.

Workers own only their branches and dedicated evidence directories:
`docs/qa-logs/2026-10-13-gtk4-feasibility/` and
`docs/qa-logs/2026-10-13-proxy-memory-feasibility/`. They return exact changes,
verification limits, blockers and a concrete next experiment. The coordinator
reviews and integrates; workers do not push, update shared records or create
another worker hierarchy. No runtime lease is granted: no VM/device tests,
provider/account actions, full build/cache copy or production pin changes.
The coordinator must allocate those separately with VM-first and #493 gates.

Proxy cost (about76–105MiB PSS in prior bench observations) is measured overhead,
not proof of a leak or the cause. Actual Dropbox trials show pressure in a VM
without its background service enabled. Preserve award queue/database integrity,
reconnect delivery, optional preparation duties and next-game listener readiness.
Prefer upstreamable reductions; service suspension alone does not release RAM.
Do not trade away working offline achievements to obtain a smaller number.

Completed shared VM is retired with [receipt](../2026-10-13-dropbox-breakpoints/retirement.json).
No browser runtime or firmware build is active at this checkpoint. Herdr worker
activity is separate from test completion; inspect their actual returned evidence
before describing a candidate as tested. Keep lanes available after a bounded
return. Current coordinator retains dispatch authority; no other project lane was
interrupted. Private dispatch receipts: `/workspace/tmp/pix570-parallel-20261013/`.

### Bounded host-fixture exception, granted after initial dispatch

At the memory worker's concrete request, the coordinator allocated one source-only
host experiment: fresh import snapshots and in-process synthetic SQLite/award
checks, maximum60seconds aggregate execution and20MiB scratch. No listener,
provider network, owner/production configuration, dependency installs or service
launch; fail-closed network denial and synthetic-path assertions precede execution.
This can attribute host imports only, not target PSS or installed lifecycle safety.
The original service/VM/device hold remains. The grant is recorded in
[#570](https://github.com/pixelelated/distribution/issues/570#issuecomment-6138855457).
Inspect the returned result before granting another run; elapsed time is not proof
of completion. No other memory runtime was active when allocated.

### Completion and next allocation

Both source-only assignments are complete and integrated into the coordinator branch; publication is recorded by the current checkpoint delivery owner. The single worker host run passed10cases in1.79s and consumed its allocation. Coordinator fresh VM bytecode/listener proof is [complete and retired](../2026-10-13-proxy-memory-vm/README.md). No worker runtime, VM or firmware build remains. D-WORKFLOW-163 keeps both candidates diagnostic-only and prioritizes page/script CPU versus reclaim attribution; all runtime is still serialized. GTK4 timeout cleanup is statically corrected, with negative runtime controls owed before compiling. Keep lanes available without inventing new work or replaying consumed owners.

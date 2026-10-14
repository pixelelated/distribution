## Request

Owner, October 14, verbatim:

> As a future task, and I know we're still isolating the memory pressure causes. It might be good to explore if we could have the offline proxy temporarily stop running when the browser is opened, because this would relieve memory pressure just when the browser is open.
>
> There's no reason to have the offline proxy running necessarily when you're browsing, because no gameplay is occurring at that time. If that hurts the general functionality of the proxy, then we don't have to approach it. If starting and stopping the service, or if their background processes need to be available, etc., jeopardizes the efficacy of the proxy itself, we can reconsider the solution.
>
> It might be something to test or explore if it's a known way to help reduce memory pressure on certain devices, like the ones using the H700 processor, where we know that we're dealing with only a limited amount of RAM.

## Existing behavior and scope

Future feasibility experiment, not an added M7 release gate or a selected production change. Related #570/#576; preserve the current candidate order. This makes the previously discussed browser/proxy lifecycle alternative separately findable.

The source review in `docs/qa-logs/2026-10-13-browser-stack/proxy-lifecycle.md` found no browser dependency on RAOfflineProxy. The enabled service remains running, with connectivity/reconnect award flushing, cache workers and periodic work. Pending awards are persisted; graceful shutdown exists, but interruption safety and the packaged 15-second stop timeout need actual service testing. The unit has a 30-second listener readiness check. Emulator launch paths can route direct when the proxy is absent; they do not themselves start it. A stop without reliable restoration could therefore lose offline achievements for the next session. D-UI-095's treatment of in-flight award sending must be preserved; do not silently interrupt a send.

The measured 390 KiB lazy-import improvement is not the memory saving from stopping the complete service. No browser-owned stop/restart benefit or lifecycle safety has been measured. SIGSTOP alone would retain resident memory and is not the proposed memory-reclamation mechanism. Keep the player's enabled preference, routing, account data and cache intact; do not use the disable/configuration-revert operation.

## Experiment and acceptance criteria

Can this be done on the VM? Yes: constrained-memory guests, the actual packaged service and browser handoff, synthetic queued awards/cache work and a local fake upstream can test lifecycle, memory and recovery without real accounts. Any later H700 corroboration must separately name its physical RAM/renderer fact and follow device policy. No owner-device service action is requested by this issue.

- [ ] A dated source/upstream review identifies every background task and browser/frontend consumer, records existing upstream reports/fixes, and determines when a graceful stop is safe or should be skipped. Artifact: dependency and stop/restart contract with exact source identities.
- [ ] Reordered baseline/temporary-stop trials report actual process PSS, total available memory/pressure, browser responsiveness and return-to-game readiness latency. Artifact: original samples and timings with RAM, renderer, source and observation-window limits; no expected savings assumed.
- [ ] Actual-service synthetic tests preserve pending signed awards, deduplication/account separation, SQLite integrity, cached achievements and interrupted cache/preparation recovery. Restart/reconnect may flush only to the synthetic peer; originals show no lost or duplicate awards.
- [ ] Normal browser exit, cancellation, failed launch, crash, repeated openings, interrupted handoff and failed proxy restart restore the prior intended state or give an explicit recoverable outcome. Previously disabled/failed services are not spuriously enabled. Artifact: lifecycle journals, unchanged preference/routing manifests, owned-process cleanup and next-game readiness results.
- [ ] The decision records measured benefit versus latency/reliability cost: adopt with any justified low-memory scope, revise, or reject. If adopted, source/flow/reviewed frames where affected and clean/retained install evidence precede promotion; upstreamable pieces enter #585. Rejecting an unsafe or negligible optimization is a valid outcome.

This issue does not authorize live account uploads, stopping an owner's proxy, changing offline-achievement preferences, or an external audit transfer. Current M7 native-proxy correctness work remains required independently.

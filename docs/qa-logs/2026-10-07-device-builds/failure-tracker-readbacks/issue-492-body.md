## Maintainer request

> You have my approval to do the cleanup, and you have my approval to generate the H700 build. Following the H700 build, we should try the SM8550 build.

## Current state and order

Candidate 16 is qualified on GENERIC_X64: all eight audit findings resolved, 15 VM suites and 318 protocol checks pass. #491 completed the exact approved22-file cleanup and independently verified42.05GiB recovery. The first H700 arm run failed in spirv-tools:host at04:05:41UTC; #495 owns its compiler diagnosis/repair. The failed run and all interrupted package scopes are preserved before resumption. #494 prepares a further capacity proposal; its read-only scan projects432.62GiB gross with15.37MB of new unique custody bytes, but no further deletion is approved. Build H700 arm compatibility prerequisites, remeasure capacity and build H700 aarch64 firmware, then remeasure capacity and build SM8550. Keep each build in its own frozen build worktree using the standard watcher and active result consumption. No additional deletion, reserve change, release publication or physical-device operation is authorized by this issue.

Can this be done on the VM? Common software qualification is already complete there. Compilation, host capacity, artifact identity and archive inspection are build-host facts. Physical boot, panel and device smoke facts remain separately scoped in docs/releases/device-facts.md and do not gate compilation of the next requested target.

## Acceptance criteria

- [ ] Frozen input manifests show the qualified product-source comparison, distribution/ES pins, actual pinned container digest, source cache and concurrency for each target.
- [ ] H700 arm compatibility build has matching terminal result channels, unchanged input seals and verified builder exit; retain its output/stamp manifest.
- [ ] H700 aarch64 firmware build follows a measured capacity pass and has verified terminal results, raw/update identity and hashed DDR3/DDR4 artifacts.
- [ ] SM8550 compilation follows completed H700 artifact verification and a measured capacity pass; retain verified terminal results and hashed image/update artifacts.
- [ ] Artifact inspection records lowercase pixelelated identity, expected qualified source pins and source/licence inventory; release/publication and separately authorized hardware facts remain explicit in the milestone.

Failure logs remain retained. Source repairs discovered by these builds receive their own issues and appropriate requalification; a build failure is not waived. Watcher status alone is not off-session delivery (#395).

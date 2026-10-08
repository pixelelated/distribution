# Completed dependency build owner retirement

Only `/workspace/repos/rocknix.worktrees/m7-duckstation-deps01` was removed,
through `tools/fork-worktree remove <exact-owner> --force`, on 2026-10-08.
The helper exited 0 after checking 43,675 directories; no permission repair was
needed. The path is absent and no longer registered as a worktree.

`preflight.json` proves the exact source/branch, no live owner jobs, three
terminal successful watchers, six verified target artifacts, and the expected
owned build/source directories. `result.json` verifies nine protected accepted,
shared-cache/toolchain, and product inputs remain byte/mode identical; product
HEAD stays `052771f05d`. All original 469 host seal entries and two external
references still verify. That original seal is unchanged; this retirement packet
is separate from its historical file list.

Space values are observed filesystem counters, not an exclusive freed-byte
claim: copied toolchains share reflink blocks, and unrelated work can change free
space concurrently. Build/install/source receipts remain in the sealed parent
packet; the completed VM proof already received the qualified target library.

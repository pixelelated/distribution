# Step 0 triage of the open M7 bugs, 2026-11-25

Issue #555 (step 0 of the M7 release candidate), the futro's adjustment 1
(`docs/futros/2026-11-25-m7-rc-step0.md`). Each bug was read to its end before
any class move; the reason for each move is a comment on the bug itself
(D-QA-051, `bugs-are-agent-first.md`).

## The phone status controls, re-run on the candidate's bytes (#1113)

`phone-controls-0a3e979e50.log` is `tools/cloud-input-test PhoneStatus Phone
BrowserKeyboardClear` run on 2026-11-25 against the two files exported from
`0a3e979e50` with `git archive`:

- `projects/ROCKNIX/packages/network/rclone/sources/cloud_oauth`, sha256
  `71b82811845763949c8a0d5bdc5e92da93facad0e045599fea36965c5a785f85`. The
  October 26 guest proof (phone03, `docs/qa-logs/2026-10-26-cloud-followup/`,
  `source-bindings.json`) is bound to the same hash.
- `tools/cloud-input-test`, sha256
  `dc06f941924f463a4ea5b19a4c7b664d072210df7cad578a35681b569465a776`.

The run used `GIT_DIR` set to the primary checkout's `.git`, because the
negative controls read the old shipped source with `git show a1b0c65165:...`.
A first run without it errored on those two controls and is not the result.
The result is 16 tests in 0.548 s, OK, rc 0 (`phone-controls-0a3e979e50.rc`).
The shipped-source control
(`test_shipped_source_reproduces_success_overwritten_by_disconnect`) still
reaches the false disconnect on the old page. Every case passes on the
candidate's page.

## Carried record

`docs/qa-logs/2026-10-25-rgsp-signin-disconnect/` is #1113's sanitized
timeline from October 25. It was written then but never committed; it sat
untracked in the `m7-player-setup` worktree. It is carried here unchanged, and
its `SHA256SUMS` verifies.

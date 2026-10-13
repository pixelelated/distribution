# Verification boundary — 2026-10-13

Evidence level: **static source only**. No browser, broker, service, listener,
container, VM, compiler, test suite, account/provider request, device operation,
dependency install, image build, or package build was run. No shared record was
edited. The fixture is prepared source, not a passing test report.

The permitted checks ran with host Python 3.14.4 and Node v24.21.0. Python parsed
source/literal AST and inspected hashes; Node's `--check` parsed JavaScript without
executing it. No `cloud_oauth` import occurred. The full non-page Python AST was
compared with the recorded `next` source; the whole typing/pointer queue block
was compared byte for byte.

| Command / action | Actual result |
| --- | --- |
| `git show 0ea6eaf74ad47503c05955d1c0bd4bd00bdfb816:projects/ROCKNIX/packages/network/rclone/sources/cloud_oauth` | Exit 0; baseline SHA256 in source.json |
| Compare that source with worker-parent `HEAD:…/cloud_oauth` before edits | Equal bytes; no historical merge or refresh needed |
| `TMPDIR=/workspace/tmp/pix-m7-investigation-20261013/tmp python3 docs/qa-logs/2026-10-13-phone-status-source/static_check.py` | Exit 0; stdout retained as static-result.json |
| `node --check` for extracted EN and FR scripts | Both exit 0; empty stderr |
| `node --check` for fixture MOCK literal | Exit 0; empty stderr |
| `git diff --check` | Exit 0 |
| `sha256sum --check SHA256SUMS` from the packet directory | Exit 0; all listed bytes match |
| `browser_fixture.py` | **UNRUN**, no runtime lease |
| Existing C3/C4 suite, VM broker/native input, EN/FR frame review, screen reader | **UNRUN** |

No static command failed. The static source check was repeated after scoped source
edits; it did not execute the old host measurement or either old readiness fixture.
No frame exists in this packet. Dynamic browser outcomes, touch/keyboard focus
on actual phone browsers, and real lifecycle acceptance remain unproved.

The next executable runtime command and allocation prerequisites are in README.
The coordinator should retain the first fixture result, including failures, before
deciding whether another execution is warranted. The fixture writes `result.json`
on PASS or FAIL and keeps already-created screenshots; missing browser dependencies
are a failure, not permission to install them.

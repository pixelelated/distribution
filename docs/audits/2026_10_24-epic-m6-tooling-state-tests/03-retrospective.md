# Retrospective: M6.P2 T14, the last-good, settings and state tests (#661)

Phase 3: the slice's tests read against what they were written to prove, and against the tree that has moved since.

## 3.1 What the tests were for

- **The family is the qualification record of M7's issues:** #365 (the cloud epic), #421 and #526 (the writers), #508, #510, #520, #521 and #524 (the folder contracts), #531 and #532 (the gadget and identity), #565 (the state check), #337 and #383 (the identity).
- **Each was written to qualify one fix** and has a `docs/qa-logs/` folder from that day.
- **Five are called afterwards:**
  - T15's `last-good-scripts-test` calls four;
  - `vm-qa` calls one;
  - the fork CI calls one;
  - the release preparer calls two.
- **The rest were run once for their issue and not again.**

## 3.2 What drifted

- **Three tools hold a value the tree also holds,** and the tree moved:
  - `build-identity-test`'s stand-in against a gate added after it (`d9f428e1a0`);
  - `rasteratops-identity-check`'s licence string against `84ff94fb3d`;
  - the two rclone-pin tests against `a0f60255ab`.

  Each failure is a test asserting a past state of the tree as if it were a property.
- **One script got safer:** `cloud_content_restore` now refuses `..` before rclone, and its test (content-scope) did not follow.
- **The migration was retired (#508),** and the two guest tests that proved it now refuse every run.

## 3.3 What none of them noticed

The six at-hash failures sit in tools with no caller (F-11). The four called through T15, the one in `vm-qa` and the one in CI all pass at the hash, the one in CI only without `-O`. A test nobody runs ages silently, which is the brittleness this slice was ordered to measure.

## 3.4 What the record says about catches

Every tool with a qa-log folder has a recorded failure on purpose (an old source, a negative control), so all but two have a seen positive. What none records is a regression caught in a later candidate after its own issue closed, except:
- `retroarch-wrapper-test` (`e5d14d4220`);
- the cloud-layout test's partial-retry control (2026-10-06).

## 3.5 The seams

| Seam | What crosses it | What breaks at it |
| --- | --- | --- |
| the four callees × T15's `last-good-scripts-test` × `vm-qa`'s `scripts` | T15 passes `--busybox "${BB_HOST}"`, `--rclone "${SA_RCLONE_SRC}"`, `--archives-only` and its own `TMPDIR` | `image_tool_source` falls back to the host's binary unmarked (F-13), and the callees accept it. `vm-qa` runs T15 without a `TMPDIR` that would leak into the sandbox, so F-04 has not shown there. A caller that sets one gets a false FAIL |
| the real-rclone four × `cloud-test-backend` × the host's `rclone.conf` | none use `cloud-test-backend`: each has its own `alias` remote to a local `/cloud` inside `bwrap`, `HOME=/storage` | the host's home is never mounted, so a real `rclone.conf` cannot be read. The caller's environment does pass (F-04): `TMPDIR` breaks it today, and an `RCLONE_CONFIG` would reach it (inference) |
| the release preparer's two × `release-candidates.md`'s gates | `fork-publish-release --prepare` calls `rasteratops-candidate-store` and `pixelelated-state-check` | the state gate was added after `build-identity-test` (F-01): the gate's contract held, and the test that exercises the preparer broke. The contract is not this slice's to change; the test's stand-in is |
| the guest two × T12's harness | `vm-pair`, `cloud-test-backend`, `vm-visual-qa`; T12's `vm-walks/cloud-epic/migration-protocol.sh` is sourced by the epic | both refuse on this tree (F-10). The boundaries test stops its guests by a `/proc` scan, not `vm-stop` (F-09) |
| the writer tests × the busybox rule × a build root's presence | `--busybox` | no M6 root holds a busybox. The M7 root's (1.36.1, the effective pin) and the host's (1.37.0) both pass, and neither test can tell them apart (F-13) |

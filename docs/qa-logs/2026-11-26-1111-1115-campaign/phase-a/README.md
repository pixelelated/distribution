# Phase A: the host suites on the round's bytes

OS coordinator, 2026-11-26. The suites ran from the round's tree (`m7-rc-round-20261125`) with the image's own rclone, 1.76.0: the binary build 12 installed, `build.pixelelated-GENERIC_X64.x86_64/install_pkg/rclone-1.76.0/usr/bin/rclone`, sha256 `a0e5be1a…`. `BINDING.txt` records the head, the rclone and both validators' hashes. The host runs Python 3.14 and GNU tools, not the image's busybox; phase B runs the same scripts installed.

| Log | Suite | Source | Result |
| --- | --- | --- | --- |
| `A1-limits-original.log` | `tools/cloud-validator-limits-test --source <bcc866f1's cloud_folder_validate>` | `c6eb5c3e…`, the validator #1115 was filed against | **FAILED, as it should.** The merged result is reproduced: byte-limit, request-time-limit (twice) and total-time-limit each come back as `time-or-listing-limit`. The entry-limit, invalid-shape, cancellation and backend-error tests fail too. The 12 errors are tests of functions the fix added (`directory_access`). |
| `A2-limits-round.log` | the same suite, on the round's validator | `54ea660e…` | **22 of 22 OK.** |
| `A3-profiles.log` | `tools/cloud-connection-profiles-test` | the round | **25 of 25 OK.** |
| `A4-local-rclone.log` | `tools/pixelelated-cloud-validator-test` before #1479 | the round's tree at `a069abd236` | 24 PASS, then it stopped: the test seeded without the config_id the M7 tree requires. |
| `A4c-local-rclone.log` | the same, after #1479's fix (round `18169f5efe`) | the round | **32 of 32 PASS:** missing, empty, malformed, entry limit, byte limit, request timeout, accessible-but-limited BIOS, bucket empty prefix, partial failed listing, selected-only reads, explicit seeding with a wrong config_id refused, and the rest. |
| `A5-connections.log` | `tools/cloud-connections-test` | the round | **48 of 48 OK.** |
| `A6-layout-archives.log` | `tools/rasteratops-cloud-layout-test --archives-only` | the round | **13 of 13 PASS:** the ordinary settings-archive checks. |

**Not kept:** the suites' fixture trees, 71 MB of synthetic cloud and storage trees, which are reproducible from the commands. The logs carry every case's verdict.

**The layout test's migration matrix** is refused on the current source by design: #508 retired it, and the tool says to use `--ref` for historical source. Its six bare `--seed-folders` calls are all inside that matrix: `actor_case`, `settle_failure`, `failure_actor`, `marker_refusal`, `migration_retry` and `binding_rewrite`. They therefore run only against historical source, where the flag took no config_id (#1479).

**What this phase supports:**
- **#1115 C01:** the original reproduces the merged result, and the round's controls tell each failure apart without a false success. Authentication against permission stays generic where rclone does not say which (`test_backend_errors_not_guessed_as_auth`).
- **The source halves of #1111** C01, C04, C06, C16, C19, C22 and C25, and of #1115 C03. Their installed halves are phase B.

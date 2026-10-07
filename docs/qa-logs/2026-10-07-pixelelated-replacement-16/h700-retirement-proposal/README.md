# Proposed QA disk retirement for H700 arm

Status: awaiting separate approval. No deletion has occurred.

Retire only the 22 files below, recovering **42.05 GiB**. Their complete compact evidence, current candidate 16, qualified fallback 15, ROCKNIX baselines, source inputs and shared cache remain retained. The two referenced base disks are explicitly excluded.

| Capacity | GiB |
| --- | ---: |
| Available at the report | 149.25 |
| Proposed recovery | 42.05 |
| Available after recovery | 191.29 |
| First-stage budget, including 100 GiB operating allowance | 185.98 |
| Additional headroom beyond that budget | 5.31 |

The first stage builds H700 arm compatibility components. The aarch64 stage produces the firmware and needs a further capacity review; the current conservative combined forecast is 353.72 GiB. This proposal does not establish capacity for that later stage.

The fresh report inspected 3,722,420 directories and the same 311 disk chains as report01. All 24 inspected QA disk identities/hashes and protected-root identities are unchanged. It independently checked preserved evidence, actual processes and container mounts, and classified 64 tiny source samples against the pinned archive. There are zero unresolved dependencies. Both runs and all refusal controls are retained.

| Exact file (under `/workspace/tmp/`) | GiB |
| --- | ---: |
| `pixelelated-m7-boot-qualification-06/clean-640.qcow2` | 0.155 |
| `pixelelated-m7-boot-qualification-07/clean-640.qcow2` | 0.000 |
| `pixelelated-m7-p4-build16-partial-retry-1280x800-02/guest-d.qcow2` | 2.093 |
| `pixelelated-m7-p4-build16-partial-retry-640x480-01/guest-d.qcow2` | 2.091 |
| `pixelelated-m7-p4-build16-partial-retry-640x480-02/guest-d.qcow2` | 2.093 |
| `pixelelated-m7-p4-build16-recovery-1280x800-01/guest-d.qcow2` | 2.096 |
| `pixelelated-m7-p4-build16-recovery-640x480-01/guest-d.qcow2` | 2.096 |
| `pixelelated-m7-p4-build16-root-reasons-1280x800-01/guest-d.qcow2` | 2.095 |
| `pixelelated-m7-p4-build16-root-reasons-640x480-01/guest-d.qcow2` | 2.095 |
| `pixelelated-m7-p4-cloud-ui-fixes-02/guest-d.qcow2` | 2.091 |
| `pixelelated-m7-p4-cloud-ui-fixes-04/guest-d.qcow2` | 2.099 |
| `pixelelated-m7-p4-coverage-ui-03/guest-d.qcow2` | 2.090 |
| `pixelelated-m7-p4-coverage-ui-04/guest-d.qcow2` | 2.093 |
| `pixelelated-m7-p4-coverage-ui-05/guest-d.qcow2` | 2.091 |
| `pixelelated-m7-p4-fresh-root-06/guest-d.qcow2` | 2.091 |
| `pixelelated-m7-p4-fresh-root-07/guest-d.qcow2` | 2.090 |
| `pixelelated-m7-p4-library-fixes-01/guest-d.qcow2` | 2.106 |
| `pixelelated-m7-p4-library-fixes-02/guest-d.qcow2` | 2.108 |
| `pixelelated-m7-p4-presentation-fixes-01/guest-d.qcow2` | 2.095 |
| `pixelelated-m7-p4-recovery-ui-fixes-03/guest-d.qcow2` | 2.092 |
| `pixelelated-m7-p4-recovery-ui-fixes-05/guest-d.qcow2` | 2.092 |
| `pixelelated-m7-p4-recovery-ui-fixes-06/guest-d.qcow2` | 2.096 |

Excluded referenced files:
- `/workspace/tmp/pixelelated-m7-boot-qualification-06/clean-base.qcow2`
- `/workspace/tmp/pixelelated-m7-boot-qualification-07/clean-base.qcow2`

`proposal.json` binds each exact identity and SHA256. Execution must refresh the full read-only report, recheck every named file and preserved dependency, and verify actual recovery. The earlier two-disk approval (D-INFRA-019) is complete and does not cover these files. No worktree, source tree, candidate bundle, cache or filesystem reserve is changed.

Tracked separately as [#491](https://github.com/pixelelated/distribution/issues/491). `execute.py` defaults to verification only; that mode passed under the watcher with all four result channels zero, four seals and actual owner exits. The receipt is retained in `../retirement-verification-01/`. Mutation has not been invoked and requires its own explicit approval record and a fresh full-root report.

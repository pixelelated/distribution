# #589 baseline harness continuation — source only, unrun

The original owner02 remains failed. This additive packet corrects the host
harness and runs only its failed `scripts` row plus the two pending SFTP/S3
round-trip rows against the same fac608ff image. It does not alter the frozen
checkout, firmware, active owner, previous reports or accepted product controls.
Root owns allocation, execution, report review and admission consumption.
Tracking: https://github.com/pixelelated/distribution/issues/589.

The original seven failures are six `kill -0` liveness assertions and one stale
phone-page selector. Four named helper PIDs are confirmed zombies under the
outer subreaper by root's actual-host stat receipt, copied unchanged under
`evidence/`. The two unnamed cancellation helpers have the same assertion and
owner mechanism, but no PID-specific snapshot; that attribution remains a
source-supported inference until corrected execution. The original cancellation
exits, unlocked locks, removed running markers and disable exits are retained.
`failure-map.json` binds every original FAIL line to its assertion.

This is not a recurrence of the seven #550/#551 failures. Their accepted tool
SHA256 ebd9a4669d8e96d6a18a874f95058911ed2a7b38329a5236891ef3bdd6894d20
equals the current frozen tool. Those failures were six quota-full host
compiler/patch operations and a retired AUTOSTARTED extraction. The accepted
1378-check run used source1a026648442321609b2288c2c9c06803817f9df2 and a plain
subprocess wrapper. This owner adds subreaper custody; it only reaped adopted
children on exception/final cleanup, leaving zombies visible to `kill -0`
during the suite. Existing TMPDIR and readiness fixes remain unchanged.

The #571 product commit0d69fca540c7a75833e26054463145635c121b00 moved prose
from `#state` into `#status-message`. The current template and phoneStatus()
write that detail correctly. PL-016 still reads the icon button, whose independent
stub textContent remains empty. Its correction selects `status-message` when
present and falls back to `state` for historical `--old` templates. The existing
nonempty/no-fictitious-send-button assertion and full input-queue cases remain.
The open→waiting sequence now correctly reads the closed-page explanation.

`run.py` drains only exited direct/adopted children during the existing quarter
second observation loop using PID-specific waitpid(WNOHANG). The current Popen
PID is excluded, leaving its poll/wait and original stage status untouched.
No waitpid(-1), signal, blocking wait or forced cleanup runs in observation.
Every collected status is retained raw, with PID/PPID/start ticks and decoded
returncode, both immediately in `records/adopted-exits.jsonl` and in the final
result. The existing identity-checked final cleanup remains separate. A running
QEMU/backend returns zero from WNOHANG and remains owned by its ordinary helper.

There is no existing subgroup option for these six subprocess cases or PL-016:
the harness only has `--old` and unrelated `--cloud-layout`. Therefore the
smallest existing executable scope is unchanged `vm-qa --only scripts`, then
unchanged `vm-qa --only round-trip --backend sftp` and `s3`, serialized under one
new owner. The other fourteen same-image standard rows are retained. Preparation
refuses until owner02 has completed with exactly scripts FAIL and all fourteen
other rows PASS, no backend rounds already run, and completed cleanup. If the
actual final remainder differs, root must review it rather than use this packet.

The private harness has an unchanged copy of vm-qa and the three-line selector
correction to last-good-scripts-test. Its eight supporting helper links resolve
to unchanged frozen tools and are bound along with target hashes. The existing
LAST_GOOD_SOURCE_ROOT selects the frozen product checkout. SFTP/S3 call vm-qa
at the original frozen path. No fake guest module or product overlay is used.
The remaining original prepare/close machinery, image/source/ES/binary checks,
two4CPU/8GiB default guests, local-only endpoints and result channels remain.

Bounds are unchanged ceilings:5700s work+180s cleanup, pair-up900s,
scripts3600s, SFTP300s, S3300s, each backend-up120s/backend-down25s,
pair-down70s;512MiB records/4096files/16MiB stage streams. Disk admission retains
the actual raw image,32GiB guest disks and8GiB host/backend scratch allowance.
No host/kernel quota beyond those existing controls is claimed. This source
preparation launched no fixture, compiler, VM, service, container or provider.

After owner02 completes, its original rows are reviewed/exported and its
admission consumed, use these exact inputs in the actual host PID namespace:

```bash
TASK_SOURCE=/tmp/pix-m7-baseline-harness-correction-20261014
TASK_TREE=/workspace/repos/rocknix.worktrees/m7-p5-build-20261014-02
TASK_VERIFY=/workspace/tmp/pix-m7-image-readback-20261014-02/artifacts
TASK_PRIOR=/workspace/tmp/pix-m7-final-baseline-20261014-02
TASK_OWNER=/workspace/tmp/pix-m7-final-baseline-20261014-03
TASK_BUILD="$TASK_TREE/build.pixelelated-GENERIC_X64.x86_64"

python3 -I -B "$TASK_SOURCE/prepare.py" \
  --checkout "$TASK_TREE" --verification "$TASK_VERIFY/result.json" \
  --system-root "$TASK_BUILD/image/system" \
  --es-source /home/max/Development/emulationstation-next.worktrees/qa-integration \
  --retroarch-source "$TASK_BUILD/build/retroarch-bdba046fa6766380bc2457532f38e589df769aaf" \
  --baseline /workspace/artifacts/rocknix-images/walk-baseline \
  --prior-owner "$TASK_PRIOR" --owner "$TASK_OWNER"
cd "$TASK_TREE"
tools/host-maintenance/retention-report --plan "$TASK_OWNER/retention-plan.json" \
  --output "$TASK_OWNER/retention-report.json"
tools/host-maintenance/build-admission prepare --plan "$TASK_OWNER/admission-plan.json" \
  --output "$TASK_OWNER/admission.json"
tools/watch-build-submit --owner "$TASK_OWNER/lifecycle-owner" -- \
  --admission "$TASK_OWNER/admission.json" --activity-dir "$TASK_OWNER" --recursive-activity -- \
  python3 -I -B "$TASK_OWNER/run.py"
```

Root supervises every original stage, adopted exit receipt and resource sample.
After actual completion, export with unchanged command shape:

```bash
TASK_RUN=$(cat "$TASK_OWNER/run.path")
TASK_EXPORT=/workspace/tmp/pix-m7-final-baseline-export-20261014-03
python3 -I -B "$TASK_OWNER/close.py" --owner "$TASK_OWNER" \
  --run "$TASK_RUN" --output "$TASK_EXPORT"
# After original evidence/cleanup review, root consumes explicitly:
tools/host-maintenance/build-admission consume --run "$TASK_RUN" \
  --evidence "$TASK_EXPORT/consumption-draft.json"
```

The exporter requires exactly scripts/round-trip/round-trip, all PASS, and
original zero channels before proposing qualification. The original15-row
report is never rewritten. AST parsing, shell syntax checks, immutable-source
comparisons and diff review are source checks only; corrected behavior remains
unrun. Raw unified diffs and original source bytes are retained verbatim; archive
them if carrying into Git where context whitespace otherwise trips show --check.

# Engineering build launch — reviewed revision03

SOURCE ONLY; these commands have not run. Execute from the host PID namespace
after root has consumed all current VM owners, published the final distribution
source with reviewed ES3178, and verified `origin/next` is that published source.
The existing build checkout and consumed independent cache are reused. Do not
recreate either. If the unused build owner is no longer empty, allocate a fresh
owner rather than remove or overwrite its files.

```bash
set -eu
TASK_PACKET=/workspace/repos/rocknix.worktrees/m7-player-setup/docs/qa-logs/2026-10-14-m7-engineering-image-plan-revision03
TASK_TREE=/workspace/repos/rocknix.worktrees/m7-p5-build-20261014-01
TASK_BUILD=/workspace/tmp/pix-m7-engineering-build-20261014-01
TASK_CACHE=/workspace/tmp/pix-m7-engineering-cache-20261014-01
TASK_MEASUREMENT=/workspace/tmp/pix-m7-capacity-20261014-01/measurement.json
TASK_ES=3178b832b8d134198b2b4eede4f725d4ed283f8c
test -z "$(git -C "$TASK_TREE" status --porcelain)"
test -z "$(ls -A "$TASK_BUILD")"
test "$(sha256sum "$TASK_PACKET/SHA256SUMS" | cut -d ' ' -f 1)" = 8e6d2280464e6c41b2662609d2c6eecbef7971142c4dac8bb7a4c6981b0c4a80
(cd "$TASK_PACKET" && sha256sum -c SHA256SUMS)
TASK_COMMIT=$(git -C "$TASK_TREE" rev-parse origin/next)
git -C "$TASK_TREE" merge --ff-only "$TASK_COMMIT"
cd "$TASK_TREE"
test "$(git rev-parse HEAD)" = "$TASK_COMMIT"
test -z "$(git status --porcelain)"
tools/build-preflight
TASK_STAMP=$(date -u +%Y%m%dT%H%M%SZ)
python3 -I "$TASK_PACKET/prepare-owner.py" --checkout "$TASK_TREE" --commit "$TASK_COMMIT" --expected-es "$TASK_ES" --owner "$TASK_BUILD" --cache-ready "$TASK_CACHE/cache-ready.json" --timestamp "$TASK_STAMP"
```

Review the resulting `build-inputs.json` before the final submission below:
exact final source/ES recipe, cache-ready digest, revision03 helper hashes,
old logical container prefix, cold4CPU/24GiB and image full-affinity/40GiB,
no container swap, six-hour family, host8GiB and volume64GiB floors.

```bash
python3 -I "$TASK_PACKET/prepare-plan.py" --checkout "$TASK_TREE" --commit "$TASK_COMMIT" --expected-es "$TASK_ES" --measurement "$TASK_MEASUREMENT" --owner "$TASK_BUILD" --stage build
tools/watch-build --record-only -- python3 -I tools/host-maintenance/retention-report --plan "$TASK_BUILD/retention-plan.json" --output "$TASK_BUILD/retention-report.json"
python3 -I tools/host-maintenance/build-admission prepare --plan "$TASK_BUILD/admission-plan.json" --output "$TASK_BUILD/admission.json"
tools/watch-build-submit --owner "$TASK_BUILD" -- --admission "$TASK_BUILD/admission.json" -- python3 -I "$TASK_BUILD/build-owner.py"
```

Admission/report expire after15minutes and registry changes require fresh
preparation. Measurement is the original18:55:50UTC bounded measurement and is
accepted only within its24-hour age bound with unchanged measured roots.
Cache run `.build-runs/20261014T191656Z-0cac274a/admission-consumed.json`
records consumed19:30:27UTC and original command/monitor/runner0. Cache-ready
records checksum equality and2,533,024 independent regular files.

Root actively supervises the first clean stage before allowing its automatic
sequence to proceed. Read owner `console.log`, `run.path`, `owner-result.json`,
`resource-result.json`, stage original host/inner exits, and original
runner/monitor/launcher results. Submission is not completion. Actual process
and owned-container exit plus genuine result consumption remain required.
Engineering output identity, x86_64 loader/UI and clean/retained image QA follow;
execution PASS does not qualify the image or designate an RC.

Revision03 changes only Docker absence diagnostic matching to casefold; original
lowercase stderr is retained. All15 sealed members verified, Python AST3.10
parsed. No further deterministic lifecycle blocker found in this focused review.

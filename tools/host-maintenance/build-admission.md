# Build admission and retained output ownership (#493)

Native, Docker and ad-hoc compilation requires a fresh, single-use admission.
`watch-build` checks it after the watcher arms and before starting the payload.
Normal native device targets have one outer run covering all their ABI phases;
Docker enters once on the host. Nested entrypoints reuse the admission and check
source and profile. A non-compiling job uses `--record-only`; it cannot be a native
or Docker build entrypoint, and a nested build cannot inherit it as an admission.
This is an operational guard, not a security boundary against someone deliberately
labelling a compiler command as a recording job or bypassing the build tools.

## Prepare from the existing report

Use `retention-report` to create a current report from a measured stage budget,
protected inputs and the explicit reviewed scan scope. Unknown historical trees
still need their separate classification; the admission tool does not crawl or
delete the volume. Use the recording mode for this read-only report job:

```sh
tools/watch-build --record-only -- python3 -I tools/host-maintenance/retention-report \
  --plan /absolute/owner/retention-plan.json --output /absolute/owner/retention-report.json
```

Create an admission plan (private, outside tracked source):

```json
{
  "checkout": "/absolute/frozen-checkout",
  "retention_plan": "/absolute/owner/retention-plan.json",
  "retention_report": "/absolute/owner/retention-report.json",
  "stage": "the exact measured stage name",
  "profiles": [
    {"PROJECT": "ROCKNIX", "DEVICE": "H700", "ARCH": "arm"},
    {"PROJECT": "ROCKNIX", "DEVICE": "H700", "ARCH": "aarch64"}
  ],
  "outputs": [
    {"path": "/absolute/frozen-checkout/build.pixelelated-H700.aarch64",
     "issue": 555, "kind": "build-cache",
     "release_when": "the immediately queued H700 qualification and required source custody are accepted"}
  ]
}
```

Enumerate **all** output roots and profiles in the real plan; the example only
illustrates the schema, not a sufficient H700 budget. Supported output kinds are
`build-cache`, `firmware`, and `qa-scratch`. Parent directories must exist on the
measured filesystem. An existing output directory is allowed; protected input
identity checks still apply. A redirected native `BUILD_DIR` must be a declared
output root. Docker's `BUILD_DIR` names the container checkout; set
`container_checkout` in the plan when it differs from the host path. The Docker
mount contract must map the admitted host checkout there, as usual.

```sh
python3 -I tools/host-maintenance/build-admission prepare \
  --plan /absolute/owner/admission-plan.json --output /absolute/owner/admission.json
export PIXELELATED_BUILD_ADMISSION=/absolute/owner/admission.json
make H700
```

For an ad-hoc compile or cache copy, use
`tools/watch-build --admission /absolute/owner/admission.json -- COMMAND`.
For durable submission, pass those runner arguments after
`tools/watch-build-submit --owner FRESH_OWNER --`. A fresh submission owner is
always required. Do not label a compiler or cache copy `--record-only`.

Both the report and admission expire after15minutes. The guard binds the report
and its producing tool, plan, measurement evidence, protected identities, tracked
source state, checkout, profiles, filesystem and current shared registry generation.
It rechecks `f_bavail` at launch, excluding filesystem reserve, and subtracts
unconsumed reservations on the same filesystem. No planned reclamation is counted
as free space. A changed plan/source/input, unresolved inventory error, refused
budget, changed registry or used admission requires fresh preparation. A report
being written successfully does not make its budget acceptable.

The registry is shared by Git worktrees in the common Git directory under
`pixelelated-build-admission/`, with a file lock. Reservations are conservative
future byte allowances; existing allocated files are already reflected in available
space. Ordinary host processes outside these tools are not space-reserved. Existing
memory/swap preflight and ongoing pressure monitoring remain required.

## Consume completion; retain outputs honestly

Each admitted `.build-runs/<id>` retains admission/plan/report snapshots, original
command/watcher/runner results and output ownership. A submitted run additionally
requires the launcher's original result and wrapper rc. The reservation persists
until evidence consumption succeeds; a completed compile is not qualification.

An acceptance JSON names the exact `run`, `expected_rc`, `disposition` (`qualified`
or `failed-investigated`), unchanged `outputs` from `admission.json`, and an
`evidence` list of absolute paths and SHA256s covering the actual qualification
or failure diagnosis. Then run from the **original host PID namespace**:

```sh
python3 -I tools/host-maintenance/build-admission consume \
  --run /absolute/frozen-checkout/.build-runs/ID --evidence /absolute/owner/acceptance.json
```

The consumer checks original results, terminal watcher state, retained evidence,
recorded process exits and surviving command-group members. A lost watcher or
unknown/active process keeps the reservation. Repeating the same accepted evidence
is idempotent; different evidence for a consumed run is refused. An interactive
Docker-shell run must be consumed in its original container namespace before that
container is removed; ordinary host-wrapped Docker builds are preferred. A
container namespace that has disappeared is not proof of individual host exits.

**Consumption releases the reservation, not the outputs.** Output holds and release
conditions remain recorded; this tool performs no deletion. #493's automatic
qualified-artifact retirement, interrupted-removal reconciliation, complete
historical classification and next-build resource telemetry remain separate open
criteria. No root dependency visibility or automatic cleanup is claimed here.

Run the synthetic controls with `test-build-admission` and `test-build-monitor` in
this directory. They invoke actual launch wrappers and Makefile routes with small
payloads, synthetic capacity/report inputs, and no compiler, VM or real container.
The earlier historical routing fixture stays unchanged in its QA evidence folder.

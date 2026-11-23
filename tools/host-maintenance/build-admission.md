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

Consumption always settles the reservation independently of retirement.
Existing plans keep their original output holds. Successful plans that opted
into the narrow generated-file scope below also attempt retirement during the
same `consume` call. The original consumed receipt stays immutable.

With [the ordinary-account retirement cycle](build-retention-cycle.md)
installed, the consumption CLI also triggers the shared generated-tree sweep
after the authoritative result and reservation are settled. The periodic
checkout sweep reconciles missed triggers and interrupted work. Both use the
canonical engine's ownership, independent custody and current-use guards.

### Automatic retirement of declared generated headers

The first scope is one to four exact `cmake_pch.hxx.gch` files in
`CMakeFiles` below a declared, private `build.*/build/` output under that
checkout. Use only same-volume, ordinary-account, singly linked regular
files. Keep source, licences, staging, caches, archives, media, directories
and all other generated files under their existing holds. Directory permissions
stay intact. Set up private writable directories at creation. A shared,
unreadable or non-writable parent holds the file.

In the admission plan, before `prepare`, add:

```json
{
  "inputs": ["/absolute/protected/input"],
  "retire_on_consume": {
    "files": ["/checkout/build.example/build/p/CMakeFiles/p.dir/cmake_pch.hxx.gch"],
    "reference_roots": ["/absolute/managed/compact-reference-root"],
    "reference_stores": ["/absolute/managed/compact-reference-root"]
  }
}
```

Use `inputs` to register other exact files or directories the job will use.
Each prepared receipt places a 15-minute dependency hold under the normal
shared registry lock. An admitted job takes over its queued hold. Expired
prepared holds cannot start a job. Retirement also checks other active and consumed owners. Consumption
records the actual qualification evidence paths. The checks protect earlier
input scopes and retained evidence after a peer's output hold ends. The
current qualification file and every file in its `evidence` list stay held,
including otherwise eligible generated outputs. Legacy peer rows with
unverified scopes or retained operands hold automatic retirement.

Retirement binds the invoking account's passwd and effective home state
locations and any absolute `XDG_STATE_HOME` to the admitted request. It
checks the deployed filesystem-keyed registry location in those state
roots, using the selected volume's device and filesystem ID. An existing
registry for the volume, a changed route, an unresolved or unreadable route,
or missing route bindings holds all selected files. These checks run under
the Git-common lock before observation and again at unlink. A detected
alternate registry is a hold even when its queue looks empty, since its
writers use a different lock. The reader does not acquire, repair or write
that registry. Mixed registries need a common ownership and locking contract
before automatic retirement can be admitted. Executors with unrepresented
routing remain outside this scope. The declared roots and stores still need
to cover all known incoming references. Whole-host use and local
stopped-container checks are additional to registered ownership.

Add `retirement` to the normal successful qualification evidence:

```text
{
  "manifest_sha256": "<approved host-use enrollment SHA-256>",
  "source_custody": {"path": "<retained source receipt>", "sha256": "<digest>"},
  "superseded_by": {"path": "<retained successor receipt>", "sha256": "<digest>"},
  "files": [{
    "selection": {"path": "<exact declared header>", "identity": {...}, "aliases": []},
    "ninja_graph": {"path": "<actual enclosing build.ninja>", "sha256": "<digest>"}
  }]
}
```

Use the exact identity and alias fields from the fixed host-use manifest.
Enroll **one singleton batch per file** under one manifest digest so a prior
removal cannot make the remaining singleton reports incomplete. Bind the
enrollment through the established [host-use protocol](host-in-use-report.md).
New operands require the existing explicit enrollment. No installation or
access-policy change is part of consumption.

The source receipt has `result: "PASS"`, `source` equal to the admitted
tracked source identity, and an `evidence` list for retained source and
licence custody. The successor receipt has `result: "PASS"`, `admission_id`,
the exact declared `files`, `reference_roots`, `reference_stores`, and an
`evidence` list for the accepted independent supersession and dependency
scope. The evidence lists use the normal path/SHA-256 format. Include both
receipts, every referenced evidence file and each actual Ninja graph in the
top-level qualification `evidence` list. The checker matches each claimed
header to an actual CMake C++ compiler output edge in the bound graph.
The acceptance owner verifies the correspondence of sources, original
results and the independent replacement when forming those receipts.

Run the same normal `consume` command shown above. A zero result settles the
original reservation. An added JSON summary and `<run>/retirement.json`
show `retired`, `held` or `partial`. The private journal records per-file
holds and the original trusted use observations. It records allocated bytes
of verified final-link removals separately from the observed filesystem
available-byte delta, which can include unrelated filesystem activity. An
interrupted intent whose path is later absent is unconfirmed and contributes
zero credited bytes. The capacity guard still uses fresh measured free space.

Use the same `consume` and exact acceptance for retry. It resumes untouched
or still-identical files after renewed checks and never deletes a replacement
at an already settled name. It performs no build replay. A verified durable
unlink is credited once; the immutable original consumed receipt still
records the original reservation transition. The path and dependency
checks are serialized with cooperating admissions. The trusted host-use
check remains a short-lived snapshot. Keep the selected scope quiescent and
exclude independent writers or unmanaged consumers. The tool holds on
unreadable dependencies, unknown media, failed originals, private owner
mismatches or a missing/stale/incomplete host check.

Run `python3 -I -B tools/host-maintenance/test-generated-retirement` for the
ordinary-account controls. They run a disposable normal watcher, perform
actual unlinks, test interrupted accounting and provide bounded fabricated
host-use observations to the real consumer validator. They do not use the
host's installed helper or Docker daemon. These filesystem controls can run
in a VM. Host-use and filesystem capacity evidence must come from the
actual target host and volume.

Run the synthetic controls with `test-build-admission` and `test-build-monitor` in
this directory. They invoke actual launch wrappers and Makefile routes with small
payloads, synthetic capacity/report inputs, and no compiler, VM or real container.
The earlier historical routing fixture stays unchanged in its QA evidence folder.

## Recover the reviewed launcher receipt collision (#597)

`consume-reporting-failure` is a separate, deliberately narrow custody operation.
Ordinary `consume` is unchanged. It supports the reviewed four-stage engineering
producer (`clean-dolphin-sa`, `build-dolphin-sa`, `build-emulationstation`, `image`)
and exact launcher SHA256
`3777c68fb2677775550183f8bacdb860d7e1e477ebac4e923beda63beba8e88e` only.
It is not an ignore-missing-results option. A different producer or launcher
requires its own reviewed recovery; neither a successful submission nor an
operator-created zero establishes the original launcher's wait status.

For this collision, preserve the copied launcher, complete console, conflicting
`tool-wrapper.rc` bytes and identity, and all original producer receipts. Do not
write `launcher-result.json` or replace the conflicting file. The terminal console
must contain the exact exclusive-create Errno17 diagnostic for that owner's
wrapper receipt. The final launcher wait status stays unknown; a source-derived
exit2 may be documented separately but is never stored as an original result.

Create a separate immutable failure JSON with these fields:

```json
{
  "schema": 1,
  "reason": "exclusive-wrapper-receipt-collision",
  "run": "/absolute/frozen-checkout/.build-runs/ID",
  "admission_id": "the original admission id",
  "owner": "/absolute/submission-owner",
  "source": {"head": "original full commit", "tracked_diff_sha256": "original hash"},
  "pid_namespace": 123456789,
  "original_launcher_returncode": null,
  "qualification": false,
  "coordinator_provenance": {
    "action": "premature-wrapper-receipt-write",
    "receipt_path": "/absolute/submission-owner/tool-wrapper.rc",
    "receipt_is_launcher_result": false,
    "acknowledgment": "Explicit account of the operator's premature write."
  },
  "collision_identity": {"device": 0, "inode": 0, "size": 2, "mtime_ns": 0,
    "allocated_bytes": 4096, "uid": 1000, "links": 1, "mode": 33152},
  "originals": [{"path": "/absolute/original/file", "sha256": "actual SHA256"}]
}
```

The identity object uses `path_identity`'s complete actual values, including
device, inode, mode and nanosecond mtime. The numbers above are illustrative.
Required original hashes cover:

- Run: `admission.json`, `runner-result.json`, `build.rc`, `build.status`,
  `build.pid`, `command.pid`, `watcher.pid`, `build.status.pid`.
- Owner: `watch-build-submit.py`, `console.log`, `launcher-start.json`,
  `launcher-pid.json`, `launcher-submission.json`, `tool-wrapper.rc`,
  `owner-start.json`, `owner-result.json`, `resource-result.json`, `inner.rc`,
  `build-inputs.json`. The three producer helper files are additionally checked
  against the original `build-inputs.json` helper hashes.
- Each of the four stage directories: `host-result.json`, `inner-result.json`,
  `inner-ready.json`, `host-observed.json`, `container-observed.json`,
  `host-command.json`, `container.cid`.

Additional original submission and diagnosis evidence may be retained in the
same list. Missing or changed originals, symlinked paths, a changed source,
nonterminal watcher, nonzero/noninteger result, inconsistent nonce/container
identity or unresolved resource/cleanup result refuse consumption. The new
acceptance file uses the existing schema with `expected_rc: 0`, unchanged
outputs, and `disposition: "failed-investigated"`; its evidence list must bind
the failure JSON by absolute path and SHA256. This preserves runner0 separately
from the reporting failure.

```sh
python3 -I tools/host-maintenance/build-admission consume-reporting-failure \
  --run /absolute/frozen-checkout/.build-runs/ID \
  --evidence /absolute/recovery-owner/acceptance.json \
  --launcher-failure-evidence /absolute/recovery-owner/launcher-failure-evidence.json
```

Run from the original host PID namespace, after the whole producer has ended.
Under the existing registry lock, recovery rehashes the originals and requires
all named PIDs, direct children, process groups and sessions to be absent. It
conservatively refuses even reused PIDs or zombies. A successful bounded Docker
container-ID census must exclude all four exact original CIDs. Unreadable process
state, daemon errors or diagnostic output do not mean absence. This checks the
recorded process/container custody; it makes no whole-host root-FD visibility
claim and does not stop any process/container or delete any output.

The consumed record retains the unchanged original runner result and records
`completion_disposition: "failed-investigated/reporting-failure"`,
`qualification: false`, `original_launcher_returncode: null`, the failure
evidence path/hash and known launcher source hash. `recovery_tool_path` and
`recovery_tool_sha256` identify the actual reviewed recovery implementation;
`recovery_absence` records the namespace and exact PID/group/CID sets checked.
Outputs remain held with zero deleted bytes. Identical evidence through the same
tool is idempotent; altered evidence or recovery semantics refuses. A later
artifact verifier must explicitly accept this nonqualified reporting-failure
record while preserving every independent product/artifact check. Recovery
alone is not firmware qualification, an RC gate or a reason to relabel the
original submission successful.

The added `test-build-admission` controls use temporary fake originals/registry,
mocked process and container observations, and the real recovery logic. They
never consume a production reservation or contact Docker. Existing ordinary
admission/lifecycle controls remain in the same suite.

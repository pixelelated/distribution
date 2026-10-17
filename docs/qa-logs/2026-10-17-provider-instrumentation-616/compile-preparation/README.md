# #616 fresh diagnostic-helper compile owner preparation

This packet is source preparation only. Its preparer has **not been executed**
by the source agent. No compiler, Docker container, listener, VM, device, or
service was launched. The coordinator reviews, materializes, admits, and runs it.
Existing owners and the original instrumentation packet are unchanged.

Preparer: `prepare.py`, SHA256
`cf814946aeb3c6b4aee7f588558236b387275d461e7c8e225ff4e82f3eed1ecc`.
Keep companion `compile-owner.py.in` beside it; SHA256
`69b23f4ea552d5666d7bc0b28cdaaa0e549ef18af5090e481616e3ef6d50cba0`.
Both source files are frozen at handoff.

The materialized owner is exclusively
`/workspace/tmp/pix-provider616-compile-20261017-01`.
An existing owner is refused. It does not alter the previous compile owner,
accepted build caches, pinned checkout, candidate C, or source packet.

The candidate is the immutable instrumentation source:
`/tmp/pix-provider616-instrumentation-20261017/prepared/cloud-signin-window.c`,
SHA256 `63b8cf5725652874f361aa5fe04abe2b5f326b1cb9ae113590d5c422f9e16b6d`.
The preparer verifies it, the original 12-case parser fixture, and reused
host/cgroup helpers before writing the new owner. It checks the exact clean
tracked state of frozen `077197e6cd3ea31f33b28aaf3882a694b3423b53`.

## Limits and evidence

* One container, sequential GENERIC_X64 and H700 helper compiles, pinned existing
  build-image digest; `--pull=never`, no network, read-only root filesystem.
* CPU4 only, one CPU quota, 1 GiB cgroup memory, **zero cgroup swap**, 128 PIDs.
  This allocation is separate from GTK4/WebKit6 CPU0–3 and 20 GiB.
* Original accepted toolchains are mounted read-only at the same canonical
  paths as the previous successful helper compile. No build tree/toolchain copy.
* Only new owner outputs and stage receipts are writable in the container;
  source inputs are read-only. Temporary compiler files use a 128 MiB tmpfs.
* A 180-second producer deadline includes setup/observation/compilation/parser
  cases. Expiry stops the specifically identified owned container and reaps its
  Docker CLI process group. Bounded cleanup and observer joining occur afterward;
  the deadline is not a promise that all cleanup finishes exactly at second180.
* A conservative 192 MiB admission covers 128 MiB temporary allowance and 64 MiB
  outputs/records. Compiler log guard is 2 MiB. Host sampling only scans this
  small new owner, never accepted caches or the concurrent GTK4 build tree.
* Reused `host-resources.py` samples host RAM/swap, OOM counts, memory/I/O pressure,
  workspace space, and allocated owner bytes. Floors: 8 GiB host available RAM,
  100 GiB workspace available, and the existing >=20% swap-free rule. The
  sampler's original result records thread termination and observed peaks.
* Reused `inner-build.py` validates actual one-CPU visibility and cgroup
  memory/swap limits before compilation. It waits for the host's nonce-matched
  inspection of the exact container, mounts, CPU4 affinity, memory, user, and
  network contract. It records cgroup before/periodic/after samples and actual
  `memory.peak`, pressure/I/O stats, and OOM deltas.

Original channels remain distinct: shell/compiler status in
`stages/compile/inner-result.json`; inner-wrapper status there; original Docker
CLI wait status in `stages/compile/host-result.json` and `result.json`; host
observer in `resource-result.json`; canonical watch-build `build.rc` and
`runner-result.json`; durable launcher `submit/tool-wrapper.rc` and
`submit/launcher-result.json`. Submission exit0 is not completion. No source
agent writes these receipts or supplies an acceptance result.

The target x86 loader/library path runs **14 pre-GTK parser cases**: the original
12 unchanged cases plus `CLOUD_SIGNIN_DEBUG=''` and `CLOUD_SIGNIN_DEBUG='1'`, both
expected to exit78. Display variables are absent, and valid cases must not emit
periodic samples or proof-layer records. This tests actual parser dispatch after
compilation; it does not initialize GTK, launch a WebView, contact a provider, or
prove normal broker/phone handoff. No environment values or credentials are
printed. The container receives only fixed TMPDIR/locale and the existing
watch-build run marker, never arbitrary host variables.

## Coordinator preparation, admission, and launch

Run each command from the frozen checkout; do not set internal watch-build run
markers manually. Report/admission are fresh and expire after15minutes.

```sh
cd /workspace/repos/rocknix.worktrees/m7-p5-build-20261015-03
python3 -I -B /tmp/pix-provider616-compile-source-20261017/prepare.py

tools/watch-build --record-only -- python3 -I tools/host-maintenance/retention-report \
  --plan /workspace/tmp/pix-provider616-compile-20261017-01/retention-plan.json \
  --output /workspace/tmp/pix-provider616-compile-20261017-01/retention-report.json

python3 -I tools/host-maintenance/build-admission prepare \
  --plan /workspace/tmp/pix-provider616-compile-20261017-01/admission-plan.json \
  --output /workspace/tmp/pix-provider616-compile-20261017-01/admission.json

tools/watch-build-submit \
  --owner /workspace/tmp/pix-provider616-compile-20261017-01/submit -- \
  --admission /workspace/tmp/pix-provider616-compile-20261017-01/admission.json \
  --activity-dir /workspace/tmp/pix-provider616-compile-20261017-01 \
  --recursive-activity --interval 2 --stall-min 2 -- \
  python3 -I -B /workspace/tmp/pix-provider616-compile-20261017-01/compile.py
```

Supervise the owner until the original channels complete. Inspect resource,
cleanup, ELF, exact binary hashes, and fourteen actual parser results. Use the
original `run.path` and unchanged admission outputs to prepare qualified or
failed-investigated evidence, then the existing build-admission consumer from
the original host PID namespace. Do not rerun a successful compile merely to
replace reporting artifacts. The resulting binaries remain diagnostic inputs
requiring separately admitted VM qualification; there is no device launch here.

## Source checks performed

The two new Python sources parse. Pure construction of the extended test source
preserves the original12 case ASTs exactly and appends both expected78 cases.
The generated shell passes `bash -n`; no shell payload ran. These are recorded
in `source-checks.json`. Preparer materialization, Docker inspection, admission,
compilation, actual parser executions, and resource sampling remain unrun by
this source agent. Source checks are not runtime acceptance evidence.

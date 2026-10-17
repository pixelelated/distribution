# GTK4 input compile owner — source only

This packet prepares one diagnostic compile of the immutable
`/tmp/pix-gtk4-postbuild-20261017/compile-input.py --execute` payload. No Docker,
compiler, target code, VM or provider was launched by this lane. No source,
options, toolchain, cache or original postbuild packet was edited.

The coordinator supplied `/tmp/pix-gtk4-compile-only-qualification-20261017.json`:
94 ELF records,378 resolved dependency edges and11 matching normalized critical
package/sysroot pairs. The strict closure checker remains FAIL for six search
paths inherited from the accepted runtime image. qualification.py verifies the
exact inventory/evidence hashes, counts, matching pairs, resolved edges and
unchanged findings; it requires explicit `allowed_compile_only:true` and
`runtime_authorized:false`. It does not relabel this as runtime qualification.

The fresh owner is `/workspace/tmp/pix-gtk4-input-compile-20261017-01`. An existing
owner is refused. Preparer checks actual host PID namespace, non-root ownership,
CPU4 availability, frozen clean969354955741d6c0ca8ce816e1c59ad338b1605b and all
source/qualification hashes. Materialization creates plans, never admission or
runtime evidence. The original proven host-resource and inner-cgroup helpers
are reused byte-for-byte; compile-owner.diff shows the owner adaptation.

Reviewed contract:

- Owner pinnedCPU4; container1CPU/CPU4,2GiB RAM, zero swap,128PIDs, no network,
  pinned existing build image, no pull, read-only root filesystem.
- Frozen isolated checkout mounted read-only at canonical m7-pixelelated;
  common `.git` and immutable source packet read-only. Only fresh output/stage
  directories writable;128MiB `/tmp` tmpfs stays inside the memory cgroup.
- The installed target GCC path is a ccache wrapper. A diagnostic read-only
  file bind places the exact GCC15.2.0 ELF over that container pathname. The
  source wrapper is untouched and ccache is bypassed. Actual bind set, user,
  workdir, memory/swap, quota, affinity and512MiB file limit are inspected before
  the nonce-matched inner wrapper can compile.
- Output aggregate sampled ceiling512MiB; individual file ceiling512MiB;
  compiler console2MiB. Retention forecast512MiB output+64MiB records=576MiB.
  There is no bind-filesystem aggregate quota: exceeding the sampled ceiling
  aborts and fails the owner; the final stable total is checked too.
- 90s producer budget plus30s cleanup,120s total. Original cleanup still runs
  to release owned processes/container. Any cleanup>30s or total>120s is FAIL;
  cleanup is not abandoned to manufacture an in-budget PASS.
- Host RAM/swap/OOM/space/pressure and allocated-owner sampling, cgroup before/
  periodic/after/peak/OOM facts, original compiler/wrapper/Docker/watch/launcher
  returns and exact container retirement remain separate evidence channels.

Root reviews and performs these commands from the frozen checkout, using fresh
retention/admission immediately before launch:

```sh
cd /workspace/repos/rocknix.worktrees/m7-gtk4-build-20261017-01
python3 -I -B /tmp/pix-gtk4-postbuild-owner-prep-20261017/prepare.py

tools/watch-build --record-only -- python3 -I tools/host-maintenance/retention-report \
  --plan /workspace/tmp/pix-gtk4-input-compile-20261017-01/retention-plan.json \
  --output /workspace/tmp/pix-gtk4-input-compile-20261017-01/retention-report.json

python3 -I tools/host-maintenance/build-admission prepare \
  --plan /workspace/tmp/pix-gtk4-input-compile-20261017-01/admission-plan.json \
  --output /workspace/tmp/pix-gtk4-input-compile-20261017-01/admission.json

env -u BUILD_DIR tools/watch-build-submit \
  --owner /workspace/tmp/pix-gtk4-input-compile-20261017-01/submit -- \
  --admission /workspace/tmp/pix-gtk4-input-compile-20261017-01/admission.json \
  --activity-dir /workspace/tmp/pix-gtk4-input-compile-20261017-01 \
  --recursive-activity --interval 2 --stall-min 2 -- \
  taskset -c 4 python3 -I -B /workspace/tmp/pix-gtk4-input-compile-20261017-01/compile.py
```

The watch owner is a host-side command, following the previous helper-compile
pattern; it inspects its own internal Docker contract. Do not call Docker or
compile-input.py independently and do not forge inherited run markers.

Output should be `out/input/input-spike` and `out/input/compile-result.json`.
Require original compiler/compile-wrapper/inner-wrapper/Docker/owner results,
resource result and cleanup to pass. Submission exit0 alone is not completion.
Consume the original admission from the actual host namespace. A later read-only
closure inventory can include this binary; running it still needs separate
runtime qualification and allocation. No provider/browser/device authority is
granted by this compile.

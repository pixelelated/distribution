# Installed clean → #588 outer lifecycle — UNRUN

This additive source packet makes the accepted installed startup fixture runnable
on the next image. No VM, container, compiler, service, fixture, allocation,
source preparer, or payload reader ran here. Only source reads, AST parsing and
hash/seal inspection ran. There is no new product criterion or RC claim.

It reuses the accepted QEMU/serial/media/stop/admission lifecycle from
`docs/qa-logs/2026-10-14-independent-format-runtime/coordinator`, while replacing
old-image assumptions with exact final-build custody. The lifecycle programs:

- `prepare.py` verifies the frozen HEAD and exact ES package pin, original archive
  and manifest hashes, and actual payload reports. It extracts the unchanged
  installed #588 packet; extracts the unchanged timeout correction; prepares a
  separate corrected retained-state derivative. It creates fresh owner/config,
  retention and admission plans. It launches nothing.
- `vm-lifecycle.py` runs one admitted, default-boot, no-NIC QEMU using the accepted
  helper and its exact adjacent profile. It runs the original ready clean-state
  helper **before attaching fixture media or seeding anything**. It preserves
  that original JSON/serial receipt, captures actual boot and host process facts,
  and only then invokes the original `bind-image.py`. Fixture media is read-only;
  the boot-specific binding travels over serial in <=2000-character chunks.
- `run-guest.py` stops the actual frontend, mounts the sealed fixture/binding
  read-only, provides the existing 64 MiB scratch tmpfs, and runs the exact
  systemd owner command from the installed packet. It retains the real
  systemd-run wait status separately from timeout indication; exports original
  owner/payload receipts; restores the frontend; unmounts its scratch. Any
  forced cleanup or cleanup error prevents PASS.
- `close.py` derives from the accepted exporter: verifies original wrapper,
  runner, watcher, lifecycle and guest outcomes; requires actual owners gone;
  reads the stopped output filesystem; hash-verifies a lossless original-record
  archive. It neither consumes admission nor deletes anything. Failed attempts
  remain failed, with original records retained.

The proxy's actual `.pyc`, native library, unit, controller, readiness, queue,
flush and timers are untouched. Only the already reviewed observer/bootstrap is
mounted; no product-source PYTHONPATH or native overlay is an input. Accepted
baseline/service/ten-component/native-codec controls are not repeated. The
retained-state fixture is prepared separately and never seeds this clean guest.

Default topology stays unchanged. The explicit `outer-vm` path uses actual
4-vCPU/8-GiB QEMU, the existing per-process limits and process census, a 310-second
command watchdog with 10-second TERM grace (then a 2-second KILL wait), and the
watched host lifecycle. There is no kernel per-service memory/task cap claim.
An actually readable host memory-controller value is recorded, otherwise null;
ancestor caps are not inferred. No cgroup mount, kernel argument, or private
cgroup-v2 reboot is added. Input/output media each reserve 256 MiB; scratch is
64 MiB. Output bounds remain 4 MiB per guest file, 16 MiB for original fixture
records, and 32 MiB for exported guest evidence. Host command output is observed
once per second with an 8 MiB limit. Work has a 900-second alarm and an independent
90-second finalizer. Slow stages can therefore fail the original run; no retry,
deadline extension, or acceptance downgrade happens automatically.

## Final build facts needed, not available in this source lane

Current published freeze is distribution
`d6a87f05c1935516115b2cca1af22151a0209224`, ES
`3178b832b8d134198b2b4eede4f725d4ed283f8c`. The active engineering build is
`m7-p5-build-20261014-01/.build-runs/20261014T204343Z-b7a72fc6`.
This packet never reads an unfinished artifact as complete and must not be
launched during that compilation without root's separate allocation.

Before preparation, root must retain and review these actual completed receipts:

1. Build owner `/workspace/tmp/pix-m7-engineering-build-20261014-01/owner-result.json`,
   `inner.rc`, per-stage `stages/*/host-result.json`, `inner-result.json`, original
   container/make exits, resource finish receipt, and that run's `build.rc`,
   `runner-result.json`, watcher and launcher exits. All work/cleanup must have
   completed and actual build owners must be gone. The owner source explicitly
   cleans proxy/rcheevos/libchdr before image assembly; that is not proof those
   package commands later succeeded.
2. Actual final proxy package logs/stamps and prepared 112-source manifest,
   including startup source SHA
   `432bb07ac6b0abcdcb38800d7c75a92c768b2b6bea583a1bab6834bb7f7b0d00`;
   successful original package and `python_compile` outcome; source-removal and
   emitted `.pyc` paths/hashes; native c7eb/143317/607694 inputs and emitted
   post-strip ELF identity. Record the install→SYSTEM output transformation.
   A successful enclosing package with unmodified fail-fast compile steps
   may provide that exit chain; do not fabricate a separately logged child exit.
   The old unstripped component ELF hash is provenance, not the required final hash.
   Native STRIP in scripts/build uses `|| :`; its original exit remains unknown
   unless separately captured. Compare actual pre/staged/final ELF bytes and
   allocated-section correspondence; never infer strip success from the stamp.
3. Exact final install `.img.gz`, update `.tar`, SYSTEM and KERNEL hashes and their
   equality/custody across both artifacts. Record actual inflated image size
   (existing GPT/backup-LBA receipt), independently extracted boot config, and
   completed build image/system tree, with every binder-consumed byte, mode and symlink hop verified equal to final SYSTEM. An unverified package staging/SDK root is insufficient.
4. Original `update.json`, `install.json`, `.rc`, stderr and watched payload owner
   receipts from the existing `payload-check.sh`. Both must pass. The correction's
   existing positive shared-developer-identity post-check requires count >0 for
   the approved identity and zero unapproved identity; it is not a new gate.

Use the unchanged `source-receipt.example.json` schema carried here (also in the installed packet) for the
reviewed build-only source receipt, with actual evidence paths/bytes/hashes.
Its clean fields can remain false/unset before boot: the lifecycle preserves
that original receipt and adds only the real clean JSON hash, boot ID and verified
clean result to a separate `source-receipt.bound.json`. The binder still validates
the native pins, final ELF, 112 sources and bytecompile/package status. It does
not prove a fabricated review assertion true. Root must inspect underlying
receipts. Reports retain `source_pins_verified:false` where the original fixture
uses it; installed identity does not retroactively relabel native codec evidence.

Fill `custody.example.json` from those originals. The `reviewed_install_to_system_identity`
field records root's review of actual install→SYSTEM identity; this runner does not
pretend to prove that by a filename. Big image/SYSTEM hash reads occur under the
admitted lifecycle, not during `prepare.py`. There are no hardcoded final hashes;
explicit expected commit/ES arguments must equal both the actual frozen checkout
and the supplied custody. If the freeze changes, supply its actual reviewed pins.

## Exact continuation commands, after root allocation

Can this be done on the VM? Yes; root records the existing #565/#588 allocation
before running. This packet itself authorizes no allocation. The payload readers
are the already accepted host release-preflight components. Use a fresh owner
for each attempt; submission success is not completion. Commands below are
intentionally **not run** in this lane.

```bash
TASK_TREE=/workspace/repos/rocknix.worktrees/m7-p5-build-20261014-01
TASK_PLAN="$TASK_TREE/docs/qa-logs/2026-10-14-m7-installed-state-plan"
TASK_PACKET=/workspace/repos/rocknix.worktrees/m7-browser-memory-570/docs/qa-logs/2026-10-14-proxy-startup-race-internal/installed-lifecycle
TASK_OWNER=/workspace/tmp/pix-m7-installed-clean588-20261014-01
TASK_CUSTODY=/workspace/tmp/pix-m7-final-image-custody-20261014-01.json
# TASK_CUSTODY is the reviewed, completed record described above.
# Root chooses an unused display explicitly; 121 is a proposed allocation only.
python3 -I -S -B "$TASK_PACKET/prepare.py" \
  --checkout "$TASK_TREE" \
  --expected-commit d6a87f05c1935516115b2cca1af22151a0209224 \
  --expected-es 3178b832b8d134198b2b4eede4f725d4ed283f8c \
  --custody "$TASK_CUSTODY" --owner "$TASK_OWNER" --vnc 121

cd "$TASK_TREE"
tools/build-preflight
tools/watch-build --record-only -- python3 -I tools/host-maintenance/retention-report \
  --plan "$TASK_OWNER/retention-plan.json" --output "$TASK_OWNER/retention-report.json"
python3 -I tools/host-maintenance/build-admission prepare \
  --plan "$TASK_OWNER/admission-plan.json" --output "$TASK_OWNER/admission.json"
tools/watch-build-submit --owner "$TASK_OWNER/lifecycle-owner" -- \
  --admission "$TASK_OWNER/admission.json" -- \
  python3 -I -S -B "$TASK_OWNER/vm-lifecycle.py"
```

Before the above, if the actual payload gates still need execution, reuse their
existing executable and an independently admitted owner with its existing 24 GiB
scratch allowance; do not pack it into this 900-second VM owner:

```bash
# TASK_PAYLOAD_OWNER exists and is fresh; actual TASK_UPDATE/IMAGE and SHA values
# come from completed artifact custody, not a predicted timestamp.
cd "$TASK_TREE"
tools/watch-build-submit --owner "$TASK_PAYLOAD_OWNER" -- \
  --record-only --activity-dir "$TASK_PAYLOAD_OWNER" -- \
  bash "$TASK_PLAN/payload-check.sh" "$TASK_TREE" "$TASK_PAYLOAD_OWNER" \
  "$TASK_UPDATE" "$TASK_UPDATE_SHA" "$TASK_IMAGE" "$TASK_IMAGE_SHA"
```

Supervise the returned `.build-runs/<id>/` status and the submitted owner's
console. After it has finished, root supplies that exact run path (not `latest`):

```bash
TASK_RUN="$TASK_TREE/.build-runs/ACTUAL_RETURNED_RUN_ID"
TASK_EXPORT=/workspace/tmp/pix-m7-installed-clean588-evidence-20261014-01
python3 -I -S -B "$TASK_OWNER/close.py" \
  --owner "$TASK_OWNER" --run "$TASK_RUN" --packet "$TASK_EXPORT"
```

Review original clean JSON and serial marker, guest/owner/payload JSON and original
unit exits, installed bytecode/native identities, exactly one queued award/flush,
readiness, natural second online probe, stop/SQLite integrity, controller value
restoration, no cleanup intervention, actual QEMU/watch/owner exits and lossless
export. Then use the existing admission-consumption/retirement workflow with
those exact owner/run/output paths. `close.py` does not mark acceptance or consume
admission; failure remains a failure. Retain evidence before removing disk/media/
UEFI. A stop refusal or missing receipt requires diagnosis, not automatic reuse.

## Corrected retained proof stays separate

`prepare.py` extracts both original archives freshly and verifies their exact
original SHA256SUMS. It runs the correction's unchanged source materializer,
producing `$TASK_OWNER/source/retained-corrected`; original parent/child seals and
archive bytes remain unchanged. The only corrected existing file is the backup
process receipt: real wait returncode plus separate timeout indication.

For the later real replacement20→candidate rehearsal, root uses that derivative's
existing `prepare.py`, `run-phase.sh` and `collect.py` commands as documented in
its README. It seeds a **different fresh predecessor guest**, verifies before,
stages the exact new update tar through read-only media or separately allocated
transport, reboots through the real updater, verifies after, then runs installed
backup. Real Recent/account preservation and actual default backup secret
exclusions still need their original runtime receipts. No current-image cold boot
can substitute for that history; no proxy queue is added to the retained fixture.
That longer real-update allocation is not hidden inside this clean→#588 runner.

The executable continuation's remaining blockers are actual final build/image
custody, passing original payload reports and root's runtime allocation. Source
qualification here is not an installed PASS and does not hold compilation.

## Concrete source-chain producer and image verifier handoff

Root's `docs/qa-logs/2026-10-14-m7-image-verification` producer owns raw/update
SYSTEM/KERNEL equality and the selected final `image/system`→SYSTEM file/mode/link
comparison. `binder-members.txt` is the complete additional dependency set for
this binder. `/etc/profile`, `/etc/profile.d/001-functions`, `/usr/bin/python3`,
`/usr/bin/systemctl`, `/usr/lib/systemd/systemd`, `/usr/lib/autostart/daemons/006-raofflineproxy`,
and the real targets of zstd/crypto/systemd library symlinks must be included,
besides the proxy tree/unit/controller/native ELF and os-release. The boot config
is a separate install-image member. Original binder code resolves absolute links
beneath the supplied root and never follows them into host `/usr`. Its help text
calls this a bounded extracted SYSTEM root; code has no directory-name gate.
Root's verified completed `image/system` tree is byte-equivalent for every
consumed path, so it satisfies the same custody boundary without copying it.

`capture-source-chain.py` is the executable, bounded host readback producer for
the previously unspecified source receipt. Run only after the original build is
complete and root's image identity verifier has completed. It writes fresh
small evidence; imports no product code; executes no packaged interpreter,
compiler, strip, emulator or service. It:

- retains original successful owner/image-stage/runner receipts, clean-stage
  receipts, exact recipes, unpack/build stamps, source engine functions, proxy
  `DONE` job lines and their original package logs;
- matches all 112 actual prepared `.py` files to the already reviewed manifest
  with only the accepted startup021 replacement; retains the actual C files
  named by the native recipe and its LZMA glob;
- requires the original fresh compileall log to contain compilation and the
  startup module, records every emitted `.pyc` header/hash/mode/path unchanged,
  and compares the package stage to root's verified image/system tree;
- compares pre-strip/staged/final ELF allocated sections and actual hashes,
  preserves the unknown original strip exit, and records the source of the
  inferred compileall-success result separately from an independent wait status.

`config/path` enables `set -e`; `pkg_call` invokes `makeinstall_target` without
conditionally swallowing its result; `python_compile` runs the exact toolchain
`compileall.py -f -d <image path>` then removes source. The package's fresh `DONE`
job, its actual compile log, stamps and emitted files provide the original
compile outcome chain. The tool neither recreates `.pyc` with another interpreter
nor unmarshals it on the host. It retains magic/flags/header bytes to avoid
conflating timestamp headers with executable code. If a direct bytecode
correspondence check is later needed, it must use that exact packaged/toolchain
version, path, optimization and legacy-bytecode semantics in a separate allocation;
this continuation does not add that test.

```bash
TASK_BUILD_ROOT="$TASK_TREE/build.pixelelated-GENERIC_X64.x86_64"
TASK_BUILD_OWNER=/workspace/tmp/pix-m7-engineering-build-20261014-01
TASK_BUILD_RUN="$TASK_TREE/.build-runs/20261014T204343Z-b7a72fc6"
TASK_CHAIN=/workspace/tmp/pix-m7-proxy-final-chain-20261014-01
# TASK_IMAGE_VERIFICATION is the actual completed coordinator verifier receipt.
python3 -I -S -B "$TASK_PACKET/capture-source-chain.py" \
  --checkout "$TASK_TREE" --build-root "$TASK_BUILD_ROOT" \
  --build-owner "$TASK_BUILD_OWNER" --run "$TASK_BUILD_RUN" \
  --verified-root "$TASK_BUILD_ROOT/image/system" \
  --verification-receipt "$TASK_IMAGE_VERIFICATION" --output "$TASK_CHAIN"
```

The result is deliberately `source-receipt.review-required.json`, not a forged
review PASS. Root checks the retained original image-verifier receipt, source
manifest, uncached compile log/fail-fast call chain, emitted pycs and native
transformation. Then root retains a separate reviewed receipt using the exact
schema (`status: PASS`, `reviewed_source_to_bytecode_and_strip_chain: true`),
keeping all evidence and the explicit inferred-compile/unknown-strip qualifiers.
Point custody `source_receipt` at that reviewed file and its hash. No manual flag
alone supplies the evidence: every primary input and readback is retained by the
producer, with concrete missing-input failures. The existing final-image verifier
and this source-chain readback are complementary and do not duplicate a full
SYSTEM extraction or accepted runtime/component controls.

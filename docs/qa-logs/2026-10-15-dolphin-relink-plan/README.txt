SOURCE PREPARATION ONLY — compiler, Docker owner, VM, listener and fixture UNRUN.
Prepared 2026-10-15 for #584; no production tree, frozen output, tracker, or existing gameplay packet changed.

The frozen cache supports one-object recompilation and a private relink. build-plan.json is derived from compile_commands.json, build.ninja and CMakeFiles/rules.ninja belonging to Dolphin6094cfcf7b8fba733b3116fdf3414d51c1c0e4a4 in distributionfac608ff89940ce358ea9b8a95e9a08a6fe26568. All103 explicitly named persistent inputs resolve inside the frozen tree; the records include exact hashes, sizes and original symlink chains (411293175 bytes hashed, not copied). The original Ninja edge has8 object arguments and76 library arguments, including intentional repeated archives. Archive inputs are normal archives, not thin references. Candidate MainNoGUI.cpp is byte-identical to the previous sealed source finding's patched file.

The Docker source derives from the already qualified docs/qa-logs/2026-10-14-chdman-build-runner. docker_owner.py and watchdog.py are byte-identical, retaining exact CID/nonce checks, host PID namespace handshake, cgroup membership, original attach/container exits, independent watchdog and exact cleanup proof. Their inherited pix574 labels are ownership keys, not a claim that this work belongs to another issue. common.py changes the sole stage/limit and removes unrelated MAME helpers; run-stage.py removes MAME stage progression and binds these exact frozen inputs. The diff files make the small adaptations reviewable. No new generic runner or build system is introduced.

Mount the frozen root read-only at its original compiler prefix:
  physical /workspace/repos/rocknix.worktrees/m7-p5-build-20261014-02
  container /workspace/repos/rocknix.worktrees/m7-pixelelated
The exact pinned builder image is in build-plan.json. The working directory remains the original generated Dolphin build directory through that alias. The compiler wrapper calls its ccache and GCC15.2.0 binaries through absolute original paths; use CCACHE_DISABLE=1, private CCACHE_DIR/CCACHE_TEMPDIR and TMPDIR under /work. Only the changed source/object, compile dependency file, binary, linker dependency file and compiler temporaries are written in private /work. The compiler's original source path changes to /work/MainNoGUI.cpp; includes continue to come from the exact frozen source/generated include directories. No copy of a whole build cache, reconfigure, dependency install or shared stamp mutation occurs.

The candidate compile retains the original flags and adds only dependency capture. The link retains its exact object/library sequence and flags except that the MainNoGUI object, output and dependency-file destinations point to /work, and -flto=4 becomes -flto=2 to fit the already qualified2CPU limit. The earlier -flto=auto remains in FLAGS, with the final explicit -flto=2 overriding its worker selection. This is an explicit resource-scheduling variation, not a claim of byte-identical output. Compile, link, strip and ELF header/dynamic readback are separate original child receipts. The container has4GiB RAM/no swap,2CPU,256PIDs, offline networking, read-only root and a sampled1GiB scratch stop threshold. One900s work clock includes input checks, all children and final receipt work. The inherited cleanup retains its per-operation deadlines and300s final guard wait; the plan's600s cleanup value is a conservative allocation forecast, not a new enclosing timer. Do not describe this inherited failure cleanup as a120s hard bound.

The103-input inventory is the explicit Ninja/toolchain basis, not an invented claim to know every implicit header or CRT input before compilation. inner.py retains the actual GCC and GNU ld dependency files and hashes every surviving dependency after the child exits, checking frozen/private path ownership. Any linker-generated LTO temporary already removed by GCC is recorded as a generated dependency, with its raw path retained, rather than assigned a guessed hash. Unexpected missing persistent dependencies fail. Frozen inputs are hashed before and after. The exact source pin, current patches, generated metadata, retained toolchain and compile/link argv accompany the candidate. target-artifact.json expressly says this is a relink candidate and is not installed-image evidence.

Build allocation path, for root only after reviewing and integrating production patch018:

  TASK_TREE=/workspace/repos/rocknix.worktrees/m7-player-setup
  TASK_PACKET=/tmp/m7-dolphin-ra-runtime-plan-20261015
  TASK_BUILD=/workspace/tmp/pix-m7-dolphin-ra-relink-ACTUAL_FRESH_OWNER
  python3 -I -S -B "$TASK_PACKET/plan.py" --checkout "$TASK_TREE" --owner "$TASK_BUILD"
  cd "$TASK_TREE"
  tools/build-preflight
  tools/watch-build --record-only -- python3 -I tools/host-maintenance/retention-report \
    --plan "$TASK_BUILD/stages/dolphin-relink/retention-plan.json" \
    --output "$TASK_BUILD/stages/dolphin-relink/retention-report.json"
  # Review and consume original report/watcher channels and capacity before admission.
  python3 -I tools/host-maintenance/build-admission prepare \
    --plan "$TASK_BUILD/stages/dolphin-relink/admission-plan.json" \
    --output "$TASK_BUILD/stages/dolphin-relink/admission.json"
  tools/watch-build-submit --owner "$TASK_BUILD/stages/dolphin-relink/submit" -- \
    --admission "$TASK_BUILD/stages/dolphin-relink/admission.json" \
    --activity-dir "$TASK_BUILD/stages/dolphin-relink/logs" -- \
    python3 -I -S -B "$TASK_PACKET/run-stage.py" \
    --checkout "$TASK_TREE" --owner "$TASK_BUILD" --stage dolphin-relink

No allocation above has run. Do not regenerate this source packet during its owner. Consume original launcher, wrapper, command, watcher, container and guard receipts with the existing build-admission consume schema. A failure remains a failure; inspect it before proposing any new owner. The candidate can be retained for this single proof while compact receipt/manifest copies are sealed. A missing expected cache dependency is not permission to edit/rebuild the frozen tree: use a separately owned warm-package checkout with this exact pin/patch set and existing toolchain/sysroot read-only, rebuilding only Dolphin through the repository's watched/admitted package path if the minimal relink proves infeasible. Do not silently relax provenance checks or launch a full image build as recovery.

The VM route reuses the accepted single-guest installed-native lifecycle's original source archive at docs/qa-logs/2026-10-14-installed-native-lifecycle/source-originals.tar.gz. vm-basis contains only those small original scripts for inspection. census.py and guest-manifest.py remain byte-identical. vm-lifecycle.py changes only the coordinator HEAD check to a separately captured coordinator_commit; the guest BUILD_ID/image source remains frozenfac608ff. guest-owner.py changes only the case-result predicate and description; its subreaper/pidfd cleanup,180s guest work/210s owner,256MiB executable private tmpfs and compact original-output export remain. close.py changes only the case-specific acceptance predicate. prepare-vm.py binds the completed build originals, fresh case seal and final image readback; no source HEAD is confused with the older frozen guest image. The guest remains8GiB4CPU, no NIC, with the unchanged1200s work/120s cleanup host envelope and16GiB disk.

Can this be done on the VM? Yes. Client initialization, configuration reading, a local HTTP login request and clean process exit require no physical-device property. Root should put this answer and the exact four-row evidence contract on #584 before allocating. There is no real account, successful authentication, award, external endpoint, or proxy service. A listener inside the disposable guest returns only a synthetic failed login; it has no service-manager installation. All config, logs and generated DOL bytes are private tmpfs. The bare HostUrl127.0.0.1:8080 is intentionally the shipped proxy address: receiving POST /dorequest.php with r=login2 and the synthetic u/t demonstrates the real client's HTTP normalization and request path.

The four rows are deliberately small:
  1. Actual installed frozen /usr/bin/dolphin-emu-nogui, achievements enabled: establish a live CPU thread and advancing CPU ticks for2s, then ordinary SIGTERM exit0. Expect no manager initialization/shutdown/request. Preserve this as KNOWN_DEFECT_REPRODUCED, not a fixed-behavior claim.
  2. Hash-bound candidate in private executable tmpfs, enabled: same live-core observation; exactly one synthetic login POST to127.0.0.1:8080/dorequest.php, one initialization and one shutdown log, ordinary SIGTERM exit0.
  3. Same candidate, disabled: same live-core observation, no manager lifecycle or request, ordinary SIGTERM exit0.
  4. Same candidate, enabled, deliberately absent .iso: GenerateFromFile returns null (Linux DefaultMsgHandler writes stderr without blocking), startup still initializes RA, then BootManager::BootCore immediately returns false. Require original exit1, exact boot-error text and one initialization/shutdown pair. The queued login may be cancelled before dispatch, so0or1 synthetic requests are allowed here. This proves the dedicated RA scope guard's early-return path.

The self-authored0x104-byte DOL contains a single GameCube branch-to-self instruction. It is generated only by the future admitted guest run. Dolphin's CPU thread is entered only after BootUp succeeds, and the added2s CPU-tick interval prevents treating an alive but failed startup as a valid negative control. It is not a first-frame, rendering or gameplay claim. Null rendering and no audio keep this initialization proof independent of unchanged Wayland/gameplay evidence. The existing normal gameplay packet cannot prove HostUrl as written because it never enables RA. This probe avoids replaying it. Its ownership machinery could later consume a reviewed candidate overlay, but no existing gameplay packet or in-flight source was modified here.

VM preparation/allocation, only after the original relink owner is closed and root allocates this one guest:

  TASK_VERIFY=/workspace/tmp/pix-m7-image-readback-20261014-02/artifacts
  TASK_VM=/workspace/tmp/pix-m7-dolphin-ra-startup-ACTUAL_FRESH_OWNER
  # Choose an actually observed-free VNC number;123 is only a placeholder.
  python3 -I -S -B "$TASK_PACKET/prepare-vm.py" --checkout "$TASK_TREE" \
    --verification "$TASK_VERIFY" --build-owner "$TASK_BUILD" --owner "$TASK_VM" --vnc 123
  tools/watch-build --record-only -- python3 -I tools/host-maintenance/retention-report \
    --plan "$TASK_VM/retention-plan.json" --output "$TASK_VM/retention-report.json"
  # Review/consume original report channels; then prepare this distinct admission.
  python3 -I tools/host-maintenance/build-admission prepare \
    --plan "$TASK_VM/admission-plan.json" --output "$TASK_VM/admission.json"
  tools/watch-build-submit --owner "$TASK_VM/lifecycle-owner" -- \
    --activity-dir "$TASK_VM/logs" --admission "$TASK_VM/admission.json" -- \
    python3 -I -S -B "$TASK_VM/vm-lifecycle.py"
  # Wait for all original owners to finish; read the actual run path from the submission.
  python3 -I -S -B "$TASK_VM/close.py" --owner "$TASK_VM" \
    --run "$TASK_TREE/.build-runs/ACTUAL_RUN" --packet /workspace/tmp/pix-m7-dolphin-ra-result-ACTUAL_FRESH_PACKET

The final acceptance remains coordinator review of original guest/host results, requests, logs, exe hashes, PID/start identities, exact CID/QEMU/descendant absence and source bindings. The unmodified installed baseline is tied to the final image readback; its current expected hash ise6c6207d663f7ab53ca6f9fe3c836c98751545b45b869cf32477f7f130e0170b (8569152bytes). The candidate is intentionally not called an installed new-image binary. A guest-only temporary installed-path bind overlay would be a distinct, explicit adaptation if the issue wording demands that before the next image. After production integration/image construction, the installed smoke should check the new installed SHA and one enabled synthetic startup request without replaying all unchanged gameplay or component matrices.

Upstream/source conclusions remain in /tmp/m7-dolphin-ra-init-20261015: Dolphin is the code-fix destination; ROCKNIX is the packaging backport/comment destination; keep #585 tracking the upstream opportunity and respect deferred submission. This packet makes no new upstream/issue state change.

Static-result.json records only AST parsing, bash -n,103 frozen input rehashes, exact candidate-source comparison and byte identity of reused ownership components. These are not compile, runtime, fixture or service PASS claims. All runtime entrypoints remain UNRUN.

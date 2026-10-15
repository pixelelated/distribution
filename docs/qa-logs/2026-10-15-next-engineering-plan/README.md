# Next GENERIC_X64 engineering image — source-only executable derivative

UNRUN. Template product source is historical local-next956f9481872d3d64f3e33d495e5ab25dfd9aaefd, compared with frozenfac608ff89940ce358ea9b8a95e9a08a6fe26568. A final40-hex commit is required at every preparation/transfer step; the final independently reviewed Dolphin package.mk SHA256 is also required as --dolphin-recipe-sha256. That one recipe may differ from the historical template to accommodate the newly identified immutable Sys installation correction. All other product hashes and the exact three changed product paths remain fixed. Record-only later commits are allowed. Any additional product-path change requires a reviewed packet revision, not changing a success record or weakening a hash. Final source must be committed, clean, and published: the qualified predecessor prepare-plan.py already requires it to be an ancestor of origin/next, and that guard is unchanged.

FREEZE HOLD: root is addressing the auditor finding that Dolphin compiles its Sys data location under /usr/share/dolphin-emu/sys while the recipe copies Data/Sys only under /usr/config/dolphin-emu. No fix bytes or resulting behavior are asserted here. Root must settle/review that source change and explicitly supply its final recipe hash before allocation. Known primary source findings and the Steam continuation settle before the freeze. Root reports Steam owner02 metadata+14 terminalPASS originals exported and consumed; this packet does not independently qualify that run. The engineering image can precede full Milestone audit closure because remaining installed/native criteria require it. Audit may continue in parallel. H700/SM8550 builds and RC progression still require completion of the applicable audit. Publication for this runner does not declare audit completion or waive it.

Only this private packet and its assigned durable copy were written. No worktree, cache, owner, admission, compiler, container, VM, service, fixture or commit was created/executed. Python AST/static byte comparisons are the only validation. Can this be done on the VM? Installed behavior: yes, in the existing no-NIC guest. The production build uses the qualified cross-toolchain container.

## What is preserved and changed

The parent is docs/qa-logs/2026-10-14-gstnet-rebuild-plan/source-originals.tar.gz, engineering/. Its actual three-stage execution is qualified in 2026-10-14-gstnet-corrected-image/build, and original transfer in its transfer/ directory. originals/ retains exact prior scripts and predecessor receipts. complete.diff.gz is the complete lossless script diff. host-resources.py and inner-build.py are byte-identical both to the parent archive and the actual completed build owner. No generic runner was added.

Changes are the new source/destination/owner identities, required final commit, exact product allowlist/hashes plus the explicit final reviewed Dolphin recipe hash, current predecessor evidence/measurement, package stage selection, and caller-selected exclusive output for the existing dependency census. The existing same-filesystem rename, source/branch guards, original result channels, nonroot identity, private container /tmp check, source freeze checks, nonce-bound container observation, PID/CID checks, resource limits, failure stop, and cleanup semantics remain.

The three stages are clean-dolphin-sa (canonical docker-package-clean), build-dolphin-sa (canonical docker-package), then image (canonical docker-GENERIC_X64). The image stage invalidates only its destination .stamps/image/build_target first. Standard CLEAN_OS_BASE regenerates emulators for Install Steam.sh; standard image installation resets image/.stamps and image/system. Dolphin scoped clean/re-unpack applies patch018 to the unchanged pin6094cfcf7b8fba733b3116fdf3414d51c1c0e4a4. No Qt/ES/GStreamer/proxy/Flycast/library clean is added. This is not an injected one-object candidate or forged stamp.

Source cache moves from m7-p5-build-20261014-02 to new m7-p5-build-20261015-01, branch build/m7-p5-20261015-01. Only build.pixelelated-GENERIC_X64.x86_64 moves. Both tracked checkouts, old target/release and historical receipts remain. No copy, hardlink clone, symlink alias, overwrite, cross-device fallback or automatic rollback. A failed post-rename owner retains exact intent and custody for root diagnosis.

## Coordinator preparation — execute only after allocation

Use this directory unchanged, or the byte-verified durable copy at docs/qa-logs/2026-10-15-next-engineering-plan. All proposed new worktree/owner paths below must be absent; if used meanwhile, stop and revise the sealed identities rather than reuse an owner. Root supplies TASK_COMMIT explicitly after review/commit/publication, and TASK_DOLPHIN_RECIPE_SHA explicitly from the independently reviewed final recipe. The following commands are documentation, not execution performed by this packet.

```bash
: "${TASK_COMMIT:?Set the final reviewed, committed, published 40-hex distribution source}"
: "${TASK_DOLPHIN_RECIPE_SHA:?Set the SHA256 of the independently reviewed final Dolphin package.mk}"
TASK_PACKET=/workspace/repos/rocknix.worktrees/m7-player-setup/docs/qa-logs/2026-10-15-next-engineering-plan
TASK_TREE=/workspace/repos/rocknix.worktrees/m7-p5-build-20261015-01
TASK_ES=3178b832b8d134198b2b4eede4f725d4ed283f8c
TASK_TRANSFER=/workspace/tmp/pix-m7-next-cache-transfer-20261015-01
TASK_BUILD=/workspace/tmp/pix-m7-engineering-build-20261015-01
TASK_MEASUREMENT=$TASK_PACKET/capacity-measurement.json
(cd "$TASK_PACKET" && sha256sum -c SHA256SUMS)
git -C /workspace/repos/rocknix fetch origin next
git -C /workspace/repos/rocknix ls-remote --exit-code origin refs/heads/next
git -C /workspace/repos/rocknix merge-base --is-ancestor "$TASK_COMMIT" origin/next
git -C /workspace/repos/rocknix worktree add -b build/m7-p5-20261015-01 "$TASK_TREE" "$TASK_COMMIT"
mkdir -m 700 "$TASK_TRANSFER" "$TASK_BUILD"
cd "$TASK_TREE"
tools/build-preflight
python3 -I "$TASK_PACKET/prepare-plan.py" --checkout "$TASK_TREE" --commit "$TASK_COMMIT" --dolphin-recipe-sha256 "$TASK_DOLPHIN_RECIPE_SHA" --expected-es "$TASK_ES" --measurement "$TASK_MEASUREMENT" --owner "$TASK_TRANSFER" --stage transfer
tools/watch-build --record-only -- python3 -I tools/host-maintenance/retention-report --plan "$TASK_TRANSFER/retention-plan.json" --output "$TASK_TRANSFER/retention-report.json"
```

Inspect original retention-report command/runner/monitor results before admission. The measurement is the existing final_after_producer sample at2026-10-14T23:06:25.774014Z, cache125591408640bytes. The original allocation log and original0 rows are bound; no new scan occurred. Its unchanged24-hour age limit and source-log SHA guard apply. Refresh via the existing scoped measurement workflow if stale or the named roots changed materially; do not alter a timestamp. Current preflight/admission checks actual free capacity. Transfer allowance65GiB is metadata+margin, not a duplicate cache. Build allowance is max(cache/3,32GiB)+8GiB sources+16GiB firmware+32GiB immediate QA+64GiB margin. No cold-Qt allowance or reclamation credit.

## Fresh dependency readback and explicit coordinator assessment

All old-cache readers must finish or be rebound first. Include the completed Dolphin relink, any remaining source/audit readers and prepared fixture owners; retain corresponding-source/evidence custody. Do not infer current host absence from their past PASS. Fresh census must run in actual host PID namespace4026531836, after the retention report ends and before transfer admission. It is the original scoped Docker/readable-process census with only the old-root and output identities changed; output creation is exclusive.

```bash
tools/watch-build --record-only -- python3 -I "$TASK_PACKET/dependency-readback.py" --output "$TASK_TRANSFER/dependency-readback.json"
```

Review that original readback and its original watch results. Preserve its process errors and Docker/registry facts. The scope remains all readable argv, same-UID cwd/root/fd/maps, and all Docker mounts inspected; it is not a privileged whole-host FD census. No previous protected-service exemption or PID is reused. A freshly inspected protected session service or exited zombie may be explicitly excluded with its actual PID/comm/state/cgroup and stated basis, as in the qualified predecessor. An unexplained error, live matching process, overlapping mount, active admission or pending cache consumer prevents clearance.

Root then writes a NEW `$TASK_TRANSFER/dependency-assessed.json` from that readback, using the existing transfer contract below. This is an explicit coordinator review, not an automatic success transform. `utc_epoch` is copied from the raw observation, never refreshed during assessment. `remaining_consumers:[]` and `prepared_consumers_resolved:true` require root's actual resolved-consumer check. Preserve the raw file and record its SHA256, original path, every error/exemption and scope in the assessed record.

```json
{
  "status": "CLEAR_WITH_STATED_SCOPE",
  "root": "<exact raw root>",
  "root_identity": {"device": "<raw identity.device integer>", "inode": "<raw identity.inode integer>"},
  "host_pid_namespace": 4026531836,
  "utc_epoch": "<raw utc_epoch number>",
  "process_matches": [],
  "process_errors": [],
  "docker_all_mounts": [],
  "active_admissions": [],
  "remaining_consumers": [],
  "prepared_consumers_resolved": true,
  "excluded_from_fd_scope": [],
  "original_readback": "<absolute original readback path>",
  "original_readback_sha256": "<actual SHA256>",
  "scope": "<actual reviewed scope and any exclusions>"
}
```

This is a field contract, not an existing receipt. `docker_all_mounts:[]` records the empty overlapping-mount set after inspecting all containers, not a claim that Docker globally has no mounts. Raw `container_references` must be empty. If any unresolved item remains, keep REVIEW_REQUIRED and do not submit. The transfer itself rechecks assessed root/inode/namespace/age<=900s, absence assertions, Docker overlaps, original qualified predecessor outputs and admission/source binding.

```bash
TASK_DEPENDENCY=$TASK_TRANSFER/dependency-assessed.json
TASK_DEPENDENCY_SHA=$(sha256sum "$TASK_DEPENDENCY")
TASK_DEPENDENCY_SHA=${TASK_DEPENDENCY_SHA%% *}
python3 -I tools/host-maintenance/build-admission prepare --plan "$TASK_TRANSFER/admission-plan.json" --output "$TASK_TRANSFER/admission.json"
tools/watch-build-submit --owner "$TASK_TRANSFER" -- --admission "$TASK_TRANSFER/admission.json" --activity-dir "$TASK_TRANSFER" -- python3 -I "$TASK_PACKET/transfer-cache.py" --owner "$TASK_TRANSFER" --commit "$TASK_COMMIT" --dolphin-recipe-sha256 "$TASK_DOLPHIN_RECIPE_SHA" --dependency-readback "$TASK_DEPENDENCY" --dependency-sha256 "$TASK_DEPENDENCY_SHA"
```

Actively supervise the exact run returned. Original transfer bound120s. Then require original transfer-result/cache-ready PASS, inner.rc0, command/monitor/runner/launcher/tool-wrapper0, same device/inode, old cache absent/new cache present and actual owners exited. Preserve source/target custody, intent, raw+assessed dependency readbacks and originals. Root prepares consumption-evidence.json from those actual facts with the exact admission outputs and consumes through the existing tool; this packet does not manufacture it.

```bash
TASK_TRANSFER_RUN=$(cat "$TASK_TRANSFER/run.path")
python3 -I tools/host-maintenance/build-admission consume --run "$TASK_TRANSFER_RUN" --evidence "$TASK_TRANSFER/consumption-evidence.json"
```

## Warm production build after transfer consumption

Only after the transfer is complete/consumed, refresh preflight and make a new build admission. No concurrent VM/compiler family. Preserve the qualified actual-host namespace, main.git/source-cache/options mounts and absence/presence-only environment checks. The canonical Docker path remains /workspace/repos/rocknix.worktrees/m7-pixelelated for embedded cached compiler wrappers; do not rewrite those wrappers. Builder digest988c0ba586263caeba4be4c03bd16eee055c9d066657951e320087bb8226ee39 remains pinned by the existing Makefile/container contract.

```bash
tools/build-preflight
TASK_TIMESTAMP=$(date -u +%Y%m%dT%H%M%SZ)
python3 -I "$TASK_PACKET/prepare-owner.py" --checkout "$TASK_TREE" --commit "$TASK_COMMIT" --dolphin-recipe-sha256 "$TASK_DOLPHIN_RECIPE_SHA" --expected-es "$TASK_ES" --owner "$TASK_BUILD" --cache-ready "$TASK_TRANSFER/cache-ready.json" --timestamp "$TASK_TIMESTAMP" --family-seconds 7200
python3 -I "$TASK_PACKET/prepare-plan.py" --checkout "$TASK_TREE" --commit "$TASK_COMMIT" --dolphin-recipe-sha256 "$TASK_DOLPHIN_RECIPE_SHA" --expected-es "$TASK_ES" --measurement "$TASK_MEASUREMENT" --owner "$TASK_BUILD" --stage build
tools/watch-build --record-only -- python3 -I tools/host-maintenance/retention-report --plan "$TASK_BUILD/retention-plan.json" --output "$TASK_BUILD/retention-report.json"
python3 -I tools/host-maintenance/build-admission prepare --plan "$TASK_BUILD/admission-plan.json" --output "$TASK_BUILD/admission.json"
tools/watch-build-submit --owner "$TASK_BUILD" -- --admission "$TASK_BUILD/admission.json" -- python3 -I "$TASK_BUILD/build-owner.py"
```

Review build-inputs.json, retention report and original watch results before each corresponding admission/submission. Bounds are unchanged: narrow stages CPUs0–3/24GiB; image CPUs0–23/40GiB; no container swap;2048PIDs;7200s family with no extension in flight;8GiB host-available floor and64GiB volume floor. These are operating ceilings, not measured needs or a pre-created reservation. The canonical environment unsets DIRTY/CLEAN_SOURCES/custom identity overrides, sets a unique dev build identity and verifies actual nonroot UID/GID, TMPDIR/mktemp, affinity/nproc and cgroup identity. Monitoring and cleanup retain exact original exit/status semantics. No post-hoc success normalization.

Consume only after original stage host/inner/wrapper, owner/resources, command/runner/monitor and launcher/tool-wrapper channels succeed, every expected container actually exited/retired, no forced cleanup/OOM/owner survivor, and unchanged source/helper bindings. Root records completed-readback and consumption-evidence from actual originals, then consumes the exact run with the normal tool. Preserve failed original outcomes and stop; no retry/clock reset/owner reuse.

## Downstream scope

Build0 is not installed acceptance. Rebind the qualified artifact verifier to actual completed outputs and require raw/update SYSTEM+KERNEL equality, new build/source identity and both Dolphin package-install/image/guest byte identities. Private relink candidate5cb5... is prior component evidence, not a predicted new installed ELF hash. Include the final reviewed Sys resource installation/readability/byte checks required by the new source finding. Run the short installed enabled/disabled/failed-boot RA controls without replaying the old broken baseline. No real account/award.

Run the pending native gameplay/save continuation ONCE on the new image, through normal ES/launcher routes. Its prepare.py already binds a new actual clean build commit/verifier; all15 fixed consumed source rows match the template. It does not enable RA or prove HostUrl. Preserve existing1800s+120s cleanup,120s first-frame,360s earned-score and512MiB evidence bounds. Use the existing fixture and authored media; no new game/tool build is needed. New clean-install/default-loader and retained-upgrade acceptance stay required before firmware publication. Keep unchanged ES3178/UI/component evidence in its actual original scope rather than repeating broad matrices solely for os-release.

Install Steam.sh is not packaged for GENERIC_X64 or AMD64 by the current device gate; it is selected on SM4450/SM8250/SM8550/SM8650/SM8750. The x64 build regenerates emulators but cannot establish installed ARM/FEX Steam acceptance. Retain root's separately qualified source-bound metadata/transaction VM originals and later actual selected-device payload checks.

Remaining dependencies: settled Dolphin Sys recipe fix and its independently reviewed final SHA256, final root source/publication/cheap-gate review, fresh host consumer/dependency and capacity/admission review, actual transfer/build original results, actual artifact readback and installed/native/retained acceptance. Full Milestone audit closure is not a circular precondition for this engineering image. No RC/deployment/upstream submission is authorized by this packet.

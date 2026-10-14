# Fourteen remaining Steam caller cases in one guest — #564 / #579 / #580 / #582

SOURCE ONLY; UNRUN. This executable derivative implements the additive one-guest
assessment93803dd3d11fb061e8baf7bf35358bfec2a3feaa. It uses the accepted single-case
Steam lifecycle/media/serial/stop path and accepted UI-route export mechanism;
`source-originals.tar.gz` preserves those exact sources. There is no new generic
runner or product change. Can this be done on the VM? Yes: installed guest tools,
a byte-exact **source installer in a private chroot**, synthetic storage/payloads,
no NIC and actual native-client exec denial. This is not installed Steam, native
ARM64/Proton, real self-update or power-loss acceptance. GENERIC_X64's intentional
Steam absence and the later selected-SM8550 installed/native checks are unchanged.

The remaining source packet is exactly `/tmp/pix582-remaining-source01`, manifest
`79dc1d57d8741b644e99cd8348c4c362fbef3a1c815c48f6fa23b84a6e201c34`. All its executable
bytes remain unchanged. This derivative copies its sealed files into the required
repository depth on read-only input media. The only fourteen permitted labels are
listed literally in guest-stage.py; the nine accepted product cases cannot run.
The fixture's existing per-process admission/exec-death controls remain intact.

## Concrete sequence, after the engineering build and image verification finish

Use the existing completed `2026-10-14-m7-image-verification/verify-image.py` result,
inputs.json and retained candidate.img. No predecessor image or component overlay
is accepted. Preparation resolves the actual .img.gz from that result and binds
its full hash/size, frozen checkout/source commit, exact installer fab7cdb4…9229d,
source packet, VM helper and serial/stop tools. The guest independently checks
BUILD_ID and GENERIC_X64 before each stage. Preparation launches nothing.

```sh
TASK_582_PACKET=/absolute/path/to/this/sealed/packet
TASK_582_CHECKOUT=/workspace/repos/rocknix.worktrees/m7-p5-build-20261014-01
TASK_582_OWNER=/workspace/tmp/pix582-remaining-vm-20261014-01
# TASK_582_VERIFIED is the actual completed verify-image output; TASK_582_VNC is a free100..199 endpoint.
python3 -I -S -B "$TASK_582_PACKET/prepare.py" \
  --checkout "$TASK_582_CHECKOUT" --image-verification "$TASK_582_VERIFIED" \
  --remaining-packet /tmp/pix582-remaining-source01 \
  --owner "$TASK_582_OWNER" --vnc "$TASK_582_VNC"
cd "$TASK_582_CHECKOUT"
tools/watch-build --record-only -- python3 -I tools/host-maintenance/retention-report \
  --plan "$TASK_582_OWNER/retention-plan.json" --output "$TASK_582_OWNER/retention-report.json"
# Consume original retention command/monitor/runner/tool exits before admission.
python3 -I tools/host-maintenance/build-admission prepare \
  --plan "$TASK_582_OWNER/admission-plan.json" --output "$TASK_582_OWNER/admission.json"
tools/watch-build-submit --owner "$TASK_582_OWNER/lifecycle-owner" -- \
  --admission "$TASK_582_OWNER/admission.json" --activity-dir "$TASK_582_OWNER/logs" -- \
  python3 -I -S -B "$TASK_582_OWNER/vm-lifecycle.py"
```

Review exact prepared identities and capacity before submission. Submission is
not completion. Actively supervise lifecycle-owner/console.log, original launcher
and watch-build run, per-stage host receipts and vm-result.json. The single host
owner locks serial/HMP access, prints each stage start and consumed outcome, and
never dispatches a later case after an unexpected original result/restoration
failure. No user/operator visual session or parallel runtime is required.

Expected caller sequences remain five0 cases, four1 refusal cases, then five1→0
explicit retry cases; the exact table is in the earlier sealed installed-recovery
plan. Each completed fixture/namespace wrapper must0; the trace's original caller
status remains0 or1 as appropriate. The intentionally negative internal idle/death
control records remain negative and cannot be confused with the outer result.
The new wrapper records the actual **timeout command's** exit separately as
`original_wrapper_exit`; timeout/interruption is never invented as a returned
installer result. Original caller/trace channels are retained unchanged in the
fixture archive.

## Per-stage ownership, restoration and export

Each stage gets its own process, exclusive output directory and new3GiB executable
nosuid,nodev tmpfs. The unchanged fixture creates private mount/PID/network/IPC/UTS
namespaces and exact source/tools. The wrapper is a subreaper, observes the live
original command and its output cap, and checks strict proc descendants plus
absence of the recorded private namespaces before acceptance.

Selected real guest Steam/FEX/profile/kill-state paths are recorded without values
(before/after identities, hashes, link targets and explicit absence). The parent
PID/start/namespace identities and selected storage/tool/media/binfmt mount bindings
must remain identical. Unrelated journal files or background PID churn are not
mistaken for fixture state. Service commands and binfmt writes remain synthetic
inside the original chroot; no guest controller or product service is substituted.

Before scratch retirement, all original observation files are archived with the
accepted rootfs/storage/tmp/qa-payload exclusions. Every archive member is read
back against its original size/hash and the unchanged source file. Original
before/after manifests and first-failure journals remain in that archive. Only
normal umount0 and an empty removed owned mountpoint, no remaining stage processes
or mounts, and unchanged selected parent state permit `restored:true`.

On failure the family stops. The wrapper preserves original return values,
records failure cleanup and makes a bounded attempt to export quiescent scratch
records. Unrestored scratch is never erased/reused; family stop ends the disposable
guest. If a record cannot be exported, that is an explicit incomplete-evidence
failure. A final output-manifest seal/flush is attempted before stopping by the
recorded QEMU pidfile. No automatic retries, accepted-case repeats, forced/lazy
scratch unmounts, or native-success reinterpretation exist.

## Bounds and final export

One8GiB/4-vCPU no-NIC guest,16GiB virtual disk;256MiB read-only input and1280MiB
output ext4. One active3GiB tmpfs with existing2368MiB free admission. Keep original
90s fixture/80s trace/10s cleanup,120s timeout command plus10s kill allowance.
Each new wrapper has a160s normal-work alarm, bounded failure export and a host
180s stage serial envelope; a guard expires the family, not the next stage.
Each wrapper stdout/stderr is monitored at2MiB; original fixture retained-data64MiB
and event/log limits stay unchanged. Each exported stage is capped75MiB and the
family1100MiB; actual output free space is checked before dispatch.

The family alarm is3600s. No new stage starts unless its180s plus90s fail-stop
reserve fit the remaining time. Original budget:14×180=2520s,600s preparation/boot,
300s final export/stop and180s reserve. Failure cleanup uses bounded serial seal
and flush plus existing35s vm-stop, at most90s additional fail-stop reserve.
There is no per-service memory-controller requirement. Proposed host output export
is one watched allocation with1800s outer deadline/cleanup; each existing debugfs
dump retains30s and total declared guest bytes remain≤1100MiB.

Once actual lifecycle/launcher/runner/monitor/QEMU owners have exited, use the
actual printed watch-build run directory, not an example suffix:

```sh
python3 -I -S -B "$TASK_582_PACKET/export.py" \
  --owner "$TASK_582_OWNER" --checkout "$TASK_582_CHECKOUT" \
  --run "$TASK_582_RUN" --output "$TASK_582_EXPORT"
```

This reuses stopped-output-media debugfs export, verifies every guest file and
original fixture archive member, and losslessly archives original host owner/run
records. Normal success requires all original family channels0 and all14 stage
results/restoration passes. `export-result.json` explicitly carries
`qualification_pass`; even true means only the stated source-chroot scope.
After a failed family, use `--retain-failed` only to preserve evidence; it does not
waive failed channels or qualify the family. Export0 in that mode is preservation,
not acceptance. If boot/media never became available, retain the original owner
and run records directly; no absent guest results are manufactured.

Finally consume admission under the existing tools only after reviewing originals,
then retire the one disposable disk/media/UEFI and scratch exports whose dependency
has ended. Do not merge old worker ancestry; carry only this owned packet content.

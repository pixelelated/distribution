# One guest, fourteen independent Steam recovery stages — #564 / #579 / #580 / #582

SOURCE ASSESSMENT ONLY, UNRUN. This additive follow-up supersedes the **fresh VM
per case** language in commit `9e6bae8b550622ed3b3fd0549ac8838b63305a78`,
`docs/qa-logs/2026-10-14-steam-installed-recovery-plan/README.md`, specifically
“One case per newly admitted owner” and “No existing owner or input disk is
reused.” Retain that sealed original unchanged. The new disposition is one newly
admitted disposable guest and immutable input medium, with fourteen separately
watched, sequential case stages. No old spent guest/owner is revived. The
previous per-case900s lifecycle/256MiB-media example does not bound this family.

The adapter's fourteen-case allowlist, nine accepted exclusions, source/native
limitations, installed-source issue distinctions and original outcome table are
unchanged. No fixture, product, runtime, build, provider, native operation or new
whole-lifecycle code was executed or edited for this assessment.

## Source conclusion

No case requires a new boot for state isolation. In the accepted8f0eaf packet
`docs/qa-logs/2026-10-14-steam-crc-event-source/`:

- `fixture.py:242–287` forks new mount/PID/network/IPC/UTS namespaces and arms the
  inherited-parent-pidfd death guard. `namespace_worker` requires PID1 and distinct
  namespace identities before any bind. `fixture.py:429–449` makes mounts
  recursively private first, binds only each case's storage/qa/tmp and read-only
  native tool roots, and uses `mount -n` so no shared mtab is written.
- `fixture.py:442` overlays private binfmt **regular files** over the child's
  proc target. Product writes do not reach guest binfmt registration. The only
  shared writable device is the actual `/dev/null`; it stores no case state.
- `payload.py:70–137,250–316` builds a new chroot, profile, synthetic storage and
  case metadata beneath the selected new output. `/run` has no guest service
  socket; `boundary.py:148–152` substitutes systemctl/sway commands, and its
  set_kill writes only jailed `/tmp/.process-kill-data`. No real guest service,
  library, FEX root, application profile or process-kill state is changed.
- Python audit hooks, limits, signal handling and subreaper state belong to the
  newly launched fixture/descendants, not the persistent family supervisor.
  `fixture.py:152–194,563–565,804–825` reaps children and requires quiescence;
  namespace PID1 exit destroys its process namespace. The actual trace/namespace
  original result channels remain mandatory. Parent-death and trace admission
  controls stay part of each unchanged fixture; none of the nine accepted
  product-case labels is rerun.

Intentional held stages, partial clients and journals in negative cases are
**case-local evidence**, not a reason for a new guest. Export their original
records before retiring that case's tmpfs. Never feed their storage into the next
case, except the explicit second attempt already implemented within a retry case.

## Inter-stage contract

The existing fixture proves its own private namespace/process outcomes. The
current single-case wrapper does not yet record a between-case parent restoration
receipt. The family owner must add that small orchestration check before looping;
merely seeing fixture0 is insufficient. No runner change is made here.

1. Each stage has a fresh process, unique stage ID and new direct TMPDIR output
   child on its own3GiB executable,nosuid,nodev tmpfs. Never keep all fourteen
   scratch mounts live. Keep the input source tree/media read-only and byte-bound;
   preserve its `docs/qa-logs/<packet>` directory depth. Retain the existing
   2368MiB free-space and exact tool/source hash admission checks.
2. Save the parent's PID/start identity and namespace identities; record its
   mounts for the input/output media, real `/storage`, native tool roots and
   binfmt path. Snapshot only the relevant real Steam/FEX/profile/kill-state
   paths, with absence explicit; do not hash the entire live `/storage` or demand
   that unrelated journal/service activity stop. Those selected paths must be
   unchanged after the case. Parent namespaces and those original mount bindings
   must be unchanged; there must be no stage-owned mounts left outside its scratch.
3. Consume the original fixture/namespace/trace/timeout/watcher results and
   expected caller0,1 or1→0 sequence from the existing outcome table. Require
   PASS, no unexpected intervention/guard, empty recorded trace/descendant lists,
   and no actual surviving stage PID/start identities or process using the recorded
   private namespace identities. An unreadable census is failure, not empty.
   The fixture's proc reader skips PermissionError; the family restoration
   assertion must not interpret that skip alone as a complete guest census.
4. Export and hash that case's lossless original records to its unique directory
   on output media; verify the export while scratch still exists. Include first
   failure journals and every original event stream. Sync, unmount **normally**
   and remove only the now-empty owned scratch mountpoint. A busy mount, lazy or
   forced unmount, missing export, survivor or changed selected guest path stops
   the family. Do not delete scratch to manufacture restoration.
5. Write an immutable stage restoration receipt and consume the original stage
   result before starting the next label. Any unexpected failure ends dispatch;
   retain partial results and run the family-owned stop/export cleanup. Do not
   retry a case, skip a failed stage, switch to a fresh VM and continue silently,
   or convert an original negative result into success.

Use the existing serial owner/lock for all parent operations. The same guest is
reused, never the prior case process, scratch, output name or synthetic storage.
Global PID-list equality is not appropriate: normal guest services can change
PIDs. Verify stage identities/namespaces and the specific state the fixture could
reach. The unchanged kernel/tool identity guards still apply on the final image.

## Realistic family bounds and output capacity

- One normal8GiB/4-vCPU no-NIC QEMU guest, one boot, one read-only input medium.
  Existing private3GiB tmpfs is allocated once per active case and fully retired
  before the next. The production GENERIC_X64 image still contains no Steam.
- Keep each fixture at90s, each trace at80s and its cleanup10s; keep the existing
 120s guest command timeout plus10s kill allowance. A stage's proposed complete
  envelope is180s: execution/cleanup130s plus at most50s for original-result
  assessment, export and restoration. Hitting any bound stops the family.
- Use **3600s** for the family, replacing the one-case900s example. Budget
  14×180=2520s for stages,600s for image/media/preparation/boot,300s for final
  export/normal stop and180s reserve. These are source budgets, not measured
  peaks or a promise that every future case fits. The normal stop is inside the
  family deadline; reserve a separately declared ≤90s fail-stop cleanup if the
  hard deadline fires. Cleanup after deadline can never produce PASS.
- Use **1280MiB output ext4**, replacing the old256MiB single-case medium. Preserve
  the existing64MiB retained fixture and2MiB individual-log bounds. Cap each
  complete exported case directory at75MiB and the family at1100MiB; fourteen
  case ceilings total1050MiB, leaving50MiB for global evidence and180MiB filesystem
  margin. Check actual free space before dispatch. Exceeding a cap is an original
  failure; preserve what exists and stop. No unbounded accumulation or deletion
  of earlier original evidence to make space.

The accepted single-case wrapper/lifecycle at
`/workspace/tmp/pix582-client-vm-20261014-11/{run-guest.sh,vm-lifecycle.py}` is still
the operational basis, not directly runnable as this family: it hardcodes one
case,900s,256MiB output and a stop after that case. Root can adapt only orchestration
and resource declarations after image completion. Neither a14-VM requirement nor
a new general runner is justified by the source reviewed here.

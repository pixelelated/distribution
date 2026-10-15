# Steam VM helper correction — source only

UNRUN derivative of `2026-10-15-steam-metadata-vm-plan`. No preparer, admission,
test, argv generator, VM, fixture or cleanup was executed while preparing this
packet. The two executable changes are confined to `prepare.py` and
`vm-lifecycle.py`; the `.diff` files show their exact predecessor-relative edits.

Owner01, `/workspace/tmp/pix582-metadata-remaining-vm-20261015-01`, failed in
run `20261015T004521Z-34493080`: original command/monitor/runner exits1/0/1,
`vm-result.json` rc1 and `boots: []`. `qemu-args` returned2 because the preparer
bound the frozen image checkout's older VM helper, which has no `--no-network`
option. No Steam metadata or fourteen-case stage ran. The original failure is
copied verbatim under `evidence/`; its owner, media and receipts are unchanged.
The original CLI stderr was captured in memory and discarded by the old
exception handler. This source correction cannot recover those missing bytes;
no replay was used to invent a diagnostic transcript.

The fresh preparer now binds the already qualified host VM helper:

- `/workspace/repos/rocknix.worktrees/m7-offline-vm-567/projects/ROCKNIX/devices/GENERIC_X64/vm/generic-x64-vm`
- Helper SHA256 `5b058ed8a8b11135cd5997e3d925939baff30726033125acf1244863a756318d`
- Adjacent `profile.json` SHA256 `26c420ecb0cc7aae29050554c55f522e62337cf6726619a59337c073f1c65406`
- Reviewed checkout `84faea63d9f83392ff9b6ec30bd98c3585024c9d`; source change
  `6709d7c30b42b4554a3bc3b5f59f0927b0bbaf16` adds explicit no-network runs.

`vm-helper-binding.json` records this host-tool provenance separately from the
unchanged frozen image source `fac608ff89940ce358ea9b8a95e9a08a6fe26568`.
Preparation checks both files before creating the new owner; the lifecycle
rechecks both before media preparation. Both paths are protected retention
inputs. Read-only source copies are retained in `qualified-vm-helper/`.

Source review confirms both `qemu-args` and `run` share `add_qemu_options` and
`qemu_command`. The explicit option rejects an SSH port, emits exactly
`-nic none`, omits netdev/NIC/forwarding arguments and omits advertised SSH data.
The helper reads `profile.json` beside its own file. Existing generated-versus-
actual argument equality,8GiB/4CPU and independent guest loopback-only checks
are unchanged in the Steam lifecycle.

This is supported by existing Dolphin boot evidence, not a new test:
`20261015T004309Z-7bfdcf48` consumed qualified, original VM rc0, no cleanup
errors or remaining host children. Its original config binds the exact helper
and profile above. Generated and actual arguments are equal, contain one
`-nic none` and no network/forwarding arguments. Original PID1967217/start111667850
booted the same fac608 image; guest boot ID
`707a0a02-c3ff-418d-bb3b-f2fc6d3e38b7` reported only `lo` and boot command0.
The raw config, generated/actual argv, boot stdout/exit, VM result, host-exit
receipt and consumed admission are retained under `evidence/` with source hashes.

The lifecycle's existing outer exception handler now records
`command_failure.argv`, `original_returncode`, captured `stdout` and `stderr`
for `CalledProcessError`, alongside the unchanged error representation and
failed rc. Null means the command did not capture that stream. The failing
`qemu-args` call already uses `capture_output=True,text=True`, so later CLI
diagnostics survive in the original failure result. No command is repeated,
no exit is reinterpreted, and no generic runner or recovery path was added.

All metadata helper, candidate/frozen installer, original guest-stage, exporter
and remaining31-file packet bytes are unchanged. In particular:

| Input | SHA256 |
| --- | --- |
| Exact metadata helper | `68f298d4d23994ca9aebbab284dda2f8961b6c6d5569e2bee4f7574b78fe8355` |
| Candidate installer, metadata source only | `cefb22a50db915be1637e682dfba047789b276144bbe707220a2b4117c7a3264` |
| Frozen installer used by14 | `fab7cdb4ad8adbcea147be54092bb7ce2005010447be4ab8192c94d8bbe9229d` |
| Original guest-stage | `2f8896c92621a7e7f6079abe5a4d8332e0846e088baa04c6503d1f6fa3a51dad` |
| Remaining source manifest | `79dc1d57d8741b644e99cd8348c4c362fbef3a1c815c48f6fa23b84a6e201c34` |

The strict four-request list,110+10s metadata helper,150s serial envelope,
3600s family deadline,90s reserve,14 original cases, restoration, export limits
and failure-preservation rules remain as described in `predecessor-README.md`.
Can this be done on the VM? Yes: the existing no-NIC guest exercises installed
curl/Bash and private source-chroot cases. No installed Steam/native ARM64/FEX
acceptance is claimed. The original host listener FAIL also stays failed.

After coordinator review, fresh preparation can use:

```sh
TASK_STEAM_PACKET=/workspace/repos/rocknix.worktrees/m7-player-setup/docs/qa-logs/2026-10-15-steam-vm-helper-correction
TASK_STEAM_CHECKOUT=/workspace/repos/rocknix.worktrees/m7-p5-build-20261014-02
TASK_STEAM_OWNER=/workspace/tmp/pix582-metadata-remaining-vm-20261015-02
python3 -I -S -B "$TASK_STEAM_PACKET/prepare.py" \
  --checkout "$TASK_STEAM_CHECKOUT" \
  --image-verification /workspace/tmp/pix-m7-image-readback-20261014-02/artifacts \
  --owner "$TASK_STEAM_OWNER" --vnc 132
```

This command is not executed here. The new owner must not exist and the endpoint
must remain available. Use the existing serialized watched retention/admission,
lifecycle, stopped-media export and original-result consumption sequence. Do
not reuse owner01 or its failed admission. The coordinator owns its preservation
and consumption. `static-review.json` records AST-only and byte/provenance
checks; `source-packet.tar.gz` preserves the new sealed source packet.

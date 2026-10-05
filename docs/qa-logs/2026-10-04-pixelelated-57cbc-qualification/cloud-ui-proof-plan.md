# Remaining cloud UI proof on replacement06

Recorded 2026-10-05 during guest06, for #356, #365 and #383.
Can this be done on the VM? **Yes.** Use a fresh disposable VM disk from the
qualified image, the isolated synthetic backend, and installed ES/scripts.

The frozen candidate is `57cbc9b981205328444d41f6c4237dc9f5736d7f`, bundle
`d4007387afd5ac42104a53a3073b93fdadd33c51179bf9f3142101609f821ec9`.
This is a plan, not executed evidence or a product-defect finding.

Two acceptance criteria are wider than the promoted script cases:

- #365 T17: `tools/vm-walks/cloud-epic/migration-protocol.sh` invokes
  `cloud_setup --seed-folders`, faults settlement, checks unchanged cloud bytes
  and pointers, removes the fault and checks recovery. It does not drive the
  wizard through a refused folder scan, dismiss the failure, reach CLOUD SETUP
  COMPLETE, then reboot and recover through the setup step.
- #356 unsupported layouts: T26 invokes apply/follow/settle/seed/scan for
  malformed, future and trailing marker values and checks refusal plus unchanged
  bytes/pointers. It does not capture the installed interface's outcome page.

After guest06 → runtime06 → proxy05 → optins05 → memory05 → ui06 →
predecessor03 → subset02, run a separately sealed and watched cloud-UI owner:

1. Preserve exact candidate/source hashes and isolated backend ownership.
2. Drive the existing repair-connection wizard with a selected provider
   operation fault. Prove the fault fires; capture its outcome; continue to
   CLOUD SETUP COMPLETE; assert no old-root README, marker or pointer writes
   and unchanged sentinel bytes. Remove the fault, reboot, capture the boot
   step and complete recovery, checking final bytes and pointers.
3. For malformed and future markers, open the existing folder scan through
   the interface. Capture the refusal at 640×480, compare cloud hashes and
   configuration before/after, and retain the installed script outcome.
4. Review the actual frames, reconcile terminal results and host cleanup,
   then update the owning criteria. A capture exit code alone is insufficient.

Do not change the active guest06 harness, frozen source or previously executed
owners. The existing script cases remain useful scoped evidence. Ordinary RA
proof and the approved P4 fixes review remain later gates.

Prepared, not started: `/workspace/tmp/pixelelated-m7-cloud-ui-01`. Its eight
harness inputs are sealed in `harness.sha256`; shell/Python parsing passes.
`run.sh` requires subset02 success and uses the same verified candidate.
The wizard route is the retained case-L route; its source/hash is recorded in
`provenance.json`. Only the layout discovery call is faulted so the real
connectivity gate can pass. The actual fault must be observed before its
result counts.

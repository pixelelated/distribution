# Fresh-context handoff proof: RC2 and Pixman

Session-stash required a reader with no conversation context. Agent
`/root/m7_rc2_pixman_handoff` read the repository/checkpoint and performed
a read-only scoped verification before normal publication. No substantive
contradiction was found.

- Verified698 retained artifacts across seven owners, all seven build-log
  hashes, launcher results and four terminal channels each. Diagnostic10
  and fullsignin12 correctly remain failed.
- Independently decoded all36 comparison frames: RC2 software differs at0;
  accelerated RC2 and Pixman match native throughout; GLES2 differs at0/5
  and matches at15.
- Verified identical normalized QEMU arguments and page/capture code for14/15.
  Actual logs establish Pixman/dumb versus GLES2/GBM, both atomic DRM.
- Verified full13's page assertions, stable helper, reference and Pixman setup
  match full12 byte-for-byte; observer matches the retained new helper.
  All six actual full13 frames reviewed; exact finishing match,354 observer
  frames, clean stop and no recorded error.
- Inspected the nine retained loopback-control results and their source;
  did not rerun them. Six original RC2 records match retained/original hashes
  and substantiate accelerated virgl and the missing browser comparison.
- Escalated actual host `/proc` check at18:45:30UTC found all28 recorded
  owner/guest PIDs absent and no QEMU process.
- Publisher existed and its receipt was absent at inspection, correctly
  indicating publication pending. This proof does not itself prove a push.

Correct next action: narrowly scoped GENERIC_X64 software fallback,
clean/upgrade selection and regression evidence, then qualification of any
new product bytes. Runtime Pixman success is neither a permanent fix nor
RC/P4 acceptance. Exact historical-host behavior and the defective component
remain unknown.

Scope excludes a whole-project audit, re-running controls, new VMs, GitHub
mutations and credential inspection. Product/source custody was checked by
the parent runners before/after their tests; this reader did not claim a new
independent whole-source/candidate rehash.

# Fresh-context handoff proof — #383/#368

Read-only agent `/root/pixelelated_failed_qa_resume` started with only the
repository locations and the request to resume from canonical instructions.
Its initial review completed around 07:50 UTC on October 4.

The agent recovered M7.P3's correct sequence: corrected #410 installation and
host proof, replacement image containing #414, renewed qualification, remaining
P3 checks, then P4. It did not mistake historical replacement02 evidence for
qualification of b137 or propose bypassing an earlier failed stage.

Direct observations:

- Feature rules match `next`; frozen b137 retains only its generated emulator
  documentation modification.
- Actual qualification inner, outer and shared-run result files each contain
  1. All 15 original suite-log hashes match `completion.json`; the retained
  failed report is byte-identical to the original.
- The report records 13 PASS and scripts/frame-diff FAIL. The launcher stops
  before payload readbacks or RC2 upgrade on that failure. Link, guest and
  runtime owners have no start/result markers.
- The retained comparison has 78 screens, 21 claimed changed regions, zero
  unclaimed/missing, and four failing negative controls.
- All four corrected bootstrap checksums match. The old policy/helper exist;
  the corrected policy is absent and swap is nearly full.
- Live #415 is closed with all criteria checked; #414 remains open.

Two tracker defects were found: #410's introductory paragraphs still described
the build as running, and #414's last paragraph described unfinished visual
walks. Both bodies were corrected and independently read back at 07:51:08/09
UTC. They now name the completed build, failed qualification, unrun upgrade,
and corrected host installation before the replacement build. The milestone's
P3 table had the same stale running status; the primary agent corrected it and
read back M7/#383/#409 at 07:49. Historical build records remain intact.

The same agent's focused retest read the exact corrected #410/#414 GET
snapshots and confirmed both findings resolved. Both retain the installation
and host proof → preflight → replacement build → qualification sequence.

Limits: this was a resume proof, not a product audit or test rerun. No builds,
VMs, helper executions or state changes were made by the review agent. It did
not rehash multi-GB candidates or establish actual host root ownership/process
absence; those rely on separately retained primary-agent host observations.
Some later GitHub calls failed to connect, so the primary's milestone GET is
separate evidence. No disconnected notifier is configured.

The #415 implementation/evidence delivery is feature
ac1414fc0371f40cc1dcf67586b9a9fca02382bf, integrated into next
c027c24e2aae87000577f3ae5ab05e454208490c; both published refs were read back.
The original failed qualification is unchanged, and no replacement image
exists. No build or QA process remains.

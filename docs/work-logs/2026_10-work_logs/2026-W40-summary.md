# Week 2026-W40 (September 28–October 4): From ROCKNIX RC2 to pixelelated qualification

Written October 7 from the September 28–30 and October 1–4 daily logs,
the work-log index, and the linked proof records. This is the historical week;
the October 5–7 audit and candidate16 work belong to W41. Refs #254, #383.

## What landed

- The September28 audit repair integrated the source streams with independently
  rerun failure controls. Its merged harness reported1215 PASS; the subsequent
  size-only remote correction#315 reported1232 PASS and nine expected old-source
  failures. The dated logs retain the distinction between source and installed proof.
- ROCKNIX RC1 and RC2 were built for the supported device families. RC2's
  `69e6039f8f` became the preserved upgrade baseline. The September29 log records
  actual device updates and also the first x64 run's two failing suites; later
  reruns, rather than the initial run, supplied their passing evidence.
- The fork established its own organization and release contract#344, initially
  under Rasteratops. Blitterbot's account migration completed with verified
  signed attribution and an authorized push on October2. The October4 change#409
  adopted lowercase **pixelelated**, `/pixelelated`, and Tiny5 Duo LCD Ocean assets.
  The required adoption path remains ROCKNIX→pixelelated.
- The cloud epic added discovery, versioned moves, inherited-state recovery,
  and settings locking. The first independent readiness audit#375/#382 found
  gaps that became explicit remediation and installed acceptance work.
- #310 separated Mesa address-space retention, SDL mode allocations, and ES
  udev lifetimes. Source and VM controls passed unchanged memory limits; #332
  verified LED reselection with actual guest scripts and fixture sysfs.
- #394 made the shared build watcher the default at native and Docker
  entrypoints. #395 proved runner death and monitor-loss detection. Active-session
  result delivery was demonstrated; disconnected notifications remained unfinished.
- #410's installed fixed-action helper passed real guarded swap reclamation
  and refusal controls. Build inputs, immutable bundles, isolated cache copies,
  and actual RC2 upgrade evidence became part of the repeated qualification route.

## What was hard

The upstream PR series was closed on September29 for reviewability and submission
policy problems. The response was a guarded single-commit series and clearer
descriptions; no automatic resubmission was authorized. The browser test had also
accepted a page that failed in a real browser, prompting a realistic negative
control (blindspots69/70).

Early cloud proofs confused fixture defects with product behavior: a missing
configuration invalidated a timing comparison, a recovery race fixture failed,
and stale identity assumptions broke walks. Later source fixes addressed actual
private-settings and installed identity defects. Failed runs stayed in the record;
passing host tests did not close image-only criteria.

Build monitoring initially missed real package activity and did not notify chat
when a command finished. Swap exhaustion and sudo policy ordering complicated
build readiness. The resulting watcher and fixed helper have executable guards;
neither a status file nor an installed checksum alone proves operational success.

## Process and decisions

D-WORKFLOW-132 requires issue ownership for all work. D-WORKFLOW-133 establishes
the canonical resume on `next`; fresh-context exercises exposed stale rules and
missing handoff details. D-WORKFLOW-137 separates local, independent cross-lab,
and extended code audits from the five-seat council. D-WORKFLOW-139 makes the
milestone body the ordered queue and M/P prefixes the naming convention.
D-WORKFLOW-142 records automatic build monitoring; D-WORKFLOW-144 records the
lowercase project identity. These were changes made during the week, not new
instruction edits by the current audit.

## State at the end of the week

At October4 23:44, replacement06 default/RC2-upgrade/content/settings evidence
was published, #424/#428 were closed with exact identity receipts, and the
WebDAV link06 matrix had passed. S3 qualification was still running. P4 review,
remaining installed coverage, device builds, and publication were not complete.
The next week's work must consume those results and keep failed historical
evidence distinct from the current candidate. No pixelelated RC designation
was established by this week's engineering builds.

Sources: [September28](../2026_09-work_logs/2026_09_28-work_log.md),
[September29](../2026_09-work_logs/2026_09_29-work_log.md),
[September30](../2026_09-work_logs/2026_09_30-work_log.md),
[October1](2026_10_01-work_log.md), [October2](2026_10_02-work_log.md),
[October3](2026_10_03-work_log.md), [October4](2026_10_04-work_log.md).

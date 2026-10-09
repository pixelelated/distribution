# Mini-retro: #519 owner-alignment preparation

**Completed:** 2026-10-09. **Scope:** prepared operational plan, old-source
runtime/power qualification and exact executor qualification in commits
79d10bc140a984d08fcd937080cb83342e68a3e5 and
dc9e19b3e2 (primary ce30db6cb and e06b9003b9). The owner-device action and
acceptance remain open; this is not an M7 or #519 completion declaration.
The UTC date rollover and new active work-log day triggered the normal
five-day-plus-two-grace cadence. The October2 cloud-runs retro and its October5
guard-delivery receipt are the available prior phase retro for this milestone.

## What worked well

- The old installed firmware was reproduced on a disposable VM. Exact source
  checks,19 runtime controls, six follow-ups and actual power-boundary evidence
  found the unsafe mask-only assumption before any owner-device changes.
- Retained failures distinguish a disproved operational assumption, a missing
  unsynchronized QA file and a corrected continuation of the same boot. None
  was converted into a historical success.
- The exact executable subsequently passed six controls, including refusing
  stale apply bindings and intervening edits before rollback. Staging separately
  verified hashes/private modes and refused an occupied destination.
- Each watcher result was consumed, actual host exit verified, and guest/key
  retired. Compact source/receipt evidence survives; no historical VM is held.

## What was harder than expected

- Systemd masks are not durable isolation when a boot script unmasks essway.
  The temporary negative path condition needed actual power/recovery proof.
- The executor's first launch used an unsupported watcher option. Existing
  argparse refusal worked before workload execution; no new launch framework
  was needed. The correct invocation and rejected result are retained.
- The negative boot test modified its own baseline through a shared dictionary.
  Another check assumed systemctl could print Conditions, but this firmware
  reports that property as unprintable. Exact loaded unit text is the usable
  evidence. Both failures stopped before configuration alignment.
- A three-second fixture restart was not reliably idle. The procedure refused
  correctly, and the fixture now waits for observed readiness before binding.

## Discoveries that affect remaining issues

- An alignment recovery must bind the failure state as well as the initial
  state. The final executor refuses changed source, boot, payload or configuration
  before restoration; it never uses rollback to overwrite an intervening edit.
- Restoring original automatic-sync1 settings does not justify restarting the
  old frontend. Rollback keeps the maintenance gate; successful alignment removes
  it only after auto0, fallbacks, stale-record archival and protected hashes verify.
- Different inventory counts reflected scope: the broader installed filter
  adds one local backup archive. All162 earlier save hashes are unchanged.
  Filenames and manifests remain private, with a sanitized scope receipt.
- #519 preparation is complete, but owner acceptance is not. #528 publication
  source/licence/backup work remains independent; neither substitutes for the
  other, and neither calls the images a release candidate.

## Adjustments to remaining issues

- #519 now checks only its plan and synthetic-proof criteria. Its exact private
  execution04 packet, required approval, recovery boundary and receipt-bound
  H700 image are the concrete next operational step. The actual device and
  final acceptance criteria remain open in the live body.
- M7's earlier active paragraphs now point to the qualified packet rather than
  asking a new session to prepare or rerun it. Its current #528 queue is intact.
- The VM rule now requires readiness predicates before binding a restarted
  frontend fixture. This extends the existing artifact-over-report principle
  to the recurring fixed-wait setup mistake; no new product behavior is added.
- No further build, achievement reset or external audit is warranted by this
  operational-only delta. A relevant state change invalidates the pending
  device plan and requires readback, not repeating unrelated qualification.

## Scoped audit findings

| Check | Result and evidence |
| --- | --- |
| Acceptance criteria | PASS for preparation; two device/receipt criteria explicitly OPEN in executor/tracking/519-after2.json. No issue closure or full-task completion claim. |
| Project principles | PASS: synthetic VM first, exact installed source, separate owner authorization, private configuration bodies, immutable original failure results; source and receipts in both preupgrade packets. |
| Shared-state interactions | PASS within tested scope: cached ES settings, boot unmasker, live/fallback configuration, transfer lease, detached synthetic worker, stale records and interruption guard exercised. Power-cut coverage is one durable boundary, not arbitrary storage corruption. |
| Futro comparison | SKIP ratio: no separate #519 futro prediction list exists. The issue's explicit risks (old automatic consumers, stale records, interruption, protected saves) all have retained controls; no invented calibration percentage. |
| Housekeeping | PASS scoped checks: final executor six controls, staging checks,191-file packet seal, Python syntax, rules/register/work-log checks. This repository has no general unit suite. No new full-image VM run is claimed; unchanged firmware retains its previously qualified image evidence. Ceremony gate triggered this retro after the new active day. |
| UI review | SKIP: no product UI/source/copy changed. Actual frontend lifecycle was exercised; prior exact-source interface frames remain unchanged. |
| Harness self-coverage | PASS: held lease, stale apply binding, real partial mutation, exact rollback, intervening-edit refusal and actual guarded restart. Failed setup cases retain nonzero results; readiness now uses observed state. |
| Documentation | PASS: private reviewable packet, source rationale, public evidence, complete live issue/milestone bodies and canonical checkpoint reconciled. No new product noun or glossary entry. |
| Build-versus-adopt | SKIP product architecture: one-time owner operation under #519/D-CLOUD-182, using installed writers/systemd/existing device-act and watcher; no product migration system introduced. |
| Decision propagation | PASS: D-CLOUD-175/182 retain normal new-remote setup and separate owner alignment; no settled migration choice reopened. Update transfer/reboot/first sync remain separately authorized. |

## Practice adjustments

The October2 retro already identified state leaking across fixture cases and
worker completion being weaker than visible readiness. The new VM-rule paragraph
and exact observed-idle fixture guard make that lesson concrete here. The
existing watcher rejects invalid flags; retain its exact invocation instead of
inventing another wrapper. No change to council routing or the code-auditor
skill is implied by this bounded operational review.

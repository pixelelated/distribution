# Replacement10 default suites and actual ROCKNIX RC2 upgrade

QA14 completed2026-10-05 20:06:08UTC with all four result channels0.
Actual2a3cd7 cleanup20:06:47 proves owner/recorded guest absence; supplemental
receipt adds the directly restarted virgl guest. All4owner and6guest PIDs
are absent, no QEMU remains. Original exact source and bundle verified.

All15default suites PASS, including16walks and frame comparison:21expected
regions,0unclaimed,0missing screens. The separate actualRC2 upgrade passes
all26checks: saves/state bytes, settings, remote choices, backup, quirk
migration and owner files remain correct. Installed renderer proof passes
clean virgl, upgraded virgl and upgraded software (automatic Pixman).
All15actual identity/manual-update frames directly reviewed; per-phase
hashes and observations retained. The640px message wraps its long URL but
retains the complete address and instructions.

Timing smoke passes (single samples); its rapid game-to-game sample has no
new sync stamp and is not evidence of active-sync behavior. See timing-review.
GPU screenshot spans the panel height with aspect-correct sidebars, as
surface_check's existing#291 contract requires. No threshold or assertion
was relaxed. Exact software boot/browser/memory/UI/1GiB regressions follow.
This is scoped qualification, not an RC designation. Refs#447,#383.

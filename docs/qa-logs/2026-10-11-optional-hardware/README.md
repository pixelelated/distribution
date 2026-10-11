# Optional hardware readings — #548

The original installed information script on replacement19 returns127 and emits
arithmetic/sysfs errors when frequency and temperature interfaces are absent.
At640x480 the CPU rows show a bare MHz. This is inherited: #530 retained the
same original result before the identity edit.

The correction validates optional numbers before arithmetic, keeps measured
zero distinct from absence, reports missing CPU frequency as Not Available,
and omits unavailable GPU/temperature readings. Valid x86 and ARM frequency,
cluster and averaged-temperature outputs match the original. Optional quirks
skip absent/nonexecutable entries; a real executed quirk failure remains nonzero
even when a later quirk succeeds. No persistent settings or data format changes.

The reusable tools/rocknix-info-test runs12 positive/negative controls in CI;
with the original baseline it runs13, including the actual failing control.
Full-script filesystem fixtures cover missing, empty, malformed, expression,
overflow, leading-zero and measured-zero readings, valid x86/ARM hardware,
invalid temperatures and quirk success/failure. Original stdout/stderr/status
and exact source digest remain under host/.

VM02 runs the actual original and corrected script on the unchanged candidate,
using a temporary bind mount of rocknix-info only. Original127/errors become
corrected0/empty stderr. Three reviewed640x480 frames and hashes are indexed.
The owner removes the overlay, verifies original file bytes and stops its VM.
VM01's early serial command failed before any script proof; its original result
is preserved. VM02 uses explicit serial readiness, with the normal QA public-key
bootstrap recorded separately. No personal device or cloud is used.

## Focused local review

This is a narrow primary review, not a new independent code-auditor or council
claim. Input validation prevents Bash arithmetic from interpreting sensor text
as expressions or oversized numbers. Decimal prefixes keep leading zeros from
becoming octal. Temperature averaging requires at least one numeric reading.
Unreadable/disappearing optional files emit no fabricated reading. Executable
quirks retain their original invocation and stderr behavior while propagating
actual failures. Positive output comparisons retain real CPU/GPU conversions;
script syntax, full-script controls and actual guest outcomes pass.

The assembled-image criterion remains open: the next GENERIC_X64 must include
these bytes and pass installed/clean/retained proof before H700 then SM8550.
The source-overlay packet does not relabel replacement19 as corrected firmware.

Raw text with native trailing spaces or terminal carriage returns is retained
in UTF-8 raw_text JSON envelopes with its original byte SHA256; no bytes are
trimmed to satisfy whitespace checks.

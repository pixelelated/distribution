# Completed audit cadence (#489)

The old detector ignored the underscore-date phased audit and counted every
closure since October 4. `live-before.log` reproduces 95 closures/overdue with
exit 1. The corrected detector validates the completion marker, exact SHA256
bound analysis/outcomes, checked closed issue readback and verified completion
time, then runs the actual resolution linter. Invalid evidence remains a CI
failure. Existing legacy markers and the 12-closure/14-day policy remain.

`controls.json` records 15 isolated receipt/time-boundary controls. Those
fixtures test the receipt validator; `live-after.log` additionally exercises
real resolution lint and GitHub. It names #471 at 02:53:02 UTC, zero later
closures, and nothing overdue, exit 0. No external review was repeated.

The completion marker is in
`docs/audits/2026_10_06-milestone-m7-p4-fixes-383/audit-completion.json`.
Its evidence must be reverified if any bound artifact changes. The marker
records the actual verified tracker completion, not this tool fix's date.

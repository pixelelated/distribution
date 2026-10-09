# Exact #519 owner-operation qualification

This packet qualifies the exact proposed one-time local apply/rollback
executable, following the completed runtime and power rehearsal in
`../2026-10-08-preupgrade-runtime/`. It does not add a product migration flow.
The user's handheld has not been changed and #519 is not accepted yet.

The source-bound private plan will disable startup/game-exit automatic sync,
align only the agreed save/settings/keep keys with the owner's restored cloud,
refresh both active fallbacks, and archive the identified stale migration and
scan records. Credentials, content selection, saves and recovery versions stay
unchanged. Original configuration bytes stay in a private on-device archive.

Temporary systemd conditions protect interruption before configuration edits.
Successful completion removes them and restores the prior frontend state with
automation off. Failure keeps the frontend gated. The rollback command restores
exact original configuration/record bytes and modes while retaining that gate;
it does not restart original automatic-sync settings. A reboot or unexplained
state drift requires renewed inspection, not automatic acceptance.

## Scope and evidence

The exact executor runs in a fresh replacement16 GENERIC_X64 guest, using an
invented local alias and invented payloads. No private plan, configuration,
payload, cloud credentials or personal file inventory is copied to the guest
or this public packet. IPv4/IPv6 default-route blackholes constrain the guest.
Completed runtime/power tests are not repeated by this executor qualification.

The private read-only inventory is a superset of the earlier save-only check:
all162 prior payload hashes remain equal; one17,323,751-byte local backup
archive accounts for the broader filter's163files. No missing/new save is
inferred from the different scope. The backup remains protected and unchanged.

Executor01 refused before any workload ran because the launch used an
unsupported watcher option. Its original runner/wrapper result remains2;
there is no invented inner result or guest run. Executor02 used the documented watcher invocation but its negative test
accidentally changed the saved boot baseline through a shared dictionary.
Executor03 exposed systemctl's unprintable Conditions property; the corrected
check verifies loaded DropInPaths and exact unit text. Executor04 passed
interruption/rollback but correctly refused its second application while its
fixture's frontend was not idle. Those original aggregate results remain1.
The fixture now waits for actual readiness rather than trusting a fixed sleep.

Executor05 passed five controls. Final executor06 adds failure-state/boot/source/
payload binding before rollback and passes six controls:

- held transfer lease refuses before any maintenance edit;
- stale binding refuses before any maintenance edit;
- rollback refuses an intervening configuration edit and preserves it;
- injected interruption rolls back exact original bytes/modes under the gate;
- successful alignment restores the frontend and removes temporary gates;
- private archives, existing live permissions and unrelated duplicate settings
  are preserved.

The final executor SHA256 is
`4e286b7906d47ef752761442ed294960f6d7ef5b3417f8925f1249024ce676a1`.
Its host binding/dispatcher remains private. The identical staging template
also passed hash/0600 mode checks and occupied-destination refusal using a
synthetic plan. No owner plan or payload entered that guest.

All five original final result channels are0; actual host owners exited.
Every created guest/disk/firmware-variable copy/QA key has been retired after
capture; final ports10252/5972 are free. Nothing is running in the background.
The earlier runtime power proof is unchanged and does not claim every possible
storage interruption. There was no new physical-device or cloud action.

The exact packet is ready for named owner authorization. Its rollback keeps
the frontend stopped; a reboot, missing failure record or intervening drift
requires renewed inspection. #519 remains open until actual device acceptance.
No update transfer, reboot, first sync or automatic-sync reenable is included.

The preceding runtime checkpoint was published as
`ce30db6cb3c1373ea487a93ddacc18685da9f30a`; hosted record37860806534 and
wordlist37860806522 both completed successfully. The wordlist result was
consumed after its23:48:23UTC completion.

# Current-boot storage readiness — #546

The original19b actual upgrade reached a0f60255ab, but its early save hash read
preceded the boot-specific autostart wait. The read found no files; its later
inventory after that wait lists all four seeded files. Presence and byte equality
are distinct; the original remains FAIL. The readiness wait already existed for
quirk checks but was below the save checks.

The shared rehearsal now requires matching boot identity plus active autostart
before old-image seeding and before new-image retained-state reads. No answer,
wrong boot, or failed unit cannot permit the checks to continue. Five controls
run the actual wait function with ready, stale-boot, failed, delayed and absent
responses; delays are stubbed in the controls. A real image18→19 rerun is active
under upgrade19c, with the changed harness separately sealed from firmware inputs.
Its hashes and installed results are not inferred from the fixture controls.

The fresh real upgrade completed0 at18:41:13UTC after both current-boot waits.
All four save hashes match; settings, selected cloud/path, backup, owner file and
RetroArch choice checks pass. Exact installed payload checks also pass. The owner
is continuing independent retained/protocol/installed tests; this does not claim
a final batch result. Original19b remains1.

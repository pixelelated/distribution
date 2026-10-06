# Installed audit resolution evidence

## PL-008 — Resolved on candidate15

Verified 2026-10-06 20:57 UTC. The reader repair landed in distribution
`ed5a6a51f5974deec8748fbf0dbd2f4984b690f5`; command receipt
[evidence/remediation-host/pl008-resolution-commands.json](evidence/remediation-host/pl008-resolution-commands.json)
re-derives integration on `next` and the actual source-path commit.

Eight installed state/full-scan cases pass in
[reader-values04](../../qa-logs/2026-10-06-pixelelated-replacement-15/p4-reader-values-04/).
The five supported forms assert the exact decoded BACKUPS value and selected
archive/source, including a newer wrong-directory distractor and first-assignment
semantics for duplicate keys. The escaped dollar selects `/Custom/My$Backups`.
The exported, trailing-syntax and control-character forms return the exact
unreadable-settings reason before any provider operation. The observer's real
remote `lsf` control is recorded before resetting it; local `listremotes` is
permitted. Cloud bytes, configuration bytes and installed script hashes stay
unchanged.

The actual predecessor scanner from `7afa9efcfc0c1ce4b89774b38878fc1b9a9063d2`
(SHA256 `29dd9da8a9dafa3433013c2b433a40d0c10b7fb0435e6f281000f3465077502f`)
runs in a private QA path on the same guest. It reaches SETTINGS BACKUPS and
refuses the valid escaped value with the expected settings-read reason; it
leaves no settings cache. The installed corrected scanner immediately selects
the correct archive. This is an old-source control, not an old installed image.
See `proof/artifacts/old-reader-negative-control.json` and command logs0054–0059.

Primary verification: all four result channels0,212 input seals unchanged,
all four owner processes and both guests absent, backend absent and five ports
free. Completion20:57:05; primary owner/cleanup verification20:57:20.

Already written: valid escaped settings remain valid and unchanged; no rewritten
configuration or cloud migration is required. Unsupported syntax is refused
without executing it or selecting a fallback cloud directory. Existing duplicate
assignments retain first-assignment behavior.

The original installed85 run remains FAILED (82PASS/3FAIL): its malformed-input
observer faulted local listremotes before the parser. Corrected reader02 passes
8cases; reader03 failed before guest creation because its new wrapper lacked an
executable dispatch. Exact-value/control owner04 supplies the final acceptance.
All these receipts remain retained. The whole audit stays open for PL-001–007.

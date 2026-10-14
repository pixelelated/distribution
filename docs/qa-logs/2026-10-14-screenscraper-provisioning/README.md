# ScreenScraper interim provisioning — #566

Source candidate under D-WORKFLOW-166. The recipe supplies the shared JELOS
developer login when the build has no explicit override. Existing compiled-pair
precedence hides developer-entry rows; player account rows remain unchanged.
An explicit developer override is preserved for local builds but does not receive
the release-check exception. No personal device/account or provider was accessed.

The selected-state gate permits only the exact NUL-delimited shared developer
pair in the ES ELF. It still blocks different pairs, embedded RA credentials,
personal player accounts and seeded shared developer settings. Added controls
cover those boundaries in clean-image, first-boot and retained-upgrade modes.
The parser fixtures have synthetic ELF headers, not runnable ES binaries.

Can this be done on the VM? Yes. Use an offline disposable GENERIC_X64 guest to
run the complete selected-state root suite and recipe environment-selection
controls, followed later by payload and actual compiled ES/UI qualification.
These tests need no owner data, provider requests or live authentication.

## Qualification status

- Package lint, shell syntax, Python AST and whitespace checks pass.
- VM root/recipe controls: UNRUN at preparation.
- Actual rebuilt ES selection and URL construction: UNRUN.
- Clean/retained installed image, backup exclusion and EN/FR frames: UNRUN.

The canonical flow is in docs/es-menu-map.md. No pin promotion or completed UI
claim is made before the actual binary and source-bound frames are reviewed.
#586 replacement credentials remain separate backlog.

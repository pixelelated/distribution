# Affected installed-image continuation: source review and correction

The initial f665dcd0 packet was never prepared or run. The auditor initially reported it ready after reading the complete derivative and validating its source identities, but missed a package installation transform. Root caught the invalid guard before execution. That readiness judgment is superseded.

The unchanged Dolphin recipe substitutes `@DOLPHIN_BACKEND@`, `@GRENDERER@`, and `@EXPORTS@` in both launchers. GENERIC_X64 selects Wayland and OGL. Requiring the installed launcher hashes to equal their raw source hashes therefore rejects valid artifacts. The helper itself remains byte-identical.

Revision02 seal `668755cb2259e2fa3d3573870ff9cbed1362a0e346b237b551936e01f5eef675` preserves the raw source checks, binds the exact recipe, and compares the installed rows with the same replacement expression as the existing image verifier. The auditor independently verified all 67 payloads, the exact transformation AST, derived hashes and lengths, and unchanged runtime files. No remaining source blocker was found. Actual final verifier, image, inputs, fresh owner, and admission remain required; this is no runtime or installed-image result.

Both complete source packets are retained losslessly with all bytes and modes verified under `supplements/affected-installed-source/`. The original invalid validator and initial historical diff remain intact. The compact auditor receipt records source identities, four original prerequisite evidence identities, exact scopes, and the review miss.

Learning: trace package installation transforms before approving a source-to-installed hash guard. Check raw source identity and installed-byte identity separately, reusing the qualified artifact verifier's transformation. No new framework, product change, or runtime replay follows from this pre-execution correction.

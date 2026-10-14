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
- VM root/recipe controls: PASS,127 root-policy cases and4 recipe selections.
  The same new controls fail against the unchanged gate/recipe as expected.
- Actual rebuilt ES selection and URL construction: UNRUN.
- Clean/retained installed image, backup exclusion and EN/FR frames: UNRUN.

The canonical flow is in docs/es-menu-map.md. No pin promotion or completed UI
claim is made before the actual binary and source-bound frames are reviewed.
#586 replacement credentials remain separate backlog.

## Original results and retirement

Source candidate19221f4762298b10e44a08f2c3e7371c7ddeb0d1 passed the scoped VM
controls at05:22:49 UTC. attempt02 retains all original result channels: candidate
root0, recipe0, expected baseline gate2 and baseline recipe1; launcher/runner/
watcher/lifecycle0. This covers14 added root-policy cases plus the existing113.
The candidate refuses other developer pairs, prefix/suffix/query lookalikes,
missing NUL termination, shared-plus-private/RA combinations, seeded shared
settings and player accounts. Exact shared compiled identity is allowed in all
three modes. No private values are printed. Read-only state snapshots are equal.

attempt01 remains FAIL1: the generated reporting Python contained an unescaped
newline. The failure cleanup stopped the guest before flushing its mounted
output, so no root/recipe success is accepted from it. attempt02 validates both
shell and embedded Python syntax before launch and adds a finally sync/unmount
attempt before stopping QEMU. Its successful normal unmount is recorded; the new
failure-cleanup branch itself has not been fault-injection tested.

Both admissions are consumed, all recorded host/QEMU owners exited, and both
sets of disks/media/UEFI are absent:2,275,958,784 bytes retired after attempt01
and2,278,850,560 after attempt02. Compact records remain. No runtime is active.
The header-shaped ELF parser inputs do not qualify actual compiled ES or provider
authentication; the remaining image/UI/backup gates above still apply.

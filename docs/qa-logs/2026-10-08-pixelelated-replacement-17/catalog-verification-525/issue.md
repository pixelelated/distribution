The replacement17 build completed643/643 tasks and generated its engineering disk/update artifacts, but the post-build verifier opened `image/system/usr/share/locale/fr/LC_MESSAGES/emulationstation2.mo`. The package deliberately makes `usr/share/locale` an absolute link into `/storage/.config/locale`; staged catalogs actually live in `usr/config/locale`. Host Path.open follows the guest absolute link on the host and raised FileNotFoundError. The original inner/outer/wrapper/watcher outcomes are1 and stay unchanged.

Package source confirms the installation and links. A diagnostic read of the actual staged catalog passes all11 new French messages. No product or package fault is currently demonstrated. The prewritten CF10 guest verifier has the same host-side expectation and must be corrected before use.

Fix only verification: use the staged source path for host inspection and independently verify runtime alias/catalog equality in the guest. Repeat the complete assembled assertions under a fresh watched owner; bind existing artifact hashes before/after instead of recompiling unchanged product bytes. Preserve the original build result and explicit corrected-verification lineage.

The build container exited before live inspect was captured. Docker's256-event ring has already rotated into unrelated healthchecks. Keep this limit explicit: the pinned digest is bound by the actual logged Docker invocation and pre/post local image-ID checks; do not invent an observed container ID. Actual host process/container exits still require verification.

Can this be done on the VM? Yes: host checks prove staged bytes and the guest proves `/usr/share/locale` resolves to the same installed catalog, with new translations. No physical device or personal cloud is involved.

## Acceptance criteria

- [ ] Original failed watcher/launcher/results and source harness are retained unchanged, with terminal host owner exits and the exact path error.
- [ ] Fresh corrected assembled checks pass all original assertions, including all11 French messages; existing firmware hashes and frozen inputs remain unchanged.
- [ ] Fresh image guest proves staged/runtime catalog equality and required messages; prepared verifier uses the correct host path. Retained scripts/results make the host-versus-guest filesystem boundary explicit.

Parent #508; M7.P5 firmware inclusion. No new external audit is required for this fixture-only correction.

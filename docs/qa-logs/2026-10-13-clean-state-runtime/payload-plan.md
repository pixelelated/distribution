### #565 next bounded final-payload reader controls

Can this be done on the VM? The first-boot and synthetic-root policy have been
executed in the disposable OS VM. The additional component under test is the
host release-preparation program and its host filesystem readers; the OS guest
does not ship mcopy, mksquashfs, unsquashfs, sfdisk or debugfs. Execute this host
entrypoint as the normal unprivileged build user against synthetic regular
files in a fresh bounded owner, with no mounts, image build, network request,
owner data or release publication. This is host-tool qualification, not a
substitute for the guest's first-boot/upgrade checks.

After the active first-boot VM is consumed and retired, freeze the corrected
pix-nova commit plus its release helper and dependencies in a new owner. Use
the installed filesystem utilities plus the existing read-only accepted
toolchain mcopy4.0.49 (verified executable; no installation or cache mutation).
Run --payload-tests once with a180second outer bound and1GiB scratch budget.
It creates tiny synthetic SquashFS, update tar, FAT/ext4 install-image files
and release bundles; clean inputs must pass, populated credentials/history,
storage seeds, literal bracketed filenames and malformed/missing readers must
refuse without values in output. Prepared release JSON is not publishing.
Retain actual fixture/launcher/wrapper/watcher exits and byte identities, delete
temporary payloads after the run, and return any failure for source correction.
No real final firmware artifact is asserted clean by these synthetic controls.

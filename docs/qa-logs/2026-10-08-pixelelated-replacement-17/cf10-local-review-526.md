# Bounded implementation review — #526

Scope: the melonDS tail of post-update, its focused regression and standard
scripts-suite integration. Depth: local implementation review only; no new
independent audit or external transfer ran. Completed #507 remains bound to
its original scope. This does not designate a release candidate.

The source intent in upstream62c343921d is to add new hotkey variables. The
package and launcher use melonDS, while the update hook used melondDS after
unconditional deletion. #258 already noted the path mismatch. Replacement17's
complete installed entrypoint returned1; the explicit old-control VM run also
deleted a synthetic owner's INI and extra file.

Reviewed preservation boundaries:

- Missing optional defaults or configuration is a no-op; existing launcher
  seeding remains responsible for missing files. No foreign directory is copied.
- Only absent HKKey_/HKJoy_ keys are appended. Existing values, unknown keys,
  unrelated settings and extra files stay. Linked files/directories are skipped.
- Preparation keeps file mode with cp -p, uses a unique adjacent temporary and
  commits with one rename. Producer/copy/temp/rename failures retain originals.
- No-addition runs leave the original inode, bytes and mode; no-final-newline
  files gain a separator only when adding keys. The awk program preserves
  actual error status, rather than overriding an I/O error in END.
- The function is run on scratch paths by the durable test and by the standard
  last-good-scripts suite. Frozen old code fails all15 controls. Corrected code
  passes15 on the host with image BusyBox and15 inside the actual VM. The whole
  corrected hook passes twice in that VM while payload/credentials/cloud paths/
  sync choices and immutable installed bytes remain unchanged.

Evidence: [CF10 packet](cf10/README.md),
[actual VM receipt](cf10/melonds526-vm01/result.json),
[host controls](cf10/melonds526-vm01/host-corrected.json),
[old negative controls](cf10/melonds526-vm01/host-old-negative.json).
The source hook ran from /storage; it was not installed into the immutable
replacement17 image. #526 remains open for publication and new-image acceptance.

Residual boundary: already-deleted unknown settings cannot be reconstructed.
This updater runs during setup/update with the frontend stopped; the tests do
not claim protection from an unrelated process editing the same INI concurrently.

# Payload host PATH correction

The original payload owner01 exited2 because its wrapper excluded /usr/sbin and /sbin, hiding sfdisk/e2fsck/debugfs on this host. Update payload passed; install inspection and later source-chain did not complete. Its original receipts are preserved.

This additive wrapper changes only PATH to include those standard administrative binary locations; it executes read-only tools without privilege elevation. Source bindings and all payload checks/deadlines are unchanged. The original sealed plan remains byte-identical. Use this directory for the corrected payload-check.sh; use the original plan for every other procedure. Runtime pending a fresh owner.

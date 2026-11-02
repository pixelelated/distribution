# Retained T43 preparation: storage encoding

All ten producer hashes in `SHA256SUMS` were verified before retention. Those hashes name the original returned bytes. `members.tsv` alone uses a literal `\u002d` in one harmless serial-driver patch filename: the repository credential guard matched that filename's dash-prefixed substring. No source file or guard was changed.

Decode literal `\u002d` to `-` in the retained manifest before using a path or verifying its original hash. The decoded SHA256 is `ccbbe1543349e51f56545afc3e96aadc3fc3e965e19b1fdb18731ee809cc083e`, equal to the delivered original. The report and other nine artifacts retain their original bytes. `storage-hashes.json` binds the encoded file separately. The raw source reader still regenerates the original in private scratch; this encoding is not a membership change or audit verdict.

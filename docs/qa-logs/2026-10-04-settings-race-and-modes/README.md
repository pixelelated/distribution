# Installed settings recovery race and private modes

Refs #320, #420, #421, #383. Can this be done on the VM? Yes: unchanged
installed ES and real shell writers, disposable COWs over the actual RC2
upgrade disk. Hash checks bind all installed consumers and the unchanged
candidate02163. No account or physical device is involved.

settings-01/02/03 actual tools40520/21885/50319 returned1. The first fixture
was a usable non-prefix partial edit; chooseConfig deliberately preserves it,
so no recovery-lock release was reached.03 confirms the probe was actually
mapped into the ES process. Linux's15-byte comm truncation also explained why
02's diagnostic list missed ES. A separate read-only COW inspection completed
with tool27968=0; it is not race evidence.

settings-04 tool60956=1 used a strict truncated prefix of the complete backup.
The first pause proves ES recovered the live bytes and released the lock.
Installed set_setting and chksysconfig publish a newer live file and record;
the same installed ES reaches the second pause and preserves both newer byte
sequences. Its extra0600 assertion failed, exposing the separate #421 shell
writer defect. This run remains failed; no full-pass claim is made. Every
failed run restored exact settings, verified immutable installed hashes,
stopped its owned guest and rehashed the backing disk.

The #421 focused test uses actual lifted functions on scratch paths, with
candidate BusyBox applets. Original02163 fails22/29, corrected source passes
29/29. BusyBox cp reapplies the source mode over a prepared temporary; the
corrected backup/restore copies bytes into the prepared file with cat before
rename. No published file is widened; staged symlinks, failed chmod/stat,
failed producers and failed renames cannot report success.

Full source regression is still running in settings-source-01. Source-state
hashes identify this prepared correction; it is not yet image qualification.
The current product/tree/checkpoint must be read before using these receipts.
All old failures are retained. The future rebuilt candidate must rerun the
installed race and default/actual-upgrade qualification before any RC claim.

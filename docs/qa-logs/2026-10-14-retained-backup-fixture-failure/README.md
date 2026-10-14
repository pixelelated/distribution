# Retained update: backup fixture refusal preserved

The real accepted20 to d6a87f05 update, changed boot ID and selected retained
settings/history checks passed. The backup phase returned1 before invoking the
backup child: its generic key/value parser did not handle the two shell line
continuations in the shipped cloud_sync.conf. No backup result is claimed.

Stopped-disk readback confirms the8232-byte runtime configuration exactly equals
the shipped file (SHA256 a121977066ce805e791108258fe12d1ecbce5e71ce2f61f096394a9fca982305).
Original transport0/guest1, lifecycle/runner/launcher1 and monitor0 remain
unchanged. All owners exited normally, with no cleanup errors. Failed admission
was consumed. Compact original evidence was retained before10,817,536,000 bytes
of disposable VM media were removed. The temporary diagnostic extraction was
also removed. A fresh composed rehearsal requires the reviewed parser correction.

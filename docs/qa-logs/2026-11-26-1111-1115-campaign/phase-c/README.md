# Phase C: updating onto build 12 with connections in place

OS coordinator, 2026-11-26.

- **The tool:** `tools/vm-upgrade-rehearsal` from the round (`4225f5b14f`, tools only past build 12), extended for #1111.
- **When the previous image has connection profiles,** it seeds a second alias connection with its own saves and settings folders, puts the selection back on the QA remote, and after the update checks:
  - the same `cloud_remote list` (connections and selection);
  - `folder-profiles.json` byte for byte;
  - the second connection's own folders, read last of all the upgrade checks.
- **When it has none,** it says so and checks that the old device-wide saves folder now belongs to the one existing connection, with a current projection.
- **Every run** updates in place to build 12's tar (`a069abd236`) and checks the rest of the rehearsal's 30-odd items as before.

| Log | Previous image | Result |
| --- | --- | --- |
| `1533-legacy-without-block.log` | PC `0.0.1` (`m7-pc-43d0bc3b-20261125`) | 32 of 32. This run predates the adoption check: the block skipped silently, which is what showed that this image has no profile module (`unsquashfs -l` of its SYSTEM: no `cloud_connections.py`, no `cloud_connection_profiles.py`). The rehearsal now says when it skips. |
| `1535-legacy-adoption.log` | the same | **33 of 33**, with "the old saves folder adopted by the existing connection (#1111 C02)": the QA connection owns `/Rehearsal/Saves`, and `projection_current` is true. |
| `1537-profiles.log` | the candidate `0a3e979e50`'s PC image (both modules present) | **37 of 37.** The five #1111 checks pass across the update: second connection seeded, selection back, list and selection kept, profiles byte for byte, the second connection's own `/Two/Saves` and `/Two/Backups` kept with the selection put back. |

**What this does not cover:**
- A legacy `bcc866f1`-era device with several saved connections. The adoption check is one connection, as the rehearsal seeds.
- A real provider's re-authentication across the update.

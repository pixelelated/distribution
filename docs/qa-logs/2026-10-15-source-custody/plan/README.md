# #528 source-custody refresh proposal — retained 2026-10-15

**UNRUN source-only proposal. Root review and future allocation remain pending.**
This retains the released `/tmp/pix-m7-source-custody-refresh-20261015`
packet without changing its bytes. It does not establish a current inventory,
source-custody completion, legal clearance or publication-gate completion.

The proposal maps the two historical inventory baselines to frozen distribution
`f8636de1d105275dbf9420bbabbbc26f79abb10f`: 73 changed product paths, four
changed package-version declarations, ten affected input families, and the
17 existing notice rows plus the separately tracked Doom-data disposition.
It contains narrow unrun collector corrections and a five-profile binding
plan. Final device manifests, current input bindings, finite runner/member-index
rebinding and original execution evidence remain required. Historical receipts
and the VM's #597 nonqualified launcher-reporting closeout remain distinct
from independently accepted artifact integrity.

`source-proposal.tar.gz` preserves all **125 original regular files**, including
the original seal, plus 89 directory members. `member-manifest.json` records
every member's bytes/hash, type, permissions, numeric UID/GID, owner/group name
and mtime. `retention-verification.json` records full archive readback, including
the original seal and manifest checked against archived bytes and modes.
`source-SHA256SUMS` is an exact copy of the inner seal; its paths are relative
to the archive's `source-packet/` directory. The outer `SHA256SUMS` covers this
durable retention packet.

Original source seal:
`f345980a2e20c305b770e686b5c6ff4aa915cfae78c8778981bc6a48713a951d`.
Archive SHA256:
`719cc2809abeff8509b2fd1142c073457fed4d59e170f344b5cfb22156aa83f1`.

The original static check exited **0**; stdout/stderr and the candid tool-exit
observation are archived unchanged. Independent peer review was not completed;
root requested handoff without delaying H700. The first retention check exited
1 because source POSIX mode included type bits while tar records type and
permissions separately. The valid archive was kept unchanged, and full readback
verified permissions, type, ownership, bytes and seals separately. That original
failure and the diagnostic observations remain in `retention-observations.json`.

No collector, build, container, VM, source-cache scan, firmware read, network
transfer or tracker operation ran during retention. Originals remain in place.
No product or shared milestone record was edited, staged or committed.

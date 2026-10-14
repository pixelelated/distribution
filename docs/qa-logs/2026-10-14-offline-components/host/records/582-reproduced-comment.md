The bounded no-network GENERIC_X64 reproduction now confirms the partial-client retry defect in unchanged installer `c6240ed3984a` (fixture correction `71e66ba00cd8`).

Can this be done on the VM? Yes: synthetic storage and transport, actual installed BusyBox ZIP decoder, private namespaces, no account or native Steam execution.

The first native decode wrote the initial client member and failed on the intentionally corrupted second CRC (original decoder/function exit 1). A single deliberate retry returned original function exit 0 solely because the partial client directory existed. The executable remained absent, no new acquisition occurred, and unrelated existing state was preserved. Outer reproduction exit 0 means **defect reproduced**, not installer repaired. Duration 10.63 s, 413,534 retained bytes, no guard/intervention or remaining descendants.

The separately seeded valid-existing-client control passed: original function exit 0, no acquisition, identical bytes/modes/inodes/link targets and preserved beta choice; 0.50 s, no descendants. These are selected-function observations, not whole-installer retry or real Valve archive qualification.

Original first fixture failure 1 (incorrect local ZIP CRC offset) and two watcher prerequisite refusals 2 remain preserved; none ran the product probe. Current evidence owner `/workspace/tmp/pix-m7-offline-vm-20261014`, `steam-partial02-host` and `steam-existing01-host`; compact durable export follows VM retirement. Real archive layout/hash and safe existing-client classification remain prerequisites for the transactional repair. #582 remains open and precedes the next candidate build.

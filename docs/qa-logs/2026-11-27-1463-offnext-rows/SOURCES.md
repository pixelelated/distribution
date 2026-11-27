# #1463: decided rows landed on `next` by content, 2026-11-27

Each row is copied verbatim from its source, below. The rows were appended to the Decided table in date order. A read of every M7 worktree register against `next`'s found 39 IDs absent from `next`. 28 land here. 11 wait:

- D-WORKFLOW-175 to 182: each number carries two decisions (#1463 criterion 2).
- D-INFRA-1419: an issue number in the ID position. Landing it would make the ID sweep hand out D-INFRA-1420 next; it needs a clerical renumbering (D-WORKFLOW-013).
- D-UI-129: cites D-WORKFLOW-178, whose number carries two decisions (criterion 2); landing it would leave a dangling cross-reference.
- D-WORKFLOW-208: cites D-WORKFLOW-182, whose number carries two decisions (criterion 2); landing it would leave a dangling cross-reference.

Sources: "candidate line `0282367b4a`" is the first commit on `build/m7-rc-round-20261125` that carries the row (`git log -S`). `m7-player-setup` is that worktree's uncommitted `docs/decision-register.md`, sha256 `ef0e3accdf6e4fb8...`, at HEAD `e70022eb13`.

| ID | Row date | Source |
| --- | --- | --- |
| D-QA-061 | 2026-10-18 | m7-player-setup (uncommitted register) |
| D-WORKFLOW-171 | 2026-10-18 | m7-player-setup (uncommitted register) |
| D-WORKFLOW-172 | 2026-10-19 | candidate line 0282367b4a 2026-11-18 |
| D-RA-049 | 2026-10-20 | m7-player-setup (uncommitted register) |
| D-UI-128 | 2026-10-20 | m7-player-setup (uncommitted register) |
| D-WORKFLOW-173 | 2026-10-20 | candidate line 0282367b4a 2026-11-18 |
| D-WORKFLOW-174 | 2026-10-20 | candidate line 0282367b4a 2026-11-18 |
| D-RA-050 | 2026-10-21 | candidate line 0282367b4a 2026-11-18 |
| D-UI-130 | 2026-10-23 | m7-player-setup (uncommitted register) |
| D-INFRA-029 | 2026-10-24 | candidate line 0282367b4a 2026-11-18 |
| D-UI-131 | 2026-10-24 | m7-player-setup (uncommitted register) |
| D-UI-132 | 2026-10-24 | m7-player-setup (uncommitted register) |
| D-CLOUD-185 | 2026-10-25 | candidate line 0282367b4a 2026-11-18 |
| D-CLOUD-186 | 2026-10-25 | candidate line 0282367b4a 2026-11-18 |
| D-CLOUD-187 | 2026-10-25 | m7-player-setup (uncommitted register) |
| D-UI-133 | 2026-10-25 | m7-player-setup (uncommitted register) |
| D-UI-134 | 2026-10-25 | m7-player-setup (uncommitted register) |
| D-UI-135 | 2026-10-25 | m7-player-setup (uncommitted register) |
| D-UI-136 | 2026-10-25 | m7-player-setup (uncommitted register) |
| D-WORKFLOW-206 | 2026-10-25 | m7-player-setup (uncommitted register) |
| D-WORKFLOW-207 | 2026-10-25 | m7-player-setup (uncommitted register) |
| D-NET-017 | 2026-10-27 | candidate line 0282367b4a 2026-11-18 |
| D-NET-018 | 2026-10-30 | candidate line 0282367b4a 2026-11-18 |
| D-INFRA-026 | 2026-10-31 | candidate line 0282367b4a 2026-11-18 |
| D-QA-064 | 2026-11-05 | candidate line 0282367b4a 2026-11-18 |
| D-ROADMAP-001 | 2026-11-10 | candidate line 0282367b4a 2026-11-18 |
| D-ROADMAP-002 | 2026-11-10 | candidate line 0282367b4a 2026-11-18 |
| D-ROADMAP-003 | 2026-11-10 | candidate line 0282367b4a 2026-11-18 |

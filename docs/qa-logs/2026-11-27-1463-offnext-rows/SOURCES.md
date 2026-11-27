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

**Added 2026-11-27, after the 28:** D-INFRA-048 (2026-11-04), keyed `INFRA-1419` at its source, `build/m7-rc-round-20261125:docs/decision-register.md:767`. The text is verbatim and only the ID cell changed (D-WORKFLOW-013). The rekey is recorded as D-INFRA-049. Criterion 1 stands at 29 of 39. The ten left are D-WORKFLOW-175 to 182 (criterion 2), D-UI-129 and D-WORKFLOW-208.

## Criterion 2 and the rest of criterion 1 (2026-11-27)

The rows are verbatim except where named. A rekeyed row's ID cell changed, and so did each cross-reference that moves with the meaning it cites (D-WORKFLOW-013). The records are D-WORKFLOW-252 and D-INFRA-053. Every citation of D-WORKFLOW-175 to 182 is classified by meaning in `c2-classification.md` (sha256 `17f54037…`).

| On `next` | Date | Was | Source |
| --- | --- | --- | --- |
| D-WORKFLOW-175 to 180 | 2026-10-20 to 22 | same, October meaning | `m7-player-setup` (uncommitted register, sha256 `ef0e3acc…`) |
| D-UI-129 | 2026-10-23 | same | `m7-player-setup` (uncommitted) |
| D-WORKFLOW-246, 247 | 2026-10-24 | October D-WORKFLOW-181, 182; 247's reference to October 181 now reads 246 | `m7-player-setup` (uncommitted) |
| D-WORKFLOW-250, 251 | 2026-10-25 | October D-WORKFLOW-183, 184; 250's references to October 181 and 182 now read 246/247 | `m7-player-setup` (uncommitted) |
| D-WORKFLOW-208 | 2026-10-25 | same; its reference to October 182 now reads 247 | `m7-player-setup` (uncommitted) |
| D-INFRA-050, 051, 052 | 2026-10-21, 23, 25 | October D-INFRA-024, 025, 032; 051's and 052's references to them moved | `m7-player-setup` (uncommitted) |
| D-WORKFLOW-240 to 245 | 2026-11-07 to 11 | November D-WORKFLOW-175 to 180; 241's and 244's references to November 175 and 177 moved | candidate line, committed in `build/m7-rc-round-20261125` |
| D-WORKFLOW-248 | 2026-11-11 | November D-WORKFLOW-181; its reference to November 180 now reads 245 | `feature/m7-owner-feedback-20261025` (committed) |
| D-WORKFLOW-249 | 2026-11-12 | November D-WORKFLOW-182; its references to November 175 and 180 now read 240/245 | `m7-owner-feedback-20261025` (uncommitted register, sha256 `9038f89b…`) |

**Not on `next`, and why:**
- **D-WORKFLOW-181 and 182 in M6's meaning,** dated 2026-10-22, on 48 pushed M6 branches. These are M6's rows (D-INFRA-038). M7 no longer uses those numbers on `next`.
- **M6's D-WORKFLOW-183 and 184,** also dated 2026-10-22. They collide with `next`'s own rows of 2026-11-14 and 15, which keep the numbers. This is put to Max with M6's other rekeys.

**The check:** `offnext-check.py` reads every M7 worktree's register and every M7 ref's register, and looks each row up on `next` by content.

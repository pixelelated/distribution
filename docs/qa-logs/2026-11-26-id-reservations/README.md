# ID reservations for M6's colliding register rows (#1463)

OS coordinator, 2026-11-26. The direction is the one agreed on 2026-11-03: M6 asked to rekey its own rows, and M7 reserved the numbers.

- **M7 keeps its meanings at the collided IDs.** M6 rekeys its rows to the numbers in `reservations.json` when it integrates.
- **No M7 allocation may use a reserved number.** `docs/qa-logs/2026-11-25-m7-bug-triage/register-sweep.py` reads every `*id-reservations*/reservations.json` on every branch and worktree, and counts Open decisions rows.

**What went wrong.** The 2026-11-03 record (`docs/qa-logs/2026-11-03-m6-id-reservations/`) lived only on the candidate line, and the sweep read neither reservations nor open rows. So `next` spent three of its four numbers on other decisions:

| Number | Spent on `next` for | Date |
| --- | --- | --- |
| D-INFRA-033 | another decision | 2026-11-24 |
| D-RA-053 | another decision | 2026-11-26 |
| D-CLOUD-194 | the open renewal question for #1111 C15 | 2026-11-26 |

On 2026-11-25, #1463's plan proposed the reverse (M7 renumbers) without knowing of the agreement. That plan is withdrawn. It would also have meant rewriting 173 M7 citations, 163 of them in retained records (`/workspace/tmp/rocknix-session/1463-classification.md`, 2026-11-26).

**The four agreed rekeys.** D-CLOUD-195 is unchanged. The other three take fresh numbers:

| M6 row | 2026-11-03 number | Now |
| --- | --- | --- |
| D-CLOUD-185 | D-CLOUD-194 | D-CLOUD-196 |
| D-CLOUD-186 | D-CLOUD-195 | D-CLOUD-195 |
| D-INFRA-026 | D-INFRA-033 | D-INFRA-047 |
| D-RA-050 | D-RA-053 | D-RA-055 |

**The other twelve collisions are offered to M6 on the same terms.** M6 can decline any of them, and its reservation is then released:

| M6 row | Reserved |
| --- | --- |
| D-CLOUD-187 | D-CLOUD-197 |
| D-QA-061 | D-QA-067 |
| D-RA-049 | D-RA-056 |
| D-UI-128 to D-UI-136 | D-UI-138 to D-UI-146 |

**What M7 still owes.** Its rows for D-CLOUD-187, D-QA-061, D-RA-049 and D-UI-128 to D-UI-136 are not on `next` or the candidate line. They exist only in the uncommitted `m7-player-setup` register (D-QA-061 also in `b5aad48cbe`). They are landed on `next` by content under their current numbers, which is #1463's first criterion.

# Research notes: M6.P2 T14, the last-good, settings and state tests (#661)

## Scope

- **Read hashes:**
  - `8ebaf8daad` for the 22 tools and fixture;
  - `2174265e9c` (P1's tip) for the ten lint fixtures, which exist only there;
  - `reviewed-at` is `30da4853bb`, the branch at stage A.
- **The filter:** brief § 2's block, run on 2026-10-24 at 20:19 UTC in the lane's worktree:

  ```
  paths 32 lines 6911 {'fork-own': 32} {'n/a': 32} {'python': 20, 'shell': 2, 'markdown': 10}
  the globs also select, in other areas: 0 paths (expect 0)
  ```

  `wc -l < .qa-scratch/t14/paths.txt` prints 32. The per-path count at the read refs totals **6,911** (`.qa-scratch/t14/lines.txt`), with no delta from the brief.
- **Provenance:**
  - **35** fork commits since `c445081a59` over the 22, 35 without merges;
  - **none of the 32** is on `upstream/next`;
  - the ten lint fixtures are on P1 only (absent at `8ebaf8daad`, 10 of 10).
- **The branch against the read hashes, over the 32:** empty against `8ebaf8daad` for the 22, and empty against `2174265e9c` for the ten.
- **T10's #945 delta:** `2444828e89` (*lint-audit-artifacts: bound the seats' index at a heading; the folder date format agreed with ceremony-check*) adds `run.sh` and a third fixture directory beside the two members on `feature/m6-tooling-guards-657`. It is read as a delta, not a member.
- **The exports:** `.qa-scratch/t14/at-hash/` (22 files, 394,711 bytes) and `.qa-scratch/t14/at-p1/` (10 files).

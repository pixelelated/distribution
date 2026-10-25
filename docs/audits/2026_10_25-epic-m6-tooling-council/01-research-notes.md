# Research notes — M6.P2 T45, the council toolchain and runner (#692)

## Scope

- **The read hash:** `8ebaf8daad`. The 52 members are read from its bytes: `git show 8ebaf8daad:<path>`, and the clone `/workspace/tmp/m6-t45/at-hash` checked out at `8ebaf8daad8eaac6331dff6fc048fb4411d7decb`.
- **`reviewed-at`:** `32a34393dd`, the branch `HEAD` and dispatch tip.
- **The membership:** brief § 2's block, run at P1's `2174265e9c` over `docs/reviews/inventory.json`:

  ```text
  paths 52 lines 25848 {'fork-own': 52} {'json': 4, 'typescript': 23, 'javascript': 22, 'text': 1, 'python': 1, 'shell': 1} {'n/a': 52}
  in other areas: 30 {'build-engine': 30}
  ```

  - The 52 are in `stage-a/paths.txt`.
  - The 30 non-members are in `stage-a/others.txt`. They are the build engine's own `scripts/` (T5's slice), caught by the `scripts/**` glob and not read here.
- **The provenance:**
  - **At the hash:** 5 fork commits on the 52 (`git log --oneline 8ebaf8daad -- <the 52> | wc -l` prints 5):

    | Commit | Date | Subject |
    | --- | --- | --- |
    | `b3e5c92559` | 2026-09-05 | import the multi-model deliberation skill and its Facilitator (#70) |
    | `4796a78983` | 2026-09-05 | the whole verification toolchain, pinned beside the scripts |
    | `5f1b343d25` | 2026-09-30 | scaffold's council toolchain `7be6721b`, at its own paths |
    | `4bf31083c7` | 2026-10-02 | keep instructions on the installed five seats (#372) |
    | `a9af618398` | 2026-10-04 | the lowercase identity (D-WORKFLOW-144, #409) |

    None of them is on `upstream/next`.
  - **Beyond the hash:** the branch adds exactly two (`git log --format=%h 8ebaf8daad..HEAD -- <the 52>`):
    - `0ceb2994c5`, 2026-10-22: *council: add explicit Argon audit route and refusal diagnostics* (#638);
    - `033eb7ed23`, 2026-10-22: *council: stop retrying explicitly filtered responses* (#636).

    Together they change `10 files changed, 356 insertions(+), 28 deletions(-)`. Neither is on `next`.
  - **Since the dispatch tip `32a34393dd`:** none.
- **The delivery's record** (`.claude/skills/council/IMPORTED-FROM.md`, `COUNCIL-BUNDLE.md`, `COUNCIL-BUNDLE.SHA256SUMS`):
  - scaffold `main` at `7be6721be24458910e75ca639f318d25ffe7e8d5` (2026-09-30), corpus **4.29.1** plus #976;
  - **94 files**, byte-identical to that commit; the SUMS file has 94 lines and is unchanged on the branch;
  - delivered by the maintainer's agent on marvin;
  - the fork's adaptations are listed in `IMPORTED-FROM.md`, and each adapted pinned file is re-pinned with a `repin_reason` (D-WORKFLOW-089).
- **The bytes at a glance** (stage A; the full rows are `02` § Provenance):
  - at the hash: 50 listed, 41 equal, 9 differ, 2 unlisted;
  - on the branch: 50, 36, 14, 2.
- **No newer export is reachable here.** The scaffold checkout on this host (`20c0a77`, 2026-08-29, corpus 3.29.1) does not hold `7be6721b`.

## Phase 1

To be written at stage B: what each member does, in the slice's words, from the bytes at the hash.

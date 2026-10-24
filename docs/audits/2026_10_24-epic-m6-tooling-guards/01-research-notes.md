# Research notes — M6.P2 T10, the guards (#657)

## Scope

**The read hashes:**
- the 28 at-hash files are read at `next`'s `8ebaf8daad8eaac6331dff6fc048fb4411d7decb`;
- the three `renovation-*` tools are read at P1's `2174265e9c`;
- `reviewed-at` is the lane's `HEAD` at stage A, `a82d784216`.

Each tree is an export (`.qa-scratch/t10/at-hash/`, 28 files; `.qa-scratch/t10/at-p1/`, 13 files, the three tools and the lint's ten fixture files).

**The filter** of brief § 2, run unchanged:

```text
paths 31 lines 6676 {'fork-own': 29, 'upstream-carried': 2} {'n/a': 31} {'shell': 11, 'none': 2, 'yaml': 4, 'python': 14}
tier lines {'upstream-carried': 386, 'fork-own': 6290}
the glob also selects, in other areas: 375 paths
```

So the slice is **31 paths**: 6,676 lines by the inventory's column and **6,642 at the read refs** (`git show <ref>:<path> | wc -l`). It holds 29 fork-own and 2 upstream-carried files, by language 14 Python, 11 shell, 4 YAML and 2 untagged, with reach `n/a` for all 31. There are no deltas from the brief.

The 34 lines between the two totals are the brief's three:
- P1's +3 in `pre-push`;
- P1's +32 in `lint-audit-artifacts`, counted in the inventory's column on P1's tree;
- `renovation-inventory`'s column, 1,596 against its 1,597 at `2174265e9c`.

| Lines at the read ref | Path | Ref |
| ---: | --- | --- |
| 25 | `.githooks/commit-msg` | `8ebaf8daad` |
| 107 | `.githooks/guard-lib` | `8ebaf8daad` |
| 120 | `.githooks/hooks-test` | `8ebaf8daad` |
| 21 | `.githooks/pre-commit` | `8ebaf8daad` |
| 470 | `.githooks/pre-push` | `8ebaf8daad` |
| 8 | `.githooks/secret-patterns` | `8ebaf8daad` |
| 98 | `.github/scripts/generate-changelog.sh` | `8ebaf8daad` |
| 288 | `.github/scripts/generate-release-body.sh` | `8ebaf8daad` |
| 59 | `.github/workflows/fork-checks.yml` | `8ebaf8daad` |
| 13 | `.github/workflows/fork-generic-x64.yml` | `8ebaf8daad` |
| 49 | `.github/workflows/fork-mirror-build-container.yml` | `8ebaf8daad` |
| 40 | `.github/workflows/fork-wordlist.yml` | `8ebaf8daad` |
| 290 | `tools/archaeology` | `8ebaf8daad` |
| 107 | `tools/box-check` | `8ebaf8daad` |
| 461 | `tools/ceremony-check` | `8ebaf8daad` |
| 200 | `tools/es-menu-map-check` | `8ebaf8daad` |
| 50 | `tools/forbidden-terms-check` | `8ebaf8daad` |
| 164 | `tools/fork-package-freshness` | `8ebaf8daad` |
| 309 | `tools/fork-worktree` | `8ebaf8daad` |
| 394 | `tools/lint-audit-artifacts` | `8ebaf8daad` |
| 167 | `tools/pr-stack-check` | `8ebaf8daad` |
| 131 | `tools/prose-check` | `8ebaf8daad` |
| 420 | `tools/rc-preflight` | `8ebaf8daad` |
| 105 | `tools/register-check` | `8ebaf8daad` |
| 107 | `tools/release-catalog` | `8ebaf8daad` |
| 1,597 | `tools/renovation-inventory` | `2174265e9c` |
| 212 | `tools/renovation-drift` | `2174265e9c` |
| 147 | `tools/renovation-status` | `2174265e9c` |
| 245 | `tools/rules-check` | `8ebaf8daad` |
| 132 | `tools/vocabulary-check` | `8ebaf8daad` |
| 106 | `tools/work-log-index` | `8ebaf8daad` |

**Provenance:**
- **128 fork commits** since `c445081a59` touch the 28 at-hash files, 125 of them without merges (`git log --format=%h c445081a59..8ebaf8daad -- <the 28> | wc -l`, and the same with `--no-merges`).
- The two `.github/scripts/*.sh` files are the only ones of the 31 that exist on `upstream/next` (`git cat-file -e`):
  - `generate-release-body.sh` is byte-identical to `upstream/next`;
  - `generate-changelog.sh` differs by +1/-8. The difference is **upstream's two commits after the fork's last merge**, not a fork hunk: `76693a738d` (2026-10-13, *ci: add github username to release*; the author lookup) and `71d8932b33` (2026-10-14, *openabl: introduce package*; `openabl` in the kernel category). `next`'s only commit on the file in the range is the merge `7bd7f31312` (2026-09-19). This is **a delta from the brief**, which reads it as the fork's hunk `8a7f33791d`; that commit is itself the upstream merge of PR #3256, dated 2026-09-11. The file is a Q4 row: the fork is two upstream commits behind.
- The three `renovation-*` tools exist only on P1's branch (`git cat-file -e 8ebaf8daad:tools/renovation-inventory` fails).

**The branch against the hash over the 28** (`tr '\n' '\0' < paths28 | xargs -0 git diff --stat 8ebaf8daad HEAD --`) touches 5 files, +92/-9, each with its owner:

| Path | Hunk | Owner commit(s) |
| --- | --- | --- |
| `.githooks/hooks-test` | +7 | `1b8ac30421` (#696: the marker case and the setext control) |
| `.githooks/pre-commit` | +13/-1 | `1b8ac30421` (#696: the conflict-marker refusal) |
| `.githooks/pre-push` | +3 | `9966dbcd12`, `af24589b1c` (P1, #641: the three `renovation-*` personal patterns) |
| `tools/register-check` | +17 | `f00ab3e163` (ten decided rows moved, and the `MISPLACED` check) |
| `tools/lint-audit-artifacts` | +61/-9 | `fc88815ccb` (P1's renovation face), **`6874394d49`** (2026-10-22, explicit Argon reviewer receipts, +13/-7; in the coordinator's tip `69fcce37b3`, merged at `50137e3ee0`), `fa6bcdafa8` / `18747fbc52` (#810: Local depth at epic tier) |

**A delta:** `6874394d49` is a commit the brief does not list for the lint. Its hunk is inside the file and total the brief and dispatch name, so it is recorded here and is not a stop. The branch against `2174265e9c` over the three `renovation-*` tools is empty.

**The after-hash deltas:**
- `9e12014623` (#905's packet, `ceremony-check` +55/-9, 2026-10-24 15:26:33Z) is **off this branch**. It is read as a diff at stage B, beside the hash's reader.
- The four commits above are **on it**: `1b8ac30421`, `18747fbc52`, P1's `pre-push` and lint edits, and `register-check`'s `f00ab3e163`.

**The two lists:** `PERSONAL_PATTERNS` is `pre-push:62-188` at the hash, with 115 quoted entries; 84 begin `tools/` and **14** begin `scripts/`, against the brief's 12, a delta that stage B re-derives. On P1's tip it is 62-191 with 118 entries. The entry-by-entry diff against `fork-workflow.md` § *Personal paths* is `04` § Q7's.

**The rules, the registers and the blindspots read for the scope** are listed in `## Phase 1` when stage B opens.

# Research Notes — M6.P2 T6, upstream's helper tools and the other distributions

## Scope

- **Read hash:** the slice's bytes are `next`'s at **`8ebaf8daad`**; **`reviewed-at:` `b96e1ca761`**, the branch `HEAD` at stage A (stacked on P1's `2174265e9c`, the coordinator's tip `3d60062ce5` merged at `e84180386d`). `upstream/next` `e0f9deb899` at the fetch.
- **The filter** (brief § 2), run on `docs/reviews/inventory.json` (P1's `eb4763e3cc`). The membership is the `build-engine` area's rows under `tools/**` and `distributions/**`, less `distributions/ROCKNIX/**`:

```
paths 135 lines 7369 {'upstream-carried': 134, 'fork-own': 1} {'unreached': 27, 'n/a': 108}
{'image': 17, 'symlink': 1, 'shell': 37, 'none': 66, 'font': 1, 'other': 2, 'markdown': 1, 'docker': 6, 'config': 1, 'python': 3}
```

  All equal to the brief's figures: no delta. The fork-own row is `tools/pkgcheck`, the inventory's tier; Q4 settles it.
- **What else the two roots hold:** `git ls-tree -r --name-only 8ebaf8daad -- tools distributions` less `distributions/ROCKNIX/` gives 263 tracked paths. The slice's 135 are those the inventory puts in `build-engine`; the other 128 are the fork's own tools in the fork's areas (T9 to T15's), not this slice's.
- **`git diff --stat 8ebaf8daad HEAD -- tools distributions ':!distributions/ROCKNIX'`:** 15 files, none of them the slice's.

| Path | Commit | Owner |
| --- | --- | --- |
| `tools/renovation-inventory`, `renovation-status`, `renovation-drift` | `00ca350666`, `af24589b1c`, `a7cbde1737` | P1 (#641) |
| `tools/register-check` | `f00ab3e163` | P1 (#641) |
| `tools/test-fixtures/lint-audit-artifacts/fixture-epic-m6-renovation-{pass,fail}/` (10 files) | `fc88815ccb` | P1 (#641) |
| `tools/lint-audit-artifacts` | merged at `e84180386d` | the coordinator's tip (#810) |

- **Over the 135 alone:** `git diff --stat 8ebaf8daad HEAD -- $(cat .qa-scratch/t6/paths.txt)` is empty.
- **Q4's upstream-state count:** 134 identical to `upstream/next` (`e0f9deb899`), 1 differs (`tools/pkgcheck`).
- **The M7 delta:** none on the 135. M7's tree is the legacy checkout's; the slice is read at `next`'s bytes.

## Phase 1

*(stage B)*

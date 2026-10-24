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

- **#644 finding 24** (`docs/reviews/build-path-read.md:177`, read whole): *"LibreELEC's `tools/update-scan`, `update-pkg`, `distro-tool`, `refresh-patches` are carried and unused by any ROCKNIX workflow"*. Upstream's side: *the same tools, unused*. The difference: *both carry dead tooling*. Kind: *candidate*. Carrier: *T6: the reachability table decides (D-WORKFLOW-185's "unshipped is not dead" applies to devices, not to tools nothing calls)*. The other 25 findings' carriers are in `02` § The #644 finding.
- **T5's rows that touch this slice** (`feature/m6-build-engine-652:docs/audits/2026_10_24-epic-m6-build-engine/02-forward-audit.md`, read with `git show`):
  - **`scripts/update_packages`:** "`Makefile` `update` only; never run on the fork". F-19: it stripped checksums, fixed in T5's E6 (`b34868cb18`). It does not call `tools/update-pkg` or the helpers.
  - **`config/multithread`:** F-22, the statistics pipe at 64, fixed in E8 (`7abea6eb86`).
  - **`scripts/build`:** "reached by every package of every fork build"; no call of `tools/pkgcheck`.
  - **T5's Q6 Table 4:** `update-mirror-sources.yml` "runs weekly and is `skipped` by its repository gate", which decides `download-tool`'s row; `update-kernel-configs-docs.yml` "runs on the fork and fails" (PL-15, deferred to #657), which reaches `adjust_kernel_config`.
  - **T5's Q6 Table 1:** `scripts/create_addon`'s only caller is `tools/repo-tool`.
  - **T5's PL-26:** `scripts/test-audit-review.py` in the wrong area, the coordinator's; not this slice's.
- **`tools/pkgcheck`'s two names:**
  - The inventory's tier is `fork-own` (P1's rule: changed since the merge base `c445081a59`).
  - `instruction-files.md` § The fork's own tools lists `pkgcheck` *(upstream's)*.
  - `CLAUDE.md:109` and `AGENTS.md:107` introduce it as "the only lint".
  - The history decides: one fork commit, `81221658b3` (`04` § Q4).
- **The blindspots the brief names** (`docs/blindspot-register.md`, read in full once):
  - 13, assumed done: every verdict cites a command;
  - 22, a probe that cannot report absence: every zero was searched a second way, with a positive control;
  - 46, a name read as a behaviour: a tool's name is not its reach; every caller is a `git grep` hit;
  - 51, a checklist from open boxes;
  - 75, a corpus read on the wrong tree: the read is the at-hash export and `git grep 8ebaf8daad`, never the branch's two roots whole.
- **The rules read for this work** (`working-principles.md` § Pre-flight):
  - `engineering-practices.md` (§ Verify the artifact, § A name is not a behaviour, § Before deleting a duplicate, § Guards must fail closed, § Consider contributing upstream);
  - `device-builds.md`;
  - `packaging-and-patches.md`;
  - `fork-workflow.md` § Personal paths;
  - `instruction-files.md` § The fork's own tools;
  - `bugs-are-agent-first.md`;
  - `upgrade-and-install.md`;
  - `issue-tracking.md`;
  - `vm-first.md`;
  - `worktrees.md` (superseded by brief § 1 for the layout).
- **The skill:** code-auditor at epic tier with the renovation face. `templates.md` in this worktree carries #810's Local-at-epic plan shape; `tools/lint-audit-artifacts` accepts it through the two keys.
- **Decisions cited:** D-WORKFLOW-184, -186, -187, -164/165, -193/194, D-UI-079, D-INFRA-025.

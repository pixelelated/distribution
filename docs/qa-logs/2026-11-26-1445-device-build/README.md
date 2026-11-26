# #1445: one command launches a device build

`tools/device-build` on `next`, 2026-11-26 (OS coordinator). Every run below is against the round head `a069abd236` (build 12's commit) with the round's ES supplier, `m7-rc-round-20261126-03-es/inputs/es`. A host tool needs no guest.

| File | Command | What it shows |
| --- | --- | --- |
| `a-sm8550-clean.txt` | `--device SM8550 --commit a069abd236 --set m7-final-dryrun --es-supplier … --dry-run` | Exit 0. Every path, the `DOCKER_WORK_DIR` alias, the `DOCKER_EXTRA_OPTS` mounts (.git, source cache, ES supplier read-only, `TMPDIR=/tmp`) and the two-ABI export (`PROJECT`/`DEVICE`/`ARCH`). The replay plan is the one retained SM8550 build log. The one-build rule's removals are the round tree's `config/options` cache and the x64 root (111.2 GiB); its keeps are seven `target/` and `kept/` items with sizes. **Nothing created:** no set file, worktree or owner folder. |
| `a2-sm8550-clean-after-primary.txt` | the same, after `--primary` was added | Identical to `a`, except the last message, which now says that removals come after the admission. |
| `b-es-missing.txt` | `--device H700 … --es-supplier /workspace/tmp --dry-run` | Exit 2: the supplier has no `emulationstation-m7-20261126-bb3f0838f671.tar` (the recipe mounts it at `/tmp/pix-m7-es-source-delivery-20261126-03`). |
| `c-sources-missing.txt` | `… --sources /workspace/cache/no-such-cache --dry-run` | Exit 2: the source cache is missing. |
| `d-stale-root.txt` | `--device GENERIC_X64 --worktree <the x64 build worktree> --dry-run` | Exit 2: build roots already exist; `--warm` to build on them (the stale-root control of run `1bfb5a21`). |
| `g-git-missing.txt` | `… --primary /workspace/tmp/no-such-checkout --dry-run` | Exit 2: `.git` is missing, and the container mounts it because `scripts/image` runs `git rev-parse`. |
| `e-failing-step.txt` | a real run: `--device GENERIC_X64 --set test-1445-refusal --worktree <x64 worktree> --warm --protect /workspace/no-such-path-1445`, launched from a shell whose argv carries `make docker-SM8550` | Exit 1, at the retention report. Details below. |
| `f-move-set.txt` | `--device H700 --commit 0a3e979e50 --set test-1445-refusal --dry-run`, while that set's file said `a069abd236` | Exit 2: the set is at `a069abd236`, not `0a3e979e50`, and moving it means rebuilding what was built at the old head ("nothing yet"); `--move-set` moves it. |

**The failing step (`e`).** The busy check did not match the launching shell: its first line is "nothing else is running". The run then went in this order:

1. The set file was written (`e-set-file.json`).
2. The worktree was at the head already.
3. The patch replay for x86_64 ran first: 133 packages, 354 patch applications, every patch applies (`e-replay-RUN.txt`). It took 29 minutes, almost all of it waiting for `scripts/get`'s host-wide fetch lock while ppsspp-sa's `ffmpeg` submodule cloned into the shared cache.
4. The plans were written (`e-retention-plan.json`, which names the nonexistent protected path).
5. The retention report raised `FileNotFoundError` on that path (`e-retention-report.console`), and the command stopped with exit 1.

What did not happen: no `admission.json` and no submission folder, and **no removal**. The roots the dry run listed were still there afterwards (`e-roots-after.txt`), because removals come only after the admission. The test set file and owner folder were removed after these files were copied here.

**Not yet seen:**
- The real launch: the swap preflight's saved output ending `READY`, the `/tmp` warning in a run, and the first compiled package (criteria 1, 4, 6 and 8).
- The removals themselves.

These wait for the final head's build set, which waits on Max's answers.

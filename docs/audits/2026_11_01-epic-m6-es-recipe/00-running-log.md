# T37 (#684) running log -- the EmulationStation recipe and themes in the distribution

- **Executor:** the T3 session `m6-t3-emulators`, model Opus 5.5 (`claude-opus-5-5`), effort **high**.
- **Brief:** `docs/reviews/briefs/es-recipe.md` at version 2 (`926d1fbaee`) with its `## Errata before dispatch`; the dispatch comment on #684 (6551464928, 00:57 UTC 2026-11-01); the pointer check posted at 00:59 (6551479786) and confirmed by the coordinator at 01:00 (6551486741).
- **reviewed-at (distribution HEAD at stage A):** `9fa740a91ba9fcaa21a26cc72f0b50fac10f32df` (the coordinator's seeding commit over the merge `94d8ef8e7e`, which brought `566398105e` onto the P1 tip `2174265e9c`); the ES recipe is the same blob at `2174265e9c` and at HEAD (`cmp` of the two, stage A).
- **reviewed-at-es:** `none -- no ES change` (ruling (c)); the pin `16dbac5211eea7e70db7394372033be2be7df829` is read by hash from `/home/max/Development/emulationstation-next.worktrees/qa-integration` only.
- **Depth:** Independent (one seat, GPT-6 Astra at `max`, a probe and one refutation, at stage C). **Keyed invokes so far: 0.**

## The host file at stage A

Read at **01:01:29 UTC** (the § 1 block's `date -u` and `tail -n 6 ... | cut -c1-200`) and again whole-tail at **01:01:35** and **01:01:40 UTC**: 561 lines. The last six lines were T36 (#683) lane's host-only compile START/END pairs and the coordinator's automatic acknowledgements by `kit/compile-ack.sh`:

```
2026-11-01T00:59:27Z T36 (#683) lane: stage C compiles END (S0 binary, rc 1).
== M6 coordinator — 00:59 UTC (2026-11-01): acknowledged T36 (#683) lane: stage C compiles END (2026-11-01T00:59:27Z; host-only compile, no guest, no image build) -- automatic acknowledgement by kit/c
2026-11-01T01:00:56Z T36 (#683) lane: stage C compiles START (S0: binary with 3.17/3.22/3.23; host-only).
== M6 coordinator — 01:00 UTC (2026-11-01): acknowledged T36 (#683) lane: stage C compiles START (2026-11-01T01:00:56Z; host-only compile, no guest, no image build) -- automatic acknowledgement by kit
2026-11-01T01:01:05Z T36 (#683) lane: stage C compiles END (S0 binary, rc 1).
== M6 coordinator — 01:01 UTC (2026-11-01): acknowledged T36 (#683) lane: stage C compiles END (2026-11-01T01:01:05Z; host-only compile, no guest, no image build) -- automatic acknowledgement by kit/c
```

M7's own last line was line 531, `2026-11-01T00:48:41.592557+00:00 M7 RETURN owner10 remaining TLS: ... No runtime held.` (its START at line 528, 00:42:01): **no M7 standing or compile START open** at the read. This lane wrote nothing to the host file at stage A.

## Census

- **01:01:50 UTC:** `qemu 0`, `compilers 0` (`pgrep -c -x` over the qemu and compiler names; the process view is the host's: `/proc/1/comm` is `systemd`, 703 processes).
- `ls -d build.*` in the worktree: **0** at every check of stage A (s5-runs R13, R15 and its last line; plans.out).

## The scratch

- `df -i /workspace` before the first write: `/dev/nvme1n1 244195328 64707464 179487864 27% /workspace` (01:01:10 UTC).
- Scratch root `/workspace/tmp/m6-t37/` (made 01:01): `tmp/` (`TMPDIR`, `tmp/home` the `HOME` of every `env -i` call), `stage-a/` (the runs' working copies).
- **The scratch export (ruling (k)): `/workspace/tmp/m6-t37/export/`**, `git archive HEAD | tar -x` of `9fa740a91ba9fcaa21a26cc72f0b50fac10f32df` at 01:05 UTC (`export rc=0`, 133,480 files, no `.git`). Every sourced-recipe call of stage A ran there under `env -i` with `HOME` in scratch. By stage A's end the calls had made **16 build roots in the export** (GENERIC_X64 and H700 by the effective-value and patch-reach calls; the other 13 devices by mesa's per-device read; `build.pixelelated-RK3566.arm` by the arm plan) -- each holding the two `.cache_package_*` files `config/functions:801-802` write -- and **none in the worktree**. Retired at stage H.
- `.qa-scratch/t37/` in the worktree (gitignored, `.gitignore:63`) holds § 2's block's working files, as the block writes them.

## Reads outside the worktree, stage A

- The P1 research clone `/workspace/tmp/m6-coordinator/t11-research/tree` (`W`), by `git -C "$W" ls-tree/show/diff/cat-file` only, in § 2's block.
- The ES checkout `qa-integration`, by `git -C ... show/rev-parse/rev-list/merge-base/grep/for-each-ref` only.
- **The shared download cache, one file:** `/workspace/cache/rocknix-sources/es-theme-art-book-next/es-theme-art-book-next-9a50ef366e750aabfab29e6915a2867607212971.tar.gz`, read for L-22 (the errata's "read by hash"): its sha256 equals the recipe's `PKG_SHA256` `7ee1e93f...1231125`; listed with `tar -tzf` and its 28 XML members extracted to `/workspace/tmp/m6-t37/stage-a/l22/xml/`. Nothing in the cache was written. Named on #684 at stage A's checkpoint so the coordinator can rule it out of bounds.
- T36's branch `origin/feature/m6-es-core-utils-resources-683` by `git show` only (its `00` line 54, G-01).
- The host file, read only.

## Never run at stage A

No image build, package build or compiler (no compile START written); no `git fetch`, `git ls-remote` or `gh api` of an author's repository; no `rc-preflight`; `tools/fork-package-freshness` only as `--list` with both refs; no council call of any kind; no handheld, owner account or hosted account; nothing under `/workspace/repos/rocknix` or `rocknix.worktrees/*` (§ 5's candidate-provenance line not run: open item 16, the dispatch); no held directory opened in this slice; no ES worktree and no write in any ES checkout; no guest; nothing under `~/.ROCKNIX/` or `~/.rocknix/` read; `config/options` never sourced in the worktree; no edit under `packages/`, `projects/` or `tools/` (s5-runs R22: `git diff --stat 94d8ef8e7e HEAD -- packages projects tools` printed no line).

## Entries

- **00:59 UTC** -- the pointer's eleven keys read against § 10's table; none names T36; § 9's placeholder grep printed `6` on it; posted on #684 (6551479786); confirmed with the fills at 01:00 (6551486741).
- **01:01:27 UTC** -- the § 1 first commands (`stage-a/s1-first-commands.{sh,out}`, script `rc=0`): status `0`; `stacked`; no `ui/` line against `8ebaf8daad`; `upstream-next-is-here`; merge base `c445081a59518f37d9776e5412dd7b14910696f7`; `pin-here`; `rocknix/master` `f6c542872e3850c5f432929ead219547a897cd4a`; the ES merge base `cada856d86e3115fbbf0bce09dd761b0ee8fa9fd`; `origin/feature/m6-es-core-window-input-682 b7fdb3a24c859ce91f9fd381bb0956901b8d23cb` and `origin/feature/m6-es-core-utils-resources-683 fatal: Needed a single revision` (T36's ES branch exists only locally, at the pin: open-items.out); `pkgcheck emulationstation rc=0`, `pkgcheck es-theme-art-book-next rc=0`, `pkgcheck lowerdeck rc=0`, each after its `find` path; `register-check rc=0`.
- **01:03 UTC** -- § 2's block, extracted from the brief's lines 408-522 (115 lines), sha256 `f3ef373be653546772d6f4be0a27f9c9913b9aee050f432a31bf8d20286dc1b0` (the prefix `f3ef373be6535467` checked); run from the worktree (`block rc=0 wall=6s`); its output equal to the brief's expected lines 531-560 byte for byte (`diff` rc 0). The extended run printed its 8 lines; outside `CLAIMS` its output equals the block's second pass (`diff` rc 0).
- **01:05 UTC** -- the § 5 runs (`stage-a/s5-runs.{sh,out}`, R01-R22, script `rc=0`, 7 s). Every expectation held but two lines, each recorded beside its expectation in `01` § Scope: `HFS_DEV_LOGIN` is also read at the pin's `es-app/src/scrapers/HfsDBScraper.cpp:181`; and the mask `M` turns `:30`'s `-DSCREENSCRAPER_RUNTIME_DEV_LOGIN=1` into `=***` in the printed effective options (the `=1` counted separately: `1`). **The mask `M` leaves `:39` unchanged** (40 characters, masked text equal to the line, counted without printing it), so every read of the recipe here also withholds `:39` by line number (`W39` in s5-runs.sh); no stage-A read printed `:39`.
- **01:07-01:09 UTC** -- open items 3, 5 and fribidi's path: `scripts/pkgjson | scripts/genbuildplan.py` in the export, as `config/multithread:49` pipes them (a first attempt wrote the JSON to a file between them, and the parallel workers' records interleaved: `JSONDecodeError`, recorded in plans.sh's header); `stage-a/plans.{sh,out}`, `stage-a/trace.{py,out}`.
- **01:10 UTC** -- open item 9: mesa's effective GLES options for all 15 devices (`stage-a/mesa-gles.{sh,out}`).
- **01:12 UTC** -- the issues re-read (`stage-a/issues.out`).
- **01:14 UTC** -- open items 2, 13 and 15, L-22, the lanes' tips and T36's G-01 line (`stage-a/open-items.{sh,out}`, `rc=0`).
- **01:15 UTC** -- `00`, `01` § Scope, the pointer and the work log written for stage A's commit.

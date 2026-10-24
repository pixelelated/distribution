# Mini Retro: M6.P2 T7, the generic packages the image builds (#654)

**Completed:** 2026-10-24
**Scope of this retro:** the T7 lane, covering:
- the slice's 266 paths (243 recipes, 7,612 lines), read at `8ebaf8daad`'s bytes;
- the Local-depth currency audit, stages A to D (`docs/audits/2026_10_24-epic-m6-generic-packages-reached/`, #884's fifteen items);
- the one fix stream, S1 of the coordinator's `t7-streams.md`;
- verification.

Not retro'd here, because they are not this lane's:
- #877's packet (the T1 session's);
- the #585, #645 and #885 posts (the coordinator's);
- the merge to `next`.

**Commits:** `reviewed-at` `4ea87f17dd`; `fixed-at` `063f10154a` (S1's last).

## What the slice did to the two time-to-play numbers

**The slice did nothing to the two time-to-play numbers.** Interface to a game's first frame and game to game are untouched. S1 changes three `PKG_URL` lines; the bytes each recipe fetches are unchanged (P17), so the binaries the next build makes from them are the same. No time-to-play run was made, because no image changes behaviour.

## What worked well

- **Three sources, each with its mover named before a row was written.** `upstream/next`, LibreELEC master and the project, with the base merge, ROCKNIX's LibreELEC merge and the fork as the movers. No row reads `current` without (c) read. 223 rows honestly say *follows the base merge* rather than claiming currency they did not check.
- **Probing without `-L`, then fetching every redirect once through `sha256sum`.** The redirect turned out to be the normal case (132 of 235 archives), and hashing them found the one archive with nothing to match (`libfmt`). The two controls outside the set (`fbalpha2019-lr`'s 301, `portaudio`'s 404) showed the probe could tell the classes apart.
- **Reading what the build reads.** Expanding every URL and checksum through `config/options` for each of the five plans is what surfaced:
  - `libfmt`'s empty override;
  - the three overrides that change the pin;
  - `btrfs-progs`' `PKG_ARCH`.

  None of the three is visible in the recipe files the slice owns.
- **One generator for every table.** `tools/t7-tables.py` asserts 266 and 243 and fails on a missing result line. So the coverage table, the currency table, `q4-pins.json` and the #645 rows were regenerated each time a disposition changed, and never edited by hand.

## What was harder than expected

- **The incident (10:44).** An unquoted heredoc ran every backticked name in the log's prose, `scripts/update_packages` among them. It rewrote `hatarisa`'s recipe in the lane's worktree before the revert. The guard is now plan § 6b E's bullet. The lane repeated the unquoted form once more (with every backtick escaped, so nothing ran) before switching to Python and quoted heredocs only.
- **A typed hash.** A bug body's sha256 was completed from a 16-character prefix by memory, and the tail was wrong. The check that compared each body with its recipe caught it before filing.
- **Two stage-B readings were wrong:**
  - **`btrfs-progs`.** Stage B called it unexplained; the coordinator found the override's `PKG_ARCH` in minutes. The lane had expanded `PKG_VERSION`, `PKG_SHA256` and `PKG_URL` per plan but not `PKG_ARCH`; the stage-C sweep did, and found no sibling.
  - **The sourcing overrides.** Stage B called this an inventory defect, which it is not.

  Both corrections are left visible.
- **The redirect fetch's bandwidth.** About 300 MB, streamed and never stored, for a table slice. Its rule (fetch only on a redirect) was right, but the futro's S-1 had expected the probe alone to carry most rows.

## What we discovered

- **The fetch's resilience is ROCKNIX's mirror.**
  - Four primary URLs are dead (#880 to #883), and `portaudio`'s too (#849, corrected).
  - Every one builds only because `get_archive` falls back to `sources-v2`.
  - #844's tool should probe the mirror first.
- **An empty assignment is a missing checksum.** D-WORKFLOW-194 counted lines; `libfmt`'s `PKG_SHA256=""` made the count six (#877, D-WORKFLOW-196), and T5's guard would have stopped two images' builds.
- **47 ROCKNIX overrides layer onto this slice's recipes.** Three change the pin, four the URL or checksum, and six are orphans ROCKNIX has since deleted.
- **The brief's own block had a `sed` that cut a name containing `-<digit>`** (`ntfs-3g_ntfsprogs`, `01` § Brief erratum).

## Adjustments for the next lane (proposals for the coordinator, D-WORKFLOW-189)

- **Prose goes through a quoted heredoc or a Python write, never `<<EOF`.** This is in the plan now. A lane's own time stamp can be passed as an argument to Python, so no prose ever needs shell expansion.
- **A value in prose is read from its file.** A hash, a count or a line number is copied by a command, never retyped from a prefix.
- **Expand every field a build reads per plan** (`PKG_VERSION`, `PKG_SHA256`, `PKG_URL`, `PKG_ARCH`), not the three a table names. The fourth is where a plan reading goes wrong.
- **A stripping `sed` over directory names is checked against the names it strips:** grep the list for `-<digit>` first.
- **#844's fetch check probes the mirror and the primary URL**, per plan, through `config/options`.

## Scoped audit (the close-out's own checks)

- `tools/lint-audit-artifacts docs/audits/2026_10_24-epic-m6-generic-packages-reached`: `PASS`, with the D-WORKFLOW-184 line.
- `PROOF:` lines 18, `proved:` cells 18.
- The coverage table has 266 rows; `q4-table.md` has 243.
- #884: 15 of 15 at a Phase 7 outcome (3 Resolved, 11 Deferred, 1 Withdrawn); `tools/box-check --issue 884`: 0 open, 0 fail.
- #880 to #883: open, Low, mirror-covered, deferred to #585's section; `box-check` 0 fail each.
- `git diff --stat 8ebaf8daad 063f10154a -- packages projects`: three files, three lines; no `PKG_VERSION` changed; nothing deleted or renamed.
- The checkers' exit codes: in the stage-H hand-back on #654.

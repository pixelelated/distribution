# Research notes — M6.P2 T5, the build engine (#652)

## Scope

- **Read hash:** the slice's bytes are `next`'s at **`8ebaf8daad`** (the stage-A byte check of brief § 1, exit 0 at 03:51 UTC). **`reviewed-at:` `46f6c7d428`**, the branch `HEAD` at stage A. `upstream/next` `3421d7d178` at the fetch; merge base `c445081a59`.
- **The filter of brief § 2** (the inventory's rows with `tree == distribution`, `area == build-engine` and a path under `scripts/**`, `config/**`, `distributions/ROCKNIX/**`, `Makefile`, `Dockerfile`, `.gitignore`, `.merge-head`, `.github/**`), run with python3 -I over `docs/reviews/inventory.json` on the P1 tip:

  | Figure | Recorded | Re-derived | Delta |
  | --- | ---: | ---: | --- |
  | paths | 242 | 242 | none |
  | lines (numstat against the empty tree) | 13,910 | 13,910 | none |
  | fork-own paths / lines | 18 / 3,266 | 18 / 3,266 | none |
  | upstream-carried / vendor-carried | 224 / 0 | 224 / 0 | none |
  | code-class lines (the tool's `read`) | 6,776 | 6,776 | none |
  | of which fork-own | 2,419 | 2,419 | none |

  The code-class set is the tool's own (`tools/renovation-inventory` 674 to 676: `shell`, `python`, `recipe`, the C and C++ classes, `javascript`, `typescript`, `make`, `cmake`, `systemd`, `udev`, `script`, `perl`, `lua`, `rust`, `go`, `assembly`, `shader`, `docker`, `kconfig`, `html`, `css`; no `yaml`), and `order()`'s full predicate at 1274 (CODE, not vendor-carried, not `unreached`) gives the same two figures because every row's `reach` is `n/a`. **The three figures this brief reads beside the tool's:** 13,910 lines in the membership; 6,776 in the tool's `read`; 2,419 of those fork-own. Outside the tool's `read` and inside this brief's: the 139 `config/emulators/*.conf` (`config`), `config/functions`, `config/graphic` and `distributions/ROCKNIX/config/functions` and `version` (`none`), the 19 workflows (`yaml`), and the rest of the `config`, `xml`, `other`, `image`, `json`, `markdown`, `text` and `translation` rows.
- **By language:** `config` 139, `shell` 30, `yaml` 19, `none` 12, `image` 11, `other` 8, `xml` 8, `python` 5, `json` 2, `markdown` 2, `docker`, `make`, `recipe`, `systemd`, `text`, `translation` 1 each.
- **By directory:** `config/emulators` 139, `scripts/` 30, `.github/workflows` 19, `config/noobs` 15, `config/` top level 13, `config/addon` 7, `config/docker` 7, `distributions/ROCKNIX` 5, `.github/ISSUE_TEMPLATE` 2, `.github/pull_request_template.md` 1, and `Makefile`, `Dockerfile`, `.gitignore`, `.merge-head`: 242.
- **The 18 fork-own paths** (lines, language): `scripts/build` 646 shell; `scripts/image` 481 shell; `distributions/ROCKNIX/config/functions` 400 none; `distributions/ROCKNIX/options` 219 shell; `Makefile` 208 make; `scripts/install` 196 shell; `config/graphic` 168 none; `config/show_config` 160 shell; `scripts/test-audit-review.py` 150 python; `.github/workflows/validate-pull-request.yml` 121 yaml; `scripts/build_distro` 106 shell; `scripts/build_compat` 103 shell; `.gitignore` 84 other; `scripts/extract` 84 shell; `.github/workflows/check-freeze-period.yml` 63 yaml; `config/build-identity` 44 shell; `scripts/get_env` 22 shell; `distributions/ROCKNIX/version` 11 none.
- **The 30 scripts:** `autoreconf autoremove build build_compat build_distro build_mt ccache_stats checkdeps clean create_addon create_docker_package extract genbuildplan.py get get_archive get_env get_file get_git image install install_addon makefile_helper mkimage pkgbuild pkgbuilder.py pkgjson test-audit-review.py uboot_helper unpack update_packages`.
- **The five groups** (brief § 2, read in this order): 1, the 18 fork-own paths; 2, the upstream-carried engine core (`config/functions`, `options`, `path`, `arch.*`, `optimize`, `multithread`, `sources`, `blocklist`, the 23 upstream scripts, `Dockerfile`, `.merge-head`); 3, the 139 system fragments; 4, `config/noobs`, `config/addon`, `config/docker`; 5, the workflows and templates.
- **What the globs would have swept in, and who owns it:** the globs alone give 647 paths in the inventory (`build-engine` 242, `tooling-and-guards` 52, `records` 353). `git ls-files` over the glob directories gives 294; the 52 beyond the membership are all `tooling-and-guards` (T10's): 46 under `scripts/` (the council toolchain: `scripts/lib/` 24 files, `scripts/__tests__/` 2, `council-*`, `lint-council-*`, `verify-{chain,pins,seals}.ts`, `write-step-seal.ts`, `owner-queue-lint.mjs`, `forge-write-status.mjs`, `setup-council-mistral-tokenizer.mjs` and the rest), `.github/workflows/fork-{checks,generic-x64,mirror-build-container,wordlist}.yml`, and `.github/scripts/generate-{changelog,release-body}.sh`. The 353 `records` rows are the `.github/sessions/**` checkpoints, nobody's slice. No membership path lies outside the `git ls-files` listing.
- **History:** 31 fork commits on the membership `c445081a59..8ebaf8daad`; 3 upstream commits on it `c445081a59..upstream/next` (`c4d353449e`, `76693a738d`, `c200cc906d`).
- **The interacting subsystems** (brief § 2, § 6 Retrospective row; the seams § 3.5 audits): the entry points and `tools/watch-build`'s marker and lock (T9); `scripts/get_env`, the Makefile's `.env` recipe and `~/.ROCKNIX/options` (the credentials, D-INFRA-006); `calculate_stamp` and the overrides that source a generic recipe (T8); `mk_es_systems`/`add_es_system` and the `emulators` metapackage (T3); `scripts/image`'s identity, `tools/rc-preflight` and `tools/fork-publish-release` (T9, the release rules); the upstream workflows and the fork's own CI (T10).
- **The M7 delta on the membership:** `git -C /workspace/repos/rocknix log next..069fc2704421 -- <the 242 paths>` prints nothing (12 M7 commits past `next`, none on these paths; the legacy checkout's `next` is `8ebaf8daad`). The engine the M7 candidate builds with is the engine at `8ebaf8daad`.
- **The branch scan.** Predicate: a branch is ahead of `next` on the membership when `git log --oneline next..<branch> -- <the 242 paths>` prints a line. Command: that predicate over every `refs/heads` and `refs/remotes/origin` ref of this clone, at 03:53 UTC. 17 branches, all old remote branches; none local, none an M6 lane's. Posted on #652 as a lead, not read:

  | Commits ahead on the membership | Branch |
  | ---: | --- |
  | 8 | `origin/feature/conflict-resolution` |
  | 6 | `origin/x64-build-fix` |
  | 5 | `origin/backup/generic-x64-pre-rebase-20260714` |
  | 3 | `origin/rclone-bisync-beta` |
  | 2 | `origin/pr/10-es-pin` |
  | 2 | `origin/pr/09-retroarch` |
  | 2 | `origin/pr/08-saves` |
  | 2 | `origin/pr/07-cloud-setup` |
  | 2 | `origin/pr/06-retroachievements` |
  | 2 | `origin/pr/05-network` |
  | 2 | `origin/pr/04-settings` |
  | 2 | `origin/pr/03-evidence` |
  | 2 | `origin/pr/02-generic-x64` |
  | 1 | `origin/verification-anchors/2026-09-30-rasteratops-fork-plan-r2` |
  | 1 | `origin/verification-anchors/2026-09-30-rasteratops-fork-plan` |
  | 1 | `origin/pr/cairo-1.18` |
  | 1 | `origin/pr/01-build` |
- **Upstream trackers checked (D-WORKFLOW-162):** written at Phase 1, below.

## Phase 1

Not yet written (stage B).

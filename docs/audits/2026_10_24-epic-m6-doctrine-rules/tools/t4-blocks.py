#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-2.0-or-later
# Copyright (C) 2026-present ROCKNIX (https://github.com/ROCKNIX)
"""t4-blocks.py -- 02 § Command blocks for M6 T4 (#651, brief § 5 and
criterion 8): every fenced block in the 36 files at 8ebaf8daad, with the
verdict this lane reached for it.

    python3 -I t4-blocks.py <read-tree> <paths.txt>

The blocks are found in the read tree (a fence of three or more backticks to
its matching close). The verdicts below are the lane's, each from a command
recorded in 02 § Mechanical checks or § Findings; the script refuses to print
when a block has no verdict or a verdict names no block (both directions),
so a block added to a rule cannot pass unread.

Verdict words: `ran: passed` (run on the host as written, read-only),
`ran: failed`, `checked` (its tools, scripts, targets and options exist at
the hash as written), `checked: wrong` (they do not; the finding is named),
`not runnable here` (with the reason), `not a command` (an example, a log, a
diagram, code).
"""
import re, sys

root, paths = sys.argv[1], sys.argv[2]
V = {
    ".claude/rules/ceremonies.md:97": "ran: passed -- `tools/ceremony-check` rc 1 (W42, M7's) and `--gate` rc 1 likewise; `tools/archaeology D-CLOUD-076` rc 0; `work-log-index --write` not run (it writes), `--check` rc 0",
    ".claude/rules/council-substrate-integrity.md:75": "checked: wrong -- `scripts/lint-council-research-provenance.ts` and `research/council-research/` are absent at the hash (F-20)",
    ".claude/rules/device-builds.md:58": "checked -- `git worktree add -b build/...` is valid git; the path is the legacy layout (#640)",
    ".claude/rules/device-builds.md:90": "not runnable here (a device build); checked: `make docker-RK3566` matches `docker-%` (Makefile:138); the mounts name the legacy checkout (#640)",
    ".claude/rules/device-builds.md:147": "not runnable here (deletes build-root files); a recovery recipe for a warm root",
    ".claude/rules/device-builds.md:244": "not a command (linker output)",
    ".claude/rules/device-builds.md:259": "not runnable here (needs a build root); checked: names `build.ROCKNIX-<DEVICE>.<ARCH>`, where `config/path:19` and `DISTRONAME=\"pixelelated\"` make `build.pixelelated-*` (F-17)",
    ".claude/rules/device-builds.md:324": "not runnable here (no build root in this worktree); a read-only `find`",
    ".claude/rules/device-builds.md:478": "not a command (compiler output)",
    ".claude/rules/device-builds.md:650": "not runnable here (a build); checked: `EMULATIONSTATION_SRC` path is `~/Development/...`, the old ES layout (F-19)",
    ".claude/rules/device-builds.md:674": "not runnable here (needs a build root and a crash address); checked: names the legacy roots and `build.ROCKNIX-*` (#640, F-17)",
    ".claude/rules/engineering-practices.md:665": "ran: passed -- on `key=SECRET` / `name=ok` / `pass = hunter2` it printed `name=ok` only",
    ".claude/rules/engineering-practices.md:687": "ran: passed -- on `token=SECRETX user:alice PASS verdict` it printed `token=*** user:*** PASS verdict`: no value, the verdict kept",
    ".claude/rules/es-code-traps.md:145": "not runnable here (needs the ES tree and a build root); checked: `B=` names the legacy root and `build.ROCKNIX-GENERIC_X64` (#640, F-17)",
    ".claude/rules/es-native-ui.md:317": "not a command (C++)",
    ".claude/rules/es-native-ui.md:414": "not runnable here (an ES checkout and a build root); checked: `tools/es-syntax-check` exists with `--with`; its default root is #699's",
    ".claude/rules/es-ui-style-guide.md:102": "not a command (C++)",
    ".claude/rules/es-ui-style-guide.md:173": "not a command (C++)",
    ".claude/rules/es-ui-style-guide.md:241": "not a command (C++)",
    ".claude/rules/fork-workflow.md:48": "not runnable here (creates a worktree, pushes, opens a PR; D-WORKFLOW-165 defers submissions); checked: `--head maxengel:pr/<name>` names an owner other than `origin`'s `pixelelated` (F-19); worktree paths are the legacy layout (#640)",
    ".claude/rules/fork-workflow.md:129": "not run (writes git config); checked: `git config --get core.hooksPath` reads `/workspace/repos/pixelelated/distribution/.githooks`, which lists `pre-push`",
    ".claude/rules/fork-workflow.md:186": "not runnable here (moves and pushes `next`, the coordinator's); valid git",
    ".claude/rules/generic-x64-vm-testing.md:46": "not runnable here (a build); checked: `docker-GENERIC_X64` matches `docker-%`; the mounts name the legacy checkout (#640)",
    ".claude/rules/generic-x64-vm-testing.md:82": "not runnable here (a guest); checked: `generic-x64-vm` has `run`, `utm` and `--output`",
    ".claude/rules/generic-x64-vm-testing.md:106": "not runnable here (a guest); checked: `--headless`, `--daemonize`, `vm-serial wait`/`sh` exist; the comment's display (`virtio-gpu-pci, -display none`) is the `--gl none` path, not the default (F-16)",
    ".claude/rules/generic-x64-vm-testing.md:129": "not runnable here (a guest); checked: `vm-serial sh` exists",
    ".claude/rules/generic-x64-vm-testing.md:566": "not runnable here (the shared QA backend and a guest); checked: `cloud-test-backend` has `up`, `reset`, `--backend`, `seed-content`, `seed-device` (case arms 402, 593, 843, 869)",
    ".claude/rules/generic-x64-vm-testing.md:706": "not runnable here (`sudo`); a one-time host setup",
    ".claude/rules/generic-x64-vm-testing.md:900": "not runnable here (guests); checked: `vm-qa` has `--skip-up`, `--only`, `--backend`, `--guest`",
    ".claude/rules/generic-x64-vm-testing.md:972": "not runnable here (a guest); checked: `vm-visual-qa` has `--monitor`, `run`, `--outdir`; the socket name differs from the tool's default (a lead)",
    ".claude/rules/generic-x64-vm-testing.md:1207": "not a command (RetroArch log)",
    ".claude/rules/handheld-evidence.md:44": "not runnable here (a device command); checked: `projects/ROCKNIX/packages/rocknix/sources/scripts/rocknix-evidence` has `collect`",
    ".claude/rules/instruction-files.md:24": "not a command (the front-matter template)",
    ".claude/rules/instruction-files.md:80": "ran: passed -- `diff -q .claude/rules/vm-first.md <(git -C /workspace/repos/rocknix show next:...)` rc 0; it reads the legacy checkout's `next` (#640), which is `8ebaf8daad` today",
    ".claude/rules/issue-tracking.md:22": "not run (creates an issue); checked: `gh issue create --repo ... --title --body-file` is valid",
    ".claude/rules/milestone-phase-naming.md:48": "not a command (the title grammar)",
    ".claude/rules/milestone-phase-naming.md:64": "not a command (example titles)",
    ".claude/rules/packaging-and-patches.md:65": "not runnable here (needs a build root); checked: `IMG=build.ROCKNIX-<DEVICE>.<ARCH>` is the old root name (F-17)",
    ".claude/rules/packaging-and-patches.md:82": "not runnable here (writes a patch into a recipe); valid `diff`/`git diff`",
    ".claude/rules/rclone-cloud-sync.md:503": "not a command (rclone output)",
    ".claude/rules/rclone-cloud-sync.md:538": "not runnable here (the shared QA backend and a guest); checked: `cloud-test-backend` `up`/`ls`/`down`/`--backend`, `cloud-round-trip --host --port --identity` exist",
    ".claude/rules/rclone-cloud-sync.md:600": "not runnable here (the shared QA backend and a guest); checked as the block above",
    ".claude/rules/upgrade-and-install.md:73": "not a command (the `Already written:` template)",
    ".claude/rules/worktrees.md:17": "not a command (the legacy layout diagram, #640)",
    ".claude/rules/worktrees.md:45": "not run (`sync` fast-forwards every build worktree, the M7 lane's); checked: `fork-worktree` has `sync`",
    ".claude/rules/worktrees.md:119": "ran: passed for `list` (rc 0, 62 lines); `remove`, `--preserve`, `--force`, `repair` not run (they write); checked: all exist",
    ".claude/rules/worktrees.md:213": "not runnable here (moves `next`, creates a worktree); valid git; legacy paths (#640)",
    ".claude/rules/worktrees.md:222": "not runnable here (creates a worktree); valid git; legacy path (#640)",
    ".claude/rules/worktrees.md:228": "ran: passed for `list`; `remove` and `prune` not run (they write); legacy path (#640)",
    "AGENTS.md:63": "not runnable here (pulls an image, builds); checked: `docker-image-pull`, `docker-shell` targets exist, `docker-package` is `docker-%` running `package` (Makefile:120, 138); the comment's *Rasteratops mirror* is `ghcr.io/pixelelated/build` (Makefile:139; F-08)",
    "AGENTS.md:72": "not runnable here (builds); checked: `RK3588`, `kconfig-menuconfig-%` targets and `scripts/build`, `clean`, `checkdeps` exist",
    "AGENTS.md:82": "not runnable here (builds); checked: scripts exist; the comment *needs OS_VERSION/BUILD_DATE exported* is wrong (F-03)",
    "AGENTS.md:342": "ran: passed -- `pkgcheck rclone` rc 0, `rules-check` rc 0, `register-check` rc 0, `work-log-index --check` rc 0; `ceremony-check --gate` rc 1 on W42 only",
    "CLAUDE.md:65": "not runnable here (as `AGENTS.md:63`); checked as that block (F-08)",
    "CLAUDE.md:74": "not runnable here (as `AGENTS.md:72`); checked as that block",
    "CLAUDE.md:84": "not runnable here (as `AGENTS.md:82`); the comment is wrong (F-03)",
}
blocks = []
for p in open(paths).read().split():
    lines = open(f"{root}/{p}").read().splitlines(); i = 0
    while i < len(lines):
        m = re.match(r"^\s*(```+)(\S*)", lines[i])
        if m:
            j = i + 1
            while j < len(lines) and not re.match(r"^\s*" + m.group(1) + r"\s*$", lines[j]): j += 1
            blocks.append((f"{p}:{i + 1}", m.group(2) or "-", j - i - 1)); i = j + 1
        else:
            i += 1
keys = {b[0] for b in blocks}
if keys != set(V):
    sys.exit(f"t4-blocks: blocks without a verdict {sorted(keys - set(V))}; verdicts without a block {sorted(set(V) - keys)}")
print("| # | Block (file:line at the hash) | Language | Lines | Verdict |")
print("| ---: | --- | --- | ---: | --- |")
cls = {}
for k, (loc, lang, n) in enumerate(blocks, 1):
    v = V[loc]; w = v.split(" --")[0].split(" (")[0].split(";")[0]
    cls[w] = cls.get(w, 0) + 1
    print(f"| B{k:02d} | `{loc}` | {lang} | {n} | {v} |")
print()
print(f"<!-- t4-blocks: {len(blocks)} blocks; " + "; ".join(f"{k} {v}" for k, v in sorted(cls.items())) + " -->")

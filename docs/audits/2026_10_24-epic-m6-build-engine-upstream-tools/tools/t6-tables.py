#!/usr/bin/env python3
"""T6's tables (#653), from one list of 33 groups, so 02's coverage table, 04's
Q6 reachability table and 04's Q4 upstream-state table cannot disagree.

    python3 -I t6-tables.py <worktree> coverage|q6|q4 > out.md

Reads the slice's paths from the inventory with brief § 2's filter, the per-path
syntax result from .qa-scratch/t6/syntax.txt and the upstream state from
.qa-scratch/t6/q4-upstream.txt (both written by the § 5 commands). Asserts 135
paths, every path in exactly one group, and the group file counts summing to 135.
"""
import json, re, sys
from pathlib import Path

T = Path(sys.argv[1]); WHAT = sys.argv[2]
inv = json.load(open(T / "docs/reviews/inventory.json")); cols = inv["columns"]
def gm(p, g): return re.fullmatch(re.escape(g).replace(r"\*\*/", "(?:.*/)?").replace(r"\*\*", ".*").replace(r"\*", "[^/]*"), p) is not None
rows = {r["path"]: r for r in (dict(zip(cols, x)) for x in inv["rows"])
        if r["tree"] == "distribution" and r["area"] == "build-engine"
        and any(gm(r["path"], g) for g in ["tools/**", "distributions/**"]) and not gm(r["path"], "distributions/ROCKNIX/**")}
assert len(rows) == 135, len(rows)
syntax = dict(l.split(" ", 1) for l in open(T / ".qa-scratch/t6/syntax.txt").read().splitlines())
q4 = dict(l.split(" ", 1) for l in open(T / ".qa-scratch/t6/q4-upstream.txt").read().splitlines())

KEPT_585 = "kept: upstream's, unreached; #585 candidate (finding 24's class)"
NOTHING = "nothing: no artifact of it in any checkout or M7 root"
# key: (match prefix, label, path hits, name hits, verdict, disposition, Already written or None, q1, q3, q5, q7)
G = [
 ("tools/adjust_kernel_config", "tools/adjust_kernel_config", "2", "2",
  "reached by `Makefile:31,34` (`kconfig-olddefconfig-%`, `kconfig-menuconfig-%`) and `.github/workflows/update-kernel-configs-docs.yml:72` (red on the fork, T5's PL-15, #657)",
  "kept: called by the `Makefile`", None,
  "no current replacement; `kernel_make` is the engine's own", "line 32 matches the command by substring (`grep ${KERNEL_CONFIG_COMMAND}`): latent, an unknown command that is a substring of a real one passes the check; upstream's", "a developer's `make kconfig-*`; not on a build", "one job, the header says it"),
 ("tools/check_kernel_config", "tools/check_kernel_config", "2", "2",
  "reached by `tools/adjust_kernel_config:38`; also named by the message `packages/linux/package.mk:221` and `projects/ROCKNIX/packages/linux/package.mk:332` print (0 of 28 recorded M7 runs that built `linux` printed it)",
  "kept: called by `adjust_kernel_config`", None,
  "n/a: no current replacement", "no defect read: it applies `distributions/${DISTRO}/kernel_options`, which ROCKNIX carries", "with `adjust_kernel_config`", "one job"),
 ("tools/mtstats.py", "tools/mtstats.py", "1", "1",
  "reached by `config/multithread:64` (after every finished multithread build; T5's E8 made its failure not the build's)",
  "kept: called by `config/multithread`", None,
  "Python 3; no replacement", "no defect read; a failure is now said and not returned (T5 `7abea6eb86`)", "one pipe after each finished build: the statistics of its history file", "one job"),
 ("tools/pkgcheck", "tools/pkgcheck", "14", "1",
  "reached by a document only: `CLAUDE.md:109`, `AGENTS.md:343`, `.claude/rules/packaging-and-patches.md:46`, `packages/README.md:274` (run by hand after every recipe edit; no script calls it)",
  "kept: the documented recipe lint; its exit-on-no-match defect filed as a `bug` (F-02)", None,
  "no current replacement; the fork's `81221658b3` made its status mean something", "F-02: a name that matches no recipe processes nothing and exits 0, like a clean recipe (fixture); its late-binding list omits `SYSTEM_*`/`TOOLCHAIN`-class names (a lead for #657)", "by hand, one recipe at a time; none on a build", "upstream's header and the fork's 3-line comment agree with the code"),
 ("tools/refresh-patches", "tools/refresh-patches", "1", "2",
  "reached by a document only: `packages/README.md:36` (`PKG_NO_REFRESH_PATCHES`); run by hand to regenerate a recipe's patches",
  "kept: documented hand-run tool", None,
  "n/a", "n/a: not run on the fork", "by hand", "one job"),
 ("tools/ffmpeg/", "tools/ffmpeg/gen-patches.sh", "3", "52 (the word `ffmpeg`, not calls)",
  "reached by a document only: `packages/multimedia/ffmpeg/package.mk:14` (`PKG_NO_REFRESH_PATCHES`), a generic recipe no image builds (the ROCKNIX override `projects/ROCKNIX/packages/multimedia/ffmpeg` carries its own patches and does not source it)",
  "kept: upstream's, documented by an unreached recipe; #585 candidate", "nothing: it writes `packages/multimedia/ffmpeg/patches/`, whose last change came from upstream",
  "n/a", "n/a", "by hand", "named by its recipe"),
 ("tools/moby/", "tools/moby/gen-patches.sh", "2", "4",
  "reached by a document only: `packages/addons/addon-depends/docker/moby/package.mk:13`, an add-on dependency no fork image builds",
  "kept: upstream's, documented by an unreached recipe; #585 candidate", "nothing: the fork builds no add-on",
  "n/a", "n/a", "by hand", "named by its recipe and its patch header"),
 ("tools/podman-bin/", "tools/podman-bin/gen-patches.sh", "2", "3",
  "reached by a document only: `packages/addons/addon-depends/podman/podman-bin/package.mk:14`, an add-on dependency no fork image builds",
  "kept: upstream's, documented by an unreached recipe; #585 candidate", "nothing: the fork builds no add-on",
  "n/a", "n/a", "by hand", "named by its recipe and its patch header"),
 ("tools/mkpkg/", "tools/mkpkg/ (10 files)", "0", "1",
  "reached by a document only: the messages `config/functions:1342,1345` (\"use mkpkg\"); no caller",
  KEPT_585, "nothing: it makes source tarballs in the working directory; none in any checkout",
  "n/a", "n/a", "by hand", "the messages name the directory, not a script"),
 ("tools/icon-generate", "tools/icon-generate", "1", "1",
  "reached by a document only: a comment in `packages/addons/service/nqptp/icon/icon-source.svg:7`, an add-on no fork image builds",
  KEPT_585, "nothing: it writes an add-on's `resources/`; the fork builds no add-on",
  "n/a", "n/a", "by hand", "one job"),
 ("tools/distro-tool", "tools/distro-tool", "0", "0",
  "reached by a document only: named in `CLAUDE.md:131`'s list of \"dev helpers\", with no instruction to run it; no caller",
  KEPT_585 + "; `CLAUDE.md:131`'s list is a Q7 lead for the doctrine slice", NOTHING + " (no `release/` directory exists anywhere); it writes work files only while it runs",
  "a bash script with an embedded Python program (LibreELEC's mirror tool, 1,097 lines); no current replacement", "n/a: not run", "never", "`CLAUDE.md:131` presents it beside `pkgcheck` as a helper"),
 ("tools/download-tool", "tools/download-tool", "1", "1",
  "unreached: its only caller, `.github/workflows/update-mirror-sources.yml:30`, is skipped on the fork every week by its repository gate (#644 finding 11; T5's Q6 Table 4)",
  KEPT_585, "nothing that can be told apart: it fills `sources/` through `scripts/get`, as every build does",
  "n/a", "n/a", "never on the fork", "one job"),
 ("tools/update-pkg", "tools/update-pkg", "0", "0",
  "unreached: no caller in the tree; it sources the 62 helpers (`:70`, `:167`)",
  KEPT_585, "nothing: its commits read `<pkg>: update to <ver>` with no trailer, and the twelve fork commits of that shape since the base all carry a `Co-Authored-By: Claude` trailer (sessions, not the tool)",
  "agrees with D-WORKFLOW-193: it writes a `PKG_SHA256` from one fetch (`:61-64`)", "lead: `:63` `curl` without `--fail` would hash an error page; latent, unreached", "never", "two tools beside `scripts/update_packages` (T5's) for one job"),
 ("tools/update-functions/", "tools/update-functions/ (62 files)", "0", "0",
  "unreached: sourced only by `tools/update-pkg:70,167`, which nothing calls (two layers)",
  KEPT_585, "nothing: they run only inside `update-pkg`",
  "n/a", "n/a", "never", "per-package hooks of a tool nobody runs"),
 ("tools/update-scan", "tools/update-scan", "0", "0",
  "unreached: no caller",
  KEPT_585, "nothing: it queries the network and prints",
  "n/a", "n/a", "never", "see `update-pkg`"),
 ("tools/viewplan", "tools/viewplan", "0", "0", "unreached: no caller", KEPT_585, "nothing: it prints the build plan", "n/a", "n/a", "never", "one job"),
 ("tools/viewconfig", "tools/viewconfig", "0", "0", "unreached: no caller", KEPT_585, "nothing: it prints the configuration", "n/a", "n/a", "never", "one job"),
 ("tools/dashboard", "tools/dashboard", "0", "0", "unreached: no caller", KEPT_585, "nothing: it watches a build's thread logs", "n/a", "n/a", "never", "one job"),
 ("tools/pkginfo", "tools/pkginfo", "0", "0", "unreached: no caller", KEPT_585, "nothing: it prints", "n/a", "n/a", "never", "one job"),
 ("tools/packages-checker", "tools/packages-checker", "0", "0", "unreached: no caller", KEPT_585, "nothing: it commits `<dir>: automated code cleanup`, and no fork commit since the base has that subject", "n/a", "n/a", "never", "beside `pkgcheck`: one rewrites, one reports"),
 ("tools/checkunpack", "tools/checkunpack", "0", "0", "unreached: no caller", KEPT_585 + "; lead: `:91` `rm -rf \"${BUILD}/\"*`", "nothing: it empties a build root; the 29 M7 roots are populated", "n/a", "n/a", "never", "one job"),
 ("tools/repo-tool", "tools/repo-tool", "0", "0", "unreached: no caller (it drives `scripts/create_addon`, T5's Table 1)", KEPT_585, "nothing: the fork builds no add-on repository", "n/a", "n/a", "never", "one job"),
 ("tools/change_addon_version", "tools/change_addon_version", "0", "0", "unreached: no caller", KEPT_585, "nothing: it commits `distro: bump ADDON_VERSION`, and no fork commit since the base has that subject", "n/a", "n/a", "never", "one job"),
 ("tools/download-cleaner", "tools/download-cleaner", "0", "0", "unreached: no caller", KEPT_585 + "; lead: it removes cached tarballs", "nothing that can be told apart: a removed tarball is fetched again by the next build", "n/a", "n/a", "never", "one job"),
 ("tools/imgburn.sh", "tools/imgburn.sh", "0", "0", "unreached: no caller", KEPT_585, "nothing in a tree: it `dd`s an image onto a device (`:127`); the fork's route is `docs/device-flashing-runbook.md`", "n/a", "n/a", "never", "a second flashing route beside the runbook"),
 ("tools/upload_to_filebin", "tools/upload_to_filebin", "0", "0", "unreached: no caller", KEPT_585 + "; lead: it sends files to public `filebin.net` bins (its example `release/*.tar`)", "not readable from here: an upload leaves nothing in a tree", "n/a", "n/a", "never", "one job"),
 ("tools/fixlecode.py", "tools/fixlecode.py", "0", "0", "unreached: no caller", KEPT_585, "nothing: it rewrites recipe text in place when run", "Python 3", "n/a", "never", "beside `pkgcheck` and `packages-checker`"),
 ("tools/find_build_warnings.sh", "tools/find_build_warnings.sh", "0", "0", "unreached: no caller", KEPT_585, "nothing: it reports from build logs", "n/a", "n/a", "never", "one job"),
 ("tools/find_build_warnings_ignore.conf", "tools/find_build_warnings_ignore.conf", "0", "0", "unreached: read only by `tools/find_build_warnings.sh:12`, which nothing calls", KEPT_585, "nothing: data", "n/a", "n/a", "never", "its tool's data"),
 ("tools/docker/", "tools/docker/ (7 files)", "0", "52 (the word `docker`: the add-on and `make docker-*`, not this path)", "unreached: no caller; the fork's container is the root `Dockerfile`, built by the mirror workflow and pinned in the `Makefile` (T5)", KEPT_585, "nothing in a tree: an image built from one of these lives in a local Docker store, which this lane does not read", "six other distributions' containers", "n/a", "never", "`README.md` describes containers the fork does not use"),
 ("tools/RPi/", "tools/RPi/ (2 files)", "0", "29 (the word `RPi`, not calls)", "unreached: no caller; they rebase Kodi for Raspberry Pi, which the fork does not build", KEPT_585, "nothing: the fork carries no Kodi", "n/a", "n/a", "never", "one job each"),
 ("distributions/LEIoT/", "distributions/LEIoT/ (11 files)", "1 (a record: `docs/rasteratops/p0-sweep-hits.txt`)", "0", "unreached: read by `config/options` only when `DISTRO=LEIoT`, and `config/options:24` (`DISTRO=\"${DISTRO:-ROCKNIX}\"`) is the only setter; the positive control is `distributions/ROCKNIX/`, reached by the same lines", KEPT_585, "nothing: no `build.LEIoT-*` root in any checkout", "n/a", "n/a", "never", "another distribution's identity"),
 ("distributions/LibreELEC/", "distributions/LibreELEC/ (16 files)", "1 (the same record)", "1,542 (the word `LibreELEC`: copyright headers, not selections)", "unreached: as LEIoT, `DISTRO=LibreELEC` is set by nothing", KEPT_585, "nothing: no `build.LibreELEC-*` root in any checkout", "n/a", "n/a", "never", "another distribution's identity"),
]
# per-path cells where one file of a group differs from its group
PATH_Q3 = {"distributions/LEIoT/kernel_options": "F-03: a symlink to `distributions/LibreELEC/kernel_options`, relative to its own directory, so it dangles (since LibreELEC's `4130b59b50`, 2025-04-10; identical upstream); only a `DISTRO=LEIoT` build reads it"}
def group_of(p):
    for g in G:
        if p == g[0] or (g[0].endswith("/") and p.startswith(g[0])): return g
    raise SystemExit("no group: " + p)
counts = {}
for p in rows: counts[group_of(p)[0]] = counts.get(group_of(p)[0], 0) + 1
assert sum(counts.values()) == 135 and len(counts) == len(G), (len(counts), len(G))

if WHAT == "coverage":
    print("| Path | Tier | Lines | Q1 | Q2 | Q3 | Q4 | Q5 | Q6 | Q7 |")
    print("| --- | --- | ---: | --- | --- | --- | --- | --- | --- | --- |")
    for p in sorted(rows):
        r = rows[p]; g = group_of(p)
        q2 = syntax.get(p, "n/a: not a script (" + (r["language"] or "data") + ")")
        q4s = q4[p] if q4[p] == "identical" else "differs: the fork's `81221658b3`"
        q4c = "Q4: " + q4s + " to `upstream/next`"
        cell = lambda s: s.replace("|", "\\|")
        print(f"| `{p}` | {r['tier']} | {r['lines'] or 0} | {cell(g[7])} | {cell(q2)} | {cell(PATH_Q3.get(p, g[8]))} | {q4c} | {cell(g[9])} | {cell(g[4].split(':')[0] if g[4].startswith('unreached') else g[4][:140])} | {cell(g[10])} |")
elif WHAT == "q6":
    print("| Tool or directory | Files | Path hits | Name hits | Verdict | Tier | Q4 | Disposition | Already written |")
    print("| --- | ---: | --- | --- | --- | --- | --- | --- | --- |")
    for g in G:
        ps = [p for p in rows if group_of(p) is g]
        tiers = sorted({rows[p]["tier"] for p in ps}); q4s = sorted({q4[p] for p in ps})
        aw = g[6] if g[6] else "n/a: reached"
        if g[4].startswith("unreached"):
            assert g[6], g[0]
        print(f"| `{g[1]}` | {len(ps)} | {g[2]} | {g[3]} | {g[4]} | {', '.join(tiers)} | {', '.join(q4s)} | {g[5]} | **Already written:** {aw} |")
    print(f"\nRows {len(G)}, files {sum(counts.values())}.")
elif WHAT == "q4":
    print("| Path | Against `upstream/next` (`e0f9deb899`) | The fork's commits since the base |")
    print("| --- | --- | --- |")
    for p in sorted(rows):
        print(f"| `{p}` | {q4[p]} | {'`81221658b3` pkgcheck: exit non-zero when any check failed' if q4[p] != 'identical' else 'none'} |")
    print(f"\n{sum(1 for p in rows if q4[p] == 'identical')} identical, {sum(1 for p in rows if q4[p] != 'identical')} differs.")

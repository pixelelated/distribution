# Analysis: M6.P2 T37, the EmulationStation recipe and themes in the distribution (#684)

Stage C, 2026-11-01, the T3 session (Opus 5.5, high), at `reviewed-at` `9fa740a91b` (the slice's
bytes `2174265e9c`'s); `reviewed-at-es: none -- no ES change`. The evidence is `02` and its records;
this file answers the brief's Q1 to Q7 at their lines and states what the slice found.

## Executive summary

The 15 files build and install the interface correctly in the ways an image shows -- on the
candidate guest the four seeds and the three scripts are byte-identical to the tip's, the French
catalog and the pre-generated locale are present, the theme resolves as ES's default, and the state
check passes with only D-WORKFLOW-166's shared identity -- and they carry **four defects a check now
catches and nothing caught before**: the `es_systems.cfg` link to a build-host path (PL-01, #613),
`cpugov.patch` reached on no device (PL-02, #1072), `PKG_NEED_UNPACK`'s bare word (PL-03) and a
no-op `rm` (PL-04). Beside them: **upstream's ARMSX2 block lost in four merges** (PL-05), **fribidi
not linked in the candidate though the plan supplies it** (PL-06), two quiet guards (PL-07, PL-08),
an inert flag (PL-09), the checkers that do not reach these recipes (PL-10), and the currency and
doc findings (PL-11 to PL-16). Sixteen items, none above Medium; every disposition is proposed for
the stage-D pause.

## Acceptance-criteria scorecard

The 21 checkboxes of the brief's § 7 (#684's body), at stage C.

| # | Checkbox (short) | State at stage C | Artifact |
| --- | --- | --- | --- |
| 1 | the folder's files | partly: `00`-`05`, `second-opinions/`, `stage-a/` to `stage-c/`, `tools/`, `guest-cycle/` present; `stage-d/`, `stage-e/` to come | `ls` of the folder |
| 2 | the lint `PASS` both phases and with `--issue` | the pre-issue phase at stage C; the rest after stage D | `tools/lint-audit-artifacts` |
| 3 | the review plan, the probe and refutation receipts, the manifest | at stage C's end | `second-opinions/` |
| 4 | the punch-list issue at Phase 7 | stage D onward | the audit issue |
| 5 | the header fields and no `PKG_VERSION`/`PKG_GIT_CLONE_BRANCH` change | `reviewed-at` written in `00`; no lane commit touches `ui/` | `git diff --stat 94d8ef8e7e HEAD -- packages projects tools` (no line) |
| 6 | `01` § Scope with the block and its sha | met | `01` § Scope |
| 7 | `02` § Coverage 15 rows | met | the checkbox's `awk`: `15` |
| 8 | `02` § The runs | met for stages A to C | `02` § The runs |
| 9 | `tools/t37-checks.sh` FAIL-first and at the tip | met | `stage-c/failfirst.out`, `stage-c/checks-at-tip.out` |
| 10 | `02` § The recipe | met | `02` § The recipe |
| 11 | `02` § The dependencies | met | `02` § The dependencies |
| 12 | `02` § The themes and `lowerdeck` | met | `02` § The themes |
| 13 | `02` § The patches | met | `02` § The patches |
| 14 | `02` § The currency | met | `02` § The currency |
| 15 | `02` § The guest cycle | met | `02` § The guest cycle |
| 16 | `00` shows what never ran | met to stage C | `00` |
| 17 | `04` answers, bugs with their traces | the answers here; the bugs at stage D | this file; the bugs |
| 18 | `proved:` cells; `question:` per item | met | `02`, `05` |
| 19 | the retro | stage G | -- |
| 20 | the five checkers before the hand-back | stage H | -- |
| 21 | the collisions named in the hand-back | stage H | -- |

## Risk assessment

- **On the image a player has today, the risks are small**: the candidate the M7 line shipped
  corrects the link itself, carries the catalog and the locale, and its binary carries no stray
  credential pair. The tip's recipe, built as it is, would ship the dangling link (PL-01) -- the
  fallback ES uses when the player's own `es_systems.cfg` is missing.
- **The silent ones are the risk to the next image**: a patch that never applies (PL-02), a stamp
  that never moves (PL-03), a dependency taken by order (PL-06), a catalog that can vanish (PL-07).
  Each fails without a message; the checker now catches four of them before a build.
- **The merge debt** (PL-05, PL-14) is the largest change waiting: the ES recipe and `essway.service`
  conflict with upstream on the next merge.

## Coverage boundary

- **Read:** the 15 files whole (the ES recipe with `:39` withheld by number); the pin's CMake, the
  sources the questions reached, by hash; the build engine's scripts the recipes depend on; the
  build's own plan computed in a scratch export; the candidate image on one guest and its `SYSTEM`
  on the host.
- **Not read, and why:** the four patches' text beyond what the recipe reaches (T40's, T42's); ES's
  sources beyond the cited lines (the `es-*` slices'); `/workspace/repos/rocknix` (M7's), so the
  candidate's nine ES patches are cited from R3, not read; the authors' current repositories (no
  fetch, ruling (e)).
- **`CANNOT` here, the integration's:** a stamp after a real build, the `USING:` lines, the gettext
  pass, the CMake cache (`HAVE_FRIBIDI`, `HAVE_INTL`, `HAVE_UDEV`), the tip's recipe output, the H700
  and SM8550 branches on an image, upstream's RK3566 patch applied.

## The questions

### Q1 The pin and its bump

The pin is `16dbac5211eea7e70db7394372033be2be7df829` on `test/qa-integration` (`:5`, `:6`), cloned
from `https://github.com/pixelelated/emulationstation` (`:8-9`, `:17`); ROCKNIX's recipe pinned
`cada856d86` at the base and `f6c542872e` now; the pin lacks 14 of `rocknix/master`'s commits and
is 724 ahead (`02` § The recipe, Q1). No merged ES tip exists; the bump's steps are stated and none
is taken here (ruling (b)). The candidate is the same pin plus nine patches (ruling (h)); the
sidecar carries no pin (#1013). L-17's rule drift is PL-15.

### Q2 The build options, the renderers and the install steps

One row per `-D` (`:19-25`, `:30`, `:33`) with its CMake test and branch, and the derived defines
(`02` § The recipe). `:25`'s `-DGLES3=1` selects `GLSystem "OpenGL ES 3.0"`, which both adds
`-DUSE_OPENGLES_30` and lists `Renderer_GLES30`; the define compiles nothing; the list is T35's and
the bodies T36's. Every device's mesa enables GLES 2. NDEBUG is the build system's
(`config/functions:385-388`). One row per install step; the defects are PL-01 (`:101`), PL-04
(`:79`), PL-07 (`:67-68`), PL-11 (`:54`), PL-12 (`:73-75`); PL-09 is T2's PL-029 with its sibling
at `emustation.service:12`; #1193's half is the seeds' `cp -a` from `100644` (`644` on the guest).

### Q3 The dependencies

The effective `PKG_DEPENDS_TARGET` is the same 19 wants on GENERIC_X64 and H700, ending `zstd mesa`
(`02` § The dependencies). fribidi, udev (through `systemd`) and the gettext tools all arrive by
build order; pugixml is the system library; `busybox`'s word in `PKG_NEED_UNPACK` names nothing
(PL-03). fribidi's question is D-WORKFLOW-216's and the pause's (PL-06).

### Q4 The build credentials, by name

Five lines name the build's credential variables (`:30`, `:40`, `:42`, `:43`, `:44`), each a
*build-variable name*; `:39`'s value is never printed or sent, and `:40` carries only names and
references. The recipe passes no credential to cmake; `get_env` forwards four names and the loop
logs three (PL-08). The candidate's binary passes the state check with the one allowed shared
identity. #64's `:54` cannot be answered from this recipe (it always passes the runtime flag);
#586 is not a current gate. PL-16 is the state check's host route.

### Q5 The themes and `lowerdeck`

The theme is at its author's `HEAD` and `upstream/next`'s pin, by hash (`PKG_SHA256` equal to the
cached tarball's); its install steps, T42's patches (all reached), the wordmark and its licence,
and the default theme (`system-theme` -> the shipped theme) are stated at their lines; all 25
`fontPath` elements carry a `fontSize` and name bundled fonts (L-22). `lowerdeck` is behind its
author's `HEAD` (PL-13), installed by `PKG_UI`, used by three run-time scripts outside the slice.

### Q6 The patches and their directories

30 rows over 15 devices: the ES recipe's `patches/x86_64/` reached on none (PL-02), the theme's
`patches/` on all; T37's line is `PKG_PATCH_DIRS`, the patch T40's. L-18's doc drift is PL-15.

### Q7 Package currency, the structure and the #585 lines

14 rows: six upstream changes the fork lacks, six of the fork's own, two that both moved (PL-14);
the ES 14 are #791's; the ARMSX2 block (PL-05); the checkers' reach (PL-10); the licence (L-16,
#990); four #585 lines (L-03, L-06, L-19, PL-029), written in `02`, never sent.

## The take-up table (brief § 2), each row disposed

`02` § The leads, *The take-up (§ 2), one row each*: 22 rows, each with its disposition; the items
it raises are PL-01 (#613), PL-02 (#1072), PL-06 (D-WORKFLOW-216), PL-09 (PL-029).

## Renovation face

The plan's seven questions, answered from the brief's.

### Q1 Modernize

The recipes use the build system's current forms except `PKG_NEED_UNPACK` (PL-03) and the patch
directory (PL-02), whose framework forms exist (`get_pkg_directory`, `PKG_PATCH_DIRS`).

### Q2 Standards

`tools/pkgcheck` passes all three by name; `bash -n` passes the seven; the install link (PL-01) and
the no-op `rm` (PL-04) are the standard lapses, each now asserted by the checker.

### Q3 Bugs

PL-01, PL-02 and PL-05 are the defects with an effect on an image; PL-06 is the build-order
decision; PL-03 the stamp; the rest are guards and notes.

### Q4 Package currency

The theme is current; `lowerdeck` is behind (PL-13); the ES recipe's currency moves with the ES
merge (#791); upstream's six `ui/` changes wait for the distribution merge (PL-14); no tool
measures these three (PL-10).

### Q5 Efficiency

Boot to interface: `essway.service` at 5.37 s, ES at 5.82 s (G-04); the pre-generated locale keeps
`localedef` off first boot. PL-03's fix would rebuild ES when busybox changes, which is its point.

### Q6 Dead ends

The inert `--log-path` (PL-09); the commented link at `:93`; the no-op `rm` (PL-04); a patch that
never applies (PL-02).

### Q7 Clarity and structure

The recipe says what it does except at `:79`, `:101` and `:14`; the two rules that describe it
otherwise are PL-15.

## Instruction File Recommendations

Proposals for the coordinator (the lane edits no rule):

- `device-builds.md` § Iterating on EmulationStation: the fork's repository name (`:8`) in place of
  `maxengel/emulationstation-next` (PL-15).
- `CLAUDE.md`'s package rules: *"scope per device with `patches/<DEVICE>/` -- reached only where the
  recipe sets `PKG_PATCH_DIRS`"* (PL-15).
- `engineering-practices.md` § The form: a census by process name counts the kernel's 15-character
  name (`qemu-system-x86`), never `qemu-system-x86_64`, which matches nothing (this slice's stage-A
  and B censuses; corrected in `00`).
- The brief kit's read mask: *"through the mask, and `:39` withheld by line number"* (the
  coordinator's answer 3).

## Second opinion

Pending at the time of writing: the probe and the refutation run at stage C's end; their outcome is
written here before the pre-issue lint.

## Quality self-check

- Every count in `02`, `04` and `05` is a tool's line in a named file; the three generated tables
  and the punch list's generator each failed on a constructed drift first.
- The checker failed on the tip, passed the fixed fixture and caught all 15 mutations before its
  verdict at the tip was trusted (`stage-c/failfirst.out`).
- No value of a credential is in any artifact: the hooks' patterns count `0` over the folder after a
  planted positive matched `1`; `:39` and `:40`'s value parts occur `0` times.
- What the lane did not check is said: the `CANNOT`s above, the candidate's nine patches (R3's),
  the authors' current `HEAD`s (R1 C20's, dated).

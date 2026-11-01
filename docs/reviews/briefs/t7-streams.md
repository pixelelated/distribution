# T7's remediation stream (#654, audit issue #884)

Written by the coordinator at T7's stage-D pause (2026-10-24, 10:57 UTC post
at `e5beaa6064`; D-WORKFLOW-189). Fifteen items, one stream: the slice is a
currency table, and the only changes a table may carry are a `PKG_URL` line
in a recipe the fork owns (brief § 2: *a `PKG_URL` or `PKG_SHA256` line is a
fix the table can carry; a bump is not*). Everything else is a disposition
below. Plan § 6b E binds the stream: **a commit names its paths**; **a time
is produced, never typed**; **prose goes into a running log through a
quoted heredoc or the Write tool, never an unquoted one** -- the lane's own
incident of 10:44 (an unquoted heredoc ran every backticked name in its
prose, `scripts/update_packages` among them, which rewrote a recipe in the
worktree before the revert) is now a plan § 6b E bullet, and the stream's
first act is to re-read that line.

## S1. Three `PKG_URL` lines in fork-introduced recipes (PL-13, PL-14's `dmidecode`) -- `fix-tree`

- **Why a stream:** the three recipes are the fork's (added by it, absent
  upstream: `04` § Q7 rows 4, 10 and 15), so there is no upstream copy to
  propose to and the fix is ours; each is one line; none moves a pin or a
  checksum.
- **Files owned:** `packages/web/libsoup/package.mk:9` and
  `packages/devel/ruby/package.mk:10` (PL-13: `${PKG_VERSION:0:3}` cuts the
  series by a fixed width, so `3.10.0` would fetch from `3.1/`; the shape
  that holds is `glib-networking:6`'s `${PKG_VERSION%.*}`, or ruby's
  declared-series form where the recipe already names the series for the
  freshness tool), and `packages/sysutils/dmidecode/package.mk:11` (PL-14:
  the one http `PKG_URL` the fork owns; https, the same path). Nothing else:
  `syslinux`'s edited copy keeps upstream's URL (its hunk is #585's), and the
  twenty other http URLs and the five renamed or forked repositories are
  upstream's rows.
- **The test first**, each output pasted on #654 and in `02`: for each of
  the three, the URL as the build expands it (`PROJECT=ROCKNIX
  DEVICE=GENERIC_X64 ARCH=x86_64 bash -c '. config/options <pkg> >/dev/null
  2>&1; printf "%s\n" "$PKG_URL"'`) before and after; a fetch of the
  expanded URL into an empty directory under `.qa-scratch/t7/s1/` whose
  sha256 equals the recipe's unchanged `PKG_SHA256` (before: the same bytes
  from the old URL, so the change is transport or derivation only); for
  PL-13, the derivation shown on a synthetic two-digit minor (`PKG_VERSION=3.10.0`
  in a subshell: the old form prints `3.1`, the new prints `3.10`) -- the
  fixture that fails against the unfixed line.
- **The change:** the three lines, each with no comment unless the
  derivation needs one word; `tools/pkgcheck` on each recipe after. **A
  `PKG_URL` change restamps the package** (`calculate_stamp` hashes the
  recipe directory): say so in each commit; the next build rebuilds the
  three, and the bytes it fetches are the ones the test fetched.
- **Already written:** nothing on devices; a recipe's text. The shared cache
  keeps its stamps; the same bytes come from the new URL.
- **Acceptance (PL-13, PL-14's `dmidecode` row):** both `PKG_URL` lines
  derive the series without a fixed width and expand to the URL they give
  today; `dmidecode`'s is https and expands to an archive with the same
  sha256; `tools/pkgcheck` exits 0 on the three; `git diff --stat 8ebaf8daad
  HEAD -- packages` shows the three files and nothing else.
- **Commit** per recipe, `<package>: <text>`, `Refs #884, #654` (PL-13 and
  PL-14 have no `bug` issue: Renovation items), the attribution line;
  `git add -- <the one file>`; `git status --short` empty after.

## Dispositions that are not streams (the coordinator's, written into the Phase 7 table by the lane)

- **PL-01 (#877):** resolved by the packet `fix/m6-877-libfmt-sha256`
  (`cf3a8d8e62`), reviewed, merging before T5's branch; `fix-tree`.
- **PL-02 to PL-05 (#880 to #883, the four dead primary URLs):** deferred to
  **#585** (the recipes are LibreELEC's through ROCKNIX; a new URL that
  serves the same bytes is not known for any of them -- `wsdd2`'s new home
  has no 1.8.7 tag -- so the fix is upstream's to choose and the mirror
  covers the fetch meanwhile). Each bug stays open, Low, with the mirror
  named, until a URL exists or the row is accepted as mirror-only by a
  register row; the coordinator posts the four on #585 with #844 as the
  guard.
- **PL-06 to PL-09 (the four fork-introduced recipes behind their
  projects):** deferred to **one Backlog issue in #839's shape** (the
  coordinator files it at this pause: brotli 1.2.1, ruby 3.3.13,
  glib-networking 2.90.1, webkitgtk 2.54.2 -- the last the costly build,
  `device-builds.md` § Before a build); no pin moves in M6.
- **PL-10 (the sixteen #645 rows):** the table in `04` § Q7 is posted on
  #645 by the coordinator; the slice moves nothing.
- **PL-11 (`btrfs-progs`):** deferred to #879.
- **PL-12:** withdrawn, as the lane did.
- **PL-14's twenty upstream http URLs and PL-15's five repositories:**
  deferred to #585 (one proposal, the coordinator posts it; the three edited
  upstream recipes' hunks -- libyaml, libsamplerate, syslinux -- go in the
  same proposal, as `04` § Q7 rows 1, 2 and 13 say).

## Order and hand-back

S1, then stage F (`02` appended, every proof's `proved:` cell one of `tree`,
`fixture`, `fix-tree`, `fix-pending-image`), stage G (the retro: what the
slice did to the two time-to-play numbers -- nothing, say so), stage H (the
hand-back on #654, `reviewed-at:`/`fixed-at:` in its body). The coordinator
accepts by brief § 10 (the membership block, the (a) loop and the `pkgcheck`
baseline in full on an export; the (b) loop and the HEAD probe on twenty
seeded rows; `register-check` on a simulated merge) and closes #884. **A
stream that would change a recipe outside the three named, a pin, a
checksum or anything under `projects/` stops and asks on #654.**

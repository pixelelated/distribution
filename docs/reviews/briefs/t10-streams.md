# T10's remediation streams (#657, audit issue #958)

Written by the coordinator on 2026-10-24 at T10's stage-D pause
(D-WORKFLOW-189), in the shape of `t9-streams.md`: ten streams, each with the
files it owns, the test first, its `Already written:` line, its acceptance and
its commits; then the dispositions that are not streams, which the lane writes
into the Phase 7 table; then the order and the hand-back. The lane executes in
its worktree (`/workspace/repos/pixelelated/distribution.worktrees/m6-tooling-guards-657`,
branch `feature/m6-tooling-guards-657`, stage-D tip `cc7eb5ca68`). **Review
depth per stream: Local** (plan § 6c), with one rule the security list adds:
**a stream on a hook lands with the `hooks-test` case that fails on the unfixed
hook and passes on the fixed one, or it is not a stream** (the tooling futro's
T10 addendum; `fork-workflow.md` § Safety net). Every constructed input is a
recipe built at run time from `printf` pieces and a stand-in list
(`FORBIDDEN_TERMS_FILE` pointing at the suite's own file, as `hooks-test`
does), in a throwaway repository under `.qa-scratch/t10/`, never the fork's
repository, never the real list, never a credential-shaped literal at rest
(blindspot 67; `.githooks/pre-commit` refuses one anyway). **Nothing here
pushes beyond the lane's branch, runs `fork-worktree sync|remove|repair` or
`pr-stack-check` against the fork's repository, triggers a workflow, writes a
secret, or edits the primary checkout's `.githooks/`.** The hooks the lane's
own commits run are the primary checkout's copy (`core.hooksPath`), so a
fixed hook is proven by `hooks-test` in the worktree, not by committing with
it. Three contract choices are decided here and recorded as D-WORKFLOW-200,
D-WORKFLOW-201 and D-WORKFLOW-202 (the register, the same session), each
reversible by a revert before the merge, each put to the maintainer on #346
the same hour.

**What the lane found, in one sentence each, so the streams read in order:**
the hooks' diff reader skips binary-detected files, `.po`/`.pot`, and content
lines it mistakes for file headers (F-01, F-02, F-35: three Highs); the push
guard's new-branch range is set by date and its `pr/*` base can fall back to
the fork's own `next` (F-36 High, F-41); `fork-worktree` forces every removal
and destroys what `--preserve` was told to keep (F-42, F-11: two Highs); and
eleven checkers read less than they report and pass (F-04, F-05, F-07, F-08,
F-09, F-19, F-20, F-21, F-44, F-06, F-15). Two leads (F-16, F-30) and two
Renovation items (F-31, F-34) were held for the coordinator and are
dispositioned below.

## S1. `guard-lib`'s diff reader scans every added line: binary-detected files, `.po` and `.pot`, content lines that look like headers, quoted paths, `#` message lines (PL-01, PL-02, PL-35, PL-10, PL-03; #929, #930, #931, #937's path half, #938) -- `fix-case`

- **Why a stream:** three Highs and two smaller gaps in one reader
  (`guard_added_lines`, `guard_scan`, the `--name-only` match). Each is a
  line the guards never read; the fix is to read it. **No widening of a
  pattern here** (that is S3): this stream changes what reaches the scan,
  not what the scan matches.
- **Files owned:** `.githooks/guard-lib`, `.githooks/pre-commit`,
  `.githooks/commit-msg`, `.githooks/pre-push` **only where it calls the
  reader** (the range and base logic is S2's), `.githooks/hooks-test`.
- **The shape:** the diff is taken with `--text` (so a file git detects as
  binary is diffed as text and its added lines scanned; a file that is truly
  binary yields no matchable line and costs nothing); the `.po`/`.pot`
  exemption is removed unless the lane finds its recorded reason
  (`git show -s f51d081c04` found none; the French catalog is text and a
  stand-in word in it is a listed word); the parser recognises a file header
  only at the file-header position (after `diff --git`, before the first
  `@@`), so an added content line beginning `++ b/` is content; the
  personal-path match reads `git diff --name-only -z` and matches the bytes
  git gives, quoted or not; `commit-msg` scans the message as git will store
  it -- with `-m`, `#` lines are kept, so they are scanned; over-refusing a
  stripped line is the safe branch. A type change (file to symlink and back,
  the seats' narrowing of F-01) is read as a changed path and its new
  content scanned.
- **The test first** (each a `hooks-test` case, built at run time, failing
  on the unfixed hooks and passing on the fixed ones; the failing runs
  quoted in `02`): a file with a NUL byte and a stand-in word, committed
  (the pre-commit must refuse), then committed again removed and the branch
  pushed (the push guard must refuse the range); a `.po` with a stand-in
  word; a hunk that deletes a line beginning `-- ` and adds one beginning
  `++ b/` carrying a stand-in word; a quoted path under `docs/` on a `pr/*`
  branch (refused as a personal path, not only as unreadable); a `-m`
  message whose `#` line carries a stand-in word. The 22 existing cases
  still pass.
- **Already written:** the fork's history was scanned by the push guard
  with these gaps; whether any line slipped through is answered once, by
  running the fixed scanner over the whole of `next`'s fork history
  (`c445081a59..8ebaf8daad`, the `whole=1` path) **with the stand-in list
  replaced by the real one only through the tool's own redaction** -- the
  run prints file and line, never the line -- and the count recorded in
  `02` (0, or each hit named by file:line for the coordinator). Nothing on
  a device or in a cloud.
- **Acceptance (#929, #930, #931, #937's first criterion, #938):** the five
  new cases by name with their failing and passing runs; `hooks-test` PASS
  with its new count; the whole-history run's count.
- **Commits:** `hooks: the diff reader scans binary-detected files, .po/.pot and header-shaped content lines (#929, #930, #931)`,
  `hooks: personal paths matched from -z names; commit-msg scans # lines (#937, #938)`,
  each `Refs #<bugs>, #657`, the attribution line.

## S2. `pre-push`'s range and base: the exclusion set scanned whole, no fallback to the fork's `next`, tag annotations, one redaction, the empty conditional (PL-36, PL-41, PL-37, PL-38, PL-34; #932, #937's base half, #933, #934; D-WORKFLOW-200) -- `fix-case`

- **Why a stream:** a High (a new branch's range from the oldest commit by
  date leaves a parent dated after its child unscanned) and three Mediums
  in the same logic.
- **Decided (D-WORKFLOW-200):** the push guard's coverage contract is **every
  commit the push would make reachable from a remote ref, every message,
  and every tag annotation, with no fallback that reads a smaller set**: a
  new branch's range is the set of commits not reachable from any ref the
  remote already has (`git rev-list <tip> --not --remotes=<remote>`, the
  `whole=1` path's own shape, as the lane named in #932), in topological
  order; a `pr/*` push with no `upstream/next` in the clone is **refused**
  with the fetch command printed, never judged against `origin/next`; an
  annotated tag's message is scanned when a `refs/tags/` ref is pushed; a
  line matching both scans is reported as `file:line [REDACTED]`, the
  listed word never printed.
- **Files owned:** `.githooks/pre-push`, `.githooks/hooks-test`. Also in
  this stream, two hygiene lines of the same file: `pre-push:337`'s
  `if true; then` (read `git log -S'if true' -- .githooks/pre-push` first;
  remove the conditional or give it its condition, and say which in the
  commit); and the `'tools/fork-newdrive'` entry of `PERSONAL_PATTERNS`
  removed (D-INFRA-030; T9's S8 retires the tool and its rule entries on
  T9's branch, which merges before this one). The header's
  `../rocknix.worktrees/` lines are #640's (PL-32) and stay.
- **The test first:** a branch whose oldest commit by date is not its root
  (two commits with `GIT_COMMITTER_DATE` reversed) carrying a stand-in word
  in the parent: refused by the fixed guard, allowed by the unfixed; a
  clone without `upstream/next` pushing a `pr/*` branch with a personal
  path: refused with the fetch hint; an annotated tag whose annotation
  carries a stand-in word: refused; a line carrying a credential shape and
  a stand-in word: the refusal prints neither. Each case fails on the
  unfixed hook.
- **Already written:** the same whole-history scan as S1's covers the
  commits; tags already on `origin` are listed (`git ls-remote --tags
  origin`, 0 expected) and each annotation scanned once by the fixed
  reader, the count in `02`.
- **Acceptance (#932, #937's second criterion, #933, #934):** the four
  cases by name; the `if true` line's disposition in the commit message;
  `hooks-test` PASS.
- **Commits:** `hooks: pre-push scans the whole exclusion set, refuses a pr/* push without upstream/next, reads tag annotations, redacts both shapes (#932, #937, #933, #934)`
  and `hooks: pre-push's empty conditional; the fork-newdrive pattern retired (#657, D-INFRA-030)`.

## S3. `secret-patterns` matches the two missed shapes; a listed word in a file name is refused (PL-39, PL-40; #935, #936) -- `fix-case`

- **Why a stream:** two Mediums on the security list, each a shape the
  fork handles (`rclone.conf`'s `pass =`, a Google refresh token beginning
  `1//`) or a channel nobody scanned (a path).
- **Files owned:** `.githooks/secret-patterns`, `.githooks/guard-lib` (a
  name scan beside the line scan), `.githooks/hooks-test`;
  `tools/forbidden-terms-check` **only for the file-name half**, which S6
  owns with the rest of that tool: S3 adds the hook side, S6 the tool side,
  and S3 runs first.
- **The shape:** a pattern for a lowercase assignment with a long value
  (`password = <long>` and `pass = <long>`), and one for a JSON or INI
  token value carrying `/` (the `1//` shape); **every widening lands with
  the line it now catches and a line it must still pass** (a placeholder in
  angle brackets; a sentence using the word in prose; a short value), per
  `engineering-practices.md`. The added or renamed paths' names are scanned
  against the wordlist (never against the credential patterns, which judge
  a value after its label), at commit and at push.
- **The test first:** the two new credential shapes refused and the three
  control lines allowed; a file whose name is a stand-in word refused at
  commit and at push; the existing cases pass. The lines are built with
  `printf` pieces; no literal at rest.
- **Already written:** the whole-history scan of S1 is re-run after this
  stream with the widened patterns (a second count in `02`, hits by
  file:line only); file names in history are listed by `git log
  --name-only --format=` and scanned once against the real list through the
  tool, count recorded.
- **Acceptance (#935, #936):** the cases by name; the control lines named;
  `hooks-test` PASS.
- **Commit:** `hooks: lowercase and slash-bearing credential shapes; a listed word in a file name is refused (#935, #936)`.

## S4. `fork-worktree`: `--preserve` stops on a failed move, `remove` forces only on `--force`, `repair` carries back every untracked path, `sync` returns what happened, the no-directory loop ends (PL-11, PL-42, PL-12, PL-13, PL-14; #939, #940; D-WORKFLOW-201) -- `fix-case`

- **Why a stream:** two Highs and three others in the one tool whose job is
  to not destroy build output (D-WORKFLOW-005, `worktrees.md` § Removing a
  worktree). The intent read (`bcf03f7338`, the tool's first commit) found
  the always-`--force` with no reason recorded, against the rule's own
  words (*`--force` only after it has told you what dies*).
- **Decided (D-WORKFLOW-201):** `fork-worktree remove` **runs `git worktree
  remove` without `--force` unless the user gave `--force`**, and gives it
  only after the tool's own build-output refusal has passed, so git's
  untracked-file refusal is a second guard, not a bypassed one; `--preserve
  <dir>` **stops with nothing removed when a move fails** (exit non-zero,
  the failed path named); `repair` carries back **every** untracked path
  (`git ls-files --others` over the orphaned directory, or a full walk), not
  the top-level entries the fresh checkout lacks; `sync` sets its exit from
  what it skipped or failed; `--preserve` without a directory is a usage
  error, exit 2.
- **Files owned:** `tools/fork-worktree`; a new control `tools/fork-worktree-test`
  (a fork tool: the stream adds its entry to `PERSONAL_PATTERNS`,
  `fork-workflow.md`'s list and `instruction-files.md`'s index -- rule
  edits under this brief; `tools/rules-check --quiet` must pass).
  **Read first** how the tool finds its repository: if it resolves from the
  current directory (`git rev-parse --git-common-dir`), the control runs it
  inside a throwaway repository under `.qa-scratch/t10/`; if it hardcodes
  the primary checkout (the `:72,74` hints are #640's), the stream makes it
  resolve from the current directory and says so, because a control that
  cannot be pointed at a throwaway cannot exist.
- **The test first**, in the throwaway repository only: a worktree with an
  uncommitted edit, `remove` without `--force`: refused by git, the edit
  intact (the unfixed tool destroys it: the positive); with `--force`:
  removed; a worktree holding a `build.*` directory: refused by the tool
  before git is asked, with and without `--force`; `--preserve <dir>` with
  the move made to fail (a read-only destination): nothing removed, the
  path named (the unfixed tool removes: the positive); `repair` over an
  orphaned directory with an untracked file three levels deep: the file is
  back; `sync` with one worktree skipped for uncommitted changes: exit
  non-zero; `--preserve` with no directory: exit 2 within a second.
- **Already written:** the worktrees on this host are untouched by the
  stream; whether a past `remove` destroyed an uncommitted edit is not in
  the record (the tool prints what it removed, not what git would have
  refused). `worktrees.md` § Removing a worktree already states the
  contract; its words are checked against the fixed tool and left, or the
  one sentence that differs is changed under this brief.
- **Acceptance (#939, #940):** the seven cases by name with their positives;
  `rules-check --quiet` rc 0 with the new entries; `hooks-test` PASS (the
  pattern list still valid shell).
- **Commits:** `fork-worktree: --preserve stops on a failed move; remove forces only on --force (#939, #940)`,
  `fork-worktree: repair carries back every untracked path; sync returns its result; the no-directory loop (#940)`,
  `doctrine: fork-worktree-test in the lists (#657)`.

## S5. The tracker readers read everything or fail closed: `box-check` and `ceremony-check` (PL-04, PL-05, PL-15, PL-44; #941, #943) -- `fix-case`

- **Why a stream:** the checkbox gate in the CI and the push guard's
  ceremony gate have been passing while reading 300 of 458 (now 473) open
  issues and 200 of 331 closed ones, reporting a `gh` failure without
  counting it, and taking any truthy string for a boolean. This is the
  class the slice was dispatched to hunt (#845's); it sits in the two tools
  the fork's own process leans on.
- **Files owned:** `tools/box-check`, `tools/ceremony-check` **at the
  hash's bytes** (the #905 packet changes its friction reader off this
  branch; keep this stream's hunks in the tracker-reading functions and the
  marker reader, and the coordinator merges this after #905's), their
  controls: a `gh` double under `.qa-scratch/t10/` that serves N pages and
  can fail, promoted to a kept fixture beside each tool's existing
  controls (`docs/qa-logs/2026-10-24-905-ceremony-friction/`'s shape for
  `ceremony-check`; `box-check` has none: the stream gives it one under
  `docs/qa-logs/2026-10-24-box-check/`).
- **The shape:** every `gh issue list --limit N` becomes a paginated read
  to completion (`gh api --paginate` or `gh issue list -L` with the
  returned count compared against the search's total), and a count that
  does not match is a failure; a `gh` that fails makes its line fail (an
  `OVERDUE`/`FAIL`, never `ok`); the completion marker's receipt booleans
  are typed (`is True`), a `* [ ]` counts as an unticked checkbox, an
  `Audit:`-titled issue's shape is validated as the marker rule says, and
  the clocks reset only on a marker whose shape the check names (PL-15, the
  lane's `04` lists the marker shapes that reset them wrongly).
- **The test first:** the `gh` double serving 2 pages of 300 and 158 issues
  with a failing checkbox on page 2: `box-check` fails at the fix, passes
  `0 fail` unfixed (the positive); the double failing: both tools' lines
  fail at the fix, read `ok` unfixed; a receipt with `"false"` as a string:
  refused at the fix; a `* [ ]` checkbox: counted; the clock-reset marker
  shapes: not a reset. The live run against GitHub (`box-check --quiet`,
  `ceremony-check`) after the fix, with the API budget before and after
  (the brief § 5), its result quoted: the first run that reads all 473 open
  issues may find checkboxes the 300-limit hid; **each such checkbox is a
  tracker edit for the coordinator, listed in `02` by issue, not fixed by
  the lane.**
- **Already written:** the CI's green `box-check` steps since 2026-09-25
  read at most 300 issues; the fixed tool's first full run names what they
  missed (the list above). Nothing on a device or in a cloud.
- **Acceptance (#941, #943):** the cases by name with their positives; the
  live run's output and budget; the list of newly visible failing
  checkboxes (possibly empty) in `02`.
- **Commits:** `box-check: read every open issue, fail on a short or failed read (#941)` and
  `ceremony-check: read every issue, count a failed gh, type the marker's receipt (#943)`.

## S6. `forbidden-terms-check` scans symlinks and names, and asserts its own count (PL-07, PL-40's tool half; #942, #936) -- `fix-case`

- **Why a stream:** the CI's only wordlist run skips 180 tracked symlinks,
  reads no file name, and would print `0 hits in 0 tracked files` on an
  empty checkout. Runs **after S3**.
- **Files owned:** `tools/forbidden-terms-check`; its fixture (a stand-in
  list through `FORBIDDEN_TERMS_FILE`, a throwaway tree with a symlink
  whose target carries a stand-in word, a file whose name does, and an
  empty checkout), kept under `docs/qa-logs/2026-10-24-forbidden-terms/`.
- **The shape:** a tracked symlink is scanned as its target when the target
  resolves inside the tree, and as its link text otherwise; every tracked
  path's name is scanned; the number of files scanned is compared with the
  number listed and a difference is a failure; zero tracked files is a
  failure, not a clean run. `fork-wordlist.yml` runs the tool unchanged and
  gets stricter.
- **The test first:** the three fixture cases fail at the fix and pass
  unfixed (the positives), with the stand-in list; then the real run over
  the lane's worktree (`tools/forbidden-terms-check`, the real list through
  the tool only) reports its count equal to `git ls-files | wc -l` and its
  hits (0 expected; a hit is named by file and line to the coordinator,
  never by word).
- **Already written:** 180 symlinks and every file name in the tree were
  never scanned; the first fixed run answers whether any carries a listed
  word (a hit stops the stream and goes to the coordinator by file:line).
- **Acceptance (#942, #936's tool criterion):** the cases; the real run's
  count line.
- **Commit:** `forbidden-terms-check: scan symlink targets and file names; assert the scanned count (#942, #936)`.

## S7. `lint-audit-artifacts`'s index boundary and the two readers' date format (PL-08, PL-43; #945) -- `fix-case`

- **Files owned:** `tools/lint-audit-artifacts` (the branch's copy carries
  P1's renovation face and #810's fix; this stream's hunks are the index
  boundary and the folder regex), `tools/ceremony-check:364`'s folder
  regex (the second reader; the same hash-bytes rule as S5), the lint's
  fixtures on P1's tree (`tools/test-fixtures/lint-audit-artifacts/`).
- **The shape:** the seats' findings index is bounded by a heading at the
  start of a line (`^## Verification`), never by `str.find` over the whole
  text; both readers accept the dated folder with underscores
  (`YYYY_MM_DD-...`), which all 23 folders use, and the hyphen form is
  dropped or also accepted, said in the commit.
- **The test first:** a fixture whose table cell quotes `## Verification`:
  the unfixed lint stops its index at the cell (the 2026-09-28 folder's
  rows 192 to 881 unrequired, as `02` records), the fixed lint reads to the
  heading; a folder named with underscores read by both tools' clocks and
  phases. The pass and fail fixtures still PASS and FAIL.
- **Already written:** the 2026-09-28 audit's folder was linted with its
  seat rows unrequired; the fixed lint is run over it once and the result
  recorded in `02` (a FAIL there is a coordinator's item, not a rewrite of
  history).
- **Acceptance (#945):** the two cases; the three fixtures' results; the
  2026-09-28 run.
- **Commit:** `lint-audit-artifacts: bound the seats' index at a heading; the folder date format agreed with ceremony-check (#945)`.

## S8. `fork-package-freshness` diffs against the merge base and fails on a missing ref (PL-09; #946) -- `fix-case`

- **Why a stream:** the tool's set was a two-tree diff without the merge
  base (22 upstream deletions counted in, a fork addition missing) and a
  missing ref exited 0. **Its declared scope stands** (D-WORKFLOW-024: the
  packages the fork *introduces*); T8's edited recipes are outside it, as
  the seats narrowed, and the question of a second check over edited
  recipes is the coordinator's disposition below, not this stream's.
- **Files owned:** `tools/fork-package-freshness`; a fixture repository
  under `.qa-scratch/t10/` with a known merge base, kept as a script under
  `docs/qa-logs/2026-10-24-package-freshness/`.
- **The shape:** the set is `git diff --diff-filter=A --name-only
  $(git merge-base upstream/next HEAD) HEAD -- packages projects`; a ref the
  tool cannot resolve exits 2 with the ref named; the network loop is
  unchanged.
- **The test first:** the fixture with one upstream deletion, one fork
  addition and one edit: the unfixed set is wrong in the two ways `02`
  names, the fixed set is the one addition; a missing ref exits 2 at the
  fix, 0 unfixed. The real run (`tools/fork-package-freshness`, network,
  budget read first) lists the fork's own packages as T8's `02` counted
  them.
- **Already written:** every candidate since 2026-09-25 was checked with
  the wrong set; the fixed run's list is compared with the recipes
  `rc-preflight` accepted in `docs/releases/rc-accept.txt` and a package
  the old set missed is named in `02` for the coordinator.
- **Acceptance (#946):** the fixture's two cases; the real run's list.
- **Commit:** `fork-package-freshness: the set is the fork's additions since the merge base; a missing ref is an error (#946)`.

## S9. The record checkers' small fixes, one commit per bug (PL-17 to PL-29; #947 to #957) -- `fix-case`

One stream because each is contained and has, or gets, its fixture; one
commit per bug so a revert is a revert of one tool. The order within: the
tools the push guard and the CI run first (`register-check`,
`work-log-index`, `rules-check`), then the rest.

- **#947 `register-check`:** the second ID of a slash shorthand is looked
  up; the seven live documents that cite no ID are read for a reason or
  dropped from the list; T4's three gaps (the open table's column shape, an
  in-place edit of a decided row, an unescaped `|` in a decided row -- the
  six rows named in T4's F-23 are the failing control; **the tool reports
  them, the register's rows are not edited by this lane**: a decided row is
  append-only, and the coordinator fixes the six by a clerical row,
  D-WORKFLOW-013). Fixture: a constructed register under `.qa-scratch/`.
- **#948 `rules-check`:** `mention` is a word-boundary test, and an index
  row's *Detail in* rule must name the tool (T4's 31 of 85 pairs are the
  positive; **the tool reports them, and the rows are the coordinator's to
  fix** -- the first fixed run lists them in `02`).
- **#949 `work-log-index`:** `### HH:MM UTC` entries are indexed (the 14
  at the hash), and `--check` fails when one is missing; the index is
  regenerated once in this worktree after the fix (its diff is the
  positive, quoted by count).
- **#950 `archaeology`:** blindspots 1 to 29 (table rows) are searched; a
  failed `git` or `grep` is an error, not zero hits; the tool exits
  non-zero on an error (its "nothing found" stays 0 after a successful
  empty search, as the seats narrowed).
- **#951 `es-menu-map-check`:** a `new GuiSettings(` with a computed title
  is **reported** by file and line as unchecked (the 22 at the ES pin
  `16dbac5211`), never silently skipped; whether each of the 22 is mapped
  is the EmulationStation area's work, which the coordinator files from the
  lane's list (below). The checker's exit is unchanged by this stream.
- **#952 `vocabulary-check`:** the list of scripts is derived (every
  script under the two product-surface directories that prints a `>>> why`
  or a `_(` string), not hard-coded; the derived list is printed and
  compared with the old seven plus `backuptool` in `02`.
- **#953 `prose-check`:** the sign-off pattern matches at a space and at the
  line's end; the repeated-opener check reports instead of `pass`ing;
  `--self-test` still passes the maintainer's page and fails the draft, and
  gains the two cases.
- **#954 `release-catalog`:** `KEY value` with one or more spaces; a kept
  folder with no `RECORD.txt` is reported; the real run over
  `/workspace/artifacts/` regenerates `docs/releases/catalog.md` and its
  diff is read (a changed row means a record was misread before).
- **#955 `pr-stack-check`:** the tool compares the final head's tree with
  `next` on every upstream-bound path, as #322 and its header claim, or the
  header is corrected to what it does (D-WORKFLOW-079's one commit per
  PR); the lane says which in `02` after reading #322. The control runs in
  a throwaway repository with a two-line map, never the fork's.
- **#956 `rc-preflight`:** the acceptance line's kind is checked against
  the item it accepts, the decided row cited must be the one for that
  kind, and a bug's "Code trace" is read one way; the controls under
  `docs/qa-logs/2026-10-02-candidate-preflight/` gain the cases.
- **#957 the three `renovation-*` tools** (P1's; on this branch through
  the stack): `renovation-inventory` writes nothing on a run whose counts
  disagree and compares staged paths as sets; `renovation-status`'s *Drift
  since* reads the right cell and `closed` is derived from the slice's own
  issue; `renovation-drift` reads `fixed_at` from the issue as `status`
  does. P1 (#641) is closed; the coordinator notes the tools' move on #641 and on #898.
- **Already written** for each: the tool's past outputs are records read
  by people, not state on devices; where a past verdict was wrong (the
  catalog's rows, the index's 14 entries, the 31 index pairs, the six
  register rows) the fixed run names it and the coordinator owns the
  correction.
- **Acceptance (#947 to #957):** each bug's criteria; each fixture or
  self-test with its failing run on the unfixed tool.

## S10. The fork CI runs every step, wires the three revived controls, and passes its token through `env:` (PL-06, PL-31, T9's row; #944) -- `fix-pending-ci`

- **Decided (D-WORKFLOW-202):** every check step in `fork-checks.yml` runs
  whether or not an earlier one failed (`if: always()` on each check step;
  the job still fails on any failure), so a red day shows every verdict;
  the three watcher controls T9's S1 revived
  (`docs/qa-logs/2026-10-04-watch-progress/test-progress.py`,
  `test-watch-build.py`, `docs/qa-logs/2026-10-05-watch-submit/test-submit.py`)
  join the step at `:40-44`; `fork-mirror-build-container.yml:34` passes
  `GITHUB_TOKEN` through `env:` and `skopeo login --password-stdin` (PL-31,
  the documented form).
- **Files owned:** `.github/workflows/fork-checks.yml`,
  `.github/workflows/fork-mirror-build-container.yml`.
- **The test:** the workflow files parse (`python3 -I -c 'import yaml,
  sys; yaml.safe_load(open(sys.argv[1]))'`); the step shape is read against
  GitHub's documented `if: always()`; the three controls' paths exist on
  this branch (they do; their fixed bodies arrive with T9's merge, which
  precedes this branch's in the order, so the step is green on `next` only
  after both -- `fix-pending-ci`, the coordinator's proof on the first
  `next` run). **No `gh workflow run`.**
- **Already written:** the CI's record from 2026-10-19 to 10-22 hid the
  ceremony step's verdict behind an earlier red step; nothing to migrate.
- **Acceptance (#944; T9's row on this issue):** the parse; the diff
  quoted; the `fix-pending-ci` cell naming the coordinator's run to read.
- **Commits:** `fork-checks: every step runs; the three watcher controls join (#944, #913)` and
  `fork-mirror-build-container: the token through env and --password-stdin (#657)`.

## Dispositions that are not streams (the coordinator's, written into the Phase 7 table by the lane)

- **PL-16** (the push guard's ceremony gate judges the primary checkout's
  tree, not the pushed one): deferred to a **Backlog issue the coordinator
  files at this pause** (D-WORKFLOW-028's gate reading `--tree <pushed
  tip>`; today `next` is pushed only from the primary checkout, so the two
  trees coincide in practice; #258 PL-004's row is cited).
- **PL-30** (the CI scans no credential shape): deferred to a **Backlog
  issue the coordinator files at this pause**, with the decision that the
  CI half of D-WORKFLOW-061 is wanted and its vehicle is
  `forbidden-terms-check` reading `.githooks/secret-patterns` as a second
  list, run by `fork-wordlist.yml`; not this slice's stream, because it
  changes what the tool is.
- **PL-31:** S10. **PL-34:** S2 (the conditional) and #640 (the header).
- **PL-32:** #640, with `fork-worktree:72,74`'s hint named first (the lane
  did). **PL-33:** the build-engine area's merge of `upstream/next` (two
  commits behind on `generate-changelog.sh`; the coordinator notes it on
  #800) and a #585 line for the empty-success paths (the coordinator posts
  it at acceptance).
- **F-09's scope question** (edited recipes outside `fork-package-freshness`'s
  declared scope): the scope stands (D-WORKFLOW-024); T8's four recipes are
  a lead the coordinator carries to #585's queue, not a stream.
- **#951's 22 computed-title pages:** the coordinator files the mapping work
  for the EmulationStation area from the lane's list in `02`.
- **Criterion 15's form** (the lane's question): the coordinator edits it on
  #657 and in the brief to read over the 31 member paths (`tr '\n' '\0' <
  .qa-scratch/t10/paths.txt | xargs -0 git diff --stat a82d784216 <fixed-at>
  --`), so the pointer under `.github/sessions/` does not count; every hunk
  it prints is a stream briefed here or the two list entries S2 and S4 make.
- **The six register rows with an unescaped `|` and the 31 index pairs**
  (#947's and #948's first fixed runs): tracker and ledger edits for the
  coordinator, listed in `02`, never made by the lane.

## Order and hand-back

S1, S2, S3 first and in that order (the three hooks; `hooks-test` grows with
each); S4; S5, S6 (after S3), S7, S8; S9 in its listed order; S10 last.
Each commit cites its bugs (`Refs #N, #657`, no closing keyword: a bug
closes when its fix is on `next`) and carries the attribution line; `git
status --short` before every `git add -A` (`.qa-scratch/` is gitignored; the
positives and the throwaway repositories stay there). **Every hook commit
is itself committed through the primary checkout's unfixed hooks**, which
is fine: the fixed hooks are proven by `hooks-test`, and the merge to `next`
is what installs them. After S10: the Phase 7 table and the `punch_index`
at their outcomes, `02` § The suites re-run (`hooks-test` with its new
count, the lint, the self-tests, the three live runs), the lint on the
folder (`PASS`, the default phase), `fixed-at:` in #657's body, the retro
(stage G, posted on #657: what the slice did to the two time-to-play
numbers -- nothing; what each stream did to a guard's refusals -- the list),
then the hand-back comment naming the tip and each artifact by path. The
coordinator accepts by `AUDIT_ISSUE=958 $S/t10-accept.sh <tip> <coordinator
tip>` on an export (membership, line counts, `hooks-test` at the tip and on
the simulated merge with the coordinator's branch, `register-check`,
`rules-check --quiet`, `work-log-index --check`, the lint on both fixtures,
the `PERSONAL_PATTERNS` diff), reads every stream's diff and positives, ticks
#657 and #958 from the artifacts, closes #958 when its checkboxes read back
ticked by name, and merges the branch in its turn (after T9's, before
T4's); the ledger and index edits the fixed checkers surfaced are the
coordinator's, made at the merge.

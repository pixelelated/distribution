# Fix packet: `backuptool`'s credential scan reads `.toml` too (#889)

Written by the coordinator on 2026-10-24 (D-WORKFLOW-189), in the shape of
`fix-packet-887-melonds-toml.md`, whose execution found this: one narrow
stream, the files owned, the test first, the `Already written:` line, one
commit cut after the checks are green. **Nothing here builds.** The branch
merges to `next` in the integration order beside #887's packet (the same
file, different hunks: #887 touched the `RATOKENSETTINGS` list and the
blank's pattern; this touches the scan's file-type list and its value class).
The file is the OS-scripts area's (T1's accepted slice), so the T1 session
cuts it. **Review depth: Local** (plan § 6c: a glob and a value class, with
the harness case #889 specifies): the executor, `tools/last-good-scripts-test`
part k, and the coordinator reading the diff on #889. No guest (the harness
runs `backuptool` whole under bwrap with the image's busybox, as part k
does), no compiler, no `npm`, no process in an M7 worktree.

## The stream (#889)

- **The defect, from #889:** `backuptool`'s `credential_lines` -- the
  archive's last line of defence (#52, #169, #221, #307 PL-005) -- reads the
  key/value shape (`CREDENTIAL_KEYS`) only in files matching
  `*.cfg|*.conf|*.ini|*.nmconnection|*.psk|*.backup|*.bak|*.cfg.*|*.conf.*|*.ini.*`
  (`:445` at `8ebaf8daad`); `*.toml` is not in the list, and the fixed-token
  shapes (`CREDENTIAL_TOKENS`) know only the upper-case key form. So
  `melonDS.toml` with `Password = "..."` passed the scan whole before #887's
  blank existed, and any future `.toml` with a secret will.
- **Branch and worktree:** cut **from `next` at `8ebaf8daad`**, in its own
  worktree beside the lane's, never in a slice worktree:
  `git -C /workspace/repos/pixelelated/distribution worktree add ../distribution.worktrees/m6-889-scan-toml -b fix/m6-889-scan-toml 8ebaf8daad`.
  The coordinator removes the worktree with `tools/fork-worktree remove`
  after the merge.
- **Files owned:** `projects/ROCKNIX/packages/rocknix/sources/scripts/backuptool`
  -- the file-type pattern at `:445` (`*.toml` added) and, if the fixture
  shows a TOML line's quoted-empty value is not read as empty, the
  `CREDENTIAL_KEYS` value class (read the comments at `:397-410` first: they
  say quotes holding blanks alone are empty for INI); and
  `tools/last-good-scripts-test` part k, one new case in #889's shape. Nothing
  else: #887's packet owns the list and the blank.
- **The test first**, every output pasted on #889: part k with a fixture
  `.toml` **under the selection that the strip does not know** (a path not
  in `RATOKENSETTINGS`, e.g. `/storage/.config/synth-app/settings.toml`)
  holding `Password = "synth-other"` (the literal word; nothing
  credential-shaped at rest) -- **before the fix** the backup ends rc 0 with
  the file whole in the archive (the case FAILs); **after** it ends with
  `>>> why A SIGN-IN WAS FOUND IN THE BACKUP` and leaves the previous archive
  as the only one; and the same fixture with `Password = ""` completes rc 0
  (the quoted-empty value is empty). `BASE_REF=8ebaf8daad
  tools/last-good-scripts-test --old` is the control the harness header
  names. `bash -n` on both files; the image's `bash -n backuptool`.
- **The change:** `*.toml` in the pattern at `:445`; the value class only if
  the fixture demands it, as the smallest widening with its own line.
- **Already written:** nothing on devices by this change; archives already
  written were never scanned for a `.toml` secret and are not rewritten (the
  player's remedy is a fresh backup, as #887 says); #887's blank covers the
  one `.toml` known to carry a secret today.
- **Commit**, one, cut after the tests are green, by `git add -- projects/ROCKNIX/packages/rocknix/sources/scripts/backuptool tools/last-good-scripts-test`:
  `backuptool: scan .toml files for a key and value too (#889)`, body: the
  harness lines before and after, `Refs #889, #887, #677` (no closing
  keyword), the attribution line. `git status --short` empty after. Push
  `fix/m6-889-scan-toml` to origin and post the tip, the diff and the
  outputs on #889; then the session is idle.
- **Ceremonies:** the work-log entry headed `#889` is the coordinator's; the
  lane posts on #889 only; a friction line if anything slows.

## After the packet

The coordinator reads the diff and the harness lines on #889, ticks the
criteria from them, names the branch in the pointer's merge notes beside
#887's, and tells M7 on the host file that the two `backuptool` packets exist
(their candidate carries the same file; whether M7 takes them before its
images is M7's).

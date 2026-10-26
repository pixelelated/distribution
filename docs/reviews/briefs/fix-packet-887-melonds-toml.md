# Fix packet: `backuptool` blanks `melonDS.toml` too (#887)

Written by the coordinator on 2026-10-24 at T30's S3 (D-WORKFLOW-189), in
the shape of `fix-packets-802-806.md` and `fix-packet-libfmt.md`: one narrow
stream, the files owned, the test first, the `Already written:` line, one
commit cut after the checks are green. **Nothing here builds.** The packet
is a branch on `origin` that merges to `next` in the integration order
beside the other packets (after T30's branch, whose S3 made the melonDS
scripts write their credentials as data, and whose #887 this is). The file
is the OS-scripts area's (`projects/ROCKNIX/packages/rocknix/sources/scripts/backuptool`,
T1's accepted slice), which is why the T1 session cuts it. **Review depth:
Local** (plan § 6c: a one-line list entry with a fixture): the executor,
the fixture, and the coordinator reading the diff on #887. No guest unless
the fixture cannot run the sanitiser on the host (then one GENERIC_X64
cycle, named on #887 first with the host file read); no compiler, no `npm`,
no process in an M7 worktree.

## The stream (#887)

- **The defect, from #887's trace:** melonDS's `Config::Save()` (the fork's
  `000-retro-achievements.patch`, lines 7520-7522 map `RA_Password` and
  `RA_Token` into the TOML table; `Save()` runs every 60 s of achievement
  play and when the settings dialog is accepted) writes
  `/storage/.config/melonDS/melonDS.toml` with
  `[Instance0.RetroAchievements]` `Password = "..."` and `Token = "..."`.
  `backuptool`'s `RATOKENSETTINGS` (`:705-710` at `8ebaf8daad`) names
  `melonDS.ini` and not the TOML, so a settings backup carries both values
  in plain text, on the device and in the player's cloud.
- **Branch and worktree:** cut **from `next` at `8ebaf8daad`**, in its own
  worktree beside the lane's, never in a slice worktree:
  `git -C /workspace/repos/pixelelated/distribution worktree add ../distribution.worktrees/m6-887-melonds-toml-blank -b fix/m6-887-melonds-toml-blank 8ebaf8daad`.
  The coordinator removes the worktree with `tools/fork-worktree remove`
  after the merge.
- **Files owned:** `projects/ROCKNIX/packages/rocknix/sources/scripts/backuptool`,
  the `RATOKENSETTINGS` array (one line added after `:707`), and -- if the
  sanitiser's pattern does not already blank a TOML `Key = "value"` line --
  the pattern's lines, read first (the comments at `:397-410` say quoted
  values with leading blanks are handled; the fixture decides). A test file
  under `tools/` only if a backuptool test harness already exists there
  (`grep -l backuptool tools/*test*`); otherwise the fixture lives under
  `docs/qa-logs/2026-10-24-887-melonds-toml/` with its outputs.
- **The test first**, every output pasted on #887:
  1. The sanitiser, lifted by marker lines from `backuptool` (or run through
     `backuptool`'s own `STRIP=1` path over a fixture tree, whichever the
     script allows without a device: read `:794` and `:1009-1060` first),
     run with the image's `bash`, `sed` and `busybox` borrowed read-only
     from `/workspace/repos/rocknix.worktrees/m7-signin-build-20261022-07/build.pixelelated-GENERIC_X64.x86_64/image/system/usr/bin/`
     (never a process started in that tree), over a fixture
     `/storage/.config/melonDS/melonDS.toml` holding, under
     `[Instance0.RetroAchievements]`, `Enabled = true`, `Username = "synth-user"`,
     `Password = "synth-pass"`, `Token = "synth-token"`, `HardcoreMode = false`
     and two unrelated sections -- the values are the literal words `synth-*`
     and nothing else (the pre-commit's secret patterns match a long literal
     after `TOKEN=`/`PASSWORD=`; short synthetic words pass, and the file at
     rest carries no credential-shaped line).
  2. **Before the fix** the archive's (or sanitised copy's) `melonDS.toml` is
     byte-identical to the fixture (the password and token travel): the
     fixture is seen to FAIL.
  3. **After the fix** the copy has `Password = ""` and `Token = ""` (the keys
     kept, the quotes kept), every other line unchanged (`diff` shows two
     lines), and the run without a `melonDS.toml` leaves no new file and the
     same exit status as before.
  4. `bash -n backuptool`; `tools/last-good-scripts-test` if it covers
     `backuptool` (read its header), with its exit code.
- **The change:** one line in `RATOKENSETTINGS`:
  `/storage/.config/melonDS/melonDS.toml        # Password = "" Token = ""   (melonDS's Config::Save writes the table the patch maps RA_Password/RA_Token into; #887)`
  -- and nothing else unless step 1 showed the pattern misses the TOML form,
  in which case the pattern's smallest widening with its own fixture line.
- **Already written** (#887's, kept in the packet's commit): settings
  backups made on SM8550 devices since the patch shipped may hold
  `melonDS.toml` with the password and token, on the device and in the
  player's cloud; this fix blanks new backups only; an existing archive keeps
  the values until it is replaced by the next backup, and a restore of an old
  archive puts them back on the device (where the emulator overwrites them at
  its next `Save()`). The player's remedy is a fresh backup; the issue says
  so, and the coordinator carries the sentence to #585's row if upstream
  takes the patch.
- **Commit**, one, cut after the tests are green, by
  `git add -- projects/ROCKNIX/packages/rocknix/sources/scripts/backuptool`
  (and the test file, if any): `backuptool: blank melonDS.toml's RetroAchievements password and token in a settings backup (#887)`,
  body: the fixture's before and after lines, `Refs #887, #677, #872, #866`
  (no closing keyword: the first criterion closes on the fixture, the
  `Already written:` line names what the fix does not reach), the
  attribution line. `git status --short` empty after. Push
  `fix/m6-887-melonds-toml-blank` to origin and post the tip, the diff and
  the outputs on #887; then the session is idle.
- **Ceremonies:** the work-log entry headed `#887` is the coordinator's, as
  for the other packets; the lane posts on #887 only; a friction line if
  anything slows.

## After the packet

The coordinator reads the diff and the fixture lines on #887, ticks the
criteria from them, names the branch in the pointer's merge notes (after
T30's), and records the packet on #585's row for the melonDS patch (the
TOML's credentials are the patch's doing; upstream ROCKNIX carries the same
patch).

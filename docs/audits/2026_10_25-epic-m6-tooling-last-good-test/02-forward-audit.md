# Forward audit: M6.P2 T15, the last-good scripts test (#662)

Read at `8ebaf8daad` (the branch `HEAD` at stage A, `60d7f6a5b2`, does not differ on the file). The lens is brittleness. The bench is the host, with no guest: **Can this be done on the VM? Yes -- on the host, where the suite runs by design. The one thing the host lacks, a build root's busybox, is read from the M7 root `m7-signin-build-20261022-07` (BUILD_ID `069fc270442134fe771258418adf4e666e0473fb`) through `QA_SYSTEM_ROOT`, a read of one file the suite copies.**

## Phase 2: #662's checklist

Each criterion's state at stage B, with the artifact that will tick it. The coordinator ticks at acceptance, from the artifacts.

| # | Criterion (§ 7, short) | State at stage B | Artifact |
| --- | --- | --- | --- |
| 1 | the folder holds 00 to 05 | 00, 01 and 02 written; 03 to 05 at stage B to D | this folder |
| 2 | the lint prints PASS (pre-issue before D, resolution at close) | not yet run | `tools/lint-audit-artifacts` |
| 3 | `review-plan.json` and the seat's provenance; the packet's scan | stage C | `second-opinions/` |
| 4 | the punch-list issue at its Phase 7 outcomes | stage D onward | the audit issue |
| 5 | `reviewed-at` / `fixed-at` | `reviewed-at: 60d7f6a5b2` recorded in `00` | #662's body at hand-back |
| 6 | `01` § Scope | written: the inventory row, 408 commits, the 34 sections | `01-research-notes.md` |
| 7 | 34 coverage rows | written below | § Coverage |
| 8 | both runs, and the busybox-dependent checks | written below | § The runs, § The checks that depend on the busybox |
| 9 | the twelve `--old` recipes | written below | § The runs |
| 10 | no handheld, provider, guest, build or forbidden edit; every run with `SIGINT ignored=0` | holds so far; one write under `/tmp` was made and removed, recorded in `00` | `00-running-log.md` |
| 11 | Q6's 34-row brittleness table and the split proposal | stage B | `04` § Q6 |
| 12 | Q3 by section; the `|| true` sites, `check $?`, `skip()`, NOT APPLICABLE, no-busybox; the ten sorted | the ten are sorted (the fixture's history dependency, `00`); the rest is stage B | `04` § Q3 |
| 13 | Q7 | stage B | `04` § Q7 |
| 14 | Q5's wall time by section | measured (the timed run, below) | `04` § Q5 |
| 15 | every proof carries a `proved:` cell | below | § Proofs |
| 16 | `question:`, `box-check`, no `tools/` change before a stream; the two call sites' flags | no `tools/` change; the call sites at stage E | the branch's diff |
| 17 | the fixed tip refuses or marks a host-busybox run; the image run is judged on the tree | stage E | § The runs at the fixed tip |
| 18 | the retro | stage G | `docs/retros/` |
| 19 | the checkers, and `vm-qa:148`'s exit rule stated | stage E onward | § The runs at the fixed tip |

## Coverage

One row per section, as the brief's criterion 7 asks: the section's letter, its first line, its claim, its weight in the image run, its flips under the host's busybox, its seconds in the timed run, the `--old` recipe that promises a FAIL in it (and whether that run reaches it before it stops), and its sandbox and git-history dependencies counted from its lines. The sub-groups of `x`, `y` and `z` are under `04` § Q6, per the coordinator's 00:27 and 00:33 rulings.

| Section | Lines | Its claim (the `echo` line, cut) | Header claim | Checks (image run) | Flip to FAIL under the host's busybox | Seconds | `--old` recipe that promises a FAIL (reached before the stop?) | sandboxes / git-history reads |
| --- | --- | --- | --- | ---: | ---: | ---: | --- | --- |
| `a` | `:429` | chksysconfig keeps and restores the last good system.cfg | yes | 13 | 0 | 0.4 | `1d1503180d` (yes), `c15050c897` (yes) | 0 bwrap, 0 `sa_run`; 0 history |
| `b` | `:518` | backuptool: a kill mid-tar leaves the previous archive; a failed restore puts the snapshot back | yes | 14 | 0 | 2.9 | `1d1503180d` (yes) | 3 bwrap, 0 `sa_run`; 0 history |
| `c` | `:607` | set_setting is one rename; sort_settings refuses an empty result | yes | 9 | 0 | 0.2 | `1d1503180d` (yes) | 0 bwrap, 0 `sa_run`; 0 history |
| `d` | `:650` | cloud_sync_helper and the saves scripts keep the config's last good copy; stamps survive a kill | yes | 13 | 0 | 0.4 | `1d1503180d` (yes) | 1 bwrap, 0 `sa_run`; 0 history |
| `e` | `:723` | nothing a screen can show carries an exit code, a log path, a tool's name or a flag | yes | 1 | 0 | 0.1 | `1d1503180d` (yes) | 0 bwrap, 0 `sa_run`; 0 history |
| `f` | `:766` | backuptool: rclone.conf never enters an archive, and the scanner knows rclone's key names (#52) | yes | 10 | 0 | 0.6 | `1d1503180d` (yes) | 3 bwrap, 0 `sa_run`; 0 history |
| `g` | `:839` | the in-script RCLONE_NET_OPTS fallback is the shipped value (#146) | yes | 6 | 0 | 0.0 | none | 0 bwrap, 0 `sa_run`; 0 history |
| `h` | `:854` | the rclone wrapper: an automatic run's stalled call ends at the ceiling, a deliberate run's at the stall ceili… | yes | 11 | 0 | 6.3 | `8707919349` (yes) | 0 bwrap, 0 `sa_run`; 0 history |
| `i` | `:893` | cloud_net_ready settles on a held default route however NetworkManager judges connectivity | yes | 6 | 0 | 14.3 | none | 0 bwrap, 0 `sa_run`; 0 history |
| `j` | `:934` | cloud_sync_helper migrates the shipped retry bound once, and leaves a hand-tuned value alone (#107) | yes | 6 | 0 | 0.5 | `1d1503180d` (yes) | 0 bwrap, 0 `sa_run`; 0 history |
| `k` | `:962` | backuptool: what the image ships does not travel, and an older archive's copy of it is not put back (#45); a R… | yes | 25 | 11 | 1.0 | `1d1503180d` (yes), `53f390b1e9` (yes), `34aca64afd` (yes) | 2 bwrap, 0 `sa_run`; 0 history |
| `l` | `:1114` | a missing cloud folder reads as not there yet whatever the server's words (#142) | yes | 23 | 0 | 0.2 | `1d1503180d` (yes), `53f390b1e9` (yes) | 2 bwrap, 0 `sa_run`; 0 history |
| `m` | `:1251` | the shipped device name becomes this unit's own, once; a player's name is never touched (#50) | yes | 23 | 0 | 0.6 | `1d1503180d` (yes), `53f390b1e9` (yes) | 3 bwrap, 0 `sa_run`; 0 history |
| `n` | `:1403` | a deliberate cloud_backup ends a transfer that stops making progress at the stall ceiling, and says it couldn'… | yes | 11 | 7 | 41.6 | `8707919349` (yes) | 2 bwrap, 0 `sa_run`; 0 history |
| `o` | `:1534` | set_setting system.hostname default keeps the line chksysconfig's sentinel reads, empty (D-NET-009) | yes | 7 | 0 | 0.1 | `8707919349` (yes) | 0 bwrap, 0 `sa_run`; 0 history |
| `p` | `:1565` | raofflineproxy-ctl: enable records hardcore and turns it off, disable puts it back; both harmless twice (#165,… | yes | 38 | 0 | 1.6 | `34aca64afd` (yes), `d79281066c` (no), `cee1656c33` (yes) | 2 bwrap, 0 `sa_run`; 0 history |
| `q` | `:1752` | 099-networkservices: a daemon fragment that sets no CONF inherits none from the fragment before it (#166) | yes | 9 | 0 | 2.2 | `0f7785e6ed` (no) | 2 bwrap, 0 `sa_run`; 0 history |
| `r` | `:1860` | the launch log carries no credential value: setsettings' Added setting and Fetch lines, runemu's Executing lin… | yes | 18 | 0 | 0.1 | `cee1656c33` (yes), `28a80357ed` (yes) | 0 bwrap, 0 `sa_run`; 0 history |
| `s` | `:1949` | rocknix-evidence: every file in the bundle has been through the credential filter, summary.txt says so, and wi… | yes | 13 | 0 | 1.3 | `28a80357ed` (yes) | 2 bwrap, 0 `sa_run`; 0 history |
| `t` | `:2033` | raofflineproxy-ctl scan, topup and ready against the client the tree describes: the refusals, the index rule b… | yes | 80 | 42 | 33.6 | `cee1656c33` (yes), `3387cf5da0` (yes), `70b6c70ca7` (yes) | 6 bwrap, 0 `sa_run`; 1 history |
| `u` | `:2856` | wifictl current, saved, forget and join read NetworkManager, not the setting; forget says when it dropped the … | yes | 19 | 0 | 0.5 | `655f103cc5` (yes) | 2 bwrap, 0 `sa_run`; 0 history |
| `v` | `:2991` | the save state manager's arguments reach RetroArch as Batocera's launcher carries them (#196, D-UI-057): runem… | yes | 20 | 0 | 0.3 | `655f103cc5` (yes) | 0 bwrap, 0 `sa_run`; 0 history |
| `w` | `:3067` | cheevos_armsx2.sh writes one Token line to secrets.ini, however often it runs (#170) | yes | 5 | 0 | 0.2 | none | 1 bwrap, 0 `sa_run`; 0 history |
| `x` | `:3113` | the launcher's incremental-save modes, the password's handoff, and the keeper's cut/whole note (#209, #198, #2… | **no** | 350 | 33 | 82.1 | none | 24 bwrap, 0 `sa_run`; 19 history |
| `y` | `:7796` | audit #307 / #308, stream B: backuptool, wifictl, the settings writer and lock, factoryreset, chksysconfig, ro… | **no** | 448 | 180 | 248.3 | none | 24 bwrap, 145 `sa_run`; 3 history |
| `z` | `:13182` | the audit of the fix round, stream B: the conf read as text, a flag's password redacted, the restore's lists a… | **no** | 92 | 36 | 17.4 | none | 0 bwrap, 1 `sa_run`; 0 history |
| `aa` | `:13723` | cloud_migrate_layout --state, --keep and --follow (#353, D-CLOUD-160/161): the layout as facts, a kept folder,… | **no** | 0 | 0 | ? | none | 2 bwrap, 0 `sa_run`; 0 history |
| `ab` | `:13913` | cloud_scan (#350, D-CLOUD-156): the opening scan's three items, the content scan's one, the selected folder fa… | **no** | 24 | 0 | 1.4 | `1d1503180d` (no) | 2 bwrap, 0 `sa_run`; 0 history |
| `ac` | `:14121` | the Retroid Pocket Nova's ledcontrol (#332): LED BRIGHTNESS writes the LEDs, rgb with no colour set lights whi… | **no** | 6 | 0 | 0.1 | none | 0 bwrap, 0 `sa_run`; 0 history |
| `ad` | `:14142` | a backup does not make a missing earlier-default saves folder (D-CLOUD-172, #363): the offer instead, nothing … | **no** | 4 | 4 | 2.7 | none | 0 bwrap, 4 `sa_run`; 0 history |
| `ae` | `:14177` | cloud folder state table and archive writer/reader contracts (#365, #383) | **no** | 1 | 0 | 19.8 | none | 0 bwrap, 0 `sa_run`; 0 history |
| `af` | `:14191` | content inactivity across provider retries (#401) | **no** | 6 | 6 | 33.7 | none | 0 bwrap, 2 `sa_run`; 0 history |
| `ag` | `:14221` | settings writers retain private file permissions | **no** | 1 | 0 | 0.4 | none | 0 bwrap, 0 `sa_run`; 0 history |
| `ah` | `:14229` | melonDS update preserves settings and adds missing hotkeys | **no** | 1 | 0 | 0.1 | none | 0 bwrap, 0 `sa_run`; 0 history |

**The header claims sections `a` to `w` only** (`:7-148`): `x` to `ah`, 11 sections holding 933 of the 1,313 checks, have no claim there. **No `--old` recipe names a FAIL in `w` to `ah`,** and none of the twelve reaches past `s` or `x` (§ The runs). So **20 sections, `s` (or `x`) to `ah`, have no control that runs.**

## The runs

Every run is in this worktree, with `TMPDIR=/workspace/tmp/m6-t15/tmp`, started through `vm-qa:158`'s launcher (SIGINT and SIGPIPE to default). Each first line reads `signals: SigIgn=0000000001000004 SIGINT ignored=0 SIGPIPE ignored=0`. Outputs are in `.qa-scratch/t15/`.

| Run | Command | Exit | Wall | Banner (the busybox and its source) | PASS / FAIL / SKIP | A FAIL would mean |
| --- | --- | ---: | ---: | --- | --- | --- |
| 1, the image's busybox | `QA_SYSTEM_ROOT=<m7-signin-build-20261022-07>/build.pixelelated-GENERIC_X64.x86_64/image/system python3 -c "$SIGDFL" tools/last-good-scripts-test` | 0 | 517 s | `BusyBox v1.36.1 (2026-10-05 03:37:19 UTC) ... -- a copy of /workspace/repos/rocknix.worktrees/m7-signin-build-20261022-07/...`; rclone `v1.75.2` | 1,313 / 0 / 0, `PASSED` (after `1 HISTORICAL FEATURE GROUP(S) NOT APPLICABLE`) | a script under test no longer keeps its last good state, or prints what a screen must not, under the device's own applets: a `bug` for that script's lane. **The tree's baseline** (the coordinator, 00:36) |
| 2, the host's busybox | `python3 -c "$SIGDFL" tools/last-good-scripts-test` (`QA_SYSTEM_ROOT` unset) | 1 | 677 s | `BusyBox v1.37.0 (Ubuntu 1:1.37.0-7ubuntu1) ... -- a copy of /usr/bin/busybox`; rclone `v1.60.1-DEV`, a copy of `/usr/bin/rclone` | 994 / 319 / 0 | nothing about the tree: the run judges the host's applets (§ below). This is the run every M6 worktree makes by default |
| `bbhost` | run 2 with only the busybox swapped: `QA_SYSTEM_ROOT=/workspace/tmp/m6-t15/roots/bbhost/image/system` (the host's busybox, the image's rclone) | 1 | 678 s | `BusyBox v1.37.0 ...`; rclone `v1.75.2` | 994 / 319 / 0, every verdict equal to run 2's | the busybox alone makes the 319 |
| `rchost` | run 1 with only the rclone swapped (the image's busybox, the host's rclone 1.60.1-DEV) | 0 | 512 s | `BusyBox v1.36.1 ...`; rclone `v1.60.1-DEV` | 1,313 / 0 / 0, every verdict equal to run 1's | the rclone's version makes no verdict: stream A's cases do not tell 1.60.1 from 1.75.2 (a Q4 finding) |
| timed | run 1, each line stamped with its seconds (`tools/t15-attribution.sh`) | 0 | 515 s | as run 1 | 1,313 / 0 / 0 | the wall time by section, `04` § Q5 |
| `--help` / `--nosuch` | `tools/last-good-scripts-test --help`; `--nosuch` | 0 / 2 | — | — | — | — |

**The twelve `--old` recipes** (the header's `:167-226`), each once, under the image's busybox (`QA_SYSTEM_ROOT` on the same root):

| `BASE_REF` | rc | wall | PASS | FAIL | where it stopped |
| --- | ---: | ---: | ---: | ---: | --- |
| `1d1503180d` (default) | 2 | 211 s | 73 | 118 | `s`: `rocknix-evidence` is not at the ref |
| `53f390b1e9` | 2 | 156 s | 123 | 116 | `x`: `rocknix-corekeep` is not at the ref |
| `c15050c897` | 2 | 213 s | 88 | 103 | `s`: `rocknix-evidence` |
| `8707919349` | 2 | 156 s | 161 | 78 | `x`: `rocknix-corekeep` |
| `34aca64afd` | 2 | 70 s | 179 | 60 | `x`: `rocknix-corekeep` |
| `0f7785e6ed` | 2 | 0 s | 0 | 0 | at once: `fatal: invalid object name '0f7785e6ed'` |
| `d79281066c` | 2 | 0 s | 0 | 0 | at once: `fatal: invalid object name 'd79281066c'` |
| `cee1656c33` | 2 | 133 s | 256 | 90 | `x`: `rocknix-corekeep` |
| `28a80357ed` | 2 | 114 s | 218 | 122 | `x`: `rocknix-corekeep` |
| `3387cf5da0` | 2 | 118 s | 264 | 85 | `x`: `rocknix-corekeep` |
| `655f103cc5` | 2 | 121 s | 267 | 82 | `x`: `rocknix-corekeep` |
| `70b6c70ca7` | 2 | 119 s | 296 | 71 | `x`: `rocknix-corekeep` |

**A FAIL in an `--old` run would mean** that the guard the recipe names fires against the scripts from before its fix. **None of the twelve reaches a verdict.**
- **Two refs are dead:** `0f7785e6ed` (q's control) and `d79281066c` (p's pending and flushed control) exist nowhere in the repository.
- **The other ten** stop at `s` (`rocknix-evidence` absent at the ref) or `x` (`rocknix-corekeep`): `src_of` exits 2 for the whole run (`:320-325`). So from `s` or `x` to `ah`, **no section has a control that runs**.
- **Before each stop**, the promised sections fail, except one. `70b6c70ca7`'s `t` fails on patch application (*003 to 006 do not apply to the pinned client*), and its five `012` checks never run.

The detail is in `00`.

### The root changes, 2026-10-25 05:38 UTC

Every run recorded above under `QA_SYSTEM_ROOT` judged with the root `/workspace/repos/rocknix.worktrees/m7-signin-build-20261022-07/build.pixelelated-GENERIC_X64.x86_64/image/system`, BUILD_ID `069fc270442134fe771258418adf4e666e0473fb`. They stand as recorded.

**Why the root changed.** At about 05:25 the M7 lane, holding M6's 05:22 build grant, could not move its donor cache while T15's shells named that root. T15 stopped its five run shells at 05:30 (#662, 05:32). The M7 lane then renamed the root (`m7-signin-generic-build-20261025-01`) for its `bcc866f1` rebuild, which replaces its `image/system`. The coordinator ruled at 05:38 (#662): **every remaining and re-run T15 run uses M6's own retained donor, and no M6 run names an M7 root again.**

**The donor:** `/workspace/artifacts/m6-donor/1a0266484423/image/system`, written by the M6 coordinator at 05:37 from `m7-pixelelated-replacement20`'s GENERIC_X64 root (each file byte-equal by `cmp`). `RECORD.txt` and `SHA256SUMS` are two levels up. `sha256sum -c` from `image/system` at the lane's start: all three files OK.

| File | SHA-256 | What it is |
| --- | --- | --- |
| `usr/bin/busybox` | `79e7b20ddbe5abb6d18690dacc9b31803eb72cea949fce0a52cd9c2888829346` | BusyBox v1.36.1 (2026-10-05 03:37:19 UTC), 574456 bytes, with 146 applet links |
| `usr/bin/rclone` | `ed887da83d3e2c07ff8a...` (full in `SHA256SUMS`) | rclone v1.75.2, the recipe's `PKG_VERSION` |
| `etc/os-release` | `f537766379be27c18708...` (full in `SHA256SUMS`) | `BUILD_ID="1a026648442321609b2288c2c9c06803817f9df2"` |

**The busybox's identity with the `069fc2704421` file is argued, not claimed:** the same version string, the same build time (2026-10-05 03:37:19 UTC) and the same size (574456 bytes). The old file is gone, so no `cmp` is possible. Every run from 05:38 names the donor path and `BUILD_ID 1a0266484423` on its banner and in its `tools:` line.

## The checks that depend on the busybox

Every check whose verdict differs between run 1 (the image's BusyBox 1.36.1) and run 2 (the host's 1.37.0): **319**, each PASS under the image's and FAIL under the host's.
- **The pairing:** the two runs count 1,313 checks in the same order, so pairs align by position, and every PASS/PASS pair's text matches. One more pair differs only because its text carries a literal tab (`--set-content-remote refuses '/tab<TAB>name' ...`, PASS in both), and is not counted.
- **The attribution:** `bbhost` reproduces all 319 with the image's rclone, and `rchost` none with the host's rclone. So the busybox makes each one.
- **The applet:**
  - **`flock` is named on 61 lines** (*applet not found*: the suite's `flock` shims exec a busybox that lacks it);
  - **127 lines show its consequence** (rc 75, *another sync is already running*, a held lock);
  - **131 lines name no applet and carry no applet error.** No other refusal appears in either run, so these are *likely* `flock`'s too, **not proven**: a 1.37 applet that behaved differently without erroring would read the same.
- **By section and group:** `y/A` 95, `y` (`y1`-`y4`) 59, `t` 42, `x/D` 33, `y/CF` 26, `z` 24, `z/S315` 12, `k` 11, `n` 7, `af` 6, `ad` 4.

| # | Section / group | The applet | The host run's FAIL text (cut) |
| ---: | --- | --- | --- |
| 1 | `k` | busybox 1.37.0, no applet named on the line | rc 1: >>> why THE BACKUP COULDN'T FINISH WHILE GATHERING YOUR SETTINGS/[31mTHE BACKUP COULDN'T FINISH WHILE GATHERING YOUR SETTINGS. NOTHIN |
| 2 | `k` | busybox 1.37.0, no applet named on the line | archive lists:   |
| 3 | `k` | busybox 1.37.0, no applet named on the line | duckstation:  melonDS:  flycast:  aethersx2:  |
| 4 | `k` | busybox 1.37.0, no applet named on the line | log: held back 5 file(s) that hold only a RetroAchievements token; the emulator writes them again at its next start (#169) held back 5 file( |
| 5 | `k` | busybox 1.37.0, no applet named on the line | rc 1; scanner: silent; archives: 0 -- until #169 its anchor was lower-case only, and the emulators' keys are capitalised |
| 6 | `k` | busybox 1.37.0, no applet named on the line | rc 1: [32mKEEPING A COPY OF YOUR CURRENT SETTINGS...[0m/>>> why COULDN'T KEEP A COPY OF YOUR CURRENT SETTINGS/[31mCOULDN'T KEEP A COPY OF |
| 7 | `k` | busybox 1.37.0, no applet named on the line | ini='the player's ini' own='the player's own' |
| 8 | `k` | busybox 1.37.0, no applet named on the line | snapshot: none; .dat in it: absent |
| 9 | `k` | busybox 1.37.0, no applet named on the line | rc 1: [32mKEEPING A COPY OF YOUR CURRENT SETTINGS...[0m/>>> why COULDN'T KEEP A COPY OF YOUR CURRENT SETTINGS/[31mCOULDN'T KEEP A COPY OF |
| 10 | `k` | busybox 1.37.0, no applet named on the line | ini='the player's ini' own='the player's own' |
| 11 | `k` | busybox 1.37.0, no applet named on the line | link: symlink; screen: 2 KEEPING line(s) |
| 12 | `n` | busybox 1.37.0, no applet named on the line | no such why line; protocol lines:  |
| 13 | `n` | `flock` (its consequence: rc 75 or a held lock) | the outcome line is 'Skipped: another cloud sync is already running. Try again when it's done.' |
| 14 | `n` | busybox 1.37.0, no applet named on the line | the script's next sentence is glued to rclone's last progress line, which had no newline: '' (#153, LINK5 on MinIO, 2026-09-13) |
| 15 | `n` | busybox 1.37.0, no applet named on the line | log:  |
| 16 | `n` | `flock` (named: *applet not found*) | rc 75; stamp ''; marker: no; tail: flock: applet not found/flock: applet not found/Skipped: another cloud sync is already running. Try again |
| 17 | `n` | `flock` (its consequence: rc 75 or a held lock) | the outcome line is 'Skipped: another cloud sync is already running. Try again when it's done.' -- tools/cloud-round-trip's ALLOWED_SCRIPT w |
| 18 | `n` | `flock` (its consequence: rc 75 or a held lock) | rc 75 after 1s; log:  -- a fixed ceiling ends the transfers a deliberate run exists for |
| 19 | `t` | `flock` (its consequence: rc 75 or a held lock) | rc 75; out: ; stamp: none |
| 20 | `t` | `flock` (its consequence: rc 75 or a held lock) | rc 75; out:  |
| 21 | `t` | `flock` (its consequence: rc 75 or a held lock) | rc 75; stamp: none; log:  |
| 22 | `t` | busybox 1.37.0, no applet named on the line | state mtime 1789380000 vs 1789380000, content: {   "online": true } ; probes:  (#186 PL-03) |
| 23 | `t` | `flock` (named: *applet not found*) | rc 75; log: ; err: flock: applet not found/logger -t raofflineproxy-ctl scan: another scan or top-up is running/ (#186 PL-23/PL-02) |
| 24 | `t` | busybox 1.37.0, no applet named on the line | jobs:  (#186 PL-23) |
| 25 | `t` | busybox 1.37.0, no applet named on the line | out: ; stamp: ; export: 101 102 105  |
| 26 | `t` | `flock` (its consequence: rc 75 or a held lock) | rc 75; out:  |
| 27 | `t` | `flock` (its consequence: rc 75 or a held lock) | rc 75; out: ; stamp:  -- a failed game read as COMPLETED (#186 PL-24) |
| 28 | `t` | `flock` (its consequence: rc 75 or a held lock) | rc 75; jobs: ; out:  |
| 29 | `t` | `flock` (named: *applet not found*) | rc 75; out: ; stamp: ; err: flock: applet not found/logger -t raofflineproxy-ctl scan: another scan or top-up is running/ |
| 30 | `t` | `flock` (its consequence: rc 75 or a held lock) | rc 75; jobs: 0; out:  |
| 31 | `t` | `flock` (its consequence: rc 75 or a held lock) | rc 75; out:  |
| 32 | `t` | `flock` (its consequence: rc 75 or a held lock) | rc 75; out:  |
| 33 | `t` | `flock` (its consequence: rc 75 or a held lock) | rc 75; probes: ; sleeps: ; mark: none; log:  (#186 PL-04) |
| 34 | `t` | busybox 1.37.0, no applet named on the line | log: ; stamp:  |
| 35 | `t` | `flock` (its consequence: rc 75 or a held lock) | rc 75; probes: ; log:  |
| 36 | `t` | `flock` (its consequence: rc 75 or a held lock) | rc 75; probes:  |
| 37 | `t` | `flock` (its consequence: rc 75 or a held lock) | rc 75; probes: ; log:  |
| 38 | `t` | busybox 1.37.0, no applet named on the line | probes:  |
| 39 | `t` | `flock` (its consequence: rc 75 or a held lock) | rc 75; cached_game_ids.txt last-topup-attempt proxy.sqlite3  |
| 40 | `t` | `flock` (its consequence: rc 75 or a held lock) | rc 75; log:  |
| 41 | `t` | `flock` (its consequence: rc 75 or a held lock) | rc 75; log: 2026-10-25 00:32:35 index ran offline: the hash library did not come (index-pending); the library is listed once at the link's r |
| 42 | `t` | `flock` (its consequence: rc 75 or a held lock) | rc 75; probes: ; log:  |
| 43 | `t` | `flock` (its consequence: rc 75 or a held lock) | rc 75; log: ; stamp:  |
| 44 | `t` | `flock` (its consequence: rc 75 or a held lock) | rc 75; probes: 0; mark mtime 1792881156 vs 1792881156 -- a probe that reached nothing was counted as the half hour's attempt (#186 PL-04) |
| 45 | `t` | `flock` (its consequence: rc 75 or a held lock) | rc 75; mark mtime 1792881156 vs 1792881156 |
| 46 | `t` | `flock` (its consequence: rc 75 or a held lock) | rc 75; probes:  |
| 47 | `t` | `flock` (its consequence: rc 75 or a held lock) | rc 75; probes:  |
| 48 | `t` | `flock` (its consequence: rc 75 or a held lock) | rc 75; took 890s; stamp: ; smart: ; log:  -- the fifteen minutes were not one bound (#186 PL-28) |
| 49 | `t` | `flock` (its consequence: rc 75 or a held lock) | rc 75; stamp: ; log:  |
| 50 | `t` | `flock` (its consequence: rc 75 or a held lock) | rc 75; out: ; stamp:  |
| 51 | `t` | `flock` (its consequence: rc 75 or a held lock) | rc 75; seen: ; left: cached_game_ids.txt last-topup-attempt proxy.sqlite3  |
| 52 | `t` | `flock` (its consequence: rc 75 or a held lock) | rc 75; seen: ; left: cached_game_ids.txt proxy.sqlite3  |
| 53 | `t` | `flock` (its consequence: rc 75 or a held lock) | disable rc 0; helper none gone: 1; disable said: logger -t raofflineproxy-ctl disable: a scan or top-up holds the lock and left no pid; wait |
| 54 | `t` | busybox 1.37.0, no applet named on the line | running: '' (was route=run at=<epoch>images before #258 PL-013) |
| 55 | `t` | busybox 1.37.0, no applet named on the line | disable rc 0; helper none gone: 1; running left: no; helper times: ; disable said:  (#258 PL-013) |
| 56 | `t` | `flock` (its consequence: rc 75 or a held lock) | rc 75; running left: route=scan at=1792884806 index=3 total=9 name=dead |
| 57 | `t` | busybox 1.37.0, no applet named on the line | running: '' |
| 58 | `t` | busybox 1.37.0, no applet named on the line | disable rc 0; helper none gone: 1; running left: no; helper times:  |
| 59 | `t` | `flock` (its consequence: rc 75 or a held lock) | rc 75; log:  (#186 PL-17) |
| 60 | `t` | `flock` (its consequence: rc 75 or a held lock) | rc 75; jobs: ; log:  -- the walk stopped at the same ten cached files (#186 PL-17) |
| 61 | `x/D` | `flock` (its consequence: rc 75 or a held lock) | PL-013 ctl: rc 75 after 0.02s; out: ; stamp: ; helper:  -- the INT trap waited for the foreground image pass |
| 62 | `x/D` | busybox 1.37.0, no applet named on the line | PL-013 ctl: the image pass started at ? and the run exited at 1792888479.713265914 -- 1792888479.71s |
| 63 | `x/D` | busybox 1.37.0, no applet named on the line | #308 gpt F-RA-11: disable rc 0 after 10.12s; helper none gone: 1; disable said: logger -t raofflineproxy-ctl disable: the running scan or to |
| 64 | `x/D` | `flock` (its consequence: rc 75 or a held lock) | PL-055 / claude G-D-13: rc 75; stamp: ; marker: kept; log:  -- a listing that failed was stamped COMPLETED, or the marker went |
| 65 | `x/D` | `flock` (its consequence: rc 75 or a held lock) | PL-055: rc 75; stamp: ; marker: kept |
| 66 | `x/D` | `flock` (its consequence: rc 75 or a held lock) | PL-055: rc 75; probes: 0; log: ; marker: kept |
| 67 | `x/D` | `flock` (its consequence: rc 75 or a held lock) | PL-055: rc 75; log: ; marker: kept |
| 68 | `x/D` | `flock` (its consequence: rc 75 or a held lock) | PL-055: rc 75; stamp: ; marker: kept |
| 69 | `x/D` | busybox 1.37.0, no applet named on the line | PL-055: the run exited 75; marker: kept |
| 70 | `x/D` | `flock` (its consequence: rc 75 or a held lock) | PL-059: rc 75; out: ; stamp:  -- the truncation was in the log alone |
| 71 | `x/D` | busybox 1.37.0, no applet named on the line | PL-059: second scan's jobs:  -- the same first ten files held the front of the walk |
| 72 | `x/D` | busybox 1.37.0, no applet named on the line | PL-059: 0 distinct files over two scans |
| 73 | `x/D` | `flock` (its consequence: rc 75 or a held lock) | PL-059: rc 75; out: ; stamp: ; cursor: none |
| 74 | `x/D` | `flock` (its consequence: rc 75 or a held lock) | PL-060: rc 75; out: ; stamp:  -- the image pass's failure was dropped |
| 75 | `x/D` | `flock` (its consequence: rc 75 or a held lock) | PL-060: rc 75; image pass run: 0 time(s); out:  -- the nothing-new branch exited before the pass |
| 76 | `x/D` | `flock` (its consequence: rc 75 or a held lock) | PL-060: rc 75; image pass run: 0; stamp:  |
| 77 | `x/D` | `flock` (its consequence: rc 75 or a held lock) | PL-060: rc 75; stamp:  |
| 78 | `x/D` | `flock` (its consequence: rc 75 or a held lock) | PL-060: rc 75; stamp:  |
| 79 | `x/D` | `flock` (its consequence: rc 75 or a held lock) | rc 75; stamp:  -- a crash read as the sweep working |
| 80 | `x/D` | `flock` (its consequence: rc 75 or a held lock) | #308 claude F-RA-06: rc 75; jobs:  -- the listing read the base file alone |
| 81 | `x/D` | busybox 1.37.0, no applet named on the line | #308 claude F-RA-06: jobs:  |
| 82 | `x/D` | busybox 1.37.0, no applet named on the line | #308 gpt F-RA-14: jobs:  -- a patch path alone read as a complete cache |
| 83 | `x/D` | `flock` (its consequence: rc 75 or a held lock) | #308 claude F-RA-10: rc 75; stamp:  -- the recently played pass's new game was not counted as added |
| 84 | `x/D` | `flock` (its consequence: rc 75 or a held lock) | #308 gpt F-RA-15: rc 75; jobs: ; stamp:  -- a cache operation was counted as a new game |
| 85 | `x/D` | `flock` (its consequence: rc 75 or a held lock) | #308 gpt F-RA-13: rc 75; probes: ; log:  -- PPSSPP's play was invisible to the question |
| 86 | `x/D` | `flock` (its consequence: rc 75 or a held lock) | #308 gpt F-RA-13: rc 75; probes:  |
| 87 | `x/D` | busybox 1.37.0, no applet named on the line | #308 gpt F-RA-10 ctl: the scan's image pass:  -- no bound but the helper's own |
| 88 | `x/D` | `flock` (its consequence: rc 75 or a held lock) | #308 gpt F-RA-10 ctl: images rc 75:  |
| 89 | `x/D` | `flock` (its consequence: rc 75 or a held lock) | #308 gpt F-RA-10 ctl: refresh rc 75:  -- no bound but the helper's own |
| 90 | `x/D` | `flock` (its consequence: rc 75 or a held lock) | PL-060 follow-up: rc 75; out: ; stamp:  -- a badge the server does not have failed the scan |
| 91 | `x/D` | `flock` (its consequence: rc 75 or a held lock) | PL-060 follow-up: rc 75; requested:  -- an absent badge was asked for at every pass |
| 92 | `x/D` | `flock` (its consequence: rc 75 or a held lock) | PL-060 follow-up: rc 75; out:  |
| 93 | `x/D` | `flock` (its consequence: rc 75 or a held lock) | PL-060 follow-up: rc 75; requested:  |
| 94 | `y` | busybox 1.37.0, no applet named on the line | #307 PL-004: rc 1; the archive lists:  -- a path with a space split into two that do not exist |
| 95 | `y` | busybox 1.37.0, no applet named on the line | #307 PL-004: rc 1; archive:  |
| 96 | `y` | busybox 1.37.0, no applet named on the line | #307 PL-004: rc 1; archives: 0; why: 'A SETTINGS BACKUP OR RESTORE IS ALREADY RUNNING' -- find's error went to /dev/null and a short archive |
| 97 | `y` | `flock` (named: *applet not found*) | #307 PL-036: rc 1; link: symlink; f1='file1'; screen: flock: applet not found/[31mA SETTINGS BACKUP OR RESTORE IS ALREADY RUNNING. WAIT FOR |
| 98 | `y` | busybox 1.37.0, no applet named on the line | #307 PL-035: rc 1; archive: ; SECRET in:  |
| 99 | `y` | `flock` (named: *applet not found*) | #307 PL-035: rc 1; archive: ; screen: YOUR OWN BACKUP LIST IS EMPTY, SO THE STANDARD ONE WAS USED./flock: applet not found/[31mA SETTINGS B |
| 100 | `y` | busybox 1.37.0, no applet named on the line | #307 PL-038: rc 1; archives: 0; why: 'A SETTINGS BACKUP OR RESTORE IS ALREADY RUNNING' -- it was staged and silently left out of the archive |
| 101 | `y` | busybox 1.37.0, no applet named on the line | #307 PL-008: rc 1; members under the backup folder:  |
| 102 | `y` | busybox 1.37.0, no applet named on the line | #307 PL-008: rc 1; members under it:  |
| 103 | `y` | busybox 1.37.0, no applet named on the line | #307 PL-009: rc 1; f1='LIVE'; why: 'A SETTINGS BACKUP OR RESTORE IS ALREADY RUNNING' -- the failed copy read as an empty device and the rest |
| 104 | `y` | `flock` (named: *applet not found*) | #308 F-BR-17: rc 1; why 'A SETTINGS BACKUP OR RESTORE IS ALREADY RUNNING'; screen: flock: applet not found/[31mA SETTINGS BACKUP OR RESTORE |
| 105 | `y` | busybox 1.37.0, no applet named on the line | #308 F-BR-19: rc 1; why 'A SETTINGS BACKUP OR RESTORE IS ALREADY RUNNING'; archive:  |
| 106 | `y` | busybox 1.37.0, no applet named on the line | #307 PL-005: rc 1; why 'A SETTINGS BACKUP OR RESTORE IS ALREADY RUNNING'; archives: ; secret in an archive:  |
| 107 | `y` | busybox 1.37.0, no applet named on the line | #307 PL-006: rc 1; why 'A SETTINGS BACKUP OR RESTORE IS ALREADY RUNNING'; archives: 0 -- the capital P passed |
| 108 | `y` | busybox 1.37.0, no applet named on the line | #307 PL-006: rc 1; why 'A SETTINGS BACKUP OR RESTORE IS ALREADY RUNNING' |
| 109 | `y` | busybox 1.37.0, no applet named on the line | #307 PL-006: rc 1; why 'A SETTINGS BACKUP OR RESTORE IS ALREADY RUNNING' |
| 110 | `y` | busybox 1.37.0, no applet named on the line | #307 PL-006: rc 1; why 'A SETTINGS BACKUP OR RESTORE IS ALREADY RUNNING' |
| 111 | `y` | busybox 1.37.0, no applet named on the line | #307 PL-006: rc 1; why 'A SETTINGS BACKUP OR RESTORE IS ALREADY RUNNING' |
| 112 | `y` | busybox 1.37.0, no applet named on the line | #307 PL-006: rc 1; why 'A SETTINGS BACKUP OR RESTORE IS ALREADY RUNNING'; log:  |
| 113 | `y` | `flock` (named: *applet not found*) | #307 PL-007: rc 1; x.cfg='ORIGINAL' f1='file1' new.cfg: gone; screen: flock: applet not found/[31mA SETTINGS BACKUP OR RESTORE IS ALREADY R |
| 114 | `y` | busybox 1.37.0, no applet named on the line | #307 PL-007: the mark at extraction: '' |
| 115 | `y` | busybox 1.37.0, no applet named on the line | #307 PL-039: rc 1; f1='LIVE'; why: 'A SETTINGS BACKUP OR RESTORE IS ALREADY RUNNING' -- the extraction ran with no mark for the boot to fini |
| 116 | `y` | busybox 1.37.0, no applet named on the line | #307 PL-010: rc 1; rclone.conf='MINE' id='this-device' |
| 117 | `y` | busybox 1.37.0, no applet named on the line | #307 PL-010: rc 1; rclone.conf='MINE' id='this-device' |
| 118 | `y` | busybox 1.37.0, no applet named on the line | #307 PL-010: rc 1; archive:  |
| 119 | `y` | busybox 1.37.0, no applet named on the line | #537: tar credential directory changed (rc 1) |
| 120 | `y` | busybox 1.37.0, no applet named on the line | #537: zip credential directory changed (rc 1) |
| 121 | `y` | busybox 1.37.0, no applet named on the line | #307 PL-037: rc 1; es_settings.cfg after the restore: 'EDITED' |
| 122 | `y` | busybox 1.37.0, no applet named on the line | #307 PL-077: rc 1/1; archives: 0 -- the second took the first one's name |
| 123 | `y` | `flock` (named: *applet not found*) | #308 F-BR-08: rc 1; f1='file1'; screen: flock: applet not found/[31mA SETTINGS BACKUP OR RESTORE IS ALREADY RUNNING. WAIT FOR IT TO FINISH, |
| 124 | `y` | busybox 1.37.0, no applet named on the line | #308 F-BR-07: rc 1; root: ARCHIVED_ROCKNIX_BACKUP-20-01-01_00_00_00.zip ; archive/:  |
| 125 | `y` | `flock` (named: *applet not found*) | #308 F-BR-12: screen: flock: applet not found/[31mA SETTINGS BACKUP OR RESTORE IS ALREADY RUNNING. WAIT FOR IT TO FINISH, THEN TRY AGAIN.[ |
| 126 | `y` | `flock` (named: *applet not found*) | #308 F-BR-12: why 'A SETTINGS BACKUP OR RESTORE IS ALREADY RUNNING'; screen: flock: applet not found/[31mA SETTINGS BACKUP OR RESTORE IS AL |
| 127 | `y` | busybox 1.37.0, no applet named on the line | #308 F-BR-13: rc 1; raofflineproxy/q: held; p7other/q: held |
| 128 | `y` | busybox 1.37.0, no applet named on the line | #308 gpt F-BR-13: rc 1; es_systems.cfg is a symlink |
| 129 | `y` | busybox 1.37.0, no applet named on the line | #308 gpt F-BR-14: why 'A SETTINGS BACKUP OR RESTORE IS ALREADY RUNNING'; f1='LIVE'; snapshots: 0 |
| 130 | `y` | busybox 1.37.0, no applet named on the line | #308 gpt F-BR-16: rc 1; system.cfg in the archive: ''; directory entries: 0 |
| 131 | `y` | busybox 1.37.0, no applet named on the line | #308 F-BR-09: rc 1; mktemp calls:  |
| 132 | `y` | busybox 1.37.0, no applet named on the line | #308 gpt F-BR-17: rc 1; left: /workspace/tmp/m6-t15/tmp/tmp.kEAvzHFy5G/p7/storage/.cache: . .. backuptool-staging.p7dead  /workspace/tmp/m6- |
| 133 | `y` | busybox 1.37.0, no applet named on the line | #308 F-BR-18: rc 1; archives at /storage/roms/backup: 0; why 'A SETTINGS BACKUP OR RESTORE IS ALREADY RUNNING' |
| 134 | `y` | busybox 1.37.0, no applet named on the line | #307 audit G-B-01: rc 1; members: ; planted value in the archive: 0 |
| 135 | `y` | busybox 1.37.0, no applet named on the line | #307 audit G-B-01: rc 1; why 'A SETTINGS BACKUP OR RESTORE IS ALREADY RUNNING'; archives: 0 -- *.backup was not read |
| 136 | `y` | busybox 1.37.0, no applet named on the line | #307 audit G-B-03: rc 1; why 'A SETTINGS BACKUP OR RESTORE IS ALREADY RUNNING' -- the unanchored sk- refused a clean backup as a sign-in |
| 137 | `y` | busybox 1.37.0, no applet named on the line | #307 audit G-B-02: rc 1; f1='LIVE'; why 'A SETTINGS BACKUP OR RESTORE IS ALREADY RUNNING' |
| 138 | `y` | busybox 1.37.0, no applet named on the line | #307 audit G-B-12: rc 1; members:  |
| 139 | `y` | busybox 1.37.0, no applet named on the line | #307 audit G-B-11: rc 1; kept: 0 of 4; root: ARCHIVED_ROCKNIX_BACKUP-20-01-01_00_00_00.zip ARCHIVED_ROCKNIX_BACKUP-20-01-02_00_00_00.zip ARC |
| 140 | `y` | busybox 1.37.0, no applet named on the line | #307 audit G-B-02: rc 1; mybackups: ; standard folder: 0 |
| 141 | `y` | busybox 1.37.0, no applet named on the line | #307 audit G-B-09: rc 1; test/seed='device copy' -- the seed list overwrote the archive's own file |
| 142 | `y` | busybox 1.37.0, no applet named on the line | #307 audit G-B-08: rc 1; f1='LIVE'; why 'A SETTINGS BACKUP OR RESTORE IS ALREADY RUNNING'; the folder holds:  |
| 143 | `y` | `flock` (its consequence: rc 75 or a held lock) | #307 audit G-B-15: IMG:find IMG:tar HOST:flock IMG:date IMG:mktemp  |
| 144 | `y` | busybox 1.37.0, no applet named on the line | #307 PL-046: rc 1; archive: none; plant in it: 0; summary:  |
| 145 | `y` | busybox 1.37.0, no applet named on the line | #307 PL-077: rc 1/1; archives:  |
| 146 | `y` | `flock` (its consequence: rc 75 or a held lock) | #307 audit G-B-15: IMG:head HOST:flock IMG:find IMG:mkdir IMG:mv IMG:rm IMG:df IMG:date  |
| 147 | `y` | `flock` (its consequence: rc 75 or a held lock) | #308 F-PB-16: note: dump         NOT KEPT -- the cores folder could not be locked, and one dump at a time is what keeps the free-space floor |
| 148 | `y` | `flock` (its consequence: rc 75 or a held lock) | #308 F-PB-16: note: dump         NOT KEPT -- the cores folder could not be locked, and one dump at a time is what keeps the free-space floor |
| 149 | `y` | busybox 1.37.0, no applet named on the line | #308 F-PB-15: left: core.emulationstation.4000.4242.txt core.retroarch.1000.1.gz core.retroarch.1000.1.txt core.retroarch.2000.1.gz core.ret |
| 150 | `y` | busybox 1.37.0, no applet named on the line | #308 F-PB-15: notes: core.retroarch.6001.4242.txt core.retroarch.6002.4242.txt core.retroarch.6003.4242.txt core.retroarch.6004.4242.txt cor |
| 151 | `y` | `flock` (its consequence: rc 75 or a held lock) | #308 F-PB-20: note: dump         NOT KEPT -- the cores folder could not be locked, and one dump at a time is what keeps the free-space floor |
| 152 | `y` | busybox 1.37.0, no applet named on the line | #308 F-PB-21: the second note existed mid-way through the first dump: yes; left: core.emulationstation.8001.4242.txt core.retroarch.8000.424 |
| 153 | `y/A` | `flock` (named: *applet not found*) | N.nes: kept; rc 75; out: flock: applet not found/flock: applet not found/flock: applet not found/Skipped: another cloud sync is already runn |
| 154 | `y/A` | `flock` (named: *applet not found*) | N.nes: kept; rc 75; out: flock: applet not found/flock: applet not found/flock: applet not found/Skipped: another cloud sync is already runn |
| 155 | `y/A` | `flock` (named: *applet not found*) | rc 75; gb's sync: ; B.gb kept; out: flock: applet not found/flock: applet not found/flock: applet not found/Skipped: another cloud sync is a |
| 156 | `y/A` | `flock` (its consequence: rc 75 or a held lock) | second apply rc 75; plan: still there |
| 157 | `y/A` | `flock` (named: *applet not found*) | bios on the device: (none?); out: flock: applet not found/flock: applet not found/flock: applet not found/Skipped: another cloud sync is alr |
| 158 | `y/A` | `flock` (its consequence: rc 75 or a held lock) | gb/A.gb missing, nes/N.nes missing; rc 75 |
| 159 | `y/A` | busybox 1.37.0, no applet named on the line | units:  |
| 160 | `y/A` | `flock` (named: *applet not found*) | A.gb in the cloud: no; rc 75; out: flock: applet not found/flock: applet not found/flock: applet not found/Skipped: another cloud sync is al |
| 161 | `y/A` | `flock` (named: *applet not found*) | B.gb on the device: no; rc 75; out: flock: applet not found/flock: applet not found/flock: applet not found/Skipped: another cloud sync is a |
| 162 | `y/A` | `flock` (named: *applet not found*) | A.srm missing, A.gb not sent; rc 75; out: flock: applet not found/flock: applet not found/flock: applet not found/Skipped: another cloud syn |
| 163 | `y/A` | `flock` (its consequence: rc 75 or a held lock) | rc 75; replaced root holds: ./2099_01_01-000000/gb/Z.srm ; the run's own folder was pruned because 2099_... sorts after it (F-CS-06 gpt, F-C |
| 164 | `y/A` | busybox 1.37.0, no applet named on the line | the 2099 folder is still there beside the run's own |
| 165 | `y/A` | `flock` (its consequence: rc 75 or a held lock) | rc 75; the folder holds: 2097_01_01-000000-QA-ROCKNIX_SETTINGS.tar.gz 2098_01_01-000000-QA-ROCKNIX_SETTINGS.tar.gz 2099_01_01-000000-QA-ROCK |
| 166 | `y/A` | `flock` (its consequence: rc 75 or a held lock) | rc 75; replaced holds: ./2099_01_01-000000/gb/Y.srm  (F-CS-06 gpt, prune_replaced_local) |
| 167 | `y/A` | `flock` (its consequence: rc 75 or a held lock) | exit 75, stamp 'none', outcome 'Skipped: another cloud sync is already running. Try again when it's done.' -- [ overall -eq 0 ] skipped the  |
| 168 | `y/A` | busybox 1.37.0, no applet named on the line | the saves phase never reported 9; log:  |
| 169 | `y/A` | `flock` (its consequence: rc 75 or a held lock) | exit 75, stamp 'none', outcome 'Skipped: another cloud sync is already running. Try again when it's done.' |
| 170 | `y/A` | `flock` (named: *applet not found*) | units: ; out: flock: applet not found/flock: applet not found/flock: applet not found/Skipped: another cloud sync is already running. Try ag |
| 171 | `y/A` | busybox 1.37.0, no applet named on the line | saves folder's state: removed; rc 1; retired:  |
| 172 | `y/A` | busybox 1.37.0, no applet named on the line | took 11s, rc 1, entry:  -- the commit ran beside another capture's (F-CS-14) |
| 173 | `y/A` | busybox 1.37.0, no applet named on the line | rc 1; the fresh seal was collected -- another capture's pending version (F-CS-14) -- or the capture ended before its GC |
| 174 | `y/A` | busybox 1.37.0, no applet named on the line | took 14s, rc 1 -- timedatectl ran unbounded on the synchronous game-exit path |
| 175 | `y/A` | busybox 1.37.0, no applet named on the line | manifest: missing; cache: capture-failures manifest-QA-deadbeef01.json.corrupt-1792888649 stage  |
| 176 | `y/A` | busybox 1.37.0, no applet named on the line | Game.state2's unit:  -- the source's entry was inherited wholesale because the bytes matched |
| 177 | `y/A` | `flock` (named: *applet not found*) | exit 75, stamp 'none'; out: flock: applet not found/flock: applet not found/flock: applet not found/Skipped: another cloud sync is already r |
| 178 | `y/A` | busybox 1.37.0, no applet named on the line | the ROM did not come down -- the case would pass for the wrong reason |
| 179 | `y/A` | `flock` (named: *applet not found*) | exit 75, stamp 'none'; out: flock: applet not found/flock: applet not found/flock: applet not found/Skipped: another cloud sync is already r |
| 180 | `y/A` | `flock` (named: *applet not found*) | rc 75; out: flock: applet not found/flock: applet not found/flock: applet not found/Skipped: another cloud sync is already running. Try agai |
| 181 | `y/A` | `flock` (named: *applet not found*) | rc 75; bios.bin missing; out: flock: applet not found/flock: applet not found/flock: applet not found/Skipped: another cloud sync is already |
| 182 | `y/A` | `flock` (its consequence: rc 75 or a held lock) | rc 75; units: ; argv:  |
| 183 | `y/A` | `flock` (its consequence: rc 75 or a held lock) | took 1s (rc 75) -- sleep 2, sleep 2 and sleep 3 ran with nobody reading |
| 184 | `y/A` | busybox 1.37.0, no applet named on the line | summary:  |
| 185 | `y/A` | busybox 1.37.0, no applet named on the line | summary:  |
| 186 | `y/A` | `flock` (its consequence: rc 75 or a held lock) | the planted partial is still there after a run with no record (rc 75) |
| 187 | `y/A` | busybox 1.37.0, no applet named on the line | the partial was swept -- the whole saves tree, the ROM library, was walked after a transfer that completed (F-CS-08) |
| 188 | `y/A` | `flock` (its consequence: rc 75 or a held lock) | the partial survived a failed transfer's sweep (rc 75) |
| 189 | `y/A` | busybox 1.37.0, no applet named on the line | log:  -- the warning covered the settings folder only, and only under a condition that can no longer hold |
| 190 | `y/A` | `flock` (its consequence: rc 75 or a held lock) | ran it: no; rc 75; why: ; outcome 'Skipped: another cloud sync is already running. Try again when it's done.' -- the conf was sourced with t |
| 191 | `y/A` | `flock` (its consequence: rc 75 or a held lock) | ran it: no; rc 75; why: ; outcome 'Skipped: another cloud sync is already running. Try again when it's done.' -- the conf was sourced with t |
| 192 | `y/A` | busybox 1.37.0, no applet named on the line | size call: (none) |
| 193 | `y/A` | busybox 1.37.0, no applet named on the line | ls call: (none) |
| 194 | `y/A` | busybox 1.37.0, no applet named on the line | restored:  -- lexical order put the undated name last (F-CS-35) |
| 195 | `y/A` | busybox 1.37.0, no applet named on the line | restored:  |
| 196 | `y/A` | `flock` (named: *applet not found*) | rc 75; cloud A.srm: older; out: flock: applet not found/flock: applet not found/flock: applet not found/Skipped: another cloud sync is alrea |
| 197 | `y/A` | busybox 1.37.0, no applet named on the line | saves-root:  |
| 198 | `y/A` | busybox 1.37.0, no applet named on the line | removed line ''; B.gb kept, sub/C.gb kept -- the totals were the plan's, counted before the delete ran (F-CS-26) |
| 199 | `y/A` | busybox 1.37.0, no applet named on the line | in the cloud:  -- .fla is missing from SAVE_EXCLUDES |
| 200 | `y/A` | busybox 1.37.0, no applet named on the line | plan 'n64/remove/1/4'; Game.fla kept -- a save the saves tier owns was removed as content (gpt F-CS-02) |
| 201 | `y/A` | busybox 1.37.0, no applet named on the line | scummvm README missing, bios/README.txt left, card.dat 'this device's own vmu' |
| 202 | `y/A` | busybox 1.37.0, no applet named on the line | scan disagrees (system:cloud-only/here-only): bios:1/0 dc:1/0 scummvm:2/0  -- the cloud-side count and the transfer describe different sets  |
| 203 | `y/A` | `flock` (its consequence: rc 75 or a held lock) | rc 75; stamp 'none' -- a bare 69 reads SKIPPED, NO NETWORK on the row over a system that did arrive (F-CS-24) |
| 204 | `y/A` | `flock` (its consequence: rc 75 or a held lock) | rc 75; New.srm in the cloud: no; stamp 'none' |
| 205 | `y/A` | `flock` (its consequence: rc 75 or a held lock) | rc 75; stamp 'none' |
| 206 | `y/A` | busybox 1.37.0, no applet named on the line | why:  |
| 207 | `y/A` | `flock` (its consequence: rc 75 or a held lock) | G-D-01/02: rc 75; image pass run: 0 time(s); out:  -- COMPLETED over images nobody looked at |
| 208 | `y/A` | `flock` (its consequence: rc 75 or a held lock) | G-D-01/02: rc 75; image pass run: 0 |
| 209 | `y/A` | `flock` (its consequence: rc 75 or a held lock) | gpt G-D-01: rc 75; stamp: ; image pass: 0 -- a pass that never ran read as done |
| 210 | `y/A` | `flock` (its consequence: rc 75 or a held lock) | claude G-D-03: rc 75; the helper saw: ; 1792888735.26s; out:  |
| 211 | `y/A` | `flock` (its consequence: rc 75 or a held lock) | gpt G-D-06: rc 75; out:  -- a cursor write failure passed over |
| 212 | `y/A` | `flock` (its consequence: rc 75 or a held lock) | gpt G-D-06: rc 75; cursor before '', after '' |
| 213 | `y/A` | `flock` (its consequence: rc 75 or a held lock) | gpt G-D-04: rc 75; jobs: ; stamp:  |
| 214 | `y/A` | busybox 1.37.0, no applet named on the line | claude G-D-08: jobs:  |
| 215 | `y/A` | busybox 1.37.0, no applet named on the line | gpt G-D-03: the run exited 75; marker: kept -- the older run acknowledged the newer notification |
| 216 | `y/A` | busybox 1.37.0, no applet named on the line | claude G-D-10: 2026-10-25 00:39:08 index ran offline: the hash library did not come (index-pending); the library is listed once at the link' |
| 217 | `y/A` | `flock` (named: *applet not found*) | ran it: no; rc 75; out: flock: applet not found/flock: applet not found/flock: applet not found/Skipped: another cloud sync is already runni |
| 218 | `y/A` | `flock` (named: *applet not found*) | rc 75; game1.srm missing, victim home; out: flock: applet not found/flock: applet not found/flock: applet not found/Skipped: another cloud s |
| 219 | `y/A` | `flock` (named: *applet not found*) | rc 75; game1.srm missing, victim left; out: flock: applet not found/flock: applet not found/flock: applet not found/Skipped: another cloud s |
| 220 | `y/A` | `flock` (its consequence: rc 75 or a held lock) | rc 75; why: ; B.gb kept |
| 221 | `y/A` | `flock` (named: *applet not found*) | preview rc 0, apply rc 75; units: ; out: flock: applet not found/flock: applet not found/flock: applet not found/Skipped: another cloud sync |
| 222 | `y/A` | `flock` (named: *applet not found*) | rc 75; out: flock: applet not found/flock: applet not found/flock: applet not found/flock: applet not found/flock: applet not found/Skipped: |
| 223 | `y/A` | `flock` (its consequence: rc 75 or a held lock) | outcome line 'Skipped: another cloud sync is already running. Try again when it's done.' |
| 224 | `y/A` | `flock` (its consequence: rc 75 or a held lock) | rc 75; outcome 'Skipped: another cloud sync is already running. Try again when it's done.' |
| 225 | `y/A` | `flock` (its consequence: rc 75 or a held lock) | rc 75; cloud:  |
| 226 | `y/A` | `flock` (its consequence: rc 75 or a held lock) | rc 75; cloud:  |
| 227 | `y/A` | `flock` (its consequence: rc 75 or a held lock) | rc 75; cloud:  |
| 228 | `y/A` | `flock` (named: *applet not found*) | rc 75; flock: applet not found/flock: applet not found/flock: applet not found/Skipped: another cloud sync is already running. Try again whe |
| 229 | `y/A` | `flock` (its consequence: rc 75 or a held lock) | restore rc 75; scan row 'scummvm/10/1/0/1/0/10/0' (name/cloud/sup/device/...) -- the list below title/ was counted as a ROM |
| 230 | `y/A` | busybox 1.37.0, no applet named on the line | list on the device: no; scan row 'scummvm/51/1/0/0/0/0/0' |
| 231 | `y/A` | busybox 1.37.0, no applet named on the line | rc 1; entries:  |
| 232 | `y/A` | `flock` (its consequence: rc 75 or a held lock) | rc 75; N.nes missing; stamp '' |
| 233 | `y/A` | `flock` (its consequence: rc 75 or a held lock) | rc 75; N.nes in the cloud no; stamp '' |
| 234 | `y/A` | `flock` (its consequence: rc 75 or a held lock) | rc 75; stamp '' -- a unit that moved nothing counted as progress |
| 235 | `y/A` | `flock` (named: *applet not found*) | rc 75; New.srm in the cloud: no; stamp 'none'; out: flock: applet not found/flock: applet not found/flock: applet not found/Skipped: another |
| 236 | `y/A` | `flock` (named: *applet not found*) | rc 75; stamp 'none'; out: flock: applet not found/flock: applet not found/flock: applet not found/Skipped: another cloud sync is already run |
| 237 | `y/A` | `flock` (its consequence: rc 75 or a held lock) | 1s, rc 75; why:  |
| 238 | `y/A` | `flock` (its consequence: rc 75 or a held lock) | 1s, rc 75; why:  |
| 239 | `y/A` | `flock` (its consequence: rc 75 or a held lock) | rc 75; screen: ; log:  |
| 240 | `y/A` | `flock` (named: *applet not found*) | ran it: no; conf restored; rc 75; out: flock: applet not found/flock: applet not found/flock: applet not found/Skipped: another cloud sync i |
| 241 | `y/A` | `flock` (named: *applet not found*) | ran it: no; conf restored; rc 75; out: flock: applet not found/flock: applet not found/flock: applet not found/Skipped: another cloud sync i |
| 242 | `y/A` | `flock` (named: *applet not found*) | rc 75; RCLONEOPTS lines 2; out: flock: applet not found/flock: applet not found/flock: applet not found/Skipped: another cloud sync is alrea |
| 243 | `y/A` | busybox 1.37.0, no applet named on the line | the partial is still there: the tree was recorded clean across a content restore that was cut |
| 244 | `y/A` | `flock` (its consequence: rc 75 or a held lock) | rc 75; in the cloud:  |
| 245 | `y/A` | `flock` (its consequence: rc 75 or a held lock) | rc 75; the record is gone -- every saves restore after a content restore would walk the library |
| 246 | `y/A` | `flock` (its consequence: rc 75 or a held lock) | rc 75; the reader gave "Skipped: another cloud sync is already running. Try again when it's done." "Skipped: another cloud sync is already r |
| 247 | `y/A` | busybox 1.37.0, no applet named on the line | #307 audit G-B-15: rc 1; left: .collect.p7dead  |
| 248 | `y/CF` | `flock` (its consequence: rc 75 or a held lock) | gpt G2-D-01 / claude G2-D-08: the walk's gb jobs were '' (rc 75) -- expected h.gb and l.gb; a head's partial or nested GameId made the wrong |
| 249 | `y/CF` | `flock` (its consequence: rc 75 or a held lock) | gpt G2-D-02 / S-24: rc 75; stamp:  -- a failed measurement replaced by the cache count |
| 250 | `y/CF` | `flock` (its consequence: rc 75 or a held lock) | gpt G2-D-02 / S-24: rc 75; stamp: ; log:  |
| 251 | `y/CF` | `flock` (its consequence: rc 75 or a held lock) | gpt G2-D-02 / S-24: rc 75; stamp:  |
| 252 | `y/CF` | `flock` (its consequence: rc 75 or a held lock) | gpt G2-D-02 / S-24: rc 75; stamp:  |
| 253 | `y/CF` | `flock` (its consequence: rc 75 or a held lock) | gpt G2-D-02 / S-24: rc 75; stamp:  |
| 254 | `y/CF` | `flock` (its consequence: rc 75 or a held lock) | gpt G2-D-03: top-up rc 75; the writer never ran: the removal was not reached; marker: '1792888830 2760104 16439' (listed for '1792888830 276 |
| 255 | `y/CF` | busybox 1.37.0, no applet named on the line | gpt G2-D-03: 2026-10-25 00:40:35 index ran offline: the hash library did not come (index-pending); the library is listed once at the link's  |
| 256 | `y/CF` | `flock` (named: *applet not found*) | PL-002: cloud_backup: ran it: no; rc 75; out: flock: applet not found/flock: applet not found/flock: applet not found/Skipped: another cloud |
| 257 | `y/CF` | `flock` (named: *applet not found*) | PL-002: cloud_restore: ran it: no; rc 75; out: flock: applet not found/flock: applet not found/flock: applet not found/Skipped: another clou |
| 258 | `y/CF` | `flock` (named: *applet not found*) | PL-015: cloud_backup: rc 75; out: flock: applet not found/flock: applet not found/flock: applet not found/Skipped: another cloud sync is alr |
| 259 | `y/CF` | `flock` (named: *applet not found*) | PL-015: cloud_restore: rc 75; out: flock: applet not found/flock: applet not found/flock: applet not found/Skipped: another cloud sync is al |
| 260 | `y/CF` | `flock` (its consequence: rc 75 or a held lock) | PL-015: rc 75; log:  |
| 261 | `y/CF` | `flock` (its consequence: rc 75 or a held lock) | PL-015: rc 75; the copy's bound:  -- the escaped quote read as the value's end and the shipped bound stood in |
| 262 | `y/CF` | `flock` (named: *applet not found*) | G2-A-03 (gpt): rc 75; in the cloud: ; out: flock: applet not found/flock: applet not found/flock: applet not found/Skipped: another cloud sy |
| 263 | `y/CF` | `flock` (named: *applet not found*) | PL-004: cloud_backup, cp fails: conf intact; cleanup ran: no; left: ; rc 75; out: flock: applet not found/flock: applet not found/flock: app |
| 264 | `y/CF` | `flock` (named: *applet not found*) | PL-004: cloud_backup, cp says it worked: conf intact; cleanup ran: no; left: ; rc 75; out: flock: applet not found/flock: applet not found/f |
| 265 | `y/CF` | `flock` (named: *applet not found*) | PL-004: cloud_restore, cp fails: conf intact; cleanup ran: no; left: ; rc 75; out: flock: applet not found/flock: applet not found/flock: ap |
| 266 | `y/CF` | `flock` (named: *applet not found*) | PL-004: cloud_restore, cp says it worked: conf intact; cleanup ran: no; left: ; rc 75; out: flock: applet not found/flock: applet not found/ |
| 267 | `y/CF` | `flock` (named: *applet not found*) | G2-A-04 (gpt): plan written: yes; B.gb kept; rc 75; out: flock: applet not found/flock: applet not found/flock: applet not found/Skipped: an |
| 268 | `y/CF` | `flock` (named: *applet not found*) | G2-A-04 (gpt): B.gb kept; plan left; rc 75; out: flock: applet not found/flock: applet not found/flock: applet not found/Skipped: another cl |
| 269 | `y/CF` | `flock` (its consequence: rc 75 or a held lock) | G2-A-06 (claude): 16 stat calls with the stage small, 16 with 301 more seals, rc 1; the most frequent:  6 -c %s %Y /storage/roms/gb/Game.srm |
| 270 | `y/CF` | busybox 1.37.0, no applet named on the line | G2-A-06 (claude): old unclaimed KEPT; fresh kept; claimed none MISSING |
| 271 | `y/CF` | busybox 1.37.0, no applet named on the line | PL-034: read-only saves folder: rc 1; entries: ; out:  |
| 272 | `y/CF` | `flock` (its consequence: rc 75 or a held lock) | PL-034: past the bound: rc 1 after 10s; manifest none; failures: 1792888930 lock-busy gb:Game |
| 273 | `y/CF` | `flock` (its consequence: rc 75 or a held lock) | PL-034: within the bound: rc 1 after 10s; manifest none; failures: 1792888941 lock-busy gb:Game |
| 274 | `z` | busybox 1.37.0, no applet named on the line | PL-003: rc 1; the conf's command ran: no; mybk: 0 archive(s) -- backuptool sourced the file |
| 275 | `z` | busybox 1.37.0, no applet named on the line | PL-003: rc 1; ran: no; standard folder: 0; mybk: none; log: 1 |
| 276 | `z` | busybox 1.37.0, no applet named on the line | PL-003: rc 1; first: 0; second: 0 -- the source took the last |
| 277 | `z` | busybox 1.37.0, no applet named on the line | PL-003: single-quoted rc 1, 0 archive(s); bare rc 1, 0 |
| 278 | `z` | `flock` (named: *applet not found*) | PL-006 (KEEP's mktemp): rc 1; f1='LIVE'; new.cfg absent; why 'A SETTINGS BACKUP OR RESTORE IS ALREADY RUNNING'; screen: flock: applet not fo |
| 279 | `z` | `flock` (named: *applet not found*) | PL-006 (KEEP's appends): rc 1; f1='LIVE'; new.cfg absent; why 'A SETTINGS BACKUP OR RESTORE IS ALREADY RUNNING'; screen: flock: applet not f |
| 280 | `z` | `flock` (named: *applet not found*) | PL-006 (NEWLIST): rc 1; f1='LIVE'; new.cfg absent; why 'A SETTINGS BACKUP OR RESTORE IS ALREADY RUNNING'; screen: flock: applet not found/[ |
| 281 | `z` | `flock` (named: *applet not found*) | PL-006 (the final list): rc 1; f1='LIVE'; new.cfg absent; why 'A SETTINGS BACKUP OR RESTORE IS ALREADY RUNNING'; screen: flock: applet not f |
| 282 | `z` | `flock` (named: *applet not found*) | PL-006 (MEMBERS): rc 1; f1='LIVE'; new.cfg absent; why 'A SETTINGS BACKUP OR RESTORE IS ALREADY RUNNING'; screen: flock: applet not found/[ |
| 283 | `z` | `flock` (named: *applet not found*) | PL-006 (empty selection): rc 1; f1=''; screen: flock: applet not found/[31mA SETTINGS BACKUP OR RESTORE IS ALREADY RUNNING. WAIT FOR IT TO  |
| 284 | `z` | busybox 1.37.0, no applet named on the line | PL-006 (held back): rc 1; archives 0; why 'A SETTINGS BACKUP OR RESTORE IS ALREADY RUNNING' |
| 285 | `z` | `flock` (named: *applet not found*) | PL-007 (tar): rc 1; mark's first line after the extraction ''; copy's f1 ''; f1 now 'LIVE'; screen: flock: applet not found/[31mA SETTINGS  |
| 286 | `z` | `flock` (named: *applet not found*) | PL-007 (zip): rc 1; mark's first line after the extraction ''; copy's f1 ''; f1 now 'LIVE'; screen: flock: applet not found/[31mA SETTINGS  |
| 287 | `z` | busybox 1.37.0, no applet named on the line | PL-007 (backup): rc 1; archive holds:  |
| 288 | `z` | busybox 1.37.0, no applet named on the line | PL-008: rc 1; why 'A SETTINGS BACKUP OR RESTORE IS ALREADY RUNNING'; archives: 0 -- the value class could not take the space after the quote |
| 289 | `z` | busybox 1.37.0, no applet named on the line | PL-008: rc 1; why 'A SETTINGS BACKUP OR RESTORE IS ALREADY RUNNING' |
| 290 | `z` | busybox 1.37.0, no applet named on the line | G2-B-02: the mark at extraction: '' |
| 291 | `z` | busybox 1.37.0, no applet named on the line | PL-017: rc 1; upstream-era: ARCHIVED_ROCKNIX_BACKUP-20-01-01_00_00_00.zip ; contents: ARCHIVE-A ; root: ARCHIVED_ROCKNIX_BACKUP-20-01-01_00_ |
| 292 | `z` | busybox 1.37.0, no applet named on the line | PL-022 (stored, damaged): rc 1; why 'A SETTINGS BACKUP OR RESTORE IS ALREADY RUNNING'; f1 'LIVE'; d.cfg absent -- the corrupted bytes were r |
| 293 | `z` | busybox 1.37.0, no applet named on the line | PL-022 (deflated, damaged): rc 1; why 'A SETTINGS BACKUP OR RESTORE IS ALREADY RUNNING'; f1 'LIVE' |
| 294 | `z` | busybox 1.37.0, no applet named on the line | PL-022 (healthy): rc 1; why 'A SETTINGS BACKUP OR RESTORE IS ALREADY RUNNING'; f1 'LIVE'; brackets '' |
| 295 | `z` | busybox 1.37.0, no applet named on the line | PL-028 (tar): rc 1; why 'A SETTINGS BACKUP OR RESTORE IS ALREADY RUNNING'; outside: ; f1 'LIVE'; copies: 0 |
| 296 | `z` | busybox 1.37.0, no applet named on the line | PL-028 (zip): rc 1; why 'A SETTINGS BACKUP OR RESTORE IS ALREADY RUNNING'; outside: ; f1 'LIVE'; copies: 0 |
| 297 | `z` | busybox 1.37.0, no applet named on the line | PL-028 (..): rc 1; why 'A SETTINGS BACKUP OR RESTORE IS ALREADY RUNNING'; outside: ; f1 'LIVE'; copies: 0 |
| 298 | `z/S315` | `flock` (its consequence: rc 75 or a held lock) | cloud_backup --yes --saves-only --recent: no copy command was issued (rc 75); the assertions below are vacuous |
| 299 | `z/S315` | `flock` (its consequence: rc 75 or a held lock) | cloud_backup --yes --saves-only --recent: no copy command was issued (rc 75); the assertions below are vacuous |
| 300 | `z/S315` | `flock` (its consequence: rc 75 or a held lock) | cloud_backup --yes --saves-only: no copy command was issued (rc 75); the assertions below are vacuous |
| 301 | `z/S315` | `flock` (its consequence: rc 75 or a held lock) | cloud_backup --yes --saves-only --update: no copy command was issued (rc 75); the assertions below are vacuous |
| 302 | `z/S315` | `flock` (its consequence: rc 75 or a held lock) | cloud_restore --yes --saves-only: no copy command was issued (rc 75); the assertions below are vacuous |
| 303 | `z/S315` | `flock` (its consequence: rc 75 or a held lock) | cloud_restore --yes --method=copy --update --saves-only --automatic: no copy command was issued (rc 75); the assertions below are vacuous |
| 304 | `z/S315` | `flock` (its consequence: rc 75 or a held lock) | cloud_backup --yes --saves-only: no copy command was issued (rc 75); the assertions below are vacuous |
| 305 | `z/S315` | `flock` (its consequence: rc 75 or a held lock) | cloud_backup --yes --saves-only --recent: no copy command was issued (rc 75); the assertions below are vacuous |
| 306 | `z/S315` | `flock` (its consequence: rc 75 or a held lock) | cloud_restore --yes --saves-only: no copy command was issued (rc 75); the assertions below are vacuous |
| 307 | `z/S315` | `flock` (its consequence: rc 75 or a held lock) | cloud_backup --yes --saves-only: no copy command was issued (rc 75); the assertions below are vacuous |
| 308 | `z/S315` | `flock` (its consequence: rc 75 or a held lock) | cloud_backup --yes --saves-only --recent: no copy command was issued (rc 75); the assertions below are vacuous |
| 309 | `z/S315` | `flock` (its consequence: rc 75 or a held lock) | cloud_backup --yes --saves-only: no copy command was issued (rc 75); the assertions below are vacuous |
| 310 | `ad` | `flock` (named: *applet not found*) | rc 75; /GAMES in the cloud: no; out: flock: applet not found/flock: applet not found/flock: applet not found/Skipped: another cloud sync is  |
| 311 | `ad` | `flock` (named: *applet not found*) | rc 75; /GAMES: no; out: flock: applet not found/flock: applet not found/flock: applet not found/Skipped: another cloud sync is already runni |
| 312 | `ad` | `flock` (named: *applet not found*) | rc 75; A.srm missing; out: flock: applet not found/flock: applet not found/flock: applet not found/Skipped: another cloud sync is already ru |
| 313 | `ad` | `flock` (named: *applet not found*) | rc 75; out: flock: applet not found/flock: applet not found/flock: applet not found/Skipped: another cloud sync is already running. Try agai |
| 314 | `af` | `flock` (named: *applet not found*) | cloud_content_backup: rc 75, 2s; flock: applet not found/flock: applet not found/flock: applet not found/Skipped: another cloud sync is alre |
| 315 | `af` | busybox 1.37.0, no applet named on the line | cloud_content_backup: stamp/second-copy/cleanup mismatch |
| 316 | `af` | `flock` (named: *applet not found*) | cloud_content_backup: progressing run rc 75, 1s; flock: applet not found/flock: applet not found/flock: applet not found/Skipped: another cl |
| 317 | `af` | `flock` (named: *applet not found*) | cloud_content_restore: rc 75, 1s; flock: applet not found/flock: applet not found/flock: applet not found/Skipped: another cloud sync is alr |
| 318 | `af` | busybox 1.37.0, no applet named on the line | cloud_content_restore: stamp/second-copy/cleanup mismatch |
| 319 | `af` | `flock` (named: *applet not found*) | cloud_content_restore: progressing run rc 75, 1s; flock: applet not found/flock: applet not found/flock: applet not found/Skipped: another c |

## Proofs

| Proof | What it shows | Proved |
| --- | --- | --- |
| P1 | the image's busybox run is the tree's baseline: 1,313 / 0 / 0, rc 0, from the worktree | proved: tool-run |
| P2 | the coordinator's ten image-run FAILs are the fixture's git-history dependency (an export without `.git`), not the tree's: the same bytes from the worktree pass all ten | proved: tool-run |
| P3 | all 319 host-busybox flips are the busybox's: `bbhost` 319 with the image's rclone, `rchost` 0 with the host's | proved: tool-run |
| P4 | none of the twelve `--old` recipes reaches a verdict: two refs dead, ten stopped at `s` or `x` | proved: tool-run |
| P5 | `70b6c70ca7`'s promised `012` FAILs do not fire: its `t` stops at the patches, with 0 lines naming `012` | proved: tool-run |

## The streams' positives

Each stream's case, run against the unfixed file (the stage-D export, a `git clone --shared` detached at `2eface0727`, history present) or a copy of the file with its other sections cut, and against the fixed one. Fallback runs have `QA_SYSTEM_ROOT` unset on purpose. Judging runs set it on the `069fc2704421` M7 root's `image/system`. Every run starts with SIGINT and SIGPIPE at their defaults (`signals: SigIgn=0000000001000004 SIGINT ignored=0 SIGPIPE ignored=0`) and `TMPDIR` under `/workspace/tmp/m6-t15/`. The outputs are in `/workspace/tmp/m6-t15/s1/`.

### S1, #1018: no silent host tools

| Case | File | Result | Proved |
| --- | --- | --- | --- |
| no root, no flag (the positive) | unfixed, export | rc 1 in 675 s, 994 PASS / 319 FAIL. The verdict is `319 CHECK(S) FAILED, 0 SKIPPED` and names no tool source. The banner reads `a copy of /usr/bin/busybox` (the host's 1.37.0), and line 270 still says `the sed in use (the image's busybox)` | proved: tool-run |
| no root, no flag | fixed, worktree | rc 2 in 26 ms: `CANNOT -- no candidate image's busybox: QA_SYSTEM_ROOT is unset and no build root's image/system/usr/bin/busybox is beside ... (found: /usr/bin/busybox). Set QA_SYSTEM_ROOT=<a build root>/image/system, or run with --host-diagnostic ... (marked, not device evidence: exit 1 on a failing case, else 3).` | proved: tool-run |
| no root, `--host-diagnostic`, full suite | fixed, worktree | rc 1 in 676 s (D-QA-063's 1 branch), 994 PASS / 319 FAIL. All 1,313 result lines are marked `HOST:` and none is unmarked. The verdict: `tools: busybox /usr/bin/busybox -- BusyBox v1.37.0 (Ubuntu 1:1.37.0-7ubuntu1) multi-call binary.; source: host`, then `NOT DEVICE EVIDENCE -- --host-diagnostic: 319 CHECK(S) FAILED, 0 SKIPPED under the host's tools, not the candidate's` | proved: tool-run |
| no root, `--host-diagnostic`, no failing case | fixed, cut to the harness, `a` and the verdict (`lgst-cut3`, `LAST_GOOD_SOURCE_ROOT` = the worktree) | rc 3 (D-QA-063's 3 branch), 13 PASS / 0 FAIL, all marked. `NOT DEVICE EVIDENCE -- --host-diagnostic: 0 CHECK(S) FAILED, 0 SKIPPED ...`. It never exits 0 | proved: tool-run |
| no root, `--host-diagnostic`, one injected failing case | fixed, cut as above plus `false; check $? ...` (`lgst-cut1`) | rc 1, 13 PASS / 1 FAIL, `FAIL  HOST: S1 injected: the deliberately failing case failed, as built`. The verdict is still marked: `NOT DEVICE EVIDENCE -- --host-diagnostic: 1 CHECK(S) FAILED, 0 SKIPPED ...` | proved: tool-run |
| the M7 root (the judging run) | fixed, worktree | rc 0 in 517 s, 1,313 PASS / 0 FAIL / 0 SKIP, 0 lines marked `HOST:`. `tools: busybox .../m7-signin-build-20261022-07/.../image/system/usr/bin/busybox -- BusyBox v1.36.1 (2026-10-05 03:37:19 UTC) multi-call binary.; source: root, BUILD_ID 069fc270442134fe771258418adf4e666e0473fb`, then `PASSED`. The two G-B-15 probes now name the source: `(root, BUILD_ID 069fc2704421...)` | proved: tool-run |

**A correction to the stream brief:** its *"the unfixed file ... prints `329 CHECK(S) FAILED`"* is 319. The other ten are the history dependency (P2, #1021), which a clone with `.git` does not trigger. Ten fewer failures, same cause.

### S1, #1020: stream A's rclone is the root's, at the recipe's version

The coordinator's 03:11 ruling (a): a root whose rclone is missing, or not the recipe's `PKG_VERSION` (read through `src_of`, so `--old` reads the ref's), is CANNOT before section `a`, exit 2. A root whose rclone is not the tree's was built from another tree, so its busybox is not this tree's either. The rclone is now taken from the busybox's own system root, not found by a second search.

| Case | File | Result | Proved |
| --- | --- | --- | --- |
| the `rchost` root: the M7 busybox with the host's rclone 1.60.1-DEV (the positive) | unfixed (`3037ce6b8c`, a `git clone --shared` detached there, not shallow) | rc 0 in 516 s, **`PASSED`, 1,313 / 0 / 0**. Stream A's banner says `rclone v1.60.1-DEV -- a copy of .../rchost/image/system/usr/bin/rclone`, while the verdict claims `source: root, BUILD_ID 069fc2704421...`: the provenance line #1018 added cannot see the mismatch | proved: tool-run |
| the `rchost` root | fixed | rc 2 in 47 ms: `CANNOT -- the root's rclone is v1.60.1-DEV (.../rchost/image/system/usr/bin/rclone) and the recipe in <worktree> says v1.75.2: a root whose rclone is not the tree's was built from another tree, so its busybox is not this tree's either. Rebuild the root from this tree, or run BASE_REF=<the ref it was built from> --old.` | proved: tool-run |
| the M7 root, `BASE_REF=417dcd8610 --old` | fixed | rc 2 in 57 ms: `... the root's rclone is v1.75.2 (...) and the recipe at 417dcd8610 says v1.75.1 ...`. The ref's recipe is read through `src_of`, as the ruling says | proved: tool-run |
| no root, `--host-diagnostic` | fixed, cut to the harness, `a` and the verdict | rc 3 in 428 ms. The verdict's second provenance line: `tools: rclone /usr/bin/rclone -- v1.60.1-DEV; the recipe says v1.75.2`, then `NOT DEVICE EVIDENCE` | proved: tool-run |
| the M7 root | fixed, cut as above | rc 0 in 434 ms: `tools: rclone .../m7-signin-build-20261022-07/.../usr/bin/rclone -- v1.75.2; the recipe says v1.75.2` | proved: tool-run |
| the M7 root (the judging run) | fixed, full suite | rc 0 in 522 s, **1,313 / 0 / 0**. Stream A: `rclone v1.75.2 -- a copy of .../m7-signin-build-20261022-07/.../usr/bin/rclone`. The verdict: `tools: busybox ... source: root, BUILD_ID 069fc270442134fe771258418adf4e666e0473fb`, `tools: rclone ... -- v1.75.2; the recipe says v1.75.2`, then `PASSED` | proved: tool-run |

**A consequence for `--old`:** the recipe pins rclone 1.75.1 at every ref the suite's positives name (`417dcd8610`, `f3d19dc8fb`, `320d2b2bea`, `286759eb6d`) and 1.75.2 at the stage-D tip. The only GENERIC_X64 roots on this host (`m7-signin-build-20261022-07`, `m7-pixelelated-replacement20`) carry 1.75.2. The sources cache's `rclone/` directory is empty, because the recipe removes the zip after unpacking it (`package.mk:58`). So, under the ruling, no `--old` run reaches a verdict on this host until a root of a 1.75.1 ref exists. This was put to the coordinator with the #1020 checkpoint, since S2's #1022 and #1023 prove themselves with `--old` runs.

### S1, #1029 and #1038: section `b` binds the busybox; PL-022 needs verified provenance

**#1029.** Section `b`'s sandbox now binds the run's busybox copy at its own path and `/nbin` wrappers for the 28 applets backuptool calls that the image links to busybox (`tar find sed awk cp mv rm mkdir ls cat date head tail tr cut wc stat chmod basename dirname readlink sync flock mktemp touch unzip cmp install`, read from the M7 root's `usr/bin` links). The profile's PATH is `/shim:/nbin:/usr/bin:/bin`, and the two tar shims exec `/nbin/tar`. `grep`, `gzip`, `sort` and `zip` are real binaries on the image, so the host's stand in for them, as in stream A. A new probe inside the same sandbox checks that each applet resolves to `/nbin/<applet>` and that its `--help` first line is the copy's banner.

**#1038.** The PL-022 block runs only when the busybox's source is a root or a build (#1018's `BB_KIND`). On the host's busybox it is a counted, named SKIP. The measurement line names the source instead of saying "the image's".

| Case | File | Result | Proved |
| --- | --- | --- | --- |
| #1029, the probe with `b`'s sandbox as it was: no `/nbin` and no busybox bound, PATH `/shim:/usr/bin:/bin` (the positive) | fixed, cut to the harness, `a`, `b` and the verdict, with those three lines reverted (`lgst-ab-unbound`), the M7 root | rc 1: `FAIL  #1029: 0 of 28 applets in backuptool's sandbox are the run's busybox: tar=/usr/bin/tar find=/usr/bin/find sed=/usr/bin/sed awk=/usr/bin/awk cp=/usr/bin/cp mv=/usr/bin/mv`. `b`'s other 14 checks PASS on the host's tools, which is the defect | proved: tool-run |
| #1029, the same cut copy with the binding (`lgst-ab`) | fixed, M7 root | rc 0: `PASS  #1029: backuptool's sandbox reaches the run's busybox for all 28 applets it calls (tar --help: BusyBox v1.36.1 (2026-10-05 03:37:19 UTC) multi-call binary.)`, and `b`'s 14 others PASS under the image's applets | proved: tool-run |
| #1038 under the host's busybox (the positive) | unfixed, full suite, no root (`unfixed-fallback.out:1379`) | `PASS  audit of the fix round PL-022 (the measurement, BS-3): the image's busybox unzip passes a damaged STORED member (-t rc 0, -p rc 0) ...`: the host's 1.37.0, measured and called the image's | proved: tool-run |
| #1038 and #1029, `--host-diagnostic`, full suite | fixed, no root | rc 1 in 674 s, 985 PASS / 325 FAIL / 1 SKIP, all marked `HOST:`. `SKIP  HOST: audit of the fix round PL-022: the busybox here is the host's (--host-diagnostic), and the case is the candidate's unzip (#1038)`. `FAIL  HOST: #1029: 27 of 28 applets ... flock=/nbin/flock`: the host's busybox has no `flock`. The difference from #1018's host run, line by line: `b`'s 8 backuptool checks now FAIL with `A SETTINGS BACKUP OR RESTORE IS ALREADY RUNNING` (backuptool's lock, no `flock` applet), plus the probe; PL-022's 4 checks (1 PASS, 3 FAIL) become the 1 SKIP; the rest is timestamps and timings. 319 + 9 − 3 = 325; 994 − 8 − 1 = 985 | proved: tool-run |
| #1029 and #1038, the M7 root (the judging run) | fixed, full suite | rc 0 in 517 s, **1,314 / 0 / 0** (the baseline plus the probe). The probe PASSes with the banner above; `PASS  ... PL-022 (the measurement, BS-3): the candidate's busybox unzip (root, BUILD_ID 069fc270442134fe771258418adf4e666e0473fb) passes ...`; `PASSED` | proved: tool-run |

### S1, #1019: `ag` and `ah` carry the busybox's origin; a child's 2 and 3 reach the verdict

The coordinator's 03:58 ruling (a): a child suite's CANNOT (2) or UNVERIFIED (3) gives the suite 3 when nothing failed, counted and named in the verdict; a FAIL anywhere is 1; exit 2 stays the suite's own refusal to start. `ag` and `ah` now pass `--busybox-from "${BB_ID}"` when a root or build supplied the busybox, and `--unverified-busybox` when the host did. Their results go through `check_child`: 0 PASS, 2 CANNOT, 3 UNVERIFIED, otherwise FAIL. `ag`'s tool moved from `${ROOT}/tools/` to `${HARNESS_ROOT}/tools/`, as `ah`'s already was: the writer tests are the harness's instruments, and under `--old` the ref's scripts are judged by the current writer tests (approved at 03:58, and said beside the move).

The positives run in two `git clone --shared` copies detached at `4e5b6c6103` (`/workspace/tmp/m6-t15/s1/t14stage`, `t14double`). Each holds a cut copy of the file: the harness, `ag`, `ah` and the verdict. `t14stage` carries T14's two tools from `7c1d729b57`. `t14double` carries doubles: `settings-modes-test` prints a CANNOT line and exits 2, and `melonds-upgrade-test` prints one line and exits 3.

| Case | File | Result | Proved |
| --- | --- | --- | --- |
| T14's tools, the M7 root (the positive) | unfixed (`4e5b6c6103`), cut | rc 1: `settings-modes-test: CANNOT -- .../busybox is not under a build root's image/system/; name its origin with --busybox-from <BUILD_ID|image>, or pass --unverified-busybox (exit 3)`, then `FAIL  #421: settings mode regression (details above)`; the same for melonDS; `2 CHECK(S) FAILED` | proved: tool-run |
| the doubles, the M7 root (the positive) | unfixed, cut | rc 1: the child's exit 2 and exit 3 both read `FAIL ... regression (details above)`, `2 CHECK(S) FAILED` | proved: tool-run |
| T14's tools, the M7 root | fixed, cut | **rc 0**: each child says `busybox: declared from 069fc270442134fe771258418adf4e666e0473fb`, then `PASS  #421: private modes and refused publications`, `PASS  #526: preserved configuration and atomic hotkey additions`, `PASSED` | proved: tool-run |
| the doubles, the M7 root | fixed, cut | **rc 3**: `CANNOT  settings-modes-test could not run (exit 2, its reason above), so not: #421: ...`, `UNVERIFIED  melonds-upgrade-test ran and could not qualify (exit 3), so not evidence: #526: ...`, `1 CHILD SUITE(S) COULD NOT RUN, 1 UNVERIFIED -- settings-modes-test could not run; melonds-upgrade-test unverified (#1019)` | proved: tool-run |
| T14's tools, `--host-diagnostic` | fixed, cut | rc 3: both children print `busybox: host busybox, not the candidate's`; `UNVERIFIED  HOST: ...` twice; `NOT DEVICE EVIDENCE -- ...` | proved: tool-run |
| this branch's own tools (before T14 merges), the M7 root: the end of S1 | fixed, full suite | **rc 3** in 518 s, 1,312 PASS / 0 FAIL / 0 SKIP / **2 CANNOT**: `settings-modes-test: error: unrecognized arguments: --busybox-from 069fc2704421...`, then `CANNOT  settings-modes-test could not run ...`; the same for melonDS; `2 CHILD SUITE(S) COULD NOT RUN, 0 UNVERIFIED -- ...`. Both provenance lines are as before. With T14 merged, these two are the cut copy's two PASSes above, and the run is 1,314 / 0 / 0 | proved: tool-run |

`grep -n -E 'busybox-from|unverified-busybox' tools/last-good-scripts-test` prints both call sites (`:14348`, `:14355` at this commit), each with its flag comment.

### S6, #1030: `ag` runs the harness's settings-modes-test (the fix landed with #1019)

The fix, `${ROOT}/tools/settings-modes-test` to `${HARNESS_ROOT}/tools/settings-modes-test`, is in `3da816ce24` (#1019), approved by the coordinator at 03:58. It was made there as part of `ag`'s call before the lane saw that #1030 is a separate bug. No separate code commit follows.

| Case | File | Result | Proved |
| --- | --- | --- | --- |
| `LAST_GOOD_SOURCE_ROOT` naming a checkout without `tools/settings-modes-test` (a clone at `4e5b6c6103` with that one file removed); the harness in `t14stage` with T14's tools; the M7 root (the positive) | unfixed (`4e5b6c6103`), cut to the harness, `ag`, `ah` and the verdict | rc 1: `.../nosmt/tools/settings-modes-test: No such file or directory`, then `FAIL  #421: settings mode regression (details above)`. The other FAIL is `ah`'s #1019 refusal | proved: tool-run |
| the same | fixed (`3da816ce24`), cut | rc 0: `PASS  #421: private modes and refused publications`, `PASSED` | proved: tool-run |

### S2, #1023: `--old` reaches a verdict -- CANNOT, a promised FAIL, or NOT APPLICABLE by name

The shape follows the seat's three distinctions (the 02:36 ruling) and the 03:34 per-tool ruling.
- **An invalid ref is CANNOT at once.**
- **A script absent at the ref** works in three ways:
  - in a section the header promises for that ref, it is that promise firing: one FAIL;
  - in another section, the rest of the section is NOT APPLICABLE by name, its checks printing `N/A`, counted, never PASS;
  - before any section, an input the harness itself needs is CANNOT.
- **The header's recipes are now data** (`old_promises`). The verdict says which promises fired and which did not.
- **Each tool borrowed from the root** (rclone, busybox) is compared with the ref's recipe. A mismatch is named and its sections are unverified, rather than the 03:11 CANNOT, which stands outside `--old`.
- **The exit** follows D-QA-063.
- **The 34 section banners** are now `section <letter> "<text>"`, with the same output, which is what tracks the section.

| Case | File | Result | Proved |
| --- | --- | --- | --- |
| `BASE_REF=0f7785e6ed --old`, a dead ref (the positive) | unfixed (stage A, `.qa-scratch/t15/old-0f7785e6ed.out`) | exit 2 mid-run, at the first read: `fatal: invalid object name '0f7785e6ed'.` / `cannot read projects/ROCKNIX/packages/rocknix/sources/scripts/chksysconfig at 0f7785e6ed` | proved: tool-run |
| `BASE_REF=0123456789 --old` and `BASE_REF=0f7785e6ed --old` | fixed | exit 2 in 11 ms and 9 ms, before any fixture: `CANNOT -- BASE_REF 0123456789 is not a commit in <worktree>` (the same for the dead ref) | proved: tool-run |
| `BASE_REF=1d1503180d --old`, the M7 root (the positive) | unfixed (stage A, `old-1d1503180d.out`) | exit 2 at `s`: `fatal: path '.../rocknix-evidence' exists on disk, but not in '1d1503180d'` / `cannot read ... at 1d1503180d`. No verdict, and sections `s` to `ah` never ran | proved: tool-run |
| `BASE_REF=1d1503180d --old`, the M7 root | fixed | **exit 1** in 1,219 s, a verdict: 126 PASS / 354 FAIL / 659 `N/A` lines (654 checks plus 5 *from here* lines) / 26 SKIP / 2 CANNOT (`ag`, `ah`: this branch's writer tests, #1019). `--old 1d1503180d: promised: a b c d e f j k l m; fired: a b c d e f j k l m; did not fire: none`. `NOT APPLICABLE at 1d1503180d: 654 check(s) in section(s) s x y z ab -- a script the ref predates; not run, never PASS`. `UNVERIFIED under --old: rclone v1.75.2 from the root; the ref's recipe says v1.75.0 -- the old scripts under the candidate's rclone; stream A's 0 check(s)` (stream A's checks are all inside `y`'s N/A). Each N/A section is named with its script: `s` rocknix-evidence, `x` rocknix-corekeep, `y` rocknix-evidence, `z` cloud_log_scrub, `ab` cloud_scan. The suite's existing absence checks still fire as before: `p` and `t` FAIL with `raofflineproxy-ctl is absent at 1d1503180d: ...` | proved: tool-run |

The run is slower than an ordinary one (1,219 s against 517 s). The sections marked N/A keep executing against empty placeholder scripts, and their stderr carries the noise of that (`/logs/exec.log: No such file or directory`, the missing RetroArch patches). Their checks print `N/A`, never PASS or FAIL.

`34aca64afd` (#1023's second case, `p`'s promised absence) and the twelve-recipe table run after S2's other commits. The table is S2's last step.

**A departure, and its fix (`e430d61cfa`).** `--old 717bc04449` at `5d1f67ca0b` ended after 328 s with rc 1 and no verdict: `line 8176: D19_IMAGES[0]: unbound variable`. N/A section `x`'s leftover code ran against an empty placeholder, as `5a155ed7fc` designed, and an unbound expansion under `set -u` ended the whole run, silently. Two changes:
- `old_absent` lifts `set -u` for the rest of an N/A section, and `section()` and the verdict restore it;
- an EXIT trap turns a run that ends before its verdict, other than by an exit 2 the harness chose, into `ABORTED in section <x> (rc N) -- no verdict`, exit 2.

| Case | Script | Result | Proved |
| --- | --- | --- | --- |
| an unbound expansion before the verdict (the positive) | `5d1f67ca0b`, `--old 717bc04449` | rc 1 in 328 s, no verdict line; the last line is the shell's `D19_IMAGES[0]: unbound variable` | proved: tool-run |
| the same shape, constructed: the fixed file's trap block, `set -u`, `SECTION=x`, then `echo "${A[0]}"` on an empty array | the trap of `e430d61cfa` | `line 7: A[0]: unbound variable`, then `last-good-scripts-test: ABORTED in section x (rc 1) -- no verdict; the harness failed, not a script (its message above)`, **rc 2** | proved: tool-run |
| a CANNOT the harness chose, constructed: `echo "CANNOT -- something" >&2; exit 2` before the verdict | the same trap | `CANNOT -- something`, rc 2, and no ABORTED line | proved: tool-run |

The first five of the twelve stand at `5d1f67ca0b`, where each reached its verdict. The rest run at `e430d61cfa` (the coordinator's 08:05 (a)).

### S2, #1021: a history read fails closed at the read (on the donor)

The constructed input is a shallow clone, the coordinator's 04:12 ruling: a clone with the condition the bug is about, not a figure. In each, `417dcd8610` is unreachable (`git cat-file -e 417dcd8610^{commit}`: *Not a valid object name*). Unfixed: `bea0374f3b`, `git clone --depth 2` so that its parent commit could be checked out. Fixed: `70af8e3771`, `--depth 1`. Both run with no `--old`, on the donor root.

| Case | File | Result | Proved |
| --- | --- | --- | --- |
| a shallow clone (the positive) | unfixed | rc 1 in 518 s, 1,302 PASS / **10 FAIL** / 0 SKIP / 2 CANNOT. All ten are vacuity detectors downstream of the silent read: `the earlier builds' pass wrote nothing -- the fixture proves nothing`, `still on /storage after a boot:`, `the take-back boot's journal: ''`, `the repair changed: 'nothing'`, `a second run changed the repaired copy`, `the old quirks' next boot left the owner's edit or the unmask: ...`, `the downgrade wrote 0 file(s), -- the fixture proves nothing` (twice), and `G2-F1-01: after a downgrade to the prev/first old quirks and back ...` (twice). Census `cc1plus=0 qemu=0` | proved: tool-run |
| a shallow clone | fixed | **rc 2 in 127 s**, after 397 PASS: `last-good-scripts-test: CANNOT -- 417dcd8610 is not in this checkout's history (an export or a shallow clone?), so projects/ROCKNIX/packages/hardware/quirks/platforms/GENERIC_X64 cannot be read at it`. Load 24.5 at its end, from M7's build beside it | proved: tool-run |

The same run from a full clone passes `F1.`, `F1r.` and `C.` as before: root-tip at `a286e5b49f`, 1,312 / 0 / 0 / 2 CANNOT, above.

### S3, #1026: rc non-zero and nothing written requires the script to have run

The constructed input is a sandbox that cannot start: a `bwrap` first on PATH that prints `bwrap: a constructed sandbox that cannot start (#1026)` and exits 1 (`/workspace/tmp/m6-t15/s3/fakebwrap/bwrap`). Each side is a full suite on the donor, from a clone. Unfixed is `11952dfcf3`, the commit before `812d09e3af`; fixed is `5d1f67ca0b`. The comparison (`witness-compare.py` in the lane's scratch) takes each witnessed check's ok-text from the fixed file, up to its first expansion, and looks for it among each run's PASS lines.

| Case | File | Result | Proved |
| --- | --- | --- | --- |
| no sandbox can start (the positive) | unfixed | rc 1 in 177 s, 581 PASS / 678 FAIL / 1 SKIP / 2 CANNOT; the fake refused 214 times. **23 of the 64 witnessed checks matched by their text PASS**, among them `b`'s founding cases: `PASS  the run died (rc 1)`, `PASS  a restore whose extraction fails exits non-zero` | proved: tool-run |
| no sandbox can start | fixed (`5d1f67ca0b`: 63 checks witnessed, plus `b`'s two with their guarded steps) | rc 1 in 217 s, 544 PASS / 715 FAIL / 3 SKIP / 2 CANNOT. **0 of the 64 PASS.** `FAIL  the run exited 0 through a tar that killed the group, or never reached it (started: no, tar reached: no)`; `FAIL  rc 1 from a failed extraction, or the extraction was never reached (started: no, extraction reached: no)` | proved: tool-run |
| sandboxes that start (the judging run) | fixed, root-final | rc 3, 1,315 / 0 / 0 / 2 CANNOT: every witnessed check passes on the real scripts | proved: tool-run |

The other 41 witnessed checks failed even on the unfixed file under the broken sandbox, because of another conjunct, such as a missing why line. `7987e9cc9f` gave the witness to the remaining eight checks under `nb`, `ev`, `c2`, `p7w`, `p7ev` and `cf3`: 71 of 71. Their positive is the fake-`bwrap` run at the final tip, in the close-out.

### S5, #1028: sa_run clears its environment and unshares the network

The probe is a cut copy: the harness, stream A's setup through `sa_tail`, then a script run through `sa_run` that prints what reached it, with the caller exporting `RCLONE_CONFIG=/probe/rclone.conf`, `RCLONE_CONFIG_QA_TYPE=webdav`, `BASH_ENV=/dev/null` and a function (`export -f lgst_probe_fn`). The interfaces are read from the sandbox's `/proc/net/dev`. Unfixed is `b729628ad6`, fixed `5d1f67ca0b`; both on the donor root, and both ran in about a second.

| Case | File | Result | Proved |
| --- | --- | --- | --- |
| the caller's environment and network (the positive) | unfixed | rc 1: `probe saw: RCLONE_CONFIG=/probe/rclone.conf;RCLONE_CONFIG_QA_TYPE=webdav;BASH_ENV=/dev/null;FN=function;IF=lo <the host's interfaces: its ethernet and Wi-Fi, a VPN and the container bridges>`, then `FAIL  #1028: the sandbox received: ...` | proved: tool-run |
| the same | fixed | rc 0: `probe saw: RCLONE_CONFIG=unset;RCLONE_CONFIG_QA_TYPE=unset;BASH_ENV=unset;FN=unset;IF=lo ;`, then `PASS  #1028: the sandbox received none of the caller's RCLONE_*, BASH_ENV or exported functions, and has loopback only` | proved: tool-run |

**The exceptions:** none. The 179 call sites were searched for a variable passed in front of the call (only `SA_CWD`, which `sa_run` reads itself), and the harness for an export reaching them (none). `SA2_EXTRA`'s `--setenv CLOUD_CAPTURE_EXIT_BOUND` comes after `--clearenv`. root-final at `5d1f67ca0b` (rc 3, 1,315 / 0 / 0 / 2 CANNOT) shows that no case needed the host network or an inherited variable.

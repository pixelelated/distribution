# Brief: M6.P2 T17, cloud sync: setup, sign-in, connections, content and settings backups (#664)

**Version 2, 2026-10-26, the coordinator's** (D-WORKFLOW-189; version 1 the same hour, corrected by a stranger's proof -- eleven corrections, listed at the end). Written from a
read-only research digest (sixteen commands over the scratch clone at
`2174265e9c`, every figure with its command and population; the first
attempt died at an API limit before its first command and was rerun whole),
T16's brief (`cloud-sync-core.md`, version 2) and T13's audit as the models,
and the cloud area futro (`docs/futros/2026-10-25-m6-cloud-sync-and-saves.md`).
The stranger's proof of version 1 ran before dispatch (ten commands from the scratch clone); this version records what it found. The lens is **security**; the depth reason is **state preservation**: these
fourteen files hold every credential the product touches, the only content
action that deletes, and the archive a player's settings travel in.

## 1. Identity

- **Issue:** #664 `M6.P2 E1047/T17: cloud-sync-and-saves: cloud sync:
  setup, sign-in, connections, content and settings backups`, slice
  `cloud-setup-content` (`k: 17`) in `docs/reviews/slices.json`, seventeenth
  in `docs/reviews/order.md` (its § T17 paths line: *"14 paths, 11,180
  lines, 11,180 read, of which 11,180 fork-own; 0 patch and config lines;
  reach shipped 14"*; its `why`: *"handles credentials (`rclone.conf`,
  OAuth tokens, the sign-in window) and the only content action that
  deletes (`--match`, D-CLOUD-023)"*; kind read; lens security; depth
  Extended, *"security and state preservation (plan § 6c)"*). **Epic:**
  #1047 (the cloud area: T13 #660 accepted and closed out; T16 #663 at
  stage C with its guest window to re-grant; this slice last), whose futro
  carries T13's and T16's addenda and takes a T17 addendum written with
  this version. **Milestone:** M6. **Predecessors:** #346, #641, **T13
  #660** (`docs/reviews/briefs/cloud-harness.md`; its audit on
  `feature/m6-cloud-harness-660`: `04-analysis.md` § Q2 *The oracle
  verdict* -- 78 rows and `CONTRACT`, 25 both ends, 46 synthetic, 8 the
  device's own report -- and its bugs #1057-#1070, #1081, #1092, #1093,
  fixed at `3a653eaec4` -- on `origin/feature/m6-cloud-harness-660` after a fetch; a clone older than 2026-10-25 08:30 lacks it -- open until `next`; two touch this slice's files or tests: **#1081** `cloud-census` runs `cloud_device_id`, **#1061** the credential-shaped fixture literal in `tools/cloud-connections-test`; T15's **#1029**, `last-good-scripts-test`'s section b running `backuptool` with the host's tools, touches it too), **T16 #663** (`cloud-sync-core.md`: the twins, the
  stamps, the seam named from its side; its stage-B deltas -- the built
  `last-${name}` stamp name, the rule's rc sentences against the scripts'
  -- are T16's, not this slice's), **T1 #648** (`post-update` and
  `chksysconfig`, whose state `backuptool` archives), **T22 #669**
  (`os-system-services.md`: the Extended recipe and the guest cycle's
  conditions), **T4 #651** (#909: `rclone-cloud-sync.md` is under its drift
  bug; the scripts are the truth where they disagree), **T15 #662**
  (`tools/last-good-scripts-test`, which runs `backuptool` and every cloud
  script under the image's busybox on the host; its section b is #1029),
  **T10** (the pre-commit pattern that #1061 trips). **Beside it:** T29 in
  the T5 session (the quirks; no shared path), T16 in the T1 session when
  it resumes; **the host is M7's** under the coordinator's handoff of 2026-10-26 04:47 UTC on `/tmp/m7-m6-host-coordination-20261023.txt`: M7's native stage ran 04:48-04:50 and returned, and its guest window is queued behind the T16 guest's stop; M7 writes timestamped lines, not `== ` blocks, so the whole tail is read (D-WORKFLOW-190 for the lanes; the host file for the guests). The register rows this brief cites (D-WORKFLOW-190, 195, 209; D-QA-063) are on the coordinator's branch, merged into the lane's worktree at dispatch; `2174265e9c` alone lacks them and holds D-WORKFLOW-188 (§ 9).
- **The division of labour (D-WORKFLOW-189).** This lane executes. It does
  not re-cut the slice, change a criterion, write a brief, move the M6
  body, edit `slices.json`, `areas.json`, `order.md` or the plan, file a
  Backlog issue, post on #346, #585 or #909, or decide a question of scope:
  those are the coordinator's, reached through #664, one question at a
  time. What it does file: its own audit punch-list issue (stage D) and a
  `bug` issue for a defect it proves, with its trace and `Already written:`
  line (D-WORKFLOW-187). A fix lands only under a stream brief the
  coordinator writes at the stage-D pause. **Thirteen of the fourteen are
  the fork's own and `backuptool` is the fork's rewrite of upstream's
  68-line script** (§ 2): a defect anywhere here is the fork's to fix, and
  D-WORKFLOW-209's class decision reaches nothing in this slice. **M7's
  open work on these same scripts** (#1111, #1113, #1115, #1117 on its
  branch, not on `next`) is cited by issue number where a finding meets it
  and is never read from M7's worktrees; the read is `8ebaf8daad`'s bytes.
- **One worktree, one session.** Branch `feature/m6-cloud-setup-content-664`
  at `/workspace/repos/pixelelated/distribution.worktrees/m6-cloud-setup-content-664`,
  created by the coordinator, **stacked on `feature/m6-p1-survey-641` at
  `2174265e9c`** (`docs/reviews/{order.md,slices.json,inventory.json,status.md}`
  are there and on no other branch) with the coordinator's tip merged in
  (the briefs, the futros, the rules edited since) and the lane's pointer
  seeded; the two hashes are in the dispatch comment on #664. Until that
  comment exists the pointer is not seeded, the first command's `cat`
  fails, and nothing starts. The session is the one the dispatch comment
  names (the first idle lane session; its earlier worktrees stay idle
  beside this one, read with `git show` only: T13's audit is on its branch,
  `git show feature/m6-cloud-harness-660:docs/audits/2026_10_25-epic-m6-cloud-harness/<file>`;
  T16's on `feature/m6-cloud-sync-core-663`).
- **Depth: Extended** -- two seats, as T22's and T16's stage C: GPT-6
  Astra at `max` over a trimmed, scanned packet (D-WORKFLOW-195), a probe
  then one refutation; then Gemini 4 Argon at `high` over the same packet
  plus the lane's grades of Astra, a probe then one refutation;
  `review-plan.json` records depth `extended` and both reviewers with their
  served models; **exactly four keyed `tools/council/run invoke` calls**,
  every other `tools/council/run` call with `COUNCIL_ENV_FILE=/nonexistent`,
  `--help` included; the runtime from `npm install --offline`, no fetch.
  **The packet is scanned before it leaves** (D-WORKFLOW-195's three-way
  scan): these fourteen files carry the words the scanner looks for in
  comments and variable names (`cloud_oauth` has 22 `token` lines and 6 `secret` lines by a case-insensitive count, 1 whole-word, read here as counts only), so the manifest records every
  scan hit and its disposition, and a hit that is a value rather than a
  name stops the packet. Every seat item is re-read at its lines before it
  is graded (T22's practice).
- **Model and effort:** Opus 5.5 at high effort, written into `00` at
  stage A.
- **The first commands** (stage A, in the worktree):

```bash
cd /workspace/repos/pixelelated/distribution.worktrees/m6-cloud-setup-content-664
cat .github/sessions/saved-session-state-feature-m6-cloud-setup-content-664.md  # the pointer: the dispatch's two hashes
git status --short | wc -l                                                      # 0
git log --oneline -3; git merge-base --is-ancestor 8ebaf8daad HEAD && echo stacked
git diff --stat 8ebaf8daad HEAD -- packages projects | tail -1                  # empty: the read is of next's bytes
git diff --stat 8ebaf8daad HEAD -- tools | tail -1                              # P1's own 15 files under tools/ (#641, #646, #810), nothing else; the removal check is from the dispatch tip (§ 5)
git rev-parse --verify 651150fc88^{commit} >/dev/null && echo upstream-next-is-here   # read locally, never fetched
git show feature/m6-cloud-harness-660:docs/audits/2026_10_25-epic-m6-cloud-harness/04-analysis.md | grep -c '^| ' # T13's tables are reachable
tools/register-check >/dev/null && echo register-ok
tail -n 3 /tmp/m7-m6-host-coordination-20261023.txt | cut -c1-200              # who holds the host: no guest of this slice's before M7's RETURN and T16's re-granted window
```

## 2. Scope

**The membership block** (T16's shape over the inventory; the slice's rule
is the area, three globs -- the eleven named scripts, the sign-in window's
package, `backuptool` -- and no exclusion):

```bash
python3 -I - <<'PY'
import json, collections, os, fnmatch, re
inv = json.load(open("docs/reviews/inventory.json")); cols = inv["columns"]
rows = [dict(zip(cols, r)) for r in inv["rows"]]
sl = json.load(open("docs/reviews/slices.json"))
k17 = [s for s in sl["slices"] if s["k"] == 17][0]; sel = k17["select"]
def expand(g):   # {a,b} brace alternation, recursive; fnmatch does not know it and the inventory's slice_of does
    mm = re.search(r'\{([^{}]*)\}', g)
    if not mm: return [g]
    return [x for alt in mm.group(1).split(",") for x in expand(g[:mm.start()] + alt + g[mm.end():])]
inc = [x for g in sel["globs"] if not g.startswith("!") for x in expand(g)]; exc = [x for g in sel["globs"] if g.startswith("!") for x in expand(g[1:])]
def m(p, g): return fnmatch.fnmatchcase(p, g) or (g.endswith("/**") and p.startswith(g[:-2]))
t17 = [r for r in rows if r["tree"] == "distribution" and any(m(r["path"], g) for g in inc) and not any(m(r["path"], g) for g in exc)]
L = lambda rs: sum(r["lines"] or 0 for r in rs)
print("paths", len(t17), "lines", L(t17), dict(collections.Counter(r["reach"] for r in t17)), dict(collections.Counter(r["tier"] for r in t17)))
print(dict(collections.Counter(r["language"] for r in t17)), dict(collections.Counter(r["area"] for r in t17)))
rc = [r for r in rows if r["tree"] == "distribution" and r["path"].startswith("projects/ROCKNIX/packages/network/rclone/")]
print("the rclone directory in the inventory", len(rc), L(rc), "of which this slice's", sum(1 for r in rc if r in t17), L([r for r in rc if r in t17]))
os.makedirs(".qa-scratch/t17", exist_ok=True)
open(".qa-scratch/t17/paths.txt", "w").write("".join(r["path"] + "\n" for r in sorted(t17, key=lambda r: r["path"])))
for r in sorted(t17, key=lambda r: r["path"]): print(r["lines"], r["language"], r["tier"], r["path"])
PY
wc -l .qa-scratch/t17/paths.txt     # 14
```

Recorded (2026-10-26, from the digest's `git ls-tree -r -l 8ebaf8daad` and
`git show | wc -l` over the three globs expanded by hand; the inventory's
own figures are the block's to print and the lane records any delta): **14
paths, 11,180 lines; read 14 / 11,180 (bash 8, python 4, C 1, recipe 1);
tier fork-own 14; shipped 14**. Eleven sit in
`projects/ROCKNIX/packages/network/rclone/sources/`, which holds 25
inventory rows (the other 14 are T16's; the two slices share no path);
two are the `cloud-signin-window` package; one is
`projects/ROCKNIX/packages/rocknix/sources/scripts/backuptool`.

**The provenance correction to the order.** The inventory's tier is
fork-own for all 14, and for thirteen that is the whole story: none of them
exists in upstream `651150fc88` or in the base `c445081a59` (`git ls-tree`
on each; `git diff --stat 8ebaf8daad 651150fc88 -- <the 14>`: *14 files
changed, 26 insertions(+), 11,138 deletions(-)*). **`backuptool` is the
exception**: upstream and the base carry an identical **68-line** script of
that name (`git show 651150fc88:projects/ROCKNIX/packages/rocknix/sources/scripts/backuptool | wc -l`),
two pre-base commits (ROCKNIX Team, 2025-07-13 `9f1fab30f6`; tiopex, 2026-04-29 `beb5d8a239`),
and the fork's is 1,899 lines after 79 commits since the base. Nothing
upstream-carried is left in it to disposition (D-WORKFLOW-209 reaches
nothing here); what it means for the upstream PR bucket is the
coordinator's question, cited not decided.

**The 14, with what each is** (lines at `8ebaf8daad`; shell functions by `grep -c -E '^[a-z_]+\(\) \{$'` -- a definition whose brace is on its line with no trailing comment; the looser `^[a-z_]+\(\)` counts 22 39 5 16 6 17 19 23 = 147, and the lane states which it used -- python by `grep -c -E '^\s*def '`):

| File | Lines | Mode | Language | Functions | What it is |
| --- | ---: | --- | --- | ---: | --- |
| `cloud_oauth` | 2,830 | 755 | python (`#!/usr/bin/env python3`) | 89 defs, 7 classes | the sign-in: drives `rclone authorize <backend> --auth-no-open-browser` on `127.0.0.1:53682` (`LOCAL_AUTH` `:74`), serves a phone page on `lan_address()` behind a four-digit pin, keeps its state under `/var/run/cloud_oauth/` (`:72`), logs to `/var/log/cloud_sync.log` (`:77`) |
| `backuptool` | 1,899 | 755 | bash | 19 | the settings archive: `tar -czf ... -C / -T <list>` (`:649`), legacy zip read with a CRC check (`:487-518`), the held-back lists, the credential scan, the sanitised copies, the refusals, `ARCHIVE_KEEP=3` (`:172`) |
| `cloud_content_restore` | 1,589 | 755 | bash | 27 | the content restore and **the only deleting path** (`--match --apply`, § 4) |
| `cloud-signin-window/sources/cloud-signin-window.c` | 1,052 | 644 | C | -- | the WebKit window the sign-in opens on the device (`grep -c`: `decide-policy` 2, `policy` 6, `allowed` 10, `https` 3 -- counts; the body is the lane's to read) |
| `cloud_setup` | 976 | 755 | bash | 15 | setup: the folder markers, `--validate-folders`, `--validation-context` (`config_id` the sha256 of REMOTE/SAVES/BACKUPS/CONTENT, `:556`), `--folder-state`, `seed_categories` (CREATE FOLDERS, D-CLOUD-179); **it writes no `rclone.conf`**: its eight `rclone config` lines are two reads (`config file` `:553`, `config show` `:651`), the `pkill` at `:775`, three echoed console instructions (`:938`, `:958`, `:972`) and two comments |
| `cloud_content_backup` | 799 | 755 | bash | 17 | the content backup: `bounded_content_rclone copy` (`:753`, `:766`) under the save and metadata excludes |
| `cloud_device_id` | 401 | 755 | bash | 16 | this device's cloud name: `<device_label>-<md5(permanent MAC\|DEVICE)[:10]>` (`:144`, `:175`), `/etc/machine-id` fallback (`:170`), poisoned-hash healing (`:317-338`, #86), `/storage/.config/cloud_sync-device-id` (`:54`) and `.previous` (`:58`) |
| `cloud_scan` | 362 | 755 | bash | 11 | the scan the transfer pages run first (D-CLOUD-156): read-only, results under `/storage/.cache/cloud_sync/scan/`, every non-zero exit routed (`stop_on` `:150-166`) |
| `cloud_remote` | 345 | 755 | python | 13 defs | providers, fields, choices, list, `active` (the reader `cloud_backup:475/:957` and the harness use); `cmd_create` (`:257-266`) writes through `connections.save` (`:264`; the module imported at `:46`), and its own two `rclone(` calls (`:83` the helper, `:102` `config providers`) are reads |
| `cloud_folder_validate` | 278 | 755 | python (`#!/usr/bin/python3`) | 10 defs, 1 class | the bounded read-only category check: `rclone lsjson --recursive --max-depth N --no-mimetype --no-modtime --contimeout 3s --timeout 5s --max-duration 6s` (`:90-93`), 2 MiB / 4,096 entries / 25 s, stderr to `/dev/null` (`:49`, *diagnostics can contain provider credentials*), any error `Unreadable` |
| `cloud_connections.py` | 258 | 644 | python (a module) | 12 defs, 1 class | **the only writer of `rclone.conf` among the 14** (`CONFIG` `:20`; `cloud_remote create` reaches it through `connections.save`): `atomic()` `:72-85` (`mkstemp` beside the file, write, fsync, `os.replace`, directory fsync), staged configs `chmod(0o600)` (`:160`, `:241`), `active-connection` beside it, `flock` on `/var/run/cloud_sync.lock` (`:107-113`), refuses while either automatic sync option is on (`require_manual` `:117-126`) |
| `cloud_log_scrub` | 206 | 755 | bash | 3 | once per device at boot (`autostart/102-cloud-saves:29`): rewrites `cloud_sync.log*` and `es_log*.txt` under `/storage/.cache/log` through temp and rename with line-count parity (`:148`), masking ` name=value` pairs (`SCRUB_SED` `:78-94`), `cloud_oauth`'s sign-in failure words and ES's `cloud_remote create:` records, plus `redact_credentials`; `set -o pipefail` (`:63`); its record `/storage/.cache/cloud_sync/log-scrubbed` |
| `cloud_content_transfer` | 158 | 644 | bash (sourced) | 4 | `bounded_content_rclone`: the fifo and ceiling under `${CEILING_DIR_ROOT:-/var/run}/cloud-content.XXXXXX` (`:117`), the inactivity bound (D-CLOUD-127, #401), `idle_timeout_seconds` |
| `cloud-signin-window/package.mk` | 27 | 644 | recipe | -- | builds the window against webkitgtk (`-latomic` for WebKit's 128-bit atomics); pulled in by `rclone/package.mk:22` |

Shell: 112 function definitions in 8 files by the strict pattern (147 by the loose one); python: 124 defs and 9 classes (7, 0, 1, 1) in 4 files. **No file sets `set -e` or `set -u`**; `set -o pipefail` globally
only in `cloud_log_scrub:63` (local subshells at `cloud_setup:556`, `backuptool:492/504/537/1177`); `set -x` 0; `eval` 0 in code (`cloud_setup:114`
is a comment saying why). `readonly EXIT_LOCK_HELD=75 EXIT_NO_NETWORK=69`
in the two content scripts; `readonly EXIT_NO_NETWORK=69` at `cloud_scan:43`;
no exit constants elsewhere.

**History** (`git log --no-merges c445081a59..8ebaf8daad -- <the 14>`):
**284 commits** (294 with merges), **Max Engel 265, blitterbot 12,
rasterabot 7**, from 2026-07-25 (`f63308522a`) to 2026-10-13
(`31012f0ca1`); `--since='2026-06-01T00:00:00Z'` on `8ebaf8daad` gives the
same 284 and the same split; all-time 286 (the two extra are upstream's on
`backuptool`). Per file: `cloud_oauth` 70, `cloud_setup` 56,
`cloud_content_restore` 68, `cloud_content_backup` 49, `backuptool` 79 (81 all-time), the sign-in window 32 over its directory (31 the `.c`, 2 the recipe), `cloud_remote` 9, `cloud_device_id`
9, `cloud_scan` 8, `cloud_log_scrub` 3, `cloud_connections.py`,
`cloud_content_transfer` and `cloud_folder_validate` 1 each. The newest
fifteen are blitterbot's and rasterabot's of October: the French phone
keyboard (`31012f0ca1`, `0d69fca540`), saved connections bound to account
state (`bc2dceb406`), explicit folder setup and save coverage
(`e6645cb5ea`), the M7 audit repairs (`ed5a6a51f5`), the content
inactivity bound (`134e89c4fc`), the archive preservation (`f864baac02`).

**Callers outside the 14** (`git grep -l -w <name> 8ebaf8daad`, the 14
excluded; **19** distinct non-slice files under `projects/` and
`packages/`): `rclone/package.mk:67-88` installs the eleven scripts into
`/usr/bin` (`:67-75`, `:82`, `:88`); `autostart/102-cloud-saves:29` runs
`cloud_log_scrub`; `cloud_backup` (T16's) runs `cloud_remote active`
(`:475`, `:957`), `cloud_device_id` (`:1446`) and `backuptool`;
`cloud_capture:698` runs `cloud_device_id`; `cloud_restore` (T16's) runs
`cloud_scan`; `generic-x64-vm` names `cloud_setup` and `cloud_device_id`;
`raofflineproxy-ctl` relies on `backuptool` holding its directory back
(`:237`, `:285`). **The fork's tools** that exercise these files, with the
invoking line: `tools/cloud-connections-test` (`:18` imports
`cloud_connections`; `:177`/`:198` load `cloud_remote` and `cloud_oauth`
by `SourceFileLoader`; T13's Q2: it runs against the host's rclone, not the
image's), `tools/cloud-input-test` (`:9` `cloud_oauth`; `:127` the
pre-fix `a1b0c65165` copy as the control; #535/#536), 
`tools/pixelelated-cloud-validator-test` (22 lines: `cloud_setup
--validate-folders`, `--validation-context`),
`tools/pixelelated-content-scope-test` (21: `cloud_content_restore`'s
modes and `--all`), `tools/pixelelated-save-layout-test` (16:
`cloud_folder_validate`, `cloud_content_backup --list-sizes`,
`cloud_content_restore --scan`), `tools/signin-memory` (the window's load
on a guest), `tools/cloud-round-trip` (139 lines name these files; its
`ACTIVE_COMMAND` `:298` reads `cloud_remote active`),
`tools/cloud-census:76` (`cloud_device_id`, #1081), `tools/vm-qa` (`:233`
the two guests' ids differ; `:304` the active reader; `:417` `cloud_setup
--validation-context`), `tools/rasteratops-vm-cloud-epic`,
`tools/pixelelated-vm-cloud-boundaries` (`cloud_scan --folder`),
`tools/last-good-scripts-test` (every one, under the image's busybox).
**The ES side** is named by path and not read: the setup wizard, the
connection pages, the transfer and scan pages and `ApiSystem` in the
separate `ROCKNIX/emulationstation-next` fork (pinned on
`test/qa-integration`); they are the ES slices' rows.

**The T16 / T17 seam** (from this side; T16's brief names it from its).
A call site is this slice's; the callee's internals are the callee's
slice's: `cloud_scan` runs `cloud_content_restore --scan` and `--systems`
(`:276-279`, here) and `cloud_setup --folder-state` (`:295`, here), and
sources `rasteratops-settings-archive` (`:328`, T16's); `cloud_backup`
(T16's) calls `cloud_remote active`, `cloud_device_id` and `backuptool`
(here) -- what each hands over and what it does with the answer is read
here, the caller's reasons are T16's. The content scripts and `cloud_scan` read `cloud_sync.conf` with readers of their own and call none of T16's `conf_valid`, `cleanup`, `finish` or `usage` (the proof: those names occur in these files only in comments and player text; the definitions live in `cloud_backup:1107`, `cloud_restore:1156`, `cloud_sync_helper:240`, `cloud_capture` and `cloud_net_ready:57`, none in `profile.d`); what they source is `/etc/profile` and `cloud_content_transfer` (the § 5 run lists each file's `source` lines).

**The decisions that bind this slice** (every one a Decided row): **D-CLOUD-023**
(2026-09-04: a third content action makes the device match the cloud; its
deletions are not recoverable locally; preview, confirm, delete outright),
**D-CLOUD-141** (the plan a preview writes is spent by its apply; the same
command again is refused), **D-CLOUD-142** (`cloud_sync.conf` is never
sourced with a command in it; `conf_valid` refuses `$(`, a backtick, `$`,
backslashes and control characters in the folder values), **D-CLOUD-174**
(the defaults `/pixelelated/{Saves,Backups,Content}`), **D-CLOUD-175**
(no automatic cloud-folder migration; linking creates nothing), **D-CLOUD-178**
(the category validator is read-only; fixes are separate explicit actions),
**D-CLOUD-179** (CREATE FOLDERS is its own confirmed action), **D-CLOUD-181**
(integrity inputs apart from published evidence; never a credential in a
packet), **D-CLOUD-127** (SDK retries never outlive inactivity; no total
bound on a progressing library, #401), **D-SYS-001** (`/var/log` is
persistent: the logs the scrubber rewrites are on the card), **D-WORKFLOW-061**
(the wordlist outside every tree; a finding names file:line, never the
word), **D-QA-021** (the read filter: every config-shaped read dropped
through `grep -v -i -E 'key|pass|token|user|psk'`, verdict lines masked),
**D-QA-058** (WebDAV, SFTP and local MinIO/S3 are the baseline; no hosted
account; a provider's real OAuth page stays an unverified follow-up),
**D-INFRA-006** (build credentials stay local), **D-QA-015** (nothing on a
person's device or cloud), **D-QA-063** (the exit lattice). The rule
`rclone-cloud-sync.md` is read whole, with #909's caveat; its lines on
`--delete-excluded` (`:207-226`: safe on backup, catastrophic on a `sync`
restore, stripped unconditionally) and on the allowlist are the standard
the content scripts are held to.

**The blindspots this slice is read against** (`docs/blindspot-register.md`
entries whose text names these files: **1, 3, 7, 13, 16, 19, 22, 24**; the
sign-in and `rclone.conf`: **8, 19, 20, 26**; **48**, the sign-in window's
WebKit video pipeline constraint that lived only in a commit subject):
**7** (archiving a tree with symlinks: `backuptool`'s own history), **13**
(assumed-done), **22** (a probe that cannot report absence: `cloud_scan`'s
routing and `cloud_folder_validate`'s `Unreadable` are its answers), **24**
(a definition below its consumer), **38** (a QA run on the maintainer's
device and cloud: this slice's history, never again). Each is a question
to put to the code, not a finding to copy.

## 3. Read first

1. `docs/reviews/plan-for-the-plan.md` § 6b (the per-slice procedure) and
   § 6c (depth), `docs/reviews/order.md` § T17 and § T16, § T13;
   `docs/futros/2026-10-25-m6-cloud-sync-and-saves.md` whole, its T16
   addendum and errata included.
2. `.claude/rules/rclone-cloud-sync.md` (whole; #909), `engineering-practices.md`
   § *Guards must fail closed*, § *Verify the artifact*, § *Nothing runs
   on a person's device* (the read filter), `upgrade-and-install.md`
   (every fix's `Already written:`; § Migrating data that lives in
   someone's cloud), `es-player-text.md` § Outcome vocabulary (the
   `>>> why` sentences these scripts print are player text), `vm-first.md`,
   `bugs-are-agent-first.md`, `generic-x64-vm-testing.md` (the guest is the
   candidate image: compare the installed file first), `fork-workflow.md`
   § Safety net (the pre-commit's credential patterns: a fixture is
   assembled at run time, never a literal -- #1061 is the case), `docs/device-testing-policy.md`
   § Reading a device's output.
3. T13's audit on its branch: `04-analysis.md` § Q2 (the oracle verdict
   and the host-rclone note), § Q6 (the `cloud-census` ruling), `05-punch-list.md`
   PL-22; `02-forward-audit.md` § Assertion shapes (the 79 rows: which name
   this slice's scripts -- the lane counts them, since the digest found the
   names `cloud_device_id`, `cloud_oauth`, `cloud_connections` and
   `backuptool` in `04` and none in `01`, and T16's lane report's *15 rows
   run only T17's scripts* is unverified by name).
4. The 14, in the lens's order, every line (the order says 11,180 read):
   **`cloud_connections.py`** first (258 lines, the one direct writer of
   `rclone.conf`: every refusal, the lock, the atomic write, the rollback
   on a failed verification, `read_config`'s `rclone config dump` fallback
   -- *never echo the dump*), then **`cloud_oauth`** (the loopback
   authorize, the state file and its lock, the LAN listener and its bounds,
   the pin, the routes and their 409s, the per-session log file at `:915`,
   the pattern kills at `:357` and `:2819`, `lan_address()`), then
   **`cloud-signin-window.c`** (the policy handler: which navigations the
   window allows and where a redirect's query goes), **`cloud_setup`** (the
   `rclone config` write path, `seed_categories`, the markers, the
   validation context, `pkill` at `:775-776`), **`cloud_remote`**
   (`cmd_create`'s `rclone config` call: what reaches rclone's argv and
   what reaches the log), **`cloud_log_scrub`**, **`cloud_device_id`**,
   **`backuptool`** (the held-back lists at `:690-760`, `credential_lines`
   `:431`, the SECRETLIST and SENDLIST arithmetic `:1018-1140`, `keep_meta`
   `:367` and its four call sites, the staging `:1161-1183`, the restore's symlink rules `:813-820` and `:1623-1692`, `snapshot_members` `:599-660`, `write_archive` `:805`, `revert_restore` `:666`, `trim_archive` `:1372`, the `5)` arm at `:1858-1859`),
   **`cloud_content_restore`** (`--match`: `match_plan_one` `:726`, the dry
   run `:750`, `match_plan_write` `:813-821`, `match_run` `:860-911`, the
   apply's `sync` with `--max-delete` `:1046-1049` and the `rclone delete`
   `:1015`, the excludes `:578-584`, `:613-615`, `:676-682`, `set -f`
   `:1389`), **`cloud_content_backup`**, **`cloud_content_transfer`**,
   **`cloud_scan`**, **`cloud_folder_validate`**, the recipe.
5. The tools that already exercise these files (§ 2's list), read for what
   each asserts and under which rclone (`tools/cloud-connections-test`
   runs the host's); `tools/vocabulary-check` for how it reads script
   strings.

## 4. The questions

The renovation face's seven, each answered in `04-analysis.md` with a
proof in `02` (a `proved:` cell: `tree`, `history`, `tool-run`, `fixture`,
`guest`, `design`); the lens is security and the depth reason state
preservation, so Q3 leads with two families of question and Q6 is small:

- **Q3 Bugs -- the lead question, in two families.**
  **(a) Where a secret can travel.** For every credential the product
  touches -- a provider's token in `rclone.conf`, the OAuth code in the
  redirect, the pin, a WebDAV or SFTP secret typed on the phone page, the
  device id -- name every sink it can reach and what masks it there: the
  file it rests in and that file's mode (`rclone.conf` 0600 by
  `mkstemp`'s default carried through `os.replace` -- **by construction,
  not yet observed**: a § 5 fixture reads the mode after `atomic()`;
  `/var/run/cloud_oauth/session.json` written under the default umask
  (`:187-193`) while its lock is 0600 (`:179`) -- what `read_state`
  exposes and whether any field can carry rclone's words; the per-session
  log `open(self.log_path, "w")` at `:915`), the logs (`log()` at `:80`
  appends to `/var/log/cloud_sync.log`, 31 call sites; `logger -t` in
  `backuptool` 38 lines, `cloud_device_id`, `cloud_scan`; the `>>> why`
  lines ES shows), stderr dropped or kept (`cloud_folder_validate:49` drops it on purpose; `cloud_connections.read_config` never echoes the dump;
  where else rclone's stderr is captured and where it goes), a packet
  (D-CLOUD-181), a screen. `cloud_log_scrub` is the measure of what has
  already leaked: its three pattern families are the shapes earlier builds
  wrote, and the question is whether any writer in these 14 still writes
  one of them. **(b) What the deleting path can delete.** `--match --apply`
  is the only content action that deletes (D-CLOUD-023), by two statements:
  `rclone delete "${DEST}/${sys}"` at `:1015` and `bounded_content_rclone
  sync ... --max-delete "${files}"` at `:1046`, both under the preview's
  count. `--max-delete` is a cap, not a transaction (the comment at
  `:1036-1044`: on rclone 1.75.0, three deletions and `--max-delete 2`
  exits 7 having removed two), so the refusals before it are the guard: the
  plan spent (`:890-893`), the context drift (`:898-900`, `SOMETHING
  CHANGED SINCE YOU CHECKED`), the empty plan (`:904-906`, `CHECK WHAT
  WOULD CHANGE FIRST`), a count above the preview's. Are both deleting
  statements reachable only under apply with a spent plan? Can
  `bounded_content_rclone` (`cloud_content_transfer:85`) be handed a verb
  from input? Is `--delete-excluded` absent from every statement (one hit
  in the 14, a comment at `cloud_content_restore:528`; 0 in code)? Does any
  `rm -rf` reach outside the scripts' own temporaries (12 sites: `backuptool`'s
  ten on `${STAGING}`, `cloud_content_transfer:110` on its ceiling dir,
  `cloud_content_restore:1271` on its scan temp)? What do the `pkill -f`
  by pattern at `cloud_setup:775-776`, `cloud_oauth:357` and `:2819` reach
  on a device, and on a host running the harness (blindspot: a pattern that
  matches a harness whose argv carries the words -- `cloud_oauth:861` says
  the serve walks `/proc` for its own kind for this reason)? The LAN phone
  page: what bounds guessing the four-digit pin (`secrets.randbelow(10000)`
  `:2062`, `compare_digest` `:2206`, `MAX_CONNECTIONS 16`,
  `REQUEST_TIMEOUT 15`, the 409s at `:2413` and `:2442`, the serve's
  timeout), and what the page serves to an unauthenticated GET? Then the
  ordinary shapes: a write unchecked (`cmd; rc=$?` on its own line), a
  pipeline judged by its last stage in a file with no `set -o pipefail`
  (every shell file but the scrubber), an unquoted expansion feeding a
  command (five known: `>> ${LOG_FILE}` at `cloud_content_backup:40`,
  `cloud_content_restore:77`, `cloud_setup:53`; `[ -f ${SYNC_CONF} ]` at
  `cloud_scan:54`, `cloud_setup:137`; constants today, each a disposition),
  the predictable `/tmp` fallbacks at `cloud_content_restore:837-838`
  (`$$` when `mktemp` fails: fail-open on a single-user device), a probe
  that cannot report absence (blindspot 22: `cloud_scan`'s `stop_on`,
  `cloud_folder_validate`'s `Unreadable`, `cloud_connections.active`'s
  legacy first remote), a success recorded from an exit status rather than
  the artifact (`backuptool`'s `.partial` then `listed_files` count then
  `mv`, `:649-655`, is the model to hold the others to). **Each bug carries
  its trace, its `Already written:` line and its VM line**; the
  `Already written:` is where state preservation lives: an archive already
  on a device or in a cloud (legacy zip, tar, `ARCHIVE_KEEP=3`, the
  `.backuptool-seeds` list), a `rclone.conf` with no `active-connection`
  beside it (the legacy first remote), a `cloud_sync-device-id` from a
  sit-tunnel kernel (#86's healing), a `content-match-plan` in an older
  shape, a `log-scrubbed` record from a build that covered one family.
- **Q2 Standards.** The player text (`es-player-text.md`): the 13 unique
  `>>> why` sentences the shell files print and `backuptool`'s own list
  (`THERE'S NOTHING TO BACK UP YET`, `A SIGN-IN WAS FOUND IN THE BACKUP`,
  `THIS BACKUP HOLDS FILES A RESTORE CAN'T PUT BACK`, ...) against the
  outcome vocabulary and the two verbs (`BACK UP` 7, `BACKUP` 38 across the 14 by whole-word count; the digest's heuristics found no violation; `tools/vocabulary-check` reads only four of the 14 -- `cloud_content_backup`, `cloud_content_restore`, `cloud_setup`, `backuptool` -- and needs an EmulationStation checkout (`--es`, else exit 1), so the other ten's strings are the lane's own read against the rule, § 5); `cloud_oauth`'s phone page strings in both languages (the
  French phone keyboard, `31012f0ca1`). The scripts' discipline without
  `set -e`: the `|| return` and `rc=$?` shapes, read rather than assumed.
  The modes and owners of what these scripts write under `/storage/.config`,
  `/storage/.cache/cloud_sync` and `/var/run`. The three temp conventions
  (`mktemp` checked in `backuptool:239`, unchecked at `cloud_setup:394`
  with `|| return 5`, the `$$` fallback in the restore).
- **Q1 Modernize.** `cloud_connections.py` is the one writer of `rclone.conf` and the newest shape (atomic, locked, refusing): `cloud_remote create` reaches it through `connections.save`, and `cloud_setup` writes no `rclone.conf` (version 1 said otherwise; the proof corrected it). So the question is whether every path to `connections.save` -- `cloud_remote create`, the interface's connection pages by name, the harness -- takes the same lock and meets the same refusals, and whether `active()`'s legacy first-remote fallback (a `rclone.conf` with no `active-connection` beside it) is still a shape a device can hold once the new writer has written. `cloud_oauth` at 2,830 lines
  and seven classes is the largest single file the fork wrote: name its
  seams (the serve, the browser session, the phone page, the state) as a
  proposal, not a change.
- **Q4 Currency.** `rclone` 1.75.2 on the image against the host's
  1.60.1-DEV that `tools/cloud-connections-test` runs (T13's Q2 note):
  every verdict from that test is a host verdict until the guest repeats
  it. `webkitgtk`'s version and blindspot 48's constraint (video on; the
  recipe says why). M7's open issues on these scripts (#1111 connection
  folders and active selection, #1113 the phone disconnect notice, #1115
  accessibility against the validator's limits, #1117 the validator bound
  to the package's rclone): a finding that meets one is recorded with the
  number and stands against `8ebaf8daad`'s bytes. Upstream: thirteen files
  absent, `backuptool` rewritten (§ 2); the ROCKNIX tracker is not
  consulted from the lane (no network beyond the seats; D-WORKFLOW-162's
  check is the coordinator's at the PR bucket).
- **Q5 Efficiency.** The scan's bounded listings (`cloud_folder_validate`'s
  6 s / 25 s, 2 MiB, 4,096 entries), the content transfer's inactivity
  bound, the sign-in's timeouts (10 s on the opener at `:300`, 15 s on the
  redirect post at `:516`, `REQUEST_TIMEOUT 15`): each stated with what the
  player waits for, and whether `time-to-play` is touched (these scripts
  run from menus, not on the launch path; say so and cite `docs/vm-qa-log.md`).
- **Q6 Dead ends.** The digest found **0 shell functions defined and never
  named elsewhere in the 14** and three python defs referenced once that
  the framework calls (`redirect_request`, `do_GET`, `do_POST`): the lane
  re-counts and reads any `--` option parsed and never used, and the zip
  path in `backuptool` (`:487-518`: read-only for legacy archives --
  reachable while any device holds one; D-WORKFLOW-209: a disposition, a
  row). Removals none.
- **Q7 Clarity and structure.** Can a reader tell, from the directory and
  the rule, which script writes `rclone.conf`, which reads it, which
  deletes anything, which runs at boot, and where each secret may and may
  not appear? One generated table answers it (§ 6, *The writers* and *The
  secrets' paths*); the rule's drift is cited where it misleads (#909).

A finding is one question with its evidence; `Renovation` is the category
for everything here that is not a defect. The seats (Phase 4.6) grade the
findings and the dispositions; each seat's probe comes first.

## 5. The evidence floor

1. Tracker state is never sole evidence; every cell cites a command's
   output or a file:line at `8ebaf8daad`.
2. Mechanical evidence outranks reading: `grep -n` on the scripts, a
   fixture that writes the file and reads its mode back, `git log` with the
   three fork identities, the harness's rows; a comment is the author's
   claim (blindspot 31). **A credential-shaped line is never quoted**: a
   finding names file:line and the shape; counts of the words `key`,
   `pass`, `token`, `user`, `psk`, `secret` are taken unfiltered, lines
   are read through the filter (D-QA-021, D-WORKFLOW-061).
3. **The bench is the host first, then one guest, after two other
   windows.** **Can this be done on the VM? Yes** -- the host for every
   read, count and fixture (`tools/cloud-connections-test`,
   `tools/cloud-input-test`, `tools/pixelelated-cloud-validator-test`,
   `tools/pixelelated-content-scope-test`, `tools/pixelelated-save-layout-test`
   run on the host with synthetic real-rclone controls and no network;
   each records which rclone binary it ran, the host's or the build
   root's); the GENERIC_X64 guest runs the same scripts, busybox, rclone
   1.75.2, sway and webkitgtk as a handheld, with `tools/cloud-test-backend`'s
   WebDAV, SFTP and MinIO/S3 as the cloud (D-QA-058: no hosted account, no
   Dropbox, nothing offsite; a provider's real OAuth page is an unverified
   follow-up, not a "no"); **nothing on a person's device or cloud**
   (D-QA-015; blindspot 38 is this slice's own history). **The window is
   asked for on #664 with its plan after stage B, and runs only after M7's
   RETURN on the host file and after T16's re-granted window has returned**;
   one guest, 30 minutes from START, T13's conditions (the installed
   fourteen hashed against `git show 8ebaf8daad:<path>` before any verdict;
   START and RETURN posted; stop by pidfile; the leftover check; outputs
   kept with `--dump`; the disk retired with its path, size and sha in `00`,
   D-INFRA-022). What the guest proves that the host cannot: the installed
   files are the read tree's; `cloud_connections.atomic()`'s file mode and
   the lock under the image's python; `--match` preview and apply over a
   seeded synthetic content root on WebDAV with the count made to exceed
   the preview (the refusal) and with it matching (the bounded delete), the
   plan spent after; `backuptool backup` with a credential-shaped line
   assembled at run time in a staged config (exit 5, the archive unchanged,
   `THERE'S NOTHING TO BACK UP YET` and `A SIGN-IN WAS FOUND IN THE BACKUP`
   on the page's protocol) and `backuptool restore` over a live symlink
   (never extracted); `cloud_setup --validation-context` and `cloud_scan
   --folder` against each backend's `caps`; the sign-in window's load with
   `tools/signin-memory` (a page load, no account); `cloud_oauth serve` on
   the guest with its state file's mode read back. **The phone page from
   the host** is the one open harness question (bugs-are-agent-first,
   rule 3): under QEMU user-mode networking the guest's `lan_address()` is
   not reachable from the host without a forward the tools do not have, so
   the lane records `CANNOT` with the gap named for the coordinator (a
   Backlog), and proves the handler's ordering and bounds with
   `tools/cloud-input-test` on the host. `tools/council/run invoke` runs
   four times with the key, the two seats' probes and refutations.
4. **What result would have produced a FAIL** is asked of every PASS, in
   writing, in `02`; a verdict from a *device-report* row is not a PASS of
   the code under test, and the exit lattice is D-QA-063's.
5. **A verdict from the guest is a verdict on the installed file** (T22's
   lesson, `generic-x64-vm-testing.md`): the image is the M7 candidate
   `069fc2704421` from M6's retained copy, and the fourteen installed files
   are hashed against the read tree over serial **before any verdict is
   used**; a difference is diffed through the mask on both sides and
   written beside every verdict it touches.

**What never runs in this slice:** a build, a compiler, a plan generation,
a fetch, a network read beyond the four seat calls, a hosted or offsite
cloud account, a provider's sign-in page with an account behind it,
`--real-roms`, `cloud-census`, a command against a handheld or a person's
cloud, a read of an M7 build root or worktree, a guest outside the one
granted window or before M7's RETURN, a `tools/council/run` call with the
key beyond the four, a credential-shaped literal written to any file at
rest, and a change to any file under `packages/`, `projects/` or `tools/`
at stages A to D.

**The runs, with what the coordinator read** (the lane runs each at stage
A and records the exit, the wall time and the summary line; `TMPDIR` under
`/workspace/tmp/m6-t17/`; `R=8ebaf8daad`; `P` the eleven scripts' directory):

```bash
D=/workspace/repos/pixelelated/distribution.worktrees/m6-cloud-setup-content-664
cd "$D"; export TMPDIR=/workspace/tmp/m6-t17/tmp; mkdir -p "$TMPDIR" .qa-scratch/t17
R=8ebaf8daad; P=projects/ROCKNIX/packages/network/rclone/sources
# the membership block (§ 2) -> .qa-scratch/t17/paths.txt (14)
# the lines, modes and functions (expect 11,180; modes 100755 x 10 and 100644 x 4; shell definitions by the strict pattern 17 27 4 16 3 11 15 19 = 112 and by the loose one 22 39 5 16 6 17 19 23 = 147; python defs 89 13 10 12 = 124, classes 7 0 1 1)
tr '\n' '\0' < .qa-scratch/t17/paths.txt | xargs -0 git ls-tree -l $R -- | awk '{print $1}' | sort | uniq -c
while IFS= read -r p; do printf '%6d %s\n' "$(git show "$R:$p" | wc -l)" "$p"; done < .qa-scratch/t17/paths.txt | awk '{s+=$1} END {print "lines", s}'
for f in cloud_content_backup cloud_content_restore cloud_content_transfer cloud_device_id cloud_log_scrub cloud_scan cloud_setup; do printf '%s strict %s loose %s\n' "$f" "$(git show "$R:$P/$f" | grep -c -E '^[a-z_]+\(\) \{$')" "$(git show "$R:$P/$f" | grep -c -E '^[a-z_]+\(\)')"; done; printf 'backuptool strict %s loose %s\n' "$(git show "$R:projects/ROCKNIX/packages/rocknix/sources/scripts/backuptool" | grep -c -E '^[a-z_]+\(\) \{$')" "$(git show "$R:projects/ROCKNIX/packages/rocknix/sources/scripts/backuptool" | grep -c -E '^[a-z_]+\(\)')"
for f in cloud_oauth cloud_remote cloud_folder_validate cloud_connections.py; do printf '%s %s defs %s classes\n' "$f" "$(git show "$R:$P/$f" | grep -c -E '^\s*def ')" "$(git show "$R:$P/$f" | grep -c -E '^class ')"; done
# set discipline (expect: no global set -e or set -u in any; pipefail global only in cloud_log_scrub:63; set -x 0; eval 0 in code)
tr '\n' '\0' < .qa-scratch/t17/paths.txt | xargs -0 git grep -n -E '^\s*set -[eux]|set -o pipefail|\beval\b' $R -- | sed "s/^$R://" | grep -v -E '^[^:]+:[0-9]+:\s*#'
# the exit constants (expect EXIT_LOCK_HELD=75 EXIT_NO_NETWORK=69 in the two content scripts; EXIT_NO_NETWORK=69 at cloud_scan:43)
git grep -n -E 'readonly EXIT_|^EXIT_[A-Z_]+=' $R -- "$P" | sed "s/^$R://"
# the one writer of rclone.conf (expect cloud_connections.py:20 CONFIG, :72-85 atomic, :160 and :241 chmod 0o600; cloud_remote:264 connections.save with its rclone( calls :83 and :102 reads; cloud_setup's 'rclone config' lines :553 and :651 reads, :775 the pkill, :938 :958 :972 echoes, the rest comments; the scrubber's five are patterns)
git grep -n -E 'rclone\.conf|mkstemp|os\.replace|chmod\(0o600\)|umask' $R -- $(tr '\n' ' ' < .qa-scratch/t17/paths.txt) | sed "s/^$R://" | grep -v -i -E 'key|pass|token|user|psk' | grep -v -E ':[0-9]+:\s*#'
git show "$R:$P/cloud_setup" | grep -n 'rclone config' | grep -v -E '^[0-9]+:\s*#' | cut -c1-120; git show "$R:$P/cloud_remote" | grep -n -E 'connections\.(save|select|remove)|rclone\(|^import |^from ' | cut -c1-120
# the deleting statements and the one --delete-excluded (expect rclone delete at cloud_content_restore:1015; sync at :750 with --dry-run and at :1046 with --max-delete; --delete-excluded 1 hit, a comment at :528, 0 in code; rm -rf 12 sites, every one on a script's own temporary)
git grep -n -E 'rclone (delete|purge|sync|move|rmdir)|bounded_content_rclone (sync|delete|move|purge)' $R -- $(tr '\n' ' ' < .qa-scratch/t17/paths.txt) | sed "s/^$R://" | grep -v -E ':[0-9]+:\s*#'
git grep -n -- '--delete-excluded' $R -- $(tr '\n' ' ' < .qa-scratch/t17/paths.txt) | sed "s/^$R://"
git grep -n -E 'rm -rf' $R -- $(tr '\n' ' ' < .qa-scratch/t17/paths.txt) | sed "s/^$R://" | grep -v -E ':[0-9]+:\s*#' | wc -l
git show "$R:$P/cloud_content_restore" | sed -n '886p;890,893p;898,900p;904,906p;1046,1049p'
# the pattern kills, the unquoted sites, the $$ names (expect cloud_setup:775-776, cloud_oauth:357 and :2819, :861 a docstring; backup:40 restore:77 setup:53 scan:54 setup:137; 14 `.$$` lines in the slice, restore:837-838 the two mktemp fallbacks among them)
git grep -n -E 'pkill|killall' $R -- $(tr '\n' ' ' < .qa-scratch/t17/paths.txt) | sed "s/^$R://" | grep -v -E ':[0-9]+:\s*#'
git grep -n -E '\[ -[a-z] \$\{[A-Z_]+\} |>> \$\{[A-Z_]+\}$' $R -- $(tr '\n' ' ' < .qa-scratch/t17/paths.txt) | sed "s/^$R://"
git grep -n -E '\.\$\$' $R -- $(tr '\n' ' ' < .qa-scratch/t17/paths.txt) | sed "s/^$R://" | grep -v -E ':[0-9]+:\s*#'
# cloud_oauth's constants and bounds (expect STATE_DIR /var/run/cloud_oauth :72; LOCAL_AUTH 127.0.0.1:53682 :74; LOG_FILE /var/log/cloud_sync.log :77; lock 0o600 :179; MAX_BODY 64 KiB :2215; REQUEST_TIMEOUT 15 :2216; MAX_CONNECTIONS 16 :2217; the pin :2062 and :2206)
git show "$R:$P/cloud_oauth" | grep -n -E '^(STATE_DIR|RCLONE|LOCAL_AUTH|LOG_FILE|MAX_BODY|REQUEST_TIMEOUT|MAX_CONNECTIONS) =|0o600|secrets\.(randbelow|compare_digest)|def (log|state_path|_write_whole|write_state|write_owned|read_state|lan_address|serve_with|cmd_serve)\b|class BoundedHTTPServer'
# backuptool's lists and refusals (expect DEVICEONLYDIRS rclone/ and raofflineproxy/; DEVICEONLY 4 files; ARCHIVE_KEEP=3 :172; the 5) arm :1858-1859; .partial then listed count then mv :649-655; 37 'logger -t backuptool' lines; one >>> why emitter :270)
git show "$R:projects/ROCKNIX/packages/rocknix/sources/scripts/backuptool" | sed -n '690,760p' | grep -v -E '^\s*#' | grep -v -E '^\s*$' | grep -v -i -E 'key|pass|token|user|psk'
git show "$R:projects/ROCKNIX/packages/rocknix/sources/scripts/backuptool" | grep -n -E '^ARCHIVE_KEEP=|A SIGN-IN WAS FOUND|\.partial|^[a-z_]+\(\)' | grep -v -i -E 'key|pass|token|user|psk' | head -60
git show "$R:projects/ROCKNIX/packages/rocknix/sources/scripts/backuptool" | grep -c 'logger -t backuptool'
# cloud_device_id's derivation (expect :54 ID_FILE, :58 .previous, :144 md5 cut -c1-10, :170 machine-id, :175 the id, :289-292 tmp then mv)
git show "$R:$P/cloud_device_id" | sed -n '54p;58p;144p;170p;175p;289,292p'
# cloud_folder_validate's bounds and cloud_scan's routing (expect lsjson flags :90-93, stderr DEVNULL :49, 2 MiB / 4096 / 25 s; stop_on :150-166)
git show "$R:$P/cloud_folder_validate" | grep -n -E 'MAX_BYTES|MAX_ENTRIES|TOTAL_SECONDS|contimeout|max-duration|DEVNULL|class Unreadable'
git show "$R:$P/cloud_scan" | sed -n '43p;150,166p'
# the scrubber's record and the boot hook (expect 102-cloud-saves:29; log-scrubbed; SCRUB_SED :78-94; parity :148)
git grep -n 'cloud_log_scrub' $R -- projects/ROCKNIX/packages/network/rclone/autostart/102-cloud-saves | sed "s/^$R://"; git show "$R:$P/cloud_log_scrub" | grep -n -E 'log-scrubbed|^SCRUB_SED|set -o pipefail'
# the history with the three identities (expect 284 non-merge base..R; 265 / 12 / 7; span 2026-07-25 .. 2026-10-13; since June 284; backuptool 79 of them)
tr '\n' '\0' < .qa-scratch/t17/paths.txt | xargs -0 git log --no-merges --format='%h %an' c445081a59..$R -- | tee "$TMPDIR/hist.txt" | wc -l; cut -d' ' -f2- "$TMPDIR/hist.txt" | sort | uniq -c | sort -rn
tr '\n' '\0' < .qa-scratch/t17/paths.txt | xargs -0 git log --no-merges --format='%ad' --date=short c445081a59..$R -- | sort | sed -n '1p;$p'
tr '\n' '\0' < .qa-scratch/t17/paths.txt | xargs -0 git log --no-merges --format=%h --since='2026-06-01T00:00:00Z' $R -- | wc -l
git log --no-merges --format=%h c445081a59..$R -- projects/ROCKNIX/packages/rocknix/sources/scripts/backuptool | wc -l
# the upstream relation (expect only backuptool in 651150fc88 and c445081a59, 68 lines in each, identical; diff --stat R..upstream over the 14: 14 files, +26 / -11,138)
for c in 651150fc88 c445081a59; do tr '\n' '\0' < .qa-scratch/t17/paths.txt | xargs -0 git ls-tree --name-only $c -- 2>/dev/null; done | sort | uniq -c
git show 651150fc88:projects/ROCKNIX/packages/rocknix/sources/scripts/backuptool | wc -l; git diff --quiet 651150fc88 c445081a59 -- projects/ROCKNIX/packages/rocknix/sources/scripts/backuptool && echo identical
tr '\n' '\0' < .qa-scratch/t17/paths.txt | xargs -0 git diff --stat $R 651150fc88 -- | tail -1
# the callers outside the 14 (expect 19 distinct non-slice files under projects/ and packages/; package.mk:67-88 installs eleven; 102-cloud-saves:29; cloud_backup :475 :957 :1446; cloud_capture:698)
for n in cloud_oauth cloud_setup cloud_remote cloud_connections cloud_content_backup cloud_content_restore cloud_content_transfer cloud_scan cloud_folder_validate cloud_device_id cloud_log_scrub cloud-signin-window backuptool; do git grep -l -w "$n" $R -- projects packages | sed "s/^$R://"; done | sort -u | grep -v -x -F -f .qa-scratch/t17/paths.txt | tee "$TMPDIR/callers.txt" | wc -l
git grep -n -E 'cp cloud_|cloud-signin-window' $R -- projects/ROCKNIX/packages/network/rclone/package.mk | sed "s/^$R://"
# the tools that exercise the 14 (expect the invoking lines the brief names; cloud-connections-test imports cloud_connections at :18)
for t in cloud-connections-test cloud-input-test pixelelated-cloud-validator-test pixelelated-content-scope-test pixelelated-save-layout-test signin-memory cloud-round-trip cloud-census vm-qa pixelelated-vm-cloud-boundaries last-good-scripts-test; do printf '%s %s\n' "$t" "$(git show "$R:tools/$t" | grep -c -w -E 'cloud_oauth|cloud_setup|cloud_remote|cloud_connections|cloud_content_backup|cloud_content_restore|cloud_content_transfer|cloud_scan|cloud_folder_validate|cloud_device_id|cloud_log_scrub|cloud-signin-window|backuptool')"; done
# T13's oracle rows that name this slice's scripts (expect 5 rows within 02's `## Assertion shapes`, whose 78 rows and CONTRACT sit at 02:128; 04 names cloud_device_id 3, cloud_oauth 1, cloud_connections 1, backuptool 1, and 01 none)
git show feature/m6-cloud-harness-660:docs/audits/2026_10_25-epic-m6-cloud-harness/02-forward-audit.md | awk '/^## Assertion shapes/{p=1;next} /^## /{p=0} p' | grep -c -w -E 'cloud_oauth|cloud_setup|cloud_remote|cloud_connections|cloud_content_backup|cloud_content_restore|cloud_content_transfer|cloud_scan|cloud_folder_validate|cloud_device_id|cloud_log_scrub|backuptool'
# the player text (expect 'BACK UP' 7, 'BACKUP' 38 across the 14, whole words; vocabulary-check reads four of the 14 and needs an EmulationStation checkout: its verdict, or CANNOT with the four named and the other ten read by hand)
tr '\n' '\0' < .qa-scratch/t17/paths.txt | xargs -0 git grep -o -h -w -E 'BACK UP|BACKUP' $R -- | sort | uniq -c
grep -n -E 'cloud_|backuptool|--es|ES_SRC' tools/vocabulary-check | head -n 12; if [ -n "${ES_SRC:-}" ]; then tools/vocabulary-check --es "$ES_SRC" 2>&1 | tail -n 3; else echo "CANNOT: no EmulationStation checkout named (ES_SRC); the four scripts it reads are read by hand against es-player-text.md"; fi
# what each shell file sources (expect /etc/profile and cloud_content_transfer; none of T16's conf_valid, cleanup, finish or usage is called -- the names occur here only in comments and player text)
for f in cloud_content_backup cloud_content_restore cloud_content_transfer cloud_device_id cloud_log_scrub cloud_scan cloud_setup; do printf '%s: ' "$f"; git show "$R:$P/$f" | grep -n -E '^\s*(\.|source) ' | tr '\n' ' '; echo; done; printf 'backuptool: '; git show "$R:projects/ROCKNIX/packages/rocknix/sources/scripts/backuptool" | grep -n -E '^\s*(\.|source) ' | tr '\n' ' '; echo
# the removal rule's own check against the dispatch tip (expect empty)
git diff --stat <dispatch tip> HEAD -- packages projects tools | tail -1
```

## 6. Outputs

As T16's brief § 6, with the folder `docs/audits/<yyyy_mm_dd>-epic-m6-cloud-setup-content/`:
`00` to `05`, `second-opinions/` (both seats' plans, the manifest with its
three-way scan and every scan hit's disposition, each probe and refutation
with provenance), `guest-cycle/` (the window's record: the image's identity,
the fourteen image-versus-tree hashes, each proof's dump, the leftover
check), the lint before D, the audit issue (`Audit: M6 T17 cloud setup,
sign-in, connections and settings backups -- N findings (...)`, a sub-issue
of #664), the bugs, and the retro at
`docs/retros/<date>-m6-cloud-setup-content.md` (**what the slice did to
the two time-to-play numbers**: nothing here is on the launch path, so the
answer is cited from `docs/vm-qa-log.md`, never "nothing" by default;
**what the ES slices inherit**: the surfaces these scripts' `>>> why`
lines reach, the sign-in window's contract, the phone page's states).
**`02` carries § Coverage (14), § The writers (one generated row per
statement that writes `rclone.conf`, `active-connection`,
`cloud_sync-device-id`, the match plan, the OAuth state, the scan results,
the scrubber's record or an archive: file:line, the file written, the
mode it ends with, the lock held, temp-and-rename or in place), § The
secrets' paths (one row per credential kind and per sink it can reach --
file, log, stderr, state, packet, screen -- with the mask at that sink or
`none`), § The deletions (every `rm`, `rclone delete`, `sync`, `move`,
`purge`, with its bound and the condition that reaches it), § The archive
(`backuptool`'s held-back lists, the SECRETLIST arithmetic, `keep_meta`'s
fields, the restore's skip rules, the legacy zip path), § The phone flow
(the listener's bind, bounds, pin, routes and their responses), § The
runs (every § 5 command), § The guest cycle, § Positives, and every proof
with `proved:`.** The stage-D pause as T22's: the punch list posted on
#664, the lane waits for the coordinator's dispositions and any stream
brief.

## 7. Acceptance

The checklist on #664 becomes this section at dispatch, written there by
the coordinator in place of P1's five generated ones. Every checkbox names
the artifact that ticks it (D-QA-044); the coordinator ticks at acceptance,
from the artifacts, never from the hand-back's words.

- [ ] `docs/audits/<date>-epic-m6-cloud-setup-content/` holds `00-running-log.md` and `01-research-notes.md` to `05-punch-list.md`.
- [ ] `tools/lint-audit-artifacts docs/audits/<date>-epic-m6-cloud-setup-content/` prints `PASS` (its default `resolution` phase, at close; before stage D the same command with `--phase pre-issue` prints `PASS pre-issue artifacts (does not certify resolution)`), the renovation face included.
- [ ] `second-opinions/review-plan.json` records `depth: extended` and two reviewers (`gpt`, `openai/gpt-6-astra`, `max`; `gemini-argon`, `google/gemini-4-argon`, `high`); each seat's probe and refutation have a `.provenance.json` beside them whose served model is the seat's, whose verification is PASS and whose `facilitator` block is present (read with `tools/council/run summary` over `second-opinions/`, the run summary from the provenance siblings, and `tools/council/run verify-seals`); `manifest.json` lists every packet file with its sha256 and its three-way scan, every scan hit with a disposition, and no hit that is a value.
- [ ] The slice's punch-list issue has every item at a Phase 7 outcome: resolved with its commit, deferred to a named issue (a `bug`, a Backlog the coordinator files, #909, #585, an ES slice's issue the coordinator names, an M7 issue by number), or recorded as a design with its sentence; `tools/box-check --issue <N>` 0 fail; the issue closed by the coordinator with the lint's PASS quoted.
- [ ] `reviewed-at:` and `fixed-at:` in the checklist's header carry the lane's commits; the read is on `8ebaf8daad`'s bytes for the 14 (``tr '\n' '\0' < .qa-scratch/t17/paths.txt | xargs -0 git diff --stat 8ebaf8daad <reviewed-at> --`` empty) and nothing under `packages/`, `projects/` or `tools/` changes at stages A to D (`git diff --stat <dispatch tip> <stage-D tip> -- packages projects tools` empty).
- [ ] `01-research-notes.md` § Scope records § 2's block with its output (14 paths, 11,180 lines; read 14; fork-own 14; shipped 14; the rclone directory's 25 rows, 11 of them this slice's -- or the deltas beside them), the provenance correction (`backuptool` 68 lines in upstream and base, identical; the other thirteen absent), the history (284 non-merge since the base, 265 / 12 / 7, 2026-07-25 to 2026-10-13; since June the same), the callers (19 non-slice files; the tools' invoking lines) and the T16 / T17 seam from this side.
- [ ] `02-forward-audit.md` carries a coverage table with exactly one row per path under its own `## Coverage` heading, the path in backticks as the first cell: ``awk '/^## Coverage/{p=1;next} /^## /{p=0} p' 02-forward-audit.md | grep -c -E '^\| `'`` prints `14`.
- [ ] `02-forward-audit.md` § The writers is generated by a script under the audit folder's `tools/` from `grep -n` over the 14 at `8ebaf8daad` (the generator asserts its row count and exits 1 on drift), one row per writing statement of `rclone.conf`, `active-connection`, `cloud_sync-device-id`, the match plan, the OAuth state, the scan results, the scrubber's record and an archive, each with the mode the file ends with (`observed` from a fixture or the guest, else `by construction`), the lock held and temp-and-rename or in place; the one writer of `rclone.conf`, `cloud_connections.atomic()`, appears with every path that reaches it (`cloud_remote create` through `connections.save`; the interface's pages by name), and the table states in words that `cloud_setup` writes no `rclone.conf`.
- [ ] `02-forward-audit.md` § The secrets' paths has one row per credential kind (provider token, OAuth code, pin, typed WebDAV/SFTP secret, device id) per sink it can reach (file, `/var/log/cloud_sync.log`, stderr, `/var/run/cloud_oauth/session.json`, the per-session log, a packet, a screen), each with the mask at that sink or `none`, and names `cloud_log_scrub`'s three pattern families as the shapes earlier builds wrote with a `writes it today: yes/no` cell per family.
- [ ] `02-forward-audit.md` § The deletions lists every `rm -rf`, `rclone delete`, `sync`, `move` and `purge` statement in the 14 with its bound and the condition that reaches it, states `--delete-excluded` 0 in code (one comment at `cloud_content_restore:528`), and shows the two deleting statements of `--match --apply` (`:1015`, `:1046`) reachable only with a spent `plan2` plan whose context and mode match and whose count the device's listing does not exceed, with the refusal lines quoted.
- [ ] `02-forward-audit.md` § The runs records every § 5 command with exit, wall time, the figure and *a FAIL would mean ...*; a run that cannot be made is `CANNOT` with its reason, never a pass; the per-file list of sourced files is one of them.
- [ ] `02-forward-audit.md` § The guest cycle records the window the coordinator granted on #664 (the comment's time, after M7's RETURN and T16's re-granted window on the host file), the image by file name and BUILD_ID (read from the guest), the fourteen installed files' hashes against `git show 8ebaf8daad:<path>` before any verdict (and every verdict a difference touches named), the `--match` refusal and the bounded apply over a seeded synthetic root with their dumps, `backuptool`'s exit 5 on a run-time-assembled credential-shaped line and its unchanged archive, the symlink never extracted, `cloud_connections.atomic()`'s observed mode, `tools/signin-memory`'s row, and the phone-page `CANNOT` with its gap, or the proof if the harness can reach it; **if no window is granted before the hand-back**, the section records `CANNOT` with the host file's state at the hand-back and names each guest proof that moved to a host fixture or stays open.
- [ ] `00-running-log.md` shows no build, no compiler, no plan generation, no fetch (the council runtime from `npm install --offline`), no handheld, no hosted or offsite account, no provider page with an account behind it, no `--real-roms`, no `cloud-census` run, no M7 build root or worktree read, guests only inside the granted window and after M7's RETURN, exactly four `tools/council/run invoke` calls with the key and every other `tools/council/run` call with `COUNCIL_ENV_FILE=/nonexistent`, every config-shaped read through the filter, and no credential-shaped literal written to any file (the pre-commit hook never refused a commit, or the refusal and its fix are recorded).
- [ ] `04-analysis.md` § Q3 states each bug decision with its trace, its `Already written:` line and its VM line, in the two families (where a secret can travel; what the deleting path can delete); § Q2 the player-text and discipline findings with `tools/vocabulary-check`'s verdict or its `CANNOT` (it reads four of the 14 and needs an EmulationStation checkout) and the lane's own read of the other ten; § Q4 the host-rclone caveat on every `tools/cloud-connections-test` verdict and each M7 issue a finding meets by number; § Q6 the zip path's disposition and every uncalled function, removals none; § Q7 points at the two generated tables.
- [ ] Every proof in `02-forward-audit.md` carries a `proved:` cell reading `tree`, `history`, `tool-run`, `fixture`, `guest` or `design`; every punch item carries `question:`; every `bug` passes `tools/box-check --issue N` and carries its `Already written:` line and names file:line, never a credential-shaped value.
- [ ] The retro exists at `docs/retros/<date>-m6-cloud-setup-content.md`, is posted on #664, says what the slice did to the two time-to-play numbers (cited from `docs/vm-qa-log.md`; these scripts are off the launch path, and it says so), and what the ES slices inherit.
- [ ] `tools/register-check`, `tools/work-log-index --check`, `tools/rules-check --quiet`, `tools/forbidden-terms-check` and `.githooks/hooks-test` pass on the branch before its merge (after the coordinator's hand-back merge).

## 8. Stop conditions

Stop only on: every item of § 7 that is this lane's ticked and the branch
pushed (the hand-back); the stage-D pause; an explicit maintainer pause on
#664; a blocker named on #664 (a seat that fails its provenance gate twice,
a packet scan hit that is a value, a backend that will not come up on the
lane's ports, two commands that disagree, a block whose output differs
from § 2's beyond the deltas it records); a branch that differs from
`8ebaf8daad` on one of the 14 at stage A; or an execution limit, stated as
such with the running log current. A checkpoint is not a stop. An idle
session says it is idle on #664, **and does not end a turn on a post that
asks nothing**.

## 9. Ceremonies owed

- A work-log entry per session headed `#664`, its time from `date -u` in
  the same command, prose through a quoted heredoc; `tools/work-log-index
  --write` after it.
- A friction line the moment something slows, with `issue: #664` or the
  guard.
- The VM question written before any proof (§ 5: yes, the host first, then
  one guest window after M7's RETURN and T16's; nothing on a person's
  device or cloud).
- The mini-retro at stage G, posted on #664, Instruction-Recommendations
  mode; its *adjustments* are proposals for the coordinator; its scoped
  audit runs check 7's step 5 where a fix landed.
- A register row the same session for any decision the slice forces (none
  expected); D-WORKFLOW-209 is the highest Decided row on the coordinator's
  branch (D-WORKFLOW-188 on the P1 branch only; the merge unites them); a
  row this slice forces takes an ID the coordinator assigns on #664.
- `tools/ceremony-check` before every push; never `--no-verify`; a merge
  with conflicts is checked for markers; the ledgers united by whole
  entries; **a commit names its paths**; anything temporary under
  `/workspace/tmp/m6-t17/` after `df -i`, never `/tmp`; the window's
  record kept on the branch, the guest disk retired after it with the
  retirement recorded in `00` (D-INFRA-022); **`rm -rf` only as
  `"${VAR:?}"/...` or a literal path, in its own short command, never
  inside a `bash -c` script** (the T16 lane's first runner was auto-denied
  for that shape).
- Commit messages `docs: ...`, with `Refs #664`.

## 10. Hand-back

The coordinator accepts by reading, in this order, without re-reviewing:
#664's checkboxes against their artifacts; the lint's `PASS` line;
`review-plan.json` and the four provenance files (read with the current
reader) and the manifest's scans; the audit issue's checkboxes all at an
outcome; the coverage table's row count (14), § The writers' and § The
secrets' paths' generated counts, § The deletions' statements; every Q3
bug with its three lines; **re-running on a clone of the branch at the tip
under `/workspace/tmp/m6-coordinator/`: the membership block and every § 5
run in full** (no guest: the window's record is read, not repeated);
`register-check` on a simulated merge with the coordinator's tip (the
ledgers united); the retro's answers; the six exit codes. The lane posts one
hand-back comment naming the tip and each artifact by path, writes
`reviewed-at:` and `fixed-at:` into #664's body, then says it is idle.
After acceptance the coordinator closes the audit issue, prompts the lane
for `audit-completion.json` and the full lint, merges the branch in its
turn after the M7 candidate (after T16's), regenerates the ledgers, posts
any #585 lines in the shape the lane wrote, and closes #664 when every row
is proven; the cloud epic #1047 closes when its three slices have.

**The readings before dispatch** (plan § 3, principle 3): the epic's futro
(#1047) takes a T17 kickoff addendum written with this version, and a
stranger's proof of this brief is run by a reader with no context before
dispatch; version 2 records what each found.

## Version 2: what the stranger's proof found (2026-10-26)

Ten commands from the scratch clone at `2174265e9c`; the membership block
ran as written (14 / 11,180 / fork-own 14 / shipped 14 / the directory's 25
of which 11), and every path, mode, history figure, constant and refusal
line held. The corrections:

1. **Version 1's two "writers through rclone" do not exist.** `cloud_setup`'s
   eight `rclone config` lines are two reads, the `pkill`, three echoed
   instructions and two comments; `cloud_remote create` writes through
   `connections.save`. `cloud_connections.atomic()` is the one writer among
   the 14. § 2's table, Q1, the § 5 run and checkbox 8 are rewritten.
2. The shell function counts reproduce only with `^[a-z_]+\(\) \{$`; the
   loose pattern gives 147. Both are stated and the run prints both.
3. § 5's mode tally kept the size column; fixed.
4. The config-verb run is replaced by the writer run above.
5. The `BACKUP` count needs `-w` (126 without it).
6. `tools/vocabulary-check` reads four of the 14 and exits 1 without an
   EmulationStation checkout; Q2, the run and checkbox 14 say so.
7. The local-or-inherited run could not answer: none of the four names is
   called in these files. The question is closed and the run lists each
   file's sourced files instead.
8. Line slips: `write_archive` is `:805` (`:599-660` is `snapshot_members`),
   `cloud_folder_validate`'s `DEVNULL` is `:49`, `backuptool:1858-1859` is
   the `5)` arm, the symlink rules run to `:1692`, a pipefail subshell at
   `backuptool:1177`.
9. Counts: `logger -t backuptool` 37; the sign-in window's 32 commits are
   31 on the `.c` and 2 on the recipe; the second pre-base `backuptool`
   commit is tiopex's; the `.c` keyword counts restated; `secret` 6 is
   case-insensitive.
10. The `.$$` and deletion runs now take the 14 paths, not the whole
    directory, and drop comments.
11. Stranger traps named: the register rows on the coordinator's branch
    only; `3a653eaec4` after a fetch; #1029 is T15's; M7's host-file lines
    are timestamped, not `== ` blocks, and its native stage has returned;
    checkbox 2's string quoted whole; checkbox 3 names the reader; checkbox
    12 has a `CANNOT` form for a window never granted.

## Errata at acceptance (2026-10-26)

What the lane found that version 2 had wrong or did not foresee, recorded
here rather than edited into the sections above:

- **15 `.$$` lines in the 14, not 14:** `cloud_content_restore:819` is the
  plan's temp-write `printf`, beside the two `mktemp` fallbacks at
  `:837-838` (stage A).
- **The exit-constant run read the whole rclone directory** and printed
  T16's four constants too; it should take the 14 paths like the other runs
  (stage A).
- **`backuptool:224`'s `rm -rf "${STAGING_PREFIX}"*`** sweeps the script's
  own prefix (`/storage/.cache/backuptool-staging.`, `:762`): "every
  `rm -rf` on a script's own temporary" holds, and the brief should have
  said so (stage A).
- **`tools/vocabulary-check`'s default EmulationStation checkout exists on
  the host** (`~/Development/emulationstation-next.worktrees/qa-integration`,
  at the pin); the brief's `CANNOT` assumed none. Ruled a read with
  provenance; it ran, 163 judged, 0 wrong (stage A).
- **The symlink-member proof (F-04) was answered on the host** by the image's
  own busybox `tar` refusing a symlink with a child, not on the guest; the
  guest's full restore then found **F-24**: a standalone symlink member is
  restored, and a failed restore's revert over a restored-into directory
  fails too (stream S7, #1136-class bug).
- **The window sequencing changed at stage B**: M7's guest first, then T17's,
  then T16's re-grant when its session can run; the brief's "after T16's
  re-granted window" assumed the T1 session could run. T17's first window
  ran 07:59-08:06 and a second, 08:18-08:21, for five proofs the first did
  not reach.
- **Checkbox 3's reader was wrong:** `tools/council/run summary` and
  `verify-seals` read a council run's manifest, which audit invokes do not
  have; the evidence is the direct read of each `.provenance.json`
  (verification PASS, served model and provider, output hash,
  `facilitator_version`). #664's checkbox 3 was reworded at the stage-D
  pause.
- **Six streams, then seven, where the futro's addendum said "none
  expected"**: PL-01+14, PL-02 (Medium), PL-03 (Medium), PL-04+08, PL-05,
  PL-06, F-24. **D-CLOUD-185** was written for PL-02's allowlist, and the
  seam to T16's twins posted on #663.
- **The seats added F-20** (an option-shaped key reaching rclone as a flag),
  which version 2 did not anticipate; both seats raised F-02 and F-03 to
  Medium and the ruling followed them on impact.
- **The image copy the lane used is `m6-t2-20261023`**, not the
  `m6-t3-20261024` copy T16's grant named; both carry `069fc2704421`.
- **Seven streams, the seventh at the hand-back:** S7 (`backuptool`, #1136)
  refuses every member that is not a file or a folder before extraction --
  pairing `tar -tv`'s lines with `tar -t`'s names, since busybox prints a
  hard link as `-` -- and the revert removes, under `/storage` only, a
  folder the restore made; its fixture runs the real `backuptool restore`
  in an unprivileged bubblewrap sandbox (`--clearenv`, after the sandbox
  inherited the host's `TMPDIR`) and fails on the unfixed file.
- **The credential refusal's exit is 1, not 5:** 5 is `write_archive`'s
  return, which the `backup` command maps to the why at `backuptool:1858`;
  the brief wrote the function's code as the process's.
- **`tools/signin-memory`'s default page is a network read** (`example.org`)
  the slice forbids; the lane loaded a host-local static page instead
  (`python3 -m http.server` on 127.0.0.1, stopped by its PID), keeping the
  QA WebDAV root's 401 as the FAIL it was: PASS at 104, 98 and 42 MB, 245
  MB together. The brief's "a page load, no account" assumed the tool's
  page was local.
- **The phone page stayed `CANNOT`** under user-mode NAT with only ssh
  forwarded, the gap named as the brief asked: a `hostfwd` for the serve's
  port, or a second guest. The handler is proved on the guest over
  loopback (the first window).
- **A stream regressed a check and the suite caught it two streams later:**
  S3's name check at `f8feb15bb4` also refused `--selected` and `--all`,
  and every name where `es_systems.cfg` could not be read;
  `tools/last-good-scripts-test`, first run at S7, failed three
  `cloud_content_backup` checks, and `c3e260861b` narrowed the check to
  explicit names (the shape always, the declared systems when the file
  reads; 1,379 PASS lines). The plan § 6b now carries the stream practice:
  a stream that changes a covered script runs the suite before its commit.
- **The second window's match refusal** planned `snes|sync|1|10`, saw two
  ROMs added, refused with `previewed sync|1, now sync|3`, and removed
  nothing; **`atomic()`'s mode** read 0600 on a real save and under the
  image's python, including over a 0644 file.

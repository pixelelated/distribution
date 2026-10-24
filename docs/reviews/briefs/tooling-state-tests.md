# Brief: M6.P2 T14, the last-good, settings and state tests (#661)

A session with no other context runs this brief start to finish. It is the
unit of handoff the plan defines (`docs/reviews/plan-for-the-plan.md` § 7);
read that document whole before the first command, then this brief whole.
Every section below is mandatory; a section that does not apply says so and
why. Where this brief and the checklist on #661 differ, #661 wins and the
coordinator corrects the brief in the same session. **Version 1
(2026-10-24):** written after T10 (#657, the guards) was accepted at
`afdce9a65b` and while T12 (#659, the VM harness) runs in the other lane;
the tooling area's futro (`docs/futros/2026-10-24-m6-tooling-and-guards.md`,
posted on #903) carries this slice's kickoff addendum. Every figure below was
produced by a command on the tree at `8ebaf8daad`, on P1's tip `2174265e9c`
for the inventory and the ten lint fixtures that live only there, or on this
host today, and says which; a stranger's proof precedes the dispatch and
version 2 records what it found. **Each command block sets its own
variables** (`D`): a Bash call in this harness starts a fresh shell. **This
is a read of the fork's state tests through the lens the order gives it,
brittleness**: twenty-one test tools and eleven fixture files that prove the
OS scripts, the cloud layout, the settings writers, the release identity and
the hardware quirks with synthetic roots, busybox applets, real rclone and,
for two of them, a guest -- and the question of the slice is what each test
depends on that is not the thing it proves (a build root's applets, a
guest's image, a host path, a fixture's bytes, the order of a dictionary),
what each would miss, which ones nobody runs, and which have been retired in
place. **Nothing here builds, flashes, touches a handheld or a person's
cloud, or starts a guest the host file has not been told about**; the
host-side tests run in the lane's worktree with their own fixtures, and one
bounded guest cycle is authorized in § 5 for the two tests that need one, if
a claim needs it.

## 1. Identity

- **Issue:** #661 `M6.P2 E903/T14: tooling-and-guards: the last-good,
  settings and state tests`, slice `tooling-state-tests` (`k: 14`) in
  `docs/reviews/slices.json`, fourteenth in `docs/reviews/order.md` (its row:
  *32 | 6,911 | 6,807 (6,807) | 0 | Independent*; its `why`: *the
  `pixelelated-*`/`rasteratops-*` test family, the settings, wait-lock and
  upgrade tests, and their fixtures; read before the code it proves under
  D-WORKFLOW-186*). **Epic:** #903 (the tooling and guards: T9 and T10
  accepted, T12 running, then this slice, T15 #662, T45 #692). **Milestone:**
  M6; its body holds the live order; read it first. **Predecessors:** #346
  (the plan), #641 (the survey, closed; its lint fixtures are this slice's
  ten Markdown files), **T10 #657** (accepted: `lint-audit-artifacts`'s
  fixtures gained `run.sh` and a third fixture on its branch, `#945`; the
  fork CI runs `rocknix-info-test` at `fork-checks.yml:49-50`; its retro's
  five fail-open shapes are this slice's first checklist), **T9 #656**
  (accepted: `test-build-admission` and its siblings are the model of a
  control with constructed positives), **T8 #655** and **T12 #659** (the
  recorded guest cycles, if one is needed here), **T15 #662** (not yet
  dispatched: `tools/last-good-scripts-test`, 14,238 lines, the one-file
  slice that **calls four of this slice's tools** -- `wait-lock-test`,
  `rasteratops-cloud-layout-test`, `settings-modes-test`,
  `melonds-upgrade-test` -- and is itself what `vm-qa`'s `scripts` suite
  runs; this slice reads those four as T15's callees and never edits T15's
  file). **Beside it:** T12.
- **The division of labour (D-WORKFLOW-189).** This lane executes. It does
  not re-cut the slice, change a criterion, write a brief, move the M6 body,
  edit `slices.json`, `areas.json`, `order.md` or the plan, file a Backlog
  issue, edit a rule or a decided register row, or decide a question of
  scope: those are the coordinator's, reached through #661, one question at
  a time. What it does file: its own audit punch-list issue (stage D) and a
  `bug` issue for every defect it finds (D-WORKFLOW-187). Nothing else.
- **One worktree, one session.** Branch `feature/m6-tooling-state-tests-661`
  at `/workspace/repos/pixelelated/distribution.worktrees/m6-tooling-state-tests-661`,
  created by the coordinator, **stacked on `feature/m6-p1-survey-641` at
  `2174265e9c`** with the coordinator's tip merged in and the lane's pointer
  seeded (the hashes are in the dispatch comment on #661). **Before that
  comment exists nothing runs in it.** The session is the T3 lane's
  (`m6-t3-emulators`), which ran T3, T30, T24, T4 and T10; those worktrees
  stay beside this one, idle, until their merges, and nothing is written
  there. The primary checkout `/workspace/repos/pixelelated/distribution`
  stays on `next` (D-INFRA-025); the legacy checkout and `rocknix.worktrees/*`
  are the M7 lane's, read only. **The rules in this worktree are `next`'s
  except the paths the dispatch comment lists.**
- **Model and effort:** Opus 5.5 (the maintainer, 2026-10-22: *"the work
  will be Opus 5.5"*) at high effort. Record what ran in `00-running-log.md`'s
  header.
- **Review depth: Independent** (plan § 6c, `slices.json` k 14: *an ordinary
  code slice*): one reviewer from another lab through the Facilitator
  (`tools/council/run invoke --member gpt --provider openrouter`): **GPT-6
  Astra at `max`**, a probe first (identity, effort, provider from the
  provider's own field), then one refutation pass over one packet, as T9's
  and T12's Phase 4.6 did (T9's `second-opinions/` on
  `feature/m6-tooling-build-supervision-656` is the model). `npm install
  --prefix tools/council`, `verify-pins` and `test` first; the key is
  `~/.config/council/env`, sourced by `run`, never read into a transcript. **A
  failed seat is a hold**, never a self-grading; a seat cut by its output
  ceiling re-runs on a trimmed packet (D-WORKFLOW-195). The packet is the
  slice's 32 files, **396,588 bytes (387 KiB) at the read refs**, plus, as
  read-only context, `engineering-practices.md` § Guards must fail closed and
  `upgrade-and-install.md` § Verify on a device, not on the host (what the
  tests promise). The packet is scanned with `tools/forbidden-terms-check
  --stdin` and the pre-commit's patterns before it is sent (T10's rule; two
  of these tools carry credential-shaped fixture literals at the hash -- see
  § 2 -- and the scan is what decides whether the packet may carry them, or
  must redact them as PL-012 says). `review-plan.json` records depth
  `independent`, scope `epic`, primary `anthropic/claude-opus-5-5` / lab
  `anthropic`, one reviewer `gpt` (`openai/gpt-6-astra`, `openai`, `max`),
  provider `openrouter`, `allow_fallbacks: false`.
- **The host, read on 2026-10-24 by the coordinator:** M6's since M7's 17:09
  return; census qemu 0 after T12's cycle ended at 19:30. The newest
  GENERIC_X64 image present is the M6 lanes' copy of the `069fc2704421`
  build under `/workspace/artifacts/m6-t1-20261023/` (its `.img.gz.sha256`
  beside it; the `.identity.json` carries no digest), the one T12 booted;
  T12's cycle record (`docs/audits/2026_10_24-epic-m6-tooling-vm-harness/`
  on `feature/m6-tooling-vm-harness-659`, `00` § The guest cycle) is the
  shape this slice follows if § 5's cycle is needed. **No build root is
  expected on this host for this slice's busybox applets**: `settings-modes-test`
  and `melonds-upgrade-test` take candidate applets from a build root when
  one exists and say so when none does; the lane records which it had.

First commands:

```bash
D=/workspace/repos/pixelelated/distribution.worktrees/m6-tooling-state-tests-661
cd "$D"
git fetch origin && git fetch upstream --no-tags
git branch --show-current                                            # feature/m6-tooling-state-tests-661
git merge-base --is-ancestor 2174265e9c HEAD || echo "not stacked on the P1 tip: stop"
test -f docs/reviews/inventory.json || echo "no inventory.json: this is not the lane's worktree (stacked on P1): stop"
git diff --stat next -- .claude CLAUDE.md AGENTS.md tools/lint-audit-artifacts   # exactly the paths the dispatch comment lists, nothing else
cat .github/sessions/saved-session-state-feature-m6-tooling-state-tests-661.md
tail -3 /tmp/m7-m6-host-coordination-20261023.txt | cut -c1-200; pgrep -c -x qemu-system-x86   # the host file's last lines and the census, before anything
df -i /tmp | tail -1                                                 # never export a tree under /tmp
ls -d /workspace/repos/pixelelated/distribution.worktrees/*/build.* 2>/dev/null | head -3   # a build root for the busybox applets, if any (none expected)
"$D/tools/rules-check" --quiet; echo "rc=$?"; "$D/tools/register-check" | tail -1
git push -u origin feature/m6-tooling-state-tests-661
```

## 2. Scope

**32 paths, 6,911 lines (the inventory's column and the read refs agree);
all 32 fork-own; 20 Python, 2 shell, 10 Markdown; reach `n/a` 32; 396,588
bytes at the read refs (394,711 for the 22 at the hash).** The membership
is the inventory's at P1's `2174265e9c` with the slice's rule (`k: 14`): the
area `tooling-and-guards` and two globs,
`tools/{settings-modes-test,melonds-upgrade-test,wait-lock-test,pixelelated-*,rasteratops-*,build-identity-test,rocknix-info-test,usb-gadget-test,nova-led-test,retroarch-wrapper-test}`
and `tools/test-fixtures/**`. **The brace glob is written out as names**
(T10's and T12's briefs met the naive glob-to-regex). The re-derivation, in
the lane's worktree:

```bash
python3 -I - <<'PY'
import json, collections, os, fnmatch
inv = json.load(open("docs/reviews/inventory.json")); cols = inv["columns"]
rows = [dict(zip(cols, r)) for r in inv["rows"]]
names = "settings-modes-test,melonds-upgrade-test,wait-lock-test,pixelelated-*,rasteratops-*,build-identity-test,rocknix-info-test,usb-gadget-test,nova-led-test,retroarch-wrapper-test".split(",")
def sel(p):
    if p.startswith("tools/test-fixtures/"): return True
    if not p.startswith("tools/"): return False
    rest = p[6:]
    return "/" not in rest and any(fnmatch.fnmatchcase(rest, n) for n in names)
t14 = [r for r in rows if r["tree"] == "distribution" and r["area"] == "tooling-and-guards" and sel(r["path"])]
print("paths", len(t14), "lines", sum(r["lines"] or 0 for r in t14), dict(collections.Counter(r["tier"] for r in t14)), dict(collections.Counter(r["reach"] for r in t14)), dict(collections.Counter(r["language"] for r in t14)))
print("the globs also select, in other areas:", sum(1 for r in rows if r["tree"] == "distribution" and sel(r["path"]) and r["area"] != "tooling-and-guards"), "paths (expect 0)")
os.makedirs(".qa-scratch/t14", exist_ok=True)
open(".qa-scratch/t14/paths.txt", "w").write("".join(r["path"] + "\n" for r in sorted(t14, key=lambda r: r["path"])))
PY
wc -l < .qa-scratch/t14/paths.txt                                                                        # 32
while IFS= read -r p; do case "$p" in tools/test-fixtures/lint-audit-artifacts/*) r=2174265e9c;; *) r=8ebaf8daad;; esac; printf '%6d %s\n' "$(git show $r:"$p" | wc -l)" "$p"; done < .qa-scratch/t14/paths.txt | awk '{s+=$1; print} END {print s " lines"}'   # 6911
```

Recorded (2026-10-24; the 21 tools by size; the last fork commit from
`git log -1 --format='%h %ad' --date=short 8ebaf8daad -- <path>`; *who runs
it* from `git grep -l -F <name> 8ebaf8daad -- tools .github/workflows
.claude/skills`, the rules' index and list entries not counted):

| Lines | Path | Last fork commit | What it is | Who runs it |
| ---: | --- | --- | --- | --- |
| 1,224 | `tools/rasteratops-cloud-layout-test` | `083f4fad86` 2026-10-08 | production cloud scripts against isolated real rclone filesystems (#365): numbered layout transitions, partial-state recovery, missing-remote refusal | `last-good-scripts-test` (`--cloud-layout`, `:252`, `:14188`); `pixelelated-cloud-validator-test`, `-content-scope-test`, `-save-layout-test` |
| 909 | `tools/pixelelated-state-check` | `8794630e8f` 2026-10-15 | inspect selected image, default and first-boot state without disclosing values (#565): the release preparer's selected-state inspection | `fork-publish-release`; its own test |
| 783 | `tools/pixelelated-state-check-test` | `8794630e8f` 2026-10-15 | disposable #565 controls: clean and contaminated roots and payloads, no imports of the gate, providers or real accounts | nobody |
| 724 | `tools/pixelelated-vm-cloud-boundaries` | `083f4fad86` 2026-10-08 | installed-image cloud boundaries and real pair recovery (#356/#365): **a guest, two for the pair** | nobody |
| 409 | `tools/pixelelated-save-layout-test` | `bc4ae05d30` 2026-10-08 | source-bound real-rclone controls for standalone progress coverage (#520) | nobody |
| 402 | `tools/rasteratops-vm-cloud-epic` | `bc2dceb406` 2026-10-11 | the cloud epic's guest-d proof, promoted from run 101 (#365): **a guest and the synthetic WebDAV**; cases A to L, T08 to T26 | T12's `vm-walks/cloud-epic/migration-protocol.sh` (which refuses on today's image: `cloud_migrate_layout` is retired) |
| 361 | `tools/pixelelated-duckstation-capture-test` | `bc4ae05d30` 2026-10-08 | actual DuckStation launchers and configs in isolated host fixtures (#521) | nobody |
| 359 | `tools/pixelelated-cloud-validator-test` | `bc4ae05d30` 2026-10-08 | real local-rclone controls for bounded category validation (#508/#510) | the two retired stubs |
| 256 | `tools/pixelelated-content-scope-test` | `083f4fad86` 2026-10-08 | selected-library boundaries with production scripts and real rclone | nobody |
| 226 | `tools/retroarch-wrapper-test` | `8f2803a080` 2026-09-24 | does the threaded video wrapper run a posted command exactly once | `vm-qa` (the `wrapper` suite, on every default run) |
| 183 | `tools/build-identity-test` | `40bc5469b9` 2026-10-11 | actual assembly identity blocks and offline release planning (#532) | nobody |
| 159 | `tools/wait-lock-test` | `f13cf9f001` 2026-09-09 | a device-less check of `wait_lock()` in `001-functions`, the settings lock every `get_setting`/`set_setting`, `runemu.sh`, `backuptool` and the cloud scripts take | `cloud-round-trip`; `last-good-scripts-test` (`:148`, `:8608`: it lifts the functions the same way) |
| 157 | `tools/rasteratops-identity-check` | `7d64713537` 2026-10-04 | 0.0.1 identity inputs and retained RC2 contracts in source and an image (#337, #383) | nobody |
| 147 | `tools/usb-gadget-test` | `6f1d138adb` 2026-10-11 | actual USB preparation functions in a disposable configfs fixture (#531; D-WORKFLOW-160's `bcdDevice`) | nobody |
| 125 | `tools/melonds-upgrade-test` | `7f58b7b1c5` 2026-10-08 | the actual post-update function with owned paths and candidate busybox applets (#526); an older post-update as the negative control | `last-good-scripts-test` (`:14231`) |
| 107 | `tools/rasteratops-candidate-store` | `3d7c075f63` 2026-10-02 | keep a candidate bundle by manifest digest, without overwriting it (#344) | `fork-publish-release` |
| 68 | `tools/nova-led-test` | `a3d617ff54` 2026-10-03 | the real Nova LED scripts with only profile, path and service boundaries adapted (#332) | nobody |
| 60 | `tools/rocknix-info-test` | `3fcff2e1e2` 2026-10-11 | optional hardware reporting with complete-script filesystem fixtures | **the fork CI** (`fork-checks.yml:49-50`) |
| 44 | `tools/settings-modes-test` | `ff249d2172` 2026-10-04 | real shell writer functions, scratch paths, candidate busybox applets (#421) | `last-good-scripts-test` (`:14224`) |
| 30 | `tools/pixelelated-cloud-folder-vm-test` | `2cc6ce30e3` 2026-10-08 | **retired** historical folder-overlay control (#524 PL-002): refuses execution | nobody (by design) |
| 29 | `tools/pixelelated-cloud-folder-test` | `2cc6ce30e3` 2026-10-08 | **retired** historical folder-contract control (#524 PL-002): refuses execution | nobody (by design) |

**And the eleven fixture files:** `tools/test-fixtures/cloud_connections_fixture.py`
(at the hash; `cloud-connections-test`'s staged connection fixture, #537/#540
-- the test itself is the cloud area's) and the **ten Markdown files of the
lint's two fixtures**, `tools/test-fixtures/lint-audit-artifacts/fixture-epic-m6-renovation-{pass,fail}/0{1..5}-*.md`
(**on P1's tip `2174265e9c` only**; absent at `8ebaf8daad`; written with
`fc88815ccb`, 2026-10-22, #641; T10's #945 adds `run.sh` and a third fixture
beside them on T10's branch, which this lane reads as a delta, not a member).

**Provenance.** None of the 32 is on `upstream/next` (`git cat-file -e
upstream/next:<path>` fails for every one). `git log --format=%h
c445081a59..8ebaf8daad -- <the 22 at the hash> | wc -l` is **35** fork
commits since the base (35 without merges); counting every occurrence, their
messages cite #383 (8 times), #565 (6), #471 (5), #532, #409 and #365 (3
each), #98, #510, #508 and #479 (2 each) -- the family's own record is #365
(the cloud epic's proofs), #421 and #526 (the settings and melonDS writers),
#508/#510/#520/#521/#524 (the cloud-folder contracts and their retirement),
#531/#532 (the USB gadget and the build identity), #565 (the state check),
#337/#383 (the identity). **No blindspot entry names any of the 21** (a
register grep over every entry; the value side of this slice's lens is
therefore the tests' own records -- their issues and the work logs -- not the
blindspot register), and three decision rows do: D-CLOUD-074 (the cloud
scripts' sentinels `wait-lock-test` exercises), D-WORKFLOW-159 (the versioning
`build-identity-test` proves), D-WORKFLOW-160 (the `bcdDevice`
`usb-gadget-test` proves).

**Who runs what, in one list.** On every default `vm-qa` run:
`retroarch-wrapper-test` (the `wrapper` suite) and, through T15's
`last-good-scripts-test` (the `scripts` suite, 13 minutes of the 33 by
T12's cost table), `wait-lock-test`'s lifted functions, `settings-modes-test`,
`melonds-upgrade-test` and `rasteratops-cloud-layout-test`. In the fork CI:
`rocknix-info-test`. From the release preparer: `pixelelated-state-check`
and `rasteratops-candidate-store`. From `cloud-round-trip`: `wait-lock-test`.
From T12's protocol walk: `rasteratops-vm-cloud-epic` (which refuses today).
**Eleven tools nobody runs**: `build-identity-test`, `nova-led-test`,
`pixelelated-content-scope-test`, `pixelelated-duckstation-capture-test`,
`pixelelated-save-layout-test`, `pixelelated-state-check-test`,
`pixelelated-vm-cloud-boundaries`, `rasteratops-identity-check`,
`usb-gadget-test`, and the two retired stubs (by design). The lane confirms
each from the record (a tool run once for a candidate and recorded in a
`docs/qa-logs/` folder has a caller in the record, not in the tree; both
count, and the Q6 table says which).

**Two fixture literals at the hash.** T10's S3 (#935, #962) found that the
widened credential patterns match `tools/last-good-scripts-test:8004` (T15's
file) and `tools/cloud-connections-test:37` (the cloud area's); **neither is
in this slice**, but the same read applies to every fixture here: a
credential-shaped value in a test is built at run time from `printf` pieces
(blindspot 67; `engineering-practices.md` § Guards must fail closed), and a
fixture file that carries one at rest is a Q2 finding and a `bug`. The packet
scan (§ 1) is the mechanical check.

**The hash.** The 22 at-hash files are read at `8ebaf8daad`'s bytes and the
ten lint fixtures at `2174265e9c`'s, both from the exports
(`.qa-scratch/t14/at-hash/`, `.qa-scratch/t14/at-p1/`); `reviewed-at:` is
the branch `HEAD` at stage A and names both hashes. The lane's branch differs
from the hash on **none of the 22** and from P1's tip on none of the ten
(`tr '\n' '\0' < .qa-scratch/t14/paths.txt | grep -zv test-fixtures/lint |
xargs -0 git diff --stat 8ebaf8daad HEAD --` is empty; a non-empty result is
the first lead). Off this branch, T10's #945 changes
`tools/test-fixtures/lint-audit-artifacts/` (a `run.sh` and a third fixture
directory): read as a delta, named by commit, when the lint's fixtures are
the question.

**The policy on change (plan § 5; D-WORKFLOW-187):** a defect here is the
fork's alone and is fixed under a stream brief at stage E, never at stage B;
a stream on a test adds the case that fails on the unfixed test (a test's
own positive control: the thing it claims to catch, constructed, caught);
a stream on a tool a release gate calls (`pixelelated-state-check`,
`rasteratops-candidate-store`, `build-identity-test`, `rasteratops-identity-check`)
is read against `release-candidates.md` and D-WORKFLOW-157/159/168 first and
changes no gate's contract (a lead for the coordinator); a retired stub
(`pixelelated-cloud-folder-test`, `-vm-test`) is a Q6 row with a disposition
for the coordinator (keep as a refusing marker, or remove with its index row
and list entry), not a stream; **T15's `last-good-scripts-test` is never
edited here** (its slice follows this one; a finding about how it calls a
tool of this slice is posted on #662 by the coordinator). **Brittleness is
the lens, not a licence to delete**: a test with no caller and no recorded
catch is reported with what it depends on and what it would catch, and the
coordinator decides its fate with the maintainer.

## 3. Read first

- **The rules the work touches**, from `next`, this session
  (`working-principles.md` § Pre-flight): `engineering-practices.md` (§
  Guards must fail closed: *a fixture for a secret scanner is built at run
  time*, *success reported over a no-op*, *a suite is not wired in until it
  has been seen to FAIL once*; § Verify the artifact, not the report; § A
  failure you find is yours to fix), `upgrade-and-install.md` (§ Verify on a
  device, not on the host: the busybox-applet rule `settings-modes-test` and
  `melonds-upgrade-test` live by; § Every fix answers what was already
  written), `generic-x64-vm-testing.md` (the two guest tests; *what the
  guest's busybox lacks*), `rclone-cloud-sync.md` (the cloud tests' subject:
  the filter file, `--delete-excluded`, the layout), `release-candidates.md`
  (the state check and the candidate store as release gates;
  `fork-publish-release --prepare`), `device-builds.md` (§ Build credentials,
  § Publishing: D-WORKFLOW-157/159, the identity blocks `build-identity-test`
  proves), `vm-first.md`, `decision-register.md`, `learning-capture.md`.
- **The registers for the scope:** D-CLOUD-074 (the sentinels), D-CLOUD-078
  (the last known good state is a record kept on purpose: the shape
  `settings-modes-test` proves), D-CLOUD-175/178/179 (the folder contracts
  the two retired stubs served, retired by #508/#510), D-WORKFLOW-157/159/160
  (identity, versioning, `bcdDevice`), D-WORKFLOW-166/168 (the shared
  developer identity and the private-owner images `pixelelated-state-check`
  inspects for), D-INFRA-006/007 (credentials in a build), D-QA-058 (the
  local cloud baseline the rclone tests use), D-QA-044 (agent-first
  criteria), D-WORKFLOW-187/189/190. **Blindspots:** none names these tools;
  the class entries 8, 13, 14, 22, 34 (the guest's busybox), 39 (a PASS over
  missing numbers), 67 (a credential-shaped fixture), 76.
- **T10's five fail-open shapes** (its retro, 2026-10-24): a fixed `--limit`
  read as the whole set; a regular expression that takes a heading for an
  answer; a count compared where a set was meant; a `\b` after punctuation;
  a two-space key where records use one -- plus T10's S9 lesson, **a control
  that ends `|| true` cannot fail**: `grep -n '|| true'` over the 21 is a
  stage-A read. And T9's: a control isolated by `.git`, by `HOME` or by the
  current tool's bytes depends on the old location when state moves.
- **The guards' recorded positives** (`engineering-practices.md` § The
  positive is recorded where the guard is wired): `wait-lock-test`'s (#98,
  2026-09-09); `settings-modes-test`'s #421 run (2026-10-04);
  `melonds-upgrade-test`'s #526 negative control (2026-10-08);
  `retroarch-wrapper-test`'s first FAIL (audit #258 P-02, 2026-09-24);
  `rocknix-info-test`'s quirk failure controls (#471); `usb-gadget-test`'s
  old/new metadata cases (#531); `build-identity-test`'s tamper controls
  (#532); `pixelelated-state-check-test`'s contaminated roots (#565);
  `nova-led-test`'s battery writer (#332); the cloud tests' refusal cases
  (#365, #508, #510, #520, #521). A test whose positive the lane cannot find
  in the record is a Q6 row saying so.
- **The evidence folders**: `docs/qa-logs/2026-10-04-*` (the settings
  modes), `2026-10-08-*` (the cloud-folder retirement and the save layout),
  `2026-10-11-*` (the USB gadget, the identity), `2026-10-15-*` (the state
  check); T9's `02` (the model of a control table); T12's `04` § Q5 (the 13
  minutes `scripts` costs every run).
- **The stranger's proof of this brief** (version 2's errata).

## 4. The questions

All seven apply (plan § 4); **the lens is brittleness, so Q6 (what each
test depends on that is not the thing it proves; what it has caught; who
runs it) and Q3 (a test that passes without proving) carry the slice**, Q2
the fail-closed shapes, Q7 the three descriptions of each tool (its header,
the rule that names it, the index row) against the code.

| Q | What is asked of these 32 | Where the answer lands |
| --- | --- | --- |
| Q1 Modernize | A test that reads a layout the tree has retired (`rocknix.worktrees`, a legacy build root, `/tmp` roots: #640's rows); a test bound to a tool version the host no longer has (rclone, QEMU, Python 3.14's changes); a retired stub kept in place (the two `pixelelated-cloud-folder*` files: what they refuse, and whether the index still sells them as tests) | the rows; #640 named, not changed |
| Q2 Standards | Fail-closed shapes: a count asserted, a missing input a FAIL not a skip, `pipefail`, every expansion quoted, exits defined where named, `assert` statements (which `python3 -O` removes: T9's F-13 shape) counted per tool, no `|| true`, no credential-shaped literal at rest, no write outside the test's own temp root, no dependence on a dictionary's order or on the host's `HOME` | a finding per violation, with the line |
| Q3 Bugs | **A test that can pass without proving**: a case whose rc 0 does not depend on the thing it checks (an `--only` that matches nothing and passes, as T12 found in `emulator-exit-test`; a fixture copied from the current tool so the test cannot see a regression, as T9 found in the #597 recovery fixture; a negative control that fails for an unrelated reason); a test whose applets fall back to the host's when the build root is absent and still say PASS (the busybox rule, blindspot 34); a cloud test whose rclone backend is the host's real config rather than its isolated one | a `bug` per defect, `Already written:` and the VM line, its fix under a stream with a case |
| Q4 Currency | Not a package slice. The row is the rclone, busybox and Python the tests assume against the host's and the image's (`rclone version`, the image's busybox applet list from a build root if one exists, `python3 --version`), and the ES, DuckStation and melonDS versions the fixtures encode against the pins | one table |
| Q5 Efficiency | What each test costs: its wall time on this host (run once each at stage A, the host-side ones; the two guest tests from the record or the one cycle), its temp footprint, and what `last-good-scripts-test` pays for calling four of them on every `vm-qa` run (T12's 13 minutes: how much is theirs) | the figures with their source |
| Q6 Dead ends and brittleness | **The brittleness table**: for each of the 21, (a) what it depends on that is not the thing it proves -- a build root's applets, a guest, a real rclone binary, a host path, a fixture's bytes, a tool's own current source -- and what happens when that is absent (skip, fail, or a false pass); (b) its last recorded catch (the issue, the qa-log folder, the date) or `nothing recorded`; (c) its caller (`vm-qa` through T15, the CI, the release preparer, another test, a walk) or `nobody`; (d) its positive control, named, or `none`. The eleven no-caller tools confirmed or refuted from the record; the two retired stubs' disposition proposed | the table in `04` § Q6, every row sourced |
| Q7 Clarity | The three descriptions of each tool (its header, the rule that names it, `instruction-files.md`'s index row) against the code: a header that promises a device-less proof the code does not keep is a Q3 bug if it hides a failure and a Q7 row otherwise; the index rows for the two retired stubs (which say *refuses execution*) against what they do | the rows; a drift in a rule is a lead for the coordinator |

## 5. The evidence floor

The code-auditor skill's rules apply to every verdict (`SKILL.md` § Evidence
floor):

1. Tracker state is never sole evidence: every verdict cites the tree
   (`git grep`, `git log`), a test's run with its exit, a recorded report
   (`docs/qa-logs/`), or a guest cycle's own record.
2. Mechanical evidence outranks reading: a test's behaviour is its run and
   its exit, not the docstring above it.
3. **The bench is the host and, if a claim needs it, one bounded guest
   cycle.** The host-side tests run in the lane's worktree with their own
   fixtures and temp roots; the real-rclone tests run against
   `tools/cloud-test-backend`'s local backends or their own isolated
   filesystems (D-QA-058), **never a real provider or a real account**; a
   GENERIC_X64 guest is the bench for `pixelelated-vm-cloud-boundaries`
   and `rasteratops-vm-cloud-epic` only, and **one cycle is authorized**
   under T12's ritual: the `069fc2704421` image copied under
   `/workspace/tmp/m6-t14/` and checked against its `.img.gz.sha256`, the
   host file line before (`== M6 T14 lane (#661) -- <UTC>: census qemu N; one
   GENERIC_X64 guest from <image>, pidfile /workspace/tmp/m6-t14/qemu.pid,
   <what runs>`), the pidfile, `tools/vm-stop` to end it, the census after,
   the host file line after, the disk retired after its record (D-INFRA-022),
   and an entry in `docs/vm-qa-log.md`. **A second cycle needs a line on
   #661 first.** A test that needs a build root's busybox applets and finds
   none records the fallback it took, and a PASS under the host's applets is
   a PASS of the host, said so in `02` (blindspot 34).
4. **What result would have produced a FAIL** is asked of every PASS, in
   writing, in `02`.

**The host-side runs, with what the coordinator read on 2026-10-24** (the
lane runs each at stage A in its worktree and records the exit and the wall
time; a test that fails is a finding; a test that needs what the host lacks
records it as `CANNOT`, never as a pass):

```bash
D=/workspace/repos/pixelelated/distribution.worktrees/m6-tooling-state-tests-661
cd "$D"
for t in wait-lock-test settings-modes-test melonds-upgrade-test retroarch-wrapper-test rocknix-info-test usb-gadget-test nova-led-test build-identity-test rasteratops-identity-check pixelelated-state-check-test pixelelated-duckstation-capture-test; do s=$(date +%s); timeout 900 tools/$t > .qa-scratch/t14/$t.out 2>&1; echo "$t rc=$? $(( $(date +%s) - s ))s $(tail -1 .qa-scratch/t14/$t.out | cut -c1-80)"; done   # read each header first: an argument it needs (a build root, --profile) is given from the tree, never guessed
for t in rasteratops-cloud-layout-test pixelelated-cloud-validator-test pixelelated-content-scope-test pixelelated-save-layout-test; do tools/$t --help 2>&1 | head -4; done   # the real-rclone four: read what backend each binds before running it against tools/cloud-test-backend's local one
tools/pixelelated-cloud-folder-test 2>&1 | head -3; echo "rc=$?"; tools/pixelelated-cloud-folder-vm-test 2>&1 | head -3; echo "rc=$?"   # the two retired stubs: they refuse; the refusal text and rc recorded
tools/rasteratops-candidate-store --help 2>&1 | head -4; tools/pixelelated-state-check --help 2>&1 | head -4   # the release preparer's two: modes only, nothing stored or inspected for real
tools/pixelelated-vm-cloud-boundaries --help 2>&1 | head -4; tools/rasteratops-vm-cloud-epic 2>&1 | head -4   # the two guest tests: their usage, nothing started
grep -n '|| true' $(grep -v test-fixtures .qa-scratch/t14/paths.txt | tr '\n' ' ') | cut -c1-120   # T10's lesson: a control that cannot fail
grep -cE '^\s*assert ' $(grep -v test-fixtures .qa-scratch/t14/paths.txt | tr '\n' ' ') | grep -v ':0$'   # T9's F-13 shape: asserts python3 -O removes
grep -nE '/tmp/|HOME|rocknix\.worktrees|/workspace/repos/rocknix' $(grep -v test-fixtures .qa-scratch/t14/paths.txt | tr '\n' ' ') | cut -c1-120 | head -40   # Q1/Q2: host paths and roots
```

**The reading, per file:** every test matched to what it depends on, what
it caught, who runs it and its positive (Q6's table); the real-rclone four
read for which backend they bind and whether a host `rclone.conf` could leak
in; the two guest tests read for how they find, wait for and stop their
guest (pidfile and owned disk, or pattern: T9's and T12's finding, every one
guest-side so far); the release preparer's two read against the gates they
serve; T15's four call sites read (never edited) for what `last-good-scripts-test`
assumes of them; the two retired stubs' refusals; the three descriptions per
tool (Q7).

**The seat (Phase 4.6, one seat):** `npm install --prefix tools/council`,
`tools/council/run verify-pins`, `tools/council/run test`; the packet
(`gpt-brief.md`: the 32 files and the two rule sections; `packet-manifest.json`
with the sha256 of each) **scanned before it is sent** (`tools/forbidden-terms-check
--stdin` 0 hits; the pre-commit's patterns 0 lines -- a hit here is a
finding and the packet redacts it as PL-012 says); the probe (`gpt-probe.md`
with its `.provenance.json`); the refutation (`gpt-audit.md` with its
`.provenance.json`), the seat asked first for the four real-rclone tests'
isolation, the two guest tests' guest handling, `pixelelated-state-check`'s
non-disclosure and the busybox fallback of the two writer tests; each item
graded in `04` § Second opinion with the artifact that decided it; a seat cut
by its ceiling re-runs on a trimmed packet (D-WORKFLOW-195). The call runs
plainly with a harness waiter.

## 6. Outputs

All in the worktree, committed on its branch with messages that cite `#661`
(`Refs #661`, never a closing keyword); the stage letters are plan § 6b's.

| Output | Path | Shape | Stage |
| --- | --- | --- | --- |
| Running log | `docs/audits/<yyyy_mm_dd>-epic-m6-tooling-state-tests/00-running-log.md` | the flight recorder: the model and effort, `reviewed-at` with `8ebaf8daad` and `2174265e9c` beside it, the host file's last line and the census before each run, every § 5 command with its exit status and wall time, every `PROOF:` line, the guest cycle's lines if one ran, each time from `date -u` | A onward |
| Research notes | `.../01-research-notes.md` | § Scope: the 32 re-derived with § 2's block and its output, the provenance (35 fork commits, none upstream, ten files on P1 only), the branch's diff from the hash (empty) and T10's #945 delta named; § Phase 1: what each test proves and depends on, in the slice's words, and the stage-A runs with exits | A, B |
| Forward audit | `.../02-forward-audit.md` | Phase 2 over #661's checklist, plus **a coverage table with one row per path under its own `## Coverage` heading** (32; the first cell the path in backticks), § Mechanical checks, § The runs (each test's run, exit, wall time, *a FAIL would mean ...*, and the fallback it took if any), § The guest cycle (the record, or that none was needed and why), § T15's call sites (read, not edited); every proof with a `proved:` cell | B, then F |
| Retrospective | `.../03-retrospective.md` | Phase 3 with § 3.5 for the seams: the four tests x T15's `last-good-scripts-test` x `vm-qa`'s `scripts` suite; the real-rclone four x `cloud-test-backend` x the host's `rclone.conf`; the release preparer's two x `release-candidates.md`'s gates; the guest two x T12's harness; the writer tests x the busybox rule x a build root's presence | B |
| Analysis | `.../04-analysis.md` | Phase 4, § Finding Verification (4.5), § Second opinion (4.6), **§ Renovation face** Q1 to Q7, **Q6 carrying the brittleness table** (every test with its dependencies and their failure mode, its last catch or `nothing recorded`, its caller or `nobody`, its positive or `none`; the eleven no-caller tools confirmed or refuted; the two stubs' proposed disposition), Q5 the cost figures | C |
| Second opinions | `.../second-opinions/` | `review-plan.json` (independent; `gpt` at `max`), the brief, `packet-manifest.json`, the probe prompt, the probe and the refutation with their `.provenance.json` | C |
| Lint, before D | `tools/lint-audit-artifacts <folder> --phase pre-issue` | `PASS pre-issue artifacts (...)` with `review plan: independent, 2 model perspectives, 1 verified external calls` | C |
| Punch list | `.../05-punch-list.md` | Phase 5: every item with `question:`, severity, category, where (file:line at the hash), acceptance, `Already written:` and the VM line; the YAML `punch_index`; a no-caller test or a retired stub as a `Renovation` item with the coordinator's disposition pending | D |
| Audit issue | GitHub, labels `audit`, `punch-list`, milestone M6, a sub-issue of #661 | `Audit: M6 T14 the state tests -- N findings (...)`; one checkbox per item, agent-first | D |
| Bugs | GitHub, label `bug`, milestone M6 | one per defect, with its code trace, `Already written:`, the VM line and the case that will prove the fix; no bug body quotes a credential-shaped value | D |
| Streams | the coordinator's brief `docs/reviews/briefs/t14-streams.md` | one per fix the coordinator briefs at the stage-D pause | E |
| Retro | `docs/retros/<date>-m6-tooling-state-tests.md`, posted on #661 | the mini-retro, Instruction-Recommendations mode; what the slice did to the two time-to-play numbers (nothing); what each stream did to a test's refusals | G |

## 7. Acceptance

The checklist on #661 becomes this section at dispatch, written there by the
coordinator in place of P1's five generated ones (until then #661 carries
those five). Every checkbox names the artifact that ticks it (D-QA-044); the
coordinator ticks at acceptance, from the artifacts, never from the
hand-back's words.

- [ ] `docs/audits/<date>-epic-m6-tooling-state-tests/` holds `00-running-log.md` and `01-research-notes.md` to `05-punch-list.md`.
- [ ] `tools/lint-audit-artifacts docs/audits/<date>-epic-m6-tooling-state-tests/` prints `PASS` (its default `resolution` phase, at close; before stage D the same command with `--phase pre-issue` prints `PASS pre-issue artifacts`), the renovation face included: Q1 to Q7 answered in `04-analysis.md`, and every punch item's `question:` in the index.
- [ ] `second-opinions/review-plan.json` records `depth: independent`, one reviewer (`gpt`, `openai/gpt-6-astra`, `max`), and the probe and refutation outputs have a `.provenance.json` beside them whose served model is the seat's and whose verification is PASS; `packet-manifest.json` lists the 32 files with their sha256, and `02` records the packet's own scan (`forbidden-terms-check --stdin` 0 hits, the credential patterns 0 lines, or the redaction made and recorded) before it was sent.
- [ ] The slice's punch-list issue has every item at a Phase 7 outcome: resolved with its commit, deferred to a named issue (#640 for a legacy path; a `bug` for a defect; the coordinator's lead for a gate's contract, a no-caller test or a retired stub), or withdrawn with its reason.
- [ ] `reviewed-at:` and `fixed-at:` above carry the lane's commits the read and the fixes were made at (the read on `8ebaf8daad`'s bytes for the 22 and `2174265e9c`'s for the ten lint fixtures, both hashes named; no EmulationStation path), and, after the coordinator closes this issue and the branch merges to `next`, `tools/renovation-status` lists this slice as `closed`.
- [ ] `01-research-notes.md` § Scope records the read hashes, the filter of brief § 2 with its output (32 paths, 6,911 lines; 32 fork-own; 20 Python, 2 shell, 10 Markdown; reach `n/a` 32, or the deltas beside them), the provenance (35 fork commits since `c445081a59` over the 22; none on `upstream/next`; the ten on P1 only), the branch-vs-hash diff over the 32 (empty, or each hunk listed with its owner), and T10's #945 delta to the lint fixtures named by commit.
- [ ] `02-forward-audit.md` carries a coverage table with exactly one row per path under its own `## Coverage` heading, the path in backticks as the first cell: ``awk '/^## Coverage/{p=1;next} /^## /{p=0} p && /^\| `tools\//{n++} END{print n}' 02-forward-audit.md`` prints 32; each row's Q1 to Q7 cells answered or `n/a` with a reason (a fixture file answers Q6 and Q7 at least: who reads it and what it fixes).
- [ ] `02-forward-audit.md` § The runs records every § 5 run with command, exit status, wall time and summary line, each with the sentence *a FAIL would mean ...* and, for the two writer tests, which busybox the applets came from (a build root's, or the host's with the PASS marked as the host's); the two retired stubs' refusal text and exit; the `|| true`, `assert` and host-path greps with their lines; the real-rclone four's backend binding read before any run.
- [ ] `02-forward-audit.md` § The guest cycle records the one authorized cycle (the image and its `.img.gz.sha256`, the host file line before and after, the pidfile, the two guest tests' commands and results, `tools/vm-stop`'s exit, the census after, the disk retired) -- or records that no cycle was needed, with the claims that would have needed one listed and marked `proved: tree` or `proved: history`.
- [ ] `00-running-log.md` shows no handheld action, no real provider or real account touched by a cloud test, no guest beyond the one cycle (a second only with a line on #661 quoted), no build, no edit to `tools/last-good-scripts-test`, no `fork-worktree sync|remove|repair`, no write under the M7 lane's trees or `/tmp`, and the host file's lines before and after any cycle quoted.
- [ ] `04-analysis.md` § Renovation face Q6 carries the brittleness table: one row per tool (21), each with (a) its dependencies that are not the thing it proves and what happens when each is absent (skip, fail, or a false pass, with the line), (b) its last recorded catch by issue or qa-log folder and date or `nothing recorded`, (c) its caller or `nobody`, (d) its positive control named or `none`; the eleven no-caller tools confirmed or refuted from the record; the two retired stubs with a proposed disposition for the coordinator.
- [ ] `04-analysis.md` § Q3 hunts the pass-without-proving shape through every test by name, each with the line read and a constructed input that would pass wrongly or the statement that none can; the busybox fallback of the two writer tests classified; the two guest tests' find/wait/stop path classified pidfile-and-disk or pattern.
- [ ] `04-analysis.md` § Q7 reads each tool's three descriptions (header, the rule that names it, the index row) against the code, the two retired stubs' index rows against their refusals, with each drift a Q7 row or a Q3 bug; a rule drift is a lead for the coordinator, not an edit here.
- [ ] `04-analysis.md` § Q5 carries each host-side test's wall time from its stage-A run and the two guest tests' from the record or the cycle, and names what share of T15's `scripts` suite (T12's 13 minutes) the four callees are, from `last-good-scripts-test`'s own timing lines if it prints them or marked unmeasured.
- [ ] Every proof in `02-forward-audit.md` carries a `proved:` cell reading `tree`, `history`, `tool-run`, `guest`, `fix-tree`, `fix-case` (a fix proved by the test's new case that failed on the unfixed test) or `fix-guest`; ``grep -c 'proved:' 02-forward-audit.md`` equals ``grep -c '^PROOF:' 00-running-log.md``.
- [ ] Every punch item carries `question:`; every `bug` this lane files passes `tools/box-check --issue N`; no file under `tools/` is changed on this branch before a stream brief (over the 32 members: ``tr '\n' '\0' < .qa-scratch/t14/paths.txt | xargs -0 git diff --stat <the lane tip the dispatch comment names> <fixed-at> --`` is empty, or every hunk is a stream the coordinator briefed), and a stream on a test records in `02` the case that failed on the unfixed test and passes on the fixed one.
- [ ] The retro exists at `docs/retros/<date>-m6-tooling-state-tests.md`, is posted on #661, and says what the slice did to the two time-to-play numbers (nothing) and, per stream, what it did to a test's refusals.
- [ ] `tools/register-check`, `tools/work-log-index --check`, `tools/rules-check --quiet`, `tools/forbidden-terms-check` and `.githooks/hooks-test` pass on the branch before its merge (after the coordinator's branch is merged into it at hand-back, if a row cited lives there), and `tools/lint-audit-artifacts` prints `PASS` on the folder, each exit code in the hand-back comment.

## 8. Stop conditions

Stop only on: every item of § 7 that is this lane's ticked and the branch
pushed (the hand-back); **the stage-D pause**; an explicit maintainer pause
on #661; a blocker named on #661 with what is needed (the seat failed, a
test that cannot run for a reason outside the tree, two commands that
disagree); a branch that differs from `8ebaf8daad` on one of the 22 or from
`2174265e9c` on one of the ten at stage A; or an execution limit, stated as
such with the running log current. A checkpoint is not a stop; a differing
count is a delta; `next` moving is drift. An idle session says it is idle on
#661, **and does not end a turn on a post that asks nothing**.

**What never runs in this slice:** a handheld action of any kind (D-QA-015);
a cloud test against a real provider or a real account (the local backends
and isolated filesystems only, D-QA-058); any read of a credential file
(`~/.config/council/env`, `~/.ROCKNIX/options`, `~/.config/rocknix/forbidden-terms`,
the QA accounts' store, a real `rclone.conf`); a push to any branch but the
lane's own; a second guest cycle without a line on #661; a guest found or
stopped by pattern; a build; `fork-worktree sync|remove|repair`;
`fork-publish-release` without `--prepare`, `rasteratops-candidate-store`
against the real candidate store, `pixelelated-state-check` against a real
image's root (its own test's disposable roots only); an edit to
`tools/last-good-scripts-test` (T15's), to a rule, `CLAUDE.md`, `AGENTS.md`,
a decided register row or `.github/sessions/saved-session-state-next.md`; a
write under `/workspace/repos/rocknix*` or `/tmp` (use
`/workspace/tmp/m6-t14/`); a credential-shaped literal written anywhere (a
fixture is built at run time); `--no-verify`; bare `git stash`; `git worktree
remove --force` or `rm -rf` on a worktree.

## 9. Ceremonies owed

- A work-log entry per session headed `#661`, its time from `date -u` in
  the same command, its prose through a quoted heredoc or the Write tool;
  `tools/work-log-index --write` after it (in this worktree only).
- A friction line the moment something slows, with `issue: #661` or the
  guard.
- The VM question written before any proof (§ 5: the host-side tests on the
  host; one authorized guest cycle for the two guest tests, if a claim needs
  it; nothing on a device).
- The cycle's own ritual if one runs (`generic-x64-vm-testing.md` § After
  every VM cycle): an entry in `docs/vm-qa-log.md`.
- The mini-retro at stage G, posted on #661, Instruction-Recommendations
  mode; its *adjustments* are proposals for the coordinator (D-WORKFLOW-189).
- A register row the same session for any decision the slice forces; the
  next Decided ID is checked on every pushed branch at the time (on
  2026-10-24 the highest Decided rows are D-WORKFLOW-205 and D-INFRA-030,
  the coordinator's; T12 runs beside this lane and may take 206); it goes at
  the end of `## Decided`, and a row is never edited.
- The merge notes: when `next` moves, the **coordinator** merges `next` into
  this branch, never between stage A and stage D; the coordinator merges its
  own branch into this one at hand-back before criterion 17's checkers run
  (as for T9, T10 and T12); a merge with conflicts is checked for leftover
  markers before it is committed (#696), and the ledgers are united by whole
  entries.
- Commit messages `docs: ...` for the audit, `<tool>: ...` for a stream's
  fix, each with `Refs #661` and the attribution line; `git add -A` only
  after `git status --short` shows nothing a test left behind
  (`.qa-scratch/` is gitignored; a test's temp root is its own, and one that
  leaves bytes in the tree is a Q2 finding).

## 10. Hand-back

The coordinator accepts by reading, in this order, without re-reviewing:
#661's checkboxes against their artifacts; the lint's `PASS` line; the
seat's `review-plan.json` and provenance and the packet's recorded scan; the
audit issue's checkboxes all at an outcome (the ticked and open counts read
by name); the coverage table's row count (32) and the brittleness table's
rows against § 7; **re-running on an export of the tip under
`/workspace/tmp`: the membership block, the file list with line counts, the
host-side tests that need no build root (`wait-lock-test`,
`retroarch-wrapper-test`, `rocknix-info-test`, `usb-gadget-test`,
`nova-led-test`, `build-identity-test`, `pixelelated-state-check-test`), the
two stubs' refusals, the `|| true` grep**; the guest cycle's record read if
one ran and the host checked for a payload left behind; `register-check` and
`rules-check` on a simulated merge with the coordinator's tip (the ledgers
united); the retro's answers; the six exit codes. The lane posts one
hand-back comment naming the tip and each artifact by path, writes
`reviewed-at:` and `fixed-at:` into #661's body, then says it is idle. After
acceptance the coordinator closes the audit issue, prompts the lane for
`audit-completion.json` and the full lint, merges the branch in its turn
after the M7 candidate (after T12's, before T4's), regenerates the ledgers,
and closes #661 when every row is proven.

**The readings before dispatch** (plan § 3, principle 3): the area's futro
(#903) carries this slice's kickoff addendum, and a stranger's proof of this
brief is run by a reader with no context before dispatch; version 2 records
what each found.

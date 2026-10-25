# Audit Analysis — M6.P2 T22, the OS's system services and platform quirks

**Date:** 2026-10-25
**Spec:** `docs/reviews/briefs/os-system-services.md` v3 (`cc8b6cf2a3`); `docs/reviews/plan-for-the-plan.md` § 6b, § 6c
**Issues:** #669, #695, #339
**Commits:** read at `8ebaf8daad`; upstream `next` for the delta and Q4 `651150fc88` (merge base `c445081a59`); guest image `069fc270442134fe771258418adf4e666e0473fb`

---

## Executive Summary

T22 read the 422 paths of the OS's system services and platform quirks
(16,604 lines; 24 fork-own) at `8ebaf8daad` with the security lens first.
One GENERIC_X64 guest proved the boot behaviour (`02` § The guest cycle).

- **All 29 units run as root, and every root-run input a player can write is
  one the platform hands them on purpose:**
  - the hook directories `/storage/.config/autostart/` and `/storage/.config/profile.d/`;
  - three boot markers under `/storage`;
  - an inserted medium.
- **No unauthenticated remote path was found.** The tty1 root shell exists
  only on a `textmode` boot.
- **The defects are brittleness and dead lines, all in upstream-carried
  files that stand at `651150fc88`:**
  - the custom autostart loop runs entries without a `-f` test and with an
    unquoted name, so a hook with a space in its name runs a different file
    with an argument (F-01, shown on the guest);
  - udevil mounts a btrfs medium without the `nosuid,noexec,nodev` its own
    file says every type must carry (F-04);
  - `udevil-mount@.service` calls a `samba-autoshare` that no shipped image
    has (F-05);
  - busybox is setuid root with `su`, `login`, `passwd` and `httpd`+CGI
    enabled and nothing in the tree calling them (F-03).
- **Brief leads that landed differently:**
  - cron is on no shipped image (F-09);
  - `video.service` cannot meet a missing binary;
  - #740 is reachable only on a developer's build, with a second copy site
    in `post-update` (F-06).
- **The two selection mechanisms leave 213 platform files (108,294 bytes) on
  every image that never run there** (F-10), and neither recipe says so (F-14).
- **Upstream's next merge** settles the http busybox pin and brings two
  collisions (crash logging and the sysctls), which are deferred as designs
  (F-12, F-13).

## Acceptance-criteria scorecard

| ID | Criterion (#669) | Verdict | Notes |
| --- | --- | --- | --- |
| AC-01 | the folder holds `00` to `05` | PARTIAL ⚠ | `05` at stage D |
| AC-02 | the lint prints `PASS` | PARTIAL ⚠ | pre-issue at stage D; resolution at close |
| AC-03 | `review-plan.json`, two seats with provenance, the packet manifest | PARTIAL ⚠ | written before the first call; the seats at Phase 4.6 |
| AC-04 | the punch-list issue at Phase 7 outcomes | MISSING ✗ | stage D onward |
| AC-05 | `reviewed-at`, `fixed-at`; the 422 at `8ebaf8daad`; nothing under `packages/`, `projects/`, `tools/` | PASS ✓ | `git diff --stat 4a48d388c4 HEAD -- packages projects tools` empty (`02` § The runs, `18`); the header is written at hand-back |
| AC-06 | `01` § Scope with the block and the figures | PASS ✓ | `01` § Scope |
| AC-07 | the coverage table, 422 rows | PASS ✓ | `02` § Coverage, generated |
| AC-08 | the reachability table, 422 rows, 8 and 213 named | PASS ✓ | `02` § The reachability table; the generator asserts the figures |
| AC-09 | the units table, 29 rows, enablement, the named units' findings | PASS ✓ | `02` § The units; F-01 to F-09 below; `tools/archaeology shell.service tty1` quoted in `02` § Proofs L-03 |
| AC-10 | § busybox: the pin and each flagged applet's caller | PASS ✓ | `02` § busybox |
| AC-11 | § The upstream delta: 44 M with states, 20 D split, 42 A and 2 R, two collisions | PASS ✓ | `02` § The upstream delta |
| AC-12 | § The guest cycle | PASS ✓ | `02` § The guest cycle; `guest-cycle/` |
| AC-13 | § The runs: exit, wall, figure, *a FAIL would mean* | PASS ✓ | `02` § The runs |
| AC-14 | `00` shows what never ran, four seat calls, nothing written outside | PARTIAL ⚠ | so far, yes; the seats are pending |
| AC-15 | `04` § Q3, Q4, Q6, § Second opinion | PARTIAL ⚠ | Q1 to Q7 below; § Second opinion after the seats |
| AC-16 | `proved:` cells; `question:` per item; box-check per bug | PARTIAL ⚠ | `02` carries every cell; items and bugs at stage D |
| AC-17 | the retro posted | MISSING ✗ | stage G |
| AC-18 | the five checkers on the branch | MISSING ✗ | after the hand-back merge |

## Risk Assessment

Every finding, with its question, severity and evidence class. A finding on
an upstream-carried file names the file's state at `651150fc88`.

| Finding | Question | Severity | Defect or item | Evidence |
| --- | --- | --- | --- | --- |
| F-01 | Q3 | Low | `autostart`'s `common` and custom loops run each entry with no `-f` test and `${script}` unquoted: a non-executable file or a directory is an error in the journal, and a hook whose name has a space runs another hook with an argument (L-01). Stands at `651150fc88` | proven on the guest |
| F-02 | Q3 / Q2 | Low (design) | `/etc/profile:19-23` sources `/storage/.config/profile.d/*` into every root service that loads it; guarded by `-f`, `. ${CONFIG}` unquoted (L-02). Stands | trace / read |
| F-03 | Q3 / Q5 | Low | busybox is setuid root (`package.mk:177,209`; mode 4755 on the guest) with `su`, `login`, `passwd` and `httpd`+CGI enabled, linked and called by nothing in the tree (L-04). The flags stand at `651150fc88` | proven on the guest |
| F-04 | Q3 | Low | `udevil.conf:233` gives btrfs `compress=zstd:3` alone, against `:213`'s *FOR GOOD SECURITY ... SHOULD ALWAYS INCLUDE: nosuid,noexec,nodev* (L-05); upstream's (`c288a47e62`). Stands. The effective mount is not proven | trace / read |
| F-05 | Q3 / Q6 | Low | `udevil-mount@.service` runs `-/usr/lib/samba/samba-autoshare`, which no shipped image has (SAMBA_SUPPORT=no); the `-` hides the failure (L-06, blindspot 16) | proven on the guest |
| F-06 | Q3 | Low | #740's `cp ... /storage/.ssh` has a second site at `post-update:54-57`; both are reachable only on a build with `LOCAL_SSH_KEYS_FILE` (L-07). #740 is cited, not re-filed | trace / read |
| F-07 | Q3 | Low (design) | `shell.service`, an unauthenticated root shell on tty1, only on a `textmode` boot (L-03); no register row | proven on the guest |
| F-08 | Q3 | Low (design) | markers under `/storage` change root behaviour at boot: `.please_resize_me`, `.cache/volatile-log`, `.cache/debug.rocknix` (L-10) | trace / read |
| F-09 | Q6 | Low | cron's two units and `default.d/crond.conf` are on no shipped image (CRON_SUPPORT=no) (L-08) | proven on the guest |
| F-10 | Q6 / Q5 | Low | 213 platform files (108,294 bytes) ship on every image and run on none; 8 `system-utils` rows are installed by no shipped image | trace / read |
| F-11 | Q4 | Low | busybox 1.36.1 over http; systemd 255.8; util-linux 2.39.2: upstream has 1.38.0 over https, 261.2 and 2.42.4. The http pin is settled by the next base merge | trace / read |
| F-12 | Q1 | Low (design) | collision C-1: `8bce25b3b7` replaces core files with journal crash logging, against the fork's keeper (D-INFRA-011/012/013) | trace / read |
| F-13 | Q1 | Low (design) | collision C-2: `54acd9556f` moves the sysctls into the image (`60-rocknix.conf`) and deletes the fork-carried `sysctl.d/rocknix.conf` | trace / read |
| F-14 | Q7 | Low | neither `system-utils/package.mk` nor `quirks/package.mk` says which files each image carries or runs; the quirks recipe ships every platform with no comment | trace / read |
| F-15 | Q2 | Low (design) | no unit names a user (all 29 run as root) | proven on the guest |
| F-16 | Q2 | Low | `systemctl is-enabled` reads `disabled` for every vendor-linked unit, so no tool answers "enabled on which build" except the `.wants` links (L-15) | proven on the guest |

## Coverage Boundary

**Examined:** all 422 paths at `8ebaf8daad`; every shell, recipe, systemd, udev and C row read, the 30 config files read, busybox's three configurations at the flagged lines and the rest scanned; the 29 units and the GENERIC_X64 quirks run on one guest (`02` § The guest cycle).
**Deliberately not examined:** `quirks/devices/**` (T29's), the interface and launch scripts beyond their call sites (T1, T2), the cloud scripts (T16, T17).
**Dimensions not exercised:** anything on a handheld: the H700 and SM8550 platform quirks run (read only), `QUIRK_DEVICE`'s device-tree branch, `sleep.d/` on a real suspend, `volume-fixup` (RK3566), an inserted btrfs medium's effective mount options (F-04), a `textmode` boot (F-07).

## Finding Verification (Phase 4.5)

No finding is Critical or High. The four with a reachable consequence were
re-read at their lines after the guest window:
- **F-01:** `autostart:73-76`, and the guest's `40 uid=0 args=[split]`.
- **F-03:** `busybox/package.mk:177,209`, and `mode=4755` on the guest.
- **F-04:** `udevil.conf:209,213,233`.
- **F-05:** the unit's line, and the guest's `No such file or directory`.

## Renovation face

### Q1 Modernize

- **The two collisions (F-12, F-13)** are the modernization the next base merge forces. Each carries a design sentence in `02` § The upstream delta, deferred to the coordinator; no edit.
- **The hook directories** (`/storage/.config/autostart/`, `/storage/.config/profile.d/`) are LibreELEC's design, and T1 named the autostart shape as a design the coordinator holds. This slice adds that both run as root, last in the boot order, and that the custom loop is unguarded (F-01).

### Q2 Standards and best practices

- **F-15:** 29 units, no `User=`. On a single-user handheld this is the platform's choice, recorded as a design.
- **F-02:** `/etc/profile`'s loop is guarded but unquoted.
- **F-16:** `systemctl is-enabled` misleads on these images.
- **The inventory's `last_upstream_commit`** is upstream's tip, not the read tree's (brief § 2; T10's): it is cited here as the tip's.

### Q3 Bugs

The root-and-writable-path findings, each with its bug decision (proposed; stage D settles it) and its `Already written:` line:

| Finding | Writable input | Guard | Decision proposed | Already written |
| --- | --- | --- | --- | --- |
| F-01 | `/storage/.config/autostart/*` | none | `bug` (the guard and quotes are contained, `bugs-are-agent-first.md` rule 6); class decision #346 (upstream-carried) | nothing inherited: the loop reads the directory at each boot and writes nothing |
| F-02 | `/storage/.config/profile.d/*` | `-f` | design | nothing inherited |
| F-03 | none (an applet surface) | -- | `bug`-candidate for #346: disable the four applets in the configuration, or a design row | nothing inherited: a configuration choice |
| F-04 | an inserted btrfs medium | `udevil.conf` | `bug` (#346): the file's own warning; a VM proof of the effective mount is owed (a loop-backed btrfs on the guest) | mounts made under it are transient; nothing on `/storage` |
| F-05 | -- | `-` prefix | `bug` (#346): remove the post lines, or ship the script | nothing inherited |
| F-06 | `/usr/config/ssh` at build | `-e` test | cited on #740 with the second site | on a developer's device built with `LOCAL_SSH_KEYS_FILE`: a file `/storage/.ssh`; #740's own line |
| F-07 | tty1 on a `textmode` boot | the boot mode | design | -- |
| F-08 | three markers | -- | design | -- |

### Q4 Package currency: every pin at both hashes

| Package | Pin at `8ebaf8daad` | At `651150fc88` | Author's release | Note |
| --- | --- | --- | --- | --- |
| busybox | 1.36.1, http (`package.mk:7,11`) | 1.38.0, https | `CANNOT (no network)` | settled by the next base merge; the generic recipe already 1.38.0 (#997) |
| systemd | 255.8 (`systemd-stable`) | 261.2 | `CANNOT (no network)` | the generic recipe 261.2 at both; the override shadows it until the merge |
| util-linux | 2.39.2 | 2.42.4 | `CANNOT (no network)` | the generic recipe 2.42.2 at both |

`tools/fork-package-freshness` covers only the packages the fork introduces; none of these three is one (D-WORKFLOW-024).

### Q5 Efficiency

- **Bytes shipped and never run:** 213 platform files, 108,294 bytes, by directory:

  | Directory | Files | Bytes |
  | --- | ---: | ---: |
  | SM8250 | 30 | 23,075 |
  | SM6115 | 31 | 19,262 |
  | SM8750 | 26 | 12,944 |
  | SM8650 | 24 | 10,769 |
  | RK3566 | 16 | 6,921 |
  | SM4450 | 13 | 6,748 |
  | AMD64 | 18 | 6,723 |
  | RK3326 | 12 | 6,250 |
  | S922X | 10 | 4,286 |
  | RK3588 | 12 | 4,032 |
  | RK3576 | 13 | 3,845 |
  | RK3399 | 8 | 3,439 |

  Small against an image; the cost is the reader's, not the card's.
- **busybox's enabled applets against their callers:** `su`, `login`, `passwd` and `httpd` (with CGI, `/etc/httpd.conf` and a `/usr/www` webroot) have no caller (F-03); `nc` has 3 and `udhcpd` 1.

### Q6 Dead ends: a disposition per unit

- **The 8 `system-utils` rows no shipped image installs** (AMD64 3, RK3399 3, RK3566 1, S922X 1): *carried by placement* (D-WORKFLOW-185). They serve the devices upstream builds.
- **The 213 platform files, by directory** (AMD64, RK3326, RK3399, RK3566, RK3576, RK3588, S922X, SM4450, SM6115, SM8250, SM8650, SM8750): each directory is *carried by placement*. They serve upstream's devices, and the run-time selection is upstream's design.
- **The 9 files upstream deleted:** *settled by the next base merge*.
- **Cron's three files (F-09):** *carried, off by option* (`CRON_SUPPORT`).
- **`samba-autoshare`'s two lines (F-05):** the dead lines of F-05's decision.
- **`volume-fixup.service`:** RK3566's, carried by placement.
- **Removals:** none.

### Q7 Clarity and structure

A reader cannot tell from the tree which units run on which device, or which
quirks a boot selects. Three things would let them:
- the two `package.mk` files saying what they ship (F-14);
- `098-deviceutils` being the place the five sensing units start;
- the boot order (platform, device, common, custom) being written down.

The reachability and units tables in `02` are that record for this
reading, and T29 inherits their *runs on* column.

## Instruction File Recommendations

### Coverage Gaps (would-have-prevented)

- A check that every unit's `Exec*` path exists in the image would have caught F-05 (blindspot 16). The guest read here is a manual instance.

### Codification Gaps (needs-new-rule)

- `generic-x64-vm-testing.md` could say that `systemctl is-enabled` is not the enablement answer on these images, and that the `.wants` links are (F-16). Proposed to the coordinator; this lane edits no rule.

### Recommended Action Sequence

1. F-01, F-04 and F-05 to #346 with their traces.
2. F-06 as a comment on #740.
3. F-12 and F-13 to the coordinator before the next base merge.

## Second opinion (Phase 4.6)

Depth **extended** (`second-opinions/review-plan.json`): the primary (Anthropic, Opus 5.5) and two reviewers from other labs. Each seat ran its probe first, then its refutation pass, through the Facilitator.

| Seat | Call | Provenance | Served | Outcome |
| --- | --- | --- | --- | --- |
| GPT-6 Astra, `max` | `tools/council/run invoke --member gpt --provider openrouter`, brief `second-opinions/gpt-brief.md` (382,673 bytes), under `tools/watch-build --record-only` (`.build-runs/20261025T093302Z-f3543809/`, `build.rc` 0), 09:33:02-09:53:54 | `second-opinions/gpt-audit.md.provenance.json`: `council-facilitator@1.14.1-pixelelated.2`, outcome success, 0 retries, verification PASS (`provider_response`), provider PASS, effort PASS (48,690 reasoning tokens) | `openai/gpt-6-astra` by OpenAI | 34 items of its own (G-01 to G-34) and a grade for each of F-01 to F-16; output sha256 `107d6168aebfbe40d6552e2532e36cc8b103411c918b702776a0e06e9d4d4987` |
| Gemini 4 Argon, `high` | *pending: its brief is the Astra packet unchanged, a third-reader preamble, and the grades below* | | | |

### Astra's items, graded against the artifacts

Each grade below comes from re-reading the cited lines at `8ebaf8daad` (09:54-09:57 UTC), not from the seat's wording. The grades are:
- **confirmed** (the lines show it);
- **confirmed, re-graded** (they show it, at another severity);
- **narrowed** (part of it holds);
- **disagree** (with the artifact that refutes it);
- **not re-read** (carried as a lead, the seat's citation unchecked).

For each item on a file upstream changed, the state at `651150fc88` follows the grade.

| Item | Grade | The lines read, and what they show | At `651150fc88` |
| --- | --- | --- | --- |
| G-01 update acceptance | **narrowed, Low** | `init:298-317` sources `/update/etc/os-release`, and `:330-331` runs the update's own `canupdate.sh`, before acceptance; the check is an md5 the package carries (`:1031-1069`), skipped by `.nocheck`. The trigger is a file the owner stages; authenticity is the downloader's business, outside this slice | stands (the update code is unchanged) |
| G-02 write failures ignored | **confirmed, Medium** | `update_file`'s `dd` status is discarded (`:403`); `update_partition` captures and prints but never tests (`:420-423`); `Update complete` follows regardless (`:1133`) | stands |
| G-03 no rollback pair | **narrowed: design, Low** | no A/B pair (`:1123-1129`): LibreELEC's architecture, a Q1 item, not a defect | stands |
| G-04 rejection unmounts `/storage` | **confirmed by trace, Medium** | every rejection calls `do_cleanup` (`:1065,1077,1116`), which unmounts `/storage` (`:861-863`), then returns 0. The boot loop checks no step (`:1312-1314`), and `prepare_sysroot`'s `mount --move /storage` (`:1143`) finds nothing. **What the device boots into is not proven**; the VM can show it (stage an update with a wrong md5) | stands |
| G-05 empty arch skips both checks | **confirmed, Low** | `:349` gates both checks on both arches being non-empty; the comment (`:348`) calls it deliberate for pre-`os-release` builds | stands |
| G-06 a bare pair is refused | **confirmed, Low** | `:883` tests only the three archive names; a bare `KERNEL`/`SYSTEM` pair gives an empty string, so it is *unsupported* and deleted (`:886-889`) | stands |
| G-07 space check order | **confirmed, Low** | `:1101` credits the old SYSTEM's size, and the kernel is written first (`:1123-1127`); the 5 MB minimum (`:1102`) is the margin | stands |
| G-08 NBD device name | **confirmed, narrowed to Low** | `:205` uses the unset `NBD_DEV` instead of `NBD_DEVS` (`:50,211`); NBD is a netboot path no handheld uses | stands |
| G-09 iSCSI option reuse | **confirmed, Low** | `option` is never reset in the loop (`:143-174`) | stands |
| G-10 fsck results | **confirmed, Low** | result 4 after `-y` reboots (`:623-633`); 16 and above continue boot (`:652-654`) | stands |
| G-11 the repair countdown | **confirmed, Low** | `:618` reads `$?` twice; the second is the first test's status, so any failed `read` (EOF) repairs at once | stands |
| G-12 init's error shell | **confirmed: design, Low; corrects F-07** | `error()` opens `setsid cttyhack sh` (`:86-99`) on any init error: a second unauthenticated console path besides `textmode` | stands |
| G-13 `debug-shell.service` enabled | **confirmed in the tree, Medium; corrects F-07** | `systemd/package.mk:332` enables it unconditionally. `enable_service` links it from its `WantedBy=` (`config/functions:1700-1720`), so a root shell on its console starts on every boot. The guest's `.wants` read was filtered to the 29, so it is **not proven on the guest**; the VM can show it | **settled by the next base merge** (`f2379f83b7`, *only start the debug shell when debugging is on*) |
| G-14 `.configured` after unchecked copies | **confirmed, Low** | `userconfig-setup:17-66` tests nothing before `touch /storage/.configured` | the fork's lines; stands |
| G-15 the ld.so stamp | **confirmed, Low** | `:76-77` writes the stamp whatever `ldconfig` returned | stands |
| G-16 the locale copy | **confirmed, Low** | `:80-83` treats the directory's existence as done | stands |
| G-17 a setting run as a command | **confirmed, Low** | `autostart:93-94` runs `$(get_setting system.cpugovernor)`; T1's F-01 is the same shape in the launch path | stands |
| G-18 a hook that never returns | **confirmed, Low** | `rocknix-autostart.service` is `Type=oneshot` with no `TimeoutStartSec` (systemd gives oneshots no start timeout by default); the hooks run before the interface starts (`autostart:73-91`) | stands |
| G-19 stderr not in `boot.log` | **confirmed, Low** | `2>&1 >>${BOOTLOG}` sends stderr to the journal. The guest shows it: s5's errors are in the journal and not in `boot.log` | stands |
| G-20 the interface's start unchecked | **confirmed, Low** | `autostart:91` backgrounds `systemctl start` and nothing collects it | stands |
| G-21 `EnvironmentFile=/etc/profile` | **confirmed; corrects `03` § 3.5** | systemd's `EnvironmentFile=` reads `KEY=VALUE` lines and does not run shell; `powerstate.sh:11` is what sources the profile | stands |
| G-22 the warning threshold | **confirmed, Low** | `powerstate.sh:59-61`: `[[ ${BATLEFT} -le ${AUDIBLEALERT_THRESHOLD} ]]` evaluates a setting as an arithmetic expression (the owner's setting; the owner is root) | stands |
| G-23 duplicate input readers | **confirmed, Medium** | `input_sense:292` empties the list once, before the retry loop (`:294-330`), so up to six passes append the same devices. The fork's comment at `:290-291` states the intent the code misses. The guest's s2b shows six `input_sense` processes: consistent, not counted against devices | stands (upstream's lines are the same here) |
| G-24 reload restarts nothing | **confirmed, Low** | the two disconnect patterns are identical (`:105-106`); `get_devices` rebuilds the array, but the readers started at `:347-357` keep running | stands |
| G-25 hat events filtered out | **confirmed, Low** | `:360` passes only `EV_KEY`, `EV_SW` and `error reading`; the `ABS_HAT0` handlers (`:93-96`) never see an event | stands |
| G-26 latched repeat on disconnect | **not re-read** | carried as a lead | -- |
| G-27 a blocking action stalls the loop | **not re-read** | carried as a lead | -- |
| G-28 wall-clock debounce | **confirmed, Low** | `:216-217` | stands |
| G-29 `killall` operands | **confirmed, Low** | `:224` runs `killall ${TO_KILL}` unquoted with no `--`; `runemu.sh` (T1's) writes the file | stands |
| G-30 the mount's failure ignored | **narrowed, Low** | `ExecStart=-` hides a failed mount, and `RemainAfterExit=yes` leaves the unit active; but the rule uses `systemctl restart` (`95-udevil-mount.rules`), so a re-insert does retry | `--no-block` only |
| G-31 fstrim's stamp | **confirmed, Low** | `fstrim.service:6-7`; off by default (`fstrim.enabled=0`) | stands |
| G-32 the resolver fallback | **confirmed, Low** | `systemd/package.mk:222-224`: `sed -i` succeeds without a match, so the `\|\| echo` never runs; a build-time item, and its effect depends on the template's line | the recipe changed upstream; not re-read there |
| G-33 the VM port check | **confirmed, Low (a harness item, D-QA-053)** | `095-cloud-ssh:38` does `tr -cd '0-9'`, so `12x34` is kept as `1234`, against its own comment (`:33-34`) | the fork's own; absent upstream |
| G-34 update paths not filename-safe | **confirmed, Low** | `ls ... \| head -n 1` (`:872-874`), and unquoted `dd` operands (`:403`) | stands |

**Astra's grades of F-01 to F-16, and what changes:**
- **F-04 is re-graded Medium,** as Astra argues. An inserted medium is not the owner writing a root hook, and the file's own policy (`udevil.conf:213`) is what btrfs breaks.
- **F-02 is narrowed** to a Low quoting defect inside a designed interface.
- **F-03 is narrowed** to a Low hardening question. No caller in the tree does not prove an applet is unused interactively.
- **F-07's "only on a `textmode` boot" is wrong** (G-12, G-13). The shell findings become one item: three unauthenticated console paths.
- **F-08 is incomplete.** `scripts/init:1363-1368` also selects factory reset (`reset_oe`, `reset_xbmc`) and restore (an archive in `.restore/`). Those two are **settled by the next base merge**: they were in the merge base, and upstream removed them (`a98a3066f5`).
- **F-10's wording becomes "not selected by these dispatchers"** (the generator does not resolve symlinks or cross-references).
- **F-14 adds the `/usr/lib/autostart/${HW_DEVICE}` layer** to the boot order (platform, device, common, the device's own, custom).
- **F-15's "29 units run as root"** is restated as: no unit declares an identity, and of the 29 files, 23 are services.
- **F-16 is narrowed:** activation is links, dependencies, conditions and script-driven starts, not links alone.
- **F-05, F-06, F-09, F-11, F-12 and F-13 stand,** with Astra's narrowings recorded.

## Quality Self-Check

| Item | Status |
| --- | --- |
| Acceptance Criteria Scorecard present, IDs match #669 | present (AC-01 to AC-18) |
| Coverage Boundary present (02 + 04) | present |
| Finding Verification recorded for all Crit/High | none at those grades; the four reachable findings re-read |
| Second opinion recorded (Phase 4.6) | pending |
| Instruction File Recommendations (epic) | present |
| Verdicts use the defined vocabulary only | yes |
| Traceability / Evidence / Reproducible / Actionable / Complete | self-checked against `02` |

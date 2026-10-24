# Running Log — M6.P2 T8, the image's own packages (projects/ROCKNIX)

**Issue:** #655 (`M6.P2 E848/T8`), slice `image-packages` (`k: 8`); epic #848; renovation #339; milestone M6
**Brief:** `docs/reviews/briefs/image-packages.md` version 2 (`dede8effec`); its § 7 is the contract, identical to #655's eighteen criteria
**Executor:** Claude Code, `anthropic/claude-opus-5-5` (Opus 5.5) at high effort; the T5 session `c649553c-8086-4db7-ad9c-248c7e41ff95`, herdr agent `m6-t5-build-engine`, pane `wN:p7` (the dispatch, issuecomment-6384032445)
**Skill:** code-auditor at epic tier, the renovation face (plan § 6b); depth **Independent** (D-WORKFLOW-184): one GPT-6 Astra seat at `max` through the Facilitator, a probe then one refutation over one bounded packet; the dispatch authorizes the two calls; a failed seat is a hold
**Worktree:** `/workspace/repos/pixelelated/distribution.worktrees/m6-image-packages-655`, branch `feature/m6-image-packages-655`
**Read hash:** the slice's bytes are `next`'s `8ebaf8daad`; **`reviewed-at` = `caf1de3727`** (the branch `HEAD` at stage A; the commit carrying this log changes no slice path); `upstream/next` `e0f9deb899` at the fetch (12:10)
**The bench:** the recipes, scripts, units and configs at the hash (`.qa-scratch/t8/at-hash/`), `upstream/next`, the hosts `tools/fork-package-freshness` reads, the GitHub API's `compare`, one HEAD probe per effective URL, ROCKNIX's mirror, the shared source cache's stamps, and the five M7 roots' `build/` listings and GENERIC_X64 install tree, read only. A guest only for a stage-E behaviour claim
**Can this be done on the VM?** **Yes, for every behaviour claim** (a stream's unit, script or install step, on the GENERIC_X64 guest); **no guest for the reading or the tables** (brief § 5)
**Prose:** written through Python or a quoted heredoc only (plan § 6b E; T7's incident)

Every time below is a `date -u` reading taken in the command that wrote it.

---

### [Stage A] 12:10 to 12:12 — Scope

- **Read**, in the order the dispatch gave: the dispatch comment on #655 (12:09, with T6's 08:57 lead before it); the lane pointer; `docs/reviews/plan-for-the-plan.md` (read whole for T7; its one change since, the stage-E row's three new bullets, read word by word with `git diff --word-diff e7978a1ca5 HEAD`); the brief whole (version 2).
- **Rules:** `git diff --stat next -- .claude CLAUDE.md AGENTS.md tools/lint-audit-artifacts` lists exactly the dispatch's eight paths (127 insertions, 11 deletions).
- **The first commands** (12:10:46 to 12:10:58):
  - `git fetch`: rc 0; `upstream/next` is `e0f9deb899`;
  - the branch is stacked on `2174265e9c`; `inventory.json` is present;
  - `df -i`: `/workspace` 20%, `/tmp` 41%;
  - the at-hash export of `projects/ROCKNIX/packages`: 2,614 files under `.qa-scratch/t8/at-hash` (gitignored), rc 0;
  - P1's tools are present;
  - `rules-check` rc 0; `register-check` rc 0 (664 IDs); `ceremony-check` rc 1 on `OVERDUE: 2026-W42 summary missing` (M7's week, not this lane's);
  - the push set the upstream;
  - the host file's tail read (the coordinator's 10:36 correction on `portaudio`; census qemu 0);
  - the API budget: 4,007/5,000;
  - `~/.config/council/env` is present (not read).
- **The scope, re-derived** with brief § 2's filter on `inventory.json` (`00ca350666`). **All equal to the brief's: no delta:**
  - **485 paths, 20,644 lines**: upstream-carried 450, fork-own 35; reach `shipped` 478, `test` 6, `n/a` 1;
  - **260 recipes** (27 fork-own) in the brief's 22 groups; 60 with patches;
  - **14 paths contain spaces, and none of them is a recipe.**

  The full listing is `.qa-scratch/t8/scope-out.txt`.
- **Branch against the hash, over the 485** (`xargs -0`): empty.
- **Provenance by git:**
  - against the base: 11 A, 24 M (the fork's 35);
  - against `upstream/next`: 31 A, 87 M;
  - the absent recipes: **11 orphans, 7 fork-added**;
  - 40 upstream commits on these paths since the base; 66 recipes changed upstream;
  - `fork-package-freshness --list` under `projects/`: 34;
  - the conflict set (fork-changed ∩ upstream-changed since the base): **11**, as the brief has it.
- **A T7 erratum found here:**
  - **What T7 wrote:** `docs/audits/2026_10_24-epic-m6-generic-packages-reached/` (`05`'s PL-12, `tools/punch-items.py`) and its retro called six of the 47 sourcing overrides *orphans ROCKNIX deleted*.
  - **The fact:** three of the six (`harfbuzz-icu`, `gst-plugins-bad`, `gnutls`) are **fork-added**, absent at the base too; only `libfreeaptx`, `opus` and `libfmt` are orphans. T7's check read `upstream/next` alone, not the base.
  - **Where it is recorded:** `01` § T7 erratum here; reported on #655, since T7 is accepted and its folder is not this lane's to edit.

### [Stage B] 12:13 to 12:36 — Phases 1 to 4: the movers, the sweep, the record, the conflicts

- **Phase 1 reads:**
  - the rules the brief § 3 names, `packaging-and-patches.md` from this worktree (the rest loaded this session at `next`'s bytes, by the stage-A diff);
  - `tools/fork-package-freshness` (read whole for T7, unchanged since: `git diff --quiet 4ea87f17dd HEAD -- tools/fork-package-freshness`), `tools/viewplan`, `tools/pkgcheck`;
  - `scripts/update_packages` (`PKG_PATH` at `:16`; its checksum lines `:52`, `:61`, `:63`), never run;
  - T7's audit (accepted at `db6597356b`), whose loops this stage re-uses; T6's widened `pkgcheck` (`git show 44f64842b6`);
  - T30's `second-opinions/` on `origin/feature/m6-emulators-standalone-677` (the probe prompt, the brief's head, the probe's provenance, `review-plan.json`).
- **§ 5's checks**, each in `02` § Mechanical checks with its exit status:
  - (a): 12:13:04;
  - the expansion: 12:13:05 to 12:13:50;
  - `make update`'s set: 12:15:06;
  - the freshness tool: 12:15:17 to 12:15:29, rc 2;
  - the hash pins: 12:16:02 to 12:17:10;
  - the HEAD probe: 12:17:32 to 12:20:13;
  - both `pkgcheck` runs: 12:17:40 to 12:18:33;
  - `bash -n`: 12:19:09;
  - the units: 12:19:33;
  - the redirect fetch: 12:20:44 to 12:28:36;
  - the mirror for the three: 12:20:56 to 12:22:07;
  - the base merge simulated: 12:23:57;
  - `git ls-remote` ×10: 12:25:28 to 12:26:24;
  - `samba` again: 12:28:05.
- **API budget:** 4,007 at 12:10; 3,907 before the freshness tool; 3,843 to 3,703 over the hash pins.
- **Posts on #655:**
  - 12:12 (stage A);
  - 12:14 (`simple-http-server`). The coordinator filed it as **#890**, packeted (`fix/m6-890-shs-sha256`), with D-WORKFLOW-197.
  - The T7 erratum was answered by a note on #654.
- **Deltas from the brief** (`03` § 3.3):
  - the record block's regex prints `entware` for `arm`;
  - 50 sourcing recipes are 43 plus 7 `get_pkg_directory` users;
  - the overrides that reset a pin are 6, not 8;
  - `sway`'s gap is RK3588's only;
  - the third empty checksum is #890.
- **Written:**
  - `02`: 485 coverage rows, § Mechanical checks, § The fetch sweep, § The conflict set, § The #644 findings, P1 to P15;
  - `03`;
  - `04` (§ Second opinion pending), with the orphan table and the conflict list;
  - `q4-table.md`, `q4-pins.json` and `tools/t8-tables.py`, one generator asserting 485 and 260.
- **The proof counts:** P1 to P15 in `02`; their proof lines follow.

PROOF: 12:11 P1 the slice is the brief's 485 paths and 260 recipes; 14 paths with spaces -- `01` § Scope
PROOF: 12:12 P2 35 fork changes; 11 orphans, 7 fork-added; 66 recipes changed upstream -- `prov-*.txt`
PROOF: 12:13 P3 (a): 367 identical, 87 differs, 21 orphan, 10 fork-added over the 485 -- `q4a.txt`
PROOF: 12:24 P4 9 of the 11 conflict at a simulated base merge; `gamescope`'s wraps agree at both commits -- `base-merge.txt`
PROOF: 12:13 P5 three archive versions without a checksum on the shipped plans -- `effective.txt`
PROOF: 12:15 P6 `make update`'s set holds 13 of this slice's recipes -- `update-set-*.txt`
PROOF: 12:17 P7 (c): the tool's 34, `cairo` BEHIND, 44 GitHub hash pins compared, 6 short -- `q4c.txt`, `q4c-hash.txt`
PROOF: 12:20 P8 the HEAD histogram; the controls 404 and 200 -- `probe/head.txt`, `probe/controls.txt`
PROOF: 12:28 P9 140 of 143 redirected archives match; the mirror covers `libaio`, `rocknix-abl`, `samba` -- `probe/fetch.txt`
PROOF: 12:18 P10 `pkgcheck` 258 and 257 PASS; each FAIL read -- `pkgcheck-*.txt`
PROOF: 12:22 P11 `bash -n` 48 ok; the four shapes absent, each grep proved on a fixture -- `bashn.txt`, `grep-fixture.sh`
PROOF: 12:22 P12 sourcing `virtual/image` wrote `image/system/opt` in three build directories here (#852) -- the symlinks' mtimes
PROOF: 12:20 P13 the units: no directive warning; `xorg-configure`'s script in no image -- `units-verify.txt`, `units-exec.txt`
PROOF: 12:21 P14 every plan's reached recipes stamped; the unbuilt the 12 virtual and `qcom-abl` -- `stamps-*.txt`
PROOF: 12:30 P15 the orphans' pins after the base merge; `glslang` 16.6.0 to 16.5.0 -- `git show upstream/next:<generic>`

### [Stage C] 12:36 to 12:40:00 — Phase 4.6: the Facilitator, the probe, the packet, the refutation started

- **Setup (12:36:46 to 12:37:17):** `npm install --prefix tools/council` rc 0. `tools/council/run verify-pins`: `OK - verifier pins match current files and every re-pin is accountable.` `tools/council/run test`: 39/39, 127/127, 19/19, 0 fail. `run` sources `~/.config/council/env` itself, and the env was not read.
- **The probe** (12:37:35 to 12:37:43): `tools/council/run invoke --member gpt --provider openrouter --prompt-file second-opinions/gpt-probe-prompt.md --output second-opinions/gpt-probe.md`, rc 0.
  - attempt 1, http 200, `model_field` `openai/gpt-6-astra` (`model_identity_source: provider_response`), served by **OpenAI**, effort `max`, 252 reasoning tokens, `finish=stop`;
  - `final.verification`: **PASS** (semantic; observed `openai/gpt-6-astra`);
  - the seat's own line reads `READY unknown`; the provider's field is the authority.
- **The packet** (`tools/t8-packet.py`): `second-opinions/gpt-brief.md`, **398,152 bytes, sha256 `7e93a08906a8168fe86ecf6b24c9e2d6381d1f316c28ce1af63cd59e41d6dca5`**, 69 parts (`second-opinions/packet-manifest.json` names each with its sha256).
  - **What it carries:** `02` less its 485 generated rows, `03`, `04` less its 260 generated rows, `q4-table.md`, the 35 fork-own files whole, the 64 upstream-carried paths that differ from `upstream/next` as their diff, 14 line-numbered excerpts, 15 mechanical outputs, and the ask.
  - **Checks before sending:** redirect query strings cut; the hook's secret patterns 0 hits; `forbidden-terms-check --stdin` rc 0; under the 440,000-byte cap.
- **The refutation** started at 12:40:00: `tools/council/run invoke --member gpt --provider openrouter --prompt-file second-opinions/gpt-brief.md --output second-opinions/gpt-audit.md`, in the background.
  - **Watching it:** the harness task delivers its end.
  - **Its silent mode:** a seat that hangs is ended only by the Facilitator's own per-attempt and total timeouts, and by the `timeout 5400` around it.

### [Stage C] 12:55 to 13:01 — the second opinion graded, the punch list drafted

- **The refutation ended at 12:55:20, rc 0.** One attempt, http 200, `model_field` `openai/gpt-6-astra` (`provider_response`), served by OpenAI, effort `max`, 40,720 reasoning tokens, 46,644 completion, `finish=stop`, 920 s. `final.verification`: PASS. The provenance's `user_prompt_sha256` equals the packet's `7e93a089...`. The output is `second-opinions/gpt-audit.md`, 26,313 bytes.
- **Graded in `04` § Second opinion, every item read at its site:**
  - **27 new items:**
    - G-01 and G-15 confirmed Medium → F-14 and F-13, both `bug`s;
    - G-20 confirmed → F-15, a lead for #844;
    - G-22 confirmed → F-16;
    - G-27 confirmed → F-11 widened to the `spirv-headers` triple;
    - G-16 folded into F-02's stream;
    - the eight small shapes → F-17;
    - G-07 refuted (`050-sway.conf:4-5` exports the session variables);
    - G-08, G-18, G-19 and G-25 withdrawn with reasons;
    - G-26 applied (17 table rows now say *first `PKG_VERSION` literal*).
  - **Its refutations of F-01 to F-12:** accepted, narrowing F-01, F-06, F-10, F-11 and F-12, and correcting eight conflict dispositions (`gcc`, `gstreamer`, `gamelist.xml`, `gst-plugins-base`, `spirv-tools`, `rocknix-abl`, `cairo`, `111-sway-init`).
- **Two of my statements corrected in the grading:**
  - `make update` would move four hash pins, not "three at HEAD" (five are at HEAD);
  - `cairo`'s listing read was not stamped.
- **D-WORKFLOW-198** (the coordinator's, `152c4ee3c3`) settles F-11: keep the fork's `glslang` override at the base merge. The coordinator's 12:42 answer: the conflict list is one Renovation item, F-11 its own Medium, and `libaio` and `rocknix-abl` two Low bugs.
- **Written:** `05` from `tools/punch-items.py` (seventeen items); `second-opinions/review-plan.json` complete.

### [Stage D] 13:02 to 13:04 — the punch list, the issues, the pause

- **Four lane bugs**, each labelled `bug` with no milestone, a code trace with `Already written:` and the VM line, and every hash and line read from the tree:
  - #891 `libaio` and #892 `rocknix-abl` (dead primary URLs, mirror-covered, Low);
  - #893 `mangohud` (three unverified downloads at configure, Medium);
  - #894 the installer (unchecked destructive steps, Medium).

  `tools/box-check --issue N`: 2 open, 0 fail for each.
- **#890 and #852** are the coordinator's and T6's issues, carried as PL-01 and PL-02.
- **The audit issue:** #895, `Audit: M6 T8 the image's own packages -- 17 findings (0 critical, 0 high)`. Labels `audit` and `punch-list`, milestone M6, a sub-issue of #655. `tools/box-check --issue 895`: 17 open, 0 fail.
- **`05`** is regenerated with the numbers; the pre-issue lint passes.
- **Stage-D pause:** the lane waits for the coordinator's stream briefs and drafts nothing under `projects/`.

### [Stage E] 13:26 to 13:29 — S1, #852 (`t8-streams.md` at `7c4867330b`)

- **Read first:** the stream brief whole (`git show 7c4867330b:docs/reviews/briefs/t8-streams.md`, not merged); plan § 6b E's three bullets again (the commit names its paths; a time is produced; prose through a quoted heredoc or the Write tool); `scripts/install:150-192` (`post_install` at `:189` for `TARGET=target`) and `config/path:39-40`.
- **Before** (13:27:57): an export of `8ebaf8daad` under `/workspace/tmp/m6-t8/s1-before-132757` (`df -i /workspace` 20%). Sourcing `config/options image` left `./build.pixelelated-GENERIC_X64.x86_64/image/system/opt -> /storage/.opt`.
- **The change:** `:109-110` moved into `post_install()`, `ln -sf` → `ln -sfn`, and the trailing `true` placed before the function, so no global line follows a function (`pkgcheck`'s intertwined warning).
- **After** (13:28:47): a fresh export with the fixed file laid over it (`cmp` equal):
  - links after sourcing: 0;
  - the hook in a scratch `INSTALL`: `opt -> /storage/.opt`, both on an empty tree and over an existing link to a directory;
  - the old `ln -sf` on the second shape nested `.opt` inside the directory.
- **`pkgcheck image`:** rc 0 with both copies.
- **Commit:** `43f6a81070`, one file, pushed. Outputs posted on #852; checkpoint on #655.

PROOF: 13:28 P16 S1: sourcing the old recipe leaves `image/system/opt`, the fixed one leaves none; the hook makes the link and replaces an existing one -- `.qa-scratch/t8/s1-before.txt`, `s1-after.txt`

### [Stage E] 13:30 to 13:33 — S2, #893

- **The hunt** (13:30:03): `git grep -n -E 'curl -[A-Za-z]*L|wget ' 8ebaf8daad -- 'projects/ROCKNIX/packages/*package.mk'` gives 19 lines (`s2-hunt.txt`): `mangohud`'s 6 (3 live, 3 commented) and 13 elsewhere, which are verdict lines.
- **Read before choosing:** `mangohud` v0.8.4's `subprojects/{imgui,implot,spdlog}.wrap` from the cached source (read only). Each names `directory`, `source_filename` and `source_hash`.
- **The fetch** (13:30:33), into the empty `/workspace/tmp/m6-t8/s2-fetch-133033`: all three equal their wrap's hash, and their top directories equal the wraps' `directory` lines.
- **Written:** three recipes in `mangohud-vulkan-headers`' shape, each checksum copied from the fetch output by a command; then `mangohud`'s `PKG_DEPENDS_TARGET` gains the three, and each `curl` block (and the commented `#curl` lines) gives way to an unpack from `${SOURCES}` behind a missing-file guard.
- **The tests:**
  - `scripts/get` into `.qa-scratch/t8/s2/sources` (13:31:12): rc 0 ×3, stamps equal; the shared cache has no file newer than 13:30;
  - one digit changed (13:31:30): rc 1, 10 `Incorrect checksum`, `Cannot get`;
  - the real `pre_configure_target` on the host (13:32:33): rc 0, the three directories each with a `meson.build`;
  - ImGui absent (13:32:46): rc 1, the guard's message, nothing extracted;
  - `pkgcheck` on four: 0 and 0;
  - `grep -c 'curl '`: 0.
- **Commits:** `4db09f6e2e` (the three recipes) and `1904e29d54` (`mangohud`), pushed. Outputs on #893; checkpoint on #655.
- **Criterion 14:** its `PKG_VERSION` grep now counts the three added lines (3; with `--diff-filter=M`, 0). Put to the coordinator on #655.

PROOF: 13:32 P17 S2: the three archives equal their wraps' hashes; `scripts/get` fetches them and refuses a one-digit change; the real hook unpacks them and stops on a missing one -- `.qa-scratch/t8/s2-*.txt`, `s2/sources`

### [Stage E] 13:36 to 14:06 — S3, #894 and #899

- **Read first:** the stream brief's S3 (`7c4867330b`, then `a5dae9f5d9` naming #899); `installer:1-60`, `:89-200`, `:300-345`, `:416-575` at `8ebaf8daad`; `generic-x64-vm run --help` and `qemu-args --help`; `tools/vm-serial`; T30's guest-cycle lines for the disk recipe.
- **The bench, and where it differs from the brief:**
  - The image `…20261022T235948Z.g069fc2704421…img.gz` was copied from `m6-t1-20261023/` to `/workspace/artifacts/m6-t8-20261024/`, `sha256sum -c` OK; its identity reads `build_commit 069fc270…`, `dirty: no`. `t8.qcow2` made by `gunzip`, `qemu-img convert`, `resize 16G`.
  - The target disks were attached over AHCI (`-device ahci`, `ide-hd` on `ahci.0` and `ahci.1`), not `if=virtio`. `get_device_unmount` (`:106`) lists only `/dev/sd*`, `/dev/mmcblk*` and `/dev/nvme*`, so a `/dev/vd*` target never reaches the menu.
  - The passing target was 6 GiB, not 2 GB. `/etc/installer.conf` sets `PARTSIZE_SYSTEM="4096"` (MB), so 2 GB fails at the system partition. It was grown live with the monitor's `block_resize`; libata kept the old size until a reset.
  - The failing target was an 8 MB raw disk, `/dev/sdb`.
  - The QEMU command is `qemu-args` plus the two disks (`/workspace/tmp/m6-t8/qemu-argv.txt`), with `--pidfile /workspace/tmp/m6-t8/qemu.pid`, VNC :28 and SSH 10041.
  - The dialogs were driven over the serial console by `tools/t8-installer-drive.py`, and its stripped transcripts are the evidence. Reads, the counts and every stop went over SSH with the QA key, provisioned over serial.
- **The guest's history, as it happened:**
  - Boot 1 at 13:40:18 (pid 4107561) ended by itself at about 13:43: the image's installer on MAIN MENU had powered it off. This is #899.
  - Boot 2 at 13:44:29 (pid 4146565). Reset from the monitor three times: at 13:48 to stop the loop; at 13:53 because whiptail holds the console raw, so Ctrl-\ is a key and the serial shell could not be reached; at 14:02 for the target's new size.
  - Stopped with `tools/vm-stop` at 14:04:07, rc 0 ("owned QEMU exited"). Census before 0 and after 0; the host file has an M6 line before and after.
- **#899 found** (13:45 to 13:49): the image's own installer (sha256 `9f437a91…`, equal to the tree's) starts copies of itself without end. `control-gen` prints nothing without a game controller, so `control.ini` is 0 bytes, `get_controls` is not found (`:41`), `GPTOKEYB` is unset, and `:46` runs `installer -c …` in the background. Filed as #899; the coordinator put it in S3 at 13:51, first and as its own commit.
- **#899's failing control** (13:55:58, the image's installer with a stub `poweroff` first in PATH so the guest stays up): `/proc/*/comm` counted 153 `installer` processes, then 234, 302 and 381 by 13:57:24. Every copy was killed, and the count was 0. Transcript `.qa-scratch/t8/s3/p899-control-original.txt`: 51 `get_controls: command not found` lines.
- **#899's fix:** a guard on `:43-47`, so the gptokeyb line runs only when `GPTOKEYB` is set. `bash -n` ok and the image busybox's `sh -n` ok. Commit `0602f598e9`.
  - No pad, no stubs (13:58:10): one `installer-899` and one `whiptail` at 13:58:36 and 13:58:42; `control.ini` 0 bytes.
  - A stub `control-gen` bind-mounted over `/usr/bin/control-gen`, printing control-gen's shape with `GPTOKEYB` set to a stub (13:59:32): `gptokeyb` ran once with `installer -c /storage/.config/gptokeyb/installer.gptk`; one installer, one whiptail. Unmounted after, and the real `control-gen` printed 0 bytes again.
  - `get_controls: command not found` (`:41`) still prints once before the first dialog, because the coordinator's scope was `:43-47` only.
- **#894's change** was re-applied on top of `0602f598e9` from its saved patch (`git apply --check` clean; the union of the two diffs equals the two changes). `bash -n` ok and busybox `sh -n` ok. Commit `467f19fc14`. The guest's copy is sha256 `956e2290…`, equal to the host's.
  - **Failing control, no stubs** (14:01:28, the #899-only script on `/dev/sdb`): it ended on "Install Complete — You may now remove the install media and shutdown." with 5 `Error:` lines in its log and no marker. The copy went to `/tmp/installer/part1` in RAM: 2.0 G, `/tmp` 52% full.
  - **Run 2, the failing target, no stubs** (14:00:34): the confirmation named `/dev/sdb ATA_QEMU_HARDDISK_8389kB`, and parted logged "The location 8396799 is outside of the device /dev/sdb." The dialog read "Install Couldn't Finish — The installer stopped while creating the system partition. The disk may be partly written. Check the disk and the cable, then run the installer again. The details are under View installation log." The marker held the step, and the log `# FAILED: creating the system partition`. One installer and one whiptail; `control.ini` 0 bytes.
  - **Run 1, the blank target, no stubs** (14:02:58): the confirmation named `/dev/sda ATA_QEMU_HARDDISK_6442MB`, and the run ended on "Install Complete". There was no marker and no `FAILED` line; the 2 `Error:` lines are parted reading the blank disk before the write. `blkid`: `/dev/sda1` `LABEL="ROCKNIX"` vfat and `/dev/sda2` `LABEL="STORAGE"` ext4; `/dev/sda1` holds `KERNEL`, `SYSTEM` and their `.md5` files, `syslinux.cfg` and `EFI`.
  - The sampler saw 2 `installer` processes at 14:03:09 and 1 at 14:03:19. On the guest, a pipeline's brace group runs as a forked copy under the script's own name (`t8-pipe` pid 3415, ppid 3413), and the gauge is `{ … } | whiptail`, so the second process is that subshell. It is not a background copy.
- **G-05 read from the bytes:** the installed system partition (`dd` from `t8-target.raw` at sector 8192, listed and read with `7z`) has the installation media's `syslinux.cfg` (`DEFAULT run`, `portable`, the media's console arguments), not the one `:322-329` writes (`DEFAULT linux`, `${EXTRA_CMDLINE}`). It also has the media's `EFI/BOOT/grub.cfg` and `fs-resize.log`, which records `/dev/vda2`. `cp -r /flash/*` (`:339`) runs after the generated config and replaces it.
- **The leads' verdicts** are in `02` § S3's leads.

PROOF: 13:59 P18 #899: the image's installer started 153, then 381 copies of itself with no pad; the guarded one runs one, and with a pad-shaped `control.ini` calls `gptokeyb` once -- `.qa-scratch/t8/s3/p899-*.txt`, the `/proc` counts
PROOF: 14:03 P19 #894: with no stubs, the 8 MB disk stops at "creating the system partition", the 6 GiB disk ends on Install Complete with ROCKNIX and STORAGE, and without the change the 8 MB disk claimed complete -- `.qa-scratch/t8/s3/run-*.txt`, `blkid`

### [Stage E] 14:16 to 14:31 — S3's addendum (#899) and S4 (#901)

- **Read first:** the coordinator's 14:16 post on #655 and `t8-streams.md` at `3e64156023` (S4, the S3 addendum); `scripts/mkimage:140-181` and `:290-293` (the media's `syslinux.cfg`, `grub.cfg` and `EFI/BOOT` copies); `tools/installer/package.mk` `post_install`.
- **S3 addendum:** `:41` now reads `command -v get_controls >/dev/null 2>&1 && get_controls`.
  - Under the image's busybox, `command -v` finds a defined function and skips an undefined one with status 127, which stops nothing because the script runs without `set -e`.
  - `bash -n` ok and busybox `sh -n` ok. Commit `412be96c77`.
- **S4, the reorder:** the `syslinux.cfg` heredoc and the two `EFI/BOOT` copies move into an `x86_64` arm of a second `case` after `cp -r /flash/*`. `syslinux -i` stays before the copy, and the `arm|aarch64` arm is untouched. The moved lines are unchanged and get no new checks.
- **The media's `EFI/BOOT`**, read on the guest:
  - `bootx64.efi` equals `/usr/share/syslinux/bootx64.efi` (`83199a7a…`);
  - `ldlinux.e64` differs: media `6b1ec643…` (`mkimage:180`, the toolchain's syslinux), image `2b34610e…`;
  - the media also has a `grub.cfg` (`mkimage:181`) that syslinux does not read.
- **The guest cycles** (`t8.qcow2`, AHCI targets, `--pidfile /workspace/tmp/m6-t8/qemu.pid`; each stopped with `tools/vm-stop` rc 0; census 0 before each; host-file lines at 14:18 and 14:27):
  - **Install 1** (14:19:13, pid 600819; the reorder alone; blank 6 GiB `t8-target-s4.raw`, `/dev/sda ATA_QEMU_HARDDISK_6442MB`; no stubs):
    - Install Complete; 0 `get_controls` lines and 0 "not found" lines in the transcript (the addendum's proof); 0 `FAILED`;
    - the target's `syslinux.cfg`: `DEFAULT linux` / `PROMPT 0` / `LABEL linux` / ` KERNEL /KERNEL` / ` APPEND boot=LABEL=ROCKNIX disk=LABEL=STORAGE `, with no `portable`;
    - `EFI/BOOT`: the image's pair, `83199a7a…` and `2b34610e…`;
    - the media's `/flash/syslinux.cfg` still reads `DEFAULT run`, sha256 `0d7363c7…`, before and after.
  - **Boot of install 1** (14:20:44, pid 830264): the disk alone, under UEFI, through the overlay `s4-boot.qcow2`. The overlays are grown to 16 GiB, the launcher's floor, so the raw disk is untouched.
    - It reaches the EmulationStation carousel at 110 s (`s4-boot-110s.png`), so the image's `ldlinux.e64` beside the toolchain's `bootx64.efi` boots.
    - The serial console does not answer: the generated `APPEND` carries no `console=ttyS0`.
  - **Boot of S3's pre-fix disk, the control** (14:24:08, pid 865097): it boots, and `/proc/cmdline` reads `root=/dev/sda1 init=/sbin/init usbcore.autosuspend=-1 BOOT_IMAGE=/KERNEL boot=LABEL=ROCKNIX disk=LABEL=STORAGE portable quiet console=ttyS0,115200 console=tty0`. That is the media's `APPEND`, so syslinux's EFI loader reads the root `/syslinux.cfg`.
- **What the reorder exposed:** the generated `APPEND` ends in `${EXTRA_CMDLINE}`, which nothing sets at run time.
  - `tools/installer/package.mk`'s `post_install` runs `sed "s/@EXTRA_CMDLINE@/${EXTRA_CMDLINE}/g"` over the script, but the script carried no placeholder. Both halves are upstream's `09810c3ece`.
  - GENERIC_X64's value, through `config/options installer`, is `quiet console=ttyS0,115200 console=tty0` (`devices/GENERIC_X64/options:76`).
  - With the reorder alone, an installed disk boots without `quiet` and without its serial console.
  - Put to the coordinator at 14:26 on #655. Proposed: `@EXTRA_CMDLINE@` on the moved `APPEND` line, in S4's commit.
- **The variant**, `@EXTRA_CMDLINE@` on that line, with the recipe's own `sed` applied to the guest's copy with GENERIC_X64's value, as `post_install` does (sha256 `6cb5a145…`):
  - **Install 2** (14:27:55, pid 893477; blank 6 GiB `t8-target-s4b.raw`; no stubs): Install Complete, with 0 `get_controls` and 0 "not found" lines. `syslinux.cfg`: `DEFAULT linux` … ` APPEND boot=LABEL=ROCKNIX disk=LABEL=STORAGE quiet console=ttyS0,115200 console=tty0`. The media's file is unchanged.
  - **Boot of install 2** (14:28:38, pid 901487): `/proc/cmdline` reads `root=/dev/sda1 init=/sbin/init usbcore.autosuspend=-1 BOOT_IMAGE=/KERNEL boot=LABEL=ROCKNIX disk=LABEL=STORAGE quiet console=ttyS0,115200 console=tty0`, with no `portable`. `BUILD_ID` `069fc270…`; `/flash` holds the installed system files.

PROOF: 14:30 P20 #901: the installed disk carries the generated `syslinux.cfg`, not the media's, and boots on it under UEFI (`/proc/cmdline` without `portable`); S3's pre-fix disk, the control, boots on the media's (`portable`) -- `.qa-scratch/t8/s3/s4*-after.txt`, `s4b-boot-cmdline.txt`, the boot frames
PROOF: 14:19 P21 #899's addendum: with no pad, the installer's serial transcript carries no `get_controls: command not found` -- `.qa-scratch/t8/s3/run-s4-6g.txt`, `run-s4b-6g.txt`

### [Close] 14:46 to 14:51 — accepted, the marker, the payloads retired

- **Accepted** by the coordinator on #655 at 14:46 UTC, at `13394550d6`. #895 is closed as completed.
- **The marker:** at 14:48, `tools/write-completion.py` refused (`ticked=0 open=19`): the body was last edited at 14:36:56 and the acceptance's ticks had not landed. Put on #655. The coordinator ticked all nineteen and posted an erratum at 14:51.
- At 14:51:14 the writer read #895 back as closed, completed, 19 ticked and 0 open, and wrote `tracker-final-readback.json`, `tracker-completion.json` and `audit-completion.json`. `tools/lint-audit-artifacts`: `PASS`. `tools/ceremony-check` reads the marker as the last audit.
- **Retired** under D-INFRA-022 at 14:49 (`c146da433d`): the S3 and S4 payloads, 15,791,276,032 bytes, each listed with its hash in `docs/vm-qa-log.md`.

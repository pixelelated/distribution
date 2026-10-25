# Analysis — M6.P2 T27, the H700 device (RG35XX SP, RG SP) (#674)

## Executive summary

**The H700 device is current with upstream, and nothing in the 28 behaves wrongly.**
- **The pins:** u-boot `v2026.01`, the suspend stub `712653d11230`, atf 2.12.0 and the kernel 7.2 are all unchanged at `651150fc88`.
- **The configuration is upstream's, with a base:** 12 / 13 lines from upstream's copy. Those are the fork's six settings (D-SYS-002/003/004) and four upstream commits a base merge brings.
- **`update.sh`'s memory selection fails safe:** any voltage but the two known writes no loader.

The findings are:
- a merge seam on atf's checksum and URL (F-02, for T25);
- the rule's SIMD column, which describes the arm FPU for an aarch64 build (F-03);
- the fresh card's hand-activated `/dtb.img` (F-04, a design question with #44);
- firmware files both built in and installed (F-05);
- dispositions for the `.disabled` patch, 13 placement-carried trees and a rule deleted upstream (F-06 to F-08);
- two clarity notes and an erratum (F-09 to F-11).

No `bug`. Removals none (D-WORKFLOW-209). The seat's grading is at stage C.

## Acceptance-criteria scorecard

| Criterion (#674) | State | Evidence |
| --- | --- | --- |
| `00` to `05` | `05` at stage D | this folder |
| The lint | at stage C and at close | — |
| The seat | at stage C | `second-opinions/` |
| The punch-list issue | stage D | — |
| `reviewed-at` / `fixed-at`; the empty diffs | `ed7fd0ea50`; r16 empty | `02` § The runs |
| `01` § Scope | complete | `01` |
| `## Coverage` 28 | 28 | `02` |
| § The pins | six rows | `02` |
| § The configuration | 12 / 13 attributed | `02` |
| § The loader and the tree | written | `02` |
| § The device trees | 15 rows and the `.disabled` row | `02` |
| § The runs | 17 | `02` |
| `00` clean | so far | `00` |
| `04` Q4, Q2, Q3, Q6, § Second opinion | below; the second opinion at C | this file |
| `proved:`; `question:` | 14 proofs; the items at D | `02`, `05` |
| The retro; the checkers | stages G, H | — |

## Risk assessment

| Risk | Likelihood | Impact | Note |
| --- | --- | --- | --- |
| A merge takes upstream's atf URL with T5's checksum, or the reverse | Medium at the next base merge | every H700 build refuses its atf fetch | F-02, for T25 |
| A fresh card is flashed without the hand step | Medium for anyone new | the card does not boot | F-04; the runbook covers it |
| A third memory type or a failed regulator read | Low | no loader update: the card keeps its old loader | `update.sh:52`; fails safe |
| A firmware change in the list is not rebuilt | High until #836 lands | the image keeps the old list | T5's F-17 |

## Coverage boundary

- **Read:** all 28 at `8ebaf8daad`, with the 15 trees whole and the configuration by diff against upstream's copy.
- **Read beyond the 28,** for the questions: the project `bootloader/mkimage`, `config.xml`'s H700 lists, `distributions/ROCKNIX/config/functions:224`, `scripts/unpack:143-159`, the ROCKNIX `atf` and `linux` recipes, `device-builds.md`'s device table, and device-facts L15, L16 and L29. T5's atf commit was read on `feature/m6-build-engine-652` with `git show`.
- **Not done:**
  - no network, so the authors' releases are `CANNOT`;
  - no build, so whether each tree's `#include` exists at 7.2 is a build fact;
  - nothing on a unit, so the RG35XX SP's tree name, the cores' crypto extension, and the watchdog and ramoops on a board are open items to test or rows (L29).
- **Not this slice's:** the 32 live kernel patches and the ramoops patch (T41, #688), the u-boot patches (T40's `patches-and-configs`), the H700 quirks (T29, #676), and the overlay source (T11).

## Second opinion

At stage C: one seat, GPT-6 Astra at `max`, a probe first, then one refutation pass. Every item is graded here.

## Finding Verification

| Finding | Re-read | Verdict |
| --- | --- | --- |
| F-01 | r07; `git log -S` for each pin | stands |
| F-02 | `atf/package.mk:16-28` at `8ebaf8daad`, at `651150fc88` and on T5's branch (`430abc8f66`); D-WORKFLOW-194 | stands; cited, not re-filed |
| F-03 | `options:9-17`; `device-builds.md:22-23` | stands |
| F-04 | `mkimage:45-50`, `:88`; r10; `update.sh:26-32` | stands |
| F-05 | `kernel-firmware.dat`; `package.mk:223-243` | stands |
| F-06 | `scripts/unpack:143-159`; `fad6d7d27a` | stands |
| F-07 | `config.xml`'s lists; r13 | stands |
| F-08 | r15; `899193e5af` | stands |
| F-09 | `options:77-84` | stands |
| F-10 | the two recipes' diff (two lines) | stands |
| F-11 | `mkimage:18-30` | stands |

## Renovation face

### Q1 Modernize

- **The three u-boot recipes against one parameterised recipe (F-10).** DDR3 and DDR4 differ only in `PKG_NAME` and `PKG_UBOOT_CONFIG`; the wrapper loops over `${SUBDEVICES}`; the stub reads each recipe's defconfig. *The design sentence, deferred to the coordinator:* a single recipe taking the memory type from the SUBDEVICE would remove the duplicate, but the wrapper, the stub and `config.xml` name the two packages, so it is upstream's to change, not a fork edit.
- **`update.sh`'s `vdd-dram` selection against a declared memory type.** The type is inferred at update time from the regulator (`:35-48`), and fails safe. A declared type would need a per-unit record the image does not have.
- **`/dtb.img` on a fresh card (F-04).** `mkimage` names it and never writes it; the runbook's hand step activates it. *The design sentence, for the coordinator:* the image step could write a default `/dtb.img` per SUBDEVICE, but which tree a unit needs is a fact about the unit, which is the question #44 (D-WORKFLOW-033) parks. Cited, not reopened.

### Q2 Standards

- **`TARGET_CPU_FLAGS` against the rule's table (F-03).** `.claude/rules/device-builds.md:22-23` says *cortex-a53, crypto-neon-fp-armv8* for both units. `options:10` reads `TARGET_CPU_FLAGS="+crc+fp+simd"` on aarch64, and `options:17` reads `TARGET_FPU="crypto-neon-fp-armv8"` on arm. **The table quotes the arm FPU for an aarch64 image, so the table is wrong in what it describes.** Whether the aarch64 flag should add `+crypto` depends on whether the cores carry the extension, which no row records. This is a rule-edit lead for the coordinator and an open item to test.
- **The `.disabled` patch (F-06):** a file the build never reads, 31 % of the slice.
- **The configuration's `tier_note: fork-written`:** the inventory's reading of a file the fork touched once (`cbf75c0b06`). Cited, not re-tiered (T10's).
- **The identical u-boot bodies (F-10)** and the identical patch pairs (T41's, outside the slice).

### Q3 Bugs

- **`update.sh`'s thresholds are not a bug.** At a voltage that is neither 1,200,000 nor 1,100,000 µV, or with no `vdd-dram` regulator or an unreadable `microvolts`, `UBOOT_BIN` stays empty and `:52` writes nothing. The unit keeps the loader already on its card. A missing dt-id skips the `dtb.img` copy (`:29`). No input makes it write a loader it should not. `Already written:` the two units' cards carry the loaders and trees L15 and L16 record; nothing written by this script is wrong, so nothing is inherited.
- **T5's F-17** (a `kernel-firmware.dat` change does not move the stamp): #836's, cited, not re-filed.
- **atf's missing checksum (F-02):** fixed on T5's branch (D-WORKFLOW-194); the merge seam is recorded.

### Q4 Package currency

The pin table (`02` § The pins), with its verdicts:

| Unit | Verdict |
| --- | --- |
| u-boot-DDR3, u-boot-DDR4 `v2026.01` | current with upstream; set 2026-06-08; the author's release `CANNOT (no network)` |
| the wrapper `1.0` | no source |
| h700-suspend-stub `712653d11230` | current with upstream; set 2026-09-17 |
| atf 2.12.0 (H700) | current with upstream's pin; the oldest here (2025-07-13); the generic recipe is at 2.15.0; the checksum seam is F-02 |
| kernel 7.2 | current with upstream; set 2026-08-17 |
| the configuration | 12 / 13 from upstream's copy: the fork's six (`cbf75c0b06`) and upstream's four (`c0980b2b71`, `5f56cd5150`, `6fbefc45c6`, `dcafa74090`) |
| the trees | the include targets are mainline board files; their presence at 7.2 is a build fact, and the patches that add them are T41's |

`tools/fork-package-freshness` is the RC's check for the authors' releases (D-WORKFLOW-024), named, not run.

### Q5 Efficiency

- **The configuration's size against upstream's copy:** equal but for 25 lines.
- **The 15 trees against the two units:** 2 are a shipped unit's; 13 are other H700 handhelds', compiled into every image and carried by placement (F-07). Removals none.
- **The firmware list against `CONFIG_EXTRA_FIRMWARE`:** the same 13 files both ways, no misses. The root-filesystem copies duplicate the built-in ones (F-05).

### Q6 Dead ends

| Unit | Disposition |
| --- | --- |
| `0203-...patch.disabled` | disabled at birth, upstream's; its removal is #346's class decision |
| the 13 non-unit trees | carried by placement (D-WORKFLOW-185) |
| `80-clock.rules` | gone upstream (`899193e5af`): settled by the next base merge |
| `kernel-firmware.dat`'s root-filesystem copies | recorded (F-05); the list is upstream's |
| everything else | live |

### Q7 Clarity and structure

- **Which unit boots which loader and tree:** a reader of the device directory cannot tell. `update.sh` decides by voltage and dt-id at update time; the rows and the rule's table say it for the two units (F-09).
- **Where `/dtb.img` comes from:** `update.sh` on an update, the runbook on a fresh card (F-04).
- **`options`** does not say why zram and swap are 0 (F-09).
- **The `vm-first` answer for every device fact:** L15, L16 and L29, read; nothing new asked of a unit.

## Instruction File Recommendations

Proposals for the coordinator:
1. **`device-builds.md`'s device table** names the arch its SIMD column describes. For H700 that means aarch64 `+crc+fp+simd`, with the arm build's `crypto-neon-fp-armv8` as a separate value (F-03).
2. **For briefs and acceptance scripts:** a history count uses an explicit cutoff (`--since='YYYY-MM-DDT00:00:00Z'`), never a bare date (the friction line of 08:11).

## Quality self-check

- **Every figure comes from a timed run** (r01 to r16, r14b), and every finding is re-read at its lines.
- **Every recipe read was masked;** `h700-suspend-stub/package.mk:43` appears nowhere unmasked.
- **What would change the verdicts:**
  - an upstream bump between the two hashes;
  - a writer of `dtb.img` in the image step;
  - a branch in `update.sh` that writes a loader for a third value;
  - a row naming the RG35XX SP's tree;
  - a second fork commit on the configuration.

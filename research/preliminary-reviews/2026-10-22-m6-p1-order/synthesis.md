# Preliminary synthesis: the renovation order (advisory)

**Run:** `2026-10-22-m6-p1-order`. **Format:** three-model preliminary review,
advisory; no vote, no approval, `formal_council_complete: false`. **Input:**
`docs/reviews/order.md` at `d2f631e801` (the first version, 43 slices) with
`inventory.md`, `areas.json` and `plan-for-the-plan.md` (`source-manifest.json`).
**Seats, verified before each next call** (`verification.md`): claude
(`anthropic/claude-fable-5.1`, xhigh), gemini (`google/gemini-3.8-flash`,
high), gpt (`openai/gpt-6-astra`, max, provider pinned).

## Readiness

All three: **ready with named changes**. None found the gates or the first
three out of bounds. All three found the review depths in conflict with the
order's own sensitive-file lists, and the read counts hiding work (patches,
prose, table rows). All three found T10's prerequisite unenforced. These
three are the changes that decided the second version.

## Material findings, source-checked

Each finding that claimed a fact about the tree was checked with a command
before it changed the order:

| Claim | Seat | Check | Result |
| --- | --- | --- | --- |
| the launch entry is in `views/` | claude | `git grep -n launchGame es-app/src/views` at the pin | `ViewController.cpp:483: if (game->launchGame(mWindow, options))`: confirmed, moved to T2 |
| `es_systems.cfg` is generated in the distribution | claude | `git grep -n es_systems projects/ROCKNIX/packages/virtual/emulators/package.mk` | `mk_es_systems` at line 1726: confirmed, moved to T3 |
| ES's `patches/x86_64` may be a mislabel | claude | `scripts/unpack` lines 127-128; `grep PKG_PATCH_DIRS` in the ES recipe | `PATCH_ARCH="x86"` on x86_64 and no `PKG_PATCH_DIRS`: the patch never applies; the inventory is right (a lead for T41) |
| GENERIC_X64 might boot from the unreached `grub` | claude | `grep BOOTLOADER projects/ROCKNIX/devices/GENERIC_X64/options` | `BOOTLOADER="syslinux"`: `grub` unreached is consistent |
| `glibc`, `virtual/libc`, `openssl`, `squashfs-tools`, ... mislabelled unreached, so T3 would delete the toolchain | gemini | per unit: the ROCKNIX override exists? the name in the plan? which generic paths are unreached? | Each named package is built, from its ROCKNIX override, and only the shadowed generic copy is unreached. `quilt`, `gcc-aarch64` and `binutils-aarch64` appear in no plan and are referenced nowhere. **Not a mislabel**, but a removal hazard: `shadowed_by` added to the inventory (620 rows) |
| the fork-written patches sit in Local tables | claude, gpt | `tier_note` counts in `inventory.json` | 41 files; the first version had already moved the proxy's, RetroArch's and two kernel configurations; the rule is now explicit in `order.md` |

## Disagreements between seats, and the resolution

- **Dead-end tables.** Claude wanted them early (T36 to T38 beside T3 and
  T4). Gemini wanted the patch dead ends late, since they shrink only the
  patch tables. GPT kept T3 and T4 after T10. Resolution: the package and
  device dead-end tables at T14 to T17, after the security cluster. They are
  Local and parallelizable. The patch dead ends sit with the patch tables
  (T41). Claude's alternative is recorded in `order.md`.
- **Small slices.** Claude would merge some; gpt advised against merging
  merely for size. Not merged.
- **The H700 kernel patch.** GPT would move it into the device slice. It
  stays in the kernel provenance table (T42), which T20 names.

## Remaining questions for the maintainer (pass 7)

1. The shipped-device set: `device-builds.md` (five devices) or plan § 5,
   which also names SM8250, S922X and SM6115 as built.
2. Whether `backuptool` (T7) and the system services (T12) also gate `0.1`
   beside T1.
3. The cost of the depths: 13 slices are now Extended (T1 to T3, T5 to T13, T24) (OpenRouter credit,
   plan § 11 Q3).

## What this review does not establish

It is advisory. It does not approve the order. The maintainer's yes does
that, recorded on #641 and in D-WORKFLOW-184. It does not verify the lens
scores, which were not embedded, and it is not an audit of the survey's
tools. Those tools are read in T5.

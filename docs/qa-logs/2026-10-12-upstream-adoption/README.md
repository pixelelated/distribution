# ROCKNIX 20261001 source intake — #563

Owner selection is recorded as D-WORKFLOW-161. The next candidate uses the exact
stable commit `c445081a59518f37d9776e5412dd7b14910696f7`; later upstream/next is
excluded. This is source review and adapted host proof, not image acceptance.

## Source identity and preservation

- Previous upstream base: `9fd38fa87094d4f0e956d03ac6c660fe4fd5e9d6`.
- Fork before source merge: `ca5d034488f58e4a755a30e760df24e9fd6d5e3c`.
- Merge: `f370dc87873fecb683c6af73d70a2f377715f47f`, on
  `feature/m7-rocknix-20261001`, with the exact stable commit as second parent.
- Intake: 11 commits including merges, 12 upstream paths, 11 final changed paths.
  Every imported path matches stable bytes except DuckStation, which retains the
  pre-merge fork recipe byte for byte. Every other tracked path is unchanged.
- One manual conflict, within the declared maximum of three. DuckStation already
  uses `install -m 0755`; retain that equivalent permission fix, its newer pin and
  `STRIP=true`, instead of reverting to upstream's older recipe.

All imported source was read before running checks. `source-checks.json` records
path hashes, expected references and preservation. Reproduce the scope with
`git diff --name-status f370dc8787^1 f370dc8787` and verify stable ancestry with
`git merge-base --is-ancestor c445081a59518f37d9776e5412dd7b14910696f7 f370dc8787`.

## Changed inputs and required qualification

| Area | Finding | Required new proof |
| --- | --- | --- |
| SM8250 Mangmi | Two device trees, charger patch, wireplumber/UCM and SoC-specific DP startup guard. | Relevant device/package build coverage; do not assign these as a Nova fix. |
| Common Linux 7.2 | DP audio-prepare patch also enters SM8550's kernel; DRM_MSM and DRM_MSM_DP are enabled there. H700 uses this source version but does not enable MSM; GENERIC_X64 uses 7.1.2. | Rebuild Nova kernel, exact installed bytes and appropriate DP/audio evidence. |
| ABL | 1.1.9 to 1.2, pinned archive checksum in the recipe; selected for SM8550. | Fresh package/firmware/actual-slot chain checks. #528 implementation-source/licence gap remains; no claim that it fixes #558. |
| FEX | Nixpkgs pinned to b6018f87da91d19d0ab4cf979885689b469cdd41, FEX source unchanged. | Fresh native outputs, dependency/source custody and capability checks. |
| Steam | Runtime refresh removes working runtime before replacement download. | Repair #564 and prove failures, recovery and success before candidate acceptance. |

Recipe/patch hashes invalidate corresponding package inputs; shared-package input
changes may rebuild additional targets even for device-specific data. Determine
actual stamp invalidation in the new frozen build, not by reusing old receipts.
Accepted caches were not modified and no full cache copy or build was launched.

## Completed host checks

- `tools/pkgcheck` succeeds for FEX, rocknix-abl and DuckStation (three receipts).
- `bash -n` succeeds for those recipes and the Steam installer.
- Common kernel patch applies with `patch --dry-run --batch --fuzz=0 -p1`
  to isolated copies of dp_audio.c from both architectures of accepted H700 and
  SM8550 caches, with no offsets/fuzz. This is applicability, not compilation.
- Non-patch source whitespace check passes. Raw `git diff --check` reports spaces
  that are unified-patch context prefixes in two imported patch files. Preserve
  those upstream bytes; both original result codes/output are in whitespace.json.

## Confirmed regression — #564

Can this be done on the VM? Yes. The initial controls here are adapted host tests:
extract only `install_steam_runtime_arm64` from each exact source, set STEAM and
RUNTIME_DIR to a disposable directory containing a known-good runtime marker,
stub curl to return fixture-version, stub wget to return9, and invoke the function.
No full installer, /etc/profile, account, network transfer or owner device is used.

Both functions return1. Accepted bc9dfe8141 preserves the old marker; stable20261001
deletes it. `steam-failure-control.json` binds script/function hashes and outcomes.
Private fixture scripts remain under
`/workspace/tmp/pixelelated-upstream-adoption-20261012/steam-failure-control/`.
The failing imported code remains isolated on the qualification branch. It has
not been merged into next or shipped. #564 requires staged replacement, rollback,
interruption/retry and space controls, followed by installed VM qualification.

## Continuation

1. Repair #564 on the qualification branch and retain source-bound regression proof.
2. Finish #493 mandatory retention/capacity lifecycle before any full cache copy/build.
3. Freeze the resulting source, qualify clean and retained GENERIC_X64 behavior,
   cloud protocols/time-to-play and required independent review; resolve findings.
4. Build H700 then SM8550, qualify changed native/kernel/ABL inputs and obtain any
   new named device-action authority. Finish #528/#344 publication gates.

Owner testing of accepted bc9dfe8141 continues separately. No public RC allocated.

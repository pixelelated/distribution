# Source-derived save layouts and coverage — #515/#520/#521/#522/#523

This packet retains qualified M7.P5 source work, integrated through #508 in
`e6645cb5ea` and published with evidence at next `bc4ae05d30`. #515 and source
fixes #520/#521/#522/#523 are closed; #507's independent audit is next. It contains synthetic fixtures and public/package
source references, never a personal cloud inventory. It is not assembled-image
adoption, gameplay compatibility, or the independent audit.

## Case disposition

[source-cases.md](source-cases.md) traces a finite set through public ROCKNIX
release20261001 and the exact packaged writers. Legitimate standalone paths
remain in place; path names alone cannot identify the historical unpublished
extra wrapper or the unique consumer of a flat save/state/image. The current
relocation disposition is instructions and explicit root selection, with no
repair action or repair-screen completion claimed. Concrete coverage defects
are fixed separately, not dismissed as ambiguous layouts.

## #520 — source, host and affected VM proof accepted

Product commit `1ee8e5199da0bc02e6aa4ebff94b951f5e8b4804` covers PPSSPP savedata,
DuckStation cards and Mupen64Plus native/alternate slots across saves, content
transfer/list/count/match and bounded metadata checks. Old remote content copies
must not replace local progress. Both rule templates and custom-rule precedence
are exercised. No file relocation or remote historical-copy cleanup occurs.

- [Focused qualification](coverage/qualification.json):39PASS,0FAIL on final03.
  Fifteen accepted old-source failures demonstrate omitted saves, unsafe content
  transfer/media treatment and shallow classifier gaps. Failed fixture startup
  is retained separately and is not a product-defect reproduction.
- [Root source review](coverage/root-source-review.json): committed hashes,
  22-file install map, actual failing controls/startup witnesses and retirement.
- [Affected regressions](coverage/affected-regressions.json):21 content checks,
  30 validator checks and nine actual-image BusyBox find/awk controls. The last
  are isolated host fixtures using the image applets, not a guest/gameplay claim.
- [UI evidence index](ui/evidence-index.json): actual owned GENERIC_X64 source
  overlay: ten reviewed frames, one rejected fixture frame, no pending #520 case. EN640 and FR1280
  representative layouts; no full locale/panel Cartesian coverage claim.

Base validator depth remains3. Only observed `psp/PSP/SAVEDATA` and
`psx/duckstation/memcards` receive bounded supplementary metadata reads;
unknown deeper content is not marked inspected. The25-second budget,4096-entry
and2MiB per-listing limits remain. Files found means readiness within that
scope, not byte integrity or emulator compatibility.

## #521/#522/#523 — source, package and native capture qualification

The exact DuckStation action/writer and shipped configurations put default
captures in application data outside the saves tree. #521 corrects new default
capture placement on clean and retained-default configs while preserving custom
paths and historical files. Old captures are not automatically moved or claimed
backed up; that requires separate deliberate placement. Both game and Tools
entrypoints must be exercised.

Actual guest preparation reproduced the exact pinned AppImage installed with
mode0644 and direct execution refusal126. #522 owns the recipe mode correction,
original/fixed install control and real target entrypoint proof before #521's
screenshot test. A guest-only chmod cannot close that package defect.

The complete121 bundled ELF/plugin closure then found one missing target
library, `libcom_err.so.2`; #523 adds the existing target package dependency.
Its normal build/install passed in an isolated owner with accepted build roots
read-only. The helper and package-mode source passes31host controls against four
original failures. [Native proof](duckstation-captures/vm-ui/README.md) verifies
the unchanged hotkey writes rendered PNGs to default and explicit custom paths,
and ordinary save backup/restore preserves the generated default PNG. Existing
captures/custom settings remain unchanged. This uses an original synthetic
reset ROM, not commercial game/BIOS or save-compatibility testing.

The guest/compiler were retired after final completeness review, with compact
receipts; the two owned scratch paths are absent. Product integration commit
`e6645cb5ea5ae3c7f699390a74b22d098fbeb7fb` carries the exact26 package changes
and the matched ES pin; ES4e410dc9 is published on its integration branch.
Distribution source and evidence are published on next `bc4ae05d30`. No firmware build, physical
action, private backend, independent audit or release publication has started.

## Tracker and remaining release gates

[Tracker receipts](tracker/) retain exact body hashes/readbacks. M7 orders
#515 with children520/521 and521 prerequisites522/523, then508 integration,507audit,
engineering firmware/public adoption and final H700-then-SM8550/release gates.
The owner test handheld separately requires519/D-CLOUD-182 controlled alignment
and relevant residue disposition before any next update transfer/reboot.

# SM8550 ABL checksum retry: source custody

This retains the reviewed immutable source packet for #600 at
`/tmp/pix-m7-sm8550-abl-retry-20261015`, seal `a9eebe1cdad405e46c45719624284ed15c8482673a9fa01e70a20f678bc93bf7`.
Its source-only review snapshot was UNRUN when sealed. Root has since begun
its separately supervised create/preparation lifecycle; this custody packet
does not capture or qualify that execution. Source is exact commit
`9aa7affee9d4ad5e69725cab20b6d7ad84d93dea`; the intended fresh branch/checkout
is `build/m7-pixelelated-sm8550-05` and fresh owner is
`/workspace/tmp/pix-m7-sm8550-refresh-20261015-02`.

`source-packet.tar.gz` contains all **75 original regular files**: 74 sealed
payloads plus the original top-level SHA256SUMS, and nine directories. The
peer source review is already retained under `source-packet/peer-review/`,
including its seal `defc80d19ee92f9a9a0e1c3127ca3540e44af41e5f1584eeb7620207a630235b`. Nothing was appended to or rewritten in the
immutable source packet. `source-seal.SHA256SUMS` is an exact convenience copy;
its relative paths refer to the archived packet, not this outer directory.

The packet preserves the old SM04 owner's consumed cache-copy 0 followed by
consumed partial-build 2/0/2, launcher2, as failed history. It binds only the
one ABL recipe-checksum product change versus accepted H700/VM f863, with
new checkout ordinary admission8923610c and checker65ab. Independent cache/Nix
copies, all 12 normal package cleans, canonical ARM then AArch64 build,
current FEX inputs/14 ELF checks, exact five ABL files and independent firmware
readback remain required. The historical ARM manifest is only a comparison
baseline; no successful parent image or new ARM acceptance is invented.
Original static checks exited0 (93 checks), and finite peer source review found
no concrete blocker. Those are source findings, not execution qualification.

`publication-originals.tar.gz` separately retains the exact evidence.json and
e32-hosted-complete.json from `/tmp/pix-m7-600-publication-20261015`. They describe
producer9aa7 as a published ancestor of e32e8c6f, with the three recorded e32
hosted runs completed successfully. **This is the historical publication
receipt before the ca888 documentation follow-up**, not a current-HEAD receipt
or RC/publication clearance. The copied files retain their original wording.

`member-manifest.json` records both archives' exact member names, original
locators, SHA256/size, permission modes, UID/GID, user/group names and nanosecond
mtime. Readback compared every member with its original using stat.S_IMODE and
exact decimal PAX timestamps, then rechecked the originals unchanged. No archive
was extracted. No links, special files, caches, firmware or live-owner payloads
are included. The source/peer seals and publication receipt hashes were checked.

This retention step ran no preparer, admission, cache operation, compiler,
container, VM, installed reader or source collector. Root owns all actual
execution and later acceptance. No physical boot, gameplay, RC, #528 source
custody completion or release clearance is claimed. Outer SHA256SUMS binds
this compact retention directory; root owns staging/integration.

# Upstream disposition — read 2026-10-14 UTC

Fresh read-only GitHub intake (request, timestamp, original exit, and response)
is retained under evidence/. Search/release/history/PR records explicitly project
selected fields; irrelevant API metadata, release assets, and unrelated issue bodies
are omitted. Owning issue/comments and the selected Valve issue/comments are complete.
No upstream post or product/pin change was made.

- ROCKNIX latest release remains **20261001**, and next is
  **becc8cb2a97b8b44b25d39dd5b6aa8f77b0af1c5**. Its client function is byte-identical
  to c624: SHA256 `037fa82e1ccbdc875b10aafe67649b02b83857b887226a94e77ac3891c3388d3`.
  [Exact upstream source](https://github.com/ROCKNIX/distribution/blob/becc8cb2a97b8b44b25d39dd5b6aa8f77b0af1c5/projects/ROCKNIX/packages/virtual/emulators/sources/Install%20Steam.sh).
  This is a local installer repair candidate, not a missing upstream client fix
  established by a newer release.
- Source intent: ff40ff1897fa renamed/refactored the ARM installer; f546596cc8a8
  extracted the directory-based skip/direct extraction into a function;
  d50674f4dee9 added exit/error handling while retaining that predicate. The later
  Proton/container changes do not replace it. #3258 is merged at September 1,
  #3204 at August 18; their stated scope is Proton/container/FEX setup.
  [3258](https://github.com/ROCKNIX/distribution/pull/3258),
  [3204](https://github.com/ROCKNIX/distribution/pull/3204).
- Bounded current searches: ROCKNIX PR `steamrtarm64` returns 0; `Steam install`
  returns 17 (all 17 retained). Valve linuxarm64 issues return 2, about UI/codec
  behavior. Install-manifest search returns 113 and only its first 30 were read;
  bootstrap/corrupt returns 28. This is not an exhaustive absence claim.
- [Valve #11602](https://github.com/ValveSoftware/steam-for-linux/issues/11602)
  concerns a corrupt x86 CEF/sniper runtime in a running client. A Valve comment
  on January 15, 2025 says the beta forces full checksum verification after
  expansion trouble; the report was closed March 8. It does not repair ROCKNIX's
  standalone ZIP function or specify a read-only ARM64 legacy classifier.
  [Exact maintainer comment](https://github.com/ValveSoftware/steam-for-linux/issues/11602#issuecomment-2593789488).
- [Valve launcher documentation](https://repo.steampowered.com/steam/) describes
  a minimal bootstrap whose updater downloads further components. The current
  [steam-for-linux README](https://github.com/ValveSoftware/steam-for-linux/blob/master/README.md)
  lists x86_64/AMD64 requirements; its inspected bytes do not define an ARM64
  `.installed` readiness contract. That absence is limited to the inspected sources,
  not a claim that no ARM support or internal contract exists.
- The local packaging input is `steam-launcher_1.0.0.85_amd64.deb`, SHA256
  `b44634a6a604ca7c8b23809d0f2a921a0348bb2081c8cb8944116d0799872b70`.
  The [official stable directory](https://repo.steampowered.com/steam/archive/stable/)
  now lists **1.0.0.87** (June 26, 2026). Its binary/source archive was not fetched
  or decoded. This is the packaged amd64 launcher, not the dynamically fetched
  ARM64 client selected by install_steam_client_arm64. A launcher bump alone is
  not evidence that this function or its preservation contract is fixed.
- The inspected [steam-runtime README](https://github.com/ValveSoftware/steam-runtime)
  documents separate client/runtime distribution and game-runtime setup. Runtime
  release/version changes cannot substitute for the ARM64 client transaction's
  selected manifest, archive inventory, or native qualification.

No new dependency is presently added. A future bounded reader can use the existing
Python3 package (already declared by Steam), but selected-image module/tool closure
and full-caller/native acceptance remain coordinator-owned. Do not copy an updater
implementation or advertise signature verification merely because TLS/hash/CRC
checks passed.

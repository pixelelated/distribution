# M7 #528 engineering input disposition — 2026-10-11

Eleven missing recipe declarations now name their source-backed primary terms.
HarfBuzz ICU inherits MIT from HarfBuzz; the exact pinned builder resolves it
as MIT/14.3.0. It was a static-collector gap, not a missing runtime declaration.
[The disposition map](dispositions.json) hashes every available retained notice
used here and records the scope and remaining work for all17 prior gaps.
Five aggregate bases remain unresolved: common, GLSL, RetroPie and slang shader
collections, plus ABL. No component, emulator or capability is removed; the
engineering image retains these exact versions with publication held. Root
licence declarations do not clear bundled/vendor inputs or corresponding source.

The idtech launcher recipe now fetches the existing Doom archive through the
normal get/checksum/cache path at upstream commit
4cb65b687c90f56856e9d6a55e51f56a09955699. The download and installed archive match
prior firmware SHA256 ff35cde05801cfb27005229a6c55f20130ffa8f026ca27d7717c03152634e168
(1,689,157 bytes). Installation copies the verified archive without networking.
The archive contains only doom.wad, not a licence notice. The recipe declaration
covers launcher scripts; game-data redistribution terms remain a #528 hold.

Final proof69 ended0 in pinned builder
sha256:988c0ba586263caeba4be4c03bd16eee055c9d066657951e320087bb8226ee39,
Python3.10.12: real scripts/unpack from the immutable public URL, checksum and
byte equality, installation with curl/wget refusing calls, actual HarfBuzz ICU
resolution, and corrupt downloader output rejected without an acceptance stamp.
Proof66/67 failed because their wrappers imposed shell options before
config/options unlike the framework's own entrypoints. Both original failures
are retained; proof68 uses its normal startup semantics. Final proof69 repeats the passing
checks after matching the launcher declaration to its actual GPL-2.0 header
(GPL-2.0-only); no broader or-later permission is inferred from the old typo. All12 edited recipes pass pkgcheck.
This is build-input proof; assembled-image inspection and VM QA remain required.

The retained WildMIDI cache enables WANT_PLAYER. Its metadata therefore records
both LGPL library and GPL player terms; this pass does not change that build
option. ABL v1.1.9 still names LinuxLoader4588733123554b1f7bf935b04e494e4284894546;
public packaging/release metadata is not implementation-source clearance.
Shader per-file terms, vendor coverage, prebuilt provenance (including rclone's
modified=true), final-image inventory, independent retrieval and off-host source
custody remain publication work. No RC is allocated or publication approved.

Can this be done on the VM? Yes for installed artifacts and behavior. Build
fetch/resolution checks use the exact builder first; no owner cloud or device
operation occurred. The scoped review checked unchanged payload equality,
late-bound recipe paths, normal checksum failure behavior, effective inherited
metadata and source-backed declarations. It does not reopen the completed
#540 audit or extend that audit's scope to these changes.

## Later rclone refresh — current binding

The original disposition above predates #541 and describes rclone1.75.1.
[The 1.75.2 binding](rclone-1.75.2-binding.json) records the current recipe and
actual amd64/arm64 archive hashes. Historical 1.75.1 source and notices do not
establish corresponding source or notice coverage for1.75.2. All #528 source,
vendor-notice, retrieval and custody publication holds remain open. The newer
installed protocol proof is engineering qualification only.

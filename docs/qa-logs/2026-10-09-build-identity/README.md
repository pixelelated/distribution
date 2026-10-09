# Rolling build identity — #530

The owner removes the community-build concept from pixelelated and keeps the
rolling0.0.x approach. Detailed alpha/beta/RC/stable progression remains #265.
D-WORKFLOW-157 and `docs/releases/versioning.md` define the current naming.

## Verified scope

`host-results.json` records29 passing controls using real disposable Git trees,
actual image naming/metadata shell blocks, the actual old/new rocknix recipe
post_install hooks, and immutable-manifest release planning. The generated fresh
system.cfg bytes are identical with DEVELOPMENT_DEFAULTS=yes; no behavior depends
on the release qualifier. A separate opt-out remains explicit.

Versions use semantic release text, UTC timestamp and twelve source-hash digits.
Same-source builds one second apart differ; reusing an existing identity refuses
without touching the prior bytes. Sidecar/os-release/banner fields agree.
Malformed versions/timestamps, contradictory source/image overrides, dirty or
mismatched release metadata, modified bundles and unbound firmware are refused.
The release plan is a local JSON document, not a created GitHub release or a
claim that qualification/custody/credential gates passed. Historical date-based
publishing/asset-clobber/undraft behavior is retired.

`ui02` executes the exact revised rocknix-info script on replacement18 (ES1d76),
with a clearly recorded synthetic metadata overlay. Original metadata,
new metadata and legacy-metadata branches were viewed at640x480. The version,
UTC seconds and short hash fit; no new row or translated label is introduced.
Both protected stored-settings files retain identical hashes. Exact script
hash, source bindings and reviewed frame hashes are recorded separately.
This is not an assembled image or a physical-device test.

## Original outcomes, including the harness failure

Setup's five result channels are0. The first UI owner has five1s because it
required rocknix-info to return0; the original guest also returns127 from an
absent optional hardware-quirk glob after emitting its complete information.
The corrected second owner compares original/revised exit and exact rows,
then walks the actual display. Its five channels are0. No failed result was
overwritten or relabelled. `original-results.json` records actual owner exits.

The guest had a synthetic SSH key and isolated external routes; no personal
configuration was imported and no handheld was contacted. `retirement.json`
records stopped QEMU, removed disk/UEFI vars/keys and allocated bytes recovered.

## Remaining work

#530 stays open for next assembled-candidate installed metadata, sidecar,
filenames, clean/retained-storage and INFORMATION qualification, alongside
#529's startup fix. #265 retains actual versioned publication and future
progression policy. #528 remains the source/licence/custody gate.

Source tracing also found the old USB gadget parser expects calendar OS_VERSION
and already derives an invalid bcdDevice from0.0.1. #531 tracks that existing
consumer separately before the next candidate. No USB/device test is claimed.

Four raw text outputs (network boundary, staged banner, new/legacy information)
are encoded as JSON raw_text with the original UTF-8 byte SHA256. This preserves
native trailing spaces/newlines without whitespace errors in the source diff.

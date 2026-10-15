# Phase 4.6 primary verification of external leads

The blind response is immutable: 13649 bytes, SHA256
097db216f847d83b0a1fb9be82f72aa50355937c08251e3b48a807ee428a0fd6.
The refutation call is active. These are source observations, not final grades
or target-runtime reproduction. No product code or frozen prompt is changed.

## 21:40 UTC — Steam journal and registry leads

G-01: current Install Steam.sh stores complete mountinfo fields in
metadata.mounts (mount_rows1386–1395, available1398–1416, metadata1678).
Uncommitted journal validation1470–1474 requires exact equality. check_probe1638
also requires recorded st_dev/inode/type entries. This source substantiates the
predicted rejection when volatile mount fields differ after a restart; it does
not itself reproduce the boot condition. A new VM interruption/reboot control
is needed before claiming target recovery behavior. Safe rejection remains
important: do not fix by simply discarding mount/identity protections.

G-02: install_bundled_proton_files2367–2370 unconditionally copies the packaged
registry.vdf to STEAM_DOT. The template has fixed language/OOBE/source-mod-path
values. The current metadata transaction explicitly preserves existing channel
and alias entries1671–1694, but that later copy is outside those protected nodes.
git log -S registry.vdf identifies inherited ff40ff1897 and d50674f4de changes.
Source supports a preservation concern; inspect intent and caller/protected-root
fixtures before selecting a fix or asserting which actual Steam preferences are
lost. No device/player registry was read.

## 21:49 UTC — Steam scope, existing intent and current upstream

G-01 is specific to durable uncommitted recovery, not the correct same-invocation
mount guard. Linux's upstream proc documentation defines mount/parent IDs as
mount-instance identifiers and st_dev separately; it provides no stable reboot
identity guarantee (https://www.kernel.org/doc/Documentation/filesystems/proc.txt,
section3.5). Both volatile mount rows and path-chain inode/device checks need a
safe durable-identity design; dropping the guards is not an acceptable fix.

G-02 remains an inherited source-confirmed overwrite. The previous narrow client
review explicitly excluded existing registry-copy/first-launch behavior
(2026-10-14-steam-client-source-review/README.md and followup-03e130.md).
That is a scope limit, not an authorization to destroy player-owned registry
state. No register row settling installer ownership was found by the bounded
archaeology search. Current public ROCKNIX next still has the unconditional copy
at line191, eval assignments72–75 and unguarded binfmt first-launch window246–263;
API blob27b125b6870cb93b9c7af7227cc4b26f6c200e0f, source SHA256
b88672f607d581cb93d7774de37c04a463793c9843c3602f70d5562f91845be8.
Read2026-10-15; no upstream fix, contact or PR is claimed.

G-03 is a prospective supported-format/availability limit, not an observed failure
of the currently inspected55-member archive. G-23 similarly concerns slow-link
adequacy; finite bounds and safe refusal are intentional. Track actual future
unsupported inventory/slow-link evidence without falsely calling current accepted
archive parsing broken. G-21's data-to-eval path is concrete source; confirm a
safe fixture before implementation. G-22 is within the already-open #563/#344
native ARM first-launch qualification boundary; no duplicate completion claim.

H700 applicability: virtual/emulators/package.mk754–767 installs Steam only for
SM4450/SM8250/SM8550/SM8650/SM8750. H700 also omits standalone Dolphin in its package
selection. Shared ES RVZ indexing requires separate applicability review; package
absence alone does not settle shared-code behavior. These source checks do not
replace the current H700 reader's exact installed-inclusion evidence.

The read-only primary workers verify Dolphin/RVZ and receipt leads independently.
No source edit, target fixture, VM, service or device action has run in this phase.

## Final primary grading of both external responses

Both immutable Fable5.1/xhigh responses passed provider-observed identity,
provenance and byte-hash verification. Blind completed21:36:18UTC; refutation
completed21:51:19UTC. Every original command/monitor/runner/launcher is0; no retry.
Root verified all recorded process identities absent. No external call remains.

| Leads | Primary disposition and deciding evidence |
| --- | --- |
| G-01 | Concrete volatile-journal mechanism; reboot/remount trigger unmeasured. PL-002/#608 owns reproduction and safe durable-identity recovery. Do not remove live ownership checks. |
| G-02 | Confirmed inherited registry overwrite; no installer-ownership decision found. PL-001/#607. Prior helper scope excluded the copy, so narrow preservation generalizations. |
| G-03/G-23/G-24 | Current archive contract passes; future inventory growth, real FEX limits and slow-link adequacy remain explicit #563 native/real-payload qualification. No observed current parser failure or new blanket gate. |
| G-04/G-28 | Deliberate safe refusal of unowned/ambiguous retained state. PL-007/#611 clarifies recovery guidance. G-04's source is retained GC resources, not proven immutable-only: automatic deletion is not justified. |
| G-05 | Refuted for normal production flow: exact ES switch writes literal0; ctl writes/reads0 before enabling offline mode. IPv6 wildcard exclusion is deliberate; checks/lead-verification/retroarch-hardcore/findings.md. |
| G-06 | Reader annotation distinguished from real archive measurement; installed steam resolves to packaged bin_steam.sh. No newly measured header bytes. Receipt note supplies exact identities. |
| G-11 | Confirmed recurring automatic retry of failed GameCube RVZ hashes, conditional on enabled indexing. PL-003/#609. No measured performance cost or browser-cause claim. Valid unmatched hashes remain protected. |
| G-12/G-13 | Packet omissions resolved from exact patched IPv4 proxy binding and complete launcher blocks; no new live socket/gameplay claim. checks/lead-verification/dolphin-rvz/findings.md. |
| G-14/G-15 | Original product/tool identities are distinct; actual continuation config binds corrected current harness and exact run.py. No historical1378-pass result is relabelled as current product execution. Receipt note. |
| G-16 | Frozen readiness already retains f863 producer-reporting failure/unknown launcher wait. Independent artifact/VM success remains distinct; same caveat added to scorecard. |
| G-17/G-18 | Exact preparation timestamp precedes actual launch; old/current four Python heredocs are byte-equal. Receipt note closes these source-binding omissions. |
| G-19/G-27 | Actual composed claims equal frozen Git claims,391 rows with zero wildcard heads; vm-qa uses that path.78 original pixel-pair/scalar rows retained; no new all-frame review claim. |
| G-20 | Current exact recipe lint0 supplies mechanical check. Historical original status remains unavailable. |
| G-21 | Inherited release-metadata eval assignment is a concrete quoting boundary. PL-004/#610; safe VM control and repair required before affected deployment. |
| G-22 | Existing #563 native first-launch/binfmt lifecycle qualification remains unproved. Frontend kill list names Steam/FEX, not proof that the shell is killed. Do not assert observed unrecovered binfmt state. |
| G-25 | Original before/after manifests and logs show successful recovery followed by injected wget9; all retry1 outcomes remain1. No successful replacement-download claim. Receipt note. |
| G-26 | Subreaper setup, driver0, joined worker and absent exact identities prove bounded cleanup. Clean grandchild individual wait statuses are not retained; no claim of all individual exit codes. Preserve this receipt limitation. |
| G-29 | Preservation/no-defect wording narrowed in03/04; PL-006 owns record correction and exact evidence links. |
| AC-53 challenge | Accepted: prior literal criterion included RetroArch. Native02/03 close Dolphin/Flycast only; missing RetroArch process/stat binding leaves aggregate PARTIAL. PL-005/#606 owns a focused current VM proof, not an exhaustive historical search. |

The seven punch items distinguish product defects, predicted recovery risk,
missing evidence and guidance. H700 package selection excludes Steam and Dolphin;
actual packaged inventory and retained-device overrides remain separately checked.
This does not exempt shared frontend code or authorize device actions. All source
and receipt packets above were independently hash-verified into checks/lead-verification.

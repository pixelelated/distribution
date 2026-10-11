# pixelelated build identity

The current rolling release target is **0.0.1** (M7). D-WORKFLOW-157 removes
ROCKNIX's official/community distinction from this distribution. No behavior
is selected by the words alpha, beta, rc, stable, or community.

## Public release policy

D-WORKFLOW-159 (#532) selects only **release candidates** and **releases**.
The initial rolling sequence is `0.0.1-rc.1`, `0.0.1-rc.2`, then `0.0.1`;
the next release target is `0.0.2`, whose RC counter starts again at1.
No alpha/beta stage is required or accepted by the build qualifier. `dev`
remains an internal engineering label, never a public release plan. Names
alone confer neither RC qualification nor publication permission.

Before freezing a candidate set, one owner records its base version, next
unused positive RC number, full source/input identities, UTC timestamp and
owning issue in the candidate build record linked from the milestone. Check
both the allocation record (including failed/private attempts) and existing
tags. The number is consumed at freeze, even if the build or QA fails; never
reuse it. All target/board variants in the same coordinated set share the
number, source and timestamp. A resumed build using unchanged frozen inputs
keeps that identity; reassembly with new bytes or a new freeze gets a new
number and timestamp. Adding an unbuilt target to that exact set is not a new RC.
Allocation is explicit workflow, not an automatic counter in the build script.
No RC number has been allocated by the #532 policy tests.

Public tags and titles omit build metadata: `v0.0.1-rc.1` / `pixelelated
0.0.1-rc.1` and `v0.0.1` / `pixelelated 0.0.1`. Both are immutable. UTC time
and source hash remain in firmware filenames, installed identity and sidecars.
Two newly frozen sets on one day receive distinct RC numbers and timestamps.
A reserved RC-shaped engineering image remains unqualified until the required
preflight, image QA and applicable review gates pass.

### RC to release

Removing `-rc.N` changes embedded `/etc/os-release` and related bytes. Select
the accepted product source, set the qualifier explicitly empty, and reassemble
with a new timestamp and immutable manifest. Cached packages may be reused;
RC firmware may not be renamed or retagged as release firmware. That new
release assembly receives its own installed-byte, clean/retained-storage and
applicable release qualification. Any evidence carried forward must cite exact
unchanged inputs; the version change alone does not waive tests or review.
After publication, corrections target the next patch version rather than
replacing tags/assets. The rolling0.0.x convention does not declare a stable
public API or decide future major/minor compatibility policy.

## One identity, several readable forms

| Field/surface | Example |
| --- | --- |
| Base target in distributions/ROCKNIX/version | `0.0.1` |
| Release version, default engineering qualifier | `0.0.1-dev` |
| Complete build identity | `0.0.1-dev+20261009T231500Z.gc6afa31db1c0` |
| UTC build time | `2026-10-09T23:15:00Z` |
| Full source BUILD_ID | `c6afa31db1c00ecd82ff615310f97debe63b519c` |
| RC GitHub tag/title | `v0.0.1-rc.1` / `pixelelated 0.0.1-rc.1` |
| Stable GitHub tag/title | `v0.0.1` / `pixelelated 0.0.1` |

These are examples, not a designated RC or released build. `config/build-identity`
freezes the UTC timestamp once at image assembly, keeps the full source hash,
and gives every output a twelve-character hash abbreviation. A local edited
tree adds `.dirty` to build metadata and is refused by release preparation.
The metadata identifies a build; SHA256 and the immutable manifest identify
its exact bytes. Build metadata is not an update-order comparator.

The base OS_VERSION stays stable while packages build, avoiding timestamp-based
package/cache roots. Installed OS_VERSION and VERSION_ID carry the release
version; VERSION and BUILD_VERSION carry its complete build identity.
BUILD_DATE is ISO8601 UTC. INFORMATION shows VERSION, then BUILD ID with the UTC
time and short hash. Existing diagnostic branch/full-hash metadata remains.
Login banners and the configuration report use the same identity.

Files use `pixelelated-<device>.<arch>-<complete-build-identity>`, with existing
board variants and the `-from-ROCKNIX` adoption suffix retained. A matching
`.identity.json` accompanies them. A repeated timestamp/source identity for
the same target refuses existing output instead of replacing it. Candidate
custody retains the sidecar, firmware, checksums, and qualification evidence.

Set `BUILD_TIMESTAMP=YYYYMMDDTHHMMSSZ` once for a coordinated set of sequential
device builds. Use a new timestamp for a new build set, even when source is
unchanged. Do not infer timestamp from file modification time or build finish.
`BUILD_QUALIFIER` defaults to `dev`; explicit `rc.N` requires N >=1 without
leading zeroes, and an explicit empty value selects a release. All other
qualifiers are refused. For example, set `BUILD_QUALIFIER=rc.1` or
`BUILD_QUALIFIER=''` alongside the set's recorded `BUILD_TIMESTAMP` when running
the normal build entrypoint. These settings never publish or automatically
promote an image.

Fresh-install network/logging defaults are controlled by
`DEVELOPMENT_DEFAULTS=yes|no`, default yes to preserve the previous engineering
build behavior. They are independent of the qualifier. Existing stored settings
are not changed. Hardware and cloud tests remain separate from names.

## GitHub preparation

`tools/fork-publish-release --prepare <immutable-bundle>` verifies the candidate
store manifest and all file bytes, sidecar identities, source commit, firmware
names and checksum files. It emits a JSON plan containing the exact assets,
matching tag/title, source target, draft flag and unassessed qualification gates.
It accepts only RC/release versions, refusing dev or other prerelease stages.
It performs no network call or GitHub mutation. The former newest-file/date-tag,
asset-overwrite and automatic-undraft behavior is retired.

Every target in one plan shares the version, timestamp and source commit. A
historical bundle with no sidecar is refused; never relabel existing firmware.
Historical ROCKNIX tags/releases are left intact. Stable tags are immutable;
a later corrected release increments the rolling patch target instead of
replacing published bytes. Existing #528 source/licence/custody requirements,
artifact credential checks, unused tag/allocation verification, candidate qualification, and named publication
approval still precede a public release. Implementing the actual qualified
publication transaction and publishing0.0.1 remain #265/#344 work.

The syntax follows [SemVer2.0.0](https://semver.org/spec/v2.0.0.html), including
prerelease qualifiers and ignored-for-precedence build metadata. GitHub's
[draft/prerelease model](https://docs.github.com/en/repositories/releasing-projects-on-github/managing-releases-in-a-repository)
is a publication property, independent of naming. This initial0.0.x rolling
scheme does not declare a stable1.0 API or a complete alpha-to-stable policy.

## USB device revision

USB gadget `bcdDevice` is a separate interface revision, currently BCD 1.00
(`0x0100`), shared by networking and MTP (#531, D-WORKFLOW-160). It does not encode OS_VERSION,
release channel, date or source hash. Only a deliberate gadget-interface
revision changes it. The vendor/product/serial identities and mode definitions
are preserved; a new OS version alone does not change this descriptor.

## Qualification boundary

The reusable `tools/build-identity-test --output <new.json>` exercises actual
assembly blocks and the actual manifest verifier/planner. #532 host results are
in `docs/qa-logs/2026-10-11-release-policy/`; no firmware is built by that tool.

Earlier source/host controls and VM runtime-overlay frames are recorded under
`docs/qa-logs/2026-10-09-build-identity/`. Next assembled-candidate qualification
must check installed metadata/sidecar/image names, clean and retained storage,
and INFORMATION frames before #530 closes. #529's startup fix goes into that
same candidate. No new owner-device transfer follows from these source changes.

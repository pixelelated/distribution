# pixelelated build identity

The current rolling release target is **0.0.1** (M7). D-WORKFLOW-157 removes
ROCKNIX's official/community distinction from this distribution. No behavior
is selected by the words alpha, beta, rc, stable, or community.

## One identity, several readable forms

| Field/surface | Example |
| --- | --- |
| Base target in distributions/ROCKNIX/version | `0.0.1` |
| Release version, default engineering qualifier | `0.0.1-dev` |
| Complete build identity | `0.0.1-dev+20261009T231500Z.gc6afa31db1c0` |
| UTC build time | `2026-10-09T23:15:00Z` |
| Full source BUILD_ID | `c6afa31db1c00ecd82ff615310f97debe63b519c` |
| Prerelease GitHub tag/title | `v<complete-build-identity>` / `pixelelated <complete-build-identity>` |
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
`BUILD_QUALIFIER` defaults to `dev`; an explicit empty value means stable.
SemVer-compatible qualifiers such as `alpha.1`, `beta.1`, and `rc.1` are accepted
as names. This adds no mandatory progression, automatic promotion or release
approval: the later policy lives in #265, per the owner's scope refinement.

Fresh-install network/logging defaults are controlled by
`DEVELOPMENT_DEFAULTS=yes|no`, default yes to preserve the previous engineering
build behavior. They are independent of the qualifier. Existing stored settings
are not changed. Hardware and cloud tests remain separate from names.

## GitHub preparation

`tools/fork-publish-release --prepare <immutable-bundle>` verifies the candidate
store manifest and all file bytes, sidecar identities, source commit, firmware
names and checksum files. It emits a JSON plan containing the exact assets,
matching tag/title, source target, draft flag and unassessed qualification gates.
It performs no network call or GitHub mutation. The former newest-file/date-tag,
asset-overwrite and automatic-undraft behavior is retired.

Every target in one plan shares the version, timestamp and source commit. A
historical bundle with no sidecar is refused; never relabel existing firmware.
Historical ROCKNIX tags/releases are left intact. Stable tags are immutable;
a later corrected release increments the rolling patch target instead of
replacing published bytes. Existing #528 source/licence/custody requirements,
artifact credential checks, candidate qualification, and named publication
approval still precede a public release. Implementing the actual qualified
publication transaction and publishing0.0.1 remain #265/#344 work.

The syntax follows [SemVer2.0.0](https://semver.org/spec/v2.0.0.html), including
prerelease qualifiers and ignored-for-precedence build metadata. GitHub's
[draft/prerelease model](https://docs.github.com/en/repositories/releasing-projects-on-github/managing-releases-in-a-repository)
is a publication property, independent of naming. This initial0.0.x rolling
scheme does not declare a stable1.0 API or a complete alpha-to-stable policy.

## Qualification boundary

Source/host controls and VM runtime-overlay frames are recorded under
`docs/qa-logs/2026-10-09-build-identity/`. Next assembled-candidate qualification
must check installed metadata/sidecar/image names, clean and retained storage,
and INFORMATION frames before #530 closes. #529's startup fix goes into that
same candidate. No new owner-device transfer follows from these source changes.

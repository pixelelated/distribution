# Identity classification, version 2 (#409)

`pixelelated` (always lowercase) is the OS_NAME, DISTRONAME and image-name prefix for 0.0.1.
`DISTRO=ROCKNIX`, the distribution/project directories, toolchain triples,
partition labels, kernel default hostname, units, commands, settings keys,
share names, mount points and backup archive writer suffix remain compatible
with RC2 (D-WORKFLOW-123). Readers retain legacy archive display identities.
The adoption tar includes `-from-ROCKNIX` (D-WORKFLOW-128).

Player-facing names and brand artwork change; upstream copyright, component
credits and historical documentation retain their original names. Tools-list
`developer` and `publisher` fields preserve attribution. A reference to the
ROCKNIX partition means the actual retained label, not the distribution name.
New fork-owned helpers use the `pixelelated` prefix. Existing `rasteratops-*`
helper names and watcher variables are temporary internal interfaces, with
their retirement tracked in #509 (D-WORKFLOW-151). Inventory callers and rename
active fork-owned tools, folders and documents in reviewed batches after their
running jobs finish. Compatibility aliases need explicit retirement conditions.
Historical evidence, the Rasteratops character and maintainer handle retain
their correct names; this cleanup does not rename upstream-owned interfaces.
The cloud default is `/pixelelated`; existing `/GAMES`, `/ROCKNIX` and custom
choices remain until explicitly changed. Setup does not move their contents
(D-CLOUD-174/175/176).

The wordmark uses Tiny5 Duo LCD, whose unmodified source and SIL OFL 1.1 terms are
retained by the splash fork. Its icon-free form follows D-WORKFLOW-145.
The previous distribution's update and statistics endpoints are inactive;
manual updates and a masked statistics timer implement the recorded decisions.

The full baseline classification is `docs/rasteratops/p0-sweep-hits.txt`.
A remaining ROCKNIX identifier is assessed by its consumer using the rules
above; a blanket string replacement is not an identity migration.

The first pixelelated artifact classification is retained under
`docs/qa-logs/2026-10-04-pixelelated-artifact-sweep/`. Its allowlist binds each
reviewed context to a path and hash; seven known stale player-text contexts
remain FIX until #416's corrected image removes them. Use `scan-artifact.py`
there for each new extracted SYSTEM. New or changed contexts require review.
This text sweep does not replace the guest old-logo frame control.

`tools/rasteratops-identity-check --es <pinned checkout>` verifies the source
contracts, including inert updater/statistics commands in a network-isolated
filesystem. A template-only negative control is retained under
`docs/qa-logs/2026-10-02-candidate-preflight/`. It is not the image-wide brand
classification or an old-logo frame matcher; those remain image QA criteria.

D-WORKFLOW-144 makes pixelelated the project and OS name. Rasteratops is a
character and the maintainer's GitHub handle; the organization is pixelelated.
Blitterbot's account and email stay unchanged. The owner confirms no systems
use /Rasteratops: ROCKNIX → pixelelated is the required adoption path.
Historical docs/artifacts keep their original names and paths; current art is
in `docs/pixelelated/art/`. The wordmark contains no character artwork.

## Version and build classification

New images use semantic release versions plus a UTC timestamp and source hash,
with no community/official category (D-WORKFLOW-157, #530).
[Build identity](docs/releases/versioning.md) defines filenames, metadata,
INFORMATION and GitHub naming. Release qualifiers are independent of fresh-install
network/logging defaults. Historical firmware and published tags retain their names.

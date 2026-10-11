# M7.P5 dependency refresh — #541

Freshness71 stopped the initial combined-image freeze before compilation:
rclone1.75.1 was behind1.75.2 and RAOfflineProxy879b158 was14 commits behind.
The initial63a2090a56 cache-copy freeze is superseded for compilation; its
independent cache can be reused after verification and an explicit new freeze.

## Source and compatibility

rclone1.75.2 amd64 and arm64 archives match upstream SHA256SUMS and independent
hashing (`fetch.json`). The [upstream release notes](https://rclone.org/changelog/#v1-75-2-2026-10-09)
include security repairs, network retry/cancellation fixes, and Dropbox shared
folder handling changes. Hosted-provider success is not inferred from those notes.
Full WebDAV/SFTP/local S3 backup/restore regression remains an installed-image gate.

RAOfflineProxyc7ebd1b6e777f3751ff0ecdf8aba54045844e00d changes Linux background
queue pacing and adds opt-in watched folders. No automatic watched folder is
configured by this fork. The16-patch series applies without fuzz;001/004/005/011/012
were context-rebased. Coupled rcheevos1433173220a7eaede6a9ed7a18e94117be1821e0
and libchdr607694ca0812edfc9cc2030c64634fc2393668de remain unchanged.
Storage review found a protected watch-seen key prefix, with no changed SQL
cache/award columns. This source review is backed by an actual predecessor-written
store reopened by the new code, not just a revised schema annotation.

The removed upstream cooldown helper made our preparation command fail at
import (`old-helper-failure.json`). A local compatibility helper preserves its
existing30-second pause after each50 games. The deliberate OS whole-library
command still opts out of the100-game background window; it retains request
throttling, persistent server pauses, and truthful queued-versus-ready outcomes.
Upstream's background queue keeps its new pacing. This is a preservation change,
not an attempt to disable the new upstream background safety behavior.

## Completed source proof

`proxy74`: actual recipe-built native library,866 upstream Linux tests with no
skips and11 fork integration tests pass. Real old879b158 source writes the store;
cache/sign-in/base/subset pending-award rows and old image paths survive reopens.
Synthetic game/HTTP boundaries exercise125-game preparation, failure/retry,
persisted429 refusal and default100-game queue behavior. No account-backed award
or owner cloud/device mutation occurs. Source seals and original terminal receipts
are retained. Installed service, native formats, consent transitions and reconnect
proof remain required on the new image.

`discovery-fixture.json`: an actual temporary Git repository reproduces stale
archived docs/package.mk fixtures being discovered as active recipes. Restricting
the search to build-engine roots packages/ and projects/ excludes them while
retaining active root and override recipes and the explicitly owned rclone recipe.
The fixture changes discovery only; it does not exempt either real update.

Can this be done on the VM? Yes: installed protocol, service and retained-state
proof follows assembly. Source/native harness checks run locally first. No physical
handheld fact is involved. ES stays atc8dc72cf9e; no screen or navigation is changed
by this refresh. Its existing flow reference remains current, with exact new-image
frames to be recorded during combined qualification.

## Original integration-harness failures retained

Regression75's focused11 integration checks pass, but its broad suite ends with
2 failures and26 skipped checks. The new proxy archive was not in the cache the
suite searches, so proxy sections did not run. Two final host helpers lost the
owned TMPDIR when the harness deliberately cleared it for bubblewrap and hit the
host /tmp user quota. No skipped check is counted as passed. Fresh79 supplies the
verified archive and new rclone binary, and scopes TMPDIR to those host helpers.

The first cache comparison failed on seven generated predecessor .pyc files plus
their directory metadata. Actual predecessor imports created these during copying.
The integration tool now suppresses predecessor bytecode writes. The original
nine-line comparison and nonzero terminal result remain; a fresh owner performs
another full checksum comparison and inode independence verification.

## Cache accepted; patch-test quota isolated

`cache-recheck` ended0: empty full checksum comparison and2,532,289 independent
regular-file inode pairs. Original copying did not produce firmware. New build
source will be explicitly fast-forwarded and frozen after source publication.

`patch-temp80` reproduces the two RetroArch dry-run failures with the default
host temporary directory: patch reports a write error from the disk quota. All21
patches apply in package order and every required zero-fuzz dry run passes with
the owned temporary directory. Product patches did not change. This separates a
host fixture failure from a product patch failure; the original full run remains
failed until its exact corrected section is separately verified.

## Final source disposition

Fresh79: upstream freshness0, both recipe lints0, proxy schema guard0 and12 fork
integration checks0. Its full host run uses the verified rclone1.75.2 binary and
accepted-image BusyBox in an explicitly separate tool fixture, plus the real pinned
proxy archive. It ends1 with1,372 PASS,1 FAIL,0 SKIP and one retired historical
feature group. The sole failure is the patch dry-run quota diagnosed above.
It is not relabeled as an aggregate passing run.

`target82` extracts the exact final F2-4 harness section and passes the package-order
and zero-fuzz check with its owned TMPDIR. That is the only harness change after79;
all source changes now match `final-source.json`. The affected section is rechecked
without replaying unrelated passing cases. The two earlier host-helper quota failures
also pass in79. Full installed VM qualification will use the final assembled image.
No unresolved reported product failure remains from these source checks.

Freshness includes all active recipes and deliberately coupled pins and returns0.
The full ceremony checker reports nothing overdue. #541 remains open for real local
WebDAV/SFTP/S3 transport on the new image and final freeze/installed follow-through.
Public RC naming, component/source clearance and publication remain separate gates.

## Evidence-count correction — #543

Original74/75/79 each report11 integration tests. Earlier claims of12 were wrong:
the newly declared pacing class was absent from the CLI's manual suite list.
[Discovery repair and original logs](../2026-10-11-proxy-test-discovery/README.md)
retain that discrepancy. The corrected runner executes all12; a wrong-duration
negative control fails the named pacing assertion. The production helper and
replacement19 bytes remain unchanged. Do not attribute the new12-test result to79.

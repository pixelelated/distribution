# M7.P3 current proxy source review (#426)

Selected upstream7252fc781392d45b22f50d1a92f9febc4d1fa172 follows865e21 by
three commits: Linux large-library memory/menu fixes,2.1.0-alpha1 metadata,
and Android login choice/auth-rejection handling. The latter Android behavior
is not shipped by this recipe. The Linux delta is real; old byte-equivalence
claims are not carried forward.

## Source and integration

The reviewed archive is c5c85da105782828c738539db048e62677c9da11d215c0dcc5dae8c3f79c5680.
Eleven consumed Python files change. All53 native source files match865e21;
libchdr8e7b8bd32bc676b7e5c6b42fe7d2daca986c4a0d and
rcheevos1433173220a7eaede6a9ed7a18e94117be1821e0 remain the parent's pins.

Storage retains api_cache and pending_awards columns and adds cached_game_meta,
an index, delete/rename triggers and metadata backfill. Reads now stream bodies,
or query keys/summaries/metadata. This avoids loading every cached response to
list a library. The ctl's direct SQL projections remain compatible. Its fallback
and the image-repair helper stream bodies; refresh uses keys and summaries,
retaining the newest-row age despite the new API's unordered output.

Award lookup searches only the needed IDs, preferring a likely/recent game and
falling back to the full cache, including achievementsets. Existing account,
softcore/status filters and base/subset mapping remain required. Metadata
queries do not make queued work ready offline. The explicit125-game preparation
route retains its opt-out from the100-game background budget, request pacing,
429 pauses and locks.

All15 patches apply with zero fuzz.003 follows the changed import context;
005 wraps the new key-based refresh pass and preserves auth/error bounds.
008 adds upstream-test adaptations for the existing explicit-consent contract:
real incident + explicit true may report; missing/false/numeric/string settings
must not upload or mark the incident reported. Production consent code is
unchanged. Other patch behaviors remain unchanged.

Already written: the old client's actual Storage creates the predecessor
fixture. Reopening it twice with new Storage preserves cache, account, queued
base/subset awards and legacy image bytes; additive metadata is backfilled.
No personal account or cloud mutation is part of these tests. New-image installed
proof and a real new ordinary RA award remain separate acceptance criteria.

## Test custody and limits

The original patched814-test run failed the upstream automatic-report test,
which lacked the fork's required consent. A subsequent new-test syntax error
and an incorrect assertion forbidding even a local incident read also failed;
those original runs are retained with rc1. Corrected negative controls use a
real unreported incident and assert no upload or reported mark. No failure is
relabeled as a pass, and the production consent gate was not weakened.

Pristine upstream809 tests passed with17 native-library skips. The final
patched815 tests pass with the previous candidate's verified native library,
without those skips. Eleven downstream integration tests pass, including both
125-game paths, retry/pause behavior, predecessor preservation and actual
image/refresh helper consumers. Early old-API and new-test fixture failures are
retained. The full scripts suite ends PASSED with no FAIL/SKIP lines. Actual tool5816
exited0; inner/wrapper/watcher results all0. All27 sealed source hashes
match. Actual host observation03:11:24 confirms runner1430289, watcher1430291
and command1430320 absent. Completion, original failed attempts and watcher
receipts are retained here. These are source/host tests using the previous
candidate native library and applets, not replacement07 installed evidence.

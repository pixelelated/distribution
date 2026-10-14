# Scoped Steam client source review — #582

Reviewed `a057a2a7e94c372642fd66ff9795125487f1fa75` read-only, including the sealed
README, criteria, complete issue/comment intake, exact installer, client helper,
caller order and relevant fault controls. Installer SHA256:
`7a46ace9ea0a8f1c9509380e2826fcef318ae0f211f7fee6900ddb7c6735aa9b`.
Two actionable findings follow. This is source evidence, not runtime reproduction,
native acceptance, a formal external audit or a containment approval.

1. **P1 — detached transfer cleanup requires a proc file absent on the accepted
   kernel.** `Install Steam.sh:1752–1753` (`client-helper.py:584–585`). After killing
   and reaping the transport leader, a still-live adopted child makes
   `waitpid(-1, WNOHANG)` return 0. The helper then reads
   `/proc/<self>/task/<self>/children`. The retained #584 guest trace establishes
   that this optional file is absent on the accepted GENERIC_X64 kernel; the
   prepared `transport-timeout` boundary explicitly creates a new-session child
   sleeping for 600 seconds (`boundary.py:89–93`). That child is outside the
   killed group, and the missing-file exception exits supervision before its
   pidfd signal/reap. The client install exception path can then perform stage
   cleanup despite unestablished transfer quiescence (`client-helper.py:1061–1068`).
   The synthetic acceptance case therefore cannot demonstrate its required
   product-owned cleanup on that kernel, and the bounded helper can leave a child
   alive. This does not claim ordinary curl always creates such a descendant.

   **Repair/control:** use the already qualified numeric `/proc/PID/stat`
   PPID/start-time census and identity-checked pidfds, with bounded reaping of
   this subreaper's children. A census/quiescence error must retain transaction
   state instead of permitting cleanup under a possible writer. Allocate the
   existing timeout case after the correction; require the original installer
   failure and no descendants without fixture rescue. Do not substitute an empty
   census for a read error. Historical evidence is bound in `source.json`.

2. **P2 — lexical normalization can select the wrong profile support directory.**
   `Install Steam.sh:1608–1610` (`client-helper.py:440–442`). `probe_directory`
   normalizes a symlink's target with `normpath` before traversing its components.
   For the valid layout `STEAM_DOT=/storage/profile`,
   `/storage/profile -> link/../support`, and
   `/storage/link -> /storage/elsewhere/deep`, filesystem resolution selects
   `/storage/elsewhere/support`; this helper selects `/storage/support`.
   Both directories can exist on admitted writable storage without overlap with
   Steam. Fresh metadata is consequently created/journaled in the wrong support
   directory (`metadata` and `prepare_metadata`), while the unchanged bundled
   registry copy follows the actual logical `STEAM_DOT` (`Install Steam.sh:2288`).
   The bootstrap can be committed with its support aliases in another folder.
   Existing-client metadata validation also inspects the wrong folder. The
   prepared profile cases do not include this nested-link/parent traversal.

   **Repair/control:** retain symlink target components and process `..` after
   resolving preceding links, as the existing root helper's component walk does;
   retain no-follow identity/mount checks and compare the logical destination
   again before metadata writes. Prepare fresh and existing profile-alias cases
   with both possible destinations seeded independently. Require only the actual
   resolved support folder to be used and the lexical decoy to remain identical.
   These proposed controls are UNRUN.

No additional concrete defect found in the reviewed supported-existing-client
skip, profile timing, prepared/published/committed recovery branches or ownership
deletion rules under their stated contract. The four-core structural predicate,
pre-profile client check/post-profile metadata split, deliberate holds for
creation/journal gaps, and lack of full-installer rollback are explicit limitations,
not newly invented findings. All 11 non-client shell function bodies match c624;
the terminal copy no longer claims native success. Existing registry-copy and
first-launch behavior remain outside this helper's repair claim.

Static AST/hash/source comparisons passed, including separate body-without-final-
newline and actual-stdin identities. The reviewer's initial boundary-digest
assertion failure and correction are recorded in `source.json`; it was not a
product failure. No Steam source/shared record edit, fixture import, runtime,
provider call or new worker occurred. Coordinator owns remediation, containment
review, runtime allocation and integration.

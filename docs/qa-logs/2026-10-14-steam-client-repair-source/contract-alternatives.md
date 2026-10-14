# Concrete contract choices against c624

## A — verify recorded bytes, otherwise preserve and stop (recommended)

For a truly absent client, stage and validate the complete selected archive and
record every canonical member's type, length, digest or link target plus the exact
publication/metadata identities. A receipt is an index to revalidate, never the
readiness predicate by itself. On a later invocation, verify those actual bytes
and paths under read-only identity checks before continuing. An absent/truncated
receipt, any missing or changed required member, a client alias, unsupported
shape, or unknown older partial tree gets a nonmutating refusal. Do not import
arbitrary old metadata into the new ownership schema.

Preserve custom/unrelated entries; an unexpected entry must not enter a cleanup
set. Existing beta/channel and accepted aliases remain byte/identity identical.
A self-update may legitimately change the recorded bytes: that is unverified
state, not proof of corruption. Refuse installer continuation with truthful copy;
never call it broken, delete it, downgrade it to today's archive, or rewrite its
channel to make the test pass. Ordinary client launching remains unchanged.

Tradeoff: old working clients and self-updated clients may be unable to complete
this installer until a separate recognition/adoption contract is qualified. This
satisfies conservative preservation, but it is a player-visible compatibility
change, not a transparent recognition fix. The historical synthetic
`valid-existing-client` control uses a shell sentinel and cannot establish real
legacy recognition under this policy.

## B — version-tolerant structural bootstrap recognition

Define an explicit bounded structure contract: real executable ARM64 entrypoint,
required ELF/dynamic structures and companion files, safe resolvable in-tree links,
channel/aliases, and complete membership for each supported layout. Preserve the
existing tree without comparing it to today's package hashes. New transactions
still use full selected-archive hashes, CRCs, member accounting, and a journal.

Tradeoff: a complete-looking but corrupted or truncated older installation can
meet a structure-only predicate. Required members can change across self-updates;
there is no inspected official read-only ARM64 completeness specification to make
that list authoritative. A versioned list, its accepted limitations, and actual
legacy/self-update qualification are necessary before coding it as a success
path. Calling the result "bootstrap structure recognized" is more accurate than
claiming runtime readiness, but copy alone does not satisfy #582's incomplete-state
criterion. Do not promote a `.installed` marker to a substitute oracle.

## Alternative outside this assignment — client-managed verification/adoption

Valve's own bootstrap/updater can validate and reacquire files. Running it is an
execution/network/state-changing operation, not a read-only classifier. Upstream
#11602's `-verifyfiles` discussion does not define an offline installer predicate.
No native client, download, account, or adoption action is authorized here. This
would require a separate precise scope and preservation/exit contract; it is not
an implicit third branch of a source-only repair.

## Exact caller seam and input compatibility

The whole frozen script is bound in source.json. At c624:

1. Line 1530 runs `steam_root_layout inspect` before profile code; line 1531 freezes
   STEAM, STEAM_GAMES_ROOT, and STEAM_ROOT_PLAN. Reuse its resolved-root plan and
   mount/path identities rather than introducing a second root resolver.
2. Line 1532 sources `/etc/profile`. The target profile sources `/etc/profile.d/*`,
   creates `/storage/.config/profile.d` if absent, then sources all user snippets.
   Refusing later cannot honestly mean that no writes occurred.
3. Line 1533 chooses STEAM_DOT after those snippets. A profile can set an otherwise
   unprovided override. The existing root inputs were deliberately frozen before
   profile in ba0c530bf0f4; STEAM_DOT was not included.
4. Line 1548 revalidates roots. Line 1549 invokes `set_kill`, whose exact target
   implementation writes `/tmp/.process-kill-data`. It does not establish client
   quiescence or lock the updater.
5. FEX/root/desktop/runtime work precedes the line-1556 client call. Checking only
   inside install_steam_client_arm64 leaves earlier mutations on refusal.
6. The first-launch call at line 1519 logs a client error and continues; the final
   `log_success` reports success without enforcing that native exit.
   See the exact line bindings in source.json rather than treating this prose as
   executable offsets. Native launch success remains outside synthetic proof.

Minimal seam for A: add a nonmutating client preflight immediately after the
existing root inspection/freeze and before `source /etc/profile`; revalidate its
plan before transaction writes. Existing-state refusal must happen there. Keep
all completed FEX/runtime/Proton helper bodies byte-identical. Fresh transaction
activation stays at the existing client-call position, with its own journal and
only explicitly owned new nodes eligible for cleanup. Earlier successful helper
transactions are not rolled back as if the whole installer were atomic.

STEAM_DOT has two concrete choices:

- Freeze its environment/default value before profile, like STEAM, and refuse
  profile attempts to change it. This permits early metadata refusal but changes
  support for profile-defined STEAM_DOT overrides. An environment-supplied path
  still works after the same early read-only path checks.
- Preserve the current post-profile override contract. Perform the client-tree
  ambiguity check before profile and check metadata after profile. State the
  narrower guarantee explicitly: ambiguous client-tree refusal is before writes;
  metadata refusal may follow profile effects. This does not meet the literal
  before-all-writes criterion without a criterion/contract decision.

Do not execute arbitrary profiles in a probe merely to discover their variables.
Do not move all profile code, FEX, or launch behavior as an incidental ZIP fix.

## Format and preservation facts now established

Only these names change spelling inside a newly owned stage:
`steamrtarm64\\libs/`, `steamrtarm64\\swiftshader/`,
`steamrtarm64\\libs\\libcurl.so`, `steamrtarm64\\libs\\libnghttp2.so`, and
`steamrtarm64\\libs\\libnghttp2.so.14`. Their slashes become `/` according to the
exact map in format-contract.json; reject other backslashes, traversal, collisions,
new roots, unexpected types, duplicate members, and local/central disagreement.
The three link targets are respectively `libcurl.so.4.8.0`,
`libnghttp2.so.14.20.1`, and `libnghttp2.so.14.20.1`; create links last after their
regular targets. These mappings never authorize touching existing literal-backslash
siblings left by older extraction.

All canonical members are under steamrtarm64. There is no linuxarm64 SDK payload:
SDK aliases can be deliberately deferred, not evidence of SDK readiness. The
regular entries have DOS provenance, so derive explicit executable policy from
qualified requirements; do not assume their high attribute bits are Unix modes.
The old function chmods only `steam`. Native execution modes for companion programs
remain a qualification boundary, not something the structural report proved.

Proposed new-transaction bounds retain the reviewed 384 MiB aggregate decoded,
128 MiB per member, 128 entries, 10 s connect, 180 s transport and 90 s decode
ceilings. Actual archive size/digest must match its bounded HTTPS manifest; no
partial resume across a changed selection. Output, report, worker-memory, free
space, elapsed-time, and process-group cleanup guards still need implementation
and tests. A new size/layout beyond reviewed policy refuses; no automatic cap
increase. These are proposed production bounds, not measured installer limits.

Keep staging on the resolved Steam filesystem. Publish only into absent owned
names, with metadata before the client-directory rename and recovery before any
skip. `.steam` metadata may use a different filesystem and needs parent-local
atomic nodes with durable before/created identities. A failed/unknown journal,
changed node, missing parent, active/unknown consumer, or visibility gap refuses
cleanup. No recursive removal of an arbitrary existing directory. An installer
lock alone cannot eliminate races with the client's independent updater. Signal
recovery and successful compilation do not prove power-loss safety or native
readiness.

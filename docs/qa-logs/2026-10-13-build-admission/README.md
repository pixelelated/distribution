# Mandatory build admission — #493

Normal native, Docker and ad-hoc compilation now requires a fresh retention and
capacity admission before its payload starts. Native device targets share one
admission across their ABI phases. The common Git-directory registry reserves the
measured future budget, records output owners/release conditions and holds the
reservation until original results and retained evidence are consumed. Explicit
`--record-only` is for non-compiling jobs and cannot authorize nested compilation.
See [the tool contract](../../../tools/host-maintenance/build-admission.md).

## Evidence and limits

- 27 admission controls pass on final tool bytes, including refusal of missing,
  expired/future, changed-source/evidence/profile/registry and insufficient-space
  admissions; one-use receipts; process/PID-namespace protection; original failure
  preservation; and idempotent completion without deleting held outputs.
- 36 routing controls pass through actual script prefixes and Makefile routes,
  with synthetic payloads and fake Docker. The sole subsequent watcher change
  disables Python bytecode writes into frozen tool trees. Final admission tests
  and the real host lifecycle include it; CI repeats both suites on final bytes.
- The real reporter, submitted runner and completion consumer pass on this host
  for a 1,024-byte synthetic job with a 16 MiB allowance. Admission observed
  2,996,727,742,464 available bytes. This is not a compiler forecast or proof of
  full-host retention classification. No compiler, actual container or VM ran.
- All seven original owners are consumed with terminal watcher state and actual
  host process exits. Six return zero; controls01 retains its original setup
  failure 2 (wrong working directory, no test executed). Never replay it.
- The existing historical monitor fixture remains unchanged. New CI tests live
  beside the operational tool. Test-created temporary directories retire through
  their fixture context; the tiny host payload is retained as this proof's output.

Can this be done on the VM? The portable refusal/routing controls use disposable
synthetic roots. Actual host filesystem availability, shared Git registry and PID
namespace/exit verification are host facts; no handheld or personal-cloud action
was needed. The plan was recorded in #493 before execution.

This slice performs **no deletion**. Automatic qualified-artifact retirement,
interrupted-cleanup reconciliation, remaining historical classification and real
build resource telemetry remain open #493 criteria. Directory identities are not
recursive content seals. The consumer proves recorded process and process-group
exit, not arbitrary root-only dependencies or escaped sessions. The operational
entrypoint guard is not a security boundary against deliberate bypass. Source
review here is local; no independent/cross-lab audit is claimed.

`source.json` binds implementation inputs; `consumption.json` retains original
result and process channels; normalized logs retain their original/public hashes.
`host-proof.json` records the real admission and consumption. Private raw host
inventory stays with its owner; the public summary gives its bounded scope.

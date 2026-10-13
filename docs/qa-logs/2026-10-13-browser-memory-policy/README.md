# WebKitGTK memory policy feasibility — 2026-10-13

Refs [#570](https://github.com/pixelelated/distribution/issues/570).
**Source-only diagnostic candidate, not a fix or a measured saving.**
GTK3/WebKitGTK 2.54.1 exposes a usable per-WebProcess cleanup control. The
candidate changes only the strict fraction from **0.50 to 0.35**, selected with
`CLOUD_SIGNIN_MEMORY_POLICY=strict35`; `default` restores engine defaults in the
same diagnostic binary. JS, authentication, ephemeral storage, related popups,
input, and the existing renderer workaround remain in the source.

The hypothesis is that releasing reclaimable caches and collecting dead JS
earlier may reduce kernel reclaim during sign-in. The competing hypothesis is
that extra GC, cache misses, and recompilation worsen responsiveness. Neither is
established. This control cannot fix a large live JS/DOM working set, control
total browser PSS, or resolve time spent executing page scripts. It changes the
periodic decision only in the **35–50% of physical RAM RSS band per WebProcess**;
above 50%, both arms already request strict cleanup. Do not run or interpret the
comparison until the coordinator's attribution shows whether that band and the
30-second periodic monitor are relevant.

The WebProcess cache is a poor lead for this specific short, low-RAM GTK3 flow:
the exact source disables it below 2 GiB and when navigation process swapping is
off. Its upstream five-minute expiry fix is already present. WebCore's resource
cache is separate and remains relevant. Details and caveats are in
[source analysis](source-analysis.md); [upstream checks](upstream.md) distinguish
existing changes from unresolved reports.

## Packet and provenance

- [inputs.json](inputs.json): 38 SHA256-bound source/build-configuration/evidence files,
  source anchors and line numbers. Read-only accepted cache is WebKit2.54.1
  under `m7-pixelelated-replacement20`; the two packaged patches are bound too.
  The archive digest is the recipe digest, not a new full-archive measurement.
- [context-policy.c.inc](context-policy.c.inc), [strict35.patch.gz](strict35.patch.gz),
  and [candidate.json](candidate.json): helper, exact compressed unified diff,
  raw patch hash/name, baseline and derived C hashes. No production file changed.
- [prepare.py](prepare.py): source/hash/AST validator, and optional deterministic
  C emission. It imports no target code, launches no child process or network,
  and writes nothing except stdout. No GNU patch dependency.
- [next-experiment.md](next-experiment.md): the conditional, serialized VM test
  and preservation/observation requirements. All compile/runtime steps UNRUN.
- [verification.json](verification.json), [static-validation.json](static-validation.json),
  [SHA256SUMS](SHA256SUMS): actual static checks and discovery failures.

The assigned clean feature branch merged `next` at
`1a37cde40ab0893c9c21c0a383c59ac0c1403b06` using merge commit `eb120acd2a`.
Published work was not rebased. The current #570 body/comments, canonical rules,
checkpoint and D-WORKFLOW-163 were read. Delivery03 is COMPLETE; none of its
historical owners or commands was replayed. The proxy packet's target saving is
390 KiB, and its listener proofs are already accepted. Nothing here reruns or
revises those receipts. GTK4 and proxy work remain diagnostic paths under
D-WORKFLOW-163. Today's provider controls establish pressure without the proxy;
they do not establish a leak or identify page/CPU/reclaim causation.

## Verification boundary

Only static source/hash/AST and patch checks ran. No compiler, browser, VM,
service, provider/account operation, package install, full cache copy, or runtime
fixture ran. The accepted cache was read only. This packet adds no shared
record, production recipe, source, or pin change. The coordinator owns issue,
GitHub, delivery, integration, and any later runtime allocation.

The immediate executable step is the static command in
[next-experiment.md](next-experiment.md). The remaining blockers are compile/API
validation on the installed target pair, a source-bound observer/runner from the
coordinator, and target evidence of activation, benefit, and preserved behavior.
No amount of source inspection closes those acceptance items.

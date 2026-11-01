**Verdict: ready with named changes; do not post the current version unchanged.**  
Keep T1 and T2 first, but correct the under-depth sensitive slices, hidden review workload, and unenforced prerequisites before seeking the maintainer’s yes.

This is an advisory review of the four embedded documents only. Citations below bind to the declared paths and embed-verified SHA-256 values recorded in the inline `corpus.provenance.json` below. I did not access the filesystem, rerun generators, or independently verify hashes.

## 1. The gates and the first three

**minor — G1: The leading positions and nominal read sizes meet the requirement.**

T1 explicitly gates `0.1` and has 11,560 read lines; T2 explicitly precedes #336 Step 1 and has 9,598. Both are among the first three. Their named contents—OS launch/control/state scripts, then ES launch, proxy cards and save-state bookkeeping—are sensible boundaries.

T3 is not a 95,398-line code read, so that total does not itself violate the size limit. However, being a table does not establish that its work fits one session; see **Z1**.

T1’s exclusion of `backuptool` is deliberate, not an overlap error: `areas.json` assigns it to cloud sync, and T6 owns it. Consequently, T1’s completion must not be described as review of *all* state-preservation code. Its gate needs explicit contract checks against the excluded dependencies.  
**Evidence:** `docs/reviews/order.md`, T1–T3, T6; `docs/reviews/areas.json`, `os-scripts-and-launch` and `cloud-sync-and-saves`; `docs/reviews/plan-for-the-plan.md`, §§5, 6a.

**material — G2: T10’s “before #336” prerequisite exists only in prose.**

T10 says it must be read before the runner replacement begins, but its gate is `none`. Position ten does not enforce that prerequisite against a parallel feature lane.

I would move **current T10 immediately after T2**, and record an explicit prerequisite before #336 Step 1. Moving it alone is insufficient: the gate must also appear in the generated issue/brief dependency. This enforces the order’s own promise; it is not a third requirement being attributed to D-WORKFLOW-102. Recount its locally authored patch-reading work when confirming the first-three budget.  
**Evidence:** `docs/reviews/order.md`, “How the order was argued,” T2, T10; `docs/reviews/plan-for-the-plan.md`, §§6a, 8.

## 2. The argument from the lenses

**minor — L1: The broad argument is sound, but its quantitative ranking is not independently checkable here.**

Early dead ends, then saves and credentials, central build machinery, shipped devices, and records last are defensible applications of the six lenses. Framework-after-consumers is also a reasonable way to learn the actual use cases first.

However, the underlying scores, churn evidence and cross-reference results are in unembedded `assessment.md`, `p1-tracking.md` and `cross-reference.md`. I can assess the stated reasoning, not confirm its numerical basis. Also, “package currency” is a renovation question, not one of §6a’s six ordering lenses; its priority should be connected explicitly to security, planned change or cost against value.  
**Evidence:** `docs/reviews/order.md`, “How the order was argued” and slice lens fields; `docs/reviews/plan-for-the-plan.md`, §§4, 6a.

**material — L2: Locally authored functional patches should not wait for the late vendor table.**

T39 explicitly includes fork-written patches that will be read line by line, including a shipped H700 kernel patch. Treating those as late, Local-depth provenance work separates local behavior from its owning device/package review.

Move the **fork-written H700 kernel patch from T39 into T17**. Move other genuinely local patch logic into the slices owning the patched packages, retaining their provenance rows. The exact remaining path assignments require the unembedded selectors/inventory rows; I would not invent them from package names alone. Upstream-carried provenance-only patches can remain late.  
**Evidence:** `docs/reviews/order.md`, T17, T39; `docs/reviews/plan-for-the-plan.md`, §§3, 5, 6c.

**minor — L3: Improve the cloud/proxy adjacency without enlarging a slice.**

Move **current T8 immediately after T6**, yielding the block **T5, T6, T8, T7, T9**. This keeps the cloud scripts and pages together, followed by the proxy and its pages. It better implements the stated brittleness/seam rationale at little scheduling cost.  
**Evidence:** `docs/reviews/order.md`, T5–T9 and “How the order was argued”; `docs/reviews/plan-for-the-plan.md`, §5.

## 3. Seams

**material — S1: Several dependency entries are asymmetric or insufficiently actionable.**

The clearest omissions are:

- **T8 → T2:** T2 expressly identifies `FileData::launchGame`’s running-sync decision and its interaction with `ThreadedCloudSync`. T8’s context names cloud scripts and text/style rules, but not the launch consumer. An executor reading T8 alone could miss that contract.
- **T1/T11 → T24:** T24 identifies `ApiSystem` as the bridge calling these OS scripts. Neither earlier slice explicitly names that bridge in its context.
- **T3 → patch ownership:** `areas.json` excludes patches from generic packages. The inventory separately lists the unreached generic `busybox` unit and its patches. Removing that package directory therefore crosses T3/T4 ownership; T3 names the override but not this deletion handoff.

There is also a **candidate seam, not established by these documents alone**, between T6’s settings backups and T26/T27’s settings and last-good persistence helpers. The cross-reference evidence should settle it explicitly.

For each important cross-slice contract, name the read-only paths, shared state or interface, proof owner, and point at which both sides are checked together. “Every page” or “the packages they patch” is useful orientation, not an executable context specification.

For removals, co-locate the removable unit’s paths or declare coordinated remediation ownership **before dispatch**. Do not discover the need to re-scope during the audit. Splitting large interacting systems is reasonable, but adjacency and read-only context alone do not replace the joint check that §5 intended.  
**Evidence:** `docs/reviews/order.md`, T1–T4, T6, T8, T11, T24, T26–T27; `docs/reviews/inventory.md`, “The unreached set,” `packages/sysutils/busybox` and its patches; `docs/reviews/areas.json`, `generic-packages` and `patches-and-configs`; `docs/reviews/plan-for-the-plan.md`, §§5, 7.

## 4. Sizing and kinds

**material — Z1: The read counter is not a complete workload estimate.**

Three cases need correction:

| Case | What the current number conceals | Required change |
|---|---|---|
| **T14 doctrine** | 190 code lines, but 59,715 total lines. Rules and skills alone account for 20,400 lines in the inventory. The prose is the object of this review. | Budget mandatory prose reading and split T14 into consecutive bounded doctrine slices at its current position. Exact cuts need per-path data. |
| **T3/T4 tables** | T3 covers 1,587 paths; T4 requires 778 patch rows. Origin, upstream status, applicability and removal decisions are not automatically cheap because code-read size is zero. | Show generated/prepopulated evidence and bound the remaining manual decisions, or split by package groups. |
| **Patch/config work** | T7 and T10 require locally authored patch reading; T39 reports zero read lines despite requiring some line-by-line reads. T17/T20 require kernel-config comparisons. | Report patch-reading and config-comparison work separately and include it in session sizing. Do not count whole configs as mandatory line-by-line reads when the required operation is a diff. |

There is also a method inconsistency: the plan says vendor-carried patches are never read line by line, while the order introduces exceptions for fork-written patches. That may be a good improvement, but it needs an explicit provenance/review-action rule rather than silently retaining `0 read` and Local depth.  
**Evidence:** `docs/reviews/order.md`, slice-kind definitions, T3–T4, T7, T10, T14, T17, T20, T39; `docs/reviews/inventory.md`, “Read size per area” and doctrine units; `docs/reviews/plan-for-the-plan.md`, §§2–3, 5.

**minor — Z2: Large currency totals are not automatically oversized.**

T22–T27’s large total-code figures should not be confused with their fork-own reading budgets. The latter range from 4,930 to 9,541 lines and fit the nominal guide. Currency comparison and any retained upstream code needing deeper investigation still require time.

Conversely, small fork-own counts do not make device slices empty: their configurations and provenance questions justify keeping device-specific contexts separate. I see no mandatory merge merely because a slice is small.  
**Evidence:** `docs/reviews/order.md`, T17–T19, T22–T27; `docs/reviews/plan-for-the-plan.md`, §§2–3, 5.

**minor — Z3: Keep T32 whole, but describe it as an explicit exception.**

The shared-fixture rationale is reasonable for a 14,238-line file. I would retain T32 provisionally, with a session budget covering the audit and punch list as well as reading.

However, §5 literally permits “one package group” or “one device”; it does not say “one unit,” as T32 claims. Correct that citation and record the one-file exception explicitly.  
**Evidence:** `docs/reviews/order.md`, T32 and “One deliberate exception”; `docs/reviews/plan-for-the-plan.md`, §5.

## 5. Depth

**material — D1: The sensitivity list and assigned depths disagree.**

The order itself places these files on its security/state lists, while their owning slices remain Independent:

| Slice | Explicitly sensitive owned material |
|---|---|
| T8 | `CloudTransferJob`, `ThreadedCloudSync` — state |
| T9 | `RetroAchievements.*` — security |
| T12 | `scripts/get_env` — security |
| T22 | `GuiWifi.*` — security |
| T26 | `HttpReq.*` — security; `Settings.*`, `SystemConf.*` — state |
| T27 | `AtomicFileUtil.*` — state |
| T29 | `.githooks/**` — security |

These require **Extended review**, either for the existing slice or for a separately cut sensitive subset. Calling the surrounding slice “ordinary” does not resolve the contradiction. T9’s claim that credential handling belongs to the proxy needs reconciliation with its own security classification.

The slice descriptions additionally identify:

- **T11:** root-running system services, expressly under the security lens.
- **T16:** standalone emulator start scripts—launch-path work.
- **T23:** credential wiring for scrapers.

Under the plan’s stated categories, these also need Extended depth or a documented, evidence-backed scope distinction. T16/T23 additionally warrant checking the completeness of the sensitivity globs.

This affects drift too: reopening a sensitive file “at its original depth” preserves an initially insufficient depth.  
**Evidence:** `docs/reviews/order.md`, named slices and “The security, state-preservation and launch-path files”; `docs/reviews/plan-for-the-plan.md`, §§6a–6c, 8.

**material — D2: Local-depth code exceptions need explicit treatment.**

T15 is a 9,327-code-line read, not merely a small configuration table. Assign at least Independent depth unless the maintainer expressly adopts another policy.

T28 and T35 also contain code reading but use Local depth. They may merit inexpensive exceptions, but §6c currently authorizes Local for tables and doctrine reads—not a general “small recipe/upstream currency” category. Name and justify those exceptions rather than presenting them as already established policy.  
**Evidence:** `docs/reviews/order.md`, T15, T28, T35; `docs/reviews/plan-for-the-plan.md`, §6c.

## 6. Coverage and reachability

**minor — C1: The reported totals are coherent, but they are not an independently reproduced coverage proof.**

The two tree counts sum correctly: 133,477 + 1,114 = 134,591. The apparent patch discrepancy is also explainable: 1,709 patch-area files plus 10 doctrine patches and 50 records patches gives 1,769. Clarify the scope of the `find` comparison rather than treating those numbers as evidence of missing patches.

I cannot establish a concrete false “unreached” label from the embedded material. Build-plan reachability is evidence; deletion still needs the caller/selection checks required by Q6.  
**Evidence:** `docs/reviews/inventory.md`, tool checks, “Per area,” “The plans”; `docs/reviews/plan-for-the-plan.md`, §§4, 6.

**material — C2: Fork-touched paths and authored code need separating in T41.**

T41 is provenance-only, yet reports 14,487 fork-own code lines. The inventory includes fork-own classifications for doctest and files in libretro-common/rcheevos.

That does **not** establish 14,487 lines of locally authored changes: adding an unchanged third-party library also appears in a merge-base diff. But the converse matters too—version-only review must not hide genuine local modifications.

Require an import/origin comparison that distinguishes unchanged imported material from local deltas. Route genuine local changes to line-by-line review at the appropriate depth. The council toolchain’s byte-for-byte export exception is explicitly authorized; T41 needs equally explicit evidence for its treatment.  
**Evidence:** `docs/reviews/order.md`, T41–T42; `docs/reviews/inventory.md`, interface units; `docs/reviews/plan-for-the-plan.md`, §§2–3.

**material — C3: T15’s promised runtime distinction is not represented by its reachability labels.**

T15 promises to read shipped-device quirks and table the rest, but all 333 paths are labelled `shipped`. That may correctly describe package installation; it does not identify which model-specific paths are selected at runtime.

Supply a model-selection query or explicit subset for that split. Do not infer that an installed-but-inactive quirk is “unreached” merely from the shipped-device list.

Likewise, preserve the distinction between T3’s `unreached` and `unshipped` paths: the latter are reached by plans, just not shipped plans.  
**Evidence:** `docs/reviews/order.md`, T3, T15; `docs/reviews/inventory.md`, reachability totals and unshipped-set definition.

**material — C4: Two required P1 tools have no visible owner in the rendered selectors.**

The plan requires `tools/renovation-drift` and `tools/renovation-status`. T29 explicitly selects `renovation-inventory`, but neither of the other two appears in the displayed tooling selectors.

This does not prove that existing tracked files were omitted: they may not yet exist at the inventory snapshot. It does require reconciliation. Add their ownership to T29, account for their tests, and regenerate the census before asserting final P1 coverage.  
**Evidence:** `docs/reviews/order.md`, T29–T34, T42; `docs/reviews/plan-for-the-plan.md`, §§6, 9.

## 7. Anything else

**material — P1: Make the drift contract executable and unambiguous.**

Before relying on drift to preserve this investment, settle:

1. **Repository-qualified baselines.** Distribution and ES have different histories. A bare hash plus `git diff … next -- es:…` is not an executable cross-repository specification. Record the repository, reviewed/fixed commits, and the relevant ES pin relationship.
2. **Accepted-drift checkpoint.** Small drift advances `reviewed-at`, while the tool is specified to compare from `fixed-at`. Define the checkpoint that advances after a successful no-fix drift review, so already-reviewed drift is not repeatedly reported as outstanding.
3. **The exact boundary and denominator.** “Under 20%” and “over 20%” leave exactly 20% unspecified. Prefer `<20%` versus `≥20%`, and define the denominator for read, currency and table slices.
4. **Dependency replacement.** Demonstrate the promised reopening when an interacting subsystem changes even if the dependent slice’s own paths do not.

The implementations and fixtures were not embedded, so these are specification gaps to reconcile, not claims that the tools currently malfunction.  
**Evidence:** `docs/reviews/inventory.md`, tree identities; `docs/reviews/plan-for-the-plan.md`, §§3, 8; `docs/reviews/order.md`, sensitivity section.

**minor — P2: Correct the small handoff inconsistencies when regenerating.**

- T12’s rationale says 12,328 read lines; its slice count is 6,776.
- T1 asks for five phase files; the plan’s brief requires six.
- The opening says the order was posted at pass 7, while the footer describes a pending review before that post.

These are inexpensive corrections, but executors should not have to choose between conflicting instructions.  
**Evidence:** `docs/reviews/order.md`, opening, T1, T12, final section; `docs/reviews/plan-for-the-plan.md`, §7.

### Corpus and gaps for the orchestrator

The following is the inline artifact for `corpus.provenance.json`. Unembedded inputs are **not asserted absent from the repository**. They limit verification of selectors, scores, call edges and tool behavior; supplying them would allow those questions to be settled.

```json
{
  "access_mode": "embedded corpus only",
  "filesystem_access": false,
  "independent_hash_verification": false,
  "hash_verification_origin": "Council Facilitator: verified at embed time",
  "manifest_read_timestamp_utc": "2026-10-22T20:09:11Z",
  "source_file_paths": [
    "docs/reviews/order.md",
    "docs/reviews/inventory.md",
    "docs/reviews/areas.json",
    "docs/reviews/plan-for-the-plan.md"
  ],
  "source_file_hashes": [
    "7f537288564682ebbf794592833b9cac60aa57cc65e8dc339e3335c0b4b8be91",
    "1b0eac803cb0d46a742d0f7072416311f8e97aa4eb060fb278d8e048c34882db",
    "985f742cfd4a2138339f1ed41bd5f5f9e3755fe69b309ff3ddb10d1466fced90",
    "f01f2b82cc628073640050bcb56cbc9a2e5c9e9a8a289978b171897ce9951f0f"
  ],
  "hash_path_mapping": "Corresponding array indices identify each source.",
  "unembedded_referenced_inputs": [
    {
      "references_as_written": [
        "slices.json",
        "docs/reviews/inventory.json"
      ],
      "verification_gap": "Exact selectors, per-path provenance, sensitivity ownership and reproducible slice coverage."
    },
    {
      "references_as_written": [
        "assessment.md",
        "p1-tracking.md",
        "cross-reference.md"
      ],
      "verification_gap": "Underlying lens scores, supporting measurements and cross-area edges."
    },
    {
      "references_as_written": [
        "tools/renovation-inventory",
        "tools/renovation-drift",
        "tools/renovation-status",
        "tools/lint-audit-artifacts"
      ],
      "verification_gap": "Implementation behavior and required positive/negative fixture evidence."
    }
  ],
  "limitations": [
    "No generator, build, reachability search or test was run by this reviewer.",
    "Names without full paths above are retained as referenced, not expanded into fabricated paths.",
    "No hashes or contents are asserted for unembedded inputs."
  ]
}
```

## Changes I would make, in priority order

1. **Correct sensitive-slice depths**, and explicitly resolve the Local-depth exceptions.
2. **Expose the real workload:** split doctrine appropriately, bound table work, and account for local patches/config comparisons. Separate imported material from genuine fork changes.
3. **Enforce the #336 prerequisite and adjust the sequence.** Using current labels, my preferred prefix is:  
   **T1 → T2 → T10 → T3 → T4 → T5 → T6 → T8 → T7 → T9 → T11 → T12**, then the remaining order subject to recuts.
4. **Add explicit seam contracts and deletion ownership**, including launch/cloud interactions and package/patch removals; move the local H700 patch into T17.
5. **Resolve the drift specification and assign the remaining P1 tools to T29**, with fixture evidence.
6. **Regenerate—not hand-edit—the order and counts**, then update the review record and posting status. Preserve stable slice IDs while renumbering positions.
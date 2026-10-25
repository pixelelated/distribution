Source review only; no rerun. Unqualified line references below are to `last-good-scripts-test` at `8ebaf8daad`.

## Revisited findings

| Item | Review | Why and lines |
|---|---|---|
| **F-07** | **confirmed with narrowing** | This holds against **T14’s `7c1d729b57` S8 contract**, not the callees at `8ebaf8daad`: the former validate provenance (`settings-modes-test :19–31`; `melonds-upgrade-test :39–68`), while the latter merely copy the supplied binary (`settings :5–8`; `melonds :23–40`). The ordinary scratch copy at `:417–418` is outside `image/system/`, and `:14224–14232` supply neither provenance flag, so the new callees refuse it with exit 2. “Every host” is too absolute: a scratch directory itself under a qualifying image root would behave differently. |
| **F-09** | **confirmed with narrowing** | The mixed missing-input policy is visible—FAIL at `:4004–4008` and `:4296–4297`, group SKIP at `:6490–6491`—as are silent omissions, e.g. `:7040–7078`, `:10128–10141`, and the BusyBox probes at `:8776–8780`. But dependency SKIPs are not PASSs: t’s missing-client SKIP already prevents ordinary exit 0 (`:2059`, `:14236–14238`). Also, one of x/D’s 21 skip sites depends on **p**, not t (`:7227`). The closing branches of F1r-d and D31 are not supplied, so their specific “no else” claims remain unverified. |
| **F-17** | **confirmed** | All named leaks are present: g’s constants (`:845–851`), h’s fallback constants—not its correctly selected wrapper (`:865`, `:887–890`)—i’s executions (`:903–928`), t’s imported helper (`:2427`), and C7’s current index/worktree modes (`:6505–6507`). Additional same-defect sites include current package pins at `:3999`, `:4291`, and `:10344`, and current WebKit patches/version at `:6481–6485`. |
| **F-19** | **confirmed with narrowing** | The quoted `printf` fixtures do **not** execute their payloads during construction. However, `sf_valid` runs the extracted validator unsandboxed (`:13671`); a regression that evaluates those payloads targets fixed **host** `/tmp/s3f-*` paths (`:13672–13777`—specifically `:13672`, `:13675`, `:13677`). Stale files make `:13678` fail, and the shown setup does not reset them; the EXIT trap only removes `${TMP}` (`:294`). Mere erroneous acceptance need not execute a canary. |
| **F-21** | **confirmed** | Applicability tests only whether `BB` is nonempty (`:13399`); the measurement executes `${BB_HOST}` and calls it “the image’s busybox” (`:13402–13406`). Matching the expected unzip behavior does not establish candidate provenance. With no BusyBox, this block does explicitly SKIP (`:13422–13424`). |

## F-08: does the refutation stand?

**Yes, as a refutation of F-08’s categorical claim that N/A is a hidden PASS.** This is not simply “file missing ⇒ retired”:

- An existing engine is loaded from the selected source (`:4548–4551`).
- Otherwise, the **selected source’s recipe** is read; a recognized installation command for the missing engine causes exit 2 (`:4553–4556`).
- aa’s engine load is inside the applicability condition (`:13722–13731`). Its live no-folder-check assertions remain outside that condition (`:13898–13910`), and ae retains archive coverage (`:14183–14189`).
- The summary explicitly excludes N/A checks from PASS (`:14235`).

**But this is not an unconditional proof of retirement.** It establishes absence of the engine and of one recognized installation spelling. That distinction matters: G-05 below identifies a concrete misclassification path. The supplied packet does not establish that the actual recipe at `8ebaf8daad` takes that path.

## Further G-n findings

- **G-05 — Low: the retirement probe is syntax-fragile.**  
  `:4554` recognizes only a line beginning with `cp cloud_migrate_layout`. A selected recipe containing, for example, `cp -f cloud_migrate_layout …` still requires the file, but would not match; with the engine missing, `:4558–4559` would declare retirement. The gate should validate a recognized retirement/install contract rather than equate absence of this spelling with “does not install one.”

- **G-06 — Medium: a Python driver can crash after one PASS and silently lose the remaining predicates.**  
  D13b ignores the Python process status and accepts any verdict line (`:7320–7357`). For example, after the PASS at `:7337`, failure while importing the helper or calling `damaged` (`:7340–7347`) leaves that PASS to be replayed, with no FAIL for the omitted checks. D13c has the same aggregation pattern (`:7370–7432`). Require successful driver completion **and the complete expected verdict-ID set**, not merely one printed verdict.

- **G-07 — Low: S3F has concrete PASS paths when extracted functions are absent.**  
  Three empty `conf_valid` extracts compare equal (`:13668–13670`). An absent `sort_settings` returns 127, but its status is discarded and the untouched fixture satisfies `:13690`. An absent `ack_index_pending` prints `rc=127`, which matches the unanchored `grep -q 'rc=1'`; the pre-existing B marker then satisfies the remaining predicates (`:13713–13715`). Assert extraction/function presence, verify that the injected operation was reached, and capture or match statuses exactly. Companion positive checks may fail; these are individual false PASSs, not proof of whole-suite false success.

- **G-08 — Medium: D29 does not force the concurrent-marker scenario it claims.**  
  The helper gets a timed wait, and the harness polls for its start without asserting that the poll succeeded (`:10328–10330`). If the foreground harness resumes only after the top-up finishes, the second `index-offline` writes its marker afterward; both exits are zero and the marker exists, so `:10333` passes even with broken acknowledgement of markers written **during** a run. This is another instance of G-04’s synchronization problem. Hold the helper at a barrier until the replacement marker has been written.

- **G-09 — Low: D21 does not actually require mode `100755`.**  
  `:7776` rejects only `100644` and `none`, despite claiming all four scripts are committed executable. A symlink’s Git mode `120000`, for example, passes this predicate. Compare every returned mode exactly with `100755` (`:7771–7776`).

- **G-10 — Medium: child setup refusals are flattened into script regressions.**  
  Both writer-test calls pass every nonzero result to `check` (`:14224–14233`), which increments `FAIL` (`:310`), ultimately producing exit 1 (`:14238`). Thus S8’s **CANNOT/2** becomes a reported regression rather than inability to run. The same wiring would flatten **unverified/3** when that mode is forwarded (`settings-modes-test@7c1d729b57 :73`; `melonds-upgrade-test@7c1d729b57 :173`). Passing the new flags alone does not fix this: the caller must explicitly preserve the distinctions between failure, inability, and unverified evidence.
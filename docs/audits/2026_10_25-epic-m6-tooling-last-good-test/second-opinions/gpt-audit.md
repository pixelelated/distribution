I reviewed the supplied source excerpts. I did not rerun the suite; execution results below are the first reader’s reported observations, not independently reproduced runs.

## 1. BusyBox fallback and banner

**Read:** `:147–160`, `:234–250`, `:381–426`, `:14235–14238`.

**F-01’s substantive defect is real, but “silently” is inaccurate when a BusyBox is found.**

- After the three searches fail, `:400` returns the host’s BusyBox path—or an empty string with success.
- With host BusyBox, `:426` **does print its banner and source path**. What is missing is an explicit qualification that this is **not candidate-image evidence**, especially in the final verdict.
- With no BusyBox, no copy or wrappers are created (`:415–423`), and the **tool banner** is absent (`:426`). The general suite banner at `:425` still appears. Wrapped commands can then resolve to host tools; this does not guarantee the entire suite will finish, because other cases may require BusyBox-specific paths/applets.

**I recommend refusal, exit 2, for the existing command.** Its foundational requirement is candidate-device applet semantics, not merely finding something named BusyBox. A suitable diagnostic is:

> CANNOT RUN: no candidate image BusyBox found; host tools will not be substituted. Set QA_SYSTEM_ROOT.

An explicitly requested **host-diagnostic mode** could instead exit 3, but it should mark every result as unverified host-tool evidence and finish with **NOT DEVICE EVIDENCE**, never ordinary `PASSED`. Host-diagnostic failures must not masquerade as candidate regressions.

The normal verdict should identify the selected tool provenance, not leave that information hundreds of lines above it. Fixing selection alone also does not fix the unwrapped execution in section **b**; see G-01.

## 2. Sandbox network and environment

**Read:** `:289–295`, `:8895–9032`, particularly `:8993–9022`.

**F-16 is substantially right about `sa_run`’s default sandbox.**

There is no `--unshare-net` or `--clearenv`. `setsid`, `timeout`, filesystem mounts and `--die-with-parent` do not provide either isolation. The helper overrides `PATH` and `HOME`; the harness previously unsets `TMPDIR`. Other exported caller variables remain available, subject to normal executable/setuid sanitization. This is not a claim that every unexported shell variable survives, or that every other sandbox in the suite has this configuration.

The fixture’s alias remote (`:8997`) and route/ping shims (`:8970–8971`) make ordinary execution local; **they do not enforce locality**. Inherited `RCLONE_*` settings can change behavior, and an inherited `BASH_ENV` naming a visible file can affect shell execution. The shared network permits unintended external access.

That matters both for reproducibility and for the claimed safety boundary. The packet establishes no actual external connection, but “no cloud or player-data risk” is stronger than this containment supports.

Use network isolation and an environment allowlist by default, with explicit case-specific exceptions. Sanitize the launcher too: clearing the sandbox environment cannot undo `BASH_ENV` effects on the harness’s own startup.

## 3. `check $?` after compound tests

**Read:** `:270`, `:309–311`, `:481–514`, `:533–604`, `:2086`, `:3013–3062`, `:3324–3329`, `:8776–8787`.

### Correct findings

- **F-11 is correct at `:3051`.** Semicolons separate the three `is` tests; only the final status reaches `check`. A concrete counterexample: make the first `sa` incorrectly produce the **third** case’s expected configuration. The first `is` fails, skipping the second `sa`; the second `is` fails, skipping the third `sa`; the final `is` nevertheless passes on the first run’s files. This is the three-case fallback test, not the separate START NEW GAME check at `:3052`. Record each case separately.
- **Ordinary `[ ... ] && [ ... ] && grep ...; check $?` preserves failure correctly**, as at `:511` and `:8723`: success requires every command to succeed. That validates status propagation, not necessarily the adequacy of the predicates or fixture.
- **F-15 is correct at `:548`.** `!` negates the pipeline’s status, which here comes from `grep`. An unreadable archive/member can therefore become successful “absence.”

**Adding `pipefail` alone does not repair that negative assertion.** A failed producer still gives a nonzero pipeline status that `!` turns into success; `grep -q` can also cause producer SIGPIPE. First require successful extraction into an owned file, then distinguish grep’s **no-match status 1** from its error statuses.

The companion at `:547` is weaker than the first reader suggests: listing `test/f1` does not prove that the particular `system.cfg` member at `:548` exists and was read successfully.

### Corrections and additional sites

- **The Q3 criticism of `:3053` is wrong for a nonzero `sa` return.** Every `sa` there participates in the `&&` chain; its nonzero status cannot be discarded. By contrast, `:3061–3062` really does discard `sa`’s status before checking that no `-e` appeared.
- **The claim that `:3329` passes on empty `F1_WROTE` is also wrong.** The here-string supplies one empty line. At `:3328`, that makes the tested path the existing `${F1}/b/` directory, and the assignment appends a space to `F1_LEFT`; `:3329` then fails. Moreover, `:3326` already rejects an empty `F1_WROTE`.
- **Another negative-pipeline weakness is `:8784`.** A nonempty archive pathname and a readable summary do not prove that the complete archive was successfully scanned for the planted value. Both tar pipelines discard producer failure.
- **`:599` has the same negative-pipeline problem** if the first grep cannot read the output. Its adjacent positive screen assertion may catch the broader failure, but that particular PASS is not evidence of a successful scan.

## 4. Standing of the `--old` controls

**Read:** `:162–226`, `:313–369`, `:1781–1789`, `:1857`, `:2051–2086`, `:3002–3003`, `:14235–14238`; first reader `02`’s control-run table.

The reported twelve runs establish **broken full-run recipes**, not that every earlier observed negative control is worthless. A correctly reached, correctly attributed FAIL before the eventual exit 2 remains evidence for that particular guard. The first reader’s blanket “no controls from s onward” formulation is contradicted by its own reported runs reaching s, t, u and v.

**Do not implement F-05 as “any script absent at BASE_REF makes its section NOT APPLICABLE.”** `src_of`’s refusal protects against grading empty source as a genuine historical implementation. The header even explicitly expects absence of the old proxy script to be a failing observation (`:180–184`).

Distinguish:

1. **Invalid/unavailable ref or unreadable required input:** CANNOT, exit 2.
2. **A required historical feature is absent:** an explicit presence-contract failure may be valid, but it does not demonstrate execution of a behavioral guard.
3. **An unrelated, newer section excluded from a particular control’s declared scope:** legitimately unselected/not applicable.
4. **A selected check that cannot execute:** incomplete/SKIP, not PASS. If execution continues, preserve that incompleteness in the summary and exit policy.

The useful fix is **per-control selection with explicit fixture dependencies and expected failing check IDs**, plus ref/input preflight. Section t must also select the historical package pin, not mix current source with old patches.

A genuinely retired feature can be outside the current product’s test obligations. That is why **F-08’s categorical objection to N/A is not sound**. The important question is whether the availability gate establishes retirement or merely mistakes a missing required file for retirement; that gate is absent from this packet.

## 5. Splitting the file

**Read:** `04` § Q6, the section/group index, `:320–369`, `:8684–8715`, `:8993–9022`, `:14177–14238`.

I agree with a **subject-oriented split**, and with establishing smaller independently runnable controls before physically splitting everything.

The costs are real: fixtures currently depend on earlier sections’ globals and artifacts; tool selection/copying, source selection and sandbox policy need shared implementations; result aggregation must preserve FAIL, CANNOT and SKIP rather than flattening every nonzero child status.

The gains are maintainability, independently selectable controls, clearer attribution and explicit dependencies—not automatically shorter full-suite runtime. A split alone also does not solve historical applicability.

Two qualifications to the proposal:

- The quoted **2,166-line maximum** describes stream A, not the proposed combined cloud subject file containing A, CF and other sections.
- **ae is not wholly retired**: `:14183–14189` deliberately retains live archive contracts after retiring the migration matrix.

**Yes to the cheaper half first—but not its blanket N/A implementation.** Add control selection, explicit setup dependencies and reliable completeness reporting first.

## Findings F-01 to F-21

| Finding | Review | Reason and lines |
|---|---|---|
| **F-01** | **confirmed with narrowing** | Automatic host/no-BusyBox fallback is real (`:400–423`), and the verdict is unqualified (`:14236–14238`); host BusyBox is nevertheless disclosed by `:426`, so it is not literally silent. |
| **F-02** | **confirmed with narrowing** | rclone has the same unverified selection (`:8908–8914`), but its provenance is printed; compatible behavior under two versions is not itself a test defect or a reason to demand an artificial version-sensitive failure. |
| **F-03** | **confirmed** | Historical read failures do not reliably propagate: the pipeline and final `true` defeat failure handling (`:3208–3214`), and `git show` at `:4271` is unchecked and silenced; downstream failures are not a proper input preflight. |
| **F-04** | **confirmed with narrowing** | The reported runs establish that the refs documented at `:185` and `:191` are unresolved in that checkout; neither global disappearance nor the suggested replacement refs is independently established here. |
| **F-05** | **confirmed with narrowing** | Required-source failure exits the whole run (`:320–325`), making the reported recipes incomplete; that refusal is intentional protection, and automatic N/A is not a sound general replacement. |
| **F-06** | **confirmed** | The pin is read from the working tree (`:2051`) while patches come from `BASE_REF` (`:2075–2083`), contradicting the historical-client claim at `:2034–2036`. |
| **F-07** | **cannot tell from the packet** | The calls pass the copied BusyBox (`:14224–14232`), but the callee validation code is absent and cited at another revision; `02` reports both calls passing at the audited baseline. |
| **F-08** | **refuted** | N/A is explicitly not counted as PASS (`:14235`); excluding a genuinely retired feature can coexist with passing applicable checks. Whether the omitted availability gate wrongly declares retirement remains unresolved. |
| **F-09** | **cannot tell from the packet** | No-BusyBox probe omission is visible (`:8776–8812`), but the download/DT_OK/qemu gates are mostly absent; the explicit group SKIP at `:2059` is not itself a false pass. |
| **F-10** | **confirmed with narrowing** | Failed startup can satisfy individual assertions at `:573`, `:594`, `:8787` and `:8828`; this does not establish whole-suite false success, and the criticism of nonzero `sa` at `:3053` is incorrect. |
| **F-11** | **confirmed** | The final `is` alone determines the recorded status at `:3051`, and it can accept output left by an earlier incorrect run while intervening runs were skipped. |
| **F-12** | **confirmed** | `:13826` supplies two arguments; on failure, `check` expands absent `$3` (`:309–310`) under `set -u` (`:270`) and aborts before counting/reporting the FAIL. |
| **F-13** | **confirmed with narrowing** | `:1835` reports `wait` rather than the sourced pass’s status, and `:1840` pre-creates markers; however, positive start/stop log checks at `:1846–1854` reject a wholesale no-op. |
| **F-14** | **confirmed** | At `:2086`, only `TPATCH_OK` determines the result; compilation occurs inside message construction and cannot make that check fail. |
| **F-15** | **confirmed with narrowing** | `:548` converts extraction failure into successful absence; `:547` checks a different member, not successful reading of `system.cfg`. The same producer-status weakness appears at `:8784`. |
| **F-16** | **confirmed with narrowing** | The default helper shares the network and retains unspecified exported environment (`:9013–9021`); PATH/HOME are overridden, TMPDIR was removed, and actual external access is not demonstrated. |
| **F-17** | **cannot tell from the packet** | The named g/h/i, t and C7 bodies are absent; the independently visible historical-pin mismatch at `:2051` is already F-06. |
| **F-18** | **confirmed with narrowing** | Help overclaims image-tool execution (`:241`) and the header is incomplete (`:7–226`); however, foreground `setsid -f` from a clean parent can avoid shell-background SIGINT inheritance—it merely cannot reset an already ignored signal (`:258–268`). |
| **F-19** | **cannot tell from the packet** | The actual canary construction, execution context and cleanup at the claimed `:13672–13678` sites are not supplied. |
| **F-20** | **confirmed with narrowing** | The probes establish “BusyBox,” not candidate identity (`:8777–8779`, `:8809–8811`); the reported host 1.37 **does not pass these probes**, because it lacks flock. Provenance is chiefly the central F-01 issue. |
| **F-21** | **cannot tell from the packet** | The unzip test and its availability gate at `:13400–13424` are not supplied; the general tool-provenance problem alone does not verify this particular branch. |

## Additional findings / omissions from the F-list

- **G-01 — Medium: candidate BusyBox selection does not ensure candidate applet execution.** Section b’s profile selects `/shim:/usr/bin:/bin` (`:522`), and its sandbox mounts neither the BusyBox copy nor its wrappers (`:536–541`); normal tar delegation uses host `/usr/bin/tar` (`:566`, `:586–590`). Thus the original whole-script kill/restore tests remain host-tool tests even after F-01 is fixed. The first reader notes the missing wrappers in its table but does not carry this independent defect into the findings.

- **G-02 — Medium: `LAST_GOOD_SOURCE_ROOT` also replaces one verifier.** Help promises a separate source checkout **without replacing this harness** (`:248–249`), but ag executes `${ROOT}/tools/settings-modes-test` (`:14224`), whereas ae and ah use `${HARNESS_ROOT}` (`:14188`, `:14231`). Selecting an older/different subject checkout can therefore select a missing or weaker checker. ag should use the harness-owned verifier.

- **G-03 — Low: q’s historical fragment set is the intersection of two trees.** `:1781–1789` enumerates current working-tree filenames, then reads their historical contents and excludes names absent historically. A fragment present only at `BASE_REF` can never run. This undermines the promised whole historical boot pass independently of source-read failure; enumerate the selected ref’s own tree.

- **G-04 — Medium: the corekeeper contention test does not establish overlap.** `:8854–8860` uses sleeps rather than acquisition/entry acknowledgments. If the second handler starts late, the midpoint sees no note and both archives eventually exist—even with broken locking. Use bounded barriers proving that the first handler holds the protected operation and the second has reached it before testing that it waits.

## Sections I need

- **F-08:** `x/C :4540–4565`, plus `aa :13723–13740` and `:13890–13912`, to inspect the retirement/applicability decision.
- **F-09:** `x/F2 :3990–4015` and `:4290–4310`; `x/C :6475–6495`; `x/D :6635–7795` for the DT_OK definition and guarded branches; `y/A :10120–10365`; `y/F1r :11170–11205`.
- **F-17:** `g–i :839–933`, `t :2410–2445`, and `x/C7 :6495–6525`.
- **F-19/F-21:** `z/S3F :13665–13722` and `z :13390–13430`.
- **F-07 requires external code, not another section of this file:** the argument/provenance validation and exit contracts of `settings-modes-test` and `melonds-upgrade-test`, identifying what exists at `8ebaf8daad` versus the later T14 revision cited by the reader.
## Requested checks

### G-1 — High — The shared real-rclone runner is not network- or environment-isolated

**Files:** `tools/rasteratops-cloud-layout-test:66–67,81–96,138–148`; `tools/pixelelated-cloud-validator-test:19–22,326–336`; `tools/pixelelated-content-scope-test:30–43`; `tools/pixelelated-save-layout-test:75–99`; `tools/pixelelated-duckstation-capture-test:123–154`.

All tool references below are at `8ebaf8daad`; lint-fixture references are at `2174265e9c`. This is a source review, not a new execution of the controls.

The isolation differs materially between the runners:

| Execution route | Host IP network | Caller environment | Host configuration files |
|---|---|---|---|
| Ordinary `Fixture.run`, used by cloud-layout, validator and content-scope | **Available:** only PID isolation is requested | Inherited except for the two variables reset by bwrap | Host `/usr` and **all of `/etc`** are mounted read-only |
| Validator’s `public_adoption` sandbox | **Available:** no network unshare | Inherited except `HOME` and `PATH` | Host `/etc` and the listed `/usr` directories are mounted |
| Save-layout’s adapted `Fixture.run` | **Isolated:** it inserts `--unshare-net` | Still inherited | Host `/etc` and substantial `/usr` subtrees remain readable |
| DuckStation’s sandbox | **Isolated:** `--unshare-all` includes the network namespace | Still inherited except `HOME`, `PATH` and `CAPTURE_PROBE` | Curated host binaries/libraries/share directories; not the host’s whole `/etc` or home |

The ordinary fixture does install a synthetic alias configuration at `rasteratops-cloud-layout-test:67`, and sets `HOME=/storage`. That protects against accidentally finding the **usual** configuration beneath the host’s home directory. It does **not** establish that real configuration cannot be read:

- `RCLONE_CONFIG` and `XDG_CONFIG_HOME` are not removed.
- Neither are per-remote configuration variables such as `RCLONE_CONFIG_QA_TYPE`, `RCLONE_CONFIG_QA_REMOTE`, endpoint variables or credentials.
- `RCLONE_DRY_RUN`, filtering/logging options, proxy variables and other behavioral settings also survive.
- `BASH_ENV` and exported Bash functions survive. An imported function can take precedence over a PATH shim; an accessible `BASH_ENV` file can run before the script.
- The wrapper at `81–96` forwards to `/rclone.real` without enforcing a configuration file or sanitizing its environment.

**Concrete failure scenario:** a caller has `RCLONE_CONFIG` pointing to a readable file under `/etc`, or environment-defined settings overriding the fixture’s `qa` remote. The ordinary runner and validator’s adoption runner have both access to those inputs and an outward network route. Instead of operating exclusively on `/cloud`, a test can fail against, read from, or potentially mutate a real remote.

The precise remote operation is an **inference**, because the production scripts and rclone’s implementation are not supplied. The inherited variables, readable mounts and missing network boundary are directly established by these lines. The harness does not enforce the claimed exclusion.

Conversely, do **not** claim that save-layout or DuckStation has the same outward-network defect: their network-unshare flags refute that. DuckStation’s shown rclone transfers also name two local endpoints, for example `:223–230`; merely defining a remote would not change those arguments into a remote transfer.

Finally, cloud-layout, validator and DuckStation run their version probes **outside** bwrap (`:1198`, `:57`, and `:177`, respectively). Those probes inherit the host environment too, although the shown `version` invocation is not itself a transfer.

**F-04 is substantially understated:** this is more than a `TMPDIR` portability failure.

---

### G-2 — High — Guest ownership is not established by the mechanisms used to find and stop guests

**Files:** `tools/pixelelated-vm-cloud-boundaries:44–75,270–302,674–716`; `tools/rasteratops-vm-cloud-epic:34–57,65–95,98,127–131,366–371`.

**Boundaries runner**

It does take useful precautions:

- Requires a fresh, empty output directory and creates private subdirectories (`:48–55`).
- Supplies an owned pair directory to `vm-pair` (`:56–57,277`).
- Refuses if a visible process’s `argv[0]` basename begins `qemu-system-` (`:270–276`).
- Checks the guests’ build IDs, installed script hashes, and distinct boot/device IDs (`:287–299`).

But those checks are not process ownership:

- It records no QEMU PID/start-time identity from `vm-pair`.
- Its own `local()` has no timeout; readiness waiting is delegated to the **unprovided** `vm-pair` implementation (`:64–66,277`). The subsequent SSH calls have individual timeouts, not an explicit boot-readiness loop here.
- SSH uses fixed ports, disables host-key verification, and does not disable the caller’s SSH configuration (`:68–75`). Whether the helper securely binds those endpoints to the newly created pair cannot be verified from this packet.
- It changes guest state **before** checking the build and script identities (`:283–293`).
- The supposed absence check at `:295` is ineffective as a guard:  
  `test ... && test ...; mkdir -p ...` returns the status of `mkdir`, so existing QA state need not make the call fail.

Cleanup is the more serious defect. It signals any process whose `argv[0]` looks like QEMU and **any argument contains the pair-path substring** (`:682–685`). It does not require an actual disk argument beneath that directory, an exact path boundary, or a recorded owned PID. Cleanup runs even when `start()` refused before starting anything (`:712–716`).

**Concrete failure scenario:** an unrelated, already-running QEMU has a `-name` argument containing `<requested-output>/pair`. The requested output directory itself is empty. `start()` refuses because another QEMU exists; `finally` then runs cleanup and sends that unrelated QEMU `SIGTERM`. This tool has started no guest but can nevertheless kill one.

The subsequent wait is up to ten seconds for the discovered PID numbers to disappear (`:686–690`), with no identity revalidation. If discovery finds no matches, both `all(...)` checks are vacuously true and `cleanup.json` says `"all_absent": true` (`:687–694`). Hidden or differently named guests could therefore remain while cleanup reports success. Whether T12 can launch a guest outside this process’s PID view is **inference**; the empty-discovery success is explicit.

**Epic runner**

This runner intentionally borrows an existing guest. It checks a global monitor socket, a global pidfile and a key (`:43–50`). Its pidfile validation searches **any command-line argument** for `qemu-system-x86_64`; it does not bind that PID to the monitor socket, SSH port, disk, image or this invocation. The build ID is merely logged at `:98`.

It can therefore reuse and report on an unrelated guest, and then modify it destructively: `:127` deletes saves, and `:129–130` replaces cloud configuration.

Its waiting also fails open:

- `wait_card()` reaches the end of 60 unsuccessful polls and returns the successful final `sleep` (`:71–78`).
- The remote `pgrep | wc -l` can yield zero when `pgrep` fails; host `pipefail` does not automatically apply inside the guest’s shell (`:74`).
- In `reboot_guest()`, an empty later boot ID differs from a previously nonempty ID and can satisfy `:88`.
- The frontend and idle loops do not assert that their success condition was reached; the function ultimately ends with a successful sleep (`:89–95`).

The shown cleanup does **not** stop the guest QEMU. It kills/waits for the VNC capture child and invokes an external `protocol_cleanup` whose body is not supplied (`:53–56`). The held SSH child in case L is not in that trap; failure of `walk()` can leave it running (`:366–371`, with `walk()` exiting at `:62`).

Both runners refuse ordinary execution against the current retired migration source (`boundaries:709–710`, `epic:22–25`). These are therefore latent defects on their supported historical execution paths, not evidence that stage A killed or reused a guest.

---

### G-3 — Low — The state checker’s reports are non-disclosing; a literal “never writes selected values” claim is not true

**File:** `tools/pixelelated-state-check:97–112,245–257,366–371,378–405,617–680,692–704,739–793,865–905`.

I found **no ordinary report or diagnostic path that prints an inspected credential or account name**:

- Report rows contain policy labels, categories and counts (`:378–405`).
- Input-derived sibling names and recursively discovered names are replaced by policy labels (`:625–650,657–680`).
- Child stderr is discarded (`:105–106`, and `:820–823`).
- Argument errors do not echo supplied arguments (`:865–868`).
- Unexpected exceptions produce a fixed error report rather than an exception string or traceback (`:897–903`).
- The final JSON print serializes that bounded report (`:904`).

But the tool **does write raw inspected data privately during payload inspection**:

- `command()` directs child stdout to a `TemporaryFile` (`:100–112`).
- `Squash.read()` uses that mechanism for `unsquashfs -cat` of selected configurations (`:366–371`). Thus a selected account or credential is temporarily written to that file before parsing.
- Payload inspection copies SYSTEM, the decompressed disk, and the storage partition into a private temporary directory (`:742–793`), using raw writes at `:692–704`.

**Concrete scenario:** inspect a contaminated update tar containing a selected username in SYSTEM. The result contains only the policy finding, but the SYSTEM copy and the selected file’s raw `unsquashfs` output have been written to scratch storage.

That is **not a demonstrated public disclosure**: the temporary objects are private and normally cleaned up. A killed process can leave the named payload scratch copies behind—an **inference about abrupt termination**, not an observed run here. The defensible guarantee is “no values in reports/forwarded diagnostics and no modification of inspected input,” not “no selected value ever reaches disk.”

---

### G-4 — Medium — Both writer tests can report candidate-app\-let success after being given host applets

**Files:** `tools/settings-modes-test:2,5–12,25–26,40–44`; `tools/melonds-upgrade-test:5–7,23–45,94–95,110–118`; quoted T15 call sites `tools/last-good-scripts-test:381–400,426,14224,14231`.

Neither writer test performs its **own** automatic fallback: `--busybox` is required. Both copy and execute the supplied file. However, neither verifies that it belongs to the candidate image, matches an expected image digest, or even distinguishes a host-app\-let result in its verdict. Recording the supplied file’s hash is not that verification.

The supplied T15 account says `image_tool_source` falls back to `command -v`, and passes the result to both tools. The full T15 source is absent, so that wiring is verified only to the extent of the quoted call-site evidence.

**Concrete failure scenario:** no build root is found; T15 supplies `/usr/bin/busybox`. Both tools print the same PASS verdict and produce the same report shape as an image-app\-let run. Stage A demonstrates that the host BusyBox passes. Printing its source path upstream is useful provenance, but does not qualify the verdict as host-only.

There are two further ways to run host applets despite supplying the image binary:

1. **Incomplete shimming in settings-modes.** Its list at `:9` omits such commands as `grep`, `sort`, `cat`, `rm` and `mktemp`; `PATH` falls through to host directories at `:26,40`. A writer that gains a GNU-only option on an unshimmed command can pass here and fail on the image. The exact current production command inventory is outside this packet, but the fallback surface is explicit.
2. **Inherited Bash functions/environment.** Both tools construct the child environment from `os.environ`. An exported `cp`, `awk`, `mv`, etc. function can outrank the installed PATH wrapper. Neither test records actual applet invocations.

The melonDS shim list may cover its current function’s external commands, as the first reader reports, but it does not enforce that coverage as the function evolves.

These remain function-level host controls. In particular, extracting and directly invoking `update_melonds_hotkeys` does not prove that the real post-update entrypoint still calls it.

## Disposition of F-01 through F-15

### G-5 — Medium — F-01 confirmed, with the integration attribution qualified

**Files:** `tools/build-identity-test:131–145,168–179`; `tools/pixelelated-state-check:767–770,897–905`.

The firmware stand-in is plain text with an `.img.gz` name. A payload inspection of it necessarily fails gzip decoding and becomes exit 2. The identity test nonetheless requires its public preparation to succeed at `:145`.

**Scenario/result:** use the supplied stand-in with a preparer that invokes the state gate; a correct rejection becomes a failed identity test.

The actual preparer body and introducing commit are not supplied, so that integration/history attribution is **inference from the first reader’s account**, supported by the recorded failure. Also, “two failed” is not two independent defects: one failed check raises, then `:169` adds “harness completed” as another failure.

---

### G-6 — Medium — F-02 confirmed as a hardcoded-license defect; the history is not independently established here

**File:** `tools/rasteratops-identity-check:137–143`.

The tool checks the recipe against the literal `"MIT"`; it does not derive or verify the license against the supplied ES source.

**Scenario/result:** a correct recipe uses `MIT AND BSD-3-Clause`; the test reports “ES licence matches its source” as FAIL solely because the literal changed.

The stated recipe value and commit attribution are not included as source in this packet, so those are **inference from the supplied audit account**. The brittle assertion itself is directly verified.

---

### G-7 — Medium — F-03 confirmed

**Files:** `tools/pixelelated-cloud-validator-test:57–58`; `tools/pixelelated-duckstation-capture-test:177–178`; `tools/pixelelated-cloud-folder-test:10–11`.

Both executable tests require exactly `rclone v1.75.1`. The stage-A refusal explicitly shows a supplied `v1.75.2` binary being rejected.

**Scenario/result:** supply the recorded image rclone; neither test reaches a product case. The retired stub also directs users to the stale version.

The package-history attribution is not independently available, but the incompatibility with the supplied image binary is verified.

---

### G-8 — High — F-04 understated

**Files:** `tools/rasteratops-cloud-layout-test:138–148`; `tools/pixelelated-cloud-validator-test:326–336`; `tools/pixelelated-save-layout-test:94`; `tools/pixelelated-duckstation-capture-test:123,149–154`.

G-1 gives the substantive correction. `TMPDIR` is one symptom of a broad inherited-environment boundary. The ordinary runner and validator’s adoption sandbox also retain the host network.

**Scenario/result:** environment-selected real configuration changes the endpoint or execution behavior rather than merely breaking temporary-file creation.

Do not generalize the network exposure to save-layout or DuckStation: their network isolation is explicit.

---

### G-9 — Medium — F-05 confirmed; one cited line is wrong

**File:** `tools/pixelelated-content-scope-test:129–135,218–226`, with exception-to-FAIL handling at `:61–63`.

The traversal case reads `ctl/argv` at **`:132`**, not `:121`. Line 121 belongs to the provider-failure helper.

**Scenario/result:** the product correctly rejects traversal before invoking rclone. No argv file exists; `read_text()` raises and the test records FAIL. The pointer-traversal case has the same defect at `:222`.

The production change’s commit attribution is outside the supplied source, but this failure on a legitimate early refusal is directly established.

---

### G-10 — Medium — F-06 confirmed, and more consequential than Low

**File:** `tools/pixelelated-cloud-validator-test:63–66,355–359`.

After satisfying the version gate, `--case no-such-case` skips every case, writes `"result": "PASS"` with an empty list, prints `PASS 0 controls`, and exits successfully.

**Wrong result:** a requested check that never ran is represented as a successful test invocation.

It also silently accepts a mixture of valid and invalid requested names. There is neither a nonempty result assertion nor an exact requested-versus-executed selection check.

---

### G-11 — Medium — F-07 confirmed and understated

**Files:** `tools/rocknix-info-test:28–29,55–60`; `tools/nova-led-test:48–50,51–68`.

The optimizer removes the verdict assertion in rocknix-info, but not the unconditional PASS print. An explicit `python3 -O` is not the only trigger: the shebang invocation can also inherit `PYTHONOPTIMIZE`.

**Scenario/result:** a quirk failure incorrectly becomes exit 0. Under optimization, rocknix-info records a false condition, prints PASS and exits 0.

For Nova, a script can perform the expected writes and then return an error. Under optimization that return-code failure disappears while the value checks still pass.

The claim that CI always avoids this environment is not independently verifiable from the supplied files.

---

### G-12 — Low — F-08 confirmed, with two qualifications

**File:** `tools/retroarch-wrapper-test:42–57,61–67,213–226`.

- Temporary source and executable are not cleaned up.
- Missing `gcc` raises before the explicit compiler-status handling, giving an ordinary Python failure rather than documented exit 2.
- The bare defaults depend on the named old build-root locations.

**Scenario/result:** no compiler is installed; the tool exits in the status class documented for a product failure, although no fixture ran.

However, actual compiler **nonzero returns** are correctly mapped to exit 2 at `:218–219`, and `RETROARCH_SRC` is supported at `:45–50`. The absence of the default roots is a closed refusal, not a false PASS.

---

### G-13 — High — F-09 understated

**File:** `tools/pixelelated-vm-cloud-boundaries:270–277,674–694,712–716`.

The finding is not limited to failing to see hidden PIDs. Cleanup can signal an unrelated QEMU by substring, even following a start-time refusal before any owned guest was launched.

**Scenario/result:** the unrelated-QEMU `-name` scenario in G-2 causes an unowned process to receive `SIGTERM`.

Empty discovery also produces a successful cleanup receipt without proving that the expected pair exited. The hidden-namespace mechanism remains an **inference**; the selection and vacuous-success defects do not.

---

### G-14 — Low — F-10 overstated

**Files:** `tools/pixelelated-vm-cloud-boundaries:699–710`; `tools/rasteratops-vm-cloud-epic:20–25`; both retired folder stubs’ `:4–18,23–26`.

The current-source refusals are confirmed. “Cannot run at all today” is too broad:

- Boundaries explicitly accepts a historical source tree and firmware.
- Epic explicitly directs historical execution to a historical checkout.
- The stubs deliberately refuse execution and clearly say so.

**Counter-scenario:** run these against current retired migration source; they return a refusal, not a misleading PASS. That is the correct fail-closed behavior.

Possible misleading index rows are a documentation issue, not demonstrated by the supplied index source. They should not be conflated with defective refusal guards.

---

### G-15 — Medium — F-11 overstated as verified, and understated numerically

**Evidence:** first reader `04`, F-11 and Q6; concrete drift example at `tools/pixelelated-cloud-validator-test:58`.

The repository-wide caller search is not supplied, so I cannot independently confirm absence of callers. That conclusion remains **inference from the first reader’s inventory**.

The inventory is internally inconsistent:

- Its thirteen-name list omits cloud-validator, which its own Q6 table also calls uninvoked.
- On that inventory’s invocation rule, the count is **fourteen**, not thirteen.
- The F-11 list of failing/refusing non-stub tools names **seven**, not six, when the two pin tests and two guest tests are counted separately.

**Scenario/result, conditional on that inventory:** the validator’s hardcoded version drifts, but the normal automated qualification never executes it, so the failure remains unseen. That is a legitimate coverage risk; the claimed exact counts are not sound.

---

### G-16 — Low — F-12 not independently confirmed; overstated as a correctness finding

**Files:** `tools/pixelelated-cloud-folder-test:4–17`; `tools/pixelelated-cloud-folder-vm-test:4–18`; first reader `04`, Q7.

The index rows and complete *Detail in* documents are not supplied. Their alleged omissions are therefore **inference**, not independently verified findings.

The supplied entrypoint descriptions do explicitly say retired, explain the former scope, and direct users elsewhere. Those lines refute any suggestion that the **tools themselves** present their refusal as current qualification.

**Possible failure scenario:** an index link takes a user to general policy rather than command-specific instructions. That is a Low discoverability problem if verified, not evidence that a test passes incorrectly. A rule can also apply to a tool without literally naming it.

---

### G-17 — Medium — F-13 confirmed for writer provenance; overstated for save-layout’s default scope

**Files:** `tools/settings-modes-test:5–10,26,43`; `tools/melonds-upgrade-test:24,40–45,95,118`; `tools/pixelelated-save-layout-test:2–6,47–48,393–402`.

G-4 confirms the writer/T15 issue and the incomplete settings shim boundary.

**Scenario/result:** T15 supplies host BusyBox and receives an unqualified writer PASS.

For save-layout, however, image applets are explicitly optional and the header expressly disclaims installed-firmware qualification. Running it without `--busybox` is a host-source control, not inherently a false claim of image execution. Supplying the wrong BusyBox while labeling it “Image find/awk applets” remains a provenance weakness.

---

### G-18 — Low — F-14 factually confirmed, but overstated as an unsafe product execution

**File:** `tools/pixelelated-duckstation-capture-test:324–342`.

The execution at `:334` is outside bwrap. But the file’s bytes are first required to equal the fixed, tiny synthetic shell payload at `:325,332`, and the receipt expressly says it is not the AppImage runtime (`:340`).

Those lines refute an interpretation that an arbitrary installed emulator/AppImage is being executed on the host.

**Concrete brittleness:** an otherwise correct 0755 installation on a host temporary filesystem mounted `noexec` fails the direct-execution check. That proves a host execution restriction, not a packaging-mode defect. The issue is a host dependency and boundary-description detail, not demonstrated execution of unverified product code.

---

### G-19 — Low — F-15 refuted on both allegations

**Files:** `tools/rasteratops-identity-check:103–111`; `tools/usb-gadget-test:4–9,59–71,118,133–136`.

`check(True, "Tools metadata is well-formed XML")` is reached only after `ET.parse()` succeeds. Malformed XML takes the exception branch and calls `check(False, ...)` at `:111`.

**Counterexample to F-15:** malformed gamelist XML produces FAIL. The complete check can fail; inspecting only the literal `True` loses its control flow.

The USB header explicitly says the tool runs on the **host or guest**, models configfs directories, and does not prove kernel semantics or USB enumeration. It extracts the actual functions and records the selected/resolved shell.

**Counterexample to F-15:** a host `/bin/sh` run is reported as a host-capable filesystem fixture with its shell identity, exactly as described. There is no promise here that the interpreter is the image’s shell.

There is a separate vacuous **semantic XML** check, described in G-36.

## Additional findings

### G-20 — High — The OAuth fixture’s “fake provider” guard can admit real rclone and discard the scratch configuration argument

**File:** `tools/test-fixtures/cloud_connections_fixture.py:15–35`.

The guard rejects only one exact combination:

```text
module.subprocess is subprocess
module.RCLONE == '/usr/bin/rclone'
```

An equivalent real binary at `/bin/rclone`, `/usr/local/bin/rclone`, a copied path, or a real-subprocess proxy object bypasses it.

More importantly, `run()` takes the stage from `args[1]`, then invokes the provider using only `args[2:]` (`:23–27`). The configuration-selection arguments are not forwarded.

**Concrete failure scenario:** a host caller supplies real subprocess and a real rclone under a different pathname, then requests `config create` with a scratch `--config` argument. The fixture executes real `config create` without that argument. It can modify the caller’s default rclone configuration, then separately fabricate the expected section in the scratch stage and return success.

Whether a current T15 invocation can supply that combination is **inference**, because its full setup is absent. The adapter itself does not enforce its fake-provider boundary.

---

### G-21 — High — Epic can continue after failing to install the QA cloud configuration

**File:** `tools/rasteratops-vm-cloud-epic:9,127–138`.

There is no `set -e`. At `:129`, failure of configuration generation or `scp` is followed by an unconditional `rm`, without checking the setup result.

At `:130`, failure of the `mkdir && mv && helper` chain does not prevent the following `if ...` block from selecting/listing an existing remote and ending successfully.

**Concrete failure scenario:** the borrowed guest already has a real cloud configuration; copying the synthetic configuration fails. The tool continues, resets only the host-side QA backend, rewrites the guest’s cloud pointers, and starts the UI proof with the old guest configuration still active.

The resulting real-provider operation is an **inference about the installed scripts/network**, but continuing with an unverified existing configuration is explicit. A later test failure would not undo any preceding real-cloud operation.

The current-tree retirement guard prevents this in the recorded ordinary run; the historical execution path remains unsafe.

---

### G-22 — Medium — A lost SSH request can pass the guest atomic-publication failure control

**File:** `tools/pixelelated-vm-cloud-boundaries:68–85,339–363`.

`audit_atomic()` permits any return code from the interrupted migration (`:352`). Its intended fault witness is:

```text
test -s <pointer-fired>; rm -f <shim>
```

at `:353`. A failed `test` is overwritten by successful `rm`.

**Concrete failure scenario:**

1. The injected shim is installed.
2. SSH fails transiently before the migration command runs.
3. No pointer fault fires and no configuration changes.
4. The next SSH command’s `test -s` fails, but `rm` succeeds.
5. The nonzero migration status and unchanged snapshot satisfy `:354–355`.
6. The retry succeeds.

The case reports PASS without exercising failed pointer publication. Similar overwritten witnesses occur at `:262` and `:391`.

---

### G-23 — Medium — Partial selectors silently omit requested controls; Epic also has an empty-selector success

**Files:** `tools/pixelelated-content-scope-test:40–42,249–252`; `tools/pixelelated-duckstation-capture-test:181–183,348–357`; `tools/rasteratops-vm-cloud-epic:11–15,34–42,120,400–402`.

**Concrete scenarios:**

- Content-scope with `--cases selected-rom-bios-bytes,typo` runs the valid case, silently drops `typo`, and can exit 0.
- DuckStation does the same with a valid case plus an unknown name, once its version gate is satisfied.
- On Epic’s historical path, `--case ""` executes zero loop iterations and exits with `total_rc=0` before checking guest prerequisites.
- An inherited nonempty `PROOF_CASE` bypasses the validated outer dispatch. An unknown value can reach the end with zero case assertions and zero failures after performing common setup.

Save-layout’s exact-set and nonempty checks at `:384–386` are the relevant counterexample: it does not have this selector defect.

---

### G-24 — Medium — Validator can pass its full-category cases with no category results

**File:** `tools/pixelelated-cloud-validator-test:31–42,68–89,119–130,271–278`.

`request()` checks exit status, JSON decoding, unchanged files and run ID. It does not require the requested category set or count.

Several callers then use `all(...)` over an unchecked list or dictionary:

- populated categories at `:75`;
- content exclusions at `:87,89`;
- missing categories at `:122`;
- empty categories at `:129`.

**Concrete failure scenario:** the product regresses only for the default five-category request, performs local remote discovery, then returns:

```text
complete = true
categories = []
run_id = requested run ID
```

The argv file exists from local discovery. The populated, missing and empty full-category controls all pass; namespace validation also accepts `complete=true` without checking its rows.

The remaining smaller-category behavior can remain correct, allowing the suite to pass while five-category validation does nothing. This is a stronger false-PASS hole than merely omitting a printed count assertion.

---

### G-25 — Medium — First-boot readiness accepts an argument mentioning autostart as proof that autostart executed

**File:** `tools/pixelelated-state-check:805–845,847–861`; `tools/pixelelated-state-check-test:514–518,741–749`.

The readiness check validates unit execution metadata, but its executable check is only a substring search for `/usr/bin/autostart` in the serialized `ExecStart` property (`:839`).

**Concrete failure scenario:** the named oneshot executes `/bin/true /usr/bin/autostart`. It completes successfully, and its `ExecStart` text contains the required substring. If the other required artifacts/mounts and one ES process exist, the gate can report boot-ready even though this unit never executed autostart.

That is a source-derived counterexample to the claimed execution check; it is not a claim about the current installed unit.

The supplied self-test checks refusal of `--require-ready` on a non-root fixture, but does not exercise this valid-root execution-identity distinction.

---

### G-26 — Medium — The ROM-category seeding positive can pass after a no-op

**File:** `tools/pixelelated-cloud-validator-test:258–269,309–317`.

The settings seeding half requires a README to exist. The subsequent ROM seeding half checks only exit 0 and that BIOS was not created (`:267–268`).

**Concrete failure scenario:** `--seed-folders roms` returns 0 without creating anything. The case still passes its ROM assertion.

The explicit-root case likewise does not assert the seeded ROM/BIOS artifacts or their resulting states; `request()` alone is not such an assertion. A positive artifact/count assertion is needed to distinguish “created the requested category” from “did nothing.”

---

### G-27 — Medium — The validator’s oversized-output and timeout controls do not discriminate the advertised bounds

**File:** `tools/pixelelated-cloud-validator-test:175–178,350–353`; underlying runner timeout at `tools/rasteratops-cloud-layout-test:147`.

The byte-limit injection emits 2.2 MB of `x`, which is not JSON.

**Concrete failure scenario:** remove the product’s output-size limit but retain JSON parsing. The oversized response is still rejected as malformed, and the byte-limit case reports PASS. It has not shown that the byte limit exists.

The timeout case checks only an eventual unreadable result. It measures no elapsed time.

**Concrete failure scenario:** a broken request takes substantially longer than its promised bound, then returns the expected unreadable JSON before the fixture’s 120-second timeout. The timeout case passes.

These controls need independently valid over-limit input and an observed deadline, respectively.

---

### G-28 — Medium — The local legacy backup test can use its input archive as proof that a new backup was written

**File:** `tools/rasteratops-cloud-layout-test:1025–1042`.

For the legacy variant, `:1029` creates a `*-ROCKNIX_SETTINGS.tar.gz` file. The test verifies that it survives unchanged at `:1038`. After calling `backuptool backup`, it checks only that **some** file with that suffix exists.

**Concrete failure scenario:** restore works, but the subsequent backup command returns 0 without creating a new archive. The original legacy input still satisfies `any(...)` at `:1042`, so `T24-local-legacy-recovery` passes.

The renamed-input companion can catch some versions of this regression; that does not make this individual selected case a valid writer witness.

---

### G-29 — Medium — Several failure controls do not prove the intended failure was reached or propagated

**Files:** `tools/rasteratops-cloud-layout-test:295–301,346–356`; `tools/pixelelated-content-scope-test:105–123`.

Three concrete holes:

- `settle_failure()` checks unchanged cloud/pointers but neither a nonzero caller result nor a settlement-invocation witness. A seeder that exits 0 immediately passes.
- `provider_failure()` requires the provider fault to fire but **never requires the script’s return code to indicate failure**. A script can swallow the provider error, return 0, preserve the existing sentinel and avoid the create-folder offer; the case passes.
- Content-scope’s failed-listing cases install a fault, but do not check that it fired. A different failure after local `listremotes` creates the argv file and can satisfy the nonzero/no-transfer assertions.

These are distinct from legitimate negative controls that prove both fault activation and the expected refusal.

---

### G-30 — Medium — Missing-library controls can pass without inspecting the selected library

**File:** `tools/pixelelated-content-scope-test:65–84`.

The scan’s row assertion is vacuous for no rows, and the scope assertion examines only calls beginning `lsf`, `copy` or `sync`.

**Concrete failure scenario:** the script runs only local `rclone listremotes`, then exits 0 with no output. The argv file exists, the filtered provider-call loop has no members, and the missing list/scan/all controls can pass without reading the selected library.

There is a useful correction to the first reader’s Q3: a literal `exit 0` with **no rclone call at all** would normally fail at `:77` because the argv file is absent. The passing counterexample is local discovery followed by a no-op, not an entirely command-free script.

---

### G-31 — Medium — Historical migration cases do not always establish the state or value they claim to exercise

**Files:** `tools/rasteratops-cloud-layout-test:889–907,627–677`; `tools/pixelelated-vm-cloud-boundaries:590–610`.

Two independently weak oracles:

1. **Reader grammar:** accepted forms are checked for successful return and unchanged state, but not for the decoded `SETTINGS_REMOTE` value.  
   **Scenario:** the reader ignores a valid custom value and uses its default; these successful-form cases can pass. The guest reader test has a stronger value-selection oracle at `boundaries:495–503`, but that does not repair the host case.

2. **Completed predecessor fixture:** `predecessor_retry()` records the old script’s return code without asserting success or its completed state (`:647–654`). The guest equivalent similarly does not require success for `stage == complete`.  
   **Scenario:** the predecessor fails before completing; the candidate successfully performs a fresh migration. The “completed predecessor” case passes without having created that predecessor state.

These are historical-path findings; the ordinary current-source migration refusal remains intact.

---

### G-32 — Medium — State-check controls can credit an unrelated reader exception; the recorded control count is not enforced

**Files:** `tools/pixelelated-state-check-test:125–137,142–154,395–401,721–737,769–775`; gate catch-all at `tools/pixelelated-state-check:897–903`.

For most expected-2 controls, any value-free error report with exit 2 satisfies `invoke()`. No policy path or intended error location is required.

**Concrete failure scenario:** a malformed-input branch develops a `NameError` rather than exercising its intended parser guard. The gate correctly fails closed through its catch-all. The corresponding test still reports that specific malformed-input control as passed.

This is **not** a clean-input acceptance or a disclosure defect in the gate. It is an inability of the test to distinguish “the intended guard fired” from “the reader crashed safely.”

Separately, `control_count` is computed and printed, never checked. Removing a control registration lowers the count while preserving `"status": "pass"`. Dynamic shipped-profile enumeration has only a two-name minimum. The recorded 183 controls are evidence of that run, not an enforced coverage contract; an expected mandatory-name set would be stronger than merely freezing a magic total.

---

### G-33 — Medium — Epic can report successful evidence collection with zero captures, and absence checks can pass on SSH errors

**File:** `tools/rasteratops-vm-cloud-epic:65–70,123–126,304,334–340,400–402`.

`grab_stop()` overwrites a failed `wait "$GRABPID"` with the successful `GRABPID=""` assignment. Frame counts are printed, not asserted.

**Concrete failure scenario:** the capture child exits immediately because VNC is unavailable or its script cannot start. Other guest assertions succeed. The case can report PASS despite having no continuous/boot capture evidence.

Also:

- `! esl ... | grep -q .` treats a failed SSH/log read as absence.
- `! G_ 'test -e ...'` treats SSH exit 255 as successful proof that a marker disappeared.

For `:304`, the first positive log probe must succeed, but a failure of the **second** probe still makes the absence half pass. At `:334` and `:340`, the negative probe itself has no such same-operation success witness.

These defects remain relevant to supported historical execution despite current-source retirement.

---

### G-34 — Medium — The wrapper test counts total calls, not exactly one call for every posted command

**File:** `tools/retroarch-wrapper-test:57,111–124,159–181,191–205`.

The only execution counter is global `g_calls`; commands carry no unique test sequence. Equality of aggregate calls and posts does not prove a one-to-one mapping.

**Concrete failure scenario:** one posted command is executed twice and another is acknowledged without executing. The total remains 2000, so the harness prints “every command ran exactly once.”

There is also no deterministic scheduling gate: `--gated` is assigned at `:57` and never used. The frame injection relies on a thread and `usleep(200)`, so a scheduling run that misses the bad window can pass. That consequence is **inference about scheduling**, whereas the unused option and aggregate-only oracle are explicit.

The hardcoded packet handler at `:127–140` is also a model, not an extraction of the product’s handler; the result must remain scoped to the extracted wrapper logic.

---

### G-35 — Medium — The lock test loses the function’s return status and never races two fresh acquirers

**File:** `tools/wait-lock-test:59–64,95–113,117–129,147–156`.

The generated script calls `wait_lock`, then runs other commands without preserving or checking its status.

**Concrete failure scenario:** a function acquires and logs correctly but returns nonzero. `HELD` and the final `rm` succeed, so the harness records rc 0 and can pass every control despite the function’s wrong API result.

The concurrency coverage is also narrower than “mutual exclusion proven”: each live-holder case creates one holder first, then one taker.

**Concrete failure scenario:** acquisition uses a non-atomic “if absent, write my PID” sequence. It handles the already-present holder correctly and passes these cases, but two simultaneous callers can both enter when starting from an absent lock. No supplied case exercises that acquisition race.

---

### G-36 — Medium — The identity check has real vacuous/content-selection checks, but not the `check(True)` defect alleged in F-15

**File:** `tools/rasteratops-identity-check:39–41,103–109,131–143`.

An empty, well-formed XML document passes the metadata parse and produces an empty `stale` list. The code does not require `gameList`, any game entries, or required names/descriptions.

**Concrete failure scenario:** replace the tools gamelist with `<gameList/>` or another empty well-formed root. It reports both well-formed metadata and current tool identity while no tool metadata was inspected.

Separately, `value()` returns the first matching assignment.

**Concrete failure scenario:** an options file contains `DISTRONAME="pixelelated"` followed by an overriding assignment. The check passes the first value while an ordinary shell consuming the file uses the later value. Similar source-literal checks can be satisfied by inactive/commented C++ text; they are not behavioral proofs.

---

### G-37 — Medium — Literal path rewriting is not a filesystem containment boundary

**Files:** `tools/nova-led-test:35–41,48–49`; `tools/rocknix-info-test:21–26`.

These tools execute on the host after uncounted `.replace()` adaptations. They do not assert that every expected replacement occurred or sandbox remaining filesystem accesses.

**Concrete failure scenario:** the Nova source changes the spelling or quoting of its `LED_PATH` assignment, so the exact replacement at `:38` no longer matches. The script can overwrite the supplied environment path and address real `/sys` instead of the fixture.

Whether that causes writes on a particular host depends on hardware and permission—**inference**—but an unadapted host-path execution is no longer excluded. The same class of source drift can make rocknix-info read real host data and produce a false failure or an accidental witness unrelated to the synthetic fixture.

---

### G-38 — Medium — Candidate verification resolves away the supplied digest-name boundary

**File:** `tools/rasteratops-candidate-store:28–43,56–57`.

The CLI resolves the bundle path before comparing its basename with the manifest digest.

**Concrete failure scenario:** the caller supplies `store/sha256/A`, but that path is a symlink to a different, self-consistent bundle `B`. `verify()` checks and prints PASS for resolved bundle B, not for the identity named by the original argument A.

The acceptance is directly visible. A release-preparer bypass is **not established** because that caller’s binding logic is absent. The consequence is conditional: any caller treating “verify A returned 0” as proof that the frozen identity A survived can be misled.

This is more specific than the already-known fact that a newly manifested, newly named bundle is self-consistent.

---

### G-39 — Low — Settings-modes breaks when its temporary root contains spaces, and can label the resulting execution failures as successful refusals

**File:** `tools/settings-modes-test:7–10,26,40–42`.

The BusyBox pathname is concatenated unquoted into each shell wrapper.

**Concrete failure scenario:** `TMPDIR` names a valid directory containing spaces. The wrapper attempts to execute only the first pathname word and returns 127.

The ordinary cases fail, so this is not an overall false PASS. But refusal rows accept any nonzero code and unchanged files, so those rows can still print PASS for a fixture execution failure rather than a rejected staging action.

MelonDS correctly quotes the copied BusyBox path at `:45`; that line refutes extending this particular pathname bug to it.

---

### G-40 — Medium — Save-layout requires applet invocations even for selected cases that do not use those applets

**File:** `tools/pixelelated-save-layout-test:119–144,168–177,393–398`.

The final BusyBox assertion requires nonzero invocation counts for **both** find and awk whenever `--busybox` is supplied.

**Concrete failure scenario:** select only `filter-psp` with an image BusyBox. The shown control executes rclone version and rclone filter probes; neither control calls the find/awk wrappers. The filter property can pass, then the global invocation assertion fails the run.

Thus the optional image-app\-let proof imposes an unrelated dependency on a pure-rclone selected control. The assertion should be tied to the selected cases’ required applets, not applied universally.

---

### G-41 — Medium — Some receipts bind later/current source files, not necessarily the bytes executed

**Files:** `tools/settings-modes-test:6–8,43`; `tools/melonds-upgrade-test:27,40,117–118`; `tools/pixelelated-cloud-validator-test:64,355–356`; `tools/pixelelated-save-layout-test:389–392`; historical source enumeration at `tools/rasteratops-cloud-layout-test:46–65`.

**Concrete custody scenario:** a source or supplied BusyBox file changes after the writer test reads/copies it but before report generation. The test executes the old bytes, then records the hash of the new input path. It can issue a passing receipt apparently bound to bytes it never executed. Concurrent modification in the recorded run is **not alleged**.

There is also a historical-source reporting mismatch in save-layout: its summary enumerates **today’s** source-directory files, then performs `git show <ref>:<each-current-name>`.

**Concrete failure scenario:** the historical ref lacks a newly added, unused helper that exists today. Its selected historical control can run correctly, but receipt generation fails on the nonexistent historical filename. The fixture’s own historical enumeration correctly uses `ls-tree`; the receipt does not.

Copying current source into a fixture is not automatically circular—the semantic oracles can still be independent. The verified flaw here is loss of custody or use of the wrong file inventory when describing what was tested.

---

### G-42 — Low — The lint pass/fail fixture pair couples two violations, so it may not prove either guard independently

**Files:**  
`tools/test-fixtures/lint-audit-artifacts/fixture-epic-m6-renovation-fail/04-analysis.md:1–16`;  
`.../fixture-epic-m6-renovation-fail/05-punch-list.md:13–18`;  
`.../fixture-epic-m6-renovation-pass/04-analysis.md:18–33`;  
`.../fixture-epic-m6-renovation-pass/05-punch-list.md:13–19`.

The fail fixture simultaneously lacks:

1. the renovation-face sections; and
2. the punch item’s `question` field.

**Concrete failure scenario:** a runner checks only that the pass directory succeeds and the fail directory fails. Remove either one of the linter’s two guards; the remaining violation still rejects the fail fixture, so both expected outcomes remain satisfied.

This conclusion is **conditional inference**: the linter and fixture runner are not supplied, and they may assert individual diagnostic identities. From these fixture files alone, there is no independently isolated negative for either requirement.
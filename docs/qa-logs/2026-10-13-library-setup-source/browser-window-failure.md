# #570 browser-window failure extension — SOURCE ONLY / UNRUN

Final source: `6b1dd68246c89f4c1c0fa17c3d8941ffd3b3d420`, parent
`44b0522ae39a664209af35f8503b933bee09a1db`; only `GuiMenu.cpp` changes in this
second commit. No allocator or `ApiSystem.cpp` change is duplicated.

The coordinator reports a real browser-start failure in its f7b71 candidate:
`/usr/bin/cloud-signin-window` failed, `ApiSystem::launchCloudSignIn` returned
false, but native sign-in still showed SIGNING IN / provider page opening.
Reported evidence is under
`/workspace/tmp/pix570-es-flows-20261013/en640-open-failure03/`:
`browser-open-failure.png` and `result.json`. Its overall fixture1 remains a
failure because of a later Continue-focus assumption. This worker did not
replay that owner or claim its results for the new code.

## Behavior and copy

Both native immediate launch and phone CONTINUE now call
`cloudOAuthOpenSignIn`. Successful native launch still returns to its existing
CONTINUE page; successful phone launch still checks the broker immediately.
A false result stops the phone path before the generic still-waiting dialog.
Both routes show one error dialog with TRY AGAIN and CANCEL SIGN-IN:

> THE SIGN-IN WINDOW DID NOT OPEN OR STOPPED WORKING.
>
> TRY AGAIN, OR CANCEL SIGN-IN.

The wording covers the existing boolean API: false can mean open failed or
the wait command failed. It does not invent a provider, credential, network
or memory cause. The exact single new msgid and French translation are in
`copy.fr.po`, preserving the two `\n` separators. Existing French buttons are
`RÉESSAYER` and `ANNULER LA CONNEXION`; the existing catalog entries are reused.
No translation catalog was edited in this worker's scope.

The broker remains the authority:

| State at failure / retry | Action |
| --- | --- |
| Failure return, but broker already says `signed-in` | Go to the existing connected flow; do not claim failure or start another attempt |
| Error visible; TRY AGAIN, broker still `waiting` | Reopen with the same native/phone keyboard flag and the same authorization attempt; no cancel/serve or new phone pairing |
| Error visible; TRY AGAIN, broker now `signed-in` | Go to the existing connected flow without another browser launch |
| Error visible; TRY AGAIN, failed/ended/unrecognized/absent broker state | Deliberately use existing `cloudOAuthStart`: cancel stale state, start a fresh attempt, then choose input with its new readiness/URL |
| CANCEL SIGN-IN or Back | Delete the dialog, close the current sign-in page, and let its existing session finalizer cancel once |
| Repeated window failure | Replace the dismissed error with one new error dialog, not an accumulating stack |

No OK button drops the player onto the failed page's stale opening instructions.
The error remains visible until retry/cancel. There is no automatic retry or
silent authorization restart. The existing launch wait can still take its
20-second startup bound before reporting failure; this patch does not shorten
the broker's timeout or establish a latency/memory repair.

## Lifetime reasoning and source boundary

Read `.claude/rules/es-native-ui.md` wizard replacement rule,
`es-code-traps.md` button-bar lifetime rule, `tests/cloud-oauth-lifetime.py`,
`tests/cloud-oauth-await.py`, `GuiSettings::close`,
`GuiMsgBox::deleteMeAndCall`, `ButtonComponent::input`, and the broker's
`open`/`wait`/`open_when_asked` source before choosing callbacks.
The broker source read in this checkout matches coordinator `0ea6eaf74a`
exactly: Git blob `a611ebf2aaddc944949e55aa15f03321609589e0`.

- `cloudSetupPresent` pushes the successor, removes the predecessor from
  `sOAuthSessionPages`, then closes/deletes the predecessor. The successor's
  callbacks refer to that successor. For native launch, `cloudOAuthShowSignIn`
  now receives backend/name **by value**: after page presentation, references
  into the deleted chooser callback would be invalid.
- The error dialog keeps the live sign-in page beneath it. It does not replace
  that page, rebuild its buttons, or acquire a second session owner. Its
  retry/cancel callbacks capture values and the current page, never `prev`.
- `GuiMsgBox::deleteMeAndCall` copies the chosen callback and deletes the
  dialog before invoking it. Retry may therefore show a replacement error or
  transition to another page; cancel may close the underlying owner safely.
  Back selects the last button because neither button is OK/NO: cancel.
- The phone completion lambda is separated from window launch and copied into
  the launch helper by value. Direct CONTINUE also copies it before invocation.
  It can therefore replace/delete its own page without losing the executing
  closure. There is no recursive shared-function cycle or queued callback.
- Runtime status is re-read on retry; a captured earlier `waiting` state cannot
  overwrite a completed sign-in or reuse an expired readiness/URL. The page
  owns cleanup until a normal transition hands ownership on.

The original `ApiSystem::launchCloudSignIn` remains unchanged: open result,
frontend suspend, wait, frontend restore, close, boolean result. The independent
f7b71 allocator commit belongs at that same existing suspend/wait boundary when
the coordinator composes the candidate.

## Prepared failure controls (all UNRUN)

`fixtures/cloud-window-lifetime.py` extracts the **actual** source's
`cloudOAuthOwnSession`, `cloudSetupPresent`, `cloudSetupSetButtons`,
`cloudOAuthOpenSignIn` and full `cloudOAuthShowSignIn`. It uses real C++ deletion
with ASan and doubles for rendering, API launch, broker commands and destination
pages. The two production callers must use the new helper or it refuses.
Source SHA256 must match `static-review.json` before compilation.

Eighteen prepared cases: native/phone × cancel, Back, repeated failure,
retry-success, ended attempt, missing state, completed while prompted,
completed despite false launch result, and successful initial launch. They
check one dialog, keyboard flag preservation, no cancel/restart while waiting,
one cancellation from the new error, no redundant open after completion, a new
attempt only for ended/unknown state, session ownership, actual page deletion,
and empty owner/GUI sets at teardown. Heap-backed chooser captures expose
borrowing predecessor-owned strings after deletion. Callback invocation does
not make a protective copy in the fixture's page-button dispatcher: the shipped
code must own the completion invocation itself.

The older `tests/cloud-oauth-lifetime.py` does **not** extract the actual sign-in
page: it replaces it with a small stand-in and covers choice/ownership only.
Static reading also shows its `Menu` double lacks `setPosition`, now used by
`cloudSetupPresent`; coordinator should repair that double before treating the
old command as an executable gate. No failed compiler result is claimed here.
The new prepared fixture supplies that method and covers the new callers.

After a fresh coordinator allocation, the exact pending command is:

```sh
python3 "$PACKET/fixtures/cloud-window-lifetime.py" \
  --source /home/max/Development/emulationstation-next.worktrees/m7-library-setup-567/es-app/src/guis/GuiMenu.cpp \
  --compiler /usr/bin/g++ --out "$FRESH_OWNER/oauth-window-lifetime"
```

This command compiles/runs and **was not executed by this worker**. The output
directory must not exist. Capture original compile stdout/stderr/exit, every
case's stdout/stderr/exit, and `result.json`; a refusal/timeout is not PASS.
No account, network, service, real browser or compiled image is covered by
these doubles. The image-toolchain syntax check and installed VM proof remain
separate gates.

## Coordinator's real VM branch/frame proof

Can this be done on the VM? **Yes.** Extend the already owned synthetic broker
and injected `/usr/bin/cloud-signin-window` startup failure to the newly built
composition, with fresh result owners. Preserve the original f7b71 failure.
Use the same exact binary/boot/PID binding and no public provider forwarding.
For native and phone routes, at EN/FR and 640×480/1280×800:

1. Force startup failure once. Verify absent browser plus retained failure
   marker/log, unchanged frontend PID/start/boot, and the new error frame.
   On phone CONTINUE there must be no second still-waiting dialog on top.
2. Leave the failure in place, retry twice. Verify one dialog each time,
   matching phone/native launch flags and no new broker attempt/pairing.
3. Cancel, and separately press Back. Verify return to the cloud hub, broker
   listener/browser cleanup, and no stale error or blocked frontend.
4. Remove only the owned failure injection; retry on the same waiting attempt.
   Verify native/phone input policy, actual browser appearance, same attempt
   identity (equality only; do not publish URLs/PINs), normal frontend return,
   and the respective completion flow. Use actual native/phone input fixtures
   for those interfaces; a host callback harness does not cover input.
5. Complete the local synthetic authorization while the error is visible;
   retry goes to the connected destination without re-opening or restarting.
   Separately expire/fail the attempt: retry creates a new attempt/readiness
   and the player sees the input choice again. Preserve unrelated connections.
6. Retain ordinary success/cancel/provider-failure controls on both routes.
   Do not infer CONTINUE focus from a fixed number of key presses; review the
   current frame before the decisive input, as the original failure exposed.

Canonical proposal for `docs/es-menu-map.md` cloud sign-in flow: add an edge
from **both** keyboard routes' browser-open action to the error dialog above;
Retry loops to open while waiting, goes to connected when completed, and to
STARTING SIGN-IN/input choice when ended; Cancel/Back returns to the cloud hub
through session cleanup. Row placement and successful flows are unchanged.
Add error, retry-error, retry-loaded, cancelled hub, completed-race and
expired-retry frames to the same source/build/locale/panel/review index described
in `flow-proposal.md`. No frame or timing in this packet has been produced.

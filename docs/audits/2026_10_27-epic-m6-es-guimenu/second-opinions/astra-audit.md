This is an **excerpt review**, not a new execution of the pin. I treat the guest results as evidence about the later image only. `GuiMenu.cpp` citations below are at `16dbac5211`; script citations are at `8ebaf8daad`.

## 1. Q2 — Rows, stores and write attribution

**GM-1 — L-09 — confirmed (excerpt).**  
The global VIDEO FILTER row reads and writes `global.videofilters`; the per-system row writes singular `.videofilter`. The launch script requests singular `videofilter`, and the supplied fallback reader looks for `global.videofilter` (`GuiMenu.cpp:5928,5946-5947,10990-10991`; `setsettings.sh:792-808`; `001-functions:165-172`).

**Change:** Keep the finding. It is a wrong-key defect in the global default, not evidence that the per-system row is broken.

**GM-2 — L-10 — confirmed (excerpt).**  
`false` selects SystemConf for this switch, both when reading its initial value and when saving it. The scrolling code instead reads the cached Settings value (`GuiMenu.cpp:9485`; `GuiSettings.cpp:395,408-412`; `Settings.cpp:37,61,145`; `IList.h:110-113,118-121,418-421`).

**Change:** Keep the finding. The supplied code proves the mismatch independently of the guest.

**GM-3 — L-13 and the rows table — narrowed (excerpt).**  
I cannot establish a third **wrong store or wrong key** from the supplied reader/writer pairs. Nor do I see a demonstrably wrong write-to-row assignment in the portions that can be checked:

- The shared transfer save hook assigns each of its four writes to the corresponding component, including the SETTINGS component whose displayed row has an alternative dimmed branch (`GuiMenu.cpp:4864-4913,4919-4925`).
- `internalwifi` really is a local derived from `internal_wifi` (`GuiMenu.cpp:9949-9950`).
- The immediate `wifi.adhoc.id` write takes its value from `optionsAdhocID`, although the enclosing callback belongs to `enable_adhoc`; attributing that write to LOCAL PLAY ID is correct (`GuiMenu.cpp:10052-10053,10133-10138`).

The corresponding theme hooks and several other if/else builder pairs are **outside the packet**, so this is not independent validation of all 275 assignments.

The “eleven unread rows” must not become “eleven ineffective settings.” AUDIO PROFILE calls its API directly; WIREGUARD VPN runs its commands directly. Also, the shown DMD opener is BATOCERA-gated even though the table marks the function’s rows as compiled (`GuiMenu.cpp:2743-2749,2979-2981,10308-10316`). The boot-game path has a visible ES read, too (`GuiMenu.cpp:11318`).

**Change:** Retain the name-search inventory, but distinguish **compiled**, **reachable**, **used as persisted state**, and **applied directly by an API/command**. Repository-wide consumer absence remains outside the packet.

**GM-4 — L-07 — narrowed: caller coverage is right; the claimed protection needs qualification (excerpt).**  
Every `addInputTextConfigRow` invocation goes through `buildInputTextConfigRow`. T21’s diff passes its new `onOk` wrapper to all three editor routes, including the custom editor (`GuiSettings.cpp:167-174,241-254`; T21 diff at the same block).

That establishes coverage of these callers. It does **not** establish a universal “non-empty and changed” guard: the diff sets `openedBlank` only for a hidden, previously non-empty password. Nor is the change in the distribution’s ES pin. The implementation of `TextRowEdit::writes` is **outside the packet**.

**Change:** Say “covered by T21’s common-helper change when that change is incorporated,” not “fixed in the pin.” Keep the narrower hidden-value/untouched-blank contract. The six cited credential sites include conditional builds (`GuiMenu.cpp:8354-8357,8372-8375`).

**GM-5 — L-08 — narrowed; its principal defect is real (excerpt).**  
The SECURITY row is unmasked, the separately constructed `rootpassword` component is never added, and every normal close runs the save hook and invokes `setrootpass` (`GuiMenu.cpp:3263-3273`; `GuiSettings.cpp:73-95`). The command is synchronous despite the double fork: both generations wait (`Platform.cpp:857-876`). For a non-empty password, the script performs the hash, Samba and Syncthing work and conditionally restarts the two services (`setrootpass:29-63`).

The first reader is wrong to make the empty-store/device-password split a consequence introduced by S1. **It already exists at the pin:** this row has `password=false`, and the pin’s editor callback writes an empty string without a guard (`GuiMenu.cpp:3265`; `GuiSettings.cpp:218-237`). The script then refuses it (`setrootpass:22-26`).

**Change:** Remove “after T21’s S1” as the onset of this defect. Also qualify “its twins guard”: they guard script invocation, not persistence of the empty value—GM-32 below.

**GM-6 — L-11 — confirmed, with two reporting corrections (excerpt).**  
The favorite-music write is conditional on the option being enabled with no favorites; the battery threshold write is conditional on a missing value. Both occur in **the same SOUND SETTINGS page**, not two pages (`GuiMenu.cpp:9609-9613,9653-9661`). The timezone is seeded at construction if absent and written by its save hook regardless of whether it changed (`GuiMenu.cpp:1857-1870`).

**Change:** Say “two conditional writes at one page’s construction.” A file mtime change after leaving SOUND SETTINGS does not identify either branch: normal `GuiSettings::save()` also saves both stores when the page has save hooks (`GuiSettings.cpp:88-95`).

**GM-7 — L-12 — narrowed; the six-page description is wrong (excerpt).**  
The empty-save-function trap is real (`GuiSettings.cpp:88-95`). The four relink subpages use explicit finalizers to persist their direct config editors (`GuiMenu.cpp:8307-8309,8360,8376,8393`).

But the cited provider form and ADD CONNECTION page are not two more config-row-only pages. They use `addInputTextRow` and keep values in local shared objects, later consumed by explicit connection actions (`GuiMenu.cpp:7260-7262,7361-7365,7381-7390,7900-7919`).

**Change:** Replace “six `addInputTextConfigRow`-only pages” with the four relevant relink subpages. Keep the systemic persistence trap, but do not prescribe a SystemConf/Settings save for the two cloud forms. Also correct `03`’s claim that *every* settings-page close writes both stores; the early return disproves that.

**GM-8 — L-14 — confirmed (excerpt).**  
The RGB LED section and the first SECURITY page are behind BATOCERA conditions. The supplied ROCKNIX LED COLOR implementation consistently uses `led.color` (`GuiMenu.cpp:2987-3105,3202-3246,2150-2171`).

**Change:** None to the conclusion. Do not promote `led.colour` into a shipped ROCKNIX wrong-key finding.

**GM-9 — L-15 — narrowed (excerpt).**  
The developer page does not consume `exitreboot`, but the same change also sets `reboot`, which its finalizer does consume (`GuiMenu.cpp:1095-1101,1457-1466`). Thus the notification is not lost. What is absent is the `ExitOnRebootRequired` handling found on the other pages (`GuiMenu.cpp:976-982,3281-3290`).

**Change:** Describe the missing exit-on-reboot-required behavior, rather than implying that the change produces no reboot indication.

## 2. Q3 — Interface-thread work and bounds

**GM-10 — L-04 — narrowed: the concern holds, but the inventory and timing claims need repair (excerpt).**

**Visible omissions or misleading classifications:**

- The page table has a `CloudConnectionsPage` class row, but omits work in its two actual page builders: `cloudSetupInfo()` in the cloud hub and the additional `cloudRemoteLines("list")` in CLOUD CONNECTIONS (`GuiMenu.cpp:5605,5678,8065-8066`). The constructor’s list read and the top-window read are separate costs (`GuiMenu.cpp:5579,5589`).
- `cloudFolderContext()` is marked unbounded in the table, but its command explicitly requests a five-second timeout (`GuiMenu.cpp:6916-6919`). This applies both at construction and in the action-time selection check (`GuiMenu.cpp:6993,7012-7018`).
- `cloudCheckFolders()` is not simply an unbounded worker helper: it has a five-second context read, a 35-second validation command, and another five-second context read—nominally up to 45 seconds across those subprocesses (`GuiMenu.cpp:6976-6985`).
- Calling `cloudScanContent` or `cloudOpenTransfer` “bounded” because a transitive stamp check uses `timeout 5` is too broad. The scan command itself is handed to `GuiCloudTransfer` without that timeout; the five-second checks run in continuation callbacks (`GuiMenu.cpp:5229-5238,5260-5268`).
- The intentionally blocking native sign-in handoff is another distinct category. It calls `launchCloudSignIn` on the interface thread, after placing the return page on the stack; it is not a spinner-backed check (`GuiMenu.cpp:7684-7687,7862-7870`). Its API implementation is **outside the packet**.

**What a player can encounter:**

| Path | What the supplied code establishes |
|---|---|
| Cloud hub, connections, provider/form metadata | No caller-side deadline for the list/providers/fields/choices calls. These pages have no general network precondition (`GuiMenu.cpp:5579,5589,7233,7321,7450,8066,8091`). However, `cloud_remote list` visibly reads configuration; it does not visibly invoke rclone (`cloud_remote:244-254`). A wedged rclone is therefore not a proved explanation for every listed call. The relevant helper implementations are partly **outside the packet**. |
| SSH setup information | A requested ten-second timeout per `cloudSetupInfo()` call. Entry can make another such call when it proceeds into the first SSH step (`GuiMenu.cpp:6254,8164-8181,6662`). |
| Folder/stamp gates | Requested five-second timeouts on the interface thread, with no spinner for that wait (`GuiMenu.cpp:4188-4190,6918,7014`). |
| Starting or leaving sign-in | `cancel` is not merely a normally instantaneous local call. Its script invokes a function containing a one-second sleep (`cloud_oauth:879,2817-2819`). Starting sign-in calls it before showing the loader (`GuiMenu.cpp:7515,7533,7624`). The waiting dialog’s explicit cancel calls it and then closes a session-owning page, causing a second cancel: at least two seconds of script sleeps on that path (`GuiMenu.cpp:7833-7836,6471-6476`). |
| Sign-in which never becomes ready | The worker can perform 60 half-second sleeps **plus** the time spent in the unbounded `info` invocations. Thirty seconds is not an end-to-end bound (`GuiMenu.cpp:7552-7589`). |
| Non-answering NetworkManager | The shown current-SSID query, saved-network enumeration, forgetting, and association run off the interface thread (`GuiMenu.cpp:9830-9847,9857-9866,10414-10434,10495-10511`). Their exact API timeouts are **outside the packet**. These particular paths must not be described as synchronous NM freezes. |
| Network services and USB gadget | The service commands and the USB gadget reads have no caller-side deadline and are reachable without Internet access (`GuiMenu.cpp:10182-10224,10232-10246`). Tailscale’s seven-second option does not bound the subsequent `tailscale status` invocation or the surrounding service commands (`GuiMenu.cpp:10336-10341,10514-10517`). |

The explicit worker-command deadlines of 30, 100 and 60 seconds are correctly visible for the folder editor, connection form and connection changes (`GuiMenu.cpp:6564-6565,7407-7408,7994-7995`). They are requested command deadlines, not measured whole-flow maxima.

**Change:** Regenerate or annotate the page inventory. Describe the count as caller-side process sites under the tool’s method, not 116 independently proved indefinitely blocking operations. Separate deliberate application handoff, bounded UI stalls, worker waits and genuinely unbounded UI calls. The deterministic cancel delays deserve attention even on a healthy device.

## 3. Q4 — Reads that can be stale

**GM-11 — L-01 — confirmed (excerpt).**  
The shell removes and rewrites one fixed QR filename; the existence test uses the cache. A cached miss therefore survives a later successful write (`GuiMenu.cpp:7767-7796`; `FileSystemUtil.cpp:200-215,1122-1145`). File caching defaults on (`Settings.cpp:29,155`).

**Change:** Keep the defect, but say “until cache invalidation,” not literally “until restart.” The packet includes an explicit cache reset and a UI route which invokes it (`FileSystemUtil.cpp:258-262`; `GuiMenu.cpp:1455`). A cached positive proves a stale predicate, not by itself what image will subsequently be drawn.

**GM-12 — L-02 — narrowed: the transition route exists; the visual-cache conclusion is conditional (excerpt).**  
A ready session with `onDevice=false` goes directly to another sign-in page. Its QR is constructed before `cloudSetupPresent` closes the previous page (`GuiMenu.cpp:7644-7646,7767-7793,7862`; `GuiMenu.cpp:6501-6503`). TRY AGAIN at `7826` can supply that still-live predecessor.

The code explicitly allows no-device and legacy-script routes: `info` derives `ON_DEVICE` from browser availability, while ES’s legacy `url` fallback leaves `onDevice=false` (`cloud_oauth:802,882-885,2803-2810`; `GuiMenu.cpp:7542-7543,7599-7603`). Thus the guest’s `ON_DEVICE=yes` does not establish general unreachability.

However, the texture key is **not path alone**: it includes tiling, filtering and `shareId`. `ImageComponent` can use a per-instance share ID (`TextureResource.cpp:100-131`; `ImageComponent.cpp:382-408`). The relevant constructor/default sharing state and complete reload behavior are **outside the packet**, including the beginning of `UntintedImageComponent` before the supplied `:6406` excerpt.

**Change:** Keep a conditional stale-texture lead and the retry route. Do not call the old QR’s actual rendering proved until shared-key/default and reload behavior are checked. A two-session image fixture should demonstrate it.

**GM-13 — L-03 — narrowed; the “stamp gate” and stated symptom are inaccurate (excerpt).**  
The cached regular-file predicate is real (`GuiMenu.cpp:4133-4149`; `FileSystemUtil.cpp:238-240,1164-1177`).

But `:4589` is **not a gate around the reads**. It assigns `r.rc`; both scan files are then read regardless, and only `build(r)` interprets the status (`GuiMenu.cpp:4588-4592,4306-4314`). The first reader therefore cannot use this as proof that a prior failed write is necessary before a miss can be cached.

Nor do all poisoned reads produce COULDN’T SAVE WHAT YOU TICKED. That is the selection-save path. A later valid scan status with an empty scan vector can instead reach the “nothing matches” message; a failed settings-facts read becomes an empty facts map (`GuiMenu.cpp:4213-4217,4476-4480,4158-4169,4899-4905`).

**Change:** Separate selection-file and scan-file consequences. The exact production route to missing scan files requires `cloud_scan` behavior **outside the packet**; do not replace that missing evidence with the claimed gate.

**GM-14 — L-30 — narrowed; the exclusion of other mutable files is wrong (excerpt).**  
The table itself contains another important cached mutable path: `/storage/.config/wireguard/wg0.conf`, whose existence controls whether the VPN row is built (`GuiMenu.cpp:10302-10307`). It cannot be dismissed as a binary on the immutable image. See GM-34.

The writers and lifecycle of such other table entries as `/storage/.ms_supported` are **outside the packet**; the table’s `GuiMenu.cpp:2239,2270` references alone do not establish their safety.

**Change:** Keep the enumeration as a reported tool result, but remove the conclusion that only QR and scan/selection paths need external-writer scrutiny. Distinguish “listed” from “writer and invalidation audited.”

## 4. Q1 — Page lifetimes and transitions

**GM-15 — L-16 — narrowed to layout coupling, not a demonstrated clipping defect (excerpt).**  
The ordinary branch is explicitly 75% high; the comment describes a retained 15% top offset. Those figures leave a margin. The taller instruction branch is both resized and positioned (`GuiMenu.cpp:6488-6499`).

**Change:** Keep this as reliance on the default positioning contract, not an established off-screen-buttons bug. The actual `GuiSettings` constructor positioning is **outside the packet**. The full-screen branch also prevents the supplied small-panel walk from testing this code (`GuiMenu.cpp:6488`).

**GM-16 — L-17 — narrowed; “safe by a self-capture cycle” is too strong (excerpt).**  
The fork’s Wi-Fi callbacks do capture their own shared components, creating retention cycles (`GuiMenu.cpp:10097,10133`). That can preserve the switch and callback across a page deletion. It does **not** preserve the deleted settings page, its list, or every caller above the switch. The two supplied input levels return immediately after the consumed input; the remaining input chain is **outside the packet** (`SwitchComponent.cpp:64-67,156-163`; `ComponentList.cpp:154-165`).

Also, the specific synchronous `!wifienabled` local-play branch is not shown to be an ordinary reachable player path: LOCAL PLAY MODE is added only while base Wi-Fi is enabled, and turning Wi-Fi off puts up a loader and rebuilds the page (`GuiMenu.cpp:9964-10036,10124-10129,10149-10153`). Do not equate a constructed callback invocation with demonstrated UI reachability.

The supplied weak/ownership protections otherwise look locally appropriate: picker rebuild ownership, transfer callback cleanup, and the connections page’s alive check are visible (`GuiMenu.cpp:4529-4584,5202-5206,5580-5594`). The detached workers use weak rows and `AppWindow::post`, but the latter’s shutdown guarantee is **outside the packet** (`GuiMenu.cpp:9748-9751,9785-9804,9835-9847`).

**Change:** Restore `02`’s qualified “plausible-safe at the levels read,” rather than `04`’s safety conclusion. Record cycles as leaks, not an ownership strategy. There is also a concrete missed failure-path lifetime defect—GM-31—and additional cycles in GM-33.

## 5. Q5 — Words, French and dialog landings

**GM-17 — L-18 — confirmed (excerpt).**  
The failure text names CONNECT OR REPAIR CLOUD STORAGE, whereas the hub builds CLOUD CONNECTIONS and opens that page (`GuiMenu.cpp:8460,5722-5724,8065`).

**Change:** Keep the finding. Use the pin’s label, not the later image’s MANAGE CLOUD CONNECTIONS label, when describing the correction.

**GM-18 — L-19 — confirmed (excerpt).**  
The match refusal collects raw non-plan lines, uppercases them and places them directly into the dialog. No localization mapping intervenes (`GuiMenu.cpp:5313-5326`). This differs from the explicit localization of persisted cloud failure reasons (`GuiMenu.cpp:4695-4703`).

**Change:** Keep it, and broaden the search for this pattern: the maintenance failure path has the same omitted localization step—GM-37.

**GM-19 — L-20 — confirmed as an extraction/catalog gap, not an inability of runtime gettext to translate (excerpt).**  
The two descriptive provider labels are plain strings in `recommendedProviders`, while the caller passes a computed msgid to `_()` (`CloudText.cpp:20-35`; `GuiMenu.cpp:8116`). That call could translate a manually supplied catalog entry; the defect is that this source location does not provide an extractable literal.

The actual French catalog contents are **outside the packet**, so their absence is supported here by the supplied audit results, not an independent catalog read.

**Change:** Keep that distinction. Fixing extraction alone will not fix the other provider displays that never call gettext—GM-36.

**GM-20 — L-21 — narrowed (excerpt).**  
The fork-specific branch contains sentence-case dialog prose (`GuiMenu.cpp:1513-1520`), contrary to the supplied ALL CAPS rule. The URL, however, is explicitly something to open **on a computer**. These lines do not establish a clickable-link expectation or independently prove that a URL itself violates the rules.

**Change:** Keep the case finding; separate it from any proposed URL/QR design change.

**GM-21 — L-22 — confirmed, with an important boundary on the back-button conclusion (excerpt).**  
Both TRY AGAIN / CANCEL SIGN-IN dialogs select the last button as their back accelerator; that closes the owning page and cancels the session (`GuiMenu.cpp:7702-7717,7824-7827,6471-6476`; `GuiMsgBox.cpp:121-133`). The OK / CANCEL SIGN-IN dialog instead selects OK (`GuiMenu.cpp:7830-7837`; `GuiMsgBox.cpp:125-128`).

I see no additional destructive **confirmation** landing on its affirmative button in the supplied cloud/network paths: removal, folder creation and matching all have inert last/NO alternatives (`GuiMenu.cpp:8056-8058,7036-7045,5381-5386`).

But “back only dismisses single-OK dialogs” would be false: the completed settings-restore acknowledgment invokes `maintenanceRestart`, so Back there reboots after the already-authorized restore (`GuiMenu.cpp:383-384,419-421,327-332`; `GuiMsgBox.cpp:117-119`).

**Change:** Keep the sign-in landing as a style decision, not a newly discovered destructive-operation consent bug. Describe two dialog sites, not one.

**GM-22 — L-23 — narrowed to the evidence actually supplied (excerpt).**  
The page and both openers agree on FINISH RESTORE PROCESS (`GuiMenu.cpp:8266,5739-5741,10269-10271`), matching D-UI-046.

**Change:** Keep the code-side conclusion. The claimed stale heading at `docs/es-menu-map.md:405` is **outside the packet**; identify it as a reported documentation discrepancy rather than an independently reread one.

**GM-23 — L-24 — narrowed (excerpt).**  
Mixed-case source msgids do not by themselves prove mixed-case rendered row labels. The relevant calls use `addWithLabel`, and this file expressly documents that helper as uppercasing labels (`GuiMenu.cpp:10349,10860,10443-10445`). Its implementation is **outside the packet**, so the displayed-case defect is not established here.

The fuel-gauge catalog entries and the cited bare ejection-dialog literals are also **outside the supplied source/catalog excerpts**. Furthermore, the ejection method’s declaration is BATOCERA-only (`GuiMenu.h:94-96`).

**Change:** Separate literal spelling, rendered case, translation coverage and ROCKNIX reachability. Do not count all these as demonstrated shipped French/UI defects.

**GM-24 — L-25 — narrowed (excerpt).**  
A blank HOSTNAME is already writable at the pin: the row is not a password row, and its editor writes the submitted value directly (`GuiMenu.cpp:9929`; `GuiSettings.cpp:218-237`). The row displays an empty stored value as empty (`GuiSettings.cpp:190-193`). S1 does not introduce that behavior.

The precise empty-hostname fallback contract is implemented elsewhere; the code here only invokes `cleanHostname` and conditionally shows NETWORK NAME (`GuiMenu.cpp:9909-9912`). That implementation and the boot script are **outside the packet**.

**Change:** Remove the “after S1” framing. Keep AUTO as a proposed presentation decision, contingent on the actual fallback contract.

## 6. Q6 — Commands and output readers

**GM-25 — L-27 — confirmed, but the nine credential sites are not a whole-file quoting audit (excerpt).**  
The two quoting functions implement the same single-quote algorithm (`GuiMenu.cpp:7183-7194`; `StringUtil.cpp:426-442`). The supplied cloud builders quote their variable arguments, including selections, paths, form fields and nested OAuth arguments (`GuiMenu.cpp:4111-4116,6564-6565,7381-7390,7525-7530`).

There are nevertheless unquoted string-built commands elsewhere: the selected timezone, LED color and USB gadget selection (`GuiMenu.cpp:1868,2167,10244`). Timezone/USB values come from script/API option sources whose full contracts are **outside the packet**. LED color has a visible persistent-config fallback and a concrete shell-syntax problem—GM-35. Constant QR and WireGuard paths are a different, much narrower case (`GuiMenu.cpp:7767-7771,10302,10310-10314`).

**Change:** Keep the duplicate-helper refactor note. Do not turn “nine credential sites quoted” into “all string-built commands quoted.”

**GM-26 — L-05 — narrowed; the byte loss is proved, but two conclusions need correction (excerpt).**  
`GetShOutput` unconditionally removes the last byte of each `fgets` result and discards line boundaries and the process exit status (`Platform.cpp:891-904`). The form/error matching is exposed to that loss (`GuiMenu.cpp:7139-7155,7407-7422`).

However:

- `find_first_of("\r\n")` is not universally dead. A CRLF line loses its LF but retains its CR. The statement “can never match” is false for this reader in general (`Platform.cpp:897-900`).
- Falling back to the generic **failure** sentence is diagnostic loss, not by itself a fail-open guard. The supplied refusal fixture does not prove false success (`GuiMenu.cpp:7429-7432`).

There is another affected reader: the connections-page snapshot comparison. Two outputs differing only at a discarded byte can compare equal and suppress refresh (`GuiMenu.cpp:5579,5589-5592`).

**Change:** Keep the byte-loss finding; narrow the newline claim, remove the unsupported fail-open characterization, and include snapshot fidelity in its impact analysis. GM-38 is a separate, actual fail-open status-reader path.

**GM-27 — L-06 — confirmed as brittleness (excerpt).**  
The parsers differ exactly as reported (`GuiMenu.cpp:7419-7422,7998`). The explicit success records for create/update and select/remove are both `OK=<name>` (`cloud_remote:257-266,320-335`).

**Change:** Cite both producer paths, not only select/remove. Retain this as inconsistent protocol handling, not a demonstrated current failure. Whether called helpers emit additional output is partly **outside the packet**; a robust common reader should use a complete success record and the exit status.

## 7. Q7 — Structure, duplication and merge debt

**GM-28 — L-26 — confirmed (excerpt).**  
The three outcomes differ as reported: the close-time association always shows a verdict, relink shows only failure, and the ENABLE WI-FI callback discards the result and rebuilds (`GuiMenu.cpp:10084-10090,8320-8332,10124-10129`). LOCAL PLAY MODE also discards its result (`GuiMenu.cpp:10172`).

**Change:** Keep the inconsistency finding, but describe the operations separately rather than assuming every Wi-Fi preference change must have the same success dialog. Add the unchanged-credential application issue in GM-40.

**GM-29 — L-28 — narrowed: overlap is not proof of a future Git conflict (excerpt/table evidence).**  
The supplied merge table is internally consistent with eight overlapping hunks, including all four listed Wi-Fi hunks. But its method widens hunks by context. Hunk proximity/overlap does not alone prove that the next merge will conflict, much less establish the required resolution.

The current competing network implementation is substantial and plainly separable as a planning concern (`GuiMenu.cpp:9744-10512`; `GuiMenu.h:51-59,79`). Actual upstream/fork diffs and a trial merge are **outside the packet**.

**Change:** Replace “certain at the next merge” with “identified integration hotspots.” Keep D-WORKFLOW-080(a) as the recorded planning option, not an already-proved mechanical split.

**GM-30 — L-29 and the structural positives — narrowed (excerpt).**  
The split conditional braces are real in the supplied filter code, but a non-balancing first arm is not a malformed preprocessed translation unit (`GuiMenu.cpp:5918-5950`). The whole-file counts and complete declaration/definition matching remain supplied generator evidence; omitted definitions prevent an independent full recount.

Two positive claims need precision:

- FINISH RESTORE PROCESS’s two menu rows really are textually equivalent (`GuiMenu.cpp:5739-5741,10269-10271`).
- The gated-row press recheck applies only to rows initially built **unconfigured**. The configured branch installs the action directly (`GuiMenu.cpp:6290-6294,6313-6324`).

Also, “each page is one function” is not an accurate structural description: `openRestoreRelink` constructs its main page and multiple nested settings pages (`GuiMenu.cpp:8266,8296,8352,8370,8391,8412`).

**Change:** Keep the structural inventory with its build-flag/method scope. Correct the universal recheck and one-page/one-function language; the page inventory limitations in GM-10 also need addressing.

## New findings

**GM-31 — new — new: failed repair transition leaves a dangling parent pointer (excerpt).**  
**Family:** a page’s lifetime or thread.

With multiple connections, each picker row captures the original setup page `s`. A press closes `s` **before** attempting to build the SSH step (`GuiMenu.cpp:8226-8235`). If that step finds no IP, it shows a dialog and returns without replacing the picker (`GuiMenu.cpp:6662-6667`). The picker survives with every row still holding the freed `s`; a second press calls `s->close()` again. `close()` deletes its object (`GuiSettings.cpp:73-80`).

**What would prove it:** An ASan lifetime fixture: open the multi-connection picker, make `cloudSetupInfo()` return no IP, dismiss the error, press a connection again.

**Change:** Add a high-priority lifetime finding. Closing a different callback holder is not sufficient safety analysis; failed replacement must preserve valid ownership for another press.

**GM-32 — new — new: both “guarded” device-password pages can persist an empty password setting (excerpt).**  
**Family:** a row that writes or reads the wrong place.

SSH PASSWORD and DEVICE PASSWORD both use unmasked config editors. Submitting empty writes `root.password=""` into memory. Their guards skip `setrootpass`, but the enclosing `GuiSettings::save()` subsequently saves SystemConf anyway (`GuiMenu.cpp:6527-6539,8413-8423`; `GuiSettings.cpp:234-237,88-95`). The device password stays unchanged while its displayed/configured representation is cleared.

**What would prove it:** Exercise each actual close path with a non-empty initial value and an empty accepted edit. Assert an empty persisted setting, no `setrootpass` invocation, and unchanged device-password state.

**Change:** Extend L-08’s state-split finding to these pages. The guard must protect the stored credential as well as the application command.

**GM-33 — new — new: additional self-capture cycles survive ordinary page closure (excerpt).**  
**Family:** a page’s lifetime or thread.

The cloud hub’s two switches capture their own shared pointers. Provider-form boolean switches do likewise and additionally retain the shared values map. Several network-service switches repeat the pattern (`GuiMenu.cpp:5648-5660,7298-7304,10178-10195,10285-10297`). These are additional cycles beyond L-17’s three examples.

There is no corresponding cleanup in these builders, unlike the explicit callback clearing on transfer options (`GuiMenu.cpp:5202-5206`).

**What would prove it:** Retain weak component/map probes, open and close the pages without changing anything, and assert expiration; use LSan or object counters across repeated visits.

**Change:** Record these as lifecycle leaks. In the provider form the retained map can contain entered credentials; do not claim the whole page is retained when the graph specifically retains components and captured data.

**GM-34 — new — new: WireGuard row availability is cached across external configuration changes (excerpt).**  
**Family:** a read that can be stale.

The VPN row exists only if the cached `exists(wg0.conf)` returns true (`GuiMenu.cpp:10302-10307`). Creating that file externally after a cached miss can leave the row absent on subsequent visits; deleting it after a positive leaves a row whose prerequisite is gone (`FileSystemUtil.cpp:200-215,1127-1131`).

**What would prove it:** Open NETWORK SETTINGS with the file absent, create a test configuration from another process, reopen in the same ES process, then compare after cache reset. Test deletion in the opposite direction too.

**Change:** Add this to the mutable-file findings. Identifying the distribution’s normal installer/writer requires files **outside the packet**, but the external-write/cache failure itself does not.

**GM-35 — new — new: persisted LED color is interpolated into nested shell syntax (excerpt).**  
**Family:** a row that writes or reads the wrong place—its data is passed as command syntax.

An unrecognized `led.color` from SystemConf is deliberately retained as a selectable option. The selected string is then inserted into `sh -lc` without argument quoting (`GuiMenu.cpp:2150-2167`). This is stronger evidence than merely observing an unquoted constant: a persistent setting has a visible path into shell interpretation.

**What would prove it:** A command-construction fixture using a harmless metacharacter-bearing stored color, selecting it after another option, and checking that the shell performs only one intended invocation with one literal argument.

**Change:** Add a command-boundary defect. The packet proves the unsafe construction, not a remote attacker’s ability to supply that setting; do not invent that threat path.

**GM-36 — new — new: provider text bypasses localization outside the recommended list (excerpt).**  
**Family:** a word or dialog that breaks the house rules.

`providerLabel()` returns the plain recommended label without gettext. Its results are displayed directly in CONNECTED TO, connection details and connection-list descriptions (`CloudText.cpp:39-46`; `GuiMenu.cpp:5679-5682,8012,8078-8080`). Thus adding French catalog entries for L-20 alone will not translate WINDOWS SHARE (SMB) or AMAZON S3 AND COMPATIBLE at these sites.

The provider form also displays script-supplied choice descriptions directly. The script selects the example’s Help line as the label; ES installs that label without localization (`cloud_remote:232-237`; `GuiMenu.cpp:7323-7328`). Subprovider labels take a similar raw-text route (`GuiMenu.cpp:7452-7455,7471`).

**What would prove it:** A French fixture with catalog entries for the descriptive provider labels and a known descriptive choice label; exercise these displays separately from RECOMMENDED.

**Change:** Audit the entire provider-text pipeline. Distinguish descriptive English from proper names and user-supplied connection names.

**GM-37 — new — new: maintenance failure reasons also bypass French (excerpt).**  
**Family:** a word or dialog that breaks the house rules.

`runMaintenanceCommand` extracts `>>> why` or the last plain line, then uppercases that raw result into the dialog. Only the fallback and COULDN’T FINISH prefix are localized (`GuiMenu.cpp:343-349,360-389`). The known reason does not pass through the localization used by cloud last-run messages (`GuiMenu.cpp:4695-4703`).

**What would prove it:** Feed a nonzero maintenance result with an English reason having a French translation; verify the dialog body under French. The scripts’ complete current reason inventory is **outside the packet**.

**Change:** Add this alongside L-19 rather than treating the match preview as the only script-text localization leak.

**GM-38 — new — new: missing relink status output is accepted as success (excerpt).**  
**Family:** a row that writes or reads the wrong place—command-output reader.

The relink check parses the returned string with `atoi`; an empty result becomes zero and displays YOUR CLOUD IS ANSWERING (`GuiMenu.cpp:8445-8453`). `GetShOutput` discards `pclose`’s status, so a shell that terminates before producing the final echo is indistinguishable here from a successful numeric answer (`Platform.cpp:893-904`).

**What would prove it:** Inject a child termination before `echo $?`, or supply an empty-output/nonzero-exit fixture, and assert that the page does not report success.

**Change:** Add a fault-path fail-open finding. This is not the normal “cloud is offline” path; it is loss of the status channel.

**GM-39 — new — new: `GetShOutput` does not handle process-open failure (excerpt).**  
**Family:** a row that writes or reads the wrong place—command-output reader.

Unlike `GetShOutputLines`, `GetShOutput` does not check whether `popen` returned null before passing the pointer to `fgets` (`Platform.cpp:893-897,911-913`). Callers include page construction itself (`GuiMenu.cpp:5579`).

**What would prove it:** A fixture which forces `popen` failure and verifies a handled failure rather than undefined behavior/crash.

**Change:** Add this to the Platform handoff accompanying L-05. The existing four output-content cases do not cover process-start failure.

**GM-40 — new — new: leaving an untouched Wi-Fi credential page reapplies the connection (excerpt).**  
**Family:** a row that writes or reads the wrong place—credential application/save semantics.

The relink Wi-Fi page’s finalizer always saves, then calls `enableWifi` whenever Wi-Fi, SSID and key are non-empty. It does not compare the key with its value at entry (`GuiMenu.cpp:8296-8333`). Merely opening the page and backing out can therefore start association work. T21’s blank-editor guard does not prevent it.

**What would prove it:** Start with complete credentials, open WI-FI PASSWORD, make no edit, close it, and count `enableWifi` invocations.

**Change:** Add this under the supplied non-empty-and-changed saving rule. Keep any timing claim conditional: the association implementation is **outside the packet**.

**GM-41 — new — new: FINISH silently ignores failure to remove the restore marker (excerpt).**  
**Family:** a word or dialog that breaks the house rules.

When `consumeMarker` is true, FINISH ignores `std::remove`’s result and closes unconditionally (`GuiMenu.cpp:8486-8493`). On a read-only/erroring storage path it therefore behaves like LATER with respect to the marker, despite the distinct contract described immediately above (`GuiMenu.cpp:8467-8482`). The menu entry remains eligible because its existence check is fresh (`GuiMenu.cpp:10261-10271`).

**What would prove it:** Inject a removal error and verify that the marker remains while the page closes without a failure indication.

**Change:** Add an explicit marker-consumption failure case; do not describe consumption as guaranteed.

**GM-42 — new — new: the no-`cloud_scan` compatibility branch cannot reach transfer options (excerpt).**  
**Family:** a word or dialog that breaks the house rules—a recovery dead end.

`cloudOpenTransfer` explicitly falls back to `cloudOpenTransferOptions` when `cloud_scan` is absent. But that function immediately requires `cloudScanStamped("done")`; with the initially empty run ID it fails without constructing the options page (`GuiMenu.cpp:5253-5256,4838-4841,4176,4183-4186`). The documented older-script fallback therefore does not work in that state.

**What would prove it:** A fixture with `cloud_scan` absent and no prior run ID, invoking the transfer opener and asserting that the intended compatibility page can be reached.

**Change:** Record this as a latent compatibility-path defect, not a demonstrated failure on the supplied image. Either preserve a working compatibility path or remove the misleading fallback contract.

## Highest priorities

1. **GM-31:** a recoverable no-network failure leaves a picker capable of calling a deleted page on the next press (`GuiMenu.cpp:8234-8235,6662-6667`). This is the strongest newly identified lifetime defect.
2. **GM-35:** persistent row data reaches shell syntax in a root interface. The unsafe construction is concrete even though an external attacker path is not established (`GuiMenu.cpp:2150-2167`).
3. **GM-10 and GM-5:** interface-thread blocking is broader and sometimes more deterministic than the first reader’s “normally short local calls” framing—especially cancellation sleeps and unconditional password application.
4. **GM-1, GM-2 and GM-32:** player choices or credential representations are persisted incorrectly. Fix verification should include an existing `/storage` configuration, not only fresh defaults.
5. **GM-17:** the dead recovery instruction is certain on its error branch and cheap to correct. The localization findings should then be fixed as complete text pipelines, not isolated literals.
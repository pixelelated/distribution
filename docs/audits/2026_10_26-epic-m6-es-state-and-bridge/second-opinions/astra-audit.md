## 1. The commands — Q1

**SO-1 — narrowed — The command count is not a complete argument-flow audit (excerpt).**  
Evidence: `ApiSystem.cpp:838,1527,1578,1659,2509,2591-2593,3489-3518,884-886`.  
The twelve double-quoted call sites visible here are listed in 02; the other four listed sites, and the construction of some variable commands, are **outside the packet**, so I cannot certify exhaustiveness. Count arguments, not just calls: extraction quotes both source and destination, and PDF rendering includes a filename-derived output prefix. The external-string table also omits the visible `system` argument joined into the BIOS command at `:884`, demonstrating that a checked call count does not establish complete string provenance.

**SO-2 — narrowed — L-01 is a real shell sink, but not “every .7z up to 128 MB” (excerpt).**  
Evidence: `ScreenScraper.cpp:274-308`; `ApiSystem.cpp:1524-1531,1557,2239`; `guest-cycle/g01-identity.txt:25`.  
02 is wrong about unconditional reachability: a name override bypasses hashing, an existing MD5 bypasses it above 1 MiB, the size must be positive, and archive-content hashing must be enabled. With that flag enabled, the filename reaches a shell inside double quotes, with EmulationStation’s supplied root privilege. The shown function calls `getSevenZipCommand()`; its literal definition at `ApiSystem.h:422`, and which systems enable archive extraction, are **outside the packet**, although the guest demonstrably contains `7zr`. An absent executable would not itself prevent shell expansion if this command were invoked.

**SO-3 — refuted — “All bare joins are safe by shape” is not supported (excerpt).**  
Evidence: `GuiBluetoothDevices.cpp:131-151`; `GuiMenu.cpp:3128-3151`; `ApiSystem.cpp:800-815,984,1484-1489`.  
The Bluetooth removal path strips the display name but does not validate MAC syntax; its producer and the other Bluetooth callers are **outside the packet**. The storage assertion is directly wrong: the DEV branch stores the **whole output line** as the selected value, not merely its first token. Bezel installation/removal likewise accepts an unquoted string, but the network-list producer and any filtering are **outside the packet**. These are unvalidated shell boundaries; this packet does not establish an attacker-controlled producer for each one.

**SO-4 — new — More synchronous calls lack a bound in this layer (excerpt).**  
Evidence: `ApiSystem.cpp:573-593,2412-2413,2447-2448,2509,2593`; `HttpReq.h:52-54`.  
Cloud sign-in performs synchronous `open`, `wait`, and `close` commands; notably, `close` runs after the interface has been restored. Even the suspend-capability query can execute an unbounded command, and the PDF and download wrappers provide no deadline. These operations block their caller; exact interface-thread call sites and script-internal bounds not shown here are **outside the packet**, so the audit should distinguish “no wrapper bound” from a demonstrated end-to-end UI freeze.

## 2. The client — Q2

**SO-5 — confirmed — L-02 is an out-of-bounds read with no callback-length bound (excerpt).**  
Evidence: `HttpReq.cpp:579-593`; `stage-b/positives/lifted.out`, header case.  
Converting `buffer` to the string accepted by `trim` searches for a NUL instead of using `size * nitems`. It can read beyond the supplied header until an incidental NUL or inaccessible memory; the fixture’s fifteen-byte read is one manifestation, not its maximum extent. This establishes memory unsafety, not a demonstrated credential disclosure or exploit.

**SO-6 — narrowed — Target deletion is proved; default re-scrape reach is not fully established (excerpt).**  
Evidence: `HttpReq.cpp:324-344`; `Scraper.cpp:434-452,539-567,630-635`; `Settings.cpp:198`.  
Once the temporary opens, `HttpReq` removes the destination before even adding the transfer to the multi handle. Existing-art loss therefore follows when the computed destination names existing art and this download is attempted. But `ScrapeOverWrite=true` alone does not prove that condition: the derivation of `overWriteMedias`, which controls the existing-file bypass, is **outside the packet**. The proposed guest download positive was not supplied.

**SO-7 — narrowed — `file://` rejection is not a complete security closure (excerpt).**  
Evidence: `HttpReq.cpp:147,230-242,324-344,377-378,430-473,529-549`.  
A normal successful libcurl FILE transfer has response code zero, which the intended status logic rejects; see SO-50 for a separate defect in that status read. Its bytes have nevertheless already been read and remain accessible through `getContent()`, with file-backed cleanup deferred until destruction and absent after a kill. The pre-existing destination has already been removed. This proves neither protocol exclusion nor exfiltration, and the packet contains no `file://` guest positive despite 02’s closure saying the window confirmed one.

**SO-8 — narrowed — The extension/path closure depends on filesystem contents (excerpt).**  
Evidence: `ScreenScraper.cpp:722`; `Scraper.cpp:646-676,804-812`; `FileSystemUtil.cpp:642-668`; `HttpReq.cpp:333`.  
The argument that a traversal fails when its first filename-prefixed component is not a directory is reasonable for that particular layout. The code does not establish that this directory or a suitable symlink cannot exist on retained `/storage`, and neither extension source is constrained to an allowed media suffix. Failure to lexically resolve `..` is not a containment guarantee—the kernel resolves it during lookup. The implementation of `changeExtension`, needed to finish the Content-Type analysis, is **outside the packet**.

**SO-9 — new — A media-only TLS exception would be lost on retry (excerpt).**  
Evidence: `Scraper.cpp:539-567,594-596,630-635`; `HttpReq.cpp:111-116`; `HttpReq.h:48-65`.  
Initial media requests receive `HttpReqOptions`, but the 429 retry reconstructs the request using only URL and destination. An exception added only to those initial options would therefore revert to verification on retry; the existing Referer customization is already lost there. A resulting TLS failure becomes an ignored I/O error, leaving the destructive-download problem intact. The fix must preserve an owned request policy across every retry.

**SO-10 — new — Verification changes require error and compatibility changes, not just a switch (excerpt).**  
Evidence: `HttpReq.cpp:192-200,462-468,517-520`; `ScreenScraper.cpp:989-990`; `guest-cycle/g01-identity.txt:29-32`.  
Certificate failures become `REQ_IO_ERROR`, which the scraper reports as “YOU’RE NOT ONLINE”; enabling verification will expose that false diagnosis for trust, hostname, and clock failures. Client-certificate requests also explicitly disable hostname checking, so changing only `VERIFYPEER` leaves that exception behind. The supplied CA-link listing does not prove successful verification against every existing endpoint. Finally, verification does not prohibit initial HTTP URLs or HTTPS-to-HTTP redirects under the shown protocol policy.

## 3. The credentials — Q3

**SO-11 — narrowed — The principal Wi-Fi sinks are present, but the screen proof is incomplete (excerpt).**  
Evidence: `ApiSystem.cpp:635-637,2325-2328`; `wifictl:177`; `GuiWifi.cpp:360-367,392-394`; `StringUtil.cpp:764-784`.  
The key reaches the shell command line, `nmcli`’s command line, and `system.cfg`; command logging applies the dedicated mask before execution. Masking the log does not mask argv or the stored value. Both key-entry popup calls are visible, but their rendering and constructor contracts are **outside the packet**, so I cannot independently verify the stronger claim that the classes have no password mode at all.

**SO-12 — new — Saved-network joins expose the key through another command line and environment.**  
Evidence: `wifictl:452-460`; `001-functions:432-434,578-586,600-602`.  
`join_wifi` obtains the stored key from NetworkManager and passes it to `set_settings`. That helper constructs value-bearing environment assignments and passes them as **argv to the external `env` command**, before they become `awk`’s environment. The single-setting writer likewise puts values into `awk`’s environment through `K` and `V`. This missing sink exists independently of the initial `wifictl connect` command and its log mask.

**SO-13 — narrowed — Scraper storage and query sinks are real; compiled identity is unverified (excerpt).**  
Evidence: `ScreenScraper.cpp:34-45,859-894,1030-1031`; `Settings.cpp:504-506,524-534`; `AtomicFileUtil.cpp:115-147`; `HttpReq.cpp:283-288`; `guest-cycle/g02-modes.txt:4-6`.  
Runtime scraper credentials are ordinary settings strings, serialized without encryption into the live file, record, and potentially interrupted temporaries. Developer credentials enter the shown API URLs; the personal account is appended only when both fields are populated, while the developer probe omits it. The actual compiled identity and provisioning check are **outside the packet**—a permitted identity in the register is not artifact verification. The shared, default-enabled cookie jar is another potential credential store observed at 0644, although the supplied record does not establish that it contained an authentication cookie.

**SO-14 — refuted — The log attribution and blanket “account rows masked” statement are too broad (excerpt).**  
Evidence: `Scraper.cpp:438-452,522-528`; `ScreenScraper.cpp:722,874-878`; `StringUtil.cpp:511-520,738-746`; `GuiMenu.cpp:8364-8374`.  
`Scraper.cpp:524` logs **media-download URLs**, not automatically every API-query URL; account/developer identifiers reach that sink only if present in the returned media URL. The mask does not recognize `devid` or `ssid` as secret names, but the packet does not supply the provider response needed to prove that particular flow. The restored-account heading explicitly displays the ScreenScraper username at `GuiMenu.cpp:8365`, so the account is not uniformly masked on screen.

**SO-15 — confirmed — The root-password display is a configuration value or literal fallback (excerpt).**  
Evidence: `ApiSystem.cpp:1029-1037`; `GuiMenu.cpp:3209-3210`; `StringUtil.cpp:753-762`.  
The screen receives `root.password`, or the literal `linux`, through an ordinary `TextComponent`. Nothing shown checks that this matches the OS authentication database, so it must not be described as verified knowledge of the current root password. The `setrootpass` masking rule is real, but the setter’s other sinks are **outside the packet**.

**SO-16 — narrowed — L-21 describes the sampled image, not an invariant of every writer (excerpt).**  
Evidence: `guest-cycle/g02-modes.txt:2-6`; `guest-cycle/g03-argv.txt:2`; `AtomicFileUtil.cpp:115-147,315-326`; `SystemConf.cpp:106-110`; `001-functions:385-404`; `chksysconfig:67-70`.  
The live system store, record, and installed seed were indeed 0645 in this image. ES normally preserves the replaced file’s mode, but shell writers intersect source modes **and umask**, so “kept by every writer” is false as a universal statement. Mode is also read as recovery policy by `chooseConfig` and `recordLastGood`, not merely copied as metadata. `post-update`’s actual edits and the build step responsible for the installed seed’s mode are **outside the packet**; differing contents do not identify that step.

## 4. The writers and the readers — Q4–Q5

**SO-17 — confirmed — L-10’s seed-to-record chain is real, with an additional missing-file path.**  
Evidence: `001-functions:540-555,593-597`; `AtomicFileUtil.cpp:352-361`; `SystemConf.cpp:86-110,232-238`; `chksysconfig:278-303,323-328`.  
A successfully seeded, usable live file wins selection and can replace the player’s record after ES revalidates that same seeded text. The shell fixture’s S1 is consistent with this exact chain. The first reader also misses that `chksysconfig verify` can leave the file absent when restoration, reseeding, and the subsequent rsync fail; the shown code does not establish a successful existence postcondition. Actual reset/removal entry points and their scheduling are **outside the packet**, but boot ordering alone does not close this failure path.

**SO-18 — narrowed — `SystemConf` protects against cooperating writers, not every writer.**  
Evidence: `AtomicFileUtil.cpp:499-545`; `SystemConf.cpp:91-110,304-337`; `001-functions:542,555-557,595-603`; `chksysconfig:67-104`.  
The locked read-modify-write and publication recheck correctly protect against shell writes that honor the same lock. They cannot serialize the pre-lock seed copy or the unlocked `chksysconfig` copy/rename operations. An unlocked writer can overwrite a newer live file or record despite every individual file remaining whole. The actual `post-update` commands and a scheduling proof excluding overlap are **outside the packet**, so safety against them is not established.

**SO-19 — new — The obsolete-temporary sweep can delete an active record publication.**  
Evidence: `SystemConf.cpp:203-210`; `chksysconfig:67-70,87-96`.  
The comment that nothing else writes `system.cfg.backup.tmp` is wrong: `chksysconfig backup` uses exactly that destination temporary. ES can unlink it before the shell’s rename, making publication fail. This need not destroy the existing record, but it can lose the replacement record the shell was preparing.

**SO-20 — narrowed — `Settings` has both concurrency exposure and a record-retry gap (excerpt).**  
Evidence: `Settings.h:147-157`; `Settings.cpp:469-506,524-539,645-650,670-682`.  
There is no synchronization around map traversal, mutations, dirty state, or the two publications; overlapping saves can publish an older snapshot last or pair a newer live file with an older record. A concrete worker-thread save call is **outside the packet**, so that runtime reach remains unproved. In a single save, a kill between publications leaves a whole new live file and an older record, not necessarily total state loss. But record-write failure merely logs a warning and returns success without restoring dirty state, so the next unchanged save does not retry it. The lifted two-write fixture does not test these map, serialization, or retry behaviours.

**SO-21 — new — XML parse success is insufficient validation, and recording rereads different bytes (excerpt).**  
Evidence: `Settings.cpp:566-601,615-632`; `AtomicFileUtil.cpp:258-264`.  
A well-formed unrelated XML document can pass `load_file`, supply no settings, and then replace the valid record while defaults stand. Moreover, the recording branch rereads the pathname after parsing rather than publishing the bytes that were validated; the recovery branch similarly rereads its source through `copy`. A concurrent replacement can therefore cause unvalidated bytes to become the record or recovered live file. Validation must retain supported legacy settings formats without treating arbitrary XML as a successful settings artifact.

**SO-22 — refuted — The parser does not safely represent every value the shell can write.**  
Evidence: `AtomicFileUtil.cpp:453-466`; `SystemConf.cpp:428-434,466-474`; `001-functions:581-586`.  
Empty values are dropped, so the duplicate rule is actually “last **nonempty** value wins,” not simply “last wins.” A BOM remains part of the key, and carriage returns remain in values: `getBool(..., false)` rejects `1\r`, while `getBool(..., true)` accepts `0\r`. These differences require a shared file grammar; blindly stripping credential bytes is not a safe repair.

**SO-23 — new — The generic rewrite can destroy the hostname sentinel and then its record (excerpt).**  
Evidence: `SystemConf.cpp:32-36,366-406,336-337`; `AtomicFileUtil.cpp:267-277,352-360`; `chksysconfig:57-62,278-301`; `GuiMenu.cpp:9927-9929`.  
Setting an existing hostname to empty, `auto`, or `default` removes its line, unlike the shell’s intentional empty sentinel. If another usable line remains, ES can record that file; `chksysconfig` then rejects both copies for lacking `system.hostname=` and can reseed defaults. The same generic magic-word handling is unsuitable for literal values such as an SSID named `auto`, and the append branch treats `default` inconsistently. The HOSTNAME row’s empty-input validation is **outside the packet**, so this proves the writer defect, not an unconditional menu-trigger trace.

**SO-24 — new — Reloads retain removed or emptied credentials in memory (excerpt).**  
Evidence: `SystemConf.cpp:73-80,148-179,428-430`; `GuiWifi.cpp:332-335`; `wifictl:452-460`.  
`parseSystemConf` adds to `confMap`; reload clears other bookkeeping but not that map. The cleanup only erases affected previously-unsaved keys, so an ordinarily saved key removed by another writer remains visible through `get`. In particular, joining an open network can write an empty `wifi.key`, then reload while retaining the previous network’s key in memory because parsing drops the empty value. This is more consequential than the first reader’s fresh-load BATOCERA example.

## 5. What a failure reads as — Q6

**SO-25 — narrowed — L-22 reaches the successful-connect branch; the toast itself is not supplied (excerpt).**  
Evidence: `wifictl:48-57`; `ApiSystem.cpp:627-637,2328`; `GuiWifi.cpp:377-408`; `guest-cycle/g03-argv.txt:3-8`.  
Both keyed-connect commands return success without a radio, and also when `NMCLI` is unavailable. The GUI then sets the pair, ignores the save result, and invokes `joined(name)` without checking association. The guest proves the script result, not the page interaction; the actual toast implementation after `GuiWifi.cpp:408` is **outside the packet**. Open-network connection is expressly guarded with exit 2, so this is not every Wi-Fi path.

**SO-26 — new — Other callers also turn absence or failure into success (excerpt).**  
Evidence: `wifictl:48-57`; `ApiSystem.cpp:687-705,711-718`; `GuiWifi.cpp:548-569`; `GuiBluetoothDevices.cpp:117-121`.  
A no-device `saved` request exits zero with no lines, which both saved-network readers accept as a successful empty list. By contrast, the shown join/current parsers require positive content, so they do not all inherit L-22. The Bluetooth bulk-delete completion ignores its boolean result and unconditionally says the devices have been deleted.

**SO-27 — narrowed — Signal handling is wrong, but not every killed child becomes zero (excerpt).**  
Evidence: `ApiSystem.cpp:234,2251,2255-2260,2291,2319,2328`.  
The unsafe `WEXITSTATUS` calls can turn a signal terminating the **reaped shell** into zero, as the fixture demonstrates. A shell that survives and reports its child’s signal as a normal nonzero exit is different; the plain `system()==0` executor also does not have this decoding defect. The vector-returning legacy overload discards its pair result too, independently of fixing the decoder. Only three of the reported eleven unsafe reads are visible here; the rest are **outside the packet**.

## 6. L-01–L-22 — dispositions, severity, fixes, and existing devices

**SO-28 — narrowed — L-01; High remains justified (excerpt).**  
Evidence: `ScreenScraper.cpp:274-308`; `ApiSystem.cpp:1527-1528,1659-1660,2509,2593`.  
The conditional root shell-injection boundary warrants High, but the “every archive” claim must be removed. A stream should use literal argv and a checked extraction/hash pipeline, covering source paths, destination paths, and PDF-derived names. **Already written:** retained filenames must remain usable literally after upgrading; a quoting fix cannot identify or undo arbitrary effects of any past execution.

**SO-29 — confirmed — L-02; Medium is reasonable (excerpt).**  
Evidence: `HttpReq.cpp:579-593`.  
Construct the header string using the callback length, then parse bounded bytes. The fixture establishes an overread, not merely malformed header handling. **Already written:** no persistent damage from this read is demonstrated; the fix prevents future reads but cannot retroactively remove any resulting crash material or disclosures.

**SO-30 — narrowed — L-03; Medium for the proven replacement path (excerpt).**  
Evidence: `HttpReq.cpp:324-344,477-510`; `Scraper.cpp:440-452,630-635`.  
Keep the existing target until a unique temporary has completed checked writing/closing and artifact validation, then replace atomically. Do not claim default re-scrape reach until the missing overwrite-policy wiring is inspected. **Already written:** missing or partial art requires a successful re-download or another copy; an update alone cannot recreate it.

**SO-31 — confirmed — L-04’s synchronization defect (excerpt).**  
Evidence: `HttpReq.cpp:395-397,416-521,526`; `HttpReq.h:130-135,161`.  
Writes under the global mutex do not synchronize unlocked reads of `mStatus`. Progress and other exposed state also need a coherent ownership/synchronization policy; making only the status enum atomic is not automatically a complete repair.

**SO-32 — narrowed — L-05 is not “every body verbatim” (excerpt).**  
Evidence: `HttpReq.cpp:439-473,559-562`; `ScreenScraper.cpp:978-980`.  
Only memory-backed requests take this response-body path, and HTML bodies are transformed before logging. Non-HTML bodies remain unredacted peer-controlled text, and the scraper logs its derived error again, so the credential-reflection/log-injection concern remains.

**SO-33 — confirmed — L-06, with an incomplete proposed integration plan (excerpt).**  
Evidence: `HttpReq.cpp:192-200,230-242`; `Scraper.cpp:594-596`.  
Peer verification is disabled globally, and hostname verification is additionally disabled on the client-certificate path. The stream must address both checks, credential-bearing transport policy, and retry option preservation rather than merely introduce a media flag.

**SO-34 — confirmed — L-07 is a leaked header list (excerpt).**  
Evidence: `HttpReq.cpp:172-180,371-390`.  
The list has no retained owner or matching free in request destruction. Its replacement owner must keep it alive for the easy handle’s use; freeing it immediately after `setopt` would replace the leak with a lifetime defect.

**SO-35 — narrowed — L-08’s exposure is real, but the process census is limited (excerpt).**  
Evidence: `ApiSystem.cpp:615-645`; `wifictl:177`; `guest-cycle/g03-argv.txt:4-6`; `001-functions:600-602`.  
The Windows-only unbounded `enable` call is correctly excluded from this Linux finding, and the guest observed three processes, not a live-device `nmcli` join. Add the saved-join `env`/environment sink from SO-12; a zero-hit `top` sample does not exclude later capture.

**SO-36 — confirmed — L-09, with narrower archive and content claims (excerpt).**  
Evidence: `AtomicFileUtil.cpp:50-64,115-154`; `Settings.cpp:557-558`; `SystemConf.cpp:210`; `backuptool:283-292`.  
Unique interrupted temporaries are not matched by these sweeps, but they can be empty or partial, and lock-staging leftovers are not credential stores. The shown default archive list excludes store temporaries; “never reaches a cloud” would require reviewing other collection configurations, which are **outside the packet**.

**SO-37 — confirmed — L-10; High is defensible.**  
Evidence: `001-functions:540-555,593-603`; `SystemConf.cpp:86-110,232-238`.  
The stream should choose recovery before defaults, under the same lock, and publish a checked replacement without a pre-lock copy. It must also distinguish an intentional reset from an accidental missing live file. **Already written:** once seed-derived contents have replaced both live and record, those two files cannot recover the lost player settings; preserve any surviving external recovery source rather than claiming automatic repair.

**SO-38 — narrowed — L-11’s serialization defect is proved, but its exposure is not closed (excerpt).**  
Evidence: `SystemConf.cpp:386-406,414-418`; `TextEditComponent.cpp:68-89,176-185`.  
Line ends in values create additional records. Handling Return specially does not establish an input invariant—`textInput` inserts its supplied text without that check—while the actual clipboard/network path providing such text is **outside the packet**.

**SO-39 — confirmed — L-12, but a mechanical fix is unsafe.**  
Evidence: `SystemConf.cpp:38-54,366,389-391`; `chksysconfig:61`.  
Looking up a key including `=` cannot match this defaults table. Merely changing the lookup to the bare key would start deleting a default hostname too; preserve the shell’s sentinel and define per-key reset semantics first.

**SO-40 — narrowed — L-13’s absent synchronization is established, not a particular worker trace (excerpt).**  
Evidence: `Settings.cpp:469-539,645-650,670-682`; `Settings.h:147-157`.  
The implementation does not meet the stated serialized-writer contract. Which worker invokes a save is **outside the packet**, but record-write retry and validation defects exist independently of proving that concurrency.

**SO-41 — narrowed — L-14’s primitive is unsafe; all eight caller classifications are not independently checked (excerpt).**  
Evidence: `FileSystemUtil.cpp:1429-1443`; `GuiMenu.cpp:11579-11587`.  
`writeAllText` truncates in place and ignores write/close results, with no durability operation. This excerpt proves a persistent theme-settings caller; the other seven call-site bodies and the claimed T18 fix are **outside the packet**.

**SO-42 — narrowed — L-15 is a fresh-load result, not every reload’s result.**  
Evidence: `AtomicFileUtil.cpp:463-466`; `SystemConf.cpp:44,73-80,428-434`.  
A fresh load drops the empty hostname and returns BATOCERA, as the fixture and guest show. An existing instance may instead retain an earlier value because its map is not cleared; the issue is not confined to display wording.

**SO-43 — confirmed — L-16’s unchecked numeric parsing (excerpt).**  
Evidence: `ApiSystem.cpp:1877-1887,2075-2087`; `GuiMenu.cpp:2988-2989`.  
The calls can throw and do not require complete numeric consumption or valid RGB ranges. The page-level consequence is conditional on reaching the supported LED path, rather than affecting every device.

**SO-44 — confirmed — L-17’s lost failure channel (excerpt).**  
Evidence: `ApiSystem.cpp:872-886,924,2233-2252`; `Settings.cpp:207`.  
Enumeration cannot distinguish a successful empty answer from execution/read failure, and it retains output from failed commands. BIOS-at-launch defaults off; the final launch decision made from this result is **outside the packet**.

**SO-45 — narrowed — L-18’s signal claim and eleven-site count (excerpt).**  
Evidence: `ApiSystem.cpp:234,2291,2319,714-718`.  
The demonstrated decoder defect is real for the reaped shell, and printed positive protocol text can then authorize a join result. Do not generalize that to every signalled descendant or claim all eleven sites were independently inspected from these excerpts.

**SO-46 — confirmed — L-19 ignores close failure (excerpt).**  
Evidence: `ApiSystem.cpp:584-595`.  
The function returns the earlier wait result regardless of whether closing the external page succeeds. The close is also synchronous with no deadline in this function, so this is more than an unused diagnostic.

**SO-47 — narrowed — L-20 is an inventory, not an unreachability proof (excerpt).**  
Evidence: `ApiSystem.cpp:2335-2439,3483-3518`.  
The reported 82-row count is supplied tool evidence, not reproducible from the omitted rows here. Existence gates are neither argument validation nor a complete page-reachability table, and a missing command does not prevent shell expansion when a constructed command is invoked.

**SO-48 — narrowed — L-21; Medium remains appropriate (excerpt).**  
Evidence: `guest-cycle/g02-modes.txt:2-6`; `AtomicFileUtil.cpp:115-147,315-326`; `001-functions:385-404`.  
Fix provisioning and converge retained credential files, records, and obsolete temporaries to suitably private modes without widening stricter copies. The first reader’s universal preservation claim and attribution to an unidentified build step should be withdrawn. **Already written:** image updates retain existing broad modes and leftover files unless migration explicitly treats them; narrowing permissions cannot undo previous reads.

**SO-49 — narrowed — L-22; Medium for the proved false-positive operation (excerpt).**  
Evidence: `wifictl:48-57`; `ApiSystem.cpp:627-637`; `GuiWifi.cpp:385-408`.  
The stream should require a positive association result for the requested network and distinguish connection success from failure to remember its settings. The success-handler reach is proved, while the exact toast tail is **outside the packet**. **Already written:** a pair saved after this false positive may still be valid user configuration; re-evaluate actual connection state after upgrading rather than deleting it automatically.

## 7. What the first reader missed

**SO-50 — new — The HTTP response-code read has the wrong destination type (excerpt).**  
Evidence: `HttpReq.cpp:430-435`.  
`CURLINFO_RESPONSE_CODE` requires a `long*`, but the code supplies an `int*`. On LP64 Linux, including the supplied x86-64 guest architecture, that permits an eight-byte write into four-byte storage: a separate memory-corruption defect, not L-02’s overread. Use `long`, check `curl_easy_getinfo`’s result, and do not treat the current status logic as a reliable closure proof.

**SO-51 — new — A successful HTTP status does not prove a successfully written artifact (excerpt).**  
Evidence: `HttpReq.cpp:326-344,361-368,477-506,613-621`; `FileSystemUtil.cpp:1448-1463`.  
Buffered errors from `fflush` or `fclose` are ignored before publication. Separately, `renameFile` returns true when its source is absent, which can authorize `REQ_SUCCESS` without publishing anything. Requests for the same destination also share and remove the same `.tmp` pathname, allowing one request to interfere with another’s open file or publication. These require checked I/O and per-request temporary ownership, not just removal of the early destination unlink.

**SO-52 — new — “Do not record a cut base” lasts only one save.**  
Evidence: `AtomicFileUtil.cpp:343-360,522-539`; `SystemConf.cpp:336-339,414-418,232-238`.  
When a cut file is retained as Live rather than recognized as recoverable, `applyChanges` supplies a final newline to its remaining text. That save skips record publication, but the next load sees a complete usable live file and can record it over the whole older record. Recovery must prevent this promotion or retain evidence of incompleteness; skipping one publication is not a durable safeguard.

**SO-53 — new — `Settings` can widen a stricter copy during recovery or recording (excerpt).**  
Evidence: `Settings.cpp:533,615-631`; `AtomicFileUtil.cpp:118-125,258-264`.  
Recovery copies the backup’s mode onto the live path, so a 0644 backup can replace a damaged 0600 live file with a world-readable one. Conversely, recording uses only the live mode and can widen an already-private backup. Unlike `SystemConf`, this path does not intersect the modes of the copies it is reconciling.

**SO-54 — new — Failed or unvalidated answers become a number or a valid-looking hash (excerpt).**  
Evidence: `ScreenScraper.cpp:1039-1040,1075-1089,306-312`; `ApiSystem.cpp:1527-1530`.  
A successful HTTP response containing invalid user-info XML falls through to thread count **1**, instead of reporting an invalid answer. The developer probe likewise accepts an XML declaration prefix without validating the expected document. In the hash pipeline, extraction failure can still leave `md5sum` producing a valid-looking digest of empty input, which is accepted and written into metadata. Checking only the pipeline’s final exit would not repair that last case.

**SO-55 — new — “RESTORED” and “the next save writes it” overpromise (excerpt).**  
Evidence: `Settings.cpp:615-619`; `SystemConf.cpp:221-227,243-265,290-291`; `AtomicFileUtil.cpp:503-507`; `main.cpp:1041-1042`.  
Both stores set their recovered flag even when writing the recovery back fails; `SystemConf` also does so when the lock is busy. The message therefore conflates using a record in memory with repairing the file on disk. The promised next save may do nothing when there are no pending changes, and a still-missing live file is expressly refused by `saveUnderLock`.

**SO-56 — narrowed — No owner-lifetime bug can be established from the supplied tails (excerpt).**  
Evidence: `GuiWifi.cpp:314-337,350-357,382-408`; `Scraper.cpp:594-596`; `HttpReq.cpp:174-180`.  
The raw-`this` completions require scrutiny, but `GuiLoading`’s lifetime rules and `joined` after line 408 are **outside the packet**; I cannot honestly declare those paths either safe or use-after-free. The visible retry copies its URL before deleting its owner, while the header list is leaked rather than prematurely freed. The reported profile-choice test does not settle every other asynchronous callback’s ownership.

**SO-57 — new — The durability claim is stronger than the checked implementation.**  
Evidence: `AtomicFileUtil.h:16-18`; `AtomicFileUtil.cpp:29-37,168-183`; `001-functions:430-435`; `chksysconfig:67-70`.  
The primitive checks file synchronization but discards directory-open and directory-`fsync` failures before returning true. The shell writers do not synchronize either publication stage. Ext4’s delayed-allocation mitigation and successful SIGKILL fixtures do not establish checked persistence across power loss; the audit should distinguish whole-file replacement, successful rename, and confirmed durability.

**SO-58 — new — A five-second lock budget is not a five-second interface bound (excerpt).**  
Evidence: `SystemConf.cpp:293-305`; `AtomicFileUtil.cpp:195-256,541-543`; `HttpReq.cpp:397-423,599-605`; `HttpReq.h:13-16`.  
Whole-file reads, serialization, writes, and synchronization after lock acquisition have no end-to-end deadline. Likewise, an ostensibly non-blocking HTTP status call processes other requests’ callbacks and file completions under the shared mutex, while memory-backed bodies have no size cap. Move such work off the interface thread and bound transfer/resource consumption; neither a lock budget nor polling terminology guarantees a bounded frame.
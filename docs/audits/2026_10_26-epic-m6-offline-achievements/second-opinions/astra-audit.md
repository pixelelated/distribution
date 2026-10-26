## 1. Where a credential travels

**A-1 — confirmed**  
Evidence: `proxy_service.py:444–474,491–507`; `auth.py:86–109,142–143`.

F-01’s core disclosure is real: the offline-login handler returns the stored body unchanged, and ordinary login rows contain `Token`. In the shown request branch, this requires a `login`/`login2` action, a nonempty `u`, an existing matching login row, and an upstream result other than `"success"` or `"http_error"`; an earlier hardcore branch must not have intercepted the request. An upstream HTTP refusal—including 401/403—returns directly rather than triggering this fallback. Conversely, the connectivity monitor need not declare the whole device offline: failure of this particular upstream attempt suffices. The handler compares neither password nor token, checks neither token invalidation nor the currently configured account, and can therefore return a former account’s retained row.

**A-2 — narrowed**  
Evidence: `proxy_service.py:289–325,452–484,505–507`; `config.py:376–377`.

The first reader missed an explicit peer-address check: anything other than literal `127.0.0.1` or `::1` receives 403. That check also protects against direct LAN requests if the configured bind address is widened, but does not distinguish a local browser’s requests from an emulator’s. No `Host` or `Origin` validation appears in the supplied handler; however, the beginning of `process_proxy_request` and the browser’s navigation/DNS/private-network policies are **outside the packet**, so F-02’s readable browser exploit is conditional, not demonstrated. `X-RA-Store-Only` is a behavior selector reached after the login attempt, not credential proof or a way to override an upstream login refusal; `X-RA-Offline` is response provenance only.

**A-3 — new**  
Evidence: `proxy_service.py:315–320`; `utils.py:110–128`; `network.py:21`; `log_uploader.py:52–55,83–113,354–358`.

The redaction is not complete across credential representations. The raw-query regex recognizes only literal lowercase `t=` and `p=`, so percent-encoded parameter names escape it; the form-body redactor does decode parameter names, making the two paths materially different. Neither utility generally removes `token`, `password`, or JSON `Token` values, and the broader key set in `network.py` does not change the utilities used by this request logger and uploader. The quarantined-store regex protects a particular ordered serialization of sensitive cache rows, not arbitrary credential-bearing JSON, while `extra_files` bypasses redaction altogether. These are coverage defects, not proof that every missing representation occurs in normal emulator traffic.

**A-4 — narrowed**  
Evidence: `raofflineproxy-cache-indexed:185–211`; `raofflineproxy-refresh:123–134,216–219`; `auth.py:119–134`; `network.py:400–427`.

The packet establishes unredacted exception-text sinks, but does not establish a particular helper exception containing a credential-bearing URL. An exception’s possession of a URL is not sufficient: ordinary `HTTPError` stringification does not automatically print its URL. Here, however, the GET implementation can replace the printable message with an upstream API error, and the helpers print dependency-provided errors verbatim. The relevant error-description implementation and ROM-cache/browser exception wrappers are **outside the packet**, so the first reader’s blanket “none needed” conclusion is not justified; nor would it be justified to claim a demonstrated credential leak from these lines alone.

**A-5 — narrowed**  
Evidence: `raofflineproxy-ctl:616,647,788,1029,1244–1265,1979`; `raofflineproxy.service:26–43`; `auth.py:108–109`.

F-05 correctly identifies four username arguments, but incorrectly treats the quoted environment rule as file-wide: that comment specifically describes the listing, which uses `RA_SCAN_USER` as promised. These arguments expose the public account name, not the password or session token. F-25 likewise overgeneralizes: the unit supplies no explicit creation-mode policy, but that does not prove every file is 0644—`mktemp` files and pre-existing files are counterexamples to such a universal rule. The persisted token body is established by code; universal pinned-client file modes are not established by the supplied lines.

## 2. What runs as root on an unauthenticated port

**A-6 — narrowed**  
Evidence: `raofflineproxy-ctl:440–478,925–955`; `raofflineproxy.service:33–40`; `setsettings.sh:536` as quoted in `03-retrospective.md`.

The readiness predicate unquestionably accepts a foreign wildcard listener and checks neither owner nor protocol. Accepting `0.0.0.0` is reasonable for the narrow question “can an IPv4 connection to loopback reach a listening socket,” but insufficient for “is this proxy ready.” The quoted RetroArch launch check excludes that wildcard address, so the predicates disagree. The first reader’s stronger assertion that this necessarily turns the toggle on is wrong: `enable` still requires `systemctl start` to succeed, and the real service’s competing bind can fail the start. “Every launch goes direct” is also too broad: the complete launch scripts, including other emulators’ routing, are **outside the packet**.

**A-7 — confirmed**  
Evidence: `raofflineproxy.service:26–43`; `raofflineproxy-ctl:279–303`; `storage.py:87–94,117–139`.

The unit adds no privilege reduction, filesystem confinement, capability restriction, resource ceiling, or explicit umask. Under the stated root-everywhere model, this is not a local privilege-escalation finding: another native root process already has substantial equivalent access. It still matters for containment if hostile network data or content compromises this process, because this unit provides no boundary protecting writable storage, credentials, or the award database from that compromised process. No such code-execution exploit is demonstrated here, and effective system-wide restrictions or unit overrides are **outside the packet**.

## 3. A check whose failure reads as success

**A-8 — confirmed**  
Evidence: `raofflineproxy-ctl:490–514,517–527`.

F-06’s open-failure branch is reachable when an existing lock path cannot be opened, and it returns “nothing running” without attempting a signal. There is an additional important qualification: `do_disable` ignores `stop_running_run`’s status entirely, including its explicit timeout failure. Thus changing line 492 to return failure alone would not fix the unsafe continuation. The demonstrated consequence is failure to coordinate shutdown with a live preparation run, not demonstrated SQLite corruption or lost awards.

**A-9 — confirmed**  
Evidence: `raofflineproxy-ctl:1073–1094,1818–1821,1990–1991,2014–2016,2031–2033,2103–2107,2411–2429`.

F-07 is real: callers continue to their preselected result after a stamp-write failure, leaving an older stamp or no stamp. Atomic replacement prevents readers seeing a partially written target; it does not make failed publication observable. There is also a success-shaped failure not covered by merely checking the return code: if `last-scan` is a directory, ordinary `mv` can move the temporary file into it successfully without publishing the intended stamp path. A fix must validate publication at the intended pathname as well as propagate errors.

**A-10 — confirmed**  
Evidence: `raofflineproxy-ctl:1416–1417`; `storage.py:74–94,106–165`.

F-08 is directly established: listing constructs writable `Storage`, whose initialization sets journal mode, creates schema objects, and can add a column. It also invokes metadata indexing and legacy import, although those implementations are **outside the packet**. This is a genuine exception to the read-only description, but not by itself an unauthorized-write vulnerability on this platform.

**A-11 — confirmed**  
Evidence: `raofflineproxy-ctl:2372–2387,2407–2430`.

F-15’s silent-default branch is reachable when the process exits zero but its result is absent, unreadable, differently spaced, or unparsable. The grep requires the exact compact spelling `"type":"result"`, and parsing failure explicitly substitutes three zeros. The `grep | tail` pipeline discards the grep status under ordinary shell pipeline semantics, while its status is not checked anyway. A nonzero process exit is distinguished, but a successful process exit with an invalid result can become “nothing changed,” leaving no new stamp.

**A-12 — confirmed**  
Evidence: `raofflineproxy-ctl:849–852,888–900,2039–2044,2395–2403`.

F-16 is broader than just one pipeline: an unreadable nonempty export receives no fallback, both producer statuses are ignored, and any nonnumeric result becomes zero. The client-count pipeline also loses the first command’s status behind `tail`; even enabling `pipefail` would not help unless the assignment’s status were checked. A failed client that prints a numeric last line can therefore have that number trusted, not merely be converted to zero. This path never calls `cannot_tell`, and its result is subsequently copied into stamps.

**A-13 — new**  
Evidence: `raofflineproxy-ctl:768–793`; compare `raofflineproxy-ctl:582–585,616,746–747`.

There is another concrete `cannot_tell` bypass: a login row containing valid JSON of the wrong type, such as an array, exits 1 at lines 780–781. The shell interprets that as “no account points,” bypassing the unreadable-store handling at line 793, even though malformed JSON in the same row exits 3. Missing score fields in a legitimate token-only object deserve the absence result; a non-object row should not be conflated with that case. The other cited SQL command-status guards do catch a nonzero Python exit, so they should not be accused of the pipeline defect without additional evidence.

**A-14 — confirmed**  
Evidence: `raofflineproxy-ctl:1587,1672–1677,1987–1991`; `raofflineproxy-cache-indexed:148–160`.

F-17 follows from the strict UTF-8 job-file write when a selected pathname contains a surrogate-escaped filesystem byte. The scope is a pathname actually selected into the job list, not every undecodable filename anywhere in the library. The resulting listing failure is reported as `LIBRARY_UNREADABLE`; merely making the writer byte-tolerant would be insufficient because the helper also reads strict UTF-8.

**A-15 — confirmed**  
Evidence: `raofflineproxy-ctl:316,942–944,1933–1938,2433–2453,1727–1764`; `raofflineproxy-cache-indexed:176–211`.

F-18’s two usage conventions are real and reachable, although neither represents success. F-24 is also real: error classification searches the complete line, including the filename, rather than an isolated reason field. `OK` lines are protected by an earlier branch, and an earlier skip pattern can win over the login pattern, so not every filename containing those words produces the claimed refusal. The same flaw can also turn genuine failures into harmless skips or “cache limit reached,” which is more than a misleading sign-in message.

## 4. A bound that is not enforced

**A-16 — narrowed**  
Evidence: `raofflineproxy-ctl:325–337,490–511,1755–1763,2248–2255,939–955`; `raofflineproxy-cache-indexed:71–79,174–175`; `raofflineproxy.service:23–24,40–43`.

The probe row means at most nine probe invocations with at most eight ten-second sleeps, not a ninety-second elapsed-time ceiling; probe execution time is additional. `STOP_WAIT` limits the lock-wait loop to ten sleeps but neither establishes that the run stopped nor prevents disable continuing. Three consecutive failures are enforced for lines reaching the generic `FAIL` branch, and the thirty-second cooldown occurs before jobs 51, 101, and so on. The unit provides thirty readiness looks, five-second restart delay, five starts per 300 seconds, and a fifteen-second stop timeout; “30 + 5” describes that scheduling arrangement rather than an exact duration for every start.

**A-17 — confirmed**  
Evidence: `raofflineproxy-ctl:869–885,2220–2238,2264`.

The half-hour age test deliberately does not suppress a negative age, but the subsequent history comparison still suppresses an ordinary link-return top-up when the mark is in the future. That latter suppression requires no pending-index marker and no `--after-index` bypass; it is not universal across all top-up routes. The unchecked `touch` independently means an attempt can proceed without establishing its future throttle. These are operational defects, not just descriptions of a clock policy.

**A-18 — refuted**  
Evidence: `raofflineproxy-ctl:1135–1149,2196–2206,2248–2255,2279–2282,2445`.

The table’s claim of an enforced 900-second whole-run deadline is too strong. `time_left` uses wall-clock subtraction, so a backward clock adjustment can increase the remaining budget above 900 seconds. The probe subprocess receives neither an enclosing timeout nor the remaining budget, and the deadline is inspected only after a probe returns. There is no outer timeout around `do_topup` in this dispatch, so these mechanisms are not a hard elapsed-time bound.

**A-19 — narrowed**  
Evidence: `raofflineproxy-ctl:1261–1265,1871–1876,1915,1954–1957,1965–1967,1987,2037,2062–2063,2419`; `raofflineproxy-cache-images:308–309,417,468–476`; `raofflineproxy-cache-indexed:82–95,217`; `raofflineproxy-refresh:158–170`.

The scan’s missing total deadline is explicit foreground-operation policy, with cancellation handling, rather than an accidentally omitted top-up limit. The image pass gets 300 seconds in a normal scan, potentially the whole remaining top-up budget, and a 310-second outer timeout for standalone `images`; the connection between the helper’s `budget_end` and later `deadline` assignment is **outside the packet**. Refresh receives a 960-second process wrapper around a 900-second between-game check, after its separate online probe. The 120-second badge wait bounds the displayed thread join, not demonstrably total process lifetime, because `shutdown_image_downloads` is **outside the packet**. These timeout invocations also contain no explicit kill-after escalation.

**A-20 — confirmed**  
Evidence: `raofflineproxy-ctl:843–846,888–897,1711–1713,1876`; `013-validate-a-cached-image-before-publishing-it.patch:70–79,103–125`; `network.py:270–296,299–331,367–394`.

The log threshold is a rotation trigger, not a byte ceiling, and direct helper appends bypass it. Download bodies and IDAT inflation lack size caps in the supplied patch. The resolver’s three seconds bounds a join, not thread count or resolver lifetime; moreover, an unremembered lookup can fall through synchronously to the original resolver, including from direct `http_get` calls. The table’s final `count_ready` row is a failure-semantics issue rather than a resource bound, and its zero fallback is confirmed in A-12.

**A-21 — narrowed**  
Evidence: `network.py:408–420,516–577`; `raofflineproxy-cache-indexed:103–120`; `001-dorequest-4xx-passthrough.patch`, added `handle_online_request` hunk.

F-14 is correct about these two functions: GET records a 429 pause, whereas POST treats 429 as a reachable HTTP error without recording one. The indexed helper also explicitly persists the pause it observes. Patch 001 passes a general-path 429 through, but the complete forwarding call graph and patch 004’s drain implementation are **outside the packet**; “nothing paces the emulator’s next POST” is therefore broader than the supplied evidence establishes.

## 5. Finding-by-finding disposition

**A-22 — F-01: confirmed**  
Evidence: `proxy_service.py:452–507`; `auth.py:108–109,142–143`.

**Severity: Low on the demonstrated device-local/root model**, with a potentially higher confidentiality consequence if the browser reach is established. A stream should require actual credential proof before returning a cached token and define the allowed account scope; Host validation is complementary, not a replacement. Existing `/storage` already contains usable or formerly usable login tokens, and a code update cannot retract tokens previously returned. Provide revocation/re-sign-in handling where exposure is credible without indiscriminately deleting queued awards.

**A-23 — F-02: narrowed**  
Evidence: `proxy_service.py:289–325`; `config.py:376–377`.

The supplied handler lacks Host/Origin checks but does enforce loopback peers. Retain this as a conditional browser-origin concern, not a proven readable DNS-rebinding attack; the missing request-path prefix and browser policy are **outside the packet**.

**A-24 — F-03: narrowed**  
Evidence: `raofflineproxy-ctl:451–478,925–955`; `raofflineproxy.service:33–40`; quoted `setsettings.sh:536`.

**Severity: Low**, for false readiness and inconsistent routing predicates, not proven unconditional successful enablement. Unify the launch/start contract and verify the intended service’s socket or protocol, rather than merely excluding wildcard binds while continuing to accept foreign loopback listeners. Where false readiness previously allowed enablement, the marker, toggle, and hardcore record may persist across an OS update. Reconcile those existing states instead of assuming a new readiness predicate repairs them retrospectively.

**A-25 — F-04: confirmed**  
Evidence: `raofflineproxy.service:26–43`.

Info/defense-in-depth is appropriate absent an exploit. Hardening should constrain the service’s actual required resources and writes, with existing storage ownership considered, rather than treating a different `User=` alone as a complete containment design.

**A-26 — F-05: narrowed**  
Evidence: `raofflineproxy-ctl:616,647,788,1029,1244–1265`.

The four username arguments exist, but the cited rule concerns the listing and is obeyed there. This is not demonstrated secret-credential exposure or a violation of that particular comment’s promise.

**A-27 — F-06: confirmed**  
Evidence: `raofflineproxy-ctl:490–527,1420–1425`.

**Severity: Low**, for failed shutdown coordination. Make lock-inspection failure observable and make `do_disable` act on it; changing only the helper’s return value leaves behavior unchanged. The pre-fix state can already be toggle-off/service-stopped with a preparation helper still working and partially completed cache work retained. Repair coordination and allow preparation to resume; do not purge the store as a substitute.

**A-28 — F-07: confirmed**  
Evidence: `raofflineproxy-ctl:1093–1094,2103–2107,2411–2429`; `CloudText.cpp:1212–1220,1273–1276`.

**Severity: Low**, for reporting success without publishing the run record. Check publication at every call site, reject unsuitable destination objects, and propagate failure through the caller’s result contract. An old `last-scan` and an abandoned temporary file can already survive on devices. Preserve the distinction between that historical result and the latest operation instead of presenting failed publication as a completed update.

**A-29 — F-08: confirmed**  
Evidence: `raofflineproxy-ctl:1417`; `storage.py:87–94,106–165`.

Keep this as an architectural/read-only-contract exception unless initialization during listing is shown to cause damage. A genuinely read-only listing interface would avoid schema and migration side effects rather than merely opening some separate SQL connections with `mode=ro`.

**A-30 — F-09: confirmed**  
Evidence: `raofflineproxy-cache-images:169–177`; `raofflineproxy-ctl:843–846,1711–1713,1876,2366`.

The cursor lacks atomic replacement, and direct log appenders are outside the rotation check. These are distinct issues: cursor damage affects resumption, while unrestricted logging can consume storage; neither is evidence of award corruption by itself.

**A-31 — F-10: confirmed**  
Evidence: `raofflineproxy-ctl:1708–1716`.

The FIFO has a name-reservation race. Because `mkfifo` failure aborts, pre-creating an object before that call does not automatically make the helper write through it; replacement after creation remains a separate race, best removed with a private temporary directory.

**A-32 — F-11: confirmed**  
Evidence: `raofflineproxy-ctl:1965–1967,1987,2037,2062–2063`.

The scan has no total deadline, intentionally. Keep the design observation as Info; the separate problem is any consumer that assumes every run has a bounded lifetime.

**A-33 — F-12: confirmed**  
Evidence: `raofflineproxy-ctl:2220–2238,2264`.

Both the unchecked attempt mark and future-mtime suppression are real. This deserves a Low operational bug, including treatment of already-future marks retained in `/storage`, rather than Info alone.

**A-34 — F-13: confirmed**  
Evidence: `013-validate-a-cached-image-before-publishing-it.patch:72,103–125`; `network.py:299–331`.

Both resource caps are absent. In particular, the newly introduced inflater warrants an availability fix using bounded incremental decompression and input limits—not treating a decompressor’s initial buffer size as a hard bound.

**A-35 — F-14: narrowed**  
Evidence: `network.py:408–409,549–577`.

The missing POST pause is confirmed at the function level. Keep the finding, but do not claim the behavior of every forwarded emulator POST without the missing call graph.

**A-36 — F-15: confirmed**  
Evidence: `raofflineproxy-ctl:2372–2387,2407–2430`.

A zero exit with no valid result can silently become zero work. Treat this as a Low reporting/control-flow bug and require a valid result record, independently of process exit status.

**A-37 — F-16: confirmed**  
Evidence: `raofflineproxy-ctl:888–900,1990,2039–2044,2395–2403`.

**Severity: Low**, for turning an unknown count into an authoritative number. Capture and validate producer status before extracting the count, then propagate unknown/error through every command substitution and stamp consumer rather than only changing `count_ready`. Devices may already retain unreadable exports and stamps containing false zero counts; this function does not repair either. Regenerate or validate exports from the retained store without deleting award data.

**A-38 — F-17: confirmed**  
Evidence: `raofflineproxy-ctl:1587,1672–1674,1987–1991`; `raofflineproxy-cache-indexed:149–160`.

**Severity: Low**, because one selected pathname can prevent preparation of the whole selected batch. Use a byte-safe framed representation end to end, or report and skip the individual unsupported entry; changing only the writer to replacement characters would silently change the pathname. Existing devices retain the problematic filename and the failure stamp, so updating the immutable image alone does not remove the trigger. Retrying with corrected handling should not require renaming user files or clearing cached awards.

**A-39 — F-18: confirmed**  
Evidence: `raofflineproxy-ctl:316,944,1935–1938,2453`.

The inconsistent usage codes are real. This is a contract-consistency issue, not a success-on-failure branch.

**A-40 — F-19: narrowed**  
Evidence: `raofflineproxy-refresh:50–51,166–170,216–227`; `raofflineproxy-ctl:833–836`.

The second `done` field means failed games at normal completion, unattempted games at the deadline, and all unfinished games—including failures—after repeated failures. Unprefixed human notes need not themselves violate a protocol explicitly distinguished by `>>>`; the claim that no interface consumer exists is **outside the packet**.

**A-41 — F-20: narrowed**  
Evidence: `CloudText.cpp:1032–1033,1241–1250`; `raofflineproxy-ctl:1119–1122,2012–2014,2433–2450`.

The visible producer uses `note NO_GAMES`, while the old `NO_GAMES_FOUND` mapping remains. `have_account` is indeed a function rather than a dispatched verb, but the cited settings-page comment is **outside the packet**.

**A-42 — F-21: narrowed**  
Evidence: `package.mk:5–13`.

The “16 patches” comment disagrees with the supplied eighteen-patch inventory. The sibling recipe contents and patches 020/021 are **outside the packet**, and an older explanatory parent-commit date would not by itself prove a coupled pin is wrong.

**A-43 — F-22: narrowed**  
Evidence: `package.mk:12`; contribution-map and draft files: **outside the packet**.

The draft inventory and all draft-base comparisons cannot be independently confirmed from the supplied code. Retain them as reported contribution bookkeeping, not verified runtime findings or proof that patches are ready to submit.

**A-44 — F-23: narrowed**  
Evidence: `raofflineproxy-ctl:247–258`; checker and harness implementations: **outside the packet**.

The source comment describes a schema contract, not an executable validation of it. Accept the supplied run summaries as reported results, but neither comment matching nor a passing sandbox suite establishes coverage of every failure discussed here.

**A-45 — F-24: confirmed**  
Evidence: `raofflineproxy-ctl:1727–1764`; `raofflineproxy-cache-indexed:176–211`.

The filename participates in classification, subject to the earlier-match qualifications in A-15. This should become a structured outcome/reason protocol, not another collection of free-text exclusions.

**A-46 — F-25: narrowed**  
Evidence: `raofflineproxy.service:26–43`; `raofflineproxy-ctl:1094,1979`; `storage.py:87–94`.

The reported cache-directory modes are an observation, not a guarantee for every writer or every existing file. A future umask change would neither change existing `/storage` permissions nor automatically cover helpers launched outside this unit; any mode-hardening stream needs an explicit, non-destructive existing-state migration.

## 6. What the first reader missed

**A-47 — new**  
Evidence: `raofflineproxy-ctl:408–410,420–437,469–479,525–527`; `006-raofflineproxy:7–10`.

The writers table and retrospective are wrong to say rollback setting writes are each read back: `put_back` does no readback, and `enable_undo` ignores its results. A failed forward step followed by a failed rollback can therefore leave changed settings despite the claimed “as if enable never ran” guarantee. Service-stop failure is also deliberately swallowed before disable continues. Such inconsistent settings can survive an image update and be used again by boot reconciliation, so the stream needs verified rollback or an explicitly reported partial state.

**A-48 — new**  
Evidence: `raofflineproxy-ctl:2137–2157,2163–2181,2345–2351`.

The pending-marker lock is not a complete serialization boundary because writers proceed without it using one shared temporary pathname. Concurrent fallback writers can interfere with that temporary file, undermining the “whole or not at all” claim. Independently, acknowledgement unconditionally removes its aside file after attempting restoration, even if restoration failed, yet returns the value the caller describes as “kept.” Use safe concurrent publication and distinguish retained, removed, and failed-to-restore states; do not delete the only retained notification after a failed restore.

**A-49 — new**  
Evidence: `raofflineproxy-ctl:1672–1674,1730–1735,2046–2059`; `raofflineproxy-cache-indexed:149–163,196–211`.

The job format also fails on otherwise valid pathnames containing newline or other characters recognized by Python’s `splitlines`. Such a pathname is split into separate records, malformed fragments are silently skipped, and the remaining fragment can be reported as an ordinary missing-file skip. The worker can consequently finish cleanly without doing the intended job, while the ctl neither reconciles completion counts against its planned jobs nor requires `DONE` when the process exits zero. This needs framed pathname transport and validated completion, not just the UTF-8 repair in F-17.

**A-50 — new**  
Evidence: `013-validate-a-cached-image-before-publishing-it.patch:44–51,103–125`; `raofflineproxy-cache-images:128–154`.

Patch 013’s `+` side introduces the unbounded inflation operation: before it, publication did not allocate the decompressed image. Its new validator also never requires an IHDR, legal chunk order, dimensions, or a matching decompressed image layout. CRC-correct, inflating IDAT data followed by IEND can therefore pass without constituting a valid PNG. Fix both the resource limit and structural validation, then re-verify existing cached files rather than assuming new-download checks repair previously published entries.

**A-51 — new**  
Evidence: `proxy_service.py:268–278,298–303`.

The request-body limit fails for negative `Content-Length`. A negative integer passes the upper-bound comparison and is truthy, so it reaches `rfile.read` as a negative size—an unbounded read until EOF rather than a capped body read. The socket timeout is not a total byte limit against a continuously transmitting peer. Reject negative and malformed lengths before reading; this is a real bound defect even though the shown peer check restricts its direct reach to loopback.

**A-52 — new**  
Evidence: `raofflineproxy-ctl:1851–1857,2361–2390,2410–2430`.

Required work can be skipped without becoming a failure. A missing executable image helper returns success with no image-failure reason, and a top-up with fewer than sixty seconds left simply omits its recently-played pass without setting `TOOK_TOO_LONG`. In the latter case, if nothing was cached earlier, it can exit zero without a new stamp despite never examining that work. Distinguish deliberate “nothing due” decisions from unavailable or unattempted required phases.

**A-53 — new**  
Evidence: `raofflineproxy-cache-images:145–156,267,333–343,425–426,452–465`.

A damaged image that cannot be unlinked can still be counted as present by the later presence-based accounting. The unlink error is only logged, while success ultimately depends on the missing-file set and remaining verification slice. This permits a pass to finish successfully with a known damaged file retained, and the final message can describe damaged files as “re-fetched” without proving that outcome. Track failed removal/replacement as an unresolved image failure, separately from mere existence.

**A-54 — new**  
Evidence: `raofflineproxy-ctl:827–830,1720–1723,1771–1774,1985–1987,2037,2062–2063`; `CloudText.cpp:1335–1343`.

The running-state protocol contradicts the intentional unbounded scan design. The parser rejects an old progress timestamp on the premise that the ctl bounds its runs, but listing and an individual scan job can run indefinitely without refreshing that timestamp. A live scan can therefore parse as not running; the numerical stale threshold and higher-level UI decisions are **outside the packet**. Add independent liveness/heartbeat handling rather than imposing an accidental total scan deadline merely to satisfy this parser assumption.

**A-55 — new**  
Evidence: `raofflineproxy-ctl:2224–2238,2264,2372–2387`; `013-validate-a-cached-image-before-publishing-it.patch:103–125`; `storage.py:125–139`.

F-12 and F-15 should move from Info to Low bugs: they respectively suppress required work and accept an invalid result as no change. F-13 also deserves an availability-fix disposition rather than being treated only as efficiency commentary, although a higher attacker-driven severity needs reachability evidence **outside the packet**. Finally, “no finding loses an award or a save” is stronger than this coverage supports: no such loss is demonstrated, but the complete queue/flush and persistence behavior needed to exclude it is **outside the packet**.
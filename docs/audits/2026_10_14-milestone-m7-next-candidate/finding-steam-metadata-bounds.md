# Candidate finding: Proton release metadata has no deadline

Frozen distribution fac608ff89940ce358ea9b8a95e9a08a6fe26568. Independent source observation; no runtime reproduction dispatched by auditor.

**Severity:** Medium (installer can remain waiting indefinitely). **Criterion:** #580 / AC083, explicit time bounds. **Source:** projects/ROCKNIX/packages/virtual/emulators/sources/Install Steam.sh:213, callers2748 and2750.

The full installer invokes fetch_proton_latest_release after the bounded FEX/runtime/client helpers return. Its curl -fsSL metadata request has neither connect nor total deadline nor response-size bound. A server that establishes a connection and stalls can leave this installer waiting indefinitely. The helpers’ Python alarms exist in exited child processes and cannot bound this request. This is an inherited upstream request within the changed installer and the explicitly audited full-caller transaction boundary. Failure occurs before Proton stage activation; no destructive-state claim is made.

Refutation: inspected caller and beginning of installer; no global timeout is set. The existing helper deadlines protect their own children only. The exact local shell option request does not establish a download deadline. A retained curlrc can alter behavior, so this path cannot depend on a user’s configuration to provide a bound.

Minimal source correction proposal (root integrates):

```diff
-  release_json=$(curl -fsSL "${api_url}") || die "Failed to fetch ${display_name} latest release info."
+  release_json=$(curl -q -fsSL --connect-timeout 10 --max-time 30 --max-filesize 1048576 "${api_url}") || die "Failed to fetch ${display_name} latest release info."
```

Put -q first to bypass retained curlrc for this defined metadata transfer. Keep current failure message, parser, caller order, no retry/fallback change. A one MiB response limit is a proposed metadata bound, not a measured normal maximum; root should check retained successful metadata size before accepting that value.

One bounded regression proposal: invoke the actual source function against a controlled local endpoint that accepts the request and never completes the body. Test the changed function with its real curl, preserving current production flags; a wrapper may rewrite only the URL to local HTTP, with the exact adaptation recorded. Assert nonzero return and original failure message within35seconds, no Proton activation, unchanged existing family bytes/types, and endpoint/client cleanup. Keep fullcaller installed evidence separate from the narrow function control. If adapting a fullcaller fixture instead, retain all original metadata/caller bytes and replace only the network route. No need to repeat accepted unrelated cases.

No patch has been applied to the frozen product. External review has not run.

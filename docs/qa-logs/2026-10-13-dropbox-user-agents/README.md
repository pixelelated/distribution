# Actual Dropbox authorization: user agents — October 13, 2026

[#570](https://github.com/pixelelated/distribution/issues/570). Eight completed
account-free VM trials load actual rclone authorization at
`www.dropbox.com/oauth2/authorize`. The earlier public `/login` tests and local
synthetic controls did not cover this exact provider entry point. The owner's
request and VM-first scope are in [plan.md](plan.md).

## What changed, and what did not

Diagnostic-only browser copy from accepted source `bc9dfe8141d9`, exact source,
patch and compiled hash retained. The running engine is WebKit2.54.1 for every
identity; advertising Chrome does not run Chromium. Installed broker, actual
rclone and normal ES launch/wait/return are preserved. Old synthetic broker was
cancelled and its real rclone executable restored. Its already displayed QR is
setup-only, not proof of the new PIN; no phone connected to either session.

Same VM as the preceding handoff packet:1280MiB assigned/1042.6MiB visible,
four virtual CPUs, software renderer,640×480 panel,640×457 CSS page, no proxy
account/background service. Each launch gets a fresh ephemeral browser.65second
budget, original100MiB available-memory guard, per-second PSS/kernel sampling.
The order is handset/desktop/iPad/Android, then reverse. No login submitted,
identity-provider button pressed or cookie banner dismissed. These are initial
unauthenticated landing-page controls, not completion of authorization.

The observer adds a100ms top-frame heartbeat and at most one pending2second
JavaScript evaluation. Its round-trip latency measures page-process availability,
not touch-to-paint. Resource counters include subframes; performance resource
entries expose only eligible top-document timing and are TAO-limited. Summed
response content lengths are **not measured total network bytes**. The observer
cost is common to cases but is not independently quantified.

## Results

| Identity / repeat | Load event (ms) | Longest heartbeat gap (ms) | Longest evaluation (ms) | Peak browser PSS (MiB) |
| --- | ---: | ---: | ---: | ---: |
| Current handset1 | 1341 | 1931 | 748 | 485 |
| Current handset2 | 1009 | 5079 | 2190 | 490 |
| Desktop1 | 892 | 538 | 71 | 487 |
| Desktop2 | 1018 | 590 | 82 | 474 |
| iPad1 | 1012 | 7880 | 1843 | 457 |
| iPad2 | 1058 | 9127 | 3516 | 472 |
| Android Chrome1 | 982 | 2092 | 1729 | 505 |
| Android Chrome2 | 1515 | 636 | 65 | 511 |

All eight reached the real authorization page, retained the same boot/frontend
and returned normally; no guard fired. Desktop was most consistently responsive
in this small sample. Memory remains high for every identity; this is not a
memory fix, statistically established ranking or proof of usable login on H700.
The iPad identity was worse in both samples. Initial load-event time alone misses
later stalls. [Analysis](analysis.json) retains exact values and counter deltas;
compressed samples and page-metrics retain the observations.

**The provider really changed its scripts.** The effective current UA identifies
as `Linux; like Android 4.4 ... Version/60.5 Mobile Safari/605.1.15`. Both handset
trials select `oauth2_authorize_page_rspb_fallback` assets. Desktop, iPad and Android
select `oauth2_authorize_page_rspb_modern`. [Script sets](script-sets.json) preserve
actual host/path identities without queries. This supports user-agent-dependent
content delivery, not a causal claim that fallback explains all stalls. Modern
bundles alone did not prevent the iPad/Android pauses. No production UA, chassis
setting or engine pin has changed.

## Visual and source evidence

All eight60second native frames were reviewed: the real Dropbox/rclone heading
and cookie overlay, not a browser-error substitute. One Android frame has a
different scroll position. The untouched cookie overlay obscures the email field;
`geometry_email_field` means a positive-width enabled email input, **not** unobscured
interactive readiness (height and viewport intersection are not checked). Twelve-second/return frames are retained in the
[index](frames/index.json), but are not all individually reviewed.

[Channels](channels.json) bind compiler/matrix launcher, wrapper and runner0 and
host-process exits. The diagnostic binaries are not firmware. The subsequent [CSS-width screen](../2026-10-13-dropbox-breakpoints/README.md) is
complete. Its [retirement receipt](../2026-10-13-dropbox-breakpoints/retirement.json)
covers all 22 trials; the shared disposable guest and its disk/keys are retired. Fixtures are archival inputs with explicit
private-owner/port dependencies, not a self-contained one-command replay tool.

Upstream check October13: Dropbox's official
[authorization documentation](https://www.dropbox.com/developers/documentation/http/documentation#oauth2-authorize)
identifies this as the authorization endpoint; rclone's
[v1.75.2 provider source](https://github.com/rclone/rclone/blob/v1.75.2/backend/dropbox/dropbox.go)
uses it. Official Dropbox forum reports describe webview compatibility limits;
no matching performance fix was established. Earlier engine/release research
remains in the WebKit-versions packet. Actual field/navigation/redirect/popup
compatibility and physical confirmation remain open before selecting a fix.

The original unified diff is retained byte-for-byte in `fixtures/diagnostic.patch.gz`;
`diagnostic-patch.json` binds its uncompressed hash. The frame-index name refers
to that original diff. This preserves patch context while avoiding a source-file
whitespace-lint interpretation of blank diff context lines.

# Normal browser handoff and phone controls — October 13, 2026

[#570](https://github.com/pixelelated/distribution/issues/570). Six completed
VM controls use the real accepted cloud_oauth/browser/ES path, with only rclone's
authorization redirect replaced by a fixed local page. The provider content is
synthetic, not Dropbox; passing this comparison does not resolve the reported hang.
No product code or owner device/account changed.

## What ran

Can this be done on the VM? Yes; recorded before execution in
[the issue](https://github.com/pixelelated/distribution/issues/570#issuecomment-6137795383).
Accepted VM20 source `1a026648442321609b2288c2c9c06803817f9df2`, ES
`c8dc72cf9ec00ab00d6c4a9fcdcea1746c6f1f78`; exact installed hashes in
[installed-readback.txt](installed-readback.txt). Four virtual CPUs, software
rendering, 640×480, 1280MiB assigned and 1067648KiB visible. This is about68MiB
more visible RAM than the H700 bench. No proxy account/background proxy service;
this does not match the populated handheld's complete background load.

Every case selects phone keyboard policy, so actual phone presence is isolated
from on-screen keyboard/viewport policy. None: no phone client. Idle: actual
REMOTE_PAGE polls in host Chromium at390×844. Active: same page types64 lowercase
characters and drags through30 pointer events on each of four pages. The fixed
page touches80MiB and navigates every20seconds. Each case observes75seconds after
initial load, then normal browser exit and ES return. The repeated order is
none/idle/active/active/idle/none; fresh browser contexts, same boot/frontend.

[Fixtures](fixtures/) preserve the actual scripts. [Samples](samples.json.gz)
contain per-second PSS/CPU/memory/reclaim observations for all processes; sampler
cost is at most30ms. [Events](events.jsonl.gz) and
[phone requests](phone-requests.json.gz) contain only synthetic input and timing.
[Analysis](analysis.json) is computed from those observations. Requests record
POST issuance and acknowledgement, not the original DOM gesture timestamp;
page input events are not a pixel-paint timestamp.

## Outcomes

| Case | Initial load (s) | 100ms heartbeat p95 / maximum (ms) | Peak browser PSS (MiB) | Minimum available (MiB) |
| --- | ---: | ---: | ---: | ---: |
| None1 | 0.80 | 104 /155 | 458.0 | 179.0 |
| Idle1 | 1.10 | 104 /213 | 386.2 | 249.2 |
| Active1 | 2.91 | 105 /143 | 475.4 | 172.2 |
| Active2 | 1.41 | 104 /149 | 472.4 | 174.1 |
| Idle2 | 1.71 | 104 /145 | 473.6 | 185.6 |
| None2 | 2.32 | 104 /319 | 473.9 | 181.0 |

All six reached all four pages. Active trials applied all64 characters on every
page; POST-to-acknowledgement was2.20–2.22seconds, consistent with the existing
34ms-per-character injection pacing. The next movement POST follows typing's
acknowledgement, confirming queue serialization. Precise gesture-to-pointer
latency was not instrumented. No typing/page freeze resembling the reported
crawl occurred. Resource variation across sequential trials is not a causal
ranking of phone modes; the second pass's memory peaks are very similar.

The guard did not fire, but file-page reclaim/refaults and direct scans did occur.
Same boot `5f507670-bab1-4cd9-9803-f0a1fbbdcf1e` and ES PID1630 throughout; real
cloud_oauth wait was sampled in every trial. Browser children were absent from
final samples and available memory recovered. ES remained resident while its
resources were unloaded/reinitialized. This is not a proof that the whole stack
is pressure-free or that Dropbox's live content is equivalent.

## Frames, failures and custody

[Reviewed frame index](frames/index.json) binds native640×480 page and normal
return/QR frames. No ES presentation changed. The phone screenshot taken after
browser close says “Not open yet”; it is not used as connected-state proof.

Before measurement, a synthetic server had a non-daemon timer keeping it alive
after shutdown; original owner/build137 is retained, not recast as success from
its inner close result0. A placeholder replacement defect was caught before any
measured page used it. Corrected server02 is the consumed fixture. The initial
VM's QR screen also needed explicit compositor focus; input had reached the
guest but not ES. An early wait-for-change caught a startup overlay rather than
the completed keyboard-choice screen. Those unmeasured setup frames/failed page
are excluded from results. This is setup repair, not a shipped focus fix.

[Channels](channels.json) retain original boot/server/matrix results and actual
host process exits. Matrix launcher/wrapper/build are all0. The VM was reused
immediately for the separately tracked real Dropbox/user-agent comparison;
its eventual retirement receipt covers both experiments. No full firmware build
or external audit ran. The requested [actual authorization user-agent comparison](../2026-10-13-dropbox-user-agents/)
has since completed. Separate CSS-width controls are the immediate follow-up,
then focus/background-load and the earlier-engine boundary as evidence warrants. #570 remains open.

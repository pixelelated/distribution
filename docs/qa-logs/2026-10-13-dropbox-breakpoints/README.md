# Dropbox CSS breakpoint controls — October 13, 2026

[#570](https://github.com/pixelelated/distribution/issues/570). Eight completed
account-free trials use actual rclone Dropbox authorization, two user agents and
four CSS widths. [Plan](plan.md), [exact analysis](analysis.json), [script paths](script-sets.json).

## Result and limits

No consistent memory or responsiveness improvement from a narrower layout was
established. This is one observation per cell, a screening experiment rather than
a statistical ranking. All eight loaded the actual page, retained the same boot
and frontend, returned normally and avoided the memory guard. Significant reclaim
and file refaults remain. Initial load is not a measure of subsequent usability.

| Case / CSS width | Load (ms) | Max heartbeat gap (ms) | Max evaluation (ms) | Peak browser PSS (MiB) | Min available (MiB) |
| --- | ---: | ---: | ---: | ---: | ---: |
| desktop360 | 987 | 917 | 239 | 507 | 149 |
| handset768 | 2545 | 1194 | 347 | 505 | 127 |
| desktop480 | 2443 | 1875 | 450 | 459 | 156 |
| handset640 | 1223 | 4073 | 1235 | 479 | 144 |
| desktop640 | 1143 | 561 | 99 | 515 | 152 |
| handset480 | 1138 | 682 | 215 | 490 | 132 |
| desktop768 | 1362 | 1638 | 424 | 500 | 154 |
| handset360 | 2117 | 3976 | 2783 | 466 | 137 |

The order shown is the execution order. WebKit page zoom is 640/requested-width,
with the same physical 640×480 framebuffer. Observed CSS dimensions are 360×257,
480×342, 640×457 and 768×548; device-pixel ratio also changes to about 1.778,
1.333, 1 and 0.833. `screen.width/height` remain 640×480. This varies responsive
layout, CSS height and DPR together; it is not a physical mobile screen comparison.
The observer asserts requested/actual width within one CSS pixel and records
max-width:480px/min-width:768px queries. All handset cases still use fallback
Dropbox bundles and all desktop cases modern bundles, regardless of these widths.

Same WebKit2.54.1/GTK3 diagnostic copy, actual broker/rclone and normal ES handoff
as the preceding [UA comparison](../2026-10-13-dropbox-user-agents/README.md).
Same guest boot, four virtual CPUs, software graphics and 1042.6MiB visible RAM;
no proxy account/service or actual phone client. Each ephemeral launch has a
65-second budget and a 100MiB available-memory guard. No credentials entered,
provider login submitted or cookie banner dismissed. Common observer overhead
is not independently measured. Content-length sums are not actual transferred
network bytes, and cross-origin resource sizes are limited by Timing-Allow-Origin.
Resource completion counters include failures; individual-script execution cost
has not been attributed. Heartbeat/evaluation delays are not input-to-paint latency.

## Evidence and retirement

All eight 60-second native frames were reviewed: real Dropbox/rclone content and
the untouched cookie overlay, which obscures the form. Narrow layouts stack banner
buttons differently. `geometry_email_field` asserts only an enabled positive-width
input, not height, viewport intersection, absence of occlusion or usability.
Twelve-second and return frames are retained but not all individually reviewed.
[Frame index](frames/index.json) binds hashes/dimensions. [Source](source.json),
[diagnostic binary hash](binary.sha256), patch/fixtures and compressed numeric/page
observations bind the experiment. Fixtures retain private-owner and port dependencies;
they are archival inputs, not a self-contained replay command.

[Completion channels](channels.json) verify compiler and matrix launcher/wrapper/
runner exits 0 and actual owner exits. Matrix completion was 05:05:04 UTC.
[Retirement](retirement.json) binds all 22 results: six synthetic phone cases,
eight actual authorization UA cases and these eight breakpoint cases. Original
browser and rclone were restored, no browser children remained, and the exact
owned VM process was stopped before removing its disk, firmware variables and
keys. Measured allocated recovery: **2,362,486,784 bytes**. The VM is no longer
available; do not reuse its old PID/ports or replay a boot owner over old artifacts.
This is diagnostic evidence, not a full VM suite, product fix or candidate acceptance.

Next: correlate page/script execution with CPU and reclaim; prepare the separate
[#576 GTK4 experiment](https://github.com/pixelelated/distribution/issues/576) and
service-footprint control. Keep runtime comparisons serialized and preserve
sign-in, offline achievements and next-game readiness. See
[parallel lane ownership](../2026-10-13-dropbox-user-agents/parallel-lanes.md).

The original unified diff is retained byte-for-byte in `fixtures/diagnostic.patch.gz`;
`diagnostic-patch.json` binds its uncompressed hash. The frame-index name refers
to that original diff. This preserves patch context while avoiding a source-file
whitespace-lint interpretation of blank diff context lines.

# Browser memory isolation — October 12, 2026

Issues [#570](https://github.com/pixelelated/distribution/issues/570) and
[#572](https://github.com/pixelelated/distribution/issues/572). Diagnostic evidence,
not candidate qualification or a production fix.

## Finding

The public Dropbox login page alone reproduces substantial memory pressure on the
H700 RG SP DDR3. The bounded physical probe stopped at 34 seconds when available
RAM fell below its 160 MiB guard, before attempting a hang. The WebKit page process
accounted for about 430 MiB PSS, mostly anonymous memory. After closing the probe,
available RAM recovered to 572 MiB and the same EmulationStation process remained.
The phone bridge, authenticated navigation and owner credentials were not involved.

This establishes a demanding page/engine workload on the actual hardware. It does
not establish which engine change introduced it, a memory leak, or the complete
failure mechanism behind the earlier forced reset. No older WebKit engine was run.

The missing GStreamer controller library and plugin scanner are independently
confirmed packaging failures. Supplying them clears the plugin errors but does
not materially reduce this workload's memory use. They need a source/package fix
under #572; the diagnostic injection is not that fix.

## Source and historical comparison

[manifest.json](manifest.json) binds the accepted VM/device sources, exact browser
source and compiled diagnostic payloads. All runtime experiments use WebKit 2.54.1
and GStreamer 1.29.2. The September 29 browser application was compiled against the
same current engine, so its control isolates application code, not engine version.

- October 9 source `8b5113fa164ada7d002ab138b1e3a9bf795e9de5` and accepted device
  `bc9dfe8141d9561dc1d8502313d00a84c4566ee8` have the same WebKit recipe and handset
  setting. Later application changes concern popups, allowed hosts, backspace and
  the focused-view probe. No initial-page memory improvement appeared with the
  older application in this matrix.
- WebKit 2.54.0 changed to 2.54.1 at `3d7c075f63277506dffb65c41f23d23c14775faf`
  on October 2. GStreamer 1.29.2 predates that change. The source archive comparison
  is retained in [engine-source-diff.json](engine-source-diff.json) and
  [engine-changed-files.json](engine-changed-files.json). Graphics and process
  changes are leads for a runtime bisect, not causal evidence.
- #228 previously found a DMABuf memory problem; the mitigation remains in the
  accepted source. [installed-renderer-env.json](installed-renderer-env.json)
  verifies `WEBKIT_DISABLE_DMABUF_RENDERER=1` in this VM's installed browser children.
  The incident handheld environment was not captured. The old 246 MiB Dropbox
  baseline was a failed page, later corrected in #228; it is not a healthy control.
- October 5 loaded public-login VM evidence already reports roughly 379–386 MiB
  summed browser RSS. Those figures use RSS rather than this matrix's PSS and are
  not directly interchangeable. They show the heavy initial page predates the
  latest firmware, not that every earlier build behaved identically. The owner's
  earlier responsive build is not source-bound.

## VM experiment

Can this be done on the VM? Yes for source, user-agent, cache, synthetic navigation,
plugin and renderer comparisons. Actual H700 working set and recovery are a named
physical limit; the owner separately authorized bounded WebKit tests.

The disposable VM uses accepted replacement20, a 16 GiB disk, four Haswell CPUs,
1024 MiB assigned RAM, and 640×480 output. Guest MemTotal is 810372 KiB (791 MiB),
versus 998120 KiB (975 MiB) on the H700. Guest PSI is unavailable. Browser launches
leave ES resident and use `--no-auto-keyboard`; these are matched direct launches,
not the normal ES renderer suspension or phone-control handoff. The first eight
cases use software graphics. The last uses verified virtio-gpu-gl-pci and
EGL headless with the host render node.

Three-second samples retain browser PSS/RSS and memory composition in
[vm-samples.json](vm-samples.json); aggregates are in [vm-summary.json](vm-summary.json).
PSS apportions shared pages, avoiding RSS double-counting across browser processes.

| Case | Duration (s) | Peak browser PSS (MiB) | Minimum available (MiB) |
| --- | ---: | ---: | ---: |
| Installed browser, public login | 150 | 383.5 | 58.3 |
| September 29 application, current engine | 150 | 391.5 | 56.8 |
| Desktop user agent | 120 | 380.1 | 71.1 |
| DOCUMENT_VIEWER cache model | 120 | 393.6 | 48.9 |
| Synthetic navigation, default | 75 | 393.3 | 57.1 |
| Synthetic navigation, DOCUMENT_VIEWER | 75 | 390.8 | 55.4 |
| Synthetic navigation, focus polling disabled | 75 | 394.0 | 52.5 |
| Public login, missing GStreamer payload supplied | 150 | 389.1 | 57.0 |
| Public login, accelerated VM graphics | 150 | 391.0 | 69.4 |

All nine workloads reached the expected loaded page and produced reviewed frames.
That is not a responsiveness or login acceptance result. None of these controls
shows a useful memory reduction. Each is one sequential trial against live provider
content, with different run lengths and no cold boot between the first eight cases;
small numeric differences cannot be treated as causal effects.

The synthetic fixture touches an 80 MiB array on each of four pages, navigates
forward three times at 16-second intervals and sends a one-second heartbeat.
All three variants reach page 3. Maximum within-page heartbeat gaps were 4.60 s
(default), 5.75 s (cache change) and 1.08 s (focus polling disabled). This is a
latency lead requiring repeated, reordered trials and real input tests; it is not
proof that removing the focus probe is safe or fixes the memory pressure.
[Heartbeat aggregates](heartbeat-summary.json) retain the distinction. No input
was injected and back/popups/authenticated navigation were not exercised.

Five-second teardown snapshots sometimes still contain a WebKit child. That
observation alone is not a leak: engine shutdown can wait longer, and remaining
identified QA processes were terminated before the next case. No browser or guest
process survives final retirement. The live-data mapping identifies anonymous
memory, not specifically JavaScript heap versus native allocations.

## GStreamer failure and supplied-payload control

The generic GStreamer post-install hook deletes libgstcontroller; the fork enables
OpenGL plugins that require it. `tools=disabled` also prevents the upstream helper
build, leaving the configured `/usr/lib/gstreamer-1.0/gst-plugin-scanner` absent.
[Archaeology](gstreamer-archaeology.txt) retains the source search.

[Fresh-registry controls](gst-controls.json) show the installed OpenGL plugin fails
with exit 1 and a missing-controller error. Supplying the retained target library
and a helper compiled from the exact GStreamer source produces exit 0, loads the
OpenGL plugin and registers appsink/glupload. The following browser run reports
no GStreamer warnings but remains memory-heavy. All supplied files lived only in
the disposable guest; neither the recipe nor accepted firmware was modified.

Next #572 work: keep the required runtime library in the ROCKNIX override, build
and install the scanner at its configured path, and prove the actual package
install with fresh-registry failure/success controls. Keep unrelated upstream
trimming decisions scoped. Run pkgcheck and qualify installed dependency closure
in the next assembled clean/retained image before closing the issue.

## Bounded physical confirmation

The device reported H700 RG SP DDR3; retain that identity rather than treating its
frame as a generic RG35XX SP benchmark. It ran accepted source bc9dfe8141 with no
other browser/game at preflight. The owner explicitly authorized WebKit testing;
launch/capture/cleanup ran through `tools/device-act`. No account configuration,
cloud transfer, injected input or reboot occurred. Native compositor frames are
720×480, distinct from the VM's 640×480 frames.

The sampler checked every two seconds and stopped for available RAM below 160 MiB
or PSI some avg10 above 8. It ran example.org for 35 seconds, then a public login
probe intended for 90 seconds. [handheld.json](handheld.json) omits device/account
identifiers and retains memory/process samples.

| Case | Observed end | Peak browser PSS | Minimum available | Available after close |
| --- | --- | ---: | ---: | ---: |
| Simple page | Duration, 35 s | 134.5 MiB | 521.6 MiB | 564.2 MiB |
| Public login | Memory guard, 34 s | 501.8 MiB | 152.6 MiB | 572.2 MiB |

The final public-login page process accounts for 430.4 MiB PSS (371.9 MiB anonymous),
versus 66.7 MiB PSS on the simple page. The same boot and ES process survived,
all probe browser processes exited, and the temporary test tree was removed.
These numbers cannot be directly equated with x86 VM consumption: architecture,
panel dimensions, kernel reserve and graphics differ.

## Reproduction, evidence and remaining boundary

[frames.json](frames.json) binds 11 reviewed frames: nine VM endpoints and two
physical public pages. They are diagnostic evidence, not new canonical ES flow
baselines. No private sign-in contents are present.

The two diff JSON envelopes preserve the exact UTF-8 patch bytes and their SHA256;
extract their `diff` field when applying or inspecting a patch. This avoids treating
unified-diff blank context lines as whitespace errors in the containing record.

The `fixtures/` directory preserves the executed VM samplers and orchestration.
These are run-bound evidence, not a portable command to replay in place. Recreate
in a fresh private owner, verify the source/image hashes, generate a new guest key
and provision SSH using the canonical VM tools. `boot.py` refuses an existing disk;
`lowmem-vm.py` changes only the canonical profile's RAM. Reconstruct current browser
C from the device source and extract and apply the `diff` field in `fixtures/instrumentation-diff.json`; reconstruct historical
C from the full manifest commit. Compile using `compile.sh` against replacement20's
read-only sysroot mounted at its original `/workspace/repos/rocknix.worktrees/m7-pixelelated`
prefix, with the private owner mounted as `/work`. `compile-gst.sh` uses that same
sysroot and exact retained GStreamer helper source. Do not mutate the frozen cache.
Provision the compiled binaries and guest sampler, then run matrix, GStreamer
follow-up and graphics comparison sequentially under separate `tools/watch-build-submit`
owners. Their predecessor-result checks intentionally require consumed results.
The physical script stays in private incident evidence; it is not a general device
testing tool. Any future physical action remains within applicable named authority.

[consumption.json](consumption.json) records original terminal results and actual
launcher exits. Two preparation errors (unsupported `--qa`, and a simultaneous
worktree monitor lock) stopped before workloads, remain rc2 and were corrected
using fresh owners. All five executed owners returned 0. No audit or firmware build
ran. [retirement.json](retirement.json) records the stopped guest, removed disk,
UEFI state and keys (2,247,143,424 allocated bytes), and physical probe cleanup.
Private originals: `/workspace/tmp/pixelelated-browser-isolation-20261012/`.

The next discriminating experiment is a source-bound older-engine comparison,
followed by repeated navigation/input/normal ES-handoff tests with memory and
recovery criteria. No usable older engine runtime was found in the inspected
retained inputs; an isolated package build is needed. Do not choose an engine
downgrade, cache setting, polling removal or process limit from these single runs.
The previous page-load checks missed the low-memory usability boundary; #570 stays
open for the measured repair and regression guard. #572 stays open for the real
packaging repair. Existing #565–#567 and #571 work and the stable20261001/build/
publication gates remain in the milestone's order.

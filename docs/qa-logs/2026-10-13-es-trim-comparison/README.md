# Actual allocator candidate: constrained memory and repeated handoff

Issue #570. The exact ES candidate `f7b71db0a` from the preceding
[compiled-source packet](../2026-10-13-es-trim-product/README.md) reduces
EmulationStation anonymous memory by about **78 MiB** in this bounded VM
comparison. No interposer or modified browser is used. The distribution pin
remains unchanged; this is component evidence, not a new release candidate.

## Comparison

One accepted VM20 boot, four virtual CPUs, 1280 MiB assigned / 1067652 KiB
visible RAM, 640×480 and software graphics. QEMU's actual argv is retained;
there is no separately measured GL_RENDERER string. The guest log contains
EGL fallback warnings. This profile deliberately matches the earlier memory
diagnostic, not the standard hardware-rendered UI acceptance profile.
Actual current-boot rocknix-autostart success and frontend idle were required.

Normal ES cloud setup opens the actual unauthenticated Dropbox page using
the unchanged installed broker, rclone and browser. The cookie overlay is
untouched; no account, phone client, entered credentials or completed login.
Fresh ES sessions alternate baseline/candidate/candidate/baseline on one boot.
Every accepted workload verifies the actual executable hash and PID/start.

| Case | Original result | Browser observation | ES anonymous median, 2–6 s | Minimum available |
| --- | --- | --- | ---: | ---: |
| Baseline 1 | 1, memory guard | stopped at sampled +9.07 s | 114596 KiB | 159456 KiB |
| Candidate 1 | 0 | full 60 s, reviewed page and normal return | 34236 KiB | 218212 KiB |
| Candidate 2 | 0 | full 60 s, reviewed page and normal return | 34408 KiB | 234596 KiB |
| Baseline 2 retry | 1, memory guard | stopped at sampled +8.06 s | 113812 KiB | 160608 KiB |

The early common window was chosen after the first guard stop; it has three
samples per baseline and four per candidate. Median difference 79882 KiB
(78.01 MiB), pairwise range 77.54–78.48 MiB. The two candidate settled 10–55 s
anonymous medians remain 34240/34420 KiB. Whole-case minima and browser
peaks have unequal observation lengths and are not a speed or browser-memory
efficiency comparison. One boot, live provider variability and few cases
limit generalization. The guard prevents the severe incident being replayed.
Run `python3 analyse02.py` to reproduce the comparison from original archives.

## Repeated use

Three additional 25-second launch/close/reopen cycles keep ES PID10857, its
start identity and the same boot. All three display the provider page and
return; sampler/result0, no memory guard. Anonymous medians in each cycle's
5–20-second window are 33784/34552/35164 KiB, with minimum available229108 KiB.
This short observation does not establish long-term leak freedom.

The first two immediate return captures are black and explicitly rejected.
The later frontend frames after dismissing the result modal show the correct
QR/Continue page; the third return and final settled frame show STILL WAITING.
The frame index records19 reviewed captures:11 public, six accepted private
and two rejected private. Private copies retain temporary QA pairing frames.
No source, screen content, row order, screenshot mask or canonical baseline
is changed by these tests.

## Original failures and fixture correction

The first report submission refused2 because the publication watcher still
owned the coordinator. A relative submitter invocation then failed127 before
a launcher existed; the absolute-path submission in isolated scratch passes.
These are setup attempts, not runtime evidence.

The first reverse baseline refused1 before opening the browser: its hash was
still the candidate. `mountpoint -q` missed a file bind on this image; shared
mount propagation overlaid the source paths too. No baseline file bytes were
rewritten. Exact owned mountinfo cleanup restored both original hashes, then
the fresh retry made the new bind private and reproduced the guard. Original
refused case and both original scripts are retained. Actual candidate hashes
were verified for both earlier positive trials; their identities remain valid.
The first analyzer also refused the incomplete case (missing launch timestamp);
`analyse02.py` records it separately instead of manufacturing sample data.

## Consumption and remaining scope

All 10 submitted owners are consumed: nine created watched runs and one
submission refused before run creation. Every available original launcher,
wrapper, runner and monitor result and actual host exit is verified. Six exit0; two baseline guards1, one identity
refusal1 and one report refusal2 remain unchanged. The lifecycle owner stops
the exact QEMU guest successfully. Disk/UEFI/temporary SSH files are retired:
2275385344 allocated file bytes recovered. This was explicit cleanup; #493
automatic retirement is still separate. The earlier11.8MB compiled candidate
is retained only for immediately queued remaining qualification.

Final guest state: same ES/boot, broker idle, no browser or configured remote.
No owner device, save, account or personal cloud operation occurred.
Remaining before pin promotion: success/failure branches including actual
browser-open failure, broader standard-profile source-bound UI evidence
(1280×800/French as required), and separate physical corroboration. The
original severe handheld slowdown is not claimed resolved by this VM result.
Fixtures are archived original commands, not replay instructions: this owner,
its ports10604/5993 and all VM paths are retired. Use a fresh measured owner.

# #603 retained-receipt gap verification

Read-only follow-up to Claude G-06, G-14–20, G-25–27. Frozen distribution source
is `cdd92f10605517e789e09d13b6f4ba68573c2617`. No test, VM, compiler, source
collector, provider call, firmware extraction, product edit or shared-record edit
occurred. This is routine local source/receipt verification, not a new external
review or a claim that #603 is complete. The later077197 ZeroTier change remains
outside the frozen audit. Original failures and honest limits remain unchanged.

`evidence-index.json` gives exact original path/member, full digest and byte count
for every retained original. Source copies preserve line numbering. Derived
projections identify their full input digest and explicitly say they are derived.
The retained Python file only reads named Git objects, compact selected members
and already-held metadata; it does not execute any supplied source/helper.

## G-06 — archive annotation and Steam exemption

`sm/verify-additions.py:84` is indeed an annotation. The independent archive
measurement is `sm/archive-reader-result.json:3–5,31–35,94–96`, original
`/tmp/pix-m7-audit603-20261015/extracted/checksum/archive-reader/result.json`,
SHA256 `d08a01330ad3e4923b2d979d3c02b17e7766e8aa24cc30a844f0932f712aa19c`.
It binds archive64034fb076ea0bb858beaa2f29dbef635e97d29f3e3d32c13bce61bd4af4cff7
to signed member8c27a70961476b327071ada2fd9b9c55dd2dcdc913eff3d33f2576133d7e398c.

The actual installed row is `sm/affected-products-staged.json:111–123`, SHA256
`30a83282534388d66e294414c498e3ae0669636ca5cb802daa2c7bc66fe89849`:
`/usr/bin/steam` resolves through `../lib/steam/bin_steam.sh`,8303bytes,
digest`a56d881670d9585c4ca946d5c4c1e5463039d8902976be10a74a38161158f394`.
The frozen Steam package recipe lines14–26 extracts the Debian launcher package,
edits `usr/lib/steam/bin_steam.sh` and copies its bin/lib trees. This gives the
specific script-wrapper/source explanation for the reader exception. The compact
row does not retain header bytes, so this report does **not** claim a fresh
measured shebang or ELF-header read. No archive/image payload was opened. The
exception itself does not establish a product defect.

## G-14 — historical tool identity and current test transfer

Exact Git ancestry command `merge-base --is-ancestor 1a026648442321609b2288c2c9c06803817f9df2 cdd92f10605517e789e09d13b6f4ba68573c2617`
returned0. Ancestry alone does not equate helper bytes:

- At1a026648, `tools/last-good-scripts-test` SHA256 is
  `8f9dc9107a30aa6e299f1e1dd542b1dfd79a811920033ea5afbe25227d5f9ae2`.
- The historical1378-pass receipt records retained helper
  `ebd9a4669d8e96d6a18a874f95058911ed2a7b38329a5236891ef3bdd6894d20`.
- Atcdd92, the helper is
  `b8495055873e4ce506fa0a5c72ed62bbfe97f3dab5823d161078742400f75066`.

The receipt's `source` field names the **product checkout**: exact original
`baseline/evidence/qa20-first-run.py:5–7,33–38` separately checks its tool
`source-manifest.json`, asserts product HEAD1a026648 and sets
`LAST_GOOD_SOURCE_ROOT` to that checkout. It runs the helper from its own cwd.
Thus the historical SHA mismatch is real and expected from separate test-tool
custody; do not claim that receipt executed the Git helper at1a026648 orcdd92.

There is a stronger current binding: the exact difference between retained
ebd9 and frozencdd92 b849 is only the PL-016 selector correction at6265–6273,
retained in `baseline/original-to-frozen.diff`; it matches the originally
retained `baseline/last-good-scripts-test.diff` change. The actual continuation
config lines200–205 binds `harness/tools/last-good-scripts-test` to b849. Its
original result lines555–567 reports scripts PASS521s; original host-exits
lines2–13 records all seven channels0 and owners gone. This is evidence for the
corrected helper in the continuation's declared fac608ff product scope, not a
new claim that the1378-pass historical result ran on cdd92 product bytes.

## G-15 — executed continuation source/config

The actual owner is `/workspace/tmp/pix-m7-final-baseline-20261014-03`;
run`20261015T000858Z-720211a2`. Its config, run.py and result are byte-equal to
the retained compact copies (comparison in `baseline/binding-check.json`).
`baseline/config.json` SHA256
`d70c710f57aa2006dfe64e85caa370591921865e4c23b0ae4770e50b9e499e73`, lines200–205,
binds run.py`5ed44531cbb111b9fca34262e0e50538d3ef1f6379a4bf532d296a1a5638572e`
and the exact current helper above. `run.py:149` validates the complete code map.
Actual `baseline/result.json` SHA256
`2ba4ac3276af0ed6db02b0cc13a4b8b620d10679ea3718790a0e2f380d98676a`
records rc0, scripts/SFTP/S3 PASS and cleanup empty. The docstring and prepared
config's UNRUN label are immutable preparation-time statements; execution is
established by these originals, not by editing the preparation labels.

## G-16 — f863 build-reporting caveat

Frozen cdd92 `docs/releases/next-candidate-work.md` is retained as
`frozen/readiness.md`, SHA256
`d26c1e005d817a43cedab32a4d9af1ad54df0b08acfc10c76e03067faec9e675`.
Lines175–184 say artifact and installed clean/retained qualification passed,
while preserving the original reporting failure and unknown launcher wait.
Lines186–196 explicitly record all four canonical build stages and original
command/monitor/runner0, then the prematurely-created wrapper receipt,
exclusive-write failure, absent launcher-result and unknown final launcher wait.
The source states that recovery must preserve the failure before independent
artifact readback and VM proofs; it does not convert the producer qualification
flag to true. Attach this caveat wherever AC-37/49/51 say "final installed".
No firmware defect or successful producer-submission receipt follows from it.

## G-17 — SM preparation stamp versus actual launch

Original owner `/workspace/tmp/pix-m7-sm8550-refresh-20261015-02/inputs.json`
is1,431,974bytes, SHA256
`2d57e84b4fe4a8d10232a15a85a65c46a65d595eb69c635ed9e845493140762d`.
Original lines5,9,25,28 bind fresh root-supplied build identity,
`build_timestamp=20261015T075604Z`, source9aa7 and
`frozen_at=2026-10-15T07:56:24.747684+00:00`. These exact fields are projected
without rewriting the original under `sm/inputs-projection.json`.
`sm/preparation.json` binds that exact input SHA. `sm/prepare-owner.py:30–31,66`
accepts a supplied actual timestamp less than24h old; it does not require launch
time equality. `sm/build.py:3,18–19` consumes the same inputs and exports
`BUILD_TIMESTAMP=j['build_timestamp']` to the canonical build.

Original `sm/launcher-submission.json` SHA256
`6b38b1895bc323a8200ee040b5d1a8b6dd8e5c943b4865c5aff8acb01020f35b`
records actual submission08:18:27.231408. `sm/acceptance.json:23,50–51` links
the075604 image to producer run081827Z-07dceee9 and preserves its combined exit1.
The22-minute interval is preparation-to-launch time, not unexplained image
substitution. No image was restamped and no successful producer exit is inferred.

## G-18 — old/current Steam heredoc identity

Git07a16c4d2f3cb923e171c0f6b8dd43aafc4282b2 holds the exact old67,550-byte
installer9e1ce7b52279c9d057eb3acf7caa4d03843871b2fec5ccc15b06287b4de67402;
the earlier source packet's735226dc commit has the same bytes. Frozen cdd92
holds124,399-byte1694f7a9b892988a67a3445c8f51031c5a5c8be02628b0be8031f233b512ad3b.
Both complete source files and newline-preserving block calculations are
retained. Body spans exclude opening/closing heredoc delimiter lines.

| Block | Old body lines | Current body lines | Body bytes | SHA256, equal in both |
|---|---|---|---:|---|
| ROOT |21–199|21–199|7033|`0a8d0bee1678099e9b45de8dcd97b36267ff7ee289d0d9f8d0b17b8192d9b332`|
| RUNTIME |781–1149|781–1149|16606|`1c6edbf421b7037124671d48361716167ec933934406c10aa4ca02c3082eefae`|
| PROTON_VARIANT |1194–1481|2378–2665|12682|`18d2bed395aa8c5242964ecf513d0d6a202ad139db5591c5c82b1a798460da2f`|
| FEX, additional check |254–755|254–755|22170|`2381da57a79e9c2b07238f71e2cfd3b57bf106a0ba3b43ad0471700bef918b49`|

The component receipt helper hashes refer to adapted synthetic fixture helpers,
not these raw heredoc bytes; do not conflate them. Equal body identity supports
transfer of the retained enumerated component controls, not a whole-installer,
real-download, real-FEX-budget or native-ARM execution claim.

## G-19/G-27 — actual claims and pixel diagnosis; repository custody

Frozen cdd92 `tools/vm-walks/claims.txt` is byte-equal to the actual continuation
`claims.composed.txt`:57,101bytes, SHA256
`7764b6824a8489b1e22d793ac8adcbf90b559d3235e9d65189c55e618101cf5e`.
Both exact texts are retained. All391 noncomment claim rows name baseline
`d72084ccad`; **zero** use wildcard heads.348 entries cite#578; the added section
begins at78 and exact rectangles at89. Frozen `tools/vm-qa:525` passes this
repository `tools/vm-walks/claims.txt` to frame-diff. Thus the passing composed
file is durably in the frozen Git source and does not survive baseline changes
through wildcard heads.391 claim rows and389 matched/claimed result regions are
different counts, not a contradiction.

The original published `docs/qa-logs/2026-10-15-frame-claims/pixel-inventory.json`
is3,588,002bytes, SHA256
`6827c253d8f4d2ec649a2baea13fda8aa4e07daa0e937b1d4ea959df37a16517`.
`frames/pixel-summary.json` retains all78 frame-pair hashes and diagnostic scalar
rows; the full original also retains row_spans.65 rows have residual pixels,
total12,786,825; all78 have zero outside_carousel_change_support.
For example original lines5–20 bind back-up-page/01-cloud-hub.png baseline
ef9aa00e… and current2407ad31…,201,035 residual pixels, zero outside support.
`proposed-578-background-regions.json` contains65 screens/348 rectangles.
Exact full claims text and scalar rows now supply the missing packet context.

These remain original diagnostic data and actual continuation results, not a
new pixel comparison or a claim of reviewing every frame. A rectangle still
accepts any change inside its bounds. `frames/review.txt:49–55` lists its actual
reviewed sample and explicitly disclaims all78-pair visual review; the accepted
root representative review remains separate. No comparator-semantic limitation
is erased by the custody check.

## G-20 — current mechanical pkgcheck, historical status unchanged

`pkgcheck/invocation.json:2–17` gives actual command, cwd, timestamps,
original_exit0, frozen sourcecdd92, recipe6b07c262b11e8cc3fd45e8097b7fdb06a1f612cb31008daafdc3ecf68f892b3c,
tooldea8addbc2a0a3c3d70da227d2be27f705e7d813ee129d0e43a5781215c04e18,
and stdout/stderr hashes. Exact frozen recipe/tool copies are included. Current
mechanical lint is verified by the retained invocation; historical
root_reported_status is still unrecovered. Nothing here invents that exit.

## G-25 — six runtime kill retries

The exact compact archive remains
`docs/qa-logs/2026-10-13-library-vm/results/steam-results/compact-receipts.tar.gz`,
SHA256`74617b668eb42e792672be170eb305780db597d5c04d4133739ba4b08f1feaf2`.
Selected original `runtime/tmp/cases/<case>/{before,after-first,after}.json`
and retry.log are retained under `runtime-recovery/`, with each full hash in
the evidence index. No fixture was executed.

For staging/old-renamed/new-renamed/first-link/second-link, before and after
dictionaries match exactly, including file bytes/modes and link targets. For
committed, after-first and after match exactly, preserving the committed tree.
Every retry.log lines1–4 records mocked curl then wget, injected wget exit9,
"Steam runtime replacement failed", and OWNER_EXIT1. None has "Runtime recovery
needs attention". The intentionally failing **next download** is therefore
distinguishable from a recovery failure using the original log and manifest
channels. The additionally retained recovery-failure/cleanup-failure cases have
the same intended restored-old/preserved-committed retry outcomes.

Disposition: missing packet evidence supplied for rollback/recovery correctness;
the six retry exits remain1. These cases do not prove a succeeding replacement
download after interruption, and no such stronger claim is made.

## G-26 — Wi-Fi observer exits

`wifi/guest-wifi-observer.py` is exact f895b41eabc7f22d764b0ba1856ef5c873eb71c2b8d2dafd3c50fe14aa9636e3;
`guest_helpers.py` is89a1c39a8b88e87ad4561014d0f32e5371787fe1a5aacf7b5147d6d42a99b9aa.
Observer line126 requires successful `prctl(36,1,...)` (child subreaper),
135–139 records adopted group wait statuses when available, and178–188 retains
frontend status, reaping, exact-identity absence, no later backend and joined
worker checks. This refutes the suggestion that no subreaper was installed.

The clean original result155ad890373795aea8669eeab153bedf7e1e3585e5cf08baf56edd96e8a1e741
still records reaped[] at78; neither before-cleanup nor stdout/stderr supplies
individual exit statuses for2510/2511. Retained result48694a7ba66357d2a8de31cecd525ac4978d67eeccad6d2b3fa685cd07af6a4c
records one adopted-9 exit. Do not infer the missing clean statuses from empty
census. Both retain driver0, bounded group stop, no identities/survivors and no
forced cleanup. Preserve AC-49 as clean shutdown/cleanup proof and narrow any
"all individual worker exit statuses recorded" wording. The missing wait-status
receipt is a verification limit, not evidence of a surviving worker/product bug.

## Supplemental H700 applicability boundary

Current077197 H700 owner installed-inclusion.json is retained separately,
SHA256`8536dbe840425b880fe1cb152e93f5b6902921d75b92dbd7c8d35353bac89463`,17,964bytes.
It records selected positive hashes, ES/source/build identity and ARM counts;
it contains no es_systems.cfg row or explicit Steam/GameCube/Dolphin absence
assertion. The compact currentH700 member index has no retained es_systems.cfg.
This particular installed-inclusion receipt does not prove those absences.
The frozen recipe exclusions establish source selection only; no firmware
payload inspection was performed here to strengthen that boundary.

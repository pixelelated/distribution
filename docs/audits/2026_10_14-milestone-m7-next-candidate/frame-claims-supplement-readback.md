# Supplemental independent readback — retained frame comparison #591

Read 2026-10-15 after the Phase 4.6 blind packet was sealed. This note does not amend that packet or retroactively convert the original baseline frame-diff failure into a success.

## Exact original records

Archive: `docs/qa-logs/2026-10-15-frame-claims/original-packet.tar.gz`, SHA256 `6c463ab9cce5defc51a2dd5a76d75a3b42328cf4505ca8b9c5339f47ca032588`.

| Member | SHA256 |
| --- | --- |
| packet/frame-diff-591.patch | 7604b420659af885d3ae185786433433adede168352f160c605e7b771a09826d |
| packet/claim-controls.py | 96631be5bee6881a8dd83bc8e0c60f258fc276586c87b1027c20bfe39458de79 |
| packet/claims.composed.txt | 7764b6824a8489b1e22d793ac8adcbf90b559d3235e9d65189c55e618101cf5e |
| packet/continuation01.md | 0043e9b703fa96aa4f495e444d0ff7d05f71c24b5c83bcac57232937aea9a332 |
| packet/pixel-inventory.json | 6827c253d8f4d2ec649a2baea13fda8aa4e07daa0e937b1d4ea959df37a16517 |
| packet/execution01/inputs.json | 6e1cf4dfd5f23937c560b1d2ef1c1cd77aaa25362cb292f711d5ef6e5a573a19 |
| packet/execution01/result.json | 3e952d480fd3bda7016259d85fd79e9b6a98204cfe449a52eed6e9d24af19bc3 |
| packet/controls01/result.json | 24cff6fe52d193cec65ac4f1a73c468a2fdd0466a8fca300cc01a67ac80cd172 |
| packet/old-control01/result.json | e7fc9f9ee609cf8dadf45c302b284ea905cf3ab3c950eae23501e1165d2f835e |
| watcher/runner-result.json | f256c461dc1e616861e4e1432bd2762559d148113ddf89bf3de5998b8508e44f |

Read the complete checker patch and control source, original per-control results and stage commands, comparison report header/tail and selected rows, and the inventory schema and two exact selected pair identities. Did not rerun the checker, fixture, VM, or source preparation.

## Source/control assessment

The patch applies live, screen-matching claims to each changed pixel after masks and before clustering uncovered pixels. A claimed pixel is counted once; the first matching live claim owns it. It does not use a union's bounding rectangle to cover gaps. Size mismatch remains an unconditional failure before masks/claims; missing frames, new-frame whole-claim requirement, stale-build filtering and screen filtering remain separate.

The old checker original adjacent-control child exited 1, as expected for the reproduced defect; the old-control wrapper exited 0 because it correctly expected that failure. The candidate's 20 original child statuses match the control source's expected statuses. Negative controls retain failures for connecting pixels, bounding gaps, half-open edges, stale/mixed/wrong-screen claims, new-frame partial unions, missing/size mismatch and foreground pixels outside a background claim. Positive controls cover adjacent and overlapping claims, explicit whole/new claims, masks, unchanged frames and explicit thresholds. All result error arrays are empty.

Original stage exits were 0/0/0 for old-control wrapper, candidate-controls wrapper and retained comparison, with elapsed seconds 0.0636/0.3641/11.7498 and no timeout. Original runner command/monitor/runner were 0/0/0 at `2026-10-15T00:22:49.648982+00:00`. Input record binds candidate checker `49cdaf5275dceef5ae3bfa06f71c4adb7f35a3b285abf9b1200f0323fec57330`, old checker `c8cf439f0ce3fd1a79b6addeb44a15a393e9c0324ce1830e74c6934133807265`, original masks `64c817d443a15585e194451772424e89ffcb7ad64f83aa3d2b799f0ecbb63a00`, and unchanged composed-claim/control hashes above. Result records `inputs_unchanged: true`.

The actual comparison command uses `/workspace/artifacts/rocknix-images/walk-baseline` and the original `qa-fac608ff89-webdav-a-20261014-2320/walks` under baseline owner02. Original report records 78 screens, 7 masks, 391 live claims, zero stale claims, and concludes 389 claimed regions, zero unclaimed, zero missing. The earlier 65-unclaimed original failure remains original evidence, and this is a later corrected-checker/explicit-claims comparison of those retained frames.

## Direct visual sample

Viewed four complete original PNGs, each 1280×800, copied read-only to private `/tmp/m7-audit-590-frame-samples/` from the two exact command input directories. Their hashes match the original pixel inventory:

| Screen | Baseline SHA256 | fac SHA256 |
| --- | --- | --- |
| back-up-page/01-cloud-hub.png | ef9aa00e4b21eee76f6a70e0457fe7cb23278d52771923bdd35bfa48cb432d98 | 2407ad318213837e373fa7fca2a4acb22f82c75d3e8bf692ecdaee84ec52b3c3 |
| manager-fbn/01-0-carousel.png | 6efc5708fa27bfaaca5886cf37e84b5dd6a1cddf16da595bee59398f8c228b36 | 3278e6a995ad7d4f96359f057c913c8ca37d49bb51896cc24197f06b78457f88 |

The hub has the same centered CLOUD modal, backup/restore rows and bottom prompts; its exposed left/top background shifts with the carousel. The FBNeo frame retains the logo and help prompts while the left backdrop shows the introduced star/blue car. Clock differences are visible and covered by the pre-existing clock mask. This sample supports the recorded backdrop explanation. The inventory's overlay-fit calculations and source worker's review are diagnostic evidence, not substitutes for visual inspection of all 78 pairs; this auditor has not newly inspected every pair.

## Disposition

Accept the original corrected comparison and focused checker controls within the exact frozen fac/3178 retained-frame scope. No new source finding. This independently resolves the frame-checker follow-up's original-outcome uncertainty but does not qualify a new image, native gameplay/save behavior, public docs, or the still-pending external review. AC020 remains PARTIAL for broader final qualification. Scorecard unchanged: 81 PASS, 15 PARTIAL, 16 SKIP, 2 FAIL, 1 UNTESTABLE. Include this later readback in the refutation stage without modifying the sealed blind prompt.

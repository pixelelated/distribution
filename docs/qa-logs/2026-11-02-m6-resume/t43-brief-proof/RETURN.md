# T43 #690 stranger proof: one record correction required

Reader: Codex (GPT-6), actual harness session 01a19d12-1c5f-7022-8053-102f6a94b7fe, m6-t2-es-launch, wN:p5. Return to m6-coordinator, wN:p2. I did not author the brief. This is bounded brief/input verification, not T43 execution, planning, dispatch or acceptance.

Frozen candidate and helper remained byte-identical:

- patches-unshipped.md: `9cbdc0a2ceae4678bab380d880ae7826c472b00424ec4f61a08d7498de465d38`
- t43-brief-inputs.py: `5e8f14567bf8cb6e0916b7a7d3cc67f9dfd899b38c9d38ff6a2d37a3ff88191f`
- Source baseline `afdec2bf8b88135befcb7ec56efb3a7ea327bd73`; tree `1325b129c1a506671cc06fc80c22fa11f1231a00`.
- P1 `2174265e9cc1b248c0fbe27fa101875984d46d6b`; tree `cfda7cb901a9e628af5d5839ec0302cc7a91244a`.

## Concrete correction

The brief §2 labels the retained members.tsv SHA256 as `ccbbe1543349e51f56545afc3e96aadc3fc3e965e19b1fdb18731ee809cc083e`. That is the decoded manifest identity, not the committed file identity. Immutable Git read at afdec returns 83,282 bytes, SHA256 **`d89d6fe612587635c2bb6d1101362242f03b9f0c3c391015f5344c2357eb1c49`**. The committed TSV contains exactly one literal `\u002d` escape in the SM6115 `0034-serial-qcom-geni-mask\u002dirq-during-system-suspend.patch` path. Decoding that one escape yields 83,277 bytes and exactly the quoted `ccbbe...` hash. Direct raw path-set comparison fails on that one key; lossless decoding makes all 432 rows match. No source drift exists.

Correct the brief to name both committed-byte and decoded-manifest hashes and the exact lossless path comparison. Do not change the accepted source or historical manifest. Evidence: manifest-hash-discrepancy.json, manifest-path-discrepancy.json, manifest-normalization.json and reconciliation.json. The initial literal-hash and raw-key assertion failures are retained in observed-failures.txt. No candidate bytes were edited here.

## Bounded results

- Literal membership block ran unchanged in **one shell invocation**, inside a private repository with no checkout and private HEAD pinned to afdec. Source and seed outputs are byte-identical, including summaries. Receipt: receipts/membership-literal-01.json plus raw stdout/stderr; exact block: membership-literal.sh. Output directory: `/tmp/m6-t43-inputs.tfsJLH/`.
- PASS: 432 paths / 328,516 logical lines / 328,512 LF bytes / 10,690,267 literal blob bytes; modes 428×100644, 2×100755, 2×120000; 346 Linux patches / 12 configs / 74 other patches; 72 directories / 31 prefix groups / 28 overlapping consumer combinations / 21 target-architecture configurations. Path-list SHA256 `8ec78172f80d28d28117eaf1efefe2c769ea58d07a57c3a16616b595fb429912`. Fork-written set and selected net diff from c445081a59518f37d9776e5412dd7b14910696f7 are empty. All retained manifest fields reconcile after the specified escape decoding.
- PASS: all 31 recipe hashes, modes/blobs, numbered pin/selector excerpts and P1-derived owners; recipes/member rows T25 12/25, T8 10/36, T30 3/3, T23 5/10, T11 1/358. Two T43 MangoHud links retain their exact literal targets and 34/37-line referents; the separate T42 SM8550 link shares the battery referent without moving ownership.
- PASS: **49 meaningful refusal controls**: all six selector/input byte drifts; missing selector; selected config, link and referent byte/mode/missing mutations; byte drift in EACH of 31 recipes; recipe mode/missing mutations. Every case returned nonzero with its expected diagnostic and created no output directory. Mutations used private Git objects only; private refs/HEAD stayed fixed. Referent mutations correctly stop at the earlier selected-source identity guard because both referents are members; this does not claim isolated coverage of the later redundant referent assertion.
- Static interface/source reads confirm the build's architecture mapping, recipe precedence, selected patch patterns, actual patch/git-apply branches, RK3588 reset, all kernel conditional pins, RK3566 source-loader versus wrapper distinction, module pin, libmali/wlroots conditions, ATF branch, config writers and fixed upstream 7.2.6 selector versus 7.2.11 source. Read-only retained context hashes reconcile; exact T41 e481 and T42 4cf8 contexts were read, not replayed. See source-seams.json, additional-seam-hashes.json, accepted-seams.json, reconciliation.json and read-commands.json.
- Interface readback: `tools/lint-audit-artifacts FOLDER --phase pre-issue` prints `PASS pre-issue artifacts (does not certify resolution)`; normal resolution is default, with optional `--issue AUDIT_ISSUE --repo pixelelated/distribution`. Local epic support requires depth `local`, reviewers[], tier_exception D-WORKFLOW-184, nonempty reason and actual primary identity fields. `tools/box-check --issue N` and work-log-index --check/--write interfaces exist. These final checks were inspected, not executed. Only the bounded helper and private negative controls executed; helper --help also returned 0.
- Full #690 body and its comment were read, plus #1054 and frozen plan/order/rules. Existing generated criteria are intentionally pending coordinator replacement. Questions, output stages, unknown-input handling, D222 promotion, no replay, source-only limits and coordinator D/H/acceptance boundaries are consistent. Future C/D tables, application proof, Local-lint fixtures and final gates are future lane obligations, not missing stranger-proof artifacts.

## Reproducible commands and boundaries

All source/record subprocesses inherited CPUs 8–23; no runtime slot was allocated. Recorded commands and scripts are in this packet. For read-only reproduction:

```sh
taskset -c 8-23 git -C /workspace/repos/pixelelated/distribution.worktrees/m6-es-launch-path-649 show afdec2bf8b88135befcb7ec56efb3a7ea327bd73:docs/qa-logs/2026-11-02-m6-resume/t43-preparation/members.tsv
taskset -c 8-23 python3 -I /tmp/m6-t43-stranger-xb328xv5/reconcile.py
```

The literal shell argv/cwd, timestamps, exit and output hashes are in receipts/membership-literal-01.json. refusal-controls.py records each private mutation commit, exact argv, diagnostic, elapsed time and raw-output hashes in refusal-results.json and receipts/. Its rerun is not needed for this result. SHA256SUMS binds the packet excluding itself and the private Git object store; mutation object identities and per-command receipts bind that store.

No audit producer/application, config, archive, extraction/export, build, guest, fetch, provider, device/cloud, host-ledger, tracker, repository or shared-kit write occurred. The historical T2 checkout is clean at 7041b0d710363ddac7ae1b047ebae3e182548631. All four frozen T41 tool hashes still match the prior return; preservation.json records them. Private scratch is about 2.6 MB, including approximately 1.66 MB of private Git objects, with the separate small literal-helper output directory. Coordinator retains brief/version/criteria, planning, dispatch and final acceptance. Bounded result complete; stop.

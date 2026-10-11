# Next pixelelated candidate — working list

Recorded 2026-10-11 under #533, following the maintainer's request to document
the list and begin #531. The [M7 milestone body](https://github.com/pixelelated/distribution/milestone/7)
is the authoritative current order; this is a dated working reference, not a
second release queue. No new candidate is built or designated by this list.

| Order | Work | Evidence needed before advancing |
| --- | --- | --- |
| 1 | #531: USB revision independent of the OS version | Actual networking/MTP preparation controls on host and guest, old-source failure, preserved descriptor identities; then installed bytes on the combined image. Source controls pass: 72/72 on host and guest, old-source failure retained. The combined-image check remains. |
| 2 | #532: thin rolling RC/release naming | D-WORKFLOW-159 selected: rc.N then release, explicit never-reused counter per frozen set, internal dev default, new qualified assembly for release. Host57 controls pass; shared #530 installed-image proof remains. |
| 3 | #533: reconcile remaining issue criteria | Reconciled in [the scope table](next-candidate-scope.md): 18 M7 issues, four bugs. Retire migration; preserve #349/#350 exact-frame gaps and publication requirements. #528 firmware dispositions precede final freeze. |
| 4 | #535/#536/#537/#538/#539: Dropbox pointer/navigation and visible connection lifecycle; #528: component decisions that affect firmware | Implement #535 open-network selection with protected/unknown/saved regression checks; resolve #536 with credential-free VM input/navigation proof and #537 with explicit add/renew/edit/remove preservation and exact-source flow/frame proof. In parallel resolve #528 source/licence/vendor dispositions before freezing inputs; prepare the updated component-to-source map. |
| 5 | #344/#529/#530/#531: combined engineering image | Recheck #493 build/QA headroom, freeze one input set, actively supervised build, installed fixes/identity, clean/public ROCKNIX and retained-storage tests, affected flow frames and applicable delta review. |
| 6 | #528/#265/#344/#359: release completion | Independent retrieval/hash verification and off-host custody, adoption/recovery/support/source/branding notes, applicable hardware/attachment gates and named publication authority. |

#529's startup fix and #530's build identity are integrated; their next-image
criteria are open. Earlier accepted VM/cloud/audit/device evidence is retained
with its source scope and is not replayed merely to resume. No automatic cloud
move/follow returns. Names do not confer qualification, and an image needed for
QA may be built before its installed-image criteria can pass.

Website #511, broad observability #432, disconnected notifications #395,
active-name cleanup #509 and personal cleanup/redundancy #516/#518 remain
separate. Active supervision and prompt delivery of long-job results remain
required now. Previously approved device transfers/reboots have completed;
owner devices are in use. #536 consumed one later explicit screenshot approval;
its frame/aggregate navigation-log observation is recorded separately. No input,
sign-in submission or configuration change was performed. #535 open Wi-Fi is now part of M7.P5 under the latest implementation approval.

## 2026-10-11 audit delta

The approved Fable 5.1/xhigh refutation completed and its identity/provenance
verified. #540 owns seven findings: three High, one Medium, three Low. All seven
repairs pass focused guest controls, 1,373 full-regression PASS controls,
108 WebDAV + 108 SFTP checks, 26 connection transactions and 15 whole-script
refusals. Final54 builds; matrix55 supplies 16 reviewed affected EN/FR small/large
frames. Earlier rejected fixtures/layouts remain recorded with their own source.
Distribution `bc2dceb406` is integrated on next and pins published ES
`c8dc72cf9e`. All seven #540 findings are resolved. #528 and the combined-image
clean/retained qualification gates remain next. No new RC designation or
owner-device action follows from source-overlay qualification.

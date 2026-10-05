# GENERIC_X64 Pixman fallback qualification

The installed fallback resolves the reproduced software-VM stale/partial
browser display on clean and actual ROCKNIX RC2-upgraded guests. Accelerated
virgl remains selected and passes the same browser comparison. This qualifies
the scoped fix in #447; it is not a release-candidate or device-ready claim.

Source: `d6e8390c93bed87efe2dcc23cd402a271cacd1c7`.
Manifest: `0b24bfcd0d7dad134872b88ed6a2955ddaf9cdf9d55f8a25c17fa5e2de36ad51`.
Immutable bundle: `1c69bcf5ab6ebdc3e893a6a989545ac7a23359f0e07baef4e9c2beaca94c52b4`.
Image: `1cc9c22d63286fbe5d6bdf7f1826d5d977798a472c7f87f8546c1d272a6492bb`.
Update: `a9fa66dc63fdb42678a98c42b3abbe84d20f623eb922501bd36f0aa50dfdc1a3`.

| Evidence | Verified outcome |
| --- | --- |
| qa-14 | All15 default suites,26 actualRC2 upgrade checks;21expected frame regions, zero unclaimed/missing; installed renderer and15identity frames. |
| boot-qualification-05 | Four clean/upgraded software boots at640/1280 match1.0;12negative controls reject; allfour intended wordmarks directly reviewed. |
| signin-ui-14/15/16 | Clean software, actual-upgraded software andvirgl each pass40checks and15reviewedframes. Native/HMP/VNC agree exactly at0/5/15seconds, without forced resize/input. |
| memory-12 | Original10virgl/10software/50software+sync cycles pass strict1024KiBVmSize/2048KiBRSS growth limits;55distinct completed sync stamps. Both renderer exit/timing suites pass. |
| ui-14 | All70 English/French menu/Tools frames reviewed,12unchanged ES lifetimes and installed Pixman at640/1280. |
| signin-1g-13 | Actual1GiB baseline load/responsiveness, noOOM; peak271416KiB. |
| signin-provider1g-05 | Actual1GiB publicDropbox load/responsiveness, noOOM; peak395676KiB. |

All successful owners have matching durable results and actual process cleanup.
Original failed owners remain failed. Full source/cache/build/image custody is
retained here; ../2026-10-05-generic-x64-pixman retains44selector controls.

Only the GENERIC_X64 wrapper/service drop-in and VM README changed from
replacement09. Shared handheld startup and package versions are unchanged.
The actual old ROCKNIX RC2 also reproduces this on today's software host;
the rename is not necessary to trigger it. Exact defective component remains
unknown. Historical comparison records stay under replacement09.

Already written: the selector writes no persistent setting. Existing /storage
Sway configuration remains readable; selection is recomputed each startup.
Clean and retained-storage installed behavior is proven by the records above.

Limits: public provider pages and the synthetic finishing marker do not prove
authenticated trust. Fast game-to-game timing samples have no new sync stamp,
so they do not prove launching during active sync. Performance smoke samples
are not distributions. Remaining P3 criteria/accounts and approved P4 review
precede H700 arm/aarch64 and named physical/P5 gates. Refs #447, #383, #409.

## Build and content custody

Cache comparison and 2,526,399 independent regular files pass. The quiet
checksum phase triggered an inactivity warning; actual I/O proved continued
progress. Build01 refused exhausted swap before compilation. Its caller's
missing fail-fast allowed submission after an external refusal; the inner
preflight guard held. Missing build.start/run.path/inner.rc remain missing
evidence. The installed guarded helper reclaimed swap; fresh build02 passed
all 642 package steps and installed-byte checks.

Build02 completed at 19:26:30 with all four results zero; actual047d1c at
19:26:43 confirms all four owner PIDs absent and the observed container removed.
Image12 completed at 19:27:17 with all four results zero; actuald62687 at
19:27:23 confirms all four owner PIDs absent. Raw GPT image SYSTEM and update
tar SYSTEM both hash to
`5bf4888cfcb29798887f2daab0858981a969e8d3eb71797c0a0a18ffde42cf32`.
These remain build/content proofs; the table above records separate runtime
qualification. Original replacement09 remains intact. VM-first: yes.

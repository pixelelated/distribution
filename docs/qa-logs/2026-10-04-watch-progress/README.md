# Overall build progress — #412

The active cold build's aggregate log contained flushed Ninja counters.
The old watcher selected the last generic numeric counter and briefly
reported 130/130 as overall progress. This did not mark the build complete:
completion still requires its result file. The original watcher remains
active, unchanged, on frozen b137d8c373.

`watch-job --build-progress` reads only anchored, ANSI-stripped pkgbuilder
DONE/FAIL build/install/unpack lines for the overall count. Package activity
keeps the generic/custom pattern. `watch-build` enables this for native/Docker
builds; explicit QA activity-directory mode retains generic progress.
Detached observation preserves the option.

Can this be done on the VM? Yes: isolated host log/process fixtures exercise
the actual shared runner without a guest or build. Initial control before
the change:7 PASS/5 FAIL. Final identical 13-check suite: corrected13/0,
frozen old tools7/6 (the added checks include option forwarding and separate
package activity). Existing lifecycle suite32/0; current full routing
fixture35/0. No product image behavior is claimed by these tests.

The historical routing fixture failed after20 passing assertions because its
simulated Docker lookup expected the retired registry namespace (#413).
`routing.log` retains that failure. `test-watch-build.py` is a current copy
with the lookup bound to the reviewed Makefile's exact image/digest;
`routing-current.log` retains all35 original assertions passing. The original
historical fixture is unchanged. This test simulates Docker, and does not
claim a new real-container launch or a change to image custody.

`live-replay.status` is a **one-shot read-only replay** of the active aggregate
log, with a synthetic replay result file. Its finished/rc0 describes that
replay, not the cold build. It reads the actual structured count627/642.
The real build remains running under its own result/status files.

# Current proxy and coupled CHD reader qualification

Owners: #361 and #451; delivery #383. Exact new upstream parent
3036478f2b2d22db451396a48f44feee94e8462f pins libchdr
607694ca0812edfc9cc2030c64634fc2393668de and unchanged rcheevos
1433173220a7eaede6a9ed7a18e94117be1821e0. `archives.json` records verified
downloads and full hashes; `coupled-pins.json` is the parent tree readback.

All15 patches apply with zero fuzz. All113 Linux Python source/test files
match the actual replacement10 consumed tree. The earlier comparison against
patched-v6 correctly failed because that review copy predates #436's removal
of the unused RASTERATOPS identity; it is preserved as a failed comparison.
The current identity behavior remains ROCKNIX→pixelelated only.

Three libchdr commits change C declaration ordering and the legacy CHD metadata
formatter. The constant format holds four signed32-bit integers: at most68
bytes including NUL in the unchanged256-byte buffer. `source-review.json`
records the bound; no input string is interpolated. The native build uses
the actual package make_target function with the selected new libchdr and
unchanged rcheevos sources. This is host compilation, not target-image proof.

Original host01 passed815 Linux tests with the new native library, then
failed the fork predecessor fixture: current7252fc removed its old list API.
Actual diagnostic stderr proves AttributeError. All four original rc1 results
and original helper source are preserved in `host01-failed/`; actual4f8c50
at22:08:07 confirms its four processes absent. No result is transferred.

#451 updates only the fixture to use the predecessor's streaming API when
available, retaining the historical list path and all preservation assertions.
Subprocess stderr now accompanies a fixture failure. Fresh host02 rebuilds a
separate native library, passes815 Linux tests with no native skips, and
passes all11 integration checks with **each** actual7252fc and historical
865e21 predecessor. Both reopen cycles preserve exact cache rows, sign-in,
ROM/image paths and queued base/subset awards. Input hashes pass before/after.

Durable host02 result22:08:58/allfourrc0; actual4db2ce22:10:32 proves allfour
processes absent. First connected readback was22:09:51,53seconds after the
recorded completion; the launch-to-first-read interval exceeded60seconds,
so no uninterrupted60second supervision claim is made. The watcher remained
active and recorded the result. Disconnected delivery remains #395.

Both recipes pass pkgcheck. Selected package pins now match these reviewed
archives. **A fresh immutable candidate and affected installed-image proof are
still required**, as are ordinary RA-account, P4 and release gates. No player
behavior change or authenticated-account success is inferred from host tests.

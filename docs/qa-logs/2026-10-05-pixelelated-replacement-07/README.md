# M7.P3 replacement07 build and crash evidence (#383, #426, #433, #436)

Current result: build and inventory pass; initial QA fails before defaults/upgrade.
Diagnostic03 proves the System Settings abort. Replacement08 must qualify the
repair; no replacement07 RC claim. The preparation and attempt records below
are historical snapshots, followed by the confirmed diagnosis.

## Preparation snapshot

Frozen distributiona2586374b7b565965fe0c644656e22ff3c0ec317. Input manifestdcc242bbb3039559515b20ca395135af809fdb099d31b3710cf907c97c4d4e84,6547 product files/180 symlinks/200 QA files. Ten reviewed product paths differ from57cbc: upgrade-safe quiet splash policy plus current7252fc proxy integration. Native parent pins, ES/splash/font/container and24/4 concurrency are unchanged. Full local inputs remain under /workspace/tmp/pixelelated-m7-replacement-07/inputs.json; the digest binds this public receipt.

Independent cache copy actual74291 began03:19:50UTC.104071339531 bytes copied; checksum/inode verification is still running at this preparation snapshot. Runner1861473/watcher1861474/command1861503 are observed. Quiet checksum workers advanced about52GB of reads from03:26:47 to03:29:57; a log-inactivity alert is not evidence that those processes stopped. No build or candidate bundle yet.

Eighteen fresh QA owners are sealed and unstarted. QA08 repeats15 defaults/actualRC2 upgrade and installed identity; boot-qualification01 adds four predeclared first-clean/actual-upgrade boots at640/1280 with original0.995 matcher/rejection controls, actual kernel digest and retained nonquiet upgraded configuration. No guest boot config or product file is edited. The proxy/subset fixtures use upstream's streaming/mapping APIs and also assert metadata backfill; existing preservation criteria remain. Predecessor04 additionally requires new boot and semantic UI acceptance. Other matrix assertions stay bound to the new manifest. Preparation does not constitute acceptance.

## Build completion and initial QA snapshot

Build-attempt02/tool68993 completed actual/inner/outer/wrapper/watcher0. All642 packages, regenerated kernel/initramfs and exact assembled payload checks pass. Actual03:41:43 runner1935790/watch1935791/command1935822 and container1237c7c67bb7 are absent. Original failed7435/allrc2 remains in failed-attempt-01; its owner-cwd mistake cannot be replayed through the new pre-mutation cwd guard. Full successful build log is in the immutable bundle and bound by its manifest; this repository retains its tail and completion hash.

Store/independent verify tool17028=0. Bundle95dbc93b666f886c35af16a5b67e81dd77fad7f667e2307efb061cabf1ffc188 has15 recorded files. Image347c9da649b795f3af48bb9c83e79d21a22a9a7301163a8b3d3c17a6d470c66d (2073510170 bytes); tare057d9c11e72c90adcaf27733ecc116ba285a6d26fc22f844b6617cb723396fe (2074368000 bytes).

Inventory05/tool30750/allrc0 verifies current source/cache and recovered rclone binary with0 errors;584 components/568 roots/526 stamps. Fourteen previously tracked licence metadata gaps remain P5; this is not publication-complete. Own processes exited03:43:49; separate QA VMs were allowed to continue.

QA08/tool38098/allrc1 failed before defaults/upgrade in the initial identity walk:04-updates.png is Favorites, not Updates. Main-menu/Information and actual payload identity pass. Original failed/stuck frames and actual03:46:04 cleanup remain. #422 owns the generic dismiss/reopen/wrap assumption. Fresh QA09 changes only that navigation to known Back/Back/up transitions;11 unstarted dependencies were rebound, originals retained. Same frozen source/bundle; no product change and no repeated failed owner. QA09 subsequently failed; its result and the corrected diagnosis follow below.

## Confirmed System Settings crash (#436), not an accepted navigation workaround

QA09/tool26670/allrc1 also failed before defaults/upgrade. Back/Back from
Information reached the PICO-8 list after a black frame, not retained Main Menu.
Original source, frames and actual03:52:31 cleanup are retained.

Diagnostic01/tool1868=125 did not launch a guest: preparation had a Python
syntax error, then the shell continued to an unexecutable outer.sh. No inner/
outer result or qa.start exists. Fresh preparation/launch calls were separated.
Diagnostic02/tool40399/allrc0 captures Back transitions and close-all/reopen.
The latter reaches Updates/manual instructions, but avoids Settings save and
does not resolve the crash. Actual04:03:02 verifies every owned process absent.

Diagnostic03/tool31827/allrc0 is successful diagnosis, NOT software acceptance.
On exact a258/c75aa3, ES1511 disappears on second Back; journal logs missing
099-freqfunctions, vector::_M_range_check on empty selection, abort/status134.
After five seconds, ES3017 is running and the screen is the PICO-8 carousel.
The black, carousel and reopened Main Menu frames were directly reviewed.
Actual04:07:53 runner2324528/watcher2324529/command2324558/guest2324581 absent;
source/bundle and backing hashes unchanged. Lifecycle logs are sanitized.

Source trace: ApiSystem::getAvailableGpuGovernors executes the unavailable
helper; the global GPU save callback unconditionally called getSelected even
with no options. OptionList::getSelected uses selected.at(0). Per-game callback
already calls it only after changed(), which returns false for no selection.
The repair therefore changes only the global callback: no selection returns
without writing the saved preference or applying an unsupported setting.
No row, label, supported selection or save behavior is changed.

ES f6f0c134212bc696f2f6a747c8d390a588f2f0ce is published on test/qa-integration,
actual39201=0 with remote hash readback. Six real callback/selection-method
controls pass; old c75 source fails with the same empty-vector exception.
Pinned-container syntax check/tool66802=0. The normal vm-qa lifetime suite
now includes this callback regression and preserves the first check's failure.
These are host/source controls; a new image must supply clean and upgraded
process-stability/menu proof. Replacement07 remains unqualified and immutable.
